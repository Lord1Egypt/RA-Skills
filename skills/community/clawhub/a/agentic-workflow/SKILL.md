---
name: agentic-workflow
description: Enables the Agentic Workflow (Kanban + Heartbeat + QA Subagent). Use this when instructed to set up a continuous, asynchronous task system for any agent.
---

# Agentic Workflow (Kanban & Heartbeat System)

This skill enables an OpenClaw agent to operate continuously in the background using a State Machine (Kanban board) driven by heartbeats, and ensures high-quality output through a Maker-Checker (QA subagent) verification loop.

## Core Components

1. **The Task Board (`TASK_BOARD.yaml`)**: The single source of truth for all tasks.
2. **The Heartbeat (`HEARTBEAT.md`)**: The cron-engine that reads the board and executes tasks without user intervention.
3. **The Checker (QA Subagent)**: The `sessions_spawn` mechanism used to verify results before showing them to the user.

## Implementation Steps (How to install this for an agent)

When a user asks you to "set up the task system" or "agentic workflow", follow these steps in their workspace:

### 1. Create `TASK_BOARD.yaml`
Create this file in the workspace root:

```yaml
# Master Task Board
# Status Enum: TODO, IN_PROGRESS, QA_REVIEW, DONE, BLOCKED

current_sprint:
  active: false
  focus: "General"

tasks:
  - id: T-001
    title: "Example Task"
    status: TODO
    created_at: "YYYY-MM-DD"
    description: "What needs to be done."
    history: []
```

### 2. Update `HEARTBEAT.md`
Ensure the agent's `HEARTBEAT.md` contains the following Executor instruction (usually at the top or highest priority):

```markdown
### Task Board Executor (Highest Priority)
**Trigger**: Every heartbeat
**Action**:
1. Read `TASK_BOARD.yaml`.
2. If a task is `IN_PROGRESS`, continue its next step and update the `history` in YAML.
3. If no `IN_PROGRESS`, pick the highest priority `TODO` task, set to `IN_PROGRESS`, and begin.
4. When a task step yields a deliverable, set status to `QA_REVIEW`. Use `sessions_spawn(runtime="subagent")` to spawn a strict QA Checker agent. Give it the original goal and the output.
5. If the QA Checker approves, set status to `DONE` and notify the user. If it fails, fix the issue. If it fails 3 times, set to `BLOCKED` and notify the user.
6. If everything is running smoothly or waiting, DO NOT message the user. Reply `HEARTBEAT_OK` to stay silent.
```

## The Maker-Checker Loop (Crucial!)
When you (the Maker) finish a piece of work (e.g., generating a PDF, writing a script), **you must not immediately tell the user**. 
Instead, you must spawn a subagent to act as the Checker.

**Example `sessions_spawn` payload for the Checker:**
```json
{
  "task": "You are a strict QA inspector. Review this output: [Output]. Does it perfectly meet these requirements: [Requirements]? Reply ONLY with 'PASS' or a list of specific flaws to fix.",
  "runtime": "subagent",
  "mode": "run",
  "agentId": "distiller"  // Or the default subagent
}
```

## Golden Rules for the Agent
- **Silence is Golden**: Never message the user just to say "I am working on step 2." Only message them when a task hits `DONE` or `BLOCKED`.
- **Read Before Acting**: Always read `TASK_BOARD.yaml` upon waking up (heartbeat) to know your current state.
- **Self-Correction**: Let the QA subagent hurt your feelings. Fix the code/output internally before bothering the human.