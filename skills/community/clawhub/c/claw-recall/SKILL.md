---
name: claw-recall
description: "Searchable conversation memory that survives context compaction. Indexes session transcripts into SQLite with full-text and semantic search so your agent can recover context after compaction, search past conversations, and find what other agents discussed. Works across multiple agents (OpenClaw + Claude Code). Also indexes Gmail, Google Drive, and Slack. Self-hosted, open source, no cloud dependency. Use when: recovering lost context, searching conversation history, cross-agent knowledge sharing. NOT for: replacing MEMORY.md or storing secrets."
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["python3", "pip3"] },
        "env": [
          { "key": "OPENAI_API_KEY", "description": "OpenAI API key for semantic search (optional, keyword search works without it)", "required": false },
          { "key": "PYTHONPATH", "description": "Path to claw-recall installation directory", "required": true }
        ],
        "tags": ["memory", "search", "recall", "conversation", "context", "compaction", "multi-agent"],
        "homepage": "https://github.com/rodbland2021/claw-recall",
        "community": "https://discord.gg/4wGTVa9Bt6"
      }
  }
---

# Claw Recall — Searchable Conversation Memory for AI Agents

Your agent just lost context mid-task. The decision you made an hour ago? Gone. What your other agent figured out yesterday? Unreachable. Claw Recall fixes this by indexing every conversation into a searchable database your agents can query anytime.

## The Problem

Context compaction drops critical decisions. Cross-session knowledge vanishes. Long conversations push early context out of the window. If you run multiple agents, they can't access each other's conversations at all. MEMORY.md helps with preferences, but it can't answer "what exactly did we discuss about the API last Tuesday?"

## What Claw Recall Does

- **Post-compaction recovery**: Get the full transcript from before compaction wiped your context
- **Cross-agent search**: Any agent can search any other agent's conversations
- **Unified search**: Conversations, captured thoughts, Gmail, Google Drive, and Slack in one query
- **Hybrid search**: Keyword (FTS5) + semantic (OpenAI embeddings) with automatic detection
- **Self-hosted**: Your data stays on your machine. No cloud, no subscription, no vendor lock-in.

## Installation

Claw Recall is an MCP server. Install the Python package, then connect it to your agent.

```bash
git clone https://github.com/rodbland2021/claw-recall.git
cd claw-recall
pip install -r requirements.txt
python3 -m claw_recall.indexing.indexer --source ~/.openclaw/agents-archive/ --incremental
```

Full setup guide: https://github.com/rodbland2021/claw-recall#quick-start

### Connect via MCP (OpenClaw)

Add to your OpenClaw config (`~/.openclaw/openclaw.json` or agent config):

```json
{
  "mcpServers": {
    "claw-recall": {
      "command": "python3",
      "args": ["-m", "claw_recall.api.mcp_stdio"],
      "env": { "PYTHONPATH": "/path/to/claw-recall" }
    }
  }
}
```

### Connect via MCP (Claude Code)

Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "claw-recall": {
      "command": "python3",
      "args": ["-m", "claw_recall.api.mcp_stdio"],
      "env": { "PYTHONPATH": "/path/to/claw-recall" }
    }
  }
}
```

### Remote agents (SSE)

Start the SSE server on the Claw Recall machine, then connect from anywhere:

```bash
python3 -m claw_recall.api.mcp_sse
```

```bash
claude mcp add --transport sse -s user claw-recall "http://your-server:8766/sse"
```

## MCP Tools Reference

### Primary Tools (use these most)

**`search_memory`** — The main search tool. Searches ALL sources in one call: conversations, captured thoughts (Gmail, Drive, Slack), and markdown files.

```
search_memory query="what did we decide about the API" [agent=butler] [days=7]
```

Optional params: `agent` (filter by agent name), `days` (limit to recent), `force_semantic` (use embeddings), `force_keyword` (use FTS5 only), `convos_only`, `files_only`, `limit`.

**`browse_recent`** — Full transcript of the last N minutes. The go-to tool for context recovery after compaction.

```
browse_recent [agent=kit] [minutes=30]
```

Returns the complete conversation with timestamps. Use this FIRST after any context reset.

**`capture_thought`** — Save an insight, decision, or finding so any agent can find it later.

```
capture_thought content="SQLite WAL mode requires checkpoint for readers to see writes" [agent=kit]
```

### Secondary Tools

| Tool | Purpose |
|------|---------|
| `search_thoughts` | Search captured thoughts only (usually `search_memory` is better) |
| `browse_activity` | Session summaries across agents for a time period |
| `poll_sources` | Trigger Gmail/Drive/Slack polling on demand |
| `memory_stats` | Database statistics (indexed sessions, messages, embeddings) |
| `capture_source_status` | Check external source capture health |

## When to Use Each Tool

| Situation | Tool | Example |
|-----------|------|---------|
| Just restarted / lost context | `browse_recent` | "What was I working on?" |
| Looking for a past decision | `search_memory` | "What did we decide about pricing?" |
| Need another agent's work | `search_memory` with `agent=` | "What did atlas find about the schema?" |
| Found something worth sharing | `capture_thought` | Save a reusable insight |
| Checking if something was discussed | `search_memory` with `days=` | "Did we talk about X this week?" |
| External source check | `poll_sources` | Trigger Gmail/Drive/Slack re-scan |

## How It Works

```
Session Files (.jsonl) → Indexer → SQLite DB (FTS5 + vectors) → MCP Tools
                                        ↑
Gmail / Drive / Slack → Source Poller ───┘
```

All data is stored locally in a SQLite database. Keyword search uses FTS5 (zero API keys). Semantic search uses OpenAI embeddings (requires `OPENAI_API_KEY` in `.env`).

## Requirements

- Python 3.10+
- SQLite 3.35+ (bundled with Python)
- OpenAI API key (optional, only for semantic search)

## Links

- **GitHub**: https://github.com/rodbland2021/claw-recall
- **Discord**: https://discord.gg/4wGTVa9Bt6
- **Full Guide**: https://github.com/rodbland2021/claw-recall/blob/master/docs/guide.md
- **Changelog**: https://github.com/rodbland2021/claw-recall/blob/master/CHANGELOG.md
