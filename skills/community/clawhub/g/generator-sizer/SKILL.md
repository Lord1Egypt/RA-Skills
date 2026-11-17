---
name: generator-sizer
description: Use when buying or running a backup generator during outages — builds an appliance-by-appliance load sheet with starting-surge multipliers (fridge 3x, well pump 3x), picks the right generator class (2k/3.5k/7.5k/13kW) from real surge math, computes gasoline/propane burn and storm-duration fuel needs, and flags CO/transfer-switch/backfeed safety before the power dies.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [generator, power-outage, emergency-prep, load-calculation, surge-watts, fuel-planning, safety]
---

# Generator Sizer

## Overview

Generators are sold on one number — "7500 watts!" — and that number is
usually **surge rating, not what you can run**. Meanwhile the appliances
that actually matter in an outage are motors: a refrigerator that runs at
150 W needs 450+ W for the two seconds its compressor starts, a ½ HP well
pump that runs at 1,000 W needs 3,000 W to start. Stack two motor starts
on top of your base load and a "7,500 W" generator that really delivers
6,000 W continuous trips its breaker, and the fridge never gets its turn.

`scripts/generator_sizer.py` does the audit nobody does: per-appliance
running watts, starting-surge multipliers, a priority-tier load-shed plan,
the honest generator class for your list, fuel burn per hour and per
storm, and the transfer-switch / CO-safety verdicts — before the storm,
not during it.

## When to Use

- Buying a portable or standby generator ("will a 3,500 W run my house?").
- Outage prep for a storm: which appliances can run, in what rotation.
- Sizing a generator for a well pump, furnace blower, sump pump, or medical
  device (the four loads that force a class jump).
- Deciding gasoline vs propane vs tri-fuel, and how much fuel a 48-hour
  outage actually consumes.
- Checking whether a neighbor's/friend's generator offer covers your needs.

**Don't use for:** whole-house automatic standby + ATS design (needs a
licensed electrician's load calculation per NEC 220), solar/battery
systems, or RV electrical planning — those have different load models.

## How It Works

1. **Appliance catalog.** Built-in table of ~30 common loads with running
   watts, surge multiplier, and priority tier (TIER 1 life-safety:
   furnace blower, sump, fridge, medical; TIER 2 comfort; TIER 3 luxury).
   Override or add your own wattages from nameplates.
2. **Load sheet.** Sums running watts; computes worst-case simultaneous
   surge = base load (all non-motor) + the single largest motor surge +
   running watts of motors already spinning. Staggered-start doctrine:
   you never start two compressors in the same second on purpose.
3. **Class verdict.** Snaps required continuous watts to the real market
   classes: 2,000 W inverter → 3,500 W → 7,500 W → 10–13,500 W → 22 kW
   standby, with what each class realistically runs (a 2,000 W inverter
   runs a fridge + lights + internet, period).
4. **Fuel model.** Gasoline burn ≈ 0.05 gal/h base + ~0.095 gal/h per
   delivered kW at load (so a 7,500 W unit at 50% ≈ 0.4 gal/h); propane
   burns ~2× by volume with a 20 lb tank (4.7 gal) factored in. Output:
   hours per tank and gallons needed for your storm duration at your
   actual load fraction — not the marketing number at 25% load.
5. **Safety gates.** 240 V loads (well pump, furnace on 240) demand a
   transfer switch or breaker interlock — backfeeding a dryer outlet is
   an electrocution hazard for line workers and illegal. CO doctrine:
   20+ ft from any window/door/vent, never in a garage or under a deck,
   battery CO alarm indoors. Inverter-class needed for sensitive
   electronics if THD matters (CPAP, oxygen concentrator).

## Using the Script

```bash
# essentials for a storm: fridge + freezer + sump + furnace blower + lights/router
python3 scripts/generator_sizer.py \
  --appliances fridge freezer sump-pump furnace-blower lights-10 router \
  --storm-hours 48

# adding a well pump (the classic class-jumper) with custom watts
python3 scripts/generator_sizer.py \
  --appliances fridge freezer well-pump furnace-blower lights-10 \
  --custom microwave:1100:1.5 --fuel propane --storm-hours 24

# what does my existing 3500W generator actually carry?
python3 scripts/generator_sizer.py --appliances fridge sump-pump lights-10 router cpap \
  --generator-watts 3500 --check-only
```

Outputs: tiered load sheet (running W, surge W, tier), worst-case surge
event, required continuous watts, generator class verdict with the
"skipped" appliances if your `--generator-watts` is too small, staggered
start order, fuel plan (gal/h at your load fraction, hours per tank,
gallons per storm), and a safety checklist with the transfer-switch flag.

## Common Pitfalls

1. **Sizing by surge rating.** "7,500 W" units deliver ~6,000 W
   continuous. Size to continuous watts + one motor surge, never the box
   number.
2. **Forgetting starting surge entirely.** Motors need 2–3× for 1–3
   seconds. Two motors starting together (fridge + sump after a power
   blip) is exactly when generators stall.
3. **Assuming "240V plug = house wiring."** Any connection to home wiring
   legally requires a transfer switch or listed interlock. Backfeed cords
   kill linemen and melt dryer outlets.
4. **Fuel math from the manual.** Runtime quotes are at 25% load. Your
   real load fraction doubles or triples the burn; a 48 h storm on a
   7,500 W genset at 50% needs ~20 gal of gasoline stored safely.
5. **Running it "just for an hour" in the garage.** CO kills at low
   concentrations; generators run outdoors 20+ ft from openings, with a
   battery CO alarm indoors. More deaths come from CO than from wiring.
6. **Ignoring altitude.** Gasoline engines lose ~3% output per 1,000 ft
   above sea level — at 8,000 ft a "7,500 W" is a 6,000 W. The script
   takes `--elevation-ft`.
7. **Forgetting the furnace blower is a motor.** Gas furnace heat needs
   electricity for the blower (400–800 W, 3× surge). "I have gas heat"
   households discover this in the first outage.

## Verification Checklist

- [ ] Every Tier-1 appliance entered with nameplate watts (not guesses).
- [ ] Largest-motor surge added to total running load for the sizing check.
- [ ] Generator class ≥ required continuous watts with ≥15% headroom.
- [ ] 240 V loads → transfer switch/interlock identified; no backfeed plan.
- [ ] Fuel plan covers storm duration at REAL load fraction + 25% reserve.
- [ ] CO safety: 20 ft clearance, outdoor only, battery CO alarm indoors.
- [ ] Elevation derate applied if above 3,000 ft.
- [ ] Dry-run test: run the generator + top-3 loads for 30 min before storm
      season, log voltage sag on motor starts.
