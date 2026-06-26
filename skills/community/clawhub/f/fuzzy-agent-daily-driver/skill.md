---
name: fuzzy-agent-daily-driver
description: The 6 core workflows every OpenClaw agent uses every day — recall, spawn, schedule, research, delegate, monitor-update. A pattern reference for building reliable daily-driver agents.
triggers:
  - "what patterns do you use every day"
  - "how do you recall memory"
  - "how do you run background tasks"
  - "everyday agent workflows"
  - "what tools do you use most"
  - "build a daily driver skill"
installed: true
version: 1.0.0
owner: fuzzyb33s
tags:
  - opencllaw
  - patterns
  - memory
  - cron
  - sessions
  - subagents
  - research
---

# Fuzzy Agent Daily Driver

The 6 workflows that power every effective OpenClaw agent. Master these and you can build any daily-driver setup.

## The 6 Core Patterns

### 1. Recall — Start Every Session Right
Before anything else, search long-term memory. This is mandatory at session start.

```javascript
// Tool: memory_search + memory_get
memory_search({ query: "recent decisions, context, preferences" })
// Then pull the relevant lines
memory_get({ path: "MEMORY.md", from: LINE, lines: 20 })
```

**When to use:** Session startup, before any important decision, when context is unclear.

---

### 2. Spawn — Run Tasks in Isolation
Don't block. Spawn sub-agents for anything that takes more than a few seconds.

```javascript
sessions_spawn({
  task: "Your instruction here",
  runtime: "subagent",
  mode: "run",          // "run" = one-shot, "session" = persistent
  runTimeoutSeconds: 300,
  cleanup: "delete"
})
```

**When to use:** Long-running commands, parallel work, anything that could timeout.

---

### 3. Schedule — Set It and Forget It
Use cron for anything that needs to happen repeatedly or later.

```javascript
cron({
  action: "add",
  job: {
    name: "Daily digest",
    schedule: { kind: "cron", expr: "0 9 * * *", tz: "Africa/Johannesburg" },
    sessionTarget: "isolated",    // or "main" for direct chat
    payload: {
      kind: "agentTurn",
      message: "Run the morning digest check — emails, calendar, news"
    }
  }
})
```

**When to use:** Morning briefings, periodic health checks, reminder follow-ups.

---

### 4. Research — Fetch + Extract + Synthesize
Web fetch for raw content, web search for discovery.

```javascript
// Discover with search
web_search({ query: "latest on topic", count: 5 })

// Deep read a page
web_fetch({ url: "https://...", extractMode: "markdown", maxChars: 8000 })
```

**When to use:** Before answering unfamiliar topics, checking prices/news/status.

---

### 5. Delegate — Route Work to the Right Place
Send tasks to other sessions or agents.

```javascript
// To a named session
sessions_send({ sessionKey: "alex", message: "Handle this please" })

// To a channel
message({ action: "send", channel: "discord", target: "channel-name", message: "Update" })
```

**When to use:** Handing off to specialized agents, sending alerts, cross-channel updates.

---

### 6. Monitor-Update — Track and Adjust
Keep track of long-running work and update records.

```javascript
// Poll a background process
process({ action: "poll", sessionId: "session-id", timeout: 30000 })

// Write results to memory
write({ path: "memory/YYYY-MM-DD.md", content: "## What happened\n..." })
```

**When to use:** After spawning background jobs, at end of session to capture decisions.

---

## Everyday Session Template

Run this at the start of every session:

```javascript
// 1. Recall (mandatory)
memory_search({ query: "today's context, recent decisions" })
memory_get({ path: "MEMORY.md", from: 1, lines: 50 })

// 2. Check cron status (optional)
cron({ action: "list" })

// 3. Check active sessions (optional)
sessions_list({ activeMinutes: 60 })
```

---

## Tool Frequency Guide

| Frequency | Tools |
|-----------|-------|
| Every session | `memory_search`, `memory_get`, `read`, `write` |
| Several times/day | `web_fetch`, `web_search`, `exec`, `process` |
| Daily | `cron`, `sessions_list`, `sessions_history` |
| As needed | `sessions_spawn`, `message`, `gateway`, `subagents` |

---

## Session Startup Checklist

1. `memory_search` — what was decided recently?
2. `memory_get` — pull the relevant MEMORY.md lines
3. Check `HEARTBEAT.md` — any pending tasks?
4. Review `DAILY_SKILLS.md` or project tracker
5. Start working

## Key Files in Your Workspace

| File | Purpose |
|------|---------|
| `MEMORY.md` | Long-term curated memory — update after significant decisions |
| `memory/YYYY-MM-DD.md` | Daily session logs |
| `AGENTS.md` | Agent personality and workspace rules |
| `HEARTBEAT.md` | Periodic background tasks to run |
| `TOOLS.md` | Notes on local environment (cameras, SSH hosts, etc.) |

---

## Anti-Patterns to Avoid

- **Don't busy-poll** — use `sessions_spawn` with callback, not while loops
- **Don't skip memory recall** — context gaps cause errors and重复 work
- **Don't write destructive commands** without asking first
- **Don't respond to everything** in group chats — quality > quantity
- **Don't forget to write it down** — if you learned it, file it

---

## Credits

Pattern framework inspired by the OpenClaw agent architecture — built for the 90-day skill challenge.
