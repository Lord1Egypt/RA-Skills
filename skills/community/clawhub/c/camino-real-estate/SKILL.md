---
name: camino-real-estate
description: "Evaluate any address for home buyers and renters. Get nearby schools, transit, grocery stores, parks, restaurants, and walkability using Camino AI's location intelligence."
metadata: {"clawdbot":{"emoji":"🏠","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## Installation

**Companion Skills**: This is part of the Camino AI location intelligence suite. Install all available skills (camino-query, camino-places, camino-relationship, camino-context, camino-route, camino-journey, camino-real-estate, camino-hotel-finder, camino-ev-charger, camino-school-finder, camino-parking-finder, camino-fitness-finder, camino-safety-checker, camino-travel-planner) for comprehensive coverage.

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill camino-real-estate
```

**Via clawhub:**
```bash
npx clawhub@latest install camino-real-estate
# or: pnpm dlx clawhub@latest install camino-real-estate
# or: bunx clawhub@latest install camino-real-estate
```

# Real Estate Scout

Evaluate any address or location for home buyers and renters. Combines location context analysis with targeted amenity searches to surface nearby schools, transit, grocery stores, parks, restaurants, and walkability insights.

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
# Evaluate an address
./scripts/real-estate.sh '{"address": "742 Evergreen Terrace, Springfield", "radius": 1000}'

# Evaluate with coordinates
./scripts/real-estate.sh '{"location": {"lat": 40.7589, "lon": -73.9851}, "radius": 1500}'

# Evaluate with smaller radius for dense urban area
./scripts/real-estate.sh '{"address": "350 Fifth Avenue, New York, NY", "radius": 500}'
```

### Via curl

```bash
# Step 1: Geocode the address
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/query?query=742+Evergreen+Terrace+Springfield&limit=1"

# Step 2: Get context with real estate focus
curl -X POST -H "X-API-Key: $CAMINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": {"lat": 40.7589, "lon": -73.9851}, "radius": 1000, "context": "real estate evaluation: schools, transit, grocery, parks, restaurants, walkability"}' \
  "https://api.getcamino.ai/context"
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| address | string | No* | - | Street address to evaluate (geocoded automatically) |
| location | object | No* | - | Coordinate with lat/lon to evaluate |
| radius | int | No | 1000 | Search radius in meters around the location |

*Either `address` or `location` is required.

## Response Format

```json
{
  "area_description": "Residential neighborhood in Midtown Manhattan with excellent transit access...",
  "relevant_places": {
    "schools": [...],
    "transit": [...],
    "grocery": [...],
    "parks": [...],
    "restaurants": [...]
  },
  "location": {"lat": 40.7589, "lon": -73.9851},
  "search_radius": 1000,
  "total_places_found": 63,
  "context_insights": "This area offers strong walkability with multiple grocery options within 500m..."
}
```

## Examples

### Evaluate a suburban address
```bash
./scripts/real-estate.sh '{"address": "123 Oak Street, Palo Alto, CA", "radius": 1500}'
```

### Evaluate an urban apartment
```bash
./scripts/real-estate.sh '{"location": {"lat": 40.7484, "lon": -73.9857}, "radius": 800}'
```

### Evaluate a neighborhood by coordinates
```bash
./scripts/real-estate.sh '{"location": {"lat": 37.7749, "lon": -122.4194}, "radius": 2000}'
```

## Best Practices

- Use `address` for street addresses; the script will geocode them automatically
- Use `location` with lat/lon when you already have coordinates
- Start with a 1000m radius for suburban areas, 500m for dense urban areas
- Combine with the `camino-relationship` skill to calculate commute distances to workplaces
- Combine with the `camino-route` skill to estimate travel times to key destinations
- Use the `camino-school-finder` skill for more detailed school searches
