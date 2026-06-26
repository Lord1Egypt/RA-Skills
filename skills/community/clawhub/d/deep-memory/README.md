# Deep Memory 🧠

> One-click production-grade semantic memory system for AI agents.

## What is this?

A complete memory infrastructure that gives your AI agent:

- **Tiered file storage** — HOT/WARM/COLD Markdown layers
- **Vector search** — Qdrant DB with qwen3-embedding (4096 dims, local/free)
- **Graph relationships** — Neo4j for entity and relationship memory
- **Joint query** — combines vector similarity + graph traversal

## Quick Start

```bash
# Install the skill
openclaw skill install deep-memory

# Run setup (one-time)
python3 ~/.openclaw/workspace/skills/deep-memory/scripts/setup.py
```

## Requirements

- Docker Desktop (running)
- Ollama (`brew install ollama`)
- macOS / Linux

## Architecture

```
User Query
    ↓
Joint Query Engine
    ├── Qdrant (semantic similarity, 4096-dim vectors)
    └── Neo4j  (entity relationships, graph traversal)
         ↓
    Merged & ranked results
```

## Performance

| Layer | Accuracy | Latency |
|-------|----------|---------|
| Keyword (baseline) | ~30% | instant |
| Vector only (Qdrant) | ~70% | 10-30ms |
| Vector + Graph (joint) | ~80% | 20-50ms |

## License

MIT
