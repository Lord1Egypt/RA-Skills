# Scheduling algorithm

The data model and the algorithm behind a scheduling pass. The Odoo
`drivethru_mcp` tools do the heavy lifting (ranking, machine eligibility,
receipt readiness) server-side; this is the reasoning you layer on top.

## Entities

| Entity | Odoo model | Meaning |
| --- | --- | --- |
| Production batch | `mrp.production.batch` | The scheduling unit — a batch of MOs sharing a machine + slot. |
| Manufacturing order | `mrp.production` | One order inside a batch. |
| Workcenter | `mrp.workcenter` | A machine (e.g. "Manual Press A"). |
| Production center | `production.center` | A group of workcenters (e.g. "Screen Print Floor"). |
| Decoration | `decoration` | An imprint on a product, carrying artwork/readiness. |
| Decoration method | `decoration_method` | A process type (Screen Print, Embroidery, DTF, Heat Press). |
| Purchase order | `purchase.order` | A vendor order for the batch's components. |
| Receipt | `stock.picking` (incoming) | Goods arriving for the batch. |
| Vendor tracking | `vendor.tracking` | Carrier / tracking number / status / delivery date. |

## The writable scheduling fields

| Field | Notes |
| --- | --- |
| `sequence` | **The run order** — the batch's rank in the queue. The primary decision. Written across a whole queue by `production_set_run_order`. |
| `manual_sequence` | Pins a batch against re-ranking. Set when a manufacturing manager drags the list view. Your `sequence` writes skip pinned batches. |
| `primary_workcenter_id` | The machine. Must be eligible (see below). |
| `production_center_id` | Derived from the machine if omitted. |
| `date_planned_start` | ISO datetime. Not gated — mind receipt readiness (see `receipt_readiness.md`). Optional: only set it when you can justify it. |
| `date_planned_finished` | Auto-computed as `start + Σ MO.duration_expected` unless set explicitly. |

## Run-order ranking

`production_schedule_queue` returns open batches already ranked. The ranking
combines three things: pins, then art readiness, then the shop rule.

**Pins.** A batch a manufacturing manager dragged in the list view carries
`manual_sequence = true`, and holds the slot its stored `sequence` gives it.
Their call outranks the rule — you rank *around* a pin, never over it.

**Art readiness** tiers everything else before any date is looked at. Two
things gate it, either of which stops the job:

| Signal | Blocked when | Means |
| --- | --- | --- |
| `print_decals_status` | `no`, `partial`, `sample` | The DTF / Heat Press decals aren't printed. `na` = this batch prints none. |
| `art_status` | anything but `done` | Digitizing outstanding, art still in progress, or a CLC licensing hold. |

The tier is then:

```
tier(batch) =
    0  if not art_ready and art_at_risk    # expedite — top of the queue
    1  if art_ready                        # runnable — the normal case
    2  if not art_ready                    # deferred — below runnable work
```

`art_at_risk` is true once `days_until_due` (days to the earlier of the event
and ship dates) is `<= art_release_days`, default **3**. So art-blocked work
sinks below work that can actually run, and stays there until deferring it
further is what would make it late — then it goes to the very top, ahead of
everything.

**Everything else** sorts by the shop rule within its tier, filling the slots
the pins left open. The full sort key is:

```
key(batch) = (
    tier(batch),                       # 0. art readiness (above)
    0 if event_imminent else 1,        # 1. near/late event dates lead
    min(event_date, ship_date),        # 2. governing deadline, earliest first
    event_date or FAR_FUTURE,          # 3. event date breaks ties
    0 if is_fully_received else 1,     # 4. ready jobs first
    id,                                # stable tiebreak
)
```

`event_imminent` is true when `days_until_event <= event_horizon_days`
(default **5**) — which includes a late event date, since that day count goes
negative.

So: art readiness tiers the queue; within a tier a **near or late event date**
leads; everything else is ordered by its **governing deadline**, the earlier of
its event and ship dates; event date breaks ties; among identical dates, the
batch whose goods are in gets the slot. Undated batches sink to the bottom of
their tier — and an art-blocked batch with no dates at all can never be at
risk, so it stays deferred until it gets a date or its art is finished. Work
the returned `rank` order.

**Why the governing deadline and not the event date.** An event date used to
outrank every batch that didn't have one, however far out it was, so a
tournament in three months sorted ahead of an order shipping Friday. An event
date now earns the top tier by being *near*; past the horizon it is ordered
like any other deadline and gives way to a sooner ship date. Since a batch
usually ships before its event, `min(event, ship)` is normally the ship date —
which is exactly the date the floor has to hit.

**A tier-0 batch is not a job to schedule.** It's at the top because its art
has to be finished now, not because it can run. Report it — `art_blockers`
names what's missing — and leave it off the machines.

A stored `sequence` on a batch that is *not* pinned is just the last pass's
output — it does not fight the rule, or a rush order could never move up.

Rush handling falls out of this for free: a rush batch with a near event or
ship date re-ranks to the top the next time you call
`production_schedule_queue`. Never hand-insert a rush job into a stale plan —
re-rank and reflow.

## Writing the ranking back

A ranking that only exists in your reply isn't a schedule. Push it to Odoo so
the floor's Production Batches list is in the order you decided:

```
queue = call("production_schedule_queue", {})
if not queue["matches_stored_run_order"]:
    call("production_set_run_order", {
        "batch_ids": [b["id"] for b in queue["queue"]],   # already in rank order
        "activity_message": "Re-ranked after rush 41207",
    })
```

- Pinned batches come back under `skipped` rather than renumbered — so the
  order you get back is the order the floor will see. Read it.
- `override_manual: true` clears that protection. Only when a human has
  actually asked for the pins to be released — never on your own initiative.
- `matches_stored_run_order` is the "is this write needed?" flag. When it's
  `true`, don't write.

## Machine eligibility

A batch may only be assigned a machine that can actually run its work.
`production_get_batch` pre-computes `eligible_workcenters` and
`eligible_production_centers`, but the rules are:

- The batch's methods = its `decoration_ids` → `decoration_method`.
- A **production center** is eligible when its `decoration_method_ids` overlaps
  the batch's methods **and** `minimum_piece_count <= batch.piece_count`.
- A **workcenter** is an eligible `primary_workcenter_id` when it is `active`,
  `allow_production_batch = true`, its `decoration_method_ids` overlaps the
  batch's methods, and it belongs to an eligible production center.
- Respect capacity: `units_per_hour`, `min_mo_quantity`, `max_mo_quantity` on
  the workcenter; the batch's `calculated_duration` (minutes); and the machine's
  current `scheduled_batches` (inlined on the workcenter payloads) so you slot
  into a real gap rather than double-booking.

Also worth checking before committing a start: `art_ready` / `art_blockers`
(decals printed and artwork digitized? — already tiered into the rank, but
never give a blocked batch a slot), `is_screens_burned` (screens ready?),
`licensing_hold` (CLC approval pending?). A batch that's blocked upstream
shouldn't jump the queue onto a machine.

## A pass in pseudocode

Ranking first, and it stands on its own. Machine + slot is the refinement
you layer on for the batches you can actually time.

```
result = call("production_schedule_queue", {"include_eta": true})
queue = result["queue"]                   # already in run-order rank

# 1. Publish the run order. This alone is a complete, useful pass.
if not result["matches_stored_run_order"]:
    call("production_set_run_order", {"batch_ids": [b["id"] for b in queue]})

# 2. Report the art blocks. These rank at the top and cannot be started —
#    they are work for the art department, not for a machine.
for batch in queue:
    if not batch["art_ready"]:
        report_art_block(batch, batch["art_blockers"],
                         urgent=batch["art_at_risk"])

# 3. Refine into slots where the picture is solid enough to justify one.
for batch in queue:                       # already in priority rank
    if not batch["art_ready"]:
        continue                          # can't run: no machine, no slot
    if not batch["is_fully_received"]:
        # Goods aren't all in yet. Default: start on/after the ETA — but this
        # is judgment (and learned shop preferences), not a hard block.
        if batch.get("expected_ready_date"):
            target_start = max(now, batch["expected_ready_date"])
            # (only place it now if you also have a machine gap then)
        else:
            flag_blocked(batch)            # unknown ETA — chase purchasing
            continue

    detail = call("production_get_batch", {"batch_id": batch["id"]})
    machine = pick_machine(detail["eligible_workcenters"])  # capacity + open gap
    if machine is None:
        flag_no_capacity(batch)
        continue

    slot = first_open_gap(machine, duration=detail["calculated_duration_minutes"])
    plan.append({
        "batch_id": batch["id"],
        "primary_workcenter_id": machine["id"],
        "date_planned_start": slot.start,
    })

call("production_bulk_schedule", {"atomic": true, "updates": plan})
```

`pick_machine` / `first_open_gap` are your judgment calls over the pre-filtered
candidates and their `scheduled_batches`. Keep the batch of writes atomic so a
single rejection doesn't leave a half-applied day.

Skipping step 3 for a batch is a legitimate outcome, not a failure: its rank
already says what runs next. A start time you can't justify is worse than no
start time, because the floor learns to ignore the ones you can.

## After writing

- `production_bulk_schedule` returns `results` (with `changes_applied`) and, in
  non-atomic mode, per-entry `errors`. Read them back.
- Optionally run `production_plan_batch` to let Odoo's native slot allocator
  finalize workorder timing (requires `primary_workcenter_id` already set).
- `is_scheduled_late` / `is_scheduled_close` on a batch tell you if the slot you
  chose still misses/nears the ship date — re-check after a reflow.
