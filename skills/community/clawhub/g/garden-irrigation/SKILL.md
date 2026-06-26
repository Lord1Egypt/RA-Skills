---
name: garden-irrigation
description: "Smart garden irrigation — reads soil sensors (avg of last 50 readings), checks weather, and decides when and how long to water each zone. Use when the user asks: 'should I water today?', 'run irrigation report', 'water the garden', 'irrigation status'. Requires TUYA_ACCESS_ID, TUYA_ACCESS_SECRET."
license: MIT
metadata: {"openclaw":{"emoji":"🌱","primaryEnv":"TUYA_ACCESS_ID","requires":{"env":["TUYA_ACCESS_ID","TUYA_ACCESS_SECRET","TUYA_API_ENDPOINT"],"bins":["python3"]}}}
---

# garden-irrigation

Automated irrigation skill for greenhouse and outdoor garden zones. Reads Tuya soil sensors (avg of last 50 readings, looking back up to 7 days), fetches rolling 7-day weather history + 3-day forecast from Open-Meteo, and makes deficit-based watering decisions. Generates a bilingual (EN/ZH) Markdown report on every run.

## Tools

### `irrigation_report` — report only, no valve actuation

Read all sensors, fetch weather, compute decision for every zone, and generate a report. **Does not open any valves.**

```bash
python scripts/run_with_notifications.py
```

Use when the user asks: *"should I water today?"*, *"garden status"*, *"irrigation report"*, *"今天需要浇水吗？"*

### `run_irrigation` — full automation

Read sensors, fetch weather, decide, and **open valves automatically** if soil moisture is below the zone threshold. Respects `automation` config (enabled, max minutes per session).

```bash
python scripts/run_once.py
```

Use when the user asks: *"water the garden"*, *"run irrigation"*, *"start watering"*

### `run_irrigation_with_confirmation` — confirm before watering

Same as `run_irrigation` but prompts `y/n` on stdin before opening each valve. For each zone that needs water it prints the zone name, suggested duration, and reason, then waits for interactive input. Zones where the user answers `n` are skipped and logged as cancelled.

```bash
python scripts/run_with_confirmation.py
```

None of the three scripts accept CLI arguments — all configuration is read from `config/system.json` and `config/zones.json`.

## Decision logic

For each zone:

```
avg_moisture = mean(last 50 humidity readings per sensor, looking back up to 7 days)
                └─ falls back to current reading if Tuya logs API unavailable

recent_rain_mm  = sum of precipitation_sum over the last 7 days (Open-Meteo history)
forecast_rain_mm = precipitation_sum for the next 1 day (Open-Meteo forecast)

if avg_moisture < target_moisture_min (default 30%):
    deficit  = target_moisture_min - avg_moisture
    minutes  = default_minutes + round(deficit / 5)   ← +1 min per 5% deficit
    if zone is rain_sensitive AND (recent_rain_mm ≥ 8 OR forecast_rain_mm ≥ 5):
        minutes -= 4
    if any of the last 3 irrigation log entries exist for this zone:
        minutes -= 1                                  ← recently watered penalty
    minutes = clamp(0, minutes, max_minutes)
    → water if minutes > 0
else:
    → skip  (reason: "within target range" if ≤ target_moisture_max, else "above target range")
```

## Zone configuration (`config/zones.json`)

| Zone | Target | Default | Max | Rain-sensitive |
|---|---|---|---|---|
| Greenhouse | 30–50% | 6 min | 20 min | No |
| Outdoor Garden | 30–50% | 8 min | 25 min | Yes |

Edit `config/zones.json` to set your device IDs:
- `soil_sensor_ids` — list of Tuya soil sensor device IDs for the zone
- `valve.device_id` — Tuya water valve device ID
- `valve.switch_code` / `valve.countdown_code` — DP codes (e.g. `switch_1`, `countdown_1`)

## System configuration (`config/system.json`)

Key settings:
- `location.name` / `latitude` / `longitude` — used for weather lookup
- `timezone` — e.g. `Europe/Oslo`
- `language` — `"auto"` (follows query language), `"en"`, or `"zh"`
- `automation.enabled` — master switch for valve actuation
- `automation.max_minutes_per_session` — safety cap (default 20 min)
- `automation.require_confirmation` — if `true`, `run_once.py` skips actuation (use `run_with_confirmation.py` instead)

Reporting / notification settings (all under `reporting`):
- `enabled` — must be `true` for any notification to be sent
- `send_report_to_bot` — must also be `true` to actually send
- `send_on_irrigation` — send when watering is triggered (default `true`)
- `send_on_no_irrigation` — send even when no watering needed (default `false`)
- `bot_account_id` — OpenClaw account ID of the bot that sends the message
- `bot_target` — destination the bot sends to (e.g. a Telegram chat ID)

## Report format

Every run produces a Markdown report saved to `data/reports/` and (if configured) sent via Telegram:

```
# 🌱 Daily Irrigation Report
*Generated at: YYYY-MM-DD HH:MM UTC*

## 🌤️ Weather Summary
## 📡 Device Status        ← per sensor: avg (last 50 readings) + current moisture, temp, battery
## 💧 Irrigation Decision  ← per zone: should water, duration, reason
```

Data is written to `../data/` relative to the skill folder (created automatically). Config files from `../config/` override local config on every run.

## Setup

```bash
# .env (project root)
TUYA_ACCESS_ID=your_access_id
TUYA_ACCESS_SECRET=your_access_secret
TUYA_API_ENDPOINT=https://openapi.tuyaeu.com
```

Requires the **tuya-cloud** skill installed alongside this skill.

## Troubleshooting

| Symptom | Fix |
|---|---|
| "No sensor data" in report | Check `soil_sensor_ids` in `config/zones.json`; verify device is online in Tuya app |
| Soil moisture avg shows `—` | Tuya logs API rate-limited from too many recent queries — wait a few minutes and retry |
| Valve does not open | Check `valve.device_id` and DP codes in `config/zones.json`; test with `tuya_control_device` |
| Weather section shows `—` | Network error fetching Open-Meteo; check internet connection |
| Report not sent to Telegram | Check `reporting` config in `config/system.json`: `enabled` and `send_report_to_bot` must both be `true`; `bot_account_id` and `bot_target` must be set; `send_on_no_irrigation` must be `true` if you expect a report on dry days |