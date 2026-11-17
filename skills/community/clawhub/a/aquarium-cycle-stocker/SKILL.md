---
name: aquarium-cycle-stocker
description: "Use when starting or restocking a fish tank: fishless nitrogen-cycle planning with dosing schedule, bioload-safe stocking plans (adult-size IOU rule), compatibility screening, and a nitrate-driven water-change scheduler. Prevents new-tank syndrome and overstocking deaths."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [aquarium, fishkeeping, nitrogen-cycle, stocking, water-change, hobby]
---

# Aquarium Cycle & Stocker

## Overview

Most fish deaths happen in the first 6 weeks — "new tank syndrome" — because ammonia and
nitrite are invisible killers that spike before beneficial bacteria colonize. And most
overcrowded tanks were stocked by inches-of-fish rules of thumb that ignore adult size,
biomass, and filter capacity. This skill plans the **fishless cycle with an exact ammonia
dosing calendar**, computes a **bioload-safe stocking plan from adult sizes** (not the
cute juveniles in the store), screens species compatibility, and turns your nitrate
readings into a **water-change schedule that keeps up with production**.

## When to Use

- Setting up a new tank: "when can I add fish?" (answer: a dated cycle calendar)
- Cycle crashed / detectable ammonia or nitrite in an established tank
- Choosing fish: how many of what, in this tank, without disaster
- Nitrate creeping: how big/how often must water changes be
- Vacation/hospital/planted-tank variants of the above

**Don't use for:** reef/marine chemistry (this is freshwater logic; saltwater adds Ca/Alk/Mg
budgeting), or medication dosing (follow the product + quarantine protocol).

## The Nitrogen Cycle (what the plan automates)

```
fish waste / decaying food  →  NH₃/NH₄⁺ (ammonia, TOXIC >0.25 ppm)
   → Nitrosomonas (colonize ~2-3 wk at 25-27°C) → NO₂⁻ (nitrite, TOXIC; blocks blood O₂)
   → Nitrobacter/Nitrospira (~1-2 wk later) → NO₃⁻ (nitrate; safe <40, best <20)
   → removed only by water changes / plants / (anaerobic denitrification in deep substrate)
```

**Fishless cycling** (the humane method): dose pure ammonia to 2–4 ppm, wait for nitrite
spike then fall, wait for nitrate rise, then dose again — "bottle of ammonia to a full
cycle" in ~3–6 weeks. The script prints the dated calendar with what you'll test each day.

**Speedups:** bottled bacteria (Tetra SafeStart, FritzZyme 900, Fluval Cycle) genuinely
shorten to 1–2 weeks; higher temp (27–28°C, no fish!), pH ≥7, oxygenation help. Pure
ammonia must be surfactant-free (shake test: no foam).

## Numbered Workflow

1. Collect: tank volume (real: interior L×W×H minus substrate/displacement), filter type
   + flow rating, intended stocking list, temperature, tap-water parameters (pH, and
   whether tap nitrate is already high), test kit availability.
2. Run `scripts/tank_plan.py cycle --volume 75 --temp 26 [--bacteria]` → dated dosing and
   testing calendar with expected readings per phase and a "safe to stock" gate
   (0 ammonia, 0 nitrite, nitrates present, processes 2 ppm in ≤24 h).
3. Run `scripts/tank_plan.py stock --volume 75 --fish "6 harlequin rasbora" --fish "1 honey gourami" ...`
   → adult-size biomass totals, IOU warning (buy juveniles = adult bioload), compatibility
   screen (temp/pH/hardness overlap, aggression classes, schooling minimums), verdict.
4. Run `scripts/tank_plan.py wc --volume 75 --nitrate 35 --target 20` → water-change size
   and frequency to hold nitrate at target given tap nitrate.
5. Print the emergency card: fish-in-cycle fallback (if fish are already in), 25-50% daily
   changes + Prime/Amquel dosing, when to stop feeding.

## Stocking Rules Encoded

- **1 cm of adult fish per liter** is the classical ceiling; the script uses adult length
  × biomass factor (body-shape weighted: a 10cm goldfish ≈ 5× a 10cm tetra).
- Schooling fish need ≥6 of their own kind or they stress/pine.
- **Betta + guppy/tiger barb = no**; the compatibility screen knows the classic conflicts.
- Bottom coverage: 1 bottom-dweller per 15×15 cm footprint, needs sand if burrowers.
- Filter turnover: 4–6× volume/hour (gentle for bettas, higher for goldfish/messy fish).

## Pitfalls

1. **Stocking by juvenile size.** A 2 cm juvenile iridescent shark is a 100 cm adult.
   Always compute adult bioload ("the IOU you sign at the register").
2. **"One inch per gallon" with body shape ignored.** Goldfish are 3–4× the biomass per cm
   of a neon tetra. The script weights by shape class.
3. **Testing right after a water change** — always test BEFORE the change, 24h stable.
4. **Washing filter media in tap water** — chloramine kills the colony you spent a month
   building. Rinse in tank water only.
5. **Ammonia spike after adding fish "because the pet store said it's fine."** The gate is
   a 2-ppm clearance test in 24 h, not calendar days.
6. **Nitrate math without tap nitrate.** If your tap is 20 ppm NO₃ you can never get below
   20 with water changes alone — plants, resins, or RO blend needed. Script asks.
7. **All the fish at once.** Stock in waves 2 weeks apart even on a cycled tank; bacteria
   capacity needs to catch up to each bioload step.

## Example

```
$ python3 scripts/tank_plan.py cycle --volume 75 --temp 26 --bacteria
Day  1 (2026-10-24): dose ammonia to 3 ppm; test NH₃/NO₂ baseline
Day  7: NO₂ spike phase (can exceed 5 ppm — toxic, no fish!). Keep NH₃ at 2-3 ppm.
Day 17: CLEARANCE TEST — dose 2 ppm NH₃; if NH₃=0 AND NO₂=0 within 24h: CYCLED
 → safe to stock: add ONE wave (see stocking plan), feed lightly, test daily 1 week.
 Expected ~10 days seeded (vs 4-6 wk unseeded); the GATE is the 24-h clearance test, not dates.

$ python3 scripts/tank_plan.py stock --volume 75 --fish "10 neon tetra" --fish "6 corydoras" --fish "1 betta"
BIOMASS: adult bioload 85.7/75 = 114% → MAX (heavy: strict water changes + weekly NH₃ tests)
COMPATIBILITY: betta + neon tetra = RISKY (neons nip betta fins; prefer ember/chili rasbora)
SCHOOLING: neons ≥6 ✓ (10), corydoras ≥6 ✓
TEMP 24-26°C overlap ✓ | pH 6.5-7.0 overlap ✓
STOCK IN WAVES: tetras week 1 → +14d → cories → +14d → betta last.
 Try instead: 8 ember tetra + 6 corydoras + 1 honey gourami = 64% load, zero conflicts.

$ python3 scripts/tank_plan.py wc --volume 75 --nitrate 35 --target 20 --tap 8 --production 12
 ONE-SHOT to target: change 56% (42 L) now.
 HOLD at target with production 12 ppm/wk: needs ~62% weekly — or cut feeding/add plants.
```

## Verification Checklist

- [ ] Real volume measured (interior dims minus substrate/rocks), not the box number
- [ ] Cycle gate = 2 ppm ammonia clearance in 24 h, tested twice
- [ ] Stocking computed at ADULT sizes, shape-weighted
- [ ] Schooling minimums and compatibility flags surfaced
- [ ] Water-change plan accounts for tap nitrate floor
- [ ] Emergency fish-in-cycle card given if fish are already present
