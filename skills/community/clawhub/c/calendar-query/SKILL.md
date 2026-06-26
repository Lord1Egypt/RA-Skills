---
name: calendar-query
description: Query Matt's calendars with the gog CLI. Always prioritize the Flowcode work calendar (matt.williams@flowcode.com) and include personal calendar (williams.e.matt@gmail.com) context when relevant. Use when asked about schedules, events, availability, or reminders.
---

# Calendar Query Skill

Use the `gog` CLI (already authenticated as ferdi.bot.matt@gmail.com) to read Matt's calendars. Always follow this order:

1. **Work calendar first** — matt.williams@flowcode.com
2. **Personal calendar as aside** — williams.e.matt@gmail.com (summaries, FYIs)

## Commands

### List events for a specific day
```
gog calendar events <calendar_id> --from "YYYY-MM-DDT00:00:00" --to "YYYY-MM-DDT23:59:59"
```
- Example (work calendar tomorrow):
```
gog calendar events matt.williams@flowcode.com --from "2026-03-18T00:00:00" --to "2026-03-18T23:59:59"
```

### Relative ranges
- `--tomorrow`, `--today`, `--days N`, `--week`
- Example: next 7 days on personal calendar
```
gog calendar events williams.e.matt@gmail.com --days 7
```

### Keyword search
```
gog calendar events <calendar_id> --query "keyword" --from <start> --to <end>
```
Use for finding Bulls games, travel, etc.

### Multiple calendars at once
Use separate commands per calendar and merge results in your reply.

## Response Pattern
1. Summarize **work calendar** events chronologically (time + title + context).
2. Add **personal calendar** notes afterward if relevant ("On personal calendar: ...").
3. Mention all-day events clearly.

## Tips
- Use ISO timestamps; `--from/--to` are required for single-day accuracy.
- For afternoon-specific questions, query narrowed windows (`--from "2026-03-24T12:00:00"`).
- When unsure about date, confirm with the user.
- If `gog` errors, include the error message and suggest retrying or re-authenticating.
