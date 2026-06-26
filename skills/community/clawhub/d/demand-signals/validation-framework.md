# Demand Signal Validation Framework

This framework provides a structured method for determining whether a detected demand signal represents a real, sustainable, and actionable commercial opportunity or whether it is noise, manipulation, or a transient spike not worth committing inventory capital to.

Apply this framework to every signal that passes your initial collection phase. A signal must clear all three validation gates (Reality, Sustainability, Actionability) to qualify for demand sizing and competition assessment.

---

## Gate 1: Is the Signal Real?

This gate filters out false positives, manufactured signals, and data artifacts. A "real" signal reflects genuine consumer interest that exists independently of any single promotional event or algorithmic anomaly.

### Multi-Source Confirmation Test

**Threshold:** The signal must appear in at least 2 independent source categories (social, search, marketplace, supplier).

| Confirmation Level | Sources Confirming | Interpretation |
|---|---|---|
| Strong | 3+ independent source categories | High confidence the signal is real |
| Acceptable | 2 independent source categories | Proceed with caution, monitor for third source |
| Insufficient | 1 source category only | Do not proceed; continue monitoring |

**How to apply:** List every data point you have collected for this signal. Group them by source category: social media (TikTok, Instagram, Reddit), search data (Google Trends, Keyword Planner), marketplace data (Amazon BSR, listing count, reviews), and supplier/industry data. Count how many categories have confirming evidence. A signal that appears only in TikTok engagement data but shows no corresponding search volume increase or marketplace movement has not passed this test.

**Common pitfall:** Do not count multiple data points from the same source category as separate confirmations. Three different TikTok videos are one source category, not three sources.

### Organic Authenticity Check

**Purpose:** Determine whether the signal is organically driven or artificially manufactured through paid campaigns, bot activity, or coordinated promotion.

**Indicators of organic signal:**
- Content from many independent creators with different audience sizes and niches
- Gradual growth curve rather than a single-day explosion
- Geographic distribution across multiple regions
- User-generated content showing actual product usage (not just reaction content)
- Comment sections with varied, natural language

**Red flags for manufactured signal:**
- All engagement traces back to a single creator or a coordinated group
- Sudden spike with no prior baseline activity
- Engagement metrics that do not match content quality (e.g., a low-effort video with millions of views and suspiciously uniform comments)
- All Amazon reviews posted within a narrow time window or using similar language
- Referral patterns suggesting incentivized sharing

**Scoring:** Assign Organic (proceed), Uncertain (investigate further), or Manufactured (discard signal).

### Data Quality Verification

**Purpose:** Confirm that the data you are interpreting is accurate and that you are not misreading the source.

**Checks to perform:**
- Verify Google Trends data is for the correct geography and time period. A search trend in India does not validate a US market opportunity.
- Confirm Amazon BSR data is from the correct category. BSR is category-relative; a product can have a BSR of 5,000 in a large category and a BSR of 50 in a subcategory.
- Ensure social media metrics are not inflated by paid promotion. Check if posts are labeled as sponsored or if the creator has disclosed a brand partnership.
- Validate that supplier order data refers to the specific product type, not a broader category.

**Outcome of Gate 1:** Signal classified as REAL (proceed to Gate 2), UNCERTAIN (gather more data, re-evaluate in 7 days), or FALSE (discard and document for future reference).

---

## Gate 2: Is the Signal Sustainable?

A real signal may still be ephemeral. This gate assesses whether demand will persist long enough for you to source, ship, and sell profitably.

### Duration and Trajectory Test

**Threshold:** The signal must show growth sustained for a minimum of 14 consecutive days.

| Duration | Trajectory | Interpretation |
|---|---|---|
| 21+ days | Accelerating or steady growth | Strong sustainability indicator |
| 14-21 days | Steady growth | Acceptable; proceed with monitoring |
| 14-21 days | Decelerating growth | Caution; may be peaking early |
| Under 14 days | Any pattern | Too early to assess sustainability; wait |

**How to apply:** Plot the available data points on a timeline. For Google Trends, use daily resolution for the past 90 days. For social media, count the number of new creator posts or engagement volume per day/week. Look at the shape of the curve:
- **Hockey stick (accelerating):** Strongest indicator of an early-stage sustainable trend
- **Linear climb:** Good indicator of steady, organic demand growth
- **Spike and plateau:** Acceptable if the plateau holds for 14+ days above baseline
- **Spike and decline:** Likely an event-driven moment, not sustainable demand

### Demand Driver Analysis

**Purpose:** Identify what is driving the demand signal and assess whether that driver will persist.

| Driver Type | Sustainability | Examples |
|---|---|---|
| Functional need | High | Products solving real daily problems (organization, ergonomics, efficiency) |
| Lifestyle/aesthetic trend | Medium-High | Products aligned with broader cultural movements (minimalism, cottagecore, home gym) |
| Seasonal alignment | Medium | Products boosted by upcoming seasonal demand (pool accessories in spring, cozy blankets in fall) |
| Platform algorithm boost | Low-Medium | Products amplified by TikTok or Instagram algorithm trends that may shift |
| Single influencer endorsement | Low | One celebrity or major creator featuring the product |
| News event or media coverage | Low | Product featured in a news story or TV show segment |

**How to apply:** Identify the primary driver behind the demand signal. If the driver is a functional need or lifestyle trend, sustainability is more likely. If the driver is a single event or influencer, the signal requires stronger evidence from other tests to pass.

### Comparable Trend Analysis

**Purpose:** Find past products or categories that followed a similar emergence pattern and use their lifecycle as a reference.

**Steps:**
1. Identify 2-3 products from the past 12-24 months that had a similar signal profile (same source channels, similar growth rate, comparable product category).
2. Research their lifecycle: How long did the growth phase last? What was the peak? How quickly did demand decline? Did a sustained baseline establish?
3. Use these comparables to set expectations for the current signal's likely trajectory.

**Example:** If you are evaluating a trending kitchen gadget and find that three similar kitchen gadgets from the past year each sustained elevated demand for 4-6 months before settling to a lower but stable baseline, this provides evidence that the current signal could follow a similar pattern.

**Outcome of Gate 2:** Signal classified as SUSTAINABLE (proceed to Gate 3), LIKELY TRANSIENT (proceed with caution and reduced order sizes only), or EPHEMERAL (do not proceed).

---

## Gate 3: Is the Signal Actionable?

A real and sustainable signal may still not be actionable if the competitive landscape, supply chain constraints, or margin structure prevent profitable execution.

### Timing Feasibility Test

**Question:** Can you get product to market while demand is still in a commercially viable phase?

**How to apply:**
1. Estimate the remaining duration of the growth or peak phase based on your sustainability analysis and comparable trend data.
2. Calculate your minimum time to market: fastest production time + fastest shipping method + customs and receiving.
3. Compare the two. If your minimum time to market exceeds the estimated remaining viable demand window, the signal is not actionable through traditional sourcing. Consider alternatives (domestic sourcing, existing inventory pivot, dropship test).

| Timing Scenario | Assessment |
|---|---|
| Arrival during growth phase with 4+ weeks of margin | Actionable -- standard sourcing |
| Arrival near peak with 2-3 weeks of margin | Actionable -- air freight and reduced initial order |
| Arrival during projected decline | Not actionable through traditional sourcing |

### Margin Viability Test

**Question:** Can you sell this product at a price consumers will pay while covering all costs and generating acceptable margin?

**How to apply:**
1. Determine the consumer price ceiling by analyzing current marketplace pricing and consumer price sensitivity signals.
2. Estimate full landed cost: product cost + shipping + duties + marketplace fees + advertising.
3. Calculate gross margin. Apply your minimum acceptable margin threshold (typically 25-40% depending on category and risk level).

| Margin Result | Assessment |
|---|---|
| Gross margin above 40% | Strong -- proceed with confidence |
| Gross margin 25-40% | Acceptable -- proceed with tight cost controls |
| Gross margin below 25% | Not viable -- margin too thin for risk |

### Competitive Entry Feasibility Test

**Question:** Can a new entrant realistically capture meaningful market share?

**Factors to evaluate:**
- **Listing density:** Fewer than 20 existing listings is an open field; 20-50 is competitive but enterable; 50+ requires significant differentiation or cost advantage.
- **Review moat:** If top sellers have 1,000+ reviews, a new listing with zero reviews faces a steep disadvantage. Consider whether you can overcome this through advertising, product differentiation, or a launch strategy.
- **Brand dominance:** If a recognized brand controls more than 40% of category sales, entry is significantly harder.
- **Differentiation potential:** Can you offer a meaningfully different product (better materials, additional features, superior design, bundle) or is this a commodity race to the lowest price?

| Competitive Scenario | Assessment |
|---|---|
| Open field, no dominant brand, differentiation possible | Actionable |
| Moderate competition, entry possible with advertising investment | Actionable with higher capital requirement |
| Entrenched competition, strong brand moats, commodity product | Not actionable without significant advantage |

**Outcome of Gate 3:** Signal classified as ACTIONABLE (proceed to full analysis and action plan), CONDITIONALLY ACTIONABLE (proceed with specific mitigations noted), or NOT ACTIONABLE (document reasoning and archive).

---

## Validation Summary Scorecard

After completing all three gates, summarize your findings in this scorecard format.

| Gate | Test | Result | Confidence | Notes |
|---|---|---|---|---|
| 1: Real | Multi-source confirmation | [Pass/Fail] | [H/M/L] | [Key evidence] |
| 1: Real | Organic authenticity | [Pass/Fail] | [H/M/L] | [Key evidence] |
| 1: Real | Data quality | [Pass/Fail] | [H/M/L] | [Key evidence] |
| 2: Sustainable | Duration and trajectory | [Pass/Fail] | [H/M/L] | [Key evidence] |
| 2: Sustainable | Demand driver analysis | [Pass/Fail] | [H/M/L] | [Key evidence] |
| 2: Sustainable | Comparable trend analysis | [Pass/Fail] | [H/M/L] | [Key evidence] |
| 3: Actionable | Timing feasibility | [Pass/Fail] | [H/M/L] | [Key evidence] |
| 3: Actionable | Margin viability | [Pass/Fail] | [H/M/L] | [Key evidence] |
| 3: Actionable | Competitive entry feasibility | [Pass/Fail] | [H/M/L] | [Key evidence] |

**Overall validation result:** [VALIDATED / CONDITIONALLY VALIDATED / NOT VALIDATED]

**Recommended next step:** [Proceed to demand sizing / Monitor for X more days / Archive with reason]

---

## When to Re-Validate

Validation is not a one-time event. Re-run this framework when:

- **7 days have passed** since initial validation and you have not yet placed an order. Market conditions change quickly.
- **New contradicting data appears** from any source. A single strong contradicting signal can invalidate an otherwise positive assessment.
- **Your production timeline has shifted.** If your expected arrival date moves by more than 2 weeks, the timing feasibility test must be re-run.
- **A major competitor enters.** The competitive entry feasibility assessment changes when a well-resourced seller lists a competing product.
- **The trend trajectory changes shape.** If a previously accelerating trend begins decelerating, re-evaluate sustainability.
