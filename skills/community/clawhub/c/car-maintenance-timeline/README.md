# Car Maintenance Timeline 🔧

**What's actually due on my car right now — and what is the dealer just selling me?**

## The problem

Car maintenance schedules are dual-interval tables: every N kilometers **or**
M months, whichever comes first. Almost nobody tracks them that way. Instead:

- Owners guess, defer, and then face a $1,200 surprise when deferred fluid
  services cascade into real repairs — or skip a safety item like brake fluid
  that degrades by chemistry even on a parked car.
- Service advisors hand over "recommended packages" whose contents are chosen
  for margin, not mileage. A typical 90k package can contain hundreds of
  dollars of work the schedule says isn't due yet — and omit the one thing
  that is.

Meanwhile the actual inputs — odometer, registration date, service history,
driving profile — are sitting in your glovebox and phone. The math between
them is deterministic. This tool does that math.

## What it does

`scripts/car_maintenance.py` (Python 3, stdlib only, no network):

| Command | What you get |
|---|---|
| `tasks` | The 13-task generic library: km/month intervals, severe-service columns, safety priority, cost range, DIY difficulty |
| `status` | Per-task OVERDUE / DUE SOON / OK with due-at km and date, reason strings, safety-critical first |
| `timeline` | 24-month forward projection of services from your annual mileage, with estimated odometer and cost at each event |

Core mechanics:

- **Dual intervals, whichever-first**: low-mileage cars trigger services by
  time (oil oxidizes, brake fluid absorbs water), high-mileage by km.
- **Severe service** (`--severe`): short trips, city, towing, dust, heat —
  the conditions that actually describe most commuting — switch tasks to
  their severe intervals (oil 10,000→5,000 km, transmission fluid
  100,000→60,000 km).
- **Service history**: feed `--history '[{"task":"oil","km":63000,"date":"2026-01-15"}]'`
  and intervals anchor to real events instead of assuming "never done".
- **Projections & budgets**: `timeline` extrapolates the odometer from annual
  km (derived automatically or set explicitly) and lays out recurring
  services across 24 months.

## Quick start

```bash
python3 scripts/car_maintenance.py status \
  --km 84500 --in-service 2021-03-10 --severe

python3 scripts/car_maintenance.py status --km 84500 --in-service 2021-03-10 \
  --history '[{"task":"oil","km":63000,"date":"2026-01-15"}]' --json

python3 scripts/car_maintenance.py timeline \
  --km 84500 --in-service 2021-03-10 --annual-km 15000
```

Run the test suite:

```bash
python3 scripts/test_car_maintenance.py   # 58 assertions, stdlib only
```

## Who needs this

- **Any vehicle owner** (there are ~1.4 billion cars in the world, each with
  a maintenance schedule almost nobody tracks correctly).
- **Used-car buyers**: run `status` on the seller's numbers to see the
  deferred-maintenance backlog before you negotiate.
- **City commuters** unknowingly on severe-service schedules.
- **Households budgeting** an aging car: the 24-month timeline turns "car
  stuff always surprises me" into a quarterly line item.

## Honest limits

Generic intervals, not model-specific — **your owner's manual always wins**.
The tool is km-based (convert miles ×1.609). It schedules; it does not
diagnose symptoms or track warranty compliance. See `references/maintenance-model.md`
for the full model, task table, and worked examples.

MIT © 2026 Denis Voronin
