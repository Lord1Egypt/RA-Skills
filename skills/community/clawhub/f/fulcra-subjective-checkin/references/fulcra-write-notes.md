# Fulcra read/write notes (for the subjective-checkin skill)

Read this when a write fails, verification comes up short, or you need to understand
exactly what the bundled `fulcra_checkin.py` does under the hood. It is NOT needed for
the normal happy path.

## The API surface this skill uses

Base URL: `https://api.fulcradynamics.com`. All calls send `Authorization: Bearer <token>`.

Reads go through the `fulcra-api` CLI (`uv tool run fulcra-api ...`), which prints
**NDJSON** -- one JSON object per line, not a JSON array. The script's `parse_records`
handles NDJSON, a plain array, or a `{"data": [...]}` envelope.

- `get-records SleepStage <startISO> <endISO>` -- raw Apple Health sleep-stage samples,
  each with `start_date`, `end_date`, `value`. This is how the official `fulcra-context`
  and `fulcra-morning-briefing` skills read sleep, so this skill matches them.
  Fulcra has **no single "sleep score."** SleepStage is a 0-5 discrete metric:
  `0=in bed, 1=asleep (unspecified), 2=awake, 3=core/light, 4=deep, 5=REM`.
  **Time asleep = stages 3 + 4 + 5** (stage 2 is awake-in-bed). `summarize_sleep()`
  groups samples into sessions (gaps > 60 min split a session), takes the latest session,
  and derives hours asleep, deep/REM %, efficiency, and a poor/fair/good/excellent quality
  label (same heuristic as `fulcra-morning-briefing`). It reads a ~30h window and picks
  the most recent session, so it works at any time of day. "Sleep score 82" from the
  original spec doesn't exist natively; pass hours asleep as the objective number instead.
- `calendar-events <startISO> <endISO>` -- Apple Calendar events in the window. Count
  the records for "today's event count." Event fields: `title`, `start_date`/`start_time`,
  `location`. (`calendar-events` is its own command; it is NOT in the metric `catalog`.)
- Heads-up: an older `fulcra-morning-briefing` SKILL.md documents the stage values as
  `0=InBed,1=Awake,2=Core,3=Deep,4=REM` -- that is **wrong/outdated**. The live `catalog`
  and `fulcra_sleep_utils.py` agree on `2=awake,3=core,4=deep,5=REM`; trust those.

Writes go through direct REST (the `fulcra-api` CLI is read-only -- it has no create or
record command):

- `GET  /user/v1alpha1/annotation` -- list annotation definitions.
- `POST /user/v1alpha1/annotation` -- create a definition.
- `POST /ingest/v1/record` -- record one annotation value/event.
- Readback: `GET /data/v1alpha1/event/MomentAnnotation` and
  `GET /data/v1alpha1/metric/ScaleAnnotation`, filtered by `start_time`/`end_time`.

## Ingest payload shape

`POST /ingest/v1/record` body (the `data` field is a JSON *string*, not an object):

```json
{
  "specversion": 1,
  "data": "{\"note\": \"...\", \"value\": 4}",
  "metadata": {
    "data_type": "ScaleAnnotation",
    "recorded_at": "2026-05-27T07:30:00-04:00",
    "source": ["com.fulcradynamics.subjective-checkin", "com.fulcradynamics.annotation.<def-id>"],
    "tags": [],
    "content_type": "application/json"
  }
}
```

The second entry in `source` (`com.fulcradynamics.annotation.<def-id>`) is what ties a
recorded value back to its definition. Readback matches on `source_id` or membership in
the record's `sources` array.

For the **Morning Check-In** moment, `data` is `{"note": "<full check-in as JSON>"}`,
so the entire structured record round-trips inside the note. On readback,
`json.loads(record["note"])` returns the original object.

## Alignment with fulcra-common (the verified wire format)

The user's `fulcra-tools` monorepo has `packages/fulcra-common/fulcra_common/wire.py`, described
as the single source of truth for the Fulcra annotation wire format, verified against the live
API. This skill's write path matches it:

- A **moment** record's `recorded_at` is a **bare ISO scalar string** (point-in-time). A
  duration record uses `{start_time, end_time}`. A `{start_time}`-only object matches neither
  and is silently dropped -- so never send that shape.
- `source` is `[caller_source, "com.fulcradynamics.annotation.<def-id>"]`; readback dedups/matches
  on the def source entry.
- `data` is a JSON string (this skill sorts its keys, matching fulcra-common).
- Definitions are resolved by canonical name, **oldest-by-`created_at` wins**, so repeated runs
  across machines converge on one def instead of duplicating (mirrors `resolve_definition_id`).
- There is also a batch endpoint, `POST /ingest/v1/record/batch` (JSONL body, one record per
  line), for writing many records in one call. This skill writes its handful of records
  individually so it can verify each one; switch to batch if write volume ever grows.

## Eventual consistency (the #1 gotcha)

`POST /ingest/v1/record` returns **204** the instant it accepts the write, but the
record is not query-able for ~1-3 seconds afterward. A readback done immediately returns
zero matches even though the write succeeded. `verify()` therefore polls (5 tries, 2s
apart) before giving up.

If `confirmed_count` is still short after that:
- The data was almost certainly written -- 204 means accepted. Check the Timeline.
- **Do not re-run `save`** to force confirmation; there is no dedupe, so you'd create
  duplicate records. Re-reading is safe (`get-records MomentAnnotation "1 day"`),
  re-writing is not.

## Windows one-time setup gotchas

These bit us during setup on this machine. They are environment issues, not skill bugs.

1. **`uv` / `python3` on PATH.** This skill needs `uv`. Installing it (e.g.
   `winget install astral-sh.uv`) updates PATH for *new* shells only. Bare `python3`
   may resolve to the Windows Store stub, which is broken -- that's why the skill runs
   the script via `uv run --python 3.12 ...`, which provisions Python itself.
2. **`~/.config/fulcra` creation.** The CLI does a non-recursive mkdir of
   `~/.config/fulcra` and crashes with `WinError 3` if `~/.config` doesn't exist yet.
   Fix: create `~/.config` once (`mkdir %USERPROFILE%\.config`), then `auth login`.
3. **`charmap` Unicode error on login.** The login prints a ✨ emoji; the default
   Windows console code page can't encode it and the login crashes before showing the
   URL. Fix: set `PYTHONUTF8=1` (and optionally `PYTHONIOENCODING=utf-8`) for the login
   command.

## What the skill writes

One `save` writes up to four annotations, all sharing the check-in timestamp:

| Definition | Type | Value | Holds |
|---|---|---|---|
| Morning Check-In | moment | (none) | full structured record in the note (lossless) |
| Morning Energy | scale 1-10 | energy_level | energy_words in note |
| Morning Mood | scale 1-5 | rough=1 .. great=5 | feeling word in note |
| Social Battery | scale 1-3 | low=1, medium=2, high=3 | -- |

The moment is the canonical "structured annotation." The three scales exist so the
quantifiable dimensions chart over time next to objective health data -- which is the
point of capturing subjective state at all. Energy/mood/social are skipped individually
if the user didn't give a value for them, but the moment always captures everything
provided.
