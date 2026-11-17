---
name: cron-quickstart
description: Use the OpenClaw cron tool for scheduling reminders, delayed follow-ups, and recurring periodic checks. Covers one-shot and recurring schedules, session targeting, delivery modes, and wake events.
metadata: {"openclaw":{"emoji":"⏰"}}
---

# Cron Quickstart Skill

Schedule reminders, delayed tasks, and periodic checks using the OpenClaw `cron` tool.

## When to Use

- One-shot reminders ("remind me in 20 minutes")
- Recurring periodic tasks ("every Monday at 9 AM")
- Deferred follow-ups ("check back after the meeting")
- Waking a session at a specific time

## Schedule Types

### One-shot (`at`)
```json
{ "kind": "at", "at": "2026-09-02T18:00:00Z" }
```

### Recurring (`every`)
```json
{ "kind": "every", "everyMs": 3600000 }
```

### Cron expression (`cron`)
```json
{ "kind": "cron", "expr": "0 9 * * 1-5", "tz": "Asia/Shanghai" }
```

## Payload Types

- **systemEvent** — Injects text as a system event into a session (use with `sessionTarget: "main"`)
- **agentTurn** — Runs an agent turn with a message (use with `sessionTarget: "isolated"` or `"current"`)

## Common Patterns

### Simple Reminder
```json
{
  "name": "Meeting reminder",
  "schedule": { "kind": "at", "at": "2026-09-02T09:00:00Z" },
  "payload": { "kind": "systemEvent", "text": "Reminder: Team standup meeting starts now." },
  "sessionTarget": "main"
}
```

### Periodic Check
```json
{
  "name": "Email triage",
  "schedule": { "kind": "every", "everyMs": 21600000 },
  "payload": { "kind": "agentTurn", "message": "Check for urgent emails and summarize." },
  "sessionTarget": "isolated",
  "delivery": { "mode": "announce" }
}
```

### Cron Schedule
```json
{
  "name": "Morning briefing",
  "schedule": { "kind": "cron", "expr": "0 8 * * *", "tz": "Asia/Shanghai" },
  "payload": { "kind": "agentTurn", "message": "Prepare a morning briefing of calendar, news, and weather." },
  "sessionTarget": "current"
}
```

## Key Constraints

- `sessionTarget: "main"` **requires** `payload.kind: "systemEvent"`
- `sessionTarget: "isolated" | "current" | "session:xxx"` **requires** `payload.kind: "agentTurn"`
- ISO timestamps without timezone are treated as UTC
- Use `delivery.mode: "announce"` for isolated agent results
- Use `deleteAfterRun: true` for one-shot jobs that should auto-cleanup

## Manage Jobs

- List: `cron list`
- Run immediately: `cron run`
- Check history: `cron runs`
- Remove: `cron remove`
- Wake session: `cron wake`
