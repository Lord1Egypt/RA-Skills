---
name: amazfit-health-log
version: 1.0.0
description: Fetches Amazfit GTR3 health data from HCGateway and writes a daily Obsidian log note. Use when user says "health log", "GTR3 data", "write health data", "fetch health data", or when the daily cron triggers health logging.
---

# Amazfit GTR3 Health Log Skill

Automatically fetches Amazfit GTR3 health data from HCGateway and writes a structured daily Obsidian note.

## When Triggered

- User says: "health log", "fetch GTR3 data", "write health data", "health log for yesterday/today/[date]"
- Daily cron job runs at 06:00 (configurable)

## Prerequisites

- HCGateway is running at `http://127.0.0.1:6644`
- Docker containers `hcgateway_api` + `hcgateway_db` are active
- HCGateway Android app has completed at least one sync (auto-syncs every 2h)
- Credentials stored in `skills/amazfit-health-log/config.json`

## Execution

### Step 1: Verify container status

```bash
docker ps --filter "name=hcgateway" --format "{{.Names}}: {{.Status}}"
```

If containers are not running:
```bash
sudo docker compose -f /home/docker/hcgateway/docker-compose.yml up -d
```

### Step 2: Run the Python script

**For yesterday (default):**
```bash
python3 ~/.openclaw/workspace/skills/amazfit-health-log/scripts/fetch-health.py
```

**For a specific date:**
```bash
python3 ~/.openclaw/workspace/skills/amazfit-health-log/scripts/fetch-health.py 2026-04-06
```

### Step 3: Confirm output

The script prints a summary and writes the note to:
```
<VAULT_ROOT>/30 Bereiche/Gesundheit/Logs/GTR3/YYYY-MM-DD.md
```

## Output Format (Note)

The generated note contains:
- Frontmatter: date, weekday, tags, source, created timestamp
- Summary table: steps, distance, sleep duration, resting HR, SpO2
- Sleep section: period, duration, stage breakdown table (Deep / REM / Light / Awake)
- Heart rate section: avg, min, max, resting HR
- SpO2 section: daily average
- Navigation links to previous and next day

## Sleep Stage Decoding

| Code | Stage  |
|------|--------|
| 1    | Awake  |
| 4    | Light  |
| 5    | Deep   |
| 6    | REM    |

## Troubleshooting

**No data for date:**
- Check that Zepp App → Health Connect sync is enabled
- Open the HCGateway Android app and trigger a manual sync
- Data is only available for the last 30 days

**Containers unreachable:**
```bash
sudo docker compose -f /home/docker/hcgateway/docker-compose.yml logs --tail=20
```

**Changing credentials:**
- Edit `skills/amazfit-health-log/config.json`
- Password changes invalidate all existing tokens (re-login required)

## Cron Configuration (daily at 06:00)

For automatic daily execution:
```
0 6 * * * python3 /home/openclaw/.openclaw/workspace/skills/amazfit-health-log/scripts/fetch-health.py
```

## Data Sources

| Type | HCGateway Endpoint | Source |
|------|--------------------|--------|
| Steps | `/fetch/steps` | com.huami.watch.hmwatchmanager |
| Sleep | `/fetch/sleepSession` | com.huami.watch.hmwatchmanager |
| Heart Rate | `/fetch/heartRate` | com.huami.watch.hmwatchmanager |
| Resting HR | `/fetch/restingHeartRate` | com.huami.watch.hmwatchmanager |
| SpO2 | `/fetch/oxygenSaturation` | com.huami.watch.hmwatchmanager |
| Distance | `/fetch/distance` | com.huami.watch.hmwatchmanager |
