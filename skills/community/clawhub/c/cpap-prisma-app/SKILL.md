---
name: cpap-prisma-app
version: 1.1.0
description: Fetches CPAP therapy data from the PrismaAPP API (Löwenstein Medical) and writes a daily Obsidian log note. Use when the user says "CPAP log", "sleep therapy", "CPAP data", "prisma log", "CPAP today", "CPAP yesterday", or when the daily cron triggers CPAP logging.
---

# CPAP PrismaAPP Log Skill

Automatically fetches CPAP therapy data from the Löwenstein PrismaAPP backend and writes a structured daily Obsidian note.

## When Triggered

- User says: "CPAP log", "CPAP data", "write sleep therapy", "prisma log", "CPAP today/yesterday/[date]"
- Daily cron job fires (configurable)
- User requests a historical backfill

## Prerequisites

- Account at `my.prismacloud.com` with a linked Löwenstein CPAP device
- Device synced via the PrismaAPP mobile app (data must be uploaded to the server)
- Credentials stored in `skills/cpap-prisma-app/config.json`

## Execution

### Step 1: Run the Python script

**Yesterday (default):**
```bash
python3 ~/.openclaw/workspace/skills/cpap-prisma-app/scripts/fetch-cpap.py
```

**Specific date:**
```bash
python3 ~/.openclaw/workspace/skills/cpap-prisma-app/scripts/fetch-cpap.py 2026-04-06
```

**Backfill all data since first sync:**
```bash
python3 ~/.openclaw/workspace/skills/cpap-prisma-app/scripts/fetch-cpap.py --all
```

**Backfill from a specific date:**
```bash
python3 ~/.openclaw/workspace/skills/cpap-prisma-app/scripts/fetch-cpap.py --from=2026-03-01
```

### Step 2: Confirm output

The script prints a summary and writes the note to:
```
<vault_path>/<log_dir>/YYYY-MM-DD.md
```

## Output Format (Note)

The generated note contains:
- Frontmatter: date, weekday, tags (including quality tag), source, created timestamp
- Summary table: sleep duration, deep sleep, AHI, leakage, snoring %, mask fit %, therapy mode/pressure
- Overall quality rating (🟢/🟡/🟠/🔴) derived from AHI, leakage, and deep sleep scores
- Detailed sections: Sleep, CPAP Therapy, Snoring & Mask
- Navigation links to the previous and next logged day

All text is fully localised — see the `locales/` folder.

## Quality Mapping

| API value | Label | Meaning |
|-----------|-------|---------|
| 0 | 🟢 Good | Optimal |
| 1 | 🟡 Okay | Acceptable |
| 2 | 🔴 Poor | Needs attention |
| 3 | 🟠 Borderline | Monitor closely |
| 4 | — | No data |

## AHI Reference

| AHI | Classification |
|-----|---------------|
| < 5 | Normal |
| 5–15 | Mild |
| 15–30 | Moderate |
| > 30 | Severe |

## Troubleshooting

**No data for date:**
- Check whether the device was used that night
- Open PrismaAPP on the phone to trigger a Bluetooth sync
- Data only appears after the device has synced with the app

**Login error:**
- Verify credentials in `config.json`
- Check that `my.prismacloud.com` is reachable
- A password change in PrismaAPP requires a `config.json` update

**Wrong API responses (HTML instead of JSON):**
- Always use `my.prismacloud.com` as the API base
- `bucharest.prismacloud.cc` is the web SPA only — it returns HTML for all paths

## Cron Configuration (daily at 18:17)

```
17 18 * * * python3 /path/to/skills/cpap-prisma-app/scripts/fetch-cpap.py
```
