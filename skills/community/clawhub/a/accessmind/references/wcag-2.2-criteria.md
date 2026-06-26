# WCAG 2.2 Kriterleri

## İlke 1: Algılanabilir (Perceivable)

### Yönerge 1.1: Metin Dışı İçerikler

| Kriter | Seviye | Açıklama | Test Yöntemi |
|--------|--------|----------|--------------|
| 1.1.1 | A | Metin olmayan içeriklerin alternatifi | Axe, manuel kontrol |

**Kontrol Listesi:**
- [ ] Tüm img elementlerinde alt attribute var mı?
- [ ] Dekoratif görsellerde alt="" kullanılmış mı?
- [ ] İkonlarda aria-label veya aria-labelledby var mı?
- [ ] SVG'lerde role="img" ve aria-label var mı?
- [ ] Video/ses için transkripsiyon/caption var mı?

### Yönerge 1.2: Zaman Tabanlı Medya

| Kriter | Seviye | Açıklama |
|--------|--------|----------|
| 1.2.1 | A | Sesli/video içeriğe alternatif |
| 1.2.2 | A | Altyazı (caption) |
| 1.2.3 | A | Sesli betimleme veya medya alternatifi |
| 1.2.4 | AA | Canlı altyazı |
| 1.2.5 | AA | Sesli betimleme |

### Yönerge 1.3: Uyarlanabilir

| Kriter | Seviye | Açıklama | Test Yöntemi |
|--------|--------|----------|--------------|
| 1.3.1 | A | Bilgi ve ilişkiler | DOM yapısı analizi |
| 1.3.2 | A | Anlamlı sıra | Tab order kontrol |
| 1.3.3 | A | Sensory characteristics | Renk/şekil bağımsız |
| 1.3.4 | AA | Ekran yönü | Landscape/portrait test |
| 1.3.5 | AA | Girdi amacını belirleme | autocomplete attribute |
| 1.3.6 | AAA | Amaca uygun tanımlama | ARIA landmarks |

**1.3.1 Kontrolü:**
```
- Başlık hiyerarşisi: h1 > h2 > h3... (atlama yok)
- Listeler: ul/ol > li yapısı
- Tablolar: th, scope, headers
- Formlar: label > input ilişkisi
- Fieldset/legend kullanımı
```

### Yönerge 1.4: Ayrırt Edilebilir

| Kriter | Seviye | Açıklama | Test Yöntemi |
|--------|--------|----------|--------------|
| 1.4.1 | A | Renk kullanımı | Renk bağımsız bilgi |
| 1.4.2 | A | Ses kontrolü | Auto-play kontrolü |
| 1.4.3 | AA | Kontrast (minimum) | 4.5:1 normal, 3:1 büyük |
| 1.4.4 | AA | Metni yeniden boyutlandırma | 200% zoom test |
| 1.4.5 | AA | Metin görselleri | Vektör/font tercih |
| 1.4.10 | AA | Yeniden akış | 320px genişlik test |
| 1.4.11 | AA | Metin dışı kontrast | UI bileşenleri 3:1 |
| 1.4.12 | AA | Metin aralığı | Line height, letter spacing |
| 1.4.13 | AA | Hover/focus üzerinde içerik | Kapatılabilir, kalıcı |

**Kontrast Hesaplama:**
```javascript
// WCAG 2.1 kontrast formülü
function getLuminance(r, g, b) {
  const [rs, gs, bs] = [r, g, b].map(c => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

function getContrastRatio(l1, l2) {
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}
```

## İlke 2: İşletilebilir (Operable)

### Yönerge 2.1: Klavye Erişilebilirliği

| Kriter | Seviye | Açıklama | Test Yöntemi |
|--------|--------|----------|--------------|
| 2.1.1 | A | Klavye erişimi | Tab navigation test |
| 2.1.2 | A | Klavye tuzağı yok | Escape/close test |
| 2.1.3 | AAA | Klavyede çıkış yok | Full keyboard nav |
| 2.1.4 | AA | Klavye kısayolları | Modifier key kontrol |

**Klavye Testi Protokolü:**
```
1. Tab ile tüm interaktif elementlere eriş
2. Shift+Tab ile geri navigasyon
3. Enter/Space ile aktivasyon
4. Arrow keys ile grup içi navigasyon
5. Escape ile modal/close
6. Focus hiçbir yerde takılmamalı
7. Focus görür olmalı (outline)
```

### Yönerge 2.2: Yırtaım Süresi

| Kriter | Seviye | Açıklama |
|--------|--------|----------|
| 2.2.1 | A | Zamanlama ayarlanabilir |
| 2.2.2 | A | Duraklat, durdur, gizle |

### Yönerge 2.3: Nöbetler ve Fiziksel Tepkiler

| Kriter | Seviye | Açıklama |
|--------|--------|----------|
| 2.3.1 | A | Üç flashes veya alt sınır |
| 2.3.2 | AAA | Üç flashes |
| 2.3.3 | AAA | Animasyonlardan etkileşim |

### Yönerge 2.4: Navigasyon

| Kriter | Seviye | Açıklama | Test Yöntemi |
|--------|--------|----------|--------------|
| 2.4.1 | A | Blokları atla | Skip link kontrol |
| 2.4.2 | A | Sayfa başlıklı | title element |
| 2.4.3 | A | Focus sırası | Tab order mantığı |
| 2.4.4 | A | Link amacı | Link text anlamı |
| 2.4.5 | AAA | Çoklu yollar | Site haritası, nav |
| 2.4.6 | AAA | Başlıklar ve etiketler | Açıklayıcı metin |
| 2.4.7 | AA | Focus görünürlüğü | :focus-visible |
| 2.4.11 | AA | Focus görünür (WCAG 2.2) | Focus indicator |
| 2.4.12 | AAA | Blok başlangıcı | Skip to content |
| 2.4.13 | AAA | Sayfa görünür konum | Breadcrumb |

### Yönerge 2.5: Girdi Modaliteleri

| Kriter | Seviye | Açıklama |
|--------|--------|----------|
| 2.5.1 | A | İşaretçi hareketleri |
| 2.5.2 | A | İşaretçi iptali |
| 2.5.3 | AA | Etiketteki isim |
| 2.5.4 | AA | Hareketle etkinleştirme |
| 2.5.5 | AAA | Hedef boyutu |
| 2.5.6 | AAA | Eşzamanlı girdi |
| 2.5.7 | AA | Sürükleme hareketleri (WCAG 2.2) |
| 2.5.8 | AA | Hedef boyutu minimum (WCAG 2.2) |

**Hedef Boyutu (2.5.8):**
- Minimum 24x24 CSS piksel
- İstisnalar: inline linkler,间距(spacing) yeterliyse

## İlke 3: Anlaşılabilir (Understandable)

### Yönerge 3.1: Okunabilir

| Kriter | Seviye | Açıklama |
|--------|--------|----------|
| 3.1.1 | A | Sayfa dili |
| 3.1.2 | AA | Bölüm dili |

### Yönerge 3.2: Öngörülebilir

| Kriter | Seviye | Açıklama |
|--------|--------|----------|
| 3.2.1 | A | Focus üzerinde |
| 3.2.2 | A | Girdi üzerinde |
| 3.2.3 | AA | Tutarlı navigasyon |
| 3.2.4 | AA | Tutarlı tanımlama |
| 3.2.6 | AA | Tutarlı yardım (WCAG 2.2) |

### Yönerge 3.3: Girdi Yardımı

| Kriter | Seviye | Açıklama |
|--------|--------|----------|
| 3.3.1 | A | Hata tanımlama |
| 3.3.2 | A | Etiketler veya talimatlar |
| 3.3.3 | AA | Hata önerisi |
| 3.3.4 | AA | Hata önleme |
| 3.3.7 | AA | Yedekli giriş (WCAG 2.2) |
| 3.3.8 | AAA | Erişilebilir kimlik doğrulama |

## İlke 4: Sağlam (Robust)

### Yönerge 4.1: Uyumlu

| Kriter | Seviye | Açıklama | Test Yöntemi |
|--------|--------|----------|--------------|
| 4.1.2 | A | İsim, rol, değer | ARIA audit |
| 4.1.3 | AA | Durum mesajları | aria-live kontrol |

**4.1.2 Kontrolü:**
```javascript
// Custom widget'lar için gerekli:
- role attribute
- aria-label veya aria-labelledby
- aria-expanded, aria-selected, aria-checked (durum)
- tabindex
- Keyboard interaction

// Örnek: Accordion
<button aria-expanded="false" aria-controls="content1">
  Section Title
</button>
<div id="content1" aria-hidden="true">
  Content...
</div>
```

## WCAG 2.2 Yeni Kriterler

| Kriter | Seviye | Açıklama |
|--------|--------|----------|
| 2.4.11 | AA | Focus görünür |
| 2.4.12 | AAA | Blok başlangıcı |
| 2.4.13 | AAA | Sayfa görünür konum |
| 2.5.7 | AA | Sürükleme hareketleri |
| 2.5.8 | AA | Hedef boyutu minimum |
| 3.2.6 | AA | Tutarlı yardım |
| 3.3.7 | AA | Yedekli giriş |
| 3.3.8 | AAA | Erişilebilir kimlik doğrulama |

## Denetim Öncelik Matrisi

```
           ┌─────────────────────────────────────┐
           │           KULLANICI ETKİSİ          │
           ├──────────┬──────────┬───────────────┤
           │   Düşük  │  Orta    │    Yüksek     │
   ┌───────┼──────────┼──────────┼───────────────┤
   │   A   │  Orta    │  Yüksek  │   KRİTİK     │
S ├───────┼──────────┼──────────┼───────────────┤
E │  AA   │  Düşük   │  Orta    │   Yüksek     │
V ├───────┼──────────┼──────────┼───────────────┤
İ │  AAA  │  En Düşük│  Düşük   │   Orta       │
Y └───────┴──────────┴──────────┴───────────────┘
E
```