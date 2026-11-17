# Cleaning Mix Guardian

**Check BEFORE you mix.** Bleach + ammonia → chloramine gas. Bleach +
acid → chlorine gas. Two drain cleaners → boiling caustic. Thousands of
ER visits a year from mixtures people didn't know were reactions. This
is the pre-mix checker: product names in, hazard verdict, symptoms,
first aid, and the safe sequence out.

## The problem

The most dangerous chemicals in most homes sit under the sink. The
injury pattern is always the same: two effective products, one dirty
bathroom, and no idea that "toilet cleaner" means 9 % hydrochloric acid
and "bleach" means hypochlorite — a combination chemists handle in
fume hoods. Product labels warn about THEIR product, not combinations;
nobody reads the back of two bottles simultaneously and does redox
chemistry in their head.

## What it does

- `check` — two products in → CRITICAL/HIGH/MODERATE verdict with the
  gas name, symptoms, first aid, and the poison-control card.
- `products` — table of common products → their reactive class (read
  labels; formulations vary).
- `sequence` — planning a multi-product deep clean: flags every dangerous
  pair in the set and prints the rinse/wait protocol between them.
- `incident` — it already happened: evacuation steps, probable gas,
  escalation triggers, pet guidance.

## Quick start

```bash
python3 scripts/mix_guard.py check --a bleach --b "glass cleaner"
python3 scripts/mix_guard.py sequence --items "toilet cleaner,bleach,limescale remover"
python3 scripts/mix_guard.py incident --a bleach --b vinegar
python3 scripts/mix_guard.py products
```

Stdlib-only Python 3. No data leaves the machine.

## Who needs this

Every household that cleans. Literally: bleach is in ~80 % of homes, and
acid toilet/limescale cleaners in most of the same shopping carts.
Parents, pet owners (gases pool low), caregivers, and anyone who has
ever thought "I'll mix them, it'll clean better".

## Disclaimer

First-aid-level information. Real exposure → fresh air + poison control
(US 1-800-222-1222, UK 111, EU 112); breathing difficulty → emergency
services immediately. Always read the actual product label.

## License

MIT © 2026 Denis Voronin
