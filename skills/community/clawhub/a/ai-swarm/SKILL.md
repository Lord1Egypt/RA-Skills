---
name: ai-swarm
description: Multi-agent AI coding swarm orchestration. Plan parallel tasks, spawn Claude/Codex/Gemini agents in tmux sessions with git worktrees, auto-review, auto-integrate branches, notify via Telegram. Use when you need to break a project into parallel coding tasks and orchestrate multiple AI agents to build, review, and merge them.
---

# AI Swarm Orchestration

Orchestrate parallel AI coding agents with automated review, integration, and notifications.

## Setup

### Prerequisites
- `tmux` — agent sessions run here
- `git` — worktrees for parallel branches
- `claude` CLI (Claude Code) — primary agent
- Telegram bot token + chat ID (optional, for notifications)

### Install scripts
Copy `scripts/` to your swarm directory (e.g., `~/workspace/swarm/`). Make executable:
```bash
chmod +x ~/workspace/swarm/*.sh
```

### Initialize state files
```bash
mkdir -p ~/workspace/swarm/{logs,endorsements}
echo '[]' > ~/workspace/swarm/active-tasks.json
echo '' > ~/workspace/swarm/pending-notifications.txt
```

### Duty table
Copy `references/duty-table-template.json` to `~/workspace/swarm/duty-table.json`. Configure model assignments.

## Core Workflow

### Phase 1: PLAN (present to human, STOP, wait for approval)

⛔ **CRITICAL GATE**: Present the plan table to the human. Then **STOP**. Do NOT write prompts or spawn agents until the human explicitly approves.

The plan message and the spawn action **must be in DIFFERENT turns**. Never combine them.

```
🐝 Swarm Plan: [batch description]

| # | Task ID | Description | Agent | Model |
|---|---------|-------------|-------|-------|
| 1 | fix-xyz | Fix the freeze bug | claude | sonnet |
| 2 | add-feat | Add feature X | claude | sonnet |

Dependencies: None (all parallel)
Estimated time: ~15-20 min

Proceed? 👍/👎
```

**Wait for human reply.** Only after "yes"/"go"/👍 → proceed to Phase 2.

### Phase 2: BUILD (write prompts, spawn agents)

Write task prompts to `/tmp/prompt-<task-id>.md`, create batch JSON, then spawn:

```bash
cat > /tmp/batch-tasks.json << 'EOF'
[
  {"id": "task-1", "description": "/tmp/prompt-task1.md", "agent": "claude", "model": "claude-sonnet-4-6"},
  {"id": "task-2", "description": "/tmp/prompt-task2.md", "agent": "claude", "model": "claude-sonnet-4-6"}
]
EOF

cd ~/workspace/swarm
bash spawn-batch.sh "/path/to/project" "batch-id" "Batch description" /tmp/batch-tasks.json
```

`spawn-batch.sh` handles everything automatically:
- Creates git worktrees + feature branches
- Launches agents in tmux sessions
- Starts per-agent completion watchers (auto-review + Telegram notification)
- Starts integration watcher (auto-merge when all done)

For single tasks: `bash spawn-agent.sh "/path/to/project" "task-id" "/tmp/prompt.md" "claude" "claude-sonnet-4-6"`

### Phase 3: SHIP (automatic)

The scripts handle this automatically:
1. `notify-on-complete.sh` detects each agent finishing → spawns reviewer → sends Telegram
2. `integration-watcher.sh` detects ALL agents done → spawns Opus integration agent → merges branches → resolves conflicts → verifies builds → sends Telegram

## Prompt Template

Write clear, self-contained prompts for each agent. Include:
- Project path and stack
- Specific files to modify
- What to do (detailed steps)
- Verification commands (`tsc --noEmit`, `npm run build`, etc.)

**Do NOT** include `openclaw system event` in prompts — `notify-on-complete.sh` handles notifications automatically.

## Monitoring

```bash
tmux ls                              # List active agent sessions
bash check-agents.sh                 # Health check all agents
bash pulse-check.sh                  # Detect stuck agents (auto-kills)
cat pending-notifications.txt        # Check pending notifications
```

## Script Reference

| Script | Purpose |
|--------|---------|
| `spawn-batch.sh` | Spawn N agents + auto-integration watcher |
| `spawn-agent.sh` | Spawn single agent with completion watcher |
| `integration-watcher.sh` | Poll agents, auto-merge when all done |
| `start-integration.sh` | Manual integration watcher start |
| `notify-on-complete.sh` | Per-agent watcher: detect done → review → notify |
| `pulse-check.sh` | Detect and kill stuck agents |
| `check-agents.sh` | Quick status check |
| `endorse-task.sh` | Create endorsement file for a task |
| `esr-log.sh` | Update project ESR docs |
| `eor-log.sh` | Write agent end-of-run log |
| `fallback-swap.sh` | Model selection with fallback |
| `assess-models.sh` | Weekly model benchmark |
| `deploy-notify.sh` | CI/CD notification |

## Hard Rules

### ALWAYS
- Present plan → **STOP** → wait for human approval → THEN spawn (separate turns!)
- Use `spawn-batch.sh` for 2+ tasks, `spawn-agent.sh` for single tasks
- Let scripts handle tmux, notifications, review, integration — don't bypass

### NEVER
- Spawn agents without human endorsement
- Present plan and spawn in the same message/turn
- Write prompts before receiving endorsement
- Use bare `claude --print` or background exec (bypasses entire pipeline)
- Spawn agents in the orchestrator's workspace directory

## Heartbeat Checks

Read `references/HEARTBEAT.md` for periodic checks:
1. Read `pending-notifications.txt` → send to human → clear
2. Run `pulse-check.sh` for stuck agents
3. Check `tmux ls` for completed agents
4. Report brief status if agents are running

## Further Reading

- `references/ROLE.md` — Full role definition with lessons learned
- `references/TOOLS.md` — Detailed script usage and prompt patterns
