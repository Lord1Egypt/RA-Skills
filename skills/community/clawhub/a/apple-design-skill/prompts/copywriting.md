# Copywriting Optimizer

This module defines the rules and patterns for transforming ordinary product copy into Apple-style "fruit-flavored" text. Apple's voice is unmistakable: short, confident, and laser-focused on a single benefit per line. Every headline earns its place; every word pulls its weight.

> **Usage:** When writing or optimizing headlines, subheadings, or body copy for Apple-style pages, apply the principles, patterns, and length constraints defined below. Detect the user's language and select the matching pattern set (English or Chinese).

---

## 1. Core Principles

Apple copywriting follows five non-negotiable rules:

1. **One idea per line.** Each headline or sentence communicates exactly one benefit. Never stack multiple selling points into a single phrase.
2. **Short beats long.** If you can say it in three words, don't use six. Brevity signals confidence.
3. **Lead with the benefit, not the spec.** Users care about what a feature *does for them*, not what it *is*. Transform technical parameters into felt experiences.
4. **Rhythm matters.** Apple copy has a cadence — fragments, pauses (periods mid-sentence), and parallel structures create a reading tempo that feels intentional.
5. **Surprise with simplicity.** The most memorable Apple lines are disarmingly simple. Complexity is the enemy.

### The Apple voice checklist

Before finalizing any piece of copy, verify:

- [ ] Is every word necessary?
- [ ] Does it focus on one benefit?
- [ ] Would a non-technical person understand it instantly?
- [ ] Does it sound confident without being arrogant?
- [ ] Does it have rhythm when read aloud?

---

## 2. English Copywriting Patterns

Apple's English copy relies on a small set of repeatable sentence structures. Use these patterns as templates when generating headlines and subheadings.

### 2.1 Fragment Sentences

Short noun-verb or noun-preposition fragments separated by periods. The period forces a pause that adds weight to each word.

| Pattern | Example | Product |
|---------|---------|---------|
| Noun. Preposition noun. | Chip. For dip. | M2 MacBook Air |
| Noun. Adverb. | Pro. Beyond. | MacBook Pro |
| Noun. Adjective. | Supercharged. By M2. | MacBook Air |

**When to use:** Hero headlines where maximum impact is needed in minimum words.

### 2.2 Single-Word / Two-Word Impact

A single word or ultra-short phrase that stops the reader. Often used as a section opener.

| Pattern | Example | Product |
|---------|---------|---------|
| Interjection. | Whoa. | MacBook Pro |
| Adjective. | Brilliant. | iPhone display |
| Noun. | Power. | Mac Studio |

**When to use:** Section transitions or dramatic reveals.

### 2.3 Superlative / Comparative

A bold claim framed as the best, fastest, or most advanced. Apple earns these claims by pairing them with specific context.

| Pattern | Example | Product |
|---------|---------|---------|
| The best [noun] ever. | The best Mac ever. | iMac |
| The most [adjective] [noun] ever. | The most powerful MacBook Pro ever. | MacBook Pro |
| Our [superlative] [noun]. | Our thinnest design. | MacBook Air |

**When to use:** Product introduction headlines where a clear competitive claim is warranted.

### 2.4 Rhyme and Wordplay

Phonetic play that makes the line memorable. Apple uses this sparingly — one per page at most.

| Pattern | Example | Product |
|---------|---------|---------|
| Rhyming pair | Whoa. The new MacBook Pro. | MacBook Pro |
| Alliteration | Powerful. Portable. Pro. | MacBook Pro |
| Double meaning | Light. Years ahead. | MacBook Air |

**When to use:** Taglines or hero headlines where memorability is the primary goal.

### 2.5 Question / Challenge

A rhetorical question that implies the answer is obvious.

| Pattern | Example | Product |
|---------|---------|---------|
| Why [action]? | Why Mac? | Mac |
| What's [noun]? | What's a computer? | iPad Pro |

**When to use:** Campaign-level headlines or section openers that challenge assumptions.

---

## 3. Chinese Copywriting Patterns

Apple's Chinese localization is not a direct translation — it is a cultural adaptation. The Chinese copy leverages classical Chinese rhetorical devices to achieve the same impact as the English originals.

### 3.1 对仗 (Parallel Structure)

Two clauses of equal length with mirrored grammatical structure. This is the most common pattern in Apple's Chinese copy.

| Pattern | Example | Product |
|---------|---------|---------|
| A得很，B得很 | 强得很，轻得很 | MacBook Air |
| A又B，C又D | 又轻又薄，又快又强 | iPad Air |
| 有A，有B | 有颜值，有实力 | iMac |

**When to use:** Headlines that need to convey two complementary benefits.

### 3.2 四字格 (Four-Character Idiom Style)

Compact four-character phrases that echo the rhythm of classical Chinese idioms. They feel authoritative and polished.

| Pattern | Example | Product |
|---------|---------|---------|
| ABCD | 放心比好了 | iPhone comparison |
| ABCD | 岂止于大 | iPhone Plus |
| ABCD | 超凡出众 | Apple Watch |

**When to use:** Taglines and section headers where a sense of gravitas is needed.

### 3.3 反问 (Rhetorical Question)

A question whose answer is self-evident. In Chinese, this carries a tone of confident challenge.

| Pattern | Example | Product |
|---------|---------|---------|
| 还有谁？ | 还有谁？ | iPhone |
| 谁说A不能B？ | 谁说轻薄不能强大？ | MacBook Air |
| 何止A？ | 何止于快？ | M-series chip |

**When to use:** Bold claims where the product's superiority is implied rather than stated.

### 3.4 押韵 (Rhyming)

End-rhyme or tonal rhyme that gives the line a musical quality.

| Pattern | Example | Product |
|---------|---------|---------|
| A的B，B的A | 大的好，好的大 | iPhone Plus |
| AB，CD (rhyming) | 一身轻，万事行 | MacBook Air |

**When to use:** Memorable taglines — use sparingly, one per page.

---

## 4. Title Length Constraints

Apple headlines are ruthlessly concise. Enforce these hard limits when generating or optimizing titles.

### Title (H1 / Hero headline)

| Language | Constraint | Measurement |
|----------|-----------|-------------|
| English | ≤ 8 words | Count space-separated tokens |
| Chinese | ≤ 12 characters | Count Unicode characters (excluding punctuation) |

### Subtitle (H2 / Section subheading)

| Language | Constraint | Measurement |
|----------|-----------|-------------|
| English | ≤ 20 words | Count space-separated tokens |
| Chinese | ≤ 30 characters | Count Unicode characters (excluding punctuation) |

### Enforcement rules

1. **Count before output.** Before finalizing any headline, count words (EN) or characters (ZH). If over the limit, rewrite.
2. **Punctuation does not count.** Periods, commas, question marks, and exclamation marks are excluded from the count.
3. **Numbers count as one word** (EN) or by their character length (ZH).
4. **If a title exceeds the limit**, shorten it by removing qualifiers, merging clauses, or switching to a fragment pattern.

---

## 5. Technical Spec to Experience Conversion

Apple never leads with raw specifications. Every technical parameter is reframed as a human benefit. Follow these conversion rules when the user provides spec-heavy copy.

### Conversion framework

| Step | Action | Example |
|------|--------|---------|
| 1. Identify the spec | Extract the raw technical claim | "M3 chip with 8-core GPU" |
| 2. Find the user benefit | Ask: "What does this let the user *do* or *feel*?" | Faster graphics rendering |
| 3. Translate to experience | Rewrite as a felt outcome | "Blazingly fast graphics that keep up with your biggest ideas" |
| 4. Compress | Apply title length constraints | "Graphics that fly." |

### Common spec-to-experience mappings

| Technical Spec | ❌ Spec-heavy | ✅ Apple-style |
|---------------|--------------|----------------|
| M3 chip with 8-core GPU | M3 chip with 8-core GPU for faster rendering | Blazingly fast graphics that keep up with your biggest ideas |
| 18-hour battery life | 18 hours of battery life | All day. And then some. |
| 6.7-inch Super Retina XDR display | 6.7-inch Super Retina XDR OLED display | A display that makes everything look incredible |
| 48MP main camera | 48-megapixel main camera sensor | Every detail. Captured beautifully. |
| 256GB SSD storage | 256GB solid-state drive | Room for everything you love |
| Wi-Fi 6E support | Supports Wi-Fi 6E 802.11ax | Faster wireless. Everywhere. |
| A17 Pro chip, 6-core CPU | A17 Pro with 6-core CPU architecture | The most powerful chip in a smartphone. |
| IP68 water resistance | IP68 rated water resistance to 6 meters | Don't worry about splashes. Or dunks. |

### Chinese spec-to-experience mappings

| Technical Spec | ❌ Spec-heavy | ✅ Apple-style |
|---------------|--------------|----------------|
| M3 芯片，8 核 GPU | 搭载 M3 芯片和 8 核图形处理器 | 图形性能，快到飞起 |
| 18 小时续航 | 电池续航长达 18 小时 | 一整天，不插电 |
| 4800 万像素主摄 | 配备 4800 万像素主摄像头 | 每个细节，纤毫毕现 |
| 256GB 存储 | 256GB 固态硬盘存储空间 | 装得下你的一切 |

### Conversion rules

1. **Never lead with a number.** If the spec starts with a number, restructure the sentence so the benefit comes first.
2. **Avoid jargon.** Replace "GPU", "SSD", "OLED" with what they enable. If the acronym is well-known (like "Wi-Fi"), it may stay.
3. **Use sensory language.** Words like "blazingly", "beautifully", "incredibly" connect specs to feelings.
4. **One spec per sentence.** Don't combine multiple specs into a single line.
5. **Apply the fragment pattern.** After converting, check if the result can be shortened into a fragment sentence (Section 2.1 or 3.1).

---

## 6. Copywriting Rules Data Structure

The following JSON block encodes the copywriting rules for programmatic access and testability.

```json
{
  "copywritingRules": {
    "corePrinciples": [
      "One idea per line",
      "Short beats long",
      "Lead with benefit, not spec",
      "Rhythm matters",
      "Surprise with simplicity"
    ],
    "titleRules": {
      "en": { "maxWords": 8 },
      "zh": { "maxChars": 12 }
    },
    "subtitleRules": {
      "en": { "maxWords": 20 },
      "zh": { "maxChars": 30 }
    },
    "patterns": {
      "en": [
        {
          "name": "fragment-sentences",
          "description": "Short fragments separated by periods",
          "examples": ["Chip. For dip.", "Pro. Beyond.", "Supercharged. By M2."]
        },
        {
          "name": "single-word-impact",
          "description": "One or two words for dramatic effect",
          "examples": ["Whoa.", "Brilliant.", "Power."]
        },
        {
          "name": "superlative-comparative",
          "description": "Bold best/most/fastest claims",
          "examples": ["The best Mac ever.", "The most powerful MacBook Pro ever.", "Our thinnest design."]
        },
        {
          "name": "rhyme-wordplay",
          "description": "Phonetic play for memorability",
          "examples": ["Whoa. The new MacBook Pro.", "Light. Years ahead."]
        },
        {
          "name": "question-challenge",
          "description": "Rhetorical questions implying obvious answers",
          "examples": ["Why Mac?", "What's a computer?"]
        }
      ],
      "zh": [
        {
          "name": "parallel-structure",
          "description": "对仗 — Two clauses with mirrored grammar",
          "examples": ["强得很，轻得很", "又轻又薄，又快又强", "有颜值，有实力"]
        },
        {
          "name": "four-character-idiom",
          "description": "四字格 — Compact four-character phrases",
          "examples": ["放心比好了", "岂止于大", "超凡出众"]
        },
        {
          "name": "rhetorical-question",
          "description": "反问 — Questions with self-evident answers",
          "examples": ["还有谁？", "谁说轻薄不能强大？", "何止于快？"]
        },
        {
          "name": "rhyming",
          "description": "押韵 — End-rhyme or tonal rhyme",
          "examples": ["大的好，好的大", "一身轻，万事行"]
        }
      ]
    },
    "specConversion": {
      "rules": [
        "Never lead with a number",
        "Avoid jargon — replace acronyms with benefits",
        "Use sensory language",
        "One spec per sentence",
        "Apply fragment pattern after conversion"
      ],
      "examples": [
        {
          "spec": "M3 chip with 8-core GPU",
          "bad": "M3 chip with 8-core GPU for faster rendering",
          "good": "Blazingly fast graphics that keep up with your biggest ideas"
        },
        {
          "spec": "18-hour battery life",
          "bad": "18 hours of battery life",
          "good": "All day. And then some."
        },
        {
          "spec": "48MP main camera",
          "bad": "48-megapixel main camera sensor",
          "good": "Every detail. Captured beautifully."
        }
      ]
    }
  }
}
```

---

## Quick Reference

| Rule | English | Chinese |
|------|---------|---------|
| Title max length | ≤ 8 words | ≤ 12 characters |
| Subtitle max length | ≤ 20 words | ≤ 30 characters |
| Primary pattern | Fragment sentences | 对仗 (parallel structure) |
| Secondary pattern | Superlative / comparative | 四字格 (four-character idiom) |
| Tone | Confident, simple, benefit-first | Confident, rhythmic, culturally resonant |
| Spec handling | Convert to felt experience | Convert to felt experience |
