---
name: compost-balancer
description: "Use when you compost (or want to start) and the pile smells, stalls, or you don't know what to add: computes the C:N ratio of mixed ingredients from batch weights, diagnoses odor/moisture/temperature symptoms, fixes a pile with targeted 'add this much' prescriptions, sizes a system for your household waste stream, and tracks temperature curves. Solves the failed-backyard-pile problem that makes most beginners quit."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [compost, garden, soil, sustainability, organic-waste, c-n-ratio]
---

# Compost Balancer

## Overview

Backyard composting has a brutal attrition rate: most first piles go anaerobic, smell like sulfur or ammonia, attract flies, and get abandoned within a season. The failure is almost never mysterious — it's arithmetic. Compost microbes need a **carbon-to-nitrogen ratio near 25–30:1**, **moisture like a wrung-out sponge (50–60%)**, and **oxygen**. Kitchen scraps alone run 15–20:1 (too nitrogen-rich, soggy, sour); a pile of dry leaves runs 60:1 (nitrogen-starved, sits for a year). Neither composts. The fix is mixing, by weight, and nobody weighs things intuitively.

This skill is a calculator + diagnostician. Feed it what you're adding (ingredient + weight) and it computes the blended C:N and moisture, tells you what's missing, and prescribes exact additions ("add 2.1 kg of shredded cardboard or 3.5 kg dry leaves"). Feed it symptoms (smell, temperature, pest type) and it routes to the cause and the fix. It also sizes a bin system for a household from its waste stream, and explains the hot-thermophilic vs cold-slow tradeoff honestly.

## When to Use

- Starting a pile: what ratio of browns-to-greens for THIS week's scraps
- The pile smells (ammonia = too much nitrogen; rotten-egg = anaerobic = too wet/too dense)
- The pile isn't heating (C:N too high, too dry, too small, or just cold weather)
- Designing a system: bin size/count for household size, or sizing for fall leaf-cleanup surplus
- Deciding hot vs cold composting for your effort level
- Troubleshooting pests (flies/rodents = wrong ingredients exposed or meat/dairy in the mix)

**Don't use for:** commercial/municipal compost operations (different regulations, temperatures, and turning regimes), humanure (health-code territory), or worm bins (vermicomposting has its own moisture/pH rules — only the ingredient C:N table overlaps).

## The Model

1. **C:N by weight.** Each ingredient has a carbon:nitrogen ratio (table below). Blended C:N = Σ(mass × CNᵢ) / Σ(mass) — the script does the weighted average and reports the mix's ratio with a target band of 25–30:1.
2. **Rule-of-thumb volumes** for people who won't weigh: 2–3 parts *browns* : 1 part *greens* by loosely-packed volume approximates 30:1 for typical ingredients.
3. **Moisture.** Target 50–60%. Ingredient moisture table in the reference; squeeze test: a few drops = right, streaming = too wet, crumbles = too dry.
4. **Size threshold for hot composting.** ≥ 1 m³ (≈ 3 ft³ × 27) holds heat; smaller piles run cold-slow regardless of mix. Hot piles reach 55–65 °C in days if C:N, moisture, oxygen, and size are right.
5. **Turning.** Hot pile: turn when temperature drops from peak (every 3–7 days early). Cold pile: turn monthly or never (6–18 month timeline).

### Ingredient C:N quick table (avg values — varies by source)

| Ingredient | C:N | Class |
|---|---|---|
| Kitchen veg scraps | 15–20 | green (N) |
| Coffee grounds | 20 | green |
| Grass clippings (fresh) | 15–20 | green |
| Manure (chicken) | 7–10 | hot green |
| Manure (cow/horse) | 15–25 | green |
| Garden weeds (seed-free) | 20–30 | green-ish |
| Dry leaves | 50–60 | brown (C) |
| Straw/hay | 60–80 | brown |
| Shredded cardboard | 250–350 | concentrated brown |
| Wood chips/sawdust | 300–500 | concentrated brown |
| Paper (shredded) | 150–200 | brown |
| Pine needles | 60–80 | brown (slow) |

## Symptom → Cause → Fix Router

1. **Ammonia smell** = nitrogen excess (C:N < 20), often + too wet. Fix: mix in high-carbon browns per the calculator; turn.
2. **Rotten-egg / sour smell** = anaerobic (moisture > 65% or compaction). Fix: turn + add dry browns that wick (cardboard/leaves); check drainage.
3. **Not heating** — in order of likelihood: pile too small (<1 m³), too dry (<40%), C:N too high (>40, common in autumn leaf piles), insufficient oxygen, or ambient cold (insulate, don't expect thermophilic below ~10 °C ambient).
4. **Flies/maggots** = exposed food/meat. Fix: bury greens 15 cm under browns; never meat/dairy/oils in a cold bin.
5. **Rodents** = accessible food + cozy nesting. Fix: hardware cloth floor, bury scraps, no cooked food.
6. **Fire fang (white ash mold)** = past-peak dry hot pile. Normal-ish; turn and moisten.
7. **Slimy mats** (esp. grass clippings) = anaerobic pockets from layering too thick. Fix: thin layers <10 cm, mix, add structural browns for airspace.
8. **Finished?** Dark, crumbly, earthy-smell, unrecognizable ingredients, ~1/3 original volume. Sift coarse bits back in as starter culture.

## Common Pitfalls

1. **Weighing nothing, guessing everything.** "Some scraps, some leaves" fails silently. Weigh kitchen scraps for one week — once — and the script converts to a standing browns prescription.
2. **Autumn = all-browns pile.** A leaf-only pile sits until spring unless you add nitrogen (coffee grounds, fresh manure, grass, or even urea per reference).
3. **Adding soil "to make it work".** Small amounts inoculate; buckets just dilute and add weight. Soil is not a browns substitute.
4. **Compacting layers.** Oxygen lives in structure — mix, don't lasagna without turning; keep woody/straw material for airspace.
5. **Meat/dairy/oils in a cold bin.** Fine in a *maintained hot* pile (>55 °C for 15+ days) in some municipal regimes; in a backyard bin it's pest bait. Default: keep them out.
6. **Expecting hot speeds from a cold setup.** A 200 L bin of mixed waste will not hit 60 °C in winter. That's physics, not failure — adjust the timeline, or go bigger.
7. **Watering blindly.** City water is fine; the failure mode is a hose on an already-wet core. Squeeze-test first.

## Verification Checklist

- [ ] Blended C:N computed from actual weights, with target band shown
- [ ] If off-target: exact kg of named additions (both a strong-brown and a common-brown option)
- [ ] Moisture assessed (squeeze test / table) and corrected in the same pass
- [ ] Pile size vs hot-composting threshold stated
- [ ] Symptom routing done before math when the user reports smell/pests
- [ ] Timeline expectation set (hot: 4–8 wk with turning; cold: 6–18 mo)

## One-Shot Recipe

```bash
# this week's kitchen output: 3 kg scraps + 1 kg coffee — what to add?
python3 scripts/compost.py mix "scraps:3" "coffee:1"
# → C:N ~18:1 TOO NITROGENOUS → add 2.4 kg dry leaves or 0.4 kg cardboard

# symptom mode: pile smells like rotten eggs, rained all week
python3 scripts/compost.py diagnose --smell rotten-egg --moisture wet

# size a system: family of 4, wants hot composting
python3 scripts/compost.py size --people 4 --mode hot
```
