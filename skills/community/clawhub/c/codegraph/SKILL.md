---
name: code-graph
description: Build and query AST summaries + call graphs for codebases. Use when exploring a project's structure, finding function definitions, tracing call chains, understanding imports, or navigating unfamiliar code. Replaces repeated file reading with cached structural queries. Supports Python and JavaScript/TypeScript.
---

# Code Graph

Analyze project structure via AST parsing instead of reading every file.

## Quick Start

### Build cache (first time or after changes)

```bash
python3 skills/code-graph/scripts/analyze.py <project_dir>
```

Creates `.code-graph.json` in the project root. Takes seconds for most projects.

### Query the cache

```bash
python3 skills/code-graph/scripts/analyze.py <project_dir> --query <command> [args]
```

## Available Queries

| Query | Description |
|---|---|
| `stats` | Project overview: file counts, lines, functions, classes |
| `functions` | List all functions with file + line number |
| `classes` | List all classes with bases, methods, file + line |
| `calls <func>` | What does `func` call? (outgoing edges) |
| `callers <func>` | Who calls `func`? (incoming edges) |
| `file <path>` | Full summary of one file (functions, classes, imports, calls) |
| `imports` | Import graph: file → modules imported |
| `search <pattern>` | Find functions/classes matching pattern |

## Workflow

1. **First encounter with a project**: run the build to create cache
2. **Before reading files**: query `stats` then `search` to find what you need
3. **Before modifying code**: query `callers` to check impact
4. **After modifying code**: rebuild cache with a fresh run (no `--query`)

## Cache Location

- Default: `<project_dir>/.code-graph.json`
- Override: `--output <path>`

## Rebuild

Re-run without `--query` to rebuild. The cache includes a fingerprint for staleness detection.

## Exclude Directories

```bash
python3 skills/code-graph/scripts/analyze.py <project_dir> --exclude vendor --exclude tmp
```

Default excludes: node_modules, .git, __pycache__, .venv, dist, build, .next, coverage
