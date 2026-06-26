# Platform Audience Specifications

## Meta (Facebook & Instagram)

### Lookalike Audiences
- **Minimum seed size:** 100 (recommended 1,000–5,000)
- **Percentage options:** 1%–10% in 1% increments
- **1% size:** ~2.1M in US, varies by country
- **Source types:** Customer list, website visitors, app activity, engagement (video views, lead forms, page/profile interactions)
- **Refresh:** Automatic every 3–7 days if source updates
- **Stacking:** Can layer LAL + interest for narrower targeting
- **Key limitation:** LAL quality degrades significantly above 5%; 8–10% approaches broad targeting

### Custom Audiences
- **Website Custom Audiences:** Based on pixel events; windows up to 180 days
  - ViewContent, AddToCart, InitiateCheckout, Purchase events
  - Frequency filters: "people who visited X times"
  - Time recency: 1–180 day windows
- **Customer List:** Upload via CSV (email, phone, MAID); match rate typically 50–70%
- **Engagement:** Video viewers (25%/50%/75%/95%), lead form openers, IG profile visitors, page engagers
- **Minimum audience size for delivery:** 1,000 users (20+ for LAL seed, but quality suffers below 1,000)

### Exclusion Capabilities
- Exclude custom audiences from ad sets
- Cannot exclude across campaigns without manual management
- Advantage+ campaigns have limited exclusion support (audience suggestions only)

### Frequency Management
- No native frequency cap for auction campaigns
- Reach & Frequency campaigns allow caps but require higher minimums
- Monitor via Ads Manager "Frequency" column
- Practical cap enforcement: budget pacing + audience sizing

### Budget Minimums
- $1/day per ad set minimum
- Advantage+ Shopping: $50/day recommended minimum
- CBO: $100/day minimum recommended for 3+ ad sets

---

## TikTok

### Lookalike Audiences
- **Minimum seed size:** 1,000
- **Expansion options:** Narrow, Balanced, Broad (no percentage control)
- **Source types:** Customer file, pixel audiences, app event audiences, engagement audiences
- **Refresh:** Manual re-creation required for updated seeds
- **Key limitation:** Less granular than Meta; Broad lookalike ≈ near-broad targeting

### Custom Audiences
- **Website Audiences:** Based on TikTok pixel; windows up to 180 days
  - ViewContent, AddToCart, PlaceOrder, CompletePayment
  - URL-based rules available
- **Customer File:** Upload via CSV/TXT (email, phone, MAID, GAID, IDFA)
  - Match rate typically 30–50% (lower than Meta)
- **Engagement:** Video views (2s/6s/full), profile visits, follower lists
- **App Event:** Install, registration, purchase, etc.
- **Minimum for delivery:** Approximately 1,000 matched users

### Ad Format Audience Considerations
- **Video Shopping Ads (VSA):** Product catalog + audience targeting; best for retargeting
- **Product Shopping Ads (PSA):** Catalog browsing format; works for prospecting
- **Keep VSA and PSA in separate campaigns** — overlapping audiences causes self-competition
- **Spark Ads:** Boost organic posts to targeted audiences; good for warm/social proof

### Smart+ Campaigns
- Automated targeting; limited audience control
- Can add "audience suggestions" but algorithm may ignore them
- Best used as a broad prospecting comparison test alongside manual targeting
- No exclusion support within Smart+

### Frequency Management
- Native frequency cap available (by day or by campaign lifetime)
- Set at ad group level
- Recommended: 3–4/week for prospecting, 6–7/week for retargeting

---

## Google Ads

### Customer Match
- **Upload:** Email, phone, mailing address, mobile device ID
- **Match rate:** 30–60% depending on data quality
- **Use cases:** Audience signal in PMax, Similar Segments seed, RLSA bid adjustment, exclusion
- **Refresh:** Manual upload or automated via API/Zapier
- **Requirements:** 1,000+ matched users, account in good standing, 90-day history, $50K+ lifetime spend (for some features)

### In-Market Audiences
- Google-defined audiences actively researching or comparing products
- Available for Search, Display, YouTube, Discovery, PMax
- Categories like "Beauty & Personal Care > Skin Care" or "Apparel > Women's Clothing"
- **Best practice:** Layer as observation first, then bid adjust; or use as PMax signal

### Similar Segments (formerly Similar Audiences)
- Auto-generated from remarketing lists and Customer Match
- **Deprecated for most campaign types** as of 2023; replaced by audience expansion and optimized targeting
- Still available as PMax audience signals

### Remarketing Lists
- **Google Ads tag / GA4 audiences:** website visitors with customizable conditions
- **YouTube audiences:** channel subscribers, video viewers, ad interaction
- **App audiences:** users who installed, or performed in-app actions
- **Minimum size:** 100 for Display, 1,000 for Search (RLSA)
- **Windows:** up to 540 days for Display, 180 days common

### Performance Max
- Asset-based campaign type serving across all Google surfaces
- **Audience signals:** Customer Match, website visitors, in-market, custom segments, interests
- Signals are suggestions, not restrictions — PMax will go broader
- Cannot add exclusions except brand exclusions and customer lists at account level
- **Best practice:** Use strong audience signals + asset groups organized by product category

### Frequency Management
- Display campaigns: manual frequency cap (impressions per day/week/month)
- Search: not applicable (intent-based)
- YouTube: frequency cap available
- PMax: no frequency cap control
- Discovery: limited frequency control

---

## Cross-Platform Considerations

### Data Sync Methods
| Method | Platforms | Automation | Cost |
|--------|----------|-----------|------|
| Manual CSV upload | All three | None | Free, time-intensive |
| CDP (Segment, mParticle) | All three | Full | $1K–$10K+/month |
| Zapier / Make | Meta + Google | Partial | $50–$200/month |
| Platform APIs | All three | Full | Developer cost |
| LiveRamp | All three | Full | $5K+/month |

### Match Rate Optimization
- **Always hash before upload** (SHA-256 for Meta/TikTok, Google auto-hashes)
- **Include multiple identifiers:** email + phone increases match rate by 15–30%
- **Normalize data:** lowercase emails, remove spaces, format phone numbers with country code
- **Country-specific:** match rates vary significantly by region

### Attribution Windows (defaults)
| Platform | Click | View |
|----------|-------|------|
| Meta | 7 days | 1 day |
| TikTok | 7 days | 1 day |
| Google | 30 days | — (Display: 30 days view-through) |

Note: Cross-platform attribution overlap is inevitable. Budget 10–15% of measured conversions as likely double-counted when running all three platforms simultaneously.
