---
name: fitbit-tracker
description: Personal Fitbit (by Google) integration for daily health tracking with adaptive sleep and activity reporting
version: 0.2.3
triggers:
  - "how did I sleep"
  - "fitbit sleep"
  - "sleep report"
  - "fitbit"
  - "fitbit health"
  - "fitbit steps"
  - "fitbit activity"
  - "full report"
  - "daily summary"
permissions:
  network:
    - api.fitbit.com
  env:
    - FITBIT_CLIENT_ID
    - FITBIT_CLIENT_SECRET
    - FITBIT_REDIRECT_URI
    - FITBIT_TZ
    - FITBIT_SCOPES
  file:
    - read/write: ~/.config/openclaw/fitbit/token.json (OAuth tokens, one-time setup)
    - write: optional, only when --out flag is supplied to fetch/normalize scripts
  shell: none
  setup:
    - One-time OAuth callback server on FITBIT_REDIRECT_URI (default localhost:8080) — only runs during initial authentication
metadata:
  clawdbot:
    emoji: "💪"
    requires:
      bins: [python3]
    config:
      env:
        FITBIT_CLIENT_ID:
          description: Fitbit OAuth client ID
          required: true
        FITBIT_CLIENT_SECRET:
          description: Fitbit OAuth client secret
          required: true
        FITBIT_REDIRECT_URI:
          description: OAuth redirect URI (typically http://localhost:8080)
          required: true
        FITBIT_TZ:
          description: Timezone for date calculations (e.g. Europe/London)
          default: UTC
---

# Fitbit Tracker

Effortless health monitoring powered by the official **Fitbit (by Google)** API. No apps, no dashboards — just ask and get your health stats instantly.

## Features

### Smart Sleep Tracking
- Automatically separates naps from main sleep
- Reports duration, efficiency, and all sleep stages (Deep, Light, REM, Wake)
- Nap detection with separate reporting

### Complete Activity Picture
- Steps, calories, distance, active minutes
- Resting heart rate
- Heart rate zones (Out of Range, Fat Burn, Cardio, Peak)

### Adaptive Reporting
Only shows what you ask for — no unnecessary data.

| You say... | Reports... |
|-------------|-----------|
| "how did I sleep" / "sleep" | Duration, efficiency, all stages, nap |
| "just my steps" | Steps only |
| "activity today" | Steps, calories, distance, active mins, HR zones |
| "full report" / "everything" / "summary" | All available data |
| "fitbit" / "health" | Complete daily summary |

### Clean Formatting
- Numbers formatted for readability (e.g., "8,234 steps")
- Stages grouped logically
- No raw data dumps

## Data Available

**Sleep:**
- Duration (total sleep time)
- Sleep efficiency %
- Sleep score (when available)
- Sleep stages: Deep, Light, REM, Wake
- Nap duration (when taken)

**Activity:**
- Steps
- Calories (total + BMR)
- Distance (km)
- Resting heart rate
- Active minutes (Very Active, Fairly, Lightly, Sedentary)
- Heart rate zones

## Fitbit OAuth Scopes (why each is needed)

The Fitbit OAuth flow requests these scopes by default (override via `FITBIT_SCOPES` env var):

| Scope | Purpose | Why needed |
|---|---|---|
| `activity` | Daily activity summary | Steps, calories, distance, active minutes |
| `sleep` | Sleep records | Duration, efficiency, stages, naps |
| `heartrate` | Heart rate data | Resting HR + HR zones |
| `profile` | User profile basics | Display name, timezone alignment |
| `weight` | Body weight | Optional — included by default for completeness |

The OAuth is **one-time setup** — the callback server runs only during initial authentication, then tokens are stored locally and auto-refreshed.

## Setup

### 1. Create Fitbit Developer App

1. Go to [dev.fitbit.com](https://dev.fitbit.com)
2. Log in and click **Register an App**
3. Fill in:
   - **Application Name**: OpenClaw Fitbit (or any name)
   - **Description**: Fitbit integration for OpenClaw
   - **Application Website**: `https://github.com/yourusername/openclaw`
   - **OAuth 2.0 Application Type**: Choose **Personal**
   - **Callback URL**: `http://localhost:8080` (for local) or your redirect URI
4. Accept the terms and register
5. Copy your **Client ID** and **Client Secret**

### 2. Configure Environment Variables

```bash
export FITBIT_CLIENT_ID="your_client_id"
export FITBIT_CLIENT_SECRET="your_client_secret"
export FITBIT_REDIRECT_URI="http://localhost:8080"
export FITBIT_TZ="Europe/London"  # Your timezone
```

Or add to `~/.openclaw/.env`:
```
FITBIT_CLIENT_ID=your_client_id
FITBIT_CLIENT_SECRET=your_client_secret
FITBIT_REDIRECT_URI=http://localhost:8080
FITBIT_TZ=Europe/London
```

### 3. Authenticate

Run the OAuth login script:
```bash
python3 scripts/fitbit_oauth_login.py
```

This will:
- Open Fitbit authorization page in your browser
- Ask you to approve access
- Exchange the code for tokens
- Save tokens to `~/.config/openclaw/fitbit/token.json`

Tokens are automatically refreshed when they expire.

## Commands

The skill uses a 3-step pipeline:

```bash
# Step 1: Fetch raw data from Fitbit API
# IMPORTANT: For sleep queries (morning), use --date today not yesterday!
# Fitbit returns last night's sleep under today's date.
python3 scripts/fitbit_fetch_daily.py --date today --out /tmp/fitbit_raw.json

# Step 2: Normalize into clean format (extracts actual sleep time, stages, activity)
python3 scripts/fitbit_normalize_daily.py /tmp/fitbit_raw.json --out /tmp/fitbit_day.json

# Step 3: Render for display (use --channel discord, telegram, or generic)
python3 scripts/fitbit_render.py /tmp/fitbit_day.json --channel discord
```

For a specific date (YYYY-MM-DD format):
```bash
python3 scripts/fitbit_fetch_daily.py --date 2026-03-25 --out /tmp/fitbit_raw.json
```

For sleep section only:
```bash
python3 scripts/fitbit_render.py /tmp/fitbit_day.json --channel discord --section sleep
```

**Critical date rule:** When user asks about sleep in the morning (e.g., "how did I sleep"), use `--date today`. Fitbit's sleep API associates sleep with the date you woke up, so last night's sleep (Mar 25 11pm → Mar 26 7am) appears under date "today" (Mar 26). Only use `--date yesterday` for activity-only queries when you specifically want the previous full day's activity data.

**Important:** Always run the full pipeline (fetch → normalize → render). Never use raw API `duration` field directly — it includes wake periods inside the sleep window. The normalized `duration_minutes` field (which maps to Fitbit's `minutesAsleep`) is the actual sleep time.

## Usage Examples

**Sleep report:**
```
Fitbit — 2026-03-21
- Sleep: 7h 32m (score 85) | 93% efficiency
  - Stages: Deep: 1h 42m, Light: 3h 20m, REM: 1h 45m, Wake: 45m
- Nap: 1h 6m
```

**Full daily summary:**
```
Fitbit — 2026-03-21
- Sleep: 7h 32m (score 85) | 93% efficiency
  - Stages: Deep: 1h 42m, Light: 3h 20m, REM: 1h 45m, Wake: 45m
- Nap: 1h 6m
- Steps: 8,234
- Calories: 1,892 (1,048 BMR)
- Distance: 6.2 km
- Resting HR: 58 bpm
  - Active mins: V. Active: 45m, Fair: 23m, Light: 1h 24m, Sedentary: 8h 12m
  - HR Zones: Out of Range: 12h, Fat Burn: 1h 30m, Cardio: 32m, Peak: 8m
```

**Steps only:**
```
- Steps: 8,234
```

## Python Dependencies

No third-party dependencies required. Uses Python standard library:
- `urllib.request` - HTTP requests
- `json` - JSON parsing
- `datetime` - Date handling
- `zoneinfo` - Timezone support (Python 3.9+)

## Troubleshooting

### "Missing env var: FITBIT_CLIENT_ID"
Environment variables not loaded. Source your `.env` file or ensure variables are set in the gateway environment:
```bash
source ~/.openclaw/.env
```

### "Token expired" error
Tokens auto-refresh. If you see this error repeatedly:
1. Delete `~/.config/openclaw/fitbit/token.json`
2. Re-run `python3 scripts/fitbit_oauth_login.py`

### "No data found for this day"
- Check `FITBIT_TZ` matches your timezone
- Try `--date yesterday` to confirm data exists
- Verify Fitbit account has data for the date

### Nap not separating from main sleep
This may indicate `isMainSleep` flag isn't set correctly on your Fitbit account. The skill filters records by this flag — some older Fitbit devices don't set it properly.

### Sleep score not showing
Not all Fitbit accounts/devices provide sleep scores. This is a Fitbit API limitation, not the skill. Efficiency and stages are always reported when available.

## API Endpoints Used

- `GET /1/user/-/activities/date/{date}.json` - Daily activity summary
- `GET /1.2/user/-/sleep/date/{date}.json` - Sleep records

## References

- API details: `references/fitbit_api.md`
- Output schema: `references/output_schema.md`
