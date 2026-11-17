# Batch mockup routine — fill in missing `mockup_image` on decoration requests

This is the workflow the **Mockup Artist Agent** runs on its schedule (a
Drivethru routine). No user is watching each run; the agent picks up every
decoration request assigned to **Zach Tucker** that still needs a mockup,
generates one for every request where both required inputs exist, and writes
it back to Odoo's `mockup_image` field. Requests that don't have the inputs
yet are left alone (a **skipped** verdict per request, not a failure).

The rendering itself is the same deterministic pipeline the interactive skill
uses — this doc only wraps it in a per-request loop and the
Odoo read/write plumbing. **Same rules still apply:** no model-generated
pixels, always self-review before writing back (see
[`self_review.md`](self_review.md)).

## What the routine does on each fire

1. **Find the work.** Search Odoo for open decoration requests assigned to
   Zach Tucker (see [Finding the queue](#1-finding-the-queue)).
2. **For each request, decide if it's actionable.** Skip anything that
   already has a `mockup_image`. For the rest, list the request's attachments
   and pick a **blank product image** and a **decoration image**. If either
   is missing, record `skipped: missing_inputs` and move on.
3. **Generate the mockup.** Download both images to a temp file, run
   `compose_mockup.py`, then run the mandatory self-review loop
   ([`self_review.md`](self_review.md)) — up to 3 attempts.
4. **Write it back.** Upload the reviewed PNG into the request's
   `mockup_image` binary field.
5. **Log an outcome per request** — `mockup_written`, `skipped:<reason>`, or
   `failed:<reason>` — plus a one-line summary of the run.

Requests remain in their current state; this routine only fills the mockup
field. Advancing state (e.g. `mark_ready`, `self_approve`) is out of scope
and stays a human decision.

## 1. Finding the queue

`decoration.request` isn't queryable through `ops_search`. Reach it through
`sale.order` instead — `sales_search_orders` accepts dotted paths across the
`decoration_request_ids` relation, so filter the orders that carry an open
request assigned to Zach:

```jsonc
sales_search_orders {
  filters: [
    { field: "decoration_request_ids.user_id.name", op: "ilike", value: "Zach Tucker" },
    { field: "decoration_request_ids.state",        op: "in",    value: ["created", "progress"] }
  ],
  fields: ["id", "name", "decoration_request_ids"],
  response_detail: "standard",
  limit: 100
}
```

That returns the parent orders and each order's `decoration_request_ids`.
For every request id in the union, fetch the request itself:

```jsonc
sales_get_decoration_request { request_id, response_detail: "full" }
```

The record you care about carries:

- `user_id` — assignee (confirm it's Zach; the order-level filter can pick up
  siblings on the same order).
- `state` — only work `created` or `progress`; leave `ready`/`sent`/
  `approved`/`revision`/`done`/`cancelled` alone.
- `mockup_image` — the destination binary field. **If it's already
  populated, skip.** (The routine is idempotent; do not overwrite existing
  mockups.)
- `partner_id`, `name` — for logging.

Cap the queue at a sane per-run number (start with 25). Better to run more
often than to blow the whole batch on one long-tail request.

## 2. Picking blank + decoration images from the request

A decoration request accumulates attachments through the OWL process/
requirement widget plus the chatter. `decoration_list_attachments` is the
one place that enumerates all of them:

```jsonc
decoration_list_attachments {
  model: "decoration.request",
  record_id: <request_id>,
  only_images: true,
  include_processes: true,
  include_data: false      // metadata only; fetch bytes only for the pair we pick
}
```

Each entry has a fetchable web URL and a source label. The heuristic for
which is which:

- **Blank product image.** Look for entries whose filename or process label
  mentions **blank / product / garment / style** or matches the request's
  `blank_style_number` / `blank_vendor`. It usually looks like a plain
  product photo on white.
- **Decoration image.** Look for entries labeled **art / logo / decoration
  / mockup source / customer art** (or the customer-uploaded process on the
  approval portal). It's the graphic the customer wants printed.

**When it's ambiguous — skip.** If you see two candidates for either role
and can't confidently pick, record `skipped: ambiguous_inputs` and move on;
a human will label them. **Don't guess and don't ask the user mid-run** —
the routine fires unattended.

**When either role has no candidate — skip.** Record
`skipped: missing_inputs` (which one) and move on. This is the *most common*
skip; expect it.

Fetch the bytes for the two picked attachments by GET on their `web_url`
(the CDN URL when offloaded) and save each to a temp file. Do **not** pull
them via `decoration_get_image` unless a URL is missing — the raw HTTP path
keeps the base64 out of the token stream.

## 3. Compose + self-review

Same as the interactive workflow. Pick a **placement** from the request:

- If the request or its linked `decoration_id` names a location (e.g.
  "Left Chest", "Full Front", "Back Yoke"), map it to the placement key
  (`left_chest`, `full_front`, `back_yoke`, …).
- If the request only lists the location on the process/requirement lines,
  read it from there.
- If nothing says, fall back to `full_front` and note it in the outcome.

If the blank photo shows a hoodie/tee/hat/mug, pass `--category` too;
otherwise omit and let the `_defaults` rules apply.

```bash
python3 scripts/compose_mockup.py \
    --blank /tmp/blank.jpg \
    --decoration /tmp/deco.png \
    --category <category-or-omit> \
    --placement <placement>
```

Then run the **[self-review loop](self_review.md)** — read the rendered PNG,
judge it, layer corrective deltas (`--width-delta-pct`, `--offset-x-pct`,
`--offset-y-pct`, `--rotate-deg`), re-compose. **Hard cap at 3 attempts;**
if attempt 3 still isn't great, keep the best one and log
`review_notes: <what's still off>` in the outcome. Never loop past 3, never
ping-pong a delta's sign.

Cleanup and background-removal helpers still apply if the decoration is
degraded / on a solid plate — same rules as
[Background removal](../SKILL.md#background-removal-flat-art-vs-photos) and
[Cleaning up degraded art](../SKILL.md#cleaning-up-degraded--ai-generated-art).
Use them when the source obviously needs it; skip them by default so a clean
PNG doesn't take the scenic route.

## 4. Writing the mockup back to Odoo

The `mockup_image` field is a stored, writable binary on
`decoration.request`. A mockup PNG is small (unlike a 300 DPI DTF file), so
the streaming split isn't needed. Use `decoration_set_image` directly:

```jsonc
decoration_set_image {
  model:       "decoration.request",
  record_id:   <request_id>,
  field:       "mockup_image",
  data_base64: "<base64 of the reviewed PNG>"
}
```

Read the reviewed PNG from disk, base64-encode it, and send it in one call.
Verify the tool's response reports the field written before logging
`mockup_written`.

**Do not** advance the request's state; that's a human decision.

**Do not** overwrite an existing `mockup_image`; the pre-check in step 2
already skipped populated requests.

## 5. Per-request outcome + run summary

Emit one outcome record per request the routine touched, so the run's
verdict is legible in the Routines page:

| Outcome | When |
|---|---|
| `mockup_written` | Compose + self-review passed and `decoration_set_image` succeeded. |
| `skipped:already_has_mockup` | `mockup_image` was already populated. |
| `skipped:missing_inputs` | No blank *or* no decoration attachment. |
| `skipped:ambiguous_inputs` | Multiple candidates for a role, no confident pick. |
| `failed:<reason>` | Compose/upload/HTTP error. Do not swallow the traceback — put it in the outcome so the human can see it. |

Then log a single **run summary**: `queue=<N>, written=<w>, skipped=<s>,
failed=<f>`. If the queue was empty, the whole run is a `nothing_to_do`
verdict — that's the desired steady state most of the time.

## Rules specific to this routine

- **Idempotent.** Never overwrite an existing `mockup_image`. A second run
  on the same request should either write once (first run had inputs) or
  skip forever (still missing).
- **Unattended.** No `AskUserQuestion`. Ambiguity → skip with a reason.
- **Bounded.** Cap the per-fire queue at 25 requests. Nothing else in this
  container is watching wall-clock.
- **Non-destructive.** The routine only writes the `mockup_image` binary.
  It does not change state, add chatter attachments, edit fields, or
  create/modify decorations.
- **Same eyes-on rule.** Even in batch mode, the self-review loop is
  required. A silent bad mockup is worse than a skipped one.

## The routine (paste into the Mockup Artist Agent's Routines page)

- **Name:** `Zach Tucker — fill missing mockups`
- **Schedule:** every hour on the :07 mark
  (cron `7 * * * *`, local time)
- **Per-day cap:** 24 (one per hour)
- **Prompt:**

  ```
  Fill in missing mockups for decoration requests assigned to Zach Tucker.
  Follow references/mockup_routine.md in the drivethru-graphic-artist skill:
  search sale.order for orders whose decoration_request_ids.user_id.name is
  "Zach Tucker" and whose state is in ["created","progress"]; for each
  request, skip if mockup_image is already set; otherwise pick a blank
  product image and a decoration image from decoration_list_attachments; if
  both exist, generate a mockup with compose_mockup.py, self-review up to 3
  attempts, and write the reviewed PNG back to mockup_image via
  decoration_set_image. Cap the queue at 25. Log one outcome per request
  (mockup_written / skipped:<reason> / failed:<reason>) plus a run summary.
  Never overwrite an existing mockup_image, never advance state, never ask
  a human — ambiguity is a skip.
  ```
