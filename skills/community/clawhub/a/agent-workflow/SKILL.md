---
name: agent-workflow
description: "A structured workflow plugin for OpenClaw agents. Guides work through brainstorm → plan → execute → verify → deliver with persistent state and multi-project support. Trigger ONLY when the user explicitly requests a structured workflow (e.g. 'start a workflow', 'use agent-workflow', 'plan this project'). Do NOT trigger for: simple questions, one-off tasks, quick edits, routine conversations, or any task where the user has not requested workflow management."
---

# Agent Workflow

A structured workflow engine for OpenClaw agents. Migrated and generalized from the [superpowers](https://github.com/anthropics/claude-code-superpowers) workflow system into a code-agnostic, general-purpose workflow plugin.

## What it does

Provides a persistent state machine that guides your agent through a complete work lifecycle:

```
brainstorming → writing-plans → [execute] → verification → finishing-work
                                     ↓
                          subagent-driven-execution
                               OR
                          executing-plans
```

With support for:
- **Persistent state** — workflow survives session restarts
- **Multi-project** — run multiple workflows concurrently
- **Branching** — choose execution strategy at branch points
- **Context-plugins** — fork into review/parallel-agents without leaving main flow
- **Soft-guard goto** — jump to any step with warnings about skipped prerequisites
- **11 bundled Skills** — covering the full workflow lifecycle

## Installation

This is a **Plugin**, not a plain Skill. Install via:

```bash
openclaw plugins install clawhub:agent-workflow
openclaw gateway restart
```

Then enable in your `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "allow": ["agent-workflow"]
  },
  "tools": {
    "allow": ["agent_workflow"]
  }
}
```

## Usage

In your agent (via Feishu, Discord, or any channel):

```
Start a new workflow for my Q2 planning project
```

The agent will call `agent_workflow` with `action: "start"` and guide you through the workflow.

## Tool: `agent_workflow`

| Action | Description |
|--------|-------------|
| `start` | Begin a new workflow |
| `status` | View current state (all active workflows if no ID given) |
| `next` | Advance to the next step |
| `goto` | Jump to any node (soft-guard warns about skipped steps) |
| `complete` | Mark current node done |
| `fork` | Activate a context-plugin without leaving main flow |
| `join` | Complete a fork and return |
| `getSkill` | Load full SKILL.md for the current node |
| `list` | List all workflows |
| `abandon` | Abandon a workflow |

## Bundled Skills

- `brainstorming` — Turn ideas into specs
- `writing-plans` — Break specs into tasks
- `executing-plans` — Sequential execution
- `subagent-driven-execution` — Parallel subagent execution
- `verification-before-completion` — Evidence before claims
- `finishing-work` — Delivery options
- `dispatching-parallel-agents` — Fork independent tasks
- `requesting-review` — Dispatch reviewer subagent
- `receiving-review` — Evaluate feedback rigorously
- `systematic-problem-solving` — Root-cause diagnosis
- `writing-skills` — Create/improve Skills
