# Compost Engineering Reference

## 1. The microbiology in one page

Composting is aerobic microbial oxidation of organic matter. Two thermal phases:

- **Mesophilic (0–40 °C):** startup crowd, 1–3 days in a good mix.
- **Thermophilic (40–70 °C):** bacteria take over; this is where weed seeds and most pathogens die. Needs ≥55 °C for ≥3 days (turn to expose all material) for "sanitizing" — 15 days across 5 turns is the EPA/backyard gold standard.
- **Curing:** after peak heat subsides, fungi and actinomycetes finish lignin/cellulose; 2–8 weeks. Underrated step — immature compost can stunt seedlings (phytotoxicity, N immobilization).

**Why C:N matters:** microbes building biomass want ~1 C for energy per ~25–30 C per 1 N assimilated (cell C:N ≈ 8–10, plus respiration). Excess N → ammonia gas (loss + smell). Excess C → N-limited slow decay (leaves sit).

## 2. Ingredient tables (typical values — lab analyses vary ±30%)

### Carbon:Nitrogen
| Ingredient | C:N | Notes |
|---|---|---|
| Food scraps (mixed veg) | 15 | varies with fruit sugar content |
| Coffee grounds | 20 | free at cafés; slightly acidic, irrelevant in mix |
| Tea leaves | 20 | bags compost if paper |
| Grass clippings | 17 | mats easily; thin layers |
| Chicken manure | 8 | powerful N; compost hot before garden use |
| Horse/cow manure | 20–25 | ideal green if bedding included (pre-mixed C!) |
| Urine (diluted 1:4) | ~1 | the free N accelerator; see §7 |
| Autumn leaves | 55 | the seasonal bulk brown |
| Straw | 75 | structural + carbon |
| Cardboard (shredded) | 300 | wicks moisture, superb rescue material |
| Sawdust (untreated wood) | 400 | high potency — small amounts |
| Newspaper | 175 | shred; avoid glossy |
| Wood ash | 25 | also raises pH, K — sprinkle only |
| Eggshells | — | Ca, not N or C in meaningful terms; crush |

### Moisture content (typical)
| Ingredient | % water |
|---|---|
| Food scraps | 80–90 |
| Grass clippings | 80 |
| Coffee grounds (used) | 60 |
| Dry leaves | 20–30 |
| Straw | 10 |
| Cardboard/paper | 5–8 |
| Sawdust | 10 |

Blend moisture (weighted average) targets **50–60%**. The script computes it.

## 3. The arithmetic

```
blended_CN = Σ(wᵢ × CNᵢ) / Σwᵢ                (approx — treats CN as intensive)
blended_H2O = Σ(wᵢ × Mᵢ) / Σwᵢ
```
Correction prescriptions solve for the addition mass x that brings blended_CN to 30:
`x = W × (CN_mix − 30) / (30 − CN_add)` (only when CN_add < 30 < CN_mix or the reverse).

**Volume shortcut:** 1 m³ loose leaves ≈ 50–100 kg depending on shredding; 10 L bucket scraps ≈ 5 kg. Weigh once, convert forever.

## 4. System sizing

- Per person kitchen waste: ~0.15–0.3 kg/day → family of 4 ≈ 1–1.5 kg/day ≈ 400–500 kg/yr.
- **Hot pile minimum: 1 m³** (roughly a 3×3×3 ft bin, filled AT ONCE — the hardest backyard requirement; stockpile ingredients until you can).
- Bin sizing rule: 2–3 bins of 0.8–1 m³ each (one filling, one cooking, one curing) covers a family of four plus garden waste.
- **Cold (add-as-you-go) system:** any size ≥ 100 L; speed set by C:N luck and turning; 6–18 months. Best for low-effort households — the skill should say this is a legitimate choice, not a failure.
- Autumn leaf surplus: 4–5 m³ of leaves per mature tree. Leaf-mold (leaves alone, 12–24 mo, fungal) is the low-effort honest answer if you lack greens.

## 5. Temperature discipline (hot mode)

- Day 1–2: 20→45 °C. Day 3–5: 55–65 °C peak. When it drops ~10 °C from peak → **turn** (moves outside material in).
- 55 °C+ days: turn on days ~5, 10, 15; after 4–5 turns temperature won't re-rise → curing.
- > 70 °C: too hot (microbes die, N volatilizes) — turn to vent.
- Thermometer: 50 cm compost dial probe, ~$15 — the single best tool purchase in hot composting.
- Winter: piles steam but won't re-heat from cold start below ~10 °C ambient; insulate with straw bales; treat as cold pile until spring.

## 6. Diagnostics detail

| Symptom | Cause chain | Fix |
|---|---|---|
| Ammonia | C:N < 20; often wet + dense | add browns (script kg), turn |
| Rotten egg | O₂ gone: >65% moisture or compacted | turn + dry wicking browns; fork base for drainage |
| No heat, big pile | dry (<40%) or C:N > 40 | water + greens per calc |
| No heat, small pile | surface/volume ratio | merge bins, or accept cold mode |
| Maggots | fly access to food | bury 15 cm, cover browns blanket |
| Rat sign | nesting + food | 6 mm hardware cloth, no cooked food |
| Slimy grass mats | anaerobic pockets | layers < 10 cm, mix in straw |
| White powdery | actinomomycetes at work / dry | normal; moisten if dusty |
| Ants colonizing | too dry | water thoroughly, turn |

## 7. Accelerators, honestly

- Fresh manure / urine (diluted): real N, real speed.
- "Compost starter" powders: mostly harmless inoculum — your soil already has the microbes; speed gain ≈ 0 vs a shovelful of old compost.
- Sugar/molasses feeds: brief bloom, then stall; not worth it.
- Shredding/branch-mulching: the actual best accelerator — surface area beats every additive.

## 8. Using the finished product

- Sift 10–15 mm; coarse returns as inoculant.
- Garden rates: 2–5 cm incorporated, or 5 cm mulch (keep off stems).
- Not a fertilizer substitute: N ~1–2%, slow release; it's biology + structure.
- Phytotoxicity test (for impatient harvesters): put 20 cress seeds on damp compost; < 80% germination vs control = not cured, wait 2+ weeks.
