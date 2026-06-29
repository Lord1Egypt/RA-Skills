---
name: codegraph-tool
description: CodeGraph — Pre-indexed code knowledge graph tool. Provides semantic code intelligence for Claude Code, Cursor, Codex, Gemini, OpenCode, Hermes, Antigravity, Kiro and other AI agents. 
---

# CodeGraph Tool

Local-first code intelligence tool. tree-sitter parsing → SQLite (FTS5) storage → MCP exposes knowledge graph. 

##  Use Cases

Use when users need to install CodeGraph, initialize code graph, index projects, understand code structure, trace call chains, evaluate change impact.

## Installation

```bash
npx @colbymchenry/codegraph          # Recommended: one-click install + auto-configure Agent
curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh  # No Node required
npm i -g @colbymchenry/codegraph     # npm
```

Non-interactive: `codegraph install --yes [--target=claude,cursor] [--location=local]`

## Project Initialization

```bash
cd your-project
codegraph init -i    # Create .codegraph/ + build index
codegraph index      # Full index (or rebuild: --force)
codegraph sync       # Incremental sync (changed files only)
codegraph status     # Check status
```

## MCP Tools (8)

> Tool selection guide is automatically sent to Agent in MCP `initialize` response.

| Intent | Tool | Key Parameters |
|--------|------|----------------|
| **Almost any question** — architecture, flow, bug, investigation | `codegraph_explore` ⭐ | `query` (natural language or symbol names) |
| Locate symbol by name | `codegraph_search` | `query`, `kind`, `limit` |
| Call chain | `codegraph_callers` / `codegraph_callees` | `symbol`, `limit` |
| Change impact | `codegraph_impact` | `symbol`, `depth` |
| Single symbol full source / overload disambiguation | `codegraph_node` | `symbol`, `includeCode`, `file`, `line` |
| File structure | `codegraph_files` | — |
| Index health | `codegraph_status` | — |

### Core Principles

- **`codegraph_explore` is the PRIMARY tool** — call it first, usually the only call needed. Returns relevant symbol source code (grouped by file), with line numbers.
- **Answer directly, don't delegate to sub-Agent for file exploration** — CodeGraph IS the pre-built index, grep/read loops are redundant work.
- **One `explore` > `search` + `node` chained calls**.

### Anti-patterns

❌ Don't use grep to verify codegraph results (AST is more accurate than grep)  
❌ Don't chain `search` + `node` to understand an area (one `explore` does it)  
❌ Don't loop `node` over multiple symbols (one `explore` returns all)  
⚠️ Check staleness banner after edits — pending files need direct Read

## Auto-sync

Three-layer protection: ① Native FS events + 2s debounce auto-sync ② Per-file staleness banner (pending files prefixed with ⚠️) ③ Auto-reconciliation on MCP reconnect.  
Manual sync only needed in sandbox (`CODEGRAPH_NO_DAEMON=1`) or CI pre-flight.

## CLI Queries

```bash
codegraph query <symbol> [--kind class] [--limit 10] [--json]
codegraph callers <symbol> [--limit 20] [--json]
codegraph callees <symbol> [--limit 20] [--json]
codegraph impact <symbol> [--depth 2] [--json]
codegraph context "<task>" [--max-nodes 20]
codegraph affected <files...> [--stdin] [--depth 5] [--filter "e2e/*"] [--quiet]
```

## Configuration

**Zero-config** — no config files. Auto-excludes `node_modules`/`vendor`/`dist`/`build`/`target`/`.venv`/`Pods`/`.next` + `.gitignore` entries + >1MB files. Exclude more: add to `.gitignore`; bring back: `!vendor/`.

Environment variables: `CODEGRAPH_WATCH_DEBOUNCE_MS`(2000) `CODEGRAPH_NO_DAEMON` `CODEGRAPH_EXPLORE_LINENUMS`(1) `CODEGRAPH_ADAPTIVE_EXPLORE`(1)

## Supported Languages (21)

TS/JS/Python/Go/Rust/Java/C#/PHP/Ruby/C/C++/Swift/Kotlin/Scala/Dart/Svelte/Vue/Liquid/Pascal-Delphi/Lua/Luau

## Framework Routes (14)

Django/Flask/FastAPI/Express/NestJS/Laravel/Drupal/Rails/Spring/Gin-chi-gorilla-mux/Axum-actix-Rocket/ASP.NET/Vapor/ReactRouter-SvelteKit — auto-recognize route files and generate `route` nodes.

## Cross-language Bridging

Swift↔ObjC / RN legacy bridge / TurboModules / RN events / Expo Modules / Fabric-Paper views. Synthesized edges marked `provenance:'heuristic'`.

## Uninstall

```bash
codegraph uninstall    # Remove MCP config
codegraph uninit       # Delete .codegraph/
```

## References

- [references/configuration.md](references/configuration.md) — Full CLI commands, manual Agent config, TypeScript API
- [references/architecture.md](references/architecture.md) — Architecture pipeline, NodeKind/EdgeKind, explore budget