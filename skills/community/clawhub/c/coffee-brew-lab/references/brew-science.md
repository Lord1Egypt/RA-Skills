# Coffee Brew Lab — Reference

## Extraction: the one concept that explains everything

Coffee brewing is dissolving ~18–22% of the ground coffee's mass into water.
The SCA target zone is **18–22% extraction** at **1.15–1.45% TDS (strength)**
for filter coffee. Every taste defect maps to a position relative to that zone:

- **Under-extracted** (< ~18%): sour, grassy, salty, thin. The acids came out
  fast but the sugars and bitters never got time.
- **Over-extracted** (> ~22%): bitter, drying, hollow, astringent. You kept
  dissolving past the good stuff into tannins.
- **Wrong strength** (TDS out of band): weak/watery or harshly intense —
  this is the *ratio* (coffee:water), independent of extraction.

The four levers, in order of home usability: **grind size** (strongest lever),
**water temperature**, **contact time**, **agitation**. Ratio changes strength;
the other four change extraction. Diagnosis starts by deciding which axis
you're on — that single distinction fixes most people's dial-in confusion.

## Method profiles (defaults the script uses)

### Pour-over (V60 / Chemex / origami)
- Ratio 1:15–1:17 (1:16 default). 2 cups: 30g coffee, 480g water.
- Grind: medium-fine (table-salt finer side; ~600–800 µm).
- Water 92–96°C (light roasts hotter, dark roasts cooler — roast swaps the
  ceiling by ±3°C).
- Structure: bloom with 2–3× coffee weight in water, 45s; then 2–3 pours to
  60% by 1:15; total drawdown 2:30–3:30.
- Signs of good pour: bed flat at end, no high-and-dry grounds.

### French press
- Ratio 1:15 (immersion is less efficient per gram — dose up).
- Coarse grind (French press ~1000–1400 µm), 93–96°C.
- 4:00 steep → break crust, skim foam, wait 2:00, decant ALL of it (coffee
  left on grounds keeps extracting → bitterness).
- Press slowly; the plunger is a strainer, not a piston.

### AeroPress
- Ratio 1:12–1:14 (short dwell needs concentration), medium-fine.
- 85–92°C — the AeroPress's superpower is that lower temps + fine grind give
  sweetness without harshness (original championship recipes trend 80–85°C).
- 1:30–2:00 total including 20–30s press. Press stops at the hiss.

### Cold brew
- Concentrate 1:8 by weight, extra-coarse, room-temp water, 12–18h.
- Dilute 1:1 with water/milk to serve. Hot-water "flash" versions exist but
  the profile changes (more acidity).

### Moka pot
- 1:10, fine but NOT espresso-fine (finer packs the basket and channels).
- Start with cold water on low-medium heat; the goal is a slow, lazy stream.
- Gurgling/hissing = overheated = bitter; pull it off heat and cool the base
  under tap water to stop extraction. Serve immediately (moka coffee doesn't
  hold).

### Espresso
- Baseline: 18g in → 36g out (1:2) in 25–32s at 90–94°C.
- Changed ONE variable: grind finer to slow the shot, dose is last resort.
- Channeling (fast first drops + blonding early + simultaneous sour-bitter
  cup) = distribution problem: WDT / tamp level / headspace, not grind.

## Water chemistry (the silent 98%)

- SCA target: ~75–150 ppm TDS hardness as CaCO₃, ~40 ppm alkalinity, pH ~7.
- Tap water that tastes bad makes coffee that tastes bad — a carbon filter
  fixes most; distilled + third-party remineralization packets fix the rest.
- Hard-water failure mode: scale + dull flat cups. Soft-water failure mode:
  sour, empty cups that no grind change fixes. If diagnosis loops forever,
  suspect water before beans.

## Altitude correction

Boiling point drops ~1°C per 300m. At 1800m water boils at ~94°C — you cannot
pour 96°C. The script's `--altitude` flag lowers temperature targets to
min(target, boil−2°C) and flags the gap. On moka: boil point matters less (sealed
pressure) but the same intuition applies.

## The diagnosis tree in full

| Taste | Axis | Move (one at a time) |
|-------|------|----------------------|
| sour, grassy, salty | under-extraction | finer grind (first choice) |
| sour + very fast brew | under-extraction | finer grind; check dose accuracy |
| bitter, drying, astringent | over-extraction | coarser grind (first choice) |
| bitter + dark roast | over-extraction | lower temp 3–5°C before coarsening |
| harsh + intense + bitter | over-strength | raise ratio 1:15 → 1:16 |
| weak + watery, NOT sour | under-strength | lower ratio 1:16 → 1:15 |
| sour AND bitter together | channeling / uneven extraction | fix distribution; don't touch temp or grind yet |
| hollow, papery, boring | staleness / under-dose | check roast date (7–45d ideal), then dose +10% |
| great first sip, bad aftertaste | late over-extraction | shorten dwell / faster drawdown |

## Brew-log analysis method

The log is the memory the palate doesn't have. `log analyze` runs a simple
per-variable correlation (score vs grind/temp/dwell/ratio, Pearson r) and
prints the direction + strength. With ≥8 logged brews, the strongest
correlation is usually real for that grinder+bean pair. Rebuild the analysis
per bean — sweet spots do NOT transfer between roasts.

## Practical notes

- Scale to 0.1g matters more than any kettle. If it can't read 0.1g it's a
  kitchen scale, not a coffee scale.
- Purge thermoblock machines; first shots are temperature lies.
- Clean everything monthly (cafiza or equivalent): rancid oils read as
  "bitter" and send you chasing the wrong variable forever — the most common
  false diagnosis in home coffee.
