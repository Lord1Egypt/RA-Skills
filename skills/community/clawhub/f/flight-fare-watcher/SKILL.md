---
name: flight-fare-watcher
description: Watch Google Flights fares and get alerted only when a price drops or hits a target. Use when the user wants flight price tracking, fare-drop alerts for a route and dates, or a one-off flight search with structured prices. Runs the magnova/flight-price-watch Actor through the Apify plugin for OpenClaw; flight records cost $0.002 and drop alerts $0.02 on the user's own Apify account.
version: 1.0.1
homepage: https://apify.com/magnova/flight-price-watch
metadata:
  openclaw:
    requires:
      env:
        - APIFY_API_TOKEN
---

# Flight Fare Watcher

Fares move daily, and nobody wants to re-check the same
route by hand. This skill registers fare watches on routes
and dates the user cares about and, on each check, reports
only what changed: itineraries whose price fell, and the
first moment a route's lowest fare reaches the user's
target price. It can also run a plain one-off search.

## Prerequisites

1. The Apify plugin for OpenClaw is installed and allowlisted:
   `openclaw plugins install @apify/apify-openclaw-plugin`
2. `APIFY_API_TOKEN` holds the user's own Apify API token. All
   runs bill to that account.
3. You call Actors through the plugin's `apify` tool: `start`
   (returns a runId), then `collect` (returns the results).

If the plugin or token is missing, stop and tell the user
exactly what to install or set. Do not scrape Google Flights
yourself and do not substitute another source.

**Cost, stated plainly:** the Actor charges $0.002 per
flight record and $0.02 per price-drop alert, no start fee.
A watch's first check delivers the current itineraries as
baseline records (about $0.04 for 20 results); later checks
charge nothing unless a fare actually drops. A daily watch
on one route typically costs a few cents a month. The Actor
reads public Google Flights data only — no login, no
booking.

## Setup (first run only)

Ask the user for: origin and destination airport codes
(e.g. JFK to LAX), the departure date (and return date for
a round trip), and optionally a target price. Store the
watch input so later checks reuse it exactly — a watch is
identified by route, dates, cabin and passengers, so
changing any of them starts a new baseline.

## Workflow

**Register or check a watch** — call the Actor
`magnova/flight-price-watch` with:

```json
{
  "routes": [{"origin": "JFK", "destination": "LAX", "departureDate": "2027-06-15"}],
  "mode": "watch",
  "targetPrice": 150,
  "maxResultsPerRoute": 20
}
```

**One-off search** — same input with `"mode": "search"`.

Reading the results:

- `BASELINE` records appear only on a watch's first check.
  Summarize the cheapest few and the lowest price, and tell
  the user the watch is set.
- `PRICE_DROP` records carry `previousPrice`, `dropAmount`
  and `dropPercent` — report the airline, times, new price
  and the drop, with the record's `googleFlightsUrl`.
- `TARGET_HIT` means the route's lowest fare reached the
  target — lead with it.
- A check that returns only a `SUMMARY` record means
  nothing changed: say so in one line, or stay silent if
  the user asked for alerts only.
- `ERROR` records name the route that could not be checked;
  mention it and retry on the next scheduled check.

## Scheduling

Offer to run the watch check on a daily cadence (the user's
own scheduler or cron). Fares for far-out dates move slowly;
daily is plenty, twice daily for departures inside a month.
