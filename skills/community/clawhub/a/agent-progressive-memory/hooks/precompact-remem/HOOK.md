---
name: precompact-remem
description: "Before session context compaction, trigger a memory flush to preserve current session memory."
events:
  - session:compact:before
requires:
  config:
    - workspace.dir
install:
  - id: precompact-remem-hook
    kind: local
    label: "Pre-Compaction Memory Flush"
---

# precompact-remem Hook

Intercepts `session:compact:before` event and runs a 6-step memory flush
to preserve the current session's context before it gets summarized away.

## Behavior

1. Detect session context (message count, token count)
2. Discover active memory groups
3. Read old memory timestamps from flush-state
4. Compute deltas (changed files since last flush)
5. Update memory files with session context
6. Stamp flush-state timestamp

## Events

- `session:compact:before` — fires just before OpenClaw compacts the transcript

## Notes

- This hook complements `remem-flush` which responds to `/remem` commands.
- `precompact-remem` handles the automatic case: session is being compacted,
  flush now so no context is lost.
- Both hooks share the same flush logic and flush-state file.
