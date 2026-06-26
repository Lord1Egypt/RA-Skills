# 🧠 Agent Memory Tools

Multi-source persistent memory for AI agents. Runs 100% local via [Ollama](https://ollama.com) — no API keys, no cloud dependency, zero cost.

## How it works

```
Question
  │
  ▼
unified_recall.py ──── fan-out (parallel) ────┐
  │                                            │
  ├─→ Fact store     (extracted facts, dedup)  │
  ├─→ Embeddings     (semantic search, nomic)  │
  ├─→ BM25           (keyword match, QMD)      │
  └─→ Knowledge graph (entity traversal)       │
                                               ▼
                                         Merge + Dedup
                                               │
                                         Multi-signal Score
                                         (relevance × recency × source weight)
                                               │
                                         LLM Rerank (gemma3)
                                               │
                                         Synthesize answer
                                         with source citations
```

Each layer adds a different recall strength — embeddings catch semantic similarity, BM25 catches exact terms, the graph catches relationships, and the fact store catches previously validated knowledge. Together they cover blind spots that any single method would miss.

## Quick start

```bash
# 1. Install
bash setup.sh

# 2. Search your workspace
python3 scripts/unified_recall.py "What happened last week?"

# 3. Extract facts from text
python3 scripts/extract_facts.py "Meeting notes..." --store

# 4. Auto-ingest file changes
python3 scripts/auto_ingest.py --scan
```

**Requirements:** Python 3.9+, Ollama, ~2GB disk (for models).

## Key features

- **Multi-hop reasoning** — chains searches with LLM synthesis for complex questions
- **Contradiction detection** — blocks facts that contradict existing knowledge (local LLM, 0€)
- **Temporal decay** — recent facts score higher, errors/knowledge protected from decay
- **Auto-ingestion** — watch workspace for .md changes, extract + store automatically
- **Knowledge graph** — entity/relationship graph built from workspace files
- **Cross-platform** — macOS, Linux, Windows (polling watcher)
- **Flexible storage** — local JSON (default) or Convex cloud (optional)
- **Model presets** — Ollama, LM Studio, OpenAI, OpenRouter — switch with `--preset`

## As an OpenClaw Skill

```bash
clawhub install agent-memory-tools
```

See [SKILL.md](SKILL.md) for agent integration details.

## Configuration

See [references/configuration.md](references/configuration.md) for the full guide, including:
- Model recommendations by RAM (4GB → 32GB+)
- Per-script model overrides
- Platform auto-trigger setup (LaunchAgent, systemd, Task Scheduler)
- Convex cloud backend setup

## Benchmark

10-question recall benchmark on synthetic workspace:

| Metric | Score |
|--------|-------|
| Precision | 96.7% |
| Questions OK | 10/10 |
| Backend | Local JSON |

Run it yourself: `python3 scripts/benchmark.py --verbose`

## Tests

```bash
python3 scripts/tests.py    # 28 unit tests
```

## License

MIT

---

Built by [Primo Studio](https://github.com/Primo-Studio) 🇬🇫
