---
name: Ad Creative Testing
description: Design structured A/B test hypotheses for ad creatives, hooks, destination pages, and audience segments with clear success metrics and test duration logic.
---

# Ad Creative Testing

Design structured A/B test hypotheses for ad creatives, hooks, destination pages, and audience segments with clear success metrics and test duration logic. Stop guessing which ad works and start building a repeatable testing machine that improves ROAS with each iteration.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Variables tested per experiment | 1 variable isolated | 1 primary + 1 secondary (flagged) | Multiple variables in one test |
| Sample size per variant | 500+ conversions | 200–499 conversions | Under 100 conversions |
| Test duration | 2–4 weeks | 1–2 weeks with caveat | Under 7 days |
| Statistical confidence target | 95% confidence | 90% confidence | Declaring winner under 80% |
| Primary metric choice | Conversion rate or ROAS | CTR (with caveat) | Vanity metric (likes, reach) |
| Creative variable to test first | Hook (first 3 seconds) | Offer/headline | Brand colors/logo placement |
| Budget split | 50/50 even split | 70/30 (asymmetric with rationale) | One variant gets <20% of budget |

## Solves

1. **Multi-variable contamination** — Testing hook, offer, and format simultaneously means you can't attribute any improvement to a specific change.
2. **Underpowered tests** — Declaring a winner on 50 conversions creates false confidence and leads to scaling losers.
3. **Wrong primary metric** — Optimizing for CTR when the goal is profit leads to high-traffic, low-converting ads that inflate spend.
4. **Too-short test windows** — Ending tests after 3 days misses the natural performance cycle of ads (learning phase, peak, fatigue).
5. **No structured hypothesis** — Testing random creative ideas with no documented prediction means learnings don't compound across iterations.
6. **Audience bleed** — Running audience A/B tests without proper segment separation means both variants serve the same people, corrupting results.
7. **Ignoring creative fatigue signals** — Scaling a winning creative without monitoring frequency and CTR decline leads to wasted spend at the exact moment a test should be run.

## Workflow

### Step 1 — Define the Test Objective and Primary Metric
Start by answering: what specific business outcome is this test designed to improve? Map the objective to a primary metric:
- **Reduce cost per purchase** → Primary metric: Cost per purchase / ROAS
- **Increase click volume on fixed budget** → Primary metric: CTR (but validate CTR improvements lead to purchases)
- **Improve video content performance** → Primary metric: Video-through rate (VTR) to hook rate to conversion
- **Find the best-converting destination page** → Primary metric: Destination page conversion rate (not bounce rate)

Document the primary metric before designing the test. Do not change it after launch.

### Step 2 — Write the Hypothesis Statement
A structured hypothesis has three parts:
- **If** we change [specific variable]
- **Then** we expect [specific measurable outcome]
- **Because** [the reasoning based on evidence or prior data]

Example: "If we change the hook from a product demonstration opening to a pain-point question opening, then we expect a 15% improvement in thumb-stop rate and a 10% reduction in cost per initiate checkout, because our audience research shows the target buyer is problem-aware but not solution-aware."

A weak hypothesis: "Let's try a different video style and see if it performs better." No prediction, no reasoning, no measurable outcome.

### Step 3 — Isolate the Variable
Identify the single variable you are changing between Variant A (control) and Variant B (challenger). Everything else must remain identical:
- **Hook test**: Same offer, same body copy, same CTA, same product, same format — only the first 3 seconds change
- **Offer test**: Same creative format, same hook, same visual — only the offer text/structure changes
- **Destination page test**: Same ad creative driving to two different destination page variants
- **Audience test**: Same creative, same budget, different audience segments (use proper audience exclusions to prevent overlap)
- **Format test**: Same offer/copy presented in different formats (15s video vs. static image vs. carousel)

### Step 4 — Determine Sample Size and Test Duration
Use the following framework:
- **Minimum sample size**: 200 conversions per variant before considering a result meaningful; 500+ for high confidence
- **Minimum duration**: 7 days (to capture weekly seasonality patterns); 14 days preferred
- **Budget guidance**: If your current ad spend generates 50 purchases/week per variant, you need 4–10 weeks to reach 200–500 conversions — adjust test budget or accept a longer timeline
- **Statistical significance**: Use a significance calculator (e.g., AB Testguide, Optimizely Stats Engine) — target 95% confidence; do not declare winners below 90%

### Step 5 — Set Up the Test Structure
For paid social (TikTok Ads, Meta Ads):
- Create a dedicated test campaign or ad set
- Use even 50/50 budget split unless you have a specific reason to weight differently
- Disable automatic creative optimization during the test (prevents the platform from picking a winner before you have enough data)
- Set start/end dates and document them
- Confirm the test is running on the correct audience and that audience exclusions are in place if testing segments

### Step 6 — Monitor During the Test
Check performance at regular intervals (not daily — resist the urge to call a winner early):
- **Day 3–4**: Verify both variants are delivering and spending approximately equally (not a data review — just a delivery check)
- **Day 7**: Check if there are any technical issues (a variant not spending, creative rejected); do not make creative decisions yet
- **Day 14**: First data review; check sample sizes; run significance test if above 200 conversions per variant
- **Day 21–28**: Final read if sample size reached; declare winner or extend if still underpowered

Watch for these early kill signals (valid reasons to stop a test before planned end):
- One variant has a CPA 3× or higher than the other after 100+ conversions (likely a strong loser; killing it quickly saves spend)
- One variant has delivery problems and is not spending

### Step 7 — Document the Result and Build the Learning
After the test concludes:
- Record the hypothesis, test structure, results, and winning variant
- Calculate the magnitude of improvement (e.g., "hook B reduced CPA by 22%")
- Identify what the result implies for the next test (e.g., "pain-point hooks outperform demonstration hooks for this audience — next test: which pain point resonates most?")
- Add to a test log that accumulates learnings across campaigns

This log becomes your competitive advantage over time.

## Examples

### Example 1 — Hook A/B Test for TikTok Shop Product

**Input:**
- Product: Skincare serum, TikTok Shop UK
- Current creative: Opens with 3-second product shot + "Now available in the UK"
- Hypothesis: Pain-point hook will outperform product demonstration hook
- Primary metric: Cost per purchase (current: £18)
- Weekly volume: ~60 purchases/week

**Structured Test Design:**

```
TEST HYPOTHESIS
If we change the video hook from a product shot ("Now available in the UK") to a
pain-point question ("Struggling with dull skin even after your skincare routine?"),
then we expect a 20% reduction in cost per purchase,
because our top-performing organic videos use problem framing and our current
hook has a 15% thumb-stop rate vs. the 25–30% we see on viral skincare content.

VARIABLE BEING TESTED
Variant A (Control): Opens with close-up product shot + "Now available in the UK"
Variant B (Challenger): Opens with creator asking "Struggling with dull skin even
after your skincare routine?" — same body copy, same CTA, same offer

EVERYTHING IDENTICAL IN BOTH VARIANTS
✓ Offer: same (no discount, standard price)
✓ Body copy: same
✓ Button text: "Shop Now" in both
✓ Video length: 15 seconds in both
✓ Target segment: same (UK, F 25–44, niche: skincare)
✓ Budget: £50/day each, 50/50 split

SAMPLE SIZE & DURATION PLAN
Target: 200+ purchases per variant
Current rate: 60/week × £50/day test budget ÷ current £100/day = ~30/week per variant
Minimum test duration: 7 weeks to reach 210 purchases per variant
Decision: Run for 8 weeks to be safe; check statistical significance at week 6

SUCCESS CRITERIA
- Primary: Variant B achieves ≥15% lower cost per purchase than Variant A with ≥90% statistical confidence
- Secondary: Variant B thumb-stop rate (3-second view rate) is higher than Variant A
- Kill switch: If either variant reaches CPA of £40+ after 100 purchases, kill it and investigate
```

### Example 2 — Landing Page A/B Test for DTC Brand

**Input:**
- Product: Protein supplement, Shopify store
- Ad platform:  Generic homepage
- Test idea — Product-specific landing page vs. homepage
- Primary metric — Landing page conversion rate (current — 1.8%)
- Monthly traffic to landing — ~8,000 visitors/month

**Structured Test Design:**

```
TEST HYPOTHESIS
If we send ad traffic to a dedicated product landing page (with product video,
reviews, and FAQ above the fold) instead of the generic homepage,
then we expect landing page conversion rate to increase from 1.8% to 2.5%+,
because product-specific pages remove navigation distractions and maintain
message-match with the ad creative.

VARIABLE BEING TESTED
Variant A (Control): Traffic → Homepage (generic, navigation visible)
Variant B (Challenger): Traffic → Dedicated product landing page (no nav, product
video hero, 5 reviews, FAQ, single CTA)

SAMPLE SIZE CALCULATION
Current conversion rate — 1.8% (to detect 2.5% with 95% confidence, 80% power)
Required visitors per variant — ~2,400 (use AB Testguide calculator)
Current monthly traffic to this landing — 8,000/month
50/50 split — 4,000 per variant per month
Estimated time to significance — ~18 days (assuming even traffic distribution)
Duration — Run for 21 days minimum to capture day-of-week patterns

SUCCESS CRITERIA
- Primary — Variant B conversion rate exceeds Variant A by ≥15% with ≥95% confidence
- Secondary — Revenue per visitor (not just conversion rate — larger carts matter)
- Kill switch — No kill switch for low-performing variant; this is a page test, not a spend test
```

## Common Mistakes

1. **Changing two things and calling it an A/B test** — Testing a new hook AND a new offer simultaneously means any improvement (or degradation) is unattributable. Isolate one variable per test.

2. **Declaring a winner after 3 days** — Most ad platforms have a 7-day learning phase. Early data is noisy, especially for conversion-focused campaigns. Decisions made on day 3 are often wrong.

3. **Using CTR as the primary metric when you care about purchases** — Ads with high CTR and low conversion rates increase spend without increasing revenue. Always validate that CTR improvements translate to downstream conversion improvements.

4. **Not calculating required sample size before starting** — If your current volume means you'd need 6 months to reach significance, you should increase test budget, widen the test window, or pick a higher-frequency metric as a leading indicator.

5. **Running audience tests without exclusions** — If Audience A and Audience B overlap (e.g., both are "females 25–44 interested in beauty"), the same person can be served both variants, corrupting the test.

6. **Letting the platform auto-optimize mid-test** — Most paid social platforms have creative optimization features that will automatically shift budget toward the "better" performing creative. Disable this during a test — it will pick a winner long before you have statistical significance.

7. **Not documenting hypotheses before seeing results** — Writing a "hypothesis" after you see the data is confirmation bias, not testing. Record your prediction before the test starts.

8. **Scaling a winner without monitoring creative fatigue** — Winning creatives eventually fatigue. Monitor CTR and frequency weekly after scaling; begin a new iteration test before performance declines.

## Resources

- [output-template.md](references/output-template.md) — Structured output format for A/B test designs
- [hypothesis-library.md](references/hypothesis-library.md) — Pre-built hypothesis templates by test type
- [metrics-reference.md](references/metrics-reference.md) — Primary and secondary metric selection guide by campaign objective
- [test-log-template.md](assets/test-log-template.md) — Tracking template for recording test results and building a learning library
