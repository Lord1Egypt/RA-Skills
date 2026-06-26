---
name: deep-recall
version: 1.0.8
description: Pure-Python recursive memory recall for persistent AI agents. Manager→workers→synthesis RLM loop — no Deno, no fast-rlm, just HTTP calls to any OpenAI-compatible LLM.
metadata: {"openclaw": {"requires": {"env": ["ANTHROPIC_API_KEY (optional)", "OPENAI_API_KEY (optional)", "GOOGLE_API_KEY (optional)", "OPENROUTER_API_KEY (optional)", "DEEPSEEK_API_KEY (optional)", "MISTRAL_API_KEY (optional)", "TOGETHER_API_KEY (optional)", "GROQ_API_KEY (optional)", "FIREWORKS_API_KEY (optional)", "COHERE_API_KEY (optional)", "PERPLEXITY_API_KEY (optional)", "SAMBANOVA_API_KEY (optional)", "CEREBRAS_API_KEY (optional)", "XAI_API_KEY (optional)", "MINIMAX_API_KEY (optional)", "ZHIPU_API_KEY (optional)", "MOONSHOT_API_KEY (optional)", "DASHSCOPE_API_KEY (optional)"], "config_paths": ["~/.openclaw/openclaw.json", "~/.openclaw/agents/*/agent/models.json", "~/.openclaw/credentials/*"]}, "homepage": "https://github.com/Stefan27-4/DeepRecall"}}
---

# DeepRecall v2 — OpenClaw Skill

Pure-Python recursive memory for persistent AI agents.
Implements the Anamnesis Architecture: *"The soul stays small, the mind scales forever."*

## Description

DeepRecall gives AI agents **infinite memory** by recursively querying their own
memory files through a manager→workers→synthesis RLM loop — entirely in Python.
No Deno runtime, no fast-rlm subprocess, no vector database. Just markdown files
and HTTP calls to any OpenAI-compatible LLM endpoint.

When the agent needs to recall something, DeepRecall:

1. **Scans** the workspace for memory files (scoped by category)
2. **Indexes** file metadata — headers, topics, dates, people
3. **Manager** selects the most relevant files from the index
4. **Workers** (parallel) extract exact verbatim quotes from each file
5. **Synthesis** combines quotes into a cited, grounded answer

Workers are constrained by anti-hallucination prompts to return only verbatim
quotes. The synthesis step cites every claim with `(filename:line)`.

## Installation

```bash
pip install deep-recall
```

Or install from source:

```bash
git clone https://github.com/Stefan27-4/DeepRecall
cd DeepRecall && pip install .
```

### Dependencies

- **httpx** (preferred) or **requests** — HTTP client for LLM calls
- **PyYAML** — config parsing
- **Python ≥ 3.10**
- An LLM provider configured in OpenClaw

> **v2 breaking change:** Deno and fast-rlm are no longer required.
> The entire RLM loop runs in-process as pure Python.

## Quick Start

```python
from deep_recall import recall

result = recall("What did we decide about the project architecture?")
print(result)
```

## API

### `recall(query, scope, workspace, verbose, config_overrides) → str`

The primary entry point. Runs the full manager→workers→synthesis loop.

```python
from deep_recall import recall

result = recall(
    "Find all mentions of budget discussions",
    scope="memory",          # "memory" | "identity" | "project" | "all"
    verbose=True,            # print progress to stdout
    config_overrides={
        "max_files": 5,      # max files the manager can select
    },
)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | `str` | *(required)* | What to recall / search for |
| `scope` | `str` | `"memory"` | File scope — see [Scopes](#scopes) |
| `workspace` | `Path \| None` | auto-detect | Override workspace path |
| `verbose` | `bool` | `False` | Print provider, model, file selection info |
| `config_overrides` | `dict \| None` | `None` | Override `max_files` and other settings |

**Returns:** A string containing the recalled information with source citations,
or a `[DeepRecall]` status message if no files/results were found.

---

### `recall_quick(query, verbose) → str`

Fast, cheap recall scoped to identity files. Best for simple lookups.

```python
from deep_recall import recall_quick

name = recall_quick("What is my human's name?")
```

Equivalent to `recall(query, scope="identity", config_overrides={"max_files": 2})`.

---

### `recall_deep(query, verbose) → str`

Thorough recall across all workspace files. Best for cross-referencing.

```python
from deep_recall import recall_deep

summary = recall_deep("Summarize all decisions from March")
```

Equivalent to `recall(query, scope="all", config_overrides={"max_files": 5})`.

---

### CLI

```bash
python deep_recall.py <query> [scope]

# Examples
python deep_recall.py "What was the first project we worked on?"
python deep_recall.py "Find budget discussions" all
```

## Scopes

Scopes control which files DeepRecall searches. Narrower scopes are faster
and cheaper.

| Scope | Files Included | Speed | Cost | Use Case |
|---|---|---|---|---|
| `identity` | SOUL.md, IDENTITY.md, MEMORY.md, USER.md, TOOLS.md, HEARTBEAT.md, AGENTS.md | ⚡ Fastest | Cheapest | "What's my name?" |
| `memory` | Identity files + memory/LONG_TERM.md + memory/*.md daily logs | 🔄 Fast | Low | "What did we do last week?" |
| `project` | All readable workspace files (skips binaries, node_modules, .git) | 🐢 Slower | Medium | "Find that config change" |
| `all` | Identity + memory + project (everything) | 🐌 Slowest | Highest | "Search everything" |

### File Categories

DeepRecall classifies discovered files into categories:

- **soul** — `SOUL.md`, `IDENTITY.md` — who the agent IS (always in context)
- **mind** — `MEMORY.md`, `USER.md`, `TOOLS.md`, `HEARTBEAT.md`, `AGENTS.md` — compact orientation
- **long-term** — `memory/LONG_TERM.md` — full detailed memories, grows forever
- **daily-log** — `memory/YYYY-MM-DD.md` — raw daily logs
- **workspace** — everything else (project files, configs, docs)

## Configuration

DeepRecall reads your existing OpenClaw setup — no additional config files needed.

### Provider Resolution

Provider, API key, and model are resolved automatically from:

1. `~/.openclaw/openclaw.json` — primary model setting
2. `~/.openclaw/agents/main/agent/models.json` — provider base URLs
3. `~/.openclaw/credentials/` — cached tokens (e.g. GitHub Copilot)
4. Environment variables — fallback (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`, etc. (18+ providers supported, all optional))

### Supported Providers (20+)

Anthropic · OpenAI · Google (Gemini) · GitHub Copilot · OpenRouter · Ollama ·
DeepSeek · Mistral · Together · Groq · Fireworks · Cohere · Perplexity ·
SambaNova · Cerebras · xAI · Minimax · Zhipu (GLM) · Moonshot (Kimi) · Qwen

### Auto Model Pairing

The manager and synthesis steps use your primary model. Workers use a cheaper
sub-agent model automatically:

| Primary Model | Worker Model |
|---|---|
| Claude Opus 4 / 4.6 | Claude Sonnet 4 |
| Claude Sonnet 4 / 4.5 | Claude Haiku 3.5 |
| GPT-4o / GPT-4 | GPT-4o-mini |
| Gemini 2.5 Pro | Gemini 2.0 Flash |
| DeepSeek Reasoner | DeepSeek Chat |
| Llama 3.1 70B | Llama 3.1 8B |

### `config_overrides`

Pass overrides via the `config_overrides` parameter:

```python
recall("query", config_overrides={
    "max_files": 5,       # max files manager can select (default: 3)
})
```

## Skill Files

| File | Purpose |
|---|---|
| `deep_recall.py` | Public API — `recall`, `recall_quick`, `recall_deep`, RLM loop |
| `provider_bridge.py` | Resolves LLM provider, API key, base URL from OpenClaw config |
| `model_pairs.py` | Maps primary models to cheaper worker models |
| `memory_scanner.py` | Discovers and categorises workspace files by scope |
| `memory_indexer.py` | Builds a structured Memory Index (topics, people, timeline) |
| `__init__.py` | Package exports |

## Memory Layout

Recommended workspace structure for the Anamnesis Architecture:

```
~/.openclaw/workspace/
├── SOUL.md              # Identity — always in context, never grows
├── IDENTITY.md          # Core agent facts
├── MEMORY.md            # Compact index (~100 lines), auto-loaded each session
├── USER.md              # About the human
├── AGENTS.md            # Agent behavior rules
├── TOOLS.md             # Tool-specific notes
└── memory/
    ├── LONG_TERM.md     # Full memories — grows forever, searched via DeepRecall
    ├── 2026-03-05.md    # Daily raw log
    ├── 2026-03-04.md
    └── ...
```

## ⚠️ Privacy Notice

DeepRecall reads your workspace memory files and **sends their contents to your configured LLM provider** (Anthropic, OpenAI, Gemini, etc.) to perform recall. This is how it works — there is no local-only mode.

**What gets sent:**
- File metadata (names, headings, topics) → to the manager LLM
- Full file contents of selected files → to worker LLMs
- This may include personal notes, daily logs, project files

**What is NOT sent:**
- API keys and credentials (read locally for auth, never in prompts)
- Files outside your workspace

**Credentials used locally:**
- `~/.openclaw/openclaw.json` and `~/.openclaw/credentials/*` — to resolve your LLM provider
- Env vars (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`, etc. (18+ providers supported, all optional)) — as fallback if no OpenClaw config found

## Recommended Memory Architecture

DeepRecall works best with a **two-tier memory system**:

### Tier 1: MEMORY.md (The Index)
- **Auto-loaded every session** — keep it SMALL (~100 lines)
- Contains: quick reference facts, active projects, key metrics, a **table of contents** pointing to LONG_TERM.md sections
- Think of it as your orientation file — "what do I need to know right now?"
- If it grows past ~120 lines, move details to LONG_TERM.md

### Tier 2: memory/LONG_TERM.md (The Encyclopedia)
- **Never auto-loaded** — searched via DeepRecall when needed
- Contains: full context, decisions with reasoning, timestamps, bugs with fixes, architecture details
- **Grows forever** — never delete, only append
- The devil is in the details — "the diary entry, not the Wikipedia summary"

### Tier 3: memory/YYYY-MM-DD.md (Daily Logs)
- Raw notes of what happened each day
- Distilled into LONG_TERM.md at end of day

### Nightly Sync Routine
At the end of each day (or via cron/heartbeat):
1. Read today's daily log
2. Append key events, decisions, lessons, bugs, metrics to LONG_TERM.md
3. Update MEMORY.md index table if new topics appeared

> ⚠️ **Setting this up?** Ask your human before restructuring existing memory files.
> Show them this recommendation and let them decide how to organize their agent's memory.

## License

MIT — see [LICENSE](../LICENSE).
