---
name: car-battery-cold-start-doctor
description: Use when the car cranks slow or won't start in cold weather (or before winter) — converts measured battery voltage + temperature into CCA health verdicts, predicts no-start temperature from battery age/capacity loss, separates battery vs starter vs alternator failure signatures with 3 no-tool tests, and gives jump-start plus cold-start protocol order.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [car, battery, cold-start, cca, winter, alternator, diagnosis, roadside]
---

# Car Battery Cold-Start Doctor

## Overview

Cold mornings kill batteries in a specific, predictable way: at −18 °C a
lead-acid battery delivers ~40% of its rated cranking power while the
engine simultaneously demands ~2.5× more current (thick oil). A battery
that started the car fine all summer can cross the no-start line on the
first hard freeze — not randomly, but at a temperature you can compute
from resting voltage, age, and one cranking observation.

`scripts/battery_doctor.py` turns three numbers anyone can get (resting
voltage, temperature, battery age in years) into a health verdict, a
predicted no-start temperature, three no-tool tests that separate
battery / starter / alternator failures, and the right cold-morning
protocol — including when a jump is safe and when the battery is done
regardless.

## When to Use

- Car cranks slower than usual, especially mornings / after sitting.
- Won't crank at all: click / crank-no-start / nothing decision tree.
- Pre-winter check: will this battery survive the season?
- After a jump-start: is the battery recoverable or replace-now?
- Deciding battery tester readings at a shop (CCA measured vs rated).

**Don't use for:** EV traction batteries, hybrids' NiMH packs, AGM
start-stop systems with intelligent battery sensors (different
diagnostics), or 6 V classics — the model is 12 V lead-acid.

## How It Works

1. **Resting voltage → state of charge.** 12.7+ V ≈ 100%, 12.4 ≈ 75%,
   12.2 ≈ 50%, 12.0 ≈ 25%, <11.9 = discharged/possibly dead cell
   (a reading under ~10.5 V at rest = shorted cell, replace).
2. **Age → capacity fade.** Lead-acid loses ~5–8% of capacity per year
   average climate (faster with heat, deep discharges, short trips).
   Combined capacity × cold derate gives effective cold-cranking amps.
3. **Cold derate physics.** Available power falls roughly with
   temperature: 100% at 27 °C, ~65% at 0 °C, ~40% at −18 °C. Cranking
   demand rises ~2× by −18 °C (oil viscosity). The script finds the
   temperature where effective CCA < demand → your no-start line.
4. **Failure signature triage.** Three no-tool tests:
   - Headlights-bright-but-click → starter circuit/solenoid or cable.
   - Cranks-strong-but-no-start → fuel/ignition, NOT the battery.
   - Cranks-slow-then-dies → battery (or big parasitic drain).
   Plus dash voltmeter alternator check: 13.8–14.6 V running = charging.
5. **Verdict ladder.** OK / WATCH (this winter, likely) / REPLACE NOW
   (predicted no-start above your local design temperature, resting
   voltage <12.2 after a full charge, or dead-cell signature).
6. **Protocols.** Jump order (positive donor → positive dead → negative
   donor → negative ground on dead engine block), never let clamps
   touch, donor running; cold-start protocol (all loads off, crank 5 s
   bursts, 30 s rest, 3 attempts max); after-jump: 30+ min driving to
   put back real charge (idling barely charges).

## Using the Script

```bash
# morning no-crank: 12.1V rest, -5°C outside, 5-year-old battery, 550 CCA rated
python3 scripts/battery_doctor.py --resting-v 12.1 --temp-c -5 --age-years 5 --cca-rated 550

# pre-winter check on a healthy-reading battery
python3 scripts/battery_doctor.py --resting-v 12.55 --temp-c 10 --age-years 3 --cca-rated 600 \
  --design-low-c -25

# no voltmeter? age + temperature only (coarse mode)
python3 scripts/battery_doctor.py --age-years 6 --temp-c -12 --cca-rated 520 --no-meter
```

Outputs: SOC from resting voltage, effective CCA at current temperature,
demand estimate for your engine class, the temperature where this
battery stops starting the car, verdict (OK / WATCH / REPLACE NOW), the
failure-signature triage guide, and jump/cold-start protocol reminders.

## Common Pitfalls

1. **Testing right after driving.** Surface charge reads 13+ V for
   hours. True resting voltage: headlights on 30 s, off, wait 5 min,
   key off — or measure in the morning before anything.
2. **Reading voltage while cranking is the real test.** A healthy
   battery holds >10.5 V *while cranking* at −10 °C; below 9.5 V under
   load = insufficient. Resting voltage can look fine and still fail
   this (sulfation: voltage present, no current delivery).
3. **Blaming the battery when it's the starter or cables.** One click
   with bright headlights = starter circuit, not battery. The triage
   tests prevent a $180 battery that doesn't fix the problem.
4. **Assuming a jump "fixed" it.** A jump gets you going; it does not
   recharge a deeply discharged battery. 30+ minutes of driving or a
   proper charger — and if it deep-discharged twice, it's compromised.
5. **Ignoring parasitic drain.** Battery fine, alternator fine, but dies
   after sitting 3 days = something staying on (trunk light, dash cam,
   aftermarket alarm). Battery replacement won't fix it.
6. **Buying CCA you don't need, or too few.** Match the group size and
   meet/exceed OEM CCA. In cold climates +15–20% CCA headroom is cheap
   insurance; the script shows your real margin.
7. **Cranking until it grinds.** 5-second bursts, 30-second rests, three
   attempts. Long cranking overheats the starter and floods modern
   engines.

## Verification Checklist

- [ ] Resting voltage taken correctly (no surface charge; morning, key off).
- [ ] Battery age from the date code stamped on the case (letter+digit,
      e.g. D6 = April 2016-style; not the purchase receipt).
- [ ] Temperature = actual local low, not the daily high.
- [ ] Failure signature triage done BEFORE buying anything.
- [ ] If voltage-under-crank available: >10.5 V pass, <9.5 V fail noted.
- [ ] After any jump: 30+ min drive or charger session; retest next morning.
- [ ] Verdict REPLACE NOW → replaced before the first hard freeze, not after.
