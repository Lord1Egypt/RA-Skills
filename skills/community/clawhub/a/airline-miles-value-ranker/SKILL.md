---
name: airline-miles-value-ranker
description: Use when deciding how to spend frequent-flyer miles or credit-card points — comparing redemption options, judging a "deal," choosing between pay-with-miles, booking awards directly, or transferring points to partners — computes cents-per-point for each option with fare-comparison math, checks against 12 known partner sweet spots, prices the cash-fare floor, and issues BURN / HOARD / NEVER verdicts so a 300k-point balance never gets flushed at 0.4¢.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [travel, miles, points, awards, loyalty, cpp, redemption, credit-cards]
---

# Airline Miles Value Ranker

Points and miles die twice: they expire, and they die quietly when
you spend 50,000 of them on a $200 flight — a 0.4¢-per-point
redemption that a transfer partner would have turned into $1,000+
of value. The average leisure redeemer doesn't compute cents per
point (CPP) at all; the airline apps make sure the worst option is
the easiest button to press ("Pay with miles — 25,000 points!"
on a $180 ticket).

This skill turns every redemption decision into arithmetic:

```
CPP = (cash fare − taxes/fees paid on award) / points spent × 100
```

It ranks your actual options, compares them to anchor values
(~1.0–1.5¢ for major currencies), flags the sweet spots worth
chasing, and says BURN / HOARD / NEVER plainly.

## When to Use

- "Should I use 60,000 miles for this flight or just pay $580?"
- Comparing an airline's own "book with miles" price vs a transfer
  partner award vs paying cash and saving the miles
- Deciding whether to move credit-card points to a partner now or
  wait for a transfer bonus
- Planning a big redemption (business class, family of four) and
  wanting the ordering: which airline, which route, which cabin
- Points expiring — "dump them on something" mode: best floor
  values to burn into rather than $0 after devaluation
- Post-devaluation triage: an award chart just got worse — what's
  the new best use of the balance?

Don't use for: hotel points (different economics — nightly value
vs fare comparison; the CPP math transfers but the anchors don't),
or cash-back cards (no redemption complexity — just take 2%).

## The Value Model

### Step 1 — Establish the cash fare honestly

The comparison fare is **what you would actually pay** for that
exact itinerary in that exact cabin:

- Same flights, same cabin, same date — from a search, not memory
- If you'd never pay $6,000 for business class, you may still use
  it as the ceiling, but ALSO price premium-economy on the same
  route: the honest "value over what I'd buy" number
- Include the taxes/fees the award requires you to pay in cash:
  award value = (cash fare) − (award's cash copay)

### Step 2 — Compute CPP for every option on the table

For each candidate: `(fare − copay) / points × 100`. The script
(`scripts/miles_ranker.py evaluate`) does this and ranks them.

### Step 3 — Judge against anchors

| Currency | Weak | Fair | Good | Excellent |
|---|---|---|---|---|
| Amex MR / Chase UR (transferable) | <1.0¢ | 1.0–1.25¢ | 1.25–1.8¢ | >1.8¢ |
| Airline miles (UA/DL/AA class) | <0.8¢ | 0.8–1.2¢ | 1.2–1.6¢ | >1.6¢ |
| Hotel points (context only) | <0.5¢ | 0.5–0.8¢ | 0.8–1.2¢ | >1.2¢ |

A transferable point spent at 1.0¢ via portal credit is the floor
— spending transferrable points BELOW the portal rate is a pure
loss with extra steps.

### Step 4 — Verdicts

- **BURN** — CPP at or above "Good" for that currency, or points
  expiring, or a known devaluation announced: book it
- **HOARD** — below Fair but balance is young, no expiry pressure,
  and a plausible big redemption within 12 months
- **NEVER** — any airline-program redemption below ~0.7¢, nearly
  all "pay with points at checkout" options, merchandise/gift
  cards (0.5–0.8¢ fixed), or paying with miles for taxes only

## Known Sweet Spots (verify current charts — they shift)

The script ships a sweet-spot table; treat it as a starting map:

1. **Short-haul partner awards** — 5,000–7,500 miles for hops
   that cost $150+ cash (1.5–2.5¢ CPP routinely)
2. **Business class to Europe on partners** — 55k–70k one-way
   vs $3,000+ fares
3. **ANA / Lufthansa first via partners** — the classic 2–4¢
   ceilings (fuel surcharges can gut it — compute, don't assume)
4. **Off-peak economy (AA-style charts)** — dated charts keep
   off-peak pricing long after dynamic cash pricing moves up
5. **Transfer bonuses 20–30%** — effectively multiply CPP of any
   partner plan; rarely worth chasing for sub-1¢ plans though

## The Expiry and Devaluation Clock

- Points that expire (many airline programs: 18–24 mo activity)
  are worth ~15% less book value — plan a burn before the wall
- A announced chart devaluation (happens ~yearly somewhere)
  converts HOARD to BURN for the affected program
- Transferable bank points don't expire — they are the correct
  parking lot for indecision

## Pitfalls

1. **Valuing business class at retail.** $8,000 first-class fare
   ≠ $8,000 of value if you'd never pay it. Use "value over the
   cabin you'd actually buy" as a second line — the script
   supports both via `--ceiling-fare` vs `--realistic-fare`.
2. **Forgetting the copay.** "Free" award with $560 in surcharges
   (LONDON) can be worse than a cheap cash ticket.
3. **Dynamic award pricing bait.** Programs now show
   "miles from 12,500" — your date may price at 95,000. Always
   evaluate the actual priced option.
4. **Transfer before confirming award space.** Points move one
   way. Confirm the award seat exists, THEN transfer.
5. **Sunk-mile fallacy.** "I have the miles so the flight is
   free" — no: miles spent below 0.7¢ are cash set on fire.
   Compare to the floor redemption every time.
6. **Mixing currencies in your head.** 100k Amex ≠ 100k Delta
   ≠ 100k Air France. Rank per-currency, then choose.

## Verification Checklist

- [ ] Cash fare pulled from a live search (not remembered)
- [ ] Award copay/taxes included in the math
- [ ] CPP computed per option, ranked
- [ ] Compared to the currency's anchor table
- [ ] Expiry / devaluation pressure factored into BURN vs HOARD
- [ ] Transfer options checked for bonuses before moving points

## Quick Recipe

```
python3 scripts/miles_ranker.py evaluate \
  --label "SFO→NRT business" --points 75000 --copay 42 \
  --realistic-fare 2600 --ceiling-fare 6800
python3 scripts/miles_ranker.py evaluate \
  --label "Same route economy" --points 40000 --copay 42 \
  --realistic-fare 850 --ceiling-fare 850
python3 scripts/miles_ranker.py compare
```

The compare view prints the ranked table with verdicts, so the
decision is a one-glance read.
