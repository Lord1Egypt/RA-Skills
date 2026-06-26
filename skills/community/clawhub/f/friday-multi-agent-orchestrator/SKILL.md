---
name: multi-agent-orchestrator
description: Design, build, and manage multi-agent teams that turn a solo operator into a 1000-person organization. Covers team role design (CEO/PM/Engineer/Analyst/Writer/Monitor), inter-agent communication patterns, task distribution, conflict resolution, and priority management. Based on real production experience running 13-agent teams on OpenClaw. Use when the user wants to build an agent team, orchestrate multiple AI agents, design agent roles, set up agent communication, create a one-person company with AI agents, implement multi-agent workflows, or scale from solo to team-of-agents. Triggers on multi-agent, agent team, agent orchestration, AI team, agent collaboration, agent roles, one-person company, solo founder scaling, agent communication, task delegation to agents, swarm intelligence.
---

# Multi-Agent Orchestrator

Build production-grade agent teams. Battle-tested with 13 concurrent agents running real operations—financial analysis, content production, code engineering, and executive decision-making.

## Core Philosophy

**One human, many agents.** Each agent has a narrow, well-defined role. Communication flows through structured channels. The human sets direction; agents handle execution.

Three laws of agent teams:
1. **Specialization over generality** — Each agent does ONE thing well
2. **Structured communication** — No ad-hoc messaging; use defined protocols
3. **Human-in-the-loop for decisions** — Agents execute, humans decide

## Workflow

### Step 1: Define Your Team Composition

Read `references/team-roles.md` to select roles from the template library.

Start minimal (3 agents), scale to what you need:

| Team Size | Composition | Use Case |
|-----------|-------------|----------|
| Solo+1 | Human + 1 Assistant | Personal productivity boost |
| Core (3) | CEO + PM + Engineer | Small project delivery |
| Full (5+) | + Analyst + Writer + Monitor | Business operations |
| Enterprise (8+) | + Specialist roles per domain | Multi-domain scaling |

### Step 2: Design Communication Architecture

Read `references/communication-patterns.md` for protocol details.

Choose your communication stack:

| Pattern | Latency | Best For |
|---------|---------|----------|
| Shared directory | Minutes | Async handoffs, document sharing |
| Message passing (sessions_send) | Seconds | Real-time coordination |
| Heartbeat scheduling | Periodic | Monitoring, health checks |
| Event queue | Async | Complex multi-step workflows |

### Step 3: Set Up Task Management

Read `references/task-management.md` for tracking systems and report formats.

Implement the three-layer task system:
1. **Strategic** (CEO layer) — Goals and OKRs
2. **Tactical** (PM layer) — Sprint planning and allocation
3. **Operational** (Engineer layer) — Ticket execution and delivery

### Step 4: Launch and Iterate

```bash
# Minimum viable team setup
1. Create AGENTS.md for each agent with role + scope
2. Set up shared directory structure
3. Define reporting cadence
4. Run first task cycle
5. Review and adjust roles/communication
```

## Quick-Start Templates

### Solo Founder Starter Pack (3 agents)

**CEO (Strategic)** — Owns vision, priorities, decision gates
**PM (Coordination)** — Translates goals into tasks, tracks progress
**Engineer (Execution)** — Builds, tests, ships

### Content Machine (4 agents)

**Strategist** — Topic research, audience analysis, content calendar
**Writer** — Draft production, SEO optimization
**Editor** — Quality review, brand voice consistency
**Publisher** — Distribution, scheduling, performance tracking

### Research & Analysis (4 agents)

**Data Collector** — Gather raw data from sources
**Analyst** — Process, analyze, identify patterns
**Synthesizer** — Produce actionable reports
**Monitor** — Track changes, alert on anomalies

## Anti-Patterns (Learn from Our Mistakes)

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Agent with 5+ responsibilities | Context thrashing, low quality | Split into specialized agents |
| All-to-all communication | Message chaos, conflicts | Hub-and-spoke or hierarchical |
| No escalation path | Decisions stall, work stops | Define clear human escalation triggers |
| Copy-paste between agents | Knowledge silos, inconsistency | Shared knowledge base or wiki |
| Agents making strategic decisions | Misaligned with human intent | Agents propose, humans dispose |

## Platform Compatibility

This skill is platform-agnostic. The principles apply to:
- **OpenClaw** — Native multi-agent with sessions_send, shared dirs, cron
- **Claude Code** — Multiple sessions with file-based coordination
- **Codex** — Task files and workspace sharing
- **Cursor** — Agent rules files (.cursor/rules/) with workspace coordination

## Real-World Case Study

**晟瑞智联 AI Team (13 agents, OpenClaw)**

```
                    ┌─────────┐
                    │   于哥   │  (Human CEO)
                    └────┬────┘
                         │
                    ┌────┴────┐
                    │  老A    │  (CEO Agent / Strategic)
                    │  Friday │  (Executive Assistant)
                    └────┬────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
     ┌────┴────┐   ┌────┴────┐   ┌────┴────┐
     │  艾琳   │   │  瓦里斯  │   │  唐    │
     │ (PM)    │   │(Engineer)│   │(Writer) │
     └────┬────┘   └────┬────┘   └────┬────┘
          │              │              │
     ┌────┴────┐   ┌────┴────┐   ┌────┴────┐
     │Simons   │   │  小E    │   │  +6     │
     │(Analyst)│   │(Monitor)│   │specialists│
     └─────────┘   └─────────┘   └─────────┘
```

Communication: Shared directories for async, sessions_send for real-time, cron-based heartbeat for monitoring.

## References

- **Team Roles**: `references/team-roles.md` — Complete role templates with AGENTS.md examples
- **Communication**: `references/communication-patterns.md` — Protocols, file structures, message formats
- **Task Management**: `references/task-management.md` — Tracking systems, report formats, escalation rules
