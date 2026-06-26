---
name: A/B Interpreter
description: Interpret A/B test results for ecommerce campaigns and pages by checking statistical significance, practical effect size, and next-step recommendations.
---

# A/B Interpreter

Most ecommerce A/B tests get called too early, too late, or on the wrong metric — and the team ships whichever variant "looks like" it won without a clean read on whether the lift was real, large enough to matter, or durable past the novelty window. This skill turns raw test results into a disciplined go or no-go verdict with statistical significance, practical effect size, segment checks, and a prescribed next step so every test actually moves the business.

## Quick Reference

| Decision | Strong signal | Acceptable | Weak / Redesign |
|---|---|---|---|
| Statistical significance | p < 0.05, two-tailed, sample powered to 80% | p between 0.05 and 0.10 with large sample | p > 0.10 or sample underpowered |
| Practical effect size | Lift exceeds MDE and the lower bound of the 95% CI is positive | Lift exceeds MDE but CI barely crosses zero | Lift below MDE even if "significant" |
| Test duration | Ran across at least two full weekly cycles | Ran 10 to 14 days, no major anomalies | Under 7 days or overlaps a holiday/promo |
| Sample ratio | Observed split within 1% of planned | Split within 2% | SRM > 2% — suspect tracking |
| Guardrail metrics | All guardrails flat or positive | One guardrail flat, one minor regression | Any revenue, refund, or AOV guardrail regressed |
| Segment stability | Lift positive across all key segments | Lift positive in 3 of 4 segments | Contradicting segments (new vs returning, device, geo) |
| Novelty risk | Lift holds in final week of test | Lift decays mildly over time | Lift front-loaded and decays past week two |

## Solves

- Teams ship winners that were noise, then can't reproduce the lift in production
- Stakeholders disagree on whether a 3% lift with p = 0.08 is a "win"
- Growth managers call tests after 3 days on a heavy-traffic weekend and miss weekday reality
- Novelty-effect lifts decay in production and no one notices until the quarter closes
- Segment-level contradictions (tablet users regress) get averaged away in the topline
- Guardrail metrics like refund rate silently offset the headline conversion win
- Test readouts lack a prescribed next step, so learnings do not compound

## Workflow

1. **Ingest the test setup.** Read the hypothesis, variants, traffic split, start and end dates, primary metric, minimum detectable effect (MDE), and guardrail list. Flag any required field that is missing and stop if the primary metric is not defined in advance.
2. **Sanity-check the data.** Confirm the observed traffic split matches the planned split (SRM check). Look for outlier days, tracking gaps, or bot spikes. If the split is off by more than 2%, mark the test inconclusive and recommend re-running.
3. **Run the core statistical check.** Use a two-proportion z-test for conversion rate, Welch's t-test for continuous revenue metrics. Compute the p-value, the observed lift, and a 95% confidence interval around the lift.
4. **Compare lift against MDE.** A significant result that falls below MDE is practically meaningless; a non-significant result that exceeds MDE suggests under-powering and an extension. The lower bound of the CI must exceed zero for a confident ship call.
5. **Check segments and guardrails.** Split by new vs. returning, device, traffic source, and geography. Any segment that contradicts the aggregate direction should be called out. Any guardrail regression (bounce rate, refund rate, add-to-cart) should be weighed against the primary lift.
6. **Assess novelty and seasonality.** If the test ran under 14 days, flag novelty risk. Compare week one to week two. If lift concentrated in week one, recommend extending or running a repeat test after a cooldown.
7. **Deliver the verdict and next step.** Write a plain-language verdict (ship, kill, extend, redesign), the reasoning a skeptical analyst would demand, and the prescribed follow-up test or monitoring metric. Every readout ends with one concrete action.

## Example 1: Shopify PDP button copy test

**Inputs.** Hypothesis: "Buy Now" outperforms "Add to Cart" on the product page. 14-day test, 50/50 split, 48,200 visitors each arm. Control conversions: 1,446 (3.00%). Variant conversions: 1,640 (3.40%). MDE set at 0.25 percentage points. Guardrails: refund rate and AOV.

**Analysis.** Two-proportion z-test gives p = 0.02 with a 95% CI on the lift of +0.08 to +0.72 pp. Observed lift of 0.40 pp exceeds MDE of 0.25. Sample split was 50.1 / 49.9. New vs. returning both show directional lift. Refund rate flat. AOV down 1.2% (not significant, CI crosses zero). Week one lift 0.45, week two 0.35 — mild decay, within tolerance.

**Verdict.** Ship. The result is statistically and practically significant; guardrails are intact. Next step: monitor AOV weekly for four weeks post-rollout and re-test "Buy Now" against a bundled offer CTA in Q3.

## Example 2: Email subject line test with under-powered readout

**Inputs.** Two subject lines sent to 8,000 recipients each. Opens: A = 1,440 (18.0%), B = 1,560 (19.5%). MDE of 2 percentage points was required to justify the winner for list-wide rollout.

**Analysis.** Two-proportion z-test p = 0.022 — "significant". Observed lift of 1.5 pp is below the 2.0 pp MDE. 95% CI on the lift is +0.2 to +2.8, straddling the MDE. No segment breakdown provided.

**Verdict.** Do not ship yet. The result is statistically significant but falls short of the practical threshold the team pre-committed to. Extend the test or re-run with a larger list to narrow the CI. Do not rationalize the "win" just because p < 0.05 — the pre-committed MDE exists precisely to prevent that.

## Common mistakes

- **Peeking.** Calling the test early the moment p drops below 0.05 inflates false positive rates dramatically. Pre-commit to a sample size and honor it.
- **Ignoring MDE.** A statistically significant but practically tiny lift does not justify a rollout. The MDE is the business's pre-committed threshold.
- **No SRM check.** A broken randomizer can fabricate lifts. Always verify the observed split matches the planned split.
- **Averaging away segments.** A +2% topline with a -5% tablet regression is not a clean win. Pull the segment cuts before celebrating.
- **One-week tests.** Weekday vs. weekend behavior differs, and novelty effects dominate week one. Run at least two full business cycles.
- **Mixing up absolute and relative lift.** "20% lift" on a 3% base rate means +0.6 pp, not +20 pp. Always state which you are reporting.
- **Treating p-values as probability the hypothesis is true.** A p-value is the probability of the observed data under the null, not the probability the variant is better.
- **No guardrails declared upfront.** Retrofitting guardrails after seeing results invites cherry-picking. Name them before the test starts.
- **Ignoring post-ship drift.** Novelty decay and seasonality can erode a shipped win. Always prescribe a post-ship monitoring window.

## Resources

- `references/output-template.md` — The four-block readout structure
- `references/statistical-tests.md` — Choosing the right test for the metric type
- `references/segment-playbook.md` — Standard segments to cut and what each contradiction signals
- `assets/ab-readout-checklist.md` — Pre-flight checklist for every readout you deliver
