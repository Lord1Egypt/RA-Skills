---
name: elephantastic
description: "Executive function stack for AI agents: GTD-style task management, error/learning capture, and periodic self-review using Taskwarrior."
---

# Elephantastic

## Quick Start

1. **Install Taskwarrior** — `apt install taskwarrior` / `brew install task`
2. **Test capture** — `task add +in "first item"`
3. **Configure UDAs** — copy UDAs from `references/taskwarrior-schema.md` into `~/.taskrc`
4. **Confirm it works** — `task next`
5. **Point the agent** at this skill's `SKILL.md`

A complete executive function stack for AI agents. This is not about a human managing an AI's tasks — it's about an **autonomous agent self-managing its own cognitive overhead** using GTD principles. The agent's memory — never forget.

| Layer | Tool | Role |
|---|---|---|
| **RAM** | [Taskwarrior](https://taskwarrior.org) | Actionable tasks, internal focus, backlog |
| **Hard Drive** | Markdown files | Context, decisions, lore, "why" |
| **Workbench** | `ops/session_state.md` | Real-time state recovery (where I was 5 seconds ago) |

## Why Agent GTD? (The Sovereign Advantage)

Mainstream AI agents "drift" or plateau because they try to manage complex state inside a volatile context window. **Elephantastic** solves the fundamental scaling bottlenecks of autonomous systems:

### 1. Structured Persistence vs. Markdown Bloat
Most agents use flat files for memory. These grow noisy, expensive to parse, and lead to "context amnesia." By using **Taskwarrior** as a structured external database, the agent can query its own focus with surgical precision (`task next`, `task +urgent`), keeping the active context window lean and high-signal.

### 2. Autonomous Multi-Session Continuity
Chatbots forget the "Big Picture" once the session resets. Agent GTD provides an **Internal Prefrontal Cortex** that tracks dependencies, blockers, and `+next` actions across days or weeks. It allows an agent to "wake up" during a heartbeat, check its burndown, and make progress without human re-explanation.

### 3. Data-Driven Self-Evolution
Instead of vague prompts for "better behavior," Elephantastic implements a formal **Learning Pipeline**. Tool failures (`+error`) and user corrections (`+learning`) are logged as actionable tasks. This turns mistakes into a queryable backlog for structural improvement, making the agent more reliable with every run.

### 4. Overload Protection & Prioritization
Native Taskwarrior math (Urgency/Importance) replaces LLM waffling. The agent prioritizes tasks based on explicit weights—due dates, dependencies, and project priorities—ensuring it tackles high-leverage work instead of getting lost in "low-hanging fruit" loops.

### 5. Offline-First & Fully Auditable
No black-box state. The agent's "intent" is stored in a local, plain-text backed, version-controllable database. You can audit, fix, or reprioritize the agent’s internal goals directly via the CLI, providing a level of transparency and control that cloud-based task managers can't match.

## Core Architecture

| Layer | Tool | Role |
|---|---|---|
| **RAM (Active)** | Taskwarrior | Actionable queue, internal focus, urgency math |
| **Hard Drive (Ref)** | Markdown | Wisdom, decisions, project lore, identity |
| **Workbench (Volatile)** | `session_state.md` | Instant context recovery for active tasks |

## The Learning Loop

Log failures immediately to the `Internal.Learnings` project:

| Situation | Tag | Benefit |
|---|---|---|
| Command / tool fails | `+error` | Tracks systemic reliability issues |
| User correction | `+learning` | Captures preference drift & identity tweaks |
| Capability gap | `+featreq` | Maps the agent's actual "frontier" for the developer |

## References

- `references/taskwarrior-schema.md` — Installation, `.taskrc` config, UDAs, custom reports.
- `references/review-runbook.md` — Periodic review loop (2 min → 20 min depth levels).
- `references/vitality-heartbeat.md` — Agent silence detection and alerting.

