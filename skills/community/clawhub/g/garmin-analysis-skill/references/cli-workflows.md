# Garmin CLI Workflows

Use this reference for public `cycling-health` installation guidance, Garmin commands, and analysis conventions.

## Contents

- [Install Or Locate The CLI](#install-or-locate-the-cli)
- [Upgrade Before Use](#upgrade-before-use)
- [Feedback Channel](#feedback-channel)
- [Auth And Status](#auth-and-status)
- [China To Global Activity Sync](#china-to-global-activity-sync)
- [Sleep Data](#sleep-data)
- [Health And Recovery Context](#health-and-recovery-context)
- [Extended Garmin Queries](#extended-garmin-queries)
- [Cycling Data](#cycling-data)
- [Failure Handling](#failure-handling)

## Install Or Locate The CLI

Public repository:

```text
https://github.com/baijian/cycling-health
```

Prefer an existing installation:

```bash
command -v cycling-health
cycling-health version
cycling-health upgrade --output json
cycling-health doctor --output json
```

If `cycling-health` is missing:

1. Direct the user to `https://github.com/baijian/cycling-health`.
2. Prefer the repository's latest release/download instructions.
3. Ask the user to place the executable on `PATH` or provide its absolute path.
4. Verify with `cycling-health version`.

Do not assume a source checkout or machine-specific binary path.

Release archives also include `README.md` plus the setup guides
`docs/intervals-icu.md`, `docs/strava.md`, `docs/igpsport.md`, and
`docs/xingzhe.md`. Use the matching guide for first-time application,
credential, OAuth, and callback configuration. Do not ask the user to expose
the local secret files described by those guides.

## Upgrade Before Use

When command execution is available and `cycling-health` exists, run the public self-upgrade before Garmin status, sync, or analysis commands:

```bash
cycling-health upgrade --output json
```

The command checks the trusted Alibaba Cloud OSS release manifest first and falls back to GitHub Releases when OSS metadata is unavailable or invalid. It does not accept user-supplied release or download URLs.

Treat `status: "upgraded"` and `status: "up-to-date"` as successful upgrade states. If the upgrade fails because the network is unavailable, the executable cannot be replaced, checksum verification fails, or no compatible release asset exists, preserve the error in the final answer and ask before continuing with the currently installed binary unless the user already instructed you to proceed.

## Feedback Channel

For bug reports, installation issues, Garmin data gaps, or analysis questions, point users to the Discord invitation URL configured in `SKILL.md`.

## Auth And Status

Check status:

```bash
cycling-health garmin status --output json
cycling-health garmin status --region cn --output json
cycling-health garmin status --region global --output json
```

Interactive login:

```bash
cycling-health garmin login --region cn --email user@example.com
cycling-health garmin login --region global --email user@example.com
```

Notes:

- Garmin read-only query families documented here accept `--region cn|global`; omitting it defaults to `cn`. Select the region by login state: prompt login when neither is logged in, use the logged-in region when only one is available, and default to `cn` when both are logged in and the user did not specify a region.
- CN-to-Global activity sync requires both `cn` and `global` to be logged in.
- Password and MFA prompts are interactive. The user should enter them locally.
- Token files are local secrets; do not display or copy their contents.

## China To Global Activity Sync

Inspect sync state:

```bash
cycling-health garmin syncstatus --output json
```

Incremental sync:

```bash
cycling-health garmin sync --new-only --output json
```

Full historical sync:

```bash
cycling-health garmin sync --output json
```

Default to incremental sync. Use full sync only for first-time backfill or when the user explicitly asks for historical sync.

Report these fields when present:

- `retried`
- `synced`
- `failed`
- `lastActivityTime`
- failed record count from `syncstatus`
- state and failed-record paths only when useful for troubleshooting

## Sleep Data

Query region: select by login state (no login → prompt login; one login → that region; both logins and unspecified → `cn`). Pass it with `--region <cn|global>`.

Common queries:

```bash
cycling-health garmin sleep list --region cn --days 7 --output json
cycling-health garmin sleep list --region cn --start YYYY-MM-DD --end YYYY-MM-DD --output json
cycling-health garmin sleep list --region cn --start PREVIOUS_DATE --end WAKE_DATE --output json
cycling-health garmin summary get --region cn --date YYYY-MM-DD --output json
cycling-health garmin health get --region cn --days 7 --metrics hrv,rhr,stress,bb,respiration,spo2 --output json
cycling-health garmin health get --region cn --start PREVIOUS_DATE --end WAKE_DATE --metrics hrv,rhr,stress,bb,respiration,spo2 --output json
cycling-health garmin health get --region cn --start WAKE_DATE --end WAKE_DATE --metrics bb_events --output json
cycling-health garmin chart render --region cn --chart sleep --days 30 --output garmin-sleep.html
```

Choose the smallest useful query set:

- Single night: adjacent-date `sleep list` plus wake-date `summary get`.
- Recent baseline: `sleep list --days 7` plus health metrics for the same range.
- Longer trend: 14-30 days of sleep and selected recovery metrics; render a chart only when a visual is useful.
- Body-battery event explanation: query `bb_events` only for the relevant day because it returns event-level activity and stress context.

`summary get` is the efficient wake-date snapshot. When available, it includes sleep, resting/max HR, body battery, stress, VO2 max, training status/load, training readiness, weekly intensity minutes, and last-sync time. Do not make separate training calls for the same date unless the summary omits a required field or the user asks for raw metric detail.

Date handling:

- Interpret "today's early morning sleep" and "last night" as sleep whose wake date is the requested date.
- For a single wake date, query `sleep list` with the exact date and also `PREVIOUS_DATE` through `WAKE_DATE`; Garmin sleep records can be keyed by either sleep start date or wake date.
- If the user asks for recent sleep without a specific date, start with `sleep list --days 7`, then add health metrics for the same range.
- If `data.records[]` is empty for the exact date, do not stop. Run the adjacent-date sleep window and `summary get` for both `WAKE_DATE` and `PREVIOUS_DATE`.

Sleep JSON shape:

- `data.records[]`: per-day sleep record
- `data.averages`: aggregate sleep averages
- `warnings[]`: endpoint or data gaps

Useful sleep fields:

- `date`
- `start_time_local`, `end_time_local`
- `total_seconds`, `total_formatted`
- `deep_seconds`, `light_seconds`, `rem_seconds`, `awake_seconds`
- `sleep_score`
- `avg_heart_rate`, `resting_heart_rate`
- `avg_respiration`, `restless_periods`
- `avg_overnight_hrv`, `hrv_last_night_avg`, `hrv_weekly_avg`, `hrv_status`
- `body_battery_high`, `body_battery_low`

Fallback sequence for empty sleep records:

1. Re-check a wider sleep window:

   ```bash
   cycling-health garmin sleep list --start PREVIOUS_DATE --end WAKE_DATE --output json
   cycling-health garmin sleep list --days 7 --output json
   ```

2. Check Garmin daily summaries for both possible record dates:

   ```bash
   cycling-health garmin summary get --date WAKE_DATE --output json
   cycling-health garmin summary get --date PREVIOUS_DATE --output json
   ```

3. Check recovery metrics across the same overnight window:

   ```bash
   cycling-health garmin health get --start PREVIOUS_DATE --end WAKE_DATE --metrics hrv,rhr,stress,bb,respiration,spo2 --output json
   ```

Only say that sleep-stage details are unavailable after these fallbacks return no sleep-duration, sleep-stage, or sleep-score fields. If health metrics such as HRV, respiration, SpO2, stress, or body battery are present, describe them as recovery context rather than a substitute for sleep-stage details.

Analysis checklist:

- Duration and sleep timing vs the user's available range average.
- Sleep score and trend.
- Deep, REM, light, and awake time when present.
- Sleeping HR, respiration, and restless periods when present.
- HRV status and last-night HRV vs weekly average.
- Resting HR and stress context.
- Body battery recharge/depletion; event-level impact only when `bb_events` was queried.
- Training readiness/status as current-day context, not as a sleep metric.
- Missing days and warnings.

## Health And Recovery Context

Common queries:

```bash
cycling-health garmin health get --days 7 --metrics hrv,rhr,stress,bb --output json
cycling-health garmin health get --start YYYY-MM-DD --end YYYY-MM-DD --metrics hrv,rhr,stress,bb,respiration,spo2 --output json
cycling-health garmin health get --start YYYY-MM-DD --end YYYY-MM-DD --metrics bb_events --output json
cycling-health garmin health query --metric heart_rate --date YYYY-MM-DD --time HH:MM --output json
cycling-health garmin health query --metric stress --date YYYY-MM-DD --time HH:MM --output json
cycling-health garmin health query --metric body_battery --date YYYY-MM-DD --time HH:MM --output json
```

Use recovery metrics to explain sleep and cycling readiness only when data is present. `health get` also supports `steps`, `floors`, `intensity`, `hydration`, and `hr`; request them only when relevant to the question. Use `health query` for a specific intraday timestamp, not for broad trend analysis.

## Extended Garmin Queries

Use these read-only families only when they answer the user's question. Every
command accepts `--region cn|global`; private Garmin endpoints can return
different shapes, empty data, or warnings by region and account.

Long-term health trends:

```bash
cycling-health garmin trend get --region cn --metric daily_steps --days 90 --output json
cycling-health garmin trend get --region cn --metric weekly_steps --weeks 52 --output json
cycling-health garmin trend get --region cn --metric weekly_stress --weeks 52 --output json
cycling-health garmin trend get --region cn --metric weekly_intensity --days 90 --output json
```

Races, saved courses, workouts, and plans:

```bash
cycling-health garmin event upcoming --region cn --days 365 --output json
cycling-health garmin event list --region cn --start YYYY-MM-DD --end YYYY-MM-DD --type cycling --output json
cycling-health garmin event get --region cn --event-uuid EVENT_UUID --output json
cycling-health garmin event primary --region cn --output json
cycling-health garmin event search --region cn --query QUERY --latitude LAT --longitude LON --radius-km 100 --output json
cycling-health garmin course list --region cn --type road_biking --output json
cycling-health garmin course get --region cn --course-id COURSE_ID --output json
cycling-health garmin workout list --region cn --limit 100 --output json
cycling-health garmin workout get --region cn --workout-id WORKOUT_ID --output json
cycling-health garmin workout scheduled --region cn --year YYYY --month MM --output json
cycling-health garmin training-plan list --region cn --output json
cycling-health garmin training-plan get --region cn --plan-id PLAN_ID --type adaptive --output json
```

Achievements, account data, nutrition, lifestyle, activity inventory, and gear:

```bash
cycling-health garmin achievement records --region cn --output json
cycling-health garmin achievement badges --region cn --status earned --output json
cycling-health garmin achievement challenges --region cn --status active --limit 100 --output json
cycling-health garmin account settings --region cn --kind all --output json
cycling-health garmin nutrition get --region cn --metric food_logs --date YYYY-MM-DD --output json
cycling-health garmin lifestyle get --region cn --date YYYY-MM-DD --output json
cycling-health garmin activity count --region cn --output json
cycling-health garmin activity types --region cn --output json
cycling-health garmin gear list --region cn --output json
cycling-health garmin gear activities --region cn --gear-uuid GEAR_UUID --limit 100 --output json
```

Use event `search` for public race discovery and event `list`/`upcoming` for
events already associated with the account. Course details omit large point
arrays unless `--include-points` is requested. Nutrition returns food logs,
meals, or settings; do not reinterpret intake as Garmin calories burned.
Lifestyle data can be empty when the account or region does not expose habit
records. Keep all such warnings in the result instead of treating another
source as an automatic substitute.

## Cycling Data

Query region: select by login state (no login → prompt login; one login → that region; both logins and unspecified → `cn`). `activity list`, `activity get`, `activity export`, `training get`, `body get`, `profile get`, and `fit download` all accept `--region <cn|global>`.

List recent cycling activities:

```bash
cycling-health garmin activity list --region cn --type cycling --days 30 --output json
cycling-health garmin activity list --region cn --type cycling --days 90 --max-activities 50 --output json
cycling-health garmin activity list --region cn --type cycling --start YYYY-MM-DD --end YYYY-MM-DD --max-activities 50 --output json
```

For "last N rides", start with `--max-activities N`. If fewer than N rides are returned, increase `--days` or ask for a wider date range before analyzing ability from an incomplete sample.

Fetch one activity:

```bash
cycling-health garmin activity get --region cn --activity-id ACTIVITY_ID --output json
cycling-health garmin activity get --region cn --activity-id ACTIVITY_ID --raw --output json
cycling-health garmin activity extended --region cn --activity-id ACTIVITY_ID --output json
```

`activity get` already attempts summary, laps, HR zones, power zones, weather, gear, and detailed samples. Use `activity extended` only when typed splits or split summaries are needed and the normal detail result is insufficient. Use `--raw` only when a required field is absent from the simplified output.

Progress queries:

```bash
cycling-health garmin activity progress --region cn --days 90 --metric distance --output json
cycling-health garmin activity progress --region cn --days 90 --metric duration --output json
cycling-health garmin activity progress --region cn --days 90 --metric moving_duration --output json
cycling-health garmin activity progress --region cn --days 90 --metric elevation_gain --output json
```

Run only the axes needed for the user's progression question. Results are grouped by parent activity type by default, so use the cycling group for cycling analysis. Activity history can usually provide a quick volume summary without all four calls.

Training and body context for cycling ability:

```bash
cycling-health garmin training get --region cn --metric max_metrics --date YYYY-MM-DD --output json
cycling-health garmin training get --region cn --metric cycling_ftp --output json
cycling-health garmin training get --region cn --metric status --date YYYY-MM-DD --output json
cycling-health garmin training get --region cn --metric readiness --date YYYY-MM-DD --output json
cycling-health garmin training get --region cn --metric endurance_score --date YYYY-MM-DD --output json
cycling-health garmin training get --region cn --metric endurance_score --start YYYY-MM-DD --end YYYY-MM-DD --output json
cycling-health garmin training get --region cn --metric hill_score --date YYYY-MM-DD --output json
cycling-health garmin training get --region cn --metric hill_score --start YYYY-MM-DD --end YYYY-MM-DD --output json
cycling-health garmin training get --region cn --metric fitness_age --output json
cycling-health garmin training get --region cn --metric lactate_threshold --output json
cycling-health garmin training get --region cn --metric race_predictions --output json
cycling-health garmin training get --region cn --metric running_tolerance --start YYYY-MM-DD --end YYYY-MM-DD --aggregation weekly --output json
cycling-health garmin body get --region cn --metric weigh_ins --days 30 --output json
cycling-health garmin body get --region cn --metric composition --days 30 --output json
cycling-health garmin profile get --region cn --raw --output json
cycling-health garmin achievement records --region cn --output json
```

Use direct `cycling_ftp` first for FTP and `max_metrics` for VO2 max or additional maximum metrics. Use `status` for training status and acute/chronic load; use `readiness` only for today's training decision. Use date ranges for endurance/hill score only when progression matters. Lactate threshold, race predictions, and running tolerance are sport-specific context and must not be relabeled as cycling evidence when Garmin returns running data. Use personal records only for peak-performance questions. Use `weigh_ins` and `composition` before saying weight is unavailable. Calculate W/kg only from a relevant power/FTP value and the latest reliable body weight; report both source dates when they differ or the weight is stale.

Export and analyze local files:

```bash
mkdir -p garmin-analysis
cycling-health garmin activity export --activity-id ACTIVITY_ID --format fit --output garmin-analysis
cycling-health garmin fit download --activity-id ACTIVITY_ID --path garmin-analysis/ACTIVITY.fit
cycling-health garmin activity analyze --file garmin-analysis/ACTIVITY.fit --output json
cycling-health garmin fit parse --file garmin-analysis/ACTIVITY.fit --targets 1,5,10,last --output json
cycling-health garmin activity query --file garmin-analysis/ACTIVITY.fit --distance 10000 --output json
cycling-health garmin activity dump --file garmin-analysis/ACTIVITY.fit --max-records 0 --output json
```

Activity list fields vary by Garmin payload. Common useful fields include:

- `activityId`
- `activityName`
- `startTimeLocal`
- `distance`
- `duration`, `movingDuration`
- `averageSpeed`, `maxSpeed`
- `averageHR`, `maxHR`
- `elevationGain`
- `averageBikeCadence`, `maxBikeCadence`
- `avgPower`, `maxPower`, `normalizedPower`
- `trainingEffect`, `aerobicTrainingEffect`, `anaerobicTrainingEffect`
- `hrTimeInZone`, `powerTimeInZone`, `timeInZones`

Training and body fields vary by Garmin payload. Search returned JSON for these concepts before reporting them missing:

- VO2 max: `vo2Max`, `generic.value`, `cyclingVo2Max`, or VO2-related keys in `max_metrics`
- FTP: direct `cycling_ftp` response, then `ftp`, `functionalThresholdPower`, `cyclingFTP`, or power threshold keys in `max_metrics`
- Endurance and climbing: `endurance_score`, `hill_score`, `score`, `classification`, or trend fields
- Training load: `acute_load`, `chronic_load`, `target_min`, `target_max`, `ratio`, `acwr_percent`, or `acwr_status`
- Weight: `weight`, `weightKg`, `bodyWeight`, or latest weigh-in/composition entry
- Zones: HR/power zone arrays, time-in-zone summaries, or zone settings in raw activity/profile payloads

Local file analysis fields:

- `durationSec`
- `distanceM`
- `heartRate`
- `elevation`
- `speed`
- `cadence`
- `power`
- `kmSamples` from `garmin fit parse`
- raw records from `activity dump` when drift, stability, or point-level pacing needs calculation

Cycling analysis checklist:

- Consistency and volume: ride count, frequency, total distance/duration, and weekly trend.
- Aerobic durability: long-ride duration, HR/power stability, training effect, and endurance score when present.
- Threshold: cycling FTP, W/kg, VO2 max, power zones, and sustained power evidence when present.
- Climbing: hill score, elevation gain, climbing-specific power/HR, and terrain context.
- Intensity: average/max HR, power, training load, and time in zones when present.
- Terrain: elevation gain and climbing impact.
- Technique: cadence consistency if present.
- Pacing: first half vs second half, per-distance sample changes.
- Readiness: current sleep/recovery and training readiness, reported separately from durable ability.
- Data quality: missing HR, cadence, power, GPS, or sparse records.
- Confidence: high when multiple independent metrics agree; lower when based on one ride, speed alone, stale weight, or missing sensors.

Fallback sequence for cycling ability gaps:

1. For missing FTP, run direct `training get --metric cycling_ftp`, then `max_metrics`, then inspect selected activity details/raw payloads. For missing VO2 max, run `max_metrics`, then inspect activity details/raw payloads.
2. For missing weight or W/kg, run body `weigh_ins` and `composition`; optionally inspect `profile get --raw`. Do not calculate W/kg without both weight and a relevant power value.
3. For missing splits, run `activity extended`; for missing HR/power zones, inspect `activity get --raw`, `profile get --raw`, and FIT analysis output. If still absent, use observed averages, maxima, and distributions instead of inventing zone boundaries.
4. For missing per-distance or point-level data, export or download FIT, then run `activity analyze`, `fit parse`, and, only when needed, `activity dump --max-records 0` on selected activities.
5. Only after the relevant checks should the answer list a data gap as unavailable. Phrase it as "not returned by the checked CLI calls" and include the commands checked.

## Failure Handling

- If `cycling-health` is unavailable, guide installation from `https://github.com/baijian/cycling-health`.
- If status says not logged in, run the appropriate `garmin login` command. For data queries, pick the region by login state: if neither is logged in, prompt login; if only one is logged in, query that region; if both are logged in and the user did not specify, default to `cn`.
- If DNS or proxy errors appear, ask the user whether a proxy/VPN is expected, then retry with the correct network setup.
- If a CN endpoint returns warnings but the main payload exists, report available data and list warnings.
- If `profile get` fails for CN, do not use that endpoint as token validation; prefer `garmin status` and real data queries.
- If `sleep list` returns `records: []` for a single date, treat it as inconclusive until adjacent-date sleep and summary fallback queries are checked.
- If a command returns JSON with `warnings`, include those warnings in the final answer.
