# MySQL & MyVector Setup Guide for Agents

This document provides step-by-step instructions for agents to install MySQL, configure the `mysqlclaw` database with proper security, and set up MyVector for vector search.

---

## Part 1: Install MySQL Server

```bash
# Install MySQL server
sudo apt update && sudo apt install -y mysql-server

# Run secure installation (set root password, remove anonymous users, etc.)
sudo mysql_secure_installation

# Start and enable MySQL
sudo systemctl start mysql
sudo systemctl enable mysql
```

Verify installation:
```bash
mysql --version
sudo systemctl status mysql
```

---

## Part 2: Create the `mysqlclaw` Database and Users

Log in as root and run:

```sql
-- Create the database with proper character set
CREATE DATABASE IF NOT EXISTS mysqlclaw
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Admin user (full control, only for initial setup and maintenance)
CREATE USER IF NOT EXISTS 'mysqlclaw_admin'@'localhost'
  IDENTIFIED BY 'YourStrongAdminPasswordHere123!';

GRANT ALL PRIVILEGES ON mysqlclaw.* TO 'mysqlclaw_admin'@'localhost';

-- Least-privileged user (for daily use by VectorClaw skill)
-- Only has SELECT, INSERT, UPDATE, DELETE — no DDL, no DROP, no GRANT
CREATE USER IF NOT EXISTS 'mysqlclaw'@'localhost'
  IDENTIFIED BY 'YourStrongLeastPrivPasswordHere456!';

GRANT SELECT, INSERT, UPDATE, DELETE ON mysqlclaw.* TO 'mysqlclaw'@'localhost';

FLUSH PRIVILEGES;
```

**Important security notes:**
- Replace the example passwords with strong random passwords (32+ chars)
- The `mysqlclaw` user should NEVER have DDL privileges (CREATE, ALTER, DROP, GRANT)
- Store passwords in the skill's `.env` file with `chmod 600` permissions
- The admin user should only be used for schema migrations and maintenance

Verify the users:
```sql
SELECT user, host, plugin FROM mysql.user WHERE user LIKE 'mysqlclaw%';
SHOW GRANTS FOR 'mysqlclaw'@'localhost';
```

---

## Part 3: Set Up MyVector (Vector Search Plugin)

MyVector adds vector similarity search capabilities to MySQL. The easiest way is using the official Docker container.

### Option A: Docker (Recommended)

```bash
# Pull and run MyVector container
docker run -d \
  --name myvector-db \
  -p 3310:3306 \
  -e MYSQL_ROOT_PASSWORD=myvector \
  -e MYSQL_DATABASE=mysqlclaw \
  -v myvector-data:/var/lib/mysql \
  ghcr.io/askdba/myvector:mysql8.4
```

**Notes:**
- Port `3310` is used to avoid conflicts with any existing MySQL on `3306`
- The `mysqlclaw` database is created automatically
- Data persists in the `myvector-data` Docker volume

Verify MyVector is running:
```bash
docker ps | grep myvector
docker exec -it myvector-db mysql -u root -pmyvector -e "SELECT VERSION();"
```

### Option B: Install MyVector Plugin on Existing MySQL

If you already have MySQL running and want to add MyVector directly:

```bash
# Download the MyVector plugin (check GitHub for latest release)
# https://github.com/askdba/myvector

# Install the plugin
mysql -u root -p -e "
  INSTALL PLUGIN myvector SONAME 'myvector.so';
";
```

---

## Part 4: Apply the VectorClaw Schema

After MySQL and MyVector are running, apply the skill's database schema:

```bash
cd ~/.openclaw/workspace/skills/mysqlclaw

# Set up .env with your credentials
cat > .env << 'EOF'
MYSQL_USER=mysqlclaw
MYSQL_PASSWORD=YourStrongLeastPrivPasswordHere456!
MYSQL_HOST=localhost
MYSQL_PORT=3310
DATABASE=mysqlclaw
EOF
chmod 600 .env

# Run the setup wizard
./setup_wizard.sh
```

Or apply the schema directly:
```bash
mysql -u mysqlclaw -p -h 127.0.0.1 -P 3310 mysqlclaw < create_user_tables.sql
mysql -u mysqlclaw -p -h 127.0.0.1 -P 3310 mysqlclaw < populate_templates.sql
```

---

## Part 5: Verify Everything Works

```bash
cd ~/.openclaw/workspace/skills/mysqlclaw

# Test query
./custom_mysql.sh query "SELECT COUNT(*) FROM users;"

# Test insert
echo "yes" | ./custom_mysql.sh insert_interaction \
  "agent_test" inbound "setup verification" "Testing VectorClaw after install" positive

# Verify
./custom_mysql.sh query "SELECT * FROM user_interactions ORDER BY created_at DESC LIMIT 1;"
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│                  Agent                       │
│          (custom_mysql.sh commands)          │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│           sql_safe_exec.sh                   │
│  • Single-statement enforcement              │
│  • DDL blocking                              │
│  • Table allowlist (28 tables)               │
│  • Comment injection blocking                │
│  • Hex-encoding detection                    │
│  • DML interactive confirmation              │
│  • Credentials via --defaults-extra-file     │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│     MyVector DB (MySQL 8.4 + vectors)       │
│     Port 3310 / Database: mysqlclaw          │
│                                              │
│  28 tables:                                  │
│  • users, user_preferences, user_attributes  │
│  • user_media, user_food_preferences         │
│  • user_personas, persona_templates          │
│  • user_interactions, conversation_sessions  │
│  • session_interactions, user_relationships  │
│  • user_context, skill_usage, user_notes     │
│  • user_mood, user_engagement_patterns       │
│  • user_activity_heatmap, proactive_reminders│
│  • synaptic_memory, thought_stream           │
│  • topic_keywords, community_sentiment       │
│  • trending_topics, community_events         │
│  • agent_learnings, memory_consolidation_log │
└─────────────────────────────────────────────┘
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Access denied for user 'mysqlclaw'` | Check `.env` credentials match the MySQL user |
| `Can't connect to MySQL server` | Verify MySQL is running: `sudo systemctl status mysql` |
| `Plugin 'myvector' not found` | Use the Docker image which includes MyVector pre-installed |
| `Table doesn't exist` | Run `create_user_tables.sql` to apply the schema |
| `ERROR: Multi-statement SQL not allowed` | Remove semicolons from SQL — `sql_safe_exec.sh` handles single statements |
| Port 3306 conflict | MyVector Docker uses port 3310 by default |

---

## Part 7: v5.0.0 — MyVector Self-Sufficiency Setup

v5.0.0 adds auto-extraction and knowledge graph capabilities that replace Mem0 and Hancho.

### Apply v5 Schema Migration

```bash
# Back up first
docker exec myvector-db mysqldump -u root -p<pass> jerith > backup_pre_v5.sql

# Apply migration
docker exec -i myvector-db mysql -u root -p<pass> jerith < upgrade_v4_to_v5.sql
```

### Set Up Auto-Extraction Hook

```bash
# Test with dry run
python3 scripts/auto-extract.py \
  "Test: user likes Python for backend development" \
  --user <discord_id> --dry-run --json

# Run for real
python3 scripts/auto-extract.py \
  "User mentioned they prefer concise responses with warmth" \
  --user <discord_id>
```

### Set Up Hancho Consolidation

```bash
# Preview graph edges
python3 scripts/hancho-consolidate.py --all-users --hours 24 --dry-run

# Build the graph
python3 scripts/hancho-consolidate.py --all-users --hours 24
```

### Schedule Heartbeat Jobs

Add to `~/.openclaw/workspace/HEARTBEAT.md`:
```markdown
# MyVector v5 maintenance
- Every 1 hour: Run `python3 scripts/auto-extract.py` on recent conversations
- Every 4 hours: Run `python3 scripts/hancho-consolidate.py --all-users --hours 4`
- Every 6 hours: Run `python3 scripts/memory_consolidation.py --all-users`
- Daily: Review `extraction_log` for quality metrics
- Weekly: Review `memory_relations` for contradiction flags
```

### Parallel Run with Mem0/Hancho (7-10 days)

During validation period:
1. Keep Mem0 and Hancho running
2. Run auto-extract and hancho-consolidate in parallel
3. Compare quality: check `extraction_log` for facts extracted, merge rate, relation density
4. When auto-extract quality matches or exceeds Mem0, retire Mem0
5. When graph edges are comprehensive, retire Hancho

### New Tables Reference

| Table | Purpose | Since |
|-------|---------|-------|
| `memory_relations` | Knowledge graph edges between facts | v5.0.0 |
| `extraction_log` | Auto-extraction quality metrics | v5.0.0 |
| `memories.source` | Track fact provenance (manual/auto/consolidation/import) | v5.0.0 |
| `memories.verified_by_human` | Promotion flag for auto-extracted facts | v5.0.0 |

### New Views Reference

| View | Purpose | Since |
|------|---------|-------|
| `memory_graph_1hop` | Fast 1-hop graph traversal for retrieval | v5.0.0 |

---

## Part 8: v5.0.1 — Security Hardening Setup

### Apply v5.0.1 Security Migration

```bash
# ⚠️ Back up FIRST
docker exec myvector-db mysqldump -u root -p<pass> mysqlclaw > backup_pre_v5.0.1.sql

# Apply migration (requires root/admin — this is DDL)
docker exec -i myvector-db mysql -u root -p<pass> mysqlclaw < upgrade_v5.0.0_to_v5.0.1.sql
```

### Configure Credentials for Python Scripts

Python scripts (auto-extract, hancho-consolidate, retrieval-gate) load credentials from environment variables. **They no longer contain hardcoded passwords.**

Set up your environment:
```bash
# Add to your .bashrc or .env file
export MYSQL_USER=mysqlclaw
export MYSQL_PASSWORD=<your_least_priv_password>
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3310
export DATABASE=mysqlclaw
```

**Note**: The `.env` file is used by the shell scripts (`vector_claw.sh`, `sql_safe_exec.sh`). The Python scripts read from `os.environ`. Export the same variables or `source` the `.env` file before running Python scripts.

### Set Up Per-User Extraction Opt-In

Auto-extraction is **disabled by default**. For each user:
```bash
# 1. Insert extraction config (disabled)
docker exec -i myvector-db mysql -u root -p<pass> mysqlclaw -e \
  "INSERT INTO extraction_config (user_id) VALUES ('<discord_id>');"

# 2. After explicit user opt-in, enable:
docker exec -i myvector-db mysql -u root -p<pass> mysqlclaw -e \
  "UPDATE extraction_config SET auto_extract_enabled=TRUE, consent_given_at=NOW(), consent_method='explicit' WHERE user_id='<discord_id>';"
```

### Configure Data Retention

Default retention policies are inserted by the migration. To customize:
```bash
# Example: extend mood retention to 180 days
docker exec -i myvector-db mysql -u root -p<pass> mysqlclaw -e \
  "UPDATE data_retention_policy SET retention_days=180 WHERE table_name='user_mood';"
```

### New Tables in v5.0.1

| Table | Purpose | Since |
|-------|---------|-------|
| `extraction_config` | Per-user auto-extraction opt-in and settings | v5.0.1 |
| `data_retention_policy` | Configurable retention limits per data type | v5.0.1 |
| `audit_log` | Data access/modification audit trail | v5.0.1 |

### Updated Schema

| Change | Reason | Since |
|--------|--------|-------|
| `thought_stream.user_id` → NULL allowed | Decouple agent reasoning from user-identifiable data | v5.0.1 |

