---
name: Audience Builder
version: 1.1.0
description: Design targeted ad audiences for ecommerce campaigns across Meta, TikTok, and Google by combining purchase behavior, interest signals, lookalike modeling, and retargeting funnels into a unified audience architecture.
author: LeroyCreates
tags: [advertising, audiences, meta-ads, tiktok-ads, google-ads, ecommerce, retargeting, lookalike, media-planning]
---

# Audience Builder

Most ecommerce advertisers stack generic interest audiences on Meta, broad targeting on TikTok, and one branded search campaign on Google and call it a media plan. Audience Builder helps you design a layered audience architecture across all three platforms so your first-party purchase data, browsing behavior, and lookalike seeds are deployed where each platform actually rewards them.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|----------|--------|------------|------|
| Lookalike seed size | 1,000–5,000 high-LTV purchasers | 5,000–20,000 all purchasers | <500 or 50,000+ undifferentiated |
| Lookalike expansion | 1–3% on Meta, Similar on Google | 4–6% on Meta | 10%+ "super broad" |
| Retargeting window | 7d ATC, 14d viewers, 30d engagers | 30d flat for all events | 180d everyone |
| Exclusion strategy | Purchasers excluded from prospecting; ATC excluded from TOF | Purchasers excluded only | No exclusions |
| Budget split cold/warm/hot | 60/25/15 for scaling brands | 50/30/20 for stable brands | 90/5/5 all prospecting |
| Platform priority for prospecting | Meta LAL + Google Performance Max | TikTok Smart+ broad | Single platform only |
| Creative-audience alignment | Dedicated creative per funnel stage | 2 variants rotated | Same ad everywhere |
| Frequency cap | 2–3/week prospecting, 5–7/week retargeting | Platform defaults | No caps, burn audiences |
| Audience refresh cadence | Weekly seed updates, monthly restructure | Monthly seed updates | Set and forget |
| Cross-platform overlap handling | Shared exclusion lists via CDPs | Manual CSV sync monthly | No deduplication |

## Solves

This skill addresses these specific problems:

1. **Interest stack decay** — Meta interest audiences that converted well 6 months ago now produce $0.50 CPMs but 0.3% conversion rates because the algorithm exhausted the responsive segment and is now showing ads to the unresponsive remainder.

2. **Lookalike seed contamination** — building lookalikes from "all purchasers" including one-time discount buyers, gift purchasers, and returns produces audiences that optimize for deal-seeking behavior rather than repeat purchase potential.

3. **Retargeting cannibalization** — running 180-day retargeting without exclusions means you're paying $15 CPMs to show ads to people who already bought, while genuinely warm prospects (viewed product 3 days ago) get drowned in the same pool.

4. **Platform audience collision** — the same customer sees your prospecting ad on Meta, your retargeting ad on Google Display, and your TikTok Spark ad in the same afternoon because there's no cross-platform frequency or exclusion logic.

5. **Funnel stage mismatch** — serving bottom-funnel "Buy Now 20% Off" creative to cold audiences who have never heard of your brand, while warm audiences who already know you get generic brand awareness content.

6. **Budget misallocation by temperature** — spending 90% on cold prospecting and 5% on retargeting when your retargeting ROAS is 8x and prospecting is 1.2x, leaving money on the table in the most efficient segment.

7. **Google audience underutilization** — using only branded search and Shopping campaigns while ignoring customer match lists, in-market segments, YouTube remarketing, and Performance Max audience signals.

## Workflow

### Step 1 — Audit Current Audience Architecture

Map every audience currently running across all platforms. For each audience, document: platform, campaign name, audience type (interest/LAL/retargeting/custom), size, spend last 30 days, ROAS, CPM, frequency, and date created.

Flag audiences where frequency exceeds 8/week, ROAS is below break-even, or the audience has been running unchanged for 90+ days. These are your decay candidates.

Export customer match lists currently uploaded to each platform and note when they were last refreshed.

**Output:** Current audience inventory spreadsheet with decay flags.

### Step 2 — Segment Customer File for Seed Quality

Pull your customer export and segment into tiers:

- **Tier 1 — High-LTV Repeaters:** 3+ orders OR top 20% by lifetime revenue, excluding returns >20%. This is your premium lookalike seed.
- **Tier 2 — Recent Single Purchasers:** 1 order in last 90 days, AOV above median. Good for broader lookalikes.
- **Tier 3 — Lapsed Customers:** Last order 180+ days ago. Retargeting reactivation audience, not a seed source.
- **Tier 4 — Discount-Only Buyers:** Only purchased during sales/promotions, sub-median AOV. Exclude from lookalike seeds entirely.

For each tier, note the count, average AOV, repeat rate, and top product categories. Tier 1 should be 1,000–5,000 customers for optimal lookalike performance on Meta.

**Output:** Customer tier segmentation with counts and quality metrics.

### Step 3 — Design Platform-Specific Prospecting Audiences

Build the prospecting layer for each platform:

**Meta:**
- Lookalike 1% from Tier 1 seed (primary prospecting)
- Lookalike 3% from Tier 1 seed (expansion prospecting)
- Lookalike 1% from Tier 2 seed (secondary test)
- Interest stack: 3–5 tightly related interests with AND logic, not OR
- Broad targeting ad set for Advantage+ comparison

**TikTok:**
- Custom audience lookalike from Tier 1 purchasers
- Interest-based targeting aligned with content verticals
- Smart+ automated targeting for comparison testing
- Video Shopping Ads audience vs. Product Shopping Ads audience (separate, do not overlap)

**Google:**
- Customer Match upload of Tier 1 + Tier 2 for audience signals
- In-market segments aligned with product categories
- Performance Max with audience signals (not restrictions)
- YouTube remarketing audiences from channel engagement
- Similar segments from customer match (where available)

For each audience, specify the campaign objective, daily budget, and expected CPM range.

**Output:** Platform prospecting audience map with budget allocations.

### Step 4 — Build Retargeting Funnel Architecture

Design retargeting audiences by recency and intent signal:

**Hot (0–7 days):**
- Added to cart but didn't purchase (all platforms)
- Initiated checkout but didn't complete (all platforms)
- Budget: highest CPM tolerance, lowest volume

**Warm (7–30 days):**
- Viewed product page 2+ times (Meta pixel, Google tag)
- Engaged with ad (liked, commented, shared, watched 75%+)
- Visited site 3+ times without purchase
- Budget: moderate CPM, moderate volume

**Cool (30–90 days):**
- Single site visit, no product page view
- Email subscriber, no purchase
- Social follower, no site visit
- Budget: lower CPM, broader reach

**Lapsed (90–180 days):**
- Previous purchasers not in Tier 1
- Cart abandoners who never returned
- Budget: minimal, test only

For each segment, specify the creative approach (product-specific dynamic vs. collection showcase vs. brand story) and the offer escalation (no offer → free shipping → percentage discount).

**Output:** Retargeting funnel map with creative and offer ladder.

### Step 5 — Configure Exclusion Logic

Exclusions prevent audience overlap and wasted spend:

- **Prospecting campaigns:** Exclude all purchasers (lifetime), all ATC (30 days), all retargeting audiences
- **Warm retargeting:** Exclude purchasers (30 days), exclude hot retargeting audiences
- **Hot retargeting:** Exclude purchasers (7 days)
- **Cross-platform:** Upload shared suppression lists to prevent the same user from being in Meta prospecting and Google retargeting simultaneously

Document the exclusion hierarchy as a matrix showing which audiences exclude which.

**Output:** Exclusion matrix with cross-platform suppression plan.

### Step 6 — Set Budget Allocation and Frequency Rules

Allocate budget across funnel stages:

**Scaling Phase (new brands, <$50K/mo spend):**
- Cold prospecting: 65%
- Warm retargeting: 20%
- Hot retargeting: 10%
- Reactivation: 5%

**Stable Phase (established brands, $50K–$200K/mo):**
- Cold prospecting: 55%
- Warm retargeting: 25%
- Hot retargeting: 15%
- Reactivation: 5%

**Efficiency Phase (mature brands, >$200K/mo):**
- Cold prospecting: 45%
- Warm retargeting: 30%
- Hot retargeting: 20%
- Reactivation: 5%

Set frequency caps:
- Prospecting: 2–3 impressions per user per week
- Warm retargeting: 4–5 impressions per user per week
- Hot retargeting: 6–7 impressions per user per week (urgency justified)

Define audience refresh schedule: weekly seed updates for retargeting, monthly for lookalike seeds, quarterly full architecture review.

**Output:** Budget allocation table and frequency rules by funnel stage.

### Step 7 — Build Measurement and Optimization Framework

Define how you'll evaluate audience performance:

- **Primary KPI per stage:** Prospecting = cost per new customer; Warm = ROAS; Hot = conversion rate; Reactivation = reactivation rate
- **Audience fatigue signals:** frequency >8/week AND CTR decline >30% from baseline AND CPM increase >25%
- **Refresh triggers:** any audience hitting 2 of 3 fatigue signals gets paused and rebuilt
- **Incrementality testing:** holdout 10% of retargeting budget to measure true lift vs. organic
- **Cross-platform attribution:** define the attribution window per platform (Meta 7d click/1d view, Google 30d click, TikTok 7d click/1d view) and document where double-counting occurs

Set up a weekly review dashboard tracking: spend, impressions, frequency, CPM, CPC, CTR, conversions, ROAS, and new vs. returning customer split — broken out by platform and funnel stage.

**Output:** Measurement framework with KPIs, fatigue signals, and dashboard spec.

## Worked Examples

### Example 1: DTC Skincare Brand — $30K/month Meta + Google

**Situation:** A DTC skincare brand spending $25K/month on Meta (interest audiences only) and $5K/month on Google (branded search). Meta ROAS dropped from 4.2x to 1.8x over 6 months. No retargeting campaigns. 12,000 total customers, average AOV $65.

**Audience architecture built:**

Customer segmentation: Tier 1 = 1,847 customers (3+ orders, top 20% revenue). Tier 2 = 3,291 single purchasers last 90 days. Tier 3 = 4,108 lapsed. Tier 4 = 2,754 discount-only.

Meta prospecting: LAL 1% from Tier 1 (2.1M reach) at $12K/month. LAL 3% from Tier 1 (5.8M reach) at $6K/month. Interest stack "clean beauty AND sensitive skin AND dermatologist" at $2K/month test.

Meta retargeting: Hot 0–7d ATC/checkout ($2K/month, dynamic product ads). Warm 7–30d product viewers ($1.5K/month, collection ads). Cool 30–60d site visitors ($1K/month, brand story video).

Google expansion: Customer Match uploaded (Tier 1+2). Performance Max with audience signals at $3K/month. In-market "skin care" + "beauty products" for Discovery at $1.5K/month. YouTube remarketing from brand channel at $1K/month.

Exclusions: All purchasers excluded from prospecting. ATC excluded from warm. Hot audiences excluded from cool.

**Result expectations:** ROAS recovery to 3.0x+ within 60 days from retargeting addition alone. Prospecting efficiency improvement from cleaner LAL seeds vs. generic interests.

### Example 2: Apparel Brand — $120K/month Meta + TikTok + Google

**Situation:** Fashion brand spending $60K Meta, $35K TikTok, $25K Google. Running interest targeting on Meta, broad on TikTok, Shopping-only on Google. Significant audience overlap — internal analysis shows 40% of retargeted users are seeing ads on all three platforms in the same week. 85,000 total customers.

**Audience architecture built:**

Customer segmentation: Tier 1 = 4,200 (repeat buyers, top quartile LTV). Tier 2 = 18,500 (recent single purchasers). Tier 3 = 38,000 (lapsed). Tier 4 = 24,300 (sale-only).

Cross-platform role assignment: Meta = primary prospecting engine (LAL strength). TikTok = content-driven discovery (Video Shopping Ads for new collections). Google = intent capture + retargeting (Search, Shopping, PMax, YouTube).

Overlap resolution: Shared suppression list via CDP covering all three platforms. Platform-specific retargeting roles — Meta handles social retargeting (engagement-based), Google handles site retargeting (pixel-based), TikTok handles video retargeting (view-based).

Budget reallocation: Meta prospecting $38K → $32K (reduced broad, increased LAL). Meta retargeting $0 → $10K (new). TikTok prospecting $35K → $28K (reduced broad, added Video Shopping). TikTok retargeting $0 → $7K (video viewers). Google Shopping $25K → $18K. Google PMax + YouTube retargeting $0 → $12K. Holdout budget for incrementality: $5K.

Frequency caps enforced cross-platform: max 6 impressions/week across all platforms for any single user in retargeting.

**Result expectations:** 15–25% reduction in blended CAC from eliminating cross-platform overlap. Retargeting ROAS of 5–8x on newly created retargeting campaigns. Incremental lift measurement within 90 days.

## Common Mistakes

1. **Building lookalikes from all purchasers** — Your all-purchaser list includes gift buyers, heavy returners, and one-time discount hunters. These dilute the signal. Always segment by LTV tier first.

2. **Using 10% lookalikes for "reach"** — A 10% lookalike on Meta is essentially broad targeting with extra steps. Stay at 1–3% for prospecting efficiency; use broad targeting if you want reach.

3. **Running retargeting without recency windows** — A 180-day retargeting pool treats someone who added to cart yesterday the same as someone who glanced at your homepage 5 months ago. Segment by recency and intent.

4. **No exclusions between funnel stages** — Without exclusions, your retargeting budget cannibalizes your prospecting budget because the algorithm serves the easiest conversion (someone who was going to buy anyway) rather than finding new customers.

5. **Copying Meta audience structure to TikTok** — TikTok's algorithm and auction work differently. Interest stacks that perform on Meta often fail on TikTok where content relevance matters more than targeting precision.

6. **Ignoring Google Display and YouTube** — Many brands treat Google as "just Search and Shopping." Customer Match lists, in-market segments, and YouTube remarketing audiences are underutilized high-performing channels.

7. **Never refreshing lookalike seeds** — Customer files change. Your Tier 1 segment from 6 months ago may not reflect current best customers. Update seeds monthly and rebuild lookalikes quarterly.

8. **Setting frequency caps too high or not at all** — Showing the same ad 15 times per week doesn't create urgency, it creates ad blindness. Cap prospecting at 2–3/week and retargeting at 5–7/week.

9. **Allocating 90%+ to cold prospecting** — If your retargeting ROAS is 5x and prospecting is 1.5x, you're leaving money on the table by underfunding retargeting. Balance budget by stage efficiency.

10. **No incrementality measurement** — Without holdout tests, you can't know whether retargeting ads actually drove conversions or just took credit for purchases that would have happened organically.

## Resources

- [Meta Ads Audience Best Practices](https://www.facebook.com/business/help/717368264947302) — Official lookalike and custom audience documentation
- [Google Ads Audience Targeting](https://support.google.com/google-ads/answer/2497941) — Customer Match, in-market, and similar audience guides
- [TikTok Ads Manager Audiences](https://ads.tiktok.com/help/article/audience-targeting) — Custom and lookalike audience setup
- [Foxwell Digital Audience Framework](https://www.foxwelldigital.com/) — Practitioner community for paid social audience strategy
