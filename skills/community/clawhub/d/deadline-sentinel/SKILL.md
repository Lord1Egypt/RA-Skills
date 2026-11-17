---
name: deadline-sentinel
description: Track tasks and deadlines, update completion status, and identify approaching or overdue work using a local persistent task store.
metadata: {"openclaw":{"requires":{"bins":["node"]}}}
---

# Deadline Sentinel

Use Node.js 24.16 or later. This skill has no network or model dependency. Follow the host workspace's data-handling rules.

Run the bundled script, replacing `{baseDir}` with this skill's installed directory when necessary:

```bash
node "{baseDir}/scripts/deadlines.mjs" list
node "{baseDir}/scripts/deadlines.mjs" add ID "TITLE" "2026-11-10T17:00:00-08:00" high "PROJECT"
node "{baseDir}/scripts/deadlines.mjs" alerts
node "{baseDir}/scripts/deadlines.mjs" status ID done
```

Priorities: low, medium, high. Statuses: todo, in-progress, blocked, done. Clarify missing dates, times and timezone information before recording a task. Use timestamps with an explicit offset or Z. Confirm success only after the command succeeds.

The default store is local to the host account. `DEADLINE_SENTINEL_STATE_FILE` can select a different local file; do not put its SQLite lock file on Cloud Storage FUSE. Back it up using the host's persistence mechanism. Data is outside the installed skill, so package upgrades preserve it.

`alerts` returns incomplete tasks due within 72 hours, ordered by due time, labeled overdue, urgent (within 24 hours), or soon. It returns candidates and does not schedule a message. Use a host scheduler for proactive delivery; report delivery only after obtaining a real receipt. Do not send messages, invent deadlines, or claim that an exact-time reminder was scheduled merely because a task was added.
