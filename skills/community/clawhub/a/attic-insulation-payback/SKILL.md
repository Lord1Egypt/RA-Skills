---
name: attic-insulation-payback
description: Use when considering attic insulation upgrade, before accepting an insulation contractor quote, or when comparing home energy upgrades — R-value stack math, HDD/CDD heating-energy model from fuel bills, real payback in years with degradation and air-sealing priority doctrine (seal before you stack), and quote forensics that catches overblown R-value claims and missing prep charges.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [insulation, attic, energy-efficiency, home-improvement, payback, hvac]
---

# Attic Insulation Payback

## Overview
Attic insulation is the single highest-return home energy upgrade for most houses — **when it's actually thin**. The physics has brutal diminishing returns: going from R-2 to R-13 cuts heat loss through the attic by ~85%; going from R-38 to R-60 cuts it by ~37% more of a small remainder. Contractors quoting "double your R, halve your bill" are exploiting the fact that homeowners don't know **which side of the curve their attic is on**.

This skill computes it honestly. You enter attic area, current R-value, target R-value, fuel type, local climate (heating degree-days), and system efficiency; the tool runs the degree-day heat-loss model against **your actual fuel bills** (calibration), then outputs annual savings, simple payback, and the verdict: **DO IT / OVERSOLD — SEAL FIRST / NOT WORTH IT**, with the air-sealing-first doctrine (moving air through fiberglass carries heat straight through the batt — stacking R over unsealed bypasses buys almost nothing).

## When to Use
- Contractor quote for attic top-up (blown cellulose/fiberglass) — sanity-check the savings claim
- Deciding between competing home energy upgrades (insulation vs windows vs heat pump)
- House feels cold upstairs / ice dams recur — is more R actually the fix?
- Comparing DIY blown-in vs contractor price
- Verifying a "R-60" quote will actually deliver R-60 (settlement, density, existing R debt)

**Don't use for:** wall insulation (different economics — cavity fill cost dominates), radiant barriers (not conductive insulation; separate physics), or mobile homes. Flat-roof/hot-climate cooling dominance: use the CDD branch but expect wider error bars.

## Quick Start
```bash
# Core payback: 1200 sqft attic, R-19 current -> R-60 target, gas heat, 5200 HDD65
python3 scripts/attic_payback.py --area 1200 --r-current 19 --r-target 60 \
    --fuel gas --hdd 5200 --price 3.20 --system-eff 0.80 \
    --quote 3400

# Calibration against reality: your gas bill says 90 therms/mo avg in winter
python3 scripts/attic_payback.py --area 1200 --r-current 19 --r-target 60 \
    --fuel gas --hdd 5200 --price 3.20 --system-eff 0.80 --quote 3400 \
    --calibrate-winter-therms 90

# Cheap-test mode: is the quoted R even real? (12 inches settled cellulose)
python3 scripts/attic_payback.py --r-check --inches 12 --material cellulose
```

## The Physics (what the script computes)
1. **Attic heat loss share**: `U = 1/R` (Btu/h·ft²·°F). `Q = U × area × ΔT`. Degree-day integration over the heating season gives annual Btu through the ceiling.
2. **Savings = Q(current R) − Q(target R)**, converted to fuel units (therms/gallons/kWh) at your price and system efficiency.
3. **Bill calibration**: predicted whole-house gas use from attic loss alone can't exceed the meter. If model output > ~40% of winter fuel, either the R estimate or the area is wrong — the script flags it and rescales.
4. **Diminishing-returns table**: prints savings from R-current→R-30/38/49/60 so you can see the flattening curve and pick the knee, not the brochure number.

## Doctrine: Seal Before You Stack
- **Air first, then insulation.** Fiberglass/cellulose do almost nothing to moving air. Attic bypasses — top-plate gaps, can lights, chase ways, bath fans venting into the attic — can waste more energy than a missing R-20. Seal (caulk/foam) before or WITH the top-up; most utility rebates require it.
- **Compressed insulation loses R.** A closed soffit-baffle-free install that blocks ventilation or a floor decked over leaves dead zones; and R-value labels assume full loft — settled 12-yr-old cellulose delivers ~80% of label.
- **Vented attic stays cold in winter.** The insulation goes on the attic floor, not the underside of the roof deck (unless it's a conditioned attic — different project entirely). Warm roofs = ice dams.
- **The last inch is the cheapest per R but the least valuable per dollar of energy.** The knee of the savings curve is usually R-38–49 in cold climates; R-60+ pays mainly in very cold zones or cheap material.

## Verdict Bands
| Result | Verdict |
|---|---|
| Payback ≤ 7 yr, attic R < 30 | **DO IT** — textbook case |
| Payback ≤ 7 yr but R ≥ 38 already | Check calibration; savings likely oversold |
| Payback 7–15 yr | **BORDERLINE** — do only with rebate or DIY cost |
| Payback > 15 yr | **NOT WORTH IT** — the curve has flattened; spend on air sealing instead |
| No air sealing in quote | **OVERSOLD — SEAL FIRST**; get sealing priced separately |

## Common Pitfalls
1. **Trusting the brochure R-value on old existing insulation** — measure depth × material, apply settlement (cellulose ~20% over 12+ yrs), subtract compressed/kitty-litter-squared zones.
2. **Skipping bill calibration.** A model that says the attic is 70% of your bill in a house with single-pane windows is lying; rescale or re-measure.
3. **Paying for R-60 when the knee is R-38.** The table output exists so you can quote the contractor the flat part of the curve.
4. **Unsealed can lights / chases under new insulation** — the money walks out through the bypasses you just buried.
5. **Venting bath fans into the attic** because the insulation crew "was up there anyway" — moisture destroys R and sheathing; demand exterior venting.
6. **DIY without a blower** (hand-spreading bags) — density is wrong, R claim void; machine-blown only.

## Verification Checklist
- [ ] Attic depth measured at ≥5 spots; material identified; settlement applied
- [ ] Area from house footprint (outer walls), not room interior
- [ ] HDD from the nearest weather station (climate zone), HDD65 base
- [ ] Fuel price from a real recent bill (per-therm delivered, all charges)
- [ ] Savings checked against winter bills (model attic share ≤ ~40%)
- [ ] Air sealing included in quote or priced separately BEFORE the top-up
- [ ] Diminishing-returns table read; knee chosen over brochure R
- [ ] Payback computed at honest quote price including prep/deck removal

## Example Session
```
$ python3 scripts/attic_payback.py --area 1200 --r-current 19 --r-target 60 \
    --fuel gas --hdd 5200 --price 3.20 --system-eff 0.80 --quote 3400
ATTIC INSULATION PAYBACK — 1200 ft², R-19 -> R-60, gas @ $3.20/therm
  season heat loss now:   98.5 therms (R-19)
  season heat loss after: 31.2 therms (R-60)
  annual savings:         ~67.3 therms = $215/yr
  payback on $3,400 quote: 15.8 yr   [NOT WORTH IT at this price]
  diminishing returns (savings vs staying at R-19):
    R-30  $116/yr   (~$912 pro-rated)
    R-38  $158/yr   (~$1,576 pro-rated)
    R-49  $193/yr   (~$2,488 pro-rated)
    R-60  $215/yr   (~$3,400 pro-rated)
  -> the knee is R-38: R-49/60 add <$60/yr over R-38. Ask for the R-38 price.
VERDICT: NOT WORTH IT at this price — the savings curve has flattened;
  with a utility rebate or DIY blow machine (~$900) it becomes a win;
  air sealing at $200-600 returns faster than any depth here.
```
