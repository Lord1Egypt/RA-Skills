---
name: calendar-setup
description: "Step-by-step wizard for connecting an owner's Google Calendar to their OpenClaw PA agent, including granting write permissions. Use when: setting up calendar access for the first time, troubleshooting calendar connection issues, fixing read-only calendar access, re-authenticating after permission errors, or handling multiple calendar accounts (work + personal). Works with any LLM model."
---

# Calendar Setup Skill

## Minimum Model
Any model that can follow numbered steps.

---

## Key Concept

Two accounts are involved:
- **Agent email** — the PA's own Google account (e.g. `agent@agentdomain.com`)
- **Owner email** — the human's Google account (e.g. `owner@company.com`)

The agent needs access to the **owner's** calendar. These are separate Google accounts. The OpenClaw dashboard "calendar connected" status reflects the *agent's own* calendar — not the owner's. Verify write access explicitly.

---

## Step 1 — Owner Shares Calendar

The **owner** does this in Google Calendar (not the agent):

1. Open [calendar.google.com](https://calendar.google.com) as the **owner**
2. Find the primary calendar in the left sidebar (usually their name)
3. Click the three-dot menu → **Settings and sharing**
4. Under **Share with specific people** → click **+ Add people**
5. Enter the **agent email**
6. Set permission to **"Make changes to events"** — not "See all event details" (that is read-only)
7. Click **Send**

✅ Done. The agent receives an email confirmation — no action needed from the agent side yet.

**If owner can't find the calendar:** Scroll down in the sidebar to "Other calendars".

**If sharing is blocked:** The owner's organization may restrict external sharing. They need to ask their IT admin to allow it.

---

## Step 2 — Agent Authenticates

The **agent** runs:

```bash
# Add the owner's account to gog
gog auth add owner@company.com --services gmail,calendar,drive,contacts

# Verify it was added
gog auth list
```

Expected output of `gog auth list`:
```
owner@company.com  [gmail, calendar, drive, contacts]
```

If re-authenticating after a permission change or expired token:
```bash
gog auth remove owner@company.com
gog auth add owner@company.com --services gmail,calendar,drive,contacts
```

**If `gog` is not found:** Check PATH or reinstall via your OpenClaw distribution.

**If OAuth fails with "access blocked":** Owner must allow access in Google Account → Security → Third-party apps.

---

## Step 3 — Test Write Access

```bash
# Generate timestamps (works on Linux and macOS)
START=$(date -u -d '+1 hour' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null \
  || date -u -v+1H +%Y-%m-%dT%H:%M:%SZ)
END=$(date -u -d '+2 hours' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null \
  || date -u -v+2H +%Y-%m-%dT%H:%M:%SZ)

# Create a test event in the owner's calendar
GOG_ACCOUNT=owner@company.com gog calendar create primary \
  --summary "PA Setup Test — delete me" \
  --start "$START" \
  --end "$END"
```

Check the owner's Google Calendar. The test event should appear within 30 seconds.

Delete it after verifying:
```bash
# Use EVENT_ID from the output of the create command above
GOG_ACCOUNT=owner@company.com gog calendar delete primary EVENT_ID
```

---

## Common Issues and Fixes

### Dashboard shows "connected" but agent can't write

**Cause:** Dashboard reflects the agent's own calendar, not the owner's.

**Fix:**
1. Confirm owner shared their calendar with the agent email (Step 1)
2. Confirm agent ran `gog auth add` for the owner's account (Step 2)
3. Always use `GOG_ACCOUNT=owner@company.com` in all commands

---

### "Insufficient permissions" error

**Cause:** Calendar was shared with read-only permission.

**Fix:** Owner goes back to Step 1 and changes the permission to "Make changes to events".

---

### "Token expired" or authentication failure

```bash
gog auth remove owner@company.com
gog auth add owner@company.com --services gmail,calendar,drive,contacts
```

---

### Multiple calendars (work + personal)

```bash
# Add both accounts
gog auth add work@company.com --services calendar
gog auth add personal@gmail.com --services calendar

# See what calendars each account has
GOG_ACCOUNT=work@company.com gog calendar list
GOG_ACCOUNT=personal@gmail.com gog calendar list

# Use the specific calendar ID (from list output) instead of "primary"
GOG_ACCOUNT=work@company.com gog calendar create CALENDAR_ID \
  --summary "Meeting" \
  --start "2026-04-02T10:00:00+00:00" \
  --end "2026-04-02T11:00:00+00:00"
```

---

### macOS date command

```bash
# Linux: use -d
date -u -d '+1 hour' +%Y-%m-%dT%H:%M:%SZ

# macOS: use -v
date -u -v+1H +%Y-%m-%dT%H:%M:%SZ
```

---

## Useful Commands

```bash
# List all authenticated accounts
gog auth list

# List owner's calendars
GOG_ACCOUNT=owner@company.com gog calendar list

# List events (next 7 days)
GOG_ACCOUNT=owner@company.com gog calendar events primary \
  --from $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --to $(date -u -d '+7 days' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v+7d +%Y-%m-%dT%H:%M:%SZ)

# Create event with attendee
GOG_ACCOUNT=owner@company.com gog calendar create primary \
  --summary "Meeting title" \
  --start "2026-04-02T10:00:00+00:00" \
  --end "2026-04-02T11:00:00+00:00" \
  --attendees "attendee@company.com"

# Delete event
GOG_ACCOUNT=owner@company.com gog calendar delete primary EVENT_ID

# Remove authenticated account
gog auth remove owner@company.com
```

---

## Heleni-specific: Direct API Workaround (when gog CLI auth fails)

`gog auth login` requires a browser — doesn't work on a server. Use the pre-existing credentials in `/opt/ocana/openclaw/.gog/credentials.json` instead.

```bash
# 1. Read client_id, client_secret, refresh_token from the file (owner account)
# Accounts: "agent" (genesis@ocana.ai), "owner" (netanelab@monday.com)

# 2. Refresh access token
curl -s -X POST https://oauth2.googleapis.com/token \
  -d "client_id=<client_id>" \
  -d "client_secret=<client_secret>" \
  -d "refresh_token=<refresh_token>" \
  -d "grant_type=refresh_token"
# → get access_token from response

# 3. Call Calendar API directly
curl -s "https://www.googleapis.com/calendar/v3/calendars/netanelab%40monday.com/events?timeMin=<ISO>&timeMax=<ISO>&singleEvents=true&orderBy=startTime&maxResults=10" \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# 4. List all calendars
curl -s "https://www.googleapis.com/calendar/v3/users/me/calendarList" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Note:** `~/.config/gws/credentials.json` (gog default path) has a stale/broken token. Always use `/opt/ocana/openclaw/.gog/credentials.json`.

---

## Verification Checklist

- [ ] Owner shared calendar with agent email
- [ ] Permission is "Make changes to events" (not read-only)
- [ ] Agent ran `gog auth add` for owner's account
- [ ] `gog auth list` shows owner's account with calendar service
- [ ] Test event created successfully in owner's calendar
- [ ] Test event deleted after verification
- [ ] All calendar commands use `GOG_ACCOUNT=owner@company.com`

---

## Cost Tips

- **Cheap:** This is a one-time setup — very low ongoing cost
- **Small model OK:** All steps are procedural — any model can follow them
- **Avoid:** Don't re-authenticate repeatedly — tokens last a long time if not revoked
- **Batch:** Add all needed services in one `gog auth add` call (gmail,calendar,drive,contacts) instead of separate calls

---

## Email & Workspace Orientation (Merged from openclaw-email-orientation skill)

### The Core Concept: Two Separate Accounts

| | Account |
|---|---|
| **Owner** | The human's Google account (e.g. `owner@company.com`) |
| **Agent** | The PA's own Google account (e.g. `agent@agentdomain.com`) |

**These are separate.** Having an agent email does NOT automatically give access to the owner's email or calendar. Owner must explicitly share, and agent must explicitly authenticate.

### Key Files

| File | Purpose |
|---|---|
| `~/.openclaw/.gog/credentials.json` | gog OAuth client credentials |
| `~/.openclaw/agents/main/agent/auth-profiles.json` | OpenClaw auth profiles |
| `skills/gog/SKILL.md` | gog usage reference |

**Security:** Never print the contents of these files in chat. Path is fine; content is not.

### Using gog

```bash
# One-time: load OAuth credentials
gog auth credentials /path/to/client_secret.json

# Add an owner account (opens browser for OAuth)
gog auth add owner@company.com --services gmail,calendar,drive,contacts,sheets,docs

# Verify
gog auth list

# Always use GOG_ACCOUNT= in all commands
GOG_ACCOUNT=owner@company.com gog gmail search 'is:unread' --max 10
GOG_ACCOUNT=owner@company.com gog calendar events primary \
  --from "2026-04-01T09:00:00Z" --to "2026-04-01T18:00:00Z"
GOG_ACCOUNT=owner@company.com gog gmail send \
  --to "recipient@example.com" --subject "Hello" --body "Message text"
```

### Troubleshooting Email/Calendar Access

Work through in order:
1. **Two accounts?** — Is the question about agent email or owner email?
2. **gog installed?** — `which gog` — if missing, check PATH
3. **Account added?** — `gog auth list` — does owner's account appear?
4. **Write scope?** — OAuth must include calendar write scope, not read-only
5. **GOG_ACCOUNT set?** — All commands must include `GOG_ACCOUNT=owner@company.com`
6. **Permission level?** — Must be "Make changes to events", not "See all event details"

**"Insufficient permissions" error** → Owner re-shares calendar with write permission (Step 1 above).

**"Token expired" error:**
```bash
gog auth remove owner@company.com
gog auth add owner@company.com --services gmail,calendar,drive,contacts
```
