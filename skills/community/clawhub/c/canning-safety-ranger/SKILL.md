---
name: canning-safety-ranger
description: "Use when canning or preserving food at home (or evaluating a canning recipe) — jars, acidity, pressure vs water-bath, altitude, storage, or suspect-jar triage. Screens recipes against botulism rules, computes process-time/pressure corrections, and triages spoiled vs safe jars."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [canning, preserving, food-safety, botulism, pressure-canning]
---

# Canning Safety Ranger — Preserves Without the Poison Lottery

## Overview

Home canning is the one cooking domain where a mistake isn't "bad dinner" — it's
**botulism**, a toxin produced by *Clostridium botulinum* spores that survive boiling water
and multiply in low-acid, airless jars. The rules are few, physical, and non-negotiable:
acid below pH 4.6 (or pressure), time-at-temperature per jar size and food density, and
altitude corrections because boiling point drops as you climb. Every canning-safety scandal
traces to one of about seven violations.

This skill screens a recipe or plan against the USDA/NCHFP rule set, computes corrected
process times and pressures for your altitude, sizes batch throughput, and triages
suspect jars (seal failed? lid domed? smells off?) into eat-refrigerate-discard verdicts
with the reasoning stated.

## When to Use

- Planning a canning session: tomatoes, salsa, pickles, jam, green beans, meat, stock, fish
- Evaluating a recipe (grandma's, Pinterest, a book) for safety before running it
- Questions like "can I water-bath green beans if I add vinegar?" or "why did my lids fail?"
- Altitude confusion: "I'm at 6,000 ft — the recipe says 10 minutes, is that right?"
- Post-canning triage: a jar didn't seal / lid bulges / foam / smell — keep or kill?
- Don't use for: fermentation (sauerkraut/kimchi have live cultures, different rules),
  freezing, dehydrating (adjacent, but not this skill), or commercial production

## Core Knowledge

### 1. The acid gate — the single most important rule

```
pH < 4.6  → water-bath or steam canning is SAFE (acid stops botulinum)
pH ≥ 4.6  → MUST pressure-can (240°F/116°C kills spores) — no exceptions
```

Foods by nature:

| Food | Natural pH | Verdict |
|---|---|---|
| Most fruits, jams, jellies, pickles (with proper vinegar) | <4.6 | water-bath OK |
| **Tomatoes** | 4.3–4.9 — borderline! | water-bath ONLY with added acid (bottled lemon juice 2 Tbsp/quart or 1/4 tsp citric acid/quart) |
| Green beans, corn, potatoes, meat, stock, soups | 6.0+ | pressure-can ONLY |
| Salsas, sauces with low-acid veggies mixed in | mixed | must follow a **tested recipe** — the veggie ratio changes pH; do not improvise acid math |
| Pureed low-acid (pumpkin butter, mashed squash) | dense + low-acid | **no safe home process exists** — don't can it |

### 2. Process time & pressure (the physics)

- Water-bath times are calibrated for **sea level**; every 1,000 ft of altitude lowers boiling
  point ~2°F → add processing time (5 min per 1,000 ft above 1,000 ft; exact ladder below).
- Pressure canning: higher altitude needs MORE pressure (weighted gauge +0.5 psi /
  1,000 ft over 2,000 ft; dial gauge +1 psi per 2,000 ft over sea level).
- Jar size matters: quarts take longer than pints (heat penetration). Never open-kettle
  (hot food into hot jars, no process) or oven-can — both are unprocessed by definition.
- Density matters: the tested time for whole tomatoes won't safely cover crushed-and-heated
  sauce. Follow the *tested process* matching your preparation, not the ingredient.

### 3. Equipment gates

- **Dial-gauge canners** must be tested yearly (extension office) — they drift.
- Weighted-gauge canners (jiggle at 5/10/15) don't need testing; use the 10 lb weight ≤1,000 ft,
  15 lb above.
- Lids: single-use (the compound); rings rust-free and reusable. Plastic reusable lids exist —
  follow manufacturer process.
- Jar defects: nicks on the rim = seal failure; always finger-tight + lids + vent + purge.

### 4. The seven deadly violations (the screen the script runs)

1. Water-bathing any low-acid food (beans/corn/meat/stock/soup/vegetables)
2. Tomatoes without added acid
3. Improvised "family recipe" salsa/sauce with untested veggie-acid ratios
4. Open-kettle or oven canning
5. No altitude correction (time or pressure)
6. Thickeners/flour/rice/pasta/butter added before processing (density + heat penetration)
   — including "pumpkin butter" and creamed soups
6b. Dairy and eggs are not home-cannable, period
7. Paraffin seals, flipped-jar "sealing", asbestos-era short times from old books

### 5. Storage & triage

- Store without rings (a false seal can "hold" from ring pressure; removing rings reveals it),
  cool dark place, 12–18 months best quality (safety persists if sealed, quality fades)
- **Signs of death** (discard violently — toxin is invisible and odorless, but these indicate
  spoilage risk): bulging lid, unsealed, spurting liquid on open, mold, fizzing, off-smell,
  rising bubbles. Toxin is destroyed by boiling 10 min, but you triage, not gamble.
- Suspect jar? Boil home-canned low-acid foods 10 min (rolling) + 1 min per 1,000 ft altitude
  before tasting — the classic safety net (protects against low-level contamination).

## Workflow

1. **Describe the plan**: what food, preparation style, jar size, method (water-bath/pressure),
   altitude, recipe source (tested-book / internet / heirloom).
2. **Screen:**
   ```bash
   python3 scripts/canning_ranger.py --demo
   python3 scripts/canning_ranger.py --screen --food "tomato sauce" --method water-bath --altitude 5000
   python3 scripts/canning_ranger.py --time pints water-bath 35 5000
   python3 scripts/canning_ranger.py --pressure quarts 11 6500 weighted
   python3 scripts/canning_ranger.py --jar bulging-lid low-acid
   ```
3. **Read the verdict**: SAFE / NEEDS-ACID / PRESSURE-ONLY / UNSAFE-PROCESS / NEVER-CAN with
   the violated rule named.
4. **Apply corrections**: altitude-adjusted time or pressure, acid additions for tomatoes,
   jar-size-appropriate tested process.
5. **Triage suspect jars** with `--jar` before eating anything questionable.

## Common Pitfalls

1. **"My grandmother water-bathed beans for 40 years."** Survivorship bias + lower-risk era
   gardens; spore luck isn't a protocol. Pressure-can low-acid, always.
2. **Treating tomatoes as high-acid.** Modern varieties sit at pH 4.6+; acidify every jar
   (2 Tbsp bottled lemon juice or 1/4 tsp citric acid per quart) or pressure-can them.
3. **Ignoring altitude.** At 7,000 ft water boils at ~199°F; a sea-level 20-minute process is
   under-processed. Times AND pressures need the correction ladder.
4. **Improvising salsa.** Adding peppers/onions raises pH; only tested recipes (NCHFP/Ball)
   with stated vinegar ratios are screenable as safe. "Taste" is not a pH measurement.
5. **Thickening before processing.** Flour/rice/pasta/butter slow heat penetration beyond any
   tested time. Add thickeners when reheating, never in the jar.
6. **Rings left on stored jars** — masks false seals. Remove after 24h, store ringless.
7. **Trusting float tests / tilts / taps.** Seal = concave lid + clean ring-of-suction sound.
   Everything else is folklore; when unsure, reprocess within 24h or refrigerate.

## Verification Checklist

- [ ] Every food classified acid / borderline / low-acid with the right method enforced
- [ ] Tomatoes: acid addition specified per jar size
- [ ] Process time or pressure corrected for altitude and jar size
- [ ] Recipe source gate: tested recipe required for mixed-acid preparations
- [ ] No thickeners/dairy/eggs/flour/pasta in any process
- [ ] Suspect jars triaged with explicit keep/refrigerate/discard verdict
- [ ] Storage doctrine given (rings off, cool, dark, date-labeled)

## One-Shot Recipe: green beans at 5,000 ft

Plan: "water-bath green beans 30 minutes, grandma's book." Screen → VIOLATION 1 (low-acid,
water-bath). Corrected: pressure-can at 5,000 ft — dial gauge 13 psi / weighted 15 lb,
pints 20 min, quarts 25 min (raw pack). Lid check at 24h, rings off, label with date and
altitude-corrected process. A 20-cent jar of beans is never worth 3 weeks on a ventilator.
