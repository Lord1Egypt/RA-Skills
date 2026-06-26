---
name: memory-boost
description: Persistent task memory and keep-alive loop for OpenClaw agents. Every task gets durable notes. Arm the loop for long tasks, disarm when done. No external dependencies.
version: 1.0.0
emoji: "\u26A1"
homepage: https://github.com/TechieTer/openclaw-memory-boost
metadata:
  openclaw:
    os: [macos, linux]
---

# Memory Boost

Two things in one skill:

1. **Task Memory** — every task automatically gets persistent notes so work survives restarts
2. **Keep-Alive Loop** — arm it for long tasks, disarm when done

No external dependencies. Everything lives inside `~/.openclaw/memory/`.

## Task Memory

When you receive any task, automatically create a task folder:

```
~/.openclaw/memory/tasks/<task-name>/
  RESUME.md      — status, heartbeat, next action, key files, restart note
  CHECKLIST.md   — step-by-step progress
  DOCS.md        — goal, decisions, gotchas, notes for next session
```

### RESUME.md must contain:
- Task name and one-line description
- Current status (active / stalled / complete)
- Last heartbeat (date and time, updated whenever you touch the task)
- Next action (one concrete step)
- Key files (relevant paths)
- Restart note (what a fresh session needs to pick this up)

### CHECKLIST.md must contain:
- Numbered or checkbox steps
- Current status of each step
- A final verification step

### DOCS.md must contain:
- Goal
- Important decisions and why
- File paths that matter
- Gotchas and failure modes
- Notes for the next session

### Update rules:
- Create notes before starting a multi-step task.
- Update RESUME.md before and after major milestones.
- Mark checklist items complete as soon as they are done.
- Add discoveries and gotchas to DOCS.md immediately.
- Always update the heartbeat when touching an active task.
- A heartbeat older than 24 hours or a missing next action means the task is stale.

### Storage path:
Task notes live in `~/.openclaw/memory/tasks/`. The canonical template is at `{baseDir}/templates/TEMPLATE.md`.

## Keep-Alive Loop

For long-running tasks, the keep-alive loop prevents silent failures.

### Controls

- **`/loop-start`** — arms the loop. Monitoring jobs begin running.
- **`/loop-stop`** — disarms the loop. Jobs no-op. No wasted tokens.

The loop state lives in `~/.openclaw/memory/LOOP-STATE.md`.

### Monitoring layers

When armed, three jobs watch your agent's work:

| Layer | Job name | Schedule | What it does |
|-------|----------|----------|--------------|
| Watchdog | `boost-watchdog` | */15 * * * * | Detects stalls, writes WATCHDOG.md |
| Replayer | `boost-replayer` | */30 * * * * | Takes one concrete step on a stalled task |
| Escalator | `boost-escalator` | 0 * * * * | Forces fresh-session handoff on repeated stalls |

### Integrity layers

These run always, regardless of loop state:

| Layer | Job name | Schedule | What it does |
|-------|----------|----------|--------------|
| Validator | `boost-validator` | 5 * * * * | Repairs missing notes, refreshes task index |
| Smoke test | `boost-smoke-test` | 0 */6 * * * | Verifies the skill itself is healthy |

### Watchdog rules:
- Write WATCHDOG.md only when you can prove a stall. Do not manufacture problems.
- Include: folder path, blocker, why-stalled tag, one next action.
- Why-stalled tags: `blocked-on-external`, `ambiguous-next-step`, `repeated-promise`, `missing-context`

### Replayer rules:
- Take only one mechanical step per pass. No speculative fixes.
- If the step is ambiguous, update WATCHDOG.md with a clearer next action and stop.

### Escalator rules:
- Escalate only after the same stall repeats or a replayer pass fails to advance.
- Add an ESCALATE section to WATCHDOG.md with what was tried and the strongest next action.

### Validator rules:
- Inspect task folders for missing RESUME.md, CHECKLIST.md, or DOCS.md.
- Backfill missing notes from the canonical template at `{baseDir}/templates/TEMPLATE.md`. Do not invent formats.
- Refresh the task index so it lists all tasks with status and next action.
- Treat a task as stale if heartbeat > 24h or next action is missing.

### Smoke test checks:
- Core files exist (TEMPLATE.md, TASK-INDEX.md, LOOP-STATE.md)
- All 5 scheduled jobs exist and are enabled
- At least one active task has a heartbeat and next action
- Loop state is valid (armed or disarmed)

## File layout

```
~/.openclaw/memory/
  TEMPLATE.md          # canonical template for new task folders
  TASK-INDEX.md        # quick-scan index of all tasks
  LOOP-STATE.md        # armed/disarmed state marker
  tasks/
    <task-name>/
      RESUME.md
      CHECKLIST.md
      DOCS.md
      WATCHDOG.md      # created by watchdog when stall detected
```

## When to use

- **Task memory**: Always. Every task should get notes automatically.
- **Keep-alive loop**: For long tasks. `/loop-start` before the task, `/loop-stop` when done.
- **Quick tasks**: Just let the task memory handle it. No need to arm the loop.
