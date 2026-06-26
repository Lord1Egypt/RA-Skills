# Deep Reader

> A WorkBuddy skill for deep, layered book analysis — powered by the methodology of *How to Read a Book* (Adler & Van Doren).

---

## What It Does

Deep Reader helps you engage with a book — or a cluster of books around a theme — the way a serious reader would.

It doesn't just summarize. Based on your intent, it selects the appropriate reading depth: a quick structural scan, a full analytical breakdown, or a cross-book thematic comparison. It produces structured notes with original quotes, traces argument chains, and asks you to think critically — not just consume.

---

## Quick Start

### Single book — Inspectional Reading (get the gist)

```
@skill://deep-reader What is this book about? '/path/to/book.epub'
```

Output: book type, structural outline, thematic summary (Structural Note)

---

### Single book — Analytical Reading (understand the argument in depth)

```
@skill://deep-reader Read this book deeply '/path/to/book.epub'
```

Or ask a focused question:

```
@skill://deep-reader How does the author argue for "X"? '/path/to/book.epub'
@skill://deep-reader I'm not convinced by the author's case for "X" — walk me through the argument '/path/to/book.epub'
@skill://deep-reader What does this book mean for me in practice? '/path/to/book.epub'
```

Output: core argument analysis + original quotes + critical evaluation (Conceptual Note)

---

### Multiple books — Syntopical Reading (compare books around a theme)

```
@skill://deep-reader Compare these two books on the theme of "reading methodology": '/path/book1.epub' '/path/book2.epub'
```

Output: shared vocabulary, positions of each author, points of agreement and disagreement, integrated analytical framework (Dialectical Note)

---

## Three Reading Levels

| Your Need | Reading Mode | Output Type | Best For |
|---|---|---|---|
| Get the structure and main idea | **Inspectional** | Structural Note | Deciding whether to read it; quick overview |
| Understand arguments, evidence, and logic | **Analytical** | Conceptual Note | Serious reading; writing or discussion prep |
| Compare multiple books on one theme | **Syntopical** | Dialectical Note | Field research; building your own viewpoint |

---

## Supported File Formats

| Format | How It's Handled |
|---|---|
| `.epub` | Auto-extracted; chapters parsed from XHTML |
| `.pdf` | Text extracted via the `pdf` skill |
| `.txt` | Read directly |

---

## Trigger Keywords

**Inspectional Reading** is triggered by phrases like:
"what is this book about", "main idea", "core argument", "overview", "brief intro", "worth reading", "is it good"

**Analytical Reading** is triggered by phrases like:
"deep dive", "analyze in depth", "how does the author argue", "evidence", "reasoning", "critical analysis", "is the argument sound"

**Syntopical Reading** is triggered by phrases like:
"multiple books", "compare", "around the theme of", "cross-book analysis", "synthesize"

---

## Book Type Adaptation

The skill automatically adjusts its analysis based on genre:

| Book Type | Analysis Focus |
|---|---|
| **Fiction** (novel, drama, poetry) | Experience over argument; character, plot, mood — not logical proof |
| **Practical / How-to** | Did the author achieve the goal? Am I willing to act on this? |
| **Philosophy** | Engage with the *question*, not just the answer; test claims against your own experience |
| **History** | Notice what facts were *chosen*, and why; be alert to the author's interpretive stance |
| **Science / Math** | Identify the core research question; focus on axioms, assumptions, and core findings |
| **Social Science** | Watch for keyword ambiguity across authors; syntopical reading usually required |

---

## What Each Output Contains

### Structural Note (Inspectional Reading)
- Book type and genre
- Chapter structure and outline
- Core theme in one or two sentences
- Author's apparent intent

### Conceptual Note (Analytical Reading)
- **What is the book about?** — Theme, skeleton, central question
- **What does the author say, and how?** — Key arguments + original quotes + reasoning chains
- **Is the author right?** — What holds up; where the limits or weak points are
- Reading practice suggestions

### Dialectical Note (Syntopical Reading)
- Shared vocabulary table across all books
- Each author's position on the theme
- Points of genuine consensus
- Root causes of disagreement (different premises, evidence, values)
- Integrated analytical framework + your own stance

---

## Design Philosophy

> "The person who says he knows what he thinks but cannot express it usually does not know what he thinks."
> — Mortimer Adler, *How to Read a Book*

Deep Reader is not meant to replace reading. It's a thinking partner for when you read.

After each analysis, the skill prompts you to make your own notes — underline the key claims, number the steps in an argument, write your objections in the margins. Real reading is a skill that belongs to the reader. AI can scaffold it; only you can do it.

---

## Skill Structure

```
deep-reader/
├── SKILL.md                              # Skill logic and execution rules
├── README.md                             # Chinese documentation
├── README_EN.md                          # This file
├── references/
│   └── reading-methodology.md            # Methodology reference (from How to Read a Book)
└── assets/
    ├── improvement-directions.md         # Skill improvement notes
    ├── discussion-llm-era.md            # Discussion: does reading still matter in the LLM era?
    ├── 《如何阅读一本书》检视阅读报告.md  # Demo: Inspectional Reading
    ├── 娱乐至死-深度阅读报告.md           # Demo: Analytical Reading — Amusing Ourselves to Death
    ├── 《1984》深度阅读报告.md            # Demo: Analytical Reading — Nineteen Eighty-Four
    ├── 《美丽新世界》深度阅读报告.md       # Demo: Analytical Reading — Brave New World
    ├── 三书综合主题阅读报告.md            # Demo: Syntopical Reading — three books on freedom
    └── 从《美丽新世界》《1984》到《娱乐至死》——...  # Demo: alternative syntopical frame
```

---

## Methodology Source

This skill is grounded in the four-level reading framework from *How to Read a Book* by Mortimer Adler and Charles Van Doren (1940, revised 1972):

1. **Elementary Reading** — basic comprehension
2. **Inspectional Reading** — systematic skimming to grasp the whole
3. **Analytical Reading** — complete, thorough, deep reading
4. **Syntopical Reading** — reading across multiple books on the same theme

The four questions every active reader should ask, from the book:
1. What is the book about as a whole?
2. What is being said in detail, and how?
3. Is the book true, in whole or part?
4. What of it — what does it mean for you?

---

## Demo Outputs

The following real-book analyses were produced with this skill:

**Analytical Reading (single book):**
- `assets/娱乐至死-深度阅读报告.md` — *Amusing Ourselves to Death* by Neil Postman
- `assets/《1984》深度阅读报告.md` — *Nineteen Eighty-Four* by George Orwell
- `assets/《美丽新世界》深度阅读报告.md` — *Brave New World* by Aldous Huxley
- `assets/《如何阅读一本书》检视阅读报告.md` — *How to Read a Book* (the methodology source)

**Syntopical Reading (multi-book theme):**
- `assets/三书综合主题阅读报告.md` — Three books on "the death of freedom" (Orwell, Huxley, Postman)
- `assets/从《美丽新世界》《1984》到《娱乐至死》……` — The same theme, different framing

---

## Version History

| Version | Changes |
|---|---|
| v1.0 | Initial release: three reading levels, core pipeline, three output formats |
| v2.0 | Added keyword trigger mapping, book-type adaptation, four-step syntopical reading, note-taking guidance, "receptive reader" attitude module, reading habit formation module |

---

*This skill evolves through use. Feedback and improvement notes are tracked in `assets/improvement-directions.md`.*
