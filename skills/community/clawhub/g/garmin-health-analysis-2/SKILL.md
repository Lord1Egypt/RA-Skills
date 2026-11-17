---
name: garmin-health-analysis
description: Actively maintained fork of eversonl's original, which stopped at 1.2.2. Adds the Garmin calendar (races, events, naps, weigh-ins), Jet Lag Adviser trips (create, replace, delete, confirmation-gated), and ten extra metric tables (training status, fitness age, intensity minutes, morning readiness, hydration, hill score, calories, lactate threshold, training load balance). Talk to your Garmin data naturally, about sleep, HRV, Body Battery, or your heart rate at any time. Downloads FIT/GPX, generates interactive dashboards.
version: 1.6.1
author: EversonL, bolinches
homepage: https://github.com/bolinches/garmin-health-analysis
metadata: {"clawdbot":{"emoji":"⌚","requires":{"env":["GARMIN_EMAIL","GARMIN_PASSWORD"]},"install":[{"id":"garminconnect","kind":"python","package":"garminconnect>=0.3.18","label":"Install garminconnect (pip)"},{"id":"fitparse","kind":"python","package":"fitparse","label":"Install fitparse (pip)"},{"id":"gpxpy","kind":"python","package":"gpxpy","label":"Install gpxpy (pip)"}]}}
---

# Garmin Health Analysis

Query health metrics from Garmin Connect and generate interactive HTML charts.

**Forked from [eversonl/ClawdBot-garmin-health-analysis](https://github.com/eversonl/ClawdBot-garmin-health-analysis).**
The original had gone quiet for over six months
([issue 5](https://github.com/eversonl/ClawdBot-garmin-health-analysis/issues/5))
and did not cover what was needed here. This fork extends it.

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

## Two Installation Paths

This skill supports **two different setups**:

1. **OpenClaw Skill** (this guide) - Use with OpenClaw for automation and proactive health monitoring
2. **MCP Server** ([see MCP setup guide](references/mcp_setup.md)) - Use with standard Claude Desktop as an MCP server

Choose the path that matches your use case. You can also use both simultaneously!

---

## OpenClaw Skill Setup (first time only)

### 1. Install Dependencies

```bash
pip3 install 'garminconnect>=0.3.18' curl_cffi
```

### 2. Configure Credentials

You have three options to provide your Garmin Connect credentials:

#### Option A: OpenClaw Config (Recommended - UI configurable)

Add credentials to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "garmin-health-analysis": {
        "enabled": true,
        "env": {
          "GARMIN_EMAIL": "your-email@example.com",
          "GARMIN_PASSWORD": "your-password"
        }
      }
    }
  }
}
```

**Tip**: You can also set these through the OpenClaw UI in the Skills settings panel.

#### Option B: Local Config File

Create a config file in the skill directory:

```bash
cd ~/.openclaw/workspace/skills/garmin-health-analysis
cp config.example.json config.json
# Edit config.json and add your email and password
```

**config.json:**
```json
{
  "email": "your-email@example.com",
  "password": "your-password"
}
```

**Note**: `config.json` is gitignored to keep your credentials secure.

#### Option C: Command Line

Pass credentials directly when authenticating:
```bash
python3 scripts/garmin_auth.py login \
  --email YOUR_EMAIL@example.com \
  --password YOUR_PASSWORD
```

### 3. Authenticate

Login to Garmin Connect and save session tokens:

```bash
python3 scripts/garmin_auth.py login
```

This uses credentials from (in priority order):
1. Command line arguments (`--email`, `--password`)
2. Local config file (`config.json`)
3. Environment variables (`GARMIN_EMAIL`, `GARMIN_PASSWORD`)
4. OpenClaw config (`skills.entries.garmin-health-analysis.env`)

Session tokens are stored in `~/.openclaw/garmin/` and auto-refresh on subsequent calls.

If you have existing tokens from a previous version (`~/.garminconnect/`), they are automatically migrated on first use.

Check authentication status:
```bash
python3 scripts/garmin_auth.py status
```

## Fetching Data

Use `scripts/garmin_data.py` to get JSON data:

```bash
# Sleep (last 7 days default)
python3 scripts/garmin_data.py sleep --days 14

# Body Battery (Garmin's recovery metric)
python3 scripts/garmin_data.py body_battery --days 30

# HRV data
python3 scripts/garmin_data.py hrv --days 30

# Heart rate (resting, max, min)
python3 scripts/garmin_data.py heart_rate --days 7

# Activities/workouts (now includes activity_id)
python3 scripts/garmin_data.py activities --days 30

# Stress levels
python3 scripts/garmin_data.py stress --days 7

# Combined summary with averages
python3 scripts/garmin_data.py summary --days 7

# Custom date range
python3 scripts/garmin_data.py sleep --start 2026-01-01 --end 2026-01-15

# User profile
python3 scripts/garmin_data.py profile
```

### Activity Splits (per-lap data)

Get lap-by-lap data for a specific activity — average/max HR, speed, distance, power, cadence per lap:

```bash
# Get lap splits for an activity (use activities to find activity_id)
python3 scripts/garmin_data.py activity_splits --activity-id 600107330
```

Returns per-lap: `lap_index`, `distance_meters`, `duration_seconds`, `average_speed`, `max_speed`, `avg_hr`, `max_hr`, `calories`, `elevation_gain`, `average_power`, `normalized_power`, `average_run_cadence`, `intensity_type`, etc.

### Activity Detail (per-second time-series)

Get second-by-second data for a specific activity — heart rate, speed, distance, elevation, power, cadence, and more:

```bash
# All metrics, every second (full resolution)
python3 scripts/garmin_data.py activity_detail --activity-id 600107330

# Specific metrics only (faster, smaller output)
python3 scripts/garmin_data.py activity_detail --activity-id 600107330 \
  --metrics directHeartRate,directSpeed,sumDistance

# Sample every 30 seconds (good for quick overview of a long activity)
python3 scripts/garmin_data.py activity_detail --activity-id 600107330 \
  --sample-interval 30

# Common metrics:
#   directHeartRate   - Heart rate (bpm)
#   directSpeed       - Speed (m/s)
#   sumDistance        - Cumulative distance (m)
#   directElevation   - Elevation (m)
#   directPower       - Power (watts, running/cycling)
#   directRunCadence  - Cadence (spm for running)
#   directTimestamp   - Timestamp (ms epoch)
#   directLatitude    - Latitude
#   directLongitude   - Longitude
#   directGradeAdjustedSpeed - Grade-adjusted speed (m/s)
#   directVerticalOscillation - Vertical oscillation (cm)
#   directGroundContactTime  - Ground contact time (ms)
#   directStrideLength - Stride length (cm)
#   directVerticalRatio - Vertical ratio (%)
#   directPerformanceCondition - Performance condition
```

Output is JSON to stdout. Parse it to answer user questions.

## Calendar: Trips, Races, Events

Use `scripts/garmin_calendar.py` for anything about travel, races or calendar entries.
Trips and races are added in the Garmin app; this reads them back.

```bash
# Trips (past and FUTURE), grouped into windows
python3 scripts/garmin_calendar.py trips --months-back 14 --months-fwd 6

# Past trip days labelled with their Garmin trip name
python3 scripts/garmin_calendar.py trips --months-back 2 --with-names

# Races / events (title + URL)
python3 scripts/garmin_calendar.py races --months-back 24

# Everything, or a quick overview
python3 scripts/garmin_calendar.py calendar --months-back 12
python3 scripts/garmin_calendar.py summary --months-back 14 --months-fwd 4
```

Item types: `jetLagTrip` (trips), `event` (races, with title + URL), `nap`,
`userTimeChanged` (timezone change = flight day), `weight`, `wellnessActivity`,
`bloodpressure`, `activity`.

### Writing trips (Jet Lag Adviser)

Trips have their own API, separate from the calendar. It can **create, replace and
delete** them, so a trip can be added without the phone app:

```bash
# List trips (with their flights)
python3 scripts/garmin_calendar.py trip-list

# Add a trip
python3 scripts/garmin_calendar.py trip-add --start 2026-11-05 --end 2026-11-09 \
  --flights '[
    {"originLocation":"Helsinki, South Finland, Finland","originTimezone":"+02:00",
     "originTimestamp":"2026-11-05T15:45:00",
     "destinationLocation":"Dubai, United Arab Emirates","destinationTimezone":"+04:00",
     "destinationTimestamp":"2026-11-06T00:20:00"},
    {"originLocation":"Dubai, United Arab Emirates","originTimezone":"+04:00",
     "originTimestamp":"2026-11-09T08:25:00",
     "destinationLocation":"Helsinki, South Finland, Finland","destinationTimezone":"+02:00",
     "destinationTimestamp":"2026-11-09T13:55:00"}
  ]'

# Replace / remove
python3 scripts/garmin_calendar.py trip-update --trip-id ID --start ... --end ... --flights ...
python3 scripts/garmin_calendar.py trip-delete --trip-id ID
```

**Confirmation gate (destructive operations).** `trip-delete` and `trip-update`
change the Garmin account and cannot be undone from here, so both are
**read-only by default**. Without the flag they resolve the target, report
exactly what would change, and exit **2** having touched nothing:

```bash
# Previews only: prints the trip that would be deleted, changes nothing
python3 scripts/garmin_calendar.py trip-delete --trip-id ID

# Actually deletes
python3 scripts/garmin_calendar.py trip-delete --trip-id ID --confirm-delete

# Previews: shows the current trip beside the payload that would REPLACE it
python3 scripts/garmin_calendar.py trip-update --trip-id ID --start ... --end ... --flights ...
python3 scripts/garmin_calendar.py trip-update --trip-id ID --start ... --end ... --flights ... --confirm-update
```

Agent rule: run the preview first, show the user the exact trip (id, dates,
flights), and only re-run with `--confirm-*` after an explicit yes. Exit 2 means
"confirmation required, nothing happened", not success. `trip-add` creates a new
trip and is not gated.

**Flight fields** (all six required, one entry per leg, so a connection is two):
`originLocation`, `originTimezone`, `originTimestamp`, `destinationLocation`,
`destinationTimezone`, `destinationTimestamp`. Garmin does **not** geocode —
give the location as free text and the UTC offset (`+02:00`, `-07:00`) for that
date. Timestamps are **local time at that place, with no offset**.

Gotchas confirmed live 2026-10-17:
- A timestamp **without** a fractional second (`...T15:45:00`) is rejected with
  `HTTP 500`; with `...T15:45:00.0` it succeeds. The script normalises this for
  you, so either form may be passed.
- A trip whose dates overlap an existing trip is refused: `HTTP 400 "A trip
  already exists for this date range"`.
- Garmin auto-deletes a trip once it has ended and the user has re-adjusted to
  home time, so `trip-list` holds only current/recent trips. Older travel lives
  on as `jetLagTrip` day markers in the calendar, which is why both are kept.
- `trip-id` is required for update/delete and comes from `trip-list`.
- **`trip-update` is a full REPLACE**, not a patch: the flight list you pass
  becomes the whole trip, so an incomplete list silently drops legs. It is gated
  for that reason.

Requires `garminconnect >= 0.3.18`.

**Trips are the only place FUTURE travel appears.** `get_stats().isJetLagDay`
reports only days already lived, so anything about an upcoming trip must come from
the calendar. Future trip days have no `trip_name` (Garmin publishes the name only
after the day has passed); `--with-names` labels past days only.

## Generating Charts

Use `scripts/garmin_chart.py` for interactive HTML visualizations:

```bash
# Sleep analysis (hours + scores)
python3 scripts/garmin_chart.py sleep --days 30

# Body Battery recovery chart (color-coded)
python3 scripts/garmin_chart.py body_battery --days 30

# HRV & resting heart rate trends
python3 scripts/garmin_chart.py hrv --days 90

# Activities summary (by type, calories)
python3 scripts/garmin_chart.py activities --days 30

# Full dashboard (all 4 charts)
python3 scripts/garmin_chart.py dashboard --days 30

# Save to specific file
python3 scripts/garmin_chart.py dashboard --days 90 --output ~/Desktop/garmin-health.html
```

Charts open automatically in the default browser. They use Chart.js with a modern gradient design, stat cards, and interactive tooltips.

## Answering Questions

| User asks | Action |
|-----------|--------|
| "How did I sleep last night?" | `garmin_data.py summary --days 1`, report sleep hours + score |
| "How's my recovery this week?" | `garmin_data.py body_battery --days 7`, report average + trend |
| "Show me my health for the last month" | `garmin_chart.py dashboard --days 30` |
| "Is my HRV improving?" | `garmin_data.py hrv --days 30`, analyze trend |
| "What workouts did I do this week?" | `garmin_data.py activities --days 7`, list activities with details |
| "How's my resting heart rate?" | `garmin_data.py heart_rate --days 7`, report average + trend |
| "Show me my heart rate during my run" | `garmin_data.py activity_detail --activity-id ID --metrics directHeartRate,directSpeed --sample-interval 30` |
| "What were my lap splits?" | `garmin_data.py activity_splits --activity-id ID`, report per-lap HR + pace |
| "How did my pace change over the run?" | `garmin_data.py activity_detail --activity-id ID --metrics directSpeed,sumDistance --sample-interval 60` |
| "What trips do I have coming up?" | `garmin_calendar.py trips --months-fwd 6`, report future windows |
| "What races have I run?" | `garmin_calendar.py races --months-back 24`, list titles + dates |
| "When was I last away?" | `garmin_calendar.py trips --months-back 6 --with-names`, name the windows |

## Key Metrics

### Body Battery (0-100)
Garmin's proprietary recovery metric based on HRV, stress, sleep, and activity:
- **High (75-100)**: Fully recharged, ready for high intensity
- **Medium (50-74)**: Moderate energy, good for regular activity
- **Low (25-49)**: Limited energy, recovery needed
- **Very Low (0-24)**: Depleted, prioritize rest

### Sleep Scores (0-100)
Overall sleep quality based on duration, stages, and disturbances:
- **Excellent (90-100)**: Optimal restorative sleep
- **Good (80-89)**: Quality sleep with minor issues
- **Fair (60-79)**: Adequate but could improve
- **Poor (0-59)**: Significant sleep deficiencies

### HRV (Heart Rate Variability)
Measured in milliseconds, higher is generally better:
- Indicates nervous system balance and recovery capacity
- Track **trends** over time (increasing = improving recovery)
- Affected by sleep, stress, training load, illness
- Normal range varies by individual (20-200+ ms)

### Resting Heart Rate (bpm)
Lower generally indicates better cardiovascular fitness:
- **Athletes**: 40-60 bpm
- **Fit adults**: 60-70 bpm
- **Average adults**: 70-80 bpm
- Sudden increases may indicate stress, illness, or overtraining

### Stress Levels
Based on HRV analysis throughout the day:
- **Low stress**: Rest and recovery periods
- **Medium stress**: Normal daily activities
- **High stress**: Physical activity or mental pressure

## Health Analysis

When users ask for insights or want to understand their trends, use `references/health_analysis.md` for:
- Science-backed interpretation of all metrics
- Normal ranges by age and fitness level
- Pattern detection (weekly trends, recovery cycles, training load balance)
- Actionable recommendations based on data
- Warning signs that suggest rest or medical consultation

### Analysis workflow
1. Fetch data: `python3 scripts/garmin_data.py summary --days N`
2. Read `references/health_analysis.md` for interpretation framework
3. Apply the analysis framework: Status → Trends → Patterns → Insights → Recommendations
4. Always include disclaimer that this is informational, not medical advice

## Troubleshooting

### Authentication Issues
- **"Invalid credentials"**: Double-check email/password, try logging into Garmin Connect web
- **"Tokens expired"**: Run login again: `python3 scripts/garmin_auth.py login ...`
- **"Too many requests"**: Garmin rate-limits; wait a few minutes and try again

### Missing Data
- Some metrics require specific Garmin devices (Body Battery needs HRV-capable devices)
- Historical data may have gaps if device wasn't worn
- New accounts may have limited history

### Library Issues
- If `garminconnect` import fails: `pip3 install --upgrade 'garminconnect>=0.3.18'`
- Trip writing (Jet Lag Adviser) needs `garminconnect >= 0.3.18`; older versions
  have no trip methods at all. That release also dropped the old `garth` dep.
- Garmin occasionally changes their API; update the library if requests fail

## Privacy Note

- Credentials are stored locally in `~/.openclaw/garmin/` (tokenstore directory)
- Session tokens auto-refresh; if they expire, the module falls back to credentials from config/env
- Legacy tokens from `~/.garminconnect/` are automatically migrated on first use
- Rate-limited? The auth module retries once after 30s and tells you what to do
- No data is sent anywhere except to Garmin's official servers
- You can revoke access anytime by deleting the `~/.openclaw/garmin/` directory

## Comparison: Garmin vs Whoop

| Feature | Garmin | Whoop |
|---------|--------|-------|
| **Recovery metric** | Body Battery (0-100) | Recovery Score (0-100%) |
| **HRV tracking** | Yes (nightly average) | Yes (detailed) |
| **Sleep stages** | Light, Deep, REM, Awake | Light, SWS, REM, Awake |
| **Activity tracking** | Built-in GPS, many sport modes | Strain score (0-21) |
| **Stress** | All-day stress levels | Not directly tracked |
| **API** | Unofficial (garminconnect) | Official OAuth |
| **Device types** | Watches, fitness trackers | Wearable band only |

## References

- `README.md` — fork overview, feature diff and install summary
- `references/api.md` — Garmin Connect API details (unofficial)
- `references/health_analysis.md` — Science-backed health data interpretation
- [garminconnect library](https://github.com/cyberjunky/python-garminconnect) — Python API wrapper
- [Garmin Connect](https://connect.garmin.com) — Official web interface
- [This fork](https://github.com/bolinches/garmin-health-analysis) — source, issues

## Version Info

- **Created**: 2026-01-25
- **Authors**: EversonL (original), bolinches (fork and extensions)
- **Version**: 1.6.1
- **Dependencies**: garminconnect (>=0.3.18), curl_cffi, fitparse, gpxpy
- **License**: Apache 2.0
- **Trip API**: requires `garminconnect >= 0.3.18` (Jet Lag Adviser trips; that
  release also dropped the old `garth` dependency)
