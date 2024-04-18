import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import joblib
from sklearn.cluster import KMeans
import altair as alt
import plotly.express as px


with st.sidebar:
    selected_option = option_menu(
        "E-Commerce:",
        ["Informasi Dasar", "Distribusi", "Hubungan", "Komposisi dan Perbandingan", "Clustering"]
    )

st.title("Analisis Pengguna E-Commerce")

url = 'Dataset E-commerce.csv'
df = pd.read_csv(url)

if selected_option == "Informasi Dasar":
    st.write(df)
    st.header('Top 3 Kota Pengguna E-Commerce')
    st.write("3 kota dengan pengguna E-Commerce terbanyak secara berututan yakni Los Angles berjumlah 59, New York berjumlah 59, dan Chicago berjumlah 58. Dengan jumlah pengguna E-Commerce yang tinggi, Hal ini mengindikasikan bahwa E-Commerce dapat mengalokasikan pengembangan strategi pemasaran yang lebih khusus dan efektif di wilayah-wilayah ini agar memperluas jangkauan pasar dan meningkatkan penjualan.")
    top_3 = df['City'].value_counts().head(3)
    top_3_df = pd.DataFrame({
        'City': top_3.index,
        'Count': top_3.values
    })
    pink = '#2078e3'
    st.bar_chart(top_3_df.set_index('City'), color=pink)

    st.header('Kepuasan Pengguna E-Commerce')
    st.write("Mayoritas pengguna E-Commerce memberikan penilaian positif, terutama dengan rating 4.1 (34 ulasan) dan 4.5 (31 ulasan). Namun, ada juga sebagian kecil pengguna yang memberikan rating rendah, seperti 3.3 (25 ulasan). Penting bagi E-Commerce untuk terus meningkatkan kualitas layanan guna meminimalkan penilaian negatif dan mempertahankan kepuasan pelanggan.")
    top_rating = df['Average Rating'].value_counts().head(3)
    top_rating_df = pd.DataFrame({
        'Average Rating': top_rating.index,
        'Count': top_rating.values
    })
    st.bar_chart(top_rating_df.set_index('Average Rating'))

    st.header('Penggunaan Diskon E-Commerce')
    st.write("Data menunjukkan bahwa 51.9% dari total penjualan barang berasal dari pengguna yang membeli barang tanpa menggunakan diskon, sementara 48.1% berasal dari pengguna yang memanfaatkan diskon. Hal ini menunjukkan bahwa meskipun penggunaan diskon dapat mempengaruhi sebagian penjualan, penjualan tanpa diskon masih mendominasi.")
    df['Discount Applied'] = df['Discount Applied'].replace({0: 'False', 1: 'True'})
    fig = px.pie(df, names='Discount Applied', values='Items Purchased', hole=0.5)
    st.plotly_chart(fig)


elif selected_option == "Distribusi":
    st.subheader('Distribusi rating rata-rata yang diberikan pelanggan E-Commerce')
    num_bins = st.slider('Number of Bins', min_value=5, max_value=50, value=20)
    histogram = alt.Chart(df).mark_bar(color='pink', opacity=0.7, stroke='black').encode(
        alt.X('Average Rating', bin=alt.Bin(maxbins=num_bins), title='Rating Rata-Rata'),
        alt.Y('count()', title='Frequency')
    ).properties(
        width=600,
        height=400,
        title=''
    )
    st.write(histogram)
    st.subheader("Kesimpulan")
    st.write("Distribusi rating rata-rata yang diberikan oleh pelanggan E-Commerce menunjukkan bahwa sebagian besar pelanggan cenderung memberikan rating yang positif, dengan nilai rating yang paling umum berkisar di antara 4.20 hingga 4.40. Meskipun demikian, terdapat sedikit variasi dalam rating yang diberikan, dengan sebagian kecil pelanggan memberikan rating yang lebih rendah. Rentang rating rata-rata berkisar antara sekitar 3.20 hingga 4.80, dan distribusi tersebut cenderung simetris dengan sedikit kemiringan ke kanan, ini menunjukkan bahwa sebagian besar pelanggan memberikan rating yang cukup positif.")


elif selected_option == "Hubungan":
    st.subheader('Hubungan antara hari terakhir sejak pembelian dan jumlah barang yang dibeli')
    scatter_plot_alt = alt.Chart(df).mark_circle(size=60).encode(
        x='Items Purchased',
        y='Days Since Last Purchase',
        tooltip=['Days Since Last Purchase', 'Items Purchased','Total Spend']
    ).properties(
        width=800,
        height=500
    ).interactive()
    st.altair_chart(scatter_plot_alt, use_container_width=True)
    st.subheader("Kesimpulan")
    st.write("Grafik tersebut menggambarkan hubungan antara hari terakhir sejak pembelian dengan jumlah barang yang dibeli. Dari grafik tersebut, terlihat tren menurun yang menunjukkan bahwa semakin lama waktu sejak pembelian terakhir, jumlah barang yang dibeli cenderung sedikit. Artinya, pelanggan cenderung membeli lebih banyak barang dalam jangka waktu yang lebih pendek setelah pembelian terakhir mereka. Jadi, secara umum, terdapat hubungan negatif antara jumlah barang yang dibeli dan jumlah hari sejak pembelian terakhir, namun ada pengecualian yang mungkin dipengaruhi oleh faktor-faktor tertentu.")


elif selected_option == "Komposisi dan Perbandingan":
    st.subheader('Komposisi perbandingan antara gender, tipe membeship dan total spend')
    plot_type = "Bar Plot" 

    if plot_type == "Bar Plot":
        bar_plot = alt.Chart(df).mark_bar(opacity=0.7).encode(
            x=alt.X("Membership Type", title="Membership Type"),
            y=alt.Y("mean(Total Spend)", title="Average Total Spend"),
            color=alt.Color("Gender", title="Gender")
        ).properties(
            width=600,
            height=400
        )
        st.altair_chart(bar_plot, use_container_width=True)
    st.subheader("Kesimpulan")
    st.write("Grafik tersebut menyajikan komposisi perbandingan antara gender, tipe keanggotaan (membership), dan total pengeluaran. Dari grafik, dapat dilihat bahwa untuk setiap jenis keanggotaan (Bronze, Gold, dan Silver), total pengeluaran rata-rata untuk pelanggan wanita lebih tinggi daripada pelanggan pria. Secara khusus, pelanggan wanita memiliki total pengeluaran yang lebih tinggi dalam semua jenis keanggotaan dibandingkan dengan pelanggan pria. Selain itu, total pengeluaran rata-rata cenderung meningkat dengan naiknya tingkat keanggotaan dari Bronze ke Silver ke Gold, untuk kedua gender. Dengan demikian E-Commerce dapat menyesuaikan strategi pemasaran yang semakin banyak menarik pelanggan wanita dan untuk meningkatkan keterlibatan pelanggan pria dengan tetap meningkatkan pencapaian tipe membership semua gender.")


elif selected_option == "Clustering":
    st.subheader('Penampilan Hasil Kluster')
    st.title('')
    file_path = 'kmeansmodel.pkl'
    with open(file_path, 'rb') as f:
        model = joblib.load(f)
    url = 'Data Cleaned.csv'
    df1 = pd.read_csv(url)

    df_float = df1.select_dtypes(include=['float64'])
    n_clusters = model.n_clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(df_float)
    df1['Cluster'] = kmeans.labels_
    scatter_plot = alt.Chart(df1).mark_circle().encode(
        x='Days Since Last Purchase',
        y='Items Purchased',
        color='Cluster:N',
        tooltip=['Days Since Last Purchase', 'Items Purchased', 'Cluster']
    ).properties(
        width=800,
        height=500
    ).interactive()
    st.altair_chart(scatter_plot, use_container_width=True)
    st.write(df1)

    st.subheader("Masukkan data untuk prediksi kluster")
    input_Gender = st.number_input('Input Gender', min_value=0.0, value=0.00)
    input_Age = st.number_input('Input Age', min_value=0.0, value=0.00)
    input_City = st.number_input('Input City', min_value=0.0, value=0.00)
    input_MembershipType = st.number_input('Input Membership Type', min_value=0.0, value=0.00)
    input_ItemsPurchased = st.number_input('Input Items Purchased', min_value=0.0, value=0.00)
    input_AverageRating = st.number_input('Input Average Rating ', min_value=0.0, value=0.00)
    input_DiscountApplied = st.number_input('Input Discount Applied', min_value=0.0, value=0.00)
    input_DaysSinceLastPurchase = st.number_input('Input Days Since Last Purchase', min_value=0.0, value=0.00)
    input_SatisfactionLevel = st.number_input('Input Satisfaction Level', min_value=0.0, value=0.00)
    input_AgeCategory = st.number_input('Input Age Category', min_value=0.0, value=0.00)

    data = pd.DataFrame({
    'Gender': [input_Gender],
    'Age': [input_Age],
    'City': [input_City],
    'Membership Type': [input_MembershipType],
    'Items Purchased': [input_ItemsPurchased],
    'Average Rating': [input_AverageRating],
    'Discount Applied': [input_DiscountApplied ],
    'Days Since Last Purchase': [input_DaysSinceLastPurchase],
    'Satisfaction Level': [input_SatisfactionLevel],
    'Age Category': [input_AgeCategory]
    })
    st.write(data)
    submit_button = st.button('Submit')

    if submit_button:
        prediksi = model.predict(data)
        st.success(f"Hasil Prediksi Kluster : {prediksi[0]}")
