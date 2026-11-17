# Production scheduling (MRP) data model

The production actions in `scripts/production.py` map the
`/agent_api/v1/production/*` surface of the Production Scheduling Agent
Integration Schematic.

## Entities

| Entity                   | Odoo model              | Meaning                                            |
| ------------------------ | ----------------------- | -------------------------------------------------- |
| **Production batch**     | `mrp.production.batch`  | A batch of MOs sharing a machine and time slot.    |
| **Workcenter**           | `mrp.workcenter`        | A machine, e.g. "Manual Press A".                  |
| **Production center**    | `production.center`     | An area grouping machines, e.g. "Screen Print Floor". |
| **Decoration method**    | `decoration.method`     | A process type, e.g. "Screen Print", "Embroidery". |

## The writable scheduling fields

Each batch is scheduled by writing any subset of:

| Field                     | Meaning                                              |
| ------------------------- | ---------------------------------------------------- |
| `sequence`                | **Run order** — the batch's rank in the queue, and the primary scheduling decision. Rank a whole queue with `production_set_run_order`. |
| `manual_sequence`         | A manufacturing manager pinned this batch by hand; agent `sequence` writes skip it. |
| `primary_workcenter_id`   | Machine assignment.                                  |
| `production_center_id`    | Derived from the workcenter if omitted.              |
| `date_planned_start`      | ISO 8601 (UTC). Optional — a refinement on the run order, not a substitute for it. |
| `date_planned_finished`   | Auto-computed from start + Σ MO `duration_expected` unless set explicitly. |

## Event dates only lead when they're near

An `event_date` that is late or within `event_horizon_days` (default 5) sets
`event_imminent` and outranks everything else in the queue. A **distant** event
date does not: past the horizon a batch is ordered by its *governing deadline*
— the earlier of its event and ship dates — so a far-off event gives way to a
sooner ship date instead of jumping the queue.

## Art readiness tiers the queue

`production_schedule_queue` does not rank on dates alone. A batch whose decals
aren't printed (`print_decals_status` = `no` / `partial` / `sample`) or whose
artwork isn't ready (`art_status` != `done`) can't run, so it is **deferred
below runnable work** — until it's due within `art_release_days` (default 3),
when `art_at_risk` flips true and it is **expedited to the top**.

A top-ranked batch with `art_ready: false` is a call to chase the art, not a
job to schedule; `art_blockers` names what's missing. The
`drivethru-production-scheduler` skill covers this in full.

The server applies writes in safe order: run order → `production_center_id` →
`primary_workcenter_id` (derives center if omitted) → `date_planned_start`
(auto-computes finish) → `date_planned_finished` (explicit value wins).

## Planning workflow

1. **`overview`** — one round-trip returning open `batches`, `workcenters`
   (each with `scheduled_batches` inlined showing current load),
   `production_centers`, `decoration_methods`, and `open_batch_total`. If
   `open_batch_total > len(batches)`, raise `batch_limit` or page.
2. **`get-batch`** — for each batch you intend to place. The detail payload adds:
   - `decorations[]` with `decoration_production_ready` flags
   - `sales_orders[]` with `commitment_date` / `event_date`
   - `orders[]` (manufacturing orders) with per-MO durations
   - `eligible_production_centers[]` — pre-filtered by capability
   - `eligible_workcenters[]` — pre-filtered, each with `scheduled_batches`
   - `batch_operations[]` — pre-production ops (e.g. "Burn Screens")
3. **`production_set_run_order`** — publish the ranking (ids in run order).
   This is the decision the floor works from; do it before, and independently
   of, any machine/slot placement.
4. **`schedule`** (single) or **`bulk-schedule`** (many) — write decisions.
   `bulk-schedule` with `atomic: true` (default) rolls back the whole request on
   any error; `atomic: false` applies what it can and reports per-entry errors.
5. **`plan`** (optional) — run Odoo's native `button_plan()` slot allocator on a
   batch. Requires `primary_workcenter_id` already set and the batch not
   done/cancel.

## Eligibility helpers (apply these when choosing a machine)

- A workcenter can run a decoration method if its `decoration_method_ids` is
  empty (no restriction) **or** contains the method id.
- A workcenter is schedulable only if `active` **and** `allow_production_batch`.
- A production center accepts a batch if `piece_count >= minimum_piece_count`
  and (its `decoration_method_ids` is empty **or** includes the batch's method).
- A batch has a pending "Burn Screens" operation when `is_screens_burned` is
  false and it has `decoration_method_ids`.

## Status flags worth surfacing

`is_late`, `is_scheduled_late`, `is_scheduled_close`, `art_status`,
`is_screens_burned`, `receipt_status`, plus `ship_date` / `event_date` for
deadline reasoning.
