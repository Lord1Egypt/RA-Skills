---
name: errand-router
description: "Plan the optimal order for a multi-stop errand run: groceries, pharmacy, post office, pickup, drop-off. Computes distance (haversine) and travel time between stops, respects opening-hours time windows, adds service/dwell time per stop, and optimizes the visit order with nearest-neighbor + 2-opt. Outputs a timed itinerary with ETAs, wait time, and flags for stops you'd arrive at after closing. Use when someone asks what order to run errands in, whether several stops fit before closing time, or how to route a day of pickups and deliveries."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [errands, routing, tsp, time-windows, itinerary, trip-planning, logistics]
---

# Errand Router 🗺️

"Drop package at post office, pick up prescription, return library books,
groceries, and the hardware store closes at 6 — what order do I go in?"

Most people solve this by vibes and end up backtracking across town. This
skill treats a Saturday errand run as what it mathematically is: a **small
Traveling Salesperson Problem with Time Windows (TSPTW)** — small enough
to solve optimally in milliseconds with construction + local search, no
OR-tools required.

## Overview

`scripts/errand_router.py` takes a list of stops (name, lat/lon or x/y,
dwell minutes, opening hours) plus a start point and departure time, then:

1. Builds a **distance matrix** with the haversine formula (lat/lon) or
   Euclidean distance (local x/y), converted to travel time via a
   configurable city speed (30 km/h default — traffic-realistic, not
   as-the-crow-flies fantasy).
2. Applies a **road-factor** (1.3×) — real street distance is ~30% longer
   than great-circle distance; this is the standard planning correction.
3. Constructs a route with **nearest-neighbor**, then improves it with
   **2-opt** moves, rejecting any move that breaks a time window.
4. **Simulates the clock**: departure → drive → (wait if early) → dwell →
   drive → … and reports ETA at each stop, total km, total time, wait time.
5. Flags 🚨 any stop that would be reached **after closing** — the single
   most common errand failure — and suggests what to drop or reorder.

## When to Use

- "I have 5 errands and two stores close at 6pm — does my plan work?"
- "What's the best order to hit these places starting from home?"
- "Can I fit the pharmacy pickup before work if I leave at 8:15?"
- "Route my day: gym, then bank, then two returns, then lunch pickup."
- Any "visit N places, some have hours, minimize driving" request.

**Don't use for:** road-navigation turn-by-turn (no live traffic, no
one-ways), >15 stops with tight windows (that needs a real solver /
OR-tools), or multi-day logistics fleets.

## How It Works — Steps

1. **Describe the stops** — a JSON file (or CLI `--stop` repeated flags):
   ```json
   {
     "start": {"name": "home", "lat": 52.52, "lon": 13.405},
     "depart": "09:30",
     "speed_kmh": 30,
     "stops": [
       {"name": "post office", "lat": 52.51, "lon": 13.39,
        "dwell_min": 10, "open": "09:00", "close": "18:00"},
       {"name": "pharmacy", "lat": 52.54, "lon": 13.42,
        "dwell_min": 15, "open": "10:00", "close": "20:00"}
     ]
   }
   ```
2. **Run**:
   ```bash
   python3 scripts/errand_router.py plan errands.json
   python3 scripts/errand_router.py plan errands.json --end home --json
   ```
3. **Read the itinerary** — ordered stops with arrival/departure times,
   wait-for-open minutes, leg distances, and violation flags.
4. **Fix violations** — drop the flagged stop, leave earlier
   (`--depart 09:00`), or relax the constraint and re-run until clean.
5. **Use `--json`** for agent consumption of the route legs.

## Algorithm Notes

```
travel_time(a,b) = haversine(a,b) × ROAD_FACTOR(1.3) / speed
construction    : nearest feasible neighbor by time
improvement     : 2-opt segment reversal, keep if shorter AND feasible
feasibility     : arrival + dwell ≤ close (hard), open (soft: wait)
```
Haversine uses R = 6371 km. 2-opt runs to convergence (no improving move);
for n ≤ 12 stops this is effectively instant and near-optimal.

## Worked Example

```
5 errands from home at 09:30, two afternoon-only stops:
  order: post office → bank → pharmacy → grocery → hardware
  total: 11.2 km · 1h 55m (incl. 12 min waiting + 55 min dwell)
  ✅ all stops open on arrival
Re-run with --depart 15:30:
  🚨 hardware store closes 18:00, arrival 18:12 — leave ≥35 min earlier
```

## Common Pitfalls

1. **Using straight-line distance as driving time.** Always apply the
   1.3 road factor and a realistic city speed (25–35 km/h door-to-door,
   including lights and parking).
2. **Forgetting dwell time.** 6 stops × 15 min inside = 90 minutes that
   vanishes from naive plans. Dwell is often bigger than driving.
3. **Treating time windows as optional.** A route that's shortest but
   arrives after closing is worth zero. The tool hard-rejects those moves.
4. **Mixing lat/lon and x/y stops.** Pick one coordinate system per run.
5. **Trusting ETAs to the minute.** This is planning math, not live
   traffic — treat outputs as ±20% and keep one slack stop's worth of buffer.
6. **Too many stops.** Beyond ~15 with windows, 2-opt may stall in a
   local optimum; fine for errands, wrong for fleet logistics.

## Verification Checklist

- [ ] Every stop appears exactly once in the itinerary
- [ ] No arrival time after a stop's `close` (or explicitly flagged)
- [ ] Total time = drive + dwell + wait (recompute by hand for one leg)
- [ ] Route starts at `start` and ends at start or `--end`
- [ ] Distance sanity: 1° latitude ≈ 111 km — check a known pair

## One-Shot Recipes

**Quick 3-stop check from the CLI (no JSON file):**
```bash
python3 scripts/errand_router.py quick \
  --start "home,52.52,13.405" \
  --stop "pharmacy,52.54,13.42,10,09:00,20:00" \
  --stop "post,52.51,13.39,10,09:00,18:00" \
  --depart 17:00
```

**Morning run with a forced last stop (pick-up before dinner):**
```bash
python3 scripts/errand_router.py plan errands.json --end grocery
```
