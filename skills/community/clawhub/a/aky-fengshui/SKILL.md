---
name: aky-fengshui
description: "Comprehensive Feng Shui (风水) analysis skill integrating three major schools: Eight Mansions (八宅法), Flying Stars (玄空飞星), and Forms School (形峦派). Supports life trigram calculation, house-person compatibility, directional analysis, flying star chart interpretation, landscape assessment, interior layout recommendations, and Feng Shui cures. Trigger when users ask about: Feng Shui, 风水, 八宅, 飞星, 形峦, house analysis, office layout, 家居风水, 办公室风水, 本命卦, direction analysis, geomancy, 方位, 化煞, 四灵兽, or any space energy assessment."
---

# Aky Feng Shui (综合风水分析)

Comprehensive Feng Shui assessment integrating **八宅法** (Eight Mansions), **玄空飞星** (Flying Stars), and **形峦派** (Forms School) into a unified analysis framework.

> ⚠️ **DISCLAIMER**: This skill provides traditional Feng Shui analysis for cultural and reference purposes. Results should be taken as guidance, not deterministic predictions.

---

## I. Three Schools Integration

| School | Focus | Best For |
|:------:|:------|:---------|
| **八宅法** (Eight Mansions) | Person-house compatibility, directional auspiciousness | Home buyers, office selection, directional guidance |
| **玄空飞星** (Flying Stars) | Time-sensitive energy, period analysis, star combinations | Existing building diagnosis, yearly adjustments |
| **形峦派** (Forms School) | Physical forms, landscape, shapes of surroundings | Site selection, external environment assessment |

**Integrated approach:** Use all three for a complete picture. Forms School first (external), then Flying Stars (time energy), then Eight Mansions (person-house matching).

---

## II. Core Workflows

### Workflow A: Complete House Analysis (完整宅分析)

```
Step 1: Collect basic information
    ├── House: address, orientation (坐向), year built, floor plan
    ├── Residents: birth years, genders, relationships
    └── Concerns: what the user wants to improve

Step 2: External Environment — Forms School (形峦)
    ├── Check surrounding landscape / Four Animals (四灵兽)
    ├── Identify any form-based sha (形煞)
    ├── Access roads and approach
    └── See references/forms-school.md

Step 3: Time Energy — Flying Stars (玄空飞星)
    ├── Determine the Period (元运) based on year built
    ├── Period 9 (2024-2043) — current period
    ├── Generate flying star chart for the house
    ├── Identify auspicious/inauspicious star combinations
    └── See references/flying-stars.md

Step 4: Person-House Compatibility — Eight Mansions (八宅法)
    ├── Calculate life trigram (本命卦) for each resident
    ├── Classify house into trigram type (坐山 / 向)
    ├── Check East/West group compatibility
    ├── Assess each room position vs. 8 directions
    └── See references/eight-mansions.md

Step 5: Interior Assessment — Basics (室内)
    ├── Room-by-room analysis (door, bedroom, kitchen, study, etc.)
    ├── Five element balance check
    ├── Key furniture placement
    └── See references/feng-shui-basics.md

Step 6: Recommendations
    ├── Priority issues to address
    ├── Specific cures and enhancements (化煞与催旺)
    ├── Room usage suggestions
    └── Element adjustments (color, shape, material)
```

### Workflow B: Person-Floor Plan Compatibility Check (人与宅适配)

```
Step 1: Person's Life Trigram (本命卦)
    ├── Gender + Birth year → formula calculation
    ├── East Group (东四命) or West Group (西四命)
    └── See references/eight-mansions.md §1-2

Step 2: House Type Classification
    ├── Sitting direction → house trigram
    ├── East House (东四宅) or West House (西四宅)
    └── See references/eight-mansions.md §5

Step 3: Compatibility Score
    ├── Same group → 🟢 Good match
    ├── Different group → 🟡 Some adjustments needed
    └── Worst direction → 🔴 Major element mismatch

Step 4: Room-by-Room Optimization
    ├── Identify 4 auspicious + 4 inauspicious directions
    ├── Place important rooms in good directions
    ├── Place utility rooms in bad directions (to suppress)
    └── See references/eight-mansions.md §6
```

### Workflow C: Flying Star Annual Update (飞星流年)

```
Step 1: Determine current year
    ├── Current year central star → from period + year table
    └── See references/flying-stars.md §5

Step 2: Identify yearly afflictions
    ├── 五黄 (5 Yellow) location → avoid disturbance
    ├── 二黑 (2 Black) location → apply metal remedy
    ├── 三煞 (Three Sha) → avoid renovation direction
    └── See references/flying-stars.md §5-6

Step 3: Activate favorable stars
    ├── Enhance 8 White (八白) for wealth
    ├── Enhance 9 Purple (九紫) for relationships/fame
    └── See references/flying-stars.md §6
```

---

## III. Reference Resources

| File | Content | When to Load |
|------|---------|:-------------|
| references/eight-mansions.md | Life trigram calculation, 8 directions table, room placement | Person-house compatibility |
| references/flying-stars.md | 9 periods, star chart creation, combinations, annual stars | Time-sensitive analysis |
| references/forms-school.md | Four animals, landscape analysis, form sha | External environment assessment |
| references/feng-shui-basics.md | Five elements, directions, interior rules, cures, checklist | Interior layout recommendations |

---

## IV. Output Format

For a full house analysis (Workflow A), structure output as:

```
## Feng Shui Analysis — [Building/Site Name]

### 1. External Environment (形峦)
| Direction | Feature | Assessment |
|:---------:|:--------|:-----------|
| Back (玄武) | [description] | 🟢/🟡/🔴 |
| Front (朱雀) | [description] | 🟢/🟡/🔴 |
| Left (青龙) | [description] | 🟢/🟡/🔴 |
| Right (白虎) | [description] | 🟢/🟡/🔴 |
**Form Sha identified:** [list, if any]

### 2. Time Energy (玄空飞星)
**Period:** [Period number and years]
**Current Year Central Star:** [Star number and meaning]
**Key Star Combinations:**
- [Location]: [Stars] → [interpretation]

### 3. Person-House Compatibility (八宅)
**Resident 1:** [Life trigram, group, birth year]
**House:** [Sitting, facing, house trigram, group]
**Compatibility:** 🟢/🟡/🔴

| Room | Current | Recommended | Notes |
|:----|:--------|:------------|:------|
| Main door | [direction] | [direction] | [adjustment] |
| Master bedroom | [direction] | [direction] | [adjustment] |
| Kitchen | [direction] | [direction] | [adjustment] |

### 4. Recommendations (建议)
**Priority 1:** [most critical issue] — [cure/remedy]
**Priority 2:** [next issue] — [cure/remedy]
**Priority 3:** [enhancement] — [method]

**Element adjustments:** [colors, materials, shapes to introduce/avoid]
```

---

## V. Key Principles

1. **Form comes first (形峦为先)** — Physical shapes dominate over abstract calculations
2. **Time matters (时运为要)** — Energy changes with each period; what was good in Period 8 may not be good in Period 9
3. **Person-centered (以人为本)** — The same house can be good for one person and poor for another
4. **Balance over perfection (中和为上)** — Perfect Feng Shui rarely exists; aim for harmony and balance
5. **Practical before mystical (实用优先)** — A cluttered room will have bad Feng Shui regardless of theory
6. **The door is key (大门为要)** — The main door determines how qi enters and flows

---

## VI. Quick Start

| What Do You Want? | Use Workflow | Load References |
|:------------------|:------------:|:----------------|
| "这个房子风水怎么样？" | A — Complete house analysis | All |
| "我适合住什么方向的房子？" | B — Person compatibility | eight-mansions.md |
| "今年办公室要注意什么？" | C — Flying Star annual | flying-stars.md |
| "窗外有尖角对着怎么办？" | A — Form sha identification | forms-school.md + feng-shui-basics.md |
| "卧室应该怎么布置？" | A — Interior layout | feng-shui-basics.md |
