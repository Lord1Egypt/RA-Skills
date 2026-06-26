# Tools Reference — Command Cheatsheet

Run commands from the runtime directory unless shown otherwise:

```bash
cd ~/workspace/swarm
```

## Pre-flight checks

```bash
# Optional: live provider probes; consumes provider quota
bash assess-models.sh --dry-run

# Current role assignments
python3 -c "import json; d=json.load(open('duty-table.json')); [print(f'  {r}: {e.get(\"agent\")}/{e.get(\"model\")}') for r,e in d.get('dutyTable',{}).items()]"

# Runtime basics
tmux -V
tmux ls 2>/dev/null || echo "No active agents"
cat pending-notifications.txt
```

## spawn-agent.sh

```text
Usage: spawn-agent.sh <project-dir> <task-id> <description> [role-or-agent] [model] [reasoning]

project-dir:    absolute path to project root
task-id:        unique identifier; branch feat/<task-id>, session <agent>-<task-id>
description:    prompt text or path to a .md prompt file
role-or-agent:  architect | builder | reviewer | integrator | codex | gemini | deepseek | claude
model:          optional model override
reasoning:      low | medium | high (default: high)
```

Examples:

```bash
# Role-based, recommended
bash endorse-task.sh fix-bug
bash spawn-agent.sh /path/to/project fix-bug "Fix auth null pointer" builder

# Long prompt file
bash endorse-task.sh design-api
bash spawn-agent.sh /path/to/project design-api /tmp/prompt.md architect

# Direct model override, only when deliberate
bash endorse-task.sh special-task
bash spawn-agent.sh /path/to/project special-task "Fix it" codex gpt-5.5 high
```

## spawn-batch.sh

```text
Usage: spawn-batch.sh <project-dir> <batch-id> <batch-description> <tasks-json>
```

`tasks.json`:

```json
[
  {"id":"task-1", "description":"...", "role":"builder", "reasoning":"high"},
  {"id":"task-2", "description":"/tmp/prompt-task2.md", "role":"architect"},
  {"id":"task-3", "description":"...", "agent":"codex", "model":"gpt-5.5"}
]
```

Fields:

- `id` required
- `description` required; prompt text or path to `.md`
- `role` recommended; duty table resolves agent/model
- `agent` + `model` optional direct override
- `reasoning` optional: low/medium/high

## assess-models.sh

```bash
bash assess-models.sh --dry-run    # probe without updating duty table
bash assess-models.sh              # update duty-table.json
```

## model-fallback.sh

```bash
bash model-fallback.sh <role> <failed-agent> <failed-model>
```

Output:

```text
agent|model|nonInteractiveCmd
```

Example:

```bash
bash model-fallback.sh builder deepseek deepseek-v4-pro-max
# → codex|gpt-5.5|codex exec --model gpt-5.5 --full-auto
```

## Monitoring

```bash
tmux ls
cat pending-notifications.txt
bash pulse-check.sh
bash check-agents.sh
bash daily-standup.sh
python3 -m json.tool duty-table.json
tail -20 logs/<session>.log
```

## Cleanup

```bash
bash cleanup.sh
```

## Configuration: swarm.conf

```bash
SWARM_NOTIFY_TARGET=""          # Optional notification recipient
SWARM_NOTIFY_CHANNEL="telegram" # Optional channel
SWARM_MAX_CONCURRENT=8          # Max parallel agents
# DEEPSEEK_API_KEY=""           # Optional; prefer host auth where possible
```
