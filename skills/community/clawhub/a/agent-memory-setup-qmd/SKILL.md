---
name: agent-memory-setup
description: >
  Set up the full OpenClaw agent memory system with 3-tier memory (HOT/WARM/COLD), daily logs, semantic search (QMD), and lossless context management (Lossless Claw). Use when onboarding a new agent, setting up memory for a fresh OpenClaw instance, or when asked to install the memory system on a new agent. Triggers on "set up memory", "install memory system", "onboard new agent memory", "memory setup", "agent onboarding", "configure agent memory", "add memory to my agent", "how do I set up memory", "initialize memory", "memory system for OpenClaw".
metadata:
  openclaw:
    homepage: https://github.com/nichochar/openclaw
    publisher: autosolutionsai-didac
    requires:
      bins:
        - bash
        - openclaw
---

# Agent Memory Setup

Set up a complete 3-tier memory system for any OpenClaw agent. Includes directory structure, memory files, semantic search, and context compaction.

## Quick Start

```bash
# 1. Run setup script
bash scripts/setup_memory.sh /path/to/workspace

# 2. Copy AGENTS.md template to workspace
# (read references/AGENTS_TEMPLATE.md, adapt, write to workspace/AGENTS.md)

# 3. Add config to openclaw.json (see Step 3 below for exact JSON)

# 4. Restart
openclaw gateway restart
```

For full details, read the sections below.

## When NOT to Use This Skill

- **Backing up or exporting memory** — this skill sets up memory, it doesn't handle backup/migration
- **Memory is already set up** — run the verification checklist in Step 4 instead of re-running setup
- **Debugging a specific memory issue** — check the Troubleshooting section directly
- **Changing memory tier content** — that's the agent's job during normal operation, not a setup task

## Prerequisites

Before running setup, ensure:
- **OpenClaw CLI** is installed and on your PATH (`openclaw --version`). If not installed, the setup script will still create directories and memory files, but plugin installation and config changes must be done manually.
- **Python 3.8+** (for QMD only — optional). Check with `python3 --version`. QMD provides semantic search (`memory_search`) over memory files. The core memory system (tiers, daily logs, Lossless Claw) works fully without it. If you can't install QMD (no Python, restricted server), you lose semantic search but keep everything else.
- **Node.js 18+** (for OpenClaw and Lossless Claw plugin).

### Platform Notes

- **Linux**: Fully supported. No special considerations.
- **macOS**: Fully supported. Config lives at `~/.openclaw/openclaw.json` (same as Linux). The setup script uses POSIX-compatible `date` and `mkdir` — no GNU-specific flags.
- **Windows (WSL2)**: Supported via WSL2 with Ubuntu or similar. Run everything inside WSL, not from Windows CMD/PowerShell. **Gotcha**: If your workspace is on a Windows-mounted drive (`/mnt/c/...`), file permissions may behave unexpectedly — prefer using a path inside the WSL filesystem (`~/workspace`) for reliable permission handling. The script's `set -euo pipefail` and `mkdir -p` work fine under WSL2.
- **Windows (native)**: Not supported. OpenClaw requires a Unix shell.

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

Read `references/AGENTS_TEMPLATE.md` and write it to the agent's workspace as `AGENTS.md`.

**What to customize:**
- **Heartbeat section** — adapt checks to the agent's domain (e.g., a CFO agent checks costs, a marketing agent checks social metrics, a DevOps agent checks CI pipelines)
- **HEARTBEAT.md** — create a small checklist of periodic tasks specific to the agent's role
- **Memory tier descriptions** — keep as-is unless the agent has unusual memory patterns

**What to keep as-is:**
- The session startup sequence (read SOUL.md, USER.md, memory files)
- Memory tiering instructions (HOT/WARM/COLD flow)
- The "Write It Down" and "No Mental Notes" sections
- MEMORY.md security rules (main session only)

### Step 3: Configure openclaw.json

Add to `agents.defaults` (or the specific agent config):

```json
"memorySearch": { "provider": "local" },
"compaction": { "mode": "safeguard" },
"contextPruning": { "mode": "cache-ttl", "ttl": "1h" },
"heartbeat": { "every": "1h" }
```

**What each setting does:**

| Setting | Purpose | Customization |
|---------|---------|---------------|
| `memorySearch` | Enables QMD semantic search over memory files | `"local"` is the only current provider |
| `compaction: safeguard` | Lossless Claw compacts old messages into expandable summaries instead of dropping them. "Safeguard" mode triggers compaction before context overflows, preserving everything via `lcm_expand` | Change mode only if you understand Lossless Claw internals |
| `contextPruning: cache-ttl` | Evicts stale context from the active window after the TTL expires. Works WITH Lossless Claw: content is compacted first, then pruned, so nothing is truly lost | Adjust `ttl` to match your use case: `"5m"` for fast-cycling agents, `"2h"` for long research sessions |
| `heartbeat` | Triggers periodic check-ins where the agent reads HEARTBEAT.md and performs maintenance tasks (email checks, memory review, etc.) | Adjust `"every"` interval: `"5m"` for monitoring agents, `"1h"` for general use, `"4h"` for low-activity agents |

Enable these plugins for the agent:

```json
"session-memory": { "enabled": true },
"bootstrap-extra-files": { "enabled": true },
"lossless-claw": { "enabled": true }
```

**What each plugin does:**

| Plugin | Role |
|--------|------|
| `session-memory` | Persists and loads memory context across sessions. Ensures the agent reads memory files (HOT/WARM/COLD) on startup |
| `bootstrap-extra-files` | Loads additional workspace files (AGENTS.md, SOUL.md, USER.md, TOOLS.md) into the agent's context at session start |
| `lossless-claw` | Compacts old conversation into summaries that can be expanded back on demand via `lcm_expand`, `lcm_grep`, and `lcm_expand_query`. Prevents amnesia in long conversations |

**Manual plugin install** (if the setup script didn't install them):
```bash
pip install qmd                # or: pipx install qmd / brew install qmd
openclaw plugins install @martian-engineering/lossless-claw
```

### Step 4: Restart and verify

```bash
openclaw gateway restart
```

**Verification checklist** — run each and confirm:

```bash
# 1. Memory directories exist
ls -d memory/ memory/hot/ memory/warm/

# 2. Memory files exist
ls memory/hot/HOT_MEMORY.md memory/warm/WARM_MEMORY.md MEMORY.md memory/heartbeat-state.json

# 3. Today's daily log exists
ls memory/$(date +%Y-%m-%d).md

# 4. QMD is installed
qmd --version

# 5. Lossless Claw plugin is active
openclaw plugins list | grep lossless-claw

# 6. AGENTS.md is in place
head -5 AGENTS.md

# 7. Config is applied (check openclaw.json)
grep -c "memorySearch\|compaction\|contextPruning\|lossless-claw" ~/.openclaw/openclaw.json
```

If any check fails, see the Troubleshooting section below.

## Migrating Existing Memory

If you already have `MEMORY.md` or daily logs from before this system:

1. **Run the setup script normally** — it checks `if [ ! -f ]` before creating each file, so your existing files are preserved untouched.
2. **Reorganize existing content into tiers:**
   - Move active/temporary context from MEMORY.md → `memory/hot/HOT_MEMORY.md`
   - Move stable preferences, API refs, recurring config → `memory/warm/WARM_MEMORY.md`
   - Keep long-term decisions, milestones, lessons learned in `MEMORY.md` (COLD tier)
3. **Existing daily logs** stay in `memory/` as-is — the system reads them from there already.

## Recovery

**Corrupted memory file**: Delete the corrupted file and re-run `bash scripts/setup_memory.sh /path/to/workspace`. The script only creates files that don't exist, so other memory files are safe. Alternatively, manually recreate the file with the template header from the setup script.

**Lost or deleted AGENTS.md**: Re-copy from `references/AGENTS_TEMPLATE.md` and customize.

**Broken openclaw.json**: Restore from backup (the setup script doesn't modify openclaw.json — config changes are manual). If no backup exists, re-add the config from Step 3 above.

**General principle**: The setup script is always safe to re-run. It never overwrites existing files.

## Using Lossless Claw After Setup

Once installed, Lossless Claw works automatically:

1. **Compaction is automatic** — as conversations grow long, old messages are compacted into summaries behind the scenes.
2. **The agent retrieves context on demand** using these tools:
   - `lcm_expand` — expand a compacted summary back into its original messages
   - `lcm_grep` — search across all compacted history by regex or text
   - `lcm_expand_query` — ask a question and get answers from compacted context
3. **No agent code changes needed** — if the agent has access to lcm_* tools (standard in OpenClaw), it can retrieve anything that was compacted.
4. **AGENTS.md instructs the agent** to update HOT_MEMORY before compaction flushes, so critical working state survives even when context is pruned.

## How the Tiers Work

| Tier | File | Purpose | Update Frequency |
|------|------|---------|-----------------|
| 🔥 HOT | `memory/hot/HOT_MEMORY.md` | Current task, pending actions | Every few turns |
| 🌡️ WARM | `memory/warm/WARM_MEMORY.md` | Stable preferences, API refs, gotchas | When things change |
| ❄️ COLD | `MEMORY.md` | Milestones, decisions, distilled lessons | Weekly/monthly |

### Concrete examples per tier

**🔥 HOT** — "Currently debugging auth flow for client X. Waiting on API key from Bob. Next step: test endpoint once key arrives."

**🌡️ WARM** — "User prefers bullet lists over paragraphs. Slack workspace is #eng-team. API rate limit is 100 req/min. Always use UTC timestamps."

**❄️ COLD** — "2025-03-15: Migrated from v1 to v2 API. Key lesson: always pin dependency versions. Decision: adopted trunk-based development."

Daily logs (`memory/YYYY-MM-DD.md`) capture raw session events. Periodically, the agent reviews daily logs and promotes important items up to COLD.

## Multi-Agent & Multi-Context Workspaces

### Shared workspaces (multiple agents, one directory)

- **HOT_MEMORY is shared** — all agents read it. Never put agent-specific debugging context here (e.g., "Current task: fix auth bug"). Other agents (including voice/avatar) will pick it up and fixate on it.
- **Keep HOT_MEMORY generic** — use it for general state like "User is in a meeting until 3pm" or "Deploy freeze until Friday."
- **Daily logs are shared too** — agents writing to the same `memory/YYYY-MM-DD.md` should prefix entries with their name to avoid confusion.
- **WARM and COLD are typically safe** — preferences and long-term memory apply across agents.

### Separate contexts (one agent, multiple domains)

Each OpenClaw agent maps to one workspace. If you need separate memory contexts (e.g., work vs. personal):

- **Option A: Two separate agents** — each with its own workspace and memory system. Cleanest separation.
- **Option B: Use WARM memory for context switching** — track multiple contexts in WARM_MEMORY (sections for "Work" and "Personal"), switching focus based on conversation.
- **Option C: Separate memory subdirectories** — create `memory/work/` and `memory/personal/` with separate HOT files, and instruct the agent (via AGENTS.md) which to use based on context. Advanced; requires custom AGENTS.md logic.

## Long-Term Maintenance

**Daily logs grow over time.** Each day creates a new `memory/YYYY-MM-DD.md` file. Over a year, this accumulates ~365 small files. This is generally fine (each file is small — typically 1–10 KB), but for long-running agents:

- **Archive old logs**: Move logs older than 90 days to `memory/archive/` to keep the main `memory/` directory fast to scan. QMD can still index the archive if configured.
- **The agent handles promotion**: During heartbeats, the agent reviews daily logs and promotes important items to COLD (MEMORY.md). Once promoted, daily logs become reference-only.
- **Disk usage is modest**: Even with years of logs, expect tens of MB at most. Lossless Claw summaries are stored separately by the plugin and managed automatically.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Agent doesn't read memory files on startup | AGENTS.md missing or doesn't include memory instructions | Copy `references/AGENTS_TEMPLATE.md` → `AGENTS.md` |
| `memory_search` not working | QMD not installed or memorySearch not configured | Run `qmd --version`; add `"memorySearch": { "provider": "local" }` to config |
| Old conversations vanish (no summaries) | Lossless Claw not enabled | Check `openclaw plugins list` for lossless-claw; enable in plugins config |
| Config changes have no effect | Gateway not restarted | Run `openclaw gateway restart` |
| Plugin install fails | openclaw CLI not in PATH or npm issue | Verify `openclaw --version`; try `npm install -g openclaw` |
| Agent overwrites existing memory files | Script bug (shouldn't happen) | Script checks `if [ ! -f ]` before creating — report if override occurs |
