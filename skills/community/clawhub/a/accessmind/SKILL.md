---
name: accessmind
description: |
  Enterprise WCAG 2.2/2.1/EN 301 549 accessibility audit platform.
  
  OpenClaw Browser Tool ile entegre çalışan, güvenli ve profesyonel erişilebilirlik denetim sistemi.
  
  Özellikler:
  - WCAG-EM 5-step metodoloji
  - ACT Rules 50+ atomik kural
  - Klavye navigasyon testi (Tab simülasyonu)
  - Focus trap detection
  - Screen reader simülasyonu
  - Form etkileşim testleri
  - ARIA live region testi
  - OpenClaw browser tool entegrasyonu (güvenli tarama)
  - Innovative metrics (Focus Efficiency, SR Friendliness scores)
  - Profesyonel HTML/JSON raporlama
  
  Kullanım:
  (1) "https://example.com için erişilebilirlik denetimi yap"
  (2) "WCAG uyumluluk raporu oluştur"
  (3) "WCAG-EM değerlendirmesi gerçekleştir"
  (4) "Klavye navigasyon testi yap"
  (5) "Focus tuzaklarını tespit et"
  (6) "Screen reader simülasyonu yap"
  (7) "Erişilebilirlik metrikleri hesapla"

metadata:
  openclaw:
    requires:
      bins: [python3]
      python_packages: [beautifulsoup4, lxml, html5lib]
    version: 6.0

---

# AccessMind Enterprise v6.0

## 🆕 v6.0: Güvenli ve Profesyonel Erişilebilirlik Denetimi

AccessMind, OpenClaw Browser Tool ile tam entegre çalışan, güvenli ve profesyonel erişilebilirlik denetim platformudur.

```
┌─────────────────────────────────────────────────────────────┐
│  AccessMind Enterprise v6.0                                  │
├─────────────────────────────────────────────────────────────┤
│  1. OpenClaw Browser → Güvenli site açma                    │
│  2. ARIA Snapshot → DOM analizi                             │
│  3. Keyboard Navigation → Tab simülasyonu                   │
│  4. Focus Testing → Focus trap tespiti                      │
│  5. Visual Analysis → Screenshot + LLM analiz                │
│  6. ACT Rules → 50+ WCAG kuralı                             │
│  7. Professional Report → HTML/JSON çıktı                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Güvenlik

AccessMind v6.0, tüm tarayıcı işlemlerini OpenClaw Browser Tool üzerinden gerçekleştirir. Bu sayede:

- ✅ **Güvenli tarama** - OpenClaw yönetilen tarayıcı kullanır
- ✅ **Cloudflare uyumlu** - Browser tool, korumalı sitelerde çalışır
- ✅ **İzolü ortam** - Sandbox içinde çalışır
- ✅ **Şeffaf** - Tüm işlemler loglanır
- ✅ **Hafif** - Ekstra browser kurulumu gerektirmez

---

## 🚀 Hızlı Başlangıç

### Örnek Kullanım

```
Kullanıcı: https://arcelik.com.tr için erişilebilirlik denetimi yap

AccessMind:
1. Browser tool ile siteyi açar
2. ARIA snapshot alır
3. Klavye navigasyon testi yapar
4. Focus trap kontrolü yapar
5. Ekran görüntüsü alır
6. ACT Rules çalıştırır
7. Profesyonel rapor oluşturur
```

### OpenClaw Browser Tool ile Entegrasyon

```
# Siteyi aç
browser action=open url=https://example.com

# ARIA snapshot al (erişilebilirlik için optimize)
browser action=snapshot refs=aria

# Klavye navigasyonu test et
browser action=act kind=press key=Tab
browser action=snapshot refs=aria

# Focus kontrolü
browser action=act kind=press key=Tab
browser action=snapshot refs=aria

# Ekran görüntüsü al
browser action=screenshot
```

---

## ⌨️ Klavye Navigasyon Testi

AccessMind, gerçek kullanıcı davranışını simüle eder:

1. **Tab Simülasyonu** - Tüm focusable elementleri gez
2. **Focus Tracking** - Focus değişimlerini takip et
3. **Focus Indicator** - Focus göstergesi kontrolü
4. **Focus Trap Detection** - Klavye tuzaklarını tespit et
5. **Escape Test** - Modal ve dialog kapatma testi

### Sonuç Formatı

```json
{
  "keyboard_navigation": {
    "total_steps": 50,
    "focus_changes": 31,
    "visible_outlines": 28,
    "focus_visible_support": 25,
    "issues": 12
  },
  "focus_traps": {
    "total": 0,
    "details": []
  },
  "metrics": {
    "focus_efficiency": 85,
    "keyboard_accessibility": 76,
    "sr_friendliness": 92
  }
}
```

---

## 📊 ACT Rules (50+ Kural)

AccessMind, W3C ACT Rules Format'a uygun 50+ atomik kural içerir:

### Perceivable (Algılanabilir)

| Kural ID | Kriter | Açıklama |
|----------|--------|----------|
| ACT-1.1 | 1.1.1 | Image has accessible name |
| ACT-1.2 | 1.1.1 | SVG has accessible name |
| ACT-1.3 | 1.1.1 | Area has accessible name |
| ACT-2.1 | 1.3.1 | Heading has content |
| ACT-2.2 | 1.3.1 | List has proper structure |
| ACT-2.3 | 1.3.1 | Table has headers |
| ACT-3.1 | 1.4.3 | Text has sufficient contrast |
| ACT-3.2 | 1.4.3 | UI components have sufficient contrast |
| ACT-3.3 | 1.4.4 | Text resizes properly |
| ACT-3.4 | 1.4.10 | Content reflows horizontally |

### Operable (İşletilebilir)

| Kural ID | Kriter | Açıklama |
|----------|--------|----------|
| ACT-4.1 | 2.1.1 | Interactive element is keyboard accessible |
| ACT-4.2 | 2.1.1 | Focusable element has keyboard event |
| ACT-4.3 | 2.1.2 | No keyboard trap |
| ACT-4.4 | 2.4.1 | Page has bypass blocks |
| ACT-4.5 | 2.4.2 | Page has title |
| ACT-4.6 | 2.4.3 | Focus order is logical |
| ACT-4.7 | 2.4.4 | Link has accessible name |
| ACT-4.8 | 2.4.4 | Link purpose is clear |
| ACT-4.9 | 2.4.6 | Heading describes topic |
| ACT-4.10 | 2.4.7 | Focus is visible |
| ACT-4.11 | 2.5.1 | Clickable has accessible name |
| ACT-4.12 | 2.5.5 | Target size is sufficient |

### Understandable (Anlaşılabilir)

| Kural ID | Kriter | Açıklama |
|----------|--------|----------|
| ACT-5.1 | 3.1.1 | Page language is specified |
| ACT-5.2 | 3.1.2 | Part language is specified |
| ACT-5.3 | 3.2.1 | Focus doesn't change context |
| ACT-5.4 | 3.2.2 | Input doesn't change context unexpectedly |
| ACT-5.5 | 3.2.4 | Consistent navigation |
| ACT-5.6 | 3.3.1 | Error identification |
| ACT-5.7 | 3.3.2 | Form has labels |
| ACT-5.8 | 3.3.3 | Error suggestion |
| ACT-5.9 | 3.3.4 | Error prevention |

### Robust (Sağlam)

| Kural ID | Kriter | Açıklama |
|----------|--------|----------|
| ACT-6.1 | 4.1.1 | Parsing is valid |
| ACT-6.2 | 4.1.2 | Custom element has accessible name |
| ACT-6.3 | 4.1.2 | Custom element has role |
| ACT-6.4 | 4.1.2 | ARIA state is valid |
| ACT-6.5 | 4.1.2 | Form has accessible name |
| ACT-6.6 | 4.1.3 | Status message has role |

---

## 📈 Innovative Metrics

### Focus Efficiency Score (0-100)

Focus'un sayfada ne kadar verimli hareket ettiğini ölçer:
- Focus değişim tutarlılığı (40%)
- Visible focus outlines (30%)
- :focus-visible desteği (30%)

### Keyboard Accessibility Score (0-100)

Klavye erişilebilirlik sorunlarını ölçer:
- Critical sorun: -10 puan
- Serious sorun: -5 puan
- Moderate sorun: -2 puan

### Screen Reader Friendliness Score (0-100)

ARIA live region kalitesini ölçer:
- Doğru aria-live attribute'ları (50%)
- Dinamik içerik duyuruları (50%)

### Focus Trap Risk Score (0-100)

Klavye tuzağı riskini ölçer:
- 0 tuzak: 100 puan
- 1 tuzak: 70 puan
- 2 tuzak: 40 puan
- 3+ tuzak: 20 puan

---

## 📝 Profesyonel Raporlama

### HTML Rapor

```html
<!DOCTYPE html>
<html lang="tr">
<head>
    <title>WCAG Erişilebilirlik Raporu - example.com</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <header>
        <h1>Erişilebilirlik Denetim Raporu</h1>
        <p>Site: example.com</p>
        <p>Tarih: 2026-03-26</p>
    </header>
    
    <section id="summary">
        <h2>Özet</h2>
        <div class="score">Overall Score: 85/100</div>
        <div class="issues">Toplam İhlal: 12</div>
    </section>
    
    <section id="wcag-criteria">
        <h2>WCAG Kriterleri</h2>
        <!-- Her kriter için detaylı sonuç -->
    </section>
    
    <section id="recommendations">
        <h2>Öneriler</h2>
        <!-- Düzeltme önerileri -->
    </section>
</body>
</html>
```

### JSON Rapor

```json
{
  "audit_info": {
    "url": "https://example.com",
    "date": "2026-03-26T08:00:00Z",
    "auditor": "AccessMind Enterprise v6.0",
    "standard": "WCAG 2.2 AA"
  },
  "summary": {
    "overall_score": 85,
    "total_issues": 12,
    "critical": 2,
    "serious": 5,
    "moderate": 5
  },
  "criteria_results": [
    {
      "criterion": "1.1.1",
      "name": "Non-text Content",
      "result": "FAIL",
      "issues": [
        {
          "element": "<img src='logo.png'>",
          "issue": "Image missing alt attribute",
          "severity": "critical",
          "wcag": "1.1.1"
        }
      ]
    }
  ],
  "metrics": {
    "focus_efficiency": 85,
    "keyboard_accessibility": 76,
    "sr_friendliness": 92,
    "focus_trap_risk": 100
  }
}
```

---

## 🔧 Kullanım

### CLI (Eski Script'ler)

```bash
# Klavye navigasyon testi
python3 /Users/sarper/.openclaw/workspace/skills/accessmind/scripts/accessmind-behavioral-navigator.py \
  --url https://example.com \
  --steps 50 \
  --output /Users/sarper/.openclaw/workspace/audits

# Derinlemesine tarama
python3 /Users/sarper/.openclaw/workspace/skills/accessmind/scripts/accessmind-deep-crawler.py \
  --url https://example.com \
  --depth 5 \
  --pages 12 \
  --output /Users/sarper/.openclaw/workspace/audits
```

### OpenClaw Browser Tool (Önerilen)

AccessMind artık OpenClaw Browser Tool ile tam entegre çalışıyor. Kullanıcıdan gelen "siteyi denetle" talebi otomatik olarak browser tool ile gerçekleştirilir.

---

## 📁 Dosya Yapısı

```
/Users/sarper/.openclaw/workspace/skills/accessmind/
├── SKILL.md                              # Ana dokümantasyon
├── references/
│   ├── wcag-2.2-criteria.md              # WCAG 2.2 kriterleri
│   ├── aria-guide.md                     # ARIA kılavuzu
│   ├── screen-reader-patterns.md         # Screen reader kalıpları
│   ├── voiceover-patterns.md             # VoiceOver kalıpları
│   ├── common-issues.md                  # Yaygın sorunlar
│   ├── browser-tool-workflow.md          # Browser tool workflow
│   └── mobile-testing.md                 # Mobil test
├── scripts/
│   ├── accessmind-behavioral-navigator.py # Klavye navigasyon testi
│   ├── accessmind-deep-crawler.py         # Derinlemesine tarama
│   ├── act-rules-engine.py                # ACT Rules motoru
│   ├── report-generator.py                # Rapor oluşturucu
│   └── wcag-em-evaluator.py               # WCAG-EM değerlendirici
└── assets/
    └── report-template.md                 # Rapor şablonu
```

---

## 🎯 WCAG Kriterleri

| Kriter | Kategori | Test Edildi |
|--------|----------|-------------|
| 1.1.1 | Non-text Content | ✅ |
| 1.2.1 | Audio-only and Video-only | ✅ |
| 1.3.1 | Info and Relationships | ✅ |
| 1.3.2 | Meaningful Sequence | ✅ |
| 1.4.3 | Contrast Minimum | ✅ |
| 1.4.4 | Resize Text | ✅ |
| 1.4.10 | Reflow | ✅ |
| 1.4.11 | Non-text Contrast | ✅ |
| 2.1.1 | Keyboard | ✅ |
| 2.1.2 | No Keyboard Trap | ✅ |
| 2.1.4 | Character Key Shortcuts | ✅ |
| 2.4.1 | Bypass Blocks | ✅ |
| 2.4.2 | Page Titled | ✅ |
| 2.4.3 | Focus Order | ✅ |
| 2.4.4 | Link Purpose | ✅ |
| 2.4.5 | Multiple Ways | ✅ |
| 2.4.6 | Headings and Labels | ✅ |
| 2.4.7 | Focus Visible | ✅ |
| 2.5.1 | Pointer Gestures | ✅ |
| 2.5.2 | Pointer Cancellation | ✅ |
| 2.5.3 | Label in Name | ✅ |
| 2.5.4 | Motion Actuation | ✅ |
| 2.5.5 | Target Size | ✅ |
| 2.5.8 | Target Size (Minimum) | ✅ |
| 3.1.1 | Language of Page | ✅ |
| 3.1.2 | Language of Parts | ✅ |
| 3.2.1 | On Focus | ✅ |
| 3.2.2 | On Input | ✅ |
| 3.2.3 | Consistent Navigation | ✅ |
| 3.2.4 | Consistent Identification | ✅ |
| 3.3.1 | Error Identification | ✅ |
| 3.3.2 | Labels or Instructions | ✅ |
| 3.3.3 | Error Suggestion | ✅ |
| 3.3.4 | Error Prevention | ✅ |
| 3.3.7 | Redundant Entry | ✅ |
| 4.1.2 | Name, Role, Value | ✅ |
| 4.1.3 | Status Messages | ✅ |

---

## 📚 Referanslar

- **WCAG-EM**: https://www.w3.org/TR/WCAG-EM/
- **ACT Rules**: https://www.w3.org/WAI/standards-guidelines/act/
- **WCAG 2.2**: https://www.w3.org/TR/WCAG22/
- **ARIA Authoring Practices**: https://www.w3.org/WAI/ARIA/apg/
- **Axe-core Rules**: https://dequeuniversity.com/rules/axe/4.10/

---

**AccessMind Enterprise v6.0**  
*Güvenli ve Profesyonel Erişilebilirlik Denetimi*  
*OpenClaw Browser Tool Entegrasyonu*  
*WCAG 2.2 AA Uyumluluk*