---
name: fuel-cli
description: UK fuel prices CLI — find nearby stations by postcode or coordinates, get station details, ranked by price/distance/freshness, and agent-friendly JSON envelopes with `--output <path>` for field projection. Use when checking UK petrol or diesel prices, finding cheapest fuel nearby, looking up station details by name or node ID, or when an agent needs structured fuel price data with data-quality advisories.
homepage: https://fuel-cli.xyz
metadata:
  {
    "openclaw":
      {
        "emoji": "⛽",
        "requires":
          {
            "bins": ["fuel"],
            "env": ["FUEL_FINDER_CLIENT_ID", "FUEL_FINDER_CLIENT_SECRET"],
          },
        "primaryEnv": "FUEL_FINDER_CLIENT_ID",
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@shan8851/fuel-cli",
              "bins": ["fuel"],
              "label": "Install fuel-cli (npm)",
            },
          ],
      },
  }
---

# fuel-cli

Use `fuel` for UK fuel prices: nearby station search, station detail, ranked results with freshness tracking.

Setup

- `npm install -g @shan8851/fuel-cli`
- Register at https://www.fuel-finder.service.gov.uk for Fuel Finder OAuth credentials
- `export FUEL_FINDER_CLIENT_ID=***` and `export FUEL_FINDER_CLIENT_SECRET=***` or add to `.env`
- Warm cache reads work without credentials until the cache needs a refresh

Nearby Stations

- By postcode: `fuel near "SE1 9SG" --fuel E10`
- By coordinates: `fuel near "51.501,-0.141" --fuel B7_STANDARD`
- Custom radius: `fuel near "SE1 9SG" --fuel E10 --radius 8mi`
- Sort options: `fuel near "SE1 9SG" --fuel E10 --sort price` (best, price, distance, freshest)
- Limit results: `fuel near "SE1 9SG" --fuel E10 --limit 5`
- Force refresh: `fuel near "SE1 9SG" --fuel E10 --refresh`

Station Detail

- By name: `fuel station "tesco watford"`
- By node ID: `fuel station "<node-id>"`
- Project one field: `fuel station "<node-id>" --output station.prices.0.pencePerLitre`
- Project subtree: `fuel station "<node-id>" --output station.openingTimes`

Fuel Types

- `E10` — E10 unleaded petrol
- `E5` — Super unleaded petrol
- `B7_STANDARD` — Standard diesel
- `B7_PREMIUM` — Premium diesel
- `B10` — B10 biodiesel
- `HVO` — HVO diesel

Output

- Defaults to text in a TTY and JSON when piped
- Force JSON: `fuel near "SE1 9SG" --fuel E10 --json`
- Force text: `fuel near "SE1 9SG" --fuel E10 --text`
- Disable colour: `fuel --no-color near "SE1 9SG" --fuel E10`
- Success envelope: `{ ok, schemaVersion, command, requestedAt, data }`
- Error envelope: `{ ok, schemaVersion, command, requestedAt, error }`

Agent Notes

- `--fuel` is required on `near` — petrol and diesel are never mixed in one ranking
- `--output <path>` is available on both `near` and `station`
- Paths use dot notation with zero-based array indexes, for example `stations.0.selectedPricePencePerLitre` or `station.prices.0.pencePerLitre`
- In text mode, scalar projections print just the value; object or array projections print plain JSON
- Projection errors are structured: malformed paths return `INVALID_INPUT`, missing paths return `NOT_FOUND`
- Data-quality advisories live under `data.quality.advisories` — warn about stale prices, missing timestamps, and excluded test stations
- `data.quality.freshnessCounts` breaks down fresh/aging/stale/unknown price counts
- Likely test/demo forecourts are excluded automatically when normal stations exist; count is in `data.quality.excludedLikelyTestStations`

Configuration

- `FUEL_FINDER_CLIENT_ID` — required for live data (free registration)
- `FUEL_FINDER_CLIENT_SECRET` — required for live data
- `FUEL_FINDER_BASE_URL` — optional, defaults to https://www.fuel-finder.service.gov.uk
- `FUEL_CACHE_DIR` — optional, override cache location (defaults to platform cache dir)

Notes

- `near` requires `--fuel` so petrol and diesel results are never mixed
- Accepts UK postcodes (`SE1 9SG`) and coordinates (`51.501,-0.141`)
- Radius accepts unitless (miles) or with `mi`/`km` suffix
- Persistent local cache for station and price data — works offline until cache expires
- Prices include freshness bands (fresh < 30min, aging < 24h, stale > 24h, unknown)
- Exit codes: 0 success, 2 bad input or ambiguity, 3 upstream failure, 4 internal error
- When a station query is ambiguous, the error includes candidate suggestions with brand, address, postcode, and node ID
