---
name: remem-flush
description: "Memory flush hook for /remem command. Triggers 6-step memory flush when user sends /remem in any chat."
events:
  - message:received
requires:
  config:
    - workspace.dir
install:
  - id: remem-flush-hook
    kind: local
    label: "Memory Flush Hook"
---

# remem-flush Hook

Intercept `/remem` messages and trigger a 6-step memory flush.

## Events

- `message:received` — listens for `/remem` command

## Behavior

1. Intercept messages matching `/remem` or `/remem <args>`
2. Extract session context
3. Detect active memory groups
4. Compare with old memory for deltas
5. Update memory files
6. Stamp flush-state timestamp
7. Return control to AI for confirmation reply

## Files Modified

- `memory/flush-state.json` — updated on each flush
- `memory/groups/{group}/*.md` — updated based on deltas
