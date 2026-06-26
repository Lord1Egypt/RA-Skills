# Swarm Workflow — 3-Phase Build Pipeline

## Phase 1: PLAN (Architect Role)

The orchestrator (you) acts as architect:

1. **Read context**: project ESR, recent git log, open issues, codebase structure
2. **Break work into tasks**: each task = 1 agent, 1 branch, 1 worktree
3. **Assign roles**: use `role` field — duty table resolves the actual agent/model
4. **Present plan table** to human:

```
| # | Task ID | Description | Role | Priority |
|---|---------|-------------|------|----------|
| 1 | fix-auth | Fix login redirect | builder | high |
| 2 | add-search | Implement search | builder | high |
| 3 | ui-polish | Mobile responsiveness | builder | medium |
```

5. **HOLD** — Do NOT spawn until human says "go" / "approved" / "endorsed"

### Endorsement
After approval, endorsement files are created:
```bash
endorse-task.sh <task-id>        # Single
# spawn-batch.sh auto-endorses each task in the batch
```

## Phase 2: BUILD + REVIEW (Builder + Reviewer Roles)

### Spawning

**Single agent:**
```bash
spawn-agent.sh <project-dir> <task-id> <prompt-or-file> <role> [model] [reasoning]
# Examples:
spawn-agent.sh /path/to/project fix-auth "Fix the login redirect bug" builder
spawn-agent.sh /path/to/project add-search /tmp/prompt-search.md architect
```

**Batch (parallel):**
```bash
spawn-batch.sh <project-dir> <batch-id> <description> <tasks.json>
```

tasks.json format (role-based):
```json
[
  {"id": "fix-auth", "description": "Fix login redirect", "role": "builder", "reasoning": "high"},
  {"id": "add-search", "description": "Implement search page", "role": "builder"},
  {"id": "ui-polish", "description": "Mobile responsive fixes", "role": "builder", "reasoning": "medium"}
]
```

Direct agent override (bypasses duty table; use only deliberately):
```json
{"id": "special-task", "description": "...", "agent": "codex", "model": "gpt-5.5"}
```

### What Happens After Spawn

1. `spawn-agent.sh` creates git worktree + branch `feat/<task-id>`
2. Agent runs in tmux session `<agent>-<task-id>`
3. Agent maintains work log at `/tmp/worklog-<session>.md`
4. `notify-on-complete.sh` watches the tmux session:
   - Builder finishes → auto-spawns **reviewer** (from duty table)
   - Reviewer reviews code, fixes issues, updates work log
   - Up to 3 review loops if issues persist
   - Token limit mid-run → runner auto-switches model

### Monitoring
```bash
tmux ls                              # Active sessions
cat ~/workspace/swarm/pending-notifications.txt  # Alerts
bash pulse-check.sh                  # Stuck agent detection
bash check-agents.sh                 # Status of all agents
```

## Phase 3: SHIP (Integrator Role)

### Automatic (via spawn-batch.sh)
`integration-watcher.sh` starts automatically after all agents complete:
1. Merges branches sequentially into main
2. Resolves conflicts (or escalates)
3. Runs build verification
4. Persists work logs to `<project>/docs/history/`
5. Updates ESR
6. Notifies human with shipped summary

### Manual Integration
```bash
start-integration.sh <project-dir> <session1> <session2> ...
```

## Quality Gates

| Gate | Enforced By |
|------|-------------|
| Human endorsement | `endorse-task.sh` (30s cooldown) |
| Max concurrent agents | `swarm.conf` → `SWARM_MAX_CONCURRENT` |
| Review loops (max 3) | `notify-on-complete.sh` |
| Stuck agent detection | `pulse-check.sh` (no output 30+ min) |
| Token limit failover | Runner + `model-fallback.sh` |
| Build verification | Integration watcher |
| CI/CD check | `deploy-notify.sh` |

## Key Rules

1. **Never spawn without endorsement** — the 30s cooldown prevents mistakes
2. **Always use roles, not hardcoded agents** — let the duty table decide
3. **Start integration-watcher in the same step as batch spawn** — it waits for completion
4. **Work logs are mandatory** — they're the handoff mechanism between phases
5. **ESR must be updated** — every session's results get logged
