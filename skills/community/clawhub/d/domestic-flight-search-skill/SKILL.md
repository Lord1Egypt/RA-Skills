---
name: domestic-flight-search
description: "Query China domestic flights with schedules, airline details, airport resolution, and Juhe reference prices. Use when a user asks for domestic China flight options, lowest fares, same-day route comparisons, airport-specific searches, or Chinese city/airport name to IATA resolution before flight lookup."
metadata: { "openclaw": { "emoji": "✈️", "requires": { "bins": ["python3"], "env": ["JUHE_FLIGHT_API_KEY"] }, "primaryEnv": "JUHE_FLIGHT_API_KEY" } }
---

# Domestic Flight Search

Use the local Python script in this skill to query China domestic flights from the Juhe flight API. Tell users they must apply for their own Juhe API key before live queries will work.

Provider docs: `https://www.juhe.cn/docs/api/id/818`

## Setup Requirement

This skill does not ship with an API key. Users must create their own Juhe account, subscribe to the flight API, and set `JUHE_FLIGHT_API_KEY` before running live searches.

## Quick Start

Set the API key first:

```bash
export JUHE_FLIGHT_API_KEY='your_juhe_api_key'
```

Run a direct query:

```bash
python3 {baseDir}/scripts/domestic_flight_service.py search \
  --from 北京 --to 上海 --date 2026-03-20 --pretty
```

Optional reusable local HTTP mode:

```bash
python3 {baseDir}/scripts/domestic_flight_service.py serve --port 8765
```

Then call:

```bash
curl 'http://127.0.0.1:8765/search?from=北京&to=上海&date=2026-03-20'
```

## Workflow

1. Resolve the user's origin and destination.
   Accept common Chinese city names, airport names, or IATA codes.
   If the user says “北京首都” or “浦东机场”, keep the airport-specific query.

2. Query the script.
   For a single answer, run the CLI.
   For repeated machine-to-machine calls, use the local HTTP service.

3. Summarize the result.
   Mention airline, flight number, departure and arrival airport, departure and arrival time, duration, and `ticket_price`.
   Call the price `参考票价`, not a guaranteed bookable fare.

4. Handle ambiguity and missing setup.
   If the city is not recognized, ask for a specific airport or 3-letter code.
   If the user wants a round trip, run two one-way queries.
   If `JUHE_FLIGHT_API_KEY` is missing, tell the user to apply for a Juhe key and configure it before retrying.

## Output Rules

- Sort results by lowest `ticket_price` first.
- Prefer up to 5 options unless the user asked for more.
- State the exact travel date in `YYYY-MM-DD`.
- If the provider returns no results, say that no flight was found for that route/date under the current query.
- If the provider fails, surface the provider `error_code` and `reason` briefly.

## Resources

- Use [scripts/domestic_flight_service.py](./scripts/domestic_flight_service.py) for CLI and optional HTTP modes.
- Use [assets/data/domestic_city_codes.json](./assets/data/domestic_city_codes.json) and [assets/data/airport_aliases.json](./assets/data/airport_aliases.json) for Chinese name resolution.
- Read [references/provider-juhe.md](./references/provider-juhe.md) when you need the provider contract, parameters, setup notes, or limitations.
