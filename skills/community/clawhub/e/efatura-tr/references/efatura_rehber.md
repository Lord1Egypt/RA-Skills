# E-Fatura ve E-Arşiv Rehberi — Türkiye

> **Son güncelleme:** Mart 2026  
> **Kaynak:** GİB (Gelir İdaresi Başkanlığı) resmi tebliğleri  
> **URL:** https://ebelge.gib.gov.tr

---

## 1. E-Fatura Nedir?

**E-fatura**, kağıt fatura ile aynı hukuki niteliğe sahip, GİB'in belirlediği standart formatta (UBL-TR) oluşturulan, iletilen ve muhafaza edilen elektronik bir belgedir.

### Temel Özellikler
- Kağıt fatura yerine geçer, aynı hukuki güce sahiptir
- XML formatında (UBL-TR 1.2 standardı) hazırlanır
- GİB'in onaylı entegratörler veya GİB Portal üzerinden iletilir
- Alıcı ve satıcı her ikisi de e-fatura mükellefi olmalıdır
- e-imza veya e-mühür ile imzalanır

### E-Fatura Senaryoları
1. **Temel Senaryo:** Alıcının 7 gün içinde kabul/red seçeneği yoktur, fatura otomatik kabul edilir
2. **Ticari Senaryo:** Alıcı 7 iş günü içinde kabul veya iade faturası düzenleyebilir

---

## 2. E-Fatura Zorunluluk Hadleri (2026)

### Brüt Satış Hasılatı Kriteri

| Yıl | Zorunluluk Haddi | Açıklama |
|-----|-----------------|----------|
| 2024 | 3 Milyon TL | Hesap dönemi brüt satış hasılatı |
| 2025 | 4 Milyon TL | Enflasyon güncellemesi |
| 2026 | 6 Milyon TL (tahmini) | Her yıl HMB tebliğiyle güncellenir |

> ⚠️ **Önemli:** Hadler her yıl Hazine ve Maliye Bakanlığı tebliğiyle güncellenir. Güncel had için: https://ebelge.gib.gov.tr/mevzuat.html

### Sektör Bazlı Zorunluluk (Had Aranmaksızın)

Aşağıdaki sektörlerde brüt satış haddi aranmaksızın e-fatura zorunludur:

| Sektör | Kapsam |
|--------|--------|
| **Özel entegratörler** | E-fatura, e-arşiv, diğer e-belge hizmetleri verenler |
| **Aracı hizmet sağlayıcılar** | E-ticaret pazar yerleri (Trendyol, Hepsiburada vb.) |
| **Araç kiralama** | Günlük kiralama şirketleri |
| **Gübre üreticileri** | Tüm ölçekler |
| **Demir çelik ithalatçıları** | TGTC kapsamındakiler |
| **İnşaat taahhüt** | Kamu ihalesiyle iş yapanlar |
| **e-Ticaret** | Yıllık 30 Milyon TL üzeri satış yapan platformlar |

### Gönüllü Mükellefiyet
- Had altında kalan şirketler de gönüllü olarak e-fatura mükellefi olabilir
- GİB Portal üzerinden başvuru ücretsizdir

---

## 3. E-Arşiv Fatura

### E-Arşiv Nedir?
E-arşiv fatura, e-fatura mükellefi **olmayan** kişilere (nihai tüketiciler veya e-fatura dışı mükelleflere) düzenlenen elektronik faturadır.

### E-Arşiv Zorunluluğu
- Bir günde tek bir alıcıya düzenlenen faturalar toplamı **30.000 TL** (2026 için güncel haddi kontrol edin) aşarsa
- Vergi mükellefi olmayan kişilere (B2C) düzenlenen faturalar
- İnternet üzerinden mal/hizmet satışlarında

### E-Arşiv ile E-Fatura Farkı

| Özellik | E-Fatura | E-Arşiv |
|---------|----------|---------|
| Alıcı | E-fatura mükellefi şirketler | Her türlü alıcı (B2C, B2B) |
| İletim | GİB altyapısı (entegrasyon gerekli) | Herhangi bir kanal (e-posta, PDF) |
| Format | UBL-TR XML (zorunlu) | Çeşitli formatlar kabul görür |
| İmza | e-İmza / e-Mühür zorunlu | e-İmza gerekli |
| Onay süreci | GİB üzerinden | GİB'e gönderilmez, saklanır |

---

## 4. Diğer E-Belgeler

### E-İrsaliye
- Sevk irsaliyesinin elektronik karşılığı
- Malın taşınması sırasında düzenlenir
- E-fatura mükellefleri için zorunlu (belirli koşullarda)
- GİB altyapısı üzerinden iletilir

### E-Müstahsil Makbuzu
- Çiftçi ve esnaftan yapılan alımlarda düzenlenir
- Tarım sektörü için kritik
- Alıcı (şirket) tarafından düzenlenir, satıcı adına

### E-Serbest Meslek Makbuzu
- Serbest meslek erbabının düzenlediği e-belge
- Avukat, doktor, danışman vb.
- 2024'ten itibaren zorunluluk kapsamı genişledi

### E-Bilet
- Etkinlik, seyahat, eğlence sektörü
- QR kodlu, dijital bilet standardı

### E-Gider Pusulası
- Vergiden muaf kişilerden yapılan alımlarda
- Şirket tarafından düzenlenir

---

## 5. GİB Portal Kullanımı

### Portal Üzerinden E-Fatura

**URL:** https://efatura.gib.gov.tr

**Avantajlar:**
- Ücretsiz
- Entegratör gerekmez
- Küçük hacimli işlemler için uygun

**Dezavantajlar:**
- Manuel işlem yükü fazla
- ERP/muhasebe yazılımıyla otomatik entegrasyon yok
- Yüksek hacimli işlemlerde verimsiz

### Başvuru Adımları (GİB Portal)
1. https://ebelge.gib.gov.tr adresine git
2. "E-Fatura" → "Başvuru" menüsü
3. İnteraktif Vergi Dairesi (İVD) üzerinden başvur
4. Gerekli belgeler: VKN, e-imza veya mali mühür
5. Başvuru onay süresi: 1-3 iş günü

---

## 6. Entegratör Listesi ve Karşılaştırma

GİB'in onayladığı özel entegratörler üzerinden daha gelişmiş e-fatura çözümlerine ulaşabilirsiniz.

### Öne Çıkan Entegratörler

| Entegratör | Web Sitesi | Güçlü Yönler | Fiyat Aralığı |
|-----------|-----------|-------------|--------------|
| **Uyumsoft** | uyumsoft.com.tr | Geniş ERP entegrasyonu, SAP uyumlu | Orta-Yüksek |
| **İzibiz** | izibiz.com.tr | Türkkep altyapısı, KEP entegrasyonu güçlü | Orta |
| **Foriba** | foriba.com | Uluslararası standartlar, büyük kurumsal | Yüksek |
| **Türkkep** | turkkep.com.tr | KEP+E-fatura combo, yerli altyapı | Orta |
| **Paraşüt** | parasut.com | KOBİ dostu, bulut tabanlı, kolay kullanım | Düşük-Orta |
| **Logo** | logo.com.tr | Logo ERP entegrasyonu güçlü | Orta |
| **Mikro** | mikro.com.tr | Küçük işletmeler, uygun fiyat | Düşük |
| **Netsmart** | netsmart.com.tr | Telecom sektörü entegrasyonu | Orta |

### Entegratör Seçim Kriterleri
1. **İş hacmi:** Günlük fatura adedi
2. **ERP uyumu:** SAP, Oracle, Logo, Mikro vb.
3. **Destek kalitesi:** 7/24 teknik destek
4. **Fiyatlandırma:** Belge başı mı, aylık sabit mi?
5. **API kalitesi:** REST API, web servis desteği
6. **Arşivleme:** 10 yıl yasal saklama zorunluluğu

> **Resmi GİB Entegratör Listesi:** https://ebelge.gib.gov.tr/ozelistegrasyon.html

---

## 7. Muaf Tutulan Sektörler ve İstisnalar

### E-Fatura Düzenlemesi Gerekmeyen Durumlar
- Haddin altında kalan ve zorunlu sektörde bulunmayan mükellefler
- Basit usulde vergilendirilenler
- Gerçek usulde vergiye tabi olmayan çiftçiler
- Serbest bölgelerde faaliyet gösteren (bazı istisnalar)

### Geçici Muafiyetler
- Yeni kurulan şirketler: İlk hesap döneminde zorunluluk değerlendirmesi yapılır
- Had altı kalındığında bir sonraki yıl değerlendirmesi

---

## 8. Yasal Çerçeve

| Mevzuat | İçerik |
|---------|--------|
| VUK Genel Tebliği No. 397 | E-fatura uygulamasına ilişkin ilk tebliğ |
| VUK Genel Tebliği No. 416 | E-arşiv düzenlemeleri |
| VUK Genel Tebliği No. 421 | E-fatura zorunluluğu kapsamı |
| VUK Genel Tebliği No. 448 | E-irsaliye düzenlemeleri |
| VUK Genel Tebliği No. 509 | Kapsamlı e-belge genel tebliği (güncel) |
| HMB Tebliğleri (Yıllık) | Zorunluluk hadlerini günceller |

**Resmi kaynak:** https://www.gib.gov.tr/mevzuat

---

## 9. Sık Sorulan Sorular

**S: E-fatura almak ne kadar sürer?**  
A: GİB Portal üzerinden 1-3 iş günü, özel entegratörlerle 1 gün içinde.

**S: E-fatura için e-imza zorunlu mu?**  
A: Evet. Tüzel kişiler için mali mühür, gerçek kişiler için nitelikli elektronik imza (NEİS) veya mali mühür gereklidir.

**S: E-faturayı iptal edebilir miyim?**  
A: Ticari senaryoda alıcı 7 iş günü içinde iade faturası düzenleyebilir. Temel senaryoda iptal yok; iade faturası düzenlenir.

**S: E-faturayı ne kadar saklamamız gerekiyor?**  
A: 10 yıl (VUK md. 253). Elektronik ortamda saklanabilir.

**S: GİB portal yerine entegratör kullanmalı mıyım?**  
A: Ayda 50+ fatura düzenleyenler için entegratör kesinlikle daha verimlidir.

---

*Bu rehber Finhouse (finhouse.ai) tarafından hazırlanmıştır. Resmi mevzuat için her zaman GİB kaynaklarını kontrol edin.*
