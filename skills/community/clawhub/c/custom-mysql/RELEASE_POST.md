# VectorClaw v5.0.0 — MyVector Self-Sufficiency

> **Security update (v5.0.1):** This release addresses 37 findings from the ClawHub security audit. All Python scripts now use environment variable credentials (no hardcoded passwords), auto-extraction is opt-in only, migration scripts include explicit backup warnings, and privacy/consent documentation has been added.

VectorClaw v5.0.0 makes MyVector fully self-sufficient by absorbing Mem0's auto-extraction and Hancho's knowledge graph reasoning into native MySQL systems. No more external memory services — everything runs in your Docker container with local LLM support.

> **⚠️ Privacy notice:** This system automatically extracts and persists sensitive personal data (emotional states, relationship signals, health indicators, behavioral profiles) from user conversations. Obtain explicit opt-in consent before enabling auto-extraction. See the PRIVACY & CONSENT NOTICE in SKILL.md.

## New in This Release

### Auto-Extraction Hook (`scripts/auto-extract.py`)
Replaces Mem0 with a local LLM-powered extraction pipeline:
- Uses qwen3.5:4b via Ollama to extract atomic facts from conversation text
- Structured JSON output: core_fact, confidence, entities, linked_to, tags, memory_type, importance
- Auto-dedup on insert: Jaccard similarity check, merges if >50% overlap
- Auto-discovers relations: finds existing memories sharing entities, creates graph edges
- Source tracking: marks facts with `source='auto'` for quality monitoring
- Fallback to regex-based extraction when LLM is unavailable
- Validates all output against DB enums before insert

### Memory Relations Table (`memory_relations`)
Native MySQL knowledge graph replacing Hancho:
- Schema: fact_id, related_fact_id, relation_type, confidence, source, discovered_at
- Relation types: mentions, implies, contradicts, same_entity, related_to
- Unique constraint prevents duplicate edges
- Indexed for fast graph traversal during retrieval

### Hancho Consolidation Pass (`scripts/hancho-consolidate.py`)
Graph reasoning that runs as a scheduled heartbeat job:
- Scans recent memories for shared entities/terms (Jaccard > 0.15)
- Contradiction detection: same-topic facts with opposite polarity
- Inserts edges into `memory_relations`
- Derives hub insights (facts with 3+ connections flagged as important)

### Extraction Quality Logging (`extraction_log`)
Tracks quality metrics for empirical tuning:
- Facts extracted, merged, inserted, relations discovered per run
- Input length, extraction time, model used, fallback usage

### Graph Traversal View (`memory_graph_1hop`)
Pre-computed MySQL view for fast 1-hop graph expansion during retrieval.

### Schema Changes (v4 → v5)

- `memories` table: added `source`, `verified_by_human`, `extraction_prompt` columns
- `user_context` context_type enum: added `auto_extracted`, `graph_derived`, `extraction_quality`
- New tables: `memory_relations`, `extraction_log`
- New view: `memory_graph_1hop`

## Upgrade

**⚠️ Always back up first:**
```bash
docker exec myvector-db mysqldump -u root -p<pass> mysqlclaw > backup_pre_v5.sql
```

```bash
# 1. Apply schema migration (requires admin/root — this is DDL)
docker exec -i myvector-db mysql -u root -p<pass> mysqlclaw < upgrade_v4_to_v5.sql

# 2. Set environment variables for credentials
export MYSQL_USER=mysqlclaw
export MYSQL_PASSWORD=<your_least_priv_password>

# 3. Test auto-extraction (DRY RUN first — always)
cd ~/.openclaw/workspace
python3 scripts/auto-extract.py "Test fact: user likes Python" --user <id> --dry-run --json

# 4. Test consolidation (DRY RUN first — always)
python3 scripts/hancho-consolidate.py --user <id> --hours 24 --dry-run
```

**Auto-extraction is disabled by default.** Only enable per-user after explicit opt-in and dry-run review.

## Memory Architecture (v5)

Your agent now operates with four interconnected memory systems:

1. **MEMORY.md** — Always-in-context curated narrative (relationships, emotions, key lessons)
2. **MyVector (VectorClaw v5)** — Structured profiles, interactions, mood, preferences, dimensional tags, reasoning insights, auto-extraction, knowledge graph
3. **ChromaDB** — Semantic search across workspace files (skills, projects, session logs)
4. **Mem0** — Deprecated (rate-limited); auto-extract replaces it. Retire after 7-10 day parallel validation.

The `auto-extract.py` hook and `hancho-consolidate.py` run as heartbeat jobs, continuously improving recall quality without manual intervention.

---

Full changelog: [changelog.md](changelog.md)
