# EV Road-Trip Charger Planner

**How many stops, how long each, and where — decided by physics before you leave.**

Range anxiety on road trips is a planning problem, not a car problem: EV
highway consumption rises steeply with speed and cold, DC charging tapers
hard above 80%, and a naive "fill it full every time" plan wastes an hour a
day. This skill computes an honest consumption model for your car class
(speed factor, heat-pump vs resistive cold penalty, cargo, net grade), then
solves the stop sequence along your charger list with arrival floors
(≥10%, +5% in winter), 80% ceiling doctrine, taper-discounted charge
minutes, and per-stop cost — plus the pre-departure checklist (battery
preconditioning, adapters, one app per network, hotel L2 confirmation).

## What it does

- **`consumption`** — Wh/km physics stack with each factor printed, so you
  can argue with it; dashboard-average override encouraged.
- **`range`** — usable-kWh range at any SoC.
- **`plan`** — leg-by-leg table: km, arrive SoC, charge minutes (0.75 taper
  discount), depart SoC, cost; flags any leg below floor and any charge past
  80% with the reason; winter buffers automatic below 0°C.
- **`checklist`** — 9-item pre-departure gate incl. the #1 mistake: arriving
  at a DC charger without battery preconditioning (half-speed cold pack).

## Who needs this

First-time EV road-trippers, renters borrowing an EV for vacation, families
planning winter ski trips, and anyone whose nav app's ETA keeps mutating.

## Usage

```bash
python3 scripts/evroadtrip.py consumption --car-class suv --speed 120 \
  --temp -8 --heat-pump yes --cargo 180
python3 scripts/evroadtrip.py plan --battery 77 --usable 93 --start-soc 90 \
  --consumption 232 --dc-kw 190 --legs "160,135,125,75,65" \
  --names "home,I-95 EA,San Marcos,Tesla adapter,hotel" --price 0.48
python3 scripts/evroadtrip.py checklist --winter
```

Model + field notes: `references/charging-model.md`.

## License

MIT © 2026 Denis Voronin
