# Email-to-Calendar Workflow Example

A complete walk-through of processing one email, using the wrapper scripts.

> **Reminder:** NEVER call `gog` directly. ALL email and calendar operations go
> through the wrapper scripts in `scripts/` (see SKILL.md CRITICAL RULES).

```bash
SCRIPTS_DIR="$HOME/.openclaw/workspace/skills/email-to-calendar/scripts"
CONFIG_FILE="$HOME/.config/email-to-calendar/config.json"
```

## Scenario: User Forwards an Email

```
---------- Forwarded message ----------
From: Sarah <sarah@client.com>
Date: Mon, Feb 2, 2026 at 10:00 AM
Subject: Project kickoff meeting
To: team@company.com

Hi everyone,

Let's schedule a kickoff meeting for the new website project on Thursday
February 5 at 3:00 PM in Conference Room B.

Action items before the meeting:
- Review the requirements document
- Prepare your team's capacity estimates
- Submit any questions by Wednesday

Thanks!
Sarah
```

## Step 1: Read the Email

Get the full body via the wrapper script:

```bash
"$SCRIPTS_DIR/email_read.sh" --email-id "$EMAIL_ID"
```

## Step 2: Extract Events (Agent does this directly)

There is no extraction script — you read the email and extract events using
natural language understanding. For this email you identify:

- **title:** Kickoff meeting - Website Project
- **date:** 2026-02-05 (**day_of_week:** Thursday)
- **time:** 3:00 PM (default end 4:00 PM)
- **location:** Conference Room B
- **confidence:** high
- **deadline:** "Submit any questions by Wednesday" → 2026-02-04

See [extraction-patterns.md](extraction-patterns.md) for the date/time and
deadline patterns to look for.

## Step 3: Present to User and WAIT

Apply `ignore_patterns` / `auto_create_patterns` from config, then present:

> I found the following potential event:
>
> 1. **Kickoff meeting - Website Project** (Thursday, Feb 5 at 3:00 PM, Conference Room B)
>    - Deadline: submit questions by Wednesday, Feb 4
>
> Reply with numbers to create (e.g., '1'), 'all', or 'none'.

Record it as a pending invite for follow-up reminders:

```bash
"$SCRIPTS_DIR/add_pending.sh" \
    --email-id "$EMAIL_ID" \
    --email-subject "Project kickoff meeting" \
    --events-json '[{"title":"Kickoff meeting - Website Project","date":"2026-02-05","time":"15:00","status":"pending"}]'
```

**STOP AND WAIT for the user's response.** (User replies: "1")

## Step 4: Check for Duplicates

Check local tracking first (fast), then fall back to a calendar search:

```bash
# Tracked by email ID?
TRACKED=$("$SCRIPTS_DIR/lookup_event.sh" --email-id "$EMAIL_ID")

# Or by title?
TRACKED=$("$SCRIPTS_DIR/lookup_event.sh" --summary "Kickoff meeting")

# Fall back to calendar search around the date
"$SCRIPTS_DIR/calendar_search.sh" \
    --calendar-id "$CALENDAR_ID" \
    --from "2026-02-05T00:00:00" --to "2026-02-05T23:59:59"
```

## Step 5: Create the Event

`create_event.sh` handles date parsing, tracking, changelog, attribution, and
email disposition automatically:

```bash
CALENDAR_ID=$(jq -r '.calendar_id' "$CONFIG_FILE")
ATTENDEE_EMAILS=$(jq -r 'if .attendees.enabled then (.attendees.emails | join(",")) else "" end' "$CONFIG_FILE")

"$SCRIPTS_DIR/create_event.sh" \
    "$CALENDAR_ID" \
    "Kickoff meeting - Website Project" \
    "February 5, 2026" \
    "3:00 PM" \
    "4:00 PM" \
    "Event Link: (none)

Kickoff meeting for the new website project
Location: Conference Room B
From: Sarah <sarah@client.com>

Action items before the meeting:
- Review the requirements document
- Prepare your team's capacity estimates
- Submit any questions by Wednesday February 4" \
    "$ATTENDEE_EMAILS" \
    "" \
    "$EMAIL_ID"
```

## Step 6: Confirm

> Created calendar event:
> - **Title:** Kickoff meeting - Website Project
> - **When:** Thursday, February 5, 2026, 3:00 PM - 4:00 PM
> - **Location:** Conference Room B
> - **Attendees:** Invited as configured
>
> You can undo this within 24 hours with `undo.sh last`.

`create_event.sh` already tracked the event, updated the pending invite to
`created`, logged the change for undo, and dispositioned the email per config.

## Alternative: Duplicate Found

If lookup or search returns an existing event:

```json
{
  "id": "abc123xyz",
  "summary": "Website Project Kickoff",
  "start": {"dateTime": "2026-02-05T15:00:00"}
}
```

> I found an existing event "Website Project Kickoff" on Thursday, February 5 at
> 3:00 PM. Should I:
> 1. Update it with new information from this email
> 2. Skip (keep existing event as-is)
> 3. Create a separate event anyway

If the user chooses "1", update by passing the existing event ID as the 8th
argument to `create_event.sh`.

## Deadlines

This email has a soft deadline ("submit questions by Wednesday"). When an email
contains an RSVP / registration / ticket deadline, also create a separate
`DEADLINE:` reminder event and optionally send a notification email — see
SKILL.md "Creating Deadline Events".
