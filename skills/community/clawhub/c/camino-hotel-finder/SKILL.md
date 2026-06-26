---
name: camino-hotel-finder
description: "Search for hotels, hostels, and lodging near landmarks, conference venues, or neighborhoods using Camino AI's location intelligence with AI-powered ranking."
metadata: {"clawdbot":{"emoji":"🏨","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## Installation

**Companion Skills**: This is part of the Camino AI location intelligence suite. Install all available skills (camino-query, camino-places, camino-relationship, camino-context, camino-route, camino-journey, camino-real-estate, camino-hotel-finder, camino-ev-charger, camino-school-finder, camino-parking-finder, camino-fitness-finder, camino-safety-checker, camino-travel-planner) for comprehensive coverage.

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill camino-hotel-finder
```

**Via clawhub:**
```bash
npx clawhub@latest install camino-hotel-finder
# or: pnpm dlx clawhub@latest install camino-hotel-finder
# or: bunx clawhub@latest install camino-hotel-finder
```

# Hotel Finder

Search for hotels, hostels, and lodging near landmarks, conference venues, or neighborhoods. Results are AI-ranked for relevance and include a human-readable summary.

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
# Search for hotels near a landmark
./scripts/hotel-finder.sh '{"query": "hotels near the Eiffel Tower", "limit": 5}'

# Search with specific coordinates
./scripts/hotel-finder.sh '{"query": "boutique hotels", "lat": 40.7589, "lon": -73.9851, "radius": 1000}'

# Search for hostels in a city
./scripts/hotel-finder.sh '{"query": "hostels in Barcelona", "limit": 10}'
```

### Via curl

```bash
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/query?query=hotels+near+the+Eiffel+Tower&limit=5&rank=true&answer=true"
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | Yes | - | Natural language query (e.g., "hotels near Eiffel Tower") |
| lat | float | No | - | Latitude for search center. AI generates if omitted for known locations. |
| lon | float | No | - | Longitude for search center. AI generates if omitted for known locations. |
| radius | int | No | 2000 | Search radius in meters |
| limit | int | No | 10 | Maximum results (1-100) |

## Response Format

```json
{
  "query": "hotels near the Eiffel Tower",
  "results": [
    {
      "name": "Hotel du Champ de Mars",
      "lat": 48.8555,
      "lon": 2.3005,
      "type": "hotel",
      "distance_m": 350,
      "relevance_score": 0.92,
      "address": "..."
    }
  ],
  "ai_ranked": true,
  "pagination": {
    "total_results": 15,
    "limit": 5,
    "offset": 0,
    "has_more": true
  },
  "answer": "I found several hotels near the Eiffel Tower. The closest is..."
}
```

## Examples

### Hotels near a conference venue
```bash
./scripts/hotel-finder.sh '{"query": "hotels near Moscone Center San Francisco", "limit": 10}'
```

### Budget hostels in a city
```bash
./scripts/hotel-finder.sh '{"query": "hostels in Amsterdam", "radius": 3000, "limit": 15}'
```

### Lodging near an airport
```bash
./scripts/hotel-finder.sh '{"query": "hotels near JFK airport", "radius": 5000}'
```

## Best Practices

- Include the landmark or neighborhood in your query for best results without coordinates
- Use larger radius (3000-5000m) for suburban or airport searches
- Use smaller radius (500-1000m) for dense city centers
- Combine with the `camino-route` skill to calculate travel times from hotels to your destination
- Combine with the `camino-context` skill for a full neighborhood assessment around each hotel
- The AI ranking prioritizes proximity and relevance to your query intent
