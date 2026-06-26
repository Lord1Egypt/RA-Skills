name: agent-orchestration-kit
description: >
  Use when setting up or managing a multi-agent task orchestration system on OpenClaw.
  Use this skill whenever the user wants to: coordinate multiple agents, set up an agent team,
  dispatch tasks across agents, track task progress in real-time, add approval gates to agent
  workflows, create a star topology with a leader agent, build a multi-agent pipeline,
  manage agent callbacks, or anything involving agents working together on tasks.
  Also use when the user says "set up agents", "build a team", "orchestrate work",
  "multi-agent workflow", "agent coordination", or "task dispatch".
version: 0.2.0
author: kuannnn
metadata:
  {
    "openclaw": {
      "emoji": "🎛️",
      "requires": {
        "bins": ["node"]
      }
    }
  }
---

# Agent Orchestration Kit

## Overview

This skill sets up a multi-agent task orchestration system on OpenClaw. It creates:

- **Star topology** — Leader hub + specialist spokes, no spoke-to-spoke communication
- **Fully async dispatch** — `sessions_send` with `timeoutSeconds: 0`, Leader is never blocked
- **Task file tracking** — each task is a markdown file with full state, steps, outputs, and log
- **Structured callback protocol** — standardized signals drive Leader's routing decisions
- **Real-time status notifications** — owner sees live progress updates on every dispatched task
- **Approval workflow** — nothing executes externally without explicit owner approval
- **Heartbeat safety net** — automatic stale task detection and recovery every 3 minutes via OpenClaw Heartbeat

## What This Kit Is

This is not a prompt pack or a collection of agent personas. It is an **orchestration protocol** — a set of rules that govern how multiple agents coordinate work:

1. Leader decomposes requests into atomic tasks
2. Each task becomes a file before dispatch — the single source of truth
3. Agents work asynchronously and callback with structured signals
4. Leader processes callbacks, updates status, and routes next steps
5. Quality gates and approval workflow prevent unreviewed output from reaching external systems

The agent roles are pluggable — swap in any specialist. The orchestration rules are the constant.

## Prerequisites

1. OpenClaw v2026.2.26+ installed and `openclaw onboard` completed
2. At least one auth profile exists
3. `~/.openclaw/` directory exists

## Onboarding Flow

When first triggered, this skill runs an interactive setup process.

### Step 1: Prerequisites Check

- [ ] OpenClaw installed and `openclaw onboard` completed
- [ ] `~/.openclaw/` directory exists
- [ ] At least one auth profile configured

If any prerequisite is missing, guide the user to resolve it before continuing.

### Step 2: Team Selection

Present team templates. All teams include **Leader** (required), **Executor** (recommended), and the **Reviewer pattern** (on-demand).

| Team | Specialists | Best For |
|------|-------------|----------|
| **Software Dev** | Senior Developer, Software Architect | Code-centric projects |
| **Content Studio** | Content Creator, Researcher | Content production workflows |
| **Research & Analysis** | Researcher | Investigation and deep analysis |
| **Minimal** | (none — add agents later) | Custom setups, start lean |

> See `templates/teams/` for team definitions. See `templates/agents/` for all available agent templates.

After team selection, the user can add individual agents from the template catalog or create custom agents.

### Step 3: Instance Configuration

Collect from the owner:

1. **Name** (optional) — How the team addresses the owner. Can be omitted if Leader's SOUL.md/USER.md defines identity.
2. **Timezone** — For scheduling and timestamps (e.g., Asia/Taipei, US/Pacific)
3. **Communication language** — Language for all owner-facing messages (agent-to-agent is English)

After collecting, write the values to `shared/INSTANCE.md` (created by scaffold). Also update Leader's `SOUL.md` communication section to reflect the chosen language.

### Step 4: Run Scaffold

```bash
# Create directories, copy templates, inject orchestration rules
bash scripts/scaffold.sh \
  --skill-dir "$(pwd)" \
  --team <selected-team>

# For named leader workspaces:
# bash scripts/scaffold.sh --skill-dir "$(pwd)" --team <selected-team> --leader-workspace workspace-bae
```

The scaffold creates:
- Agent workspace directories with SOUL.md and AGENTS.md
- Orchestration protocol rules injected into every agent's AGENTS.md
- Shared operations files (`shared/operations/`)
- Task tracking directory (`tasks/`, `tasks/archive/`)
- Heartbeat template (HEARTBEAT.md) for task status checking

### Step 4b: Preview & Merge Config

**Always preview before merging.** Run dry-run first so the user can inspect what will change:

```bash
# Preview what will be merged (no changes written)
node scripts/patch-config.js \
  --config ~/.openclaw/openclaw.json \
  --dry-run
```

Show the user the dry-run output and explain what each section does. Only proceed after confirmation:

```bash
# Apply the merge
node scripts/patch-config.js \
  --config ~/.openclaw/openclaw.json
```

**What the config patcher merges:**

| Config Key | What It Sets | Why |
|------------|-------------|-----|
| `agents.defaults` | compaction: safeguard, timeout: 1800s, maxConcurrent: 4 | Stable defaults for multi-agent operation |
| `agents.list[]` | Agent entries (id, name, workspace, tools.deny) | Register each agent with OpenClaw |
| `tools.agentToAgent` | enabled: true, allow list | Enable inter-agent communication |
| `tools.sessions` | visibility: "all" | Agents can see each other's sessions |
| `tools.exec.safeBinTrustedDirs` | /bin, /usr/bin, /opt/homebrew/bin, /usr/local/bin | Trusted paths for CLI execution |
| `session.agentToAgent` | maxPingPongTurns: 3 | A2A session ping-pong limit |
| `session.parentForkMaxTokens` | 100000 | Fork token budget |
| `hooks.internal` | boot-md, bootstrap, command-logger, session-memory | Enable internal hooks |
| `messages.ackReactionScope` | "all" | Acknowledgment on all messages |
| `commands` | native: "auto", nativeSkills: "auto", restart: true | Native command settings |
| `agents.defaults.heartbeat` | every: "3m", target: "last" | Heartbeat interval for task status checking |

**Version compatibility:** The script checks for OpenClaw v2026.2.26+ features (A2A sessions, agent list, exec trusted dirs). If the version is older, it will warn and suggest upgrading.

**Safety:** The script creates a timestamped backup of `openclaw.json` before writing. Restore with: `cp ~/.openclaw/openclaw.json.backup-<timestamp> ~/.openclaw/openclaw.json`

### Step 5: Verification

```
openclaw gateway restart
openclaw doctor
```

Verify:
- [ ] Leader responds to messages
- [ ] `sessions_send` to at least one agent succeeds
- [ ] HEARTBEAT.md exists in the leader workspace
- [ ] After 3+ minutes, leader session shows heartbeat activity (check session logs)

The orchestration kit uses OpenClaw's Heartbeat mechanism (configured automatically by `patch-config.js` at 3-minute intervals). Task status messages and results are sent to the channel where the owner's request originated (the task's `route`). There is no fixed operations channel for routine updates.

If heartbeat is not triggering, ensure `agents.defaults.heartbeat` is set in `openclaw.json` AND the leader agent entry has an explicit `heartbeat` block.

## Agent Structure

### Required: Leader

The orchestration hub. Cannot be removed.

- Task analysis and decomposition
- Agent routing and async dispatch
- Callback processing and quality review
- Status notification management (send on dispatch, edit on every callback)
- Approval workflow gating
- Owner communication (only agent with direct owner access)

> Full protocol: `templates/leader/AGENTS.md`
> Persona: `templates/leader/SOUL.md`

### Recommended: Executor

Prevents Leader from blocking on heavy operations.

- File operations, CLI, configuration changes
- Workspace maintenance, directory operations
- Any operation that could take >30 seconds

Leader has `exec` access as fallback, but the protocol guides it to delegate time-consuming operations to Executor.

> Template: `templates/executor/`

### Built-in Pattern: Reviewer

Not a persistent agent. Spawned on-demand via `sessions_spawn` when:
- High-stakes deliverables need independent review
- Owner explicitly requests review
- Two consecutive rework failures on the same task

Uses `[APPROVE]` / `[REVISE]` signals. Max 2 review rounds per task.

> Template: `templates/reviewer/`

### Specialist Slots

Filled from templates or custom definitions. Each specialist receives:
1. **Role-specific content** from the chosen template (persona, workflow, output format)
2. **Orchestration rules** auto-injected by the scaffold (callback format, signals, context loss recovery)

Available templates:

| Template | Source | Description |
|----------|--------|-------------|
| Senior Developer | Built-in | Full-stack implementation, TDD, code quality |
| Software Architect | Built-in | System design, ADRs, trade-off analysis |
| Code Reviewer | Built-in | Code review, security audit, quality assessment |
| Content Creator | Built-in | Copywriting, visual direction, platform packaging |
| Researcher | Built-in | Market research, analysis, evidence-based briefs |
| Custom | Blank template | Define your own role |
| Agency Agents | External | 100+ templates from [agency-agents](https://github.com/msitarzewski/agency-agents) |

> See `templates/agents/_template.md` for the blank template structure.

## Core Protocol — Quick Reference

### Task Lifecycle

```
Owner request → Leader analyzes → Decomposes into atomic tasks →
  Creates task file (BEFORE dispatch) → Dispatches async →
  Sends status notification → Returns to owner (not blocked) →
  Processes callbacks → Updates status → Quality review →
  Delivers result [PENDING APPROVAL] → Owner approves → Execute
```

### Signals

| Signal | Meaning | Leader Action |
|--------|---------|---------------|
| `[READY]` | Complete and confident | Quality review → deliver or rework |
| `[BLOCKED]` | Cannot proceed | Assess alternative, re-route, or escalate |
| `[NEEDS_INFO]` | Needs more context | Gather info, re-brief |
| `[LOW_CONFIDENCE]` | Delivered but uncertain | Careful review, consider Reviewer |
| `[SCOPE_FLAG]` | Task bigger than expected | Reassess scope with owner |
| `[APPROVE]` | Reviewer approves | Mark `[PENDING APPROVAL]`, present to owner |
| `[REVISE]` | Reviewer requests changes | Compose revision request to original agent |
| `[PENDING APPROVAL]` | Awaiting owner approval | Hold until owner responds |
| `[CONTEXT_LOST]` | Session compacted | Re-send task context from task file |

### Task File

Each task: `tasks/T-{YYYYMMDD}-{HHMM}.md` — the single source of truth.

```markdown
# T-{id}: {task name}
status: in_progress | completed | cancelled
dispatched: {YYYY-MM-DD HH:MM}
route: {channel}:{thread}
callback_to: {Leader session key}
notification_status_msg: {messageId}
notification_result_msg: {messageId}

## Steps
1. [⏳] agent:{id} → {description}
   brief_to: agent:{id}:main
   output: {result summary}
   files: {paths}
```

> Full protocol (Leader's operating instructions): `workspace/AGENTS.md` (runtime) or `templates/leader/AGENTS.md` (source)
> Brief templates: `shared/operations/brief-templates.md` (runtime) or `references/brief-templates.md` (source)
> Approval pipeline: `shared/operations/approval-workflow.md` (runtime) or `references/approval-workflow.md` (source)
> Architecture and signals: `references/architecture.md`, `references/signals.md` (skill source)

## Adding Agents Post-Setup

### From Template Catalog

Say: "Add a Senior Developer agent" or "Add a Researcher to the team"

The kit will:
1. Create workspace from template
2. Inject orchestration rules
3. Update `openclaw.json`
4. Restart gateway

### Custom Agent

Say: "Add a custom agent: Security Auditor"

The kit will:
1. Create workspace from blank template
2. Guide through role definition (capabilities, output format, boundaries)
3. Inject orchestration rules
4. Update config

### From Agency Agents Catalog

Users can import agent templates from the [Agency Agents](https://github.com/msitarzewski/agency-agents) repo. The scaffold script can inject orchestration compliance rules into any external agent template:

```bash
bash scripts/scaffold.sh --inject-orchestration <path-to-agent.md>
```

## Directory Structure After Installation

```
~/.openclaw/
├── openclaw.json                     # Updated with agent configs
├── workspace/                        # Leader
│   ├── SOUL.md, AGENTS.md
│   ├── HEARTBEAT.md                  # Task status check procedure
│   ├── tasks/, tasks/archive/
│   └── shared/
│       ├── INSTANCE.md               # Owner name, timezone, language
│       └── operations/
│           ├── channel-map.md
│           ├── team-roster.md
│           ├── communication-signals.md
│           ├── brief-templates.md
│           └── approval-workflow.md
├── workspace-executor/
│   ├── SOUL.md, AGENTS.md
│   └── shared -> ../workspace/shared/
├── workspace-reviewer/               # On-demand (spawned by Leader)
│   ├── SOUL.md, AGENTS.md
│   └── shared -> ../workspace/shared/
├── workspace-{specialist}/           # Per specialist
│   ├── SOUL.md, AGENTS.md
│   └── shared -> ../workspace/shared/
```

## Scripts

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `scripts/scaffold.sh` | Create directories, copy templates, inject orchestration rules | Initial setup, adding agents |
| `scripts/patch-config.js` | Merge agent config into `openclaw.json` | Initial setup, adding agents |

## Customization

### Agent Behavior

Each agent has two files:
- **SOUL.md** — Persona, philosophy, boundaries. Freely editable.
- **AGENTS.md** — Operating procedures. Contains two sections:
  - *Orchestration Protocol* (auto-injected) — preserve this section
  - *Role-Specific Instructions* — freely editable

### Notification Format

Status message format and result delivery templates are in `references/brief-templates.md`. Customize the owner-facing templates to match your communication language and style.

### Approval Workflow

See `references/approval-workflow.md` for the full pipeline. Key customization points:
- Approval shortcuts (what phrases count as "approve")
- Stale approval timeout (default: 48h)
- Auto-approve rules (if any)
