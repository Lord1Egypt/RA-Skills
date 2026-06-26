# AccessMind - WCAG-EM & ACT Rules İşlem Akışı

## W3C Standartları Entegrasyonu

### 1. WCAG-EM (Website Accessibility Conformance Evaluation Methodology)

**Kaynak:** https://www.w3.org/TR/WCAG-EM/

#### 5 Adım Metodoloji

```
┌─────────────────────────────────────────────────────────────┐
│  WCAG-EM 5 ADIM                                             │
├─────────────────────────────────────────────────────────────┤
│  1. Define Scope         → Kapsam Tanımla                  │
│  2. Explore Website      → Site Keşfi                      │
│  3. Select Representative Pages → Temsilci Sayfalar       │
│  4. Evaluate Conformance → Uyumluluk Değerlendirmesi       │
│  5. Report Findings      → Bulguları Raporla               │
└─────────────────────────────────────────────────────────────┘
```

#### Adım 1: Define Scope (Kapsam Tanımla)

```python
scope = {
    "website": "https://www.arcelik.com.tr",
    "evaluation_target": "WCAG 2.2 Level AA",
    "evaluation_scope": "Full website",
    "languages": ["tr", "en"],
    "technologies": ["HTML", "CSS", "JavaScript", "WAI-ARIA"],
    "context": "E-commerce website"
}
```

**Çıktı:**
- Hedef website URL
- WCAG versiyon ve seviye
- Kapsam (tüm site / bölüm)
- Teknolojiler listesi
- Bağlam/sector

#### Adım 2: Explore Website (Site Keşfi)

**Yöntem:**
- Ana navigasyon crawl
- Sitemap parse
- İç link discovery

**Çıktı:**
- Bulunan sayfalar listesi
- Site hiyerarşisi
- Navigation structure

```python
explored_pages = [
    {"text": "Ana Sayfa", "href": "/"},
    {"text": "Ürünler", "href": "/urunler/"},
    {"text": "Kurumsal", "href": "/kurumsal/"},
    # ...
]
```

#### Adım 3: Select Representative Pages (Temsilci Sayfalar)

**Seçim Kriterleri (W3C Standardı):**

1. **Different purposes** - Farklı amaçlar
   - Homepage (entry point)
   - Catalog (e-commerce)
   - Support (forms, help)
   - Content (text-heavy)

2. **Essential functionality** - Temel işlevsellik
   - Navigation
   - Search
   - Forms
   - Checkout

3. **Different technologies** - Farklı teknolojiler
   - Static HTML
   - Dynamic JavaScript
   - ARIA widgets
   - Multimedia

4. **Different content types** - Farklı içerik tipleri
   - Text
   - Images
   - Video
   - Forms
   - Tables

**Örnek Representative Pages:**

```python
representative_pages = [
    {"path": "/", "type": "Homepage", "reason": "Entry point"},
    {"path": "/urunler/", "type": "Catalog", "reason": "E-commerce core"},
    {"path": "/destek/", "type": "Support", "reason": "Forms"},
    {"path": "/kurumsal/", "type": "Information", "reason": "Text content"},
    {"path": "/surdurulebilirlik/", "type": "Content", "reason": "Long-form"}
]
```

#### Adım 4: Evaluate Conformance (Uyumluluk Değerlendirmesi)

**WCAG-EM Conformance Requirements:**

1. ✅ **Full page** - Alternate version değil
2. ✅ **Only WCAG technologies** - Accessibility-supported tech
3. ✅ **Accessibility supported** - Browser/AT desteği
4. ✅ **No alternate version** - Tek version

**Evaluation Process:**

```python
for page in representative_pages:
    # Run Axe-core WCAG 2.2 AA
    axe_results = axe.run({
        runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']
    })
    
    # Group by WCAG criterion
    wcag_criteria = group_by_criterion(axe_results.violations)
    
    # Check WCAG-EM requirements
    conformance_status = check_wcagem_requirements(page, axe_results)
```

**Çıktı:**
- Her sayfa için violation count
- WCAG criterion grouping
- Conformance status (pass/fail)
- WCAG-EM requirements check

#### Adım 5: Report Findings (Bulguları Raporla)

**WCAG-EM Report Structure:**

```json
{
    "wcag_em_version": "1.0",
    "evaluation_id": "abc123",
    "scope": {...},
    "representative_pages": [...],
    "conformance": {
        "wcag_version": "2.2",
        "wcag_level": "AA",
        "results": [...],
        "overall_status": "fail"
    },
    "additional_info": {
        "tools_used": ["Axe-core", "Playwright"],
        "limitations": ["Automated tools limited"],
        "wcag_em_requirements_check": {...}
    },
    "recommendations": [...]
}
```

**Rapor Bölümleri:**
1. Scope Definition
2. Exploration Summary
3. Representative Pages
4. Conformance Evaluation
5. Additional Information
6. Recommendations

---

### 2. ACT Rules (Accessibility Conformance Testing)

**Kaynak:** https://www.w3.org/WAI/standards-guidelines/act/rules/about/

#### ACT Rule Format (W3C Standard)

```json
{
    "@context": "https://www.w3.org/WAI/act-rules/context.jsonld",
    "@type": "act-rule",
    "id": "accessmind-contrast-001",
    "name": "Color Contrast Ratio",
    "description": "Text has sufficient color contrast ratio",
    "wcag": ["1.4.3"],
    "source": "WCAG 2.2",
    "status": "draft",
    "type": "atomic",
    "requirements": [
        {"step": 1, "procedure": "Extract foreground color"},
        {"step": 2, "procedure": "Extract background color"},
        {"step": 3, "procedure": "Calculate contrast ratio"},
        {"step": 4, "procedure": "Compare with WCAG threshold"}
    ],
    "expected_result": "Contrast ratio >= 4.5:1",
    "assumptions": ["Colors are defined in CSS"],
    "accessibility_supported": true
}
```

#### AccessMind ACT Rules (10 Standart Rule)

| Rule ID | Name | WCAG | Description |
|---------|------|------|-------------|
| contrast-001 | Color Contrast Ratio | 1.4.3 | 4.5:1 normal, 3:1 large |
| alt-001 | Image Alternative Text | 1.1.1 | All images have alt |
| label-001 | Form Input Label | 1.3.1 | All inputs have labels |
| keyboard-001 | Keyboard Accessibility | 2.1.1 | Keyboard accessible |
| heading-001 | Heading Hierarchy | 1.3.1 | Logical heading order |
| link-001 | Link Purpose | 2.4.4 | Link text meaningful |
| focus-001 | Focus Indicator | 2.4.7 | Focus visible |
| skip-001 | Skip Link | 2.4.1 | Skip to main content |
| lang-001 | Language Declaration | 3.1.1 | Page language declared |
| aria-001 | ARIA Attributes | 4.1.2 | ARIA valid |

#### Test Procedure Format

```markdown
Rule: contrast-001
Step 1: Extract foreground color
Step 2: Extract background color
Step 3: Calculate contrast ratio
Step 4: Compare with WCAG threshold
Expected Result: Contrast ratio >= 4.5:1 (normal) or 3:1 (large)
Assumptions: Colors are defined in CSS
```

#### EARL Export (Evaluation and Report Language)

**Kaynak:** https://www.w3.org/ns/earl

```json
{
    "@context": "https://www.w3.org/ns/earl",
    "@type": "earl:assertion",
    "earl:assertor": {
        "@type": "earl:assertor",
        "foaf:name": "AccessMind Enterprise",
        "foaf:homepage": "https://accessmind.example.com"
    },
    "earl:subject": {
        "@type": "earl:testSubject",
        "dc:title": "https://www.arcelik.com.tr",
        "dc:source": "https://www.arcelik.com.tr"
    },
    "earl:test": {
        "@type": "earl:testCriterion",
        "dc:title": "AccessMind ACT Rules Suite",
        "dc:description": "ACT Rules Test Suite"
    },
    "earl:outcome": {
        "@type": "earl:outcomeValue",
        "rdf:value": "earl:passed" | "earl:failed"
    },
    "earl:mode": "earl:automatic",
    "dc:created": "2026-03-24T09:15:00"
}
```

---

### 3. Skill Entegrasyonu

#### Script Dosyaları

```
skills/accessmind/scripts/
├── comprehensive-a11y-audit.py    # 5 modül (WCAG + Klavye + SR + Kontrast + Görsel)
├── wcag-em-evaluator.py           # WCAG-EM 5 adım
└── act-rules-engine.py            # ACT Rules + EARL
```

#### Kullanım

```bash
# 5 Modül KAPOZLU Denetim
python3 skills/accessmind/scripts/comprehensive-a11y-audit.py

# WCAG-EM Metodoloji
python3 skills/accessmind/scripts/wcag-em-evaluator.py

# ACT Rules Test Suite
python3 skills/accessmind/scripts/act-rules-engine.py
```

#### Çıktı Dosyaları

```
audits/
├── arcelik_comprehensive_YYYYMMDD_HHMMSS.html  # 5 modül
├── arcelik_comprehensive_YYYYMMDD_HHMMSS.json
├── wcag-em_{id}_YYYYMMDD_HHMMSS.html           # WCAG-EM
├── wcag-em_{id}_YYYYMMDD_HHMMSS.json
├── act-rules_YYYYMMDD_HHMMSS.html              # ACT Rules
└── act-rules_YYYYMMDD_HHMMSS.json
```

---

### 4. W3C Uyumluluk Matrisi

| Standart | AccessMind | Durum |
|----------|------------|-------|
| **WCAG-EM 5 Adım** | ✅ Tam | 5/5 adım implement |
| **Representative Pages** | ✅ 5 sayfa | Different purpose/tech/content |
| **Conformance Requirements** | ✅ 4/4 | Full page, WCAG tech, supported |
| **ACT Rules Format** | ✅ 10 rule | Atomic, testable, WCAG mapped |
| **Test Procedures** | ✅ Step-by-step | 4 step per rule |
| **Expected Results** | ✅ Clear | Pass/fail criteria |
| **Assumptions** | ✅ Documented | Per rule |
| **EARL Export** | ✅ Available | W3C standard format |
| **Manual Testing** | ⚠️ Kısmi | Checklist var, human required |
| **User Involvement** | ❌ Eksik | Recommendation only |

---

### 5. Sektör Standardı Karşılaştırması

| Özellik | Önceki | Şimdi (WCAG-EM + ACT) |
|---------|--------|----------------------|
| Metodoloji | ❌ Yok | ✅ WCAG-EM 5 adım |
| Rule Format | ❌ Informal | ✅ ACT Rules (W3C) |
| Rapor Format | ⚠️ HTML/JSON | ✅ WCAG-EM + EARL |
| Test Procedures | ⚠️ Implicit | ✅ Explicit steps |
| Conformance Check | ⚠️ Partial | ✅ WCAG-EM requirements |
| Representative Pages | ✅ 5 sayfa | ✅ W3C criteria |
| EARL Export | ❌ Yok | ✅ W3C standard |

---

### 6. İyileştirme Önerileri

#### Kısa Vadeli (✅ Tamamlandı)
- ✅ WCAG-EM 5 adım implement
- ✅ ACT Rules format (10 rule)
- ✅ EARL export
- ✅ Representative page criteria

#### Orta Vadeli (📋 Planlandı)
- [ ] Manual test checklist
- [ ] User testing guide
- [ ] WCAG-EM Report Tool integration
- [ ] ACT Rules expansion (20+ rule)

#### Uzun Vadeli (🔮 Gelecek)
- [ ] Disabled user testing integration
- [ ] Combined expertise workflow
- [ ] Full WCAG-EM certification
- [ ] Enterprise compliance reporting

---

### 7. Kaynaklar

- **WCAG-EM:** https://www.w3.org/TR/WCAG-EM/
- **WCAG-EM Report Tool:** https://www.w3.org/WAI/eval/report-tool/
- **ACT Rules:** https://www.w3.org/WAI/standards-guidelines/act/rules/about/
- **EARL:** https://www.w3.org/ns/earl
- **Evaluation Tools:** https://www.w3.org/WAI/test-evaluate/tools/
- **Combined Expertise:** https://www.w3.org/WAI/test-evaluate/combined-expertise/
- **Involving Users:** https://www.w3.org/WAI/test-evaluate/involving-users/

---

**AccessMind Enterprise**  
*WCAG-EM + ACT Rules W3C Standartları*  
*v1.0 - 2026-03-24*
