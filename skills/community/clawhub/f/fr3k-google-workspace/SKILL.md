---
name: google-workspace
description: Google Workspace automation — Gmail, Calendar, Drive, and Sheets via service account or OAuth. Read, write, send, and manage your entire Google stack.
---
# Google Workspace

Automate Gmail, Google Calendar, Google Drive, and Google Sheets from the command line. Read and send emails, create calendar events, manage Drive files, and read/write Sheets data — all via the Google API Python client with service account authentication.

## Setup

### Option 1: Service Account (recommended for automation)
```bash
export GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account","project_id":"...","private_key_id":"...","private_key":"-----BEGIN RSA PRIVATE KEY-----\n...","client_email":"...@....iam.gserviceaccount.com","client_id":"...","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token"}'
```

Create at: Google Cloud Console → IAM → Service Accounts → Create → Add JSON key.
Then enable: Gmail API, Calendar API, Drive API, Sheets API.
For Gmail/Calendar/Drive: Enable domain-wide delegation and add scopes in Google Workspace Admin.

### Option 2: OAuth credentials file
```bash
export GOOGLE_CREDENTIALS_FILE="/path/to/credentials.json"
export GOOGLE_TOKEN_FILE="/path/to/token.json"   # created on first run
```

## Commands / Usage

```bash
# ── GMAIL ───────────────────────────────────────────────
# Read inbox (latest 10 messages)
python3 scripts/google_workspace.py gmail-inbox
python3 scripts/google_workspace.py gmail-inbox --limit 25

# Search emails
python3 scripts/google_workspace.py gmail-search --query "from:boss@company.com subject:urgent"
python3 scripts/google_workspace.py gmail-search --query "is:unread" --limit 20

# Send an email
python3 scripts/google_workspace.py gmail-send --to "client@example.com" --subject "Meeting Tomorrow" --body "Hi, just confirming our meeting at 2pm."
python3 scripts/google_workspace.py gmail-send --to "a@x.com" --subject "Report" --body "See attached." --attachment "/path/to/report.pdf"

# Apply a label to a message
python3 scripts/google_workspace.py gmail-label --message-id "18abc123..." --label "Important"

# Create a draft
python3 scripts/google_workspace.py gmail-draft --to "client@example.com" --subject "Draft Subject" --body "Draft content here."

# ── CALENDAR ────────────────────────────────────────────
# List upcoming events
python3 scripts/google_workspace.py cal-list
python3 scripts/google_workspace.py cal-list --days 14 --limit 20

# Create an event
python3 scripts/google_workspace.py cal-create --title "Team Standup" --start "2024-03-15T09:00:00" --end "2024-03-15T09:30:00" --timezone "Australia/Brisbane"
python3 scripts/google_workspace.py cal-create --title "All Day Event" --start "2024-03-20" --all-day

# Update an event
python3 scripts/google_workspace.py cal-update --event-id "abc123..." --title "Updated Title" --start "2024-03-15T10:00:00" --end "2024-03-15T10:30:00"

# Delete an event
python3 scripts/google_workspace.py cal-delete --event-id "abc123..."

# ── DRIVE ───────────────────────────────────────────────
# List files
python3 scripts/google_workspace.py drive-list
python3 scripts/google_workspace.py drive-list --query "name contains 'report'" --limit 20

# Upload a file
python3 scripts/google_workspace.py drive-upload --file ./report.pdf
python3 scripts/google_workspace.py drive-upload --file ./report.pdf --folder-id "1BxiMVs0XRA5..."

# Download a file
python3 scripts/google_workspace.py drive-download --file-id "1BxiMVs0XRA5..." --output ./downloaded.pdf

# Share a file
python3 scripts/google_workspace.py drive-share --file-id "1BxiMVs0XRA5..." --email "colleague@company.com" --role writer
python3 scripts/google_workspace.py drive-share --file-id "1BxiMVs0XRA5..." --anyone-link

# ── SHEETS ──────────────────────────────────────────────
# Read a range
python3 scripts/google_workspace.py sheets-read --spreadsheet-id "1BxiMVs0XRA5..." --range "Sheet1!A1:D10"

# Write to a range
python3 scripts/google_workspace.py sheets-write --spreadsheet-id "1BxiMVs0XRA5..." --range "Sheet1!A1" --values '[["Name","Score"],["Alice",95],["Bob",87]]'

# Append a row
python3 scripts/google_workspace.py sheets-append --spreadsheet-id "1BxiMVs0XRA5..." --range "Sheet1!A:D" --values '["John","Doe","john@example.com",42]'
```

## Requirements

- Python 3.8+
- `google-api-python-client` (`pip install google-api-python-client google-auth google-auth-httplib2`)
- `GOOGLE_SERVICE_ACCOUNT_JSON` environment variable (or OAuth credentials)
