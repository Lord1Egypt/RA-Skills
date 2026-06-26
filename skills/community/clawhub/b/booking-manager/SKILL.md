---
name: booking-manager
version: 1.3.2
description: >
  AI-powered booking manager that connects to any existing booking system and lets
  business owners manage appointments through their phone (Telegram, WhatsApp, etc.). Use when: setting up an AI
  assistant to monitor bookings, notify owners of new enquiries, confirm/reschedule/cancel
  appointments conversationally, send professional customer emails with calendar invites,
  and provide schedule summaries. Works with any data source: SQL databases (PostgreSQL,
  SQLite/Turso, MySQL), REST APIs (Calendly, Square, Fresha), Google Sheets, or webhooks.
  Triggers on: "booking assistant", "appointment manager", "manage bookings via phone",
  "AI receptionist", "booking notifications", "salon booking system".
homepage: https://github.com/Cskar10/booking-manager
repository: https://github.com/Cskar10/booking-manager
metadata:
  openclaw:
    requires:
      config:
        - env.SMTP_HOST
        - env.SMTP_USER
        - env.SMTP_PASSWORD
    env_vars:
      required:
        - name: SMTP_HOST
          description: "SMTP server hostname (e.g. smtp.gmail.com)"
        - name: SMTP_USER
          description: "Email address used to send confirmations"
        - name: SMTP_PASSWORD
          description: "SMTP app password (never a primary password)"
      optional:
        - name: BOOKING_DB_URL
          description: "Turso/LibSQL database URL"
        - name: BOOKING_DB_TOKEN
          description: "Turso/LibSQL auth token (scoped to bookings table)"
        - name: BOOKING_DB_HOST
          description: "PostgreSQL host"
        - name: BOOKING_DB_PORT
          description: "PostgreSQL port"
        - name: BOOKING_DB_USER
          description: "PostgreSQL user (limited to bookings table)"
        - name: BOOKING_DB_PASSWORD
          description: "PostgreSQL password"
        - name: BOOKING_DB_NAME
          description: "PostgreSQL database name"
        - name: GOOGLE_SHEET_ID
          description: "Google Sheets spreadsheet ID"
        - name: GOOGLE_SHEETS_TOKEN
          description: "Google Sheets API access token (scoped service account)"
        - name: SHEET_RANGE
          description: "Google Sheets range (e.g. Sheet1!A:H)"
    network:
      description: >
        The agent makes outbound requests to the configured data source (Turso API,
        PostgreSQL, Google Sheets API, or third-party booking APIs) and to the
        configured SMTP server for sending emails. No other external endpoints are
        contacted. Polling frequency is configurable via HEARTBEAT.md (default: every
        15-30 minutes).
      endpoints:
        - "Configured SMTP server (env: SMTP_HOST, port 465/587)"
        - "Configured database URL (env: BOOKING_DB_URL or BOOKING_DB_HOST)"
        - "Google Sheets API v4 (if using Sheets as data source)"
        - "Third-party booking APIs (if using Calendly/Square/Fresha)"
    security:
      - "All credentials stored in openclaw.json env block, never in workspace files"
      - "Use least-privilege: scoped service accounts, DB users limited to bookings table"
      - "SMTP app passwords only, never primary account passwords"
      - "Rotate credentials after testing"
---

# Booking Manager

An AI assistant layer that sits on top of any booking system, turning your phone into a
full booking management interface via Telegram, WhatsApp, or any supported channel.

## How It Works

```
Customer books → Data saved (DB/API/Sheet) → Agent polls for new bookings
                                                    ↓
                                          Notifies owner via phone (Telegram/WhatsApp)
                                                    ↓
                              Owner replies: "confirm" / "reschedule" / "delete"
                                                    ↓
                                    Agent updates data + emails customer
```

## Setup

### 0. First-Run Onboarding

On any booking-related request, check if TOOLS.md contains a `## Business` section
AND a `## Services` section. If either is missing, this is a first-run — begin
onboarding before doing anything else.

**Primary flow (form paste):**

1. Greet the customer:

```
Hi! I'm your new booking assistant. 👋

To get started, please paste the completed onboarding form you received
and I'll set everything up from that.

If you don't have a form, just let me know and I'll walk you through
the setup step by step.
```

2. When the customer pastes the form, parse it for these fields:

| Field | Required | TOOLS.md Section |
|---|---|---|
| Business name | ✅ | `## Business` |
| Business address | Optional | `## Business` |
| Phone number | Optional | `## Business` |
| Website | Optional | `## Business` |
| Timezone | ✅ | `## Business` |
| Services (name, duration, price) | ✅ | `## Services` |
| Operating hours per day | ✅ | `## Operating Hours` |
| Confirmation email (name + address) | ✅ | `## Email` |
| Booking/cancellation policy | Optional | `## Booking Policy` |
| Existing booking system | Optional | `## Booking Data Source` |
| Notification preference | Optional | `## Notifications` |
| Mobile number | Optional | `## Notifications` |
| Additional notes | Optional | `## Notes` |

3. Write the parsed config to TOOLS.md:

```markdown
## Business
- Name: [business name]
- Address: [address]
- Phone: [phone]
- Website: [website]
- Timezone: [timezone]

## Services
- [Service 1]: [duration] min — $[price]
- [Service 2]: [duration] min — $[price]

## Operating Hours
- Monday: [open] – [close]
- Tuesday: [open] – [close]
- ...
- Sunday: Closed

## Email
- From: [Business Name] <[email address]>

## Booking Policy
- [policy text or "No specific policy"]

## Booking Data Source
- Type: [system mentioned or "pending setup"]
- Connection: [pending admin configuration]

## Notifications
- Channel: [preference]
- Mobile: [number]
```

4. Show a summary for confirmation:

```
✅ All set! Here's what I've got:

📋 **[Business Name]**
📍 [address]
🕐 [hours summary]

**Services:**
• [Service 1] — [duration] min — $[price]
• [Service 2] — [duration] min — $[price]

**Confirmations from:** [email]
**Policy:** [policy summary]

Everything look right? If you need to change anything, just tell me.
```

5. Note about data source: "I'll need your booking system connected before I can
   see bookings — your admin will set that up for you."

**Security:** The onboarding flow collects business information only (name, services,
hours, policy). It must NEVER ask for or accept credentials (passwords, tokens, API
keys) through chat. Credentials are configured by the admin directly in `openclaw.json`
under `env`. If a customer pastes credentials in chat, do NOT store them — instruct
them to contact their admin instead.

**Fallback flow (step-by-step):**

If the customer says they don't have a form, collect info conversationally:

1. "What's your business called?"
2. "What services do you offer? For each one, I'll need the name, how long it takes, and the price."
3. "What days and hours are you open?"
4. "What timezone are you in?"
5. "What email address should booking confirmations come from?"
6. "Do you have any booking or cancellation policies?"
7. "Anything else I should know about how you run bookings?"

Write to TOOLS.md using the same format and show the same summary.

**Validation:**

- Missing required fields → ask specifically: "I noticed [field] is blank — could you fill that in?"
- Ambiguous services (no duration/price) → ask: "How long does [service] take, and what do you charge?"
- Timezone → accept common formats (AEST, Australia/Melbourne, GMT+10), normalise to IANA
- Hours → accept 9am-5pm, 0900-1700, 9:00 AM - 5:00 PM, normalise consistently

**Edge cases:**

- Partial form pasted → parse what's there, ask for the rest
- Unrelated text pasted → "That doesn't look like the onboarding form. Try pasting it again, or I'll walk you through setup."
- Customer wants to change after setup → "Sure! Just tell me what to change."
- TOOLS.md already has config → skip onboarding, booking-manager handles normally

The onboarding form template is in `references/onboarding-form.md`.

### 1. Identify the data source

Determine how the business stores bookings. Read `references/data-sources.md` for
connection patterns for each supported platform.

### 2. Configure credentials

Store connection details as **environment variables** in `openclaw.json` under `env`,
never in plaintext in TOOLS.md or any workspace file. Reference them in TOOLS.md by
name only:

```markdown
## Booking Data Source
- Type: [turso | postgres | google-sheets | api]
- Env vars configured: yes/no

## Email
- From: [Business Name] <business@email.com>
- SMTP env vars configured: yes/no
```

**Never store credentials in plaintext in TOOLS.md, SOUL.md, or any workspace file.**
See `references/data-sources.md` for which environment variables each data source expects.

### 3. Set up heartbeat polling

Add to HEARTBEAT.md to check for new bookings every 15-30 minutes:

```markdown
## Check for new bookings
- Query the data source for bookings created since last check
- If new bookings found: notify the owner with details and send acknowledgement email
```

### 4. Configure the agent identity

Set SOUL.md with the business context:

```markdown
You are the booking manager for **[Business Name]**.

## Your Role
- Monitor for new booking enquiries and notify the owner on their phone
- Confirm, reschedule, or delete bookings when instructed
- Send professional emails to customers
- Provide schedule summaries on demand

## Rules
- All times in [timezone]
- Always clean up booking locks when confirming or deleting
- Send calendar invites (.ics) when confirming
```

## Core Workflows

### New booking notification

When a new booking is detected, notify the owner:

```
📋 New booking enquiry!

Name: [name]
Service: [service] ([duration] min)
Date: [formatted date and time]
Phone: [phone]
Email: [email]

Reply: "confirm [id]", "reschedule [id] to [date] [time]", or "delete [id]"
```

Send an acknowledgement email to the customer. See `references/email-templates.md`.

### Confirm booking

1. Mark booking as confirmed in data source
2. Remove any booking lock for the customer's email
3. Send confirmation email with .ics calendar invite attached
4. Notify owner: "✅ Booking #[id] confirmed. Email sent to [name]."

### Reschedule booking

1. Update date/time in data source
2. Remove booking lock
3. Delete existing reminder record (so a new reminder sends for the updated time)
4. Send updated confirmation email with new .ics
5. Notify owner: "✅ Booking #[id] rescheduled to [new date/time]. Email sent."

### Delete booking

1. Record the customer email before deleting
2. Delete the booking from data source
3. Remove booking lock
4. Optionally send cancellation email
5. Notify owner: "🗑️ Booking #[id] deleted."

### Schedule queries

Respond naturally to:
- "What bookings do I have today?"
- "Show this week's schedule"
- "How many bookings this month?"
- "Any new bookings?"

## Calendar Invites

Generate .ics files when confirming. See `references/ics-format.md` for the template
and timezone/DST conversion logic.

## Email Sending

Send via Gmail SMTP using environment variables for credentials (never inline).
See `references/email-templates.md` for HTML templates and the secure sending pattern.

## Booking Locks

Many booking systems use a lock/hold mechanism to prevent duplicate pending enquiries
from the same customer. **Always** release locks when confirming or deleting a booking,
otherwise the customer cannot book again.

## Automated Reminder Emails

Send reminder emails to customers 24 hours before their appointment. This feature is
added to the heartbeat/cron polling cycle alongside new booking checks.

### Setup

Add a `booking_reminders` table to the data source to track sent reminders and prevent
duplicates. See `references/data-sources.md` for the schema.

Add reminder configuration to TOOLS.md:

```markdown
## Reminders
- Lead time: 24h (how far before the appointment to send)
- Window: ±1h (send if appointment is 23–25h away — accounts for polling gaps)
- Include cancel/reschedule info: [yes | no]
- Custom footer: [optional policy reminder text, e.g. "Cancellations within 48h..."]
```

The cancel/reschedule option and footer text are **entirely business-specific**. Some
businesses allow changes up until the appointment; others enforce strict late-cancellation
penalties. Configure per client.

### Heartbeat integration

Add to HEARTBEAT.md alongside the new-booking check:

```markdown
## Send appointment reminders
- Query for confirmed bookings with appointments 23–25 hours from now
- Skip any booking IDs already in the booking_reminders table
- For each eligible booking: send reminder email, then record in booking_reminders
- If any reminders sent: notify owner "📬 Sent [n] reminder(s) for tomorrow's appointments"
```

### Workflow

1. Query confirmed bookings where appointment time is 23–25 hours from now
2. Left-join against `booking_reminders` to exclude already-sent reminders
3. For each unsent reminder:
   a. Send reminder email (see `references/email-templates.md`)
   b. Insert a record into `booking_reminders` with the booking ID and timestamp
4. Notify the owner with a summary (if any were sent)

### Reminder query (Turso/SQLite example)

```sql
SELECT b.*
FROM bookings b
LEFT JOIN booking_reminders r ON b.id = r.booking_id
WHERE b.status = 'confirmed'
  AND b.appointment_datetime_utc > datetime('now', '+23 hours')
  AND b.appointment_datetime_utc <= datetime('now', '+25 hours')
  AND r.booking_id IS NULL;
```

### Edge cases

- **Polling gaps:** The ±1 hour window ensures reminders aren't missed if a heartbeat
  runs slightly late or early. The `booking_reminders` table prevents duplicates even
  if the same booking falls in the window across multiple polls.
- **Already passed:** If the agent was offline and missed the 24h window, do NOT send
  a late reminder — it's confusing. Only send if the appointment is still >22h away.
- **Deleted/rescheduled bookings:** If a booking is rescheduled, the old reminder record
  stays (harmless). The new appointment time will trigger a fresh reminder since the
  booking ID changes or the UTC time no longer matches. If using the same booking ID
  after reschedule, delete the old reminder record when rescheduling so a new one sends.

## Adapting to Different Businesses

Customise these per client:
- Business name and branding in email templates
- Services list with durations (for calendar invite end times)
- Operating hours and timezone
- Booking policy text
- Reminder settings (lead time, cancel/reschedule option, policy footer)
- Data source connection method
