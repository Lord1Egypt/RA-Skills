---
name: black-friday-deal-detector
description: "Use when evaluating any sale, Black Friday doorbuster, or 'was $X now $Y' claim: detects fake-MSRP anchoring, pre-sale price inflation, coupon-stacking theater, and % off a price nobody paid. Scores the deal against 12-month category price bands and historical-low baselines, with verdicts WAIT / OK DEAL / GREAT / PRICE THEATER."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [shopping, black-friday, deals, price-history, consumer, fraud-detection]
---

# Black Friday Deal Detector

## Overview

The "60% OFF!" tag is theater. Retail's pricing playbook has three moves this
skill detects:

1. **Fake anchor MSRP** — the "list price" nobody has charged for a year.
   TVs are the canonical case: a 65" TV "listed" at $1,299 that has sold for
   $799 every non-holiday week since March.
2. **Pre-sale inflation** — price raised 10–30% in October so November's
   "40% off" lands at the August price. Trackers catch this; shoppers don't.
3. **% off a phantom price** — "doorbusters" engineered so the discounted
   price equals the street price of an equivalent unit, with the delta made
   up by a made-up anchor.

The math that matters is not `% off` but **price vs the 12-month low band**.
A "50% off" that lands 5% above the all-time low is a mediocre deal. A "15%
off" that undercuts the 12-month low by 10% is a genuinely great one.

This skill scores a claimed deal against category-specific price behavior
(TVs depreciate on a curve, Apple gear rarely discounts, mattresses have
400% markups, power tools have two real sale windows/year) and produces a
verdict plus a buy strategy.

## When to Use

- Evaluating any Black Friday / Cyber Monday / Prime Day / "anniversary sale" claim
- Deciding between two "deals" on similar items
- Checking a doorbuster before queuing or clicking
- Any "was/now" price tag in any store, any month
- Deciding whether to buy now or wait (category seasonality table)

**Don't use for:** live price tracking (that's price-predator's job with
actual trackers), or collectibles with no price history logic.

## The Detection Model

### Input signals (what you can observe in 60 seconds)

| Signal | Where to find it |
|---|---|
| Claimed list/MSRP | the tag |
| Sale price | the tag |
| Street price (major retailers today) | 30-second check: Amazon/Walmart/BestBuy/Target |
| 12-month price range | camelcamelcamel (Amazon), Keepa, Honey |
| Model number + year suffix | the box (e.g., UN65CU7000 vs CX700D) |
| "Exclusive model" wording | the tag (often a derivative SKU built for the sale) |

### The seven price-theater patterns

1. **Inflated anchor** — claimed MSRP > any price charged in 12 months.
   Score the deal off street price, not MSRP.
2. **October bump** — price in Sept < price in late Oct < "sale" price.
   Trackers show it; treat the Sept price as the real anchor.
3. **Derivative SKU** — model number exists only at this retailer (or differs
   by one letter). Built to be "exclusive" and un-comparable. Check the spec
   sheet, not the model name.
4. **% off the bundle** — discount computed against a bundle whose extras you
   wouldn't buy (cables, software trials).
5. **Coupon-stack maze** — needs app + newsletter + card to reach the
   advertised price. The honest price is the one without the maze.
6. **Gift-card-back pricing** — "$100 back in gift cards" — real value is
   40–70% of face for a store you won't revisit; and it converts the deal
   into two transactions.
7. **Membership-gated floor** — the good price requires a paid membership
   (Costco/My Best Buy+/Walmart+). Fine if you'd pay for it anyway; not a
   "deal" if the membership was bought for this.

### Category baselines (what a real deal looks like)

| Category | Typical real discount from street | Notes |
|---|---|---|
| TVs | 20–35% off street | Derivative SKUs rampant; check panel specs vs model lineage |
| Apple | 5–15% (usually gift-card back) | Real cash discounts rare except clearance/resellers |
| Laptops | 15–30% | Compare CPU gen + RAM + screen, not model name |
| Mattresses | "50%" is normal pricing | 300–400% markup; the real question is coupon-stacked floor |
| Power tools | 20–40%, two windows (June, BF) | Bare-tool bundling hides unit price |
| Video games | new: 0–10%; catalog: 30–60% | Digital storefronts discount harder than discs for old titles |
| Small kitchen appliances | 30–50% (Ninja/Vitamix/ KitchenAid) | BF is genuinely the low for the year on these |
| Sneakers/apparel | 25–40% | Compare against outlet price, not MSRP |
| Memory/storage (SSD/RAM) | cyclic 20–40% | Watch for slower-tier component swaps |
| Toys | 30–50% but stock risk | Big-list toys often cheaper in early Dec sales |

### Scoring

```
real_discount = (street_price − sale_price) / street_price      # vs TODAY's street
anchor_discount = (claimed_msrp − sale_price) / claimed_msrp    # the theater number
low_gap = (sale_price − twelve_month_low) / twelve_month_low    # vs history
```

- Verdict is driven by **real_discount** and **low_gap**, never anchor_discount.
- Any anchor_discount − real_discount > 15 points ⇒ flag PRICE THEATER.

| Verdict | Meaning | Action |
|---|---|---|
| **PRICE THEATER** | discount is mostly fake anchor | don't buy; note the street price |
| **WAIT** | above 12-month low; category has a better window | set alert at low − 5% |
| **OK DEAL** | within ±5% of 12-month low | buy if you need it |
| **GREAT** | ≤ 12-month low, ideally beating it | buy now; this is the annual floor |

## Using the Script

```bash
# The classic: 65" TV "was $1299", now $799, street today $749
python3 scripts/deal_detector.py --msrp 1299 --sale 799 --street 749 --low 699

# Deal with gift-card back and membership gate
python3 scripts/deal_detector.py --msrp 999 --sale 799 --street 829 --low 779 \
    --gift-card-back 100 --membership-cost 50

# Compare two competing claims
python3 scripts/deal_detector.py --compare "TV-A:1299:799:749:699" "TV-B:1099:749:779:739"
```

Output: real vs anchor discount, theater gap, gift-card-adjusted price,
verdict, and a one-line strategy.

## Common Pitfalls

1. **Reading the strikethrough price.** It is marketing copy, not data. The
   only numbers that matter: today's street price and the 12-month low.
2. **Skipping the model-number check.** "Exclusive" derivative SKUs (one
   letter different) exist precisely so you can't compare. Compare specs.
3. **Valuing gift cards at face.** $100 back at a store you never revisit is
   worth maybe $40. Value gift-card-back at 50% unless you shop there monthly.
4. **Forgetting return-window resets.** BF purchases bought as gifts in
   November often have return windows that expire Dec 26 — before the gift
   is given. Check the policy; some retailers extend for holidays.
5. **Buying "50% off" mattresses.** That's the everyday disguise of the
   industry; the real deal is the coupon-stacked floor price vs competitors'
   floor.
6. **Confusing clearance with deals.** Clearance = discontinued, no support,
   final sale. Sometimes great; never the same risk profile.

## Verification Checklist

- [ ] Street price checked at 2+ major retailers (not just the seller)
- [ ] 12-month low pulled from a price tracker (camelcamelcamel/Keepa)
- [ ] Model number matches the comparable unit (letter-suffix check)
- [ ] Gift cards valued at 50%, membership cost amortized in
- [ ] Verdict from real_discount + low_gap, not the anchor
