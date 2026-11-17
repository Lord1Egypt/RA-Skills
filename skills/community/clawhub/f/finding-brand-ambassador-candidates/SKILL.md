---
name: finding-brand-ambassador-candidates
description: >
  Finds brand ambassador candidates on Instagram and TikTok using apidojo's scrapers on Apify.
  Triggers when the user asks to: find potential brand ambassadors for a company, discover
  loyal customers who post about a brand organically, identify advocates who could become paid
  ambassadors, find creators already talking positively about a brand or product category,
  build a brand ambassador program pipeline, discover micro-influencers with genuine brand affinity,
  or find repeat brand mention creators for ambassador recruitment.
  Returns creator handle, mention frequency, engagement rate, follower count, and affinity signals.
  Ideal for brand partnership managers, DTC brands, and ambassador program coordinators.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/instagram-scraper, apidojo/tiktok-scraper
---

# Finding Brand Ambassador Candidates

Identifies creators who already post about a brand or product organically — these are the highest-converting ambassador recruits because their content is authentic and their audience trusts them.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | Instagram URLs — profiles, hashtags, locations, audio pages, reels |
| `until` | string | Optional | — | Scrape posts until this date (YYYY-MM-DD) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Search brand hashtags on both platforms
- [ ] Step 2: Identify repeat posters
- [ ] Step 3: Score ambassador fit
- [ ] Step 4: Check for competing partnerships
- [ ] Step 5: Deliver ranked ambassador pipeline
```

### Step 1: Search Brand Mentions

**Instagram:**
```
Tool: apify:run-actor
Actor: "apidojo~instagram-scraper"
Input: {"keywords": ["#[brand]", "#[brand]review", "#[brand]community", "#[brandproduct]"], "maxItems": 200}
```

**TikTok:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-scraper"
Input: {"keywords": ["#[brand]", "#[brand]review", "#[brand]tiktokmademebuyit"], "maxItems": 300}
```


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**REST API fallback:**
```bash
# Instagram
curl -X POST "https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"keywords": ["#[brand]", "#[brand]review"], "maxItems": 200}'
```

### Step 2: Score Ambassador Fit

For each repeat poster (appeared ≥ 2 times):
```
ambassador_score = (post_count / 5) * 0.25                             # organic depth
                 + (engagement_rate / 5.0) * 0.30                      # audience quality
                 + (has_competing_sponsor ? 0 : 1) * 0.25              # exclusivity signal
                 + (follower_count in 1000..50000 ? 1 : 0.6) * 0.20   # partnership tier
```

**Competing sponsor check**: Scan last 20 posts for `#ad` or `#sponsored` with a brand that competes in the same category. If found: `has_competing_sponsor = true`.

### Step 3: Edge Cases

- **Brand's own reposts appear in hashtag**: Drop posts where `ownerUsername` = brand account
- **Repeat poster is a bot**: Check: ratio of followers/following ≤ 0.1 AND recent posts are all different brands — likely a spam/bot account
- **Low brand mention specificity**: Creator mentions the brand once in passing — not a genuine advocate; require at least one post that is primarily about the brand
- **Creator already in ambassador program**: No reliable way to detect this via scraping; note this as a known limitation — outreach will reveal it

## Output Format

```
# Brand Ambassador Pipeline: [BRAND/PRODUCT]
Creators found: [N] | Repeat advocates: [N] | High-fit: [N] | Date: [DATE]

## Tier 1 — High-Fit Ambassadors (Multiple Organic Posts)
| Creator | Platform | @Handle | Followers | Eng Rate | Brand Posts | Competing Sponsor | Score |
|---------|---------|---------|-----------|----------|------------|------------------|-------|
| [name] | IG/TT | @[handle] | [N] | [X%] | [N] | [Yes/No] | [0.XX] |

## Tier 2 — Early Advocates (1-2 Brand Posts)
| Creator | Platform | Followers | Brand Posts | Eng Rate |
|---------|---------|-----------|------------|----------|

## Outreach Angle
For each Tier 1 creator, note: their most engaging brand post — reference it in outreach.
```

## Troubleshooting

**Brand hashtag has too few posts**: Brand may have low organic social presence — search product category hashtags and look for anyone mentioning brand by name in caption.
**All high-fit creators already have competing sponsors**: Indicates the category is saturated. Consider offering an exclusive deal to a mid-tier creator to lock out competition.
**No repeat posters found**: Brand lacks loyal vocal advocates — this itself is a finding. Consider product seeding to build an organic advocate base before formal ambassador program launch.

