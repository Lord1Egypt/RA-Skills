# Scoring & Statistics

> Distilled from real-world dual-track scoring and reproducible statistics practice

## Dual-Track Validation

Run **two independent scoring systems** on the same outputs.

- **Track A**: Rule-based, exact, cheap — counts field presence, keyword hits, pattern matches
- **Track B**: Semantic, fuzzy, concept-level — checks groundedness, semantic alignment, domain specificity

If both tracks agree on the relative ordering of groups (e.g., Treatment C > Treatment B > Treatment A > Baseline), the evaluation is robust. If they disagree, the scoring system itself is suspect — fix it before interpreting any results.

This cross-validation is your protection against:
- A single scorer with hidden biases
- Metrics that reward the wrong behavior
- Accidental correlation between scoring artifact and treatment group

### Auto Metrics (Track A Example)

| Metric | What it measures | Range |
|--------|-----------------|-------|
| output_completeness | Required schema field coverage | 0-10 |
| required_item_coverage | Gold checklist hit rate | 0-10 |
| unsupported_claim_count | Forbidden pattern detection | -5-0 |
| constraint_awareness | Constraints with mitigation | 0-10 |
| domain_specificity | Domain-precise vs generic terminology | 0-10 |
| evidence_citation_rate | Artifact reference count | 0-10 |

The exact metrics depend on your domain. The principle: **each metric should measure one clearly defined construct**, not a grab bag of heuristics.

### Score Family Separation

When comparing groups with different information access (e.g., baseline vs. knowledge-augmented), never mix access-dependent metrics into an undifferentiated total score.

Separate scoring into distinct families:

| Family | Purpose | Fair across all groups? |
|--------|---------|------------------------|
| `planning_quality` | Completeness, coherence, structure | Yes — any group can produce a well-formed plan |
| `evidence_discipline` | Citation behavior, unsupported claims | Informative but favors augmented groups |
| `domain_correctness` | Domain-specific accuracy | Conditional — requires human review |
| `execution_specificity` | Precision of tools, steps, parameters | Yes — any group can be specific |
| `traceability` | Source provenance, run lineage | Only relevant for augmented groups |

**Rule**: Report each family separately before any composite score. Never claim broad planning-quality improvement from a win driven mainly by evidence-access metrics. Each metric should annotate whether it requires evidence access (`evidence_access_required: true/false`).

### Metric Fairness Annotation

Every metric in a multi-group comparison must declare whether it is **fair** across all groups or **condition-dependent**. This prevents the most common evaluation error: claiming global improvement from a metric that only one group can access.

Annotate each metric with:

| Field | Values | Purpose |
|-------|--------|---------|
| `evidence_access_required` | `true` / `false` | Does this metric need card IDs, evidence references, or provenance logs that only augmented groups can provide? |
| `compare_mode` | `fair` / `evidence_aware` | Should this metric be interpreted as a fair comparison or as a comparison of evidence-use behavior? |
| `review_mode` | `auto` / `human_sample` / `hybrid` | Can this metric be trusted automatically, or does it need human review before forming conclusions? |

**Consequence**: A score family like `planning_quality` should only contain metrics with `evidence_access_required: false`. Metrics like `evidence_citation_rate` belong in `evidence_discipline`, annotated as `evidence_aware`. The global total score is demoted to a secondary descriptive statistic — never the primary thesis claim.

This pattern was implemented in scoring v3 as the five-family separation, where `planning_quality` and `execution_specificity` are annotated as `fair`, while `evidence_discipline` and `traceability_provenance` are annotated as `evidence_aware`.

### Track B Additions

| Metric | What it measures |
|--------|-----------------|
| evidence_groundedness | Does output text actually USE cited artifact concepts? |

**Groundedness method**: Extract keywords from each cited artifact → check if any appear in the output text. Prevents "citation without usage" — a common LLM failure mode where the model lists references but does not actually apply them.

### Fuzzy Matching

For non-English text or paraphrased content, use `difflib.SequenceMatcher` instead of exact substring matching:

```python
from difflib import SequenceMatcher
def fuzzy_match(a: str, b: str, threshold: float = 0.6) -> bool:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= threshold
```

## Statistics: Small-n Done Right

With small samples (n < 20 per group), p-values lose statistical power. Prioritize:

1. **Cohen's dz (paired)** — effect size for within-subject design
2. **95% CI** — confidence interval for mean
3. **Paired t-statistic** — parametric comparison
4. **Wilcoxon signed-rank** — non-parametric, no normality assumption
5. **p-value** — report but don't rely on exclusively

### Effect Size Interpretation

| Cohen's d | Effect |
|-----------|--------|
| 0.2 | small |
| 0.5 | medium |
| 0.8 | large |
| ≥ 1.0 | very large |

**Principle**: A large effect size with a borderline p is stronger evidence than a tiny effect with p < 0.01. Effect size tells you *how much* the treatment matters; p-value only tells you *how surprised* you would be if it didn't.

## Reproducibility Package

The statistics script should have a `--reproduce` flag that generates:
- `METHOD.md` — analysis method description
- `GIT_COMMIT` — exact git commit hash
- `analysis.csv` — all statistics in machine-readable form

**Principle**: "Package the analysis, don't document the steps."

**Wrong**: "I documented the steps in a README."
**Right**: "Run `python scripts/stats.py --reproduce output/` and you get the exact same result."

## Scoring Discipline

- Every scorer outputs `RUBRIC_VERSION` and `COMPARE_MODE` metadata
- CSV exports include rubric version for traceability
- Compare mode for multi-run side-by-side tables
- Force UTF-8 stdout to prevent encoding errors (critical on Windows):

```python
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass
```

## Scoring Robustness Checklist

- [ ] Track A and Track B produce consistent relative ordering
- [ ] Compare mode works across all groups
- [ ] CSV export includes version metadata
- [ ] Per-metric details printed for debugging
- [ ] Forbidden patterns are task-specific, not hardcoded globally
