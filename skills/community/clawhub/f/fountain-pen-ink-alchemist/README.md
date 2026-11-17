# Fountain Pen Ink Alchemist

Dilution math, dry-time estimates, batch logging, recipe comparison,
and unit conversions for mixing fountain pen inks — with the pen-
safety rules that keep acrylic/India ink out of your feeds.

## The Real Problem

Fountain pen ink is 85-90% water, and every common problem — a dry
pen, an ink that feathers, a shade that's too dark — is fixed by
changing that ratio a few percent. The hobby's failure mode is doing
it by eye: pour a splash, overshoot, and now a $15 bottle is tinted
water. The second failure mode is treating all ink as equal: a
shimmer ink in a fine nib or a "little" India ink in a converter ends
in a cemented feed, and feeds often don't come back.

Nobody needs another app for this. You need arithmetic you trust,
the dry-time physics (glycerin and humidity move it more than the
dilution does), a lab notebook so a happy accident is reproducible,
and a short list of never-do rules.

## Who Needs It

- Fountain pen users who dilute, blend, or tweak inks — and want the
  batch logged rather than remembered
- Anyone whose pen skips and suspects the ink before the nib
- Shimmer/pigment ink owners deciding which pen is safe to fill
- Journal/planner users fighting summer smear on coated paper

## What It Does

- **mix** — `--target-ml 60 --add-water-pct 15` → water to add, new
  volume, concentration shift, dry-time estimate with `--glycerin-pct`
  and `--rh` modifiers; warns past the 30% cliff
- **batch** — `add` / `list` entries in `ink_log.json`: date,
  components, ratios, notes; survives across sessions
- **compare** — two recipes side by side: dry time, flow, wash
  resistance, nib safety, upkeep
- **convert** — drops ↔ ml with drop-size override, plus fills and
  page estimates per nib width (EF through stub)
- **references/ink-craft.md** — drying physics, preservative
  reasoning (why fountains mold), dye vs pigment mechanics, pH,
  classic recipes, log schema, full safety rules

## Quick Start

```bash
python3 scripts/ink_alchemy.py mix --target-ml 60 --add-water-pct 15
python3 scripts/ink_alchemy.py mix --target-ml 50 --add-water-pct 10 --glycerin-pct 2 --rh 65
python3 scripts/ink_alchemy.py batch add --name "misty ku-jaku" \
    --components "ku-jaku 50ml, distilled water 10ml" --ratio "5:1" \
    --notes "wet flow, dry EF finally happy"
python3 scripts/ink_alchemy.py batch list
python3 scripts/ink_alchemy.py compare shimmer pigment
python3 scripts/ink_alchemy.py convert --drops 20 --nib f
```

Stdlib only, offline, exit codes 0/2. Estimates are planning
heuristics — swab-test on the paper you'll actually use.

## License

MIT © Denis Voronin
