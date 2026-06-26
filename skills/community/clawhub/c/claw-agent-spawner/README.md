# agent-spawner

Multi-agent orchestration skill. Decompose complex tasks into parallel subtasks and spawn sub-agents to execute them simultaneously.

## Features

- **Task decomposition** — automatic breakdown of complex tasks into subtasks
- **Spawn patterns** — 6 proven patterns for different task types
- **Model selection** — guidelines for choosing the right model per subtask
- **Planner script** — CLI tool to generate spawn plans from task descriptions

## Quick Start

```bash
# Generate a spawn plan
python3 scripts/spawn_planner.py "Research the top 5 AI coding assistants in 2026"

# Then spawn agents using:
sessions_spawn task="<subtask description>" label="sub-1" mode="run" runtime="subagent"
```

## Files

- `SKILL.md` — Full documentation
- `references/spawn-patterns.md` — 6 spawn patterns with examples
- `references/model-selection.md` — Model choice guide
- `scripts/spawn_planner.py` — Task decomposition tool

## Pricing

- Service: €25-75 (multi-agent task execution)
- Skill: €5-15 (ClawHub)
