---
name: codebase-search
description: "Build a persistent semantic vector index over a Python codebase and search it with natural language. Use when an agent needs to find relevant classes, functions, or modules by meaning rather than exact name — e.g. 'find all classes that handle token payments', 'where is rate limiting implemented?', 'which functions process webhook events?'. Also use when setting up codebase-search for the first time on a new repo, rebuilding a stale index, or integrating semantic search into an agentic coding workflow. NOT for exact-string grep (use exec+grep), single-file analysis, or non-Python codebases."
---

# Codebase Search

Builds a persistent ChromaDB vector index over Python source files and enables semantic search with natural language queries.

## Quick Start

### 1. Install the scripts

Copy `scripts/code_chunker.py` and `scripts/code_index.py` into your project. They have no dependencies beyond `chromadb` (install with `pip install chromadb`).

### 2. Build the index

```python
import asyncio
from code_index import CodebaseIndex

index = CodebaseIndex(repo_root="/path/to/repo")
count = asyncio.run(index.build())
print(f"Indexed {count} symbols")
```

The index persists to `{repo_root}/.codebase_index/` and survives restarts. Subsequent calls to `build()` are fast — only new/changed files are indexed.

### 3. Search

```python
results = asyncio.run(index.search("token payment handling", top_k=5))
for r in results:
    print(f"[{r.score:.2f}] {r.symbol_name} ({r.symbol_type}) — {r.filepath}:{r.start_line}")
```

## Convenience API (when integrated into a project)

If `code_chunker.py` and `code_index.py` are in the project as a module, use the singleton helper:

```python
from prsm.compute.nwtn.corpus import search_codebase

results = await search_codebase("circuit breaker", top_k=3)
```

## Key Options

| Parameter | Default | Description |
|---|---|---|
| `top_k` | 5 | Number of results to return |
| `symbol_type` | None | Filter to `"class"` or `"function"` |
| `force_rebuild` | False | Wipe and rebuild entire index |
| `exclude_patterns` | see below | Directories to skip |

Default excludes: `__pycache__`, `.venv`, `migrations`, `tests`, `scripts`, `.git`, `node_modules`, `.codebase_index`

## How It Works

1. **Chunking** — `CodeChunker` uses Python's `ast` module to extract every top-level class and function from each `.py` file. Captures name, type, docstring, line numbers, and source.
2. **Indexing** — ChromaDB stores each chunk as a document: `"{symbol_name}: {docstring or first 300 chars of source}"`. Uses ChromaDB's default embedding function (no API key needed).
3. **Search** — Cosine similarity query returns ranked `SearchResult` objects with filepath, symbol name, line numbers, docstring, and relevance score.

## .gitignore

Always add `.codebase_index/` to `.gitignore` — it's a local artifact, not source code.

## Reference

See `references/integration.md` for integration patterns, including how to wire semantic search into sub-agent delegation prompts.
