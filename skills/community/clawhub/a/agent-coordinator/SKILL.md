---
name: agent-coordinator
description: Multi-agent coordination protocol — task distribution, result aggregation, and parallel execution across multiple AI agents. Distilled from Claude Code Team mode.
metadata:
  openclaw:
    requires:
      bins: [python3]
---

# Agent Coordinator

Distilled from Claude Code Team mode (TeamCreate/SendMessage protocol).
Coordinates multiple AI agents to work on tasks in parallel, then aggregates results.

## When to use

- Parallel data collection (scrape multiple sources)
- Parallel analysis (analyze multiple stocks/documents)
- Task decomposition (break complex task into subtasks)
- Review pipeline (one agent writes, another reviews)
- Ensemble decision (multiple agents vote on a decision)

## How it works

1. **Task Decomposition** — Break a complex task into parallel subtasks
2. **Agent Dispatch** — Assign each subtask to an agent worker
3. **Parallel Execution** — Run agents concurrently
4. **Result Aggregation** — Collect and merge results
5. **Conflict Resolution** — Handle conflicting outputs

## Usage

`ash
# Decompose and run a complex task
python3 {baseDir}/coordinator.py --task "Analyze top 5 tech stocks" --workers 3

# Run with custom subtasks
python3 {baseDir}/coordinator.py --subtasks subtasks.json

# Review pipeline (one writes, another reviews)
python3 {baseDir}/coordinator.py --pipeline review --input report.md

# Ensemble decision
python3 {baseDir}/coordinator.py --ensemble "Should we buy?" --voters 3

# Export results
python3 {baseDir}/coordinator.py --task "Research AI trends" --export results.json
`

## Task format

`json
[
  {"id": "subtask-1", "description": "Analyze AAPL financials", "agent": "analyst"},
  {"id": "subtask-2", "description": "Analyze GOOGL financials", "agent": "analyst"},
  {"id": "subtask-3", "description": "Compare results", "agent": "reviewer"}
]
`

## Built-in coordination patterns

| Pattern | Description |
|---------|-------------|
| fan-out | Same task to multiple agents, aggregate results |
| pipeline | Agent1 -> Agent2 -> Agent3 (sequential) |
| ensemble | Multiple agents vote, majority wins |
| decompose | Break task into subtasks, run in parallel |
| review | One agent produces, another reviews |

## Algorithm reference

Based on Claude Code Team mode:
- Task queue with priority
- Agent worker pool with concurrency limit
- Result aggregation with conflict resolution
- Timeout per subtask
- Progress tracking