# Airline Miles Value Ranker

You have 300,000 points. The airline app shows a big friendly
button: "Pay with miles — 45,000 points!" on a $210 flight. One
tap and you've donated ~$450 of potential value back to the bank.

## The Problem

- Points/miles are a parallel currency most people spend **without
  pricing**. The programs' own interfaces steer you to the worst
  redemptions (merchandise, gift cards, checkout sliders).
- Value varies by **5-10×** between redemptions of the same
  currency: 0.4¢ (gift card) to 3-5¢ (partner business class).
- Points quietly **expire** (18-24 months on many airlines) and
  get **devalued** (chart changes ~yearly). Hoarding without a
  plan is also a loss.
- Comparison shopping is hard: the same seat prices differently
  across 5+ partner programs, and transfer bonuses shift the math
  monthly.

## What This Skill Does

Turns "should I burn points here?" into one number and one word:

```
CPP = (cash fare − award copay) / points × 100   →   1.42c  [GOOD]
                                               →   VERDICT: BURN
```

- **evaluate** — score one option: realistic vs ceiling CPP,
  per-currency band (WEAK/FAIR/GOOD/EXCELLENT), BURN / HOARD /
  NEVER verdict, expiry-aware
- **compare** — ranked table across everything you've scored;
  names the best burn
- **sweet-spots** — 7 known high-CPP patterns (short-haul
  distance charts, ANA round-trips, transfer bonuses, surcharge
  escape routing) to check before settling
- Floor rule: never spend transferable points below the
  program's own cash-out rate — that's a guaranteed loss
- Family/mixed-itinerary options rank as their own rows

## Example

```
$ python3 scripts/miles_ranker.py evaluate --label "SFO->NRT biz" \
    --points 75000 --copay 42 --realistic-fare 2600 \
    --ceiling-fare 6800 --currency amex
  realistic: $2,600 -> 3.41 c/pt  [EXCELLENT]
  VERDICT: BURN

$ python3 scripts/miles_ranker.py evaluate --label "Weekend hop" \
    --points 45000 --realistic-fare 210 --currency amex
  realistic: $210 -> 0.47 c/pt  [WEAK]
  VERDICT: NEVER (below cash-out floor - take the cash rate)
```

Same 300k balance: one option triples its value, the other
flushes it. The ranker makes the difference visible before you
tap the button.

## Who Needs This

Anyone with a travel-rewards card or airline balance — in the
US alone, adults hold hundreds of billions of unredeemed points.
If you've ever said "I have miles, let me just use them," this
is the 30-second check that keeps those miles from being spent
at pawn-shop rates.

MIT License. Data stays local (`scripts/data/miles_log.json`).
