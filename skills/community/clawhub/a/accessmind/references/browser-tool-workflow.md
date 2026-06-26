# Browser Tool Workflow - AccessMind v5.1

Bu doküman, OpenClaw browser tool kullanarak erişilebilirlik testlerinin nasıl yapılacağını açıklar.

## 🎯 Neden Browser Tool?

### Avantajlar
- **Cloudflare Bypass:** Korumalı sitelere erişim
- **JavaScript Render:** Dinamik içerik analizi
- **Gerçek Kullanıcı Simülasyonu:** LLM odaklı test
- **Akıllı Analiz:** Pattern recognition ve context understanding
- **Hızlı Prototipleme:** Script yazmadan test

### Kullanım Senaryoları
1. Hızlı erişilebilirlik taraması
2. Cloudflare korumalı siteler
3. SPA (Single Page Application) testi
4. Dinamik form testi
5. Ekran okuyucu simülasyonu

---

## 📋 Browser Tool Komutları

### Temel Komutlar

```
browser action=status                    # Browser durumu
browser action=start                     # Browser başlat
browser action=stop                      # Browser durdur
browser action=tabs                      # Sekme listesi
```

### Sayfa İşlemleri

```
browser action=open url=https://example.com     # Sayfa aç
browser action=navigate url=https://...         # Navigate
browser action=snapshot refs=aria               # ARIA snapshot
browser action=screenshot type=png              # Ekran görüntüsü
browser action=snapshot refs=role               # Role-based snapshot
browser action=snapshot format=ai               # AI-optimized
```

### Etkileşim Komutları

```
browser action=act kind=click ref=e15           # Tıklama
browser action=act kind=type ref=e20 text="hello"   # Yazma
browser action=act kind=press key=Tab           # Tuş basma
browser action=act kind=fill ref=e25 text="test"    # Form doldurma
browser action=act kind=hover ref=e30           # Hover
browser action=act kind=wait timeMs=2000        # Bekleme
```

---

## 🧪 Erişilebilirlik Test Workflow'u

### 1. Başlangıç: Site Açma

```
# Browser başlat ve site aç
browser action=open url=https://www.example.com target=host

# Sayfanın yüklenmesini bekle
browser action=act kind=wait timeMs=3000

# ARIA snapshot al
browser action=snapshot refs=aria
```

**Beklenen Çıktı:**
- ARIA tree yapısı
- Tüm interactive elements
- ARIA labels ve roles
- Focus sırası

### 2. Klavye Navigasyon Testi

```
# İlk Tab
browser action=act kind=press key=Tab
browser action=snapshot refs=aria

# İkinci Tab
browser action=act kind=press key=Tab
browser action=snapshot refs=aria

# Focus elementini kontrol et
# (Snapshot'ta focus göstergesi görünür)

# 10-20 Tab daha
# (Loop için tekrar et)
```

**Dikkat Edilecekler:**
- Focus görünür mü? (outline, background)
- Focus sırası mantıklı mı?
- Skip link var mı?
- Focus trap var mı?

### 3. Görsel Analiz

```
# Tam sayfa ekran görüntüsü
browser action=screenshot fullPage=true

# Sadece viewport
browser action=screenshot
```

**Analiz Edilecekler:**
- Renk kontrastı
- Font boyutları
- Buton görünürlüğü
- Form label ilişkisi

### 4. Form Erişilebilirliği

```
# Form elementlerini bul
browser action=snapshot refs=aria

# Input'a tıkla
browser action=act kind=click ref=e20

# Değer gir
browser action=act kind=type ref=e20 text="test@example.com"

# Label ilişkisini kontrol et
# (Snapshot'ta aria-labelledby görünür)

# Hata mesajı testi
browser action=act kind=press key=Tab  # Submit butonuna git
browser action=act kind=press key=Enter  # Formu gönder

# Hata mesajı göründü mü?
browser action=snapshot refs=aria
```

### 5. ARIA Live Region Testi

```
# Sayfada dinamik içerik var mı?
browser action=snapshot refs=aria

# aria-live="polite" veya aria-live="assertive" ara

# Dinamik içerik tetikle (ör: filter, search)
browser action=act kind=type ref=search text="laptop"

# Sonucu bekle
browser action=act kind=wait timeMs=2000

# Sonuç bölgesini kontrol et
browser action=snapshot refs=aria
```

### 6. Link ve Button Testi

```
# Tüm linkleri bul
browser action=snapshot refs=role

# Link metni anlaşılır mı?
# "click here" yerine "Learn more about accessibility"

# Button'ları test et
browser action=act kind=click ref=button1

# Modal açıldı mı?
browser action=snapshot refs=aria

# Modal kapat
browser action=act kind=press key=Escape
```

### 7. Dinamik İçerik Testi

```
# Sayfayı yükle
browser action=open url=https://spa-example.com

# İlk snapshot
browser action=snapshot refs=aria

# Scroll yap (sonsuz scroll testi)
browser action=act kind=press key=End
browser action=act kind=wait timeMs=1000

# Yeni içerik yüklendi mi?
browser action=snapshot refs=aria

# Pagination veya load more
browser action=act kind=click ref=load-more
browser action=act kind=wait timeMs=2000
browser action=snapshot refs=aria
```

---

## 📊 Raporlama Formatı

### JSON Çıktı

```json
{
  "url": "https://example.com",
  "timestamp": "2026-03-24T14:00:00Z",
  "browser_tool_results": {
    "keyboard_navigation": {
      "total_tabs": 25,
      "focus_visible": 23,
      "focus_trap_detected": false,
      "skip_link_found": true,
      "issues": [
        {
          "element": "e15",
          "type": "missing_focus_indicator",
          "wcag": "2.4.7",
          "severity": "serious"
        }
      ]
    },
    "aria_analysis": {
      "live_regions": 5,
      "landmarks": 8,
      "headings": 12,
      "issues": [
        {
          "element": "e30",
          "type": "missing_aria_label",
          "wcag": "4.1.2",
          "severity": "critical"
        }
      ]
    },
    "visual_analysis": {
      "contrast_issues": 3,
      "font_size_issues": 1,
      "touch_target_issues": 2
    }
  },
  "scores": {
    "focus_efficiency": 85,
    "keyboard_accessibility": 78,
    "screen_reader_friendliness": 82
  }
}
```

---

## 🎯 WCAG Kriteri Eşleştirmesi

| WCAG Kriteri | Browser Tool Testi |
|--------------|-------------------|
| 1.1.1 Non-text Content | Screenshot + alt text kontrol |
| 1.3.1 Info and Relationships | ARIA snapshot + heading structure |
| 1.4.3 Contrast Minimum | Screenshot + visual analysis |
| 2.1.1 Keyboard | Tab navigation test |
| 2.1.2 No Keyboard Trap | Focus trap detection |
| 2.4.1 Bypass Blocks | Skip link search |
| 2.4.3 Focus Order | Tab order analysis |
| 2.4.4 Link Purpose | Link text analysis |
| 2.4.7 Focus Visible | Focus indicator check |
| 4.1.2 Name, Role, Value | ARIA attributes check |
| 4.1.3 Status Messages | aria-live detection |

---

## 💡 Best Practices

### 1. Snapshot Optimizasyonu

```
# ARIA snapshot (erişilebilirlik için optimize)
browser action=snapshot refs=aria

# Role-based snapshot (daha detaylı)
browser action=snapshot refs=role

# AI-optimized (LLM analizi için)
browser action=snapshot format=ai
```

### 2. Focus Trap Tespiti

```
# Tab ile gezin ve focus'u takip et
# Aynı element'e 2 kez gelirse = FOCUS TRAP
# 50 Tab sonunda başa dönmezse = FOCUS TRAP riski
```

### 3. Dinamik İçerik

```
# JavaScript-heavy sayfalar için bekleme süresi artır
browser action=act kind=wait timeMs=3000

# SPA'larda route değişikliklerini izle
browser action=snapshot refs=aria
browser action=act kind=click ref=nav-link
browser action=act kind=wait timeMs=2000
browser action=snapshot refs=aria
```

### 4. Cloudflare Bypass

```
# OpenClaw browser tool Cloudflare'ı otomatik aşar
# İnsan davranışı simülasyonu ile
browser action=open url=https://protected-site.com target=host

# İlk bekleme (challenge için)
browser action=act kind=wait timeMs=5000

# Sonra normal test
browser action=snapshot refs=aria
```

---

## 🔧 Sorun Giderme

### Sayfa Yüklenmiyorsa

```
# Uzun bekle
browser action=act kind=wait timeMs=5000

# Yeniden dene
browser action=navigate url=https://example.com
```

### Element Bulunamıyorsa

```
# Farklı snapshot formatı dene
browser action=snapshot refs=role
browser action=snapshot refs=aria

# Veya compact mod
browser action=snapshot mode=efficient
```

### Focus Görünmüyorsa

```
# CSS :focus-visible kontrolü gerekli
# Bu durum manual CSS inceleme gerektirir
# Script ile: python scripts/accessmind-agentic-auditor.py
```

---

## 📝 Örnek Test Senaryosu

### E-ticaret Site Testi

```
# 1. Ana sayfa
browser action=open url=https://shop.example.com
browser action=act kind=wait timeMs=3000
browser action=snapshot refs=aria

# 2. Arama
browser action=act kind=click ref=search-input
browser action=act kind=type ref=search-input text="laptop"
browser action=act kind=press key=Enter
browser action=act kind=wait timeMs=2000

# 3. Sonuçlar
browser action=snapshot refs=aria

# 4. Ürün detay
browser action=act kind=click ref=product-1
browser action=act kind=wait timeMs=2000
browser action=snapshot refs=aria

# 5. Sepete ekle
browser action=act kind=click ref=add-to-cart
browser action=act kind=wait timeMs=1000
browser action=snapshot refs=aria  # Modal açıldı mı?

# 6. Checkout
browser action=act kind=click ref=checkout-button
browser action=act kind=wait timeMs=2000
browser action=snapshot refs=aria

# 7. Form doldurma
browser action=act kind=fill ref=email text="test@test.com"
browser action=act kind=fill ref=name text="Test User"
browser action=snapshot refs=aria  # Labels doğru mu?

# 8. Hata testi
browser action=act kind=click ref=submit
browser action=act kind=wait timeMs=1000
browser action=snapshot refs=aria  # Hata mesajları erişilebilir mi?
```

---

## 🎓 Eğitim Kaynakları

1. **WCAG-EM 5-Step Methodology:** `references/wcag-em-workflow.md`
2. **ACT Rules Engine:** `scripts/act-rules-engine.py`
3. **Keyboard Navigation:** `scripts/keyboard-voiceover-test.py`
4. **Screen Reader Patterns:** `references/screen-reader-patterns.md`

---

**Version:** 5.1.0
**Last Updated:** 2026-03-24
**Author:** AccessMind Team