---
name: calin
description: Sync any ICS/iCal calendar to Microsoft Exchange as blocked time slots — supports recurring events, change detection, and privacy-preserving sync
version: 1.0.0
metadata:
  clawdbot:
    os: ["darwin"]
    requires:
      env:
        - CALINT_ICS_URL
        - CALINT_MS_CLIENT_ID
        - CALINT_MS_TENANT_ID
      bins:
        - python3
      config:
        - ~/.calintegration/.env
    primaryEnv: CALINT_ICS_URL
    files: ["*.py", "install.sh", "requirements.txt"]
  homepage: https://github.com/Blucaru/CalIn
---

# CalIn — ICS Calendar to Exchange Sync

Sync busy time from **any ICS/iCal calendar** to Microsoft Exchange as "Blocked" slots. Works with Google Calendar, iCloud, Outlook.com, Nextcloud, Fastmail, Proton Calendar, or any CalDAV server that publishes an ICS feed.

## When to Use This Skill

- User asks to sync calendars, block time, or mirror busy slots
- User wants personal calendar events to block time on their work calendar
- User asks to check sync status or clear synced events
- Scheduled background sync via Heartbeat (recommended: every 5-30 minutes)

## What It Does

- Fetches events (including recurring) from any HTTPS ICS feed
- Creates/updates/deletes corresponding "Blocked" events on Exchange via Microsoft Graph API
- Tracks synced events with a local mapping file — only touches what changed
- **Privacy-preserving**: only syncs time slots, never event titles, descriptions, or attendees

## Setup

### 1. Install dependencies

Requires Python 3.12+.

```bash
cd ~/.openclaw/skills/calin
bash install.sh
```

This creates a Python venv and installs `icalendar`, `msal`, `recurring-ical-events`, and `requests`.

### 2. Configure credentials

Add to `~/.calintegration/.env` (created by installer with chmod 600):

```
CALINT_ICS_URL=<your-ics-feed-url>
CALINT_MS_CLIENT_ID=<azure-app-client-id>
CALINT_MS_TENANT_ID=<azure-app-tenant-id>
# Optional: sync to a specific Exchange calendar (defaults to primary)
# CALINT_MS_CALENDAR_ID=<calendar-id>
```

**Where to find your ICS URL:**

| Provider | Location |
|----------|----------|
| Google Calendar | Settings > your calendar > Integrate > "Secret address in iCal format" |
| iCloud | Calendar app > right-click calendar > Share > Public Calendar > copy URL |
| Outlook.com | Settings > Calendar > Shared calendars > Publish > ICS link |
| Nextcloud | Calendar > three-dot menu > Copy subscription link |
| Fastmail | Settings > Calendars > Share/export > ICS URL |

**Azure AD app** (free, no client secret needed):
1. Go to https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade
2. New registration > Name: "CalIn" > Redirect URI: Public client > `http://localhost:8400`
3. API permissions > Add > Microsoft Graph > Delegated > Calendars.ReadWrite
4. Copy Application (client) ID and Directory (tenant) ID

### 3. Authenticate Microsoft

```bash
cd ~/.openclaw/skills/calin
venv/bin/python main.py setup
```

This opens a browser for one-time Microsoft login. Tokens are cached locally.

## Commands

Run these from the skill directory:

| Command | What it does |
|---------|-------------|
| `venv/bin/python main.py sync` | Run one sync cycle |
| `venv/bin/python main.py status` | Show last sync time and event count |
| `venv/bin/python main.py clear` | Remove all synced events from Exchange |
| `venv/bin/python main.py setup` | Re-run authentication setup |

## Automated Sync (macOS)

The installer generates a launchd plist for automatic sync every 5 minutes:

```bash
cd ~/.openclaw/skills/calin
bash install.sh
cp com.calintegration.sync.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.calintegration.sync.plist
```

## How It Works

1. Fetches the ICS feed and expands all recurring events within a 14-day window
2. Compares against the local event map (previous sync state)
3. For each event:
   - **New**: Creates a "Blocked" event on Exchange
   - **Changed** (time moved): Updates the Exchange event
   - **Deleted** from source: Deletes the Exchange event
4. Saves updated event map and last sync timestamp

Change detection uses a hash of start time + end time + all-day flag. Only changed events trigger API calls.

## Security and Privacy

- **Credentials** stored in `~/.calintegration/.env` with chmod 600 permissions
- **Tokens** stored in `~/.calintegration/ms_token.json` with chmod 600 permissions
- **All files** in `~/.calintegration/` directory with chmod 700
- **No event details synced** — only time slots are transmitted. Event titles, descriptions, attendees, and locations are never sent to Exchange
- **HTTPS only** — ICS URLs must use HTTPS; Graph API calls use TLS with certificate verification
- **No client secret** — uses PKCE (Proof Key for Code Exchange) for Microsoft auth
- **ICS URL validated** — rejects non-HTTPS schemes to prevent SSRF
- **API path IDs validated** — prevents injection in Graph API endpoint construction
- **All HTTP requests** have 30-second timeouts to prevent hanging

### External endpoints called

| Endpoint | Purpose | Auth |
|----------|---------|------|
| Your ICS URL (HTTPS) | Read calendar events | URL contains secret token |
| `login.microsoftonline.com` | Microsoft OAuth token exchange | PKCE flow |
| `graph.microsoft.com/v1.0` | Create/update/delete Exchange events | Bearer token |

### Data flow

```
ICS Feed (read-only) --> [CalIn on your machine] --> Microsoft Graph API (write)
                              |
                     ~/.calintegration/ (local state)
```

No data is sent to any third party. All processing happens locally.
