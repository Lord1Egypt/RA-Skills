# Attic Insulation Payback

Attic top-up insulation is the highest-return home energy upgrade for most houses — **when the attic is actually thin**. But the physics has brutal diminishing returns: R-2→R-13 cuts attic heat loss ~85%; R-38→R-60 cuts a small remainder by ~37%. Contractors quoting "double your R, halve your bill" exploit the fact that homeowners don't know which side of the curve their attic is on.

This skill computes it honestly:

1. **Degree-day heat-loss model** — `U×A×HDD×24` at current vs target R, converted to your fuel units (therms/gallons/kWh) at your price and system efficiency.
2. **Bill calibration** — the model's attic share of your winter fuel is capped at a defensible 40%; anything higher flags a wrong R estimate or area and rescales.
3. **Diminishing-returns table** — savings at R-30/38/49/60 so you can quote the contractor the flat part of the curve and buy the knee, not the brochure.
4. **Verdicts** — DO IT / BORDERLINE / NOT WORTH IT / OVERSOLD — SEAL FIRST, with the air-sealing-first doctrine (fiberglass doesn't stop moving air; buried bypasses keep wasting energy under new R).
5. **R-check mode** — quoted "R-49" from 12 inches of settled cellulose: label R vs in-service R after settlement.

## Real problem it solves
US homes leak ~$200–400/yr through under-insulated attics, and insulation quotes are ripe for overselling because the savings are invisible and deferred. The instrument replaces the contractor's claim arithmetic with your own numbers — area, measured depth, real fuel price, real bills — and tells you whether to do the job, demand the R-38 price instead of R-60, fix air sealing first, or walk away. It also catches the classic quote traps: no air-sealing line item, per-bag thickness games, and bath fans "vented" into the new insulation.

## Quick start
```bash
python3 scripts/attic_payback.py --area 1200 --r-current 19 --r-target 60 \
    --fuel gas --hdd 5200 --price 3.20 --system-eff 0.80 --quote 3400
python3 scripts/attic_payback.py --r-check --inches 12 --material cellulose
```

## Contents
- `SKILL.md` — model, verdict bands, seal-before-stack doctrine, pitfalls, example
- `references/insulation-physics-and-quotes.md` — curve tables, measuring rules, quote forensics, rebates, HDD zones, when NOT to insulate
- `scripts/attic_payback.py` — stdlib-only CLI (payback + r-check)
