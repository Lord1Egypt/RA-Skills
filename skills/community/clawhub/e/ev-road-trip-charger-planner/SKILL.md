---
name: ev-road-trip-charger-planner
description: "Use when planning a long EV road trip — which chargers, how many stops, how long each. Physics-based consumption model (speed, temperature, cargo, elevation), a leg-by-leg stop solver with arrival buffers and charge-window taper math, pre-departure checklist (preconditioning, adapters, network accounts), and etiquette rules."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [ev, road-trip, charging, dc-fast, trip-planning, travel]
---

# EV Road-Trip Charger Planner

## Overview

The #1 fear that stops people from taking an EV on a road trip is "I'll get stranded or spend the whole vacation charging." The fix is a *plan with numbers*: consumption rises steeply with speed (aero drag), cold weather can add 20–35%, and DC fast charging tapers hard above ~80% — so a naive "charge to full every time" plan wastes hours, while a leg-by-leg plan that arrives with a 10–15% buffer and stops exactly as long as needed usually adds only 15–25 minutes per 3 hours of driving.

This skill computes an honest consumption model for your car class, then solves the stop sequence along your charger list (greedy with buffers), prints a leg table (km, arrive-SoC, charge minutes, depart-SoC, cost), and runs the pre-departure checklist: battery **preconditioning** (a cold pack charges at half speed), plug/adapter compatibility, one app per network, and hotel L2 strategy.

## When to Use

- Planning any EV trip longer than one tank of range (300+ km / 200+ mi)
- "Will my car make [route]? How many charging stops and how long?"
- Winter trip — consumption and charging-speed derating both get worse
- First long trip in a new (or borrowed/rental) EV
- Don't use for: daily commuting (home charging economics — different skill), hybrid vehicles, or tesla-only planning with the in-car nav already doing this well.

## Quick Start

```bash
# 1. Consumption reality-check for a winter highway trip
python3 scripts/evroadtrip.py consumption --car-class suv --speed 120 \
  --temp -8 --heat-pump yes --cargo 180

# 2. Solve the stop plan: 460 km route, chargers at 160/255/380, start 90%
python3 scripts/evroadtrip.py plan --battery 77 --usable 93 --start-soc 90 \
  --consumption 232 --dc-kw 190 --legs "160,135,125,75,65" \
  --names "I-95 EA,San Marcos,Tesla-Hallet,hotel" --price 0.48

# 3. Pre-departure checklist (preconditioning, adapters, apps)
python3 scripts/evroadtrip.py checklist --destination-country us --winter
```

## Consumption Model

```
base by class (140 Wh/km compact · 165 sedan · 195 SUV · 225 truck/van, at 110 km/h reference)
× speed factor: 1 + 0.045 × (v − 110)      (aero-dominated; +38% from 110→130)
× temp factor:  heat pump:  1 + 0.006 × max(0, 18 − T)
                resistive:  1 + 0.014 × max(0, 18 − T)
× cargo:        +2% per 100 kg above 150 kg load
× elevation:    ±1% per 10 m/km of net grade
```
Sanity floor/ceiling: real-world highway results land between the compact-warm and truck-cold extremes; if your car's dashboard average disagrees, use *its* number — the planner accepts a measured `--consumption` and skips the model.

## Stop Solver Rules

1. Drive legs only if arrival SoC ≥ **10% floor + weather buffer** (winter: +5%).
2. Charge to the **minimum of 80%** or next-leg-need + 10% — the taper above 80% roughly halves charge speed, so minutes pile up.
3. Effective DC rate = min(vehicle max, station max) × 0.75 average taper discount (early session is faster, late slower).
4. Lunch trick: a 35–40 min meal stop usually covers two driving segments — place the longest charge where you'd eat anyway.
5. Last leg to a hotel with L2 charging can arrive lower (10% floor) because you wake at 100%.

## Common Pitfalls

1. **No battery preconditioning on arrival at a DC charger.** A pack at 0°C takes power at half rate; use the car's "precondition for charging" (usually automatic when the charger is the active nav destination). The checklist enforces this.
2. **Charging past 80%.** From 10→80% takes ~25 min on a 150–250 kW car; 80→100% can take another 25–30. The solver refuses unless the next leg demands it.
3. **Assuming nameplate charger kW.** Station max, vehicle max, cable temperature, and concurrent vehicles (paired stalls share power) all derate; the 0.75 taper discount is the honest average.
4. **Skipping the network-app setup.** Many fast chargers (especially in Europe) are app-or-RFID only; card readers fail at the worst hour. Install + top-up accounts per network BEFORE the trip.
5. **Winter arrival buffers too thin.** A 10% plan margin becomes 3% with a headwind and −10°C; the solver adds +5% buffer below 0°C automatically.

## Verification Checklist

- [ ] Consumption number cross-checked against the car's own trip average (override if off >10%)
- [ ] Every leg arrival ≥ 10% (+5% winter) — no exceptions in the printed table
- [ ] No stop charges past 80% without the solver naming the reason
- [ ] Charger list reality: plugs (CCS1/CCS2/NACS/Tesla), max kW, network app noted
- [ ] Preconditioning route set in the car's nav (not just Google Maps)
- [ ] Hotel arrival night-1 charge plan exists (L2 destination or first-morning DC)

## Example Session

```
$ python3 scripts/evroadtrip.py plan --battery 77 --usable 93 --start-soc 90 \
    --consumption 232 --dc-kw 190 --legs "160,135,125,75,65" \
    --names "I-95 EA,San Marcos,Tesla-Hallet,junction,hotel" --price 0.48 --temp -8

EV ROAD-TRIP STOP PLAN — 560.0 km, usable 93 kWh, start 90%
consumption 232 Wh/km · DC min(vehicle 190 kW) ×0.75 taper · arrive floor 15% (winter)
════════════════════════════════════════════════════════════════
Leg  To             km   arrive    charge   depart     cost
1    I-95 EA       160      50%      8 min      70%     $9
2    San Marcos    135      36%      8 min      56%     $9
3    Tesla-Hallet  125      25%      8 min      45%     $9
4    junction       75      27%      8 min      47%     $9
5    hotel          65      30%    — done        —        —
TOTAL: 5 legs, 31 DC minutes, ~$36 DC charging
No leg below the winter floor (15%); no charge above 80%.
```
