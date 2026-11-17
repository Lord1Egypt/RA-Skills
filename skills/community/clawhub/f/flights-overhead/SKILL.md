---
name: "flights-overhead"
description: "See what flights are above you right now. Identify contrails, planes overhead, and nearby air traffic using OpenSky Network (free, no key)."
---

# Flights Overhead Skill

See what flights are currently above you. Identify contrails, planes overhead, and nearby air traffic using OpenSky Network (free, no API key needed).

## When to Use

- "What flights are above me right now?"
- "What plane is that?"
- "What's that contrail?"
- "What flights are near me?"
- "What's flying overhead?"
- Any query about identifying aircraft in the sky

## Requirements

- **OpenSky Network** — free, no API key, no account needed
- **Python 3** (standard library only)
- **User's location** — lat/lng (from device location or ask the user)
- Script: `scripts/flights_overhead.py`

## Privacy & Data Disclosure

- **OpenSky Network**: Your approximate location (lat/lng bounding box) is sent as query parameters to OpenSky's public API to retrieve nearby aircraft. No account or personal data is transmitted beyond coordinates.
- **Location source**: The agent should confirm or ask for the user's location rather than silently using stored addresses. An approximate location (city-level) is usually sufficient for overhead flight queries.
- No data is stored externally.

## Script Usage

```bash
# Show flights within 50 km (default)
python3 scripts/flights_overhead.py --lat 47.68 --lng -122.21

# Smaller radius, JSON output
python3 scripts/flights_overhead.py --lat 47.68 --lng -122.21 --radius 30 --json

# Limit results
python3 scripts/flights_overhead.py --lat 47.68 --lng -122.21 --limit 5 --json
```

### Parameters

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--lat` | Yes | — | Observer latitude |
| `--lng` | Yes | — | Observer longitude |
| `--radius` | No | 50 | Search radius in km |
| `--limit` | No | 20 | Max flights to return |
| `--json` | No | — | Output as JSON |

### Output (JSON)

```json
{
  "count": 8,
  "flights": [
    {
      "callsign": "ASA640",
      "airline": "Alaska Airlines",
      "flight_number": "AS640",
      "lat": 47.65,
      "lng": -122.30,
      "altitude_ft": 4875,
      "altitude_m": 1486,
      "speed_kmh": 464.9,
      "heading": 355,
      "vertical_rate_ms": -5.2,
      "distance_km": 8.2,
      "origin_country": "United States"
    }
  ]
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `callsign` | ICAO callsign (e.g. ASA640) |
| `airline` | Resolved airline name (if recognized) |
| `flight_number` | IATA flight number (e.g. AS640) |
| `altitude_ft` | Altitude in feet |
| `speed_kmh` | Ground speed |
| `heading` | Direction of travel (degrees, 0=north) |
| `distance_km` | Distance from observer |
| `vertical_rate_ms` | Climb/descent rate (negative = descending) |

## Procedure

### Step 1: Determine User Location

Options (in priority order):
1. **Device location** (preferred for mobile users) — use `nodes` → `location_get`. Requires user to have granted location permission on their paired device. Best option when the user may be away from home.
2. **Home address** from USER.md — convert to lat/lng. Use as fallback when device location is unavailable or user is known to be at home.
3. **Ask the user** — if neither is available.

**Note:** Device location requires explicit user permission on the paired mobile device. If not granted, the call will fail — fall back to option 2 or 3. For mobile users who are frequently away from home, device location gives accurate results. For stationary/home use, the address from USER.md is sufficient.

### Step 2: Query Flights

```bash
python3 scripts/flights_overhead.py --lat <lat> --lng <lng> --radius 30 --json
```

Use radius 5 km for "what's over me" / "what's that plane" (actually audible/visible).
Use radius 30 km for "what's that contrail" (high altitude, visible far away).
Use radius 20 km for "what flights are near me" or general area queries.

### Step 3: Look Up Routes

For identified commercial flights, look up origin/destination:

```bash
# Web search for flight route
web_search "<airline> <flight_number> flight route origin destination today"
```

FlightAware (`flightaware.com/live/flight/<ICAO_CALLSIGN>`) and FlightStats typically show the route. Extract origin → destination from the search snippet.

Skip route lookup for:
- Private/GA aircraft (registration numbers like N262BS)
- If the user just wants a quick count, not details

### Step 4: Present Results

**For "what's that contrail?" or "what plane is that?":**
- Filter to high-altitude flights (>25,000 ft for contrails)
- Show closest match with airline, flight number, altitude, heading
- Mention where it's likely going based on heading

**For "what flights are above me?":**
- Show all flights sorted by distance
- Group by airline if many results
- Mention total count

**For identifying a specific plane:**
- Ask for any details (direction it's heading, approximate altitude, size)
- Filter results to match

### Step 4: Enrich (Optional)

If user wants more info about a specific flight:
- Use `flight_tracker.py` to get route (origin/destination) if callsign is known
- Mention approximate aircraft type from origin_country + airline

## Example Responses

**"What flights are above me?"**
> Right now within 30 km of Kirkland, I can see 8 flights:
> - AS640 (Alaska Airlines) at 4,875 ft, 8 km away, heading north
> - DL2980 (Delta) at 3,850 ft, 9 km away, heading south
> - WN1713 (Southwest) at 7,000 ft, 7 km away, heading north
> ...
> Mostly arrivals/departures from SEA-TAC.

**"What's that contrail heading east?"**
> That's likely UA2271 (United Airlines) at 35,000 ft, heading 208° (southwest). It's about 13 km from you.

## Data Source

- **OpenSky Network** — community-run ADS-B network, free, no key needed
- Rate limit: 1 request per 10 seconds (anonymous)
- Coverage: Excellent over US/Europe, good globally except remote oceans
- Delay: ~5-15 seconds behind real-time

## Supported Airlines

The script recognizes 40+ airlines by ICAO callsign prefix and resolves them to human-readable names and IATA flight numbers. Unrecognized callsigns display as-is (often private/cargo aircraft with registration numbers like N262BS).

## Notes

- Contrails typically form above 25,000 ft in cold air — filter by altitude for contrail queries
- Aircraft on the ground are automatically excluded
- Results sorted by distance from observer (closest first)
- Heading 0°/360° = north, 90° = east, 180° = south, 270° = west
- Private/GA aircraft show registration numbers (e.g. N262BS) without airline info
