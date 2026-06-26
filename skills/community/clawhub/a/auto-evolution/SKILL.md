---
name: auto-evolution
description: "Multi-agent auto-evolution system with hybrid mode — orchestrate review-execute-audit loops with 4 roles (Coordinator, Reviewer, Executor, Auditor). Supports manual subtasks (simple tasks) and automatic subtask generation via Reviewer (complex tasks). A single coordinator agent drives the loop by spawning sub-agents. Break goals into subtasks, auto-iterate with dual quality gates, and auto-package results. Use when: user wants autonomous task execution with built-in quality assurance."
---

# auto-evolution

**Category:** Agent Orchestration / Meta-Skill
**Version:** 0.7.0

---

## Description

**Multi-agent auto-evolution system** — a coordinator agent drives an autonomous review → execute → audit loop by spawning specialized sub-agents for each role.

This is a **meta-skill**: it doesn't handle business logic. It orchestrates the loop so complex tasks get completed autonomously with dual quality gates (pre-execution review + post-execution audit).

### Architecture (4 Roles)

| Role | Responsibility | When Spawned | Recommended Model |
|------|---------------|--------------|-------------------|
| **Coordinator** | Drives the loop, updates task state, spawns sub-agents | Always (heartbeat/cron) | Any (cost-efficient) |
| **Reviewer** | Pre-execution review, generates detailed subtasks | Complex tasks only | Strong (Sonnet/GPT-5.4) |
| **Executor** | Implements one subtask, runs verification | After review approves | Cost-effective (Qwen3.5-Plus) |
| **Auditor** | Post-execution audit, decides pass/retry | After execution completes | Strong (Sonnet/GPT-5.4) |

**Why 4 roles?**
- Reviewer and Auditor are **both quality gates** but serve different purposes
- Reviewer ensures the plan is sound before work starts
- Auditor verifies the result matches the plan after work completes
- Executor is pure labor — follows instructions, no judgment needed

**Cost control:** Only Reviewer and Auditor need strong models. Coordinator and Executor can use cheap models.

---

## 🔄 Hybrid Mode (v2.0)

**Task Complexity Assessment (5 dimensions, 1-5 points each):**

| Dimension | 1 point | 3 points | 5 points |
|-----------|---------|----------|----------|
| **Code Lines** | <100 | 200-500 | >1000 |
| **Files** | 1-2 | 5-10 | >20 |
| **Risk** | Docs/Test | Feature improvement | Architecture change |
| **Dependencies** | None | 3-5 | Cross-system |
| **Innovation** | Routine fix | Feature enhancement | New feature |

**Task Classification:**

| Total Score | Task Type | Subtask Mode | Flow |
|-------------|-----------|--------------|------|
| **5-10** | Simple | Manual | Executor only |
| **11-17** | Medium | Manual (recommended) or Auto | Optional Reviewer |
| **18-25** | Complex | Auto (required) | Reviewer → Executor → Auditor |

**Usage:**

```bash
# Create task (interactive)
node scripts/create-task.js

# Start Reviewer (complex tasks only)
node scripts/start-reviewer.js <task-id>
```

---

## Core Modules

| File | Purpose |
|------|---------|
| `scripts/heartbeat-coordinator.js` | Coordinator: scan tasks → spawn Reviewer/Executor/Auditor |
| `scripts/monitor.js` | Monitor: detect stuck tasks, clean orphaned locks |
| `scripts/pack-skill.js` | Package completed tasks → skill directories |
| `config/task-schema.json` | Task file JSON Schema |

---

## Setup

### 1. Initialize workspace

```bash
mkdir -p evolution/tasks evolution/archive evolution/test-results
```

### 2. Create a task

```bash
cp skills/auto-evolution/references/task-example.json evolution/tasks/task-001.json
# Edit with your goal and subtasks
```

### 3. Configure the coordinator

**Option A: Heartbeat** (recommended — in your agent's HEARTBEAT.md)

```markdown
## Evolution Loop
1. Run `node skills/auto-evolution/scripts/heartbeat-coordinator.js`
2. Parse output: if phase=review → spawn Reviewer sub-agent
3. Apply review → if phase=execute → spawn Executor sub-agent
4. Apply execution → if phase=audit → spawn Auditor sub-agent
5. Apply audit → done for this tick
```

**Option B: Cron**

```bash
openclaw cron add --agent <your-agent> \
  --name "evolution-coordinator" \
  --every 5m \
  --session isolated \
  --timeout-seconds 300 \
  --message "Evolution heartbeat: scan and process tasks."
```

### 4. (Optional) Configure the monitor

```bash
openclaw cron add --agent <any-agent> \
  --name "evolution-monitor" \
  --every 10m \
  --session isolated \
  --timeout-seconds 120 \
  --message "Run: node skills/auto-evolution/scripts/monitor.js"
```

### 5. Configure models (optional)

Edit `evolution/config/models.json` to customize which models are used for each role:

```json
{
  "roles": {
    "reviewer": "google/gemini-3.1-pro",
    "executor": "aiberm/gpt-5.4",
    "auditor": "google/gemini-3.1-pro",
    "coordinator": "bailian/qwen3.5-plus"
  }
}
```

**Default:** Scripts read from this config file. No environment variables needed.

### 6. Environment variables (optional)

```bash
export OPENCLAW_WORKSPACE=/path/to/workspace
export EVOLUTION_TASKS_DIR=/path/to/tasks
```

---

## How It Works

### Full Loop

```
Coordinator heartbeat
  → finds task (priority: reviewed > executing > pending)
  → if pending: spawn Reviewer → reviewed
  → if reviewed: spawn Executor → executing
  → if executing: spawn Auditor → pending (next) or completed ✅
```

### State Machine

```
pending → reviewed → executing → pending (next subtask)
                         → completed (all done)
                         → packaged ✅
```

### Key Rules

- **One subtask per iteration** — keeps cycles fast and reviewable
- **Dual quality gates** — Reviewer (before) + Auditor (after)
- **Only mark `completed` when all subtasks done**
- If Reviewer/Auditor API fails → wait and retry next heartbeat
- Monitor auto-resets tasks stuck > 10 minutes

---

## Task File Format

See `references/task-example.json` for a complete example.

Required fields:
```json
{
  "task_id": "task-001",
  "status": "pending",
  "goal": "What to build",
  "current_iteration": 0,
  "max_iterations": 10,
  "context": {
    "subtasks": ["Step 1", "Step 2", "Step 3"]
  },
  "history": []
}
```

---

## CLI Usage

```bash
# Scan and output next phase prompt
node scripts/heartbeat-coordinator.js

# Apply review result
node scripts/heartbeat-coordinator.js apply-review task-001.json review.txt

# Apply execution result
node scripts/heartbeat-coordinator.js apply-exec task-001.json exec.txt

# Apply audit result
node scripts/heartbeat-coordinator.js apply-audit task-001.json audit.txt

# Run monitor
node scripts/monitor.js

# Package completed tasks
node scripts/pack-skill.js
```

---

## Design Philosophy

- **4-role architecture** — Coordinator drives, Reviewer/Executor/Auditor specialize
- **Dual quality gates** — Review before, audit after — never skip either
- **Model-agnostic** — swap any model for any role
- **One subtask per tick** — predictable, reviewable, won't timeout
- **Self-healing** — monitor detects and fixes stuck states
- **Cost-efficient** — strong models only where judgment matters (Reviewer, Auditor)
