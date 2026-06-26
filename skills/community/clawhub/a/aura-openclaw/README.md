<p align="center">
  <img src="https://raw.githubusercontent.com/Rtalabs-ai/aura-core/main/logo.png" alt="Aura" width="100">
</p>

# 🔥 Aura for OpenClaw

**Persistent memory and instant knowledge retrieval for your OpenClaw agent.**

<p align="center">
  <a href="https://pypi.org/project/auralith-aura/"><img src="https://badge.fury.io/py/auralith-aura.svg" alt="PyPI"></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License: Apache 2.0"></a>
</p>

---

## Why Aura?

OpenClaw agents are powerful, but memory is hard. Context compaction can silently drop facts. MEMORY.md doesn't scale. Sessions start fresh.

**Aura gives your agent a real memory system:**

- ✅ **Memories persist across sessions** — facts, preferences, and decisions survive restarts
- ✅ **No context window pollution** — memory lives outside the prompt, retrieved on demand
- ✅ **Scales to thousands of documents** — compiled into indexed `.aura` archives, not flat markdown
- ✅ **Instant writes, zero blocking** — sub-millisecond write-ahead log means your agent is never waiting
- ✅ **Compile any file format** — PDFs, DOCX, code, spreadsheets, emails — 60+ formats into one queryable archive

All processing happens **locally on your machine**. Your data stays on your hardware.

---

## 3-Tier Memory OS

Aura organizes agent memory into three purpose-built tiers:

| Tier | What It Stores | Lifecycle |
|------|---------------|-----------|
| **`/pad`** | Working notes, scratch space, in-progress thinking | Transient — cleared between sessions |
| **`/episodic`** | Session transcripts, conversation history, decisions made | Auto-archived — retained for reference |
| **`/fact`** | Verified facts, user preferences, learned rules | Persistent — survives indefinitely |

> **Memory OS v2.1** (`auralith-aura>=0.2.3`): Enhanced with temporal decay scoring, noise filtering, deduplication, bloom filters, SimHash fuzzy matching, and tiered priority scoring — zero RAM overhead.

### How It Works

1. **Your agent writes to memory instantly** (~0.001s) via a write-ahead log — it's never blocked
2. **At session end**, the WAL compiles into durable `.aura` shards for fast retrieval
3. **On next session start**, your agent queries memory and picks up right where it left off

```python
from aura.memory import AuraMemoryOS

memory = AuraMemoryOS()

# Agent writes to the right tier based on context
memory.write("fact", "User prefers dark mode", source="agent")
memory.write("episodic", "Discussed deployment strategy for Q2 launch")
memory.write("pad", "TODO: check auth module for rate limiting")

# Later — search across all memory
results = memory.query("user preferences")
# → Returns: "User prefers dark mode" with metadata

# End session (compiles WAL to durable shards)
memory.end_session()
```

---

## Knowledge Compilation

Beyond memory, Aura compiles entire folders of documents into a single queryable `.aura` archive:

```
You: Learn everything in my ~/legal/ folder
Agent: 🔥 Compiling ~/legal/ → legal.aura
       ✅ Knowledge base created — documents indexed

You: What does clause 4.2 say about termination?
Agent: Based on contract_v3.pdf, clause 4.2 states...
```

Supports 60+ file formats: PDFs, DOCX, CSV, JSON, HTML, Markdown, Python, JavaScript, and more.

---

## Installation

### 1. Install Aura Core

```bash
pip install auralith-aura
```

### 2. Install the Skill

In OpenClaw, install from ClawHub or add manually:

```
/install aura-knowledge-compiler
```

Or clone this repo into your OpenClaw skills directory.

---

## Usage

### Compile Documents
```
You: Learn everything in ./docs
Agent: 🔥 Compiled → knowledge.aura
```

### Query Knowledge
```
You: How does the auth module work?
Agent: Based on auth_module.py and architecture.md...
```

### Remember Facts
```
You: Remember that I prefer dark mode and my timezone is EST
Agent: ✅ Written to /fact
```

### Recall Memory
```
You: What do you remember about me?
Agent: Found 3 results:
       [fact] User prefers dark mode, timezone EST
       [episodic] Discussed deployment strategy on 2026-02-15
       [pad] TODO: review auth module changes
```

---

## Data Provenance & Trust

Every memory entry stores `source` (agent/user/system), `namespace`, `timestamp`, `session_id`, and a unique `entry_id`. Nothing is inferred or synthesized — memory contains only what was explicitly written. No hidden embeddings, no derived data.

```python
memory.show_usage()                              # Inspect what's stored per tier
memory.prune_shards(before_date="2026-01-01")    # Prune by date
memory.prune_shards(shard_ids=["specific_id"])   # Delete specific shards
# Or delete ~/.aura/memory/ to wipe everything
```

---

## Runs Locally

- **Runs on your local hardware** — any modern laptop or desktop, your setup, your choice
- **Fully offline** — zero internet required after install
- **Cross-platform** — macOS, Windows, Linux, Python 3.8+

Your documents and memory never leave your machine.

---

## Scale Up with OMNI

Need enterprise-scale training pipelines, model fine-tuning, or production agent infrastructure? Check out [**OMNI**](https://omni.rtalabs.org).

---

## Links

- [Aura Core](https://github.com/Rtalabs-ai/aura-core) — The compiler
- [Website](https://aura.rtalabs.org) — Documentation
- [OMNI Platform](https://omni.rtalabs.org) — Enterprise scale
- [PyPI](https://pypi.org/project/auralith-aura/) — Install

---

<p align="center">
Made with ❤️ by <a href="https://rtalabs.org">Rta Labs</a>
</p>
