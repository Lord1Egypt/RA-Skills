---
name: eidolon-search
description: AI Agent memory search using SQLite FTS5. 90%+ token reduction (10x+) compared to reading full files. Use when the agent needs to search through markdown memory files, daily notes, or any text corpus efficiently. Triggers on memory search, file search, knowledge retrieval, or when context window is limited and full-file reading is too expensive.
---

# Eidolon Search

FTS5-based memory search for AI Agents. Index markdown files once, search with 90%+ token savings.

## Quick Start

### 1. Index memory files (once)

```bash
python3 scripts/build-index.py <memory_dir> <db_path>
```

Example:
```bash
python3 scripts/build-index.py ./memory ./memory.db
```

This creates a SQLite database with FTS5 full-text index of all `.md` files in the directory (recursive).

### 2. Search

```bash
python3 scripts/search.py <query> [limit] [db_path]
```

Example:
```bash
python3 scripts/search.py "Physical AI roadmap" 5
python3 scripts/search.py "project timeline" 10 ./memory.db
```

Default limit: 10. Default db_path: `./memory.db`

Output: matching snippets with file paths and relevance scores.

### 3. Re-index when files change

Run `build-index.py` again. It rebuilds the index from scratch (fast, <1 second for typical workspaces).

## When to Use

- **Memory search**: Find specific information across many daily notes or memory files
- **Token-limited contexts**: When reading all files would exceed context limits
- **Repeated searches**: Index once, search many times
- **Large workspaces**: 10+ markdown files with cumulative size >50KB

## When NOT to Use

- Single small file (<5KB): just read it directly
- Need semantic/meaning-based search: FTS5 is keyword-based only
- See [references/QUALITY.md](references/QUALITY.md) for known limitations

## Search Tips for Agents

FTS5 is keyword-based. Improve results by:

- Use specific terms: "Jetson Orin" not "hardware plans"
- Use OR for synonyms: "car OR vehicle OR automobile"
- Use quotes for phrases: `"Physical AI"`
- Try multiple queries if first attempt returns nothing
- Check file paths in results to read full context when needed

## Benchmarks

- Token savings: 90%+ (measured 93-98.9%)
- Speed: 15x faster (measured 10-20x)
- Details: [references/PERFORMANCE.md](references/PERFORMANCE.md)

Run benchmarks yourself:
```bash
python3 scripts/benchmark-recall.py    # Recall@5, Recall@10
python3 scripts/benchmark-cache.py     # Warm vs cold cache
```

## DB Schema

```sql
CREATE VIRTUAL TABLE memory_fts USING fts5(path, content);
```

Direct SQL access:
```bash
sqlite3 memory.db "SELECT path, snippet(memory_fts, 1, '<b>', '</b>', '...', 32) FROM memory_fts WHERE memory_fts MATCH 'query' ORDER BY rank LIMIT 5;"
```
