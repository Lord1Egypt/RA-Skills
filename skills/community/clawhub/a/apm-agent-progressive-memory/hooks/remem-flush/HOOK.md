---
name: remem-flush
description: "Memory flush hook for /remem command. Updates flush-state.json with mtime-gated delta tracking when user (or cron) sends /remem. Channel-agnostic."
metadata: |
  {
    "openclaw": {
      "export": "handler",
      "events": ["message:received", "system:event"]
    }
  }
---

# remem-flush Hook

Intercepts `/remem` commands and triggers a 6-step memory flush that
records mtime-based deltas. This is the **detection** side of APM
flushing; actual memory-file updates happen via the agent's own
write-back (see SKILL.md → "Write-Back on Updates").

## Events

- `message:received` — manual `/remem` from user
- `system:event` — cron-triggered `/remem` (e.g. 06:17 / 18:17 Asia/Shanghai)

> The `system:event` support was added in v1.6.0 to enable scheduled
> flushes without user intervention. The handler detects both event types
> and routes to the same logic.

## Behavior (6 steps)

1. **Intercept** messages matching `/remem` or `/remem <args>`
2. **Extract** session context (sessionId, contextUsage)
3. **Discover** active memory groups under `memory/groups/`
4. **Read** old mtime records from `flush-state.json`
5. **Compute** deltas (files modified since last flush)
6. **Stamp** new mtimes + flush timestamp into `flush-state.json`

The hook does **NOT** modify `memory/main/*.md` or
`memory/groups/{name}/*.md` — those are the agent's job (via
`memory_get` / `write` after this hook signals pending deltas).

## Files Modified

| File | When | Notes |
|------|------|-------|
| `memory/flush-state.json` | Every flush | mtime records + flush timestamp |
| `memory/groups/flush-state.json` | Every flush (if groups active) | Per-group mtime records |

> ⚠️ The handler currently writes to a single `memory/flush-state.json`
> regardless of chat type. A future revision will split this into DM vs
> group files per `apm_session_start` hook's privacy boundary. For now,
> group flushes share the DM flush-state — a known limitation.

## Files Read

- `memory/groups/*.md` (filenames only — used to discover group names)
- `memory/flush-state.json` (existing mtimes)
- `event.context.content` (for `/remem` detection)
- `event.context.usagePercent` (for context-usage recording)
