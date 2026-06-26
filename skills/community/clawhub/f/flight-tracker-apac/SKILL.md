---
name: flight-tracker-apac
description: Check flight schedules between supported airports, show timings, terminals, gates, delays, aircraft details, and optional departure countdowns using a local Python script backed by the Aviationstack API. Best for APAC routes and selected long haul routes included in the built in airport list.
metadata:
  author: Caddy Tan
  version: 1.0.1
  category: travel
  tags:
    - flights
    - aviation
    - travel
    - schedule
    - countdown
    - apac
    - python
  openclaw:
    primaryEnv: AVIATIONSTACK_API_KEY
    requires:
      env:
        - AVIATIONSTACK_API_KEY
      bins:
        - python3
---

# Flight Tracker APAC

## Overview

Use this skill to check flight schedules between supported airports with a local Python script.

This skill is best for APAC routes and also supports a small number of built in long haul airports such as SFO, LAX, and JFK.

This skill is useful for requests such as:
- check flights from SIN to HKG
- show today's flights from SIN to TFU
- give me a departure countdown for SIN to MEL
- check flights from SIN to LAX

The script can display:
- scheduled, estimated, and actual departure and arrival times
- terminal and gate details when available
- airline, flight number, aircraft, delay, and status
- calculated flight time and scheduled duration
- optional countdown to departure

If no API key is configured, the script falls back to manual lookup links for Google Flights and FlightRadar24.

## Requirements

This skill requires:
- `python3`
- a free Aviationstack API key in `AVIATIONSTACK_API_KEY`

## API key setup

1. Create a free account at Aviationstack.
2. Copy your API access key from the Aviationstack dashboard.
3. Open this file on your machine:

```bash
~/.openclaw/.env
```

4. Add this line:

```bash
AVIATIONSTACK_API_KEY=your_real_api_key_here
```

5. Restrict the file so only your user can read it:

```bash
chmod 600 ~/.openclaw/.env
```

## File layout

Recommended skill folder:

```text
flight-tracker-apac/
├── SKILL.md
└── scripts/
    └── schedule.py
```

## When to use this skill

Use this skill when the user asks to:
- check flights between two supported IATA airports
- compare available operating flights on a route
- view departure and arrival timings on a route
- see a countdown to departure for a route

Do not use this skill for:
- ticket prices, fare comparisons, or booking actions
- unsupported airport codes that are not in the script's built in airport list
- general travel planning that is unrelated to route schedules

## Supported usage patterns

Run the local script from the skill folder:

```bash
python3 {baseDir}/scripts/schedule.py SIN HKG
python3 {baseDir}/scripts/schedule.py --from SIN --to HKG
python3 {baseDir}/scripts/schedule.py --from SIN --to TFU --countdown
```

## Workflow

1. Confirm the user wants a flight schedule between two airports.
2. Use IATA airport codes from the script's supported list.
3. Run the script with origin and destination.
4. Add `--countdown` if the user wants time remaining to departure.
5. Return the results clearly, grouped by date if multiple flights are shown.
6. If the API key is missing, tell the user the script returned manual lookup links instead.

## Output guidance

When presenting results, summarize:
- route searched
- number of operating flights found
- each flight's airline and code
- departure and arrival timing
- terminal and gate where available
- status, delay, and aircraft
- countdown if requested

## External services

The script connects to:
- Aviationstack for flight schedule data over HTTPS
- Google Flights for manual fallback lookup links over HTTPS
- FlightRadar24 for manual fallback route links over HTTPS

The required API key is:
- `AVIATIONSTACK_API_KEY`

## Security and privacy

What leaves the machine:
- route lookup parameters and your Aviationstack API key go to Aviationstack
- route codes go into the fallback Google Flights and FlightRadar24 URLs

What stays local:
- the script logic
- local environment files
- any other files on the machine

Notes:
- the script uses the documented `access_key` query parameter required by Aviationstack, but the request is sent over HTTPS
- keep `~/.openclaw/.env` private and do not commit it to source control
- only install and use this skill if you are comfortable sending route data to those external services

## Notes

For best results, make sure the script and the `AVIATIONSTACK_API_KEY` environment variable are both available before running the skill.
