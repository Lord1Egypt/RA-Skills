# garmin-connect-health -- OpenClaw Skill

<div align="right">
  <a href="README.zh.md"><img src="https://img.shields.io/badge/语言-中文-red?style=for-the-badge&logo=googletranslate&logoColor=white" alt="中文"></a>
  &nbsp;
  <img src="https://img.shields.io/badge/Language-English-blue?style=for-the-badge&logo=googletranslate&logoColor=white" alt="English">
</div>

A comprehensive Garmin Connect skill for [OpenClaw](https://github.com/openclaw/openclaw) that fetches your complete health & fitness data and makes it queryable by your AI agent.

## Features

- **40+ health metrics** -- sleep, HRV, stress, body battery, SpO2, VO2 Max, training status, race predictions, and more
- **Structured JSON + SQLite output** -- daily snapshots plus queryable tables for trends and workouts
- **Multiple auth methods** -- env vars, CLI args, macOS Keychain, or credentials file
- **Auto-caches daily data** -- fast queries without repeated API calls
- **Workout detail tables** -- activities and strength-training sets are saved for deeper analysis
- **Cross-platform** -- macOS, Linux, Windows

## Screenshots

> AI-powered health analysis powered by this skill -- real data, real insights 💪

<div align="center">
  <img src="docs/screenshot-1.jpg" width="380" alt="Garmin health data overview -- steps, sleep, HRV, body battery, SpO2">
  &nbsp;&nbsp;
  <img src="docs/screenshot-2.jpg" width="380" alt="Detailed training analysis and recovery recommendations">
</div>

*Left: Full health snapshot including sleep, heart rate, body battery, blood oxygen, and HRV.*
*Right: Training review with aerobic/anaerobic effect breakdown and personalized recovery advice.*

## Quick Start

```bash
# Install dependency
pip install garminconnect

# Set credentials
export GARMIN_EMAIL="you@example.com"
export GARMIN_PASSWORD="yourpassword"

# Fetch today's data
python3 garmin_health.py

# Show cached data
python3 garmin_health.py --show
```

## Installation

### Manual
1. Copy `garmin_health.py` and `SKILL.md` to your OpenClaw skills directory
2. Install the Python dependency: `pip install garminconnect`
3. Configure credentials (see Setup section)

### First Run & MFA
Your first login may trigger MFA. You'll be prompted to enter the verification code sent to your Garmin account email. After successful login, an OAuth token is cached for future use.

## Data Storage

The skill writes both local JSON snapshots and a local SQLite database:

- `~/.garmin_health/YYYY-MM-DD.json` -- daily JSON snapshot
- `~/.garmin_health/latest.json` -- latest JSON snapshot
- `~/.garmin_health/garmin.db` -- SQLite database with `daily_summary`, `activities`, and `activity_sets` tables

No data is uploaded by this skill; storage stays on your machine unless you explicitly share it.

## Data Schema Example

The values below are synthetic examples, not real user data.

```json
{
  "date": "2026-05-07",
  "fetched_at": "2026-05-07T21:00:00",
  "steps": 8432,
  "calories": 2380.0,
  "active_calories": 520.0,
  "distance_meters": 6100,
  "resting_heart_rate": 56,
  "heart_rate_min": 48,
  "heart_rate_max": 142,
  "sleep_hours": 7.4,
  "sleep_score": 84,
  "sleep_deep_seconds": 7500,
  "sleep_rem_seconds": 2580,
  "hrv_last_night_avg": 70,
  "hrv_last_night_5min_high": 107,
  "hrv_weekly_avg": 72,
  "hrv_status": "BALANCED",
  "body_battery_start": 69,
  "body_battery_end": 11,
  "body_battery_max": 80,
  "body_battery_min": 5,
  "spo2_avg": 93.0,
  "stress_avg": 39,
  "training_status": "Recovery",
  "training_load_acute": 109,
  "training_load_chronic": 219,
  "training_load_ratio": 0.4,
  "training_readiness_score": 54,
  "vo2max": 47.5,
  "endurance_score": 5268,
  "activities": [
    {
      "name": "力量训练",
      "type": "strength_training",
      "duration_minutes": 47,
      "calories": 440,
      "avg_hr": 125,
      "max_hr": 164
    }
  ]
}
```

See full schema in [SKILL.md](SKILL.md).

## Region: Global vs China (CN)

By default the skill connects to the **global** Garmin Connect (`connect.garmin.com`).  
If your Garmin account was registered in China, or you are running from a mainland China IP, switch to the **CN endpoint** (`connect.garmin.com.cn`) for better reliability:

### One-time setup (recommended)

Add to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.) so it applies to every run:

```bash
export GARMIN_IS_CN=true
```

Then reload your shell:

```bash
source ~/.zshrc   # or ~/.bashrc
```

That's it -- you never need to pass a flag again.

### Per-run flag (ad-hoc)

```bash
python3 garmin_health.py --cn
```

### For OpenClaw skill users

The skill reads `GARMIN_IS_CN` automatically. Set it once in your shell profile (above) and all future skill invocations -- including those triggered by your AI agent -- will use the CN endpoint without any extra configuration.

> **Not sure which endpoint to use?**  
> If you registered your Garmin account on the Chinese Garmin website or app, use CN. If you registered on garmin.com (international), use the default (no flag needed).

## Credential Priority

1. `--email` / `--password` CLI arguments
2. `GARMIN_EMAIL` / `GARMIN_PASSWORD` environment variables
3. macOS Keychain (service: `garmin_connect`)
4. `~/.garmin_credentials` file (format: `email=...\npassword=...`)

## FAQ

**Q: What devices are supported?**
A: Any Garmin watch/fitness tracker that syncs to Garmin Connect. Some features (body battery, SpO2) depend on device capabilities.

**Q: Can I use this without OpenClaw?**
A: Absolutely. It's a standalone Python script that outputs JSON.

**Q: My body composition data is empty**
A: You need a Garmin Index smart scale connected to your account.

**Q: Is my data sent anywhere?**
A: No. Data is fetched locally and stored as JSON/SQLite files on your machine.

## Acknowledgments

- [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) -- excellent Garmin API wrapper

## License

MIT-0
