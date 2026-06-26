# EasyClaw Brain Migration Map

## Direct imports

Good candidates to import with minimal risk:
- `~/.easyclaw/workspace/MEMORY.md`
- `~/.easyclaw/workspace/memory/*`
- `~/.easyclaw/workspace/docs/context-management.md` (reference only)
- `~/.easyclaw/workspace/.memos/*` (archive/reference)

## Stage for review

Stage these into `imports/easyclaw/` before editing active files:
- `AGENTS.md`
- `SOUL.md`
- `CORE-PRINCIPLE.md`
- `HEARTBEAT.md`
- `USER.md`
- `IDENTITY.md`

## Rebuild manually in OpenClaw

These represent automation wiring rather than plain memory:
- `~/Library/LaunchAgents/com.easyclaw.*.plist`
- `~/.easyclaw/workspace/scripts/*.sh` and automation runners
- heartbeat-driven queues like `.evolution-tasks/`, `.killerapp-tasks/`, `.influencer-tasks/`

Preferred replacements:
- move standing instructions into `HEARTBEAT.md`
- move exact schedules into OpenClaw cron jobs
- keep helper scripts only if the workflow is still wanted

## Important legacy findings from this machine

Observed legacy workspace:
- `~/.easyclaw/workspace/AGENTS.md`
- `~/.easyclaw/workspace/SOUL.md`
- `~/.easyclaw/workspace/MEMORY.md`
- `~/.easyclaw/workspace/CORE-PRINCIPLE.md`
- `~/.easyclaw/workspace/HEARTBEAT.md`
- `~/.easyclaw/workspace/memory/`
- `~/.easyclaw/workspace/docs/context-management.md`

Observed legacy automations:
- context manager launch agent
- self-evolution schedule
- influencer daily + weekly schedules
- task-classifier schedules
- evolution memo schedule
