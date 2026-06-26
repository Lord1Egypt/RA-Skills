---
name: aky-iching-divination
description: "Comprehensive Yijing (I Ching / 易经) divination skill integrating the Zhouyi original text (周易本经), Plum Blossom Yishu (梅花易数) numerology methods, and traditional coin casting. Supports multiple divination methods: 3-coin casting, Plum Blossom numeric/time/character/object methods, with full hexagram generation (本卦/变卦/互卦), 体用生克 analysis, and detailed interpretation. Trigger when users ask about: divination, fortune-telling, Yijing, I Ching, 易经, 占卜, 起卦, 梅花易数, 爻, 卦象, 解卦, hexagram, 算命, 命理, or any fortune-telling or divination-related queries."
---

# Aky I Ching Divination (经易整合占卜)

Comprehensive Yijing (I Ching) divination skill integrating **周易本经** (Zhouyi original text), **梅花易数** (Plum Blossom Divination), and **金钱卦** (traditional coin method).

> ⚠️ **DISCLAIMER**: This skill is for cultural, educational, and entertainment purposes. All divination results should be taken as reflective guidance, not absolute predictions.

---

## I. Divination Methods

This skill supports **5 methods** for generating hexagrams:

| Method | Input | Process | Output |
|:------:|:------|:--------|:-------|
| **🍀 金钱卦** (3 Coins) | User mentally asks a question, tosses 3 coins 6 times | Convert head/tail results to lines | 本卦 + 变卦 from moving lines |
| **🔢 梅数起卦** (3 Numbers) | User provides 3 numbers (any range) | ÷8=upper trigram, ÷8=lower trigram, ÷6=moving line | 本卦 + 变卦 + 互卦 |
| **⏰ 时间起卦** (Time) | Current date/time or a specified time | Time→numbers→trigrams | 本卦 + 变卦 + 互卦 |
| **🀄 文字起卦** (Characters) | Chinese character(s) or word | Stroke count→trigrams | 本卦 + 变卦 + 互卦 |
| **💬 自由起卦** (Free Inquiry) | User describes their question naturally | AI selects the best method | Full divination reading |

---

## II. Core Workflow

### Standard Divination Session

```
Step 1: Clarify the Question
    ├── Guide the user to form a clear, sincere question
    ├── If the question is vague → help refine it
    └── If the question is inappropriate (same question repeatedly, harmful intent) → gently advise

Step 2: Choose Method
    ├── If user specifies a method → use that
    ├── If user gives 3 numbers → Plum Blossom numeric
    ├── If user gives coin results → coin method
    ├── If user gives a time → time method
    └── If user just asks freely → AI recommends based on context

Step 3: Generate Hexagram
    ├── 本卦 (Original hexagram) — current situation
    ├── 变卦 (Changing hexagram) — future outcome (if moving line exists)
    ├── 互卦 (Interplay hexagram) — hidden/process factors (Plum Blossom only)
    ├── Identify: upper/lower trigrams, hexagram name & number
    ├── If Plum Blossom: 体用 analysis
    └── Read 卦辞 from references/iching-core.md

Step 4: Detailed Interpretation
    ├── Hexagram meaning → references/iching-core.md
    ├── Moving line significance → read the 爻辞
    ├── 体用生克 → references/plum-blossom-methods.md §2 Step 5
    ├── Trigram correspondences → references/trigram-correspondences.md
    ├── Five elements interaction
    └── Synthesize into a coherent reading

Step 5: Output
    ├── Present hexagram(s) with name and symbol
    ├── Judgment (卦辞) interpretation
    ├── Answer to the specific question
    ├── Contextual advice and guidance
    └── Closing: Yijing wisdom
```

---

## III. Reference Resources

| File | Content | When to Load |
|------|---------|:-------------|
| references/iching-core.md | All 64 hexagrams — name, symbol, judgment, image, core meaning | Every divination (reading hexagrams) |
| references/plum-blossom-methods.md | Plum Blossom Yi Shu casting methods & 体用 analysis | When using Plum Blossom method |
| references/trigram-correspondences.md | 8 trigram properties, 万物类象, 五行生克 | When analyzing beyond the hexagram text |
| references/interpretation-guide.md | Coin method protocol, integration workflow, taboos | Setup procedures, general guidance |

---

## IV. Output Format

For each divination session, structure the output as:

```
## Divination Reading — [Question]

**Method:** [Coin / Plum Blossom / Time / Character]

### 本卦 (Original): [Name] ䷀
- Upper ☰ (Heaven) — Lower ☷ (Earth)
- 卦辞: [Judgment text with translation]
- Core meaning: [Summary]

[如果变卦:]
### 变卦 (Changing): [Name] ䷁
- Transformation direction: [what changes and why]

[如果梅花:]
### 互卦 (Interplay): [Name] ䷂

### 体用生克 Analysis
| Role | Trigram | Element | Represents |
|:----:|:-------:|:-------:|:-----------|
| 体 (You) | ☳ 震 | 木 | The questioner |
| 用 (Matter) | ☲ 离 | 火 | The question/subject |
| **Relationship:** [用生体 / 体克用 / etc.] | — | — | — |

### Moving Line (动爻)—[Line X]
[Line text and interpretation]

### Interpretation
[Comprehensive answer to the question, integrating all factors]

### Advice
[Practical guidance based on the hexagram]
```

---

## V. Key Principles

1. **Sincerity matters** — the quality of the reading reflects the quality of the question
2. **One question per session** — don't ask multiple questions in one casting
3. **Moving lines are the focus** — they show where change and guidance are needed
4. **No hexagram is purely good or bad** — each contains the seed of its opposite
5. **体用 is the core** — the relationship between subject and object determines outcome
6. **Respect the tradition** — this is rooted in thousands of years of Chinese philosophical tradition

---

## VI. Trigrams Quick Reference

| Trigram | Symbol | Element | Nature | Direction |
|:-------:|:------:|:-------:|:------:|:---------:|
| 乾 | ☰ | Metal | Heaven | NW |
| 兑 | ☱ | Metal | Lake | W |
| 离 | ☲ | Fire | Fire | S |
| 震 | ☳ | Wood | Thunder | E |
| 巽 | ☴ | Wood | Wind | SE |
| 坎 | ☵ | Water | Water | N |
| 艮 | ☶ | Earth | Mountain | NE |
| 坤 | ☷ | Earth | Earth | SW |

→ See references/trigram-correspondences.md for complete 万物类象 tables.
