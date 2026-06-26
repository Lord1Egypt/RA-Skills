# garden-irrigation

Automated garden irrigation skill — reads Tuya soil sensors (24h average), checks rolling weather history + forecast, and decides when and how long to water each zone. Generates a bilingual Markdown report on every run.

## Dependencies

Requires the **[tuya-cloud](https://clawhub.ai/minshi-veyt/tuya-cloud)** skill to communicate with Tuya IoT devices. Install and configure it before using this skill.

## What it does

- reads all zone soil sensors via `tuya-cloud` (uses 24h average humidity, falls back to current)
- fetches rolling 7-day rain history + 3-day forecast from Open-Meteo (no API key needed)
- computes a deficit-based watering decision per zone
- opens valves automatically (or with confirmation, or report-only — see scripts below)
- writes sensor and decision history to `data/` as JSONL
- generates a Markdown daily report (EN or ZH based on query language)
- sends report via Telegram if configured

## Run

```bash
# Decision + report only — no valve actuation
python3 scripts/run_with_notifications.py

# Full automation — opens valve if moisture is below threshold
python3 scripts/run_once.py

# Ask y/n before opening valve
python3 scripts/run_with_confirmation.py
```

## Configuration

### `config/zones.json` — zones, sensors, valves

Each zone needs:
- `soil_sensor_ids` — list of Tuya device IDs for soil moisture sensors
- `valve.device_id` — Tuya device ID for the water valve
- `valve.switch_code` / `valve.countdown_code` — DP codes (e.g. `switch_1`, `countdown_1`)
- `target_moisture_min` / `target_moisture_max` — moisture target range in %
- `default_minutes` / `max_minutes` — base and max watering duration
- `rain_sensitive` — if `true`, reduces watering when recent or forecast rain is significant

For **dual-channel valves** (e.g. SGW02), each channel is independent:
- Channel 1: `switch_1` / `countdown_1`
- Channel 2: `switch_2` / `countdown_2`

### `config/system.json` — system-wide settings

| Field | Description |
|---|---|
| `location.name` / `latitude` / `longitude` | Location for weather lookup |
| `timezone` | IANA timezone, e.g. `Europe/Oslo` |
| `language` | `"auto"` (follows query language), `"en"`, or `"zh"` |
| `automation.enabled` | Master switch for valve actuation |
| `automation.require_confirmation` | If `true`, valve won't open without user approval |
| `automation.max_minutes_per_session` | Hard cap on valve-open time per run |
| `reporting.bot_target` | Telegram destination, e.g. `telegram:1234567890` |

### Environment variables (`.env` at project root)

```bash
TUYA_ACCESS_ID=your_access_id
TUYA_ACCESS_SECRET=your_access_secret
TUYA_API_ENDPOINT=https://openapi.tuyaeu.com   # EU; adjust for your region
```

## Decision logic

```
avg_moisture = mean(24h humidity readings)   # falls back to current if unavailable

if avg_moisture < target_moisture_min:
    minutes = default_minutes + round(deficit / 5)
    if rain_sensitive AND (recent_rain ≥ 8mm OR forecast_rain ≥ 5mm): minutes -= 4
    if recently watered: minutes -= 1
    minutes = clamp(0, minutes, max_minutes)
    → water
else:
    → skip
```

## Data storage

| Path | Contents |
|---|---|
| `data/soil/<zone_id>.jsonl` | Sensor readings per run |
| `data/irrigation/<zone_id>.jsonl` | Decisions and execution results per run |
| `data/reports/daily-<timestamp>.md` | Markdown report per run |