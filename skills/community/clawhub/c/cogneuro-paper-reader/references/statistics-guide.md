# Statistics Guide — Reading the Numbers in These Papers

How to interpret and report the statistics commonly used in attention, memory,
and population-neuroscience papers.

## Effect sizes

- **Cohen's d** — standardized mean difference. Rough benchmarks:
  - 0.2 = small, 0.5 = medium, 0.8 = large.
  - Report the value and direction (e.g. "d = 1.68, a large effect").
- **Pearson's / Spearman's r** — correlation strength. Rough benchmarks:
  - 0.1 small, 0.3 medium, 0.5 large.
  - **Spearman's r** is rank-based (non-parametric); used when data are not
    normally distributed (e.g. RTs, accuracy).
- **95% confidence interval (CI)** — the range that plausibly contains the true
  effect. If it excludes zero, the effect is "reliable" at p < .05.

## Null-hypothesis testing

- **p-value** — probability of the observed data (or more extreme) under the null
  hypothesis. These papers often report exact p, with values below 1/1000
  approximated as `p < 0.001`.
- **One-tailed vs. two-tailed** — directional hypotheses (e.g. "fast RTs predict
  worse memory") use one-tailed tests; non-directional comparisons use two-tailed.
  Note which one the paper used.
- **Bootstrap** — resample participants with replacement (e.g. 100,000 times) and
  compute the statistic each time; the distribution gives CIs and a p-value
  (proportion of iterations in the opposite direction). A robust, non-parametric
  alternative used by deBettencourt et al. (2019).

## Bayesian statistics

- **Bayes factor (BF₀₁)** — evidence for the null vs. the alternative:
  - BF₀₁ > 3 = moderate evidence for the null; > 10 = strong evidence.
  - Used in deBettencourt et al. (2019) Experiment 3 to argue that attention and
    memory precision did *not* co-vary.

## Task-specific indices

- **A′ (A-prime)** — a non-parametric sensitivity index combining hits and false
  alarms; chance = 0.5, perfect = 1.0. Used for sustained-attention accuracy when
  one response is rare.
- **Working memory capacity K** — K = N × (H − FA), where N is set size, H is hit
  rate, FA is false-alarm rate. Estimates the number of items held in mind.
- **Accuracy on frequent vs. infrequent trials** — frequent trials are usually
  easy (high accuracy); infrequent (rare) trials are where lapses show up as errors.
- **Slope across blocks** — the linear change in accuracy over blocks; a negative
  slope indexes the vigilance decrement.

## Memory error modeling (continuous report)

- **Mixture model** — response errors are modeled as a mixture of a **von Mises
  distribution** (centered on the true value; its dispersion s.d. = precision) and
  a **uniform distribution** (height g = guessing probability). Fit with maximum
  likelihood (e.g. MemToolbox).

## What to report in a summary

For each key result, give: the descriptive statistics (means ± uncertainty), the
test statistic (d, r, t), the effect size, and the p-value or BF. If any is
missing, write "not reported".
