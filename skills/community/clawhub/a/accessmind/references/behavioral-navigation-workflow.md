# Behavioral Navigation Workflow

## Davranış Bazlı Erişilebilirlik Gezinim Testi

Bu workflow, gerçek kullanıcı davranışını taklit eden erişilebilirlik testi için kullanılır.

---

## 🎯 Test Senaryoları

### 1. Klavye Kullanıcı Gezinimi

```
Senaryo: Kullanıcı sadece klavye ile sayfayı geziyor

Adımlar:
1. Tab tuşu ile sırayla gezin
2. Her element'te:
   - Focus göstergesi var mı?
   - Erişilebilir isim var mı?
   - Rol doğru mu?
   - Harekete geçirilebilir mi?
3. Focus tuzağı var mı?
4. Başa sarma var mı?

WCAG Kriterleri:
- 2.1.1 Keyboard
- 2.1.2 No Keyboard Trap
- 2.4.3 Focus Order
- 2.4.7 Focus Visible
```

### 2. Screen Reader Kullanıcı Gezinimi

```
Senaryo: Kullanıcı NVDA/JAWS ile sayfayı geziyor

Adımlar:
1. Sayfa başlığı duyuruluyor mu?
2. Landmark'lar duyuruluyor mu?
3. Başlıklar hiyerarşisi doğru mu?
4. Form etiketleri duyuruluyor mu?
5. Hata mesajları live region'da mı?

WCAG Kriterleri:
- 1.3.1 Info and Relationships
- 2.4.6 Headings and Labels
- 4.1.2 Name, Role, Value
- 4.1.3 Status Messages
```

### 3. Motor Engelli Kullanıcı Gezinimi

```
Senaryo: Kullanıcı sadece klavye ve tek tuş ile geziniyor

Adımlar:
1. Büyük focus alanları var mı?
2. Kısayol tuşları var mı?
3. Skip link mevcut mu?
4. Yeterli hedef boyutu var mı?

WCAG Kriterleri:
- 2.1.1 Keyboard
- 2.4.1 Bypass Blocks
- 2.5.5 Target Size
- 2.5.6 Concurrent Input Mechanisms
```

### 4. Bilişsel Engelli Kullanıcı Gezinimi

```
Senaryo: Kullanıcı karmaşık gezinimden kaynaklanan sorunlar yaşıyor

Adımlar:
1. Navigasyon karmaşık mı?
2. Error recovery kolay mı?
3. Tutarsız element'ler var mı?
4. Hidden content sorunları var mı?

WCAG Kriterleri:
- 3.2.1 On Focus
- 3.2.2 On Input
- 3.2.3 Consistent Navigation
- 3.2.4 Consistent Identification
```

---

## 📊 Skor Hesaplama

### Focus Efficiency Score

```
Focus Efficiency = (Visible Focus Count / Total Steps) * 100

Örnek:
- Toplam adım: 50
- Visible focus: 35
- Focus Efficiency = (35/50) * 100 = 70
```

### Keyboard Accessibility Score

```
Keyboard Accessibility = 100 - (Critical * 10) - (Serious * 5) - (Moderate * 2)

Örnek:
- Critical: 2
- Serious: 5
- Moderate: 8
- Score = 100 - (2*10) - (5*5) - (8*2) = 100 - 20 - 25 - 16 = 39
```

### Screen Reader Friendliness Score

```
SR Friendliness = 100 - (Name Issues * 5)

Örnek:
- Name calculation issues: 8
- Score = 100 - (8*5) = 60
```

### Focus Trap Risk Score

```
Focus Trap Risk:
- 0 trap: 100
- 1 trap: 70
- 2 traps: 40
- 3+ traps: 20
```

### Overall Behavioral Score

```
Overall = (Focus Efficiency * 0.20) +
          (Keyboard Accessibility * 0.25) +
          (SR Friendliness * 0.20) +
          (Focus Trap Risk * 0.20) +
          (Form Accessibility * 0.15)
```

---

## 🔧 Test Komutları

### Temel Klavye Testi

```bash
python3 /Users/sarper/.openclaw/workspace/skills/accessmind/scripts/accessmind-behavioral-navigator.py \
  --url https://example.com \
  --steps 50 \
  --mode smart \
  --html
```

### Form Odaklı Test

```bash
python3 /Users/sarper/.openclaw/workspace/skills/accessmind/scripts/accessmind-behavioral-navigator.py \
  --url https://example.com/form \
  --steps 30 \
  --mode form \
  --html
```

### Landmark Odaklı Test

```bash
python3 /Users/sarper/.openclaw/workspace/skills/accessmind/scripts/accessmind-behavioral-navigator.py \
  --url https://example.com \
  --steps 20 \
  --mode landmark \
  --html
```

### Başlık Odaklı Test

```bash
python3 /Users/sarper/.openclaw/workspace/skills/accessmind/scripts/accessmind-behavioral-navigator.py \
  --url https://example.com \
  --steps 15 \
  --mode heading \
  --html
```

---

## 📋 Rapor Analizi

### JSON Rapor Yapısı

```json
{
  "url": "https://example.com",
  "timestamp": "2026-03-25T11:00:00",
  "navigation_mode": "smart",
  "statistics": {
    "total_steps": 50,
    "focus_changes": 50,
    "unique_elements": 42,
    "interactive_elements": 38,
    "visible_focus_count": 35,
    "missing_focus_count": 15,
    "focus_visible_support": 70
  },
  "focus_traps": [],
  "screen_reader": {
    "announcements_count": 28,
    "live_regions_count": 3
  },
  "form_tests": [
    {
      "name": "Form 1 Interaction",
      "passed": true,
      "wcag_criteria": ["1.3.1", "3.3.1", "3.3.2", "4.1.2"]
    }
  ],
  "shortcut_tests": [
    {
      "name": "Skip Link Test",
      "passed": true,
      "expected": "Skip link visible",
      "actual": "Skip link found: Ana içeriğe geç"
    }
  ],
  "wcag_violations": [
    {
      "wcag": "2.4.7",
      "severity": "serious",
      "message": "Focus göstergesi yok: button - Submit",
      "element": "step_23"
    }
  ],
  "violations_by_criterion": {
    "2.4.7": 8,
    "4.1.2": 4
  },
  "scores": {
    "focus_efficiency": 70,
    "keyboard_accessibility": 72,
    "screen_reader_friendliness": 85,
    "focus_trap_risk": 100,
    "form_accessibility": 90,
    "overall_behavioral_score": 78
  },
  "recommendations": [
    "⚠️ 15 element'te focus göstergesi eksik. :focus-visible CSS sınıfı ekleyin.",
    "📌 2.4.7 Focus Visible: Tüm focusable element'lere görünür focus göstergesi ekleyin."
  ]
}
```

### HTML Rapor Özellikleri

- Skor kartları (renk kodlu: kırmızı < 50, turuncu < 80, yeşil >= 80)
- İstatistik grid'i
- Focus tuzağı listesi
- WCAG ihlalleri (severity bazlı renk)
- Öneriler listesi

---

## 🎓 En İyi Uygulamalar

### Focus Visible

```css
/* Modern focus-visible */
:focus-visible {
  outline: 3px solid #3182ce;
  outline-offset: 2px;
}

/* Fallback */
:focus {
  outline: 3px solid #3182ce;
  outline-offset: 2px;
}

/* Mouse için focus'u gizle */
:focus:not(:focus-visible) {
  outline: none;
}
```

### Skip Link

```html
<body>
  <a href="#main-content" class="skip-link">
    Ana içeriğe geç
  </a>
  
  <header>...</header>
  
  <main id="main-content">
    <!-- Ana içerik -->
  </main>
</body>
```

```css
.skip-link {
  position: absolute;
  top: -100px;
  left: 0;
  background: #3182ce;
  color: white;
  padding: 8px 16px;
  z-index: 1000;
}

.skip-link:focus {
  top: 0;
}
```

### ARIA Live Region

```html
<!-- Hata mesajları için -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
  <!-- Dinamik hata mesajları -->
</div>

<!-- Yükleme durumu için -->
<div aria-live="assertive" aria-busy="true">
  <!-- Yükleme durumu -->
</div>
```

### Form Label

```html
<!-- Doğru -->
<label for="email">E-posta</label>
<input type="email" id="email" aria-describedby="email-hint">
<span id="email-hint">Geçerli bir e-posta adresi girin</span>

<!-- ARIA ile -->
<input type="email" aria-label="E-posta" aria-describedby="email-hint">

<!-- Group -->
<fieldset>
  <legend>İletişim Tercihleri</legend>
  <label><input type="checkbox"> E-posta</label>
  <label><input type="checkbox"> SMS</label>
</fieldset>
```

---

## 📖 Kaynaklar

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [Understanding Focus Visible](https://www.w3.org/WAI/WCAG21/Understanding/focus-visible.html)
- [Understanding No Keyboard Trap](https://www.w3.org/WAI/WCAG21/Understanding/no-keyboard-trap.html)
- [Focus-Visible Polyfill](https://github.com/WICG/focus-visible)