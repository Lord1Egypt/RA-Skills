---
name: car-maintenance-timeline
description: "Use when the user asks what car maintenance is due or overdue, whether a service can wait, what a dealer 'recommended service' actually contains, or to build a maintenance schedule and budget from mileage, vehicle age, and service history. Computes dual-interval status (every N km OR M months, whichever first), applies a severe-service multiplier for city/short-trip/towing driving, projects a 24-month service timeline from annual mileage, and shows typical cost ranges and DIY difficulty so owners can challenge upselling."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [car, vehicle, maintenance, schedule, automotive, diy, service, ownership-cost]
---

# Car Maintenance Timeline 🔧

"What's actually due on my car at 84,500 km?" Most owners answer this by
guessing, ignoring it, or trusting a service advisor whose incentives are not
aligned with their wallet. Result: missed safety services on one end, and
$600 "premium packages" full of items that aren't due yet on the other.

This skill treats the manufacturer maintenance schedule as what it is — a
table of **dual intervals** (every N km OR M months, whichever comes first) —
and computes, from your odometer, in-service date, and service history, what
is genuinely **OVERDUE**, **DUE SOON**, or OK, what it typically costs, and
how hard it is to do yourself.

## Overview

One tool, three commands (`scripts/car_maintenance.py`):

1. **`tasks`** — the built-in task library: 13 generic services with km/month
   intervals, severe-service intervals, priority class (safety-critical /
   wear-item / standard), typical cost range, and DIY difficulty.
2. **`status`** — per-task evaluation: last done (from `--history` or
   in-service by default), km-due-at, date-due-at, status with reason string
   ("overdue by km (+2,400 km vs interval)"), sorted safety-critical and
   overdue first. `--severe` switches to the severe-service column.
   `--json` for agents.
3. **`timeline`** — projects the next 24 months of services by extrapolating
   the odometer from annual mileage (explicit `--annual-km` or derived from
   km ÷ age), repeating recurring tasks across the window.

## When to Use

- "Is my car due for a service? It's at 84,500 km."
- "The dealer says I need the 90k package — what's actually due?"
- "I mostly do short city trips — does that change the schedule?" (yes: `--severe`)
- "What will maintenance cost me over the next two years?"
- "I changed the oil at 63,000 km in January — when is the next one?"

**Don't use for:**
- Diagnosing symptoms (noises, warning lights, leaks) — that's a mechanic.
- Model-specific intervals — the library is generic; **your owner's manual
  always overrides** (see Pitfall #1).
- Warranty compliance tracking (needs dealer-documented service records).

## Quick Start

```bash
# 1. See the task library
python3 scripts/car_maintenance.py tasks

# 2. What's due right now? (84,500 km, registered 2021-03-10, mostly city driving)
python3 scripts/car_maintenance.py status \
  --km 84500 --in-service 2021-03-10 --severe

# 3. Same, but you know the oil was done at 63,000 km on 2026-01-15
python3 scripts/car_maintenance.py status --km 84500 --in-service 2021-03-10 \
  --history '[{"task":"oil","km":63000,"date":"2026-01-15"}]' --severe

# 4. Budget the next 24 months (~15,000 km/yr)
python3 scripts/car_maintenance.py timeline \
  --km 84500 --in-service 2021-03-10 --annual-km 15000

# 5. Machine-readable output for agents
python3 scripts/car_maintenance.py status --km 84500 \
  --in-service 2021-03-10 --json
```

## How It Works

**Dual intervals (whichever comes first).** A task is due at
`last_done_km + interval_km` OR `last_done_date + interval_months`, whichever
event arrives first. A 12,000 km/year car hits the oil change's 10,000 km
before its 12 months; a retired driver's 4,000 km/year car hits the 12 months
first. Both are "due" — mileage is a proxy for engine hours and heat cycles,
time for chemistry (oil oxidation, brake fluid hygroscopy, coolant
inhibitors).

**Severe service.** Short trips, city driving, towing, dust, and extreme heat
are the manufacturer-defined "severe" conditions. `--severe` switches tasks
to their severe intervals (oil 10,000→5,000 km; transmission fluid
100,000→60,000 km) or applies a global 0.75 multiplier where no specific
value exists. Most urban commuting qualifies — this is the single most
commonly missed adjustment.

**Due-soon band.** `DUE SOON` = within 20% of the km interval remaining, or
within 30 days of the time deadline. Anything beyond is `OK`.

**No-history default.** Without `--history`, the model assumes each task was
last done at in-service @ 0 km — i.e. never. On a used car with unknown
history this deliberately over-reports: baseline everything cheap (fluids,
filters) and move on. Feed real history entries (`task`, `km`, `date`) as you
learn them.

**Projection.** `timeline` converts annual mileage to km-per-day and walks
each task's next event forward, repeating recurring services across the
24-month window, giving each event an estimated odometer reading and cost
range — the basis of a realistic maintenance budget.

## Task Library (generic defaults)

| Task | km | months | severe km | priority | Typical cost | DIY |
|---|---|---|---|---|---|---|
| Engine oil & filter | 10,000 | 12 | 5,000 | wear | $40–90 | Easy |
| Tire rotation | 8,000 | 6 | — | **safety** | $20–50 | Easy |
| Engine air filter | 20,000 | 24 | — | wear | $15–40 | Easy |
| Cabin filter | 20,000 | 24 | — | standard | $20–60 | Easy |
| Brake fluid | 40,000 | 24 | — | **safety** | $80–150 | Moderate |
| Spark plugs | 60,000 | 48 | — | wear | $100–250 | Moderate |
| Coolant | 100,000 then 50,000 | 60/36 | — | wear | $90–180 | Moderate |
| Transmission fluid | 100,000 | 120 | 60,000 | wear | $150–350 | Hard |
| Drive belt (inspect) | 100,000 | 120 | — | wear | $0–120 | Moderate |
| Battery test | — | 48 (replace ~60) | — | wear | $0–30 test | Easy |
| Wiper blades | — | 12 | — | **safety** | $15–50 | Easy |
| Annual inspection/MOT | — | 12 | — | **safety** | $30–120 | — |
| Winter/summer tire swap | — | 6 | — | standard | $40–100 | Moderate |

Values are rounded generic conventions, not a substitute for the book for
your exact model.

## Workflow

1. Gather inputs: current odometer, in-service/first-registration date, any
   known service history (from receipts or the dealer's printout).
2. Decide severe vs normal: any of short trips <10 km, mostly stop-and-go,
   towing, dusty/unpaved roads, extreme heat → `--severe`.
3. Run `status`. Read OVERDUE safety-critical items first (tires, brake
   fluid, wipers, inspection) — those are the ones that bite.
4. Cross-check against the owner's manual; the manual wins where they differ.
5. Feed real history entries as you collect them; the report sharpens.
6. Run `timeline` once a year to budget; run `status` monthly or before trips.

## Common Pitfalls

1. **Trusting generic intervals over the owner's manual.** Intervals vary by
   engine, transmission, and market. Use this tool to understand structure
   and challenge upselling; use the manual for the numbers.
2. **Ignoring severe service.** "Severe" sounds exceptional but describes
   most city commuting. Running normal intervals on a severe-duty car is how
   sludge and transmission failures happen.
3. **Assuming time-based items don't matter on a low-mileage car.** Oil,
   brake fluid, and coolant age by chemistry, not just km. A 5-year-old
   30,000 km car is overdue for fluid services.
4. **Reading a giant OVERDUE list as a literal work order on a used car with
   unknown history.** It's a "baseline it" signal, not 13 simultaneous
   failures. Prioritize safety-critical, then fluids.
5. **Accepting a dealer's bundled "package" at face value.** Compare its
   contents against `status` output; items listed as OK are profit, not
   maintenance.
6. **Forgetting units.** The tool is km-based. For miles, convert first
   (×1.609) — mixing units silently shifts every interval.

## Verification Checklist

- [ ] `python3 scripts/car_maintenance.py tasks` runs and prints the library
- [ ] `status` with your km/date prints a sorted table + summary counts
- [ ] `--severe` visibly shortens oil (10,000 → 5,000 km) in `tasks`
- [ ] `--history` entries shift the oil due-at km/date
- [ ] `timeline` covers 24 months and repeats recurring tasks
- [ ] `--json` output parses (`meta` + `tasks` keys)
- [ ] `python3 scripts/test_car_maintenance.py` → ALL TESTS PASSED

## Example: reading the output

```
Vehicle: 84,500 km | in service 2021-03-10 | ~15,463 km/yr | SEVERE SERVICE
 ! Tire rotation          OVERDUE  safety-critical  6,000   2021-07-10
 ! Brake fluid            OVERDUE  safety-critical  30,000  2022-09-10
 ! Engine oil & filter    OVERDUE  wear-item        68,000  2026-07-15
   ...
Summary: 13 OVERDUE, 0 DUE SOON, 0 OK
```

The oil row reflects the history entry (63,000 km + severe 5,000 = due at
68,000, and Jan 15 + 6 mo = Jul 15 — km wins, it's already past). The tire
rows show why "the car feels fine" isn't evidence: the model surfaces what
the odometer and calendar already know.

## One-Shot Recipes

**Used-car baseline audit** (unknown history, 3 years, 60,000 km):
```bash
python3 scripts/car_maintenance.py status --km 60000 \
  --in-service 2023-08-01 --severe --json
```
Read: safety-critical OVERDUE = do now; wear OVERDUE = baseline fluids &
filters, ~$250–450 at an independent shop.

**Challenge a dealer's 90k package:**
```bash
python3 scripts/car_maintenance.py status --km 91000 --in-service 2019-05-02 \
  --history '[{"task":"oil","km":85000,"date":"2026-03-01"},
              {"task":"cabin_filter","km":85000,"date":"2026-03-01"},
              {"task":"tire_rotation","km":85000,"date":"2026-03-01"}]'
```
Anything in the package marked OK here is upsell; anything OVERDUE, price it
against the cost column before agreeing.

**24-month budget:**
```bash
python3 scripts/car_maintenance.py timeline --km 91000 \
  --in-service 2019-05-02 --annual-km 14000 --json
```
Sum the cost ranges by quarter; expect roughly $500–900/yr for an aging
commuter car, front-loaded if the list has OVERDUE entries.

---
*Advisory tool. Generic intervals; your owner's manual and local law
(e.g. mandatory inspection dates) always take precedence.*
