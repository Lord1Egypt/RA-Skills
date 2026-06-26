# AOMS API Reference

Base URL: `http://localhost:9100`

## Memory Tier Endpoints

### POST /memory/{tier}
Write an entry to a memory tier.

**Path params:** `tier` — one of `episodic`, `semantic`, `procedural`

**Body:**
```json
{
  "type": "experience",
  "payload": {
    "title": "string",
    "outcome": "string",
    "tags": ["string"]
  },
  "tags": ["string"],
  "weight": 1.0
}
```

**Response:** `{"status": "ok", "tier": "episodic", "type": "experience", "id": "uuid"}`

### POST /memory/search
Keyword search with weighted scoring.

**Body:**
```json
{
  "query": "string",
  "tier": ["episodic"],
  "limit": 10,
  "date_from": "2025-01-01",
  "date_to": "2025-12-31",
  "min_weight": 0.5
}
```

All fields except `query` are optional.

### POST /memory/weight
Adjust entry weight (reinforcement learning).

**Body:**
```json
{
  "entry_id": "uuid",
  "tier": "episodic",
  "task_score": 0.9
}
```

`task_score` > 0.5 boosts weight, < 0.5 decays it.

### GET /memory/browse/{path}
Browse the module tree at a path. Returns directory listing or file contents.

### POST /memory/semantic-search
Vector search using embeddings (requires Ollama with `nomic-embed-text`).

**Body:**
```json
{
  "query": "string",
  "tier": ["episodic"],
  "limit": 10,
  "min_score": 0.35,
  "hybrid": true
}
```

`hybrid: true` combines vector + keyword results.

### POST /memory/decay
Apply time-based weight decay to old memories.

**Body:**
```json
{
  "tier": "episodic",
  "min_age_days": 30,
  "decay_rate": 0.995,
  "dry_run": true
}
```

### POST /memory/consolidate
Cluster similar old memories and merge them into summaries (uses Ollama).

**Body:**
```json
{
  "tier": "episodic",
  "min_age_days": 30,
  "similarity_threshold": 0.85,
  "max_entries": 100,
  "dry_run": true
}
```

### POST /memory/deduplicate
Find and merge duplicate memories based on embedding similarity.

**Query params:** `tier`, `similarity_threshold`, `limit`, `dry_run`

### POST /memory/index
Index existing memories into vector store for semantic search.

**Query params:** `tier`, `limit`, `skip_indexed`

## Agent Recall

### POST /recall
Single endpoint for agents to get relevant context.

**Body:**
```json
{
  "task": "description of current task",
  "tiers": ["episodic", "semantic", "procedural"],
  "token_budget": 500,
  "format": "markdown"
}
```

**Format options:** `markdown` (with tier headers), `json` (raw), `plain` (text blocks)

**Response:**
```json
{
  "context": "## Relevant Memory\n### Past Experiences\n- ...",
  "tokens": 450,
  "sources": [{"tier": "episodic", "id": "...", "score": 0.85, "content": "..."}],
  "tiers_searched": ["episodic", "semantic", "procedural"]
}
```

## Cortex (Progressive Disclosure)

### POST /cortex/ingest
Ingest a document with auto-generated L0/L1/L2 tiers (uses Ollama).

**Body:**
```json
{
  "content": "full document text",
  "title": "Document Title",
  "hierarchy_path": "docs/guides",
  "doc_type": "guide",
  "tags": ["deployment"]
}
```

### POST /cortex/query
Smart tiered query with auto-escalation within token budget.

**Body:**
```json
{
  "query": "deployment process",
  "token_budget": 1000,
  "top_k": 3,
  "directory": "docs/",
  "agent_id": "main"
}
```

### GET /cortex/document/{doc_id}?tier=l0
Get a specific tier of a document. Tier: `l0`, `l1`, `l2`.

### POST /cortex/regenerate/{doc_id}
Re-generate L0/L1 summaries for a document.

### GET /cortex/documents
List all indexed documents.

## Entity Extraction

### POST /entities/extract
Extract entities from text and optionally store as semantic relations.

**Body:**
```json
{
  "text": "AOMS runs on port 9100 and uses FastAPI",
  "store": true,
  "source_id": "conversation-123"
}
```

## Health & Stats

### GET /health
Service health check with tier counts and uptime.

### GET /stats
Full analytics: entry counts by tier/type, weight distribution, vector index stats, recency metrics.

## CLI Commands

```
cortex-mem start [--port 9100] [--host localhost] [--daemon]
cortex-mem stop
cortex-mem status
cortex-mem search QUERY [--limit 5] [--tier episodic]
cortex-mem migrate SOURCE_DIR
```
