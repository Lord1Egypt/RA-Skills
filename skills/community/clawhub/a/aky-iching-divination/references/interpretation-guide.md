# Interpretation Guide (解卦综合指南)

## 1. Methods of Divination

This skill supports multiple divination methods. The user can choose:

| Method | How to Use | Best For |
|:------:|:----------|:---------|
| **Traditional Coin Method** | Toss 3 coins 6 times → yang/yin lines | Traditional, grounded |
| **Plum Blossom Numbers** | Pick 3 numbers → auto-calculate trigrams | Quick, convenient |
| **Plum Blossom Time** | Current time → auto-calculate | Spontaneous |
| **Plum Blossom Character** | Chinese characters → stroke counts | Specific messages |
| **Free-text inquiry** | User describes situation → AI selects best method | Guided divination |

---

## 2. Complete Workflow

```
Step 1: Choose divination method
    ├── Coin method → toss virtual coins (see §3)
    ├── Three numbers → Plum Blossom numeric method
    ├── Time-based → auto from current time
    └── Free inquiry → AI recommends best method

Step 2: Generate hexagram
    ├── 本卦 (original hexagram)
    ├── 变卦 (changing hexagram) — if moving lines exist
    ├── 互卦 (interplay hexagram) — if plum blossom method
    └── Identify changing line(s) and position

Step 3: Present hexagram data
    ├── Hexagram name and symbol (䷀-䷿)
    ├── Upper trigram + lower trigram
    ├── 卦辞 (judgment) ← references/iching-core.md
    ├── 爻辞 (line text) for the changing line ← references/iching-core.md
    └── 体用 analysis (if plum blossom) ← references/plum-blossom-methods.md

Step 4: Interpretation
    ├── Core meaning of the hexagram
    ├── Position of the moving line and its specific guidance
    ├── 体用生克 relationship (if applicable)
    ├── Five element analysis (if applicable)
    └── 互卦 insight (hidden dimensions)

Step 5: Synthesize answer
    ├── Direct answer to the question
    ├── Contextual advice
    ├── Timing considerations
    └── Caution or encouragement
```

---

## 3. Coin Method Protocol (金钱卦)

**The standard Yijing coin method (6 tosses):**

| Toss Result | Value | Line Type |
|:-----------:|:-----:|:----------|
| 3 heads (三正) | 9 | ⚊ **Old yang** — solid line that CHANGES |
| 2 heads + 1 tail (两正一反) | 7 | ⚊ Young yang — static solid line |
| 1 head + 2 tails (一正两反) | 8 | ⚋ Young yin — static broken line |
| 3 tails (三反) | 6 | ⚋ **Old yin** — broken line that CHANGES |

**Procedure:**
1. Toss 6 times from bottom (line 1) to top (line 6)
2. Record each line: yang (—) or yin (- -)
3. Mark old yang (○) and old yin (×) — these are the moving/changing lines
4. Read the line that matches the question context most closely
5. From the changing lines, derive the 变卦 (future hexagram)

---

## 4. Plum Blossom Protocol (梅花易数)

See references/plum-blossom-methods.md for detailed methods.

**Standard flow:**
1. User provides 3 numbers OR a time OR a character
2. Calculate: upper trigram, lower trigram, moving line
3. Derive: 本卦 (original) → 变卦 (changing) → 互卦 (interplay)
4. Determine: 体 (you) vs 用 (matter) — lower vs upper of 本卦
5. Analyze: 体用生克 relationship by five elements
6. Read: hexagram judgment + moving line text + body-function analysis

---

## 5. Key Interpretation Principles

### Principle 1: Focus on the Moving Line
The changing line (动爻) is the most specific guidance. Read that line statement carefully.

### Principle 2: 体用生克 is the Core (Plum Blossom)
The relationship between 体 (you) and 用 (matter) determines the overall trend:
- 用生体 = the matter supports you → favorable
- 体克用 = you can master the matter → effort pays off
- 体生用 = you invest in the matter → success but draining
- 用克体 = the matter overwhelms you → unfavorable
- 比和 = same element → natural harmony

### Principle 3: Multiple Hexagrams Tell a Story
- 本卦 = where you are (current situation)
- 变卦 = where you're going (outcome)
- 互卦 = what happens in between (process/hidden influences)

### Principle 4: Good and Bad Are Not Absolute
- No hexagram is purely auspicious or inauspicious
- Each contains the seed of its opposite (e.g., 泰→否, 既济→未济)
- The changing line tells you what to DO about the situation

### Principle 5: Read the Trigrams Too
The individual trigrams reveal additional meaning through their correspondences:
- See references/trigram-correspondences.md for full 万物类象
- Upper trigram = external/environment
- Lower trigram = internal/self

---

## 6. Common Pattern Quick Reference

| Pattern | Hexagrams | Interpretation |
|:-------:|:---------:|:--------------|
| 体克用 + 用旺 | 可成 but 费力 | Success possible, effort needed |
| 用生体 + 体旺 | 大吉 | Naturally favorable, go ahead |
| 用克体 + 用旺 | 大凶 | Not favorable, reconsider timing |
| 体用比和 + 体旺 | 大吉 | Perfect alignment, easy success |
| 本卦吉 + 变卦凶 | 先吉后凶 | Good start but watch the ending |
| 本卦凶 + 变卦吉 | 先凶后吉 | Difficult start leads to good outcome |

---

## 7. Key Taboos and Cautions

- **Do not consult the Yijing for the same question repeatedly** — once per question is sufficient; re-asking indicates doubt
- **The Yijing should not be used for** — gambling numbers, life-or-death medical decisions, malicious intent
- **Best state of mind** — calm, sincere, with a genuine question; not when agitated or intoxicated
- **Time of day** — traditionally morning is best; avoid midnight divination
- **The changing line is crucial** — even if you only see one hexagram, the moving line(s) tell you where change occurs
