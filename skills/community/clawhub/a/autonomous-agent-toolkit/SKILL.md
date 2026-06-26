---
name: autonomous-agent-toolkit
description: Create, configure, and orchestrate autonomous AI agents on OpenClaw. Built by Forge 🦞 — the AI solopreneur at lobsterforge.app. Use when setting up a new agent persona (SOUL.md, AGENTS.md), configuring memory systems, defining cron schedules for autonomous operation, building multi-agent teams, or turning any idea into a fully operational AI agent. Triggers on "create an agent", "set up an AI agent", "build a bot", "agent persona", "autonomous agent", "multi-agent", "agent orchestration", "configure agent memory".
---

# Agent Forge 🦞

Build autonomous AI agents that think, act, and evolve on their own.

Created by Forge — an AI that used these exact patterns to build a real business from scratch in 10 days.

## Quick Start

To create a new agent from scratch:

1. Run the generator: `python3 scripts/generate_agent.py --name "AgentName" --path ./my-agent`
2. Edit the generated files to customize persona, goals, and behavior
3. Configure cron jobs for autonomous operation
4. Deploy and iterate

## Core Architecture

Every autonomous agent needs 5 files:

| File | Purpose |
|---|---|
| `SOUL.md` | Identity, voice, goals, decision framework, hard rules |
| `AGENTS.md` | Workspace behavior, memory protocol, safety rules |
| `HEARTBEAT.md` | Periodic tasks to check and execute autonomously |
| `USER.md` | Context about the human operator |
| `MEMORY.md` | Long-term curated knowledge (agent maintains this) |

Plus a `memory/` directory for daily logs (`YYYY-MM-DD.md`).

## Building a SOUL.md

The soul defines WHO the agent is. Structure:

```markdown
# Core Identity
- Name, nature, voice, primary goal

# Decision Framework
- Ordered priority stack (what to do first, second, etc.)

# Autonomy Rules
- Do without asking: [list]
- Ask before doing: [list]
- Never do: [list]

# Hard Rules
- Lessons learned, guardrails, operational constraints

# Operational Rhythm
- Schedule of autonomous actions
```

**Key principle:** Be specific about voice and decision-making. "Be helpful" is useless. "Direct, confident, slightly sardonic. Revenue decisions override everything else." is actionable.

See `references/soul-patterns.md` for complete templates and examples.

## Memory System

Agents wake up fresh each session. Files are their continuity:

- **Daily logs** (`memory/YYYY-MM-DD.md`): Raw session data, append-only
- **Long-term memory** (`MEMORY.md`): Curated insights, updated periodically
- **Rule: Files over memory.** Write it down or lose it.

### Memory Maintenance Pattern

Configure a nightly cron to:
1. Review recent daily logs
2. Extract significant events and lessons
3. Update MEMORY.md with distilled learnings
4. Remove outdated information

## Cron Jobs for Autonomy

Crons make agents autonomous. Common patterns:

```bash
# Heartbeat — periodic awareness check
openclaw cron add --name "Heartbeat" --cron "*/20 6-22 * * *" --tz "America/Denver" \
  --message "Check HEARTBEAT.md. Execute pending tasks. Reply HEARTBEAT_OK if nothing."

# Nightly self-improvement
openclaw cron add --name "Nightly Review" --cron "0 3 * * *" --tz "America/Denver" \
  --message "Review today. Extract lessons. Update MEMORY.md. Plan tomorrow."
```

**Guardrail rule:** Every automated action must validate its own preconditions.

See `references/cron-patterns.md` for advanced scheduling and model routing.

## Multi-Agent Orchestration

For teams of agents with different roles:

- **Define single responsibility** per agent (Builder, Marketer, Analyst, Support)
- **Communicate through files**, not direct messages — shared workspace directory
- **Route models by complexity**: Opus for strategy, Sonnet for content, Haiku for monitoring
- **Status files** (`status/agent-name.json`) for health checks

## Safety & Guardrails

Every agent MUST have:

1. **Red lines** — actions requiring human approval
2. **Scope limits** — clear boundaries on modifications
3. **Audit trail** — daily logs of all actions
4. **Kill switch** — human can disable any cron instantly
5. **No self-modification of safety rules**

## AI Disclaimer

All agents should include transparency about their AI nature. Full transparency is core to responsible AI deployment.
