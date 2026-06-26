# Fitbit Training Schema

## Tables

### sync_runs
- id (pk)
- started_at
- finished_at
- status (ok|partial|error)
- scope (sync-day|backfill)
- requested_date
- details_json

### daily_metrics
- date (pk)
- steps
- distance_km
- calories_out
- floors
- active_zone_minutes
- resting_hr
- hrv_rmssd
- sleep_minutes
- sleep_efficiency
- sleep_score
- readiness_state
- readiness_confidence
- reasons_json
- pp_recommendation
- data_quality (complete|partial|degraded)
- updated_at

### quality_flags
- id (pk)
- date
- level (info|warn|error)
- flag
- message
- created_at

## Derived readiness rules (v2)

Baseline-first (personalized):
- red if any severe deviation vs baseline (sleep debt large, RHR spike, HRV suppression)
- amber for moderate deviations
- fallback to absolute thresholds only when baseline is unavailable (<7 days)

Confidence:
- high: sleep + rhr + hrv present
- medium: any 2 present
- low: <=1 present

Data quality:
- complete: all endpoint pulls succeeded
- partial: some endpoint failures
- degraded: many endpoint failures (>=4)
