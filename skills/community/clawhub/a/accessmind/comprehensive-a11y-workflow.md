# AccessMind KAPOZLU Erişilebilirlik Denetim İşlem Akışı

## 5 Test Modülü

### 1. ✅ WCAG 2.2 Otomatik Tarama
- **Motor:** Axe-core 4.10.0
- **Standartlar:** WCAG 2.2 A/AA, WCAG 2.1 AA, WCAG 2.2 AA
- **Çıktı:** İhlal listesi, pass count, score

### 2. ⌨️ Klavye Navigasyon Denetimi
- **Testler:**
  - Focusable element tespiti
  - Skip link kontrolü
  - Tab order analizi
  - Positive tabIndex tespiti
  - Keyboard trap kontrolü
- **WCAG:** 2.1.1, 2.4.1, 2.4.3, 2.4.7

### 3. 🔊 Ekran Okuyucu Uyumluluğu
- **Testler:**
  - ARIA landmarks (main, nav, header, footer, etc.)
  - Accessible names (buttons, links, images, forms)
  - Live regions (aria-live, role="alert")
  - Heading hiyerarşisi
- **Screen Readers:** NVDA, JAWS, VoiceOver patternleri
- **WCAG:** 1.3.1, 4.1.2, 1.3.6

### 4. 🎨 Renk Kontrastı Analizi
- **Testler:**
  - Foreground/background color extraction
  - Contrast ratio calculation (WCAG formülü)
  - Large text detection (18pt+/14pt bold)
  - AA (4.5:1) vs AAA (7:1) compliance
- **WCAG:** 1.4.3 (Contrast), 1.4.6 (Enhanced Contrast)

### 5. 👁️ Görsel Erişilebilirlik
- **Testler:**
  - Base font size (min 16px)
  - Line height (min 1.5)
  - Text alignment (no justify)
  - Touch target size (min 44x44px)
  - Focus indicator visibility
- **WCAG:** 1.4.4, 1.4.8, 1.4.12, 2.5.8, 2.4.7

## Skor Hesaplama

```python
wcag_score = 100 - (critical×25 + serious×15 + moderate×8 + minor×3)
keyboard_score = 100 - (issues×10)
sr_score = 100 - (issues×15)
contrast_score = 100 - (issues×12)
visual_score = 100 - (issues×10)

final_score = (wcag×0.4 + keyboard×0.2 + sr×0.2 + contrast×0.1 + visual×0.1)
```

## Çıktı Dosyaları
- `audits/arcelik_comprehensive_YYYYMMDD_HHMMSS.html`
- `audits/arcelik_comprehensive_YYYYMMDD_HHMMSS.json`
- `skills/accessmind/comprehensive-a11y-workflow.md`

## Kullanım
```bash
python3 /Users/sarper/.openclaw/workspace/skills/accessmind/scripts/comprehensive-a11y-audit.py
```
