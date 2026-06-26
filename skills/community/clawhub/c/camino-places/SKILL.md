---
name: camino-places
description: "Locate places using flexible query formats - free-form search or structured address components. Returns coordinates, addresses, and optional street-level photos. Use for geocoding addresses or finding specific named places."
metadata: {"clawdbot":{"emoji":"📌","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## Installation

**Companion Skills**: This is part of the Camino AI location intelligence suite. Install all available skills (camino-query, camino-places, camino-relationship, camino-context, camino-route, camino-journey, camino-real-estate, camino-hotel-finder, camino-ev-charger, camino-school-finder, camino-parking-finder, camino-fitness-finder, camino-safety-checker, camino-travel-planner) for comprehensive coverage.

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill camino-places
```

**Via clawhub:**
```bash
npx clawhub@latest install camino-places
# or: pnpm dlx clawhub@latest install camino-places
# or: bunx clawhub@latest install camino-places
```

# Places - Flexible Place Lookup

Locate places using free-form queries or structured address components. Supports geocoding, place lookup, and optional street-level imagery.

## Places vs Query

| Feature | `/camino-places` | `/camino-query` |
|---------|-----------|----------|
| Method | POST | GET |
| Input | Free-form OR structured address | Natural language with context |
| Coordinates | Returns them (geocoding) | Can auto-generate for search center |
| AI Ranking | No | Yes |
| Photos | Optional street-level imagery | No |
| Best For | "Eiffel Tower", address lookup | "quiet cafes near Times Square" |

**Use `/camino-places`** for geocoding addresses or finding specific named places.
**Use `/camino-query`** for natural language queries with AI ranking.

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
# Free-form search for a landmark
./scripts/places.sh '{"query": "Eiffel Tower"}'

# Search with street-level photos
./scripts/places.sh '{"query": "Empire State Building", "include_photos": true}'

# Structured address search
./scripts/places.sh '{"street": "1600 Pennsylvania Avenue", "city": "Washington", "state": "DC", "country": "USA"}'

# Search by city
./scripts/places.sh '{"city": "San Francisco", "state": "California", "limit": 5}'
```

### Via curl (direct API calls)

The skill is named `camino-places` but calls the `/search` API endpoint. For direct API calls:

```bash
curl -X POST -H "X-API-Key: $CAMINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "Eiffel Tower", "include_photos": true}' \
  "https://api.getcamino.ai/search"
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | No* | - | Free-form search (e.g., "Eiffel Tower", "Central Park") |
| amenity | string | No | - | Amenity/POI type |
| street | string | No | - | Street name and number |
| city | string | No | - | City name |
| county | string | No | - | County name |
| state | string | No | - | State or province |
| country | string | No | - | Country name or code |
| postalcode | string | No | - | Postal/ZIP code |
| limit | int | No | 10 | Maximum results (1-50) |
| include_photos | bool | No | false | Include street-level imagery |
| photo_radius | int | No | 100 | Photo search radius in meters (10-500) |
| mode | string | No | "basic" | "basic" or "advanced" search depth |

*Either `query` or at least one address component is required.

## Response Format

```json
[
  {
    "display_name": "Eiffel Tower, 5 Avenue Anatole France, 75007 Paris, France",
    "lat": 48.8584,
    "lon": 2.2945,
    "type": "tourism",
    "importance": 0.95,
    "address": {
      "tourism": "Eiffel Tower",
      "road": "Avenue Anatole France",
      "city": "Paris",
      "country": "France",
      "postcode": "75007"
    },
    "photos": [
      {
        "url": "https://...",
        "lat": 48.8580,
        "lon": 2.2948,
        "heading": 45
      }
    ],
    "has_street_imagery": true
  }
]
```

## Examples

### Geocode an address
```bash
./scripts/places.sh '{"street": "350 Fifth Avenue", "city": "New York", "state": "NY"}'
```

### Find a landmark with photos
```bash
./scripts/places.sh '{"query": "Statue of Liberty", "include_photos": true, "photo_radius": 200}'
```

### Search by postal code
```bash
./scripts/places.sh '{"postalcode": "90210", "country": "USA"}'
```

### Advanced mode for richer data
```bash
./scripts/places.sh '{"query": "Times Square", "mode": "advanced", "include_photos": true}'
```

## Best Practices

- Use `query` for landmarks, POIs, and well-known places
- Use structured address fields for precise geocoding
- Enable `include_photos` when you need visual context
- Use `mode: "advanced"` for web-enriched place data
- Combine address components for more accurate results
