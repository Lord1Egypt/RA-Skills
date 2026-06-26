# Essay Humanize Iterator — Skill Specification

## Purpose

Iteratively refine essays to minimize false positives from oversensitive AI detectors by removing stereotypical AI writing patterns and aligning semantic density and syntactic complexity with native human writing norms.

## When to Use

- User submits an essay and wants to **reduce AI stylistic patterns** that trigger false positives
- User asks to **rehumanize**, **iterate humanize**, or **improve writing naturalness**
- User wants to improve **semantic density** or **syntactic complexity** to match human writing norms
- User mentions **AI风格优化**, **减少AI痕迹**, **迭代改写**, **写作自然度**

## Workflow

```
1. User provides essay text
2. MEASURE: Run skill/scripts/measure.py → get AI score, MDD, TTR, CW ratio
3. CHECK: If all metrics pass → output essay + report. Done.
4. REWRITE: Generate targeted revision using feedback from measurement
5. RE-MEASURE: Run measure.py on rewritten text
6. REPEAT: Loop steps 3-5 until pass or max iterations (default 3)
7. OUTPUT: Final essay + iteration report table + change summary
```

## Measurement Axes

| Axis | Tool | Pass Criteria |
|------|------|---------------|
| AI Pattern Score | 24-regex weighted scan | ≤ 15 / 100 |
| MDD Mean | spaCy dependency parse | 2.15 – 2.55 |
| MDD Variance | per-sentence MDD spread | ≥ 0.016 |
| Lexical TTR | content-word type/token | ≥ 0.50 |
| Content-Word Ratio | content / all tokens | 0.52 – 0.65 |

See `skill/references/metrics.md` for formulas and baselines.

## Iteration Strategy

- **Iter 1:** Remove highest-weight AI patterns (em dashes, markdown, bolding, cliche metaphors)
- **Iter 2:** Fix remaining patterns + increase syntactic variety
- **Iter 3:** Fine-tune semantic density + register naturalness

See `skill/references/iteration_strategy.md` for full escalation logic.

## Rewrite Engine

All rewriting is performed locally by the orchestrating LLM based on targeted feedback from `measure.py`. No external API calls are made.

Rules for rewriting:
- Process the essay paragraph by paragraph
- Follow the specific feedback instructions from `build_iteration_feedback()`
- Preserve all citations, references, and factual claims
- Do not add new sources or fabricate evidence
- Output plain text only (no markdown formatting, no LaTeX delimiters)

## Output Format

### Final Essay
Plain text. Preserve the original heading structure if any. No markdown artifacts.

### Iteration Report

```
| Iter | AI Score | MDD Mean | MDD Var  | TTR    | CW Ratio | Status |
|------|----------|----------|----------|--------|----------|--------|
|    0 |     45.2 |   2.4821 |   0.0098 | 0.4712 |   0.6280 |   FAIL |
|    1 |     18.6 |   2.3891 |   0.0142 | 0.4988 |   0.5932 |   FAIL |
|    2 |     11.3 |   2.3504 |   0.0178 | 0.5124 |   0.5801 |   PASS |
```

### Change Summary

After the table, provide a brief bullet list of what changed across iterations:
- Which patterns were removed
- How sentence structure was varied
- What vocabulary changes were made

## Rules

1. **Preserve argument:** The author's thesis, evidence, and logical flow must remain intact
2. **Preserve citations:** Never remove, alter, or fabricate citations/references
3. **Plain text output:** No markdown headings (unless input had them), no bold, no em dashes
4. **No hallucination:** Do not add claims, data, or sources not in the original
5. **Idempotent measurement:** Always use `measure.py` for scoring — do not estimate scores
6. **Early exit:** If the input essay already passes all thresholds, output it unchanged with a passing report
7. **Transparency:** Always show the iteration table so the user sees the convergence trajectory

## Supporting Files

| File | Purpose |
|------|---------|
| `skill/scripts/measure.py` | Quantitative scorer (AI patterns + MDD + semantic density) |
| `skill/scripts/iterate.py` | Iteration engine (measure + feedback generation) |
| `skill/references/patterns.md` | 24 AI pattern definitions and fix strategies |
| `skill/references/metrics.md` | Metric formulas, baselines, thresholds |
| `skill/references/iteration_strategy.md` | Per-iteration focus and escalation logic |
| `data/analysis/weights.json` | Corpus-derived pattern weights |
