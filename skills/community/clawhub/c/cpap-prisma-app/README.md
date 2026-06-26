---
name: cpap-prisma-app
version: 1.1.0
description: Fetches CPAP therapy data from the PrismaAPP API (Löwenstein Medical) and writes a daily Obsidian log note. Use when the user says "CPAP log", "sleep therapy", "CPAP data", "prisma log", "CPAP today", "CPAP yesterday", or when the daily cron triggers CPAP logging.
---

# CPAP PrismaAPP Log Skill

Fetches CPAP therapy data from the Löwenstein PrismaAPP backend API and writes structured daily Obsidian notes.

## Supported Devices

Any Löwenstein Medical CPAP/APAP/BiLevel device paired with the **PrismaAPP** (com.lmt.sleeppatientapp). Tested with the prisma SOFT max.

## Setup

> **Note:** `config.json` contains your personal credentials and is listed in `.gitignore`. Never publish or share it. Only `config.example.json` is tracked.

1. Copy `config.example.json` to `config.json`
2. Fill in your PrismaAPP credentials and vault path
3. Optionally set `"language"` to one of: `en`, `de`, `fr`, `es`, `it`, `pt`, `pl`, `el`, `sr`

```bash
cp config.example.json config.json
# Edit config.json
```

**config.json fields:**

| Field | Description | Default |
|-------|-------------|---------|
| `email` | PrismaAPP account e-mail | required |
| `password` | PrismaAPP account password | required |
| `timezone` | IANA timezone string | `Europe/Berlin` |
| `vault_path` | Absolute path to your Obsidian vault | required |
| `log_dir` | Note output folder relative to vault | `30 Bereiche/Gesundheit/CPAP/Logs` |
| `language` | Locale for note text | `en` |

## Usage

```bash
# Yesterday (default — ideal for a daily cron job):
python3 scripts/fetch-cpap.py

# Specific date:
python3 scripts/fetch-cpap.py 2026-04-06

# Backfill all data since first device sync:
python3 scripts/fetch-cpap.py --all

# Backfill from a specific date:
python3 scripts/fetch-cpap.py --from=2026-03-01
```

## API Reference

All API calls use `https://my.prismacloud.com` as the base URL.

> ⚠️ `bucharest.prismacloud.cc` is the web SPA frontend — it returns HTML for all paths and cannot be used as an API endpoint.

| Endpoint | Description |
|----------|-------------|
| `POST /connect/token` | OAuth2 password grant → access token |
| `GET /api/Dashboard` | Returns `minDate` (first sync) and `serialNumber` |
| `GET /api/Dashboard/week?dateInWeek=YYYY-MM-DD` | Week data (7 days) |

**Authentication** uses OAuth2 Resource Owner Password Credentials (`grant_type=password`) with `Content-Type: application/x-www-form-urlencoded`. The token expires after 3600 seconds.

## Output Format

File: `<vault_path>/<log_dir>/YYYY-MM-DD.md`

```yaml
---
date: 2026-04-06
weekday: Monday
tags: ["health", "cpap", "auto-generated", "good"]
source: PrismaAPP / Löwenstein prisma SOFT max
created: 2026-04-08T18:17
---
```

Sections: Summary table · Sleep · CPAP Therapy · Snoring & Mask · Navigation links

## Metrics Explained

| Metric | Source field | Unit |
|--------|-------------|------|
| Sleep duration | `sleepTimeInMinutes` | min |
| Deep sleep | `deepSleepInMinutes` | min |
| AHI (Apnoea-Hypopnoea Index) | `ahi` | events/h |
| Leakage | `leakage` | L/min |
| Snoring | `snoringPercent` | % of sleep time |
| Mask fit | `maskFitPercentage` | % |
| Pressure | `apapMinPressure` / `apapMaxPressure` | hPa |

## Localisation

Note text is fully localised. Available locales: `en` `de` `fr` `es` `it` `pt` `pl` `el` `sr`

Set `"language": "de"` in `config.json` for German notes, etc.

## Privacy Note

This skill accesses personal medical data from your PrismaAPP account using your own credentials. Data is only read — no writes are made to the API. All data is stored locally in your Obsidian vault.
