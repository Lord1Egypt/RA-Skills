---
name: finding-youtube-sponsorship-candidates
description: >
  Finds YouTube channels suitable for brand sponsorships using apidojo's YouTube scraper on Apify.
  Triggers when the user asks to: find YouTube channels to sponsor, discover YouTubers who accept
  brand deals in a niche, identify YouTube influencers for mid-roll or integration sponsorships,
  find channels that already run sponsors in a product category, research YouTube sponsorship
  opportunities for a brand, identify high-CPM YouTube audiences for B2B or SaaS sponsorships,
  or build a YouTube outreach list for a sponsorship campaign.
  Returns channel name, subscriber count, avg views, engagement rate, niche, and sponsorship history.
  Ideal for brand partnerships managers, SaaS marketing teams, and sponsorship agencies.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/youtube-scraper
---

# Finding YouTube Sponsorship Candidates

Discovers YouTube channels that are good fits for brand integrations. Channels with existing sponsor history are the most efficient outreach targets — they've already proven willingness to accept sponsorships.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | YouTube URLs — channels, playlists, Shorts, search results |
| `youtubeHandles` | array | Optional | `[]` | YouTube channel handles (e.g. `@kurzgesagt`) |
| `getTrending` | boolean | Optional | `false` | Retrieve trending videos |
| `keywords` | array | Optional | `[]` | Search keywords |
| `gl` | string | Optional | `us` | Country code for results (e.g. `US`, `GB`) |
| `hl` | string | Optional | `en` | Language code (e.g. `en`, `de`) |
| `uploadDate` | string | Optional | `all` | Upload date filter: `any`, `hour`, `today`, `week`, `month`, `year` |
| `duration` | string | Optional | `all` | Duration filter: `any`, `short`, `long` |
| `features` | string | Optional | `all` | Feature filter: `4k`, `hd`, `live`, `cc`, `3d`, `hdr`, etc. |
| `sort` | string | Optional | `r` | Sort order for search results |
| `maxItems` | number | Optional | Unlimited | Maximum videos to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Search YouTube for niche channel content
- [ ] Step 2: Collect channel handles from results
- [ ] Step 3: Enrich channel data
- [ ] Step 4: Score sponsorship fit
- [ ] Step 5: Deliver ranked outreach list
```

### Step 1: Search for Niche Content


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~youtube-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~youtube-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~youtube-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~youtube-scraper"
Input:
{
  "searchKeywords": ["best [NICHE] tools", "[NICHE] review", "[NICHE] for beginners", "top [NICHE]"],
  "maxResults": 50,
  "type": "video"
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~youtube-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{
    "searchKeywords": ["best personal finance tools", "personal finance review"],
    "maxResults": 50,
    "type": "video"
  }'
```

Collect unique `channelId` and `channelName` values.

### Step 2: Enrich Channel Data

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~youtube-scraper"
Input:
{
  "startUrls": [{"url": "https://www.youtube.com/channel/[CHANNEL_ID]"}],
  "maxResults": 10,
  "type": "video"
}
```

### Step 3: Score Sponsorship Fit

```
view_ratio = avg_views / subscriber_count

sponsorship_score = (view_ratio > 0.1 ? 1 : view_ratio / 0.1) * 0.30
                  + (subscriber_count in 10000..200000 ? 1 : 0.6) * 0.20
                  + (avg_comments / avg_views > 0.005 ? 1 : (avg_comments/avg_views)/0.005) * 0.20
                  + (has_sponsor_history ? 1 : 0) * 0.30
```

**Sponsorship signal detection (in last 10 video titles/descriptions):**
```
sponsor_count = count(videos where description contains ["sponsored by", "use code", "thanks to", "partner"])
has_sponsor_history = sponsor_count >= 1
repeat_sponsor = sponsor_count >= 3
```

**Tier:** TIER A ≥ 0.70 | TIER B 0.45–0.69 | TIER C < 0.45

### Step 4: Edge Cases

- **View count spike from one viral video**: Use median views from last 10 videos, not mean; flag channels where `max_views > 10× median`
- **Channel in adjacent but not target niche**: Score niche alignment — percentage of last 20 videos in target niche
- **Subscriber count stale**: YouTube counts lag; use `avg_views` as the true reach proxy
- **No description available**: Skip sponsorship history check; score at 0.5 for that component

## Output Format

```
# YouTube Sponsorship Candidates: [NICHE]
Channels evaluated: [N] | TIER A: [N] | TIER B: [N] | Date: [DATE]

## TIER A — Strong Sponsorship Candidates
| Channel | Subscribers | Avg Views | View Ratio | Sponsor History | Niche Fit | Score |
|---------|------------|-----------|------------|-----------------|-----------|-------|
| [name] | [N] | [N] | [X.XX] | [Yes/No/Repeat] | [%] | [0.XX] |

## TIER B — Secondary Candidates
| Channel | Subscribers | Avg Views | View Ratio | Last Sponsor |
|---------|------------|-----------|------------|-------------|

## Sponsorship Landscape in [NICHE]
- Channels already running sponsors: [N]/[N] evaluated ([X%])
- Most common sponsor in category: [brand name] (seen on [N] channels)
- Typical viewer demographic signal (from video titles): [description]
```

## Troubleshooting

**Results are all mega-channels (> 1M subs)**: Narrow the search query with "beginner" or "indie" qualifiers; or filter post-scrape by subscriber count.
**Niche too broad**: Narrow to a sub-niche (e.g. "personal finance" → "fire movement", "crypto" → "Bitcoin long-term investing").
**Can't detect sponsor history from descriptions**: Sponsor language is sometimes hidden in video captions (not descriptions). This is a known limitation — supplement with manual check of top 5 candidates.

