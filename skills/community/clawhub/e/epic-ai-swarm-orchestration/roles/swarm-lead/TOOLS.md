# Swarm Lead — Tools Notes

## Pre-flight before spawning agents

Before any agent work:

1. Did I present a plan and get human/operator endorsement? If no, stop and present the plan.
2. Am I using `spawn-agent.sh` for one task or `spawn-batch.sh` for 2+ tasks? If no, stop.
3. Are scripts installed at `~/workspace/swarm/` and passing `doctor.sh`?
4. Will notifications be captured via `pending-notifications.txt` / configured OpenClaw delivery?

**The scripts are the swarm. Bypassing them means bypassing endorsement, tmux, watchers, pulse checks, review loops, and integration.**

## spawn-batch.sh usage

```bash
# 1. Write prompts to temp files if descriptions are long
cat > /tmp/prompt-task1.md << 'EOF'
Detailed task instructions here.
EOF

# 2. Create task JSON. Prefer roles; duty-table chooses model/vendor.
cat > /tmp/batch-tasks.json << 'EOF'
[
  {"id":"task-1", "description":"/tmp/prompt-task1.md", "role":"builder", "reasoning":"high"},
  {"id":"task-2", "description":"Implement related improvement", "role":"builder"}
]
EOF

# 3. Spawn batch
cd ~/workspace/swarm
bash spawn-batch.sh "/absolute/path/to/project" "batch-id" "Batch description" /tmp/batch-tasks.json
```

## spawn-agent.sh usage

```bash
cd ~/workspace/swarm
bash endorse-task.sh task-id
# Wait for single-task cooldown unless using batch mode.
bash spawn-agent.sh "/absolute/path/to/project" "task-id" "/tmp/prompt-task.md" builder
```

## Plan format

Always include:

- Task ID
- Description
- Priority: 🔴/🟡/🟢
- Estimated time
- Role: architect/builder/reviewer/integrator
- Dependencies and integration notes

## Prompt rules

Do **not** include OpenClaw notification commands in agent prompts. Watchers handle notifications. Duplicating notification instructions creates noisy/double alerts.

`spawn-agent.sh` appends work-log instructions automatically; only add task-specific details.

## Integration conflict resolution

When integration hits conflicts:

- Keep the most complete implementation.
- Preserve tests and add regression coverage where possible.
- For frontend/i18n conflicts, keep UX fixes and string extraction.
- For DB migrations, combine sequentially and preserve rollback/forward safety.
- Verify with the project’s smallest meaningful gate: tests, build, lint, CI, or direct inspection.

## Model selection

Prefer duty-table roles over hardcoded agents. Use direct `agent`/`model` only for explicit debugging or when the operator requests a specific vendor/model.

Useful checks:

```bash
cd ~/workspace/swarm
bash doctor.sh --target ~/workspace/swarm          # if doctor.sh is available from skill package
python3 -m json.tool duty-table.json
bash assess-models.sh --dry-run                   # uses provider quota; run deliberately
bash pulse-check.sh
tmux ls
```
