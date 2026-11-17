# DIY Materials Estimator — Reference

## 1. Where the numbers come from

All constants are manufacturer/norm mid-bands used for *purchasing* (slightly
conservative), not for competitive bidding:

- **Paint spread rates:** US paint manufacturers (Behr, Sherwin-Williams,
  Benjamin Moore) publish 350–450 ft²/gal for smooth interior surfaces, one
  coat; industry planning uses 350–400. Textured, bare drywall, or exterior
  rough surfaces: 200–300. Primer: 300–400.
- **Concrete bag yield:** a 80-lb bag of QUIKRETE yields ≈ 0.60 ft³; 60-lb ≈
  0.45 ft³; 40-lb ≈ 0.30 ft³ (packaging states both mix and yield).
- **Drywall:** 4×8 sheet = 32 ft²; waste 10% standard (cut-outs, breaks),
  15% when diagonal or lots of openings.
- **Flooring waste:** NWFA/MFMA guidance: 5% straight, 7–10% diagonal or rooms
  with many jogs, 13–15% herringbone/chevron (short pieces are unusable).
- **Mulch depth:** university extension consensus (e.g., extension services)
  2–3 in (5–7.5 cm) refresh/suppress, 4 in (10 cm) new beds; keep off trunks.
- **Fence:** post spacing ≤ 8 ft for privacy fence (6 ft pickets need 2–3
  rails); picket count = length ÷ (picket + gap); concrete: two 50-lb or one
  80-lb bag per post in normal soil.

## 2. Worked examples (hand-checkable)

### Paint — 12×14 room, 9 ft walls, 2 doors, 2 windows, 2 coats
```
perimeter = 2×(12+14) = 52 ft
gross wall = 52 × 9 = 468 ft²
openings   = 2×21 + 2×12 = 66 ft²
net wall   = 402 ft²
ceiling    = 12 × 14 = 168 ft² (if painting)
paint      = 402 ÷ 350 × 2 coats ÷ 0.95 ≈ 2.4 gal → BUY 3 gal (or 1×5-gal)
```

### Concrete — 10×12 slab, 4 in
```
volume = 10 × 12 × (4/12) = 40 ft³
80-lb bags = 40 ÷ 0.60 = 67 bags  ← past crossover; get ready-mix
(trailer mix ~$140-180 vs 67 bags ~$180 + mixing labor)
```

### Mulch — 20×4 bed, 3 in
```
ft³ = 80 × 0.25 = 20 ft³ → 0.74 yd³
2-ft³ bags: 10 bags | bulk: ¾ yd³ (min-delivery territory; bag it)
```

### Fence — 200 ft privacy, 8 ft spacing, 5.5" pickets, no gap
```
posts = 200/8 + 1 = 26
bays = 25; rails = 25 × 3 (6-ft height) = 75 (38 boards of 16 ft)
pickets = 200 ft × 12 / 5.5 = 436 → +5% waste ≈ 458
concrete = 26 × 1 (80-lb) = 26 bags
```

## 3. Bag-vs-bulk and ready-mix crossover

- Concrete: past ~20 bags (~12 ft³), ready-mix (truck) or rent a trailer
  mixer — cost per ft³ flips and mix quality becomes uniform.
- Mulch/soil: past ~4 yd³ (108 ft³ = 54 two-ft³ bags), bulk delivery wins on
  price alone; bags win under 2 yd³ (car transport, weekend pace).
- Gravel base: compacted depth (path 2-3", driveway 4-6" + fines); order by
  the ton (1 yd³ ≈ 1.4 tons crushed stone; 1 yd³ ≈ 0.75 tons soil/mulch).

## 4. Unit sanity table

| Material | Purchase unit | Covers |
|---|---|---|
| Interior paint | 1 gal | 350-400 ft² one coat smooth |
| Exterior paint | 1 gal | 250-350 ft² one coat |
| Primer | 1 gal | 300-400 ft² |
| 80-lb concrete bag | bag | 0.60 ft³ |
| 60-lb concrete bag | bag | 0.45 ft³ |
| Mulch bag (2 ft³) | bag | 24 ft² at 1" / 8 ft² at 3" |
| Drywall 4×8 | sheet | 32 ft² |
| Joint compound | 4.5-gal pail | 400-550 ft² of joints (new work) |
| Drywall screws 1¼" | 1-lb (~300) | ~300 ft² at 1/ft² |
| Thinset 50 lb | bag | 90-120 ft² (3/16" v-notch, large format 1/4") |
| Grout | 25 lb | chart: ~100-250 ft² depending on tile/joint |

## 5. Safety notes worth repeating

- Concrete wet mix is caustic (pH ~13): gloves, eye protection; wash skin
  15 min if embedded.
- Silica dust when cutting tile/drywall/masonry: wet-cut or respirator
  (P100/N95 at minimum); OSHA silica rule exists for a reason.
- Paint/strain/stain VOCs: ventilate; pilot lights off for solvent finishes.
- Lifting: 80-lb bags and 5-gal buckets are the classic DIY back injury;
  use a cart, split loads, or buy 60-lb bags.
