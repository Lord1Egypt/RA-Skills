# Measurement Metrics

Three axes quantify how "AI-like" an essay reads. All thresholds are derived from CAWSE/LOCNESS human-writing corpora and the Wikipedia "Signs of AI writing" pattern analysis.

---

## A. AI Pattern Score (0–100)

Weighted sum of 24 pattern densities (matches per 1k words), normalized to 0–100.

| Component | Formula |
|-----------|---------|
| Per-pattern density | `count(regex_matches) / word_count * 1000` |
| Weighted density | `density * pattern_weight` (from `weights.json`) |
| Total score | `sum(weighted_densities) / 5.0 * 100`, capped at 100 |

Only patterns with `weight > 0` (statistically significant AI discriminators) contribute:

| Pattern | Weight | AI freq/1k | Human freq/1k |
|---------|--------|------------|----------------|
| P15 Em dash overkill | 0.1358 | 5.30 | 0.00 |
| P21 Markdown artifacts | 0.1358 | 1.71 | 0.00 |
| P23 Textbook bolding | 0.1358 | 0.10 | 0.00 |
| P06 Cliche metaphors | 0.1358 | 0.71 | 0.004 |
| P12 Participle tailing | 0.1133 | 0.20 | 0.004 |
| P10 Rule of threes | 0.0806 | 3.12 | 0.22 |
| P04 AI vocabulary | 0.0621 | 2.29 | 0.31 |
| P14 Compulsive summaries | 0.0598 | 1.55 | 0.23 |
| P05 Excessive adverbs | 0.0540 | 1.14 | 0.22 |
| P13 Over-attribution | 0.0529 | 0.18 | 0.04 |
| P11 False ranges | 0.0341 | 1.36 | 0.62 |

**Pass threshold: AI Pattern Score ≤ 15**

---

## B. Syntactic Complexity (MDD)

Mean Dependency Distance (MDD) measures how far apart syntactically related words are in each sentence. Computed via spaCy dependency parse (`en_core_web_sm`).

| Metric | Formula |
|--------|---------|
| Sentence MDD | `mean(abs(token.i - token.head.i))` for non-punct tokens |
| Essay MDD mean | `mean(sentence_MDDs)` |
| Essay MDD variance | `variance(sentence_MDDs)` |

**Human baselines (CAWSE/LOCNESS):**

| Metric | Human | AI | Pass Threshold |
|--------|-------|-----|----------------|
| MDD Mean | 2.334 | 2.455 | 2.15 – 2.55 |
| MDD Variance | 0.0199 | 0.0116 | ≥ 0.016 |
| Variance ratio (H/AI) | 1.715 | — | — |

Key insight: human essays show **more** variance in sentence complexity. Uniformly "smooth" AI prose has low MDD variance.

---

## C. Semantic Density

Three sub-metrics capture information density and lexical diversity.

### C1. Type-Token Ratio (TTR)

```
TTR = unique_content_lemmas / total_content_lemmas
```

Content POS: NOUN, VERB, ADJ, ADV. Stop-word POS excluded.

| Writer | Typical TTR | Pass Threshold |
|--------|-------------|----------------|
| Human | ~0.55 | ≥ 0.50 |
| AI | ~0.48 | — |

### C2. Content-Word Ratio

```
content_word_ratio = content_tokens / all_non_punct_tokens
```

| Writer | Typical | Pass Range |
|--------|---------|------------|
| Human | ~0.58 | 0.52 – 0.65 |
| AI | ~0.62 | — |

### C3. Specificity (informational)

```
specificity = (named_entities + numeric_tokens) / all_non_punct_tokens
```

Higher specificity indicates more grounded, evidence-based writing. Reported but not used as a hard pass/fail gate.

---

## Overall Pass/Fail

An essay **passes** when ALL of:
1. AI Pattern Score ≤ 15
2. MDD Mean within 2.15 – 2.55
3. MDD Variance ≥ 0.016
4. TTR ≥ 0.50
5. Content-Word Ratio within 0.52 – 0.65
