---
name: discussion-logic-diagnosis
description: Diagnose logical argumentation in the Discussion of an English psychology research paper. Checks argument chains (premise → evidence → conclusion), causal claims (does X cause Y, or correlate?), and the distinction between data, interpretation, and speculation. Triggers on "check logic", "argument check", "is my reasoning sound", "Discussion 逻辑", "讨论 论证", "causal claim check", etc. Does NOT generate or rewrite prose.
---

# Discussion Logic Diagnosis

## Theory basis
*Science Research Writing* Unit 4.1.1 (forward-moving narrative wrap = logical thread) + 4.2.2 Q&A "What if I'm not confident about what my results mean?" (managing the data → interpretation → speculation chain) + 4.2.2 (mapping studies to literature is a logical act — placing your study in the research landscape).

## Three-layer epistemic chain

| Layer | What it is | Hedging required? |
|---|---|---|
| **Data** | What was directly observed | No (just describe) |
| **Interpretation** | What the data suggest | Some (the data "suggest", "indicate", "point to") |
| **Speculation** | What might be true beyond the data | Strong (it is "conceivable", "plausible", "possible") |

A common error: collapsing layers — interpreting data with the same confidence as the data, or speculating as if interpreting.

## What this skill diagnoses

1. **Argument chain integrity** — does each claim have visible support (premise → evidence → conclusion)?
2. **Causal vs correlational claims** — is "cause / lead to / result in" warranted by the design (experimental = OK; correlational = usually too strong)?
3. **Data–interpretation–speculation layering** — are these three levels kept distinct, with appropriate hedging at each?
4. **Counter-argument handling** — are limitations or alternative explanations acknowledged and addressed (not just listed)?
5. **Generalisation scope** — does the conclusion go beyond the sample/population the study actually used?
6. **Internal consistency** — does the conclusion follow from the premises, or does it introduce a new claim?

## Diagnostic signals

| Signal | Means |
|---|---|
| "Stress causes depression" (from a correlational study) | Causal overreach — "is associated with", "predicts" |
| "Therefore, .." (without a clear warrant from the prior sentence) | Missing premise — "therefore" without support |
| "Our results prove that..." | Data/interpretation collapse — studies rarely "prove" |
| Speculation introduced with the same hedging as data | Layer collapse — speculation should hedge more |
| Limitations listed in a final paragraph but never addressed in the argument | Surface-level concession — not real counter-argument handling |
| Conclusion in the last sentence introduces a claim not derived from the body | Internal inconsistency |

## Output format

```markdown
## Logic Diagnosis

### Argument chain map
- [For each major claim: list premise, evidence, conclusion; flag any chain break]

### Causal claim audit
- [list all "cause / lead to / result in" with whether design supports]

### Epistemic layer audit
- [For each sentence: tag as data / interpretation / speculation; check hedging matches layer]

### Counter-argument handling
- [For each limitation: was it actually addressed in the argument?]

### Top issues (severity: critical / major / minor)
1. ...
```

## Cross-reference
- **Causal claims** also affect **Conventions** (causal overclaim is a conventions violation).
- **Take-home / forward motion** is partly a logic concern but is owned by the **Cohesion** skill (Level 2 — global thread).

## Academic integrity
Does not generate or rewrite. Only diagnoses.

## References (to be filled in Phase 2)
- `references/rubric.md`
- `references/checklist.md`
- `references/examples/`
