# Cargo Space Packer

Moving-truck Tetris solved with arithmetic: cube-utilization fit math with
the ~80% practical ceiling, density stacking classes, the heavy-low-forward
load pyramid, tie-down count math, and blanketing protocol — plus ASCII
load maps and shopping-list checklists computed from your cargo list.

## The Real Problem

Rental trucks are sold by box volume ("26 ft = 1,600 ft³!"), but nobody
loads a truck like a shipping container. Wheel wells eat floor, the
mom's-attic slope eats headroom, sofas and mattresses refuse to nest, and
nothing heavy may sit on anything soft. Real mixed household loads achieve
55-75% cube at best — which means the #1 moving-day failure is a cargo list
that "fits on paper" and doesn't fit in the truck, discovered at 6 PM with
the truck due back at 8. The #2 failure is the inverse: it all fits but
shifts — tail-heavy loads sway, unblanketed furniture arrives destroyed,
and the door wall lets go on the first hard brake.

## What It Does

- **fit** — cube %, fit verdict with the 80% ceiling rule, per-item density
  class, crush/payload warnings, and a "next size up" suggestion when it
  won't go
- **loadmap** — greedy heavy-low-forward packing plan rendered as ASCII
  top-down + side-view maps, 60/40 axle-balance check, ratchet-strap and
  anchor-point count
- **checklist** — blankets, shrink wrap, tape, straps sized to your load,
  plus the blanketing protocol and door-load rules
- **references/packing-physics.md** — the full physics: cube ceiling,
  density classes, load pyramid, on-end doctrine, E-track/L-track math,
  axle goals, DIY vs truck-size table

## Quick Start

```bash
python3 scripts/cargo_packer.py fit \
    --cargo 'washer=L70xW70xH100:1@75,box=L60xW40xH40:25@18' --space 15ft
python3 scripts/cargo_packer.py loadmap \
    --cargo 'fridge=L70xW70xH170:1@80,mattress=L200xW90xH25:1@35,box=L60xW40xH40:20@18' \
    --space L450xW215xH215
python3 scripts/cargo_packer.py checklist --cargo 'sofa=L200xW90xH90:1@90' --space 10ft
```

Stdlib only, offline. Dimensions in cm, weights in kg. Exit code 2 = does
not fit / bad input, so it composes with scripts. Not a substitute for
your own judgment on a real load — the numbers are practical
approximations, not regulations.

## License

MIT © Denis Voronin
