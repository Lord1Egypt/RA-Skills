---
name: AKY-ES
description: "Local Elasticsearch 8.17 (free/open) — store, search, index and retrieve persistent data at localhost:9200. No cloud costs, zero config."
homepage: https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "files": ["/home/node/.openclaw/workspace/es_tools.py"] },
        "install":
          [
            {
              "id": "venv",
              "kind": "pip",
              "package": "elasticsearch>=9.4",
            },
          ],
      },
  }
---

# ES Tools Skill — Local Elasticsearch

Store, search, and manage data using a persistent **Elasticsearch 8.17** instance running at `http://localhost:9200`. No API key, no cloud costs.

Scripts available in workspace:
- `python3 es_tools.py` — full-featured Python client (preferred)
- `bash es_tools.sh` — lightweight Bash/curl client
- `bash es-manager.sh start|stop|status` — manage the ES process

---

## When to Use

✅ **USE this skill when:**

- "Save this / remember this" → index a document for later search
- "Search my notes / find that thing I saved" → full-text search across stored data
- "Store this analysis / report / document" → persistent document storage
- "Batch import these records" → bulk JSONL import
- "Count / list what I have" → index management & stats
- Any task that needs **structured, searchable long-term memory**

❌ **DON'T use this skill when:**

- Transient data that doesn't need search → use a simple file
- Large binary files (>10MB each) → use object storage
- Complex relational queries with joins → use a SQL database
- The local ES instance is stopped / not available → check with `bash es-manager.sh status`

---

## Quick Reference

### Connection

ES auto-detects: `localhost:9200` takes priority, falls back to Elastic Cloud if unreachable.

```bash
# Python (preferred)
python3 /home/node/.openclaw/workspace/es_tools.py status

# Bash fallback
bash /home/node/.openclaw/workspace/es_tools.sh status
```

### ES Service Management

```bash
bash /home/node/.openclaw/workspace/es-manager.sh status   # check if running
bash /home/node/.openclaw/workspace/es-manager.sh start    # start (waits for ready)
bash /home/node/.openclaw/workspace/es-manager.sh stop     # graceful stop
bash /home/node/.openclaw/workspace/es-manager.sh restart  # restart
```

A cron job keeps ES alive (checks every 5 min). Data persists in `es-data/`.

---

## Commands

All commands below use the Python script. Bash equivalent works the same — just replace `python3 es_tools.py` with `bash es_tools.sh`.

### Status & Health

```bash
python3 es_tools.py status           # cluster info (name, version)
python3 es_tools.py indices           # list all indexes
python3 es_tools.py indices "logs-*"  # list matching a pattern
python3 es_tools.py cat nodes         # cat API (nodes, shards, etc.)
```

### Index Management

```bash
python3 es_tools.py create my_index                           # create index
python3 es_tools.py create my_index '{"mappings":{...}}'      # create with mapping
python3 es_tools.py mapping my_index                          # view mapping
python3 es_tools.py delete my_index                           # ⚠️ delete index
python3 es_tools.py exists my_index                           # check if exists
python3 es_tools.py count my_index                            # document count
```

### CRUD — Documents

```bash
# Create / Update (immediately searchable via refresh=wait_for)
python3 es_tools.py put my_index 1 '{"title":"Hello","tags":["demo"],"count":42}'

# Read
python3 es_tools.py get my_index 1

# Delete
python3 es_tools.py del my_index 1
```

### Search

```bash
# Match all
python3 es_tools.py search my_index '{"query":{"match_all":{}}}'

# Full-text search
python3 es_tools.py search my_index '{"query":{"match":{"title":"hello"}}}'

# Range query
python3 es_tools.py search my_index '{"query":{"range":{"count":{"gte":10}}}}'

# Multi-condition (bool)
python3 es_tools.py search my_index '{"query":{"bool":{"must":[{"match":{"title":"hello"}},{"range":{"count":{"gte":10}}}]}}}'

# Aggregation
python3 es_tools.py search my_index '{"aggs":{"avg_count":{"avg":{"field":"count"}}}}'

# Search from file (for complex queries)
python3 es_tools.py search my_index /path/to/query.json
```

### Bulk Import

For importing many documents at once, prepare a **JSONL file** (one JSON document per line):

```bash
# Example: prepare data
echo '{"name":"商品A","price":100,"stock":50}' > data.jsonl
echo '{"name":"商品B","price":200,"stock":30}' >> data.jsonl

# Import
python3 es_tools.py bulk my_index data.jsonl
```

### Input from File

Any command that accepts JSON can also read from a file:

```bash
python3 es_tools.py put my_index 1 data.json       # read doc from file
python3 es_tools.py search my_index query.json     # read query from file
python3 es_tools.py create my_index mapping.json   # read mapping from file
```

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `ES_URL` | ES endpoint | Auto-detect: local > cloud |
| `ES_API_KEY` | API key (cloud) | — |
| `ES_USER` | Basic auth user (cloud) | — |
| `ES_PASS` | Basic auth password (cloud) | — |
| `AUTH_MODE` | `api_key` or `basic` | `api_key` |

---

## Practical Patterns

### Use ES as Long-Term Memory

```python
# Save a conversation note
python3 es_tools.py put memory $(date +%s) \
  '{"type":"note","content":"阿凯的商铺租赁案关键事实：...","date":"2026-06-27"}'

# Later: search all notes
python3 es_tools.py search memory '{"query":{"match":{"content":"商铺"}}}'
```

### Use ES to Store Skill Outputs

After running any analysis skill (legal, report, public opinion, etc.):

```bash
python3 es_tools.py put skill_outputs $(date +%s) \
  '{"skill":"legal-analysis","case":"商铺租赁","summary":"...","timestamp":"2026-06-27T06:59"}'
```

### Index Document Library

Create indexes by category and use mapping to define field types:

```bash
python3 es_tools.py create contracts \
  '{"mappings":{"properties":{"title":{"type":"text"},"party":{"type":"keyword"},"amount":{"type":"long"},"date":{"type":"date"}}}}}'

python3 es_tools.py put contracts 1 \
  '{"title":"商铺租赁合同","party":"武汉双联创和","amount":6903,"date":"2014-06-17"}'
```

---

## Notes

- **Local ES uses ~1GB RAM.** If resources are tight, stop it: `bash es-manager.sh stop`.
- **Data persists** in `es-data/` across restarts.
- **Cron job checks every 5 min** and auto-restarts if ES goes down.
- ES 8.17 comes with bundled JDK; no external Java dependency.
- Elastic License (Basic tier) — free for development and production use.
