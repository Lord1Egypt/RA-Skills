---
name: aes-conversion-rate-doctor
description: Diagnose conversion bottlenecks in product pages and checkout flows, then prescribe specific, data-driven fixes prioritized by expected revenue impact. Use when add-to-cart rates lag benchmarks, checkout completion drops, or you need a structured pre-launch or post-launch conversion audit.
---

# Conversion Rate Doctor

Diagnose conversion bottlenecks across ecommerce funnels and prescribe prioritized, evidence-based fixes mapped to conversion psychology principles.

## Quick Reference

| Decision | Guidance |
|---|---|
| **Data input quality** | Require at least 30 days of traffic data with >1,000 sessions per funnel stage. Flag statistical significance concerns when sample sizes fall below threshold. |
| **Funnel stage coverage** | Always map the complete path: Landing > Product Page > Add-to-Cart > Cart > Checkout Initiation > Payment > Order Confirmation. Never skip intermediate stages. |
| **Benchmark comparison** | Compare against category-specific benchmarks (see `references/conversion-benchmarks.md`). Use vertical median as the baseline; flag metrics deviating >1 standard deviation. |
| **Fix prioritization** | Rank fixes by estimated revenue impact = (traffic volume x expected lift x average order value). Secondary sort by implementation effort (low/medium/high). |
| **Psychology mapping** | Map every finding to at least one conversion psychology principle (see `references/psychology-principles.md`). Cite the principle by name and explain the mechanism. |
| **Evidence strength** | Label each finding with evidence tier: Tier 1 = A/B test data, Tier 2 = analytics correlation, Tier 3 = heuristic evaluation. Never present Tier 3 findings as certain. |
| **Output structure** | Follow the structured output template (see `references/output-template.md`). Include executive summary, metrics snapshot, stage-by-stage analysis, and implementation roadmap. |
| **Implementation guidance** | Every fix must include: what to change, why it works (psychology principle), expected impact range, implementation complexity, and a measurement plan. |

## Solves

1. **Add-to-cart rate below benchmark** — Product page views are healthy but visitors are not adding items to cart, indicating friction or messaging failures on the product page itself.
2. **Checkout abandonment spike** — Cart-to-order completion has dropped over a 30-60 day window, suggesting new friction in the checkout flow, payment options, or shipping cost presentation.
3. **Post-redesign conversion regression** — A recent page redesign caused conversion metrics to decline, and the team needs to identify which specific changes are responsible.
4. **Pre-launch conversion readiness** — A new product page, checkout flow, or sales event landing page needs a structured audit before going live to catch bottlenecks proactively.
5. **Mobile conversion gap** — Desktop conversion rates are acceptable but mobile rates significantly underperform, pointing to responsive design or mobile UX issues.
6. **High bounce rate on product pages** — Visitors land on product pages but leave without scrolling or interacting, suggesting above-the-fold content failures.
7. **Payment step drop-off** — Customers reach the payment step but abandon at unusually high rates, indicating trust signal gaps, payment option limitations, or unexpected cost reveals.

## Modes

### Mode A — Full Funnel Audit

A comprehensive end-to-end audit covering every stage from product page landing through order confirmation. Use this mode when you have access to full funnel analytics and want a complete diagnosis.

**When to use:** Quarterly conversion reviews, post-redesign audits, pre-sales-event preparation, or when multiple funnel stages show simultaneous decline.

### Mode B — Targeted Page Diagnosis

A focused diagnosis of a single page or funnel stage element. Use this mode when analytics clearly isolate the problem to one stage and you want deep analysis of that specific area.

**When to use:** Isolated add-to-cart rate drops, specific checkout step abandonment, single page bounce rate issues, or A/B test result interpretation for one element.

## Core Job

The Conversion Rate Doctor performs a structured diagnostic process:

1. **Ingest metrics and context** — Collect current conversion data, traffic volumes, device splits, and recent changes. Establish the baseline.
2. **Map the funnel** — Identify every stage and the transition rates between them. Calculate where the largest absolute drop-offs occur.
3. **Benchmark against industry data** — Compare each stage metric against category-specific benchmarks to identify underperforming stages.
4. **Diagnose root causes** — For each underperforming stage, examine page elements, UX patterns, copy, trust signals, and technical factors. Map findings to psychology principles.
5. **Prioritize fixes** — Rank all findings by expected revenue impact, factoring in traffic volume, estimated conversion lift, and implementation effort.
6. **Prescribe implementation plan** — Deliver a sequenced roadmap with specific changes, expected outcomes, and measurement criteria.

## Inputs

Provide as much of the following as available. The more complete the data, the more precise the diagnosis.

**Required:**
- Product page URL(s) or detailed screenshots
- Current conversion rate (overall or by funnel stage)
- Traffic volume (sessions per month or per day)
- Device split (% mobile vs. desktop)

**Strongly recommended:**
- Funnel stage breakdown (landing > PDP > ATC > cart > checkout > payment > confirmation)
- Time period for the data (and any comparison period)
- Product category or vertical
- Average order value
- Recent changes to pages or flow (redesigns, new features, pricing changes)

**Optional but valuable:**
- Heatmap or session recording summaries
- A/B test history and results
- Site speed metrics (page load time, LCP, CLS)
- Customer feedback or survey data
- Competitor URLs for comparison

## Workflow — Mode A: Full Funnel Audit

### Step 1: Data Collection and Validation

Gather all available metrics. Validate data quality:
- Confirm session counts exceed 1,000 per stage for statistical relevance
- Check for tracking anomalies (sudden drops that suggest broken analytics, not real behavior)
- Identify the time window and note any external factors (seasonality, promotions, market events)
- Flag any missing funnel stages — if data gaps exist, note them and proceed with what is available

### Step 2: Funnel Mapping and Drop-off Identification

Build the complete funnel with transition rates:

```
Landing Page (100%) > Product Page View (X%) > Add to Cart (X%) > Cart View (X%) > Checkout Start (X%) > Payment Entry (X%) > Order Confirmation (X%)
```

Calculate absolute drop-off at each stage. Identify the stages with the largest absolute visitor loss, not just the lowest percentage — a 5% drop-off at a high-traffic stage matters more than a 20% drop-off at a low-traffic stage.

### Step 3: Benchmark Comparison

Compare each stage metric against category benchmarks from `references/conversion-benchmarks.md`:
- Flag stages performing >1 standard deviation below median as **critical**
- Flag stages performing 0.5-1 standard deviation below as **warning**
- Note stages performing above benchmark as **healthy** (but still review for regression risk)

### Step 4: Stage-by-Stage Diagnosis

For each underperforming stage, examine:

**Product Page Elements:**
- Hero image quality, size, and zoom capability
- Title clarity and keyword alignment
- Price presentation (anchoring, strikethrough, unit pricing)
- Trust signals (reviews, ratings, badges, guarantees)
- CTA button (color contrast, copy, placement, size per Fitts's Law)
- Product description (scannable format, benefit-focused, objection handling)
- Social proof placement and recency
- Mobile layout and tap target sizing

**Cart and Checkout Elements:**
- Cart summary clarity and edit capability
- Progress indicator presence and accuracy
- Form field count and necessity
- Guest checkout availability
- Payment option breadth
- Shipping cost transparency and timing of reveal
- Error message clarity and inline validation
- Trust signals at payment step
- Order summary visibility during checkout

### Step 5: Finding Documentation

For each finding, document:
1. **What** — The specific issue observed
2. **Where** — The exact funnel stage and page element
3. **Evidence** — The data supporting the diagnosis (with evidence tier label)
4. **Why it matters** — The psychology principle explaining the impact (see `references/psychology-principles.md`)
5. **Estimated impact** — Revenue impact range based on traffic and benchmark delta

### Step 6: Fix Prioritization and Roadmap

Rank all fixes using the impact formula:

```
Priority Score = (Monthly Traffic at Stage) x (Expected Lift %) x (AOV) / (Implementation Effort Score)
```

Where Implementation Effort Score: Low = 1, Medium = 3, High = 9.

Group fixes into:
- **Quick wins** (high impact, low effort) — implement within 1-2 weeks
- **Strategic improvements** (high impact, high effort) — plan for 2-6 weeks
- **Incremental gains** (moderate impact, low effort) — batch into sprint cycles
- **Long-term investments** (moderate impact, high effort) — roadmap for next quarter

### Step 7: Output Assembly

Compile the full report following the output template in `references/output-template.md`. Include executive summary, all findings with evidence, and the prioritized roadmap.

## Workflow — Mode B: Targeted Page Diagnosis

### Step 1: Scope Definition

Identify the specific page or funnel stage to diagnose. Confirm:
- Which metric is underperforming (bounce rate, ATC rate, checkout step completion, etc.)
- The magnitude of underperformance vs. benchmark or historical baseline
- When the issue started (if a regression) or how long it has persisted
- Any recent changes to the page

### Step 2: Deep Element Analysis

Perform a thorough review of every element on the target page. For product pages, evaluate all of: hero image, title, pricing, description, reviews, trust badges, CTA, related products, mobile layout. For checkout steps, evaluate: form fields, progress indicator, trust signals, error handling, payment options, cost summary.

### Step 3: Psychology Principle Mapping

For each element issue found, identify which conversion psychology principle is violated (see `references/psychology-principles.md`). Explain the mechanism — how the violation creates friction or reduces motivation.

### Step 4: Competitive Comparison (if competitor URLs provided)

Compare the target page against competitor implementations. Note where competitors handle the same element more effectively and what pattern they use.

### Step 5: Fix Prescription

For each issue, prescribe a specific fix with:
- Exact change description
- Psychology principle supporting the change
- Expected impact (qualified by evidence tier)
- Implementation notes
- Suggested A/B test design to validate the fix

## Benchmark Interpretation Rules

When comparing metrics to benchmarks:

1. **Always use category-specific benchmarks.** A 3% add-to-cart rate is strong for electronics but weak for beauty products. Generic "ecommerce average" comparisons mislead.
2. **Account for device type.** Mobile benchmarks are typically 40-60% lower than desktop for checkout completion. Always compare mobile-to-mobile and desktop-to-desktop.
3. **Consider traffic quality.** Paid traffic from broad targeting converts differently than organic search traffic. Note traffic source mix when interpreting.
4. **Watch for seasonal effects.** Benchmark comparison during holiday periods should reference holiday benchmarks, not annual averages.
5. **Use ranges, not point estimates.** Present benchmarks as ranges (e.g., "category median: 3.5-5.2%") to avoid false precision.
6. **Distinguish correlation from causation.** A metric below benchmark does not automatically mean the page is broken — it could reflect pricing, product-market fit, or traffic quality issues outside UX control.

## Worked Example 1 — Full Funnel Audit (Electronics Category)

**Context:** An electronics retailer selling wireless headphones. Monthly traffic: 85,000 sessions. AOV: $89. Mobile: 62%. The team reports add-to-cart rates dropped from 8.2% to 5.1% over the past 45 days following a product page redesign.

**Funnel Data Provided:**

| Stage | Rate | Electronics Benchmark |
|---|---|---|
| Landing to PDP | 68% | 60-72% |
| PDP to Add-to-Cart | 5.1% | 7.0-9.5% |
| ATC to Cart View | 82% | 78-88% |
| Cart to Checkout Start | 51% | 48-58% |
| Checkout Start to Payment | 74% | 72-82% |
| Payment to Confirmation | 88% | 85-92% |
| **Overall** | **1.6%** | **2.2-3.1%** |

**Diagnosis Summary:**

The primary bottleneck is the PDP-to-ATC transition, which dropped 3.1 percentage points post-redesign and now sits below the category benchmark floor. Secondary concern at checkout start-to-payment, which is at the lower bound of benchmark.

**Key Findings:**

1. **Hero image reduced to single static view** (previously carousel with 5 angles + lifestyle shot). Evidence tier: T2 (correlation with redesign timing). Psychology: Loss of ability to mentally "try" the product violates the endowment effect — shoppers who can examine products from multiple angles develop stronger ownership feelings. Expected impact: Restoring carousel could recover 1.5-2.5% ATC rate. Effort: Low.

2. **Price displayed without anchor.** The redesign removed the MSRP strikethrough ($129 ~~$149~~). Evidence tier: T3 (heuristic). Psychology: Anchoring — without a reference price, $89 lacks context as a deal. Expected impact: 0.5-1.0% ATC lift. Effort: Low.

3. **Review summary moved below the fold on mobile.** The 4.6-star rating with 2,340 reviews was previously visible without scrolling. Evidence tier: T2 (mobile ATC drop was 40% steeper than desktop). Psychology: Social proof must be visible at the decision moment, not after scrolling. Expected impact: 0.8-1.5% mobile ATC lift. Effort: Low.

4. **Shipping cost revealed only at payment step.** $7.95 flat rate not shown until payment entry. Evidence tier: T2 (payment step shows slight underperformance). Psychology: Loss aversion — unexpected costs feel like losses and trigger abandonment. Expected impact: 1-3% checkout completion lift. Effort: Medium.

**Prioritized Fix List:**

| Rank | Fix | Expected Monthly Revenue Impact | Effort |
|---|---|---|---|
| 1 | Restore product image carousel | $2,700-$4,500 | Low |
| 2 | Add shipping cost to product page and cart | $1,800-$5,400 | Medium |
| 3 | Move review summary above fold on mobile | $1,400-$2,700 | Low |
| 4 | Restore price anchor (MSRP strikethrough) | $900-$1,800 | Low |

## Worked Example 2 — Targeted Diagnosis (Fashion Category, Checkout Step)

**Context:** A fashion retailer with strong product page performance (ATC rate: 11.2%, above the 8-11% category benchmark). However, checkout completion dropped from 62% to 44% over 30 days. Monthly checkout initiations: 14,200. AOV: $67. No recent checkout flow changes reported.

**Scope:** Checkout flow from cart to order confirmation.

**Findings:**

1. **New "create account" interstitial inserted before guest checkout option.** The team's marketing department added an account creation prompt that requires dismissing a modal before proceeding to guest checkout. Evidence tier: T1 (analytics show 31% of users who see the modal do not proceed). Psychology: Hick's Law — adding a decision step where none existed forces a choice that many resolve by leaving. Also violates cognitive load principles by interrupting the checkout mental model. Expected impact: Removing or restructuring the interstitial could recover 12-16% of lost completions. Effort: Low.

2. **Free shipping threshold message absent from checkout.** Cart subtotals averaging $67, and free shipping triggers at $75. No upsell prompt. Evidence tier: T3 (heuristic). Psychology: Loss aversion and anchoring — customers near the threshold respond to "You're $8 away from free shipping" because the perceived loss of paying for shipping outweighs the cost of adding another item. Expected impact: 3-5% AOV increase plus reduced shipping-cost abandonment. Effort: Low.

3. **Form validation errors clear all fields on mobile.** When a validation error triggers on the shipping address form, all fields reset on mobile browsers. Evidence tier: T2 (mobile checkout completion 22% lower than desktop, beyond typical device gap). Psychology: Cognitive load — forcing re-entry of correct information alongside correcting errors creates compounding frustration. Expected impact: Fixing field persistence could recover 5-8% of mobile checkout completions. Effort: Medium.

**Prioritized Fix List:**

| Rank | Fix | Expected Monthly Revenue Impact | Effort |
|---|---|---|---|
| 1 | Restructure account creation (make optional, post-purchase) | $51,000-$68,000 | Low |
| 2 | Fix mobile form validation field persistence | $14,000-$22,000 | Medium |
| 3 | Add free shipping threshold upsell prompt | $8,500-$14,200 (AOV uplift) | Low |

## Common Mistakes

1. **Using overall ecommerce benchmarks instead of category-specific ones.** Beauty and fashion ATC rates are structurally different from electronics. A 6% ATC rate is a problem for beauty but acceptable for consumer electronics. Always use the correct vertical.

2. **Diagnosing based on percentages alone, ignoring absolute numbers.** A 20% drop-off at a stage with 500 visitors matters less than a 5% drop-off at a stage with 50,000 visitors. Always calculate absolute visitor loss to prioritize correctly.

3. **Prescribing fixes without specifying how to measure success.** Every fix needs a measurement plan: what metric to track, what lift is expected, how long to run the test, and what sample size is needed for statistical significance.

4. **Ignoring device-type splits.** Aggregate data masks mobile-specific problems. A healthy overall ATC rate can hide a severely broken mobile experience when desktop traffic is dominant. Always segment by device.

5. **Attributing all conversion issues to UX.** Some conversion problems stem from pricing, product-market fit, traffic quality, or competitive dynamics — not page design. Acknowledge when findings suggest causes outside UX scope.

6. **Recommending too many simultaneous changes.** Prescribing 15 changes at once makes it impossible to attribute improvement to any specific fix. Group changes into testable batches and sequence them.

7. **Presenting heuristic evaluations with the same confidence as data-backed findings.** Tier 3 evidence (heuristic review) should be clearly labeled as hypothesis, not diagnosis. Recommend validation through A/B testing.

8. **Overlooking page speed as a conversion factor.** Every 100ms of added load time costs roughly 1% in conversion. Always check and report page load metrics, especially on mobile networks.

9. **Focusing exclusively on the lowest-performing stage.** The stage with the worst benchmark comparison is not always the highest-impact fix opportunity. A moderately underperforming stage with 10x the traffic may offer more revenue recovery.

10. **Neglecting to account for traffic source mix.** Direct and branded search traffic converts at fundamentally different rates than paid social or display traffic. A shift in traffic mix can explain conversion changes without any page issues.

## Resources

| Resource | Path | Description |
|---|---|---|
| Output Template | `references/output-template.md` | Structured templates for Mode A and Mode B deliverables |
| Conversion Benchmarks | `references/conversion-benchmarks.md` | Industry benchmark data by product category and device type |
| Psychology Principles | `references/psychology-principles.md` | Conversion psychology principles with ecommerce applications |
| Quality Checklist | `assets/quality-checklist.md` | Pre-delivery quality checklist with 40+ validation items |
