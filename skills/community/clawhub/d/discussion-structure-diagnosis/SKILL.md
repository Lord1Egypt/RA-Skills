---
name: discussion-structure-diagnosis
description: Diagnose the structural completeness and move ordering of the Discussion section in an English psychology research paper. Checks whether the draft contains expected moves (revisit results, map to literature, identify applications, limitations, future work, achievement/contribution statement) and whether the order is logical and mirrors the Introduction's Block 1–4 symmetry. Triggers on "check Discussion structure", "is my Discussion complete", "discussion 缺什么", "Discussion 结构", etc. Does NOT generate or rewrite prose.
---

# Discussion Structure Diagnosis

## Theory basis
*Science Research Writing* (Glasman-Deal) Unit 4.2 (Building Your Own Model) + 4.2.3 (Generic Discussion Model) + 4.3 (Testing and Adjusting) + 4.1.1 (narrative wrap).

## Generic Discussion Model (per 4.2.3)
A complete Discussion typically combines these moves (order is flexible, per 4.2):
- **A. Revisit results and explore their implications** — echo key results, then say what they mean
- **B. Map to literature/knowledge for comparison/support** — confirm / contrast / extend against prior work
- **C. Identify potential applications** — real-world, methodological, or theoretical
- **D. State limitations** — sample, design, measure, generalisability
- **E. Suggest future work** — specific, directional, not "more research is needed"
- **F. State achievement / contribution** — placed early, with "happy words", in one of 4 types (method / results / impact / application)
- **G. Opening move** — either (i) achievement/contribution statement, or (ii) "reboot" reader (revisit gap / aim / key results)

## Symmetry with Introduction
- Intro Block 1 (establish importance) ↔ Discussion closing (exit the article, broader implications)
- Intro Block 2 (research map) ↔ Discussion B (map to literature)
- Intro Block 3 (gap/problem) ↔ Discussion A (your response to gap)
- Intro Block 4 (describe present paper) ↔ Discussion F (your contribution)

## What this skill diagnoses

1. **Move coverage** — Which of A–G are present? Which are missing?
2. **Move ordering** — Is the order logical? Does it create a forward-moving narrative wrap?
3. **Intro–Discussion symmetry** — Does the Discussion echo and resolve what the Introduction set up?
4. **Opening move quality** — Is the first sentence an achievement/contribution or a "reboot"? Or is it a weak "In this study, we..." anti-pattern?
5. **Take-home message persistence** — Can you state the take-home after reading only the first paragraph? Does it carry to the last?

## Diagnostic signals

| Signal | Means |
|---|---|
| First sentence starts with "In this study, we..." | Weak opening — should be achievement or reboot |
| "To our knowledge, this is the first study to..." | Achievement opening — strong |
| "The aim of the present study was to..." | Reboot opening — acceptable if mirrored from Intro |
| Limitations appear in the last paragraph only | Convention-violating — should be earlier (often before future work) |
| No explicit contribution sentence anywhere | Critical miss — contribution must be stated |
| "Further research is needed" without specifics | Weak future work — should be directional |
| "Our results are consistent with..." appearing before "Our results showed..." | Move order issue — should revisit results first, then map to literature |

## Output format

```markdown
## Structure Diagnosis

### Move coverage (✓ / ✗ / ⚠ weak)
- [✓/✗/⚠] A. Revisit results and explore implications
- [✓/✗/⚠] B. Map to literature
- [✓/✗/⚠] C. Identify applications
- [✓/✗/⚠] D. State limitations
- [✓/✗/⚠] E. Suggest future work
- [✓/✗/⚠] F. Achievement/contribution statement (note location)
- [✓/✗/⚠] G. Opening move quality

### Move order
- [pass / concern / fail] — description

### Intro–Discussion symmetry
- [pass / concern / fail] — which blocks align, which don't

### Take-home message
- Extracted take-home: "..."
- Persistence: [consistent / drifts / lost]

### Top issues (severity: critical / major / minor)
1. ...
2. ...
```

## Academic integrity
Does not generate or rewrite the Discussion. Only diagnoses and suggests. If asked to write a Discussion, redirect to the diagnostic function.

## References (to be filled in Phase 2)
- `references/rubric.md` — scoring rubric
- `references/checklist.md` — line-by-line checklist
- `references/examples/` — annotated good/bad examples from the 50-paper corpus
