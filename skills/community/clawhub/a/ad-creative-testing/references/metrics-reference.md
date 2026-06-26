# Ad Creative Testing — Metrics Reference Guide

Quick reference for interpreting ad performance metrics and making test conclusion decisions.

---

## Core Metrics by Funnel Stage

### Top of Funnel — Attention and Reach

| Metric | Definition | Healthy Range | Warning Sign |
|---|---|---|---|
| CPM (Cost per 1,000 impressions) | Cost to show the ad 1,000 times | Varies by platform; $5–$30 for social | >2× your category benchmark |
| Reach | Unique accounts that saw the ad | — | Frequency >4 with declining CTR |
| Frequency | Average times each person saw the ad | 1.5–3.0 for testing | >4 = creative fatigue |
| Thumb Stop Rate | % who pause scrolling (3-sec views / impressions) | 25–40% | <20% = hook failure |

---

### Mid Funnel — Interest and Engagement

| Metric | Definition | Healthy Range | Warning Sign |
|---|---|---|---|
| CTR (Click-Through Rate) | Clicks ÷ Impressions | 0.8–2.5% social; 2–6% search | <0.5% = relevance failure |
| Link CTR | Clicks to destination URL ÷ Impressions | 0.5–1.5% | <0.3% |
| Video Completion Rate | % who watched to 75% or 100% | 15–40% at 75% mark | <10% = content holding failure |
| Hook Rate (3-sec view rate) | 3-second video views ÷ impressions | 25–40% | <20% |
| Engagement Rate | Total engagements ÷ reach | 1–5% | <0.5% in interest-stage campaigns |

---

### Bottom of Funnel — Conversion

| Metric | Definition | Healthy Range | Warning Sign |
|---|---|---|---|
| CPC (Cost Per Click) | Ad spend ÷ total clicks | Varies; $0.50–$3 social | Rising CPC with stable CTR = CPM issue |
| CPA (Cost Per Acquisition) | Ad spend ÷ conversions | Should be <30% of AOV | >50% of AOV = unprofitable |
| CVR (Conversion Rate) | Conversions ÷ landing page sessions | 1–5% for cold traffic | <0.5% = landing page issue |
| ROAS (Return on Ad Spend) | Revenue ÷ ad spend | Breakeven ROAS varies; see below | Below breakeven = pausing candidate |
| Add to Cart Rate | ATCs ÷ landing page sessions | 5–15% | <3% = offer or page issue |

---

## Breakeven ROAS Formula

```
Breakeven ROAS = 1 / Gross Margin %
```

**Examples:**
- 50% gross margin → Breakeven ROAS = 2.0×
- 60% gross margin → Breakeven ROAS = 1.67×
- 40% gross margin → Breakeven ROAS = 2.5×
- 70% gross margin → Breakeven ROAS = 1.43×

Target ROAS for scaling should be 1.5–2.0× breakeven ROAS to allow for overhead and profit.

---

## Platform-Specific Metric Notes

### Meta (Facebook / Instagram)
- **Hook Rate** = ThruPlay rate at 3 seconds ÷ impressions (calculate manually)
- **Outbound CTR** is more reliable than Link CTR — it excludes accidental taps
- Attribution window — Use 7-day click / 1-day view for testing consistency
- **Reported vs. actual ROAS**: Expect 20–30% over-reporting vs. triple-attributed revenue

### TikTok
- **6-second view rate** is the primary hook signal (not 3-second)
- **Watch time per video view** is stronger signal than completion % at scale
- Attribution window — TikTok defaults to 7-day click / 1-day view
- CPMs are generally 40–60% lower than Meta for cold audiences

### Google / YouTube
- **Skippable in-stream**: True View rate = % who watch 30s or to end (whichever first)
- **View-through conversions** carry less weight than click-through; don't include in primary ROAS calculation
- **Search ads**: Quality Score (1–10) affects CPCs significantly; track this alongside CTR

---

## Statistical Significance Quick Reference

| Sample Size Per Variant | Minimum for Reliable Read | Confidence Level |
|---|---|---|
| <50 conversions | Not reliable | Do not conclude |
| 50–100 conversions | Indicative only | 70–80% |
| 100–200 conversions | Sufficient for most decisions | ~90% |
| 200+ conversions | High confidence | 95%+ |

**Rule of thumb**: Never pause a test below 100 conversion events per variant, regardless of apparent winner.

**For click-based metrics** (CTR, Hook Rate): 10,000+ impressions per variant is the minimum before drawing conclusions.

---

## Metric Relationships and Diagnostic Logic

### Problem — Low ROAS, but CTR is strong
- Likely issue — **Landing page or offer mismatch** — the creative is setting expectations the landing page doesn't meet
- Check — CVR, Add to Cart Rate, checkout abandonment rate

### Problem — Low CTR, high CPM
- Likely issue — **Audience–creative mismatch** — the hook or visual is not relevant to this audience
- Check — Hook Rate (3-second view %), Frequency, audience overlap

### Problem — High CTR, low CVR
- Likely issue — **Landing page is the bottleneck**, not the creative
- Check — Page load speed, mobile UX, offer clarity, social proof above the fold

### Problem — Good CTR and CVR but low ROAS
- Likely issue — **AOV is too low** or **product margin doesn't support this CPA**
- Check — Average order value, upsell take rate, lifetime value projections

### Problem — Metrics look good, ROAS is declining week-over-week
- Likely issue — **Creative fatigue** (frequency too high) or **audience saturation**
- Check — Frequency, Reach change, Cost per 1,000 Reached vs. CPM ratio

---

## Testing Metric Priorities by Test Type

| Test Type | Primary Metric | Secondary Metrics | Ignore Until Scale |
|---|---|---|---|
| Hook test | Hook Rate (3-sec) | CTR, CPC | CPA, ROAS |
| Offer test | CVR, CPA | CTR, AOV | Hook Rate |
| Landing page test | CVR, Add to Cart Rate | Bounce rate | Hook Rate |
| Audience test | CPA, ROAS | CTR, CPM | Hook Rate |
| Creative format test | Hook Rate, Completion Rate | CTR | CPA (until volume) |
| Full creative test | CPA, ROAS | All above | — |

---

## Metric Glossary

**AOV** — Average Order Value — total revenue ÷ number of orders.

**ATC** — Add to Cart — user action of adding a product to cart.

**Attribution window** — The time period after a click or view in which a conversion is credited to the ad.

**Breakeven ROAS** — The ROAS at which ad revenue exactly covers cost of goods sold. Spending below this ROAS loses money on the product; spending above it generates contribution margin.

**Creative fatigue** — Declining performance caused by repeated exposure to the same ad. Typically detected when frequency rises above 4 while CTR or ROAS falls.

**CVR** — Conversion Rate — purchases ÷ sessions (or clicks, depending on platform).

**Holdout test** — A test in which one audience segment is deliberately excluded from seeing ads, to measure the true incremental lift of the advertising.

**Incrementality** — The true causal impact of advertising on conversions, net of what would have happened organically without the ads.

**MER (Media Efficiency Ratio)** — Total revenue ÷ total ad spend across all channels. A blended efficiency metric that accounts for cross-channel attribution gaps.

**ROAS** — Return on Ad Spend — revenue attributed to ads ÷ ad spend. Does not equal profitability; must be compared against breakeven ROAS.
