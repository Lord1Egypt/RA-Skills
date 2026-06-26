---
name: calendar-crab
description: Google Calendar CLI — list, create, move, and delete events. Zero dependencies, just Node.js + Google OAuth.
---

# Calendar Crab

Google Calendar management via a single Node.js script. No npm install needed.

## Prerequisites

- Node.js 18+
- Google Cloud project with Calendar API enabled
- OAuth credentials + refresh token saved to `~/.openclaw/secrets/` (see Setup below)

## Commands

### List upcoming events
```bash
node calendar-crab.js list --days=7 --max=20
```

### Create an event
```bash
node calendar-crab.js create \
  --title="Team Sync" \
  --date=2026-03-20 \
  --time=10:00 \
  --duration=30 \
  --location="Zoom" \
  --attendees="alice@co.com,bob@co.com" \
  --description="Weekly sync" \
  --tz="America/Los_Angeles"
```

### Move an event
```bash
# By date + time
node calendar-crab.js move --date=2026-03-20 --from=10:00 --to=14:00

# By event ID
node calendar-crab.js move --id="EVENT_ID" --to="2026-03-20T14:00:00-07:00"
```

### Delete an event
```bash
node calendar-crab.js delete --id="EVENT_ID"
node calendar-crab.js delete --date=2026-03-20 --time=10:00
```

## Configuration

| Env var | Default | Description |
|---------|---------|-------------|
| `CALENDAR_CRAB_SECRETS` | `~/.openclaw/secrets` | Directory containing OAuth + token JSON files |
| `CALENDAR_CRAB_TZ` | System local | Default timezone for events |
| `CALENDAR_CRAB_CALENDAR` | `primary` | Google Calendar ID |

Timezone can also be set per-command with `--tz=America/Los_Angeles`.

## Execution rules

1. Always `list` first to verify the target event exists and is unique.
2. `move` and `delete` auto-notify all attendees (`sendUpdates=all`).
3. On failure, the raw Google API error is returned for debugging.

## Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/) and create a project.
2. Enable the **Google Calendar API**.
3. Create OAuth 2.0 credentials (Desktop app type).
4. Save the credentials as `~/.openclaw/secrets/google-calendar-oauth.json`:
   ```json
   {
     "client_id": "YOUR_CLIENT_ID",
     "client_secret": "YOUR_CLIENT_SECRET"
   }
   ```
5. Obtain a refresh token via the OAuth flow and save as `~/.openclaw/secrets/google-calendar-token.json`:
   ```json
   {
     "refresh_token": "YOUR_REFRESH_TOKEN",
     "access_token": "",
     "expires_in": 0,
     "obtained_at": ""
   }
   ```
   The script auto-refreshes the access token using the refresh token.
