# Collector design — `scripts/journal_collect.py`

Why each decision exists. Change one only with a reason; several of them were bugs once.

## Window model

- `window(D) = [D {day_start_hour}:00, D+1 {day_start_hour}:00)`; the default boundary is 04:00,
  and `latest_complete_day(now) = (now − day_start_hour).date() − 1 day`.
- Only **complete** windows are writable. A late-night worker's "today" ends at 04:00, not midnight;
  set `day_start_hour` to match the user's rhythm instead of arguing with them about dates.

## Coverage bookkeeping

- The journal file is the ledger: one `<!-- window:YYYY-MM-DD -->` per entry, nothing else.
- `covered_days()` = markers found in the file; `missing_days()` = every unmarked day from
  `min(covered)` (or `JOURNAL_START`, else latest−1) through the latest complete window.
- Because the ledger is in the prose file, re-runs are idempotent and deleting a marker means
  "rewrite that day". No separate state file to fall out of sync.
- `--only DATE` bypasses the ledger on purpose (tests, re-linting). Never put it in a cron prompt.

## Session attribution

- A resumed session can hold messages in several windows. Select sessions whose
  `started_at`/`last_activity_at` straddle the window, then keep one only if it has ≥1 message
  inside the window.
- Pass a `claimed: set[session_id]` through windows in order, so each session lands in the FIRST
  window where it has messages. Without it the same session appears in two days' digests.
- Show the writer min/max message timestamps **inside the window**, never session start/end — those
  read like `18:33-16:02` and look like a 22-hour workday.

## Sources (read-only)

- `state.db` → `sessions(id, title, display_name, started_at, last_activity_at, hidden, source)` and
  `messages(session_id, role, content, tool_name, timestamp, active)`, opened with
  `file:...?mode=ro`. Nothing here ever writes to the database.
- Skip `source='cron'` (the journal job itself is not an event) and `hidden=1`; drop runtime-noise
  prompts (`[IMPORTANT: Background process…`, `[ASYNC DELEGATION…`).
- A workspace `mtime` walk supplies "files touched"; `skip_dirs` keeps `.git`, `node_modules`,
  `__pycache__`, venvs, `archive`, `memory`, `tmp` out of it. `memory` is skipped because the
  journal lives there and would otherwise report itself as work.

## Digest shape

- Per session: one `###` heading (tooltip for the linter: **one heading = one event**), the in-window
  span, `n msgs / n tool calls`, deduped prompts, the last 1–2 assistant outcomes, and a tool
  histogram (top 6). Then a touched-file section, which is **not** an event.
- Cap per window (`digest_chars`, ~2.6 KB) and per batch (`max_windows`, default 4) so the writer's
  prompt stays cheap. When a window is truncated the digest says so; the writer is told the digest
  is material, so a truncated detail is recoverable, but a truncated **heading** is a lost event —
  hence `max_sessions` (10) is generous while prose caps are tight.

## Local model use

- Embeddings: one `/api/embed` call per session, prompts dropped when cosine ≥ `dedupe_cosine`
  (0.88). Without embeddings, character-set overlap ≥ 0.8 does the same job more crudely.
- Compression: `/api/generate` with `think: false`, `temperature 0.2`, `num_predict 160`,
  `num_ctx 2048`; reject output shorter than 8 or longer than 400 chars and fall back to raw
  bullets. First call pays model load (~10 s), each further call ~2 s.
- Both features are detected at runtime by `/api/tags`. A silent model-name mismatch merely means
  the feature is off, which is why `has_model()` accepts `name`, `name:latest` and the untagged
  base name.

## Configuration

Config file keys (all optional) mirror the module's `DEFAULTS`; the JSON is merged over the
defaults, so an example file can stay short. Precedence: **CLI flag > environment variable >
config file > default**. Environment variables (`JOURNAL_FILE`, `JOURNAL_WORKSPACE`, …) exist so an
already-wired cron job keeps working after an upgrade.

`labels` is the only i18n surface: pass `"language": "zh"` and the collector swaps in the built-in
Chinese labels (`CN_LABELS`), then applies any per-key overrides you supply. Tests assert both
label sets have identical key sets, so adding a label means adding it twice.

## Scheduling reality

- The cron ticker lives inside the Hermes gateway: nothing fires while Hermes is not running.
- `cron.catch_up_missed` defaults to true, so the missed 04:00 run fires on the first tick after
  Hermes starts — boot-time catch-up is what makes the journal survive closed days.
- Multi-day gaps are handled by the collector itself (max windows per run), not by extra ticks.
