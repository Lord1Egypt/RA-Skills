---
name: context-persistence
description: Solve cross-session context storage and sync problems. Use when (1) isolated sessions (cron/subagent/heartbeat) lack context from main session, (2) long-running tasks need progress tracking across sessions, (3) multiple sessions need shared state, (4) users report "agent doesn't remember what happened", (5) designing memory/progress systems for AI agents. Triggers on "context sync", "session memory", "progress tracking", "cross-session state", "memory mechanism", "persist progress".
---

# Context Persistence & Cross-Session Sync

Design and implement persistent context systems that survive session boundaries.

## Core Problem

OpenClaw has multiple session types with different context access:

| Session | Memory Files | History | Cron Context |
|---------|-------------|---------|-------------|
| Main DM | ✅ All injected | ✅ Full | N/A |
| Group Chat | ❌ Not loaded | ✅ Partial | N/A |
| Cron (isolated) | ❌ None | ❌ None | ✅ Payload only |
| Heartbeat | ❌ None | ✅ Partial | N/A |
| Subagent | ❌ None | ❌ None | ✅ Task only |

**Result**: State created in one session is invisible to others unless persisted to files.

## Architecture: Three-Layer Memory System

### Layer 1: Long-Term Memory (MEMORY.md)
- **What**: Curated facts, decisions, lessons, key state
- **Who writes**: Main session only
- **Who reads**: Main session only (injected via AGENTS.md)
- **Update frequency**: On significant events, periodic review during heartbeats
- **Size limit**: < 200 lines (context budget)

### Layer 2: Daily Logs (memory/YYYY-MM-DD.md)
- **What**: Raw chronological notes, conversations, decisions
- **Who writes**: Any session that has something to record
- **Who reads**: Main session (at startup), heartbeats (for review)
- **Update frequency**: Real-time as events happen
- **Size limit**: Unbounded (not injected into context)

### Layer 3: Task Progress Files (memory/<task>-progress.md)
- **What**: Structured progress for long-running work
- **Who writes**: Any session doing the task
- **Who reads**: Any session continuing the task
- **Update frequency**: At task boundaries (session end, checkpoints)
- **Size limit**: < 300 lines

### The Key Insight

> **Files are the only cross-session communication channel.**
> In-memory state dies with the session. Files survive.

## Pattern 1: Progress Tracking

For tasks spanning multiple sessions (source code reading, data analysis, etc.)

See [references/progress-tracking.md](references/progress-tracking.md) for full template.

Essential elements:
```markdown
# <Task> Progress
- Total: X items
- Completed: Y items  
- Progress: Z%
## Completed List (dedup)
## Current Position / Next Steps
## Key Findings
```

## Pattern 2: Cron Job Context Injection

Isolated cron sessions have NO access to workspace memory. Solutions:

1. **Embed context in payload message** (for <1KB state)
2. **Read from progress files** (task loads its own context)
3. **Shared state file** (coordination between sessions)

See [references/cross-session-sync.md](references/cross-session-sync.md) for patterns.

## Pattern 3: Main Session Initialization

The AGENTS.md startup sequence ensures context loading:

```
1. Read SOUL.md (persona)
2. Read USER.md (who you help)
3. Read memory/YYYY-MM-DD.md (today + yesterday)
4. If main session: also read MEMORY.md
```

This is the ONLY automated context loading. Everything else must be explicit.

## Quick Checklist

When designing context for a new task:

- [ ] Can this span multiple sessions? → Create progress file
- [ ] Does cron/subagent need this? → Embed in payload or file
- [ ] Is this a fact to remember? → Update MEMORY.md
- [ ] Is this a raw event? → Append to daily log
- [ ] Should future sessions know this? → Write it DOWN, never rely on memory
