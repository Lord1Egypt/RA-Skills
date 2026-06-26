---
name: camino-fitness-finder
description: "Search for gyms, yoga studios, swimming pools, and sports facilities using Camino AI's location intelligence with AI-powered ranking."
metadata: {"clawdbot":{"emoji":"💪","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## Installation

**Companion Skills**: This is part of the Camino AI location intelligence suite. Install all available skills (camino-query, camino-places, camino-relationship, camino-context, camino-route, camino-journey, camino-real-estate, camino-hotel-finder, camino-ev-charger, camino-school-finder, camino-parking-finder, camino-fitness-finder, camino-safety-checker, camino-travel-planner) for comprehensive coverage.

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill camino-fitness-finder
```

**Via clawhub:**
```bash
npx clawhub@latest install camino-fitness-finder
# or: pnpm dlx clawhub@latest install camino-fitness-finder
# or: bunx clawhub@latest install camino-fitness-finder
```

# Gym & Fitness Finder

Search for gyms, yoga studios, swimming pools, and sports facilities near any location. Uses OpenStreetMap data with AI-powered ranking to find the most relevant fitness options.

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
# Find gyms and fitness centers nearby
./scripts/fitness-finder.sh '{"lat": 40.7589, "lon": -73.9851}'

# Search for yoga studios specifically
./scripts/fitness-finder.sh '{"query": "yoga studios", "lat": 30.2672, "lon": -97.7431}'

# Find swimming pools in a city
./scripts/fitness-finder.sh '{"query": "swimming pools in Chicago", "limit": 10}'
```

### Via curl

```bash
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/query?query=gyms+yoga+studios+fitness+centers&lat=40.7589&lon=-73.9851&radius=1500&rank=true"
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | No | "gyms yoga studios fitness centers" | Search query (override for specific facility types) |
| lat | float | No | - | Latitude for search center. AI generates if omitted for known locations. |
| lon | float | No | - | Longitude for search center. AI generates if omitted for known locations. |
| radius | int | No | 1500 | Search radius in meters |
| limit | int | No | 15 | Maximum results (1-100) |

## Response Format

```json
{
  "query": "gyms yoga studios fitness centers",
  "results": [
    {
      "name": "Equinox Fitness Club",
      "lat": 40.7595,
      "lon": -73.9845,
      "type": "fitness_centre",
      "distance_m": 80,
      "relevance_score": 0.96,
      "address": "..."
    }
  ],
  "ai_ranked": true,
  "pagination": {
    "total_results": 22,
    "limit": 15,
    "offset": 0,
    "has_more": true
  }
}
```

## Examples

### Find yoga studios
```bash
./scripts/fitness-finder.sh '{"query": "yoga studios", "lat": 30.2672, "lon": -97.7431}'
```

### Find gyms near a hotel
```bash
./scripts/fitness-finder.sh '{"query": "gyms and fitness centers near Times Square", "radius": 1000}'
```

### Find sports facilities
```bash
./scripts/fitness-finder.sh '{"query": "tennis courts and sports facilities", "lat": 34.0522, "lon": -118.2437, "radius": 3000}'
```

## Best Practices

- Use specific facility types in the query for targeted results (e.g., "yoga studios", "CrossFit gyms", "swimming pools")
- Use 1500m radius for urban areas, increase to 3000m for suburban locations
- Combine with the `camino-route` skill to calculate walking or cycling times to the gym
- Combine with the `camino-real-estate` skill when evaluating a neighborhood's fitness options
- Combine with the `camino-relationship` skill to compare distances between multiple facilities
- For travelers, combine with `camino-hotel-finder` to find lodging near fitness facilities
