---
name: Amazon PPC
description: Build Amazon Sponsored Products and Sponsored Brands campaign structures, keyword match strategies, and bid logic for profitable paid visibility.
---

# Amazon PPC

Amazon advertising is a pay-to-play channel where campaign structure determines whether you scale profitably or bleed budget on irrelevant clicks. Amazon PPC helps you design Sponsored Products, Sponsored Brands, and Sponsored Display campaign architectures from scratch — or restructure messy existing accounts — with clear keyword match type strategies, bid logic, negative keyword funnels, and budget allocation rules tied to your actual margin and ACoS targets.

---

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Campaign goal for new product | Launch (maximize data) | Scale if similar product exists | Profit mode on day 1 |
| Starting ACoS target | Below gross margin by 5-10% | Equal to gross margin | Above gross margin |
| Match type for seed keywords | Exact + Phrase in separate campaigns | Broad with negatives | Auto only |
| Budget allocation (launch) | 60% research, 40% performance | 50/50 split | 100% exact match |
| Negative keyword timing | Add day 1 (obvious irrelevants) | Add after 7 days of data | Never (bleeding budget) |
| Bid adjustment for top-of-search | +20-50% if ACoS allows | +10-20% to test | No adjustment |
| Search term graduation trigger | 5+ orders at target ACoS | 3+ orders | Never harvest |

---

## Solves

This skill addresses these specific problems:

1. **Wasted launch budget** — New sellers run auto-only campaigns for weeks, spending on irrelevant queries with no structure to capture what's working.
2. **ACoS above margin** — Campaigns running without a profit ceiling, making every sale a net loss after advertising costs.
3. **Cannibalization between campaigns** — Multiple campaigns bidding on the same keyword, competing against each other and inflating effective CPC.
4. **No negative keyword system** — Search terms that never convert keep eating budget with no mechanism to stop them.
5. **Stalled scaling** — Performance plateaus because winning search terms never graduate from broad/auto discovery into exact match optimization.
6. **Blind bidding** — Bids set by guesswork rather than derived from margin math and conversion rate assumptions.
7. **Campaign structure debt** — Accounts that grew organically into dozens of disorganized campaigns with no tier logic, making optimization nearly impossible.

---

## Workflow

### Step 1 — Establish your profitability ceiling

Before building any campaign, calculate the maximum allowable ACoS:

```
Max ACoS = Gross Margin %
Target ACoS = Gross Margin % - 5 to 10%
Max CPC = (Average Selling Price × Target ACoS) × Estimated Conversion Rate
```

Example: $30 product, 40% margin, 10% CVR → Max CPC = $30 × 0.35 × 0.10 = $1.05

This number governs every bid decision. Never let campaigns run without a ceiling derived from real unit economics.

### Step 2 — Build the campaign tier structure

Create four campaign tiers with explicit purposes:

**Tier 1 — Research (Auto + Broad):** Discovers new search terms. High impression volume, lower bids. Daily review of search term reports to identify converting queries.

**Tier 2 — Performance (Phrase + Exact):** Captures confirmed winners from Tier 1. Higher bids justified by known conversion data. Tightly controlled with exact negatives.

**Tier 3 — Brand Defense:** Protects branded terms from competitor conquest. Exact match only. Usually small budget but non-negotiable for established products.

**Tier 4 — Competitor Targeting:** ASIN targeting and keyword conquest of competitor product pages. Experimental budget, tracked separately.

### Step 3 — Set match type distribution

For each seed keyword:
- Create one **Exact** match campaign in Tier 2 with your calculated max CPC as the starting bid
- Create one **Phrase** match campaign in Tier 2 with bid at 70-80% of exact bid
- Add the exact keyword as a negative in Tier 1 to prevent overlap

For auto campaigns: Set a low flat bid (30-50% of exact bid) and use category/product targeting for complementary ASIN discovery.

### Step 4 — Build the negative keyword waterfall

Day 1 negatives (add before launching):
- Competitor brand names (unless running conquest)
- Irrelevant category terms (e.g., for a kitchen spatula: "spatula fish", "medical spatula")
- Terms with zero commercial intent ("free", "how to", "DIY")

Ongoing waterfall rules:
- Any search term with 30+ clicks and 0 conversions → add as exact negative in all campaigns
- Any search term with ACoS > 2× target → add as negative, investigate if converting at high cost
- Any search term with 5+ conversions at target ACoS → graduate to dedicated exact match campaign

### Step 5 — Set budget allocation and pacing

During launch (first 30 days), weight budget toward research:
- Tier 1 (Research): 50-60% of daily budget
- Tier 2 (Performance): 30-40%
- Tier 3 (Brand Defense): 5-10%
- Tier 4 (Competitor): Optional, 10% max if budget allows

Increase Tier 2 weight as confirmed exact-match winners accumulate. By day 60, most budget should shift to performance campaigns.

### Step 6 — Configure placement multipliers

Platform placement data shows top-of-search typically converts 2-3× better than rest-of-search for most categories. Adjust accordingly:

- Top-of-search premium: Start at +20%, increase to +50% if ACoS remains below target
- Product pages: Neutral until ASIN targeting data accumulates
- Rest-of-search: No premium by default

### Step 7 — Build the 30-day optimization calendar

- **Day 7:** First search term harvest. Pull auto search term report, identify converting terms, move to phrase/exact campaigns. Add obvious negative keywords.
- **Day 14:** Bid adjustment review. Any exact campaign with 50+ clicks and ACoS < target → increase bid 10-15%. Any campaign with ACoS > 2× target → decrease bids 20%.
- **Day 21:** Budget rebalancing. Shift budget from underperforming auto campaigns to exact campaigns with proven conversions.
- **Day 30:** Full structure review. Build permanent exact-match campaigns for top 10 converting terms. Pause or restructure anything still unprofitable.

---

## Worked Examples

### Example 1 — New Private Label Product Launch

**Inputs:**
- Product: Silicone Kitchen Spatula Set, ASIN B09XYZ123
- ASP: $24.99
- Gross margin: 42%
- Target ACoS: 32%
- Seed keywords: "silicone spatula set", "kitchen spatula set", "cooking spatula", "heat resistant spatula", "non-stick spatula"
- Goal: Launch

**Campaign structure output:**

| Campaign Name | Type | Match | Daily Budget | Starting Bid |
|---|---|---|---|---|
| SP_Discovery_Auto_Spatula | Sponsored Products | Auto | $12 | $0.45 |
| SP_Research_Broad_Spatula | Sponsored Products | Broad | $8 | $0.55 |
| SP_Perf_Exact_SiliconeSpatulaSet | Sponsored Products | Exact | $6 | $0.80 |
| SP_Perf_Exact_KitchenSpatulaSet | Sponsored Products | Exact | $6 | $0.75 |
| SP_Perf_Phrase_SpatulaTerms | Sponsored Products | Phrase | $8 | $0.60 |

Max CPC calculation: $24.99 × 0.32 × 0.12 (estimated CVR) = **$0.96**

Day-1 negatives added: "silicone spatula craft", "spatula school", "free spatula"

**30-day outcome:** Auto campaign discovered "flexible spatula for eggs" and "BPA-free cooking spatula" as converting terms → both moved to dedicated exact match campaigns by Day 21.

---

### Example 2 — Restructuring a Messy Existing Account

**Inputs:**
- Product: Yoga Mat, ASP $38, Margin 38%, Current ACoS 61% (far above target)
- Existing structure: 1 auto campaign, 3 overlapping broad campaigns with no negatives
- Goal: Cut ACoS to 30% without killing sales volume

**Diagnosis:**
- Pull 90-day search term report → 847 unique search terms
- Filter: terms with > $1 spend and 0 conversions → **214 terms** to negative immediately
- Filter: terms with ACoS < 25% and 3+ conversions → **12 terms** to protect in dedicated exact campaigns

**Restructure plan:**
1. Pause all 3 existing broad campaigns
2. Create 1 new broad campaign with 214 negatives pre-loaded
3. Create 12 new exact match campaigns (one per proven term)
4. Set exact match bids at $0.90 (calculated from margin math)
5. Cap new broad campaign at $15/day, exact campaigns at $25/day total

**Expected result:** ACoS reduction from 61% to target range within 14-21 days as budget shifts to proven exact terms.

---

## Common Mistakes

1. **Launching with only auto campaigns** — Auto gives Amazon maximum control and often routes budget to irrelevant terms. Always pair with at least one manual exact campaign.

2. **Setting ACoS targets without checking margin** — A 30% ACoS target on a product with 25% margin is a guaranteed loss. Always derive target ACoS from unit economics first.

3. **Never adding negative keywords** — Even excellent products will have irrelevant search volume. Not adding negatives is an ongoing tax on every campaign dollar.

4. **Bidding the same amount in auto and exact campaigns** — Auto campaigns should bid lower because they're discovery vehicles. Matching bids means overpaying for unknown traffic.

5. **Graduating search terms too early** — Moving a term to exact match after 1-2 orders can mislead. Statistical confidence requires 5+ conversions before bid optimization is meaningful.

6. **Ignoring placement multipliers** — Top-of-search typically converts better, but the default setting applies no premium. Failing to test placement adjustments leaves performance on the table.

7. **Running all campaigns on the same daily budget** — Discovery campaigns need room to find new terms. Underfunding auto campaigns starves the system of new search term data.

8. **Never pausing underperformers** — Campaigns with 60+ days of data and no conversions at 3× target ACoS are not going to improve. Pause, investigate, restructure.

9. **Confusing branded and non-branded ACoS** — Branded terms convert higher and need lower bids. Mixing them into non-branded campaigns inflates overall ACoS and obscures true performance.

10. **No campaign naming convention** — Without consistent naming, you can't filter or sort campaigns at scale. Always include: campaign type, match type, keyword theme, and product identifier.

---

## Resources

- `references/output-template.md` — Structured campaign plan output format
- `references/keyword-match-type-guide.md` — When to use each match type with examples
- `references/bid-calculation-formulas.md` — Margin-based bid math reference
- `assets/ppc-quality-checklist.md` — Pre-launch and optimization quality checklist
