---
name: diy-materials-estimator
description: "Use before any paint, mulch, concrete, drywall, flooring, tile, or fence store run: computes exact material quantities from room/dimensions with real coverage physics (paint spread rate by surface type, mulch depth by purpose, concrete volume + bag yield + mix water), waste factors by pattern, and a consolidated shopping list with buy-unit rounding. Kills the third-trip-to-the-store problem."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [diy, home-improvement, paint, concrete, mulch, flooring, materials, renovation]
---

# DIY Materials Estimator

## Overview

The defining experience of home improvement is the **third trip to the store**.
You bought 2 gallons of paint for a room that needed 2.6. The mulch pile
covered 80% of the bed at the depth you actually spread it. The "80-lb bag of
concrete makes 0.6 ft³" assumption silently ignored that your slab is 4 inches,
not 3. Every one of these errors comes from estimating materials by vibe
instead of by coverage physics.

This skill computes quantities from dimensions using the actual governing
math for seven project classes:

| Project | Governing math |
|---|---|
| Paint | area ÷ spread rate (350–400 ft²/gal smooth; 200–300 textured/primed dry) × coats |
| Mulch | area × depth (5 cm aesthetic / 7.5 cm weed-suppress) ÷ 27 → cubic yards; bag count |
| Concrete | L×W×D volume; 60/80-lb bag yield table (0.45 / 0.60 ft³); fibers + cure |
| Drywall | sheet count by orientation + waste factor (10% standard, 15% diagonal-layout) |
| Flooring | area × (1 + waste%): 5% straight, 10% diagonal, 13% herringbone; box rounding |
| Tile | tiles = area ÷ tile area × waste; box count; grout lbs from joint size |
| Fence | posts (spans ≤ 8 ft), rails (2–3 per bay), pickets from spacing + gap |

Output: exact quantities **and** buy-unit rounding (you can't buy 2.3 gallons;
you buy 3 × 1-gal or 1 × 5-gal if cheaper), plus a consolidated multi-project
shopping list.

## When to Use

- Any painting project: rooms, exteriors, doors/trim counted separately
- Landscaping: mulch, soil, gravel (depth by purpose: mulch vs pathway base)
- Pouring footings, pads, post bases; bag-count vs ready-mix crossover math
- Drywalling a room or wall (sheet count + screws + joint compound + tape)
- Flooring or tile purchase (the waste factor by pattern is where budgets die)
- Building or repairing a fence (posts + rails + pickets + concrete per post)

**Don't use for:** structural engineering (beams, load calculations — those
need an engineer), roofing squares (safer as its own skill), or live pricing.

## The Physics (quick reference)

### Paint
```
coverage:  interior flat/eggshell  350-400 ft²/gal (smooth, one coat)
           textured/orig. drywall  250-300 ft²/gal
           exterior, rough         250-350 ft²/gal
           primer                  300-400 ft²/gal
wall area  = perimeter × wall height − openings (door ≈ 21 ft², window ≈ 12)
ceiling    = L × W
total gal  = (area ÷ coverage) × coats ÷ 0.95 (spill/edge loss)
```
Rule of thumb check: a 12×12 ft room with 8 ft ceilings, two coats, walls
only ≈ 384 ft² → ~1.1 gal/ coat-pair ≈ **buy 2 gallons** (never 1).

### Mulch / soil / gravel
```
cubic feet  = area_ft² × depth_ft           (2" = 0.167, 3" = 0.25, 5cm ≈ 0.167)
cubic yards = cubic feet ÷ 27
2 cu-ft bags = ft³ ÷ 2      3 cu-ft bags = ft³ ÷ 3      bulk delivered if ≥ 4 yd³
```
Depth doctrine: 5 cm (2") refresh top-up; 7.5–10 cm (3–4") new bed or
weed suppression. NEVER volcano-mulch trees (keep 8 cm off trunks).

### Concrete
```
volume ft³ = L_ft × W_ft × D_ft         (4" slab = 0.333 ft)
bags:      80-lb ≈ 0.60 ft³   60-lb ≈ 0.45 ft³   40-lb ≈ 0.30 ft³
water:     ~3 qt per 80-lb bag (start at 80%, add to feel — don't drown it)
crossover: ≥ ~20 bags → ready-mix truck or trailer mix is usually cheaper
           and ALWAYS better for >4" slabs
post hole: π × r² × depth + 6" above-grade frustum ≈ bag math from table
```

### Drywall
```
sheets = (area ÷ sheet area) × (1 + waste)     4×8 = 32 ft², 4×12 = 48 ft²
screws: ~1 per ft² of board (1¼" for ½" board)
tape:   1 linear ft per ft of joint ≈ perimeter of sheets joined
mud:    1 gal per 100-140 ft² skim + fill (buy +25%)
```

### Flooring
```
waste: straight-lay 5%   diagonal 10%   herringbone 13%
boxes = ceil((area × (1+waste)) ÷ sqft_per_box)
underlay: area × 1.05; transition strips = count doorways
```

### Tile
```
tiles = (area ÷ tile_w/tile_h) × (1 + waste 10-15%)
grout lbs ≈ (area_ft² × joint_depth_in × joint_width_in × 16.7) per chart class
thinset: 50-lb bag per 90-120 ft² (3/16" trowel for large format)
```

### Fence
```
posts:    fence_length ÷ post_spacing (8 ft max for privacy) + 1
rails:    bays × rail_rows (2 standard, 3 for 6'+ or windy)
pickets:  fence_length ÷ (picket_width + gap)   (privacy gap 0; shadow ~ half-width)
concrete: 2 × 50-lb bags per post (or 1 × 80-lb) in normal soil
```

## Using the Script

```bash
# Paint a 12x14 room, 9 ft ceilings, 2 doors, 2 windows, 2 coats
python3 scripts/materials_estimator.py paint --room 12x14 --height 9 \
    --doors 2 --windows 2 --coats 2

# Mulch a 20x4 bed at 3 inches
python3 scripts/materials_estimator.py mulch --area 20x4 --depth-in 3

# 10x12 shed slab, 4 inches thick, 80-lb bags
python3 scripts/materials_estimator.py concrete --slab 10x12x4 --bag-lb 80

# 200 ft of fence, 6 ft privacy, 8 ft post spacing
python3 scripts/materials_estimator.py fence --length 200 --style privacy --post-spacing 8

# LVP flooring 550 ft², straight lay
python3 scripts/materials_estimator.py flooring --area 550 --pattern straight

# Consolidated list from several saved projects
python3 scripts/materials_estimator.py shopping-list
```

## Common Pitfalls

1. **Measuring floor area for paint.** Paint goes on walls: perimeter × height.
   Floor area is only for ceilings.
2. **One-coat math on new drywall.** New/patched drywall drinks the first
   coat (primer or diluted first coat); budget coverage at 250–300, not 400.
3. **Buying mulch in bags when the bed is big.** ≥ 4 yd³ → bulk delivery is
   typically half the price per yard and zero plastic.
4. **Forgetting waste factors on flooring patterns.** Herringbone eats 13%;
   a 550 ft² floor ordered at 5% waste comes up 40 ft² short.
5. **Mixing bag-count concrete for a 4" slab bigger than ~10×10.** That's 33+
   bags — line quality suffers; ready-mix is cheaper per ft³ past ~20 bags.
6. **Post holes sized to the post, not the load.** 4×4 post = 10-12" hole;
   depth = ⅓ above-ground height or below frost line, whichever is deeper.
7. **Rounding down to save a trip's worth of money.** Buy-unit rounding must
   round UP; the leftover pint/gallon is the cheapest insurance in DIY.

## Verification Checklist

- [ ] All dimensions in the units the script expects (feet / inches as flags say)
- [ ] Openings subtracted (doors/windows) for paint
- [ ] Correct waste/pattern factor applied for flooring & tile
- [ ] Bag counts rounded UP to whole purchase units
- [ ] Multi-project run ends with `shopping-list` consolidation before the store
