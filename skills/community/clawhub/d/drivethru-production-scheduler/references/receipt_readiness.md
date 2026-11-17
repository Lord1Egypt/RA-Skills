# Receipt readiness — knowing when a batch's goods are in

A production batch consumes bought-in components. As a rule of thumb it
shouldn't start before those are received — starting early strands the job, the
machine is committed but the blanks/parts aren't there. **This is guidance, not
a constraint the tools enforce.** The scheduling tools will set a start on a
not-yet-received batch; the readiness data below is what you reason with, and
the shop's real preferences are something you learn from feedback over time (and
should carry in memory), not a fixed rule.

## The signals

Every batch carries `is_fully_received` (a stored flag — all components on
hand). The `supply` picture (`production_batch_supply`, or the `supply` block on
`production_get_batch`) expands it:

| Field | Meaning |
| --- | --- |
| `is_fully_received` | True → every component is in; the batch can run. |
| `receipt_status` | `no_purchases` / `not_received` / `partially_received` / `fully_received`. |
| `expected_ready_date` | The **latest** expected arrival across the still-open receipts — i.e. the earliest date the *whole* batch is on hand. Usually the date to start on or after. |
| `has_unknown_eta` | An open receipt has no arrival signal — you can't compute a ready date; chase tracking/purchasing. |
| `blocked_on_receipt` | Shorthand for "not fully received". |

Where the dates come from: each open receipt's `expected_arrival` is its vendor
tracking `delivery_date` if known, else the picking's `scheduled_date`.
`expected_ready_date` is the max of those across the batch — the last item to
land gates the whole job.

## How to use it

There's no gate to satisfy and no override flag — just decide well:

- **Fully received** → free to schedule now (subject to a machine gap).
- **Known ETA in the future** → prefer to start on/after `expected_ready_date`,
  but you may slot it earlier if that's what the shop wants (e.g. a human said
  the goods land the morning of the run). Setting only a machine now and the
  start later is also fine.
- **Known ETA already past, still not received** → the receipt is late; the
  vendor tracking `status` (e.g. `bo` = backordered, `in_transit`) says why.
  Surface it — a purchasing/expediting problem more than a scheduling one.
- **Unknown ETA (`has_unknown_eta`)** → no receipt date at all. Flag it so
  tracking can be added rather than guessing a start.

## Learning the shop's real rules

The default "don't start before received" is a reasonable prior, but every shop
and decoration type has exceptions — some setup work can start early, some
vendors are reliable enough to schedule against an ETA, some batches must never
start before a specific component lands. **When a human corrects one of your
calls, remember it.** Those learned preferences are what should shape future
scheduling, layered on top of the readiness data — not a one-size rule baked
into the tools.

## Reading the underlying records

The `supply` payload already carries the feeding POs (`status_from_vendor`,
`tracking_ids`) and receipts (`state`, `scheduled_date`, `vendor_tracking`). For
any other field on `purchase.order`, `stock.picking`, or `vendor.tracking`, use
`mfg_read`.
