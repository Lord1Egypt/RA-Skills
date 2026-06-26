# Elite Human Memory — Portable Edition

Portable, Clawhub-ready human-like memory system for LLM agents.

This skill gives agents a structured, selective, and context-aware memory system that feels more human than simple key-value stores. It includes layered memory (working/episodic/semantic), rich metadata, automatic promotion heuristics, conflict detection, and optional semantic search.

Designed to work across platforms without tight coupling to any single agent framework.

## Features

- Layered memory architecture (Working / Episodic / Semantic)
- Rich contextual metadata schema
- Auto-promotion heuristics with user control
- Conflict detection and resolution workflow
- Optional vector/semantic search with graceful fallback
- Platform-agnostic design

## Quick Start

1. Copy the `elite-human-memory` skill into your agent's skills directory.
2. Load the skill in your agent loop or configuration.
3. Implement the storage layout (or configure custom paths).
4. Wire up optional embeddings/vector store if desired.
5. Let the agent follow the behavioral triggers for read/write/maintenance.

See `SKILL.md` for the full specification and behavioral rules.

## Integration Guidance

This skill is intentionally framework-agnostic. Typical integration points:

- **Storage**: Use local filesystem (recommended) or any persistent store.
- **Semantic Search**: Plug in any embedding model + vector DB (Chroma, FAISS, etc.) or skip for pure metadata/keyword mode.
- **Triggers**: Hook the "Auto-read" and "Auto-write" conditions into your agent's context management.
- **Maintenance**: Schedule weekly reviews via cron, agent heartbeat, or manual invocation.

It can run alongside simpler memory tools — use this for rich contextual memory and lighter stores for high-frequency facts.

## Storage Layout

```
memory/
├── daily/
│   └── YYYY-MM-DD.md
├── MEMORY.md
├── conflicts/
└── vectors/          # optional
```

All paths are configurable.

## Version & Status

- Version: 1.0.0 (Portable / Clawhub Compatible)
- Status: Ready for publishing and cross-platform deployment

## License & Contribution

Free to use and adapt. Contributions welcome on Clawhub.

---

*Part of the two-track Elite Human Memory project. Companion Hermes-optimized version available for local high-performance use.*