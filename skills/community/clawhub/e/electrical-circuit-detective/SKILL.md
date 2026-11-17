---
name: electrical-circuit-detective
description: "Use when a breaker keeps tripping, an outlet went dead, or you wonder if a circuit can take one more appliance. Computes real circuit load with the 80% continuous rule, routes dead outlets (GFCI cascade, backstab failure), separates overload vs short vs ground-fault trip patterns, and names the exact point to call an electrician."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [electrical, breaker, circuits, home-safety, diagnosis, diy]
---

# Electrical Circuit Detective

## Overview

Residential electrical problems come in three everyday shapes: **a breaker that keeps tripping**, **an outlet that suddenly went dead**, and **"can I plug this in here?"**. All three are answerable with arithmetic and a diagnostic tree before anyone opens a panel — and most trips and dead outlets have boring, fixable causes (overloaded 15A kitchen circuit, tripped GFCI hiding under a table, failed backstab connection).

This skill gives you the load math (watts ÷ volts = amps, 80% continuous rule), a ~45-appliance wattage database, a trip-pattern decoder, a ranked dead-outlet flow, and hard STOP gates for the situations that are genuinely dangerous.

**Scope: diagnosis and planning. Not panel work.** Anything inside the breaker panel, anything involving aluminum wiring, and anything after a "burning smell / scorch mark / tingle" report is electrician territory — the skill tells you that immediately instead of walking you deeper.

## When to Use

- A breaker trips repeatedly and you want to know WHY before resetting it again
- One or several outlets went dead and the breaker looks fine
- Planning a new appliance (space heater, air fryer, EV charger, workshop tool) and asking "will this circuit take it?"
- You want to map which outlets are on which breaker (the circuit map nobody has)
- An outlet is warm, buzzing, discolored, or a plug falls out of it → skip to Safety Gates

Don't use for: outdoor/overhead service drops, sub-panel installation, EV charger hardwire sizing at 40A+ (needs a load calc per NEC 220.83 — flag an electrician), or anything commercial 3-phase.

## Safety Gates — STOP Before Anything

Read these before touching anything:

1. **Burning smell, scorch/char marks, melted plastic, hot outlet face** → turn the breaker OFF, leave it off, call an electrician today. Do not diagnose-live.
2. **Tingle or shock from any surface** → breaker OFF, electrician, and treat wet floors as live. Do not test by touching again.
3. **Buzzing/sizzling at the panel, rust, or scorch at breakers** → electrician only. Panels are never a DIY surface.
4. **Aluminum branch wiring (houses ~1965-1973, "AL" stamped on cable sheath, oxidation-capped wires)** → any connection work is specialist work (AlumiConn/CopAlum). Detect and stop.
5. **Water contact (flooded basement, leak above an outlet)** → kill the circuit first, then diagnose.
6. **Rodent damage suspected (attic/garage, gnawed sheathing)** → electrician; damaged insulation can energize the box.

Everything below assumes: dry hands, rubber-soled shoes, non-contact voltage tester in hand, one hand in pocket when anything energized is near.

## The Load Math (30 seconds)

```
amps  = watts ÷ volts            (120V normal outlets/lights, 240V dryer/range/AC/well)
safe continuous load = breaker × 0.80   ("continuous" = 3+ hours: heaters, servers, freezers)
```

| Breaker | 120V total | Safe continuous (80%) |
|---|---|---|
| 15A | 1800 W | **1440 W** |
| 20A | 2400 W | **1920 W** |
| 30A (240V) | 7200 W | 5760 W |

The 80% rule is why a 1500 W space heater + a 1500 W microwave on one 20A kitchen circuit trips: 3000 W = 25 A on a circuit whose honest all-day ceiling is 1920 W. Heaters, hair dryers, kettles, air fryers, and irons are the classic "invisible 1500s" — two on one circuit is always over.

**Motor/compressor surge**: fridges, freezers, sump pumps, compressors, and garage openers draw 2-3× nameplate for the first second. They don't usually TRIP breakers on surge (thermal-magnetic breakers tolerate brief inrush), but they explain "trips when the fridge cycles ON while the microwave runs".

## Trip-Pattern Decoder

The timing of the trip IS the diagnosis:

| Pattern | Meaning | First move |
|---|---|---|
| Trips **instantly** when something is plugged/switched on | Short circuit or ground fault in that device/cord | Unplug it, reset, stays on = culprit found. If the breaker trips with NOTHING plugged in → wiring fault, electrician |
| Trips after **minutes** of running | Classic overload | Run `circuit_doctor.py load` on everything on that circuit |
| Trips only when **two things run together** (microwave + kettle) | Overload, marginal | Load math → move one appliance to another circuit |
| GFCI outlet RESET button pops, breaker stays on | Ground fault at plug level (moisture, worn appliance) | Unplug everything on that GFCI, reset, replug one by one |
| Trips when a **motor starts** (fridge/sump/AC) | Locked rotor / failing motor, or marginal overload | Note surge math; if fridge trips it ALONE → appliance fault |
| Trips at **random times / at night** | Water ingress, rodent chew, failing breaker, AFCI nuisance (aged motor) | Inspect attics/garage runs; swap loads; if random persists → electrician |
| Won't reset at all | Hard fault still present (or failed breaker) | Unplug everything, lights off; still won't reset → electrician |
| Trips only in **wet conditions** (bathroom, outdoor, sump) | Genuine ground fault — it's doing its job | Find the wet contact; never "fix" by removing the GFCI |

## Dead Outlet Flow (ranked by probability)

1. **Tripped GFCI somewhere else on the circuit** (~60% of "dead outlet" cases). GFCIs in garages/basements/bathrooms protect DOWNSTREAM regular outlets — sometimes in other rooms. Hunt every GFCI (test/reset buttons) in the house and press RESET. Outdoor + garage ones are the usual hidden suspects.
2. **Switched outlet**: half the outlet dead? Plug a lamp into both halves and flip wall switches. Builders wire one half to a switch.
3. **Tripped/half-seated breaker**: flip the breaker fully OFF then firmly ON. A breaker that "looks on" can be internally tripped.
4. **Failed backstabbed connection** (very common in 1970s-90s builds): push-in connectors on the BACK of outlets fail and kill everything downstream on the run. Confirm with a non-contact tester: outlet dead, but the breaker is on, and other outlets on the run are ALSO dead in a line → it's the last WORKING outlet before the dead ones. Fix = re-terminate that outlet's wires on the side screws (breaker off, test dead first).
5. **Wire-nut failure in a junction box** (thermal cycling loosens aluminum-era and old copper nuts) or a junction buried in an attic. Same downstream-dead signature.
6. **Broken outlet itself** (springs tired, plug falls out, warmth) → replace the receptacle; warmth/scorch = electrician.

Script `dead-outlet` walks this tree interactively and tells you which box to open.

## Circuit Mapping (do this once, label the panel)

1. Phone note per breaker; plug a radio loudly into the mystery zone.
2. Flip one breaker at a time (30s interval), note what dies (radio silence, lights, fridge hum stops).
3. For each circuit, count outlets + note the big loads you find.
4. Write it ON the panel door with a marker + masking tape label per breaker. Future-you needs this at 11 PM with a flashlight.

## Using the Script

```bash
# Can this kitchen circuit run microwave + kettle + toaster?
python3 circuit_doctor.py load --volts 120 --amps 20 \
    --items "microwave:1100,kettle:1500,toaster:900"

# Heater question: 1500W heater on a 15A bedroom circuit with lights
python3 circuit_doctor.py load --volts 120 --amps 15 --items "space heater:1500,led lights:40" --continuous

# Dead outlet diagnosis (interactive, ranked causes)
python3 circuit_doctor.py dead-outlet

# Trip pattern -> meaning
python3 circuit_doctor.py trip --pattern "minutes after running"

# What's in the appliance database
python3 circuit_doctor.py db
```

Output: amps drawn vs allowed, 80% ceiling, verdict OK / TIGHT / OVERLOAD, and which item to move. Unknown item names get nearest-match suggestions from the 45-entry database.

## Common Pitfalls

1. **Counting nameplate watts as gospel for corded tools/microwaves** — microwaves advertise OUTPUT (1000 W) but draw 1400-1600 W INPUT. The DB uses input draw. Rule: microwave input ≈ 1.4-1.6× advertised.
2. **Forgetting lights add up on 15A circuits** — 20 old incandescent cans = 1200 W by themselves. LED retrofit (8 W each) frees the whole circuit.
3. **Extension cords don't add capacity** — they derate it. A 16-gauge 50 ft cord on a space heater is a fire, not a solution. Cord math is in `references/circuit-guide.md`.
4. **"It held for a year" is not a load calc** — breakers trip on heat; a marginal overload can survive winter and trip every day in summer heat.
5. **Replacing a tripping breaker with a bigger one** — NEVER. The wire gauge is why the breaker is that size; a 20A breaker on 14-gauge wire is how house fires start.
6. **Resetting a GFCI repeatedly to "keep it working"** — a GFCI that trips is reporting current going somewhere it shouldn't. Find the cause.
7. **Assuming the outlet closest to the panel is first** — wiring order is rarely geometric. Map by dead-downstream evidence instead.

## Verification Checklist

- [ ] Trip pattern classified (instant / delayed / GFCI / random) before any reset attempts
- [ ] Load math run with INPUT watts (not advertised output) and 80% rule for 3h+ loads
- [ ] Dead outlet: all GFCIs in house reset-checked FIRST, half-switched outlet ruled out second
- [ ] Panel map labeled after any discovery session
- [ ] Any safety-gate finding (smell/scorch/tingle/aluminum/water) escalated to electrician, breaker left OFF
- [ ] Nothing inside the panel opened by non-electrician hands
