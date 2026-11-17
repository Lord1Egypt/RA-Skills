# Consumed feed contract (v1.1.0)

Checked 2026-11-09 against the published v1.0.4 files and
https://codex-reset-radar.pages.dev/current.json . This is the monitor's validated
projection of the live feed, not a claim that upstream publishes a formal JSON
Schema. The feed's `schema_version` is currently `"2.0"`, `service` is
`"codex-reset-radar"`, and `type` is `"public_summary"`. No authenticated/full API
is contacted. A bare HTTP 403 from this executor prevented a direct live download;
the current public body was inspected through web retrieval. The offline fixture
is a minimal projection of observed fields, not the full body. Legacy fixtures
are synthetic because the original script did not validate or bundle a schema.

| Meaning | Schema 2.0 | Legacy 1.0 / absent version |
|---|---|---|
| Observation time (required) | `monitored_at` | `checked_at`, otherwise `monitored_at` |
| Open flag (required boolean) | `window_open`, agreeing with `window.open` | `window_open` |
| Top status (required enum) | `status` | `status` |
| Window state | `window.status` | `current_window.state` |
| Stable reset ID | `window.id` / `window.event_id`; when closed, fallback `completion_observation.event_id` | `last_window.id`, otherwise current window ID |
| Open time, if known | `window.opened_at` | `current_window.opened_at`, then `last_window.opened_at` |
| Prediction | `prediction.level`, numeric `probability_24h`, `updated_at` | same |

`window` must be present in schema 2.0. A null window is permitted only when
`window_open` is false. A legacy layout requires a `current_window` or `last_window` key and must not
contain a schema-2 `window` object. Legacy missing/null `current_window` means
`current_window_state: "none"` only when closed. Window objects require their
state enum; schema 2.0 objects also require a boolean `open`. Open windows cannot
have `none`, `closed`, `expired`, or `completed` state; closed windows cannot have
`open` or `active` state. Top status is a confirmation/status dimension and need
not equal the window lifecycle state (e.g. `official_confirmed` / `completed`).
Optional objects must have the correct type when present. Conflicting nonempty
`window.id` and `window.event_id` are rejected. Stable IDs use 1–160 ASCII letters,
digits, colon, dot, underscore, slash, or hyphen, beginning with a letter/digit.
An absent/empty effective identity never means a new reset. A legacy explicit
empty `last_window.id` is invalid remote data; the old flat cache can contain an
empty baseline ID.

Status/window-state enums: `none`, `unknown`, `idle`, `watch`, `watching`,
`monitoring`, `pending`, `announced`, `possible`, `likely`, `open`, `active`,
`closed`, `expired`, `confirmed`, `completed`, `cooldown`, `unconfirmed`,
`community_confirmed`, `official_confirmed`, `stationmaster_confirmed`.
Prediction levels: `none`, `unknown`, `low`, `medium`, `high`, `very_high`.
New identifiers fail closed until reviewed. These accepted compatibility values
are the consumer's allowlist, not an exhaustive upstream specification.

Probabilities must be finite JSON numbers in [0,1]; booleans and numeric strings
are rejected. Optional `probability_48h` is validated if present but not monitored.
Timestamps must be valid RFC3339 datetimes with seconds and an explicit offset
or `Z` (up to six fractional digits). Date-only, naive, invalid calendar dates,
and malformed offsets are rejected. Missing prediction update times suppress
prediction alerts; missing observation times reject the entire sample. Opening
and closing timestamps may be null and are never replaced with poll time.

Top/window/prediction `ok: false`, `success: false`, nonempty `error`/`errors`, or
status `error`, `failed`, `unavailable`, `degraded` reject the sample. Explicit
`stale: true`, `is_stale: true`, or status `stale` reject the sample. Recognized
boolean health flags must actually be booleans. Unrelated nested sections are
ignored; they cannot grant access or change the feed URL. Stale prediction times
are handled separately from snapshot staleness so a valid window signal can
still be monitored. A stale/error envelope within prediction rejects the sample.

The inspected public observation was `2026-11-05T10:10:58.739373+00:00` and its
prediction was calculated `2026-10-24T01:50:00+08:00`. On November 9 the sample
correctly fails `stale_data`; no claim about a current reset can follow from it.
