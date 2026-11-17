# Furniture Fit Checker 🛋️📏

**Will the sofa fit through the door, up the stairs, around the corner —
and in the room? Know before you buy.**

The classic first-apartment (and third-apartment) disaster: the sofa that
can't make the turn at the top of the stairs. Delivery fees are
non-refundable. This tool runs the same geometry movers use — travel
directions, cross-sections, diagonal tilts, corner sweeps — in seconds,
before money changes hands.

## What it does

- **`path`** — doorway pass check: tries all orientations (flat, tipped,
  tilted in-plane) and reports which works
- **`corner`** — L-corner between corridors: numeric angle sweep of the
  moving criterion, plus the square-corner minimum width; auto-tries the
  **stand-on-end movers' trick** with `--ceiling`
- **`stairs`** — cross-section check vs width & headroom, 180°-landing
  pivot rule
- **`room`** — wall-length fit, walkway ≥ 75cm/30in standards, gap checks
  to opposing furniture
- **ASCII floorplan** — see the layout and walkways before committing
- Units anywhere: `86x37x35in`, `218x94x89cm`, `14x11ft`, plain = inches

## Quick start

```bash
# The classic: 86" sofa vs 32" apartment door
python3 scripts/fit_checker.py path --item 86x37x35in --door 32x80in
# → DOES NOT FIT (all orientations listed with reasons)

# Same sofa, hallway corner — stood on end it makes the turn:
python3 scripts/fit_checker.py corner --item 94x218x89cm \
  --hall-a 110cm --hall-b 110cm --ceiling 240cm
# → FITS AROUND CORNER (stood on end)

# Room layout with walkway check + floorplan
python3 scripts/fit_checker.py room --item 213x94cm --room 430x335cm --floorplan
```

## Why it matters

Furniture return rates on large items run 15-30% online, and the #1 reason
is "doesn't fit through the door/stairs". A five-minute tape-measure
session plus this check prevents a $100+ re-delivery/return ordeal — and
the awkward hallway standoff with two delivery guys and a sofa balanced on
end.

## Files

- `SKILL.md` — agent-facing usage guide
- `scripts/fit_checker.py` — the checker (stdlib only)
- `scripts/test_fit_checker.py` — self-tests
- `references/fit-geometry.md` — the geometry: corner criterion, tilt
  tricks, walkway standards, measurement protocol

## Test

```bash
python3 scripts/test_fit_checker.py
```

MIT © 2026 Denis Voronin
