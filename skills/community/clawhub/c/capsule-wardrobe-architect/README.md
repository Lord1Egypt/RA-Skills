# Capsule Wardrobe Architect

The average adult owns 100+ garments, wears ~20% of them, and still faces "nothing to wear" mornings. The problem isn't taste — it's **structure**: closets fill with orphan items that pair with nothing while the interchangeable core stays thin, and nobody does the math on what clothes actually cost per wear.

This skill is a quantitative wardrobe instrument with four commands:

1. **Cost-per-wear** — `price ÷ wears`. A $250 coat at $0.33/wear beats a $25 top worn twice ($12.50/wear) by 38×. Computes realized vs projected CPW and the break-even wear count for any target.
2. **Outfit combinatorics** — counts *real* outfits via a compatibility matrix (tops × bottoms × pairable-fraction + layer contribution), not naive multiplication. Verdicts: <14 outfits = structural wardrobe poverty; 20–40 = functional core; >40 = diminishing returns.
3. **Laundry-cycle sufficiency** — queueing math: `items needed = wears per cycle + 1 in the wash + 1 buffer`. Weekly-wash work shirts need 9, not 5 — "always behind on laundry" is a depth problem, not a discipline problem.
4. **Lifestyle-allocation gaps** — compares the closet's role mix against how waking hours are actually spent, producing a max-3-item buy list (chosen for outfit leverage) and a donate list priced by CPW.

## Real problem it solves
Americans spend ~$1,800+/yr on clothing, and impulse buys that pair with nothing are the leak. The instrument converts "I need more clothes" into numbers: whether the closet's real problem is compatibility (replace orphans with neutrals), laundry depth (buy 2 more shirts), allocation (own 40% dress-up for a 5% dress-up life), or nothing at all (do not shop). It also prices every purchase honestly, ending the "investment piece" self-deception that realized-CPW post-mortems expose.

## Quick start
```bash
python3 scripts/capsule.py cpw --price 90 --worn 9 --lifetime 60
python3 scripts/capsule.py outfits --tops 14 --bottoms 8 --layers 3 --compatible 0.45
python3 scripts/capsule.py laundry --items 5 --wears-per-item 1 --cycle-days 7 --role work
python3 scripts/capsule.py gaps --work 0.45 --casual 0.30 --active 0.15 --dressup 0.05 --home 0.05 \
    --work-items 6 --casual-items 9 --active-items 1 --dressup-items 2 --home-items 8
```

## Contents
- `SKILL.md` — the four instruments, verdict bands, pitfalls, example session
- `references/wardrobe-doctrine.md` — compatibility matrix method, uniform doctrine, shopping/declutter protocols, CPW tables
- `scripts/capsule.py` — stdlib-only CLI: cpw / outfits / laundry / gaps
