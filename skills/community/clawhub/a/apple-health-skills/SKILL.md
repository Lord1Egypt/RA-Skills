---
name: apple-health-query
description: Use this skill when the user asks for Apple Health summaries, trends, alerts, or check-ins from the local collector. Validate collector connectivity over HTTP and fetch fresh data with shell commands before giving coaching-style guidance.
---

# Apple Health Query Skill

Use this skill to analyze Apple Health data already synced into local SQLite by the collector.

## Tools to use

- **Shell tool**: run `scripts/query_health.py` to pull fresh JSON data.
- **HTTP tool**: optionally verify collector availability with `/healthz` before troubleshooting missing data.

## Workflow

1. **(Optional health check) Verify collector is reachable** when user reports stale/missing data:
   - `curl -fsS http://<collector-host>:8443/healthz`
   - if TLS is enabled: `curl -fsS https://<collector-host>:8443/healthz`
2. **Query the local database via shell** (preferred default):
   - `python scripts/query_health.py --window-hours 24 --sleep-nights 7 --types heart_rate,glucose,sleep_stage`
3. **Adjust parameters to user intent**:
   - Short check-in: `--window-hours 1`
   - Daily review: `--window-hours 24 --sleep-nights 7`
   - Alert follow-up: keep `--types` narrow to requested metrics.
4. **Summarize with numbers and timestamps**, then give practical next steps.
5. **Always include safety framing**: informational only, not medical advice; suggest clinician contact for extreme/persistent readings.

## Output expectations

Base your answer on the returned JSON fields:
- `generated_at`, `user_id`, `window_hours`
- `quantity.<metric>[]` entries with `{ts, value, unit, source, device}`
- `sleep[]` entries with `{start_ts, end_ts, category, source, device}`

## Response style guardrails

- Cite the exact time window used (for example: “last 24 hours” and “last 7 nights”).
- Highlight notable thresholds carefully (e.g., glucose outside typical 70–180 mg/dL range).
- Tie suggestions to observed values; avoid generic advice.
- Never hardcode user IDs or DB paths—`scripts/query_health.py` already reads `.env`.

---

## Live Heart Rate

The collector stores **real-time BLE heart rate** events from Wahoo HR straps (and compatible sensors) in the `live_events` table. Use this for workout monitoring, recent-activity check-ins, or comparing live readings against resting baseline.

### Tools to use

- **Shell tool**: run `scripts/query_live_hr.py` to pull live HR events and per-session summaries.

### Workflow

1. **Query recent live HR events** (default: last 60 minutes):
   - `python scripts/query_live_hr.py --window-minutes 60`
2. **Narrow to the last workout or a specific timeframe**:
   - `python scripts/query_live_hr.py --window-minutes 120`
3. **Filter to a specific session** (use a session UUID from a previous query):
   - `python scripts/query_live_hr.py --session-id <uuid> --window-minutes 180`
4. **Filter to a specific device** (useful when multiple sensors are paired):
   - `python scripts/query_live_hr.py --device-id <device_id> --window-minutes 60`

### Output fields

Base your answer on the returned JSON:

- `summary` — aggregate stats for the queried window:
  - `count` — total event count
  - `latest_bpm`, `min_bpm`, `max_bpm`, `avg_bpm`, `median_bpm`, `stddev_bpm`
  - `latest_zone` — heart rate zone: `resting` (<60), `normal` (60–99), `elevated` (100–139), `high` (≥140)
- `sessions[]` — per-session breakdown with `session_id`, `event_count`, `start_ts`, `end_ts`, `device_name`, `avg_bpm`, `min_bpm`, `max_bpm`
- `events[]` — individual readings with `ts`, `value` (BPM), `session_id`, `seq`, `device_id`, `source_device_name`

### Guidance

- **Workout summary**: report `avg_bpm`, `max_bpm`, and duration (`start_ts` → `end_ts` of the session).
- **Zone coaching**: map `latest_zone` to practical advice (e.g., elevated zone during recovery warrants attention).
- **Unusual readings**: flag sustained HR >150 or <40 bpm; recommend clinician contact if persistent.
- **Data freshness**: if `count` is 0, the sensor may not be paired or the session may not have started — advise the user to open the Live HR screen on their iPhone.
