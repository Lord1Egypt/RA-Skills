# Running as a Drive Thru routine

A **routine** is a scheduled prompt configured in Odoo (Drive Thru → Routines):
a user picks an agent (you), sets a frequency, and writes a prompt. On each
firing the Odoo module:

1. opens a **fresh platform conversation** with you — so every run starts with a
   clean context and doesn't drag along history (no wasted tokens);
2. sends your prompt, prefixed with a fenced **`[Scheduled routine]`** block
   naming the routine and the recipient's Odoo `user_id`;
3. posts your reply into a **new Discuss channel** that includes the recipient,
   authored by the agent contact — a self-contained report thread;
4. leaves that thread wired to this conversation, so if the recipient **replies**
   in it, their message comes back to you on the **same** conversation and you
   continue with that run's full context.

So: a run is one-shot from your side (query → analyze → report), but the thread
stays alive for follow-up. Write the report so a human can act on it and reply.

## Writing the report

- **Lead with the exceptions.** The prompt defines what's worth attention (late,
  short, stuck, over a threshold). Put those first; don't bury them under a
  recap of everything that's fine.
- **If nothing's wrong, say so in one line.** "All 23 open POs are on track; none
  past expected arrival." Don't manufacture noise.
- **Name records concretely.** Include the PO/picking/product reference and the
  key number (days late, qty short, $ outstanding) so a reply like "chase the
  first two" is actionable and so the reader can open the record.
- **Be self-contained.** The reader has no prior turns in this thread — don't
  reference "the query above" or assume they saw the prompt.
- **Quantify with `ops_aggregate` when it helps.** "$48k across 12 POs, worst is
  P00318 (14 days late)" reads better than a raw list.
- **Respect permissions.** For any SOP/policy lookup, call the `knowledge_*`
  tools with the `user_id` from the `[Scheduled routine]` block.

## Common sweep recipes

| Routine intent | Approach |
| --- | --- |
| Late POs | `ops_search purchase.order` — `state=purchase`, `date_planned < today`, `receipt_status != full`. Report worst-first by days late; total outstanding value with `ops_aggregate` grouped by vendor. |
| Stuck receipts | `ops_search stock.picking` — `picking_type_code=incoming`, `state not in [done,cancel]`, `scheduled_date < today`. |
| Deliveries missing tracking | `ops_search stock.picking` — `picking_type_code=outgoing`, `state=assigned`, `carrier_tracking_ref unset`. |
| Low stock / shortages | `replenish_run_report` (curated shortage lines with vendor/qty), or `ops_search stock.warehouse.orderpoint` for the raw rules. |
| Open PO spend by vendor | `ops_aggregate purchase.order` — `state=purchase`, group by `partner_id`, sum `amount_total`. |

See [`query_patterns.md`](query_patterns.md) for the exact filter JSON. Keep the
routine's *own* prompt as the source of truth for what counts as "worth
reporting" — these are just the mechanics.
