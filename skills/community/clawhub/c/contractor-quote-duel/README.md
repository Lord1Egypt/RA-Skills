# Contractor Quote Duel

Three quotes for "the same" project are rarely the same project. This
skill builds the comparison mechanics homeowners skip because they're
tedious: scope matrix, unit-price sanity, payment risk, and the
clarification emails that make bids comparable.

## The Real Problem

Home renovation is a ~$450B/year US market; the median homeowner project
runs $5-25k, and the standard advice — "get three quotes" — ends at
comparing totals. Totals lie: one roof bid includes gutters and
skylight flashing, another excludes tear-off disposal, a third is 40%
cheaper because half the scope is missing. Lowball-and-change-order is
the #1 complaint pattern at state contractor boards. And payment
mechanics (50% deposits, 100% pre-completion) turn a bad pick into a
months-long ordeal.

## What It Does

- **matrix** — scope union × bidder grid; every MISSING cell is a future
  change order; per-trade documentation checklist (ice/water shield,
  load calc, waterproofing spec...)
- **pricecheck** — unit prices vs ballpark bands; flags padding (>1.6×)
  and lowball (<0.5×)
- **risk** — deposit/payment-schedule scoring: LOW/MEDIUM/HIGH with the
  specific reasons
- **letter** — scope-gap clarification email per bidder, listing what
  competitors included
- **references/** — trade scope checklists, allowance traps, lowball
  catalog, dispute-surviving contract clauses

## Quick Start

```bash
python3 scripts/quote_duel.py --quotes-json "$Q" matrix
python3 scripts/quote_duel.py --quotes-json "$Q" pricecheck
python3 scripts/quote_duel.py --quotes-json "$Q" risk
python3 scripts/quote_duel.py --quotes-json "$Q" letter --bidder "Alpha Roofing"
```

Quotes JSON: `{"bidder","total","deposit_pct","insured","items":[{"item","price","qty"}],"docs":[...]}`

Stdlib only, offline. Decision support — bands are order-of-magnitude
US averages, not local quotes.

## License

MIT © Denis Voronin
