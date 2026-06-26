---
name: fuzzy-cron-scheduler
description: "Master OpenClaw cron scheduling for reliable background tasks, reminders, and recurring automation. Use when: (1) setting up periodic checks or heartbeats, (2) scheduling one-shot or recurring tasks, (3) choosing between main/isolated/current session targets, (4) configuring webhook or announce delivery, (5) troubleshooting missed or stuck cron jobs. Triggers on phrases like schedule this, run every X, cron job, periodic task, recurring reminder, background scheduler, set a reminder."
---

# Cron Scheduler

Schedule one-shot or recurring background tasks with OpenClaw's cron system. Background tasks run silently without cluttering your main session — results come back as announcements or webhook pings.

## Core Concepts

### Schedule Types

| Kind | Use When | Example |
|------|----------|---------|
| `at` | One-shot at a specific time | "remind me at 3pm" |
| `every` | Fixed interval (ms-based) | "every 5 minutes" |
| `cron` | Unix-style recurring with timezone | "9am every weekday" |

### Session Targets

Where the job runs and how results are delivered:

| Target | Who Runs It | Best For |
|--------|-------------|---------|
| `isolated` (default for agentTurn) | Fresh ephemeral session | Most recurring tasks — clean, no context bleed |
| `main` (default for systemEvent) | Your main conversation session | System events, heartbeat checks that need session context |
| `current` | Bound to where you are right now | One-off tasks tied to a specific ongoing conversation |
| `session:<name>` | A specific persistent session | Long-running projects that need to accumulate state |

### Delivery Modes

| Mode | What Happens |
|------|-------------|
| `announce` (default) | Result posted to the chat channel |
| `webhook` | HTTP POST to a URL you specify |
| `none` | Silent — task runs, no report |

## Recipes

### Recipe 1: Periodic Heartbeat (every N minutes)

```json
cron_add(
  name="Morning briefing",
  schedule={"kind": "every", "everyMs": 1800000},  // 30 min
  payload={
    "kind": "agentTurn",
    "message": "Check email, calendar, and any urgent notifications. Summarize what needs attention."
  },
  delivery={"mode": "announce"},
  sessionTarget="isolated"
)
```

### Recipe 2: Daily Reminder (cron, specific time)

```json
cron_add(
  name="Standup reminder",
  schedule={"kind": "cron", "expr": "0 9 * * 1-5", "tz": "Africa/Johannesburg"},
  payload={
    "kind": "agentTurn",
    "message": "It's standup time! Check the project tracker and note any blockers."
  },
  delivery={"mode": "announce"},
  sessionTarget="isolated"
)
```

### Recipe 3: One-Shot Future Reminder

```json
cron_add(
  name="Call reminder",
  schedule={"kind": "at", "at": "2026-04-15T14:00:00+02:00"},
  payload={
    "kind": "agentTurn",
    "message": "You have a call with the client in 15 minutes. Review notes in /workspace/call-prep.md"
  },
  delivery={"mode": "announce"},
  sessionTarget="isolated"
)
```

### Recipe 4: Staggered Job Fan-Out

Avoid thundering-herd by staggering identical jobs:

```json
cron_add(
  name="Data sync A",
  schedule={"kind": "cron", "expr": "0 */4 * * *", "tz": "UTC", "staggerMs": 0},
  payload={"kind": "agentTurn", "message": "Sync batch A — /workspace/data/a/*.csv"},
  sessionTarget="isolated"
)

cron_add(
  name="Data sync B",
  schedule={"kind": "cron", "expr": "0 */4 * * *", "tz": "UTC", "staggerMs": 300000},  // +5 min
  payload={"kind": "agentTurn", "message": "Sync batch B — /workspace/data/b/*.csv"},
  sessionTarget="isolated"
)
```

### Recipe 5: Health Check with Webhook Alert

```json
cron_add(
  name="Service health check",
  schedule={"kind": "every", "everyMs": 60000},  // every minute
  payload={
    "kind": "agentTurn",
    "message": "GET /health on your service. If status != 200, compose an alert payload and POST to https://your-webhook-handler.com/alert"
  },
  delivery={"mode": "webhook", "to": "https://your-webhook-handler.com/results"},
  sessionTarget="isolated",
  failureAlert={"after": 3, "mode": "announce", "cooldownMs": 300000}
)
```

### Recipe 6: Batch Heartbeat Checks (main session)

Combine periodic checks into one heartbeat to save API calls:

```json
cron_add(
  name="Morning pulse",
  schedule={"kind": "cron", "expr": "0 7 * * *", "tz": "Africa/Johannesburg"},
  payload={"kind": "systemEvent", "text": "Read HEARTBEAT.md if it exists. Check email, calendar, weather. If nothing needs attention reply HEARTBEAT_OK."},
  sessionTarget="main"
)
```

### Recipe 7: Project-Scoped Persistent Session

```json
cron_add(
  name="Weekly digest",
  schedule={"kind": "cron", "expr": "0 10 * * 5", "tz": "UTC"},
  payload={
    "kind": "agentTurn",
    "message": "Generate a weekly summary of /workspace/project-x/logs/. Include: tasks completed, blockers, and next steps."
  },
  sessionTarget="session:project-alpha-digest",
  delivery={"mode": "announce"}
)
```

### Recipe 8: Reminder with Snooze Pattern

```json
// Initial reminder
cron_add(
  name="Invoice due",
  schedule={"kind": "at", "at": "2026-04-20T09:00:00+02:00"},
  payload={"kind": "agentTurn", "message": "Invoice #1234 is due today. Draft a follow-up email if not paid. Save to /workspace/drafts/invoice-followup.md"},
  sessionTarget="isolated"
)

// Snooze — 24h later if unacknowledged (use failureAlert + snooze job)
)
```

## Cron Expression Reference

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sun=0)
│ │ │ │ │
* * * * *

Special characters:
  *       any value
  ,       value list separator (1,3,5)
  -       range (1-5)
  /       step (*/15 = every 15)

Examples:
  0 * * * *        every hour at minute 0
  0 9 * * 1-5      9am every weekday
  30 14 1 * *      2:30pm on the 1st of every month
  */15 * * * *     every 15 minutes
  0 0 * * 0        midnight every Sunday
  0 8,12,18 * * *  8am, noon, and 6pm daily
```

## Interval Reference (everyMs)

```json
60000        // 1 minute
300000       // 5 minutes
600000       // 10 minutes
1800000      // 30 minutes
3600000      // 1 hour
86400000     // 1 day
604800000    // 1 week
```

## Managing Jobs

```json
// List all jobs
cron_list()

// List including disabled
cron_list(includeDisabled=true)

// Run a job immediately
cron_run(jobId="<id>")

// Get run history
cron_runs(jobId="<id>")

// Update a job (e.g., disable)
cron_update(jobId="<id>", patch={"enabled": false})

// Remove a job
cron_remove(jobId="<id>")

// Wake a session (e.g., trigger next-heartbeat)
cron_wake(text="Check in now", mode="now")
```

## Failure Alerting

```json
cron_add(
  ...,
  failureAlert={
    "after": 3,                    // alert after N consecutive failures
    "cooldownMs": 300000,          // don't spam — wait 5 min between alerts
    "mode": "announce",             // or "webhook"
    "channel": "discord",
    "to": "alerts"                 // channel or user
  }
)
```

Set `failureAlert: false` to disable alerting entirely for a job.

## Anti-Patterns

- **Don't use `main` session for heavy recurring tasks** — it accumulates context and costs tokens. Use `isolated`.
- **Don't schedule jobs more often than needed** — every job is a LLM call. Batching checks into one heartbeat is cheaper than 5 separate 1-minute jobs.
- **Don't forget failure alerts on critical jobs** — if the task fails 10 times silently, you won't know.
- **Don't use `current` without good reason** — if your current session ends, the job binding becomes orphaned.
- **Don't set staggerMs on isolated jobs** — staggerMs only applies within a single cron expression's firing. For truly staggered behavior, use separate jobs with different schedule times.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Job never fires | Wrong timezone in cron expr | Add explicit `tz` field |
| Duplicate runs | Two jobs with overlapping schedules | Check `cron_list` for duplicates |
| "Session not found" on isolated job | Ephemeral session already expired | Normal — next scheduled run creates a new one |
| No announcement after job runs | Missing `delivery` config | Add `"delivery": {"mode": "announce"}` |
| Too many failures alert | `cooldownMs` too low | Increase `cooldownMs` |
| Job disappeared from list | It was a one-shot that ran | One-shot `at` jobs auto-delete after running |

## See Also

- `heartbeat-patterns` skill — combining cron with in-session heartbeat checks
- `webhook-automation` skill — incoming webhook triggers and outgoing webhook delivery
- `reminder-bot` skill — voice/chat reminder workflows built on cron
