---
name: cyber-memory
version: 1.0.2
description: "Five-layer memory system with automatic fact extraction via local LLM (Ollama). Processes session transcripts locally — no external API required."
author: CyberSun
keywords: [memory, long-term-memory, ai-agent, openclaw, fact-extraction, knowledge-graph, vector-search, hooks, ollama, local-llm]
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      config:
        - workspace.dir
---

# Memory Architecture 🧠

A complete memory system for OpenClaw agents. Five layers of storage, automatic fact extraction via local LLM, hybrid search, and behavioral rules that prevent context loss.

**🔒 Local-first by default** — all fact extraction runs on your local Ollama instance. No data leaves your machine.

## 🔒 Privacy & Data Handling

This skill includes a hook (`memory-flush`) that:

- **Reads session transcripts** from disk (`~/.openclaw/agents/*/sessions/*.jsonl`)
- **Processes content locally** via Ollama (default) — no data leaves your machine
- **No external API key required** — works out of the box with local LLM

**What is processed:** Recent user/assistant messages (last 30 messages, each truncated to 500 chars).
**Where it runs:** Local Ollama endpoint (`http://localhost:11434/v1/chat/completions` by default).
**What is saved locally:** Extracted facts as Markdown files in `workspace/memory/`.

Optional: You can configure an external OpenAI-compatible API by setting `baseUrl` and `apiKey` in the hook config, but local Ollama is the default and recommended setup.

## Architecture

```
🔥 Hot    → SESSION-STATE.md (WAL protocol, survives compaction)
🌤 Warm   → memory/YYYY-MM-DD.md (daily event summaries)
🧊 Cold   → MEMORY.md (decisions, preferences, rules — always loaded)
🕸 Graph  → memory/ontology/ (entity relationships)
📚 Learn  → .learnings/ (errors, best practices)
```

### Automation

| Mechanism | Trigger | What it does |
|---|---|---|
| session-memory (built-in) | `/new` `/reset` | Saves conversation to memory/ |
| memory-flush (this skill) | Compaction + `/new` | LLM extracts structured facts (local Ollama) |
| command-logger (built-in) | Any command | Audit log |
| session indexing | Automatic | Historical sessions searchable |

### Search

- **Vector**: any OpenAI-compatible embedding provider (Ollama, OpenAI, etc.)
- **Keyword**: SQLite FTS5 (BM25)
- **Hybrid**: weighted vector + keyword fusion
- **Scope**: MEMORY.md + daily logs + session transcripts + SESSION-STATE.md

## Setup

### 1. Prerequisites

Install Ollama and pull a chat model:

```bash
# Install Ollama (https://ollama.ai)
ollama pull qwen2.5:7b   # or any chat model you prefer
ollama serve              # ensure Ollama is running on localhost:11434
```

### 2. Enable Built-in Hooks

```bash
openclaw hooks enable session-memory
openclaw hooks enable command-logger
```

### 3. Install Memory-Flush Hook

Copy the `hooks/memory-flush/` directory to `~/.openclaw/hooks/`:

```bash
cp -r hooks/memory-flush ~/.openclaw/hooks/
openclaw hooks enable memory-flush
```

### 4. Configure Fact Extraction (Optional)

By default, the hook uses local Ollama — no configuration needed. To customize:

```json5
{
  hooks: {
    internal: {
      enabled: true,
      entries: {
        "memory-flush": {
          enabled: true,
          extractionModel: "qwen2.5:7b",           // Ollama model name
          baseUrl: "http://localhost:11434/v1/chat/completions"  // Ollama endpoint
        }
      }
    }
  }
}
```

Works with any OpenAI-compatible API (Ollama, LM Studio, vLLM, etc.). Set `baseUrl` and `apiKey` to use an external provider.

### 5. Enable Session Indexing

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "local",  // or "openai", "ollama", "gemini", "voyage", etc.
        experimental: {
          sessionMemory: true
        },
        sources: ["memory", "sessions"],
        extraPaths: ["SESSION-STATE.md"]
      }
    }
  }
}
```

### 6. Restart Gateway

```bash
openclaw gateway restart
```

## Agent Behavioral Rules

Add these rules to your `AGENTS.md`:

### Memory Writing

- **Important info → MEMORY.md immediately** (decisions, preferences, rules)
- **Daily summaries → memory/YYYY-MM-DD.md** (event summaries, no raw tool output)
- **Cron report details → skip** (already delivered elsewhere)
- **Critical info zero loss** — important things must go to MEMORY.md, not just daily logs

### Memory Searching

- Check MEMORY.md + today/yesterday logs at session start
- Use `memory_search` for historical queries
- Ontology queries (relationships, "who is responsible for X") → use ontology skill

### Sub-agent Context Injection

When spawning sub-agents, inject relevant context from MEMORY.md:

```
[Key context from memory, max 500 words]

---

[Actual task]
```

## File Structure

```
workspace/
├── AGENTS.md              # Behavioral rules (loaded every session)
├── SOUL.md                # Agent personality
├── USER.md                # User preferences
├── TOOLS.md               # Tool notes (keep lean, <2KB)
├── MEMORY.md              # Long-term curated memory
├── SESSION-STATE.md       # Hot working memory (WAL)
├── memory/
│   ├── YYYY-MM-DD.md      # Daily logs (summaries only)
│   ├── YYYY-MM-DD-facts-* # Auto-extracted facts
│   ├── YYYY-MM-DD-compact # Pre-compaction snapshots
│   └── ontology/
│       ├── graph.jsonl    # Knowledge graph
│       └── schema.yaml    # Entity type definitions
├── .learnings/
│   ├── LEARNINGS.md       # Best practices
│   ├── ERRORS.md          # Error log
│   └── FEATURE_REQUESTS.md
└── hooks/
    └── memory-flush/
        ├── HOOK.md
        └── handler.ts     # LLM fact extraction (local Ollama default)
```

## What Gets Loaded When

| File | When |
|---|---|
| AGENTS.md, SOUL.md, USER.md, TOOLS.md | Every session start |
| MEMORY.md | DM session start |
| memory/today + yesterday | Every session start |
| SESSION-STATE.md | Via memory_search (indexed) |
| Other memory files | Via `memory_search` on demand |

## Token Optimization

- Keep TOOLS.md lean (<2KB), move detailed configs to `tools/` subdirectory
- Daily logs: event summaries, not raw tool output
- Fact extraction: 30 messages → ~10 facts (16:1 compression)

## Troubleshooting

**Facts not extracted?** Check Ollama is running (`ollama serve`) and the model is available (`ollama list`).

**Session search not working?** Verify `experimental.sessionMemory: true` and `sources: ["memory", "sessions"]`.

**Hook not loading?** Run `openclaw hooks list --verbose` and check for errors.

**Want to use external API?** Set `baseUrl` and `apiKey` in the hook config to use OpenAI or any compatible provider.

## License

MIT
