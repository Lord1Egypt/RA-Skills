# Custom MySQL Skill v3.0.0

This skill allows interaction with a MyVector MySQL database for deep community memory storage. It is security-hardened with a 26-table write allowlist, enum validation, comment injection prevention, hex-encoding detection, fail-closed auth, and root/admin rejection. v3.0.0 replaces the local MySQL dependency with MyVector (MySQL 8.4 + vector search) running in a Docker container.

## What's New in v3.0.0

### MyVector Docker Container
- **Replaces local MySQL entirely**: No local MySQL server or client required
- All SQL is routed through `docker exec` into the MyVector container
- MyVector provides MySQL 8.4 compatibility with vector search extensions
- Container must be running before the skill can connect
- Credentials are passed via temporary `--defaults-extra-file` (never on command line)

### Security: Fail-Closed Auth
- **Refuses to connect** if `MYSQL_USER` or `MYSQL_PASSWORD` is missing from `.env`
- **Explicitly rejects** root, admin, and mysql usernames
- Requires a dedicated least-privilege MySQL account
- Verifies MyVector Docker container is running before attempting connection

### Security: Safe .env Parsing
- `.env` file is parsed as KEY=VALUE lines only — never evaluated as shell code
- Only recognized MYSQL_* keys are accepted
- Keys validated against `^[A-Za-z_][A-Za-z0-9_]*$` regex

### Updated Existing Tables
- **`users`**: Added timezone, roles, activity stats (messages, reactions, sessions), last_seen
- **`user_interactions`**: Added sentiment_score, mood_impact, followup flags, channel_id, message_id, is_important
- **`user_context`**: Added context_type (episodic/semantic/procedural/emotional), importance, source, is_active
- **`user_attributes`**: Added confidence, source (stated/inferred/observed), expanded types (skill, trait, goal, custom)
- **`user_media`**: Expanded to 10 media types (game, music, podcast, anime, comic, youtube, other), added status/progress
- **`user_food_preferences`**: Expanded preference scale (loves/likes/neutral/dislikes/allergic/hates)
- **`user_relationships`**: Added trust_level, interaction_frequency, shared_interests, expanded types (close_friend, mentor, mentee, rival)
- **`skill_usage`**: Added error_type column
- **`user_notes`**: Added tags, is_pinned, is_private, source_message_id

## Commands

### Execute SQL Query
```bash
custom_mysql query "YOUR_SQL_QUERY_HERE"
```

### Execute Script
```bash
custom_mysql execute_script --file /path/to/your/script.sql
```

### Insert Interaction
```bash
custom_mysql insert_interaction <user_id> <direction> <topic> <summary> [sentiment] [is_important]
```

### Insert Note
```bash
custom_mysql insert_note <user_id> <note> [category] [is_pinned]
```

### Insert Context (mem0-like)
```bash
custom_mysql insert_context <user_id> <key> <value> [type] [importance] [expires_at]
```
Types: `episodic`, `semantic`, `procedural`, `emotional`, `preference`, `fact`, `custom`

### Insert Skill Usage
```bash
custom_mysql insert_skill_usage <user_id> <skill_name> [action] [status] [duration_ms] [error_type]
```

### Insert Relationship
```bash
custom_mysql insert_relationship <user_id> <related_user_id> <type> [strength] [trust] [notes]
```

### Insert Mood
```bash
custom_mysql insert_mood <user_id> <mood> [intensity] [trigger_topic] [confidence]
```
Moods: `happy`, `excited`, `calm`, `neutral`, `tired`, `stressed`, `frustrated`, `sad`, `angry`, `anxious`

### Insert Reminder
```bash
custom_mysql insert_reminder <user_id> <trigger_type> <condition> <text> [priority]
```
Trigger types: `time_based`, `event_based`, `pattern_based`, `followup`

### Insert Thought
```bash
custom_mysql insert_thought <user_id> <thought> [type] [channel_id]
```
Thought types: `reasoning`, `observation`, `decision`, `reflection`, `planning`

### Insert Learning
```bash
custom_mysql insert_learning <type> <title> <description> [priority] [user] [skill]
```
Learning types: `correction`, `preference`, `pattern`, `error`, `success`, `insight`, `rule`

### Insert Community Event
```bash
custom_mysql insert_event <type> <title> [description] [channel_id]
```
Event types: `milestone`, `achievement`, `incident`, `trend`, `custom`

## Configuration

Before using this skill, set the following environment variables:

- `MYSQL_USER`: Dedicated least-privilege MySQL username (NOT root)
- `MYSQL_PASSWORD`: The user's password
- `MYSQL_PORT`: MyVector Docker port (default: 3310)
- `DATABASE`: The MySQL database name (default: mysqlclaw)

**Example setup:**
```bash
export MYSQL_USER="mysqlclaw"
export MYSQL_PASSWORD="your_secure_password"
export MYSQL_PORT="3310"
export DATABASE="mysqlclaw"
```

Or create a `.env` file in the skill directory (chmod 600).

**Prerequisites:**
- Docker must be installed and running
- MyVector container must be running: `docker run -d --name myvector-db -p 3310:3306 -e MYSQL_ROOT_PASSWORD=<pw> -e MYSQL_DATABASE=mysqlclaw ghcr.io/askdba/myvector:mysql8.4`
- A dedicated least-privilege MySQL user must be created inside the container

## Installation for New Users

1. **Start MyVector container:**
   ```bash
   docker run -d --name myvector-db -p 3310:3306 \
     -e MYSQL_ROOT_PASSWORD=<root_pw> \
     -e MYSQL_DATABASE=mysqlclaw \
     ghcr.io/askdba/myvector:mysql8.4
   ```

2. **Create dedicated least-privilege user:**
   ```bash
   docker exec -it myvector-db mysql -u root -p<root_pw> -e "
     CREATE USER IF NOT EXISTS 'mysqlclaw'@'%' IDENTIFIED BY '<strong_password>';
     GRANT SELECT, INSERT, UPDATE, DELETE ON mysqlclaw.* TO 'mysqlclaw'@'%';
     FLUSH PRIVILEGES;
   "
   ```

3. **Copy the Skill:** Copy the entire `custom_mysql` directory to `~/.openclaw/workspace/skills/`

4. **Set Environment Variables:** Set required env vars or create `.env` file

5. **Initialize Database Schema:**
   ```bash
   cd ~/.openclaw/workspace/skills/custom-mysql
   ./setup_wizard.sh
   ```

6. **Run Commands:** Use `custom_mysql query`, `custom_mysql insert_*`, etc.

---

## Data Ingestion — Source Restrictions & Consent Rules

This skill is designed to be the central hub for community user data. When ingesting data:

### ✅ Approved Sources:
- **Direct Discord messages** — messages sent by users in Discord channels/DMs
- **Discord reactions** — emoji reactions made by users
- **User-provided statements** — explicit preferences, facts, or corrections stated by users
- **Observed interaction patterns** — engagement times, topic preferences, channel usage
- **Agent reasoning** — thoughts, decisions, reflections logged by the agent

### ❌ Prohibited Sources:
- **Operational config files** — never store contents of MEMORY.md, AGENTS.md, USER.md, IDENTITY.md, SOUL.md, BOOT.md, SECURITY.md, TOOLS.md, CODE.md, or any other workspace configuration files
- **Secrets/credentials** — API keys, tokens, passwords, private keys
- **Other users' private data** — data about user A shared by user B without user A's consent
- **Arbitrary file reads** — no reading of local filesystem files not explicitly listed above

### Consent & Sensitivity Rules:
- **Explicit over inferred** — mark inferred data with `source: 'inferred'` and lower confidence
- **Emotional data** — mood tracking should be based on clear expression, not speculation (confidence ≥ 0.7)
- **Sensitive memories** — flag with appropriate importance; respect user requests for deletion
- **Opt-in required** — explicit user consent required before storing sensitive personal data
- **Provenance tracking** — all records should include source, confidence, and timestamp
- **Review before acting** — `agent_learnings` and rule-like memories must be reviewed before affecting future behavior

### Retention & Deletion:
- Interaction logs: 30-day rolling window
- Mood data: 90-day rolling window
- Thought stream: 30-day rolling window
- Synaptic memory: auto-decay via `decay_rate`
- Full user data deletion via `rollback_user.sql` covers all 26 user-data tables

### Storage Best Practices:
- Use `custom_mysql insert_*` commands (not raw SQL) for all writes
- Validate enum parameters against allowed values
- Escape all user input via the built-in Python `mysql_escape()`
- Never construct SQL by concatenating raw user input
- Use `query` command for all reads (SELECT-only)
- Use `exec --file` with reviewed scripts for batch operations
