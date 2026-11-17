---
name: cargo-space-packer
description: Use when loading a pickup bed, trailer, or moving truck — volume-vs-cube fitting with the 80% practical ceiling, density-based stacking classes, the load pyramid (heavy low and forward, mattresses/sofas on-end), tie-down count math per anchor style, axle weight distribution, and an ASCII load map so nothing ships loose or arrives crushed.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [moving, truck, cargo, packing, tie-downs, load-securing, hauling]
---

# Cargo Space Packer

"Will it fit?" is the wrong question. The right question is "will it
fit, survive stacking, and stay put at 60 mph?" Most load failures come
not from cube volume but from density (books on top of lamp shades),
weight placement (all the heavy boxes at the tailgate over the rear
axle), and too few tie-downs for the weight. This skill runs the
volume math honestly (with the ~80% practical packing ceiling), stacks
by density class, places the load pyramid correctly, and counts the
ratchet straps.

## When to Use

- Loading a pickup bed, enclosed trailer, or rental truck (10/15/20/26 ft)
- Deciding truck size for an apartment move — cube math with the 80% ceiling
- Stacking mixed loads: books, appliances, furniture, soft goods
- Securing the load: how many ratchet straps, where to anchor
- Weight distribution: front-heavy 60/40 bias for steering and sway control

## The Method

```bash
# Will it fit? cargo as LxWxH cm + count, space as LxWxH cm
python3 scripts/cargo_packer.py fit \
  --cargo 'L120xW80xH60:2,L60xW40xH40:5' --space 'L400xW200xH200'

# Load map: top-down + side view, heavy forward, tie-down plan
python3 scripts/cargo_packer.py loadmap \
  --cargo 'L120xW80xH60:2,L60xW40xH40:5' --space 'L400xW200xH200'

# Securing checklist by weight + surface
python3 scripts/cargo_packer.py checklist --weight-lb 900 --surface trailer
```

## The Load Pyramid

1. **Heavy, dense, sturdy** — low, forward, against the cab/bulkhead:
   books, tools, appliances (upright, never on their side).
2. **Medium boxes** — mid-height, mid-load, filled full (no half-empty
   boxes crushing).
3. **Light/bulky/soft** — top and rear: bedding, lamp shades, garage
   bags.
4. **On-end doctrine:** mattresses, box springs, and sofas ride
   vertically on their edge (sofas on end, feet to the wall) — they
   consume half the floor and don't crush.
5. **Long items** (table leaves, rods, skis) go along the walls or on
   top of the flat load, blanket-wrapped.

## Density Stacking Classes

| Class | Example items | Where | Stack on top? |
|---|---|---|---|
| A (dense) | Books, tools, records, canned goods | Floor, forward | Only class A |
| B (medium) | Packed boxes, small appliances | Mid | B or C |
| C (light) | Linens, shades, empty suitcases | Top/rear | Nothing |
| F (furniture) | Dressers (drawers out), tables | Floor, strapped | C only |
| F-on-end | Mattresses, sofas | Vertical, wall-side | Nothing |

## Tie-Down Math (WSTDA rules of thumb)

- Working Load Limit total ≥ 2× cargo weight (going by WSTDA indirect/
  direct methods — use 2× as the conservative floor).
- Minimum 2 tie-downs for anything ≥ 5 m long / ≥ 1,134 kg (49 CFR);
  practically: 1 strap per ~45-70 kg of cargo or per major furniture piece.
- Angular loss: a strap at 45° retains ~70% of its WLL; straight-line
  (direct) pulls keep 100%.
- Anchor spacing every 0.8-1.2 m along L-track / E-track.
- Friction is not a tie-down. Webbing over the top does little without
  downward angle; use forward-facing hooks and rub rails.

## Truck Size Table (with 80% ceiling)

| Truck | Cube m³ | Practical (80%) | Fits |
|---|---|---|---|
| Pickup 6.5-ft bed | 2.2 | 1.8 | 1-2 room's boxes |
| 10-ft box truck | 4.2 | 3.4 | Studio |
| 15-ft box truck | 7.9 | 6.3 | 1-bed apartment |
| 20-ft box truck | 10.9 | 8.7 | 2-3 bed |
| 26-ft box truck | 16.9 | 13.5 | 3-4 bed house |

## Common Pitfalls

1. **Volume math without the ceiling.** Boxes never use 100% of cube:
   plan at 80% (odd shapes, fragile no-stack zones, aisle to the door).
2. **Heavy at the tailgate.** Weight behind the rear axle lifts the
   front = steering loss and trailer sway. Load 60/40 front-biased.
3. **Sofa flat on the floor.** Rides on-end, feet to the wall — half
   the footprint and no crushed arms.
4. **Counting friction.** A blanket-wrapped stack held by gravity does
   not survive a 60 mph brake. Count straps by weight, not vibes.
5. **Half-empty boxes.** Crush. Fill them or don't stack on them.
6. **Straps over thin walls of boxes.** Corner-protect; webbing cuts
   cardboard at tension.

## Verification Checklist

- [ ] Cargo cube sum vs space cube with 80% practical ceiling applied
- [ ] Density classes assigned; nothing dense above nothing fragile
- [ ] Long/vertical doctrine applied (mattresses/sofas on-end)
- [ ] Tie-down count from weight (2× WLL floor, angular loss noted)
- [ ] Weight 60/40 front-biased; axle not overloaded
- [ ] Doors close against straps, not cargo; nothing above the rail
