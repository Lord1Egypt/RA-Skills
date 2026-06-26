---
name: fts5-session-search
version: 1.0.0
description: "Full-text search across all OpenClaw session logs using SQLite FTS5. Instant keyword search, topic queries, time-range filtering, and statistics."
license: MIT
tags: [search, fts5, full-text, session-log, sqlite, indexing, retrieval]
source: el-rudo-larios/fts5-search
trigger: "search session logs full text keyword find conversation"
metadata:
  openclaw:
    emoji: "🔍"
---

# FTS5 Search — Full-Text Search for Session Logs

Index and search all your OpenClaw session logs using SQLite FTS5. Find any conversation, topic, or keyword in milliseconds.

## Quick Start

```python
from search import SearchEngine

engine = SearchEngine(db_path="search.db")

# Index all sessions
engine.index_all(sessions_dir="/path/to/sessions")

# Search
results = engine.search("supervision layer")
# → [<SessionMatch score=0.92 session="2026-05-22-security">]

# Search by topic
results = engine.search("security audit", scope="topic")

# Time range
results = engine.search("deploy", after="2026-05-01", before="2026-05-22")
```

## Features

- **Full-text search** across all session logs
- **FTS5 tokenizer** with ranking and relevance scoring
- **Topic search** — search within topic summaries
- **Time-range queries** — find conversations by date
- **Statistics** — term frequency, session count, index size
- **Incremental indexing** — only new/changed sessions are reindexed
- **Sub-12ms query times** across 4000+ messages

## Performance

| Metric | Value |
|--------|-------|
| Sessions indexed | 115+ |
| Messages searchable | 4,126+ |
| Query time | < 12ms |
| Index size | < 5MB |

## License

MIT
