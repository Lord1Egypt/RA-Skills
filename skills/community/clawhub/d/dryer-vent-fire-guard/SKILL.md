---
name: dryer-vent-fire-guard
description: Use when clothes take multiple cycles to dry, the laundry room is hot/humid, or you want to audit a dryer vent for lint buildup and fire risk. Computes vent equivalent length vs code max, dry-time creep diagnosis, and a clean/replace/repair ladder.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [dryer, lint, fire-safety, appliance, hvoc, home-maintenance]
---

# Dryer Vent Fire Guard

## Overview

Clothes dryers cause ~13,000–15,500 reported home structure fires per year in the US alone, and **a third of them trace to failure to clean the dryer vent**. The failure mode is silent: lint accumulates inside the vent run for years, drying time creeps from 40 to 90 minutes, everyone blames "the dryer getting old" — while the exhaust restriction superheats the lint itself (an excellent fuel) behind the machine.

This skill turns the two signals every household already has — **how long a load takes to dry** and **what the vent looks like behind the dryer** — into a code-based verdict and an action ladder.

## When to Use

- A normal load needs 2+ dry cycles, or drying takes >60 minutes.
- Laundry room feels hot/humid, or you smell burning while drying.
- Dryer is hot to the touch on top; clothes come out very hot.
- You just moved into a home with an unknown vent history (always audit).
- Annual maintenance planning, or after noticing lots of lint at the outdoor hood.
- Post-incident: dryer shut off mid-cycle (thermal fuse tripped — a classic restriction symptom).

Don't use for: dryer won't start at all, drum won't turn (electrical/belt issues), gas burner diagnostics inside the machine — those are repair topics, not venting.

## How It Works

1. **Run the dry-time test.** Time a standard load (bath towels, high spin, from wet). Baseline for a healthy vent + mid-size dryer: **35–50 minutes**. 60+ minutes or a second cycle = restricted airflow until proven otherwise.
2. **Inventory the vent run.** Behind the dryer, note: duct material, length along the whole path, count every 90° elbow, duct diameter, and where it terminates.
3. **Compute equivalent length** (see Data & Physics) and compare against the code allowance — this is what `scripts/dryer_vent_audit.py` does.
4. **Grade fire risk** from material (vinyl/foil = violation), vertical rises, crush points, screencaps, and dry-time evidence.
5. **Apply the action ladder** (clean → replace duct → reroute/shorten → pro cleaning).
6. **Set the recurrence:** 1×/year minimum; 2×/year for large households or pets.

## Data & Physics

**Code allowance (IRC M1502 / manufacturers):** max 35 ft of equivalent length for a 4″ rigid duct. **Every 90° elbow costs 5 ft** of allowance. Flexible duct adds friction: figure its effective length at ~2× its actual length.

**Equivalent length = actual length × material factor − the allowance already spent by elbows.** If the result exceeds 35 ft, the vent is out of spec and will lint up no matter how often you clean it — reroute or upsize.

**Why restriction = fire:** restricted exhaust → humid air stays in the drum → longer cycles → element/burner runs longer → lint (trapped where airflow is slowest: elbows, transitions) bakes at ever-higher temperatures. Lint ignites around 250–300 °C and burns fast.

**Dry-time verdict bands (standard towel load):** ≤50 min HEALTHY · 51–60 WATCH · 61–90 RESTRICTED · >90 or 2+ cycles SEVERE (clean now, today).

**Termination rules:** must vent outdoors — never into an attic, crawlspace, garage interior, or wall. Exterior hood must have a flap damper, **not** a screen (screens catch lint = plug). Box "periscope" vents behind the dryer must not be crushed.

## The Action Ladder

1. **Clean now** (any verdict above HEALTHY): unplug dryer (gas: shut valve), pull the machine, vacuum the wall-side duct collar and the dryer's internal duct with a shop vac + flexible brush from BOTH ends. Expect a shocking lint harvest on runs older than 2 years.
2. **Replace vinyl/foil flex with semi-rigid or rigid aluminum** immediately — vinyl duct is a code violation on dryers, full stop.
3. **Shorten/reroute** if equivalent length exceeds 35 ft: straightest path wins; every elbow removed buys back 5 ft.
4. **Pro vent cleaning ($100–200)** when the run is long, vertical, in-wall, or inaccessible from both ends.
5. **Fix termination**: add/replace an exterior hood with damper, remove any screen, confirm flap isn't jammed with lint.

## Worked Examples

`python3 scripts/dryer_vent_audit.py --demo` runs a 12-ft foil flex run with 4 elbows and a 75-minute dry time → SEVERE: out of code, foil violation, clean-today directive.

`python3 scripts/dryer_vent_audit.py --material rigid --length-ft 18 --elbows 2 --diameter-in 4 --dry-minutes 48 --loads-per-week 8` → healthy but near the edge: 28 ft equivalent, schedule annual clean.

## Common Pitfalls

1. **Cleaning only the lint screen trap.** The screen catches ~80%; the rest coats the run. The trap is not the vent.
2. **Judging by "it still dries eventually."** Multiple cycles IS the symptom — each one is money ($0.50–1.00/load) and heat soak into trapped lint.
3. **Reusing crushed/kinked flex after moving the dryer.** One hard kink can halve airflow; semi-rigid costs $10.
4. **Venting "temporarily" into a bucket or indoors.** Adds gallons of moisture to the house (mold risk) and is a code violation; lint spread is uncontrolled.
5. **Assuming a new dryer fixes slow drying.** The vent came with the house, not the dryer.
6. **Screen on the exterior hood** "to keep birds out" — birds are real, but the screen plugs first; use a damper hood and check it seasonally.
7. **DIY brush without vacuuming:** pushing lint deeper into elbows can complete the blockage. Always vacuum out after brushing.

## Verification Checklist

- [ ] Dry-time test done with a standard load and timed honestly
- [ ] Duct material, length, elbow count, diameter recorded from the actual run
- [ ] Equivalent length computed and compared to 35 ft
- [ ] Exterior termination inspected: outdoors, damper, no screen
- [ ] Cleaning performed from both ends (or pro booked) before next heavy use
- [ ] Next clean date written into the home-maintenance calendar
