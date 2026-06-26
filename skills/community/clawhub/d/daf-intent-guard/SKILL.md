---
name: daf-intent-guard
description: Tracks intent drift across multi-turn tasks. Before executing any multi-step task, call this to detect if the user's new instruction is a small patch, requires replanning from a checkpoint, or should abort the current task entirely. Returns patch/replan/abort decision with semantic distance and anchor rollback count.
metadata: {"openclaw":{"emoji":"🎯","requires":{"bins":["python3"]}}}
---

## DAF Intent Guard

Use this skill when:
- A user modifies an in-progress task
- A user gives a new instruction that might conflict with what is already done
- You need to decide whether to continue, roll back, or restart

### How to use

Call the guard before executing any new instruction on an ongoing task:
```bash
python3 {baseDir}/daf_guard.py \
  --current-anchor <index> \
  --old-constraints '<json>' \
  --new-constraints '<json>' \
  --new-action '<action>' \
  --requires '<json_array>' \
  --anchors '<json>'
```

### Decision meanings
- **patch**: Small change. Update parameters and continue from current anchor.
- **replan**: Significant change. Roll back to anchor `first_affected_anchor` and re-execute from there.
- **abort**: Task cancelled or too much has changed. Stop and confirm with user before restarting.

### Example
User was booking a flight (seat locked at anchor 1), now says "change destination to New York":
- old-constraints: {"destination":"KL","date":"today","cabin":"economy"}
- new-constraints: {"destination":"New York","date":"today","cabin":"economy"}
- Expected: replan (destination change affects anchor 0)
