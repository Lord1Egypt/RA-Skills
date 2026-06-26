# Calendar Crab

Google Calendar CLI for [OpenClaw](https://github.com/pearyj/openclaw). List, create, move, and delete events from your terminal or let your AI agent manage your calendar.

**Zero dependencies** — just Node.js 18+ and Google OAuth credentials.

## Install

```bash
git clone https://github.com/pearyj/calendar-crab ~/.openclaw/skills/calendar-crab
```

## Quick start

```bash
# List next 7 days
node calendar-crab.js list

# Create an event
node calendar-crab.js create --title="Coffee" --date=2026-03-20 --time=09:00 --duration=30

# Move an event to a new time
node calendar-crab.js move --date=2026-03-20 --from=09:00 --to=11:00

# Delete an event
node calendar-crab.js delete --date=2026-03-20 --time=11:00
```

## Setup

You need a Google Cloud project with Calendar API enabled and OAuth credentials.

1. Create a project at [console.cloud.google.com](https://console.cloud.google.com/)
2. Enable **Google Calendar API**
3. Create **OAuth 2.0 credentials** (Desktop app)
4. Save credentials:

```bash
mkdir -p ~/.openclaw/secrets
```

`~/.openclaw/secrets/google-calendar-oauth.json`:
```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

5. Complete the OAuth flow to get a refresh token, then save:

`~/.openclaw/secrets/google-calendar-token.json`:
```json
{
  "refresh_token": "YOUR_REFRESH_TOKEN",
  "access_token": "",
  "expires_in": 0,
  "obtained_at": ""
}
```

The script auto-refreshes access tokens using the refresh token.

## Commands

| Command | Description |
|---------|-------------|
| `list` | List upcoming events (`--days=7 --max=20`) |
| `create` | Create event (`--title --date --time [--duration --location --attendees --description --tz]`) |
| `move` | Reschedule by time (`--date --from --to`) or by ID (`--id --to`) |
| `delete` | Delete by ID (`--id`) or by time (`--date --time`) |

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CALENDAR_CRAB_SECRETS` | `~/.openclaw/secrets` | Secrets directory path |
| `CALENDAR_CRAB_TZ` | System local | Default timezone |
| `CALENDAR_CRAB_CALENDAR` | `primary` | Calendar ID |

## How it works

Single Node.js file, no `node_modules`. Uses the Google Calendar REST API directly via `https`. Token refresh is automatic — once you have a refresh token, it just works.

## License

MIT
