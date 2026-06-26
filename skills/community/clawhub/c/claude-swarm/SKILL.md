---
name: claude-swarm
description: Claude-native multi-agent swarm orchestration for parallel coding. Use when spawning multiple Claude Code agents to work in parallel on a project with git worktrees, tmux tracking, endorsement gates, auto-review chains, integration merging, and webhook notifications. All agents are Claude (opus for architect/integrator, sonnet for builders/reviewers). Triggers on parallel coding, multi-agent work, swarm orchestration, batch spawning, or when 2+ coding tasks need coordinated execution.
---

# Claude Swarm — Multi-Agent Orchestration

Parallel Claude Code agents: plan → endorse → spawn → monitor → review → integrate → ship.

## Quick Start

```bash
# 1. Write task prompts
cat > /tmp/prompt-task1.md << 'EOF'
Implement feature X...
EOF

# 2. Create tasks JSON
cat > /tmp/tasks.json << 'EOF'
[
  {"id": "feat-x", "description": "/tmp/prompt-task1.md", "role": "builder"},
  {"id": "feat-y", "description": "/tmp/prompt-task2.md", "role": "builder"}
]
EOF

# 3. Spawn batch (auto-endorses + auto-integration)
bash scripts/spawn-batch.sh "/path/to/project" "batch-1" "Description" /tmp/tasks.json
```

## Roles & Models

| Role | Model | Effort | Use |
|------|-------|--------|-----|
| architect | opus | high | Design, planning, complex decisions |
| builder | sonnet | high | Feature implementation (parallel) |
| reviewer | sonnet | medium | Auto-review on completion |
| integrator | opus | high | Cross-branch merge + conflict resolution |

Configure in `config/duty-table.json`.

## Scripts

| Script | Purpose |
|--------|---------|
| `spawn-batch.sh` | Spawn N parallel agents + integration watcher |
| `spawn-agent.sh` | Spawn single agent in worktree + tmux |
| `endorse-task.sh` | Endorse task (required before spawn) |
| `check-agents.sh` | Show status of all running agents |
| `cleanup.sh` | Remove worktrees, branches, tmux sessions |
| `notify.sh` | Send webhook/Telegram notification |
| `notify-on-complete.sh` | Auto-watcher: notify + review on completion |
| `integration-watcher.sh` | Auto: merge all branches when batch completes |

## Workflow Detail

### 1. Planning (human + architect)
Break work into parallel tasks. Each task needs: ID, prompt, role.

### 2. Endorsement Gate
Every task requires endorsement before spawning — safety gate to prevent runaway agents.
- `spawn-batch.sh` auto-endorses all tasks in batch
- Manual: `bash scripts/endorse-task.sh <task-id>`
- 30-second cooldown between endorsement and spawn

### 3. Spawning
Each agent runs in:
- **Isolated git worktree** (`<project>-worktrees/<task-id>/`)
- **tmux session** (`claude-<task-id>`)
- **Non-interactive mode** (`claude --print --permission-mode bypassPermissions`)
- **Auto-retry** with model fallback (opus → sonnet → haiku) on rate limits

### 4. Auto-Review
When an agent completes, `notify-on-complete.sh`:
1. Detects completion (polls tmux every 60s)
2. Sends notification
3. Spawns a reviewer (sonnet) that checks the diff
4. If issues found: fixes and commits (up to 3 rounds)
5. Pushes final state

### 5. Integration
When all agents in a batch complete, `integration-watcher.sh`:
1. Collects all branches
2. Merges sequentially into main
3. Uses opus to resolve any conflicts
4. Runs integration review (opus, up to 3 rounds)
5. Pushes to main (if auto-merge enabled)

## Setup

1. Copy this skill's `scripts/` and `config/` to your workspace
2. Copy `config/swarm.conf.example` → `config/swarm.conf` and configure
3. Ensure installed: `bash 4+`, `tmux`, `git`, `gh`, `jq`, `claude` (Claude Code CLI)

### Notifications
Set `SWARM_NOTIFY` in `swarm.conf`:
- `webhook` — POST to `SWARM_WEBHOOK_URL` (Slack/Discord/custom)
- `telegram` — Send via `SWARM_TELEGRAM_BOT_TOKEN` + `SWARM_TELEGRAM_CHAT_ID`
- `none` — Log only (default)

## Hard Rules

1. **Always endorse before spawning** — no exceptions
2. **Use spawn-batch.sh for 2+ tasks** — starts integration watcher
3. **Never run bare `claude --print` in background** — use spawn-agent.sh
4. **Let the watcher handle reviews** — don't add review logic to prompts
