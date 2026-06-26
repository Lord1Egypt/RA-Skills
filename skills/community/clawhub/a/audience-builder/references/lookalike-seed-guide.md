# Lookalike Seed Quality Guide

## Seed Segmentation Framework

The quality of your lookalike audience is determined entirely by the quality of your seed. A 1% lookalike from a contaminated seed will underperform a 3% lookalike from a clean, high-LTV seed.

## Tier Definitions

### Tier 1 — Premium Seed (High-LTV Repeaters)

**Criteria (must meet at least one, plus the quality filter):**
- 3+ orders lifetime
- Top 20% by lifetime revenue
- Quality filter: return rate <20%

**Why this works:** Platforms optimize for behavioral patterns. Tier 1 customers exhibit consistent purchase behavior, brand affinity, and product preference signals that the algorithm can pattern-match against the broader population.

**Optimal seed size:** 1,000–5,000 customers
- Below 1,000: insufficient signal for the algorithm; high variance in LAL quality
- Above 5,000: signal starts to dilute as you include borderline customers
- Sweet spot for most DTC brands: 2,000–3,500

**Data fields to include per customer:**
- Email (primary match identifier)
- Phone (increases match rate 15–30%)
- First name + Last name (improves match confidence)
- City + State + ZIP (further improves match)
- Lifetime value (Meta can weight by value if using Value-Based LAL)

### Tier 2 — Secondary Seed (Recent Single Purchasers)

**Criteria:**
- 1 order within last 90 days
- AOV at or above median
- Not in Tier 4 (no discount-only)

**Use cases:**
- Broader LAL for expansion when Tier 1 is exhausted
- A/B test against Tier 1 LAL to validate seed quality matters
- Useful when Tier 1 count is below 1,000

**Expected performance vs. Tier 1 LAL:**
- Typically 15–30% lower ROAS
- 10–20% higher CPA
- 20–40% larger reach (more prospects found)

### Tier 3 — Retargeting Only (Lapsed Customers)

**Criteria:**
- Last order 180+ days ago
- Any historical purchase

**Do NOT use as LAL seed.** Lapsed customers' purchase behavior is outdated. The algorithm will find people who look like people who used to buy — not people who are likely to buy now.

**Correct use:** Email reactivation campaigns, Meta/Google retargeting with win-back offer, lookalike exclusion to prevent targeting churned profiles.

### Tier 4 — Exclude Entirely (Discount-Only Buyers)

**Criteria:**
- All purchases made during sale/promotion events
- AOV below median (adjusts for brands where sales are frequent)
- No full-price purchase in history

**Why exclude:** Including discount buyers in LAL seeds trains the algorithm to find more deal-seekers. Your prospecting audience will have high conversion rates on promotions but near-zero full-price purchase behavior, destroying margin.

## Value-Based Lookalikes (Meta)

Meta allows uploading LTV as a value column. The algorithm then weights seed members by their value — a customer worth $2,000 influences the LAL more than one worth $45.

**When to use value-based LAL:**
- Tier 1 seed size >2,000 (sufficient data for value weighting to help)
- Wide LTV distribution (10x+ difference between lowest and highest in seed)
- Goal is maximizing revenue, not just conversion count

**When to skip value-based:**
- Seed size <1,000 (insufficient signal)
- Relatively flat LTV distribution (most customers similar value)
- Goal is maximizing customer count for brand awareness

**Setup:** Upload CSV with columns: email, phone, fn, ln, value. Value = lifetime revenue. Meta will auto-normalize.

## Seed Maintenance Schedule

| Action | Frequency | Why |
|--------|-----------|-----|
| Re-export customer file | Monthly | New customers enter Tier 1/2; others lapse to Tier 3 |
| Rebuild tier segments | Monthly | Tier boundaries shift with new data |
| Re-upload seeds to platforms | Monthly | Platforms re-match and re-calculate LALs |
| Full LAL rebuild | Quarterly | Refreshes the algorithm's pattern model beyond incremental updates |
| Audit seed vs. LAL performance | Monthly | Catch seed quality degradation early |
| Remove returned/refunded | Weekly in export | Prevent training on non-genuine purchases |

## Seed Quality Diagnostic

If your LAL is underperforming, run this diagnostic:

**1. Seed contamination check:**
- What % of seed are Tier 4 (discount-only)? Should be 0%.
- What % of seed have return rates >50%? Remove them.
- Are gift purchases included? Consider excluding (buyer intent ≠ recipient profile).

**2. Seed freshness check:**
- When was the seed last updated? If >60 days, refresh immediately.
- What % of seed customers made their last purchase >180 days ago? If >30%, your Tier 1 definition needs tightening.

**3. Seed size check:**
- Is seed <500? Consider expanding Tier 1 criteria slightly (e.g., 2+ orders instead of 3+) or merging Tier 1 + Tier 2.
- Is seed >10,000? Tighten criteria — you're likely including low-quality customers.

**4. Match rate check:**
- Meta match rate <40%? Add phone numbers and full addresses to upload.
- TikTok match rate <20%? Platform may not have sufficient overlap with your customer base — test a different seed or broader Tier 1+2 combined.
- Google match rate <30%? Ensure data is properly formatted and includes multiple identifiers.

**5. LAL percentage check:**
- Running >5% LAL? Test reducing to 1–3% and compare ROAS.
- Running 1% with very small reach (<500K)? Your seed may be too niche — test 2–3%.

## Platform-Specific Seed Notes

### Meta
- Minimum: 100 for LAL creation, 1,000+ for quality
- Value-based LAL available (upload LTV column)
- Event-based seeds (Purchase pixel event) can be used but customer list gives more control
- LAL auto-refreshes every 3–7 days when source updates
- Multi-country LAL: specify countries or let Meta choose

### TikTok
- Minimum: 1,000 for LAL creation
- No value-based weighting
- Lower match rates than Meta (30–50% vs. 50–70%)
- LAL does NOT auto-refresh — must manually recreate
- Three expansion levels: Narrow (≈1%), Balanced (≈3–5%), Broad (≈10%+)

### Google
- Customer Match requires 1,000+ matches
- Similar Segments largely deprecated; use audience signals instead
- PMax audience signals: upload Customer Match as signal, not restriction
- No explicit LAL creation — Google finds similar users automatically within campaigns
- Pair Customer Match with in-market segments for stronger signal
