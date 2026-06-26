---
name: calctl
description: Native macOS Calendar CLI with EventKit for creating, listing, editing, and deleting calendar events from the terminal. Supports recurring events. Trigger phrases: "calendar CLI", "apple calendar from terminal", "calctl", "event CLI for macOS", "add recurring event to calendar", "schedule recurring calendar event".
homepage: https://github.com/christianteohx/calctl
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🗓️",
        "requires": { "bins": [] }
      }
  }
---

# calctl Skill

Native macOS Calendar CLI built with EventKit. No AppleScript, no osascript.

## When to invoke

Trigger when user says or asks for:
- "calendar CLI"
- "apple calendar from terminal"
- "calctl"
- "event CLI for macOS"
- "list calendar events from command line"
- "create calendar event from terminal"
- "add recurring event"
- "schedule recurring calendar"
- "weekly meeting in calendar"
- "every monday calendar event"

## How to use

The calctl CLI is already built at https://github.com/christianteohx/calctl.
Clone and build it, or install via Homebrew.

Install (Homebrew, recommended):

```
brew install christianteohx/tap/calctl
```

Direct binary:

```
curl -fsSL https://github.com/christianteohx/calctl/releases/latest/download/calctl -o ~/bin/calctl
chmod +x ~/bin/calctl
```

Build from source (macOS 13+, Swift 6.0+):

```
git clone https://github.com/christianteohx/calctl
cd calctl
swift build
.build/release/calctl <command>
```

First run: macOS will prompt for Calendar permission. Grant it in System Settings > Privacy & Security > Calendars > Terminal.

## Commands

```
calctl status                    check calendar access status
calctl authorize                 trigger permission prompt
calctl list                      list all calendars (with id, title, source)
calctl today [--attendees]       show today's events (--attendees shows invitees)
calctl tomorrow [--attendees]     show tomorrow's events (--attendees shows invitees)
calctl week [--attendees]        show this week's events (--attendees shows invitees)
calctl date YYYY-MM-DD [--attendees]  show events for a specific date
calctl add --title ... --start ... --end ... [--recurrence RULE]  create an event
calctl edit --id <id> ...       edit an event
calctl delete --id <id>          delete an event
--calendar <name>                filter by calendar name
```

## Recurring events

Add --recurrence with iCalendar RRULE syntax:

```
calctl add --title "Weekly Standup" --start "2026-04-14 09:00" --end "2026-04-14 09:30" --recurrence "FREQ=WEEKLY;INTERVAL=1;BYDAY=MO"
calctl add --title "Daily Reminder" --start "2026-04-15 08:00" --end "2026-04-15 08:05" --recurrence "FREQ=DAILY"
calctl add --title "Monthly Report" --start "2026-05-01 10:00" --end "2026-05-01 11:00" --recurrence "FREQ=MONTHLY;BYMONTHDAY=1"
```

Supported RRULE keys: FREQ (DAILY/WEEKLY/MONTHLY/YEARLY), INTERVAL, BYDAY, BYMONTHDAY, COUNT, UNTIL.

## Attendees

Use `--attendees` on `today`, `tomorrow`, `week`, or `date` commands to show attendee information:

```
calctl today --attendees
calctl week --attendees
```

Shows each attendee's name/email and participation status (accepted, pending, declined, tentative, etc.). Events with no attendees show no attendee data. Available in both plain text and JSON output.
