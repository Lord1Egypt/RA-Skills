---
name: agent-memory-setup-v2
description: >
  Create a 3-tier memory directory structure (HOT/WARM/COLD) for OpenClaw agents and
  configure the built-in memory-core plugin to use Google Gemini Embeddings 2
  (gemini-embedding-2-preview) for semantic memory search. Creates memory/ directories
  and stub files only — no code execution or external API calls from the setup script.
  After setup, the agent's memory_search tool uses Gemini's cloud embedding API
  to index memory files. Requires a free Google Gemini API key.
  Use when setting up a new agent's memory system or asked about semantic memory search.
  Triggers on "set up memory", "memory setup", "agent memory", "gemini memory",
  "semantic search memory", "onboard new agent".
---

# Agent Memory Setup v2 — Gemini Embeddings 2

Create a 3-tier memory directory structure for OpenClaw agents and configure semantic
search using **Google Gemini Embeddings 2**.

## What This Skill Does

1. **Creates directory structure and stub files** via a bash script (no network calls, no env reads, no dependencies)
2. **Provides configuration instructions** for openclaw.json to enable Gemini-based memory search

## Privacy Notice

⚠️ **After setup**, the agent's `memory_search` tool sends memory file content to
Google's Gemini embedding API for vectorization. This is how semantic search works —
files must be embedded to be searchable. The setup script itself makes no external calls.

## Prerequisite

Google Gemini API key — free at https://aistudio.google.com/apikey

## Setup

### Step 1: Create directory structure

```bash
bash scripts/setup_memory_v2.sh /path/to/agent/workspace
```

Creates: `memory/`, `memory/hot/`, `memory/warm/`, stub `.md` files, `heartbeat-state.json`.

### Step 2: Configure openclaw.json

Add under `agents.defaults`:

```json
"memorySearch": { "provider": "gemini" },
"compaction": { "mode": "safeguard" },
"contextPruning": { "mode": "cache-ttl", "ttl": "1h" },
"heartbeat": { "every": "1h" }
```

Set API key: `export GEMINI_API_KEY=your-key`

Enable plugin: `"lossless-claw": { "enabled": true }`

### Step 3: Restart

```bash
openclaw gateway restart
```

## Memory Tiers

- 🔥 **HOT** (`memory/hot/HOT_MEMORY.md`) — Active session state, pending actions
- 🌡️ **WARM** (`memory/warm/WARM_MEMORY.md`) — Stable preferences, references
- ❄️ **COLD** (`MEMORY.md`) — Long-term milestones and distilled lessons

## Optional Plugin

**Lossless Claw** (`@martian-engineering/lossless-claw`) — compacts old context into
expandable summaries to prevent amnesia. Install separately:
`openclaw plugins install @martian-engineering/lossless-claw`
