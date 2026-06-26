# Aoineco Squad Dispatch — Multi-Agent Task Router

<!-- 🌌 Aoineco-Verified | S-DNA: AOI-2026-0213-SDNA-SD01 -->

**Version:** 1.0.0  
**Author:** Aoineco & Co.  
**License:** MIT  
**Tags:** multi-agent, orchestration, dispatch, parallel, squad, task-routing

## Description

Routes tasks to the right agent based on skills, availability, cost, and priority. Evolved from the `dispatching-parallel-agents` pattern into a full squad orchestration engine for multi-agent teams.

**Core principle:** *Right agent for right job. Cheapest agent for simple tasks. Best agent for critical tasks.*

## Problem

Multi-agent squads waste resources when:
1. All tasks go to one expensive model
2. Simple community posts use Claude Opus ($$$) instead of Gemini Flash ($)
3. Tasks run sequentially when they could run in parallel
4. No visibility into which agent costs what

## Features

| Feature | Description |
|---------|-------------|
| **Skill-Based Routing** | Matches task requirements to agent specializations |
| **Cost-Aware Dispatch** | Prefers cheaper agents for normal tasks, best agents for critical |
| **Dependency Detection** | Automatically groups parallel vs sequential tasks |
| **Load Balancing** | Respects max concurrent tasks per agent |
| **Named Roster** | Pre-configured 7-agent squad with specializations |
| **Visual Plans** | Human-readable dispatch plans with cost estimates |

## Pre-Configured Squad

| Agent | Specialization | Model | Cost |
|-------|---------------|-------|------|
| 🧿 Oracle | Governance, Strategy | claude-opus | $$$ |
| ⚔️ Blue-Blade | Security, Audit | claude-sonnet | $$ |
| 📢 Blue-Sound | Community, Content | gemini-flash | $ |
| 👁️ Blue-Eye | Research, Data | gemini-flash | $ |
| 🧠 Blue-Brain | Strategy, Analysis | gemini-pro | $$ |
| ⚡ Blue-Flash | Build, Code | claude-sonnet | $$ |
| 🗂️ Blue-Record | Records, Docs | gemini-flash | $ |

## Quick Start

```python
from dispatch_engine import SquadDispatcher

dispatcher = SquadDispatcher()

dispatcher.add_task("Audit new skill", "Security scan", required_skills=["security"])
dispatcher.add_task("Post to BotMadang", "Korean content", required_skills=["community"])
dispatcher.add_task("Update docs", "Write summary", required_skills=["records"],
                    depends_on=["TASK-0001", "TASK-0002"])

plan = dispatcher.plan()
print(dispatcher.format_plan(plan))
```

## File Structure

```
aoineco-squad-dispatch/
├── SKILL.md               # This file
└── scripts/
    └── dispatch_engine.py  # Main engine (zero external dependencies)
```

## Zero Dependencies

Pure Python 3.10+. No pip install needed.
Designed for the $7 Bootstrap Protocol — every byte counts.
