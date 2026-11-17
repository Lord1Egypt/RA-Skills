---
name: fuel-economy-driving-coach
description: "Use when you want to spend less on fuel — turns driving-style talk into numbers: computes your engine's BSFC-based theoretical floor, prices each habit (idling, aggressive acceleration, 75 vs 60 mph, roof box, underinflated tires, AC vs windows) in real $/yr for YOUR mileage and gas price, and ranks fixes by payback."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [fuel-economy, driving, car, savings, mpg, hypermiling]
---

# Fuel Economy Driving Coach

## Overview

"Drive gentler, save gas" is true and useless. The useful form is arithmetic: your car has a **physics floor** (roughly 20-25% of fuel energy reaches the wheels; aero drag rises with the cube of speed), every habit sits on top of that floor, and each habit has a **dollar price for your actual mileage and gas price**. A roof box costs a Camry driver with a 12k-mile year about $85/yr; the same box on a once-a-month errand car costs $7. Same advice, opposite verdicts — which is why generic lists fail.

This skill computes: (1) your car's theoretical floor from weight and drag so expectations are honest, (2) the $/yr price of each bad habit at your mileage/price, (3) ranked fixes by annual saving, and (4) trip-level coaching (why this trip burned 30% more than usual).

## When to Use

- Fuel spending feels high and you want to know WHICH habits actually cost money — for your car, not generically
- Deciding roof box / bike rack / winter tires / fuel grade by total cost, not folklore
- Comparing a commute change (route, speed, departure time) in $/month
- A sudden MPG drop (10%+ over 2+ tanks) → diagnosis router (underinflation, dragging brake, MAF/oxygen sensor, thermostat stuck open)
- Planning a long road trip: cruise speed trade-off in $ and minutes
- Buying decision: does the hybrid premium pay back at your mileage?

Don't use for: EVs (different physics — regen makes habits nearly free), diesel trucks fleet management, or racing.

## The Physics (compressed)

- **Engine floor**: ~20-25% tank-to-wheel for gasoline engines (hybrids recover some via Atkinson cycle + regen; diesels ~30-35%).
- **Aero drag ∝ v³**: 60→75 mph costs most passenger cars 15-20% more fuel. The minutes saved are linear; the fuel is cubic.
- **Rolling resistance ∝ weight**: +100 lb ≈ +1-2% consumption. Roof cargo adds both weight and brutal drag: +10-25% highway.
- **Idle burns ~0.3-0.6 gal/h** for nothing. 10 min/day of drive-through + warming = $130-260/yr at $3.50/gal.
- **Underinflation**: every 1 psi below placard ≈ +0.4% consumption; 8 psi low ≈ +3-4% and wrecks tire life.
- **Aggressive driving** (jack-rabbit starts + hard braking) costs 10-40% city / 15% highway (US DOE range) because braking discards kinetic energy you paid for.
- **AC vs windows**: AC ≈ 3-10% of fuel; windows at highway speed ≈ 2-5% aero penalty. Below ~45 mph windows win; above ~55-60 mph AC wins. City: windows.
- **Cold engine**: first 3-5 minutes run rich (up to +50% consumption on short trips). Combining errands into one warm loop beats three cold starts.
- **Fuel grade**: modern engines run fine on regular via knock-sensor timing pull-back; premium in a regular car is 100% waste. Premium-required engines on regular: power loss + possible long-term risk — check the manual.
- **Winter blend + idling**: winter MPG 8-12% lower is normal (blend, warm-up, dense cold air = more drag). Don't chase a ghost.

## The Ranking That Matters (typical 15k mi/yr, 30 MPG car, $3.50/gal)

| Habit change | Saving band | Notes |
|---|---|---|
| Aggressive → smooth driving | $150-400/yr | Biggest single lever for city drivers |
| 75 → 65 mph highway | $120-200/yr | ~8-15% highway fuel; costs minutes — see trip math |
| Roof box removed (when unused) | $60-160/yr | +10-25% highway when mounted |
| Tires to placard + monthly check | $50-130/yr | Plus tire life, safety |
| No idling >30-60 s (vs 10 min/day) | $110-220/yr | Start-stop systems exist for this reason |
| Errands combined (3 cold starts → 1 loop) | $60-120/yr | Short-trip drivers feel this most |
| Trunk junk (-100 lb) | $30-70/yr | Rolling resistance |
| AC discipline (windows <45 mph) | $30-90/yr | Climate-dependent |

Fix leaks before spigots: **underinflation and roof boxes dwarf every "fuel additive" fantasy**. There is no bottled product that buys back real MPG.

## MPG Drop Diagnosis (>10% over 2+ tanks, driving unchanged)

Ranked by likelihood × cheapness:
1. Tires 5+ psi low (free check) — seasonal temp drop alone explains 2-4 psi
2. Different driving/route/season (winter normal drop 8-12%) — log before panicking
3. Dragging brake (wheel hot after gentle drive = smoking gun) / stuck caliper
4. Dirty air filter (mostly hurts acceleration; real MPG effect at severe clog on older cars)
5. Oxygen sensor aging (lazy sensor skews mixture; classic gradual 10-15% loss + check-engine sometimes late)
6. Thermostat stuck open (engine never fully warms, always runs rich)
7. Misfire / bad plug / coil (usually check-engine by now; rough idle)
8. Fuel leak or theft (do the math per tank, not per mood)

## Trip Coaching (why this tank was 30% worse)

Ask: what changed? New route with hills/stops? Headwind day (crosswind +10-15% highway)? Roof load? Cold snap? Trailer? Heavy passengers? Compare same-route same-weather baselines, not tank averages. Log per-tank: date, miles, gallons, notes (route/load/weather). 3 tanks of data beats any instinct.

## Using the Script

```bash
# What do MY habits cost? (defaults: 15000 mi/yr, 30 mpg, $3.50/gal)
python3 fuel_coach.py audit --mpg 30 --price 3.50 --miles 15000

# Price specific habits only
python3 fuel_coach.py audit --mpg 28 --price 4.10 --miles 22000 --habits roofbox,idle,speed

# Physics floor for your car
python3 fuel_coach.py floor --weight-lb 3400 --cd 0.30 --frontal 24 --mpg 30

# Trip math: is driving faster worth it?
python3 fuel_coach.py trip --miles 400 --mpg-high 34 --speed-a 65 --speed-b 75

# Diagnose a real drop
python3 fuel_coach.py diagnose --was 32 --now 27.5
```

`audit` prints each habit priced at your numbers, ranked; `floor` shows how close you are to the physics minimum (most cars run 1.5-2.5× above their floor — the gap is where coaching lives); `trip` prices the speed trade-off in both $ and minutes; `diagnose` routes the ranked cause list with first checks.

## Common Pitfalls

1. **Chasing additives and "fuel savers"** — no bottled product survives an EPA test. Air in tires is free and real.
2. **Comparing tank-to-tank instead of 3-tank averages** — pump cutoff variance alone is ±2-3%.
3. **Idling to "warm up" modern engines** — 30 s is enough; driving gently warms it 3× faster than idling.
4. **Overinflating to placard-max sidewall** — placard (door jamb) pressure optimizes wear/handling/RR; sidewall max is a safety limit, not a target.
5. **Premium fuel in a regular car** — pure waste on any knock-sensor engine (i.e., everything since ~1996).
6. **Assuming the EPA sticker is a promise** — EPA is a standardized test; your route, climate, and right foot set a ±20% band around it.
7. **Buying a hybrid on fuel math alone at low mileage** — at 6k mi/yr the premium never pays back; at 25k it does quickly. Run the numbers with your mileage.
8. **Ignoring the biggest real lever: trip count** — three cold-start errand runs cost more than one warm loop, whatever you do between stops.

## Verification Checklist

- [ ] Habits priced at YOUR mileage/price, not generic figures
- [ ] 3-tank rolling average established before diagnosing any "drop"
- [ ] Tire pressure checked cold against door-jamb placard (not sidewall)
- [ ] Speed changes evaluated in $/yr AND minutes/yr (trip subcommand)
- [ ] >10% sustained drop routed through the 8-cause list before parts-swapping
- [ ] Fixes ranked by $/yr, biggest first; additive fantasies excluded
