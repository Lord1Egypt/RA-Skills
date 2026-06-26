---
name: camino-query
description: "Search for places using natural language with Camino AI's location intelligence API. Returns relevant results with coordinates, distances, and metadata. Use when you need to find real-world locations like restaurants, shops, landmarks, or any point of interest."
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## Installation

**Companion Skills**: This is part of the Camino AI location intelligence suite. Install all available skills (camino-query, camino-places, camino-relationship, camino-context, camino-route, camino-journey, camino-real-estate, camino-hotel-finder, camino-ev-charger, camino-school-finder, camino-parking-finder, camino-fitness-finder, camino-safety-checker, camino-travel-planner) for comprehensive coverage.

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill camino-query
```

**Via clawhub:**
```bash
npx clawhub@latest install camino-query
# or: pnpm dlx clawhub@latest install camino-query
# or: bunx clawhub@latest install camino-query
```

# Query - Natural Language Place Search

Search for places using natural language. The AI automatically generates coordinates for known locations when not provided.

## Setup

These skills shell out to `curl` and authenticate via the `CAMINO_API_KEY` environment variable. Sign up at [https://app.getcamino.ai/skills/activate](https://app.getcamino.ai/skills/activate) for 100 free calls/month and an API key.

**Add your key to Claude Code:**

Add to your `~/.claude/settings.json`:

```json
{
  "env": {
    "CAMINO_API_KEY": "your-api-key-here"
  }
}
```

Restart Claude Code.

**Alternative — pay-per-request via [x402](https://x402.org):** Camino's paid endpoints also accept HTTP 402 payments in USDC on Base ($0.001/request) from any x402-capable client, with no signup or API key. These skills don't use this path; it's for agents and clients that speak x402 natively.

## Usage

### Via Shell Script

```bash
# Search for coffee shops near Times Square
./scripts/query.sh '{"query": "coffee shops near Times Square", "limit": 5}'

# Search with specific coordinates
./scripts/query.sh '{"query": "quiet cafes with wifi", "lat": 40.7589, "lon": -73.9851, "radius": 500}'

# Get AI-generated answer with results
./scripts/query.sh '{"query": "best pizza in Manhattan", "answer": true, "rank": true}'
```

### Via curl

```bash
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/query?query=coffee+shops+near+Times+Square&limit=5"
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | Yes* | - | Natural language query (e.g., "coffee shops near Times Square") |
| lat | float | No | - | Latitude for search center. AI generates if omitted for known locations. |
| lon | float | No | - | Longitude for search center. AI generates if omitted for known locations. |
| radius | int | No | 1000 | Search radius in meters (100-50000) |
| rank | bool | No | true | Use AI to rank results by relevance |
| limit | int | No | 20 | Maximum results (1-100) |
| offset | int | No | 0 | Pagination offset |
| answer | bool | No | false | Generate human-readable summary |
| time | string | No | - | Temporal query: "2020-01-01", "2020..", or "2020..2024" |
| osm_ids | string | No | - | Comma-separated OSM IDs (e.g., "node/123,way/456") |
| mode | string | No | "basic" | "basic" (OSM only) or "advanced" (web enrichment) |
| engine | string | No | auto | Backend: "overture" (BigQuery, default) or "osm" (Overpass). Auto-routes to "osm" when `osm_ids` or `time` are set. |

*Either `query` or `osm_ids` is required.

## Response Format

```json
{
  "query": "quiet coffee shops with wifi",
  "results": [
    {
      "name": "Blue Bottle Coffee",
      "lat": 40.7601,
      "lon": -73.9847,
      "type": "cafe",
      "distance_m": 150,
      "relevance_score": 0.95,
      "address": "..."
    }
  ],
  "ai_ranked": true,
  "pagination": {
    "total_results": 23,
    "limit": 5,
    "offset": 0,
    "has_more": true
  },
  "answer": "I found several quiet coffee shops with wifi near Times Square..."
}
```

## Examples

### Find nearby restaurants
```bash
./scripts/query.sh '{"query": "Italian restaurants", "lat": 40.7128, "lon": -74.0060, "limit": 10}'
```

### Search with AI answer
```bash
./scripts/query.sh '{"query": "best brunch spots in Brooklyn", "answer": true}'
```

### Historical data query
```bash
./scripts/query.sh '{"query": "restaurants", "lat": 40.7589, "lon": -73.9851, "time": "2020-01-01"}'
```

## Best Practices

- For known locations (cities, landmarks), you can omit lat/lon and let the AI generate coordinates
- Use `rank: true` for more relevant results when searching by attributes (e.g., "quiet", "cheap")
- Enable `answer: true` when you need a natural language summary of results
- Use `mode: "advanced"` for richer place data from web sources
- Keep queries descriptive but concise for best AI interpretation
