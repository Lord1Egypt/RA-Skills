---
name: amazon-inventory-action-plan
description: Turn Amazon inventory data into a prioritized operating plan for stockout recovery, restocking, inventory pacing, or overstock clearance. Use when a seller asks what to do about low stock, a recent stockout, inbound delays, excess FBA inventory, promotion capacity, or the tradeoff between sales velocity, advertising, margin, and cash recovery.
---

# Amazon Inventory Action Plan

Turn an inventory situation into clear operating decisions. Produce a scenario-based plan with review points, not an automatic purchase order, price change, promotion, or advertising change.

## Collect the operating snapshot

Ask one concise clarification when the marketplace, product, or decision is missing. Request only the inputs that can change the recommendation:

- marketplace and a product label, SKU, or ASIN;
- sellable, inbound, reserved, and unfulfillable units, without double-counting statuses;
- units sold over available 7-, 14-, and 30-day windows, with calendar days, in-stock days, and promotion or other distorted days identified separately;
- supplier lead-time range, inbound timing confidence, and any minimum order constraint;
- planned promotions or demand changes;
- current operating goal: restore sales, prevent a stockout, support growth, release cash, reduce storage exposure, or exit inventory;
- margin floor, cash limit, and any action the seller will not take.

Use redacted product labels when account identifiers are unnecessary. Treat every missing input as unknown, never zero.

## Diagnose the inventory state

Classify the situation by its operating constraint, not by a universal days-of-cover threshold:

1. **Stockout recovery** — inventory recently returned or is about to return after lost availability.
2. **Tight inventory** — likely demand can consume usable stock before reliable replenishment arrives.
3. **Working inventory** — stock can support the current plan with a reasonable monitoring buffer.
4. **Excess inventory** — expected sell-through conflicts with cash, storage, seasonality, or exit goals.

Show the math used to support the classification:

- calculate baseline daily sales as eligible units sold divided by eligible in-stock days, not total calendar days;
- exclude out-of-stock days from the baseline and keep promotion-distorted demand as a separate scenario;
- mark the baseline unknown or low-confidence when eligible in-stock days cannot be determined;
- calculate current availability cover as sellable units divided by the selected demand rate;
- exclude reserved, unfulfillable, uncertain inbound, and purchase plans from current availability cover;
- add confirmed inbound only from its expected sellable date and show it as a separate projected-coverage segment with timing confidence;
- calculate low, base, and high demand scenarios when history is volatile;
- compare the coverage range with the full replenishment window;
- distinguish arrival, receiving, and sellable dates instead of treating them as one event.

Do not turn a rough scenario into an exact reorder quantity. When lead time, demand variation, inbound reliability, or usable stock is missing, provide a risk warning and the data needed for a quantity decision.

## Build the action plan

Choose actions that match the diagnosed state:

- **Stockout recovery:** stabilize availability first, then restore previously proven traffic and demand sources in small steps. Do not treat a returning product as a new launch or assume its prior rank will return.
- **Tight inventory:** protect high-intent and economically defensible demand, postpone expansion tests, and define a trigger for further pacing. Present price, promotion, or advertising changes as options requiring approval.
- **Working inventory:** maintain the current operating plan, set an early-warning checkpoint, and test growth only within the replenishment buffer.
- **Excess inventory:** define the cash-recovery goal, margin floor, storage pressure, and decision deadline before comparing clearance options. Separate short-term clearance traffic from the product's normal demand baseline.

Connect inventory and demand decisions. A promotion or advertising increase is not a standalone action when stock cannot support the added demand. A clearance plan is not successful merely because advertising efficiency improves; include cash recovered, units cleared, remaining exposure, and margin impact.

## Output format

```markdown
# Inventory action plan | {product} | {marketplace}

## Operating decision
- Inventory state:
- Primary goal:
- Confidence:
- Most urgent risk:

## Inventory math and assumptions
| Input or calculation | Value or range | Period/source | Caveat |
| --- | --- | --- | --- |

## Scenario outlook
| Scenario | Demand assumption | Coverage or risk window | Operating implication |
| --- | --- | --- | --- |

## Prioritized actions
| Priority | Action | Why now | Guardrail | Review signal/date |
| --- | --- | --- | --- | --- |

## Demand and advertising coordination
- Preserve:
- Reduce or postpone:
- Test only if:

## Reorder or clearance checkpoints
- Continue signal:
- Escalation signal:
- Stop signal:

## Unknowns and approvals
- …
```

## Operating boundaries

- Do not access or change Seller Central, advertising, pricing, promotion, ordering, or fulfillment systems.
- Do not present a suggested order quantity, bid, budget, discount, or price as an approved action.
- Do not mix marketplaces, currencies, warehouses, fulfillment modes, or time windows without labeling them separately.
- Treat FBA limits, fees, promotion rules, and platform policies as time-sensitive; verify them in the current official account interface or documentation before action.
- Do not infer supplier reliability, unit economics, seasonality, or future demand from missing evidence.
- Require human review before purchase commitments, liquidation, disposal, pricing, promotion, advertising, tax, compliance, or account changes.

## Project

This standalone Skill is maintained by [AMZ Helper](https://amzhelper.com).
