# 🧠 Cognitive Brain

A unified cognitive memory system for AI agents, inspired by human brain architecture.

One CLI (`brain`) for all memory operations — episodic, semantic, procedural, attention filtering, sleep consolidation, and soul erosion health metrics.

## Architecture

| System | Brain Region | What it does |
|--------|-------------|--------------|
| **Episodic** | Hippocampus | Time-stamped experiences with emotional tags |
| **Semantic** | Neocortex | Structured facts (entity/key/value with FTS5) |
| **Procedural** | Cerebellum | Versioned workflows that evolve from failures |
| **Attention** | Thalamus | Score incoming info → store/summarize/discard |
| **Consolidation** | Sleep replay | Batch-process episodes → extract facts |
| **Working Memory** | Prefrontal Cortex | Capacity-limited active context with TTL |
| **Health** | Soul erosion | Detect memory drift, conflicts, emotional flatness |

## Key Feature: Procedure Evolution

Procedures that **rewrite themselves** from failure patterns:

1. Record failures with step-level granularity
2. At 3+ failures, the system suggests evolution
3. `brain proc evolve` analyzes patterns (repeat offenders, brittle chains, error keywords)
4. LLM synthesizes and rewrites steps — adds pre-checks, reorders, annotates
5. Local fallback if LLM unavailable
6. Full version history preserved

## Quick Start

```bash
# Initialize the database
sqlite3 brain.db < scripts/schema.sql

# Link the CLI
ln -sf "$(pwd)/scripts/brain.sh" ~/.local/bin/brain
chmod +x scripts/brain.sh

# Store an experience
brain store "Fixed the deploy pipeline" --title "Deploy Fix" --emotion relieved --importance 8

# Search all memory
brain recall "deploy pipeline"

# Check brain health
brain health
```

## Installation as OpenClaw Skill

Drop the `cognitive-brain/` directory into your OpenClaw workspace `skills/` folder, or install the `.skill` package.

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `BRAIN_DB` | `<skill>/brain.db` | Path to brain database |
| `BRAIN_AGENT` | `margot` | Agent identity for scoping |
| `BRAIN_FACTS_DB` | `memory/facts.db` | Legacy facts database path |
| `BRAIN_LLM_URL` | Google Gemini endpoint | LLM API for procedure evolution |
| `BRAIN_LLM_KEY` | Auto-discovered | API key |
| `BRAIN_LLM_MODEL` | `gemini-2.5-flash` | Model for evolution reasoning |

## Multi-Agent Support

Each agent gets its own scoped memory. Agents see their own data + shared data:

```bash
brain --agent bud store "Patrol complete" --title "Bud Patrol" --importance 3
brain --agent bud proc list   # sees own + shared procedures
brain who                     # show all agents in the system
```

## Soul Erosion Detection

Seven metrics, each scored 1-10:

- **Memory Freshness** — Time since last recorded episode
- **Consolidation Debt** — Backlog of unprocessed episodes
- **Importance Calibration** — Everything rated 8+? Nothing is important
- **Emotional Diversity** — Flatlined to one emotion = loss of range
- **Fact Consistency** — Contradictory facts = identity fragmentation
- **Procedure Health** — Success rates dropping on learned behaviors
- **Recording Cadence** — Silent days creating memory gaps

## Tech Stack

- **SQLite** with WAL mode + FTS5 full-text search
- **Python 3** for all database operations (parameterized queries — no SQL injection)
- **Bash** dispatcher for CLI ergonomics
- **Any OpenAI-compatible LLM** for procedure evolution (configurable)

## License

MIT
