# paradoxfuzzle/custom-mysql

## ⚠️ PRIVACY & CONSENT NOTICE — READ BEFORE INSTALLING

This skill **automatically extracts, infers, and persistently stores sensitive personal information** from user conversations, including but not limited to:

- **Emotional states and mood patterns** (stress, anxiety, sadness, joy)
- **Relationship signals** (who users interact with, closeness, trust)
- **Health and wellness indicators** (medication mentions, symptoms, coping patterns)
- **Behavioral profiling** (engagement patterns, time-of-day activity, topic preferences)
- **Inferred preferences and traits** (derived from conversation patterns, not explicitly stated)
- **Agent reasoning logs** (internal chain-of-thought stored alongside user data)

**By installing this skill, you accept responsibility for:**

1. **Informing all users** that their conversation data is being profiled and persisted
2. **Obtaining explicit opt-in consent** before enabling auto-extraction for any user
3. **Providing a clear mechanism** for users to request full data deletion (`rollback_user.sql`)
4. **Reviewing auto-extracted data** for accuracy and sensitivity before it affects agent behavior
5. **Configuring retention limits** appropriate to your use case (default: 30-90 days depending on data type)

This is a **self-hosted, self-managed system**. No data leaves your infrastructure. However, the breadth of profiling it performs is significant and should not be enabled without user awareness.

**Disable auto-extraction by default.** Enable per-user only after explicit opt-in.

---

## Overview

Security-hardened MyVector MySQL profile storage with capability bounding for OpenClaw. Tracks interactions, relationships, context, skill usage, notes, preferences, media, food, personas, mood states, engagement patterns, proactive reminders, agent learnings, community sentiment, trending topics, and community events. Now includes HindSight (post-conversation consolidation), HoloGraphic (multi-dimensional tagging), and Hancho (knowledge graph reasoning) memory systems. v4.0.0 integrates with the `memory_consolidation.py` script for automated heartbeat-based memory maintenance. All SQL is routed through `docker exec` into the MyVector container. Requires a dedicated least-privilege MySQL user — root/admin accounts are rejected.

## Version

5.0.1 – 2026-05-27 (security audit response)

## Memory Systems

VectorClaw v5.0.0 makes MyVector self-sufficient. It includes three memory enhancement systems (v4) plus auto-extraction and native knowledge graph reasoning (v5):

### HindSight — Post-Conversation Consolidation
- Analyzes recent interactions (sentiment trends, topic frequency)
- Identifies new topics not yet stored as memories
- Detects recurring themes worth tracking
- Stores findings in `user_context` (categories: discovery, behavioral, emotional)

### HoloGraphic — Multi-Dimensional Tagging
- Tags memories with: emotion, context, urgency, people
- **Emotion**: positive, negative, complex, neutral
- **Context**: work, personal, health, tech, social, creative
- **Urgency**: immediate, ongoing, timeless, historical
- **People**: auto-detected names (NoodlyPanda, Ev, Cyle, Jerith, etc.)
- Enables retrieval from any angle ("how did Ev feel about X", "health topics in May")
- Stores tags in `user_context` (category: metadata)

### Hancho — Knowledge Graph Reasoning
- Connects related facts to derive new insights via 7 reasoning rules:
  1. **medication_side_effects**: medication keywords + side effect keywords
  2. **health_chain**: condition keywords + treatment keywords
  3. **tech_infrastructure**: infra keywords + AI/model keywords
  4. **creative_passion**: interest keywords + creation keywords
  5. **relationship_depth**: emotional keywords + interaction keywords
  6. **interest_to_skill**: learning keywords + skill keywords
  7. **emotional_pattern**: stress keywords + coping keywords
- Inter-user reasoning finds shared topics between users
- Stores derived insights in `user_context` (categories: reasoning, social_graph)

### Memory Types

| Type | Table | Description |
|------|-------|-------------|
| **Episodic** | `user_context` | Specific events/experiences with timestamps |
| **Semantic** | `user_context` | General facts and knowledge |
| **Procedural** | `user_context` | How-to knowledge and habits |
| **Emotional** | `user_mood` | Emotional states with triggers and intensity |
| **Preference** | `user_preferences` | Explicit preferences with confidence |
| **Synaptic** | `synaptic_memory` | Key-value memory with priority and decay |
| **HoloGraphic** | `user_context` (metadata) | Multi-dimensional tags (emotion, context, urgency, people) |
| **HindSight** | `user_context` (discovery) | Post-conversation consolidation findings |
| **Auto-Extracted** | `memories` (v5.0.0) | LLM-extracted facts with source='auto', deduped on insert |
| **Graph-Derived** | `memory_relations` (v5.0.0) | Knowledge graph edges: mentions, implies, contradicts, same_entity, related_to |
| **Extraction Log** | `extraction_log` (v5.0.0) | Quality metrics for empirical prompt tuning |

### Memory Sources (v5.0.0)

All memories in the `memories` table now track their provenance:

| Source | Description | Initial Confidence |
|--------|-------------|-------------------|
| `manual` | Written explicitly by agent | 0.9 |
| `auto` | Extracted by local LLM hook | 0.6-0.7 |
| `consolidation` | Derived from consolidation pass | 0.7 |
| `import` | Imported from external system | 0.5 |

Auto-extracted memories can be promoted via `verified_by_human = TRUE` when grounding confirms accuracy.

### Auto-Extraction Hook (v5.0.0) — Replaces Mem0

The auto-extraction hook uses a local LLM to extract atomic facts from conversation text and insert them directly into MyVector. This replaces Mem0's zero-effort capture with full ownership.

**Script:** `scripts/auto-extract.py`

```bash
# Extract from text
python3 scripts/auto-extract.py "conversation text here" --user <discord_id>

# Extract from file
python3 scripts/auto-extract.py --file /path/to/conversation.txt --user <discord_id>

# Dry run (preview without inserting)
python3 scripts/auto-extract.py "text" --user <id> --dry-run

# Output as JSON
python3 scripts/auto-extract.py "text" --user <id> --dry-run --json
```

**Pipeline:**
1. Local qwen3.5:4b extracts structured JSON (core_fact, confidence, entities, linked_to, tags, memory_type, importance)
2. Key mapping normalizes LLM output ("fact" → "core_fact", invalid types → "semantic")
3. Dedup: Jaccard similarity check against existing memories, merges if >50% overlap
4. Insert with `source='auto'` for quality tracking
5. Auto-discover relations: finds existing memories sharing entities
6. Logs extraction metrics to `extraction_log`

**Prompt design:** Uses string concatenation (not f-strings) to avoid curly brace issues with JSON examples. Strict key name requirements in prompt.

**Fallback:** Regex-based extraction when LLM is unavailable.

### Memory Relations + Knowledge Graph (v5.0.0) — Replaces Hancho

Native MySQL knowledge graph that replaces Hancho's external reasoning.

**Table:** `memory_relations`
- `fact_id`, `related_fact_id` → FK to memories.id
- `relation_type`: mentions, implies, contradicts, same_entity, related_to
- `confidence`: 0.0-1.0
- `source`: auto, manual, consolidation
- Unique constraint on (fact_id, related_fact_id, relation_type)

**Consolidation script:** `scripts/hancho-consolidate.py`

```bash
# Consolidate recent memories (default: last 6 hours)
python3 scripts/hancho-consolidate.py --user <discord_id>

# Lookback window
python3 scripts/hancho-consolidate.py --user <id> --hours 24

# Dry run
python3 scripts/hancho-consolidate.py --user <id> --dry-run
```

**Pipeline:**
1. Scan recent memories for shared entities/terms (Jaccard > 0.15)
2. Contradiction detection: same-topic facts with opposite polarity
3. Insert edges into `memory_relations`
4. Derive hub insights (facts with 3+ connections)

**Graph traversal:** Pre-computed view `memory_graph_1hop` for fast retrieval.

### Extraction Quality Logging (v5.0.0)

Tracks auto-extraction quality for empirical tuning:

**Table:** `extraction_log`
- facts extracted, merged, inserted, relations discovered per run
- input length, extraction time (ms), model used, fallback usage
- Per-user and time-based indexes

### Consolidation Script

- **`memory_consolidation.py`** at `~/.openclaw/workspace/scripts/memory_consolidation.py`
- Runs HindSight + HoloGraphic + Hancho in sequence
- Scheduled every 6 hours via heartbeat and cron
- Commands:
  ```bash
  python3 memory_consolidation.py --user <discord_id>
  python3 memory_consolidation.py --all-users
  python3 memory_consolidation.py --user <id> --dry-run
  python3 memory_consolidation.py --user <id> --hindisght-only
  python3 memory_consolidation.py --user <id> --holohraphic-only
  python3 memory_consolidation.py --user <id> --hancho-only
  ```

## Capabilities

- MyVector MySQL read/write operations only (no external APIs, crypto, or wallets)
- All SQL routed through MyVector Docker container via `docker exec`
- Uses `.env` files for credentials (parsed as KEY=VALUE, never shell-sourced)
- All SQL routed through `sql_safe_exec.sh` for safety
- `query` command is SELECT-only
- DML requires interactive confirmation (no non-interactive bypass)
- Table allowlist enforced for all write operations (26 approved tables)
- Single-statement execution only (semicolons rejected)
- **DDL blocked at the runtime layer** (`sql_safe_exec.sh` rejects DROP, TRUNCATE, CREATE, ALTER, GRANT, REVOKE from agent-facing commands)
- **Schema migrations are an exception**: Version upgrade scripts (`upgrade_vX_to_vY.sql`) use DDL (ALTER TABLE, CREATE TABLE IF NOT EXISTS) and must be run by a human administrator using `docker exec` directly — NOT through the agent-facing `sql_safe_exec.sh` wrapper. This is intentional: schema evolution requires DDL, but day-to-day agent operations do not.
- Comment injection blocked (`/* */`, `--`, `#`)
- Hex-encoded string detection blocked
- Path traversal and sensitive file patterns blocked
- Proper MySQL string escaping via Python (handles all edge cases)
- Enum validation on all convenience command parameters
- **FAIL CLOSED**: refuses to connect if MYSQL_USER or MYSQL_PASSWORD is missing
- **REJECTS root/admin users**: requires dedicated least-privilege account
- **Verifies MyVector container is running** before attempting connection
- **Credentials loaded from environment variables** — never hardcoded in any Python script
- **Memory consolidation**: HindSight + HoloGraphic + Hancho reasoning via heartbeat
- **Auto-extraction**: Local LLM-powered fact extraction replacing Mem0 (v5.0.0)
- **Knowledge graph**: Native MySQL `memory_relations` table replacing Hancho (v5.0.0)
- **Graph traversal**: `memory_graph_1hop` view for retrieval-time graph expansion
- **Extraction quality tracking**: `extraction_log` table for empirical prompt tuning

### Deprecated Features (v5.0.0)

- **Mem0**: Auto-extraction replaced by `scripts/auto-extract.py`. Run in parallel for 7-10 days to validate quality, then retire.
- **Hancho**: Knowledge graph reasoning replaced by `memory_relations` table + `scripts/hancho-consolidate.py`. Native MySQL graph is tighter and fully owned.

## Configuration

| Option          | Default       | Notes                                  |
|-----------------|---------------|----------------------------------------|
| `MYSQL_USER`    | *required*    | Dedicated least-privilege account (NOT root) |
| `MYSQL_PASSWORD`| *required*    | Store in `.env` (chmod 600)            |
| `MYSQL_PORT`    | `3310`        | MyVector Docker port mapping           |
| `DATABASE`      | `mysqlclaw`   | Target database                        |

**MyVector Docker container must be running:**
```bash
docker run -d --name myvector-db -p 3310:3306 \
  -e MYSQL_ROOT_PASSWORD=<root_pw> \
  -e MYSQL_DATABASE=mysqlclaw \
  ghcr.io/askdba/myvector:mysql8.4
```

## Installation

**⚠️ Before installation**: Review the PRIVACY & CONSENT NOTICE above. Obtain explicit opt-in from all users before enabling auto-extraction or memory profiling.

```bash
# 1. Start MyVector container (if not running)
docker run -d --name myvector-db -p 3310:3306 \
  -e MYSQL_ROOT_PASSWORD=<root_pw> \
  -e MYSQL_DATABASE=mysqlclaw \
  ghcr.io/askdba/myvector:mysql8.4

# 2. Create a dedicated least-privilege user inside MyVector
docker exec -it myvector-db mysql -u root -p<root_pw> -e "
  CREATE USER IF NOT EXISTS 'mysqlclaw'@'%' IDENTIFIED BY '<strong_password>';
  GRANT SELECT, INSERT, UPDATE, DELETE ON mysqlclaw.* TO 'mysqlclaw'@'%';
  FLUSH PRIVILEGES;
"

# 3. Create .env file with the dedicated user's credentials
cat > .env <<'EOF'
MYSQL_USER=mysqlclaw
MYSQL_PASSWORD=<strong_password>
MYSQL_PORT=3310
DATABASE=mysqlclaw
EOF
chmod 600 .env

# 4. Apply schema with setup wizard
cd ~/.openclaw/workspace/skills/custom-mysql
./setup_wizard.sh

# 5. Run initial consolidation (DRY RUN first, then live)
cd ~/.openclaw/workspace
python3 scripts/memory_consolidation.py --user <your_discord_id> --dry-run
python3 scripts/memory_consolidation.py --user <your_discord_id>
```

**Auto-extraction is DISABLED by default.** To enable per-user after explicit opt-in:
```bash
export MYSQL_USER=mysqlclaw
export MYSQL_PASSWORD=<your_password>
python3 scripts/auto-extract.py --file /path/to/conversation.txt --user <discord_id> --dry-run
# Review output, then run without --dry-run
```

## Usage

```bash
# Query (SELECT-only)
custom_mysql.sh query "SELECT * FROM users LIMIT 5"

# Execute script (DML requires interactive confirmation)
custom_mysql.sh exec --file /path/to/scripts.sql

# Convenience commands:
custom_mysql.sh insert_interaction <uid> <dir> <topic> <summary> [sentiment] [is_important]
custom_mysql.sh insert_note <uid> <note> [category] [is_pinned]
custom_mysql.sh insert_context <uid> <key> <value> [type] [importance] [expires_at]
custom_mysql.sh insert_skill_usage <uid> <skill_name> [action] [status] [duration_ms] [error_type]
custom_mysql.sh insert_relationship <uid> <related_uid> <type> [strength] [trust] [notes]
custom_mysql.sh insert_mood <uid> <mood> [intensity] [trigger_topic] [confidence]
custom_mysql.sh insert_reminder <uid> <trigger_type> <condition> <text> [priority]
custom_mysql.sh insert_thought <uid> <thought> [type] [channel_id]
custom_mysql.sh insert_learning <type> <title> <description> [priority] [user] [skill]
custom_mysql.sh insert_event <type> <title> [description] [channel_id]

# Memory consolidation (v4.0.0):
python3 ~/.openclaw/workspace/scripts/memory_consolidation.py --user <uid>
python3 ~/.openclaw/workspace/scripts/memory_consolidation.py --all-users
```

## Data Retention & Deletion

### Retention Policies (configurable via `data_retention_policy` table, v5.0.1)
All retention defaults are configurable. Run `SELECT * FROM data_retention_policy;` to review.

| Data Type | Default Retention | Table |
|-----------|-------------------|-------|
| User interactions | 30 days | `user_interactions` |
| Mood states | 90 days | `user_mood` |
| HoloGraphic metadata | 30 days | `user_context` |
| Consolidation-derived | 90 days | `user_context` |
| **Agent reasoning (thought_stream)** | **7 days** | `thought_stream` |
| Synaptic memory | 365 days (with decay) | `synaptic_memory` |
| Community sentiment/trends | 90 days | `community_sentiment`, `trending_topics` |
| Activity heatmap | 90 days | `user_activity_heatmap` |
| Auto-extracted memories | 30 days | `memories` where source='auto' |
| Manual memories | 365 days | `memories` where source='manual' |
| Extraction quality logs | 30 days | `extraction_log` |
| Audit logs | 365 days | `audit_log` |
| Notes, relationships, preferences | Until explicitly deleted | `user_notes`, `user_relationships`, etc. |
| Reminders | Auto-deactivate after `max_triggers` | `proactive_reminders` |

**⚠️ Agent reasoning logs (`thought_stream`) default to 7-day retention.** Chain-of-thought data is sensitive and should not be retained long-term. Configure in `data_retention_policy`.

### Deletion
- Full user data deletion via `rollback_user.sql` covers all user-data tables
- Rollback procedure wipes all user-specific data while preserves schema
- **All deletions are logged to `audit_log`** (v5.0.1)

### Consent & Provenance (v5.0.1)
- **Auto-extraction is opt-in only** — disabled by default per-user (`extraction_config` table)
- Users must explicitly consent before auto-extraction is enabled
- Consent timestamp and method are recorded
- Inferred data is stored with lower confidence scores (≤ 0.7)
- Emotional/mood data requires confidence ≥ 0.7
- `agent_learnings` affecting behavior must be reviewed before activation
- Users can request full data deletion at any time

## Security (v5.0.1)

- **MyVector Docker container**: All SQL runs inside the container via `docker exec`
- **Dedicated least-privilege user required**: root/admin accounts explicitly rejected
- **Credentials via environment variables**: Python scripts load from `os.environ`. Shell scripts (`.sh`) load from `.env` file.
- **Password never on command line**: Uses temporary `--defaults-extra-file` with `chmod 600` for shell commands.
- **`.env` parsed safely**: KEY=VALUE line parsing only — never evaluated as shell code.
- `query` command is SELECT-only (no DML through query).
- DML requires interactive user confirmation (for agent-facing commands).
- Single-statement execution only (semicolons rejected).
- **DDL blocked at runtime**: `sql_safe_exec.sh` prevents DDL (DROP, TRUNCATE, CREATE, ALTER, GRANT, REVOKE) for agent-facing commands.
- **Schema migrations are a human admin task**: Upgrade scripts (`upgrade_vX.sql`) must be run directly via `docker exec` by an administrator with root privileges, not through the agent-facing wrappers.
- Table allowlist enforced (26 approved tables).
- Path traversal and sensitive file patterns blocked.
- Comment injection blocked.
- Hex-encoded string detection blocked.
- Proper MySQL string escaping via Python.
- Foreign key constraints prevent orphaned data.
- Script permissions: 700 (owner execute only).
- Config directory permissions: 700.
- **`audit_log` table**: Tracks all data access and modification for accountability (v5.0.1).
- **`extraction_config` table**: Enforces per-user opt-in for auto-extraction (v5.0.1).
- **`data_retention_policy` table**: Configurable retention limits for all data types (v5.0.1).

## Sentiment Scoring

- **Per interaction**: `user_interactions.sentiment` (enum) + `sentiment_score` (float, -1 to 1)
- **Per user trend**: Rolling average from recent interactions
- **Community-wide**: `community_sentiment` aggregated by time period
- **Mood impact**: Each interaction can shift user's mood (`mood_impact` field)
- **HindSight analysis**: Automated sentiment trend analysis during consolidation

## Engagement Patterns

- **Time of day**: When user is most active
- **Day of week**: Weekly activity cycles
- **Topic triggers**: What topics engage this user most
- **Channel preference**: Which channels they use
- **Response style**: How they prefer to interact
- **Session length**: Typical interaction duration
- **Activity bursts**: Periods of high activity

## Removed Features

- **Snapshot functionality removed (v1.1.7)`**: The `agent_config_files` table and related commands removed
- **Local MySQL dependency removed (v3.0.0)`**: Replaced with MyVector Docker container

## Change Log

See [changelog.md](changelog.md) for full version history.

## Setup Guide

For step-by-step instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

Visit <https://clawhub.ai/paradoxfuzzle/custom-mysql> for live updates.
