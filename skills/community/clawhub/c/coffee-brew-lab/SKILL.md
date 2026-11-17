---
name: coffee-brew-lab
description: Use when dialing in pour-over, French press, AeroPress, cold brew, or espresso at home — SCA golden-ratio water math, grind/temperature/dwell per method, a taste→parameter diagnosis tree (bitter→coarser/lower temp, sour→finer/hotter), and a brew-log regression that finds YOUR best extraction time.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [coffee, brewing, pour-over, espresso, ratio-calculator, recipe, kitchen]
---

# Coffee Brew Lab

## Overview

A dial-in instrument for manual coffee brewing. Two engines: (1) **recipe
math** — SCA golden ratio (1:15–1:18), method-specific grind/temperature/dwell
profiles, bloom and pulse schedules, temperature-corrected for altitude;
(2) **taste diagnosis** — a defect→cause tree that converts "bitter, hollow,
sour" into concrete parameter moves, plus a brew log that tracks every shot
and identifies which variable actually correlates with your best cups.

## When to Use

- "How much coffee/water for N cups?" — ratio math for any method
- "My coffee tastes bitter/sour/weak/harsh" — diagnosis tree
- Dialing in a new bag, grinder, or method (pour-over, AeroPress, French
  press, cold brew, moka, espresso)
- "What grind size / temperature for X method?" — method profiles
- Keeping a brew log and finding personal sweet spots

Don't use for: where to buy beans, milk-frothing art, or cafe business ops.

## Method Profiles (summary; full table in references)

| Method | Ratio | Grind | Water | Dwell | Notes |
|--------|-------|-------|-------|-------|-------|
| Pour-over V60 | 1:16 | medium-fine | 92–96°C | 2:30–3:30 | bloom 45–60s at 2× water |
| French press | 1:15 | coarse | 93–96°C | 4:00 | break crust at 4:00, skim, 2 min settle |
| AeroPress | 1:13 | medium-fine | 85–92°C | 1:30–2:00 | lower temp tames acidity |
| Cold brew | 1:8 (conc.) | extra-coarse | 20°C | 12–18h | dilute 1:1 to serve |
| Moka | 1:10 | fine (not espresso-fine) | from cold | — | just-off-boiler, serve immediately |
| Espresso | 1:2 | fine | 90–94°C | 25–32s | 18g in → 36g out baseline |

## The Diagnosis Tree (core of the skill)

**Bitter / harsh / drying aftertaste = OVER-extraction** → coarser grind OR
lower temperature OR shorter dwell OR less agitation (one variable at a time).

**Sour / grassy / salty / thin-sour = UNDER-extraction** → finer grind OR
hotter water OR longer dwell OR more agitation.

**Weak / watery but not sour = ratio problem** → more coffee (lower ratio
number, e.g. 1:16 → 1:15), not a grind change.

**Both bitter AND sour = channeling or uneven grind** → fix distribution,
pulse pouring, check grinder for bimodal distribution; do NOT chase with
temperature.

**Hollow / boring / papery = stale beans or under-dose** → check roast date
(ideally 7–45 days), then dose.

Rule: **change ONE variable per cup**, log it, keep the winner.

## Numbered Workflow

1. `recipe --method v60 --cups 2 --ratio 16` → grams coffee, water, bloom,
   pour schedule, grind, temperature (altitude-corrected if `--altitude`).
2. Brew it. Taste against the descriptors above.
3. `log add` the brew: method, ratio, grind setting, temp, dwell, and a
   1–10 score plus defect tags (bitter/sour/weak/balanced).
4. `diagnose bitter` (etc.) → get the prescribed single-variable move.
5. Apply the move, brew, log again. 2–4 iterations converge for most setups.
6. `log best` → your top cups and the parameters they share;
   `log analyze` → simple regression of score vs each numeric variable.

## Commands

```
python3 scripts/brew_lab.py recipe --method v60 --cups 2
python3 scripts/brew_lab.py recipe --method french-press --grams 30
python3 scripts/brew_lab.py recipe --method cold-brew --liters 1
python3 scripts/brew_lab.py diagnose bitter
python3 scripts/brew_lab.py diagnose sour-and-bitter
python3 scripts/brew_lab.py log add --method v60 --grams 15 --water 240 \
  --grind 4.5 --temp 93 --dwell 180 --score 7 --tags bitter
python3 scripts/brew_lab.py log best
python3 scripts/brew_lab.py log analyze
```

Brew log: `brew_log.json` next to the script (`--store` to override).

## Pitfalls

1. **Changing two variables at once** — you learn nothing. The log enforces
   nothing; discipline is yours. Change grind OR temp OR time, never two.
2. **Chasing bitterness with dose** — bitterness is extraction; dose fixes
   strength. Wrong axis, wasted beans.
3. **Trustiing thermos-kettle numbers** — many kettles read 3–6°C high; verify
   once with a real thermometer and adjust mentally forever.
4. **Grinder settings aren't portable** — "4.5 clicks" is YOUR grinder's
   language. Log your own numbers; never copy someone else's.
5. **Judging boiling-hot coffee** — high temps mute sweetness and amplify
   bitterness. Taste at ~60–65°C, slurped aerated.

## Example

New Ethiopian light roast tastes "sour and thin": diagnosis says
under-extraction → grind 2 clicks finer, same everything else → next cup
"sour mostly gone, slightly hollow" → +1 click finer and temp 93→95°C is
NOT allowed (two variables) → grind only → "balanced, juicy, 8/10". Log shows
best cups cluster at grind 3.5, 94°C, 3:00 — that's the bag's sweet spot,
recorded for next time you buy it.
