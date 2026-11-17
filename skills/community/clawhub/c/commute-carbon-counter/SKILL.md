---
name: commute-carbon-counter
description: "Use when you want to know the real carbon footprint of your daily commute or travel habits, when deciding between commuting modes (car vs transit vs bike vs carpool vs EV), when tracking a personal emissions goal, or when preparing an environmental impact report — logs every trip (mode, distance, passengers), computes kg CO2 per trip/week/month using per-passenger-km emission factors for 14 transport modes, compares against your car baseline, projects your annual trajectory, and shows what changed your footprint most."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [carbon-footprint, commute, sustainability, climate, tracking, transport]
---

# Commute Carbon Counter

## Overview

Most people's largest personal emissions source is how they move: commuting alone by car typically produces 2–4 tonnes of CO2 per year — often more than home heating. Yet almost nobody can answer "how much CO2 was my commute this month, and what actually moved the number?" Carbon footprint calculators ask 40 questions once a year and produce a single opaque number that changes nothing.

This skill treats your mobility like a measurable system: log trips (10 seconds), get per-trip/per-week/per-month kg CO2, compare modes honestly (per-passenger-km, carpooling divided by heads), track your trajectory against a personal budget, and see a ranked "what changed" list — the two trips a week that account for half your footprint, the carpool switch that cut 30%.

Emission factors are per-passenger-km averages synthesized from published transport LCA sources (UK DEFRA/BEIS, EPA, EEA — see references). They are planning-grade, not certification-grade: good enough to compare modes and track trends, not to offset certified tons.

## When to Use

- **Deciding between commuting modes** — "is driving to the station vs bus-to-station actually different?"
- **Tracking a personal emissions goal** — monthly report vs your kg budget
- **After changing something** — new job, moved house, EV purchase, started carpooling: before/after comparison
- **Team/company commute challenge** — export the log, sum per participant
- **Curiosity with stakes** — "one flight or a year of commuting?"
- Don't use for: formal carbon accounting (Scope 1/2/3 reporting, offset certification) — factors are averages, not your specific vehicle.

## Commands

```bash
# Log a trip (mode, km one-way is auto doubled unless --oneway given)
python3 scripts/commute_carbon.py log --mode car --km 18 --note "office"
python3 scripts/commute_carbon.py log --mode carpool --km 18 --passengers 3 --note "office w/ neighbors"
python3 scripts/commute_carbon.py log --mode metro --km 9 --date 2026-09-05
python3 scripts/commute_carbon.py log --mode bike --km 6

# Quick one-off comparison — no logging
python3 scripts/commute_carbon.py compare --km 18

# Reports
python3 scripts/commute_carbon.py week           # last 7 days
python3 scripts/commute_carbon.py month          # last 30 days
python3 scripts/commute_carbon.py year           # annualized trajectory vs budget

# Emission factors table (what the math uses)
python3 scripts/commute_carbon.py factors

# Manage log
python3 scripts/commute_carbon.py log-list --limit 20
python3 scripts/commute_carbon.py export --csv trips.csv
```

Trips live in `~/.commute-carbon.json` (`--file` to override).

## Modes and Factors (g CO2 per passenger-km)

| Mode | Factor | Notes |
|---|---|---|
| car | 192 | average ICE, solo driver |
| carpool | 192 / passengers | same vehicle, split by heads |
| ev | 53 | average grid mix; ~0 in clean grids |
| motorcycle | 103 | |
| bus | 97 | urban diesel average |
| coach | 27 | intercity/express bus |
| metro | 35 | heavy rail electric |
| tram | 30 | light rail |
| train | 41 | regional rail |
| bike | 0 | |
| e-bike | 5 | charging emissions only |
| walk | 0 | |
| scooter | 8 | shared e-scooter, incl. rebalancing |
| plane | 255 | short-haul per passenger-km |

## How Reports Read

```
Week 2026-09-02 → 2026-09-08      9 trips, 214 km
  CO2: 14.2 kg   (baseline all-car: 41.1 kg  →  65% saved)
  by mode:
    car      ██████████████ 9.4 kg  (3 trips)
    metro    ███ 1.2 kg  (4 trips)
    bike     (0.0 kg)  (2 trips)
  top trips:
    1. 2026-09-03 car 36 km → 6.9 kg   office
    2. 2026-09-06 car 22 km → 4.2 kg   ikea
  trajectory: 0.74 t/yr — under 1.0 t budget ✅
```

`year` annualizes the current log and compares to your budget (default 1000 kg personal transport CO2/yr, roughly aligned with 1.5°C-lifestyle targets for mobility; set your own with `--budget`).

## Common Pitfalls

1. **Comparing per-vehicle instead of per-passenger.** A full car is *greener than the train per person*; a solo driver is not. Always log `--passengers` for carpools.
2. **Ignoring the return trip.** The tool doubles distance by default (commutes are round trips); use `--oneway` for one-ways or you'll double-count.
3. **Treating EV as zero.** Grid mix matters — the factor here (~53 g/pkm) reflects an average grid; a coal-heavy grid pushes it toward 100+, hydro pulls it near 10.
4. **Forgetting the counterfactual.** "Bus emitted 2 kg" means little alone; the report's *baseline all-car* column is the number that tells you what your choices saved.
5. **Comparing to national averages.** Per-capita transport footprints vary 5× by country; compare to your own baseline and budget, not to headlines.
6. **Offsetting based on this.** Factors are planning-grade averages. If you buy offsets, use a measured/calculated tonnage from a certification body, not this log.

## Verification Checklist

- [ ] A typical week is logged (don't aim for perfection — patterns beat completeness)
- [ ] `factors` reviewed — swap in your local grid/vehicle numbers if you know them
- [ ] `week` runs and the baseline comparison looks sane (savings % vs your mode mix)
- [ ] `--budget` set to something meaningful for you (or accepted the 1 t default consciously)

## One-Shot Recipes

**"Subway vs driving to work — does it matter?"**
```bash
python3 scripts/commute_carbon.py compare --km 14
```

**Track a real week, then decide**
```bash
for d in mon tue wed thu fri; do python3 scripts/commute_carbon.py log --mode metro --km 9; done
python3 scripts/commute_carbon.py log --mode car --km 24 --note "sat errands"
python3 scripts/commute_carbon.py week
```

**EV purchase, before/after**
```bash
python3 scripts/commute_carbon.py month                 # before
# ...switch modes in your log...
python3 scripts/commute_carbon.py month                 # after
```
