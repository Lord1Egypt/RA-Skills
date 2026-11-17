---
name: firewood-cord-calculator
description: Use when buying, selling, stacking, or seasoning firewood — verifies true cord volume vs the "face cord"/"rick"/"truckload" shell game (128 ft³ vs 42), compares species BTU per cord and cost-per-MMBtu against propane/heat-pump resistance heat, computes seasoning time from split size and moisture with the 20% burn rule, and sizes annual consumption from climate house-heating demand.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [firewood, cord, wood-stove, heating, btu, seasoning, homestead]
---

# Firewood Cord Calculator

## Overview

Firewood is sold in a language designed to confuse: a "cord" is 128 ft³
(tightly stacked 4×4×8), a "face cord" is a third of that, a "rick"
is whatever the seller's rack measures, and a "truckload" is poetry. On
top of the volume shell game, species vary 2× in energy per cord (osage
orange ~30 MMBtu vs aspen ~14), green wood burns at ~60% of dry-wood heat
(evaporating water costs BTUs), and "seasoned" often means "cut last
month." `scripts/cord_calc.py` does the honest math: real stacked volume
→ true cord fraction, species-corrected energy, moisture-adjusted BTUs,
cost-per-MMBtu vs competing fuels, seasoning clock from split thickness
and stack airflow, and annual consumption from house heating demand.

## When to Use

- Buying firewood: someone offers "a cord, delivered and stacked, $350" —
  is it a cord, and is that fair vs $2.50/gal propane?
- Selling your own: pricing per face cord without shorting yourself.
- Seasoning planning: when must oak be split and stacked to be ready for
  November?
- Stove efficiency reality: comparing wood heat cost against your heat
  pump / furnace / resistance backup.
- Post-storm cleanup: how much actual heating value is in that downed
  cherry.

**Don't use for:** pellet stoves (sold by weight/BTU-per-bag, different
economy), commercial boiler sizing (needs load calcs), or fireplace
decorative burning (efficiency ~-10%, it's an ornament).

## How It Works

1. **Volume honesty.** A cord = 128 ft³ stacked (not loose: loose-thrown
   wood is ~25-30% air, so a "loose cord" is ~0.7 cord). The script takes
   your stack dimensions (or count of face cords / ricks with rack size)
   and reports true cord fraction. Packing factor: tight stack 0.95-1.0,
   typical hand-stack 0.90, thrown/loose 0.65-0.70.
2. **Species BTU table.** Per-cord energy at 20% moisture: hedge/osage
   ~30, oak ~24-29, locust ~27, maple ~22-24, birch ~20-23, cherry ~20,
   pine ~14-17 (softwood: burn hot/fast, creosote risk in cold chimneys),
   aspen/poplar ~14. The script converts to delivered heat using stove
   efficiency (EPA non-cat ~63-78%, cat ~75-83%, open fireplace ~-10%).
3. **Moisture correction.** Every pound of water in wood eats ~1,050 BTU
   evaporating. Green (50% MC) vs seasoned (20% MC) is the difference
   between a stove that heats and one that steams. Meter reading (probe
   on a freshly split face, average of 3) drives the correction factor.
4. **Cost-per-MMBtu comparison.** Wood price ÷ (delivered MMBtu) vs
   propane ($/gal ÷ 0.0916 MMBtu/gal × efficiency), natural gas ($/therm
   ÷ 0.1 × eff), resistance electric (÷ 1.0 × 1.0), heat pump (÷ 1.0 ×
   COP). The table tells you what a "fair" cord price is in YOUR fuel
   market.
5. **Seasoning clock.** Rule-of-thumb drying times to <20% MC: softwoods
   6-12 months, maple/birch 9-12, oak 12-24 (splits >6" need the long
   end). Drying drivers: split thickness (thinner dries faster),
   airflow/spacing (single row, sun, wind > stacked-against-shed), bark
   (split bark-down on softwoods... it holds moisture), top cover with
   open sides. The script back-plans "ready by Nov 1" dates per species.
6. **Annual consumption.** House heating demand (from climate zone HDD65
   and your fuel bills, or a rough BTU/ft²·HDD U-factor) ÷ stove
   delivered-BTU per cord = cords/year, with a 71% "you'll burn 1.4× the
   estimate" reality factor for the first year.

## Using the Script

```
# is it really a cord? 8ft x 4ft x 16in face cords, hand-stacked
python3 scripts/cord_calc.py --volume --length-ft 8 --height-ft 4 --depth-in 16

# 3 face cords of red oak at $300/cord, 22% moisture, EPA stove 70%
python3 scripts/cord_calc.py --evaluate --species red-oak --cords 1.0 \
  --price 300 --moisture 22 --efficiency 0.70

# fuel comparison in a $2.60/gal propane, $1.40/therm gas market
python3 scripts/cord_calc.py --compare --price 300 --species red-oak \
  --propane 2.60 --gas 1.40 --electricity 0.14 --heatpump-cop 3.0

# seasoning: when to split white oak for Nov 1
python3 scripts/cord_calc.py --season --species white-oak --split-in 5 --ready 2027-11-01

# annual need: 2000 ft² house, 5000 HDD65 climate
python3 scripts/cord_calc.py --annual --sqft 2000 --hdd 5000 --species red-oak
```

## Common Pitfalls

1. **"Face cord" priced like a cord.** A face cord (16" depth) is 1/3 of
   a cord. $150/face cord = $450/cord. The unit must be named before the
   price means anything.
2. **Loose-thrown volume counted as stacked.** A pickup "full cord,
   thrown" is ~0.5-0.65 stacked cord. Loose piles need the 0.65-0.70
   packing factor or you're buying air.
3. **Green wood BTU math done dry.** At 50% MC, roughly 40% of the
   potential heat goes up as steam. "Freshly cut, seasoned 2 months"
   oak is green oak.
4. **Trusting "seasoned" without a meter.** $25 moisture meter on a fresh
   split face settles it: <20% burns, 20-25% workable, >25% steams. Split
   a piece and measure — surface reading of a weathered log lies.
5. **Softwood in a slow overnight burn.** Pine's resin contributes to
   creosote when burned cool/damped; fine hot and fast, risky in a
   damped stove with a cool chimney.
6. **Ignoring stove efficiency.** An open fireplace has NEGATIVE heating
   efficiency (draws house air up the flue). Delivered BTUs = wood BTUs ×
   stove efficiency, and that 0.6-0.8 factor is the whole ballgame.
7. **First-year estimate without the reality factor.** Fires get lit for
   ambiance, not just demand. Plan 1.4× the calculated consumption.

## Verification Checklist

- [ ] Stack measured (L×H×D) with packing factor applied; cords to 2 decimals.
- [ ] Species identified (or worst-case mix assumed) before BTU math.
- [ ] Moisture measured on fresh-split faces, 3 readings averaged.
- [ ] Stove efficiency stated (not assumed 100%).
- [ ] Cost-per-MMBtu compared against ACTUAL local fuel prices.
- [ ] Seasoning plan dated backward from burn date with species-specific time.
- [ ] Annual estimate includes the 1.4× first-year factor.
