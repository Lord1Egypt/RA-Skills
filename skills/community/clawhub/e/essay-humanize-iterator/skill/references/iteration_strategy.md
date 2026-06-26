# Iteration Strategy

The feedback loop uses a **prioritized escalation** approach: each iteration focuses on different signal categories, from the highest-impact AI patterns down to fine-grained linguistic tuning.

---

## Iteration 1 — High-Weight Pattern Removal

**Focus:** Remove the top 3–4 highest-weight patterns that account for the largest share of the AI score.

Typical targets (ordered by weight):
1. **P15 Em dash overkill** (w=0.136): Replace em dashes with commas, parentheses, or sentence splits.
2. **P21 Markdown artifacts** (w=0.136): Strip `**`, `#`, fenced blocks, markdown links.
3. **P23 Textbook bolding** (w=0.136): Remove `**term**` patterns; use plain text.
4. **P06 Cliche metaphors** (w=0.136): Replace "tapestry", "beacon", "cornerstone" with concrete descriptions.

**Expected outcome:** AI score drops by 40–60% in one pass.

---

## Iteration 2 — Remaining Patterns + Syntactic Variety

**Focus:** Clean up all remaining detected patterns and address syntactic uniformity.

Pattern targets:
- **P12 Participle tailing** (w=0.113): ", highlighting…" → new sentence or finite verb
- **P10 Rule of threes** (w=0.081): Triplet lists → pairs or four items
- **P04 AI vocabulary** (w=0.062): delve, intricate, pivotal → plain synonyms
- **P14 Compulsive summaries** (w=0.060): "Overall," / "In conclusion," → remove or integrate
- **P05 Excessive adverbs** (w=0.054): significantly, remarkably → delete or replace with evidence

Syntactic adjustments:
- If MDD variance < 0.016: Mix very short sentences (5–8 words) with complex ones (25+ words)
- If MDD mean too high: Break compound sentences
- If MDD mean too low: Merge short choppy sentences

**Expected outcome:** AI score drops to < 20; MDD metrics approach human range.

---

## Iteration 3 — Semantic Density & Register

**Focus:** Fine-tune lexical diversity, information density, and natural register.

Targets:
- **TTR < 0.50**: Introduce synonyms for repeated content words; use pronouns/anaphora for variety
- **Content-word ratio outside 0.52–0.65**: Add or remove function words to balance information density
- **Register naturalness**: Ensure tone matches academic/professional expectations without robotic uniformity

Additional polish:
- Remove any remaining single-instance AI patterns
- Verify citations and references are preserved
- Check that no new AI patterns were introduced during rewriting

**Expected outcome:** All metrics within human baselines. Essay reads naturally.

---

## Convergence Criteria

The loop terminates when:
1. **All pass:** AI score ≤ 15, MDD mean ∈ [2.15, 2.55], MDD variance ≥ 0.016, TTR ≥ 0.50, CW ratio ∈ [0.52, 0.65]
2. **Max iterations reached** (default: 3)

If max iterations is reached without convergence, the best-scoring version is returned with a report showing remaining issues.

---

## Feedback Construction

Each iteration's system prompt is dynamically built from `measure.py` output:

```
build_iteration_feedback(report, iteration_number) → str
```

The feedback includes:
- Specific patterns to fix with hit counts and density numbers
- MDD adjustments needed with current vs. target values
- Semantic density changes with current vs. threshold values
- Hard constraints: preserve argument, citations, structure; plain text only
