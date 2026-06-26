# Changelog

## v1.0.11 — 2026-05-31

### Fixed
- Added compatibility for newer `garminconnect` activity detail APIs by supporting both `get_activity()` and `get_activity_details()`.
- Handle activity summary payloads returned as `summaryDTO`, `activitySummary`, or `summary`.
- Derive strength-training active set and rep totals from exercise-set details when summary fields are missing.
- Accept race prediction responses returned as either a list or a dict.
- Handle alternate training readiness feedback fields more safely.

## v1.0.10 — 2026-05-07

### Docs
- Restored the original real-product screenshots after owner review and approval.

## v1.0.9 — 2026-05-07

### Added
- Added SQLite storage at `~/.garmin_health/garmin.db` alongside JSON snapshots.
- Added structured tables for daily summaries, activities, and strength-training sets.
- Added richer workout detail capture for running, cycling, walking/hiking, badminton/racquet sports, cardio, and strength training.

### Fixed
- Handle Garmin training status null/missing fields more safely.

### Privacy
- Replaced public README screenshots with synthetic demo data.

## v1.0.3 — 2026-03-26

### Docs
- README (EN/ZH) and SKILL.md: added CN endpoint setup section with one-time `GARMIN_IS_CN` env var instructions
- SKILL.md: added `--cn` usage example and `GARMIN_IS_CN` to env var table

## v1.0.2 — 2026-03-26

### Added
- `--cn` CLI flag and `GARMIN_IS_CN=true` env var to switch to Garmin Connect CN (`connect.garmin.com.cn`). Recommended for Chinese Garmin accounts or when running from a mainland China IP. Default remains global.

## v1.0.1 — 2026-03-26

### Fixed
- `get_client()`: now tries `garth.load()` + profile validation first before falling back to email/password login. This prevents hammering the Garmin SSO endpoint on every run, which was causing 429 Too Many Requests errors for users running the script frequently (e.g. via cron).

## v1.0.0 — 2026-03-17

### Added
- Full Garmin Connect health data fetching (40+ metrics)
- Support for 14 data categories: daily summary, HR, sleep, stress, body battery, SpO2, respiration, HRV, training status/readiness, VO2 max, endurance, race predictions, weight/body composition, activities, weekly steps
- Multiple credential methods: CLI args, env vars, macOS Keychain, credentials file
- JSON caching per day + latest snapshot
- English UI with structured JSON output
- Cross-platform compatibility
