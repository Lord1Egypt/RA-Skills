---
name: calendar-extractor
description: Extract calendar events from recent recording and keyboard transcripts and push them to your iOS chat as one markdown card per event, each landing in its own Agent Chat thread. Use on demand when the user asks for "today's meetings" / "calendar extract" / "今日会议" / "提取日历", and fetch the last 24 hours of transcript data by default. The javis-server session dispatcher also AUTO-RUNS this skill (no approve-to-run card) when a completed unit matches the calendar route, passing a deliverable hint in the run prompt that the agent may use alongside the transcript; extracted events are written PENDING and become solid only when the user taps Confirm in the iOS calendar table. If the user asks for "today's meetings", use the local day defined by the fetched reference_date field. Triggers: 'today's meetings', 'calendar extract', '今日会议', '提取日历'.
keywords: today's meetings, calendar extract, 今日会议, 提取日历, calendar-extractor
metadata:
  openclaw:
    runtime:
      node: ">=18"
  routes:
    - route_id: calendar
      skill: calendar-extractor
      matches: "meetings, appointments, events, agenda, scheduling, dates/times mentioned"
      args_template: null
      risk: low
---

# Calendar Extractor

> Extract calendar events from recent recording and keyboard transcripts and push them to your iOS chat — one markdown card per event, each landing in its own Agent Chat thread. Fetch the last 24 hours of transcript data by default. If the user asks for "today's meetings", use the local day defined by the fetched reference_date field. Generate one digest per local day in the user's timezone, containing all events that occur on reference_date and any events explicitly mentioned as happening today.

## When to use

- "today's meetings"
- "calendar extract"
- "今日会议"
- "提取日历"
- Automatically, when the javis-server session dispatcher **auto-runs** this skill after a completed unit matches the calendar route — no approve-to-run card (see "How this skill is invoked").

## Core commands

> **`<userId>` is optional.** Omit it and it defaults to `self`. Each HiJavis user
> runs in their own openclaw container, so `self` is correctly isolated; the gateway
> token (not the userId) authenticates every server call. No registration is needed
> to start — pass an explicit ID only if you run multiple profiles in one container.

```bash
# Step 1 — fetch recent transcripts as JSON (the agent extracts events from this)
node scripts/calendar-extractor.js fetch [--hours N] [--limit N]

# Step 1 (dispatcher run) — fetch ONE completed unit (the auto-run dispatcher unit)
node scripts/calendar-extractor.js fetch --session <sessionId> [--hours N]   # audio unit
node scripts/calendar-extractor.js fetch --kbd-input <inputId> [--hours N]   # keyboard unit

# Step 2 — push: pipe the extracted-events JSON array to stdin; dedups (seen) + delivers to iOS
echo '<events-json-array>' | node scripts/calendar-extractor.js push

# anchor — print the CURRENT relative-date anchor (resolve "today / 6 pm / tomorrow" on an edit turn)
node scripts/calendar-extractor.js anchor            # optional: --tz <IANA> for the card's calendar zone

# update — edit ONE pushed card in place (verbatim dedup_key, full merged patch, auto-confirm)
echo '{"dedup_key":"<verbatim>","patch":{...}}' | node scripts/calendar-extractor.js update

# Optional: explicit userId / multi-profile (back-compat — prepend the ID)
node scripts/register.js <userId> <name>
node scripts/calendar-extractor.js <userId> fetch
echo '<events-json-array>' | node scripts/calendar-extractor.js <userId> push
node scripts/calendar-extractor.js <userId> anchor
echo '{"dedup_key":"<verbatim>","patch":{...}}' | node scripts/calendar-extractor.js <userId> update
```

## Workflow

This skill is a two-step pipeline: the **script** does the I/O (fetch transcripts, dedup, push),
the **agent/LLM** does the reasoning (extract events). Extraction is not hardcoded — the agent
reads the fetched transcripts and emits a JSON array of events.

1. **Fetch** — `node scripts/calendar-extractor.js <userId> fetch` issues
   `GET http://javis-server:8000/api/transcripts/recent?since=…&limit=…` with the
   `OPENCLAW_GATEWAY_TOKEN` bearer and prints
   `{ "reference_time": LOCAL-wall-clock (zoneless, in tz), "reference_date": "YYYY-MM-DD", "reference_weekday": "Thursday", "reference_time_utc": ISO8601, "tz": IANA, "sessions": [ { session_id, started_at, ended_at, transcript } ] }`. If fetch fails, returns invalid JSON, or yields zero sessions, output an empty events array and do not push anything; report the failure only if the user asked for a diagnostic. If the fetch response contains no sessions or the transcript text is empty, return `[]` and do not attempt to push a digest.
2. **Extract** — the agent reads that JSON and produces an events array. Each event:
   `{ "title", "start_at" (ISO 8601), "end_at" (ISO 8601, optional), "location", "attendees" (array), "notes", "source_ref" (session_id), "source_kind" ("audio"|"keyboard", from the session's source), "lead_time" (minutes before start for the "Javis calls you" voice alert, optional — defaults to 10) }`.
   Carry `source_kind` through so provenance flows to the `/api/skill/data` mirror and the iOS digest.
   **`lead_time`** is the per-event minutes-before-start at which the proactive voice-call engine rings the user (`fire = start − lead_time`). Omit it for the standard 10-minute lead; emit an integer only when the transcript states a different desired heads-up (e.g. "remind me an hour before the flight" → `60`). Negative/invalid values fall back to 10. The detail fields (`location`, `attendees`, `notes`) double as the announcement context the in-call **Details** command speaks, so keep them populated when the transcript provides them.
   **Date resolution (required):** the top-level `reference_time` is **already local
   wall-clock in `tz`** (zoneless) and `reference_date`/`reference_weekday` give the local
   "today" — so "today" == `reference_date`, and "tomorrow"/"Saturday"/"next Thursday" count
   forward from `reference_weekday`. Do **not** re-apply the tz offset and do **not** anchor on
   `reference_time_utc` (the raw instant, whose date can be the *next* day in the evening — that
   is exactly the off-by-one this field avoids). Fall back to the session's `started_at` only if
   `reference_time` is absent. Never use your own sense of "today". Emit each event's `start_at`/
   `end_at` as a full ISO 8601 instant **with the explicit `tz` UTC offset** (e.g. an 8 PM event
   in `America/Los_Angeles` → `2026-06-04T20:00:00-07:00`) — not a zoneless string, which the
   pipeline would misparse in the container's system zone. Infer AM/PM from surrounding context (e.g. "show starts at 8pm" → evening; "before Gaza's
   party at 6pm" → 18:00). If the transcript does not provide enough information to determine a unique date/time (for example, only "next Friday" with no weekday anchor or an ambiguous time like "at 8" without AM/PM), emit `null` for the unresolved field rather than guessing. When multiple plausible interpretations are equally supported by the transcript, prefer the most specific one; if two interpretations remain equally plausible, emit `null` for the unresolved field rather than guessing. If the transcript mentions recurring meetings, all-day meetings, or multi-day events, preserve them as a single event only when the recurrence is explicit; otherwise emit a single event with the best available start/end times and note the ambiguity in `notes`.
3. **Push** — pipe the events array into `node scripts/calendar-extractor.js <userId> push`. The script:
   - dedups against per-user local state (`data/users/<userId>.json` → `seen` map, 30-day TTL),
   - best-effort mirrors the **new** events to `POST /api/skill/data` (upsert by `dedup_key`) **tagged `status: "pending"`** so the server stores them pending and the iOS calendar table shows them greyed/dashed with **Confirm · Discard** — an event becomes solid only when the user taps **Confirm** (Discard deletes it). Each mirrored row carries a top-level **`lead_time`** (minutes, default 10) so the server's voice-call adapter can schedule the proactive call at `start − lead_time`; the detail fields (`location`/`attendees`/`notes`) ride in `payload` as the in-call announcement context,
   - delivers the **new** events **per card** — one `POST http://javis-server:8000/api/agent/push`
     per event, each `{"skill": "calendar-extractor", "content": "<markdown>", "dedup_key": "<event dedup_key>"}`.
     The server routes each push (carrying its `dedup_key`, no explicit `session_id`) into that card's
     own Agent Chat session, so **every event lands in its own iOS chat thread** instead of one combined
     digest. The pushes are informational — they are not a confirmation gate.

## Editing a pushed card in-thread

A user can correct a card by **replying in that card's own Agent Chat thread**
("6 pm today", "location is Zoom", "add Alex"). The reply edits **that exact row
in place and confirms it** — no duplicate row, no Confirm tap. The agent drives it:

1. **Read the injected `[CURRENT CARD]` block.** When an agent turn runs inside a
   card thread, the server injects a `[CURRENT CARD]` block carrying the card's
   **original `dedup_key` (verbatim)** plus its current fields (`title`,
   `start_at`, `end_at`, `location`, `attendees`, `notes`, `lead_time`, `status`).
   This is the source of truth for the row you are editing. Carry `lead_time`
   forward in the merged patch (default 10 if the block omits it) so an edit never
   silently resets the voice-call lead; set a new integer only if the user asks to
   change the heads-up ("ring me 30 min before" → `lead_time: 30`).
2. **Run `anchor` for a fresh "now".** `node scripts/calendar-extractor.js anchor`
   prints `{ reference_time, reference_date, reference_weekday, reference_time_utc,
   tz }` for the **current** clock. The chat happens *later* than extraction, so
   the original fetch anchor is stale — resolve "today / 6 pm / tomorrow" against
   this fresh anchor (same date-resolution discipline as extraction: anchor on
   `reference_time`/`reference_date`, never your own "today").
   - **The anchor's `tz` is the user's calendar zone.** `anchor` resolves it from
     the server (the authoritative zone) — **not** the container's `TZ`, which is
     empty/UTC in prod and would shift "today" forward a day west of UTC in the
     evening. Pass `[CURRENT CARD]`'s `tz` as `--tz <IANA>` if it carries one;
     otherwise a bare `anchor` already returns the correct zone. **Use the
     `reference_date` it prints — do not compute "today" from a UTC clock.**
3. **Resolve the correction; null-not-guess.** Resolve the user's change against
   the anchor and emit a full ISO 8601 instant **with the explicit `tz` UTC
   offset** (e.g. `2026-06-22T18:00:00-07:00`). If the change is ambiguous or
   unresolvable (e.g. "at 8" with no AM/PM, no weekday anchor), **do not call
   `update`** — ask a follow-up in-thread instead. Emit `null` rather than guess.
4. **Merge into a FULL patch (wholesale-payload rule).** The server overwrites
   `payload`/`start_at`/`end_at` **wholesale** on the matched row, so the `patch`
   must carry the **complete intended state** — the current fields from
   `[CURRENT CARD]` **merged with** the user's change, not just the changed field.
   A time-only edit must still resend `title`/`location`/`attendees`/`notes`, or
   they would be blanked.
   - **Times you are NOT changing:** copy the `start_at`/`end_at` strings from
     `[CURRENT CARD]` **verbatim**. Those are already naive-local wall-clock in the
     card zone (no offset) and the script passes a zoneless `YYYY-MM-DDTHH:MM:SS`
     value through unchanged — it will **not** re-interpret it in the runner's
     zone. (A time you *are* changing must be a full offset-bearing instant per
     step 3, so the script can collapse it correctly.)
   - **Pass the card zone.** Include the card's `tz` (the value the `anchor` step
     printed) as a top-level `tz` so the script collapses any offset-bearing
     changed time against the user's calendar zone, not the container's process
     zone (which is empty/UTC in prod, not the user's zone). If you omit `tz`,
     `update` resolves the user's zone from the server itself — but passing the
     anchor's `tz` is preferred (explicit, and avoids a second lookup).
5. **Run `update` with the verbatim `dedup_key`.**

   ```bash
   echo '{
     "dedup_key": "<the [CURRENT CARD] dedup_key, VERBATIM>",
     "tz": "America/Los_Angeles",
     "patch": {
       "title": "Design Review", "location": "Zoom",
       "attendees": ["Sam"], "notes": "bring laptop",
       "lead_time": 10,
       "start_at": "2026-06-22T18:00:00-07:00",
       "end_at":   "2026-06-22T19:00:00-07:00"
     }
   }' | node scripts/calendar-extractor.js update
   ```

   The script POSTs **one** `/api/skill/data` upsert with that verbatim key and
   `status: "confirmed"`. It does **NOT** recompute the key from the new time
   (that would create a second row — the whole bug), writes `start_at`/`end_at`
   as **naive-local** wall-clock (no `Z`/offset), does **no `seen`-dedup
   filtering**, and does **not** call `/api/agent/push`.

**Auto-confirm semantics.** Stating the corrected value in chat *is* the
confirmation: the upsert's `status: "confirmed"` flips the row `pending →
confirmed` **atomically with the field write** (strictly that direction —
confirmed never downgrades). The skill never calls a separate `/confirm`
endpoint. The iOS card re-render and the live chat reply are the user feedback.
If `/api/skill/data` fails, the script reports the error (non-silent) — tell the
user the card couldn't be updated; do **not** claim success.

This path is **edit-only** of an existing card — creating new events from chat,
re-opening a confirmed row, or deleting via chat (Discard covers delete) are out
of scope.

## How this skill is invoked

This skill has **two triggers** (dispatcher auto-run and manual).

1. **Dispatcher auto-run (automatic).** When a unit of input completes (an audio
   session ends or a keyboard input is saved), the javis-server **session dispatcher**
   classifies the transcript. If it finds scheduling content and an enabled `calendar`
   route matches, the server claims run-once (`DispatchRouteExecuted (user, unit,
   route)`) and **AUTO-RUNS this skill directly — there is no approve-to-run proposal
   card**. It runs in the user's container with a prompt of the form
   `Run /calendar-extractor for <unit>. Deliverable: …`, where the deliverable text is
   the dispatcher's classification carried as an **advisory HINT** — the agent may use
   it alongside the transcript, but should still read the unit transcript for full
   detail (time, attendees). The agent parses `<unit>` (`audio:<session_id>` or
   `kbd:<keyboard_input.id>`), runs `fetch --session <id>` / `fetch --kbd-input <id>`,
   extracts events, and pushes them. **The human gate is not running the skill — it is
   Confirm/Discard on the produced events:** every extracted event is written
   **PENDING** to the calendar table (greyed/dashed with **Confirm · Discard**) and
   becomes solid only when the user taps **Confirm** (Discard deletes it). **The skill
   does not self-gate** — the server owns run-once.
2. **Manual ("today's meetings").** On demand, the agent runs the windowed
   `fetch` (last 24h by default) → extracts → pushes. Repeating the ask re-runs
   extraction on the window; the `seen` map still prevents duplicate delivery.
   Manual writes are also **PENDING** (consistent "confirm to keep").

The route contract the javis-server team must satisfy (RouteRegistry row,
`classify_and_route` deliverable shape, prompt contract) is declared in this file's
`metadata.routes` block and documented in `references/route-contract.md`.

## Notes

- **Runtime dependencies** — the extractor script uses Node 18+ built-ins only (`fetch`, `fs`, `path`); no `npm install` is needed for the script runtime.
- **Data sources**: audio recording transcripts **and** keyboard-dictation sessions — both via
  `GET /api/transcripts/recent` (gateway-token authed), each session carrying a `source` field
  (`"audio"` | `"keyboard"`); a single keyboard unit resolves via
  `GET /api/transcripts/keyboard-input/<id>`. Plus per-user local state (dedup memory). There is no
  `HTTP_SOURCE_URL` — the script talks to javis-server directly.
- **Events are written PENDING.** Every event mirrored to `/api/skill/data` carries
  `status: "pending"`; the server stores it pending and the iOS calendar table renders it
  greyed/dashed with **Confirm · Discard**. **Confirm** promotes the row to solid (`confirmed`);
  **Discard** deletes it. This is the human gate — there is no approve-to-run proposal card.
- **Dedup is local-state-authoritative, event-level only.** The container's gateway token can
  WRITE to `/api/skill/data` but cannot read it back (`GET /api/skill/data` requires a Clerk JWT),
  so novelty is decided by the local `seen` map; the server write is a best-effort mirror for the
  iOS app. There is **no per-unit gating** in the skill — the server owns run-once
  (`DispatchRouteExecuted`); the human gate is Confirm/Discard on the pending rows. So the only
  local dedup is the event-level `seen` map (`{ "<event-key>": "<ts>" }` in
  `data/users/<userId>.json`, 30-day TTL-pruned). It keeps a duplicate event from re-reaching the
  table/chat across overlapping manual windows or a re-run.
- **Timezone**: there is **no prefs file**. On the `fetch`/extract path the skill resolves tz in
  order: the `tz` field on the fetch payload → the `TZ` environment variable → the system zone
  (`Intl.DateTimeFormat().resolvedOptions().timeZone`). The manual and dispatcher paths resolve tz
  the same way. **Edit turns (`update`/`anchor`) have no fetch payload**, so they resolve:
  explicit (`--tz` / stdin `tz` / `[CURRENT CARD]` tz) → **the server's authoritative zone**
  (a best-effort `GET /api/transcripts/recent` reads the same `tz` field) → `TZ` env → system.
  The server step exists because the prod per-user container has an **empty `TZ` (→ UTC)**, which
  shifted "today" forward a day on evening edits west of UTC. The proper long-term fix is to put
  the user's `tz` in the server's `[CURRENT CARD]` block and/or set `TZ` on the container — see
  `docs/superpowers/specs/2026-06-22-calendar-edit-timezone-fix.md`.
- **Markdown, not native cards.** A push delivers a `content` string rendered as markdown on iOS
  (`MDBlock`). Native `EventList`/`EventCard` blocks are emitted only during a live SSE agent turn
  (`_maybe_emit_chat_block`), not via the push path — so each per-card push is rich markdown by design.
- **User IDs** only allow letters, digits, `-`, `_` (path-traversal guard in `data.js`).
- **Backgrounded/killed iOS app**: `AGENT_PUSH` is WebSocket-only (no APNs). For mission-critical
  delivery, add a Telegram channel as backup.
