# Ghostclaw

> "I see the flow between functions. I sense the weight of dependencies. I know when a module is uneasy."

Ghostclaw is an OpenClaw skill that provides an **architectural code review assistant** focused on system-level flow, cohesion, and tech stack best practices.

## Prerequisites

Before installing Ghostclaw, you must have [OpenClaw](https://openclaw.ai/) and [ClawHub](https://clawhub.ai/) installed on your system.

## Quick Start (Installation)

Ghostclaw can be installed via **npm** (recommended for OpenClaw users) or **pip** (for Python environments). Choose the method that fits your workflow.

### via NPM (Recommended for OpenClaw)

Install globally from the npm registry:

```bash
npm install -g ghostclaw
```

Or run directly with npx:

```bash
npx ghostclaw /path/to/repo
```

You can also add it as an OpenClaw skill:

```bash
npx skills add Ev3lynx727/ghostclaw
```

### via ClawHub

Install using ClawHub (skill-only manager):

```bash
clawhub install skill ghostclaw
```

### via PyPI (Python)

Install using pip (includes both CLI and library):

```bash
# Latest stable release
pip install ghostclaw

# Or install the pre-release beta
pip install --pre ghostclaw

# For development, install from source
git clone https://github.com/Ev3lynx727/ghostclaw.git
cd ghostclaw
pip install -e .
```

For a detailed integration guide, see **[GUIDE.md](docs/GUIDE.md)**.

## Usage

### Run a review on a codebase

```bash
# If installed globally via NPM or Python
ghostclaw /path/to/your/repo

# If running from source
python3 src/ghostclaw/cli/ghostclaw.py /path/to/your/repo
```

### Delta-Context Analysis (PR Reviews)

Ghostclaw supports **delta-context mode** for analyzing only the code changes (git diff) instead of the entire codebase. This is perfect for:

- **CI/CD integration**: Fast PR checks without scanning the whole repo
- **Focused feedback**: Architectural review specifically on the changed files
- **Token efficiency**: Smaller prompts, lower AI costs
- **Drift detection**: Compare current changes against a previous baseline

#### Usage

```bash
# Analyze changes against HEAD~1 (default)
ghostclaw /path/to/repo --delta

# Compare against a specific branch, tag, or commit
ghostclaw /path/to/repo --delta --base origin/main
ghostclaw /path/to/repo --delta --base v1.2.3

# In CI (e.g., GitHub Actions)
ghostclaw . --delta --base ${{ github.event.pull_request.base.sha }} --json

# Combine with AI synthesis
ghostclaw . --delta --base HEAD~5 --use-ai --dry-run  # preview prompt
```

The delta report will be saved as `ARCHITECTURE-DELTA-<timestamp>.md` in `.ghostclaw/`.

For more examples and CI integration, see `docs/examples/delta-analysis.md`.

#### How It Works

1. **Diff extraction**: Ghostclaw runs `git diff` between the current working tree and the specified `--base` reference.
2. **Changed files only**: Only files modified in the diff are analyzed (filtered by stack extensions).
3. **Base context**: If a previous Ghostclaw report exists in `.ghostclaw/reports/`, it is loaded and used as baseline for comparing architectural drift.
4. **Delta prompt**: The AI prompt includes `<base_context>`, `<diff>`, and `<current_state>` sections to enable targeted synthesis.

#### Delta Summary

Use `--delta-summary` to print diff statistics (files changed, insertions, deletions) to stderr after the analysis completes. Useful for CI logs and quick metrics.

#### Benefits over Full Scan

- **Faster** (fewer files to analyze)
- **Cheaper** (fewer tokens in AI prompt)
- **More relevant** (focuses on what actually changed)

#### Base Report Auto-Discovery

When using `--delta`, Ghostclaw automatically loads the most recent report from `.ghostclaw/storage/reports/` to serve as the base context. No manual `--base-report` flag needed. If no base report exists, the delta prompt proceeds with just the diff and current metrics.

**Precise matching**: When `--base` is a specific commit SHA, Ghostclaw tries to find a report with matching `metadata.vcs.commit`. If not found, it falls back to the latest report (with a warning).

### Background Monitoring (Cron)

Set up your repositories in a `repos.txt` file and add the native watcher binary to your cron jobs:

```bash
0 9 * * * ghostclaw-watcher /path/to/repos.txt
```

## What Ghostclaw Does

- **Vibe Score**: Assigns a 0-100 score representing architectural health.
- **Architectural Ghosts**: Detects code smells like "AuthGhost" or "ControllerGhost".
- **Refactor Blueprints**: Suggests high-level plans before code changes.
- **Sub-agent Mode**: Can be spawned via `openclaw sessions_spawn --agentId ghostclaw`.
- **Watcher Mode**: Monitors repositories and opens PRs with improvements.

## Files

```text
ghostclaw/
├── package.json — Package metadata for NPM and Skills CLI
├── SKILL.md — OpenClaw skill definition
├── docs/ — Documentation for Ghostclaw
├── scripts/ — Systemd service setup configuration
└── src/ghostclaw/ — Main Python package source
    ├── core/ — Core analysis orchestration
    ├── ghostclaw_mcp/ — Model Context Protocol (MCP) server
    ├── lib/ — Utilities (GitHub, Cache, Notify)
    ├── stacks/ — Stack-specific analysis strategies
    ├── cli/ — CLI implementation
    └── references/ — Architectural patterns
```

## Integrations

### Advanced Integrations (Phase 2)

Ghostclaw now supports several advanced extensions and optional dependencies.

#### MCP Server

Ghostclaw can now be used as an MCP server for Claude, Cursor, and other AI tools.

To install with MCP support:

```bash
pip install ghostclaw[mcp]
```

To run the MCP server:

```bash
ghostclaw-mcp
```

**Exposed Tools:**

- `ghostclaw_analyze`: Full vibe analysis.
- `ghostclaw_get_ghosts`: Architectural smells only.
- `ghostclaw_refactor_plan`: Automated blueprint generation.

##### Agent-Facing Memory Tools

Agents can query past analysis runs to track architectural health over time:

- `ghostclaw_memory_search(query, repo_path?, stack?, min_score?, max_score?, limit=10)` — Search historical issues and ghosts.
- `ghostclaw_memory_list_runs(repo_path?, limit=20)` — List recent runs.
- `ghostclaw_memory_get_run(run_id, repo_path?)` — Retrieve full report.
- `ghostclaw_memory_diff_runs(run_id_a, run_id_b, repo_path?)` — Compare two runs.
- `ghostclaw_knowledge_graph(repo_path?, limit=50)` — Aggregate trends and recurring issues.

Example (MCP JSON-RPC):

```json
{
  "tool": "ghostclaw_memory_search",
  "params": { "query": "Large file", "limit": 5 }
}
```

Results include `matched_snippets` showing where the term appeared.

#### Advanced Context & AST Indexing

By utilizing the `ai-codeindex` engine, Ghostclaw can extract full structural syntax trees and build extensive call graphs.

To install:

```bash
pip install ghostclaw[ai-codeindex]
```

#### Dead Code & Clone Detection

Ghostclaw can offload syntax-level checks for dead code and near-identical code blocks to `pyscn`.

To install:

```bash
pip install ghostclaw[pyscn]
```

#### Plugin Management CLI (v0.1.6)

Ghostclaw features a native plugin ecosystem. You can manage built-in and external adapters via the CLI:

```bash
# List all active adapters
ghostclaw plugins list

# Install an external adapter from a local folder
ghostclaw plugins add ./path/to/custom_adapter

# Scaffold a new developer template
ghostclaw plugins scaffold my-new-adapter
```

### Systemd Service (Phase 3)

For a persistent local MCP service, you can use the provided setup script which installs a `systemd` unit on Linux:

```bash
# Run from the source repository directory
npm run install-service
```

## Supported Stacks

- Node.js / React / TypeScript
- Python (Django, FastAPI)
- Go (Basic)

## Performance & Best Practices

Ghostclaw is designed to be fast out of the box, but for large repositories or specific use cases, consider these tips:

### Parallel Processing (Default)
- Parallel file scanning is **enabled by default** and highly recommended.
- The `--no-parallel` flag exists only for debugging; it causes a ~300× slowdown.
- If you accidentally use `--no-parallel` on a large repo (>5000 files), Ghostclaw will automatically re-enable parallel mode to prevent timeouts.

### Caching
- Ghostclaw caches analysis results to speed up repeated runs.
- Default cache TTL is 7 days. Use `--cache-ttl` to adjust.
- To disable caching (e.g., for CI), use `--no-cache`.
- Cache statistics can be shown with `--cache-stats`.

### Benchmarking
- Use `--benchmark` to see timing breakdown per analysis phase.
- This helps identify bottlenecks (e.g., file scanning, AI synthesis).

### Large Repositories
- For repos with >10k files, expect analysis to take several seconds even with parallelism (disk I/O bound).
- Consider increasing `--concurrency-limit` if you have a fast SSD and abundant CPU cores (default is 32).
- Use `--no-write-report` if you only need console output and want to reduce disk I/O.

### AI Synthesis
- AI synthesis (`--use-ai`) adds network latency (5-30s depending on provider and model).
- Use `--dry-run` to estimate token count without making API calls.
- Cache hits skip AI synthesis entirely if the code hasn't changed significantly.

### Troubleshooting Timeouts
- Ensure `parallel_enabled: true` in `~/.ghostclaw/ghostclaw.json`.
- Avoid `--no-parallel` on any non-trivial repository.
- For extremely large repos, consider analyzing a specific subdirectory instead of the entire codebase.

### Storage & Memory Backend
- Ghostclaw stores analysis results and history in `.ghostclaw/storage/` (reports, cache, SQLite DB).
- **Automatic migration**: If you have legacy `.ghostclaw/reports/` or `.ghostclaw/cache/` from older versions, they will be automatically moved to the new storage layout on first run.
- **QMD backend** (production-ready as of v0.2.1-beta): Use `--use-qmd` or set `use_qmd: true` in config for a high-performance alternative storage with AI-Buff optimizations (requires `ghostclaw[qmd]`).
  - AI-Buff includes: embedding cache, search cache, query planning, prefetching, auto-migration for legacy data, optional IVF-PQ index, adaptive alpha tuning, and result diversity.
- MCP tools (`ghostclaw_mcp`) automatically detect and use the configured backend.

### Configuration File
- Config files support **JSON5** format (comments, trailing commas) if the `json5` package is installed.
- Global config: `~/.ghostclaw/ghostclaw.json`
- Project config: `<repo>/.ghostclaw/ghostclaw.json`
- Run `ghostclaw init` (or `python -m ghostclaw.cli.services.ConfigService.init_project`) to scaffold a local config with all options.

## License

MIT
