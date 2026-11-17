---
name: finding-real-estate-professionals-on-twitter
description: >
  Finds real estate agents, brokers, property investors, and real estate professionals on
  Twitter/X using apidojo's Twitter User Scraper on Apify. Triggers when the user asks to: find
  real estate agents on Twitter, discover property professionals on X for outreach, build a list
  of realtors active on Twitter, find real estate investors or brokers on X, prospect real estate
  professionals via their Twitter bios, identify mortgage brokers or property managers on Twitter,
  or compile a real estate professional contact list from Twitter. Returns username, bio, follower
  count, verification status, location, and website per user. Ideal for PropTech SaaS vendors,
  mortgage product teams, and B2B service providers targeting real estate professionals.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/twitter-user-scraper
---

# Finding Real Estate Professionals On Twitter

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Twitter profile or tweet URLs |
| `twitterHandles` | array | Optional | `[]` | Twitter usernames (without @) |
| `twitterUserIds` | array | Optional | `[]` | Twitter user IDs |
| `getFollowers` | boolean | Optional | `false` | Extract follower lists |
| `getFollowing` | boolean | Optional | `false` | Extract following lists |
| `getRetweeters` | boolean | Optional | `false` | Extract retweeters of a tweet URL |
| `includeUnavailableUsers` | boolean | Optional | `false` | Include unavailable/suspended users |
| `maxItems` | number | Optional | Unlimited | Maximum users to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~twitter-user-scraper" --input '{"keywords": ["realtor", "real estate agent"], "maxItems": 100}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~twitter-user-scraper" --input '{"keywords": ["realtor", "real estate agent"], "maxItems": 100}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~twitter-user-scraper" --input '{"keywords": ["realtor", "real estate agent"], "maxItems": 100}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~twitter-user-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["realtor", "real estate agent"], "maxItems": 100}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~twitter-user-scraper` and the input above.

---

## Scoring & Ranking

Score each user by:
- `followers` → normalized 0-1 (cap at 50K), weight 0.30
- `bio_match_score` (contains: realtor, broker, real estate, property, agent, MLS) → 0 or 1, weight 0.40
- `has_website` → 0 or 1, weight 0.30

```python
score = 0.30 * min(followers / 50000, 1.0) + 0.40 * int(bio_match) + 0.30 * int(has_website)
```

---

## Classification

| Score | Tier | Label |
|-------|------|-------|
| ≥ 0.70 | A | PRIME_OUTREACH |
| 0.40–0.69 | B | HOT_CANDIDATE |
| < 0.40 | C | LOW_PRIORITY |

---

## Edge Cases

- **Generic bio keywords**: "house" or "home" match too broadly. Use "realtor", "real estate agent", "MLS".
- **Personal accounts mixed in**: Filter by followers > 200 and has website link.
- **Bot accounts**: Unusually high following-to-follower ratio — filter out.
- **Keyword not in bio**: Twitter user search matches bio text — results may vary if bio is non-standard.
- **International agents**: Use country-specific terms (e.g., "estate agent" for UK).
