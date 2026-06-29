---
name: flightaware-mcp
description: Live flight tracking and aviation data via FlightAware AeroAPI through MCP. Use when the user asks to track a flight, look up a flight's status/position/route/track, see an airport's arrivals/departures/delays/weather, find flights for an airline, look up an aircraft's owner, get scheduled flights between dates, or manage FlightAware flight alerts. Triggers on phrases like "where is flight UAL123", "track flight", "JFK departures", "is my flight delayed", "flights near", "who owns tail number N12345", or "set up a flight alert". Requires the @chrischall/flightaware-mcp package installed and the flightaware server registered (see Setup), plus an AeroAPI key.
---

# flightaware-mcp

MCP server for **FlightAware AeroAPI** (v4) — live flight tracking, airport boards, operators, schedules, aircraft, and flight alerts, exposed to Claude over stdio.

- **npm:** [npmjs.com/package/@chrischall/flightaware-mcp](https://www.npmjs.com/package/@chrischall/flightaware-mcp)
- **Source:** [github.com/chrischall/flightaware-mcp](https://github.com/chrischall/flightaware-mcp)

## Setup

### Option A — npx (recommended)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "flightaware": {
      "command": "npx",
      "args": ["-y", "@chrischall/flightaware-mcp"],
      "env": {
        "AEROAPI_API_KEY": "your-aeroapi-key-here"
      }
    }
  }
}
```

Get a key at [flightaware.com/aeroapi/portal](https://www.flightaware.com/aeroapi/portal/). The free **Personal** tier (500 calls/month) is enough to get started; AeroAPI bills per query.

### Option B — from source

```bash
git clone https://github.com/chrischall/flightaware-mcp
cd flightaware-mcp
npm install && npm run build
```

## Environment

| Var | Required | Purpose |
| --- | --- | --- |
| `AEROAPI_API_KEY` | yes | Your FlightAware AeroAPI key (sent as the `x-apikey` header). |
| `AEROAPI_OUTPUT_DIR` | no | Default directory for flight-map PNGs (default: cwd). |
| `AEROAPI_CACHE_TTL` | no | Seconds to cache identical **live-data** GET responses to cut per-query billing (default: 15; `0` disables). |
| `AEROAPI_STATIC_CACHE_TTL` | no | Longer TTL for **reference data** that rarely changes — airport/operator info, routes, ownership, canonical lookups (default: 3600; `0` disables). |

## Tools

**Flights:** `fa_get_flights`, `fa_search_flights`, `fa_search_flights_advanced`, `fa_search_flight_positions`, `fa_count_flights`, `fa_get_flight_track`, `fa_get_flight_position`, `fa_get_flight_route`, `fa_get_flight_map`, `fa_get_flight_history`, `fa_resolve_flight`

**Airports:** `fa_get_airport`, `fa_get_airport_flights`, `fa_get_airport_flight_counts`, `fa_get_airport_routes`, `fa_list_airports`, `fa_get_nearby_airports`, `fa_get_airport_delays`, `fa_get_airport_weather`, `fa_resolve_airport`

**Operators / aircraft:** `fa_get_operator`, `fa_get_operator_flights`, `fa_list_operators`, `fa_get_aircraft_owner`

**Schedules / predictive:** `fa_get_scheduled_flights`, `fa_foresight_search` (Foresight is a premium tier — expect a 402/403 on a Personal key)

**Alerts** (account-mutating writes are confirm-gated — without `confirm: true` they return a dry-run preview and make no network call): `fa_list_alerts`, `fa_get_alert`, `fa_create_alert`, `fa_update_alert`, `fa_delete_alert`, `fa_get_alerts_endpoint`, `fa_set_alerts_endpoint`

## Notes

- Flight idents can be a designator (`UAL123`), a registration (`N12345`), or an `fa_flight_id`; position/track/route/map tools take an `fa_flight_id`.
- Paged collections return a `links.next` cursor — pass it back as `cursor` to fetch more.
- Every request rides your own AeroAPI key; usage counts against your subscription quota.
