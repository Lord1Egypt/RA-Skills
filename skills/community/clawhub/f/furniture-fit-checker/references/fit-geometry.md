# Furniture Fit Geometry — Reference

## 1. The core model: travel direction × cross-section

A rigid rectangular box (W×D×H) passes a rectangular opening if **some
dimension is chosen as the travel direction** and the remaining two (the
cross-section) fit inside the opening. Choosing a different travel
dimension = tipping the item over, which is exactly what movers do.

For an opening W₀×H₀ and cross-section a×b (a ≤ b):

- **Axis-aligned pass**: `a ≤ W₀ and b ≤ H₀`
- **In-plane tilt pass**: if `a ≤ W₀` and the opening is much taller than
  wide, the item can rotate *within the plane of the doorway* while sliding
  through: possible iff `√(a² + b²) ≤ √(W₀² + H₀²)` (fitting the diagonal)
  — used when b slightly exceeds H₀ but a is small.

Wall thickness adds constraints (deep wall = no in-plane rotation); for
interior doors treat walls as thin and the model is exact.

## 2. The L-corner criterion

Two corridors of widths A and B meet at a right angle. An item of plan
length L and thickness T, held horizontal, must rotate 90° while staying
inside the union of the corridors. At pivot angle θ the item's projections
onto the two corridor directions are:

```
proj_A(θ) = L·sin θ + T·cos θ
proj_B(θ) = L·cos θ + T·sin θ
```

The turn is possible iff **∃θ ∈ (0°, 90°)** with `proj_A(θ) ≤ A` and
`proj_B(θ) ≤ B`. The tool sweeps θ in 0.5° steps and also reports the
minimum equal-width corridor ("square corner minimum")
`min_θ max(proj_A(θ), proj_B(θ))` — the single number to compare your
hallway against.

For L ≫ T the square-corner minimum approaches L·√2/2 ≈ 0.707·L at θ=45°
intuition: a 7-foot sofa needs ~5-foot corridors to swing horizontally.

## 3. The stand-on-end trick (vertical tilt)

When ceiling height ≥ the item's longest dimension, movers stand it
vertually. The plan footprint collapses from `L × T` to `T₂ × T₃` (the two
smallest dims) — a 218cm sofa's footprint becomes 94×89cm, which turns in
any hallway. Constraints:

- ceiling clearance along the *whole turn path* (watch lights, low spots)
- door/window frames on the turn circle vertically too
- weight: standing a 40kg sofa needs two people and control

The tool applies tilt mode automatically when `--ceiling` is given.

## 4. Staircases

A straight stair run is a "door" seen from the side: cross-section = (stair
clear width) × (headroom above the steps), and the item travels along the
run. Because the run is long, the binding constraints are width and
headroom, not length. The narrowest point usually isn't uniform: handrail
bulge, radiator at the turn, newel post — measure each.

A 180° landing forces a pivot (a corner turn in tight quarters): practical
moving rule is landing depth ≥ 0.75 × longest face diagonal. Tighter
landings sometimes still work with the item vertical — that's pro-mover
judgment territory.

Sloped ceilings above stairs: effective headroom shrinks as you go up; use
headroom at the worst step, not the average.

## 5. Room layout standards

| Path / zone | Minimum |
|---|---|
| General walkway | 75 cm / 30 in |
| Main traffic path | 90 cm / 36 in |
| Dining chair pull-out + pass | 91 cm / 36 in behind table edge |
| Kitchen work aisle | 106 cm / 42 in |
| Bed side clearance | 76 cm / 30 in each side |
| Door swing arc | door width radius kept clear |

Walkway is measured **from the furniture edge to the nearest obstruction**,
not wall to wall. The tool computes `room depth − item projection` and
warns when < 75cm; door swings and radiator/vent clearances are listed as
manual checks in SKILL.md because they need the door position.

## 6. Measurement protocol (the 10-minute audit)

1. Door: open 90°, measure the clear opening between the frame stops,
   minus trim; note height. Doors that open *inward* into the path cost
   maneuvering room — pop the hinge pins if tight.
2. Hallways: width at the narrowest point (baseboards, radiator, turns).
3. Stairs: clear width at the handrail, headroom at the lowest step above,
   landing depth.
4. Elevator: door width × height AND cab interior diagonal; the door is
   usually the binding constraint.
5. Item: overall W×D×H; then re-measure without removable legs/feet/arms —
   4 inches of legs flips many fail→pass results. Sofas: some have
   bolt-off arms; check under the armrest fabric line.

## 7. What bends and what doesn't

- Mattresses flex around corners (they're foam/spring sandwiches); the tool
  is conservative and treats them as rigid — a marginal FAIL on a mattress
  is often a real-world pass.
- Box springs/platform bases do NOT bend: that's why "split king/queen"
  bases exist.
- IKEA-style flat packs are rigid and tall: check the diagonal against your
  stair headroom before assuming it fits because it's "flat".

## 8. Decision flowchart

```
buy/measure item
   │
   ├─ path: every door + corner + stair on the route?
   │     ├─ door/corner/stairs check → any FAIL → don't buy / disassemble
   │     └─ all pass (with tilt) → proceed
   │
   └─ room: wall length, walkway ≥75cm, door swing, vents
         └─ floorplan preview → looks right → order
```

## 9. Limitations

- Rectangular rigid items only; L-sectionals: run each section separately
  (and note the join must also clear the corner).
- No physics: weight, grip, stair rail anchorage, floor protection.
- Pianos, wardrobes with mirrors, glass tops: hire insured movers.
