# Digest Format — Attention Research Pipeline

*Version 1.0.0 | Domain-agnostic output format — all topics inherit this*

---

## Overall Structure

```
[Topic name]

• Signal item with context and connection
  Source: outlet | [Link](url)

• Second signal
  Source: outlet | [Link](url)

Read: one sentence on what this means structurally

---

[Next topic...]

---

Bottom line: 2-3 sentences tying across all topics.
What changed. What it implies. What to watch next.
```

---

## Signal Item Format

Lead with behavior or fact, not announcement.
Second sentence: context and connection to previous days / existing matrix.
End with source + link.

**Correct:**
• Iran reopened Hormuz briefly, then reclosed under continued US blockade pressure. This is the third open-close cycle in two weeks — Tehran is testing Washington's threshold while preserving leverage optics.
  Source: Reuters | [Link](https://example.com/article)

**Incorrect:**
• Iran reopens and closes Hormuz again (3rd time in 2 weeks)

---

## Read Line

One sentence. Structural meaning, not summary.

Examples:
- Read: Hormuz is a bargaining chip, not a shipping lane.
- Read: The infra race is concentrating around inference control, not model benchmarks.
- Read: Gulf markets are pricing physical risk that equity markets are still ignoring.

---

## Bottom Line

2-3 sentences:
1. What changed today
2. What it implies structurally
3. One concrete watch item in next 24-48 hours

---

## What NOT to Include

- Raw headlines without interpretation
- Statements without "why now"
- "Experts say" without naming institution and interest
- Speculation without confidence level
- Confirmation of existing beliefs without new evidence
- More than 3 items per topic (pick top signals)

---

## Freshness Indicators

Mark each topic status before digest:
`[Topic] — [fresh | stale | retry N/2 | exhausted]`

- **fresh:** news file is today
- **stale:** running fresh scan
- **retry N/2:** retry in progress
- **exhausted:** 2 failures, skipping

---

## Telegram/WhatsApp Rules

- Plain text, no markdown tables
- Bold for topic headers: `*Geopolitics*`
- Links as `[Link](url)` — readable label + compact
- Max ~800 characters per topic block
- Split by topic if needed, use `---` separators