# 🚀 Revolution — Multi-Agent Auto-Evolution

**Let your AI agents build things while you sleep.**

Revolution uses a coordinator agent to drive an autonomous review → execute → audit loop. Define a goal, break it into subtasks, and the system iterates through them — spawning specialized sub-agents for each role, with dual quality gates (pre-execution review + post-execution audit).

## How It Works

```
Your coordinator agent (on a heartbeat timer)
    ↓
Finds a task needing work
    ↓
┌─────────────────────────────────────────────┐
│ Phase 1: Spawn Reviewer                     │
│ - Audits the plan                           │
│ - Generates detailed instructions           │
│ - Decides: approve / revise                 │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Phase 2: Spawn Executor                     │
│ - Implements one subtask                    │
│ - Runs verification tests                   │
│ - Outputs results                           │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Phase 3: Spawn Auditor                      │
│ - Verifies instructions were followed       │
│ - Checks acceptance criteria                │
│ - Decides: pass / fail (retry)              │
└─────────────────────────────────────────────┘
    ↓
All subtasks done → completed → auto-packaged ✅
```

**Why 3 sub-agent roles?**
- **Reviewer** ensures the plan is sound (before work)
- **Executor** does the actual work (follows instructions)
- **Auditor** verifies the result matches the plan (after work)

Use strong models for Reviewer and Auditor (judgment roles). Use cost-effective models for Executor (labor role).

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) with heartbeat or cron support
- At least 1 configured agent (the coordinator)
- A model that supports `sessions_spawn` for sub-agents

## Quick Start

### 1. Install

```bash
clawhub install auto-evolution
```

Or clone:
```bash
git clone https://github.com/cjboy007/revolution-skill.git
cp -r revolution-skill ~/.openclaw/workspace/skills/auto-evolution
```

### 2. Initialize

```bash
cd ~/.openclaw/workspace
mkdir -p evolution/tasks evolution/archive
```

### 3. Create a Task

```bash
cp skills/auto-evolution/references/task-example.json evolution/tasks/task-001.json
# Edit with your goal and subtasks
```

### 4. Configure Your Coordinator

**Option A: Heartbeat** (add to your agent's HEARTBEAT.md)
```markdown
## Evolution Loop
1. Run `node skills/auto-evolution/scripts/heartbeat-coordinator.js`
2. Parse output:
   - phase=review → spawn Reviewer sub-agent → apply-review
   - phase=execute → spawn Executor sub-agent → apply-exec
   - phase=audit → spawn Auditor sub-agent → apply-audit
3. Done for this tick
```

**Option B: Cron**
```bash
openclaw cron add --agent <your-agent> \
  --name "evolution-coordinator" --every 5m \
  --session isolated --timeout-seconds 300 \
  --message "Evolution heartbeat: scan and process tasks."
```

### 5. Watch It Run

Tasks auto-progress through the loop. Check status:
```bash
node skills/auto-evolution/scripts/monitor.js
```

## Architecture

```
┌─────────────────┐
│   Coordinator    │  ← Your agent, on a timer
│  (any model)     │
└────────┬────────┘
         │ spawns
    ┌────┴────┬──────────┐
    ▼         ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐
│Reviewer│ │Executor│ │Auditor │  ← Sub-agents, spawned on demand
│(strong)│ │(cheap) │ │(strong)│
└────────┘ └────────┘ └────────┘
```

**Roles are filled by sub-agents, not specific agents.** You configure which model to use when spawning. The system doesn't care about agent names.

## State Machine

```
pending → reviewed → executing → pending (next subtask)
                            → completed (all done)
                            → packaged ✅
```

- One subtask per heartbeat tick
- Monitor auto-resets stuck tasks (>10 min)
- Failed audit triggers retry (up to `max_iterations`)

## File Structure

```
auto-evolution/              ← This skill
├── SKILL.md
├── README.md
├── config/
│   └── task-schema.json
├── scripts/
│   ├── heartbeat-coordinator.js   (the loop driver)
│   ├── monitor.js                 (stuck detection)
│   └── pack-skill.js              (auto-packaging)
└── references/
    └── task-example.json

evolution/                   ← Runtime data (your workspace)
├── tasks/
│   └── task-001.json
├── archive/
└── test-results/
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENCLAW_WORKSPACE` | `~/.openclaw/agents/main/workspace` | Workspace root |
| `EVOLUTION_TASKS_DIR` | `{workspace}/evolution/tasks` | Active tasks |
| `EVOLUTION_SKILLS_DIR` | `{workspace}/skills` | Output skills |
| `EVOLUTION_ARCHIVE_DIR` | `{workspace}/evolution/archive` | Completed tasks |

## Design Principles

- **4-role architecture** — Coordinator drives, 3 sub-agents specialize
- **Dual quality gates** — Review before, audit after — never skip either
- **Model-agnostic** — swap any model for any role
- **One subtask per tick** — predictable, reviewable, won't timeout
- **Self-healing** — monitor detects and fixes stuck states
- **Cost-efficient** — strong models only where judgment matters

## License

MIT

---

Built with [OpenClaw](https://openclaw.ai) 🐾
