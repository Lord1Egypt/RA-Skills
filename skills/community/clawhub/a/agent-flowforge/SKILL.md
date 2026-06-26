---
name: flowforge
description: "Run structured multi-step workflows via FlowForge engine. Use when user requests step-by-step execution, structured workflows, or when a task needs enforced ordering (e.g., 'follow the workflow', 'use flowforge', 'step by step process'). Helps AI agents execute multi-step tasks without skipping critical steps."
---

# FlowForge Workflow Runner

Execute multi-step workflows defined in YAML files using the FlowForge state machine engine.

## Prerequisites

FlowForge CLI must be installed. Check with:

```bash
flowforge --version
```

If the command fails or is not found, run the setup flow in [setup.md](setup.md) before proceeding.

## My Workflows

<!-- Map your intents to workflow names here. -->
<!-- When you notice the same intent matching the same workflow 2-3 times, add it. -->
<!-- This saves a `flowforge list` lookup every time and makes triggering instant. -->

| Intent | Workflow |
|--------|----------|
| *(add your mappings here as you use FlowForge)* | |

## Core Loop

### 1. Start or Resume

```bash
# Check for active instances
flowforge active

# Resume if exists
flowforge status

# Or start new
flowforge start <workflow>
```

### 2. Get Action

```bash
flowforge run <workflow>
```

Returns JSON: `{ action: { type, node, task, branches, ... } }`

### 3. Execute by Action Type

**`type: 'spawn'`** — Node has `executor: subagent`. **MUST spawn a sub-agent:**

```
sessions_spawn(
  task: action.task,
  mode: "run",
  label: "flowforge-<workflow>-<node>"
)
```

Wait for sub-agent to complete. Collect its output.

⚠️ **NEVER execute spawn tasks yourself in the main session.** The whole point of subagent nodes is delegation — they run in parallel, unblock the main session, and use the best tool for the job. If you do it yourself, you're blocking the main session and defeating the purpose.

**`type: 'prompt'`** — Node needs your direct judgment. Execute the task yourself in the main session. Use this for decision-making, lightweight checks, and coordination — not heavy implementation work.

**`type: 'complete'`** — Workflow finished. Report results to the user.

### 4. Advance

After getting the result (from sub-agent output or your own work):

```bash
echo "<result summary>" | flowforge advance
```

Or:

```bash
flowforge advance --result "<result summary>"
```

If the node had branches, include `Branch: N` in the result so the engine knows which path to take.

### 5. Repeat

Go back to step 2. Loop until `type: 'complete'`.

## Rules

- **spawn = sub-agent.** When action type is `spawn`, use `sessions_spawn`. Not exec, not a coding CLI, not doing it yourself in the main session.
- **Never skip nodes.** Execute every node's task before advancing.
- **Run to completion.** Execute all nodes before reporting to the user. If a node spawns a sub-agent, wait for it to finish, then advance.
- **State persists.** Workflows survive session restarts. Use `flowforge active` to resume.
- **Post-run:** Record results in your daily log.

## Manual Mode

If you prefer step-by-step control instead of the run/advance JSON loop:

```bash
flowforge status          # See current task
# ... execute task ...
flowforge next            # Advance (linear node)
flowforge next --branch N # Advance (branching node)
```

The same spawn rules apply: if the current node has `executor: subagent`, spawn a sub-agent.

## Creating New Workflows

See [references/yaml-format.md](references/yaml-format.md) for the full YAML spec.

```yaml
name: my-workflow
description: What this workflow does
start: first-node

nodes:
  first-node:
    task: What to do (detailed instructions for the executor)
    executor: subagent    # spawn a sub-agent for this node
    next: second-node

  second-node:
    task: Make a decision based on results
    # executor defaults to 'inline' — agent does it directly
    branches:
      - condition: success
        next: done
      - condition: retry
        next: first-node

  done:
    task: Report results
    terminal: true
```

### Node Fields

- `task` (required): Natural language instruction for what to do
- `executor`: `'subagent'` (spawn) or `'inline'` (default, do it yourself)
- `next`: Single next node for linear flow
- `branches`: Array of `{condition, next}` for branching
- `terminal`: `true` for end nodes

## Troubleshooting

- **"No active instance"**: Run `flowforge start <workflow>`
- **"Workflow not found"**: Run `flowforge list` to see available workflows
- **Wrong node / stuck**: Use `flowforge reset` to restart
- **Sub-agent failed**: Check the error, fix the issue, re-run the node or advance manually
