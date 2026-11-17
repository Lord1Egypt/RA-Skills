---
name: bike-maintenance-cadence
description: "Use when you ride a bike and want to know WHAT to maintain WHEN: converts ridden km/weeks/conditions into a dated service schedule per component (chain wear, cassette, brake pads, cables, tires, bearings, suspension, drivetrain deep-clean), prices wear parts by component-lifetimes math, and diagnoses drivetrain noises/brake rub/shifting ghosts. Solves the 'chain skipped, now the cassette is dead too' cascade problem."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [bicycle, maintenance, chain-wear, drivetrain, brakes, service-schedule, cycling]
---

# Bike Maintenance Cadence

## Overview

Bikes fail by cascade. A $20 chain ridden 500 km past its wear limit grinds the cassette ($40–90) and chainrings ($30–120) into matching its stretch — then the "sudden" replacement bill is $150+ instead of $20, three times a year. The entire economics of bike ownership is detecting wear at the chain-checker stage, and almost nobody owns a chain checker or knows their component lifetimes in km.

This skill converts **how you actually ride** (weekly km, weather, storage, terrain) into a **dated, per-component service calendar**: when to measure chain wear (0.5% / 0.75% / 1.0% thresholds and what each means), when pads, cables, tires, bearings, and (if fitted) suspension are due. It prices the wear-parts budget per year from component lifetime tables, and routes the common failure noises to causes with a 10-minute diagnostic sequence before parts-shopping.

The multiplier effect: wet/urban/winter riding roughly doubles drivetrain wear; dry garage storage halves cable corrosion. The schedule reflects YOUR conditions, not the manual's generic "every 500 km."

## When to Use

- Setting up maintenance for a new (or new-to-you) bike — first calendar + tool list
- "It's been making a noise / skipping / rubbing" — diagnostic router first, then maintenance
- Budgeting: what does this bike cost per year in wear parts at my km?
- Returning rider dusting off a bike after years — the revival safety checklist
- Deciding repair-vs-replace on a worn drivetrain (partial vs full replacement rules)
- Pre-season / pre-big-ride audit (the week-before checklist)

**Don't use for:** e-bike firmware/motor/battery service (manufacturer territory — though the mechanical parts here still apply), suspension internals beyond seal/fork service intervals (specialist tools), or carbon frame crack assessment (professional inspection — do not ride a suspected cracked frame).

## Component Lifetimes (typical, adjustable by conditions)

| Component | Life (good conditions) | Wet/winter/urban | Check method |
|---|---|---|---|
| Chain | 3,000–5,000 km | 1,500–2,500 km | wear gauge 0.75% |
| Cassette | 2–3 chains | 1–2 chains | hook-shaped teeth, skip under load |
| Chainrings | 3–4 chains | 2–3 chains | shark-fin teeth |
| Brake pads (rim) | 2,000–4,000 km | 1,000 km | visual wear line |
| Brake pads (disc, resin) | 2,000–5,000 km | 1,000–2,000 km | pad material ≥ 0.5 mm above backing |
| Disc rotors | 10,000+ km | — | thickness gauge; min stamped (usually 1.5–1.8 mm) |
| Cables + housing | 1–2 yr | 6–12 mo | fraying, sluggish return |
| Tires | 3,000–6,000 km rear / 2× front | less | tread squaring, cuts, casing threads |
| Tubes | until punctured | — | patch vs replace economics |
| Bottom bracket | 5,000–10,000 km | less if pressure-washed | creak under load, side-play |
| Wheel bearings | 5,000–10,000 km | — | spin + grab test, rock wheel |
| Headset bearings | 1–2 yr | less if rain | index creak, notchy steering |
| Suspension seals/fork oil | 50 hrs service / 100–200 hr full | — | manufacturer hours meter |
| Tubeless sealant | 2–4 mo | — | shake check / top-up |

**The one tool that pays for itself in a week:** a chain wear gauge ($10). Everything else follows from catching the chain at 0.75%.

## The Cascade Rules (money-saving doctrine)

1. Replace chain at **0.75%** wear → cassette usually survives (2–3 chains per cassette).
2. Chain hits **1.0%+** (≈ 0.5% too late): budget chain + cassette together. Riding further eats chainrings.
3. New chain on worn cassette = skipping under load in the 3–4 most-used cogs within a week. That skip IS the cassette's verdict — don't blame the chain.
4. Mixed-generation parts (11s chain on 10s drivetrain etc.): don't. Compatibility is speed-generation specific.
5. When replacement total > ~40% of a decent used bike's value, consider the whole-drivetrain-new or bike-replacement math honestly.

## Symptom Router (diagnose before buying)

1. **Skipping under load** → chain/cassette wear (measure first), or stiff link (flex-check), or derailleur B-gap/h-limit off.
2. **Chain suck / front derailleur jamming** → worn chainrings, chain too wide/narrow mismatch, or grimy chain.
3. **Brake rub (disc)** → caliper centering (loosen bolts, squeeze lever, retighten), rotor true (slight trueness tolerable >0.3 mm wobble fix), or bent rotor from transport.
4. **Spongy disc lever** → air in line (bleed) or pad glaze (sand lightly) — NOT "more cable tension."
5. **Grinding/crunch on pedaling** → BB bearings (side-play test), or pedal bearings, or rear DER pulley seizures. Isolate: does it happen in every gear standing vs seated?
6. **Click every crank revolution** → chainring bolts, pedal threads, BB, or shoe cleat. Tighten ring bolts first — free fix, most common.
7. **Wheel thump/click per revolution** → spoke nipple looseness, tire bead seat, or hub bearings. Spin test locates the sector.
8. **Indexing ghost-shifts in 2 cogs only** → cassette wobble/loose lockring or bent DER hanger — the hanger is the sacrificial part; alignment tool or replace ($15 vs frame).

## Common Pitfalls

1. **Pressure-washing** — forces water+grit into bearings, BB, and suspension seals; kills more parts than riding does. Bucket + brush + degreaser on the drivetrain only.
2. **Lube on a dirty chain** — makes grinding paste. Wipe → degrease when black → dry → lube → wipe. 90% of chain life is the wipe.
3. **Over-tightening** — especially stem/steerer carbon (torque wrench + carbon paste at 5 Nm typical) and BB cups. Split the difference by feel only if no torque data.
4. **New cables on worn housing** (or the reverse) — replace as pairs, or the sluggishness survives and you blame the wrong part.
5. **Ignoring the front brake** because "the back one stops me." Front = 70% of stopping power; pads wear there first.
6. **Resin pads on long descents** glaze/fade — for sustained mountains, sintered pads. For dry flat commuting, resin is quieter and grabs sooner.
7. **Tubeless "set and forget"** — sealant dries to a latex pancake in 2–4 months; top up or the system silently becomes a worse clincher.
8. **Storage wet in a shed** — cables and chain rust between rides; wipe chain, and a $5 cover beats a $60 cable set yearly.

## Verification Checklist

- [ ] Weekly/monthly km stated or estimated; conditions multiplier applied
- [ ] Dated next-service entries per component, not vague intervals
- [ ] Chain-wear measurement instruction included (0.5/0.75/1.0 thresholds)
- [ ] Cascade check: if chain > 1.0%, cassette priced into the plan
- [ ] Annual wear-parts budget computed from lifetime table × your km
- [ ] Symptom router run BEFORE any parts purchase advice
- [ ] Safety-critical items flagged (brakes, tires, headset, wheel integrity, carbon torque)

## One-Shot Recipe

```bash
# 120 km/week, urban commuting, rain, stored in a shed
python3 scripts/bike_cadence.py schedule --km-week 120 --conditions wet --storage shed \
  --last-service 2026-08-01
# → dated calendar: chain check NOW (wet multiplier), pads in 6 wk, cables 4 mo...

# what does my riding cost in wear parts?
python3 scripts/bike_cadence.py budget --km-week 120 --conditions wet --disc

# the classic: skipping under load, what do I check in what order?
python3 scripts/bike_cadence.py diagnose --symptom skip-under-load
```
