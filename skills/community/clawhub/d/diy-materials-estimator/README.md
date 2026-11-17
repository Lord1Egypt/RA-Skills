# DIY Materials Estimator

**Never make the third trip to the hardware store again.**

The defining DIY experience: 2 gallons bought, 2.6 needed. Mulch covered 80%
of the bed. The concrete ran out with two post holes left. Every one of those
failures is coverage physics done by vibe. This tool does it by math — seven
project calculators, one consolidated shopping list, quantities rounded UP to
real purchase units.

## What it computes

| Calculator | What you get |
|---|---|
| `paint` | Gallons from perimeter × height − openings, spread rate by surface, coats, primer/trim options, 5-gal-bucket heuristic |
| `mulch` | ft³ → yd³, 2-ft³/3-ft³ bag counts, bulk-delivery crossover at 4 yd³ |
| `concrete` | Slab or post-hole volume, 40/60/80-lb bag counts, water total, bag-vs-ready-mix crossover at ~20 bags, cure protocol |
| `drywall` | Sheet count by size + 10/15% waste, screws, tape, joint compound |
| `flooring` | Area × waste by pattern (5% straight / 10% diagonal / 13% herringbone), box rounding, underlayment |
| `tile` | Tile count, box rounding, sanded-grout lbs from tile+joint chart, thinset bags |
| `fence` | Posts (spacing ≤8 ft), rails, pickets by style/gap, concrete per post, fastener count |

## Quick start

```bash
# Paint a 12x14 room, 9 ft walls, 2 doors, 2 windows, 2 coats + ceiling
python3 scripts/materials_estimator.py paint --room 12x14 --height 9 \
    --doors 2 --windows 2 --coats 2 --ceiling --primer

# 10x12 shed slab at 4 in, 80-lb bags
python3 scripts/materials_estimator.py concrete --slab 10x12x4

# 26 fence posts' worth: holes only
python3 scripts/materials_estimator.py concrete --holes 26,10,30

# 200 ft privacy fence
python3 scripts/materials_estimator.py fence --length 200 --style privacy

# 550 ft2 LVP, herringbone, 23.8 ft2/box
python3 scripts/materials_estimator.py flooring --area 550 --pattern herringbone --box-sqft 23.8

# Consolidate everything into one store run
python3 scripts/materials_estimator.py shopping-list
```

The 10×12×4 slab answer (67 × 80-lb bags) is the tool telling you to order
ready-mix — that crossover saves backs and weekends.

## Who needs this

- Homeowners and renters doing any painting, flooring, fencing, or landscaping
- First-time DIYers with no intuition for spread rates and waste factors
- Landlords and property managers pricing small jobs before calling a pro
- Anyone who has ever stood in a store aisle thinking "wait, how many bags?"

## What's inside

- `SKILL.md` — per-material physics, depth/waste doctrines, pitfalls
- `references/materials-math.md` — constants sources, worked examples, unit
  sanity table, bag-vs-bulk crossovers, safety notes
- `scripts/materials_estimator.py` — stdlib-only CLI; saves each estimate to
  `materials_jobs.json` for the consolidated shopping list

Stdlib Python only. No network, no keys. Estimates are purchasing-grade
(slightly conservative), not bid-grade.

## License

MIT © Denis Voronin
