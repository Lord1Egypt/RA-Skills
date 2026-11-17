---
name: cycle-preflight-check
description: Pre-flight checks for evolver cycles to detect likely empty cycles, duplicate genes, and tool bypass patterns before running. Use when you want to reduce empty evolution cycles or audit tool usage before solidifying.
---

# Cycle Preflight Check

Run before `evolver run` to catch likely no-op cycles.

```bash
node skills/cycle-preflight-check/index.js
```

## Checks

- Duplicate recent intent+gene within last 8 cycles
- High exec/shell ratio vs registered tools in recent transcripts
- Uncommitted changes that could trigger hollow commit
- Missing validation scripts

## Output

- `PASS` / `WARN` / `FAIL`
- One-line actionable hint
