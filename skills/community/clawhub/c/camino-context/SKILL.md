---
name: camino-context
description: "Get comprehensive context about a location including nearby places, area description, and optional weather. Use when you need to understand what's around a location or provide location-aware recommendations."
metadata: {"clawdbot":{"emoji":"📍","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## Installation

**Companion Skills**: This is part of the Camino AI location intelligence suite. Install all available skills (camino-query, camino-places, camino-relationship, camino-context, camino-route, camino-journey, camino-real-estate, camino-hotel-finder, camino-ev-charger, camino-school-finder, camino-parking-finder, camino-fitness-finder, camino-safety-checker, camino-travel-planner) for comprehensive coverage.

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill camino-context
```

**Via clawhub:**
```bash
npx clawhub@latest install camino-context
# or: pnpm dlx clawhub@latest install camino-context
# or: bunx clawhub@latest install camino-context
```

# Context - Location Analysis

Get comprehensive context about a location including nearby places, area description, and optional weather.

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
# Get context about a location
./scripts/context.sh '{
  "location": {"lat": 40.7589, "lon": -73.9851},
  "radius": 500
}'

# With specific context for tailored insights
./scripts/context.sh '{
  "location": {"lat": 40.7589, "lon": -73.9851},
  "radius": 500,
  "context": "lunch options"
}'

# Include weather data
./scripts/context.sh '{
  "location": {"lat": 40.7589, "lon": -73.9851},
  "include_weather": true,
  "weather_forecast": "hourly"
}'
```

### Via curl

```bash
curl -X POST -H "X-API-Key: $CAMINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": {"lat": 40.7589, "lon": -73.9851}, "radius": 500, "context": "lunch options"}' \
  "https://api.getcamino.ai/context"
```

## Parameters

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| location | object | Yes | - | Coordinate with lat/lon |
| radius | int | No | 500 | Search radius in meters |
| context | string | No | - | Context for tailored insights (e.g., "outdoor dining") |
| time | string | No | - | Temporal query format |
| include_weather | bool | No | false | Include weather data |
| weather_forecast | string | No | "daily" | "daily" or "hourly" |

## Response Format

```json
{
  "area_description": "Busy commercial district in Midtown Manhattan...",
  "relevant_places": {
    "restaurants": [...],
    "cafes": [...],
    "transit": [...]
  },
  "location": {"lat": 40.7589, "lon": -73.9851},
  "search_radius": 500,
  "total_places_found": 47,
  "context_insights": "For lunch, you have many options including..."
}
```

## Examples

### Tourist context
```bash
./scripts/context.sh '{
  "location": {"lat": 48.8584, "lon": 2.2945},
  "radius": 1000,
  "context": "tourist visiting Paris"
}'
```

### Business meeting location
```bash
./scripts/context.sh '{
  "location": {"lat": 40.7589, "lon": -73.9851},
  "radius": 500,
  "context": "business meeting",
  "include_weather": true
}'
```

### Outdoor activity planning
```bash
./scripts/context.sh '{
  "location": {"lat": 37.7749, "lon": -122.4194},
  "context": "outdoor activities",
  "include_weather": true,
  "weather_forecast": "hourly"
}'
```

## Use Cases

- **Trip planning**: Understand what's around a destination before visiting
- **Meeting locations**: Find suitable venues for different types of meetings
- **Local recommendations**: Provide context-aware suggestions based on user needs
- **Weather-aware planning**: Include weather data for outdoor activity planning
