# calendar-extractor — route contract (for the javis-server team)

This document specifies the interface the **javis-server session-dispatcher**
control-plane must satisfy so the dispatcher can route agenda deliverables to the
`calendar-extractor` skill. It is the contract only — no javis-server code is
implemented in this repo.

See the design spec:
`docs/superpowers/specs/2026-06-08-calendar-extractor-dispatcher-adaptation-design.md`
(sections 3a–3c) and the dispatcher spec it adapts to
(javis-server `docs/superpowers/specs/2026-06-06-session-dispatcher-server-variant.md`,
implemented in `app/services/dispatcher_service.py`).

The same contract is declared, discoverably, in the skill's `SKILL.md`
`metadata.routes` block. That static block declares the skill-owned fields
(`route_id`, `skill`, `matches`, `args_template`, `risk`); `enabled` is omitted
there because it is per-user runtime state the server owns, not skill metadata.

## 3a. RouteRegistry row

Seed this row per user, enabling it when the user enables `calendar-extractor`:

| column | value |
|---|---|
| `route_id` | `"calendar"` |
| `skill` | `"calendar-extractor"` |
| `matches` | `"meetings, appointments, events, agenda, scheduling, dates/times mentioned"` |
| `args_template` | `null` (the unit + the prepended SKILL.md carry everything the skill needs) |
| `risk` | `"low"` (read-only transcript extraction + a push; no destructive side effects) |
| `enabled` | set `true` when the user enables calendar-extractor; `false`/absent otherwise |

The dispatcher only routes a deliverable to this skill when an **enabled** row with
`route_id="calendar"` exists for that user. No enabled row → the skill is never
scheduled.

## 3b. `classify_and_route` deliverable shape

Feed the user's enabled route catalog (each row's `route_id` + `matches`) into the
`classify_and_route` task prompt. For a transcript containing scheduling content,
the classifier must emit a deliverable shaped like:

```json
{
  "id": "<uuid>",
  "title": "Extract calendar events",
  "description": "<short summary of the agenda found>",
  "route_id": "calendar",
  "confidence": 0.0
}
```

- `route_id` MUST be exactly `"calendar"` so it matches the RouteRegistry row.
- No scheduling content in the transcript → **no** `calendar` deliverable → no
  proposal card. (This is the correct, silent outcome.)

The dispatcher then matches the deliverable's `route_id` against the enabled
`RouteRegistry` row, persists a `DispatchProposal`, and pushes a proposal card to
iOS. On the user's Approve, it claims run-once
(`DispatchRouteExecuted (user, unit, route)` via a unique constraint, before
scheduling) and triggers the skill.

## 3c. Prompt contract

The skill relies only on the `<unit>` being present and `_UNIT_RE`-valid in the run
prompt — which the generic dispatcher prompt already provides:

```
Run /calendar-extractor for <unit>. Deliverable: <title>. <description>
Fetch that unit's transcript, produce the deliverable, and push the result.
```

- `<unit>` is `audio:<session_id>` or `kbd:<keyboard_input.id>`. The skill parses it
  and runs `fetch --session <session_id>` or `fetch --kbd-input <keyboard_input.id>`.
- **No calendar-specific prompt enrichment is required.** `args_template` stays
  `null` and `_deliverable_prompt` needs no calendar-specific change.
- All date-resolution discipline rides in (1) the relative-date **anchor** the
  `fetch` payload emits on every path
  (`reference_time` / `reference_date` / `reference_weekday` / `reference_time_utc`
  + `tz`) and (2) the **prepended SKILL.md** instructions. The server need not
  enrich the prompt to preserve date correctness.

## Idempotency ownership

The skill **does not** self-gate per unit. Run-once is owned entirely by the server:

- the human approval gate (a proposal must be approved before the skill runs), and
- `DispatchRouteExecuted (user, unit, route)` claimed via a unique constraint
  **before** scheduling (closes the TOCTOU window).

The skill keeps only an **event-level** `seen` map so the same event is never
delivered twice across overlapping manual 24h windows or a re-run. It is safe to
invoke the skill more than once: `seen` prevents duplicate delivery and the server
prevents duplicate invocation.

## Open items for the server team

- Seed/enable the `RouteRegistry` row for `calendar` when a user enables
  calendar-extractor.
- Feed the enabled route catalog (`route_id` + `matches`) into the
  `classify_and_route` task prompt.
