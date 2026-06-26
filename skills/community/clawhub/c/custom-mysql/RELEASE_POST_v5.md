# VectorClaw v5.0.0 — MyVector Self-Sufficiency

**VectorClaw v5.0.0 makes MyVector the single source of truth for all agent memory.** Auto-extraction and knowledge graph reasoning are now native MySQL systems, eliminating dependency on external tools (Mem0, Hancho).

## New in This Release

### Auto-Extraction Hook — Replaces Mem0

The auto-extraction hook uses a local LLM (qwen3.5:4b) to extract atomic facts from conversation text and insert them directly into MyVector:

- **Structured extraction:** core_fact, confidence, entities, linked_to, tags, memory_type, importance
- **Key mapping:** Normalizes LLM output ("fact" → "core_fact", invalid types → "semantic")
- **Auto-dedup:** Jaccard similarity check on insert — merges if >50% overlap
- **Source tracking:** All auto-extracted memories marked with `source='auto'`
- **Human verification:** `verified_by_human` flag for promoting accurate auto-facts
- **Fallback:** Regex-based extraction when LLM is unavailable
- **Quality logging:** Every extraction run logged to `extraction_log` for empirical tuning

```bash
python3 scripts/auto-extract.py "conversation text" --user <discord_id>
python3 scripts/auto-extract.py --file /path/to/text.txt --user <id> --dry-run
```

### Memory Relations + Knowledge Graph — Replaces Hancho

Native MySQL knowledge graph that replaces Hancho's external reasoning:

- **`memory_relations` table:** fact_id, related_fact_id, relation_type, confidence, source
- **Relation types:** mentions, implies, contradicts, same_entity, related_to
- **Auto-discovery:** Finds existing memories sharing entities during extraction
- **Consolidation pass:** Periodic scanning for contradictions and new edges
- **Hub insight derivation:** Identifies high-degree facts (3+ connections) as important
- **`memory_graph_1hop` view:** Pre-computed 1-hop graph traversal for retrieval

```bash
python3 scripts/hancho-consolidate.py --user <discord_id>
python3 scripts/hancho-consolidate.py --user <id> --hours 24 --dry-run
```

### Database Schema Changes

- **`memories` table:** Added `source`, `verified_by_human`, `extraction_prompt` columns
- **New table:** `memory_relations` — knowledge graph edges
- **New table:** `extraction_log` — extraction quality metrics
- **New view:** `memory_graph_1hop` — fast graph traversal
- **`user_context` enum:** Added `auto_extracted`, `graph_derived`, `extraction_quality`

### Extraction Quality Logging

Tracks auto-extraction quality for empirical prompt tuning:
- Facts extracted, merged, inserted, relations discovered per run
- Input length, extraction time (ms), model used, fallback usage
- Per-user and time-based indexes

## Upgrade

```bash
# 1. Back up your database
docker exec myvector-db mysqldump -u root -p<pass> jerith > backup_pre_v5.sql

# 2. Apply schema migration
docker exec -i myvector-db mysql -u root -p<pass> jerith < upgrade_v4_to_v5.sql

# 3. Run initial consolidation to build graph edges
python3 scripts/hancho-consolidate.py --all-users --dry-run

# 4. If dry run looks good, run for real
python3 scripts/hancho-consolidate.py --all-users

# 5. Test auto-extraction
python3 scripts/auto-extract.py "Test conversation text" --user <your_id> --dry-run
```

## Deprecation Plan

- **Mem0:** Run auto-extract in parallel for 7-10 days. Compare quality. Retire Mem0 when auto-extract matches or exceeds.
- **Hancho:** Memory relations table + consolidation pass already active. Retire Hancho after 7-10 day validation.

## Why Consolidate?

- **Unified pruning:** One system for importance decay, access tracking, and cleanup
- **Confidence propagation:** Facts and relations share the same confidence model
- **No sync issues:** No more stale data between separate systems
- **Full ownership:** Every byte of memory is queryable, auditable, and tunable
- **Simpler bootstrap:** Fewer external dependencies in context window
