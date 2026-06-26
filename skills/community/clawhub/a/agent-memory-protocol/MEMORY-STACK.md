# Memory Stack — External Tools & Integration Guide

<p align="center">
  <a href="MEMORY-STACK.md">English</a> · <a href="MEMORY-STACK.zh-CN.md">中文</a>
</p>

This document describes the full memory stack used alongside the [Agent Memory Protocol](SKILL.md). The skill defines **what** to write and **where**; this document explains **how the retrieval infrastructure works** and **how to configure it**.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Agent (LLM)                          │
│                                                         │
│  memory_search ──► qmd (vector+BM25 hybrid)             │
│  memory_get    ──► direct file read                     │
│  lcm_grep      ──► LosslessClaw SQLite DAG              │
│  lcm_expand    ──► LosslessClaw summary tree            │
└─────────────────────────────────────────────────────────┘
         │                          │
    ┌────▼──────┐           ┌───────▼──────┐
    │  qmd index│           │  lcm.db      │
    │ (SQLite + │           │ (SQLite DAG  │
    │  vectors) │           │  summaries)  │
    └────┬──────┘           └──────────────┘
         │
    ┌────▼──────────────────────┐
    │  Markdown files on disk   │
    │  memory/  +  blackboard/  │
    └───────────────────────────┘
```

**Two separate systems, two separate purposes:**

| System | Tool | What it indexes | When to use |
|--------|------|----------------|-------------|
| **qmd** | `memory_search` | Markdown files in `memory/` and `blackboard/` | Finding facts, preferences, project state |
| **LosslessClaw** | `lcm_grep` / `lcm_expand` | Past conversation summaries (compressed sessions) | Recovering decisions from old conversations |

---

## Component 1: qmd (Quick Markdown Search)

### What it does

qmd is a local semantic search engine for Markdown files. It builds a hybrid index (BM25 full-text + vector embeddings) over your `memory/` and `blackboard/` directories. The `memory_search` tool calls qmd under the hood.

### Installation

```bash
# Install via bun (recommended)
bun install -g @tobilu/qmd

# Or via npm
npm install -g @tobilu/qmd
```

### Configure collections

qmd uses **collections** to define which folders to index. Set them up once:

```bash
# Index the memory directory
qmd collection add memory-root-perlica /path/to/workspace/memory --pattern "**/*.md"

# Index the blackboard
qmd collection add blackboard /path/to/workspace/blackboard --pattern "**/*.md"

# Verify
qmd collection list
qmd status
```

### Wire it into OpenClaw

In `openclaw.json`:

```json5
{
  "memory": {
    "backend": "qmd",
    "qmd": {
      "command": "/path/to/qmd",          // output of: which qmd
      "searchMode": "vsearch",            // "vsearch" (vector) or "hybrid"
      "includeDefaultMemory": true,
      "update": {
        "interval": "5m",                 // re-index every 5 minutes
        "onBoot": true,                   // re-index on gateway start
        "waitForBootSync": false
      },
      "limits": {
        "maxResults": 10,
        "maxSnippetChars": 500
      },
      "scope": {
        "default": "allow"
      }
    }
  }
}
```

### Keep the index fresh

qmd auto-updates every `interval` while the gateway runs. To force a manual update:

```bash
qmd update
qmd embed   # regenerate vector embeddings if stale
```

### How agents use it

```
memory_search("project deadline") 
  → qmd vsearch over memory/ + blackboard/
  → returns top-N snippets with file path + line numbers
  → agent calls memory_get(path, from, lines) to read the exact section
```

**Search modes:**

| Mode | When to use |
|------|------------|
| `vsearch` | Default — semantic similarity, good for concepts |
| `query` | Best for research — auto-expands + reranks |
| `search` | BM25 keyword only — exact term matches |

Direct CLI access (for debugging):

```bash
qmd vsearch "project deadline"
qmd query "what models does the agent use" -c memory-root-perlica
qmd get qmd://memory-root-perlica/user/profile.md
qmd status
```

---

## Component 2: LosslessClaw (LCM)

### What it does

LosslessClaw replaces OpenClaw's default sliding-window context truncation with a DAG-based summarization system. When context fills up, it summarizes older exchanges into a tree of summaries stored in a local SQLite database (`~/.openclaw/lcm.db`). Nothing is thrown away — old conversations are compressed, not deleted.

### Installation

```bash
# Install via OpenClaw plugin system
openclaw plugins install @martian-engineering/lossless-claw
```

### Configure in OpenClaw

In `openclaw.json` under `plugins.entries.lossless-claw`:

```json5
{
  "plugins": {
    "allow": ["lossless-claw"],
    "entries": {
      "lossless-claw": {
        "enabled": true,
        "config": {
          "summaryProvider": "anthropic",       // provider for summarization model
          "summaryModel": "claude-haiku-4-5",   // cheap fast model for summaries
          "freshTailCount": 32,                 // recent messages kept verbatim (not summarized)
          "contextThreshold": 0.75,             // trigger compaction at 75% context usage
          "ignoreSessionPatterns": [
            "agent:*:cron:**"                   // don't summarize cron sessions
          ],
          "incrementalMaxDepth": 10             // max DAG depth before forcing a full roll-up
        }
      }
    }
  }
}
```

**Key parameters:**

| Parameter | Default | Notes |
|-----------|---------|-------|
| `summaryModel` | — | Use a cheap/fast model; haiku or flash recommended |
| `freshTailCount` | 32 | Recent N messages stay verbatim in context |
| `contextThreshold` | 0.75 | Compact when context hits this fraction |
| `ignoreSessionPatterns` | `[]` | Glob patterns for sessions to skip |
| `incrementalMaxDepth` | 10 | DAG depth limit before forced roll-up |

### How agents use it

LosslessClaw exposes four tools:

| Tool | What it does |
|------|-------------|
| `lcm_grep` | Regex/full-text search across all compressed summaries |
| `lcm_describe` | Look up a specific summary by ID (sum_xxx) |
| `lcm_expand` | Expand a summary tree to recover detail |
| `lcm_expand_query` | Answer a question by expanding relevant summaries |

**Retrieval pattern:**

```
lcm_grep("wechat plugin fix")
  → returns matching summary IDs (sum_abc123)
  
lcm_expand(summaryIds=["sum_abc123"])
  → returns the compressed content of that conversation segment

lcm_expand_query(query="what was decided about the wechat trigger symbol")
  → delegates expansion + Q&A to a sub-agent, returns focused answer
```

**When to use LosslessClaw vs qmd:**

| Scenario | Use |
|---------|-----|
| "What was the user's preference on X?" | `memory_search` → qmd (searches memory files) |
| "What did we decide in that session last week?" | `lcm_grep` → `lcm_expand` (searches compressed conversations) |
| "What's the current project status?" | `memory_search` → qmd (searches blackboard) |
| "Why did we change the trigger symbol?" | `lcm_expand_query` (recovers reasoning from old conversation) |

---

## How the Two Systems Complement Each Other

```
Information lifecycle:

  Conversation ──► LosslessClaw compresses ──► lcm.db (recoverable)
       │
       │  (agent writes structured facts to memory/)
       ▼
  memory/ files ──► qmd indexes ──► memory_search retrieves
```

- **qmd** is for **current truth** — the structured, curated facts the agent writes to `memory/` files
- **LosslessClaw** is for **conversation history** — the reasoning, discussions, and decisions from past sessions that haven't been formally written to memory files

A well-functioning agent:
1. Writes important facts/decisions to `memory/` files (permanent, structured)
2. Relies on qmd for day-to-day retrieval
3. Falls back to `lcm_grep` when needing to recover something from an old conversation that wasn't formally recorded

---

## Maintenance

### qmd

```bash
# Check index health
qmd status

# Force re-index (run if files were added/changed outside gateway)
qmd update

# Rebuild vector embeddings
qmd embed -f

# Check what's indexed
qmd ls memory-root-perlica
qmd ls blackboard
```

### LosslessClaw

```bash
# Check lcm.db size
ls -lh ~/.openclaw/lcm.db

# The database grows over time; OpenClaw manages it automatically
# No manual maintenance required
```

---

## Quick Reference

| I want to... | Command / Tool |
|-------------|---------------|
| Find a fact in memory | `memory_search("query")` |
| Read a specific file section | `memory_get(path, from, lines)` |
| Search old conversations | `lcm_grep("pattern")` |
| Recover a past decision | `lcm_expand_query("what was decided about X")` |
| Force re-index memory | `qmd update` (CLI) |
| Check qmd health | `qmd status` (CLI) |
| Inspect a summary | `lcm_describe("sum_xxx")` |
