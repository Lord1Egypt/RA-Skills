---
name: apify-scraper
version: 1.0.0
description: "Scrape content from sites that block bots — Twitter/X threads, Reddit, LinkedIn, YouTube comments, Google SERP, and more. Use when standard web_fetch is blocked and you need full thread/comment data. Requires APIFY_API_KEY."
metadata:
  {
    "openclaw": {
      "emoji": "🕷️",
      "requires": {
        "bins": ["python3"],
        "env": ["APIFY_API_KEY"]
      },
      "primaryEnv": "APIFY_API_KEY",
      "network": {
        "outbound": true,
        "reason": "Calls Apify API (api.apify.com) to run cloud actors that scrape external sites. Actors run server-side on Apify infrastructure."
      },
      "security_notes": "All scraping is performed via the user's own Apify account using their API key. Actors run on Apify's infrastructure — no data is sent to third parties beyond Apify (the user's chosen scraping platform). LinkedIn scraping is ToS-sensitive; use sparingly for research purposes only."
    }
  }
---

# Apify Scraper Skill

Use this skill when you need to scrape content from sites that block bots — Twitter/X threads, Reddit, LinkedIn, YouTube comments, Google SERP, Amazon, Product Hunt, etc.

## When to Use

- A Twitter/X URL is shared and you need the full thread (not just the first tweet)
- You need Reddit thread content without the expensive API
- LinkedIn company/profile data is needed
- YouTube comments or video metadata beyond what the API gives
- Google search results programmatically
- Any site that blocks standard web_fetch

**Do NOT use for:** sites accessible via normal web_fetch or web_search. Apify costs credits — use it only when needed.

## Setup

- **API Key:** `op://OpenClaw/Apify API Credentials/credential` (also in gateway plist as `APIFY_API_KEY`)
- **Dashboard:** https://console.apify.com (account: redditech)
- **Plan:** FREE ($5/mo credit)
- **Script:** `python3 scripts/apify-run.py <actor> <input_json>`

## Running an Actor

```bash
python3 /Users/loki/.openclaw/workspace/scripts/apify-run.py \
  "apidojo/tweet-scraper" \
  '{"twitterHandles": ["solanamobile"], "maxItems": 50}'
```

## Key Actors

### Twitter/X
- **`apidojo/tweet-scraper`** — $0.40/1K tweets. Full thread support via `conversationIds`. Advanced search syntax.
  ```json
  {"conversationIds": ["2034675043033375103"], "maxItems": 50}
  ```
  or by handle:
  ```json
  {"twitterHandles": ["solanamobile"], "maxItems": 20}
  ```

### Reddit
- **`trudax/reddit-scraper-lite`** — Free tier friendly. Fetch threads + comments.
  ```json
  {"startUrls": [{"url": "https://reddit.com/r/solana/comments/..."}], "maxItems": 100}
  ```

### YouTube
- **`streamers/youtube-scraper`** — Comments + metadata.
  ```json
  {"startUrls": [{"url": "https://youtube.com/watch?v=..."}], "maxComments": 200}
  ```

### Google SERP
- **`apify/google-search-scraper`** — Search results as structured data.
  ```json
  {"queries": "solana mobile grants", "maxPagesPerQuery": 1}
  ```

### LinkedIn
- **`anchor/linkedin-profile-scraper`** — ⚠️ ToS risk. Use sparingly for research only.

## Pricing Reference
- 1 CU = 1 GB RAM × 1 hour
- Free tier: $5/mo (~16.7 CU)
- Tweet scraping: ~0.035–0.04 CU/1K tweets (~$0.01/1K on free tier)
- Some actors charge flat per-result: $0.25–$0.40/1K tweets
- Check usage: https://console.apify.com/billing

## Notes
- Results are returned as a dataset — the script polls until complete
- Timeout: 5 minutes default (most actors finish in 30–60s)
- If an actor breaks (community-maintained), check Apify Store for alternatives
- MCP integration pending — Apify MCP server exists but openclaw.json doesn't support `mcpServers` key yet (schema validation rejects it). Use this script approach instead.
