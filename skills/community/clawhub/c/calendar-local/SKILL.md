---
name: calendar-local
description: Read Google Calendar from the local host using the configured gog wrapper. Use when the user asks for their agenda, calendar events, today's schedule, this week's events, upcoming appointments, or calendar summaries on this OpenClaw host. Applies to direct chats including Telegram when the runtime has access to /home/ubuntu/.openclaw/workspace/.openclaw/calendar.sh and GOG_KEYRING_PASSWORD is present in the service environment.
---

# Calendar Local

Use the local wrapper instead of generic calendar advice.

## Commands

Run the wrapper with an explicit timeframe:

```bash
/home/ubuntu/.openclaw/workspace/.openclaw/calendar.sh today
/home/ubuntu/.openclaw/workspace/.openclaw/calendar.sh week
/home/ubuntu/.openclaw/workspace/.openclaw/calendar.sh days 7
```

The wrapper already targets the correct Google account and gog binary. It requires `GOG_KEYRING_PASSWORD` in the runtime environment.

## Workflow

1. Run the wrapper with the matching timeframe.
2. If the user asked for **today**, use `today`.
3. If the user asked for **this week**, use `week`.
4. If the user asked for **the next few days**, use `days N`.
5. Summarize results in natural language.
6. If no events match, say so plainly.
7. Do not tell the user to configure OAuth again unless the wrapper fails.

## Failure handling

If the wrapper fails:
- If output mentions `GOG_KEYRING_PASSWORD is not set`, explain that the OpenClaw service is missing the keyring password in its environment.
- If output mentions keyring unlock/auth errors, explain that the local Google token/keyring is unavailable or locked.
- Only then fall back to setup guidance.

## Output style

- Be concise.
- Prefer grouped agenda summaries.
- Separate all-day items, timed events, and birthdays/tasks when useful.
