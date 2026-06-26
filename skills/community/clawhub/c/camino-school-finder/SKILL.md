---
name: camino-school-finder
description: "Locate elementary schools, high schools, and universities near any address using Camino AI's location intelligence with AI-powered ranking."
metadata: {"clawdbot":{"emoji":"🏫","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## Installation

**Companion Skills**: This is part of the Camino AI location intelligence suite. Install all available skills (camino-query, camino-places, camino-relationship, camino-context, camino-route, camino-journey, camino-real-estate, camino-hotel-finder, camino-ev-charger, camino-school-finder, camino-parking-finder, camino-fitness-finder, camino-safety-checker, camino-travel-planner) for comprehensive coverage.

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill camino-school-finder
```

**Via clawhub:**
```bash
npx clawhub@latest install camino-school-finder
# or: pnpm dlx clawhub@latest install camino-school-finder
# or: bunx clawhub@latest install camino-school-finder
```

# School Finder

Locate elementary schools, high schools, and universities near any location. Uses OpenStreetMap data with AI-powered ranking to find educational institutions.

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
# Find schools near coordinates
./scripts/school-finder.sh '{"lat": 40.7589, "lon": -73.9851, "radius": 1600}'

# Search for specific school types
./scripts/school-finder.sh '{"query": "elementary schools", "lat": 37.7749, "lon": -122.4194}'

# Find universities in a city
./scripts/school-finder.sh '{"query": "universities in Boston", "limit": 15}'
```

### Via curl

```bash
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/query?query=schools&lat=40.7589&lon=-73.9851&radius=2000&rank=true"
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | No | "schools" | Search query (override for specific school types) |
| lat | float | No | - | Latitude for search center. AI generates if omitted for known locations. |
| lon | float | No | - | Longitude for search center. AI generates if omitted for known locations. |
| radius | int | No | 2000 | Search radius in meters |
| limit | int | No | 20 | Maximum results (1-100) |

## Response Format

```json
{
  "query": "schools",
  "results": [
    {
      "name": "PS 234 Independence School",
      "lat": 40.7175,
      "lon": -74.0131,
      "type": "school",
      "distance_m": 320,
      "relevance_score": 0.91,
      "address": "..."
    }
  ],
  "ai_ranked": true,
  "pagination": {
    "total_results": 18,
    "limit": 20,
    "offset": 0,
    "has_more": false
  }
}
```

## Examples

### Find elementary schools near a home
```bash
./scripts/school-finder.sh '{"query": "elementary schools", "lat": 40.7128, "lon": -74.0060, "radius": 1600}'
```

### Find high schools in a suburb
```bash
./scripts/school-finder.sh '{"query": "high schools in Naperville Illinois", "limit": 10}'
```

### Find universities near downtown
```bash
./scripts/school-finder.sh '{"query": "universities and colleges", "lat": 42.3601, "lon": -71.0589, "radius": 5000}'
```

## Best Practices

- Use 1600m radius (approximately 1 mile) for elementary school searches near a home
- Use larger radius (3000-5000m) for high school and university searches
- Specify school type in the query for more targeted results (e.g., "elementary schools", "high schools", "universities")
- Combine with the `camino-real-estate` skill for a complete neighborhood evaluation
- Combine with the `camino-route` skill to calculate walking or driving times from home to school
- Combine with the `camino-relationship` skill to check distances between home and multiple schools
