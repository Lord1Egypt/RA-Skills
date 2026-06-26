# Erişilebilirlik Denetim Raporu

## 📋 Denetim Bilgileri

| Özellik | Değer |
|---------|-------|
| **URL** | {{URL}} |
| **Denetim Tarihi** | {{DATE}} |
| **Denetim Türü** | {{AUDIT_TYPE}} |
| **WCAG Seviyesi** | {{LEVEL}} |
| **Denetim Aracı** | a11y-auditor v1.0 |
| **Denetim Eden** | {{AUDITOR}} |

---

## 🎯 Özet Sonuçlar

### Skorlar

| Kategori | Skor | Durum |
|----------|------|-------|
| **Genel Erişilebilirlik** | {{OVERALL_SCORE}}/100 | {{STATUS}} |
| **WCAG A Uyumu** | {{A_SCORE}}% | {{A_STATUS}} |
| **WCAG AA Uyumu** | {{AA_SCORE}}% | {{AA_STATUS}} |
| **WCAG AAA Uyumu** | {{AAA_SCORE}}% | {{AAA_STATUS}} |

### Bulgu Dağılımı

| Öncelik | Sayı | Açıklama |
|---------|------|----------|
| 🔴 **Kritik** | {{CRITICAL_COUNT}} | Kullanıcıları tamamen engelleyen sorunlar |
| 🟠 **Önemli** | {{SERIOUS_COUNT}} | Kullanıcıları zorlayan sorunlar |
| 🟡 **Orta** | {{MODERATE_COUNT}} | Kullanıcı deneyimini etkileyen sorunlar |
| 🟢 **Küçük** | {{MINOR_COUNT}} | Küçük iyileştirme önerileri |

---

## 🔴 Kritik Bulgular

### 1. {{CRITICAL_ISSUE_1_TITLE}}

**WCAG Kriteri:** {{CRITERION}}
**Etki:** Kritik
**Sayfa Konumu:** {{LOCATION}}

**Sorun Açıklaması:**
{{CRITICAL_ISSUE_1_DESCRIPTION}}

**Mevcut Kod:**
```html
{{CURRENT_CODE}}
```

**Önerilen Çözüm:**
```html
{{SUGGESTED_CODE}}
```

**Referans:**
- [WCAG {{CRITERION}}]({{WCAG_LINK}})
- [W3C Understanding {{CRITERION}}]({{W3C_LINK}})

---

## 🟠 Önemli Bulgular

### 1. {{SERIOUS_ISSUE_1_TITLE}}

**WCAG Kriteri:** {{CRITERION}}
**Etki:** Önemli

**Sorun Açıklaması:**
{{SERIOUS_ISSUE_1_DESCRIPTION}}

**Önerilen Çözüm:**
{{SUGGESTED_SOLUTION}}

---

## 🟡 Orta Öncelikli Bulgular

{{MODERATE_ISSUES}}

---

## 📊 Detaylı Analiz

### 1. Algılanabilir (Perceivable)

#### 1.1 Metin Olmayan İçerikler
| Kriter | Durum | Bulgu |
|--------|-------|-------|
| 1.1.1 Metin olmayan içerik | {{1.1.1_STATUS}} | {{1.1.1_FINDING}} |

#### 1.4 Ayrırt Edilebilir
| Kriter | Durum | Bulgu |
|--------|-------|-------|
| 1.4.1 Renk kullanımı | {{1.4.1_STATUS}} | {{1.4.1_FINDING}} |
| 1.4.3 Kontrast (minimum) | {{1.4.3_STATUS}} | {{1.4.3_FINDING}} |
| 1.4.4 Metni yeniden boyutlandırma | {{1.4.4_STATUS}} | {{1.4.4_FINDING}} |
| 1.4.10 Yeniden akış | {{1.4.10_STATUS}} | {{1.4.10_FINDING}} |
| 1.4.11 Metin dışı kontrast | {{1.4.11_STATUS}} | {{1.4.11_FINDING}} |

### 2. İşletilebilir (Operable)

#### 2.1 Klavye Erişilebilirliği
| Kriter | Durum | Bulgu |
|--------|-------|-------|
| 2.1.1 Klavye erişimi | {{2.1.1_STATUS}} | {{2.1.1_FINDING}} |
| 2.1.2 Klavye tuzağı yok | {{2.1.2_STATUS}} | {{2.1.2_FINDING}} |

#### 2.4 Navigasyon
| Kriter | Durum | Bulgu |
|--------|-------|-------|
| 2.4.1 Blokları atla | {{2.4.1_STATUS}} | {{2.4.1_FINDING}} |
| 2.4.2 Sayfa başlıklı | {{2.4.2_STATUS}} | {{2.4.2_FINDING}} |
| 2.4.3 Focus sırası | {{2.4.3_STATUS}} | {{2.4.3_FINDING}} |
| 2.4.4 Link amacı | {{2.4.4_STATUS}} | {{2.4.4_FINDING}} |
| 2.4.7 Focus görünürlüğü | {{2.4.7_STATUS}} | {{2.4.7_FINDING}} |

### 3. Anlaşılabilir (Understandable)

#### 3.1 Okunabilir
| Kriter | Durum | Bulgu |
|--------|-------|-------|
| 3.1.1 Sayfa dili | {{3.1.1_STATUS}} | {{3.1.1_FINDING}} |

#### 3.3 Girdi Yardımı
| Kriter | Durum | Bulgu |
|--------|-------|-------|
| 3.3.1 Hata tanımlama | {{3.3.1_STATUS}} | {{3.3.1_FINDING}} |
| 3.3.2 Etiketler veya talimatlar | {{3.3.2_STATUS}} | {{3.3.2_FINDING}} |

### 4. Sağlam (Robust)

#### 4.1 Uyumlu
| Kriter | Durum | Bulgu |
|--------|-------|-------|
| 4.1.2 İsim, rol, değer | {{4.1.2_STATUS}} | {{4.1.2_FINDING}} |
| 4.1.3 Durum mesajları | {{4.1.3_STATUS}} | {{4.1.3_FINDING}} |

---

## 🔧 Düzeltme Önerileri

### Öncelik 1: Kritik (Hemen Düzeltilmeli)

1. **{{CRITICAL_FIX_1}}**
   - Konum: {{LOCATION}}
   - Tahmini süre: {{ESTIMATED_TIME}}
   - Kaynak: {{RESOURCE}}

### Öncelik 2: Önemli (1-2 Hafta)

1. **{{SERIOUS_FIX_1}}**
   - Konum: {{LOCATION}}
   - Tahmini süre: {{ESTIMATED_TIME}}

### Öncelik 3: Orta (1 Ay)

{{MODERATE_FIXES}}

---

## 📸 Ekran Görüntüleri

{{SCREENSHOTS}}

---

## 📁 Ek Dosyalar

- [Axe-core Sonuçları]({{AXE_RESULTS_URL}})
- [Lighthouse Raporu]({{LIGHTHOUSE_URL}})
- [Pa11y Sonuçları]({{PA11Y_URL}})
- [Klavye Test Şablonu]({{KEYBOARD_TEST_URL}})
- [Ekran Okuyucu Test Şablonu]({{SR_TEST_URL}})

---

## 📚 Kaynaklar

- [WCAG 2.2 Kriterleri](https://www.w3.org/TR/WCAG22/)
- [WAI-ARIA Yazarlık Uygulamaları](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM WCAG 2 Checklist](https://webaim.org/standards/wcag/checklist)
- [Axe-core Dokümantasyonu](https://dequeuniversity.com/rules/axe/)
- [MDN Erişilebilirlik](https://developer.mozilla.org/tr/docs/Web/Accessibility)

---

## 📝 Notlar

{{NOTES}}

---

*Bu rapor a11y-auditor tarafından otomatik olarak oluşturulmuştur.*
*Denetim Tarihi: {{DATE}}*
*Rapor Versiyonu: 1.0*