---
name: capsule-wardrobe-architect
description: Use when the closet is full but "nothing to wear", before a clothes-shopping trip, or when building a travel/capsule wardrobe — cost-per-wear amortization, outfit combinatorics with a compatibility matrix, laundry-cycle sufficiency math, and lifestyle-allocation gap analysis that tells you exactly which 2-3 items to buy and which never to buy again.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [wardrobe, capsule, cost-per-wear, personal-finance, style, decluttering]
---

# Capsule Wardrobe Architect

## Overview
The average adult owns 100+ garments, wears ~20% of them regularly, and still faces "nothing to wear" mornings. The failure isn't taste — it's **structure**: closets accumulate single items that pair with nothing, while the working core (tops × bottoms that all interchange) stays tiny. A capsule works because of **combinatorics**: 8 interchangeable tops and 5 bottoms that all pair produce 40 base outfits; 8 mismatched tops and 5 bottoms can produce as few as 8.

This skill is a quantitative wardrobe instrument: it computes **cost-per-wear** (the only honest price of clothing), counts **real outfits** through a compatibility matrix rather than naive multiplication, checks the closet against the **laundry cycle** (enough work shirts to survive until wash day with one in the wash), and compares what you own against the **lifestyle allocation** your calendar actually shows (work 45%, gym 15%, home 25%, dress-up 5%…) — producing a buy-list of at most 2–3 items and a donate-list of everything below a CPW threshold.

## When to Use
- "I have a full closet but nothing to wear" — run the outfit count and gaps audit first
- Before a shopping trip — get the exact buy-list so impulse buys have to beat real items on CPW
- Building a travel capsule or work uniform — right-size the count for trip length × laundry access
- After weight change / new job / new climate — reallocate the closet to the new life percentages
- Decluttering — donate/keep verdicts priced by cost-per-wear, not by "might need someday"

**Don't use for:** children's clothing (sizing churn dominates — see hand-me-down logic instead), or specialty gear (ski, formalwear) where need is episodic — count those separately.

## Quick Start
```bash
# What does that $90 sweater actually cost? (worn 9 times, expects 60 lifetime wears)
python3 scripts/capsule.py cpw --price 90 --worn 9 --lifetime 60

# How many REAL outfits does the closet make? (compatibility = fraction of pairs that work)
python3 scripts/capsule.py outfits --tops 14 --bottoms 8 --layers 3 --compatible 0.45

# Do I survive 7 days between laundry with 5 work shirts?
python3 scripts/capsule.py laundry --items 5 --wears-per-item 1 --cycle-days 7 --role work

# What should I actually buy? (closet counts vs how I actually spend my days)
python3 scripts/capsule.py gaps --work 0.45 --casual 0.30 --active 0.15 --dressup 0.05 --home 0.05 \
    --work-items 6 --casual-items 9 --active-items 1 --dressup-items 2 --home-items 8
```

## The Four Instruments

### 1. Cost-per-wear (the honest price tag)
`CPW = price ÷ expected lifetime wears`. A $250 coat worn 150×/yr for 5 years = $0.33/wear. A $25 trendy top worn twice = $12.50/wear — **38× more expensive**. Rule of thumb: anything with CPW > $3 (frequently-worn categories) or destined for <10 wears is a rental/borrow candidate, not a purchase. The `cpw` command prices past purchases two ways: **realized CPW** (price ÷ wears so far — the honest post-mortem) and **projected CPW** (price ÷ lifetime — the shopping decision number).

### 2. Outfit combinatorics with compatibility
Naive count `tops × bottoms` lies: the real number is `tops × bottoms × compatible-fraction`, plus layer multipliers (each layer that works over most tops adds a distinct look for ~60–80% of combos). Verdict bands: **<14 distinct outfits for daily rotation = wardrobe poverty** (you repeat weekly and it feels like it); 20–40 = functional core; >60 = diminishing returns — more items add clutter, not looks. The fix is rarely "more clothes": going from 40% to 80% compatibility by replacing 3 odd items can double outfits while *shrinking* the closet.

### 3. Laundry-cycle sufficiency
Clothing needs are a queueing problem, not a style problem: `items needed = wears per cycle + 1 in the wash + buffer`. Work shirts worn once between weekly laundry = 8–9 needed (7 wears + 1 in the wash + 1 spill buffer). Jeans at 3 wears each across a 7-day cycle need only 3. The `laundry` command computes sufficiency per role and names the exact shortfall — the most common cause of "I'm behind on laundry" is owning 5 of something that mathematically requires 8.

### 4. Lifestyle-allocation gaps
Sort what you own by role, then compare against the *share of waking hours* each role actually occupies. A closet that is 40% dress-up while life is 5% dress-up is a mispriced portfolio. The `gaps` command outputs each role's surplus/deficit in items and a **maximum-3-item buy list** ranked by (deficit × outfit leverage) — an item that completes many pairs beats an item that pairs with one thing, always.

## Common Pitfalls
1. **Counting items instead of outfits.** 40 items that make 12 outfits lose to 15 items that make 30. Optimize pairs, not pieces.
2. **Buying into a gap that's actually a compatibility problem.** A new top that pairs with only one bottom adds 1 outfit; a neutral basic can add 5+.
3. **Ignoring the laundry cycle** — the right number of work shirts is a queueing answer (wears + 1 + buffer), not a style answer.
4. **CPW on past purchases used to justify future ones** ("the $200 boots were worth it") without checking the *realized* CPW of the last three "investment" pieces.
5. **One-color-pillar closets with zero contrast items** — a 100%-neutral capsule produces technically many outfits that all look the same; reserve ~20% statement/contrast pieces that work with ≥70% of the base.
6. **Decluttering by KonMari joy alone** — keep the boring high-CPW core (plain tees, dark bottoms); joy-based purges evict exactly the interchangeable base and keep the oddball singles.

## Verification Checklist
- [ ] Cost-per-wear computed for the last 5 purchases (realized vs projected both recorded)
- [ ] Real outfit count = tops × bottoms × compatibility + layer contribution — not the naive product
- [ ] Laundry sufficiency checked per role (work / active / home) against the real wash-day interval
- [ ] Lifestyle allocation table filled from an actual week, not an aspirational one
- [ ] Buy list capped at 3 items, each scored by outfit leverage; donate list priced by CPW threshold
- [ ] Re-run `outfits` after changes — target ≥20 distinct daily outfits from the core

## Example Session
```
$ python3 scripts/capsule.py outfits --tops 14 --bottoms 8 --layers 3 --compatible 0.45
OUTFIT MATH — 14 tops x 8 bottoms x 3 layers
  base pairs:                112
  compatible (~45%):         ~50 real base outfits
  + layers (70% coverage):   +105 looks  ->  ~155 total combinations
  distinct daily outfits:    ~50 (layers repeat looks, they don't create new ones)
VERDICT: FUNCTIONAL CORE — volume is fine. The closet's problem (if any) is
  allocation or laundry, NOT item count. Do not shop.

$ python3 scripts/capsule.py gaps --work 0.45 --casual 0.30 --active 0.15 --dressup 0.05 --home 0.05 \
    --work-items 6 --casual-items 9 --active-items 1 --dressup-items 2 --home-items 8
LIFESTYLE vs CLOSET (26 daily-rotation items)
  work      45.0% of life   6/26 items (23.1%)  -> DEFICIT +22 pts  ** biggest gap
  active    15.0% of life   1/26 items ( 3.8%)  -> DEFICIT +11 pts
  home       5.0% of life   8/26 items (30.8%)  -> SURPLUS -26 pts  donate candidates
  casual    30.0% of life   9/26 items (34.6%)  -> surplus -5 pts   about right
  dressup    5.0% of life   2/26 items ( 7.7%)  -> about right
BUY LIST (max 3 roles): 6 work item(s); 3 active item(s) — choose
  NEUTRAL basics pairing with >=4 existing pieces (leverage = outfits
  added). DONATE: 7x home; 1x casual duplicates past CPW threshold.
```
