# Scientific Thinking Patterns for AI-Conducted Research

> Distilled from real-world agent-led research failure analysis

These patterns guard against the most common failure modes of AI-conducted research. They are not domain-specific — they apply whether evaluating language models, vision systems, or biological simulations.

## 1. Evidence Boundary Awareness

**Know what your data proves and what it does not.**

An AI agent's instinct is to over-claim. A strong finding about output behavior can easily be reframed as a quality improvement — but the data may not support that leap.

**Correction**: Before writing any conclusion, ask: "What single alternative explanation survives if I rephrase this claim more cautiously?"

**Practice**:
- Every claim in writing drafts must point to evidence
- Unverified claims marked `[REF-MISSING]`
- Claims needing human judgment marked `[CRITICAL-CHECK]`
- When in doubt, underclaim. Underclaiming is fixable; overclaiming is reputation damage.

## 2. Pipeline Before Interpretation

**When a result contradicts expectations, verify the execution chain before questioning the hypothesis.**

In one real case, a treatment group showed no improvement over baseline. The initial diagnosis was "the method is ineffective" — a paper-level conclusion. The actual cause: the task configuration file had empty artifact lists for 4 out of 5 tasks. The treatment group received zero input. A 5-minute file check prevented a false negative.

**Protocol**:
```
Counter-intuitive result
    → check manifest (right runs loaded?)
    → check runner prompt construction (right context injected?)
    → check data input (fields non-empty? correct IDs?)
    → check scorer (metric computing what we think?)
    → check output files (no corruption? right paths?)
    → ONLY THEN question methodology
```

**Key insight**: Systems engineering problems take 15 minutes to fix. Methodology problems require redesign. Distinguishing them saves weeks.

This is the single most expensive mistake in agent-led research: interpreting a pipeline failure as a methodology failure.

## 3. Effect Size Over p-Value

With small-n experiments (n < 20 per group), p-values lose statistical power.

**Always report**:
- Cohen's dz (paired effect size) as the primary signal
- 95% CI for mean
- Delta in original units
- Supplement with paired t-statistic and Wilcoxon signed-rank

**Never**: Report "p < 0.05" as the sole evidence of effect.

**Why**: A Cohen's d of 0.8 means "large effect" regardless of sample size. A p of 0.04 with n=5 could easily flip to p=0.06 with one more data point. Effect size tells the magnitude of the finding; p-value only tells the stability of the noise.

*Detailed statistical methodology is in `references/scoring-statistics.md`.*

## 4. Reproducibility as Toolchain

**"Package the analysis, don't document the steps."**

A `--reproduce` flag should write METHOD.md + GIT_COMMIT + raw data to a timestamped directory.

**Wrong**: "I documented the steps in a README."
**Right**: "Run the analysis script with `--reproduce` and you get the exact same result."

Documentation drifts. Scripts don't. A runnable reproduction package is the only form of reproducibility that survives contact with time.

## Additional Principle: Failed Runs Are Evidence

**Do not delete failed experiments to make progress look cleaner.**

Failed runs are:
- Process evidence for future evaluation
- Comparison material for debugging
- Protection against survivorship bias

Register them in the manifest with status=failed, error_type, and retry_of pointer. A repo that only contains successes is a repo that cannot be trusted.
