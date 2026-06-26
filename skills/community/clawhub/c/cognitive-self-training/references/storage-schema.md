# Cognitive Training Storage Schema

Use a project-local `.cognitive-training/` directory unless the user explicitly wants global memory.

```text
.cognitive-training/
├── README.md
├── schedule.md            # HOT: dream review time and automation prompt
├── dream-style-config.md  # HOT: style pool and random/fixed selection mode
├── principles.md          # HOT: compact durable rules, always checked first
├── strategy.md            # HOT: current deliberate-practice strategy
├── cards.md               # WARM: spaced-repetition cards and due dates
├── graph.md               # WARM: concept links and transfer map
├── mistakes.md            # WARM: recurring errors, causes, prevention
├── inbox/
│   └── YYYY-MM-DD.md      # raw daily captures
├── daily/
│   └── YYYY-MM-DD.md      # reviewed daily consolidation
├── dreams/
│   └── YYYY-MM-DD.md      # scheduled dream deduction and research hypotheses
└── archive/
    └── YYYY-MM.md         # retired/stale/low-value items
```

## Entry IDs

Use stable ids:

- `CT-YYYYMMDD-001` for cognitive training cards
- `MS-YYYYMMDD-001` for mistake entries
- `PR-YYYYMMDD-001` for promoted principles
- `ST-YYYYMMDD` for strategy entries
- `DR-YYYYMMDD` for dream review entries

## Card Schema

```markdown
## [CT-YYYYMMDD-001] Short title

Type: concept | procedure | error | preference | principle | strategy
Status: active | promoted | retired
Source: conversation | user_feedback | error | tool_result | document | self_review
Created: YYYY-MM-DD
Due: YYYY-MM-DD
Stability: new | learning | stable
Tags: tag1, tag2

Prompt:
Answer:
Why it matters:
Transfer:
- Near:
- Far:
Failure mode:
Evidence:
- path-or-summary
Review log:
- YYYY-MM-DD: score N; note
```

## Mistake Schema

```markdown
## [MS-YYYYMMDD-001] Mistake title

Observed:
Root cause:
Detection signal:
Prevention rule:
Related cards:
Status: open | prevented | retired
```

## Principle Schema

```markdown
## [PR-YYYYMMDD-001] Principle title

Rule:
Use when:
Do not overapply when:
Evidence:
- CT-...
Last checked:
```

## Dream Review Schema

```markdown
# Dream Review YYYY-MM-DD

## Dream Review

## Dream Recurrence Statement

## Tian-Dao Deduction

## Research Hypotheses

## Tomorrow's Practice

## Store Updates

## Summary Narrative
```

## Dream Style Config Schema

```markdown
# Dream Style Config

Mode: random | fixed | weighted-random
Fixed style:
Enabled styles:
- research-lab
Weights:
- research-lab: 1
Safety fallback: research-lab
```
