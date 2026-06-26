# Manual Run Guide

Use this reference when the user explicitly wants to run a consolidation now.

## Trigger examples

- `dream now`
- `整理记忆`
- `跑 dream`
- `做一次记忆整理`
- `跑一次适配版 auto dream`

## Default meaning

These triggers mean:
- enter the adapted Auto Dream flow directly
- perform conservative incremental consolidation
- update target files when appropriate
- return a concise summary after completion

If the user says `dream details`, do not run consolidation; show recent dream-log history instead.

## Fixed execution order

To reduce errors, follow this order:

1. identify candidate logs
2. extract and route candidate memory
3. write core target files
4. write dream-log
5. write a short daily-note summary if needed
6. commit only if files changed

## Skip behavior

If there is nothing worth consolidating:
- do not force updates
- do not fake output
- do record the skip in dream-log
- do return a clear skip summary to the user
