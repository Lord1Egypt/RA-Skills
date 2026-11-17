# Intervals.icu CLI Workflows

Use this reference for Garmin CN Wellness synchronization and Intervals.icu cycling analysis through `cycling-health`.

## Contents

- [Authentication](#authentication)
- [Garmin Wellness Sync](#garmin-wellness-sync)
- [Wellness And Training Health](#wellness-and-training-health)
- [Cycling Activities](#cycling-activities)
- [Power Analysis](#power-analysis)
- [Statistics](#statistics)
- [Settings And Calendar Events](#settings-and-calendar-events)
- [Comparison Recipes](#comparison-recipes)
- [Analysis Rules](#analysis-rules)
- [Failure Handling](#failure-handling)

## Authentication

Verify that the installed release exposes the needed command before querying
credentials or data:

```bash
cycling-health intervals --help
cycling-health intervals wellness sync --help
```

For analysis-only tasks, replace the second check with the relevant `activity`,
`power`, `stats`, or `wellness get` help command. If the command is absent after
the normal CLI upgrade, report an outdated public release instead of building
an ad hoc API client.

Check the saved Intervals.icu credentials without exposing the API key:

```bash
cycling-health intervals athlete --output json
```

If credentials are missing, let the user provide the API key through a trusted local terminal and validate it before saving:

```bash
INTERVALS_ICU_API_KEY=... cycling-health intervals auth \
  --athlete-id i12345 --output json
```

Never request or print the API key in chat. The CLI can also read `--api-key-file` or profile-isolated saved credentials.

Garmin CN Wellness sync additionally requires:

```bash
cycling-health garmin status --region cn --output json
```

## Garmin Wellness Sync

Default seven-day preview:

```bash
cycling-health intervals wellness sync \
  --source garmin-cn --days 7 --output json
```

Explicit-range preview and write:

```bash
cycling-health intervals wellness sync \
  --source garmin-cn --start YYYY-MM-DD --end YYYY-MM-DD \
  --output json

cycling-health intervals wellness sync \
  --source garmin-cn --start YYYY-MM-DD --end YYYY-MM-DD \
  --confirm --output json
```

Conflict replacement, only after explicit approval:

```bash
cycling-health intervals wellness sync \
  --source garmin-cn --start YYYY-MM-DD --end YYYY-MM-DD \
  --overwrite --confirm --output json
```

Use `garmin-cn` by default. Do not sync `garmin-global` merely because the flag exists: Intervals.icu can ingest Garmin Global through its native Garmin connection, and an extra CLI source can create unnecessary conflicts. Use `--source garmin-global` only when the user explicitly requests it and understands the overlap.

Automatic fields:

- `sleepSecs`: Garmin total sleep seconds.
- `sleepScore`: Garmin overall sleep score.
- `avgSleepingHR`: average sleeping heart rate.
- `hrv`: Garmin last-night average HRV.
- `restingHR`: daily resting heart rate.
- `spO2`: Garmin daily average SpO2.
- `respiration`: average sleeping respiration.
- `steps`: daily total steps.

The CLI omits absent values and expected 404 no-data responses. It does not map sleep stages, Garmin device stress, Body Battery, training readiness, calories burned, training load, weight, body fat, or hydration.

Preview output:

- `status: dry-run`, `mode: preview`: no Intervals.icu write occurred.
- `data[].action`: `create`, `update`, `conflict`, `unchanged`, or `empty`.
- `data[].changes`: fields that would be written.
- `data[].conflicts`: differing non-empty target values skipped without `--overwrite`.
- `changedRecords`, `changedFields`, `conflictFields`: preview totals.

Confirmed output:

- `status: success`, `mode: write`.
- `uploadedRecords`: date records sent through the bulk endpoint.
- `verifiedRecords`: records successfully read back and matched.

Always preview first. If the preview is unchanged, stop. A normal confirmed sync fills missing fields and leaves conflicts untouched; `--overwrite` is a separate destructive decision.

## Wellness And Training Health

Daily Wellness queries:

```bash
cycling-health intervals wellness get --date YYYY-MM-DD --output json
cycling-health intervals wellness get --days 7 --output json
cycling-health intervals wellness get \
  --start YYYY-MM-DD --end YYYY-MM-DD \
  --fields sleepSecs,sleepScore,avgSleepingHR,hrv,restingHR,spO2,respiration,steps \
  --output json
```

Use Wellness for daily sleep, HRV, resting heart rate, vitals, steps, body measurements, and subjective fields when present. A single-date query cannot be combined with `--fields`.

Training-health query:

```bash
cycling-health intervals stats summary --days 30 --output json
cycling-health intervals stats summary \
  --start YYYY-MM-DD --end YYYY-MM-DD --output json
```

Keep these concepts separate:

- Daily health/recovery: sleep, HRV, resting HR, SpO2, respiration, steps, weight, soreness, fatigue, stress, mood, and readiness when present in Wellness.
- Training health: Intervals.icu fitness, fatigue, form, ramp rate, training load, eFTP, and eFTP/kg from aggregate statistics.
- Current decision: recent recovery plus current load/form.
- Durable fitness: multi-week activity, load, and power trends.

Do not infer that uploaded Wellness values necessarily drive every Intervals.icu readiness or coaching feature. Analyze observed values and their trend only.

## Cycling Activities

List or search before requesting large activity details:

```bash
cycling-health intervals activity list --days 30 --limit 100 --output json
cycling-health intervals activity list \
  --start YYYY-MM-DD --end YYYY-MM-DD --limit 100 --output json
cycling-health intervals activity search --query climb --limit 20 --output json
cycling-health intervals activity search --query climb --full --output json
```

Activity lists can include multiple sports. Select cycling records by returned activity type, normally `Ride`, rather than assuming every item is a ride.

Single-activity detail:

```bash
cycling-health intervals activity get \
  --activity-id ACTIVITY_ID --output json
cycling-health intervals activity get \
  --activity-id ACTIVITY_ID --include-intervals --output json
cycling-health intervals activity intervals \
  --activity-id ACTIVITY_ID --output json
```

Streams and best efforts can be large. Request only what the analysis needs:

```bash
cycling-health intervals activity streams \
  --activity-id ACTIVITY_ID --types watts,heartrate,cadence --output json
cycling-health intervals activity best-efforts \
  --activity-id ACTIVITY_ID --stream watts --duration 300 --output json
```

Activity analysis data:

```bash
cycling-health intervals activity data \
  --activity-id ACTIVITY_ID --metric power_curve --output json
cycling-health intervals activity data \
  --activity-id ACTIVITY_ID --metric power_vs_hr --output json
cycling-health intervals activity data \
  --activity-id ACTIVITY_ID --metric time_at_hr --output json
cycling-health intervals activity data \
  --activity-id ACTIVITY_ID --metric power_histogram --bucket-size 25 --output json
cycling-health intervals activity data \
  --activity-id ACTIVITY_ID --metric interval_stats \
  --start-index START --end-index END --output json
```

Other supported metrics include `weather`, `segments`, `hr_curve`, `pace_curve`, `hr_histogram`, `pace_histogram`, `gap_histogram`, `map`, `hr_load_model`, and `power_spike_model`.

Use activity detail for summary metrics, structured intervals for workout execution, best efforts for fixed-duration comparisons, and streams only for drift, pacing, cadence, or point-level questions.

## Power Analysis

Current modeled ability:

```bash
cycling-health intervals power model --sport Ride --output json
```

Short-term, annual, and all-time curves:

```bash
cycling-health intervals power curves \
  --curves 42d,1y,all --sport Ride --output json
```

Add `--include-ranks` only for percentile questions. Use `--model MS_2P|MORTON_3P|FFT_CURVES|ECP` only when the requested model matters.

Per-activity power at standard durations:

```bash
cycling-health intervals power activities \
  --days 90 --durations 5,60,300,1200,3600 \
  --sport Ride --output json
```

Power versus heart rate:

```bash
cycling-health intervals power hr-curve \
  --days 90 --sport Ride --output json
```

Interpretation guide:

- 5-15 seconds: neuromuscular/sprint evidence.
- 60 seconds: anaerobic capacity evidence.
- 300 seconds: VO2-range evidence.
- 1200 seconds: sustained threshold-adjacent evidence.
- 3600 seconds: long threshold/endurance evidence.
- MMP model: current critical power, W-prime, P-max, and FTP when present.
- HR curve: power-heart-rate relationship and cadence context, not proof of causation.

Use the source activity IDs returned by curves to inspect the rides that produced important points. Do not equate one peak point with repeatable current ability without recent supporting efforts.

## Statistics

Recent aggregate summary:

```bash
cycling-health intervals stats summary --days 30 --output json
```

Explicit range or tag subset:

```bash
cycling-health intervals stats summary \
  --start YYYY-MM-DD --end YYYY-MM-DD --output json
cycling-health intervals stats summary \
  --start YYYY-MM-DD --end YYYY-MM-DD --tags TAG1,TAG2 --output json
```

Inspect fitness-model overrides only when a discontinuity needs explanation:

```bash
cycling-health intervals stats fitness-events --output json
```

Statistics can include activity count, time, moving/elapsed time, distance, elevation, calories, training load, sRPE, eFTP, eFTP/kg, fitness, fatigue, form, ramp rate, weight, time in zones, and sport-category breakdowns. These are Intervals.icu server calculations; do not silently recompute them.

## Settings And Calendar Events

These commands include writes. Read the current state first, build a complete
reviewable JSON file, and run `--dry-run` before a live request.

Basic and device settings:

```bash
cycling-health intervals settings get --output json
cycling-health intervals settings device --device-class phone --output json
cycling-health intervals settings update --file settings.json --dry-run --output json
cycling-health intervals settings update --file settings.json --output json
```

The CLI restricts basic-settings updates to its supported whitelist. Device UI
settings are read-only. Run the final update only after the user has reviewed
the preview and clearly authorized the live change.

Sport settings:

```bash
cycling-health intervals sport-settings list --output json
cycling-health intervals sport-settings get --settings-id Ride --output json
cycling-health intervals sport-settings update \
  --settings-id Ride --file ride-settings.json --dry-run --output json
cycling-health intervals sport-settings update \
  --settings-id Ride --file ride-settings.json --output json
```

Intervals.icu documents sport-setting updates as full-object replacement, not
field-level patching. Start from the object returned by `get` or `list`, edit
that complete object, and preview it. Add `--recalc-hr-zones` only when the user
explicitly wants Intervals.icu to recalculate zones.

Calendar event queries and writes:

```bash
cycling-health intervals event list \
  --start YYYY-MM-DD --end YYYY-MM-DD --category RACE_A,RACE_B --output json
cycling-health intervals event get --event-id EVENT_ID --output json
cycling-health intervals event upload --file events.json --dry-run --output json
cycling-health intervals event upload --file events.json --output json
cycling-health intervals event delete --event-id EVENT_ID --output json
cycling-health intervals event delete --event-id EVENT_ID --confirm --output json
```

Every source-owned upload object needs a stable unique `external_id`. The CLI
uses it to find an existing event before create/update, rejects duplicate
external IDs in a bulk file, and treats server `uid` as read-only. A delete
without `--confirm` is only a preview. Do not perform the live upload or delete
until the user has authorized it.

There is no `event sync-garmin` command. To transfer a Garmin race, query the
Garmin event, explicitly map its date, sport, category, distance, name, tags,
and stable source ID to reviewed Intervals.icu event JSON, dry-run that JSON,
and only then upload it. Do not infer race priority (`RACE_A`, `RACE_B`, or
`RACE_C`) when the user has not chosen one.

## Comparison Recipes

The CLI does not expose a synthetic `compare` command. Run matched read-only
queries for the selected periods or activities, then compare the returned
fields locally using the rules below.

### Recent Block Versus Previous Block

Run `stats summary` for two adjacent, non-overlapping ranges of equal length. Compare ride count, duration, distance, elevation, load, eFTP/eFTP/kg, fitness, fatigue, form, and ramp rate. State both exact ranges.

### Current Power Versus Longer Baseline

Use `power curves --curves 42d,1y,all` for aligned duration points. Add `power activities --days 90` to determine whether the recent curve comes from one outlier or repeated rides. Compare watts and W/kg only when reliable weight is present.

### Ride Versus Ride

Identify each ride with list/search, fetch both details, then request identical best-effort durations and equivalent interval or stream metrics. Control for route, elevation, weather, moving time, sensor availability, and workout intent. Do not compare average speed across dissimilar terrain as a fitness test.

### Recovery Versus Performance

Query Wellness for the ride dates and a personal baseline window, then compare sleep, HRV, resting HR, and other available recovery values with ride load/power. Describe association and confidence; do not claim that one metric caused the performance.

### Efficiency And Durability

Use activity `power_vs_hr`, selected watts/heartrate streams, interval stats, or the athlete `power hr-curve`. Compare equivalent steady sections and account for heat, elevation, fatigue, coasting, and sensor dropouts.

## Analysis Rules

- Lead with the question's answer, not an endpoint inventory.
- Label Garmin and Intervals.icu values when both sources are used.
- Keep date ranges, timezone, sport, durations, and units aligned.
- Prefer medians or repeated evidence when outliers dominate averages.
- Report absolute change and percentage change; omit percentage when the baseline is zero or missing.
- Use W/kg only when watts and a reliable weight exist; state the weight date if stale.
- Distinguish `fitness`/CTL, `fatigue`/ATL, and `form`; do not call any one of them general health.
- Treat eFTP and modeled FTP as estimates and distinguish them from Garmin cycling FTP or a tested threshold.
- Do not double-count the same ride when it appears in Garmin and Intervals.icu.
- Empty lists are valid no-data results. Do not convert them into invented data gaps.

Recommended report structure:

1. Conclusion.
2. Date range and source coverage.
3. Health/recovery context.
4. Activity volume and load.
5. Power and efficiency evidence.
6. Comparison with baseline or selected rides.
7. Confidence, missing sensors/fields, and next action.

## Failure Handling

- Missing Intervals command after CLI upgrade: report that the installed public release is too old; do not silently substitute raw `curl` calls.
- Missing Intervals credentials: direct the user to `intervals auth`; never ask for the API key in chat.
- Missing Garmin CN login during Wellness sync: direct the user to `garmin login --region cn`.
- Preview contains conflicts: leave them untouched unless the user explicitly approves `--overwrite`.
- Settings or sport-settings update: require a successful dry run and explicit authorization before the live request; do not reconstruct a partial sport-settings object from memory.
- Event upload: require a stable `external_id` and successful dry run; stop on duplicate matches. Event deletion remains a preview until `--confirm` is explicitly authorized.
- Confirmed sync reports fewer verified than uploaded records or returns a read-back error: report the write as unverified and do not claim success.
- HTTP 429 or transient server failures: the CLI retries safe GET/PUT requests; preserve the final error if retries are exhausted.
- Empty activity, power, statistics, or Wellness results: widen the range only when it is relevant, and state that the checked range returned no matching data.
- Missing power: distinguish no power meter/sensor coverage from an API failure before drawing power conclusions.
- Mixed sports in activity/statistics output: isolate `Ride` data for cycling conclusions.
