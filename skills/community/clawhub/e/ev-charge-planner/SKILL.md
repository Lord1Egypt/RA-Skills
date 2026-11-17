---
name: ev-charge-planner
description: "Use when planning home EV charging — computes charge time and cost for a session (with wall-to-battery losses and breaker load checks), plans overnight charging inside time-of-use off-peak windows (latest safe start, doesn't-fit options), and compares monthly fuel cost EV vs gas car including public-charging mix; handles kW/amps, departure deadlines, and cold-day buffer advice."
version: 1.0.1
author: Denis Voronin
license: MIT
tags: [ev, electric-vehicle, charging, electricity-rates, energy, personal-finance]
---

# EV Charge Planner

## Overview
Tens of millions of drivers now charge an EV at home, and nearly all of them
get the math wrong in the same ways: they forget ~10% wall-to-battery losses
(a "60 kWh" fill draws ~67 kWh from the meter), they charge at 7¢-per-kWh
worse rates than they could because they never learned their utility's
time-of-use windows, they size charger amperage against panel capacity by
vibe, and they compare EV vs gas costs using the EPA sticker efficiency
instead of their own.

This skill is three calculators:

1. **session** — kWh needed + charger kW + rate → hours:minutes to target,
   wall energy, cost, battery %, miles added, panel/breaker load check
   (80% continuous guidance), and latest start time for a departure deadline.
2. **tou** — off-peak window planning: does the charge fit before your
   departure (with buffer)? Latest safe start? If not: raise amperage /
   accept partial / price the regular-rate tail.
3. **compare** — monthly EV vs gas cost at YOUR prices and mileage, with the
   public-charging mix that quietly destroys the economics.

Pure stdlib, offline.

## When to Use
- "How long to add 40 kWh on my 7.4 kW wallbox?" / "What will it cost?"
- "Off-peak is 23:00-07:00 and I leave at 6:30 — can I fit 44 kWh?"
- "Is the EV actually cheaper than my 30-mpg car at $4.10 gas?"
- "Can my 100A panel handle a 48A charger plus the house?"
- "My charger asks for amps — what do 16/32/40/48A mean in kW?"
- Sizing a wallbox purchase vs charging needs (power math side)

**Don't use for:** DC fast-charging road-trip planning (different curve —
charge rates fall steeply above 80%), off-grid/solar sizing (needs panel
production data), or utility-bill auditing (only the EV slice is modeled).

## How It Works — Numbered Steps
1. Know your inputs: battery usable kWh, charger kW (amps × 0.24 at 240V —
   32A ≈ 7.7 kW, 48A ≈ 11.5 kW), your rate schedule (flat vs TOU windows),
   and your car's real mi/kWh (dashboard average, not the sticker).
2. Session math:
   ```
   python3 scripts/ev_planner.py session --kwh-needed 32 --kw 7.4 \
       --rate 0.23 --battery 60 --house-amps 28 --panel-amps 100 \
       --departure "07:00"
   ```
   → 4h48m, 35.6 kWh from the wall, $8.18, panel at 59% (OK), start 02:11.
3. TOU planning (where the real savings live):
   ```
   python3 scripts/ev_planner.py tou --kwh-needed 44 --kw 11 \
       --offpeak "23:00-07:00" --rate 0.11 --regular-rate 0.34 \
       --departure "06:30" --buffer-min 30
   ```
   → fits with 2h33m slack, latest start 01:33, saves $11.24/session vs
   charging at the regular rate.
4. When it does NOT fit, the tool prices all three exits: raise charger kW,
   accept a partial charge (with miles), or pay the regular-rate tail.
5. Monthly comparison:
   ```
   python3 scripts/ev_planner.py compare --miles-month 900 --ev-mi-per-kwh 3.4 \
       --home-rate 0.14 --public-pct 20 --public-rate 0.48 \
       --gas-price 4.10 --gas-mpg 30
   ```
   → EV $61/mo vs gas $123/mo → $742/yr saved.
6. Set the car/EVSE departure-and-target once; re-run when rates, seasons,
   or commute change.

## The Physics (short version)
- **Wall ≠ battery.** Charging is ~88-92% efficient; the tool uses 90%.
  A 60 kWh fill at $0.14/kWh costs $9.33, not $8.40.
- **kW from amps @240V:** kW = amps × 0.24. Level 2 amperage ladder:
  16A=3.8, 24A=5.8, 32A=7.7, 40A=9.6, 48A=11.5 kW.
- **Panel guidance:** continuous loads (EVSE) should stay under 80% of
  breaker/panel rating. 48A charging + evening house load can breach this
  on a 100A panel — the tool flags it and computes the safe kW.
- **TOU arbitrage:** typical US spreads run 2-3× between off-peak and peak
  ($0.11 vs $0.34 here). Overnight-only charging is the single highest-ROI
  habit in EV ownership — worth $300-600/yr for an average driver.
- **Cold days:** batteries condition/warm post-charge; finishing 30 min
  before departure preserves range. Hence the buffer default.

## Common Pitfalls
1. **Charging "to full" every night.** Most batteries are happiest in the
   20-80% band; nightly 80% + 100% before trips is the standard protocol.
2. **Ignoring TOU enrollment.** Many utilities default you to flat rate;
   enrolling in EV/TOU plans is a 15-minute phone call that halves charging
   cost. The compare tool shows the spread.
3. **Counting public DC charging as 'basically home charging.'** At
   $0.40-0.60/kWh, DC fast charging costs MORE per mile than a 30-mpg car
   at $4 gas. The public-mix percentage exists to keep this honest.
4. **Sizing the charger by 'more is better.'** A 48A EVSE on a 100A panel
   with a heat pump and an electric dryer is a load-management problem;
   32A covers 40+ miles/hour of charging anyway — most overnight needs fit.
5. **Assuming the sticker efficiency.** Cold weather, high speed, and
   hills move real consumption 10-30%. Use the dashboard's lifetime mi/kWh.
6. **Departing mid-charge in winter.** The battery is warm while charging;
   a 30-minute post-charge buffer lets preconditioning work from grid power
   instead of battery.
7. **Forgetting vampire loads in compare.** If the EV lets you enter
   mileage only, add 5-10% for climate/sentinel drain on the kWh side.

## Example
```
Owner: 62-kWh EV, new 7.4 kW wallbox, off-peak 23:00-07:00 @ $0.11,
departs 06:30. Drives 900 mi/mo, gas alternative is 30 mpg @ $4.10.

$ session --kwh-needed 32 --kw 7.4 --rate 0.11 --departure "07:00"
→ 4h48m, $4.36 at off-peak (vs $8.18 flat-rate) — start at 02:11.

$ tou --kwh-needed 44 --kw 11 --offpeak "23:00-07:00" --rate 0.11 \
      --regular-rate 0.34 --departure "06:30"
→ FITS, slack 2h33m, latest start 01:33, saves $11.24/session.

$ compare --miles-month 900 --ev-mi-per-kwh 3.4 --home-rate 0.11 \
      --public-pct 10 --public-rate 0.48 --gas-price 4.10 --gas-mpg 30
→ EV ~$40/mo vs gas $123/mo → saves ~$1000/yr charging at home,
  but only $260/yr if 50% of charging is public DC.
```

## References
- `references/charging-physics.md` — efficiency losses, amperage/kW tables,
  panel load management, battery 20-80 protocol, cold-weather effects.
- `references/tou-rates-playbook.md` — how TOU plans work, typical US
  rate spreads, enrollment steps, metering options, when flat-rate beats TOU.
