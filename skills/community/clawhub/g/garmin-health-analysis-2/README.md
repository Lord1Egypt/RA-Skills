# Garmin Health Analysis

> Talk to your Garmin data naturally. Sleep, HRV, Body Battery, training
> readiness, activity splits, and the Garmin calendar: trips, races and events.

**Forked from [eversonl/ClawdBot-garmin-health-analysis](https://github.com/eversonl/ClawdBot-garmin-health-analysis).**
The original was a solid start but had gone quiet for over six months
([issue 5](https://github.com/eversonl/ClawdBot-garmin-health-analysis/issues/5))
and did not cover what I needed: per-activity splits, auth resilience, extended
metrics, time-based queries, and the calendar. This fork adds all of that.

## What's Different Here

| Feature | Original | This Fork |
|---------|----------|-----------|
| Activity splits (per-km/lap HR + pace) | no | yes |
| Auth resilience (429 retry, token fallback, legacy migration) | no | yes |
| Time-based queries ("what was my HR at 3pm?") | no | yes |
| Extended metrics (VO2max, training readiness, endurance score) | no | yes |
| FIT/GPX file download and analysis | no | yes |
| Per-second activity detail queries | no | yes |
| Interactive HTML dashboards | no | yes |
| Calendar: trips, races/events, naps, weigh-ins | no | yes |
| Jet Lag Adviser trips: create / replace / delete | no | yes |

## Installation

```bash
pip3 install 'garminconnect>=0.3.18' curl_cffi fitparse gpxpy
python3 scripts/garmin_auth.py login
```

`garminconnect >= 0.3.18` is required for the Jet Lag Adviser trip API. That
release also dropped the old `garth` dependency.

Destructive trip operations (`trip-delete`, `trip-update`) are **read-only by
default**: they preview the change and exit 2, and only act when passed
`--confirm-delete` / `--confirm-update`.

Full setup guide in [SKILL.md](SKILL.md).

## What You Can Do

- "How did I sleep last night?" — sleep hours, stages, score
- "Show me my last run with splits" — per-km pace, HR, cadence
- "What's my recovery like this week?" — Body Battery, HRV, readiness
- "What trips do I have coming up?" — future trips from the Garmin calendar
- "Add a trip" — create a Jet Lag Adviser trip from the CLI
- "Delete that trip" — gated: the CLI previews first and needs `--confirm-delete`
- "What races did I run?" — races/events with dates and links
- "Is my VO2max improving?" — trend over time
- "Download the GPX for Sunday's run" — route data
- "What was my heart rate at 3pm yesterday?" — time-based queries

## What's Included

```text
scripts/
├── garmin_auth.py              # Login, token refresh, credential resolution
├── garmin_data.py              # Core metrics: sleep, HRV, Body Battery, activities
├── garmin_data_extended.py     # VO2max, training readiness, endurance score
├── garmin_calendar.py          # Calendar: trips, races, events + trip create/update/delete
├── garmin_activity_files.py    # FIT/GPX download and analysis
├── garmin_query.py             # Time-based queries
└── garmin_chart.py             # HTML dashboard generation
```

## License

Apache 2.0. See [LICENSE](LICENSE).

## Credits

Original by EversonL. Extended by bolinches.
