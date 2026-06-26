# Yaygın Erişilebilirlik Sorunları ve Çözümleri

## 1. Görseller ve Alternatif Metinler

### Sorun: Eksik veya yanlış alt metin

**Tespit:**
```bash
# Tüm img elementlerini bul
document.querySelectorAll('img:not([alt])')  // Eksik alt
document.querySelectorAll('img[alt=""]')       // Dekoratif mi?
document.querySelectorAll('img[alt="image"]')  // Anlamsız alt
```

**Çözümler:**

| Durum | Çözüm |
|-------|-------|
| Bilgi veren görsel | Açıklayıcı alt metin |
| Dekoratif görsel | `alt=""` veya `role="presentation"` |
| Karmaşık görsel (grafik) | `aria-describedby` + uzun açıklama |
| İkon buton | `aria-label` veya görsel metin |

**Örnekler:**
```html
<!-- Bilgi veren -->
<img src="chart.png" alt="2024 satış grafik: %25 artış">

<!-- Dekoratif -->
<img src="decoration.png" alt="" role="presentation">

<!-- İkon buton -->
<button aria-label="Ara">
  <img src="search.svg" alt="">
</button>

<!-- Karmaşık -->
<img src="diagram.png" alt="İş akışı şeması" 
     aria-describedby="diagram-desc">
<p id="diagram-desc" class="sr-only">
  Şema 4 adım gösteriyor: Başlangıç, İşlem, Kontrol, Sonuç
</p>
```

---

## 2. Renk Kontrastı

### Sorun: Yetersiz kontrast oranı

**Gereksinimler:**
- Normal metin: 4.5:1 minimum
- Büyük metin (18px+ veya 14px bold): 3:1 minimum
- UI bileşenleri: 3:1 minimum

**Tespit:**
```javascript
// Kontrast hesaplama
function getContrastRatio(fg, bg) {
  const fgLum = getLuminance(fg);
  const bgLum = getLuminance(bg);
  return (Math.max(fgLum, bgLum) + 0.05) / 
         (Math.min(fgLum, bgLum) + 0.05);
}

// Axe-core otomatik tespit
// axe.run().then(results => console.log(results.violations))
```

**Yaygın Sorunlar:**

| Element | Tipik Sorun | Çözüm |
|---------|-------------|-------|
| Placeholder | Çok açık gri | Daha koyu gri (#767676) |
| İkincil metin | Düşük kontrast | Ana metin rengine yaklaştır |
| Hata mesajı | Kırmızı on kırmızı | Koyu kırmızı metin veya ikon |
| Link | Mavi on mavi zemin | Alt çizgi veya kontrast renk |
| Devre dışı buton | Çok açık | En az 3:1 UI kontrast |

---

## 3. Klavye Erişilebilirliği

### Sorun: Focus tuzağı

**Tespit:**
```javascript
// Modal/dropdown açıldığında focus trap kontrolü
// Tab ile modal dışına çıkılabilmeli (ESC ile kapatılabilir)
```

**Çözüm:**
```javascript
// Focus trap yönetimi
function trapFocus(element) {
  const focusableEls = element.querySelectorAll(
    'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
  );
  const firstFocusable = focusableEls[0];
  const lastFocusable = focusableEls[focusableEls.length - 1];

  element.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstFocusable) {
        e.preventDefault();
        lastFocusable.focus();
      } else if (!e.shiftKey && document.activeElement === lastFocusable) {
        e.preventDefault();
        firstFocusable.focus();
      }
    }
    if (e.key === 'Escape') {
      closeModal();
    }
  });
}
```

### Sorun: Focus görsel eksikliği

**Tespit:**
```css
/* Focus outline kaldırılmış mı? */
*:focus {
  outline: none; /* ❌ SORUN! */
}
```

**Çözüm:**
```css
/* Modern focus görseli */
:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

/* Alternatif: Box-shadow */
:focus-visible {
  box-shadow: 0 0 0 3px rgba(0, 95, 204, 0.5);
}

/* Özel focus stili */
.button:focus-visible {
  background-color: #003366;
  border-color: #ffcc00;
}
```

---

## 4. Form Erişilebilirliği

### Sorun: Eksik veya yanlış etiketleme

**Tespit:**
```javascript
// Etiketsiz input'lar
document.querySelectorAll('input:not([id])')
document.querySelectorAll('input:not([aria-label]):not([aria-labelledby])')
document.querySelectorAll('input').filter(input => {
  const label = document.querySelector(`label[for="${input.id}"]`);
  return !label && !input.getAttribute('aria-label');
});
```

**Çözümler:**
```html
<!-- Yöntem 1: Label for -->
<label for="email">E-posta</label>
<input type="email" id="email">

<!-- Yöntem 2: Label sarmalama -->
<label>
  E-posta
  <input type="email">
</label>

<!-- Yöntem 3: aria-label -->
<input type="search" aria-label="Site içi arama">

<!-- Yöntem 4: aria-labelledby -->
<span id="search-label">Ara</span>
<input type="search" aria-labelledby="search-label">

<!-- Zorunlu alan -->
<label for="name">
  Ad Soyad <span aria-hidden="true">*</span>
  <span class="sr-only">(zorunlu)</span>
</label>
<input type="text" id="name" required aria-required="true">
```

### Sorun: Hata mesajları erişilebilir değil

**Çözüm:**
```html
<div class="form-group">
  <label for="email">E-posta</label>
  <input type="email" 
         id="email" 
         aria-describedby="email-error"
         aria-invalid="false">
  <span id="email-error" class="error" role="alert" aria-live="polite">
    <!-- Hata mesajı buraya -->
  </span>
</div>

<script>
function showError(input, message) {
  input.setAttribute('aria-invalid', 'true');
  document.getElementById(input.getAttribute('aria-describedby')).textContent = message;
}
</script>
```

---

## 5. ARIA Kullanımı

### Sorun: Yanlış veya gereksiz ARIA

**Kurallar:**
1. Native HTML her zaman ARIA'dan iyi
2. ARIA rolleri native anlamlı elementlerle çelişmemeli
3. Interactive elementler klavye erişilebilir olmalı

**Yaygın Hatalar:**

| Hata | Sorun | Çözüm |
|------|-------|-------|
| `role="button"` on `<div>` | Klavye erişimi yok | `<button>` kullan |
| `aria-hidden="true"` on focusable | Gizli ama odaklanılabilir | Tabindex="-1" ekle |
| Duplicate IDs | ARIA referansları bozulur | Benzersiz ID |
| `role="presentation"` preserves content | Anlam kaybı | Doğru yerde kullan |
| `aria-live` overuse | Gereksiz duyurular | Sadece önemli değişikliklerde |

**Doğru ARIA Kullanımı:**
```html
<!-- Accordion -->
<div class="accordion">
  <button aria-expanded="false" aria-controls="panel1">
    Bölüm 1
  </button>
  <div id="panel1" aria-hidden="true">
    İçerik...
  </div>
</div>

<!-- Tab panel -->
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel1">Tab 1</button>
  <button role="tab" aria-selected="false" aria-controls="panel2">Tab 2</button>
</div>
<div role="tabpanel" id="panel1" aria-labelledby="tab1">...</div>
<div role="tabpanel" id="panel2" aria-labelledby="tab2" hidden>...</div>

<!-- Live region -->
<div aria-live="polite" aria-atomic="true">
  Sepete eklendi: 3 ürün
</div>
```

---

## 6. Başlık Hiyerarşisi

### Sorun: Atlamalı veya yanlış başlık yapısı

**Tespit:**
```javascript
// Başlık hiyerarşisi analizi
const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
let prevLevel = 0;
headings.forEach(h => {
  const level = parseInt(h.tagName[1]);
  if (level - prevLevel > 1) {
    console.warn(`Başlık atlaması: h${prevLevel} -> h${level}`, h);
  }
  prevLevel = level;
});
```

**Doğru Yapı:**
```html
<h1>Sayfa Başlığı</h1>      <!-- Sayfa başına 1 tane -->
  <h2>Bölüm 1</h2>
    <h3>Alt Bölüm 1.1</h3>
    <h3>Alt Bölüm 1.2</h3>
  <h2>Bölüm 2</h2>
    <h3>Alt Bölüm 2.1</h3>
      <h4>Detay 2.1.1</h4>
```

---

## 7. Skip Link

### Sorun: Skip link eksikliği

**Çözüm:**
```html
<body>
  <a href="#main-content" class="skip-link">
    Ana içeriğe atla
  </a>
  
  <nav>...</nav>
  
  <main id="main-content">
    <!-- Ana içerik -->
  </main>
</body>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px 16px;
  z-index: 100;
  transition: top 0.2s;
}

.skip-link:focus {
  top: 0;
}
</style>
```

---

## 8. Dinamik İçerik

### Sorun: SPA'de içerik değişimi duyurulmuyor

**Çözüm:**
```javascript
// Sayfa başlığı güncelleme
document.title = `Yeni Sayfa | Site Adı`;

// İçerik değişimi duyurusu
function announcePageChange(title) {
  const announcer = document.getElementById('page-announcer');
  announcer.textContent = `${title} sayfası yüklendi`;
}

// Live region
<div id="page-announcer" 
     aria-live="polite" 
     aria-atomic="true" 
     class="sr-only">
</div>
```

---

## 9. Modal ve Dialog

### Sorun: Modal erişilebilir değil

**Çözüm:**
```html
<div role="dialog" 
     aria-modal="true" 
     aria-labelledby="dialog-title"
     aria-describedby="dialog-desc">
  <h2 id="dialog-title">Onay</h2>
  <p id="dialog-desc">Bu işlemi onaylıyor musunuz?</p>
  <button onclick="closeDialog()">İptal</button>
  <button onclick="confirm()">Onayla</button>
</div>
```

**JavaScript Kontrolü:**
```javascript
// 1. Focus modal'a taşı
// 2. Focus trap uygula
// 3. ESC ile kapat
// 4. Kapatınca focus geri döndür
// 5. Background scroll engelle
// 6. aria-hidden on background
```

---

## 10. Tablo Erişilebilirliği

### Sorun: Veri tablosu yapılandırılmamış

**Çözüm:**
```html
<table>
  <caption>Ürün Fiyat Listesi</caption>
  <thead>
    <tr>
      <th scope="col">Ürün</th>
      <th scope="col">Fiyat</th>
      <th scope="col">Stok</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Ürün A</th>
      <td>100 TL</td>
      <td>50</td>
    </tr>
  </tbody>
</table>

<!-- Karmaşık tablo -->
<table>
  <thead>
    <tr>
      <th rowspan="2" scope="colgroup">Bölge</th>
      <th colspan="2" scope="colgroup">Satışlar</th>
    </tr>
    <tr>
      <th scope="col">2023</th>
      <th scope="col">2024</th>
    </tr>
  </thead>
  ...
</table>
```

---

## Hızlı Denetim Listesi

```
□ Her görselin alt metni var mı?
□ Renk kontrastı yeterli mi? (4.5:1 / 3:1)
□ Klavye ile tüm elementlere erişilebilir mi?
□ Focus görsel görünür mü?
□ Form etiketleri doğru mu?
□ Hata mesajları duyuruluyor mu?
□ Başlık hiyerarşisi doğru mu?
□ Skip link var mı?
□ Dil attribute'u var mı? (lang="tr")
□ ARIA doğru kullanılmış mı?
□ Tablo başlıkları var mı?
□ Video altyazısı/caption var mı?
□ Dinamik değişiklikler duyuruluyor mu?
□ Touch hedefleri yeterli mi? (24x24px min)
```