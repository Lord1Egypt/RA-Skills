# Topic Generator — From Paper or Thesis

*Version 1.0.0 | How to build a TOPICS file from user input*

---

## When to Use

User says:
- "Here's a paper, build a topic from it"
- "Use this thesis as the research framework"
- "Dropped a PDF — build the topic prompt"

---

## Input Options

1. **Text pasted** — agent reads directly
2. **URL** — agent fetches and reads
3. **File path** — agent reads from workspace
4. **Description** — user describes topic and lens in 2-3 sentences

---

## Agent Task

Extract:
1. **Domain** — what field/area
2. **Core Thesis** — 2-3 sentences on how this domain works
3. **Key Entities + Weights** — sum to 100%, derive from paper's emphasis
4. **Signal Criteria** — what makes a claim credible in this domain
5. **Noise Filters** — what to ignore
6. **Confidence Calibration** — what high/low confidence looks like
7. **Watch Items** — 3-5 concrete, time-bound, verifiable
8. **Source Hierarchy** — which outlets most authoritative

---

## Output

Write `PROMPTS/TOPICS/<topic-slug>.md` with:

```markdown
# [Topic Name]

> [1-sentence domain description]

## Methodology

[3-5 sentences on how to read this domain]

## Entity Framework

| Entity | Weight | Role |
|--------|--------|------|
| ... | ... | ... |

## Signal Criteria

- ...

## Noise Filters

- ...

## Confidence Calibration

- **Confirmed** → ...
- **Likely** → ...
- **Possible** → ...
- **Speculative** → ...

## Watch Items

- ...

## Source Hierarchy

1. ... — why
2. ...

## Integration

Inherits from CORE/system-prompt.md and CORE/signal-rules.md.
Do not contradict core rules.

---
Generated from: [source]
Version: 1.0.0
```

---

## Rules

1. No placeholders — complete, usable file
2. Flag gaps — note and use sensible defaults
3. Infer weights — from paper's emphasis, not invented
4. Always inherit CORE — never contradict
5. One topic per paper — extract one coherent domain
6. Version as 1.0.0 — note source and date

---

## After Building

```
Built: [topic-name]
From: [source]

Methodology: [summary]
Entity weights: [list]
Signal criteria: [what qualifies]

---
Approve to activate, or tell me what to adjust.
```

---

*Version 1.0.0 | 2026-04-20*