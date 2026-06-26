# Bidding Optimization Guide

## How ASA Bidding Works

Apple Search Ads uses a **second-price auction** — you pay slightly above the second-highest bid, not your max bid. This means:
- Setting bids higher than needed doesn't automatically increase CPA proportionally
- The "right" bid is the one that wins competitive positions without overpaying
- Bid changes affect impression volume, position, and CPA simultaneously

Two bidding modes:
1. **CPT (Cost Per Tap) bids**: You set max cost-per-tap. Full control, requires active management.
2. **CPA Goal**: You tell Apple your target cost-per-install, Apple automates bids. Easier but less transparent.

**Recommendation**: Start with CPT bids for the first 30 days to understand your baseline. Consider CPA Goal only after you have 50+ installs per ad group to give Apple's algorithm enough data.

---

## Starting Bid Strategy

### Launch Phase (Week 1-2)

Start **10-15% below Apple's suggested bid range** for each keyword.

Why lower: Apple's suggestions are averages across all advertisers in that category. Your app's conversion rate may be above or below average — you need to calibrate against your actual data, not the market average.

Exception: Brand campaign. Bid at or above Apple's suggestion for your own brand terms. You must own this traffic.

### Data Collection Requirements

Don't optimize bids until you have:
- ≥ 50 taps per keyword (for statistical significance)
- ≥ 10 installs per keyword (to assess quality)
- ≥ 7 days of running (to smooth out daily variance)

Optimizing earlier = optimizing noise.

---

## Bid Adjustment Rules

### Increase Bid When:
- CR > 40% AND CPA < target → bid up 10-20%, capture more volume
- Impression share < 30% on a top-performing keyword → bid up to win more auctions
- Keyword is in position 2-3 consistently → test bidding up to position 1

### Decrease Bid When:
- CPA > 150% of target for ≥ 2 weeks → bid down 15-25%
- TTR < 3% with ≥ 500 impressions → ad creative issue, but also reduce bid while fixing
- CR < 20% for ≥ 50 taps → keyword-to-product mismatch, reduce or pause

### Pause Keyword When:
- 0 installs after 30 taps → no conversion signal, reallocate budget
- CPA > 300% of target → no recovery path at any bid level
- Search term is irrelevant (found via search terms report)

---

## Bid Adjustment Frequency

| Phase | Frequency | Action |
|-------|----------|--------|
| Launch (Week 1-2) | No changes | Collect data only |
| Early optimization (Week 3-4) | Weekly | Pause non-performers, minor adjustments |
| Active management (Month 2+) | Bi-weekly | Full bid optimization cycle |
| Scaled campaigns | Weekly | Monitor for CPA drift |

**Don't touch bids daily.** The Apple algorithm needs time to adjust after bid changes — daily changes create noise and prevent you from reading true performance.

---

## Bidding by Campaign Type

### Brand Campaign
- Priority: Maintain top position
- Bid level: High (at or above suggested range)
- Tolerance: Accept higher CPT — conversion rate compensates
- Check: If losing impression share on your own brand, bid up immediately

### Generic Campaign
- Priority: Efficient CPA at scale
- Bid level: Start below suggested, optimize toward CPA target
- Tolerance: Accept some CPA variance while building keyword data
- Check: Weekly CPA vs target comparison

### Competitor Campaign
- Priority: Profitable installs only — no ego bidding
- Bid level: 20-30% below generic campaign bids initially
- Tolerance: CR will be lower (users searching for a competitor), accept higher CPA threshold (1.5× generic target)
- Check: Pause keywords where CR < 20% after 50 taps — competitor loyalty is too strong

### Discovery Campaign
- Priority: Data collection, not efficiency
- Bid level: 50-70% of generic campaign bids
- Tolerance: Higher CPA acceptable — you're paying for insight
- Check: Weekly export of search terms, move winners to exact match

---

## CPA Target Setting

Your CPA target should be derived from unit economics, not gut feel:

```
Max CPA = (Average Revenue Per User × Target Payback Period)

Example:
- ARPU (30-day): $8
- Target payback: 3 months
- Max CPA = $8 × 3 = $24
```

If you don't have ARPU data yet, use industry benchmarks:
- Games: $1.50–$4.00 CPA (high volume, low ARPU)
- Productivity/Utility: $3–$8 CPA
- Finance/Health: $8–$25 CPA (high ARPU, high LTV)
- Subscription apps: CPA should be < 1-month subscription revenue

---

## Scaling Strategy

### When to Scale

Scale a campaign when **both** conditions are met:
1. CPA is at or below target for 14+ consecutive days
2. You're NOT spending your full daily budget (room to absorb more impressions)

### How to Scale

**Preferred method: Budget increase**
- Increase daily budget by 20-30% per week
- Monitor CPA for 5-7 days after each increase
- If CPA rises > 20% above target, hold budget and investigate

**Secondary method: Bid increase on top performers**
- Identify keywords in positions 2-4 with CPA at target
- Increase bid 10-15% to compete for position 1
- Expect 20-40% more impressions from position improvement

**Avoid**: Doubling budgets in one step. Rapid budget increases trigger Apple's learning period and can temporarily destabilize CPA.

### Scaling Cap

Even profitable campaigns have a ceiling. Signs you're near the keyword's ceiling:
- Impression share > 70% (you're winning most auctions already)
- CPA rises despite stable bids (demand at this price is exhausted)
- Adding budget no longer increases install volume proportionally

At this point: find new keywords, not more budget for existing ones.
