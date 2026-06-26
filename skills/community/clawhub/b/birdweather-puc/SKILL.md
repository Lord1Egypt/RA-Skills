---
name: birdweather-puc
description: Access BirdWeather PUC station data — species detections, sensor readings (AQI, temperature, humidity, pressure, eCO₂, sound dB), and historical trends. Use when the user asks about backyard birds, what species were detected recently, air quality from a BirdWeather station, new species arrivals, or wants alerts when a species is detected for the first time. Requires a BirdWeather station token (free from app.birdweather.com). Triggers on phrases like "what birds have I heard", "new species today", "BirdWeather detections", "backyard birds", "PUC sensor readings".
---

# BirdWeather PUC

Fetch bird detections, species lists, and environmental sensor data from a BirdWeather PUC station.

## Setup

BirdWeather tokens are public (no auth required for read access). Find yours at:
`app.birdweather.com → Station Settings → Token`

Store token in environment or pass directly:
```bash
export BIRDWEATHER_TOKEN=your_token_here
```

## Core Script

Use `scripts/birdweather.py` for all data access:

```bash
# Daily summary — detections, species count, top birds, sensors
python3 scripts/birdweather.py summary --token TOKEN

# Recent detections (last N, default 10)
python3 scripts/birdweather.py detections --token TOKEN --limit 20

# Top species for a time period
python3 scripts/birdweather.py species --token TOKEN --period week

# Current sensor readings (AQI, temp, humidity, pressure, eCO₂, sound dB)
python3 scripts/birdweather.py sensors --token TOKEN

# Log sensor snapshot to SQLite (for history/trends)
python3 scripts/birdweather.py log --token TOKEN --db PATH_TO_DB

# Check for new species (first-ever detections vs. known catalog)
python3 scripts/birdweather.py new-species --token TOKEN --db PATH_TO_DB
```

All commands output JSON. Parse with `json.loads()` or pipe to `jq`.

## Workflows

### New Species Alert
1. Run `new-species` — compares live species list against DB catalog
2. If new species found: alert user with common name, scientific name, confidence, timestamp
3. Update DB with `log` command

### Daily Summary
1. Run `summary` for today's counts and top birds
2. Run `sensors` for current environmental readings
3. Combine into a brief — detections, species count, top 3-5 birds, AQI/temp

### Sensor Trend Analysis
1. Log regularly with `log --db` (add to cron/heartbeat)
2. Query SQLite `birdweather_sensor_history` table for trends
3. Look for AQI spikes, temperature patterns, sound level changes

## SQLite Schema

When using `--db`, two tables are maintained:

**`birdweather_species`** — cumulative species catalog:
```sql
species_id INTEGER, common_name TEXT, scientific_name TEXT,
color TEXT, thumbnail_url TEXT, first_detected_at TEXT,
detection_count INTEGER
```

**`birdweather_sensor_history`** — time-series sensor log:
```sql
id INTEGER PRIMARY KEY, recorded_at TEXT,
temp_f REAL, humidity REAL, pressure REAL,
aqi REAL, eco2 REAL, sound_db REAL, voc REAL
```

## API Reference

See `references/api.md` for full endpoint documentation.

## System Access

- **Network**: `app.birdweather.com/api/v1/stations/{token}/*` (read-only, no auth)
- **Disk**: SQLite DB at user-specified path (optional, only with `--db`)
- **No credentials stored** — token is passed per-invocation
