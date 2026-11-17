# Ink Craft — The Deep Reference

Everything behind the CLI's numbers: dilution effects, drying
physics, preservatives, particle vs dye mechanics, pH, classic
recipes, and the log schema. Written for paper, not a lab — ranges
are practical, not analytical-grade.

## 1. Water–Ink Ratio: What Dilution Actually Does

Commercial dye ink is roughly 85-90% water already; the rest is dye,
glycerin/humectants, surfactant, and biocide. Adding distilled water
changes four things at once, never just one:

| Added water | Dye conc. | Flow | Dry time | Side effects |
|---|---|---|---|---|
| 5% | 95% | slightly wetter | +4% | barely visible change |
| 10% | 91% | wetter | +9% | one shade lighter; wetter nib feel |
| 15% | 87% | wet | +14% | shading appears on good paper |
| 20% | 83% | very wet | +18% | spread increases, line fattens |
| 25% | 80% | very wet | +22% | feathering on absorbent paper |
| 30%+ | ≤77% | sloppy | +27%+ | pale, bleeds through, start over |

Concentration after adding `p`% water is `100/(1+p/100)` — the same
math the `mix` command runs. Two asymmetries surprise people:

- **Color drops faster than you expect past 20%** because dye uptake
  on paper saturates; halve the dye and you often get *less* than
  half the perceived color.
- **Dry time rises sub-linearly** (exponent ~0.85 on volume ratio):
  more water means lower viscosity and faster capillary spread into
  the paper, which partially offsets the extra water to evaporate.

Why dilute at all? Dry pens (fine nibs, tight feeds, some German
steel), hard-starters, inks that feather-prone papers reject at full
strength, and shading enhancement. The working band is 5-25%; above
that you're making tinted water.

**Distilled only.** Tap water carries dissolved minerals (scale on
the nib slit, feed channel crust) and — worse — microbes that
jump-start mold. Filtered and bottled waters still carry minerals;
"purified by distillation" or deionized is the target.

## 2. Drying-Time Physics

An ink dries when (a) water leaves and (b) the colorant stays. Three
levers dominate for fountain pen use:

- **Humidity.** Evaporation rate is roughly proportional to
  (100 − RH). Going from 50% to 90% RH doubles-to-triples dry time;
  the same ink that dries in 15 s in winter smears for a minute in an
  August office. Model: multiply by `2^((RH−50)/40)`.
- **Glycerin (and other humectants).** Glycerin is hygroscopic — it
  *holds* water and keeps holding it. Each +1% of final volume
  multiplies dry time by roughly ×1.18. At 5% you have a smear
  problem on coated papers; 1-3% is the working range for flow and
  nib-feel improvement. It also suppresses hard starts in dry
  climates — the trade is real and personal.
- **Paper.** Absorbent copy paper pulls water mechanically (fast dry,
  feathering risk); coated/HP paper holds it at the surface (slow
  dry, crisp lines). The single most effective smear fix is changing
  paper, not ink.

Surfactants (a drop of dish soap in old folk recipes) cut surface
tension: flow improves, spread increases, dry time drops slightly as
the ink wicks into the paper. Overdose and you get feathering and
bleedthrough — surfactant dosing is measured in *fractions of a drop*
per 10 ml, which is why the CLI's convert command exists.

## 3. Preservatives: Why Fountain Pen Ink Is a Food Product

Water + dye + sugar-like organics at neutral pH is a microbial
culture medium. Fountain pen ink is warm, wet, aerated, and refilled
from a bottle — everything a mold spore wants. Commercial inks add a
biocide (historically phenol derivatives; today often isothiazolinone
family at ~0.1-0.3%) precisely because without it, inks cloud, smell
sweet/earthy, and grow hyphae in the feed within weeks.

Practical reasoning for the home mixer:

- **If you mix two commercial inks, you're fine.** Biocide comes
  along with both halves (unless you dilute heavily — past ~30% added
  water you've halved the preservative load too).
- **If you start from dye powder + water, you have nothing.** Either
  accept a 1-3 week shelf life in the fridge, use a sacrificial pen,
  and flush religiously, or add a proper biocide. Food-store
  "potassium sorbate" is weak against mold; hobbyist ink makers use
  dedicated preservatives at ~0.2%. Never improvise with bleach,
  alcohol past ~10%, or anything caustic — it attacks the feed.
- **Discard on smell or cloudiness.** A sweet/earthy/musty note or
  haze means the batch is lost; mold hyphae physically clog feeds,
  and flushing a moldy pen is a full teardown. The ink is cheaper
  than the pen. Always.
- **Don't top off old bottles with new ink** — you're seeding the
  fresh batch with whatever's living in the old one.

## 4. Shimmer & Pigment vs Dye: The Particle Rule

The single most useful classification: **is the colorant dissolved or
suspended?**

- **Dye** (standard fountain pen ink) — molecules in solution. No
  settling, no particles, flows through an EF slit and a tight feed
  indefinitely. Not waterproof (re-wets), fades faster in UV. Safe in
  everything.
- **Pigment** (nano-particle waterproof inks) — solids suspended by
  dispersants. Waterproof and lightfast, but particles settle and
  accrete wherever flow is slow. Fine in F/M with weekly flushing;
  risky in EF; fatal if left to dry in any pen.
- **Shimmer** — mica/flake particles added to a dye base. The flakes
  are huge relative to a nib slit: broad and stub nibs only, swirl
  (never shake — air bubbles cause hard starts), store nib-up, flush
  weekly.
- **Sheen-heavy dye inks** — still dye, but high-concentration
  surfactant systems that deposit dye crystals on the surface. They
  can crud up like pigments if left to dry; treat with medium respect.

Mechanism of the clog: the feed is a fine capillary channel with the
nib slit ~0.05-0.2 mm. Particles lodge, accumulate more particles,
water evaporates from the mass, and you get a cemented feed. Soaking
sometimes works; often it's disassembly or a dead pen.

## 5. pH Basics

- Modern dye inks: near neutral (pH 6-9) — safe for all pens and
  papers.
- Iron gall: acidic (pH 2-4) by design — the acid is part of the
  oxidation chemistry that makes it permanent. Fine on parchment-class
  papers; corrosive to steel nibs left inked for weeks; gold nibs
  shrug. Flush after each use.
- Highly alkaline inks (some vintage recipes): attack pH-sensitive
  dyes and some feeds. Not worth recreating.
- Don't mix extremes: an acidic and an alkaline ink can react,
  precipitate solids (instant particulate where you had none), or
  shift dye color. When mixing, stay within one pH family — which in
  practice means modern neutral dye inks with each other.

## 6. Classic Recipes (starting points, adjust to taste)

- **"One shade lighter":** 10% distilled water into any dye ink. The
  single most-used mix in the hobby.
- **Dry-pen rescue:** 15-20% water + 1-2% glycerin. Wet flow, slower
  dry — test on target paper.
- **Winter hard-start fix:** 2% glycerin, no water. Keeps the feed
  from drying between uses in heated rooms.
- **Shading booster:** 15% water into a saturated dye ink on coated
  paper. Pooling does the rest.
- **"Custom" from two inks:** mix in a vial at 1:1 or 2:1, log it
  (`batch add`), swab-test next day — dyes can shift hue after a few
  hours together.
- **Never recipes:** anything with acrylic binder, India/shellac ink,
  calligraphy sumi in solvent, alcohol inks, fountain pens used as
  applicators for glue or paint. See §8.

## 7. Batch Log Schema

The CLI writes `ink_log.json` — a JSON array; each entry:

```json
{
  "id": 3,
  "date": "2026-10-18",
  "name": "misty ku-jaku",
  "components": "ku-jaku 50ml, distilled water 10ml",
  "ratio": "5:1",
  "notes": "wet flow, dry EF finally happy; shade one step lighter"
}
```

Field discipline: `components` is full inventory with volumes (so the
batch is reproducible), `ratio` is the shorthand you'll actually
remember, `notes` carries the verdict *after* a week of writing —
update it. An unlogged happy accident is a loss; the whole point of
the log is that your 200-bottle hobby accumulates instead of resets.

## 8. Safety Rules (pen safety, and some skin)

1. **Acrylic inks (art/calligraphy acrylics): never in a fountain
   pen.** The acrylic binder dries to a water-insoluble film inside
   the feed and nib channel. Cured acrylic does not redissolve in
   water, pen flush, or ammonia solution at safe strengths. Pens are
   routinely killed this way; the feed is usually not recoverable.
2. **India ink: never in a fountain pen.** Shellac binder, same
   outcome, faster. This is the classic gift-pen death.
3. **Sumi and alcohol inks: same rule, different solvents.**
4. These inks are *dip pen* and brush media. A $2 dip nib exists so
   your $200 fountain pen doesn't have to.
5. Skin: fountain pen inks are water-based and low-toxicity; wash
   with soap and water. Staining fades in a day or two. Keep inks
   away from eyes; keep away from pets and children like any dye.
6. Surfaces: dye ink re-wets — a spill mops up. Pigment and iron
   gall may not. Protect the desk before you pour.
7. Don't drink any of it, including "safe" dye inks; and never use
   ink containers for food afterward.

## 9. Decision Table

| Situation | First move | Command |
|---|---|---|
| Pen skips, ink feels dry | 10% water dilution, test | `mix --target-ml 60 --add-water-pct 10` |
| Ink feathers on cheap paper | change paper first; dilute won't help | — |
| Smears in summer | check RH, reduce glycerin, change paper | `mix --rh 80 ...` |
| Want lighter shade | 10-15% water | `mix` |
| Want waterproof | move to pigment class, F/M+ | `compare pigment dye` |
| New shimmer ink arrives | broad/stub pen only | `compare shimmer dye` |
| Made a batch worth keeping | log it now | `batch add ...` |
| Recipe in drops, syringe in ml | convert | `convert --drops 20` |
