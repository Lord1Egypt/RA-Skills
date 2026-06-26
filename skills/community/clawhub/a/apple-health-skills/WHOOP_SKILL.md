---
name: whoop-query
description: Use this skill when the user asks about Whoop data — recovery scores, HRV, strain, sleep performance, or workout analysis. Fetch fresh data from the local SQLite database (populated by the Whoop sync script) and give coaching-style guidance.
---

# Whoop Query Skill

Use this skill to analyze Whoop data synced from the Whoop API into the local SQLite database.

## Setup (one-time)

Before data is available, the user must:

1. Create a Whoop developer app at https://developer.whoop.com and add the redirect URI `http://localhost:8900/callback`.
2. Add credentials to `.env`:
   ```
   WHOOP_CLIENT_ID=<client-id>
   WHOOP_CLIENT_SECRET=<client-secret>
   ```
3. Authorize and store tokens:
   ```
   python scripts/setup_whoop.py
   ```
4. Run the initial sync:
   ```
   python scripts/sync_whoop.py --days 30
   ```

After setup, keep data fresh by running `sync_whoop.py` on a schedule (e.g. daily cron).

## Syncing fresh data

Before querying, optionally refresh the local database:

```
python scripts/sync_whoop.py --days 7
```

## Querying data

```
python scripts/query_whoop.py --window-days 7
```

Adjust `--window-days` to match the user's request (default: 7).

## Output fields

The query script returns JSON with:

### `features.recovery`
- `avg_recovery_score` — rolling average recovery (0–100 green/yellow/red)
- `latest_recovery_score` — most recent score
- `avg_hrv_rmssd` — average HRV (ms); higher is generally better
- `latest_hrv_rmssd` — most recent HRV reading
- `avg_resting_hr` — average resting heart rate (bpm)
- `latest_resting_hr` — most recent resting HR
- `samples` — number of recovery records in window

### `features.sleep`
- `avg_performance_pct` — Whoop sleep performance percentage (0–100)
- `latest_performance_pct` — last night's sleep performance
- `avg_total_sleep_minutes` — average sleep duration
- `avg_sws_minutes` — average slow-wave (deep) sleep
- `avg_rem_minutes` — average REM sleep
- `avg_respiratory_rate` — average breaths per minute during sleep
- `nights` — number of nights in window

### `features.strain`
- `avg_strain` — average daily strain (0–21 scale)
- `latest_strain` — most recent day's strain
- `max_strain` — highest strain day in window
- `days` — number of cycle records

### `recoveries[]` — individual recovery records
Each entry has `date`, `recovery_score`, `resting_heart_rate`, `hrv_rmssd_milli`, `spo2_percentage`, `skin_temp_celsius`.

### `sleeps[]` — individual sleep records
Each entry has `start_date`, `end_date`, `performance_percentage`, `total_sleep_minutes`, `stage_sws_minutes`, `stage_rem_minutes`, `respiratory_rate`, `sleep_efficiency`.

### `cycles[]` — daily strain cycles
Each entry has `date`, `strain`, `kilojoule`, `average_heart_rate`, `max_heart_rate`.

### `workouts[]` — individual workout records
Each entry has `start_date`, `end_date`, `sport_name`, `strain`, `average_heart_rate`, `max_heart_rate`, `kilojoule`, and `zone_zero_minutes` through `zone_five_minutes`.

## Workflow

1. **Sync recent data** (optional, if user wants latest):
   - `python scripts/sync_whoop.py --days 7`
2. **Query the database**:
   - `python scripts/query_whoop.py --window-days 7`
3. **Adjust window to user intent**:
   - "How was my recovery this week?" → `--window-days 7`
   - "Show me last month's trends" → `--window-days 30`
   - "Just today's stats" → `--window-days 1`
4. **Summarize with numbers**, then give practical next steps.
5. **Always include safety framing**: informational only, not medical advice.

## Coaching guidance

### Recovery score interpretation
- **Green (67–100)**: Well recovered; ready for high strain or hard training.
- **Yellow (34–66)**: Moderate recovery; consider moderate intensity.
- **Red (0–33)**: Under-recovered; prioritize rest or light activity.

### HRV coaching
- Declining HRV trend over 3+ days → flag accumulated fatigue or illness.
- HRV significantly below personal baseline → recommend recovery day.

### Sleep performance
- Below 70%: Poor sleep quality; investigate sleep hygiene, timing, or environment.
- 85%+: Good sleep; correlate with recovery score to confirm readiness.

### Strain coaching
- Strain consistently above 18 without matching recovery → overreaching risk.
- Zero-strain days with low recovery → consider active recovery (light movement).

### Respiratory rate
- Elevated respiratory rate during sleep (>18 bpm, or >2 bpm above baseline) can indicate illness or stress.

## Response style guardrails

- Cite the exact window used (e.g., "last 7 days").
- Lead with the most recent recovery score and HRV.
- Tie suggestions to actual values; avoid generic advice.
- Flag persistent patterns (3+ days) more assertively than single-day anomalies.
- Never hardcode user IDs or DB paths — scripts read `.env` automatically.
- Remind users that Whoop metrics are informational, not medical diagnoses.
