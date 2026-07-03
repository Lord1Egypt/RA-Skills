# Email Extraction Patterns

This document describes the patterns to use when extracting calendar events and
action items from emails. There is no extraction script — you (the agent) read
the email and extract events directly using natural language understanding. The
patterns below are guidance for what to look for.

## Event Detection Patterns

Look for these patterns to identify potential calendar events:

### Primary Event Keywords
- meeting, call, sync, standup, review, demo, interview
- appointment, event, conference, workshop, webinar, training
- meet (as a verb)

### Event Phrases
- "Meeting on [date] at [time]"
- "Let's meet [date] at [time]"
- "Join us on [date] for [purpose]"
- "You are invited to [event] on [date]"
- "Please attend [event] on [date]"
- "Mark your calendar for [date]"
- "Save the date: [date]"
- "When: [date]" / "Date: [date]" / "Time: [time]"

## Date Parsing

Recognize these date formats:

### With Year
- January 15, 2026
- 15 January 2026
- 01/15/2026 (US format)
- 15/01/2026 (EU format)
- 2026-01-15 (ISO format)

### Without Year (defaults to current year)
- Wednesday January 15
- January 15
- Next Tuesday
- This Friday

### Relative Dates
- Today, Tomorrow
- Next week, Next Monday
- In 3 days

## Time Parsing

### 12-hour format
- 2:30 PM, 2:30 pm
- 2 PM, 2pm
- 9:00 AM - 5:00 PM (ranges)

### 24-hour format
- 14:30
- 09:00-17:00

### Full Day Indicators
- "all day", "full day", "whole day"
- "9am to 5pm", "9:00-17:00"
- "business hours", "work day"

## Action Item Detection

### Action Keywords
- Action:, Task:, Todo:, To-do:, Follow-up:, Followup:
- Please [do something]
- Kindly [do something]
- Need to, Needs to, We need to
- Should, Must, Will need to

### Bullet Points
- `- [ ] Task description`
- `* Task description`
- `• Task description`

### Deadline Detection
Action items are checked for associated deadlines:
- "by [date]"
- "due [date]"
- "before [date]"
- "deadline: [date]"

## Header Filtering

Ignore email headers and quoted boilerplate; focus on actual content:

### Filtered Headers
- From:, Date:, Subject:, To:, Cc:, Bcc:
- "---------- Forwarded message ----------"
- "---------- Original message ----------"
- "On [date] [person] wrote:"
- "Sent from my [device]"

## Duplicate Detection

When checking for existing calendar events (`check_duplicate.sh`), duplicates
are identified by:

1. **Same Date**: Events on the same calendar day
2. **Similar Title** (keyword match on the first 5 normalized words):
   - Short titles (1-2 keywords): ALL keywords must match
   - Longer titles (3+ keywords): at least 50% of keywords must match

If a duplicate is found, update the existing event rather than creating a new
one. For ambiguous matches, use semantic judgement and confirm with the user.

## Edge Cases

### Cancellations
If an email contains cancellation language:
- "Cancelled", "Canceled", "Postponed", "Rescheduled"
- "No longer happening", "Won't take place"

You should:
1. Look up the existing event (`lookup_event.sh`, then `calendar_search.sh`)
2. Either delete it (`calendar_delete.sh`) or update the title with a
   "CANCELLED" prefix (`create_event.sh` with the existing event ID)

### Recurring Events
Extract each occurrence as a separate event. Recurring patterns ("every Monday",
"weekly") are noted; multi-day spans use `--rrule` (see gog-commands.md).

### Time Zones
Assume all times are in the user's local timezone. Time zone information in
emails is noted in the description but not used for conversion.

### All-Day Events
When detected, all-day events are created with:
- Start: 9:00 AM
- End: 5:00 PM
- Duration: 8 hours

This provides a visual block in the calendar while maintaining flexibility.

## What to Extract

For each event, produce the structured fields listed in SKILL.md "Extract
Events" — `title`, `date`, `day_of_week`, `time`, `is_multi_day`,
`is_recurring`, `confidence`, `urls`, and any `deadline_date` /
`deadline_action` / `deadline_url`. Those values are then passed to
`create_event.sh`.
