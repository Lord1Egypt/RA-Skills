---
name: agent-os
version: 0.1.1
description: Lightweight collaboration layer for multi-agent systems. Provides file-based protocols for audit findings, context packs, mission control, flight recording, and experience promotion. Triggers: agent os, multi-agent collaboration, agent handoff, audit finding, mission control, context pack, flight recorder, promote learning, 多Agent协作, Agent协作层, 审计发现, 上下文包, 健康视图, 飞行记录, 跨Agent交接, agent间协作, 多智能体协作
description_en: Lightweight collaboration layer for multi-agent systems — file-based protocols for findings, context, health views, and agent handoffs.
description_zh: "多 Agent 轻量协作层 — 基于文件协议的审计发现、上下文包、健康视图和 Agent 交接机制。触发词：多Agent协作、Agent协作层、审计发现、上下文包、健康视图、飞行记录、跨Agent交接"
allowed-tools: Read,Write,Edit,Bash,Glob,Grep
---

# Agent OS

> Make agent collaboration depend on auditable file protocols, not long chat logs.

## When to Use

This skill activates when any of these triggers appear:

- **Keywords**: agent os, multi-agent collaboration, agent handoff, audit finding, mission control, context pack, flight recorder, promote learning
- **Scenarios**: You are working with multiple agents on the same workspace and need shared state, audit trails, or human decision compression
- **Commands**: Any of the 6 core commands listed below

## What It Does

Agent OS provides a minimal file protocol (`<project>/.agent-os/`) that lets multiple agents share:

| Layer | Purpose | File |
|---|---|---|
| Audit Findings | Track issues through a status lifecycle | `findings.jsonl` |
| Context Packs | Give each agent run a compact starting context | `context-packs/*.md` |
| Mission Control | One-page health view for the human | `mission-control/*.md` |
| Flight Recorder | Replay agent decisions after the fact | `flight-recorder/*.jsonl` |
| Decision Briefs | Compress human todos into 1-3 real decisions | embedded in Mission Control |
| Experience Log | Classify learnings as rule/test/gate/prompt/doc | `experience-log.jsonl` |

## Directory Protocol

All Agent OS data lives under `<project-root>/.agent-os/`:

```
.agent-os/
├── findings.jsonl                  # Audit finding registry
├── experience-log.jsonl            # Promoted learnings
├── context-packs/
│   └── YYYY-MM-DD-<label>.md      # Task-scoped context summaries
├── mission-control/
│   └── YYYY-MM-DD.md              # Daily one-page health view
└── flight-recorder/
    └── YYYY-MM-DD.jsonl            # Agent run records
```

Agents MUST NOT require other directories. This is the only protocol root.

## Core Commands

### 1. `compile context pack`

Generate a compact context summary before an agent run.

**Script**: `scripts/compile_context_pack.py`

Reads workspace state (open findings, recent memory, repo status) and writes a context pack to `.agent-os/context-packs/`.

The primary agent should invoke this at session start or before handing off to another agent.

### 2. `upsert finding`

Create or update an audit finding in the registry.

**Script**: `scripts/upsert_finding.py`

Findings follow a status lifecycle: `open` → `accepted` → `fixed` → `verified` → `closed`. Alternate paths: `deferred`, `false_positive`.

### 3. `summarize mission control`

Generate a one-page project health view.

**Script**: `scripts/mission_control.py`

Aggregates open findings, active repos, stale items, and human decision items into a single Markdown file the human can scan in seconds.

### 4. `record flight`

Record an agent run's inputs, decisions, changes, and verification results.

**MVP scope**: Implemented as a workflow/template in `references/templates.md`. Script planned for v0.2.0.

### 5. `compress decisions`

Filter human-actionable items and compress them into 1-3 decision briefs.

**MVP scope**: Implemented as a workflow in `references/workflows.md`. Script planned for v0.2.0.

### 6. `promote learning`

Classify a learning as `rule`, `test`, `gate`, `prompt`, or `doc`.

**MVP scope**: Implemented as a workflow in `references/workflows.md`. Script planned for v0.2.0.

## Agent Onboarding Protocol

A new agent joining the workspace MUST:

1. Read the latest context pack (`.agent-os/context-packs/`)
2. Query open findings (`.agent-os/findings.jsonl` where status is `open`)
3. Read the latest mission control (`.agent-os/mission-control/`)
4. After completing work, either update findings or append a flight record

Minimal onboarding declaration (optional, for agent registries):

```json
{
  "agent": "<name>",
  "domain": "<scope>",
  "inputs": ["context-pack", "mission-control"],
  "outputs": ["handoff", "finding-update", "flight-record"]
}
```

## Boundaries

Agent OS explicitly does NOT:

- Replace GitHub Issues or project trackers (it complements them)
- Build a web dashboard or database backend
- Require any specific agent framework or runtime
- Introduce real-time messaging between agents
- Increase the human's cognitive load

## Scripts

Three scripts ship with v0.1.0 (Python 3.10+, zero external dependencies):

| Script | Purpose |
|---|---|
| `scripts/upsert_finding.py` | Create / update findings in `.agent-os/findings.jsonl` |
| `scripts/compile_context_pack.py` | Generate context packs from workspace state |
| `scripts/mission_control.py` | Generate one-page health view |

All scripts support `--help` and `--dry-run`.

## References

| File | Content |
|---|---|
| `references/schemas.md` | JSON/Markdown schemas for all data files |
| `references/workflows.md` | Daily check, weekly review, and upgrade workflows |
| `references/templates.md` | Copy-paste templates for each file type |
