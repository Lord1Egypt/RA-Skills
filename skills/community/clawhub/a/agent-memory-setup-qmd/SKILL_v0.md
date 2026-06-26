---
name: agent-memory-setup
description: Set up the full OpenClaw agent memory system with 3-tier memory (HOT/WARM/COLD), daily logs, semantic search (QMD), and lossless context management (Lossless Claw). Use when onboarding a new agent, setting up memory for a fresh OpenClaw instance, or when asked to install the memory system on a new agent. Triggers on "set up memory", "install memory system", "onboard new agent memory", "memory setup", "agent onboarding".
---

# Agent Memory Setup

Set up a complete 3-tier memory system for any OpenClaw agent. Includes directory structure, memory files, semantic search, and context compaction.

## What Gets Installed

1. **3-tier memory structure** (HOT → WARM → COLD)
2. **QMD** — semantic search over MEMORY.md and memory/*.md files
3. **Lossless Claw** — compacts old conversation into expandable summaries (prevents amnesia)
4. **AGENTS.md** — instructions the agent reads every session to use the memory system
5. **openclaw.json config** — enables memorySearch, compaction, context pruning, heartbeats

## Setup Steps

### Step 1: Run the setup script

```bash
bash scripts/setup_memory.sh /path/to/agent/workspace
```

This creates:
- `memory/`, `memory/hot/`, `memory/warm/` directories
- `memory/hot/HOT_MEMORY.md` (active session state)
- `memory/warm/WARM_MEMORY.md` (stable config & preferences)
- `MEMORY.md` (long-term archive)
- `memory/YYYY-MM-DD.md` (today's daily log)
- `memory/heartbeat-state.json` (heartbeat tracking)

It also checks for QMD and Lossless Claw, installing them if possible.

### Step 2: Copy the AGENTS.md template

Read `references/AGENTS_TEMPLATE.md` and write it to the agent's workspace as `AGENTS.md`. Adapt the heartbeat section to the agent's domain if needed (e.g., a CFO agent checks costs, a marketing agent checks social metrics).

### Step 3: Configure openclaw.json

Add to `agents.defaults` (or the specific agent config):

```json
"memorySearch": { "provider": "local" },
"compaction": { "mode": "safeguard" },
"contextPruning": { "mode": "cache-ttl", "ttl": "1h" },
"heartbeat": { "every": "1h" }
```

Enable these plugins for the agent:

```json
"session-memory": { "enabled": true },
"bootstrap-extra-files": { "enabled": true },
"lossless-claw": { "enabled": true }
```

### Step 4: Restart and verify

```bash
openclaw gateway restart
```

Verify:
- `qmd --version` returns a version
- `openclaw plugin list` shows lossless-claw
- All memory directories and files exist

## How the Tiers Work

| Tier | File | Purpose | Update Frequency |
|------|------|---------|-----------------|
| 🔥 HOT | `memory/hot/HOT_MEMORY.md` | Current task, pending actions | Every few turns |
| 🌡️ WARM | `memory/warm/WARM_MEMORY.md` | Stable preferences, API refs, gotchas | When things change |
| ❄️ COLD | `MEMORY.md` | Milestones, decisions, distilled lessons | Weekly/monthly |

Daily logs (`memory/YYYY-MM-DD.md`) capture raw session events. Periodically, the agent reviews daily logs and promotes important items up to COLD.

## Plugin Details

- **QMD**: Local semantic search engine. Enables `memory_search` to find relevant memories by meaning, not just keywords. Install: `pip install qmd`
- **Lossless Claw** (`@martian-engineering/lossless-claw`): Instead of losing old messages when context fills up, compacts them into summaries that can be expanded back. Install: `openclaw plugins install @martian-engineering/lossless-claw`
