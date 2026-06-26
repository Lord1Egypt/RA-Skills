---
name: conference-intern
description: Discover, curate, and register for crypto conference side events via Luma and Google Sheets
metadata:
  openclaw:
    emoji: "🎪"
    requires:
      bins: ["jq", "python3", "curl", "sha256sum"]
      capabilities: ["browser"]
---

# Conference Intern

Discover, curate, and auto-register for crypto conference side events. Fetches events from Luma pages and community-curated Google Sheets, filters them using your preferences with LLM intelligence, and handles Luma RSVP via browser automation.

## Quick Start

```bash
# First time: interactive setup
bash scripts/setup.sh my-conference

# Run the full pipeline
bash scripts/discover.sh my-conference
bash scripts/curate.sh my-conference
bash scripts/register.sh my-conference

# Or all at once
bash scripts/discover.sh my-conference && bash scripts/curate.sh my-conference && bash scripts/register.sh my-conference

# Monitor for new events
bash scripts/monitor.sh my-conference
```

## Commands

| Command | Script | Description |
|---------|--------|-------------|
| setup | `bash scripts/setup.sh <name>` | Interactive config — walks you through preferences, URLs, auth |
| discover | `bash scripts/discover.sh <id>` | Fetch events from Luma + Google Sheets → `events.json` |
| curate | `bash scripts/curate.sh <id>` | LLM-driven filtering and ranking → `curated.md` |
| register | `bash scripts/register.sh <id>` | Auto-RSVP on Luma for recommended events |
| monitor | `bash scripts/monitor.sh <id>` | Re-discover + re-curate, flag new events |

## File Locations

Per-conference data lives in `conferences/{conference-id}/`:

- `config.json` — user preferences, URLs, strategy, user info
- `events.json` — all discovered events (normalized schema)
- `events-previous.json` — snapshot from last run (for monitoring diff)
- `curated.md` — the curated schedule output (grouped by day, tiered)
- `luma-session.json` — persisted Luma browser session cookies
- `custom-answers.json` — user answers to custom RSVP fields (reused across registrations)

Skill-level shared files:

- `luma-knowledge.md` — shared Luma page patterns (learned by agent, speeds up registration)

## Agent Instructions

### CRITICAL: Always Use the Scripts

**You MUST run the bash scripts for every pipeline stage. Do NOT attempt to perform discovery, curation, or registration yourself by browsing pages directly.** The scripts handle looping, error recovery, state tracking, and tab cleanup that you cannot reliably do in a single agent turn.

When the user asks you to:
- **Set up a conference** → run `bash scripts/setup.sh <conference-id>`
- **Find/discover events** → run `bash scripts/discover.sh <conference-id>`
- **Curate/filter events** → run `bash scripts/curate.sh <conference-id>`
- **Register for events** → run `bash scripts/register.sh <conference-id>` (processes 10 events per batch)
- **Retry events needing input** → run `bash scripts/register.sh <conference-id> --retry-pending`
- **Check for new events** → run `bash scripts/monitor.sh <conference-id>`
- **Run the full pipeline** → run each script in sequence: discover → curate → register

The scripts will invoke you for individual tasks (one event at a time for registration). Follow the prompts they give you. **Never try to loop through events yourself** — the scripts control the loop to ensure every event is attempted.

### Browser Usage

When the scripts invoke you for browser tasks, use your browser capability to interact with pages. **Do not hardcode CSS selectors or DOM paths.** Instead:
- Navigate to URLs and read the page content
- Interpret the page like a human — find event listings, registration forms, buttons
- This approach is evergreen — it works regardless of Luma UI changes

### Registration (batch flow)

Registration processes events in batches of 10. **You MUST follow this loop until all events are processed:**

1. Run `bash scripts/register.sh <conference-id>`
2. **IMMEDIATELY tell the user** the batch results (registered/failed/needs-input/remaining counts)
3. Read `conferences/<id>/registration-status.json`
4. If `new_fields` is not empty: ask the user for answers, write them to `conferences/<id>/custom-answers.json`
5. If `done` is false: **run `register.sh` again immediately** for the next batch — do NOT wait for the user to ask
6. When `done` is true and there are `⏳ Needs input` events: run `register.sh --retry-pending`
7. Read `registration-status.json` — if `manual_registration` is not empty, present the list to the user:
   "These events need manual registration (not on Luma):"
   - [Event Name](url) for each entry
8. Report final results to the user

**CRITICAL:** After each batch completes, you MUST either run the next batch or tell the user why you stopped. Never silently stop between batches.

When invoked by the script for individual events:
- Fill only **mandatory/required** fields on RSVP forms. Leave optional fields blank.
- If you encounter required fields you cannot fill, return `needs-input` status with the field labels.
- Never guess answers for custom fields — always defer to the user.
- If the user is already registered, return `registered` status without touching the form.
- Close the browser tab after each event — unless CAPTCHA is detected (keep that tab open).

### Error Handling

The scripts handle most error recovery automatically. When invoked for a single event:
- Page fails to load → return `failed` status
- CAPTCHA detected → return `captcha` status (script will stop the loop)
- Event full/closed → return `closed` status
- Session expired → return `session-expired` status (script will stop the loop)

### Stop Conditions

The registration script (`register.sh`) automatically stops and asks the user when:
- CAPTCHA is detected (Luma likely flagged the session)
- Session expires mid-run
- Custom fields need answers (collects all unique fields, asks once per field)

Other pipeline stop conditions:
- Zero events discovered → skip curate and register
- Zero events curated → skip register
