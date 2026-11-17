# Car Battery Cold-Start Doctor

**The battery didn't "die suddenly" — it crossed a line you can compute.**
At −18 °C a 12 V battery delivers ~40% of its rated cranking power while
the engine demands ~2× more. Which morning it fails is arithmetic:
resting voltage × age fade × cold derate vs. demand.

## The Problem

- Shops sell you a battery on a hunch; you find out it was the starter
  solenoid (one click + bright headlights = not the battery).
- "It started fine yesterday" is exactly how age fade works — the curve
  approaches the demand line all summer, crosses it on the first freeze.
- A jump-start gets you moving but doesn't recharge a flat battery;
  idling barely charges. People repeat the no-start the next morning.
- Winter batteries die at the worst possible time: 6:40 AM, school run,
  −15 °C, no second car.

## What This Skill Does

`scripts/battery_doctor.py`:

```bash
python3 scripts/battery_doctor.py --resting-v 12.1 --temp-c -5 \
  --age-years 5 --cca-rated 550 --engine 6cyl-gas --design-low-c -25
```

- Resting voltage → state of charge (and the <11 V dead-cell signature)
- Age fade + cold derate → effective CCA right now vs engine demand
- **Predicted no-start temperature** for THIS battery (bisected model)
- Verdict: OK / WATCH / REPLACE NOW with reasons
- 6-row failure-signature triage: battery vs starter vs alternator vs
  parasitic drain — before you spend money
- Jump order and cold-start protocol (5 s cranks, 3 attempts, 30+ min
  drive after)

## Who Needs This

- Anyone in a freezing climate with a battery over 4 years old
- Morning no-start triage (click vs crank vs nothing)
- Post-jump decisions: recoverable or replace?
- Used-car buyers interpreting a marginal battery test

## Example

5-year-old 550 CCA battery, 6-cyl gas, resting 12.1 V, −5 °C outside,
local design low −25 °C: capacity ~70%, available power ~55% at −5 °C →
effective ~213 CCA vs demand ~293 CCA → **fails now** → REPLACE NOW,
before the tow truck. Same battery at 3 years with 12.5 V reads WATCH —
test under load, plan replacement this winter. The script prints the
full reasoning and the no-start line for each.

## License

MIT — see LICENSE.
