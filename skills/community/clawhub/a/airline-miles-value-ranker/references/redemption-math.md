# Miles Value Ranker — Reference

## The core formula

```
CPP = ((cash fare for same itinerary) − (cash copay on award)) / points × 100
```

Two fare inputs matter:

- **Realistic fare**: what you would genuinely pay for that
  itinerary in that cabin if awards didn't exist. This is the
  honest denominator for "should I burn points."
- **Ceiling fare**: the retail price of the premium cabin. Used
  only for reporting the theoretical max CPP — treat it as a
  vanity number unless you truly buy that cabin.

Report both; decide on realistic. A business award at 7¢ ceiling /
1.2¢ realistic is a genuinely good burn if you *wanted* the
experience; it's a mediocre burn if you were going to buy economy
anyway.

## Anchor tables (2024-era consensus; drift happens)

### Transferable bank currencies
| Program | Floor use | Fair | Good | Excellent |
|---|---|---|---|---|
| Chase UR | 1.0¢ (cash/portal) | 1.0–1.25 | 1.25–1.8 | >1.8 |
| Amex MR | 0.6¢ (statement) – 1.0¢ (gift) | 1.0–1.25 | 1.25–1.8 | >1.8 |
| Citi TYP | 1.0¢ | 1.0–1.25 | 1.25–1.7 | >1.7 |
| Capital One | 0.5–1.0¢ | 1.0–1.2 | 1.2–1.5 | >1.5 |
| Bilt | 1.0¢ rent floor | 1.0–1.25 | 1.25–1.8 | >1.8 |

Rule of thumb for ALL transferables: never redeem below the
program's own cash-out rate. That rate is riskless and instant;
anything below it is a donation to the bank.

### Airline programs (mid-tier carriers similar)
| Program | Weak | Fair | Good | Excellent |
|---|---|---|---|---|
| United MileagePlus | <0.8 | 0.8–1.2 | 1.2–1.6 | >1.6 |
| Delta SkyMiles | <0.8 | 0.8–1.2 | 1.2–1.5 | >1.5 |
| American AAdvantage | <0.8 | 0.8–1.2 | 1.2–1.6 | >1.6 |
| Air France/KLM FB | <0.8 | 0.8–1.2 | 1.2–1.6 | >1.6 |
| Avianca LifeMiles | <0.9 | 0.9–1.3 | 1.3–1.7 | >1.7 |
| ANA Mileage Club | <1.0 | 1.0–1.4 | 1.4–2.0 | >2.0 |
| Alaska Mileage Plan | <0.9 | 0.9–1.3 | 1.3–1.8 | >1.8 |
| British Airways Avios | <0.8 | 0.8–1.2 | 1.2–1.6 | >1.6 |

## Sweet-spot map (starting points, verify before booking)

1. **Domestic short-haul via Avios/LifeMiles** — distance-based
   charts price 650-mile hops at 5,000–7,500 miles. Cash fares on
   those routes are often $150–250. CPP 2–4¢.
2. **Partner business to Europe** — 55k–70k one-way on Star/
   oneworld partners vs $2,500–4,000 fares. Watch surcharges:
   Lufthansa/JAL-style carriers add $300–600; ANA round-trip
   awards keep them near-zero.
3. **Japan/Asia premium via ANA** — round-trip requirement, but
   75k–90k business round-trip pricing made this the canonical
   3–5¢ redemption.
4. **Off-peak economy on dated charts** — AA off-peak to Europe
   (Oct–Apr) historically 22.5k each way vs $600–900 cash.
5. **Alaska partner awards** — priced per-partner charts; good
   floors for West Coast → Hawaii and Central America.
6. **Transfer bonuses** — 25–40% happen periodically (MR→Avianca,
   MR→BA, Citi→various). A 30% bonus turns a 1.2¢ plan into a
   1.56¢ plan — it upgrades FAIR to GOOD, it does not rescue a
   bad plan.
7. **Fuel-surcharge escape routes** — booking Lufthansa via
   Aeroplan vs via Miles&More can differ by $400 in YQ. The
   partner you book THROUGH sets the surcharge, not just the
   metal you fly on.

## Bad redemptions catalog (the NEVER list)

- Merchandise / gift cards / statement credits on airline
  programs: 0.4–0.8¢ fixed
- "Pay with miles" sliders at checkout (Delta-style): ~1¢ but
  earns nothing and kills elite credit — usually worse than a
  partner award on the same route
- Award flights on monopoly routes where cash is also absurd:
  compare against driving/bus before celebrating 1.5¢ on a fare
  nobody should pay
- Upgrades from deeply discounted economy where the program
  charges cash co-pay plus points (co-pays often $300–600 —
  add to the denominator)
- Any redemption below your program's cash-out floor (see rule
  above)

## Expiry & devaluation pressure model

The script's `--expiring-days` flag shifts verdicts:

- Expiring ≤ 90 days and best plan CPP ≥ weak band: BURN anyway
  (value decays to zero at the wall)
- Devaluation announced (chart change dated): treat affected
  awards as expiring on that date
- Transferable points (UR/MR/TYP): no expiry — pure HOARD is
  safe; use them as the parking lot when airline charts wobble

## Family-of-four planning notes

- Award space for 4 seats is rarer than for 2 — airlines release
  1–2 seats per flight at the low level. Search tools show it;
  plan A/B routings.
- The math doesn't change: compute per-seat CPP, then total.
- One adult + kids on points while partner flies cash is a
  legitimate mixed solution — rank it as its own "option."

## Escalation path when nothing prices well

1. Check 5 transfer partners, not 1 — same seats, different
   charts (script's `sweet-spots` table lists who prices what)
2. Shift dates ±3 days — award space is lumpy
3. Check nearby airports (SFO/SJC/OAK pricing differs wildly)
4. If still bad: pay cash, keep points. Points at rest in a
   transferable program lose nothing.
