---
name: car-lease-end-negotiator
description: Use when a car lease is ending in the next 6 months — computes the three-way decision (return vs buy out vs buy-and-sell for equity) from residual, market value, and remaining payments, prices the excess-mileage and wear bills both ways (lease rate vs pre-purchase packs vs tire-shop fix), flags equity-positive leases people walk away from, and lays out the pre-turn-in inspection playbook that keeps the disposition fee negotiable.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [car-lease, lease-end, buyout, residual, excess-mileage, automotive, negotiation]
---

# Car Lease-End Negotiator

## Overview
Every lease ends in a decision most lessees make blind: sign the turn-in papers in the dealer parking lot. But a lease end is three transactions in one — **return** (pay disposition + mileage + wear and walk), **buyout** (pay the residual written 3 years ago), and **buy-and-sell** (buy at residual, sell at today's market). Used-car price swings since 2020 have repeatedly made residuals **below** market: lessees sitting on $2,000-$5,000 of equity have handed it back to the lessor by simply returning the car — the single most expensive default in personal automotive finance. Conversely, leases written at 2022 peak residuals (when lessors overestimated values) are gold to return and walk from.

The other money is in the fee stack: excess-mileage at $0.20-$0.30/mi vs mileage "packs" priced lower, wear-and-tear adjudicated by a third-party inspector whose findings are negotiable line-by-line, disposition fees ($300-$500) waived when you lease or buy again, and the tax wrinkle that in many states buying out your own lease avoids sales tax on the full residual only in lease-to-own transitions... which is exactly the kind of detail that moves a $1,500. This tool computes all three paths from your contract numbers and prints the negotiation sheet.

## When to Use
- Lease ends within 6 months (equity check: is market > residual?)
- Turn-in inspection letter arrived with a wear bill ("dented wheel $150, windshield chip $90")
- Over mileage and deciding between paying at turn-in, buying extra miles now, or buying the car out (mileage is irrelevant at buyout)
- Considering buying out and keeping, vs buying the same car used elsewhere
- Lease-end "loyalty offer" letters arriving (they're opening bids, not gifts)

**Don't use for:** lease-vs-buy-new-car decisions at signing (different math), early lease termination mid-contract (different playbook — the penalties dominate), or commercial/fleet leases (different fee structures).

## Quick Start
```bash
# The three-way decision
python3 scripts/lease_end.py decide --residual 18000 --market 20500 \
    --months-left 8 --payment 320 --disposition 400 \
    --miles-now 28500 --mile-allowance 36000 --mile-rate 0.25

# Price the wear bill that inspection letter just sent
python3 scripts/lease_end.py wear --items "wheel scuff,160" "windshield chip,90" \
    "tire tread,420" --self-fix-est 380

# Negotiation sheet + inspector checklist
python3 scripts/lease_end.py sheet --residual 18000 --market 20500 --disposition 400

# Worked demo
python3 scripts/lease_end.py --demo
```

## How the Decision Math Works
```
RETURN cost     = disposition + excess miles × rate + adjudicated wear
BUYOUT cost     = residual + purchase fees (+ sales tax on residual per state)
BUY-AND-SELL    = market − residual − sale/transfer costs − payoff fees
equity          = market − residual  (positive equity = NEVER just return it)
```
- Excess mileage vanishes at buyout — the car doesn't know how far you drove it. Over-mileage lessees with equity-positive cars can *sell* their way out of a $1,500 mileage bill.
- Wear items are negotiable: get the inspection report, price each line at an independent shop/tire store, fix the cheap ones (bumpers, scuffs), contest the borderline ones (normal-use vs damage definitions are in your contract's wear guide).
- Disposition fee is routinely waived with a repeat lease or purchase from the same captive — ask, it's a phone call.

## Numbered Workflow
1. Pull contract numbers: residual (purchase-option price), disposition fee, mileage allowance + rate, months remaining.
2. Get market value: private-party AND dealer-retail from 2+ guides (KBB/Edmunds/NADA vary by $1,000s — use private-party for buy-and-sell, trade/retail mid for equity sense).
3. Run `decide` — get the three-path cost table and the verdict.
4. If equity is positive: get payoff quote in writing, confirm title/paperwork path with your credit union or the captive before the last payment date; never announce you're selling at the dealer desk.
5. If returning: schedule the **pre-turn-in inspection** (not the turn-in day) — you want weeks to fix, not minutes to argue. Run `wear` on the report.
6. Run `sheet` — print the negotiation card: what's waivable (disposition), what's fixed (tax), what's contestable (wear lines), what's your walk-away (equity).
7. Compare any "loyalty pull-ahead" offer (waived remaining payments) against the equity you'd surrender — pull-ahead is often a trap when residuals are low.

## Common Pitfalls
1. **Returning an equity-positive lease** — if market > residual by $1,000+, returning donates that money to the lessor. This is the #1 lease-end mistake.
2. **Paying the wear bill at face value** — inspector line items are opening asks; tread-depth charges die when you replace two tires at Costco for less than the adjudicated 4-tire charge.
3. **Ignoring the pre-inspection** — the free inspection 60 days out is the process working for you; skipping it converts every defect into a parking-lot surprise.
4. **Accepting the first disposition-fee answer** — it's waived all the time with a same-brand next step; ask the captive directly, not the dealer.
5. **Letting mileage math run the decision when equity exists** — mileage only matters on the return path; buyout/sale paths don't see it.
6. **Forgetting purchase-option fees and state tax quirks** — a $300 purchase fee or 9% sales tax on the residual can flip a thin buyout win into a loss; `decide --tax-rate` prices it.

## Verification Checklist
- [ ] Residual/purchase-option price taken from the CONTRACT, not a statement
- [ ] Market values from 2+ sources; private-party used for buy-and-sell path
- [ ] Payoff quote in writing before the last payment date
- [ ] Pre-turn-in inspection scheduled ≥30 days before maturity
- [ ] Wear report line-itemed, each line priced independently, cheap fixes done
- [ ] Disposition-fee waiver asked for (phone, then in writing)
- [ ] Pull-ahead offer compared against equity surrendered

## One-Shot Recipes
**"Lease ends in 3 months, 5,000 miles over"** → `decide` with real numbers; over-mileage + equity-positive → buy-and-sell (miles vanish); over-mileage + equity-negative → ask the captive to sell a mileage pack pre-turn-in, usually cheaper than the end-of-lease rate.
**"Inspection letter: $912 in wear"** → `wear --items ...` with shop quotes; fix scuffs/tires yourself, contest normal-use items citing the wear guide, bring the printed comparison to the turn-in.
**"Captive offers to waive my last 4 payments to re-lease now"** → run `decide` twice (return now vs at maturity); if equity > waived payments, decline and capture the equity instead.
