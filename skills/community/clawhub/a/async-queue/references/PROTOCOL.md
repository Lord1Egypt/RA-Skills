# Async Queue Protocol

*Generic protocol for any OpenClaw agent using the async-queue skill.*

---

## Push Syntax

```bash
node ~/.openclaw/queue/push.js --to <agentId> --task "..." --delay <10s|5m|2h>
```

**Delay formats:** `10s` (seconds), `5m` (minutes), `2h` (hours)

**`--to` values:** Any agent name registered with your OpenClaw instance (e.g. `main`).

---

## When to Queue

### Always
- **After spawning a sub-agent / coding task** → queue a status check in 15–30 min  
  `"Check [session-name]: did it complete? Report back."`
- **After a deploy or background job** → queue a health check in 5–10 min  
  `"Verify [service] is healthy — check logs or HTTP status."`
- **After promising a follow-up** → queue it immediately, don't rely on memory
- **Any task you can't complete this turn** → queue the next step

### Never
- Immediate actions → just do them now
- Recurring jobs → use `openclaw cron`
- Tasks that need the user's input first → message the user directly

---

## Rules

1. **Confirm every push out loud** — tell the user what was queued and when it fires
2. **Always verify background tasks** — queue a check after any async work you initiate
3. **Re-queue on failure** — never let a task silently die; if delivery fails, retry or escalate
4. **Respect TTL** — items expire after `ttl` seconds if undelivered (default: 300s / 5 min); increase for long windows

---

## Schema

```json
{
  "id": "uuid",
  "to": "agentId",
  "task": "string — what to do when this fires",
  "runAt": "ISO 8601 timestamp",
  "createdAt": "ISO 8601 timestamp",
  "ttl": 300
}
```

---

## Common Queue Tasks

| Trigger | `--to` | Task | Delay |
|---------|--------|------|-------|
| Sub-agent spawned | `main` | `"Check [session]: complete? Report back."` | 20m |
| Background deploy | `main` | `"Verify [service] health — is it responding?"` | 5m |
| User says "remind me in X" | `main` | The reminder text | Xm/h |
| Pending action from user | `main` | Follow-up nudge | 30m–2h |

---

## Check Queue State

```bash
cat ~/.openclaw/queue/queue.json      # pending items
tail -20 ~/.openclaw/queue/daemon.log # delivery history
```

---

## Daemon Status (macOS / launchd)

```bash
launchctl list | grep queue-daemon    # check if running

# Restart:
launchctl unload  ~/Library/LaunchAgents/ai.openclaw.queue-daemon.plist
launchctl load    ~/Library/LaunchAgents/ai.openclaw.queue-daemon.plist
```

The daemon polls every 30 seconds. Combined with `requestHeartbeatNow` in the queue-wake plugin, tasks typically deliver within ~1 second of their scheduled time.
