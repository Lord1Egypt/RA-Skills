---
name: fountain-pen-ink-alchemist
description: Use when mixing, diluting, or crafting fountain pen inks — dilution math (add-water % → new volume, concentration shift, lighter shade), dry-time estimates adjusted for glycerin and humidity, batch logging to a reusable ink_log.json with ratios and notes, recipe comparison tables (dry time, flow, wash resistance, nib safety), and drops↔ml plus converter-fill/page conversions by nib width — including why DIY water+dye ink molds without a biocide, why pigment/shimmer inks clog EF/F nibs while dyes are safe, and the absolute rule that acrylic and India inks never go in a fountain pen.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [fountain-pens, ink, mixing, dilution, calligraphy, stationery, diy, dry-time]
---

# Fountain Pen Ink Alchemist

A 60 ml bottle of ink lasts most people two years. So when a pen skips,
an ink feathers, or a favorite shade is discontinued, the fix isn't
buying more ink — it's adjusting what you have: a measured splash of
distilled water, a drop of glycerin, a logged ratio you can reproduce
(or never repeat). The failure modes are all un-measured: too much
water turns the ink watery-pale, too much glycerin smears for an hour,
and a homemade dye mix grows mold in the feed within a fortnight.
This skill does the arithmetic and keeps the rules (pigment ≠ dye,
acrylic = pen death) in front of you at the moment of mixing.

## When to Use

- Ink too dry / pen skips → compute the right dilution instead of
  pouring blind (5-25% water is the useful band; 30%+ is ruined)
- Estimating how a dilution or glycerin addition changes dry time on
  YOUR paper at YOUR humidity
- Logging every custom batch (components, ratio, verdict) so a happy
  accident is reproducible — `ink_log.json` is the lab notebook
- Deciding between ink classes for a pen: dye vs iron-gall vs
  pigment vs shimmer — nib width drives the answer
- Converting recipe drops to ml and ml to fills/pages for a given nib
- Tempted by acrylic/India/calligraphy inks in a fountain pen — stop,
  read the safety section, use a dip pen instead

**Not for:** rehydrating dried-out bottles of unknown provenance,
vintage ink restoration chemistry, or anything involving solvents —
those need dedicated references.

## The Method

```bash
# The core move: dilute 60 ml by 15% and see everything that changes
python3 scripts/ink_alchemy.py mix --target-ml 60 --add-water-pct 15

# With the dry-time modifiers: 3% glycerin, humid summer office
python3 scripts/ink_alchemy.py mix --target-ml 60 --add-water-pct 10 \
    --glycerin-pct 3 --rh 70

# Log the batch you just made (ratios + verdict notes)
python3 scripts/ink_alchemy.py batch add --name "misty ku-jaku" \
    --components "ku-jaku 50ml, distilled water 10ml" --ratio "5:1" \
    --notes "wet flow, dry EF finally happy; shade one step lighter"
python3 scripts/ink_alchemy.py batch list

# Compare two ink classes before committing a pen to one
python3 scripts/ink_alchemy.py compare shimmer pigment
python3 scripts/ink_alchemy.py compare --list

# Recipe math: drops in the recipe, ml in your pipette
python3 scripts/ink_alchemy.py convert --drops 20 --nib f
python3 scripts/ink_alchemy.py convert --ml 30 --drop-ml 0.05
python3 scripts/ink_alchemy.py convert --nib-table
```

## Dilution Quick Reference

| Added water | Color | Flow | Dry time | Verdict |
|---|---|---|---|---|
| 5% | ~same | slightly wetter | +4% | subtle flow fix |
| 10% | 1 shade lighter | wetter | +9% | the sweet spot |
| 15% | noticeably lighter | wet | +14% | dry pens rejoice |
| 25% | pale | very wet | +22% | feathering risk on cheap paper |
| 30%+ | washed out | sloppy | +27%+ | start over; log the failure |

Dry time ≈ base × (volume ratio)^0.85 × 1.18^(glycerin %) × 2^((RH−50)/40).
Doubling from 50% to 90% humidity roughly doubles dry time — a mix
that behaved in winter smears all August.

## Ink Class Rules (the part that saves pens)

| Class | Particle? | Nibs | Waterproof | Upkeep |
|---|---|---|---|---|
| Dye (standard FP ink) | no — dissolved | all, incl. EF | no | flush 4-6 wk |
| Iron gall | no | steel short-term, gold safer | after oxidation | use weekly, flush monthly |
| Pigment | YES — suspended | F/M+ with weekly flush | yes | never let dry in pen |
| Shimmer | YES — mica flakes | BROAD/stub only | no | swirl, never shake |
| Acrylic / India | binder + shellac | NONE — dip pen only | yes | destroys feeds |

The mechanism matters: dye molecules stay dissolved and flow through a
0.2 mm EF slit; pigment and mica are solids that settle and accrete in
the feed channel and under the nib tines. A clogged feed means
disassembly or a parts sink — an hour of surgery to save 15 minutes of
flushing.

## Common Pitfalls

1. **Tap water instead of distilled.** Minerals crust the nib tipping
   and feed, and tap microbes jump-start mold. Distilled only.
2. **Shaking a shimmer bottle.** Shaking whips in air bubbles that
   cause hard starts; swirl gently, bottle vertical.
3. **Pigment ink left in an unused pen.** Water evaporates through the
   cap in weeks; the solids stay and cement the feed. Flush any pen
   that sits for more than a week.
4. **Glycerin as a universal flow agent.** It's a humectant — past
   ~5% it keeps the line wet enough to smear on coated paper for an
   hour. 1-3% is the working range.
5. **Homemade dye ink with no biocide.** Water + dye + no preservative
   is a microbial culture; mold hyphae physically clog the feed. If it
   smells sweet or earthy, discard the batch and flush the pen.
6. **"Just a little" acrylic or India ink.** There is no little.
   Shellac and acrylic binder dry insoluble inside the feed; the pen
   is often not recoverable. Dip pens exist for these inks.
7. **Mixing in the pen instead of a vial.** You can't measure, can't
   log, and can't undo. Always mix in a clean vial, then fill.

## Verification Checklist

- [ ] Distilled water used (not tap, not filtered)
- [ ] Dilution computed with `mix` — volume, ml to add, new total recorded
- [ ] Mix made in a clean vial, not inside the pen
- [ ] Swab/scratch test on the actual target paper, both wet and dry
- [ ] Batch logged: components, ratio, date, verdict notes
- [ ] Pen flushed before filling and scheduled for flush (4-6 wk dye, weekly pigment/shimmer)
- [ ] No acrylic/India/solvent ink ever contacted the fountain pen
- [ ] Shimmer only in broad/stub; swirl not shake

## Maintenance Cadence (flush before it's a problem)

| Ink in pen | Flush every | Why |
|---|---|---|
| Dye, daily writer | 4-6 weeks | dye films slowly; also refreshes feed |
| Dye, sitting capped | 2-3 weeks | water evaporates through the cap |
| Pigment | 1 week, no exceptions | solids cement the feed as water leaves |
| Shimmer | 1 week + swirl before each fill | mica settles flat in the converter |
| Iron gall | after each use | acid + steel nib = corrosion while stored |
| Any mix >25% water | 2 weeks | halved biocide load, mold risk |

A pen that writes fine is not evidence the feed is clean — it's
evidence it's clean *today*. Flushing is 60 seconds under the tap
followed by a converter of clear water; disassembly is an hour with
a parts sink. The cadence table is the whole trick.

## References

- `references/ink-craft.md` — the deep version: water-ink ratio effects,
  drying physics (glycerin, surfactants, humidity), why inks mold and
  preservative reasoning, dye vs pigment mechanics, pH, classic
  recipes, the batch log schema, and the full safety rules.
