# Architecture

Ghostclaw is designed as a modular, async pipeline. Key components:

## GhostAgent (`core/agent.py`)

The orchestrator. Manages the analysis lifecycle:
- Detect stack
- Create `CodebaseAnalyzer`
- Run analysis and capture report
- Optionally invoke LLM for synthesis
- Caching and benchmark timing

## CodebaseAnalyzer (`core/analyzer.py`)

Handles scanning and metrics:
- Finds files (via `detector.find_files` or `find_files_parallel`)
- Computes base metrics with `compute_metrics`
- Dispatches to metric adapters through `PluginRegistry`
- Aggregates results into an `ArchitectureReport`

## PluginRegistry (`core/adapters/registry.py`)

Manages metric adapters:
- Discovers internal plugins (e.g., PySCN, AI‑CodeIndex)
- Loads external plugins from `.ghostclaw/plugins/`
- Supports plugin enable/disable via config
- Version compatibility checks (min/max Ghostclaw)
- Runs adapters concurrently and collects errors

## LLMClient (`core/llm_client.py`)

Unified interface for AI providers (OpenRouter/OpenAI, Anthropic):
- Supports analysis generation (one‑shot) and streaming
- Implements exponential backoff retry for transient failures
- Respects token budgets and dry‑run mode

## Cache (`core/cache.py`)

Optional on‑disk cache with TTL and gzip compression to speed up repeated runs on unchanged repos.

## Config (`core/config.py`)

Central configuration via pydantic. Sources: CLI arguments, environment variables, local/global JSON files. Precedence: CLI > env > local > global.

## CLI (`cli/ghostclaw.py`)

Argparse command line interface. Primary command: `analyze`. Supports flags for caching, parallelism, LLM, plugins, reliability (`--strict`), observability (`--benchmark`, `--verbose`), and PR creation.

## Event System

Pluggy is used as the plugin manager; hooks like `ghost_analyze` allow adapters to contribute metrics. Plan for richer agent event callbacks (progress, streaming) exists.

---

This architecture emphasizes separation of concerns, testability, and extensibility.
