# Choosing the Right Statistical Test

The test you run depends on the metric shape. Mismatches produce confident-sounding numbers that mean nothing. Use this guide to pick correctly before computing anything.

## Conversion rate, click-through, signup rate

These are proportions — each visitor either converts or does not. Use a **two-proportion z-test** for the difference in rates. Pair it with a Wilson or Newcombe confidence interval on the lift rather than a naive normal approximation, especially for sub-1% rates.

- Required inputs: per-arm visitor count and conversion count
- Reports: absolute lift, relative lift, p-value, CI
- Watch out for: extremely low base rates (under 0.5%) where normal approximations break down

## Revenue per user, average order value

These are continuous and often heavily skewed by a small number of large orders. Use **Welch's t-test** (unequal variances) on the mean per visitor, not per converter. Report median and a bootstrap CI alongside the mean when the distribution has a long tail.

- Required inputs: per-user revenue series for each arm (not just summaries)
- Reports: mean lift, median lift, bootstrap CI, t-test p-value
- Watch out for: one whale order flipping the call — bootstrap helps detect this

## Session length, pages per session, engagement

Also continuous but typically less skewed than revenue. Welch's t-test works. If the distribution is bimodal (bouncers vs. deep engagers), report the breakdown separately before pooling.

## Count data: reviews per purchase, items per cart

Use a **Poisson regression** or a negative binomial test if the variance exceeds the mean. A simple t-test on means is acceptable for large samples but understates variance for small ones.

## Survival / time-to-event

For metrics like time-to-first-purchase or churn, use a **log-rank test** and report a Kaplan-Meier curve. Do not use a t-test on censored data.

## Multiple metrics at once

If you look at 5 metrics, the probability at least one returns p < 0.05 by chance is over 22%. Either pre-commit to a single primary metric, apply a Bonferroni or Benjamini-Hochberg correction, or declare guardrails as non-decision metrics where a regression is disqualifying but a "win" cannot rescue a flat primary.

## Multiple variants

Running 4 variants creates 6 pairwise comparisons. Use a Tukey HSD or Dunnett's test against control rather than running independent two-sample tests.

## When to use Bayesian

If stakeholders want statements like "probability B beats A is 94%," a Bayesian framework with a weakly informative prior gives more intuitive outputs than a p-value. The decision cost structure remains the same — you still need an MDE and guardrails.

## Sample size sanity check

After the test, confirm the achieved power was at least 80% at the MDE. An underpowered test that shows "no significant difference" does not mean the variants are equal — it means you could not detect the effect you cared about.
