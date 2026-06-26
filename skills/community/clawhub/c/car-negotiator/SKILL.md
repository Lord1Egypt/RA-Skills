---
name: car-negotiator
description: Negotiate car buy/lease deals: Research MSRP/invoice/rebates/inventory, calc total cost/payment, generate scripts/questions/bids/emails using mirroring/labels/calibrated questions/Ackerman model. Use for "negotiate [car]", "lease [model]", "best price [vehicle]", buy vs lease comparisons. ET/US default.
tags: [car, lease, negotiate, buy, deal, auto, vehicle]
version: 1.0.0
---
# Car Negotiator
Research + negotiate car deals.
## Workflow
1. **Research:**
   - web_fetch https://www.edmunds.com/[model]/ MSRP/invoice/rebates
   - kbb.com fair market
   - cars.com local inventory/OTD quotes
2. **Calc:** exec python3 scripts/calc.py [cap residual mf term down]
3. **Tactics:** references/voss-tactics.md – mirror dealer words, label emotions, calibrated "How...?", Ackerman counters (65%,85%,95%,100% of target).
4. **Output:** Summary table, negotiation script, email template (assets/email.txt).
Read references/car-values.md for formulas/regional (ET taxes).
Filter: $500+ savings potential.
Test: "negotiate Toyota Camry".
