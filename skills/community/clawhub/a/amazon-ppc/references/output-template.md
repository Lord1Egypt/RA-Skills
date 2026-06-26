# Amazon PPC Campaign Plan — Output Template

Use this template structure to deliver every Amazon PPC campaign plan. All sections are required unless marked optional.

---

## Campaign Plan: [Product Name] — [ASIN]

**Prepared for:** [Seller Name / Account]
**Product:** [Product Name]
**ASIN:** [ASIN]
**Marketplace:** [Amazon.com / Amazon.co.uk / etc.]
**Date:** [Date]
**Goal:** [Launch / Scale / Profit]

---

## 1. Unit Economics Summary

| Metric | Value |
|---|---|
| Average Selling Price | $ |
| Gross Margin % | % |
| Gross Margin $ per unit | $ |
| Target ACoS | % |
| Maximum ACoS (ceiling) | % |
| Estimated Conversion Rate | % |
| Maximum CPC | $ |
| Break-even CPC | $ |

**Calculation notes:**
- Max CPC = ASP × Target ACoS × Estimated CVR
- Break-even ACoS = Gross Margin %

---

## 2. Campaign Architecture Map

| Campaign Name | Ad Type | Match Type | Tier | Daily Budget | Starting Bid | Purpose |
|---|---|---|---|---|---|---|
| [Name] | SP/SB/SD | Auto/Broad/Phrase/Exact | 1-4 | $ | $ | [Purpose] |

**Naming convention used:** [SP/SB/SD]\_[Tier]\_[MatchType]\_[KeywordTheme]

---

## 3. Keyword and Match Type Matrix

| Seed Keyword | Auto | Broad | Phrase | Exact | Starting Bid | Priority |
|---|---|---|---|---|---|---|
| [keyword] | Include | Include | Include | Include | $ | High/Med/Low |

**Bid rationale:** [1-2 sentences explaining bid derivation for this product]

---

## 4. Negative Keyword Plan

### Day-1 Negatives (pre-load before launch)

| Keyword | Match Type | Reason |
|---|---|---|
| [term] | Exact/Phrase | Irrelevant / Competitor / Informational |

### Ongoing Graduation Rules

| Trigger | Action |
|---|---|
| 30+ clicks, 0 conversions | Add as exact negative in all campaigns |
| ACoS > 2× target with conversions | Investigate; consider bid reduction or negative |
| 5+ conversions at target ACoS | Create dedicated exact match campaign |
| Converts but ACoS 1.5-2× target | Reduce bid 15-20%, monitor for 14 days |

---

## 5. Placement Multiplier Strategy

| Placement | Recommended Premium | Rationale |
|---|---|---|
| Top of Search | +[X]% | [Reason] |
| Product Pages | +[X]% or neutral | [Reason] |
| Rest of Search | No adjustment | Default |

**Review trigger:** Adjust when placement-level ACoS data accumulates after 500+ impressions per placement.

---

## 6. Budget Allocation Table

| Campaign Tier | Daily Budget | % of Total | 30-Day Spend Estimate |
|---|---|---|---|
| Tier 1 — Research | $ | % | $ |
| Tier 2 — Performance | $ | % | $ |
| Tier 3 — Brand Defense | $ | % | $ |
| Tier 4 — Competitor (optional) | $ | % | $ |
| **Total** | **$** | **100%** | **$** |

**Rebalancing trigger:** When Tier 2 campaigns achieve target ACoS with 20+ daily clicks, shift 10% from Tier 1 to Tier 2.

---

## 7. 30-Day Optimization Calendar

| Day | Action | Trigger / Threshold |
|---|---|---|
| Day 1 | Launch all campaigns, set baseline | — |
| Day 7 | Pull search term report, harvest converting terms | First data review |
| Day 7 | Add 30-click / 0-conversion terms as negatives | Negative keyword build |
| Day 14 | Bid adjustment review (all campaigns) | 100+ clicks per campaign |
| Day 14 | Graduate confirmed converters to exact match | 5+ orders at target ACoS |
| Day 21 | Budget rebalancing | Shift from underperforming research → performance |
| Day 21 | Placement multiplier review | 500+ impressions per placement |
| Day 30 | Full structure review and 60-day plan | Monthly optimization cycle |

---

## 8. Risk Flags (Optional)

List any conditions that could affect performance:

- [ ] High competitor density may require elevated launch bids
- [ ] Product seasonality may skew early CVR data
- [ ] Limited keyword pool may exhaust discovery volume quickly
- [ ] New ASIN with no reviews may depress CVR below assumptions

---

## 9. Scope and Limitations

- This plan does not connect to Amazon Advertising API — apply recommendations to your account manually
- Bid estimates are based on provided inputs; validate against actual CTR and CVR within 14 days
- DSP (demand-side platform) campaigns are outside scope
- Keyword volume estimates are directional; verify with Amazon's keyword research tools
