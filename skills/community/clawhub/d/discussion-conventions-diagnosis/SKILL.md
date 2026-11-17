---
name: discussion-conventions-diagnosis
description: Diagnose academic-writing conventions in the Discussion of an English psychology research paper. Checks the Achievement/Contribution statement (placement, type among 4 — method / results / impact / application), limitations writing, future-work conventions, citation density and function, and the use of "happy words" / appropriate hedging. Triggers on "check conventions", "contribution statement", "happy words", "limitation check", "future work check", "Discussion 学术规范", "讨论贡献", "讨论局限性", etc. Does NOT generate or rewrite prose.
---

# Discussion Conventions Diagnosis

## Theory basis
*Science Research Writing* Unit 4.1.1 (4 types of contribution) + 4.2.2 Q&A "Is there a difference between ACHIEVEMENT and CONTRIBUTION?" + 4.2.3 ("Identify potential applications") + 4.2.2 (How many citations / what function).

## 4 types of contribution (4.1.1)

| Type | Definition | Signal phrase |
|---|---|---|
| **Method** | Modified or new method that improves on existing methods | "we developed a novel...", "the proposed method outperforms..." |
| **Results** | Better / more accurate results than prior studies | "we first demonstrated that...", "to our knowledge, this is the first..." |
| **Impact** | Game-changer / sets new direction / invalidates prior work | "our findings challenge the assumption that...", "we propose a paradigm shift..." |
| **Application** | New or extended real-world application | "could be used to...", "has implications for clinical practice..." |

## Achievement vs Contribution (4.2.2 Q&A)
- **Achievement** = what you actually did in the study (e.g., "we collected data from 500 participants")
- **Contribution** = what the field / world gains (e.g., "we provide the first evidence that...")
- Both should be present, with the **contribution** often positioned as the take-home message.

## What this skill diagnoses

1. **Achievement/contribution statement presence** — is there an explicit statement?
2. **Type classification** — which of the 4 types is being claimed? Is it consistent with the actual study?
3. **Placement** — is it in the opening moves (not buried)?
4. **"Happy words" usage** — is the claim hedged firmly (e.g., "to our knowledge", "we first demonstrated", "compelling evidence") without over-claiming ("prove")?
5. **Limitations conventions** — are they stated explicitly, with appropriate scope, and not as throwaway?
6. **Future work conventions** — is the future-work section directional (specific next steps) rather than vague ("more research is needed")?
7. **Citation density** — count per Discussion; compared to corpus baseline.
8. **Citation function** — does each citation do confirm / contrast / extend work?

## Diagnostic signals

| Signal | Means |
|---|---|
| "Our study made a contribution to the field of..." | Generic — should name the specific contribution |
| "We proved that..." | Overclaim — "prove" is rarely appropriate in a single study |
| "More research is needed" (no specifics) | Weak future work — should be directional |
| Limitations are one vague sentence | Surface-level — should be specific (sample, design, measure) |
| Contribution in the last paragraph | Placement violation — should be in the opening |
| Multiple contribution types claimed without support | Type-mixing — pick the strongest one and own it |
| Citation density <5 or >40 in a Discussion of ~1500 words | Density outside typical range |

## Output format

```markdown
## Conventions Diagnosis

### Achievement/Contribution
- [✓/✗] Achievement statement present
- [✓/✗] Contribution statement present
- Type claimed: [method / results / impact / application]
- Type appropriate for study? [yes / concern / no]
- Placement: [opening / mid / closing]
- Hedging level: [appropriate / over-claimed / under-claimed]

### Limitations
- [✓/✗/⚠] Present
- Quality: [specific / vague / throwaway]

### Future work
- [✓/✗/⚠] Present
- Quality: [directional / vague / missing]

### Citation audit
- Total count: N
- Density: N / 1000 words
- Function distribution: confirm=X / contrast=Y / extend=Z
- Coverage: [all three functions / only confirm / etc.]

### Top issues (severity: critical / major / minor)
1. ...
```

## Cross-reference
- **Hedging word choice** is owned by the **Vocabulary** skill. This skill owns the **policy** (when should you hedge, when should you commit?).
- **Citation positioning in sentences** is owned by the **Cohesion** skill (L1 — citation as glue). This skill owns the **density and function**.

## Academic integrity
Does not generate or rewrite. Only diagnoses.

## References (to be filled in Phase 2)
- `references/rubric.md`
- `references/checklist.md`
- `references/examples/`
