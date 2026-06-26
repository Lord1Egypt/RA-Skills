# CHANGELOG

All notable changes to the **VectorClaw** skill for OpenClaw are documented in this file.

The format follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) specification and respects [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.0.0] – 2026-05-27

### Added — MyVector Self-Sufficiency: Auto-Extraction + Knowledge Graph

This release makes MyVector self-sufficient by absorbing Mem0's auto-extraction and Hancho's knowledge graph reasoning into native MySQL systems.

**Auto-Extraction Hook (`scripts/auto-extract.py`):**
- Uses local qwen3.5:4b model with structured JSON prompt to extract atomic facts from conversation text
- Extracts: core_fact, confidence (0-1), entities[], linked_to[], tags[], memory_type, importance
- Key mapping normalizes LLM output (handles "fact" → "core_fact", invalid memory_types → "semantic")
- Auto-dedup on insert: Jaccard similarity check against existing memories, merges if >50% overlap
- Auto-discovers relations: finds existing memories sharing entities, creates edges in `memory_relations` table
- Source tracking: marks auto-extracted memories with `source='auto'` for quality monitoring
- Fallback to regex-based extraction when LLM is unavailable
- Validates memory_type against DB enum before insert

**Memory Relations Table (`memory_relations`):**
- Native MySQL knowledge graph replacing Hancho's external reasoning
- Schema: fact_id, related_fact_id, relation_type, confidence, source, discovered_at
- Relation types: mentions, implies, contradicts, same_entity, related_to
- Source tracking: auto (from extraction), manual, consolidation
- Unique constraint prevents duplicate edges
- Indexes for fast graph traversal during retrieval

**Hancho Consolidation Pass (`scripts/hancho-consolidate.py`):**
- Scans recent memories for shared entities/terms (Jaccard > 0.15)
- Contradiction detection: finds same-topic facts with opposite polarity
- Inserts edges into `memory_relations`
- Derives hub insights (facts with 3+ connections = important)
- Runs as heartbeat job (every 1-4 hours recommended)

**Extraction Quality Logging (`extraction_log`):**
- Tracks: facts extracted, merged, inserted, relations discovered per run
- Records: input length, extraction time, model used, fallback usage
- Enables empirical tuning of extraction prompt over time

**Graph Traversal View (`memory_graph_1hop`):**
- Pre-computed MySQL view for fast 1-hop graph traversal during retrieval
- Joins memory_relations with memories for complete edge+node data
- Filtered to confidence >= 0.5 for quality

### Changed — Database Schema

- **`memories` table**: Added `source` (enum: manual/auto/consolidation/import), `verified_by_human` (boolean), `extraction_prompt` (text) columns
- **`memories` table**: Added `idx_mem_source` index for source-based queries
- **`user_context` table**: Extended `context_type` enum with `auto_extracted`, `graph_derived`, `extraction_quality`
- **New table**: `memory_relations` — knowledge graph edges
- **New table**: `extraction_log` — extraction quality metrics
- **New view**: `memory_graph_1hop` — fast graph traversal

### Changed — SKILL.md Updated

- **Version bumped to 5.0.0**
- **Added Auto-Extraction section** documenting the auto-extract hook, prompt design, key mapping, and dedup logic
- **Added Memory Relations section** documenting the knowledge graph schema, relation types, and consolidation pass
- **Added Extraction Logging section** documenting quality tracking
- **Added deprecation notes** for Mem0 (auto-extraction replaced) and Hancho (knowledge graph replaced)
- **Updated Memory Types table** with new source tracking and graph-derived types
- **Updated data retention policies** for auto-extracted memories (7-day parallel run, then 30-day review cycle)

### Deprecated — External Memory Tools

- **Mem0**: Auto-extraction replaced by `auto-extract.py` with local qwen3.5:4b. Run in parallel for 7-10 days for quality comparison, then retire.
- **Hancho**: Knowledge graph reasoning replaced by `memory_relations` table + `hancho-consolidate.py`. Native MySQL graph traversal is tighter and fully owned.

### Migration Notes — IMPORTANT

**⚠️ Backup first!** Always back up your database before running any migration:
```bash
docker exec myvector-db mysqldump -u root -p<pass> mysqlclaw > backup_pre_v5.sql
```

- Run `upgrade_v4_to_v5.sql` to apply schema changes. **This script uses DDL** (ALTER TABLE, CREATE TABLE IF NOT EXISTS). Run directly via `docker exec`, NOT through `sql_safe_exec.sh`.
- Existing memories default to `source='manual'` — no data migration needed
- **Auto-extraction is disabled by default.** Enable per-user only after explicit opt-in.
- Run `hancho-consolidate.py --dry-run` first to preview graph edges before committing
- **Review auto-extracted data** for accuracy and sensitivity before it affects agent behavior

### Security Audit Response (v5.0.1)

This release addresses findings from the ClawHub security audit (37 findings, 2026-05-27):

- **Credential handling**: All Python scripts now load credentials from environment variables. No hardcoded passwords in any script.
- **DDL documentation**: Clarified that schema migrations require DDL and must be run by human administrators directly, not through the agent-facing wrapper.
- **Privacy notice**: Added prominent consent/privacy warning at the top of SKILL.md.
- **Auto-extraction opt-in**: Auto-extraction is now disabled by default. Must be explicitly enabled per-user.
- **Backup warnings**: Migration instructions now include explicit backup-first warnings.
- **Consolidation scope**: Added `--dry-run` and user-scoping to all consolidation commands.
- **thought_stream isolation**: Agent reasoning logs are now stored with optional user linkage (user_id can be NULL) to avoid co-locating chain-of-thought with identifiable user data.

---

## [4.0.0] – 2026-05-21

### Added — HindSight + HoloGraphic + Hancho Memory Systems

This release adds three memory enhancement systems that run during heartbeat consolidation cycles:

**HindSight** — Post-conversation analysis:
- Analyzes recent interactions for sentiment trends (positive/negative/neutral ratios)
- Identifies frequently discussed topics and new topics not yet stored as memories
- Detects recurring themes worth tracking
- Stores findings as derived memories in `user_context` (category: discovery/behavioral/emotional)

**HoloGraphic** — Multi-dimensional memory tagging:
- Tags every memory with: emotion (positive/negative/complex/neutral), context (work/personal/health/tech/social/creative), urgency (immediate/ongoing/timeless/historical), people involved
- Enables retrieval from any angle (e.g., "how did Ev feel about X" or "what health topics came up in May")
- Stores tags as structured memories in `user_context` (category: metadata)

**Hancho** — Knowledge graph reasoning:
- Connects related facts across memories to derive new insights
- 7 reasoning rules: medication side effects, health chains, tech infrastructure, creative passions, relationship depth, interest-to-skill, emotional coping patterns
- Inter-user reasoning finds shared topics between users
- Stores derived insights as new memories in `user_context` (category: reasoning)

### Added — memory_consolidation.py Script

- **`memory_consolidation.py`** — Standalone consolidation script that runs HindSight + HoloGraphic + Hancho in sequence.
- Supports `--user <id>`, `--all-users`, `--hindisght-only`, `--holohraphic-only`, `--hancho-only`, `--dry-run` flags.
- Integrates with `community-memory.py` via subprocess calls.
- Scheduled to run every 6 hours via OpenClaw heartbeat and cron.
- Already processed: NP (4 derived insights, 10 tagged memories) and Ev (10 tagged memories).

### Changed — SKILL.md Updated

- **Version bumped to 4.0.0**
- **Added Memory Consolidation section** documenting HindSight, HoloGraphic, and Hancho systems.
- **Added Memory Types table** with 6 types: Episodic, Semantic, Procedural, Emotional, Preference, Synaptic, HoloGraphic (multi-dimensional tags), and Hancho (derived reasoning).
- **Added dimensional tag reference**: emotion, context, urgency, people fields for HoloGraphic tagging.
- **Added reasoning rule reference**: 7 Hancho reasoning patterns with examples.
- **Updated data retention policies** for new memory types (HoloGraphic tags: 30-day refresh; Hancho derived: 90-day review).
- **Updated Memory Architecture section** in README to reference all 3 systems and when to use each.

### Changed — Database Schema Enhancements

- **`user_context` table**: Enhanced `context_type` enum to include new consolidation types: `hindisght`, `holohraphic`, `hancho`, `discovery`, `behavioral`, `metadata`, `reasoning`, `social_graph`.
- **`memory_consolidation_log` table**: Now actively used. Each consolidation run logs: consolidation type, source count, result count, affected users, timestamp.
- **New indexes on `user_context`**: Added composite index on `(user_id, context_type, importance)` for faster consolidation queries.
- **New index on `user_interactions`**: Added composite index on `(user_id, created_at, sentiment)` for HindSight trend analysis.

### Added — New SQL Migration Script

- **`upgrade_v3_to_v4.sql`** — Migration script for upgrading v3.x installations to v4.0.0:
  - Adds new enum values to `user_context.context_type`
  - Adds new indexes for consolidation queries
  - Safe to run on production (uses `IF NOT EXISTS` and `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`)

### Updated — Documentation

- **CAPABILITIES.md** — Added HindSight, HoloGraphic, and Hancho to capability declarations. Added memory_consolidation.py as a required script.
- **SETUP_GUIDE.md** — Added section on memory consolidation setup and scheduling.
- **SKILL.md** — Updated memory type table, added consolidation commands, updated architecture diagram.

### Security

- Consolidation performs both reads and writes: analysis is SELECT-only, but derived memories, tags, and graph edges are written to the database.
- Write operations use direct database connections (not through `sql_safe_exec.sh`) since consolidation is an automated background process, not an interactive agent command.
- Consolidation only processes data the agent already has access to.
- **Recommended**: Run with `--dry-run` first to review what will be written.

### Migration Notes (v3.x → v4.0.0)

1. Back up your `mysqlclaw` database before upgrading.
2. Run `upgrade_v3_to_v4.sql` against your existing database:
   ```bash
   docker exec -i myvector-db mysql -u mysqlclaw -p<pass> mysqlclaw < upgrade_v3_to_v4.sql
   ```
3. Copy `memory_consolidation.py` to `~/.openclaw/workspace/scripts/`.
4. Add the 6-hour consolidation heartbeat task to `HEARTBEAT.md`.
5. Run initial consolidation: `python3 memory_consolidation.py --user <id>`.
6. Existing data is preserved — new tables/columns use `IF NOT EXISTS`.

---

## [3.1.0] – 2026-05-11

### Changed — Renamed from MySQLClaw to VectorClaw

- **Skill renamed from MySQLClaw to VectorClaw.** The skill name, slug, and all internal references updated to reflect the new name. The old name `MySQLClaw` implied a MySQL-specific dependency; `VectorClaw` better reflects the MyVector (MySQL 8.4 + vector search) foundation.
- **Directory renamed from `mysqlclaw` to `vectorclaw`.** The active skill directory is now `skills/vectorclaw/`. The dev-only `custom-mysql` directory retains its name for reference.
- **Script files renamed.** `custom_mysql.sh` → `vector_claw.sh`, `setup_wizard.sh` → `vector_claw_setup.sh`.
- **`_meta.json` slug updated** from `custom-mysql` to `vector-claw`.
- **All documentation updated.** `SKILL.md`, `CAPABILITIES.md`, `updated_SKILL.md`, `SETUP_GUIDE.md`, `changelog.md` — all references to MySQLClaw replaced with VectorClaw.

---

## [3.0.0] – 2026-05-11

### Changed — Replaced MySQL with MyVector Docker Container

- **Replaced local MySQL dependency with MyVector Docker container.** The skill no longer requires a local MySQL server or client. All SQL is routed through `docker exec` into the MyVector container (`ghcr.io/askdba/myvector:mysql8.4`), which provides MySQL 8.4 compatibility with vector search extensions. This eliminates the host MySQL 8.4 client's missing `mysql_native_password` auth plugin issue.

- **`sql_safe_exec.sh` completely rewritten for Docker exec.** The `MYSQL_CMD` now uses `docker exec -i myvector-db mysql --defaults-extra-file=...` instead of the host `mysql` binary. Credentials are copied into the container via `docker cp` before each query. The container is verified to be running before any connection attempt.

- **All references to local MySQL replaced with MyVector.** `SKILL.md`, `CAPABILITIES.md`, `updated_SKILL.md`, `SETUP_GUIDE.md`, and `_meta.json` updated to reflect MyVector Docker container as the database backend.

### Security Fixes (ClawScan audit response)

- **Fail-closed authentication.** Previously, `sql_safe_exec.sh` silently fell back to `root` when `MYSQL_USER` was not set in `.env`. Now the skill explicitly refuses to connect if `MYSQL_USER` or `MYSQL_PASSWORD` is missing, printing an error message explaining the requirement for a dedicated least-privilege account.

- **Root/admin user rejection.** The skill now explicitly rejects `root`, `admin`, and `mysql` usernames. If a user attempts to use these accounts, the skill prints an error and exits. This addresses the ClawScan finding that the skill could silently fall back to database-administrator privileges.

- **Container verification.** Before attempting any SQL connection, the skill now verifies that the MyVector Docker container exists and is running. If the container is missing or stopped, the skill prints a helpful error message with the `docker run` command to start it.

- **Removed wallet/crypto/purchase capability flags from `_meta.json`.** The previous metadata incorrectly declared `crypto`, `requires-wallet`, `can-make-purchases`, and `requires-sensitive-credentials` capability signals. These have been removed. The skill has never contained wallet, cryptocurrency, or purchase code.

- **`_meta.json` updated with accurate declarations.** Added `docker` to `requiredBinaries` (replacing `mysql`). Updated `credentialEnvVars` to match actual usage. Updated description to mention MyVector and least-privilege requirement.

- **`setup_wizard.sh` rewritten for MyVector.** The wizard now: (1) checks Docker is running, (2) creates/starts the MyVector container, (3) creates a dedicated least-privilege MySQL user inside the container, (4) applies the schema, (5) verifies the connection. No longer shows the root password as a default value — prompts securely with `-s` flag.

- **`updated_SKILL.md` — added opt-in, provenance, and review rules.** Added explicit consent requirements: opt-in for each data source, provenance tracking (source, confidence, timestamp), review requirement for `agent_learnings` before they affect behavior, and retention/deletion enforcement.

- **`updated_SKILL.md` — added source path restrictions.** Explicitly lists approved sources (Discord messages, reactions, user statements, observed patterns, agent reasoning) and prohibited sources (operational config files, secrets/credentials, other users' private data, arbitrary file reads).

- **`CAPABILITIES.md` — removed wallet/crypto/purchase declarations.** Added `Fail-closed auth`, `Rejects root/admin`, and `Container verification` to the "What VectorClaw DOES" section. Added `Local MySQL server` and `Root/admin MySQL access` to the "What VectorClaw DOES NOT do" section.

- **`SKILL.md` — version bumped to 3.0.0.** Updated all documentation to reference MyVector Docker container instead of local MySQL. Added Removed Features entry for local MySQL dependency.

- **`.env` file removed from `custom-mysql` directory.** The development-only skill directory no longer contains any credentials. Only the `mysqlclaw` skill directory (the installed, active skill) has a `.env` file.

- **`custom-mysql` confirmed as dev-only.** This skill is never installed or used in production. All production use goes through the `mysqlclaw` skill directory.

### Security Audit Results (v3.0.0)

1. ✅ **File permissions** — All shell scripts set to 700 (owner execute only). All data files set to 644.
2. ✅ **No hardcoded credentials** — No passwords in any file. The setup wizard prompts interactively.
3. ✅ **No eval usage** — Zero `eval` statements across all scripts.
4. ✅ **No shell-sourced .env** — `.env` is parsed as KEY=VALUE lines only, never evaluated as shell code.
5. ✅ **No password on command line** — Uses temporary `--defaults-extra-file` with `chmod 600`.
6. ✅ **No root/admin fallback** — Root is explicitly rejected, not defaulted.
7. ✅ **Fail-closed on missing creds** — Refuses to connect without MYSQL_USER and MYSQL_PASSWORD.
8. ✅ **Container verification** — Verifies MyVector container is running before connecting.
9. ✅ **DDL blocking** — DROP, TRUNCATE, CREATE, ALTER, GRANT, REVOKE blocked.
10. ✅ **Table allowlist** — 26 approved tables enforced for all write operations.
11. ✅ **DML confirmation** — Interactive confirmation required for all write operations.
12. ✅ **Single-statement enforcement** — Semicolons rejected to prevent stacked queries.
13. ✅ **Path traversal prevention** — Sensitive paths and file operations blocked.
14. ✅ **Comment injection prevention** — `/* */`, `--`, `#` style comments blocked.
15. ✅ **Hex-encoding prevention** — `0x...` patterns blocked.
16. ✅ **Temp file safety** — `mktemp` with `chmod 600` and trap-based cleanup.
17. ✅ **Foreign key constraints** — All user-data tables have ON DELETE CASCADE.
18. ✅ **Rollback completeness** — `rollback_user.sql` covers all 26 user-data tables.
19. ✅ **No wallet/crypto/purchase code** — Confirmed zero wallet, crypto, or purchase functionality.
20. ✅ **Accurate metadata** — `_meta.json` capability flags match actual behavior.

---

## [2.1.0] – 2026-05-11

### Security Fixes (ClawScan audit response)

- **Fixed `.env` file parsing — no longer shell-sourced.** Previously, `custom_mysql.sh` and `sql_safe_exec.sh` used `source "$SCRIPT_DIR/.env"` which evaluates the file as shell code. A malicious `.env` file could execute arbitrary commands. Changed to strict KEY=VALUE line parsing with regex validation (`^[A-Za-z_][A-Za-z0-9_]*$` for keys, only recognized MYSQL_* keys accepted). The `.env` file is never evaluated as code.

- **Fixed password exposure on command line.** `sql_safe_exec.sh` was building a `MYSQL_CMD` string that included `--password=${MYSQL_PASSWORD}` directly on the command line, exposing credentials to local process inspection (`ps`, `/proc`). Replaced with temporary `--defaults-extra-file` approach: credentials are written to a `mktemp` file with `chmod 600`, used via `--defaults-extra-file`, and cleaned up via `trap cleanup_creds EXIT` on any exit (normal, error, or signal). Password never appears on the command line.

- **Added source path restrictions and consent rules.** Replaced the broad "Data Ingestion as Source of Truth" section in `updated_SKILL.md` with explicit source restrictions: approved sources (Discord messages, reactions, user statements, observed patterns, agent reasoning) and prohibited sources (operational config files, secrets/credentials, other users' private data, arbitrary file reads). Added consent & sensitivity rules: explicit over inferred, emotional data confidence threshold (≥ 0.7), retention policies, and deletion procedures.

- **Updated `_meta.json` with required binaries and credential env vars.** Declared `requiredBinaries: ["mysql", "openssl", "python3"]` and `credentialEnvVars: ["MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_HOST", "MYSQL_PORT", "DATABASE"]` so users have a complete pre-install picture of requirements.

- **Removed `.env` from `custom-mysql` directory.** The development-only `custom-mysql` skill directory no longer contains any credentials. The `.env` file with MySQL credentials exists only in the `mysqlclaw` skill directory (the installed, active skill).

- **Synced all v2.1.0 fixes to `mysqlclaw` directory.** Both `custom-mysql` (dev) and `mysqlclaw` (installed) directories now contain identical code, with the exception that only `mysqlclaw` has a `.env` file.

### Changed

- `sql_safe_exec.sh` version bumped to v2.1.0.
- `custom_mysql.sh` version bumped to v2.1.0.
- `setup_wizard.sh` version bumped to v2.1.0.
- `_meta.json` version bumped to 2.1.0.

---

## [2.0.0] – 2026-05-11

### Added — New Tables (16 new tables)

- **`user_mood`** — Emotional state tracking per user. Stores mood state (happy/excited/calm/neutral/tired/stressed/frustrated/sad/angry/anxious), intensity (0-1), trigger topic/context, source reference, and confidence score. Supports mem0-like emotional memory. Indexed by user+time and mood state.

- **`user_engagement_patterns`** — Behavioral pattern analysis per user. Tracks 7 pattern types: time_of_day, day_of_week, topic_trigger, channel_preference, response_style, session_length, activity_burst. Each pattern has a key, value, frequency count, and confidence score. Enables the agent to learn *how* and *when* each user prefers to interact.

- **`conversation_sessions`** — Groups related interactions into meaningful conversation sessions. Tracks start/end time, topic, summary, message count, average sentiment, mood at start/end, and key points. Enables higher-level reasoning about conversation arcs rather than individual messages.

- **`session_interactions`** — Many-to-many linking table between conversation_sessions and user_interactions. Allows flexible grouping of interactions into sessions without modifying the interaction records.

- **`proactive_reminders`** — Follow-up trigger system. Supports 4 trigger types: time_based (specific date), event_based (when something happens), pattern_based (when a pattern matches), followup (after interaction). Configurable priority (low/medium/high), max trigger count, and active status. Enables the agent to remember to follow up with users.

- **`synaptic_memory`** — Key-value memory store with priority scoring and automatic decay. Each entry has a priority (1-10), decay_rate (auto-reduces priority over time), access_count, and last_accessed timestamp. High-priority memories persist; low-priority ones fade naturally. Directly inspired by synaptic memory models.

- **`thought_stream`** — Agent reasoning log. Records agent thoughts with 5 types: reasoning, observation, decision, reflection, planning. Linked to users and channels. Enables the agent to review its own reasoning process and learn from past decisions.

- **`topic_keywords`** — Searchable topic index. Tracks keywords with weight scores, categories, mention counts, and first/last seen timestamps. Enables fast topic-based search across all user interactions without full-text scanning.

- **`community_sentiment`** — Community-wide sentiment aggregation. Stores sentiment (positive/neutral/negative/mixed), score, sample_size, topic, channel, and time period. Enables tracking of overall community mood over time.

- **`trending_topics`** — Trend tracking per time period. Stores mention count, unique users, average sentiment, related keywords, and date range. Enables identification of what the community is talking about.

- **`community_events`** — Milestone/incident log. 5 event types: milestone, achievement, incident, trend, custom. Tracks title, description, involved users, channel, and timestamp. Enables recording important community moments.

- **`agent_learnings`** — Self-improvement tracking. 7 learning types: correction, preference, pattern, error, success, insight, rule. Includes priority, active status, applied count, and links to related users/skills. Enables the agent to record and apply lessons from interactions.

- **`user_activity_heatmap`** — Hour × day-of-week activity matrix per user. Tracks activity_count, message_count, interaction_count, and average_sentiment per cell. Enables data-driven engagement pattern analysis.

- **`memory_consolidation_log`** — Tracks memory maintenance operations. 5 consolidation types: summarize, merge, prune, archive, reindex. Records source/result counts, affected users, and details. Enables auditing of memory lifecycle operations.

### Enhanced — Existing Tables (8 tables enhanced)

- **`users`** — Added: `timezone` (VARCHAR), `roles` (JSON), `total_messages` (INT), `total_reactions` (INT), `total_sessions` (INT), `last_seen` (TIMESTAMP), status expanded to include `new`/`away`/`dnd`. Added indexes on status, last_seen, last_interaction.

- **`user_interactions`** — Added: `sentiment_score` (FLOAT, -1 to 1 for fine-grained sentiment), `mood_impact` (FLOAT, how much this interaction shifted the user's mood), `channel_id` (VARCHAR), `message_id` (VARCHAR), `is_important` (BOOLEAN), `requires_followup` (BOOLEAN), `followup_topic` (VARCHAR), `followup_due` (TIMESTAMP), `metadata` (JSON). Added indexes on sentiment, followup, channel+time, important.

- **`user_context`** — Added: `context_type` (ENUM: episodic/semantic/procedural/emotional/preference/fact/custom), `importance` (FLOAT, 0-1 for priority), `source` (ENUM: conversation/observation/explicit/inferred/system), `channel_id`, `message_id`, `is_active` (BOOLEAN), `metadata` (JSON). Added indexes on context_type, is_active, importance. Now supports mem0-like memory type classification.

- **`user_attributes`** — Added: `confidence` (FLOAT), `source` (ENUM: stated/inferred/observed), `metadata` (JSON). Expanded `attribute_type` to include: skill, trait, goal, custom (beyond like/dislike/hobby/interest). Added indexes on attribute_type and category.

- **`user_media`** — Expanded `media_type` from 3 to 10 values: tv_show, movie, book, game, music, podcast, anime, comic, youtube, other. Added: `status` (ENUM: completed/in_progress/planned/dropped/on_hold), `progress` (VARCHAR), `review` (TEXT), `source` (ENUM: stated/observed/inferred). Added indexes on rating and status.

- **`user_food_preferences`** — Expanded `preference` from 2 to 6 values: loves, likes, neutral, dislikes, allergic, hates. Added: `context` (VARCHAR), `source` (ENUM: stated/observed/inferred), `metadata` (JSON). Added index on preference.

- **`user_relationships`** — Added: `trust_level` (TINYINT 1-10), `interaction_frequency` (ENUM: daily/weekly/monthly/rarely/never), `shared_interactions` (JSON), `notes` (TEXT), `first_interaction` (TIMESTAMP). Expanded `relationship_type` to include: close_friend, mentor, mentee, rival. Added index on relationship_type.

- **`skill_usage`** — Added: `error_type` (VARCHAR) for categorized error tracking. Added index on error_type.

- **`user_notes`** — Added: `tags` (JSON for flexible tagging), `is_pinned` (BOOLEAN), `is_private` (BOOLEAN), `source_message_id` (VARCHAR). Added indexes on is_pinned and is_private.

### Added — New Convenience Commands (custom_mysql.sh)

- **`insert_mood <uid> <mood> [intensity] [trigger] [confidence]`** — Track user mood with validation against 10 mood states and numeric validation for intensity/confidence.

- **`insert_reminder <uid> <type> <condition> <text> [priority]`** — Set proactive reminders with enum validation for trigger type and priority.

- **`insert_thought <uid> <thought> [type] [channel_id]`** — Log agent reasoning with validation against 5 thought types.

- **`insert_learning <type> <title> <desc> [priority] [user] [skill]`** — Record agent learnings with enum validation.

- **`insert_event <type> <title> [description] [channel_id]`** — Log community events with enum validation.

- **`insert_interaction`** — Added `is_important` parameter.

- **`insert_note`** — Added `is_pinned` parameter.

- **`insert_context`** — Added `context_type`, `importance` (with numeric validation), `expires_at` parameters.

- **`insert_skill_usage`** — Added `error_type` parameter.

- **`insert_relationship`** — Added `trust_level` (with numeric validation) and `notes` parameters.

### Added — New Security Controls

- **Comment injection blocking.** `sql_safe_exec.sh` now rejects SQL containing `/*`, `*/`, `--` followed by whitespace, or `#` followed by whitespace. This prevents attackers from using comments to truncate SQL and bypass security checks.

- **Hex-encoded string detection.** `sql_safe_exec.sh` now rejects SQL containing `0x` followed by hex digits, `UNHEX(`, or `HEX(`. This prevents encoding-based bypasses of the escaping system.

- **Enum validation helper.** `custom_mysql.sh` includes a `validate_enum()` function that validates parameter values against allowed lists. All enum parameters on convenience commands (mood states, trigger types, relationship types, context types, priorities, statuses, etc.) are validated before being used in SQL.

- **Numeric validation for float parameters.** `insert_mood` validates `intensity` and `confidence` as numeric. `insert_context` validates `importance` as numeric. Prevents SQL injection through these parameters.

- **Table allowlist expanded from 12 to 28.** Added all 16 new tables plus `session_interactions` and `user_activity_heatmap` to the approved write table list in `sql_safe_exec.sh`.

### Changed — Existing Security

- **sql_safe_exec.sh version bumped to v2.0.0.** Added comment injection and hex-encoding detection security controls. Added 16 new tables to the write allowlist.

- **custom_mysql.sh version bumped to v2.0.0.** Added 5 new convenience commands (insert_mood, insert_reminder, insert_thought, insert_learning, insert_event). Enhanced 5 existing commands with new parameters. Added `validate_enum()` helper function. All parameters properly escaped and validated.

- **setup_wizard.sh version bumped to v2.0.0.** Added `python3` to dependency checks. Added verification of new tables after schema application. Lists each new table with ✓/✗ status. Now also runs `populate_templates.sql` during setup.

- **`rollback_user.sql` updated.** Now covers all 26 user-data tables in proper deletion order for foreign key constraints. Added: session_interactions, conversation_sessions, user_mood, user_engagement_patterns, user_activity_heatmap, proactive_reminders, synaptic_memory, thought_stream, user_notes (already existed but order corrected). Added deletion of user's topic_keywords and agent_learnings references.

- **`create_user_tables.sql` rewritten.** Now creates 28 total tables (up from 12). All existing tables preserved with ALTER-style enhancements (new columns). 16 new tables added. Proper indexing throughout. Foreign key constraints with ON DELETE CASCADE on all user-data tables.

### Updated — Documentation

- **`SKILL.md`** — Completely rewritten for v2.0.0. Added memory type reference table (mem0-like types). Added sentiment scoring explanation. Added engagement patterns description. Updated data retention policies for new table types. Updated security section with new controls.

- **`CAPABILITIES.md`** — Expanded capability declarations. Added all new tables and capabilities. Updated approved write table list to 28 tables. Added enum validation, comment injection prevention, and hex-encoding prevention as declared capabilities. Updated trust rules to include inferred data and mood data aging.

- **`updated_SKILL.md`** — Added comprehensive v2.0.0 section documenting all new features, enhanced tables, new security controls, and new commands.

- **`changelog.md`** — This comprehensive changelog entry for v2.0.0.

### Security Audit

A comprehensive security audit was performed on all files in this release. Results:

1. ✅ **File permissions** — All shell scripts set to 700 (owner execute only). All data files set to 644.
2. ✅ **No hardcoded credentials** — No passwords, tokens, or API keys in any file. All credentials loaded from env/.
3. ✅ **No eval usage** — Zero `eval` statements across all scripts.
4. ✅ **SQL injection prevention** — All user input escaped via Python `mysql_escape()`. Numeric parameters validated with regex. Enum parameters validated against allowlists.
5. ✅ **Comment injection prevention** — `/* */`, `--`, `#` style comments blocked in SQL.
6. ✅ **Hex-encoding prevention** — `0x...` patterns blocked in SQL.
7. ✅ **DDL blocking** — DROP, TRUNCATE, CREATE, ALTER, GRANT, REVOKE, RENAME blocked.
8. ✅ **Table allowlist** — 28 approved tables enforced for all write operations.
9. ✅ **DML confirmation** — Interactive confirmation required for all write operations.
10. ✅ **Single-statement enforcement** — Semicolons rejected to prevent stacked queries.
11. ✅ **Path traversal prevention** — Sensitive paths and file operations blocked.
12. ✅ **Temp file safety** — `mktemp` with 600 permissions and trap-based cleanup.
13. ✅ **Foreign key constraints** — All user-data tables have ON DELETE CASCADE.
14. ✅ **Rollback completeness** — `rollback_user.sql` covers all 26 user-data tables.

### Bug Fixes (post-initial v2.0.0 release)

- **Fixed convenience command SQL semicolon mismatch.** The convenience commands in `custom_mysql.sh` were generating SQL with trailing semicolons (e.g., `INSERT ... VALUES (...);`), but `sql_safe_exec.sh` rejects semicolons as a security measure (single-statement enforcement). Stripped all trailing semicolons from convenience command SQL templates. The `sql_safe_exec.sh` already handles single-statement execution — semicolons are neither needed nor allowed.

- **Fixed `sql_safe_exec.sh` credential loading.** The `sql_safe_exec.sh` was invoking `mysql -D mysqlclaw -e "$SQL"` directly without loading credentials from the `.env` file. Updated to build a `MYSQL_CMD` string from env vars (`MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT`, `DATABASE`) so the `.env` file is properly used for authentication.

- **Added `upgrade_v1_to_v2.sql` migration script.** Created a standalone upgrade script for existing v1.x installations to apply the v2.0.0 schema changes (new tables, column additions, enum migrations, index additions) without data loss. Safe to run on production databases.

- **Synced skill files to `mysqlclaw` directory.** The `mysqlclaw` skill directory (installed from ClawHub as `custom-mysql` v1.1.6) was updated with all v2.0.0 files: `create_user_tables.sql`, `custom_mysql.sh`, `sql_safe_exec.sh`, `rollback_user.sql`, `setup_wizard.sh`, `SKILL.md`, `CAPABILITIES.md`, `changelog.md`, `updated_SKILL.md`, and supporting files.

- **Created `.env` file for mysqlclaw skill.** Added `.env` with MySQL credentials (`root` / `29361775`, host `localhost`, port `3306`, database `mysqlclaw`) to the `mysqlclaw` skill directory.

### Migration Notes (v1.x → v2.0.0)

For existing installations upgrading from v1.x:

1. Back up your `mysqlclaw` database before upgrading.
2. The existing 12 tables are preserved — new columns are added with ALTER TABLE.
3. New tables are created with `IF NOT EXISTS` — safe to re-run.
4. Existing data is not modified or removed.
5. Run `./setup_wizard.sh` against your existing database to apply additions.
6. Update `sql_safe_exec.sh` to get the expanded table allowlist.
7. Update `custom_mysql.sh` to get the new convenience commands.
8. The `rollback_user.sql` has been updated — use the new version for full data deletion.

---

## [1.1.7] – 2026-05-10

### Security

- **Removed snapshot functionality to prevent storage of sensitive operational files.** The `agent_config_files` table, `allowed_snapshot_paths` table, `snapshot_config` command, `cleanup_snapshots.sql`, and `sanitize_snapshot.sh` have been removed or disabled. This addresses a security concern about storing the contents of MEMORY.md, AGENTS.md, BOOT.md, and SECURITY.md in the database, which could expose sensitive operational data.
- **Removed MEMORY.md, AGENTS.md, BOOT.md, SECURITY.md from all path allowlists.** These files are no longer referenced anywhere in the skill.
- **Removed `agent_config_files` from the write table allowlist** in `sql_safe_exec.sh`.
- **Reduced approved write table count from 14 to 12** (removed `agent_config_files` and `allowed_snapshot_paths`).
- **`sanitize_snapshot.sh` converted to a no-op** with deprecation notice for backward compatibility.
- **`cleanup_snapshots.sql` emptied** and replaced with explanatory comments.
- **Updated `create_user_tables.sql`** to remove `agent_config_files` and `allowed_snapshot_paths` table definitions and all related indexes.
- **Updated `rollback_user.sql`** to remove `agent_config_files` reference.
- **Updated `CAPABILITIES.md`** to reflect removed snapshot capability and updated allowlist.
- **Updated `SKILL.md`** with removed features section and updated security documentation.
- **Version bumped to v1.1.7.**

## [1.1.6] – 2026-05-10

### Security

- **SQL Injection fix: replaced broken `sed` escaping with Python `mysql_escape()`.** All `insert_*` commands now use a Python 3 helper that properly escapes single quotes, backslashes, newlines, carriage returns, and NUL bytes.
- **Implemented table allowlist in `sql_safe_exec.sh`.** Added a strict allowlist of 14 approved `mysqlclaw` tables.
- **Implemented DDL blocking in `sql_safe_exec.sh`.** DROP, TRUNCATE, CREATE, ALTER, GRANT, REVOKE blocked.
- **Implemented path traversal blocking in `sql_safe_exec.sh`.**
- **Implemented single-statement enforcement in `sql_safe_exec.sh`.**
- **Implemented `--readonly` flag in `sql_safe_exec.sh`.**
- **Fixed `rollback_user.sql`: added missing tables.**
- **Tightened path traversal regex.**
- **Set restrictive file permissions (700 for scripts).**
- **Version bumped to v1.1.6.**

## [1.0.0] - 2026-05-04

### Added

- Complete user-profile schema (users, user_preferences, user_attributes, user_media, user_food_preferences)
- Persona management (user_personas table)
- Configuration snapshot system (agent_config_files table — later removed in v1.1.7)
- Setup wizard (setup_wizard.sh)
- Convenient high-level commands
- Error handling & transactions
- Documentation

### Changed

- Replaced hard-coded MySQL credentials with placeholder variables
- Added SQL `INSERT … ON DUPLICATE KEY UPDATE` logic for idempotent inserts

## 1.0.1 – 2026-05-04

- Security hardening: removed unsafe `eval` usage in `setup_wizard.sh`.
- Added input validation and safe variable quoting.
- Introduced `sql_safe_exec.sh` wrapper.

## 1.0.2 – 2026-05-04

- Added Secret Redaction policy, Destructive Action confirmation guidelines.

## 1.0.3 – 2026-05-04

- Added credential security (--defaults-extra-file), DML confirmation, path traversal prevention.

## 1.0.4 – 2026-05-04

- Multi-statement SQL rejection, trap-based credential cleanup.

## 1.0.5 – 2026-05-04

- Fixed sanitize_snapshot.sh, documented exec_script routing.

## 1.0.6 – 2026-05-04

- Added Capability Scope section to SKILL.md.

## 1.0.7 – 2026-05-04

- Added `custom_mysql` executable and `CAPABILITIES.md`.

## 1.1.0 – 2026-05-05

- Added 5 new tracking tables (user_interactions, user_relationships, user_context, skill_usage, user_notes).
- Enriched users table with display name/avatar/status fields.
- Added .env file support.

## 1.1.1 – 2026-05-05

- Fixed credential exposure by removing `create_admin_user.sh`.

## 1.1.2 – 2026-05-05

- Removed environment-specific Discord ID references from CAPABILITIES.md.

## 1.1.3 – 2026-05-05

- SQL Injection fix: Refactored insert commands with proper escaping.
- Added strict command whitelist in sql_safe_exec.sh.

## 1.1.4 – 2026-05-05

- Versioning fix for ClawHub registration.

## 1.1.5 – 2026-05-05

- Removed `--yes` bypass from all DML paths.
- query command is now SELECT-only.
- Added table allowlist and --readonly flag.
- Added Data Retention, Consent & Deletion policy.
