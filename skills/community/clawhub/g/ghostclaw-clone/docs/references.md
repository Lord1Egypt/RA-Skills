# Plugin Source Code Reference

This document provides quick links to the source code of Ghostclaw's core components for developers who want to extend or understand the system.

## Core Adapters (Code Quality Plugins)

Located in `src/ghostclaw/core/adapters/` — these are the architectural analysis engines.

| Adapter | Source | Purpose |
|---------|--------|---------|
| **Base** | `adapters/base.py` | Abstract base classes (`BaseAdapter`, `BaseStackAnalyzer`) |
| **Complexity** | `adapters/complexity.py` | Cyclomatic complexity, nesting depth |
| **Duplication** | `adapters/duplication.py` | Code clone detection |
| **Metrics** | `adapters/metrics.py` | Core metric collection (lines, files, etc.) |
| **Modularity** | `adapters/modularity.py` | Coupling & cohesion metrics |
| **Psychological Safety** | `adapters/psych_safety.py` | Team health indicators (experimental) |
| **Registry** | `adapters/registry.py` | Plugin discovery & lifecycle |

---

## CLI Commands

Located in `src/ghostclaw/cli/commands/`.

| Command | Source | Description |
|---------|--------|-------------|
| **analyze** | `commands/analyze/` | Main analysis orchestrator |
| **bridge** | `commands/bridge.py` | JSON-RPC 2.0 bridge server |
| **debug** | `commands/debug.py` | Interactive debugger (dev only) |
| **doctor** | `commands/doctor.py` | Environment diagnostics |
| **init** | `commands/init.py` | Project config scaffolder |
| **memory-stats** | `commands/memory_stats.py` | QMD store statistics |
| **plugins** | `commands/plugins/` | Plugin management subcommands |
| **qmd-migrate** | `commands/qmd_migrate.py` | Migration status & control |
| **test** | `commands/test.py` | Test runner |
| **update** | `commands/update.py` | Self-update |

---

## MCP Tools (Model Context Protocol)

Located in `src/ghostclaw_mcp/`. These expose Ghostclaw functionality to AI assistants.

| Tool | Source | Description |
|------|--------|-------------|
| **ghostclaw_analyze** | `server.py` | Run analysis and return structured report |
| **ghostclaw_get_ghosts** | `server.py` | Retrieve architectural ghosts from latest run |
| **ghostclaw_memory_search** | `server.py` | Search analysis history |
| **ghostclaw_memory_get_run** | `server.py` | Fetch a specific analysis run |
| **ghostclaw_memory_list_runs** | `server.py` | List recent runs |
| **ghostclaw_memory_diff_runs** | `server.py` | Compare two analysis runs |
| **ghostclaw_knowledge_graph** | `server.py` | Aggregate trends across runs |

---

## Storage Backends

| Component | Source | Notes |
|-----------|--------|-------|
| **QMD Store** | `core/qmd_store.py` | Hybrid BM25+vector store (SQLite + LanceDB) |
| **Vector Store** | `core/vector_store/` | LanceDB integration, IVF-PQ indexing |
| **Migration** | `core/migration.py` | `EmbeddingBackfillManager` for legacy data |
| **Prefetch** | `core/prefetch.py` | Async-native preloading strategies |

---

## Services (High-Level Orchestration)

Located in `src/ghostclaw/cli/services/`.

| Service | Source | Purpose |
|---------|--------|---------|
| **AnalyzerService** | `services/analyzer.py` | Analysis pipeline, events, streaming |
| **PRService** | `services/pr.py` | GitHub PR creation |
| **PluginService** | `services/plugin.py` | Plugin management |
| **ConfigService** | `services/config.py` | Config I/O, validation |

---

## Skill Entry Point

- **OpenClaw Skill** — `skill.py` (at repo root) — Defines the `ghostclaw` skill metadata and OpenClaw integration.

---

## Configuration & Core

| Module | Source | Purpose |
|--------|--------|---------|
| **Config** | `core/config.py` | `GhostclawConfig` with all settings |
| **Cache** | `core/cache.py` | Local file-based caching |
| **Agent** | `core/agent.py` | GhostAgent with event system |
| **Formatters** | `cli/formatters.py` | Output formatters (Markdown, Terminal, JSON) |
| **Commander** | `cli/commander.py` | CLI command discovery & execution |

---

## Tests (for Reference)

- QMD Store: `tests/unit/test_qmd_store.py`
- QMD Adapter: `tests/unit/test_qmd_adapter.py`
- BM25: `tests/unit/test_qmd_bm25.py`
- Vector Store: `tests/unit/test_vector_store.py`
- Migration: `tests/unit/test_migration.py` (if present)
- MCP: `tests/unit/test_mcp.py`

---

## Notes

- All paths are relative to the repository root.
- Plugin adapters live under `core/adapters/` and are auto-discovered via entry points (`pyproject.toml`).
- For plugin development, see `PLUGINS_GUIDE.md` and `COMMAND_DEVELOPMENT.md`.
