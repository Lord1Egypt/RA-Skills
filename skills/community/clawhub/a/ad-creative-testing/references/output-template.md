# Output Template — Ad Creative A/B Test Design

Use this template for every A/B test design output. A complete test design includes all five sections below. An incomplete test design missing the hypothesis statement or sample size plan is not actionable.

---

## [Campaign / Product Name] — A/B Test Design

**Test type:** [Hook / Offer / Landing page / Audience / Format / CTA]
**Platform:** [TikTok Ads / Meta Ads / Google Ads / etc.]
**Primary metric:** [Specific metric — e.g., Cost per purchase, Landing page conversion rate]
**Current baseline:** [Current metric value — e.g., £18 CPA, 1.8% conversion rate]
**Test budget:** [£/$/day per variant × number of variants]
**Test designed:** [Date]

---

## Section 1 — Hypothesis Statement

> **If** we change [specific, single variable],
> **then** we expect [specific measurable outcome with a number],
> **because** [evidence-based reasoning — prior data, audience research, or documented pattern].

*Example — "If we change the video hook from a product demonstration to a pain-point question, then we expect a 15–20% reduction in CPA, because our organic content using problem-framing generates 2× higher engagement than product-first content for this audience."*

---

## Section 2 — Test Structure

### Variable Being Tested
**Variant A (Control):** [Describe exactly what the current/control version contains — be specific]

**Variant B (Challenger):** [Describe exactly what the challenger version contains — be specific about the single change]

### Elements That Must Remain Identical
| Element | Variant A | Variant B |
|---|---|---|
| Offer / Price | [Same] | [Same] |
| Body copy | [Same] | [Same] |
| CTA text | [Same] | [Same] |
| Video length / Format | [Same] | [Same] |
| Target audience | [Same] | [Same] |
| Budget | [Same] | [Same] |
| [Other elements] | [Same] | [Same] |

**Single variable that differs:**
- Variant A — [Describe control version of the variable]
- Variant B — [Describe challenger version of the variable]

---

## Section 3 — Sample Size and Duration Plan

**Current conversion volume:** [Conversions/week or conversions/month at current spend]
**Required sample per variant:** [Use significance calculator; minimum 200, target 500]
**Conversion rate assumption:** [Current primary metric value]
**Minimum detectable effect (MDE):** [The minimum improvement that would be meaningful to act on, e.g., 15% reduction in CPA]
**Statistical confidence target:** [95% preferred; 90% minimum]
**Estimated test duration:** [Weeks needed based on volume + sample size requirement]
**Budget per variant per day:** [£/$]

**Duration:** Run for [X] weeks. First significance check at [X] days (once [X] conversions reached per variant). Use [AB Testguide / Optimizely Stats Engine / internal tool] to check significance.

---

## Section 4 — Decision Criteria

**Declare Variant B the winner if:**
- Variant B [primary metric] improves by [minimum threshold, e.g., ≥15%] vs. Variant A
- Statistical confidence ≥ [90/95]%
- Test ran for at least [X] days

**Declare no winner (extend or re-test) if:**
- After [X] days, confidence is below [80]% — extend the test or redesign
- Budget constraints prevented reaching minimum sample size

**Early kill signals:**
- Either variant CPA exceeds [3× current CPA] after [100+] conversions → stop that variant, investigate
- One variant has delivery issues and is not spending → pause and troubleshoot

---

## Section 5 — Post-Test Documentation

To be completed after the test concludes:

**Result:** Variant A / Variant B / No clear winner

**Key metrics at conclusion:**
| Metric | Variant A | Variant B | Difference | Statistical confidence |
|---|---|---|---|---|
| [Primary metric] | [Value] | [Value] | [+/- %] | [%] |
| [Secondary metric 1] | [Value] | [Value] | [+/- %] | N/A |
| [Secondary metric 2] | [Value] | [Value] | [+/- %] | N/A |

**Hypothesis confirmed:** Yes / No / Partially

**Key learning:** [1–2 sentence summary of what this test revealed about your audience or creative strategy]

**Next test implication:** [What does this result suggest as the next variable to test?]

**Winning variant status:** [Scaled / Paused / Incorporated into new creative brief]
