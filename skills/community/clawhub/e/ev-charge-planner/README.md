# EV Charge Planner

**Charge smarter, not harder: the home EV charging math nobody does.**

Over 20 million drivers now plug in at home — and most get the basics wrong:
they pay peak rates because they never enrolled in time-of-use plans, they
buy 48A chargers that their panel can't safely back, they compare EV costs
to gas using sticker numbers, and they're surprised when a "60 kWh" fill
draws 67 kWh from the wall.

## The problem
1. **Rate blindness.** The overnight off-peak window is 2-3× cheaper than
   peak in most US markets. Skipping TOU enrollment wastes $300-600/year
   for an average driver — the single biggest lever in EV ownership.
2. **Loss blindness.** Charging is ~90% efficient wall-to-battery. Every
   "my fill costs $X" mental math is ~11% optimistic.
3. **Panel blindness.** Continuous EV loads must respect the 80% rule;
   bigger charger ≠ better if the panel can't back it.
4. **Comparison blindness.** "Cheaper than gas!" depends entirely on the
   public-charging mix — DC fast charging at $0.48/kWh costs MORE per mile
   than a 30-mpg car at $4.10 gas.

## What this toolkit does
- `session` — charge time, wall kWh, cost, battery %, miles added, panel
  load check vs the 80% rule, and latest-start time for a departure deadline.
- `tou` — off-peak window planning: fit check with departure buffer,
  latest safe start, and when it doesn't fit — three priced exits
  (more amperage / accept partial / regular-rate tail cost).
- `compare` — honest monthly EV-vs-gas cost with your rates, your mileage,
  your public-charging percentage.

## Quick start
```bash
# Tonight's session: 32 kWh into a 60 kWh pack, 7.4 kW wallbox
python3 scripts/ev_planner.py session --kwh-needed 32 --kw 7.4 \
    --rate 0.11 --battery 60 --house-amps 28 --panel-amps 100 --departure "07:00"

# Does a 44 kWh fill fit the 23:00-07:00 window before a 06:30 departure?
python3 scripts/ev_planner.py tou --kwh-needed 44 --kw 11 \
    --offpeak "23:00-07:00" --rate 0.11 --regular-rate 0.34 \
    --departure "06:30" --buffer-min 30

# Real monthly comparison, 20% public charging
python3 scripts/ev_planner.py compare --miles-month 900 --ev-mi-per-kwh 3.4 \
    --home-rate 0.14 --public-pct 20 --public-rate 0.48 \
    --gas-price 4.10 --gas-mpg 30
```

Pure Python 3 stdlib. Offline. No accounts, no cloud, no telemetry.

## Who needs this
- New EV owners setting up home charging for the first time
- Wallbox buyers sizing amperage against a real panel
- TOU-curious owners deciding whether to switch rate plans
- Anyone asked "so is it actually cheaper than gas?" who wants a defensible
  number with assumptions on the table

## License
MIT — see LICENSE.
