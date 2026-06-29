# CodeGraph Architecture

## Pipeline

```
Files → ExtractionOrchestrator (tree-sitter) → DB (nodes/edges/files)
         ↓ ReferenceResolver (imports, name-matching, frameworks)
         ↓ GraphQueryManager / GraphTraverser (callers, callees, impact)
         ↓ ContextBuilder (markdown/JSON)
```

## Modules

- `src/index.ts` — `CodeGraph` class (public API)
- `src/db/` — SQLite + FTS5 (prefer better-sqlite3 native, fallback to WASM)
- `src/extraction/` — tree-sitter parsers + standalone extractors (svelte/vue/liquid/razor)
- `src/resolution/` — import resolution, name matching, framework routes (14 frameworks)
- `src/graph/` — BFS/DFS traversal, impact radius, path finding
- `src/context/` — ContextBuilder + markdown/JSON formatters
- `src/search/` — FTS5 full-text queries
- `src/sync/` — FileWatcher (FSEvents/inotify/RDCW) + debounce
- `src/mcp/` — MCP server (`server-instructions.ts` is the single source of truth for agent tool guidance)
- `src/installer/` — multi-agent installer (8 targets)
- `src/bin/codegraph.ts` — CLI (commander)

## NodeKind (22 types)

file, module, class, struct, interface, trait, protocol, function, method, property, field, variable, constant, enum, enum_member, type_alias, namespace, parameter, import, export, route, component

## EdgeKind (12 types)

contains, calls, imports, exports, extends, implements, references, type_of, returns, instantiates, overrides, decorates

## Explore Budget (Adaptive)

| File Count | explore Calls | Chars/Call | Chars/File |
|------------|---------------|------------|------------|
| <150 | 1 | 13K | 3800 |
| <500 | 1 | 18K | 3800 |
| <5000 | 2 | 24K | 6500 |
| <15000 | 3 | 24K | 7000 |
| ≥15000 | 4-5 | 24K | 7000 |

## Dynamic Dispatch Coverage

Indirect calls missed by static tree-sitter are bridged by synthesizers: callbacks/observers, EventEmitter, React re-render (`setState`→`render`), JSX child (`render`→child component), Django ORM. Synthesized edges marked `provenance:'heuristic'`.

## Auto-sync (Three Layers)

1. Native FS events + 2s debounce (adjustable via `CODEGRAPH_WATCH_DEBOUNCE_MS`)
2. Per-file staleness banner (pending files prefixed with ⚠️)
3. MCP reconnect: `(size, mtime)` + content hash reconciliation

## Internal Docs Index

- `docs/benchmarks/` — A/B tests (answer-directly-vs-explore-agent, call-sequence-analysis, codegraph-ab-matrix)
- `docs/design/` — design docs (adaptive-explore-sizing, callback-edge-synthesis, dynamic-dispatch-coverage-playbook, mixed-ios-and-react-native-bridging, template-markup-parser)
- `docs/SEARCH_QUALITY_LOOP.md` — language validation test suite