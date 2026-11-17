# Freshwater Aquarium — Cycle, Stocking, Water-Change Reference

## 1. The nitrogen cycle in detail

```
NH₃/NH₄⁺ (ammonia) --Nitrosomonas--> NO₂⁻ (nitrite) --Nitrospira/Nitrobacter--> NO₃⁻ (nitrate)
```

- **Ammonia toxicity is pH-dependent:** below pH 7 nearly all NH₄⁺ (less toxic); above pH 8
  the NH₃ fraction climbs fast. At pH 8.5 and 25°C, 1.0 ppm total ammonia ≈ 0.15 ppm NH₃
  — already stressful. The script uses a temperature+pH NH₃ fraction table.
- **Nitrite poisoning** ("brown blood"): NO₂⁻ binds hemoglobin. Cheap antidote: chloride —
  add 1 tsp non-iodized salt per 40 L (10 gal) to outcompete NO₂⁻ uptake (does not help
  ammonia; works only for nitrite, harmful to scaleless fish at higher doses).
- **Nitrate** is least toxic; stress threshold ~40 ppm, breeding/lazy best <20 ppm.

## Cycle kinetics (why 3–6 weeks)

Bacterial doubling: Nitrosomonas ~8 h, Nitrospira ~20–24 h under ideal conditions
(25–28°C, pH 7–8.5, O₂ saturated). Colonies live in the FILTER MEDIA and substrate
surface, not the water column — hence: never replace all media at once, never rinse in
chlorinated water, and a cycled filter moves the cycle with it (instant new tank).

Speed levers:
| Lever | Effect |
|---|---|
| Bottled bacteria (FritzZyme 900, Tetra SafeStart+) | 1–2 weeks vs 4–6 |
| Seeded media from an established tank | days (best lever) |
| Temp 27–28°C (fishless only) | ~20-30% faster |
| pH ≥ 7.2 | nitrifiers slower in acid water |
| Strong aeration | both genera are aerobic |
| Dark tank (no UV) | bacteria colonize faster |

Pure ammonia checklist: surfactant-free (shake → no persistent foam), no dye/perfume.
Alternative ammonia sources: raw shrimp in a mesh bag (messy), fish food (uncontrolled).

## Cycle targets (fishless)

- Dose to 2–3 ppm NH₃ equivalent. If you'll keep heavy fish (goldfish, Oscars) cycle to 4.
- Progression: NH₃ detectable days 1–7 → NO₂ spike days 7–20 (can exceed 5 ppm test max —
  dilute sample 1:1 with RO to read) → NO₂ → 0 and NO₃ rising days 14–30.
- **Clearance gate:** dose 2 ppm ammonia; 24 h later NH₃ = 0 AND NO₂ = 0 → fully cycled.
  Verify twice before fish.
- After stocking: bacteria capacity equals the ammonia you cycled at. Stocking beyond it
  produces a mini-spike — hence waves.

## Fish-in-cycle (emergency, fish already added)

1. Test daily (NH₃, NO₂). Any detectable → 25–50% water change SAME DAY, temperature-matched,
   dechlorinated.
2. Dose Prime/Amquel Plus (binds ammonia/nitrite 24–48 h at up to 5× dose — still test).
3. Feed sparse: every other day, what's eaten in 30 s.
4. No filter rinse, no gravel deep-clean (surface colonies!), no "bacteria starter" swaps.
5. Duration: 4–8 weeks until tests read 0/0 for 7 consecutive days.

## Stocking bioload model

The script's model (freshwater community; conservative):
```
capacity_cm/L  ≈ 1.0 (slim fish) with shape-class biomass factors:
  slim  (tetra, rasbora, danio):      ×1.0
  normal (barb, gourami small):       ×1.3
  deep  (goldfish, discus, angel):    ×2.0
  very deep / heavy (oscars, plecos): ×3.0
adult_bioload = Σ count × adult_cm × factor
capacity_L    = volume_liters × 1.0 cm/L × (filtration class: 
                 hang-on-back 0.9, canister 1.1, sponge/undergravel 1.0)
verdict: load/capacity ≤ 0.70 = OK, 0.7–0.85 = max, >0.85 = overstocked
```
Goldfish special case: 75 L for the first, +40 L each additional (fancy), double for
commons (they reach 30 cm and are waste machines).

Classic compatibility landmines:
- Betta + fancy guppy / neon (fin nipping either direction) — betta + ember tetra/cory OK
- Tiger barbs + anything with flowing fins
- African cichlids (mbuna) + community fish (aggression + water chemistry)
- Oscar/flowerhorn + anything that fits in its mouth (conspecifics included)
- Multiple male gouramis (except honey/dwarf heavily planted)
- Shrimp + any fish large enough to eat them (even neons pick off shrimplets)

Water-parameter classes the screen checks: temp band, pH band, hardness (GH/KH) class
(soft-water Amazon vs hard-water rift lake), current preference, territory/level spread.

## Water-change math

```
nitrate_after_change = tap_NO₃ + (current_NO₃ − tap_NO₃) × (1 − frac)
solve frac for target:  frac = 1 − (target − tap)/(current − tap)
steady-state with production P ppm/week and weekly fraction f:
  NO₃_eq = tap + P / f        → f = P / (target − tap)
```
- If tap ≥ target: water changes alone cannot reach target. Options: pothos/nitrate-hungry
  plants, NO₃ resin, RO/DI blend (mix to hit tap-equivalent GH/KH), or accept higher target.
- 2× smaller changes are not equivalent to 1× big change for spiky parameters (TDS creep).

## Quarantine protocol (skip at your own risk)

- 4–6 weeks hospital tank, sponge filter, bare bottom, daily observation
- Week 1: watch (no meds) — most pathogens declare
- Feed lightly; treat what actually appears (general cure / bacterial / parasitic lanes)
- THEN add to display. One skipped quarantine can wipe a 3-year-old tank.

## Test-kit notes

- Liquid drop kits (API Freshwater Master) >> strips for accuracy; strips expire fast.
- Nitrate test: shake bottle #2 VIOLENTLY 30 s + test tube 1 min (most common false low).
- Ammonia test reads total (NH₃+NH₄⁺); use an NH₃-fraction table for true toxicity.
- Test before water change, not after; same time of day.
