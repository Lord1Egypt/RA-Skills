---
name: async-queue
description: "Schedule delayed tasks between OpenClaw agents — set reminders, chain tasks, coordinate agents on a delay. File-backed, no infra needed. NOT for cron-style recurring jobs (use openclaw cron) or immediate actions."
version: 1.0.6
security_disclosure: |
  This skill installs a background daemon (macOS launchd) that polls a local queue file every 30s.
  daemon.js uses Node's built-in http module to POST to the local queue-wake plugin endpoint (127.0.0.1 only) — no execSync or shell invocations.
  Files are written to ~/.openclaw/queue/ (queue state) and ~/.openclaw/extensions/queue-wake/ (plugin).
  Agent targets are user-configured via ~/.openclaw/queue/targets.json — no hard-coded agent names.
  The install.sh script must be run manually — nothing runs automatically on skill install.
  All code is open source and auditable in this skill package.
---

# Async Queue

A lightweight, file-backed task queue that fires delayed tasks to any OpenClaw agent at a scheduled time. Consists of four components:

| Component | What it does |
|-----------|-------------|
| **daemon.js** | Polls `queue.json` every 30s, delivers due tasks via the queue-wake plugin |
| **push.js** | CLI to enqueue a new task with a delay |
| **queue-cli.js** | CLI to list pending tasks, cancel by id prefix, and view history |
| **queue-wake plugin** | OpenClaw plugin that receives delivery from daemon, enqueues a system event, and calls `requestHeartbeatNow` for near-exact timing |

---

## Installation (first time, macOS)

```bash
bash "$(openclaw skill path async-queue)/scripts/install.sh"
```

This will:
1. Copy `daemon.js` + `push.js` to `~/.openclaw/queue/`
2. Copy the `queue-wake` plugin to `~/.openclaw/extensions/queue-wake/`
3. Register the daemon under launchd (auto-starts on login, auto-restarts on crash)

Then restart the OpenClaw gateway to activate the plugin:
```bash
openclaw gateway restart
```

---

## Push a task

```bash
node ~/.openclaw/queue/push.js --task "description" --delay <10s|5m|2h|HH:MM|H:MMam/pm> [--to <agentId>] [--then "next task text"]
```

**Arguments:**
- `--to` — agent name (e.g. `main`). Can also be a full session key like `agent:main:main`. Optional; defaults to `queue/config.json.defaultTo` if set, else `marcus`.
- `--task` — what the agent should do when this fires
- `--delay` — how long from now: `10s`, `5m`, `2h`, or absolute time: `HH:MM` (24h) / `H:MMam` (12h)
- `--then` — optional chained task text to enqueue immediately after this task fires
- `--ttl` — (optional) seconds before item expires if undelivered (default: 300)

**Examples:**
```bash
# Remind in 30 minutes
node ~/.openclaw/queue/push.js --to main --task "Follow up: did the user save that document?" --delay 30m

# Check deploy health in 5 minutes
node ~/.openclaw/queue/push.js --to main --task "Verify deploy is healthy — check HTTP status" --delay 5m

# Fire today at 6:30 PM (or tomorrow if already past)
node ~/.openclaw/queue/push.js --task "Ping me before dinner" --delay 6:30pm

# Tonight reminder
node ~/.openclaw/queue/push.js --to main --task "Ask user about the pending decision" --delay 2h

# Chain a follow-up immediately after the first task fires
node ~/.openclaw/queue/push.js --task "Run deploy checks" --delay 10m --then "Verify logs are clean"
```

---

## When to use this skill

**Use async-queue when:**
- User asks to be reminded about something in X minutes/hours
- You spawn a sub-agent or background job and need to check back on it
- A follow-up needs to happen after a delay (e.g. verify a deploy, nudge a pending action)
- Any work that can't be completed this turn and needs to continue later

**Don't use async-queue for:**
- Immediate actions → just do them
- Recurring schedules → use `openclaw cron`
- Tasks waiting on user input → message the user directly

---

## Schema

```json
{
  "id": "uuid",
  "to": "agentId",
  "task": "string — what to execute when this fires",
  "then": "string — optional chained task to enqueue after successful fire",
  "runAt": "ISO 8601 timestamp",
  "createdAt": "ISO 8601 timestamp",
  "ttl": 300
}
```

`ttl`: seconds the item may remain undelivered before being dropped (default: 300s). Increase for tasks scheduled many hours out if the daemon might miss a window.

---

## Delivery flow

```
push.js → queue.json → daemon.js (polls 30s)
   → POST /api/queue-wake (queue-wake plugin)
      → enqueueSystemEvent([QUEUE:agentId] task)
      → requestHeartbeatNow(agentId)
         → agent wakes, sees task in context
```

---

## Check queue state

```bash
cat ~/.openclaw/queue/queue.json         # pending items
node ~/.openclaw/queue/queue-cli.js list # pretty list
node ~/.openclaw/queue/queue-cli.js history # last 20 deliveries
node ~/.openclaw/queue/queue-cli.js cancel <idPrefix>
tail -20 ~/.openclaw/queue/daemon.log    # delivery history
```

---

## Daemon status (macOS)

```bash
launchctl list | grep queue-daemon       # running?

# Restart if needed:
launchctl unload  ~/Library/LaunchAgents/ai.openclaw.queue-daemon.plist
launchctl load    ~/Library/LaunchAgents/ai.openclaw.queue-daemon.plist
```

---

## Files installed

| Path | Purpose |
|------|---------|
| `~/.openclaw/queue/daemon.js` | Polling daemon |
| `~/.openclaw/queue/push.js` | Push CLI |
| `~/.openclaw/queue/queue.json` | Queue state file |
| `~/.openclaw/queue/daemon.log` | Delivery log |
| `~/.openclaw/extensions/queue-wake/` | OpenClaw plugin |
| `~/Library/LaunchAgents/ai.openclaw.queue-daemon.plist` | launchd service |

---

## Protocol

See `references/PROTOCOL.md` for the full protocol: when to queue, rules, TTL guidance, and common task patterns.
