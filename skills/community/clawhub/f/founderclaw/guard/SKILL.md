---
name: guard
description: >
  Full safety mode: destructive command warnings + directory-scoped edits.
  Combines careful (warns before destructive commands) with freeze (blocks
  edits outside a specified directory). Maximum safety for prod or live systems.
  Use when: "guard mode", "full safety", "lock it down", "maximum safety".
---

# Guard — Full Safety Mode

Combines the destructive command warnings from **careful** with the edit scoping from **freeze**.

## Activation

1. Ask or detect the scope directory for freeze
2. Activate careful rules (warn on destructive commands)
3. Activate freeze rules (restrict edits to scope directory)
4. Announce: "Guard mode active. Edits locked to `{dir}/`. Destructive commands will require confirmation."

## Rules

### From Careful
Before running any bash command, check for destructive patterns (rm -rf, force-push, DROP TABLE, etc.). If detected, warn and wait for confirmation.

### From Freeze
Before any Edit or Write, verify the target file is within the locked directory. If outside, refuse and remind.

## Deactivation

User says "unguard" or "guard off" → deactivate both careful and freeze. Confirm: "Guard mode off. Edits unrestricted, destructive commands run without warning."

See also: `careful` (destructive commands only), `freeze` (edit scoping only), `unfreeze` (remove edit restriction).
