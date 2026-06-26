---
name: cognitive-brain
description: Unified cognitive memory system inspired by human brain architecture. Provides episodic memory (hippocampus), semantic facts (neocortex), procedural memory with LLM-driven evolution (cerebellum), attention filtering (thalamus), sleep consolidation, and soul erosion health metrics. Use when storing experiences, recalling memories, managing facts, creating/evolving procedures, filtering incoming information by importance, running memory consolidation, or checking memory health. Replaces separate facts/proc CLIs with a single `brain` command.
---

# Cognitive Brain

Unified memory system modeled on human brain architecture. One CLI (`brain`) for all memory operations.

## Architecture

| System | Brain Region | What it does |
|--------|-------------|--------------|
| **Episodic** | Hippocampus | Time-stamped experiences with emotional tags |
| **Semantic** | Neocortex | Structured facts (entity/key/value with FTS5) |
| **Procedural** | Cerebellum | Versioned workflows that evolve from failures |
| **Attention** | Thalamus | Score incoming info → store/summarize/discard |
| **Consolidation** | Sleep replay | Batch-process episodes → extract facts |
| **Health** | Soul erosion | Detect memory drift, conflicts, flatness |

## Installation

```bash
# 1. Initialize the database
sqlite3 brain.db < scripts/schema.sql

# 2. Link the CLI
ln -sf "$(pwd)/scripts/brain.sh" ~/.local/bin/brain
chmod +x scripts/brain.sh

# 3. (Optional) Migrate existing daily logs
python3 scripts/migrate-daily-logs.py --dir /path/to/memory/ --db brain.db
```

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `BRAIN_DB` | `<skill>/brain.db` | Path to brain database |
| `BRAIN_AGENT` | `margot` | Agent identity for scoping |
| `BRAIN_FACTS_DB` | `memory/facts.db` | Legacy facts database path |
| `BRAIN_LLM_URL` | Google Gemini endpoint | OpenAI-compatible chat completions URL |
| `BRAIN_LLM_KEY` | *(none — must be set)* | API key for LLM provider (required for `proc evolve`) |
| `BRAIN_LLM_MODEL` | `gemini-2.5-flash` | Model name for evolution reasoning |

## Credentials & Scope

**Required for `brain proc evolve` only:**
- `BRAIN_LLM_KEY` — Your API key for the LLM provider. Set via env var or `brain config set key <value>`.
- No credentials are auto-discovered or read from platform stores.
- Without a key, `proc evolve` falls back to local pattern-based evolution (no LLM needed).

**Data scope:**
- All data stays in your `brain.db` file (local SQLite).
- `brain facts` reads/writes `BRAIN_FACTS_DB` (default: `facts.db` in skill directory).
- `brain wm` reads/writes `SESSION_STATE` (default: `SESSION-STATE.md` in workspace root).
- No data is sent externally except LLM API calls during `proc evolve`.

## Quick Reference

### Store & Recall
```bash
brain store "Fixed the deploy pipeline" --title "Deploy Fix" --emotion relieved --importance 8
brain ingest "Docker OOM at 3 AM" --title "OOM Event" --source mqtt  # attention-gated
brain recall "deploy pipeline" --type all --limit 5
brain episodes 2026-03-15
brain emotions 7
brain important 8 14
```

### Facts (Semantic Memory)
```bash
brain facts get Darian favorite_movie
brain facts set Mae birthday "September 12" --category date --permanent
brain facts search "SSH" --limit 5
brain facts list --entity Darian --limit 10
brain facts stats
```

### Procedures (Cerebellum)
```bash
brain proc create deploy-api --title "Deploy API" --steps '["Pull latest","Run tests","Deploy"]'
brain proc success deploy-api
brain proc fail deploy-api --step 2 --error "Tests timed out" --fix "Increased timeout to 60s"
brain proc evolve deploy-api           # LLM rewrites steps from failure patterns
brain proc evolve deploy-api --dry-run # preview without applying
brain proc history deploy-api          # full evolution timeline
brain proc list
```

### Attention Filter
```bash
brain filter "GPU temperature 72°C" --source mqtt    # → discard (routine)
brain filter "SSH brute force from new IP" --source security  # → store (novel threat)
```

### Consolidation
```bash
brain consolidate --dry-run    # preview what would be processed
brain consolidate              # run sleep replay
```

### Health (Soul Erosion Detection)
```bash
brain health           # 7-metric scored report
brain health -v        # verbose with all details
brain health --json    # machine-readable for crons
```

### Configuration
```bash
brain config show              # current LLM config
brain config set model gpt-4o  # change model
brain config set url http://localhost:11434/v1/chat/completions  # switch to Ollama
```

### Multi-Agent
```bash
brain --agent bud store "Patrol complete" --title "Bud Patrol" --importance 3
brain --agent bud proc list   # sees own + shared procedures
brain who                     # show all agents in the system
```

## Procedure Evolution Flow

The core innovation — procedures that rewrite themselves from failure patterns:

1. **Record failures** with step-level granularity: `brain proc fail <slug> --step N --error "desc"`
2. At 3+ failures, brain suggests evolution
3. **`brain proc evolve <slug>`** analyzes patterns:
   - Repeat offender steps (same step failing multiple times)
   - Brittle chains (consecutive step failures)
   - Error keyword clustering (timeout, auth, permission, etc.)
4. LLM synthesizes and rewrites steps — adds pre-checks, reorders, annotates with `[vN: reason]`
5. Local fallback if LLM unavailable — pattern-matching inserts defensive steps
6. Full version history preserved: `brain proc history <slug>`

## Health Metrics

Seven metrics, each scored 1-10:

| Metric | What it detects |
|--------|----------------|
| Memory Freshness | Time since last recorded episode |
| Consolidation Debt | Backlog of unprocessed episodes |
| Importance Calibration | Everything rated 8+? Nothing is important |
| Emotional Diversity | Flatlined to one emotion = loss of range |
| Fact Consistency | Contradictory facts = identity fragmentation |
| Procedure Health | Success rates dropping on learned behaviors |
| Recording Cadence | Silent days creating memory gaps |

## Schema

Database: SQLite with WAL mode, FTS5 full-text search, foreign keys.

Tables: `episodes`, `episodes_fts`, `facts`, `facts_fts`, `procedures`, `procedure_history`, `working_memory`, `consolidation_log`, `brain_meta`.

Initialize with: `sqlite3 brain.db < scripts/schema.sql`

## Files

| File | Purpose |
|------|---------|
| `scripts/brain.sh` | Main CLI dispatcher |
| `scripts/schema.sql` | Database schema |
| `scripts/attention.py` | Thalamic attention filter (rule-based scoring) |
| `scripts/consolidate.py` | Sleep replay consolidation pipeline |
| `scripts/erosion.py` | Soul erosion health metrics |
| `scripts/evolve.py` | Procedure evolution engine (LLM + local fallback) |
| `scripts/facts.py` | Semantic fact storage wrapper |
| `scripts/migrate-daily-logs.py` | Import existing daily markdown logs |
