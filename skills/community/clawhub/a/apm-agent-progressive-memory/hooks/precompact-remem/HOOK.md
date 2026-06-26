---
name: precompact-remem
description: "Before session context compaction, record mtime-gated deltas to flush-state.json so no context is lost. Channel-agnostic."
metadata: |
  {
    "openclaw": {
      "export": "handler",
      "events": ["session:compact:before"]
    }
  }
---

# precompact-remem Hook

Intercepts `session:compact:before` and records mtime-based deltas to
`flush-state.json` so context isn't lost when OpenClaw compacts the
transcript. Like `remem-flush`, this is the **detection** side; actual
memory-file updates happen via the agent's own write-back.

## Events

- `session:compact:before` — fires just before OpenClaw compacts the transcript

## Behavior (6 steps)

1. **Detect** session context (messageCount, tokenCount)
2. **Skip** if session too small (msgCount < 10 AND tokens < 1000)
3. **Discover** active memory groups under `memory/groups/`
4. **Read** old mtime records from `flush-state.json`
5. **Compute** deltas (files modified since last flush)
6. **Stamp** new mtimes + flush timestamp into `flush-state.json` with `trigger: "precompact"`

## Why Auto-Trigger?

- `remem-flush` handles **user-explicit** flush (`/remem` command)
- `precompact-remem` handles **automatic** flush (context loss imminent)
- Both share the same mtime-gated delta logic and `flush-state.json` file
- Together they form a belt-and-suspenders safety net for context preservation

## Files Modified

| File | When | Notes |
|------|------|-------|
| `memory/flush-state.json` | Before compaction | Adds `trigger: "precompact"` + mtimes |

> ⚠️ Same known limitation as `remem-flush`: writes to a single
> `memory/flush-state.json` regardless of chat type. Group compaction
> shares the DM flush-state until a future revision adds the split.

## Files Read

- `memory/groups/*.md` (filenames only)
- `memory/flush-state.json` (existing mtimes)
- `event.context.messageCount`, `event.context.tokenCount`
- `event.sessionKey` (for logging)
