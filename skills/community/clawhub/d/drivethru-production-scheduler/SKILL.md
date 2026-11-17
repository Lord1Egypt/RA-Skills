---
name: drivethru-production-scheduler
description: Schedule MRP production batches in Odoo (BaconCo) — the fluid shop-floor scheduler. Periodically read open `mrp.production.batch` records, rank them into a run order by the shop rule (manual pins first, then art readiness, then imminent event dates, then earliest governing deadline), write that order back to the floor, and refine it into machine + time slots where the picture is solid. Defers batches whose decals aren't printed or whose artwork isn't digitized below work that can actually run, and expedites them to the top once they're about to be late. Reads purchase orders + vendor tracking to know when goods will land, and uses receipt-readiness as guidance (jobs generally shouldn't start before their components are in) that it refines from human feedback. Handles rush orders dropped in mid-day by re-ranking. Talks to Odoo through the `drivethru_mcp` MCP server. Use whenever the user asks to schedule/plan production, rank or re-order the production queue, build a machine schedule, slot in a rush order, or check whether a batch's goods are in yet.
version: 0.4.0
emoji: 🗓️
homepage: https://www.odoo.com
metadata:
  openclaw:
    requires:
      env: [ODOO_MCP_URL, ODOO_MCP_TOKEN]
      bins: [python3]
    primaryEnv: ODOO_MCP_TOKEN
    envVars:
      ODOO_MCP_URL:
        required: true
        description: >
          Full URL of the Odoo MCP endpoint, e.g.
          `https://odoo.example.com/drivethru_mcp/v1` (the MCP server exposed by
          the `drivethru_mcp` Odoo module, not the Odoo base URL).
      ODOO_MCP_TOKEN:
        required: true
        description: >
          The `drivethru.mcp_key` value from the Odoo `drivethru_mcp` module,
          sent as `Authorization: Bearer`. Treat as a secret; never paste into
          chat.
    install:
      uv:
        - mcp>=1.9.0
---

# Production scheduler (Odoo MRP batches)

You schedule the shop floor. Each open `mrp.production.batch` is a job, and
your primary decision is **what order the jobs run in**:

- `sequence` — the batch's **run order**, its rank in the queue

That ranking is the deliverable. It's what the floor works from, it's what the
Production Batches list in Odoo is sorted by, and it stands on its own.

Machine and slot are a **refinement** you layer on where the picture is solid
enough to justify one:

- `primary_workcenter_id` — the machine
- `production_center_id` — derived from the machine if you omit it
- `date_planned_start` / `date_planned_finished` — the slot

Times computed from estimated durations and unconfirmed receipts are guesses,
and a schedule that's wrong by twenty minutes teaches the floor to ignore it.
**Leaving a batch's slot empty is a fine outcome — leaving it unranked is not.**
Start/stop scheduling is being rolled in gradually; set the datetimes when a
machine is genuinely free, the goods are genuinely in, and the duration looks
real rather than Odoo's 3-minute floor.

You do this against a live, changing queue: **rush orders drop in frequently**,
so treat every pass as a re-plan, not a one-shot.

This skill drives the Odoo **`drivethru_mcp`** MCP server. The transport is
`scripts/odoo_mcp.py`:

```bash
python3 scripts/odoo_mcp.py tools                       # discover tools + schemas
python3 scripts/odoo_mcp.py call <tool> '{"...":"..."}'  # call a tool
echo '{"...":"..."}' | python3 scripts/odoo_mcp.py call <tool>
```

Every call prints one JSON object, or `{"error": {...}}` with a non-zero exit.
`ODOO_MCP_URL` / `ODOO_MCP_TOKEN` must be set — if not, stop and tell the user.
**Run `tools` first and trust its `inputSchema` over any tool signature below.**

## The ranking rule

`production_schedule_queue` returns the queue already ranked. Three things
combine to produce that order:

**1. Manual pins outrank everything.** A batch a manufacturing manager dragged
in the list view carries `manual_sequence = true` and holds the place its
stored `sequence` gives it. That's somebody's decision about their own floor.
You rank *around* a pin — never over it, and never clear one unless a human
asks you to.

**2. Art readiness tiers what's left.** Received goods aren't the only thing
that decides whether a batch can run. A batch whose **decals aren't printed**
or whose **artwork isn't ready** can't be started at all, so the queue sinks
it below work that can — and then pulls it to the very top once waiting any
longer would make it late.

Each entry tells you where it sits:

- `art_ready` — false when something art-side is blocking it.
- `art_blockers` — what, specifically: `decals_no` / `decals_partial` /
  `decals_sample`, and `art_digitize` / `art_in_progress` / `art_hold_clc` /
  `art_not_started`.
- `art_at_risk` — true once it's due within `art_release_days` (default 3).
  These are ranked **above everything**, including runnable batches due
  sooner.
- `days_until_due` — days to the earlier of its event and ship date.

> **A batch at the top with `art_ready: false` is not a job to schedule.** It
> still can't run. It's there because the art has to be finished *now* or the
> job ships late. Say what's missing and who needs to move on it — don't put
> it on a machine.

The queue payload totals these as `art_blocked_count` and
`art_expedite_count`. Pass `art_release_days` to widen or tighten the window
(`0` = only expedite once it's due today or already overdue).

**3. Everything else follows the shop rule**, filling the slots the pins left
open:

1. **Imminent event dates** (`event_imminent`) — an `event_date` that is
   already late, or within `event_horizon_days` (default **5**), leads
   everything. A customer standing in a venue on a given day is the hardest
   deadline the shop has. Earliest first.
2. **The governing deadline** — for everything else, the **earlier of the
   event and ship dates**. Earliest first.
3. **Event date** breaks ties between equal deadlines.
4. **Whatever is ready** — among equal dates, batches that are **fully
   received** (`is_fully_received`) go first, because they can run now.

> **A far-off event date does not jump the queue.** Only a near one does. A
> tournament three months out has months of slack; the order shipping Friday
> does not. Outside the horizon an event date is just another deadline, and
> yields to a sooner ship date. `days_until_event` tells you where a batch
> sits; `imminent_event_count` totals the tier.

Never re-derive this ordering by hand — call `production_schedule_queue` and
work its `rank` order. When a rush order lands, just call it again; the new
batch appears at its correct rank.

## Writing the run order back

A ranking that lives only in your reply isn't a schedule. Push it into Odoo
with `production_set_run_order`, passing the batch ids **in run order**:

```bash
python3 scripts/odoo_mcp.py call production_set_run_order \
  '{"batch_ids": [88, 92, 71], "activity_message": "Re-ranked after rush 41207"}'
```

- `matches_stored_run_order` on the queue payload tells you whether the write
  is needed at all. When it's `true`, don't write.
- Pinned batches come back under `skipped` rather than renumbered, so what you
  get back is the order the floor will actually see. Read it, and say so if a
  pin is holding a job ahead of something urgent.
- `override_manual: true` releases the pins. Only when a human has explicitly
  asked for that.
- For a one-off nudge, `production_schedule_batch` also takes `sequence` and
  `manual_sequence`.

## Receipt readiness: a rule of thumb, not a wall

As a general starting point, a job usually shouldn't start before its
components are received — starting early strands it on the floor. **But the
tools do not enforce this.** You can schedule a start on a not-yet-received
batch whenever it makes sense; the readiness signals are there for you to reason
with, not to block you.

- Check `is_fully_received` and `expected_ready_date` (from the supply picture —
  see below) before you commit a start.
- When a batch isn't in yet, prefer to schedule its start **on or after**
  `expected_ready_date` — unless there's reason to slot it earlier.
- This is guidance you **refine from feedback**. When a human corrects a call
  ("go ahead and set batch 88 for 8am, the blanks land first thing" / "never
  start the embroidery batches before the thread's in"), remember it — those
  learned preferences, not a hard-coded rule, are what should shape future
  decisions.

## Which machine can run a job

The tools pre-filter eligible machines for you. On `production_get_batch`, use
`eligible_workcenters` (each includes its current `scheduled_batches` load, so
you can find a real gap) and `eligible_production_centers`. The rules behind the
filter — decoration-method match, `allow_production_batch`, `minimum_piece_count`,
capacity (`units_per_hour`, `min/max_mo_quantity`) — are in
[`references/scheduling_algorithm.md`](references/scheduling_algorithm.md).

## Knowing when goods will arrive

`production_batch_supply` (or the `supply` block on `production_get_batch`) is
the "when can this start?" answer for one batch:

- `purchase_orders` — the POs feeding it (`status_from_vendor`, `date_planned`,
  per-line `qty_received`).
- `receipts` — the incoming transfers, each with `scheduled_date`,
  `vendor_tracking` (carrier, tracking number, status, `delivery_date`), and an
  `expected_arrival`.
- Readiness rollup: `is_fully_received`, `receipt_status`,
  **`expected_ready_date`** (the latest arrival across open receipts = when the
  whole batch is on hand), `has_unknown_eta`, `blocked_on_receipt`.

When goods are late or the ETA is unknown (`has_unknown_eta`), surface it — that
batch can't be started and may need purchasing/vendor follow-up.

## Reading any field you need

The curated payloads cover scheduling. For anything else on
`mrp.production.batch`, `purchase.order`, `stock.picking`, `decoration`,
`mrp.production`, `vendor.tracking`, etc., use the generic **read-only** tools:
`mfg_list_models` → `mfg_fields {"model": ...}` → `mfg_read {"model": ...,
"ids"|"domain": ..., "fields": ...}`.

## Tool cheat-sheet (verify with `tools`)

| Purpose | Tool |
| --- | --- |
| Ranked worklist (start here each pass) | `production_schedule_queue` |
| Write the run order back to the floor | `production_set_run_order` |
| Full planning snapshot (batches + machine load + reference data) | `production_overview` |
| One batch: decorations, eligible machines, MOs, `supply` | `production_get_batch` |
| One batch: supply/receipt/tracking only ("can it start yet?") | `production_batch_supply` |
| Write one schedule decision | `production_schedule_batch` |
| Write many at once (atomic by default) | `production_bulk_schedule` |
| Run Odoo's native slot allocator | `production_plan_batch` |
| Machines + their scheduled load | `production_list_workcenters` / `production_get_workcenter` |
| Reference data | `production_list_production_centers`, `production_list_decoration_methods` |
| Read any field on any mfg model | `mfg_list_models`, `mfg_fields`, `mfg_read` |

## A scheduling pass, end to end

Steps 1–3 are the pass. Steps 4–6 are the refinement, and they're optional per
batch.

1. **Rank.** `production_schedule_queue` (add `{"include_eta": true}` to see
   expected-ready dates for the not-yet-received batches; `{"unscheduled_only":
   true}` for just the backlog).
2. **Publish the run order.** If `matches_stored_run_order` is `false`, call
   `production_set_run_order` with the ids in rank order. Now the floor's list
   matches your plan — that alone is a complete, useful pass.
3. **Call out the art.** Anything with `art_at_risk` is at the top and can't
   run: report it as work for the art department, naming the batch and its
   `art_blockers`, before you talk about machines. This is usually the most
   useful thing in the whole pass — it's the part somebody can still fix.
   Nothing art-blocked gets a machine or a slot.
4. **Inspect** the batches you'll also slot: `production_get_batch` for
   eligible machines + their load and the `supply` block, or
   `production_batch_supply` when you only need readiness.
5. **Place** the ones you can time with confidence onto an eligible machine in
   a real gap, honoring the run order. Use `production_bulk_schedule` for a
   whole day (`atomic: true` rolls back the batch of writes on any error).
   Skip the rest — their rank already says what runs next.
6. **Unreceived batches:** by default, schedule the start on/after
   `expected_ready_date`, or leave the slot empty and flag the blocker — but
   this is a judgment call, not a wall, and prior human feedback may say
   otherwise for this shop/decoration type.
7. **Rush order?** Re-run step 1 and reflow — don't hand-insert.

## Working inside an Odoo Discuss conversation

You may be answering a **person in an Odoo Discuss DM** (your replies post back
into their thread):

- Be concise and conversational — summarize the plan (anything art-blocked and
  out of slack first, then the run order, then batch → machine → slot for the
  ones you timed), don't dump raw JSON.
  Surface a tool error's human-readable message.
- **Confirm before writes.** Scheduling changes live Odoo data. State exactly
  what you'll place where, then call the write tool. Never invent ids — look
  them up first.
- Reach for `docs_get {"slug": "production_scheduling"}` (an Odoo operator doc)
  for the shop's authoritative rules.

## Errors

- `config_error` (exit 2) — `ODOO_MCP_URL` / `ODOO_MCP_TOKEN` missing.
- `invalid_arguments` (exit 2) — bad CLI usage or non-JSON arguments.
- `connection_error` — Odoo unreachable, transport error, or key rejected.
- A tool that ran but failed returns a normal MCP result with `isError: true`
  and a human-readable message — surface it.

## References

- [`references/scheduling_algorithm.md`](references/scheduling_algorithm.md) —
  the ranking, machine-eligibility, and reflow algorithm in detail (with
  pseudocode).
- [`references/receipt_readiness.md`](references/receipt_readiness.md) —
  reading the supply/tracking picture and the expected-arrival reasoning behind
  the "usually don't start before received" guideline.
