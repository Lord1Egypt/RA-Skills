---
name: contractor-quote-duel
description: Use when comparing 2-4 contractor bids for the same home project (roof, kitchen, HVAC, floors...) — builds the scope-x-bidder matrix exposing what each quote silently omits, sanity-checks unit prices against ballpark bands (catches both padding and lowball-then-change-order bids), scores deposit/payment-schedule risk (30% deposit norm, pre-completion exposure, insurance/licensing), checks quote documentation completeness per trade, and drafts the scope-gap clarification email per bidder.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [contractors, home-improvement, renovation, quotes, bids, scopes, consumer-protection]
---

# Contractor Quote Duel

Three quotes for "the same" roof project are rarely the same project. One
bids 1,900 sq ft of shingles and nothing else; one includes gutters and
skylight flashing; one is $4k cheaper because tear-off disposal is a
change order waiting to happen. Homeowners compare totals — the single
most misleading number in the stack — because building a scope matrix by
hand across PDFs is tedious. This skill does the comparison mechanics:
scope union, gap exposure, unit-price outliers, payment risk, and the
clarification emails that turn apples/oranges into a decision.

## When to Use

- 2-4 written quotes in hand for the same project, deciding who gets it
- One bid dramatically cheaper — is it efficient or incomplete?
- Deciding what to ask each bidder before signing anything
- Checking a quote's payment structure before handing over a deposit
- Change-order dispute later: was the item in the original scope?

**Don't use for:** new construction custom builds (different economics —
cost-plus vs fixed-price needs a contract review, not a comparison
matrix); storm-chaser door-knockers (walk away, don't analyze); anything
needing a structural engineer's stamp (get the engineer).

## The Method

1. **Extract quotes to JSON** (agent does this from PDFs/photos/text):
   bidder, total, deposit %, items (name/price/qty), docs promised,
   licensed/insured flags.
2. **`matrix`** — scope union × bidder grid; every "— MISSING" cell is
   a scope gap you'd discover as a change order. Plus documentation
   completeness per trade (roof quotes without ice/water shield specs,
   kitchens without permit responsibility, HVAC without load calc).
3. **`pricecheck`** — unit price = price/qty vs ballpark band per trade.
   > 1.6× band high = padding; < 0.5× band low = lowball — the classic
   change-order bait.
4. **`risk`** — deposit & payment-schedule exposure. Deposit >30%,
   nothing written, >60% due before completion, uninsured: LOW/MEDIUM/HIGH.
5. **`letter`** — scope-gap clarification email per bidder listing
   exactly what competitors included that they didn't, plus the four
   questions (payment schedule, timeline, permits, labor warranty).

```bash
Q='[{"bidder":"Alpha Roofing","total":9500,"deposit_pct":10,"insured":true,
"items":[{"item":"asphalt roof replacement","price":9500,"qty":1900}],
"docs":["tear-off layers and disposal included"]},
{"bidder":"Beta Exteriors","total":14200,"deposit_pct":50,"insured":false,
"items":[{"item":"asphalt roof replacement","price":11800,"qty":1900},
{"item":"gutter replace","price":1200,"qty":80}],"docs":[]}]'

python3 scripts/quote_duel.py --quotes-json "$Q" matrix
python3 scripts/quote_duel.py --quotes-json "$Q" pricecheck
python3 scripts/quote_duel.py --quotes-json "$Q" risk
python3 scripts/quote_duel.py --quotes-json "$Q" letter --bidder "Alpha Roofing" --project "roof replacement"
```

## Decision Rules (from the outputs)

- Never decide on totals: decide on normalized scope + unit prices.
- A bid missing >30% of the union scope isn't cheaper — it's undefined.
  Get the gaps priced before comparing.
- Deposit >30% or >60% pre-completion is walk-risk; many US states cap
  deposits at 10-30% by trade.
- Cheapest bid + LOW unit-price flags = change-order farm. Budget
  total × 1.25 as the realistic number.
- Insurance/license unverified = stop. Verify before any money moves.

## Common Pitfalls

1. **Comparing totals across different scopes.** The matrix exists
   precisely because totals lie. Every MISSING cell must be priced or
   excluded in writing before a decision.
2. **Forgetting qty.** Unit-price checks need quantity (sq ft, linear
   ft, windows). A $9,500 roof bid without area can't be sanity-checked —
   ask for measurements.
3. **Trusting allowances.** "Allowance $1,500 for fixtures" is not a
   price. Convert allowances to spec-or-unit-price in the clarification
   letter.
4. **Ballpark bands as gospel.** Bands are US national order-of-magnitude;
   regional spread is 2×. Use flags to ask questions, not to accuse.
5. **Ignoring documentation gaps.** The docs checklist per trade is the
   cheapest dispute insurance: no ice/water shield spec on a roof quote
   is how you get felt-only under a $12k roof.
6. **Paying to a point of no leverage.** Final payment after punch list,
   always. A contractor with 100% of the money has zero incentive to
   return.
7. **Verbal "yes that's included."** If it isn't a line item after the
   clarification letter, it doesn't exist.

## Verification Checklist

- [ ] Every scope item in the union appears in the final contract of
      the winner (line items, not summaries)
- [ ] Unit-price outliers resolved in writing (spec'd or re-priced)
- [ ] Deposit <=30%, schedule written, final payment after punch list
- [ ] License + insurance verified with the state/insurer directly
- [ ] Permit responsibility named in the contract
- [ ] Change-order rule written: signed + priced before extra work

## References

- `references/trade-scope-checklists.md` — what a complete quote must
  contain per trade (roof/kitchen/bath/HVAC/electrical/structural),
  allowance traps, contract clauses that survive disputes, and the
  lowball-bid pattern catalog.
