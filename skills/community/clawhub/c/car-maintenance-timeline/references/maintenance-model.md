# The Maintenance Model

This document defines the computation behind `car_maintenance.py`: the
dual-interval model, severe service, status classification, history handling,
and projection math — plus the full default task library and worked examples.

## 1. Why dual intervals

Manufacturers express nearly every service as **every N km OR M months,
whichever comes first**. The two clocks measure different degradation:

- **Distance** proxies mechanical wear and heat cycles: engine hours at
  operating temperature, friction, clutch/brake cycles, particulate load.
- **Time** proxies chemistry: motor oil oxidizes and additive packages
  deplete in the crankcase; brake fluid is hygroscopic (absorbs atmospheric
  moisture, dropping its boiling point); coolant inhibitors deplete; rubber
  (wipers, belts, tires) cures and cracks; batteries sulfate.

A car doing 4,000 km/year of short trips can be *harder* on oil than one
doing 25,000 km of highway — short trips never fully boil off fuel and
condensation from the oil. That is also why "severe service" usually means
*city*, not racing.

## 2. The evaluation model

For each task, keep two anchors from the last completed service (or the
no-history default, §4):

```
km_due_at    = last_done_km   + interval_km
date_due_at  = last_done_date + interval_months   (calendar months)
```

The **next event** is whichever of the two arrives first *in the owner's
timeline*. To compare them, convert the km event to a date using the owner's
pace:

```
km_per_day   = annual_km / 365.25
days_to_km   = (km_due_at - current_km) / km_per_day
km_event_date = today + days_to_km
```

The task fires when `current_km >= km_due_at` **or** `today >= date_due_at`.
The reason string reports which clock won and by how much
(`overdue by km (+2,400 km vs interval)`).

### Status classification

| Status | Rule |
|---|---|
| `OVERDUE` | km clock or time clock already past due |
| `DUE SOON` | ≤ 20% of the km interval remains, or ≤ 30 days remain on the time clock |
| `OK` | anything else |

Sorting: status rank first (OVERDUE < DUE SOON < OK), then priority
(safety-critical < wear-item < standard), then soonest next event.

## 3. Severe service

Manufacturer "severe" conditions, consistently defined across brands:

- Repeated short trips (< ~10 km), especially in cold weather
- Extensive stop-and-go / city driving in hot weather
- Towing, hauling, or mountain driving
- Dusty, sandy, or salted (de-iced) roads
- Extended idling

Effect in the model: tasks with an explicit severe column switch to it
(oil 10,000→5,000 km and 12→6 mo; transmission fluid 100,000→60,000 km and
120→72 mo). Tasks without an explicit severe column take a global ×0.75
multiplier on their km interval (time intervals usually already cover the
chemistry). Most urban commuting qualifies for severe — this is the single
most common systematic error owners make (running long intervals on a
short-trip car).

## 4. No-history default & history entries

Without `--history`, every task anchors to **in-service @ 0 km** — i.e.
assumed never done. On a used car with unknown history this deliberately
over-reports: treat it as "baseline everything cheap" advice, not 13
simultaneous failures. Priority order for baselining: safety-critical →
fluids (oil, brake, coolant) → filters → the rest.

History entries look like:

```json
[{"task": "oil", "km": 63000, "date": "2026-01-15"},
 {"task": "cabin_filter", "km": 85000, "date": "2026-03-02"}]
```

Task ids accept friendly names (normalized, e.g. "oil change" → `oil`).
Each entry re-anchors *both* clocks of that task. Unknown ids are rejected
with a list of valid ids rather than silently ignored.

## 5. Annual mileage and projection

`annual_km` is explicit (`--annual-km`) or derived:

```
months   = months_elapsed(in_service, today)
annual   = current_km / months * 12        (with a floor for <1-month-old cars)
```

`timeline` walks each task forward across the window (default 24 months):
evaluate → record the next event with its projected odometer reading →
advance that task's anchor past the event → repeat until past the window
end. Events are reported grouped by month with cost range and DIY level.
A hard iteration cap (200/task) prevents infinite loops on degenerate inputs.

Worked example — 84,500 km, in service 2021-03-10, severe, oil done at
63,000 km on 2026-01-15:

```
km_due_at   = 63,000 + 5,000            = 68,000 km   (past: 84,500)
date_due_at = 2026-01-15 + 6 months     = 2026-07-15  (past today 2026-08-27)
status      = OVERDUE — overdue by both clocks
```

## 6. Task library (defaults)

| id | Task | km | mo | severe km | severe mo | priority | cost (USD) | DIY |
|---|---|---|---|---|---|---|---|---|
| oil | Engine oil & filter change | 10,000 | 12 | 5,000 | 6 | wear-item | 40–90 | Easy |
| tire_rotation | Tire rotation | 8,000 | 6 | — | — | safety-critical | 20–50 | Easy |
| engine_air_filter | Engine air filter | 20,000 | 24 | — | — | wear-item | 15–40 | Easy |
| cabin_filter | Cabin (pollen) filter | 20,000 | 24 | — | — | standard | 20–60 | Easy |
| brake_fluid | Brake fluid replacement | 40,000 | 24 | — | — | safety-critical | 80–150 | Moderate |
| spark_plugs | Spark plugs | 60,000 | 48 | — | — | wear-item | 100–250 | Moderate |
| coolant | Engine coolant replacement | 100,000 first, then 50,000 | 60 then 36 | — | — | wear-item | 90–180 | Moderate |
| transmission_fluid | Transmission fluid replacement | 100,000 | 120 | 60,000 | 72 | wear-item | 150–350 | Hard |
| drive_belt | Drive/serpentine belt inspection | 100,000 | 120 | — | — | wear-item | 0–120 | Moderate |
| battery_test | Battery load test | — | 48 (replace ~60) | — | — | wear-item | 0–30 | Easy |
| wipers | Wiper blades | — | 12 | — | — | safety-critical | 15–50 | Easy |
| inspection | Annual inspection / MOT | — | 12 | — | — | safety-critical | 30–120 | — |
| tire_swap | Winter/summer tire swap | — | 6 | — | — | standard | 40–100 | Moderate |

Costs are independent-shop/retail US-anchored ranges, included for
order-of-magnitude budgeting and upsell sanity checks, not quotes.

## 7. Priority classes

- **safety-critical** — tire rotation (uneven wear → hydroplaning), brake
  fluid (boiling point), wipers, mandatory inspection. Surfaced first.
- **wear-item** — oil, filters, plugs, fluids, belt, battery: deferring has
  compounding cost but rarely immediate danger.
- **standard** — comfort/seasonal (cabin filter, tire swaps).

## 8. Worked examples

**A. Low-mileage retiree.** 4,000 km/yr, oil never changed in 14 months.
Time clock wins: `date_due_at = in_service + 12 mo` → OVERDUE by time.
Chemistry does not care that the car "barely drives."

**B. Sales rep.** 35,000 km/yr highway. km clock wins every time; the time
column is nearly irrelevant; costs concentrate in oil, tires, brakes.

**C. City commuter (severe).** 12,000 km/yr of short trips. `--severe`:
oil due every 5,000 km ≈ every 5 months — matching the sludged-intake
reality of engines that never warm up fully.

## 9. Limitations & disclaimer

- Generic defaults. Intervals vary by engine, transmission, fuel type
  (diesels: fuel filters; EVs: almost none of this table applies), and
  market. **The owner's manual overrides everything here.**
- km-based by design; convert miles ×1.609.
- Inspection/MOT deadlines are jurisdiction-specific dates, not merely
  "12 months from first registration" — track the actual legal date.
- Advisory decision-support, not a mechanic: symptoms (noises, lights,
  leaks, smells) outrank any schedule.

MIT © 2026 Denis Voronin
