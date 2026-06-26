---
name: agenttimes
description: Live context layer for AI agents. One /ask endpoint for news, weather, crypto prices, and alerts. 228K+ articles, 3,576 feeds, 14 categories. Enriched with sentiment, entities, and credibility. Free to use, no API key needed.
metadata:
  openclaw:
    emoji: "\U0001F4F0"
    homepage: https://agenttimes.live
    author: penghian
    skillKey: agenttimes
    always: false
    requires:
      bins:
        - curl
    links:
      homepage: https://agenttimes.live
      documentation: https://agenttimes.live/info
---

# Agent Times — Live Context Layer for AI Agents

## TL;DR

```bash
# News search:
curl -s "https://agenttimes.live/ask?q=why+is+NVDA+down+today"

# Weather:
curl -s "https://agenttimes.live/ask?q=weather+tokyo"

# Crypto price:
curl -s "https://agenttimes.live/ask?q=bitcoin+price"

# Trending stories:
curl -s "https://agenttimes.live/trending"
```

Response is JSON. `/ask` auto-detects intent: news queries return articles with `title`, `url`, `summary`, `sentiment`, `entities`; `$TICKER` queries search by entity; weather queries return forecasts; crypto queries return prices. Check the `source` field. No API key needed.

## Common Tasks — Copy-Paste Commands

**Ticker search (use $ prefix):**
```bash
curl -s "https://agenttimes.live/ask?q=%24NVDA"
curl -s "https://agenttimes.live/ask?q=%24SPY"
curl -s "https://agenttimes.live/ask?q=%24AAPL"
```

**Weather (any city):**
```bash
curl -s "https://agenttimes.live/ask?q=weather+tokyo"
curl -s "https://agenttimes.live/ask?q=weather+london"
```

**Crypto prices:**
```bash
curl -s "https://agenttimes.live/ask?q=bitcoin+price"
curl -s "https://agenttimes.live/prices?symbol=ETH,SOL,BTC"
```

**News search:**
```bash
curl -s "https://agenttimes.live/ask?q=why+did+NVDA+drop+today"
```

**Job search (remote devops/SRE):**
```bash
curl -s "https://agenttimes.live/news?category=business&tag=jobs&limit=20"
```

**Country-specific news:**
```bash
curl -s "https://agenttimes.live/ask?q=singapore+news"
```

**Filter by any tag:** Add `&tag=TAG` to `/news`. Example tags: `jobs`, `gaming`, `space`, `bitcoin`, `asia`, `europe`, `startups`, `devtools`.

---

## What This Does

Agent Times is a one-stop information API for AI agents. **3,576 RSS feeds** across **14 categories**, **weather forecasts**, and **crypto prices** — all from one `/ask` endpoint.

- **Semantic search + neural re-ranking** — AI understands meaning, then a cross-encoder re-ranks results by true relevance. "Why did NVDA drop" finds "NVIDIA Falls 3% as Investors Weigh GTC Optimism Against Risks"
- **FinBERT sentiment** — finance articles scored by a financial-domain neural network. Correctly identifies "Rally fades as investors take profits" as bearish. Only runs on business, crypto, energy, ai, tech categories for accuracy.
- **Source credibility** — tier 1 (Reuters, BBC) get 1.3x ranking boost, tier 3 (unknown) get 0.8x penalty
- **GLiNER entity extraction** — zero-shot NER detects people, companies, locations, organizations, products, events. Plus ticker/crypto dictionary matching (300+ stocks, 100+ crypto).
- **ModernBERT classification** — each article classified by a fine-tuned ModernBERT model (93.9% accuracy, 149M params) reading actual text, not just RSS feed label. Tags auto-assigned by topic + country.
- **Weather forecasts** — global weather via Open-Meteo. Just ask "weather tokyo" or "weather london"
- **Crypto prices** — real-time prices from Pyth Network oracle (BTC, ETH, SOL, and 10+ more). Just ask "bitcoin price"
- **Country tags** — filter by 60+ countries and regions
- **Webhook subscriptions** — get notified when articles matching your topic arrive
- **4-tier fallback** — semantic search → keyword search → web search (70+ engines) → query suggestions

228,000+ articles with 30-day retention. 6 AI models (embedder on GPU, classifier on GPU, cross-encoder, FinBERT, GLiNER NER, tag centroids).

## When to Use Which Endpoint

| You want to... | Use this | Free? |
|---|---|---|
| Search for a topic | `GET /ask?q=TOPIC` | Yes |
| Check weather | `GET /ask?q=weather+tokyo` or `GET /weather?location=tokyo` | Yes |
| Get crypto prices | `GET /ask?q=bitcoin+price` or `GET /prices?symbol=BTC` | Yes |
| Get trending stories | `GET /trending` | Yes |
| Browse a category | `GET /news?category=CAT` | Yes |
| Filter by country/tag | `GET /news?category=world&tag=singapore` | Yes |
| Search the web | `GET /search?q=QUERY` | $0.001 (x402) |
| Monitor a topic | `POST /subscribe` | Yes |
| List categories | `GET /news/categories` | Yes |

**Rule of thumb:** Start with `/ask`. It's free, smart, and auto-detects if you're asking about news, weather, or crypto prices. Use `/news` only when you need bulk category browsing with filters.

## /ask — Smart Search (FREE)

Searches all 228K+ articles using AI semantic matching + keyword matching + web search fallback. Returns results ranked by relevance and recency.

```bash
curl -s "https://agenttimes.live/ask?q=bitcoin+etf"
curl -s "https://agenttimes.live/ask?q=singapore+startup+funding"
curl -s "https://agenttimes.live/ask?q=climate+policy+europe&limit=20"
curl -s "https://agenttimes.live/ask?q=remote+devops+jobs"
```

| Param | Default | Description |
|-------|---------|-------------|
| q | required | Search query. Replace spaces with `+` |
| limit | 10 | Max results (1-50) |

**Response:**
```json
{
  "success": true,
  "query": "bitcoin etf",
  "source": "news_db",
  "count": 10,
  "results": [
    {
      "title": "SEC Approves Spot Bitcoin ETF Applications",
      "url": "https://example.com/article",
      "summary": "The Securities and Exchange Commission has approved...",
      "category": "crypto",
      "published": "Mon, 24 Mar 2026 14:30:00 +0000",
      "sentiment": "bullish",
      "sentiment_score": 0.75,
      "credibility": "high",
      "entities": {
        "companies": ["SEC"],
        "tickers": [],
        "crypto": ["BTC"],
        "people": []
      },
      "tags": ["markets"]
    }
  ]
}
```

When `/ask` finds fewer than 3 results, it automatically falls back to web search. When 0 results, it returns `suggestions` with related categories and terms.

## /trending — Trending Stories (FREE)

Detects stories being covered by multiple independent sources.

```bash
curl -s "https://agenttimes.live/trending?hours=12"
```

| Param | Default | Description |
|-------|---------|-------------|
| hours | 6 | Lookback window (1-48) |
| min_sources | 3 | Minimum sources covering the same story |
| limit | 20 | Max trending clusters |

## /subscribe — Topic Alerts (FREE)

Get webhook notifications when new articles matching your query arrive.

```bash
curl -s -X POST https://agenttimes.live/subscribe \
  -H "Content-Type: application/json" \
  -d '{"query":"bitcoin regulation","category":"crypto","webhook":"https://your-agent.com/notify"}'
```

Response: `{"success":true,"subscription_id":1,"secret":"abc123...","note":"Save this secret — you need it to unsubscribe."}`

Unsubscribe (requires the secret from subscribe response):
```bash
curl -s -X DELETE "https://agenttimes.live/subscribe/1?secret=abc123..."
```

Your webhook receives a POST with matching articles every time new ones arrive (checked every 5 minutes).

**Security:** Webhook must be a public HTTPS URL. Localhost, private IPs, and cloud metadata endpoints are blocked.

## /news — Category Browsing (FREE)

Browse and filter articles by category with optional tag, date range, and keyword filters.

```bash
# All crypto news
curl -s "https://agenttimes.live/news?category=crypto&limit=10"

# Asian news only
curl -s "https://agenttimes.live/news?category=world&tag=asia"

# Singapore news
curl -s "https://agenttimes.live/news?category=world&tag=singapore"

# Gaming news
curl -s "https://agenttimes.live/news?category=entertainment&tag=gaming"

# Jobs in tech
curl -s "https://agenttimes.live/news?category=business&tag=jobs"

# AI news from last 2 days
curl -s "https://agenttimes.live/news?category=ai&since=2026-03-22"

# Search within a category
curl -s "https://agenttimes.live/news?category=tech&q=rust+programming"
```

| Param | Default | Description |
|-------|---------|-------------|
| category | required | One of 14 categories, or `all` |
| tag | — | Subcategory/country filter (see table below) |
| limit | 20 | Max results (1-1000) |
| q | — | Keyword filter within category |
| since | — | ISO date — articles after this time |
| before | — | ISO date — articles before this time |
| dedup | true | Deduplicate similar headlines |

## /search — Web Search ($0.001)

Search the open web via 70+ engines when you need non-news results.

```bash
curl -s "https://agenttimes.live/search?q=how+to+deploy+docker"
```

| Param | Default | Description |
|-------|---------|-------------|
| q | required | Search query |
| limit | 5 | Max results (1-50) |
| category | general | general, news, images, videos, science, files |

## Categories + Tags

14 categories. Use `&tag=` on `/news` to filter by subcategory, country, or region.

| Category | What's in it | Available tags |
|----------|-------------|----------------|
| **world** | International news, geopolitics, diplomacy | `asia`, `europe`, `middleeast`, `africa`, `india`, `latam`, `oceania`, `defense`, `government` + 50 country tags (see below) |
| **politics** | Elections, policy, legislation, regulation | — |
| **business** | Finance, commerce, employment, markets | `finance`, `startups`, `jobs`, `marketing`, `ecommerce`, `fintech`, `realestate`, `legal`, `supplychain` |
| **tech** | Software, hardware, engineering, data | `devtools`, `engineering`, `mobile`, `datascience`, `telecom` |
| **ai** | Artificial intelligence, machine learning | `robotics`, `research` |
| **crypto** | Cryptocurrency, blockchain, DeFi | `web3`, `defi`, `bitcoin`, `markets` |
| **science** | Research, discoveries, academia | `biotech`, `space`, `research` |
| **health** | Medicine, wellness, public health | `fitness` |
| **energy** | Energy, climate change, environment | `climate`, `environment`, `agriculture` |
| **security** | Cybersecurity, infosec, threats | — |
| **sports** | All sports coverage | — |
| **entertainment** | Film, music, gaming, TV, culture | `gaming`, `film`, `music` |
| **lifestyle** | Food, travel, fashion, daily life | `food`, `travel`, `fashion`, `design`, `education` |
| **automotive** | Vehicles, EVs, transportation, logistics | `shipping` |

### Country Tags (use with `category=world&tag=COUNTRY`)

**Asia:** `singapore`, `malaysia`, `philippines`, `indonesia`, `thailand`, `vietnam`, `japan`, `korea`, `china`, `taiwan`, `hongkong`, `india`, `pakistan`, `bangladesh`

**Europe:** `uk`, `germany`, `france`, `italy`, `spain`, `netherlands`, `sweden`, `norway`, `denmark`, `finland`, `ireland`, `poland`, `austria`, `switzerland`, `iceland`, `romania`, `hungary`, `greece`, `serbia`, `ukraine`, `russia`

**Middle East:** `israel`, `turkey`, `iran`, `saudiarabia`, `uae`, `qatar`

**Africa:** `nigeria`, `southafrica`, `kenya`, `ghana`, `ethiopia`

**Latin America:** `brazil`, `mexico`, `argentina`, `colombia`, `chile`, `peru`

**Oceania:** `australia`, `newzealand`

**North America:** `usa`, `canada`

## Response Format

**News results** (`/ask`, `/news`, `/trending`) return:
```json
{"success": true, "count": N, "results": [...]}
```

**Weather** (`/ask?q=weather+tokyo`) returns: `{"source": "open-meteo", "location": "...", "current": {...}, "forecast": [...]}`

**Crypto prices** (`/ask?q=bitcoin+price`) returns: `{"source": "pyth", "prices": [{"symbol": "BTC", "price": 66000}]}`

Check the `source` field to determine response shape: `news_db`, `combined`, `open-meteo`, `nea`, or `pyth`.

Each article result contains:
- `title` — headline
- `url` — link to original article
- `summary` — first 200 chars of content
- `category` — one of 14 categories
- `source_feed` — RSS feed URL
- `published` — publication date
- `timestamp` — Unix timestamp (ms)
- `sentiment` — "bullish", "bearish", or "neutral"
- `sentiment_score` — -1.0 (very bearish) to 1.0 (very bullish)
- `credibility` — "high" (tier 1 outlets), "medium" (established), or "unknown"
- `entities` — `{people, companies, tickers, crypto, locations}` extracted by GLiNER + dictionary matching
- `tags` — subcategory and country tags for this article

Errors: `{"success": false, "error": "Missing param: q"}`

## Payment (x402)

The `/search` endpoint uses the [x402](https://www.x402.org) protocol. Your agent pays **$0.001 USDC** per request on Base network — no accounts, no subscriptions, just micropayments. All other endpoints are free.

Wallet: `0x536Eafe011786599d9a656D62e2aeAFcE06a96D1` (Base)

## Other Free Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /news/categories` | List all 14 categories with counts |
| `GET /stats` | Database statistics |
| `GET /feeds/health?category=CAT` | Per-feed health and status |
| `GET /health` | Health check |
| `GET /info` | Full API docs (JSON for agents, HTML for browsers) |

## Tips for Best Results

1. **Always start with `/ask`** — it's free, semantic, and handles fallback automatically
2. **Country news:** Use `/ask?q=japan+earthquake` not `/news?category=japan` (no country categories)
3. **Filter by country:** Use `/news?category=world&tag=singapore` for source-based filtering
4. **Sentiment analysis:** Check `sentiment_score` to gauge market/public mood on a topic
5. **Entity detection:** Use `entities.tickers` and `entities.crypto` to find articles mentioning specific assets
6. **Monitor breaking news:** POST to `/subscribe` with a webhook URL to get real-time alerts
7. **Parse JSON directly** — don't pipe to `jq` (may not be installed)
8. **Replace spaces with `+`** in all query strings
9. **Check `suggestions`** when 0 results — it recommends related categories and search terms
10. **Credibility matters:** Sort by `credibility` to prioritize tier 1 sources (Reuters, BBC, AP) over unknown blogs
