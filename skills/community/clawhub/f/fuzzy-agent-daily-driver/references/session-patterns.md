# Session Patterns — Spawn, Schedule, Delegate

## The Three Session Types

### 1. Main Session (this one)
Direct chat with user. Long-lived. Has full workspace access.

### 2. Isolated Sub-Agent (`sessions_spawn`)
Ephemeral one-shot. Good for parallel work or anything that might timeout.

```javascript
sessions_spawn({
  task: "Research competitor products and write a summary",
  runtime: "subagent",
  mode: "run",
  runTimeoutSeconds: 300,
  cleanup: "delete"
})
```

### 3. Named Persistent Sessions
Long-running agents with their own workspace (alex, cellini, scout, dev).

```javascript
// Send work to a named agent
sessions_send({
  sessionKey: "alex",
  message: "Check the daily sales numbers and flag any anomalies"
})

// Get their recent history
sessions_history({ sessionKey: "alex", limit: 10 })
```

---

## Cron — The Schedule Pattern

Cron jobs are the backbone of "set it and forget it."

### Morning Briefing (7 AM Johannesburg)
```javascript
cron({
  action: "add",
  job: {
    name: "Morning briefing",
    schedule: { kind: "cron", expr: "0 7 * * *", tz: "Africa/Johannesburg" },
    sessionTarget: "isolated",
    payload: {
      kind: "agentTurn",
      message: "Morning check: emails, calendar, weather, any urgent items",
      timeoutSeconds: 120
    }
  }
})
```

### After Session Cleanup
```javascript
cron({
  action: "add", 
  job: {
    name: "Session summary writer",
    schedule: { kind: "cron", expr: "0 23 * * *", tz: "Africa/Johannesburg" },
    sessionTarget: "main",
    payload: {
      kind: "systemEvent",
      text: "SESSION_SUMMARY_REQUEST"
    }
  }
})
```

### Check Every 30 Minutes (Heartbeat)
```javascript
// Add to HEARTBEAT.md instead — lighter than cron
cron({
  action: "add",
  job: {
    name: "Periodic health check",
    schedule: { kind: "every", everyMs: 1800000 },  // 30 min
    sessionTarget: "isolated",
    payload: { kind: "agentTurn", message: "Quick health check" }
  }
})
```

---

## Process Management — Long Running Commands

### Start a background process
```javascript
exec({
  command: "python train_model.py --gpu 0",
  background: true,    // don't wait
  timeout: 3600
})
// Returns immediately with sessionId
```

### Poll for completion
```javascript
process({ action: "poll", sessionId: "session-id", timeout: 30000 })
```

### Get logs without blocking
```javascript
process({ action: "log", sessionId: "session-id", limit: 20 })
```

### Write input to a running process
```javascript
process({
  action: "write",
  sessionId: "session-id", 
  data: "yes\n"
})
```

### Kill a stuck process
```javascript
process({ action: "kill", sessionId: "session-id" })
```

---

## Delegation Patterns

### Route to Named Agent
```javascript
sessions_send({
  sessionKey: "alex",
  message: "Handle the Q3 report please",
  timeoutSeconds: 300
})
```

### Send to Channel
```javascript
message({
  action: "send",
  channel: "discord",
  target: "#alerts",
  message: "⚠️ GPU temperature high: 82°C"
})
```

### Broadcast to Multiple Channels
```javascript
["#team", "#ops"].forEach(channel => {
  message({
    action: "send",
    channel: "discord",
    target: channel,
    message: "System update complete"
  })
})
```

---

## Heartbeat vs Cron — When to Use Which

| Pattern | Use When |
|---------|----------|
| **Heartbeat** | Multiple checks batched together, conversational context needed |
| **Cron** | Exact timing matters, one-shot reminders, isolated from session history |

---

## Session ID Patterns

- `sessions_list({ activeMinutes: 60 })` — find recently active sessions
- `sessions_history({ sessionKey: "alex", limit: 5 })` — last 5 messages
- `sessions_send` waits for response; use `yield` after spawning if you need to continue working in parallel
