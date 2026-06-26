---
name: easyclaw-brain-migration
description: Migrate EasyClaw workspace-level behavior into a new OpenClaw workspace by locating and comparing old EasyClaw brain files such as AGENTS.md, SOUL.md, MEMORY.md, HEARTBEAT.md, memory/, launchd/context-management docs, then staging or importing them with backups. Use when a user wants to copy EasyClaw principles, memories, heartbeat logic, context-management setup, or other non-JSON core system behavior into the current OpenClaw workspace.
---

# EasyClaw Brain Migration

Use this skill for the files that define the assistant's operating style and continuity, not just runtime config.

## Source locations to check

Primary legacy workspace:
- `~/.easyclaw/workspace/`

Important source files:
- `AGENTS.md`
- `SOUL.md`
- `CORE-PRINCIPLE.md`
- `MEMORY.md`
- `USER.md`
- `HEARTBEAT.md`
- `memory/`
- `docs/context-management.md`
- `scripts/load_context.sh`
- launchd files under `~/Library/LaunchAgents/com.easyclaw.*.plist`

Target workspace:
- current OpenClaw workspace root

## Migration policy

### Copy directly

These usually copy well when missing in the target workspace:
- `MEMORY.md`
- `memory/` contents
- context snapshots / historical notes that are purely informational

### Merge carefully

These should be reviewed or staged before replacing active files:
- `AGENTS.md`
- `SOUL.md`
- `HEARTBEAT.md`
- `USER.md`

Why: the new workspace may already contain OpenClaw-native conventions that should not be blown away.

### Rebuild, don't blindly copy

These are automation mechanisms, not just text:
- launchd plists
- helper scripts invoked by launchd
- old context-management wrappers

Translate them into current OpenClaw mechanisms such as:
- `HEARTBEAT.md`
- cron jobs
- workspace scripts
- updated notes in `AGENTS.md` / `TOOLS.md`

## Workflow

### 1. Generate a migration report

Run:

```bash
python3 scripts/report_easyclaw_brain.py
```

This reports:
- what source files exist
- what target files exist
- which files are safe to import directly
- which should be staged for review
- legacy automations that need rebuilding

### 2. Stage legacy brain files safely

Run:

```bash
python3 scripts/stage_easyclaw_brain.py
```

This copies legacy brain files into `imports/easyclaw/` inside the current workspace without overwriting active files.

Use staging first when you want a safe reviewable landing zone.

### 3. Import memory into active workspace

Run:

```bash
python3 scripts/stage_easyclaw_brain.py --import-memory
```

This:
- backs up current target files if needed
- copies `MEMORY.md` if missing
- copies legacy `memory/` files that do not already exist
- leaves active `AGENTS.md`, `SOUL.md`, and `HEARTBEAT.md` untouched

### 4. Merge principles manually or with explicit review

After staging, read the staged files and selectively merge:
- stable operating rules from `AGENTS.md`
- persona/principles from `SOUL.md` and `CORE-PRINCIPLE.md`
- heartbeat tasks that still make sense
- context-management notes from `docs/context-management.md`

Do not auto-enable old schedules unless the user wants them restored.

## Notes

- Treat old memory and prompts as sensitive workspace data.
- Prefer additive migration over destructive replacement.
- For heartbeat and scheduling logic, surface what existed and ask whether to rebuild it as cron/heartbeat behavior.
