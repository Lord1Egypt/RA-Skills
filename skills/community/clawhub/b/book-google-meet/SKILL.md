---
name: book-google-meet
description: Create scheduled Google Calendar events with OPEN access Google Meet spaces.
metadata:
  {
    "clawbot":
      {
        "emoji": "🎥",
        "requires":
          {
            "packages":
              [
                "google-auth",
                "google-auth-oauthlib",
                "google-api-python-client",
              ],
            "files": ["client_secrets.json", "book_meeting.py"],
            "primaryEnv": ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"],
            "writes": ["meeting_token.pickle"],
          },
        "install":
          [
            {
              "kind": "pip",
              "packages":
                [
                  "google-auth",
                  "google-auth-oauthlib",
                  "google-api-python-client",
                ],
              "label": "Install Python dependencies",
            },
          ],
      },
  }
---

# book-google-meet

Create scheduled Google Calendar events with **OPEN access** Google Meet spaces.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get OAuth credentials from Google Cloud Console
#    - Enable Google Calendar API and Google Meet API
#    - Create OAuth 2.0 Desktop app credentials
#    - Download client_secrets.json

# 3. Place client_secrets.json in the skill directory

# 4. Run the script
python book_meeting.py --title "My Meeting" --date "2026-03-12" --time "15:00" --duration 45 --timezone "Asia/Shanghai"
```

## Prerequisites

### 1. Google Cloud Project Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable APIs:
   - [Google Calendar API](https://console.developers.google.com/apis/api/calendar.googleapis.com/overview)
   - [Google Meet API](https://console.developers.google.com/apis/api/meet.googleapis.com/overview)

### 2. OAuth Consent Screen

1. Go to [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent)
2. Select **External** user type
3. Fill in app name and contact email
4. Add scope: `https://www.googleapis.com/auth/meetings.space.settings`
5. Set publishing status to **In production**

### 3. Create OAuth Credentials

1. Go to [Credentials](https://console.cloud.google.com/apis/credentials)
2. Click **Create Credentials** → **OAuth client ID**
3. Select **Desktop app** application type
4. Download JSON and save as `client_secrets.json`

**Alternative:** Set environment variables instead of using client_secrets.json:
```bash
export GOOGLE_CLIENT_ID='your-client-id'
export GOOGLE_CLIENT_SECRET='your-client-secret'
```

## Required OAuth Scopes

```
https://www.googleapis.com/auth/calendar.events
https://www.googleapis.com/auth/calendar
https://www.googleapis.com/auth/meetings.space.settings
```

**Note:** Use `meetings.space.settings` (non-sensitive) instead of `meetings.space.created` (sensitive).

## Usage

### Basic Usage

```bash
python book_meeting.py --title "Team Meeting" --date "2026-03-12" --time "15:00" --duration 45 --timezone "Asia/Shanghai"
```

### With Attendees

```bash
python book_meeting.py --title "Team Meeting" --date "2026-03-12" --time "15:00" --duration 45 \
  --timezone "Asia/Shanghai" \
  --attendees "user1@example.com,user2@example.com"
```

### With Description

```bash
python book_meeting.py --title "Team Meeting" --date "2026-03-12" --time "15:00" --duration 45 \
  --timezone "Asia/Shanghai" \
  --description "Weekly sync meeting"
```

### Access Types

```bash
# OPEN - Anyone with link can join (default)
python book_meeting.py --title "Public Meeting" --date "2026-03-12" --time "15:00" --duration 45 \
  --timezone "Asia/Shanghai" --access-type OPEN

# TRUSTED - Org members + invited external users
python book_meeting.py --title "Internal Meeting" --date "2026-03-12" --time "15:00" --duration 45 \
  --timezone "Asia/Shanghai" --access-type TRUSTED

# RESTRICTED - Only invitees
python book_meeting.py --title "Private Meeting" --date "2026-03-12" --time "15:00" --duration 45 \
  --timezone "Asia/Shanghai" --access-type RESTRICTED
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--title`, `-t` | Meeting title (required) | - |
| `--date`, `-d` | Meeting date (YYYY-MM-DD) | - |
| `--time` | Meeting start time (HH:MM) | - |
| `--duration` | Duration in minutes | 45 |
| `--timezone`, `-z` | Timezone | America/New_York |
| `--attendees` | Comma-separated email list | - |
| `--description` | Meeting description | - |
| `--access-type` | OPEN, TRUSTED, or RESTRICTED | OPEN |
| `--credentials`, `-c` | Path to client_secrets.json | client_secrets.json |
| `--token-path` | Path to store OAuth token | meeting_token.pickle |

## Output Example

```
🚀 Step 1: Creating Calendar event with Meet conference...
✅ Calendar event created with Meet conference
   Meeting Code: abc-defg-hij

🚀 Step 2: Looking up Meet space using meeting code...
✅ Found Meet space: spaces/xxxxxxxxxx

🚀 Step 3: Patching Meet space to OPEN access...
✅ Meet space patched successfully!
   Access Type: OPEN

============================================================
✅ Meeting created successfully!
============================================================

📅 Title: Team Meeting
🕐 Start: 2026-03-12T15:00:00
🕐 End: 2026-03-12T15:45:00
🌐 Timezone: Asia/Shanghai

🔗 Meet URL: https://meet.google.com/abc-defg-hij
📞 Meeting Code: abc-defg-hij
🔓 Access Type: OPEN
🆔 Space Name: spaces/xxxxxxxxxx

📧 Calendar Link: https://calendar.google.com/calendar/event?eid=...
🆔 Event ID: xxxxxxxxxxxxxx
============================================================
```

## How It Works

1. **Calendar API** - Create event with Meet conference
2. **Meet API (spaces.get)** - Look up Meet space using meeting code
3. **Meet API (spaces.patch)** - Update space to set `accessType=OPEN`

## Troubleshooting

### 403 Permission Denied

**Cause:** Using `meetings.space.created` scope (sensitive) without additional verification.

**Solution:** Use `meetings.space.settings` scope (non-sensitive) instead. Already fixed in the script.

### API Not Enabled

Enable both APIs in Google Cloud Console:
- Calendar API: https://console.developers.google.com/apis/api/calendar.googleapis.com/overview
- Meet API: https://console.developers.google.com/apis/api/meet.googleapis.com/overview

### Invalid Credentials

Delete `meeting_token.pickle` to force re-authentication:
```bash
rm meeting_token.pickle
```

## Files

- `book_meeting.py` - Main script
- `client_secrets.json` - OAuth credentials (you provide)
- `meeting_token.pickle` - Cached OAuth token (auto-generated)
- `requirements.txt` - Python dependencies

## Security Notes

⚠️ **Sensitive Files:**

| File | Description | Security |
|------|-------------|----------|
| `meeting_token.pickle` | Cached OAuth tokens (contains refresh token) | Keep secure; delete when not needed; do not commit to version control |
| `client_secrets.json` | OAuth client credentials | Never commit to version control; protect as password |

⚠️ **Token File Warning:**
The script writes `meeting_token.pickle` to disk after first OAuth authorization. This file contains sensitive OAuth tokens including refresh tokens that can be used to access your Google account. Protect this file:
- Do not share it
- Do not commit it to version control
- Delete it when no longer needed
- Ensure proper file permissions (readable only by owner)

## References

- [Google Calendar API](https://developers.google.com/calendar/api/v3/reference)
- [Google Meet API](https://developers.google.com/workspace/meet/api/reference/rest)
- [Meet spaces.get](https://developers.google.com/workspace/meet/api/reference/rest/v2/spaces/get)
- [Meet spaces.patch](https://developers.google.com/workspace/meet/api/reference/rest/v2/spaces/patch)
