import csv
import difflib

def cevap_bul(soru):
    with open('veri.csv', 'r', encoding='utf-8') as dosya:
        csv_okuyucu = csv.reader(dosya)
        # İlk satırı başlık olarak al
        basliklar = next(csv_okuyucu)

        # Soru sütununun indeksini bul
        soru_indeks = basliklar.index('soru')

        # Cevap sütununun indeksini bul
        cevap_indeks = basliklar.index('cevap')

        # Benzerlik oranı için eşik değeri belirle
        esik_deger = 0.8

        # En yüksek benzerlik oranına sahip soru ve cevabı tutacak değişkenler
        en_yuksek_benzerlik = 0
        en_yakin_soru = None
        en_yakin_cevap = None

        # CSV dosyasını satır satır kontrol et
        for satir in csv_okuyucu:
            if satir and len(satir) > soru_indeks:
                # Soru sütunundaki metni al
                kayitli_soru = satir[soru_indeks]

                # Soru ile kayıtlı soru arasındaki benzerlik oranını hesapla
                benzerlik = difflib.SequenceMatcher(None, soru.lower(), kayitli_soru.lower()).ratio()

                # Benzerlik oranı eşik değerinden büyükse veya en yüksek benzerlik oranından büyükse
                if benzerlik > esik_deger and benzerlik > en_yuksek_benzerlik:
                    # En yüksek benzerlik oranını, en yakın soruyu ve en yakın cevabı güncelle
                    en_yuksek_benzerlik = benzerlik
                    en_yakin_soru = kayitli_soru
                    en_yakin_cevap = satir[cevap_indeks]

        # Eğer en yakın soru ve cevap bulunduysa, bunları döndür
        if en_yakin_soru and en_yakin_cevap:
            return en_yakin_soru, en_yakin_cevap

    # Eğer soruya karşılık gelen cevap bulunamazsa, kullanıcıya sor ve cevabı dosyaya ekle
    print("Hmm, bunu daha önce hiç duymadım.")
    yeni_cevap = input("Lütfen bu cümlenin yanıtı olarak nasıl bir cevap vereceğimi yazın: ")

    with open('veri.csv', 'a', newline='', encoding='utf-8') as dosya:
        csv_yazici = csv.writer(dosya)
        csv_yazici.writerow([soru, yeni_cevap])

    return soru, yeni_cevap
while True:
    # Kullanıcıdan soru al
    kullanici_sorusu = input("Lütfen bir soru girin: ")

    # Cevabı bul
    soru, cevap = cevap_bul(kullanici_sorusu)

    # Cevap varsa ekrana yazdır, yoksa bildir
    print(f"Cevap: {cevap}")
