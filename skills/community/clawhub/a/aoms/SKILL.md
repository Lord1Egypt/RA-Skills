---
name: aoms
description: Always-On Memory Service — persistent 4-tier memory (episodic, semantic, procedural, working) with weighted retrieval, vector search, progressive disclosure (L0/L1/L2), and automatic weight decay. Use when you need persistent agent memory across sessions, context recall for tasks, knowledge graphs, learning from mistakes, or any long-term memory capability. Replaces flat-file memory logging with a real indexed memory service. Works with OpenClaw, Claude Code, Codex, or any agent that can call HTTP APIs.
metadata:
  openclaw:
    requires:
      bins: [cortex-mem]
    install:
      - id: pip
        kind: pip
        package: cortex-mem
        bins: [cortex-mem]
        label: Install AOMS (pip)
---

# AOMS — Always-On Memory Service

Persistent memory service for AI agents. Stores experiences, facts, and skills in JSONL files with weighted retrieval and optional vector search via ChromaDB + Ollama embeddings.

## Install & Start

```bash
# Install from PyPI
pip install cortex-mem

# Start (foreground)
cortex-mem start --port 9100

# Start (background daemon)
cortex-mem start --daemon

# Check status
cortex-mem status

# Docker alternative
docker pull ghcr.io/dhawalc/cortex-mem:latest
docker run -p 9100:9100 -v aoms-data:/app/modules ghcr.io/dhawalc/cortex-mem
```

The service runs on `http://localhost:9100`. API docs at `/docs`.

> **Note:** AOMS runs as a local HTTP service on your machine. It does not send data externally. Vector search requires a local Ollama instance (optional).

## Core Concepts

**Memory Tiers:**
| Tier | Stores | Example |
|------|--------|---------|
| `episodic` | Experiences, decisions, failures | "Deployed v2 — rollback needed due to missing migration" |
| `semantic` | Facts, relations, knowledge | "Project uses pnpm, not npm" |
| `procedural` | Skills, patterns, workflows | "To deploy: run migrations first, then build, then push" |

**Weighted Retrieval:** Every entry has a `weight` (0.1–5.0). Important memories surface first. Weights increase when memories prove useful (`/memory/weight`) and decay over time (`/memory/decay`).

**Progressive Disclosure (Cortex):** Large documents are stored at 3 tiers — L0 (one-liner), L1 (summary), L2 (full text). Queries auto-escalate within a token budget.

## API Quick Reference

### Write Memory

```bash
curl -X POST http://localhost:9100/memory/episodic \
  -H "Content-Type: application/json" \
  -d '{
    "type": "experience",
    "payload": {
      "title": "Fixed auth bug",
      "outcome": "Token refresh was missing retry logic",
      "tags": ["auth", "bugfix"]
    },
    "weight": 1.3
  }'
```

### Search Memory

```bash
# Keyword search
curl -X POST http://localhost:9100/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "deployment", "limit": 5}'

# Filter by tier
curl -X POST http://localhost:9100/memory/search \
  -d '{"query": "auth", "tier": ["episodic", "procedural"], "limit": 10}'
```

### Agent Recall (context injection)

Single endpoint to get relevant context for a task, formatted for prompt injection:

```bash
curl -X POST http://localhost:9100/recall \
  -H "Content-Type: application/json" \
  -d '{"task": "deploy the API", "token_budget": 500, "format": "markdown"}'
```

Returns pre-formatted context with tier headers. Inject directly into agent prompts.

### Reinforce Memory

When a memory proves useful, boost its weight:

```bash
curl -X POST http://localhost:9100/memory/weight \
  -d '{"entry_id": "abc123", "tier": "episodic", "task_score": 0.9}'
```

### Cortex Query (progressive disclosure)

```bash
curl -X POST http://localhost:9100/cortex/query \
  -d '{"query": "deployment process", "token_budget": 1000, "top_k": 3}'
```

Auto-escalates from L0 → L1 → L2 within the token budget.

## Agent Integration Patterns

### Pattern 1: Session Boot (recall context)

At session start, call `/recall` with the current task to inject relevant memory:

```python
import httpx

resp = httpx.post("http://localhost:9100/recall", json={
    "task": "working on auth module",
    "token_budget": 500,
    "format": "markdown"
})
context = resp.json()["context"]
# Inject into system prompt or prepend to conversation
```

### Pattern 2: Log Learnings (write on events)

After completing a task, fixing a bug, or learning something new:

```python
httpx.post("http://localhost:9100/memory/episodic", json={
    "type": "experience",
    "payload": {
        "title": "pnpm not npm",
        "outcome": "Project uses pnpm workspaces. npm install fails.",
        "tags": ["build", "correction"]
    },
    "weight": 1.5
})
```

### Pattern 3: Knowledge Graph (semantic facts)

Store structured facts as subject-predicate-object triples:

```python
httpx.post("http://localhost:9100/memory/semantic", json={
    "type": "relation",
    "payload": {
        "subject": "auth-service",
        "predicate": "depends_on",
        "object": "redis",
        "confidence": 0.95
    }
})
```

### Pattern 4: Reinforce on Success

After using a recalled memory successfully, boost its weight:

```python
httpx.post("http://localhost:9100/memory/weight", json={
    "entry_id": recalled_id,
    "tier": "episodic",
    "task_score": 0.9  # >0.5 boosts, <0.5 decays
})
```

## OpenClaw Integration

To use AOMS with OpenClaw, configure it manually:

### 1. Add to OpenClaw config

```yaml
# In ~/.openclaw/config.yaml
memory:
  provider: cortex-mem
  url: http://localhost:9100
```

### 2. Session boot script

Add a boot script to your workspace (see `references/openclaw-setup.md` for a full example):

```python
# boot_aoms.py — call at session start
import httpx, sys
try:
    r = httpx.post("http://localhost:9100/recall", json={
        "task": "session boot — what's recent and relevant",
        "token_budget": 300, "format": "markdown"
    }, timeout=5.0)
    if r.status_code == 200:
        print(r.json()["context"])
except Exception as e:
    print(f"AOMS unavailable: {e}", file=sys.stderr)
```

### 3. Optional: Workspace migration

If you have existing flat-file memory (MEMORY.md, daily logs), you can import it:

```bash
cortex-mem migrate ~/.openclaw/workspace
```

> **This is optional and explicit.** Review what files will be parsed before running. The command reads Markdown files and creates structured memory entries — it does not modify or delete originals.

### Helper Functions

```python
from openclaw_integration import log_achievement, log_error, log_fact

await log_achievement("Shipped v2", "All tests passing, deployed to prod")
await log_error("Build failed", "Missing dependency: libpq-dev")
await log_fact("project", "uses", "PostgreSQL 16")
```

## Maintenance

```bash
# Weight decay (old memories fade unless reinforced)
curl -X POST http://localhost:9100/memory/decay \
  -d '{"min_age_days": 30, "decay_rate": 0.995, "dry_run": true}'

# Consolidate similar memories
curl -X POST http://localhost:9100/memory/consolidate \
  -d '{"tier": "episodic", "min_age_days": 30, "dry_run": true}'

# Deduplication
curl -X POST http://localhost:9100/memory/deduplicate?tier=episodic&dry_run=true

# Stats
curl http://localhost:9100/stats
```

## Full API Reference

See `references/api-reference.md` for all endpoints, request/response schemas, and advanced features (vector search, entity extraction, document ingestion).

## Configuration

Default config is at `service/config.yaml`. Key settings:

```yaml
service:
  port: 9100          # API port
  host: localhost      # Bind address (use 0.0.0.0 for Docker)

storage:
  root: .              # Where JSONL module files live

weights:
  decay_rate: 0.995    # Daily decay multiplier
  min_weight: 0.1      # Floor
  max_weight: 5.0      # Ceiling
```

Set `CORTEX_MEM_ROOT` env var to override the storage root.
