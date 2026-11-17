# Lessons learned — order entry

A running, **timestamped** log for things the agent learns about BaconCo's
order-entry *process* (not customer-specific — those go into the customer's
Internal Notes via `sales_add_customer_note`). Append a dated entry whenever you
discover a rule, a gotcha, or a better sequence. Newest at the top. Keep entries
short and factual; link the order/PR if useful.

Format:

```
## YYYY-MM-DD — short title
- what happened / what was learned
- the rule going forward
```

<!-- Append below. Example:

## 2026-07-14 — Preview must precede Submit for grid-decorated orders
- Confirmed an order where a decorated column's line was still a vendor_item;
  no MO was created and the blank almost shipped undecorated.
- Rule: always run `sales_preview_order` after grid entry and before submit;
  the `end_items_constructed` checklist item catches this.
-->

## 2026-07-12 — Skill created
- Initial `drivethru-odoo-sales-assistant` skill + `sales_*` entry tools shipped.
- The pre-submission checklist is seeded from Odoo's confirm gates; we tune it
  together as we test (see `pre_submission_checklist.md`).
