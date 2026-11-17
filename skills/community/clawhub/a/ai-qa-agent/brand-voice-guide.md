# Brand Voice Guide

This document defines the brand voice framework that all outbound content must adhere to. The AI QA Agent enforces this guide during final review. The AI Staff Agent references it when generating copy variants.

---

## Voice Attributes

| Attribute | Description | Do | Don't |
|-----------|-------------|-----|-------|
| **Clear** | Ideas are immediately graspable. No ambiguity. | Use short sentences. Lead with the conclusion. | Bury the point in jargon or nested clauses. |
| **Confident** | We know our domain. We speak with authority, not arrogance. | State facts directly. Use active voice. | Hedge excessively ("we believe", "it might"). |
| **Concise** | Every word earns its place. Respect the reader's time. | Cut filler words. One idea per sentence. | Pad paragraphs with qualifiers or repetition. |
| **Human** | We sound like a sharp colleague, not a press release. | Use contractions. Address the reader directly. | Use corporate buzzwords ("synergy", "leverage", "paradigm"). |

---

## Tone Spectrum by Context

Not all content sounds the same. Tone shifts by deliverable type:

| Context | Tone | Example |
|---------|------|---------|
| Technical docs / API references | Neutral, precise | "The endpoint returns a 200 status code on success." |
| Product copy / landing pages | Warm, persuasive | "Get from idea to deployment in minutes, not days." |
| Internal reports / analysis | Direct, data-driven | "Revenue grew 23% YoY, driven primarily by enterprise accounts." |
| Error messages / UX copy | Helpful, specific | "Upload failed — the file exceeds the 10 MB limit. Try compressing it." |
| Social media / casual | Approachable, punchy | "New feature drop: dark mode is here. Your eyes can thank us later." |

---

## Language Rules

### Word Choice
- Use **simple words** over complex ones: "use" not "utilize", "help" not "facilitate", "start" not "commence"
- Avoid **noun chains** of 3+ words (e.g., "customer data management system integration" → "integrating the customer data system")
- Prefer **concrete terms** over abstract ones: "3 seconds faster" not "significant performance improvement"

### Sentence Structure
- **Target**: 15-20 words per sentence average
- **Maximum**: 35 words — if a sentence exceeds this, break it up
- **Paragraphs**: 3-5 sentences max. One idea per paragraph.
- Use **parallel structure** in lists and comparisons

### Forbidden Patterns
- "In order to" → "to"
- "At this point in time" → "now"
- "Due to the fact that" → "because"
- "A number of" → "several" or specify the number
- "Very" / "really" / "quite" as intensifiers — they weaken the word they modify
- Starting consecutive sentences with the same word
- Ending sentences with prepositions where avoidable
- Exclamation marks in professional/formal content (max 1 per piece in casual content)

### Inclusive Language
- Use gender-neutral pronouns ("they/them" as singular)
- Avoid ableist metaphors ("blind spot", "crippling debt")
- Reference people-first language ("person with a disability", not "disabled person")

---

## Formatting Standards

### Headings
- H1: Title (sentence case, not title case)
- H2: Section headers (sentence case)
- H3: Subsections when needed
- Never skip heading levels (H1 → H3 without H2)

### Lists
- Use bullet lists for unordered items, numbered lists for sequences
- Keep list items parallel in grammatical structure
- Maximum 7 items per list — group into sub-lists if needed

### Numbers
- Spell out one through nine, use numerals for 10+
- Always use numerals for measurements, percentages, and currencies
- Use commas in four-digit numbers and above: 1,000 not 1000

### Punctuation
- Oxford comma: always use it ("red, blue, and green")
- Em dash: no spaces around it ("The result — unsurprisingly — was positive")
- Semicolons: use sparingly; prefer short sentences instead

---

## Brand Voice Scoring

The QA Agent scores content on a 1-5 scale per attribute:

| Score | Meaning |
|-------|---------|
| 5 | Exemplary — textbook execution of the attribute |
| 4 | Strong — minor polish needed |
| 3 | Adequate — noticeable gaps but functional |
| 2 | Weak — significant rework required |
| 1 | Off-brand — contradicts the attribute entirely |

**Minimum passing score**: 3 per attribute, with an overall average of 3.5 or higher.
**Aspirational target**: 4+ average across all attributes.