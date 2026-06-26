---
name: camino-ev-charger
description: "Find EV charging stations along a route or near a destination using Camino AI's location intelligence with OpenStreetMap data."
metadata: {"clawdbot":{"emoji":"⚡","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## Installation

**Companion Skills**: This is part of the Camino AI location intelligence suite. Install all available skills (camino-query, camino-places, camino-relationship, camino-context, camino-route, camino-journey, camino-real-estate, camino-hotel-finder, camino-ev-charger, camino-school-finder, camino-parking-finder, camino-fitness-finder, camino-safety-checker, camino-travel-planner) for comprehensive coverage.

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill camino-ev-charger
```

**Via clawhub:**
```bash
npx clawhub@latest install camino-ev-charger
# or: pnpm dlx clawhub@latest install camino-ev-charger
# or: bunx clawhub@latest install camino-ev-charger
```

# EV Charger Finder

Find EV charging stations along a route or near a destination. Uses OpenStreetMap data to locate charging infrastructure with AI-powered ranking.

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
# Find EV chargers near coordinates
./scripts/ev-charger.sh '{"lat": 34.0522, "lon": -118.2437, "radius": 5000}'

# Find chargers with custom query
./scripts/ev-charger.sh '{"query": "Tesla Supercharger stations", "lat": 37.7749, "lon": -122.4194}'

# Find chargers in a city
./scripts/ev-charger.sh '{"query": "EV charging stations in Austin Texas", "limit": 20}'
```

### Via curl

```bash
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/query?query=EV+charging+stations&lat=34.0522&lon=-118.2437&radius=5000&rank=true"
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | No | "EV charging stations" | Search query (override for specific charger types) |
| lat | float | No | - | Latitude for search center. AI generates if omitted for known locations. |
| lon | float | No | - | Longitude for search center. AI generates if omitted for known locations. |
| radius | int | No | 5000 | Search radius in meters (larger default for EV chargers) |
| limit | int | No | 20 | Maximum results (1-100) |

## Response Format

```json
{
  "query": "EV charging stations",
  "results": [
    {
      "name": "ChargePoint Station",
      "lat": 34.0530,
      "lon": -118.2450,
      "type": "charging_station",
      "distance_m": 200,
      "relevance_score": 0.94,
      "address": "..."
    }
  ],
  "ai_ranked": true,
  "pagination": {
    "total_results": 12,
    "limit": 20,
    "offset": 0,
    "has_more": false
  }
}
```

## Examples

### Find chargers near a highway exit
```bash
./scripts/ev-charger.sh '{"query": "EV charging near Interstate 5", "lat": 34.0522, "lon": -118.2437, "radius": 10000}'
```

### Find Tesla Superchargers
```bash
./scripts/ev-charger.sh '{"query": "Tesla Supercharger", "lat": 37.3861, "lon": -122.0839}'
```

### Find chargers near a hotel
```bash
./scripts/ev-charger.sh '{"query": "EV charging stations near downtown Denver", "radius": 3000}'
```

## Best Practices

- Use a larger radius (5000-10000m) since EV chargers are less densely distributed than other amenities
- Include the charger network name in the query if you need a specific one (e.g., "Tesla Supercharger", "ChargePoint")
- Combine with the `camino-route` skill to plan charging stops along a driving route
- Combine with the `camino-relationship` skill to check distances from chargers to your destination
- For road trip planning, use the `camino-travel-planner` skill with charging waypoints
