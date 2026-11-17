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
| `AEROAPI_OUTPUT_DIR` | no | Default directory for flight-map PNGs (default: `~/Downloads/flightaware-mcp`). |
| `AEROAPI_CACHE_TTL` | no | Seconds to cache identical **live-data** GET responses to cut per-query billing (default: 15; `0` disables). |
| `AEROAPI_STATIC_CACHE_TTL` | no | Longer TTL for **reference data** that rarely changes — airport/operator info, routes, ownership, canonical lookups (default: 3600; `0` disables). |

## Tools

Every read tool below takes an optional `view` and answers on the **compact**
rung when you omit it — see [Response shape](#response-shape-view).

**Flights:** `fa_get_flights`, `fa_search_flights`, `fa_search_flights_advanced`, `fa_search_flight_positions`, `fa_count_flights`, `fa_get_flight_track`, `fa_get_flight_position`, `fa_get_flight_route`, `fa_get_flight_map`, `fa_get_flight_history`, `fa_resolve_flight`

**Airports:** `fa_get_airport`, `fa_get_airport_flights`, `fa_get_airport_flight_counts`, `fa_get_airport_routes`, `fa_list_airports`, `fa_get_nearby_airports`, `fa_get_airport_delays`, `fa_get_airport_weather`, `fa_resolve_airport`

**Operators / aircraft:** `fa_get_operator`, `fa_get_operator_flights`, `fa_list_operators`, `fa_get_aircraft_owner`

**Schedules / predictive:** `fa_get_scheduled_flights`, `fa_foresight_search` (Foresight is a premium tier — expect a 402/403 on a Personal key)

**Alerts** (account-mutating writes ask the user to confirm first — a confirmation prompt where the client supports one (unless the server sets `MCP_CONFIRM_ELICITATION=off`); otherwise the first call makes no network call and returns a preview plus a `confirmToken`, and only a repeat call with that token, after the user approves, performs the write): `fa_list_alerts`, `fa_get_alert`, `fa_create_alert`, `fa_update_alert`, `fa_delete_alert`, `fa_get_alerts_endpoint`, `fa_set_alerts_endpoint`

## Response shape (`view`)

Twenty-eight of the thirty-four tools take `view: "compact" | "full"`, and
**`compact` is the default** — every read answers on the slim rung without
being asked. In practice that is *every read tool here except*
`fa_get_flight_map` and `fa_healthcheck`; the four alert writes
(`fa_create_alert`, `fa_update_alert`, `fa_delete_alert`,
`fa_set_alerts_endpoint`) take none either.

**Compact here is media stripping, not a field projection — do not expect a
field list.** It removes image and avatar URLs from the payload and nothing
else. These tools hand back AeroAPI's response close to verbatim, and this repo
holds no captured AeroAPI fixture and no documented field list, so nothing in
it can honestly say which of FlightAware's fields matter and which are noise.
Inventing a keep-list would risk a flight record coming back with holes in it
that reads like a verified answer. Stripping is subtractive: it cannot lose a
field nobody knew about. The practical consequence is that on a typical AeroAPI
flight or airport payload compact saves little — it is the honest ceiling, not
a compression claim.

`fa_list_alerts` also takes `view: "brief"` — the context-groups one-liner
(see [In context groups](#in-context-groups)).

`view: "full"` returns AeroAPI's payload untouched. There is deliberately **no
`raw` rung**: nothing normalises the payload on the way through, so `full`
already IS the untouched upstream response and a third value would silently
alias it.

Why the six without it have none:

- **`fa_get_flight_map`'s product IS the image.** It returns a rendered PNG —
  written to disk, or inline base64 with `inline: true`. Routing that through a
  rung whose whole job is removing images would delete exactly what you asked
  for, so it is not wired and never should be.
- **`fa_healthcheck`** answers "is this connector working?" with a verdict, not
  a record. There is nothing in it to strip.
- **The four alert writes return receipts** — an id, a status, a
  preview and its `confirmToken`. A receipt has nothing to strip and everything to keep.
  `fa_get_alerts_endpoint` is the read of that pair and does take `view`.

Passing `view` to one of those six is not an error and not a warning: MCP tool
schemas are non-strict, so the key is dropped and you get that tool's ordinary
output.

## In context groups

On a host with context groups (mcp-host), every FlightAware tool joins the
**travel** group (`_meta.mint.domain: "travel"`); the healthcheck joins none.

- **Canonical read:** `fa_list_alerts` answers *what's on* — the flights you
  are watching (`canonical: true`). Its `view: "brief"` answers one line per
  alert, `ident route — <start date or no date> — <active | active until … |
  expired … | paused>`, inside the untrusted-data envelope (`data: string[]`),
  with `-- none` for an account with no alerts and `-- more` when AeroAPI has
  another page; an alert description that starts with `-- ` or `\` is
  escaped with one leading `\` so it never reads as a note. It names no `subject` — AeroAPI is one account's key with no
  listable set of the person's subjects — and no `when`, as the alert list
  takes no date range. Nothing here answers *what's new* or *what's due*.
  Alerts need a Standard/Premium AeroAPI tier, so on a Personal key the group
  reports this source's 401 rather than a list.
- **Lookups and changes:** every flight, airport, operator, aircraft and
  schedule read is a `lookup` hint, with the words people say (`flight
  status`, `delayed`, `departures`, `airline`, `tail number`, …) as aliases;
  the four alert writes are `change` hints and still ask before they write.
- **A compound ask** looks like "what's on this week — any flights I'm
  watching, and is anything due at school?" — the group calls
  `fa_list_alerts` in `brief` beside the other members and merges the lines.
- **Not browser-bridged:** every call is a direct AeroAPI request on your key,
  so this source never answers "needs your browser open".

## Notes

- Flight idents can be a designator (`UAL123`), a registration (`N12345`), or an `fa_flight_id`; position/track/route/map tools take an `fa_flight_id`.
- Paged collections return a `links.next` cursor — pass it back as `cursor` to fetch more.
- Every request rides your own AeroAPI key; usage counts against your subscription quota.
