---
name: discussion-vocabulary-diagnosis
description: Diagnose vocabulary in the Discussion of an English psychology research paper. Checks (1) use of academic register and high-frequency academic expressions from the 5 functional categories in *Science Research Writing* 4.4.2, (2) appropriate modal verb usage across the 6 categories in 4.5, and (3) avoidance of colloquialisms. Triggers on "check vocabulary", "academic expressions", "hedge check", "modal verb check", "Discussion 词汇", "Discussion 用语", "讨论 学术表达", etc. Does NOT generate or rewrite prose.
---

# Discussion Vocabulary Diagnosis

## Theory basis
*Science Research Writing* Unit 4.4 (Useful Words and Phrases) — categorised into 5 functional groups — and Unit 4.5 (Modal Verbs) — 6 categories of modality.

## 5 functional categories (from 4.4.2)

1. **Map to literature / knowledge** — positioning phrases (consistent with, in contrast to, comparable to, in line with, distinct from, contrary to...) and verbs (confirm, contradict, extend, complement, challenge, support, refute, substantiate, resemble...)
2. **Refine / explore implications** — hedging (plausible, potential, tentative; postulate, hypothesise, speculate, theorise; it is conceivable that..., we cannot rule out..., this is reinforced by...)
3. **Achievement / contribution** — "happy words" (accurate, novel, effective, robust, significant, valuable, valid) and "!-substitutes" / "very happy words" (compelling, crucial, remarkable, striking, unprecedented, vital)
4. **Current and future work** — (currently, at present, promising, worthwhile, urgent; further work is needed, future studies should, we recommend, would be of interest)
5. **Applications / use / applicability** — (to apply, to enable, to implement, to generalise, to lead to, to realise, to utilise; applicable, feasible, suitable, viable, practicable)

## 6 modal-verb categories (from 4.5)

1. **Able** — can / could / be able to (and perfect forms)
2. **Possible / optional** — may / might / could (and perfect forms)
3. **Expected / likely / probable** — should / ought to
4. **Obvious / impossible** — must / cannot (and perfect forms)
5. **Advisable / recommended** — should
6. **Necessary / essential** — must / need to / have to

> ⚠️ The same form can carry different meanings (e.g., "should" = expected OR advisable; "can" = able OR possible). Context disambiguates.

## What this skill diagnoses

1. **Use of high-frequency academic expressions** — does the writer use the right phrase for each function (map / hedge / contribute / future / apply)?
2. **Modal verb appropriateness** — is the modal matched to the intended epistemic stance?
3. **Colloquialism avoidance** — is the register academic throughout (no "a lot of", "we think", "kids", etc.)?
4. **Terminology consistency** — same concept named with the same term throughout?
5. **Discipline-specific lexis** — does the vocabulary match psychology conventions (e.g., "participants" not "subjects" in modern usage, "self-report" not "survey answers")?

## Diagnostic signals

| Signal | Means |
|---|---|
| "A lot of studies have shown..." | Colloquial — replace with "A substantial number of studies..." or "Many studies..." |
| "We think that..." | Colloquial hedging — use "We propose / suggest / argue that..." |
| "Kids / subjects / patients" (when "participants" is the field norm) | Discipline-specific register issue |
| "Proved that..." (for a single study) | Overclaim — use "our results suggest / indicate / show that..." |
| "This may can cause..." | Modal stacking — "may" and "can" overlap; pick one |
| "Must" used to express possibility (when "may/might" is meant) | Modal category error — "must" = obvious, not possible |
| Same concept called "stress", "pressure", "strain" within one paragraph | Terminology inconsistency |

## Output format

```markdown
## Vocabulary Diagnosis

### Academic expression coverage (per 4.4.2 categories)
- Map to literature: [✓ / weak / ✗]
- Refine implications (hedging): [✓ / weak / ✗]
- Achievement/contribution language: [✓ / weak / ✗]
- Future work language: [✓ / weak / ✗]
- Applications language: [✓ / weak / ✗]

### Modal verb audit (per 4.5 categories)
- [list each modal found, with intended meaning, with whether it fits]

### Colloquialism hits
- [list with sentence_ref and suggested replacement]

### Terminology consistency
- [list any within-text drift]

### Top issues (severity: critical / major / minor)
1. ...
```

## References (to be filled in Phase 2)
- `references/academic-vocabulary.md` — the high-frequency academic expression list (extracted from 4.4.2)
- `references/modal-verbs.md` — the 6-category modal verb guide (extracted from 4.5)
- `references/rubric.md`
- `references/checklist.md`
- `references/examples/`
