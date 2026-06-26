# Claude Code CLI Sessions

## Purpose
Track background Claude Code CLI sessions for status queries.

## Session Registry

| Session ID | Label | Task | Started | Status |
|------------|-------|------|---------|--------|
| (populated at runtime) | (human-readable name) | (what it's doing) | (timestamp) | (running/completed/failed) |

## How It Works

### Starting a Session
```json
exec({
  command: "claude --print --dangerously-skip-permissions 'Task description'",
  background: true,
  yieldMs: 10000
})
// Returns: sessionId: "tender-nexus" or similar
```

**After starting:** Immediately log the session to this file:
```
| tender-nexus | refactor-auth | Refactor auth module | 2026-03-24 08:50 UTC | running |
```

### Checking Status
When user asks "what's the status?" or "is it done?":
```json
process({
  action: "log",
  sessionId: "tender-nexus"
})
```

### Completing a Session
When done, update the status column:
```
| tender-nexus | refactor-auth | Refactor auth module | 2026-03-24 08:50 UTC | completed |
```

### Cleanup
Remove completed sessions older than 24 hours during heartbeat cleanup.

## Session Label Naming Convention

Use descriptive labels that match the task:
- `build-feature-X` — Building a new feature
- `refactor-Y-module` — Refactoring code
- `fix-bug-Z` — Bug fix
- `test-coverage-A` — Adding tests
- `cleanup-legacy-B` — Removing old code

## Storage Location

This file: `~/memory/claude-code-sessions.md`

Before starting any Claude Code task, read this file to:
1. Check if a similar task is already running
2. Get the session ID for status queries
3. Clean up stale entries

## Example Flow

### User: "Build a login page"
1. Read this file (check for conflicts)
2. Start exec with background: true
3. Note sessionId from response
4. Append new row to registry
5. Report to user: "Started building login page (session: build-login-page)"

### User: "What's the status?"
1. Read this file to find session ID
2. Call process(action: "log", sessionId: "...")
3. Summarize output for user

### User: "Cancel it"
1. Call process(action: "kill", sessionId: "...")
2. Update status to "cancelled"
3. Confirm to user

## Rules

1. **Always log** — Every background session must be recorded here
2. **Use labels** — Never refer to sessions by ID alone, always use the human-readable label
3. **Update status** — Mark completed/failed/cancelled as soon as known
4. **Clean up** — Remove old entries during heartbeat (older than 24h)
5. **One task per session** — Don't queue multiple tasks in one session