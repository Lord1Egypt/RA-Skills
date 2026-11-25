---
name: accessibility-ramp-builder
description: Home ramp engineering from the real rise — required run at the right slope (1:12 self-propelled wheelchair / 1:10 assisted / 1:8 walker, with the descending-runaway physics behind it), rest platforms every 30 in, 60×60 in landings, handrail sizing, switchback footprints when the yard is too short, threshold wedges under 1.5 in, door-clearance traps below 32 in, rough lumber takeoff and wood/modular/concrete cost bands. Audits existing ramps and flags DANGEROUS grades instead of shrugging.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [accessibility, ramp, wheelchair, walker, seniors, diy, aging-in-place]
---

# Accessibility Ramp Builder

A hip replacement, a stroke, a walker, a wheelchair — suddenly the two
porch steps are a wall, and the hardware store sells "portable ramps"
that are 2 feet long and terrifying. Ramps are geometry with safety
consequences: this skill does the geometry.

## When to trigger
- "My mom needs a ramp to get into the house — how long does it need
  to be?"
- "Is this 1:8 ramp safe for a wheelchair?"
- "I only have 15 feet of yard — can a ramp even fit?"
- "The door is only 30 inches wide, does that matter?"
- any aging-in-place / post-surgery / mobility-equipment planning

## How it works

1. **Collect inputs**: total rise in inches (measure from driveway to
   door threshold — string + level, all steps added), user class
   (`self-propelled` wheelchair / `assisted` / `walker`), available
   straight space outside the door in feet, clear door width.
2. **Run** `scripts/ramp_builder.py --rise 22 --use self-propelled
   --space-ft 14 --door-width 30`
3. **Geometry engine**: `run = rise × ratio` (1:12 self-propelled,
   1:10 assisted, 1:8 walker-only), rest platforms every 30 in of rise,
   60×60 in landings top and bottom, 36 in clear width, handrails both
   sides above 6 in rise with 34–38 in height and 12 in extensions.
4. **Fit analysis**: straight run vs your yard; if short, a 180°
   switchback footprint (two parallel runs + 5×5 ft turn platform) —
   and if even that fails, the honest DOES NOT FIT verdict routing to
   re-grade / new door path / vertical platform lift.
5. **Threshold + door logic**: rise ≤ 1.5 in → wedge ramp, done;
   ≤ 3 in → portable options with slope caveats; door clear width
   below 32 in → swing-clear hinges / wider door (the ramp that leads
   to a door the chair can't enter is a $4,000 mistake).
6. **Audit mode**: `--existing-slope 1:8` grades a ramp you're standing
   on against all three user classes and names DANGEROUS grades —
   descending a too-steep ramp lifts front casters and runs away.
7. **Takeoff & cost**: rough lumber counts (decking, stringers, posts)
   and installed cost bands for wood / modular aluminum / concrete.

## Pitfalls encoded
- **1:12 is physics, not bureaucracy**: a hand-propelled chair
  descending 1:8 gains speed the user can't arrest; the failure mode
  is backward tip → head strike.
- **The door at the top must sit on a LEVEL landing** — you cannot
  pull a door open while sitting on a slope.
- **32 in clear door width** is the wheelchair minimum; measure the
  clear opening, not the door slab.
- **Cross-slope under 2%** (1:48): sideways tilt unseats occupied
  chairs on turns; check with a phone level in both directions.
- **Edge protection**: 2 in curbs or continuous rails so castors can't
  drop off the side; slip-resistant decking.
- **Permits**: ramps attached to the structure usually need one;
  frost-depth footings where winters are real.
- Rest platforms are not optional above 30 in of rise — users pause,
  rest, and turn.

## Examples

```bash
# Standard porch: 22 in rise, self-propelled user, 14 ft of yard
python3 scripts/ramp_builder.py --rise 22 --use self-propelled \
    --space-ft 14 --door-width 30
# → 22 ft run needed, switchback doesn't fit, 30 in door too narrow

# Same rise, 17 ft of wall → FITS AS SWITCHBACK (16 ft wall run)

# Auditing the ramp the seller described as "plenty"
python3 scripts/ramp_builder.py --existing-slope 1:8 --use self-propelled
# → DANGEROUS: too steep for hand-propelled chairs
```

## Output contract
- geometry sheet: slope, run, landings, width, handrail spec
- fit verdict: FITS STRAIGHT / FITS AS SWITCHBACK / DOES NOT FIT
- door-clearance verdict with fix options
- material takeoff + cost bands (wood/aluminum/concrete)
- safety rules list + permit reminder
