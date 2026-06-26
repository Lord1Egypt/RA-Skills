# Competitor Radar

Analyze competitor product listings, pricing strategies, and promotional tactics to identify gaps and opportunities — structured for ecommerce operators who need actionable intelligence, not just data.

---

## Quick Reference

| Decision | Guidance |
|---|---|
| Mode selection | **Mode A** (Single Competitor Deep-Dive) for detailed analysis of one rival. **Mode B** (Landscape Scan) for comparing 3-10 competitors side by side. |
| Platform focus | Amazon, Shopee, TikTok Shop, Lazada, Shopify, or platform-agnostic. Specify upfront — analysis categories shift per platform. |
| Analysis depth | **Quick scan** (~15 min): listing audit + pricing snapshot. **Full radar** (~45 min): all 6 analysis categories with strategic recommendations. |
| Data freshness | All analysis reflects the moment of observation. Flag any data older than 7 days. Never fabricate historical trends. |
| Output format | Use `references/output-template.md` for structure. Include the Competitive Positioning Map in every full radar. |

---

## Solves

This skill exists because ecommerce sellers need structured competitor intelligence but typically default to ad-hoc browsing. Without a framework, critical signals get missed — a competitor's coupon strategy, their review volume trajectory, or a gap in their keyword coverage that represents an opportunity. This skill turns scattered observations into a prioritized action plan.

---

## Modes

### Mode A — Single Competitor Deep-Dive

Analyze one competitor in depth across all 6 categories. Best when you have identified a specific rival threatening your position or a new entrant you need to assess quickly.

**When to use:**
- A new competitor has entered your category with aggressive pricing
- Your sales have declined and you suspect a specific rival is the cause
- You are preparing to launch a product that directly competes with an established listing
- You want to reverse-engineer a top performer's strategy

### Mode B — Landscape Scan

Compare 3-10 competitors across standardized dimensions. Best for quarterly reviews, market entry research, or identifying where you stand in the competitive field.

**When to use:**
- Quarterly competitive landscape review
- Entering a new product category and need to map the field
- Benchmarking your store against the top performers in your niche
- Identifying whitespace opportunities across multiple competitors

---

## Core Job

Transform raw competitor observations into a structured competitive intelligence report with a prioritized list of strategic recommendations ranked by impact and effort.

---

## Inputs

### Required

1. **Your product or store URL** — Link to your product listing or storefront so the skill can establish your current competitive baseline and market position.

2. **Competitor URLs or names** — Links to 3-10 competitor product listings or store names you want to analyze. The more competitors provided, the richer the landscape analysis. For Mode A, provide 1 competitor with deep detail.

3. **Product category** — The specific product category or niche you are competing in, e.g., "portable blenders" or "organic dog treats." This anchors the analysis and determines relevant benchmarks.

### Optional

4. **Analysis focus** — Specify whether you want deeper analysis on pricing, listing optimization, promotional tactics, or review sentiment. Defaults to a balanced overview of all areas.

5. **Time period** — Historical timeframe for trend analysis such as last 30 days, last quarter, or year-over-year comparison.

6. **Your margin floor** — Minimum acceptable margin percentage. If provided, all pricing recommendations will respect this constraint.

7. **Priority metrics** — Which KPIs matter most to you: BSR, review velocity, conversion rate, traffic share. Helps weight the recommendations.

---

## Workflow — Mode A (Single Competitor Deep-Dive)

### Step 1: Baseline Your Position

Before analyzing the competitor, document your own listing's current state across the 6 analysis categories. This creates the comparison anchor. Record:
- Your current price, promotion status, and price history (if known)
- Your listing quality: title structure, bullet points, image count, A+ content status
- Your review count, average rating, and recent review sentiment
- Your keyword visibility for the top 10 category terms
- Your current promotional activity

### Step 2: Competitor Listing Audit

Analyze the competitor's product listing element by element:

**Title analysis:**
- Character length and keyword density
- Brand positioning (brand-first vs keyword-first)
- Key feature callouts in title
- Compliance with platform title guidelines

**Visual content:**
- Main image quality and style (lifestyle vs white background vs infographic)
- Total image count and variety (usage scenarios, size reference, packaging)
- Video presence and quality
- A+ / Enhanced Brand Content modules used

**Bullet points and description:**
- Benefit-first vs feature-first structure
- Specificity of claims (numbers, measurements, proof points)
- Keyword integration patterns
- Emotional triggers and social proof references
- Reading level and tone

**Backend indicators:**
- Category node placement
- Variation strategy (how many ASINs/SKUs in the family)
- Brand registry status indicators
- Fulfillment method (FBA, FBM, SFP, platform-fulfilled)

### Step 3: Pricing Strategy Analysis

Map the competitor's pricing approach:

- **Current price** vs your price (absolute and percentage difference)
- **Price position** in category (cheapest, mid-range, premium)
- **Per-unit economics** — normalize multi-packs to per-unit cost
- **Shipping strategy** — free shipping threshold, Prime eligibility, shipping speed
- **Subscribe & Save / auto-replenishment** pricing if applicable
- **Bundle offers** — what's included and effective per-item price
- **Coupon and promotion history** — current coupons, lightning deals, percentage-off patterns
- **Price stability** — evidence of frequent changes, dynamic pricing, or price matching behavior

### Step 4: Review Intelligence

Analyze the competitor's review profile:

- **Volume and velocity** — total reviews, estimated monthly review acquisition rate
- **Rating distribution** — percentage at each star level, not just the average
- **Recent trend** — are recent reviews higher or lower than the lifetime average?
- **Sentiment themes** — what do positive reviewers praise most? What do negative reviewers complain about?
- **Response patterns** — does the seller respond to negative reviews? How quickly?
- **Review quality signals** — verified purchase percentage, photo/video review percentage
- **Competitive gaps** — complaints about the competitor that your product solves

### Step 5: Promotional Tactics Assessment

Document the competitor's promotional playbook:

- **Platform promotions** — Lightning Deals, flash sales, campaign participation (Prime Day, 11.11, etc.)
- **Coupon strategy** — coupon values, clip rates, frequency of refresh
- **Social media presence** — active platforms, content themes, posting frequency
- **Influencer partnerships** — identified collaborations, affiliate program indicators
- **Email/SMS indicators** — subscribe prompts, loyalty program mentions
- **Cross-selling and upselling** — "frequently bought together" positioning, bundle pages
- **Seasonal patterns** — promotion timing relative to category seasonality

### Step 6: Keyword and Search Visibility

Assess the competitor's search positioning:

- **Primary keyword targets** — what terms is their listing optimized for?
- **Title keyword strategy** — front-loaded vs distributed keyword placement
- **Organic rank indicators** — where they appear for key search terms
- **Sponsored placement** — are they running PPC on their own brand terms? On category terms?
- **Keyword gaps** — relevant terms they are NOT targeting that represent opportunities for you
- **Backend search term indicators** — terms where they rank but don't have visible keyword presence

### Step 7: Synthesize and Recommend

Compile findings into the Competitive Positioning Map and generate prioritized recommendations:

1. **Competitive Positioning Map** — Visual quadrant or comparison table showing where you and the competitor stand on key dimensions
2. **Threat Assessment** — Rate the competitor as low/medium/high threat across each category
3. **Opportunity List** — Specific gaps and weaknesses you can exploit
4. **Prioritized Action Plan** — Top 5-10 recommendations ranked by:
   - **Impact** (High/Medium/Low) — How much this action could move your metrics
   - **Effort** (High/Medium/Low) — Resources and time required
   - **Urgency** (Act now / This quarter / When resources allow)

---

## Workflow — Mode B (Landscape Scan)

### Step 1: Define the Competitive Set

Identify and categorize competitors:
- **Direct competitors** — Same product, same category, same platform
- **Indirect competitors** — Different product solving the same need
- **Aspirational competitors** — Market leaders whose strategies you want to study

### Step 2: Standardized Data Collection

For each competitor, collect a consistent data set using the Competitor Snapshot Card format (see `references/output-template.md`). Ensure every field is populated for apples-to-apples comparison.

### Step 3: Cross-Competitor Comparison

Build comparison matrices across:
- Pricing tiers and positioning
- Listing quality scores (rate each listing element 1-5)
- Review profiles (volume, rating, velocity)
- Promotional activity levels
- Keyword coverage overlap and gaps

### Step 4: Market Map

Create the Competitive Landscape Map showing:
- Price vs quality perception positioning
- Market share indicators (review volume as proxy)
- Segment clusters (budget, mid-range, premium)
- Whitespace areas with no strong competitor presence

### Step 5: Strategic Synthesis

Deliver:
- **Category trends** — What are most competitors doing? What's the emerging pattern?
- **Your relative position** — Where you sit in the landscape
- **Differentiation opportunities** — Where you can break from the pack
- **Defensive priorities** — Where competitors are closing in on your position
- **Prioritized action plan** — Same impact/effort/urgency framework as Mode A

---

## Analysis Categories Reference

The 6 core analysis categories, applied consistently across all competitor assessments:

| # | Category | Key Questions |
|---|---|---|
| 1 | Listing Quality | How well-optimized is the competitor's product listing? Title, images, bullets, A+ content, variations. |
| 2 | Pricing Strategy | How is the competitor positioned on price? What's their promotion cadence? Per-unit economics? |
| 3 | Review Profile | What's the review volume, rating, velocity, and sentiment? Where are the complaints? |
| 4 | Promotional Tactics | What promotions, coupons, campaigns, and partnerships is the competitor running? |
| 5 | Search Visibility | What keywords is the competitor targeting? Where do they rank? What gaps exist? |
| 6 | Brand & Positioning | How does the competitor position themselves? Premium vs value? What's their brand story? |

---

## Writing Rules

1. **State evidence strength explicitly.** Every claim must be tagged: "observed" (you saw it), "inferred" (logical deduction from available data), or "estimated" (rough approximation). Never present estimates as facts.

2. **No fabricated data.** Never invent BSR numbers, sales velocity, conversion rates, or price history. If data is unavailable, say so and explain what could be observed instead.

3. **Normalize before comparing.** Multi-packs to per-unit. Different currencies to one standard. Different sizes to per-gram or per-ounce. Shipping costs included in landed price.

4. **Separate new from used/refurbished.** Never mix condition types in price comparisons. Flag when competitor listings include refurbished or open-box inventory.

5. **Flag temporary conditions.** If a competitor is running a Lightning Deal or seasonal promotion, note it as temporary. Don't set strategy based on a flash sale price.

6. **Timestamp everything.** Every data point gets a collection date. Analysis based on old data (>7 days) gets a freshness warning.

7. **Acknowledge platform limitations.** You cannot access private analytics, internal conversion data, or exact ad spend. Recommendations must be based on publicly observable signals only.

8. **Competitor names are facts, not judgments.** Report what competitors do. Avoid characterizing their decisions as "wrong" or "stupid" — they may have information you don't.

9. **Recommendations must be specific and actionable.** "Monitor the market" is not a recommendation. "Reduce your price by 8% to match Competitor B's effective per-unit cost while maintaining a 22% margin" is.

10. **Every recommendation respects the margin floor.** If the user provided a minimum margin, no pricing recommendation should breach it without an explicit warning and justification.

---

## Worked Example 1 — Mode A Single Competitor Deep-Dive

**Scenario:** You sell a portable blender on Amazon US at $29.99. A new competitor launched 3 months ago at $24.99 and has accumulated 800 reviews with a 4.6 rating. You want to understand their strategy and respond.

**Input provided:**
- Your listing: amazon.com/dp/B0EXAMPLE1
- Competitor: amazon.com/dp/B0EXAMPLE2
- Category: Portable blenders
- Analysis focus: Pricing and review strategy
- Margin floor: 35%

**Key findings (abbreviated):**

*Listing Quality:* Competitor uses 7 images (you have 5) including a size-comparison infographic and a 30-second video. Their title is keyword-optimized with "Portable Blender" in position 1-2. Their bullet points lead with benefits and include specific measurements. A+ content with comparison chart showing advantages over 3 unnamed competitors.

*Pricing:* Competitor's effective price is $22.49 after a persistent 10% coupon. At your COGS of $9.50, matching this price would give you a 58% margin — well above your floor. However, their lower price is driving volume: estimated 500+ units/month based on review velocity.

*Review Intelligence:* 800 reviews in 3 months = ~267/month velocity (likely vine + early reviewer program + insert cards). Rating distribution: 72% 5-star, 15% 4-star, 8% 3-star, 3% 2-star, 2% 1-star. Top complaint (23 mentions): "Lid leaks when blending thick smoothies." Your product doesn't have this issue — this is an exploitable gap.

*Recommendation #1 (Impact: High, Effort: Low, Urgency: Act now):*
Add a bullet point and A+ module specifically addressing leak-proof design. Target the search term "leak proof portable blender" which the competitor is not optimizing for but their negative reviews are generating demand for.

*Recommendation #2 (Impact: High, Effort: Medium, Urgency: This quarter):*
Reduce price to $26.99 (10% reduction) and add a 5% coupon for an effective price of $25.64. This narrows the gap to $3.15 while maintaining a 73% margin. Pair with increased PPC spend on "portable blender leak proof."

---

## Worked Example 2 — Mode B Landscape Scan

**Scenario:** You sell organic dog treats on Shopee Malaysia and want to map the competitive landscape before expanding your product line.

**Input provided:**
- Your store: shopee.com.my/yourstore
- Competitors: 6 store URLs
- Category: Organic dog treats
- Time period: Last 90 days

**Key findings (abbreviated):**

*Market Map:* The organic dog treats category clusters into 3 tiers: Budget (RM 8-15/pack, 4 competitors), Mid-range (RM 18-28/pack, you + 2 competitors), Premium (RM 35-55/pack, 1 competitor). No competitor owns the "premium organic + locally sourced" positioning — whitespace identified.

*Cross-Competitor Pricing Matrix:*

| Competitor | Price/pack | Price/gram | Free shipping? | Voucher active? |
|---|---|---|---|---|
| Competitor A | RM 12.90 | RM 0.13 | Above RM 40 | 15% off, min RM 25 |
| Competitor B | RM 14.50 | RM 0.15 | Above RM 30 | Free shipping voucher |
| You | RM 22.90 | RM 0.19 | Above RM 50 | None |
| Competitor C | RM 25.00 | RM 0.21 | Free | 10% new customer |
| Competitor D | RM 38.00 | RM 0.25 | Free | Bundle: buy 3 get 1 |

*Strategic Synthesis:* You are positioned in mid-range with the highest per-gram price in your tier and no active promotions. Lower your free shipping threshold to RM 35 (matching Competitor B's approach) and introduce a "subscribe monthly" bundle at 15% off. This addresses the key competitive gap without a direct price cut.

---

## Common Mistakes

1. **Treating a flash sale price as the regular price.** A competitor running a Lightning Deal at 40% off is not "permanently cheaper." Check whether the discount is temporary before adjusting your strategy.

2. **Comparing multi-packs to single units.** A 3-pack at $15 ($5/unit) is cheaper than a single unit at $7, but the comparison must be per-unit. Always normalize.

3. **Equating review count with quality.** A competitor with 5,000 reviews and a 3.8 rating is not necessarily in a stronger position than you with 200 reviews and a 4.7 rating. Weight velocity and sentiment, not just volume.

4. **Ignoring fulfillment method differences.** FBA vs FBM pricing comparisons are apples to oranges. FBA listings include fulfillment in the price; FBM may have separate shipping. Account for landed cost.

5. **Assuming static competitor behavior.** Competitors react to your moves. A price cut that works today may trigger a price war tomorrow. Factor likely competitive response into recommendations.

6. **Over-indexing on a single competitor.** Unless Mode A was specifically requested, don't build your strategy around one rival. Market dynamics involve the full competitive set.

7. **Fabricating historical trends.** If you only have today's data, you have a snapshot, not a trend. Say "current price as of [date]" not "prices have been declining."

8. **Recommending below the margin floor.** If the user set a 35% minimum margin, every pricing suggestion must respect that constraint — or explicitly flag the exception with justification.

9. **Confusing organic rank with sponsored placement.** A competitor appearing in position 1 for a search term may be paying for that placement. Note whether rankings are organic or sponsored.

10. **Presenting competitor data without context.** "Competitor has 1,000 reviews" means nothing without knowing the category average, the competitor's time in market, and the review velocity trend.

---

## Resources

| File | Purpose |
|---|---|
| `references/output-template.md` | Structured templates for Mode A and Mode B deliverables |
| `references/analysis-frameworks.md` | Detailed frameworks for each of the 6 analysis categories |
| `references/platform-specifics.md` | Platform-specific data points and benchmarks for Amazon, Shopee, TikTok Shop, Lazada, Shopify |
| `assets/quality-checklist.md` | Pre-delivery quality checklist (45 items) |
