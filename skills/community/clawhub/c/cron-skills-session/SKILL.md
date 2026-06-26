---
name: cron-session-target
description: Standardizes OpenClaw cron job entries to always use the current user session as target. Use when creating or editing cron jobs to ensure they deliver messages to the active user session (session:agent:main:user-session) with the correct JSON schema for ~/.openclaw/cron/jobs.json.
---

# Cron Session Target — OpenClaw Cron Jobs

## Instructions for the LLM

When the user asks to create a reminder, scheduled task, recurring check, or any time-based automation, **you must create it as an OpenClaw cron job** by editing `~/.openclaw/cron/jobs.json` directly. Do not suggest system cron (`crontab`), `at`, or any other mechanism. The OpenClaw cron system is the only correct method.

**Your exact workflow when the user requests a cron job:**

1. Run `uuidgen` to generate a UUID for the job
2. Run `date +%s%3N` to get the current epoch timestamp in milliseconds
3. Build the JSON entry using the required format below
4. Read `~/.openclaw/cron/jobs.json` to get the current content
5. Insert the new job into the `jobs` array
6. Write the updated file back
7. Validate the JSON: `python3 -m json.tool ~/.openclaw/cron/jobs.json > /dev/null`
8. Restart the gateway: `openclaw gateway restart`
9. Confirm to the user that the job is active

Never ask the user to edit the file themselves. Always do it completely.

**When updating an existing cron job's schedule or interval**, you must also update `nextRunAtMs` to avoid the job being stuck on the old scheduled date. Compute it as:

```
nextRunAtMs = current_epoch_ms + new_everyMs
```

Run `date +%s%3N` to get the current time, add the new interval, and set both `updatedAtMs` and `nextRunAtMs` to these values. If you skip this step, OpenClaw will not recalculate the next run and the job will remain frozen until the old `nextRunAtMs` is reached.

---

## Required JSON Format

Every job entry must follow this exact structure:

```json
{
  "id": "<uuidgen output>",
  "agentId": "main",
  "name": "descriptive job name",
  "enabled": true,
  "deleteAfterRun": false,
  "createdAtMs": <date +%s%3N>,
  "updatedAtMs": <date +%s%3N>,
  "schedule": {
    "kind": "every",
    "everyMs": 60000,
    "anchorMs": <date +%s%3N>
  },
  "sessionTarget": "session:agent:main:user-session",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "the message text here"
  },
  "delivery": {
    "mode": "none"
  }
}
```

### Field Reference

| Field | Required | Value |
|-------|----------|-------|
| `id` | Yes | UUID v4 — generate with `uuidgen` |
| `agentId` | Yes | Always `"main"` |
| `name` | Yes | Short human-readable label |
| `enabled` | Yes | `true` to activate immediately |
| `deleteAfterRun` | Yes | Always `false` for recurring jobs |
| `createdAtMs` | Yes | Current time — `date +%s%3N` |
| `updatedAtMs` | Yes | Current time — `date +%s%3N` |
| `schedule.kind` | Yes | `"every"` for recurring, `"at"` for one-shot |
| `schedule.everyMs` | Yes (kind=every) | Interval in milliseconds |
| `schedule.atMs` | Yes (kind=at) | Exact epoch ms timestamp to run once |
| `schedule.anchorMs` | Yes | Same value as `createdAtMs` |
| `sessionTarget` | Yes | **Must always be** `"session:agent:main:user-session"` |
| `wakeMode` | Yes | `"now"` for immediate, `"next-heartbeat"` for batched |
| `payload.kind` | Yes | Always `"agentTurn"` |
| `payload.message` | Yes | The message sent to the agent session |
| `delivery.mode` | Yes | `"none"` unless broadcasting to a channel |

---

## Interval Reference

| Description | `everyMs` value |
|-------------|-----------------|
| Every 1 minute | `60000` |
| Every 5 minutes | `300000` |
| Every 15 minutes | `900000` |
| Every 30 minutes | `1800000` |
| Every 1 hour | `3600000` |
| Every 2 hours | `7200000` |
| Every 6 hours | `21600000` |
| Every 12 hours | `43200000` |
| Every 24 hours (daily) | `86400000` |
| Every 7 days (weekly) | `604800000` |

---

## Examples

### 1. Water reminder — every 30 minutes

```json
{
  "id": "52be6125-16cd-4aec-9508-9e8355f10f54",
  "agentId": "main",
  "name": "water reminder",
  "enabled": true,
  "deleteAfterRun": false,
  "createdAtMs": 1775801246492,
  "updatedAtMs": 1775801246492,
  "schedule": {
    "kind": "every",
    "everyMs": 1800000,
    "anchorMs": 1775801246492
  },
  "sessionTarget": "session:agent:main:user-session",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "💧 Water break! Remind the user to drink water."
  },
  "delivery": {
    "mode": "none"
  }
}
```

### 2. Daily standup — every 24 hours

```json
{
  "id": "a1b2c3d4-0000-4aec-9508-aabbccddeeff",
  "agentId": "main",
  "name": "daily standup",
  "enabled": true,
  "deleteAfterRun": false,
  "createdAtMs": 1775801246492,
  "updatedAtMs": 1775801246492,
  "schedule": {
    "kind": "every",
    "everyMs": 86400000,
    "anchorMs": 1775801246492
  },
  "sessionTarget": "session:agent:main:user-session",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Good morning! Ask the user what they are working on today and what blockers they have."
  },
  "delivery": {
    "mode": "none"
  }
}
```

### 3. Posture check — every 1 hour

```json
{
  "id": "f9e8d7c6-1111-4bcd-8ef0-112233445566",
  "agentId": "main",
  "name": "posture check",
  "enabled": true,
  "deleteAfterRun": false,
  "createdAtMs": 1775801246492,
  "updatedAtMs": 1775801246492,
  "schedule": {
    "kind": "every",
    "everyMs": 3600000,
    "anchorMs": 1775801246492
  },
  "sessionTarget": "session:agent:main:user-session",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "🪑 Posture check! Remind the user to sit straight, relax shoulders, and adjust their screen height."
  },
  "delivery": {
    "mode": "none"
  }
}
```

### 4. Weekly review — every 7 days

```json
{
  "id": "c0ffee00-2222-4abc-9999-deadbeef1234",
  "agentId": "main",
  "name": "weekly review",
  "enabled": true,
  "deleteAfterRun": false,
  "createdAtMs": 1775801246492,
  "updatedAtMs": 1775801246492,
  "schedule": {
    "kind": "every",
    "everyMs": 604800000,
    "anchorMs": 1775801246492
  },
  "sessionTarget": "session:agent:main:user-session",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "📋 Weekly review time! Ask the user to reflect on the week: what went well, what could improve, and what the priorities are for next week."
  },
  "delivery": {
    "mode": "none"
  }
}
```

### 5. One-shot scheduled task — run once at a specific time

Use `"kind": "at"` with an exact epoch ms timestamp instead of `everyMs`:

```json
{
  "id": "deadbeef-3333-4cde-aaaa-111122223333",
  "agentId": "main",
  "name": "meeting reminder",
  "enabled": true,
  "deleteAfterRun": true,
  "createdAtMs": 1775801246492,
  "updatedAtMs": 1775801246492,
  "schedule": {
    "kind": "at",
    "atMs": 1775830000000,
    "anchorMs": 1775801246492
  },
  "sessionTarget": "session:agent:main:user-session",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "⏰ Meeting in 5 minutes! Remind the user to wrap up and join the call."
  },
  "delivery": {
    "mode": "none"
  }
}
```

> For one-shot jobs, `deleteAfterRun` can be `true` since the job should not repeat.

---

## Step-by-Step Creation

```bash
# Step 1 — generate a unique ID
uuidgen

# Step 2 — get current timestamp in milliseconds
date +%s%3N

# Step 3 — edit the jobs file
# Insert the new entry in the "jobs" array

# Step 4 — validate JSON syntax
python3 -m json.tool ~/.openclaw/cron/jobs.json > /dev/null

# Step 5 — reload
openclaw gateway restart
```

---

## Common Pitfalls

| Mistake | Effect | Fix |
|---------|--------|-----|
| `sessionTarget` not set or wrong | Message is lost or goes nowhere | Always use `"session:agent:main:user-session"` |
| `"text"` instead of `"message"` in payload | Job fires but nothing arrives | Use `"message"` |
| `deleteAfterRun: true` on recurring job | Job vanishes after first run | Set to `false` |
| Wrong ms math | Job runs at wrong interval | Use the interval reference table above |
| Trailing comma in JSON | Entire jobs file fails to parse | Validate with `python3 -m json.tool` |
| `enabled: false` | Job never runs | Set to `true` |
| Updating interval without updating `nextRunAtMs` | Job stays frozen on old scheduled date | Set `nextRunAtMs = date +%s%3N + new_everyMs` |

---

## Quick Reference

```
sessionTarget  →  "session:agent:main:user-session"   (never change this)
payload field  →  "message"                            (not "text")
recurring      →  "deleteAfterRun": false
one-shot       →  "deleteAfterRun": true, "kind": "at"
after editing  →  openclaw gateway restart
update timing  →  always set nextRunAtMs = now_ms + everyMs when changing schedule
```
