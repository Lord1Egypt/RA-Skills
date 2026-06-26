---
name: camino-relationship
description: "Calculate spatial relationships between two points including distance, direction, travel time, and human-readable descriptions. Use when you need to understand how locations relate to each other."
metadata: {"clawdbot":{"emoji":"📐","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## Installation

**Companion Skills**: This is part of the Camino AI location intelligence suite. Install all available skills (camino-query, camino-places, camino-relationship, camino-context, camino-route, camino-journey, camino-real-estate, camino-hotel-finder, camino-ev-charger, camino-school-finder, camino-parking-finder, camino-fitness-finder, camino-safety-checker, camino-travel-planner) for comprehensive coverage.

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill camino-relationship
```

**Via clawhub:**
```bash
npx clawhub@latest install camino-relationship
# or: pnpm dlx clawhub@latest install camino-relationship
# or: bunx clawhub@latest install camino-relationship
```

# Relationship - Spatial Calculations

Calculate distance, direction, travel time, and human-readable descriptions between two points.

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
# Calculate relationship between two points
./scripts/relationship.sh '{
  "start": {"lat": 40.7128, "lon": -74.0060},
  "end": {"lat": 40.7589, "lon": -73.9851}
}'

# Include specific calculations
./scripts/relationship.sh '{
  "start": {"lat": 40.7128, "lon": -74.0060},
  "end": {"lat": 40.7589, "lon": -73.9851},
  "include": ["distance", "direction", "travel_time", "description"]
}'
```

### Via curl

```bash
curl -X POST -H "X-API-Key: $CAMINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"start": {"lat": 40.7128, "lon": -74.0060}, "end": {"lat": 40.7589, "lon": -73.9851}}' \
  "https://api.getcamino.ai/relationship"
```

## Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| start | object | Yes | Starting point with lat/lon |
| end | object | Yes | Ending point with lat/lon |
| include | array | No | What to include: distance, direction, travel_time, description |

## Response Format

```json
{
  "distance": {
    "meters": 5420,
    "kilometers": 5.42,
    "miles": 3.37
  },
  "direction": {
    "bearing": 42,
    "cardinal": "NE",
    "description": "northeast"
  },
  "travel_time": {
    "walking_minutes": 68,
    "driving_minutes": 15,
    "cycling_minutes": 22
  },
  "description": "5.4 km northeast, about 15 minutes by car"
}
```

## Examples

### Simple distance check
```bash
./scripts/relationship.sh '{
  "start": {"lat": 51.5074, "lon": -0.1278},
  "end": {"lat": 48.8566, "lon": 2.3522}
}'
```

### Get only distance and direction
```bash
./scripts/relationship.sh '{
  "start": {"lat": 40.7128, "lon": -74.0060},
  "end": {"lat": 40.7589, "lon": -73.9851},
  "include": ["distance", "direction"]
}'
```

## Use Cases

- **Proximity checks**: Determine if two locations are within a certain distance
- **Direction guidance**: Provide cardinal direction context (north, southeast, etc.)
- **Travel planning**: Estimate travel times for different transport modes
- **Location context**: Generate human-readable descriptions of spatial relationships
