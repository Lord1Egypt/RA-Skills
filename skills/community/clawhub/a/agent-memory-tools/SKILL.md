---
name: agent-memory-tools
description: Searches, stores, and manages agent memory across 4 sources (fact store, vector embeddings, BM25, knowledge graph). Runs 100% local via Ollama — no API keys, no cloud dependency. Use when searching workspace knowledge, extracting facts from text, detecting contradictions, auto-ingesting file changes, or building entity graphs. Triggers on memory recall, fact extraction, knowledge search, workspace indexing.
---

# Agent Memory Tools

Multi-source memory recall and fact management. Runs locally via Ollama (0€).

## Architecture

```
Question → unified_recall.py → fan-out 4 sources → merge → score → rerank → answer
                                 ├─ Fact store (Convex or local JSON)
                                 ├─ Vector embeddings (nomic)
                                 ├─ BM25 full-text (QMD)
                                 └─ Knowledge graph (JSON)

File changed → auto_ingest.py → extract facts → contradiction check → store
                               → update embeddings → rebuild graph
```

## Setup

```bash
# Install Ollama models (one-time)
ollama pull gemma3:4b              # LLM (~2s/call)
ollama pull nomic-embed-text-v2-moe  # Embeddings

# Verify everything works
python3 scripts/selftest.py
```

Requirements: Python 3.9+, Ollama, `curl`. Optional: QMD CLI (`bun install -g qmd`).

## Core Scripts

### Search memory

```bash
# Unified recall — recommended (all 4 sources, scored + reranked)
python3 scripts/unified_recall.py "What bugs happened last week?" --debug

# Multi-hop reasoning (chains searches with LLM synthesis)
python3 scripts/multihop_search.py "How does the deploy pipeline work?" --embed

# Temporal decay (recent facts score higher, errors protected)
python3 scripts/decay_search.py "recent issues" --half-life 14
```

### Extract and store facts

```bash
# Extract from text
python3 scripts/extract_facts.py "Some conversation or document" --store --debug

# Extract from file
python3 scripts/extract_facts.py --file path/to/doc.md --store

# Pipe from stdin
cat summary.md | python3 scripts/extract_facts.py --store
```

Facts are checked for contradictions locally (gemma3, ~2s) before storage. Categories: `knowledge`, `error`, `timeline`, `preference`, `tool`, `client`, `hr`.

### Auto-ingest workspace changes

```bash
python3 scripts/auto_ingest.py --scan          # One-shot: process modified .md files
python3 scripts/auto_ingest.py --watch          # Daemon: poll for changes every 30s
python3 scripts/auto_ingest.py --file doc.md    # Single file
```

Dedup by content hash + 5 min cooldown. Triggers: fact extraction → storage → embed cache update → graph rebuild.

### Build knowledge graph

```bash
python3 scripts/knowledge_graph.py              # Full rebuild
python3 scripts/knowledge_graph.py --dry-run    # Preview without writing
```

Graph stored at `.cache/knowledge-graph.json`. Auto-rebuilt incrementally by `auto_ingest.py`.

### Run tests

```bash
python3 scripts/tests.py    # 28 unit tests
```

## Configuration

Edit `scripts/config.json`. See `references/configuration.md` for full guide.

**Storage backend** — auto-detected:
- `convexUrl` set → uses Convex (agentMemory API)
- No `convexUrl` → uses local `.cache/agent-facts.json`

**Model presets** — switch LLM/embeddings provider in one flag:

```bash
python3 scripts/unified_recall.py "query" --preset ollama      # Default
python3 scripts/unified_recall.py "query" --preset lmstudio
python3 scripts/unified_recall.py "query" --preset openai
```

**Per-script model override** — in `config.json` → `scriptOverrides`:

```json
"scriptOverrides": {
  "recall":  { "llm": { "model": "gemma3:4b", "apiFormat": "ollama" } },
  "extract": { "llm": { "model": "gemma3:4b", "apiFormat": "ollama" } }
}
```

**Recommended models by RAM:**

| RAM | LLM | Embeddings |
|-----|-----|------------|
| 4 GB | gemma3:1b | nomic-embed-text |
| **8 GB** | **gemma3:4b** ✓ | nomic-embed-text-v2-moe |
| 16+ GB | qwen3.5:27b | nomic-embed-text-v2-moe |

⚠ Avoid Qwen 3.5 for JSON tasks — outputs to "thinking" field instead of response.

## Platform auto-trigger

| Platform | Method |
|----------|--------|
| macOS | LaunchAgent with WatchPaths |
| Linux | systemd timer or cron |
| Windows | Task Scheduler |

See `references/configuration.md` for examples.

## File Structure

```
scripts/
├── unified_recall.py      # Multi-source search + scoring + synthesis
├── extract_facts.py       # Fact extraction + contradiction check + storage
├── auto_ingest.py         # File watcher / scanner pipeline
├── multihop_search.py     # Chained reasoning search
├── decay_search.py        # Time-weighted search
├── knowledge_graph.py     # Entity/relationship graph builder
├── fact_store.py          # Storage abstraction (Convex / local JSON)
├── llm_client.py          # LLM/embedding client (Ollama/LM Studio/OpenAI)
├── selftest.py            # Setup validation
├── tests.py               # Unit tests (28)
└── config.json            # Configuration + presets
references/
└── configuration.md       # Full configuration guide
```
