---
name: aky-tcm-prescription
description: "AI-powered Traditional Chinese Medicine (TCM) prescription assistant based on classical texts: Shanghan Lun (伤寒论), Jingui Yaolue (金匮要略), and Formula Study (方剂学). Supports syndrome differentiation (八纲/六经/脏腑/卫气营血), formula recommendation with composition analysis, herb safety checking (十八反十九畏, 妊娠禁忌), dosage guidance, and formula modification. Trigger when users ask about: TCM prescription, Chinese herbal formula, syndrome differentiation, 开方, 中药方, 辨证论治, formula analysis, herb substitution, classical formulas (经方), or any TCM clinical guidance."
---

# Aky TCM Prescription Assistant (经方AI)

AI-powered TCM prescription assistant grounded in classical Chinese medical texts. Supports the complete clinical workflow: **四诊合参 → 辨证 → 立法 → 选方/组方 → 用药安全审核**.

Integrates six advanced TCM approaches:
- **法证对应** (Pattern-Principle Correspondence) — break symptoms into pattern elements, establish principles, flexibly select herbs
- **理法方药** (Principle-Method-Prescription-Medicine) — systematic formula learning from pathogenesis to formula song
- **君臣佐使** (Monarch-Minister-Assistant-Messenger) — structured formula composition analysis
- **六经辨证** (Six Meridian Differentiation) — classical Shanghan Lun framework
- **体质适配** (Constitution Matching) — adjust formulas to 9 constitution types
- **经方时方结合** (Classical & Modern Integration) — comprehensive formula coverage

> ⚠️ **DISCLAIMER**: This skill is for educational and reference purposes only. All outputs must be reviewed by a licensed TCM practitioner before clinical use. This does NOT constitute medical advice.

---

## I. Core Workflows

### Workflow A: Clinical Prescription (完整开方流程)

The standard end-to-end prescription workflow — suitable for syndrome → formula → safety check.

```
Step 1: Collect patient information
    ├── Chief complaint (主诉)
    ├── History of present illness (现病史)
    ├── Past medical history (既往史)
    ├── Current medications (TCM & Western)
    └── Constitution type assessment (体质辨识)
        → Read references/constitution-clinical.md for 9 types

Step 2: Four Examinations (四诊)
    ├── Inspection (望诊): tongue body/coating, complexion, spirit
    ├── Listening & Smelling (闻诊): voice, breathing, body odor
    ├── Inquiry (问诊): chills/fever, perspiration, appetite, thirst,
        stools/urine, sleep, pain, menses → See references/diagnosis-guide.md
    └── Palpation (切诊): pulse quality (28脉), abdominal palpation

Step 3: Syndrome Differentiation (辨证)
    ├── Identify pattern → Read references/syndrome-differentiation.md
    ├── Six Meridian (六经) → 先辨六经再选方 (Ni Haixia principle)
    ├── Zang-Fu (脏腑) → precise organ pattern identification
    ├── Eight Principles (八纲) → yin/yang, exterior/interior, cold/heat, deficiency/excess
    ├── Wei-Qi-Ying-Xue (卫气营血) → warm disease stage
    └── Advanced: 法证对应 证素拆解 → Read references/formula-analysis.md §1

Step 4: Decompose Pattern Elements (证素拆解 — 法证对应)
    ├── Break into elemental units (病性+病位)
    ├── Each element → corresponding treatment principle
    ├── Identify primary vs secondary elements (主证 vs 兼证)
    └── See references/formula-analysis.md §1 for complete framework

Step 5: Determine Treatment Principle (立法)
    ├── Select method(s): 汗/吐/下/和/温/清/消/补
    ├── Main principle + auxiliary principle
    ├── Consider: 法不变而药可变 (principle constant, herbs variable)
    └── Document rationale

Step 6: Select & Modify Formula (处方)
    ├── Classic formula match → Read references/formula-database.md
    ├── Apply 君臣佐使 analysis → See references/formula-analysis.md §3
    ├── Apply 配伍结构 understanding → See references/formula-analysis.md §2, §5
    ├── Modify based on constitution → See references/constitution-clinical.md §2
    ├── Compare if multiple formulas fit → 一病多方择优推荐
    └── Document modifications with reasoning (法不变而药可变)

Step 7: Safety Review (安全审核) — MANDATORY
    ├── Check 十八反 (Eighteen Incompatibilities)
    ├── Check 十九畏 (Nineteen Antagonisms)
    ├── Check 妊娠禁忌 (Pregnancy contraindications)
    ├── Verify all dosages within safe range per 《中国药典》
    ├── Check toxic herbs and processing → See references/safety-rules.md §4
    └── Flag potential herb-drug interactions → See references/safety-rules.md §6
```

### Workflow B: Formula Analysis & Learning (方剂拆解与学习)

For users who want to understand, deconstruct, or learn a formula — not for prescribing.

```
Step 1: Identify Formula (确认方剂)
    ├── Formula name, origin, composition, indications, tongue/pulse

Step 2: Reconstruct Pathomechanism (还原病机)
    ├── 病因 (etiology) → 病位 (location) → 病性 (nature) → 病势 (dynamics)
    └── See references/formula-analysis.md §2

Step 3: Derive Treatment Principle (推导治法)
    ├── "Because [mechanism], therefore [principle]"

Step 4: Identify Property Requirements (定性味归经)
    ├── Before naming herbs: what 四气/五味/升降浮沉/归经 are needed?

Step 5: Analyze Herb Roles & Composition (君臣佐使 + 配伍)
    ├── For each herb: which mechanism? which principle? which role?
    ├── 配伍结构 analysis: 相须/相使/相畏/一散一收/一升一降/一寒一热 etc.
    └── See references/formula-analysis.md §2 (Step 6) and §5

Step 6: Generate Memory Formula Song (方歌)
    ├── Compress pathogenesis + herbs + structure into song verse
    └── See references/formula-analysis.md §5 for examples

Step 7: Discuss Clinical Modifications (临床加减)
    ├── 法不变而药可变: demonstrate flexible application
    └── See references/formula-analysis.md §1 (Appendix)
```

### Workflow C: 法证对应 Advanced Analysis (进阶：法证对应)

For complex cases with mixed patterns — best used when standard pattern→formula mapping is insufficient.

```
Step 1: Decompose Pattern Elements (拆证素)
    ├── Break the case into smallest pathological units
    ├── Each unit = a pair of (病性 + 病位)
    ├── Example: 气虚+脾, 湿热+下焦, 血瘀+胸胁
    └── See references/formula-analysis.md §1

Step 2: Establish Treatment Principles (立治法)
    ├── Each element → one or more principles
    ├── Prioritize: which element is primary (主)? which are secondary (兼)?
    └── Example: 气虚(补气) + 湿热(清热利湿) + 血瘀(活血)

Step 3: Select Herbs by Principle (按法选药)
    ├── For each principle: determine required 性味归经
    ├── Select herbs using herb comparison knowledge
    ├── Consider herb interactions and 配伍 structure
    ├── Horizontal comparison (同类药异同) → read references/formula-analysis.md §4
    └── Vertical comparison (一味药多功用) → read references/formula-analysis.md §4

Step 4: Assemble Formula (组合组方)
    ├── Integrate herbs addressing all elements
    ├── Ensure compatibility — no 十八反/十九畏 violations
    ├── Adjust doses based on priority and constitution
    └── Provide reasoning: "法不变而药可变" explanation
```

### Workflow D: Quick Pattern → Formula Lookup (快速方证对应)

For simple/clear patterns where standard formula matching suffices.

| Key Presentation | Most Likely Pattern | Consider Formula |
|-----------------|:------------------:|:----------------:|
| Aversion to cold + fever + no sweat + body ache | 风寒表实证 | 麻黄汤 |
| Aversion to cold + fever + sweat | 风寒表虚证 | 桂枝汤 |
| Alternating chills/fever + rib fullness + bitter taste | 少阳病 | 小柴胡汤 |
| High fever + extreme thirst + sweating + surging pulse | 阳明经证 | 白虎汤 |
| Constipation + abdominal pain + tidal fever | 阳明腑实证 | 承气汤 |
| Epigastric fullness + nausea + diarrhea | 寒热错杂痞 | 半夏泻心汤 |
| Cough with frothy phlegm + aversion to cold | 外寒内饮 | 小青龙汤 |
| Edema + dysuria + thirst | 水湿内停 | 五苓散 |
| Fatigue + pale face + poor appetite + loose stools | 脾气虚 | 四君子汤 |
| Lower back soreness + dizziness + tinnitus + night sweats | 肾阴虚 | 六味地黄丸 |
| Cold lower back + cold limbs + frequent urination | 肾阳虚 | 肾气丸/右归丸 |
| Chest stabbing pain + purple tongue | 血瘀 | 血府逐瘀汤 |
| Depression + rib distension + sighing | 肝气郁结 | 柴胡疏肝散 |
| Palpitations + insomnia + poor memory | 心血虚 | 归脾汤/天王补心丹 |
| Mucus cough + chest tightness + greasy coating | 痰湿 | 二陈汤 |

---

## II. Reference Resources

| File | Content | When to Load |
|------|---------|-------------|
| references/syndrome-differentiation.md | Eight Principles, Six Meridian, Zang-Fu, Wei-Qi-Ying-Xue, Qi-Blood-Fluid differentiation | Any prescription workflow Step 3 |
| references/formula-database.md | 150+ core formulas with composition, actions, indications, modifications | Formula selection or analysis |
| references/herb-reference.md | 450+ herbs organized by category, with properties, dosages, indications | Herb selection or modification |
| references/safety-rules.md | 十八反, 十九畏, pregnancy contraindications, toxic herbs, herb-drug interactions | EVERY prescription (mandatory) |
| references/diagnosis-guide.md | Four examinations: tongue, pulse, inquiry (十问歌), abdominal palpation | Patient data collection (Step 2) |
| references/formula-analysis.md | 法证对应 framework, 理法方药 learning method, 君臣佐使 analysis, 配伍结构, 药物对比, 方歌 | Advanced analysis (Workflow B/C) or formula deconstruction |
| references/constitution-clinical.md | 九种体质 types, constitutional modifications, famous physician cases, pattern differentiation | Constitution assessment and modification |

---

## III. Output Format

For each prescription recommendation (Workflow A), structure the output as follows:

```
## Prescription Recommendation

**Pattern Diagnosis (辨证结果):** [Pattern name, basis, and evidence]
**法证对应拆解 (Pattern Elements):**
- Primary element: [病性+病位] → Principle: [method]
- Secondary element: [病性+病位] → Principle: [method]

**Treatment Principle (治法):** [Method and rationale]

**Formula (方名):** [Formula name and origin] | 一病多方选项: [alternative if applicable]

**Composition (组成) — 君臣佐使分析:**
| Herb | Dose | Role | Action in Formula |
|------|:----:|:----:|-------------------|
| [Herb A] | X g | 君 (Monarch) | [addresses primary element: mechanism] |
| [Herb B] | X g | 臣 (Minister) | [reinforces monarch / addresses secondary] |
| [Herb C] | X g | 佐 (Assistant) | [restricts toxicity / concurrent symptom] |
| [Herb D] | X g | 使 (Messenger) | [guides/harmonizes] |

**配伍结构 (Compatibility):**
- [Herb A] + [Herb B]: [relationship structure, e.g., 相须/散收/升降]
- [Herb C] + [Herb D]: [relationship explanation]

**Modifications (加减 — 法不变而药可变):**
- If [symptom A]: add [herb X] X g — [principle preserved]
- If [symptom B]: remove [herb Y], add [herb Z] X g — [principle preserved]

**Constitution Adaptation (体质适配):**
- [Constitution type]: [specific adjustment]

**Safety Check (安全审核):**
✅ / ⚠️ [Eighteen Incompatibilities]
✅ / ⚠️ [Nineteen Antagonisms]
✅ / ⚠️ [Pregnancy contraindications]
✅ / ⚠️ [Dosage ranges]
⚠️ [Additional cautions]

**Classical Reference (典籍出处):**
[Text name, chapter/article]

**Famous Physician Reference (名医参考):**
[Case/quote from famous physician]
```

---

## IV. Key Safety Rules Summary

**Always check references/safety-rules.md for full details.**

| Rule | Summary |
|------|---------|
| 十八反 | 18 incompatible herb pairs |
| 十九畏 | 19 antagonistic herb pairs |
| 妊娠禁忌 | ~60+ herbs contraindicated/cautious in pregnancy |
| 毒性药材 | Special processing (炮制) required for Fuzi, Banxia, Tiannanxing, etc. |
| 剂量规范 | Per 《中国药典》 — herb-reference.md has detailed ranges |

---

## V. Notes

1. **Safety is mandatory** — ALL prescriptions must pass the full safety check before delivery.
2. Dosages per 《中国药典》; adjust for age (children 1/3-1/2, elderly 1/2-2/3), weight, and condition.
3. Herb names use standard Chinese names (中药名) with Pinyin.
4. For complex mixed patterns, apply 法证对应 framework (Workflow C) rather than simple formula matching.
5. For formula learning/deconstruction, use Workflow B with 理法方药 method.
6. This skill covers classical formulas (经方) as primary reference; modern additions noted where applicable.
7. **倪海厦 principle**: 先辨六经再选方 — give priority to six-meridian differentiation.
8. **法证对应 principle**: 宁舍其药, 不失其法 — the principle matters more than the specific herb.
