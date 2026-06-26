<div align="center">

# agentMemo

**Semantic Memory Mesh for AI Agents**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Give your AI agents shared, searchable, decaying memory with RBAC, version history, and a real-time event bus.

**v3.0.0**

</div>

---

## Features

- **Memory CRUD** — Store text memories with namespace isolation, importance scoring, TTL, tags, and metadata
- **Semantic / Keyword / Hybrid Search** — 384-dim embeddings (all-MiniLM-L6-v2) with HNSW indexing, full-text keyword search, and hybrid reciprocal rank fusion
- **Version History** — Every update saves a version. Rollback to any previous version.
- **Tags** — Tag memories and filter search results by tags
- **RBAC** — API key auth via `X-API-Key` header with per-namespace permissions. `AGENTMEMO_ADMIN_KEY` is required — server refuses to start without it
- **Batch API** — Batch create, delete, and search in a single request
- **TTL Auto-Expire** — Background task prunes expired memories every 60 seconds
- **Importance Decay** — `importance * 0.5^(age / half_life)`, auto-pruned below 0.01
- **Import/Export** — Bulk import and export memories as JSON
- **Event Bus** — SSE and WebSocket for real-time agent coordination
- **Health & Metrics** — `/health` and `/metrics` endpoints
- **Gzip Compression** — Text >1KB auto-compressed in database
- **Web Dashboard** — Dark responsive UI with search mode toggle, version history, metrics panel
- **Zero-Dependency Client** — Python client using only stdlib
- **HNSW Index** — Approximate nearest neighbor via hnswlib with startup prewarming
- **Embedding Cache** — LRU cache (4096 entries) for embedding vectors
- **Async DB** — aiosqlite with WAL mode
- **Rate Limiting** — Per-key configurable rate limiting

## Quick Start

```bash
pip install -r requirements.txt
python server.py
```

Open [http://localhost:8790/dashboard](http://localhost:8790/dashboard)

## API Reference

### Memories

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/memories` | Store a memory (with tags) |
| `GET` | `/v1/memories/search` | Search (semantic/keyword/hybrid) |
| `GET` | `/v1/memories/{id}` | Get memory by ID |
| `PUT` | `/v1/memories/{id}` | Update memory (creates version) |
| `DELETE` | `/v1/memories/{id}` | Delete memory |
| `GET` | `/v1/memories/{id}/versions` | Version history |
| `POST` | `/v1/memories/{id}/rollback` | Rollback to version |
| `POST` | `/v1/memories/batch` | Batch create/delete/search |

#### Store Memory

```bash
curl -X POST http://localhost:8790/v1/memories \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "User prefers dark mode",
    "namespace": "preferences",
    "importance": 0.9,
    "tags": ["ui", "user-pref"],
    "ttl_seconds": 604800,
    "metadata": {"source": "onboarding"}
  }'
```

#### Search (with mode)

```bash
# Semantic (default)
curl 'http://localhost:8790/v1/memories/search?q=UI+theme&mode=semantic&limit=5'

# Keyword
curl 'http://localhost:8790/v1/memories/search?q=dark+mode&mode=keyword'

# Hybrid (semantic + keyword fusion)
curl 'http://localhost:8790/v1/memories/search?q=user+preferences&mode=hybrid&tags=ui'
```

#### Update (versioned)

```bash
curl -X PUT http://localhost:8790/v1/memories/{id} \
  -H 'Content-Type: application/json' \
  -d '{"text": "Updated text", "tags": ["ui", "v2"]}'
```

#### Batch

```bash
curl -X POST http://localhost:8790/v1/memories/batch \
  -H 'Content-Type: application/json' \
  -d '{
    "create": [{"text": "Memory 1", "tags": ["batch"]}],
    "delete": [{"id": "uuid"}],
    "search": [{"q": "query", "mode": "hybrid"}]
  }'
```

### Import / Export

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/import` | Import memories |
| `GET` | `/v1/export?namespace=X` | Export memories |

### Events

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/events` | Publish an event |
| `GET` | `/v1/events/stream` | SSE stream |
| `WS` | `/v1/ws?namespace=X` | WebSocket stream |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/metrics` | Server metrics |
| `GET` | `/v1/namespaces` | List namespaces |
| `GET` | `/v1/stats` | Storage stats |
| `GET` | `/dashboard` | Web dashboard |

### API Keys (admin only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/api-keys` | Create scoped key |
| `GET` | `/v1/api-keys` | List keys |
| `DELETE` | `/v1/api-keys/{key}` | Delete key |

## Authentication (RBAC)

Set `AGENTMEMO_ADMIN_KEY` to enable auth:

```bash
export AGENTMEMO_ADMIN_KEY=my-secret-admin-key
python server.py
```

All `/v1/` requests require `X-API-Key` header. Create scoped keys:

```bash
curl -X POST http://localhost:8790/v1/api-keys \
  -H "X-API-Key: my-secret-admin-key" \
  -H "Content-Type: application/json" \
  -d '{"name": "agent-a", "namespaces": ["agent-a", "shared"]}'
```

`AGENTMEMO_ADMIN_KEY` is **required**. The server refuses to start without it — there is no open-access mode.

## Python Client

```python
from client import AgentMemoClient

vault = AgentMemoClient("http://localhost:8790", api_key="your-secret-key")

# Store with tags
vault.store("User prefers dark mode", namespace="prefs", tags=["ui"])

# Search (semantic, keyword, or hybrid)
results = vault.search("dark mode", mode="hybrid", tags=["ui"])

# Update (versioned)
vault.update(memory_id, text="Updated text", tags=["ui", "v2"])

# Version history & rollback
versions = vault.versions(memory_id)
vault.rollback(memory_id, version=1)

# Batch
vault.batch(create=[{"text": "..."}], delete=["id1"], search=[{"q": "..."}])

# Import/Export
vault.export_memories(namespace="prefs")
vault.import_memories([{"text": "...", "namespace": "prefs"}])

# Health & metrics
vault.health()
vault.metrics()
```

## Importance Decay

```
effective_importance = importance * 0.5^(age_hours / half_life_hours)
```

- Default half-life: **168 hours** (1 week)
- Auto-pruned when effective importance drops below **0.01**
- TTL-expired memories pruned every **60 seconds**

## Performance

- **HNSW** — Approximate nearest neighbor via hnswlib (prewarmed on startup)
- **Embedding Cache** — LRU cache with 4096 entries
- **Batch Embedding** — Encode multiple texts in a single call
- **Async DB** — aiosqlite with WAL mode
- **Gzip** — Auto-compress text >1KB in database
- **Rate Limiting** — Per-key sliding window (default 120 req/min)
- **Cursor Pagination** — Efficient large dataset traversal

Run benchmarks:
```bash
python benchmark.py
```

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Agent A    │     │   Agent B    │     │   Agent C    │
│ (namespace)  │     │ (namespace)  │     │ (namespace)  │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       └────────────┬───────┴────────────────────┘
                    │
            ┌───────▼───────┐
            │   agentMemo   │
            │  FastAPI 3.0  │
            ├───────────────┤
            │ HNSW + SQLite │
            │ RBAC + Cache  │
            │ SSE + WS Bus  │
            │ Decay+Rollback│
            └───────────────┘
```

## Configuration

| Env Variable | Default | Description |
|---|---|---|
| `AGENTMEMO_PORT` | `8790` | Server port |
| `AGENTMEMO_DB` | `agentmemo.db` | SQLite database path |
| `AGENTMEMO_ADMIN_KEY` | **required** | Admin key for RBAC auth (server refuses to start without it) |
| `AGENTMEMO_RATE_LIMIT` | `120` | Requests per minute per key |

## Backward Compatibility

agentMemo v3.0.0 is fully backward compatible with the old `AGENTVAULT_*` env vars:

1. **Database**: Old `agentvault.db` still works via `AGENTVAULT_DB` env var fallback.
2. **API**: All `/v1/` endpoints unchanged. Same request/response formats.
3. **Environment Variables**: Both old and new prefixes work. `AGENTMEMO_*` takes priority.
4. **Python Client**: `from client import AgentVaultClient` still works (alias preserved).

### What changed in v3.0.0?
- Project fully renamed to `agentMemo` (service name, README, dashboard, logs)
- Importance decay mechanism verified and tested (configurable half-life)
- Version rollback mechanism verified and tested

### Hindsight vs agentMemo

| Feature | Hindsight | agentMemo |
|---------|-----------|-----------|
| Protocol | MCP native | REST + SSE + WebSocket |
| Storage | PostgreSQL + pgvector | SQLite + hnswlib (zero-dep) |
| Knowledge Graph | ✅ entity traversal | ❌ (planned) |
| Hybrid Search | ❌ | ✅ semantic + keyword + RRF |
| Version History | ❌ | ✅ full rollback |
| Importance Decay | ❌ | ✅ configurable half-life |
| Event Bus | ❌ | ✅ SSE + WebSocket |
| Zero-Dependency Deploy | ❌ requires PostgreSQL | ✅ SQLite only |

## License

MIT
