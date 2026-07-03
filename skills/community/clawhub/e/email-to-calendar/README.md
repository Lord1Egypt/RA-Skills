# Email to Calendar

**Turn your inbox into calendar events.** Forward an email (or let it scan your inbox) and this skill extracts the meetings, appointments, RSVPs, and deadlines — then creates Google Calendar events after you confirm.

> **6,000+ downloads on ClawHub** · MIT licensed · passes ClawHub security scan clean

## Why

Stop hand-copying dates out of emails. The skill reads the message, finds the event — date, time, location, links, RSVP/registration deadlines — shows you exactly what it found, and only creates the calendar entry once you say yes. Wrong about something? Undo within 24 hours.

## What it does

- 📥 **Two modes** — scan your whole inbox, or only process emails you forward to a dedicated address.
- 🧠 **Smart extraction** — pulls out title, date, time, location, links, and recurring/multi-day patterns.
- ⏰ **Deadline detection** — spots "RSVP by", "register by", "tickets until" and creates a separate reminder event (plus an optional notification email).
- 🔁 **Duplicate detection** — updates the existing event instead of creating a copy.
- ↩️ **24-hour undo** — every change is logged and reversible.
- 🔔 **Pending-invite reminders** — nudges you about events you haven't actioned yet.
- ✅ **You stay in control** — nothing is created without your explicit confirmation.

## Install

```bash
clawhub install email-to-calendar
```

Requires `python3`, `bash`, `jq`, and a Gmail/Google Calendar tool (the [`gog`](https://github.com/tonimelisma/gogcli) CLI is the reference implementation).

## Setup

On first run, the skill auto-detects your Gmail accounts and calendars and proposes sensible defaults — press Enter to accept, or tweak any setting. See **[SETUP.md](SETUP.md)** for the full configuration guide.

## What it accesses

For transparency, the skill reads Gmail to find events, manages Google Calendar (deleting only on undo), optionally sends you deadline-reminder emails, archives/labels processed mail per your config, and stores tracking state **locally** — no external servers, no telemetry. Full details in **[SKILL.md](SKILL.md#what-this-skill-accesses)**.

## License

[MIT](LICENSE)
