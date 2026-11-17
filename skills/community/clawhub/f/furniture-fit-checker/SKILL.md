---
name: furniture-fit-checker
description: "Check if furniture fits a room and the delivery path before buying or moving: computes doorway/hallway/stair clearance with diagonal-tilt geometry (the moving-industry standard), room layout fit with walkway widths, and draws an ASCII floorplan preview. Use when the user asks if a sofa/desk/bed/mattress will fit through a door, up stairs, around a corner, or in a room — preventing the classic bought-it-can't-move-it disaster."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [furniture, moving, apartment, interior, geometry, delivery, space-planning]
---

# Furniture Fit Checker 🛋️📏

The classic disaster: sofa bought online, delivery guys arrive, it doesn't
make the corner at the top of the stairs — now you own a return-shipping
nightmare. Or: desk fits the wall but blocks the door swing. This skill
runs the geometry **before money changes hands**.

## Overview

Three checks, one tool (`scripts/fit_checker.py`):

1. **Path check** — can the item pass a doorway/corridor/stairs?
   The moving-industry insight: a rigid box passes through an opening if it
   can be **tilted diagonally**. For a rectangular item (W×H×D) and a
   doorway (w×h), the effective clearance is the diagonal
   √(W²+D²) compared against the door width — plus corner-turning between
   corridor walls with the inner-diagonal trick. Handles:
   - doorway width vs item diagonal (item height vs door height)
   - L-shaped corner between corridors (inner-corner + outer-wall check)
   - straight staircase width vs diagonal, landing 180° turns
   - elevator cab diagonal (door + interior)
2. **Room fit** — does it fit where you want it, with **walkways ≥ 30 in /
   75 cm** (interior-design standards: 75-90cm paths, 90+ around dining)?
   Checks wall-length fit, walkway to opposing furniture/door, door-swing
   clearance, and radiator/vent obstruction warnings.
3. **Floorplan preview** — ASCII render of the room with the furniture
   placed, so you can *see* the walkways before committing.

Everything in metric or imperial (auto-detected per value with explicit
unit suffixes).

## When to Use

- "Will this sofa (86×37×35 in) fit through my 32-inch door?"
- "Can a king mattress go up my staircase with a landing?"
- "Will the desk fit in the bedroom without blocking the closet door?"
- "Does the dining table leave room to pull chairs out?"
- Pre-purchase sanity check before ordering big furniture online
- Moving-day planning: order of items through each door

**Don't use for:** architectural planning (load bearing, code compliance),
non-rectangular complex items (L-shaped sectionals — approximate as their
bounding boxes per section), or piano moving (hire pros, seriously).

## How It Works — Steps

1. **Measure** (a tape measure, 5 minutes): item W×D×H; door width × height
   (door open 90°, measure the frame minus trim); corridor widths if any;
   room dimensions; where you want it.
2. **Path check**:
   ```bash
   python3 scripts/fit_checker.py path --item 86x37x35in --door 32x80in
   ```
3. **Corner / stairs** if the route has them:
   ```bash
   python3 scripts/fit_checker.py corner --item 86x37x35in --hall-a 36in --hall-b 36in
   python3 scripts/fit_checker.py stairs --item 76x16x12in --width 36in --landing
   ```
4. **Room fit**:
   ```bash
   python3 scripts/fit_checker.py room --item 86x37in --room 14x11ft \
     --other 60x30in --floorplan
   ```
5. **Look at the floorplan** the tool prints; adjust and re-run.

## The Geometry (exact rules)

1. **Doorway**: item passes iff `item diagonal √(W²+D²) ≤ door width` AND
   `item min(W,D,H) ≤ door height` (tilt through). Sofas: use arm-to-arm
   width and seat depth; add nothing — but if legs/arms removable, measure
   without them.
2. **Corner (two corridors)**: moving trick — the item must satisfy
   `inner diagonal check`: for item length L and widths, at the critical
   angle θ where it simultaneously touches both outer walls and the inner
   corner: passes iff `(L·sinθ + W·cosθ) ≤ min hall width` for no θ...
   computed numerically over θ ∈ [0°, 90°] in 0.5° steps (exact for
   practical purposes).
3. **Stairs**: straight run — diagonal check vs stair width at the
   narrowest point (handrail, radiator, turn). With a 180° landing: the
   item must pivot on the landing; needs `landing depth ≥ item diagonal ×
   0.75` (empirical moving rule; tight pivots need pros' experience).
4. **Room walkways**: distance from furniture edge to the nearest
   obstruction (wall, other furniture, door swing arc) ≥ 75cm/30in;
   dining-table chairs need +90cm/36in on chair sides.

## Worked Example

```
Sofa 86×37×35in, door 32×80in:
  diagonal = √(86²+37²) = 93.6in > 32in → cannot pass flat
  BUT min(86,37,35)=35in... height check: 35in ≤ 80in ✓
  tilt geometry: sofa tilted on end, needs √(86²+35²)=92.9in vertical —
  exceeds 80in door height → FAIL flat-on-end
  workaround: angle-entry (two-person tilt) marginally possible —
  tool says TIGHT, remove door if hinge-pinned, or sofa legs off.
```

## Common Pitfalls

1. **Measuring the door slab, not the opening.** A "34-inch door" is the
   slab; the clear opening with the door open 90° is ~2in less (trim,
   hinges). Measure the gap.
2. **Forgetting the door swings IN.** An entry door opening inward eats
   ~door-width of maneuvering room on the delivery side; remove the door
   (pop the hinge pins) for tight items.
3. **Ignoring ceiling height on stairs.** Low ceilings above stairwells
   (under stairs, sloped) block items that pass the width check — the
   minimum above-step clearance matters as much as width.
4. **Using overall sofa dims when legs come off.** 4in of legs = the
   difference between fail and pass. Always check removable feet first.
5. **Hallway lights, radiators, baseboards** narrow the nominal width by
   2-6in at the critical point. Measure at the narrowest point, not the
   average.
6. **Elevator: interior diagonal ≠ door diagonal.** The cab is bigger than
   its door; the binding constraint is the door, then cab depth.
7. **Box springs don't bend.** A king mattress flexes around corners; a
   box spring/rigid base does not — that's what "split king" bases exist
   for.

## Verification Checklist

- [ ] All measurements taken at the narrowest point of the path
- [ ] Door measured as clear opening (90° open, minus trim)
- [ ] Item height-vs-doorway-height check done, not just width diagonal
- [ ] Walkway check ≥ 75cm (30in) for every side you walk past
- [ ] Door-swing arcs drawn on the floorplan output
- [ ] Removable legs/arms measured without, noted in the decision

## One-Shot Recipes

**Online sofa listing sanity check:**
```bash
python3 scripts/fit_checker.py path --item 213x94x89cm --door 81x203cm --report
```

**Full route audit (door → hall → corner → stairs):**
```bash
python3 scripts/fit_checker.py path --item 86x37x35in --door 32x80in
python3 scripts/fit_checker.py corner --item 86x37x35in --hall-a 40in --hall-b 36in
python3 scripts/fit_checker.py stairs --item 86x37x35in --width 36in --landing 36in
```

**Will the bed + desk both fit?**
```bash
python3 scripts/fit_checker.py room --item 60x80in --room 12x11ft \
  --other 48x24in --floorplan
```
