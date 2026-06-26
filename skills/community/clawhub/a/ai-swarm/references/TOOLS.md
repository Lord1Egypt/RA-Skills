# Swarm Lead — Tools Notes

## spawn-batch.sh Usage (Primary Tool)

```bash
# 1. Write task prompts to /tmp/
cat > /tmp/prompt-task1.md << 'PROMPT'
... detailed task description ...

When completely finished, run:
openclaw system event --text "Done: task-1 — brief summary" --mode now
PROMPT

# 2. Create tasks JSON
cat > /tmp/batch-tasks.json << 'JSON'
[
  {"id": "task-1", "description": "/tmp/prompt-task1.md", "agent": "claude", "model": "claude-sonnet-4-6"},
  {"id": "task-2", "description": "/tmp/prompt-task2.md", "agent": "codex", "model": "gpt-5.3-codex"}
]
JSON

# 3. Spawn batch (auto-endorses + auto-integration)
cd ~/workspace/swarm
bash spawn-batch.sh "/mnt/d/Startup projects/ProjectName" "batch-id" "Batch description" /tmp/batch-tasks.json
```

## Agent CLI Commands

| Agent | Non-Interactive Command |
|-------|------------------------|
| Claude | `claude --model X --dangerously-skip-permissions -p "prompt"` |
| Codex | `codex --model X --dangerously-bypass-approvals-and-sandbox "prompt"` |
| Gemini | `GEMINI_API_KEY=$KEY gemini --model X -p "prompt"` |

## Integration Conflict Resolution Patterns

| Conflict Type | Resolution |
|---------------|------------|
| i18n + UX changes | Keep UX styling, apply stringResource() extraction |
| DB migrations (Room) | Combine with sequential version numbers |
| Multiple feature branches | Merge in dependency order (smallest/independent first) |
| Build failures post-merge | Fix imports, remove duplicates, verify with build command |

## Agent Selection Guide

| Task Type | Agent | Model | Why |
|-----------|-------|-------|-----|
| Complex architecture | Claude | Opus | Best reasoning |
| Standard features | Codex | gpt-5.3-codex | Fast, parallel-friendly |
| Code review | Gemini | 2.5 Pro | Good at spotting issues |
| Quick fixes/UI tweaks | Claude | Sonnet | Speed + reliability |
| Integration/merge | Claude | Opus or Sonnet | Needs full context |
| Research/analysis | Claude | Opus | Deep thinking |

When Codex/Gemini are quota-blocked, fall back to Claude for all roles.

## Monitoring Commands

```bash
# Quick status of all agents
tmux ls

# Check specific agent
tmux capture-pane -t <session> -p | tail -20

# Check worktree progress
cd <worktree> && git log --oneline origin/main..HEAD

# Check for conflicts
git diff --name-only --diff-filter=U

# Check integration watcher
tail -20 ~/workspace/swarm/logs/integration-*.log
```
