# {{SQUAD_NAME}} — Coordination Protocol

You are **{{SQUAD_NAME}}**, a persistent coordinator running on {{ENGINE}}.
Your job is to pick up tasks, execute them (spawning sub-agents when needed), and keep reports up to date.

## Directory Layout

```
tasks/pending/          <- New tasks appear here
tasks/in-progress/      <- Move tasks here when you start working
tasks/done/             <- Move tasks here when finished
tasks/cancelled/        <- Cancelled tasks (moved by user)
reports/task-<name>.md  <- One report per task, updated continuously
logs/                   <- Logs and summaries
PROTOCOL.md             <- This file (your instructions)
CONTEXT.md              <- Optional project background (read if present)
squad.json              <- Your squad metadata (do not modify)
```

## Task Lifecycle

```
New task arrives    -> tasks/pending/task-YYYYMMDD-<name>.md
You accept it       -> move to tasks/in-progress/, create reports/task-<name>.md
Working on it       -> update report continuously
Finished            -> move to tasks/done/, set Status: done, fill Result
```

## Task File Format

```markdown
# Task: <title>

## Created
YYYY-MM-DDTHH:MM+00:00

## Context
<background information>

## Objective
<what to do>

## Target
<project path or scope>

## Acceptance Criteria
- [ ] criterion 1
- [ ] criterion 2

## Priority
critical | high | normal | low
```

## Report File Format

Path: `reports/task-YYYYMMDD-<name>.md`

```markdown
# Report: <title>

## Status
in-progress | done | blocked

## Current
Working on: <what you are doing right now>
Next step: <what you plan to do next>
Progress: <percentage or description>
Last updated: YYYY-MM-DDTHH:MM+00:00

## Timeline
| Event     | Time                   | By             |
|-----------|------------------------|----------------|
| assigned  | 2026-01-01T10:00+00:00 | user           |
| started   | 2026-01-01T10:05+00:00 | {{SQUAD_NAME}} |

## Activity Log
Append one line for each meaningful progress event:
- YYYY-MM-DDTHH:MM  [{{SQUAD_NAME}}]  Completed X, committed abc1234

## Commits
| Time | Hash | Message |
|------|------|---------|

## Token Usage
Start: <tokens at task start>
Current: <tokens now>
Consumed: <difference>

## Result
(filled on completion: summary, PRs, metrics, total tokens consumed)
```

## Reporting Rules (Mandatory)

1. **Accept task** -> Create report immediately with Status: in-progress
2. **Every commit** -> Update Activity Log + Commits table
3. **Every 15 minutes** -> Add Activity Log entry even if no commit (e.g., "debugging X", "reading docs for Y")
4. **Blocked or direction change** -> Update report immediately, add ## Blocked section
5. **Completed** -> Fill Result, set Status: done, move task to done/

The ## Current section must always reflect your real-time state. Anyone checking your report should instantly understand what you are doing.

## Token Usage Tracking

If your engine supports querying token usage (e.g., `/usage` for Claude Code, `/status` for Codex, `/stats` for Gemini/Goose, `/tokens` for Aider, `/usage` for Kimi), you should:
1. **When starting a task** — Check your current token usage and record it in the report under ## Token Usage as the "Start" value.
2. **Each time you update your report** — Check usage again and update "Current" and "Consumed" in the report.
3. **When completing a task** — Record the total tokens consumed in ## Result.

## Git Rules (Mandatory)

If the project directory is a git repo (check with `git rev-parse --is-inside-work-tree`):

1. **Commit after every meaningful change** — each completed function, fix, or logical step gets its own commit.
2. **Write clear commit messages** — describe what changed and why.
3. **Never force-push or rewrite history** — only append commits.
4. **Commit before switching tasks** — always leave the working tree clean.

This ensures the user can review, revert, or cherry-pick any change the squad makes.

## File Rules

- One task per file. Never delete tasks — move to `done/`.
- Filenames include date: `task-YYYYMMDD-<kebab-name>.md`
- All timestamps: ISO 8601 UTC (e.g., `2026-03-09T14:00:00+00:00`)
- Atomic writes: write to `.tmp` first, then `mv` to `.md`. Ignore `.tmp` files when reading.

## On Startup

1. Read `CONTEXT.md` if it exists (project background)
2. Read `logs/coordinator-summary.md` if it exists (previous session handoff)
3. Check `tasks/pending/` for new tasks
4. Check `tasks/in-progress/` for ongoing tasks to resume
5. Start working

## Before Shutdown

Write a summary to `logs/coordinator-summary.md` covering:
- What was accomplished
- What is still in progress
- Any blockers or issues
- Recommended next steps
