---
name: agentmemo
description: >
  agentMemo is a Semantic Memory Mesh server for AI agents. Use this skill when
  you need to store, search, or retrieve agent memory across sessions with semantic
  understanding. Triggers when: (1) an agent needs persistent memory between
  conversations, (2) multi-agent systems need shared namespaces with RBAC
  isolation, (3) hybrid semantic+keyword search over stored context is required,
  (4) versioned memory with rollback is needed, (5) real-time event streaming
  (SSE/WebSocket) between agents is desired, or (6) batch memory operations
  are needed. Built on FastAPI + SQLite + HNSW (384-dim all-MiniLM-L6-v2
  embeddings). Requires python3/pip, AGENTMEMO_ADMIN_KEY env var, and
  pip install -r requirements.txt. First run downloads ~90MB model from HuggingFace.
---

# agentMemo — Semantic Memory Mesh

FastAPI-based memory server with HNSW embeddings, hybrid search, versioning, RBAC, and real-time event bus for AI agents.

## Prerequisites

- **Python 3.12+** and **pip**
- **AGENTMEMO_ADMIN_KEY** environment variable (required, secret) — the server refuses to start without it
- **Network access on first run**: the embedding model (all-MiniLM-L6-v2, ~90MB) is downloaded from HuggingFace on first startup and cached locally at `~/.cache/torch/sentence_transformers/`

## Install

```bash
pip install -r requirements.txt
```

This installs FastAPI, uvicorn, sentence-transformers, hnswlib, aiosqlite, and other dependencies. Review `requirements.txt` before running. Prefer installing inside a virtualenv or container.

## Required Environment Variables

| Variable | Required | Secret | Default | Description |
|----------|----------|--------|---------|-------------|
| `AGENTMEMO_ADMIN_KEY` | **yes** | **yes** | — | API key for RBAC auth. Server exits if unset. |
| `AGENTMEMO_PORT` | no | no | `8790` | HTTP port (localhost only) |
| `AGENTMEMO_DB` | no | no | `agentmemo.db` | SQLite DB path |
| `AGENTMEMO_RATE_LIMIT` | no | no | `120` | Requests/min per key |
| `AGENTMEMO_POOL_SIZE` | no | no | `5` | DB connection pool size |

## Start

```bash
export AGENTMEMO_ADMIN_KEY="your-secret-key"
python server.py
```

The server binds to `127.0.0.1:8790` (localhost only). For networked deployments, use a reverse proxy with TLS + auth. Never expose port 8790 to the internet directly.

## Security

- **Auth is mandatory**: server refuses to start without `AGENTMEMO_ADMIN_KEY`
- **All endpoints require `X-API-Key` header** (except `/health`)
- **Localhost binding by default**: only accessible from the local machine
- **First-run network activity**: downloads embedding model (~90MB) from HuggingFace; subsequent starts use local cache

## Quick Reference

### Store
```bash
curl -X POST http://localhost:8790/v1/memories \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-secret-key' \
  -d '{"text": "User prefers dark mode", "namespace": "prefs", "tags": ["ui"], "importance": 0.9}'
```

### Search
```bash
curl -H 'X-API-Key: your-secret-key' \
  'http://localhost:8790/v1/memories/search?q=dark+mode&mode=hybrid&tags=ui'
```

### Python Client
```python
from client import AgentMemoClient
memo = AgentMemoClient("http://localhost:8790", api_key="your-secret-key")
memo.store("Decision: use PostgreSQL", namespace="arch", tags=["db"], importance=0.8)
results = memo.search("database choice", mode="hybrid")
```

### Batch API
```bash
curl -X POST http://localhost:8790/v1/memories/batch \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-secret-key' \
  -d '{"operations": [{"op": "create", "text": "fact A"}, {"op": "create", "text": "fact B"}]}'
```

### Versioning & Rollback
```bash
curl -H 'X-API-Key: your-secret-key' http://localhost:8790/v1/memories/{id}/versions
curl -X POST -H 'X-API-Key: your-secret-key' \
  http://localhost:8790/v1/memories/{id}/rollback -d '{"version": 2}'
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check (no auth) |
| GET | `/metrics` | Server metrics |
| GET | `/dashboard` | Web dashboard |
| POST | `/v1/memories` | Store memory |
| GET | `/v1/memories/search` | Search (semantic/keyword/hybrid) |
| PUT | `/v1/memories/{id}` | Update (creates new version) |
| DELETE | `/v1/memories/{id}` | Delete |
| GET | `/v1/memories/{id}/versions` | Version history |
| POST | `/v1/memories/{id}/rollback` | Rollback to version |
| POST | `/v1/memories/batch` | Batch operations |
| POST | `/v1/import` | Bulk import |
| GET | `/v1/export` | Bulk export |
| GET | `/v1/events/stream` | SSE event stream |
| WS | `/v1/ws` | WebSocket stream |

## Key Features

- **Hybrid Search**: RRF fusion of semantic (HNSW cosine) + keyword (BM25-style)
- **Importance Decay**: `score = importance × 0.5^(age/half_life)` — older memories fade naturally
- **Versioning**: Every update creates a new version; full rollback support
- **RBAC**: Namespace isolation + API key access control
- **Event Bus**: SSE + WebSocket for real-time agent-to-agent notifications
- **Dashboard**: Web UI at `/dashboard` for browsing and searching memories
