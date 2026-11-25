---
name: garage-sale-pricer
description: "Use when preparing a garage/yard/tag sale — pricing items, building the inventory with printable price tags, planning change float, signage, timing, and routing leftovers to donation/consignment/curb. Encodes what garage-sale items actually sell for (furniture 10-15% of retail, clothes $1-5) with condition multipliers and day-2 half-off ladders, so sellers stop guessing and buyers stop lowballing."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [garage-sale, yard-sale, declutter, pricing, selling, secondhand]
---

# Garage Sale Pricer

## The problem it solves
Half of America has run (or will run) a garage sale, and the two failure modes are symmetric:
- **Overprice everything → nothing sells** → the whole weekend becomes a staging area for the donation truck.
- **Underprice from decision fatigue** → the $200 treadmill leaves for $10 because 300 items needed prices and the seller gave up at item 40.

Meanwhile the logistics bite: no small bills at 7:15 AM when someone hands you a $20 for a $3 lamp; signs that violate city rules; no plan for the leftovers.

This skill prices from a knowledge base of what things ACTUALLY sell for at garage sales (not Facebook Marketplace — garage-sale prices are 30–50% of online), generates the priced inventory with printable tags, sizes the change float from expected sales, and routes unsold items to donation/consignment/curb by category value.

## When to trigger
- "I'm having a garage sale next weekend" / "help me price my stuff for a yard sale".
- Downsizing/estate cleanouts, moving sales, post-declutter (pairs with declutter-pilot).
- "How much should I ask for my [couch/lawn mower/kids' clothes]?" in a garage-sale context.

## Steps
1. Build the inventory: `add` items (category, brief name, condition A–D, original price optional) or feed a JSON batch.
2. **Price engine:** `base_band` per category (garage-sale reality bands) × condition multiplier (A 1.3 / B 1.0 / C 0.7 / D 0.4, floored for 'free' class) → a printed price + a "negotiable floor" (the walk-away number, typically 50-70% of tag).
3. **Day ladder:** Day 1 tag price; Day 2 (or after 11 AM) −50%; last hour "fill a bag $5". The script prints tag text with the ladder built in ("$12 / after Sat noon $6").
4. **Change float:** from expected total sales × typical transaction mix → $100-150 float ($40 in $1s, $20 in $5s, $30 in $10s, $20-roll quarters, one $20-decisions buffer). Never start a sale without ones.
5. **Logistics block:** signage count/placement (2-4 major intersection + 1-2 per turn, balloons, city ordinance check), timing (Sat 7-8 AM start, serious buyers come first 90 min), display doctrine (everything visible, nothing in boxes), power strip for testing electronics, free pile placement.
6. **Leftover router:** per item value band → donate (value < $20 class: clothes, books, housewares — schedule the truck BEFORE the sale) / consign (furniture, brand clothes > $50 band) / curb-alert / keep.

## Pricing knowledge (summary — full table in references/)
| Category | Garage-sale band | Notes |
|---|---|---|
| Furniture (upholstered) | 10-15% retail | the hardest sell; photos online if > $100 |
| Furniture (wood, solid) | 20-30% retail | mid-century/brand names command top of band |
| Clothing (adult) | $1-5 | $0.50-2 basics; brand $5-10 on a rack |
| Kids clothes | $0.50-2/pc | sizes labeled; onesies in $1 bags |
| Books/media | $0.50-2 | paperbacks 3/$1 pricing moves volume |
| Electronics | 20-30% retail | powered-on display + "works" note = price power |
| Tools (power) | 30-50% retail | sell themselves; include blades/case |
| Bikes | $20-60 adult | kids $10-30; tune-up test ride at sale |
| Toys | $1-10 | complete sets 5× loose parts; battery door check |
| Kitchen small appliances | $5-20 | clean = +30%; original box rare bonus |

## Pitfalls
- **Garage-sale ≠ online prices.** Buyers factor "no returns, no shipping, today only" downward 30-50%. Tag accordingly or route the item to marketplace/consignment instead (the router does).
- **Priced items sell; unpriced items don't.** Mystery-priced tables get skipped. Tag everything, even the free pile ("FREE — take one").
- **The $20-at-7AM problem:** no change = lost sales + vulnerable position. Get the float Friday at the bank, not Saturday at 6 AM.
- **Sign ordinance violations get sales shut down mid-morning** — check city rules (some ban signs on utility poles outright).
- **Never sell:** recalled items (drop-side cribs, old car seats — check recalls.gov), helmets after a crash, expired car seats >6-10 yrs.
- **Cash box discipline:** fanny pack > open box; large bills go to the house hourly; note Venmo/Zelle QR code taped to the table (modern buyers carry no cash — the QR recovers 20-30% of sales).
- Hot items (tools, bikes, gaming, brand kids' gear) listed on marketplace Friday night with "garage sale Saturday, first come" pulls early traffic.

## Example
```
$ python3 scripts/garage_sale.py price --category furniture_upholstered --condition C --retail 900
SOFA (retail $900, condition C): tag $70  (band $68-135 x condition 0.7)
  floor: $45 · day-2: $35 · last hour: fill-a-bag or donate
$ python3 scripts/garage_sale.py plan --items 120 --avg-price 6
Expected gross $450-720 · change float: $130 ($40x$1, $20x$5, $30x$10, quarter roll, $20 buffer)
Signs: 4 intersection + 2 directional · Sat 7:00 start · QR code for payment on every table
```

## Files
- `scripts/garage_sale.py` — price engine + inventory with tag sheet + float sizer + leftover router (stdlib only).
- `references/price-bands.md` — full category band table with condition multipliers and negotiation floors.
- `references/sale-day-playbook.md** — signage, timing, display, safety, ordinances, post-sale routing.
- `README.md` — the real-world framing.
