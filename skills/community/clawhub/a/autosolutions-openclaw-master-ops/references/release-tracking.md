# Release Tracking Workflow

## Overview

This skill tracks OpenClaw releases automatically and alerts you to:
- Breaking changes that affect operations
- Config schema changes
- Command deprecations/removals
- Skill updates needed

## Database Schema

Location: `skills/openclaw-master-ops/release-history.db`

### Tables

**releases**
- `version` — OpenClaw version (e.g., `2026.4.11`)
- `release_date` — ISO 8601 timestamp
- `changelog` — Full changelog text
- `is_breaking` — Boolean flag
- `breaking_changes` — JSON array of detected breaking changes
- `synced_at` — When this was synced

**breaking_changes**
- `version` — OpenClaw version
- `category` — Type of breaking change (feature_removal, deprecation, config_change, etc.)
- `description` — What changed
- `migration_action` — How to adapt (if known)

**skill_knowledge**
- `topic` — Skill topic (e.g., "gateway commands", "security audit")
- `last_verified_version` — Last OpenClaw version this was verified against
- `needs_update` — Boolean flag
- `notes` — Update notes

## Commands

### Sync Latest Releases

```bash
cd /home/marius/.openclaw/workspace/skills/openclaw-master-ops
python3 scripts/release-tracker.py sync
```

Fetches the last 10 releases from GitHub, detects breaking changes, updates database.

### View Release History

```bash
python3 scripts/release-tracker.py history
python3 scripts/release-tracker.py history --limit 20
```

### Check Breaking Changes

```bash
python3 scripts/release-tracker.py breaking
```

### Check If Skill Needs Updates

```bash
python3 scripts/release-tracker.py skill-update
```

Compares current OpenClaw version against tracked knowledge, flags outdated topics.

### Export for Skill Context

```bash
python3 scripts/release-tracker.py export
```

Exports to `references/release-tracker.json` — loaded into skill context when needed.

### Check Current Version

```bash
python3 scripts/release-tracker.py version
# Or directly:
openclaw --version
```

## Automated Sync (Cron)

Add to your OpenClaw cron jobs:

```bash
# Sync release tracker weekly (Sundays at 3 AM)
openclaw cron add "0 3 * * 0" "cd /home/marius/.openclaw/workspace/skills/openclaw-master-ops && python3 scripts/release-tracker.py sync"

# Check for skill updates daily
openclaw cron add "0 8 * * *" "cd /home/marius/.openclaw/workspace/skills/openclaw-master-ops && python3 scripts/release-tracker.py skill-update"
```

## Heartbeat Integration

Add to `HEARTBEAT.md`:

```markdown
# Release Tracking
- [ ] Run `release-tracker.py skill-update` if OpenClaw updated
- [ ] Review breaking changes if any
- [ ] Update skill knowledge for affected topics
```

## Skill Update Workflow

When a breaking change is detected:

1. **Review the change**
   ```bash
   python3 scripts/release-tracker.py breaking
   ```

2. **Check affected skill sections**
   - Read `references/release-tracker.json`
   - Identify which skill sections reference the changed feature

3. **Update the skill**
   ```bash
   # Edit SKILL.md
   nvim /home/marius/.openclaw/workspace/skills/openclaw-master-ops/SKILL.md
   
   # Update references
   nvim /home/marius/.openclaw/workspace/skills/openclaw-master-ops/references/
   ```

4. **Update skill_knowledge table**
   ```bash
   sqlite3 release-history.db "UPDATE skill_knowledge SET last_verified_version='2026.4.11', needs_update=FALSE WHERE topic='gateway commands';"
   ```

5. **Republish to ClawHub**
   ```bash
   clawhub publish /home/marius/.openclaw/workspace/skills/openclaw-master-ops \
     --slug autosolutions-openclaw-master-ops \
     --version 1.1.0 \
     --changelog "Updated for OpenClaw 2026.4.11: [list changes]"
   ```

## Breaking Change Detection

The tracker detects these patterns in changelogs:

| Pattern | Category | Action |
|---------|----------|--------|
| "removed" | feature_removal | Check if skill references this feature |
| "deprecated" | deprecation | Add deprecation notice, plan migration |
| "breaking" | breaking_change | High priority review |
| "migration" | migration_required | Follow migration guide |
| "changed default" | default_change | Update skill examples |
| "config schema" | config_change | Verify config commands |
| "api change" | api_change | Check API-related operations |
| "command removed" | command_removal | Remove from skill reference |
| "flag removed" | flag_removal | Update command examples |

## Manual Knowledge Tracking

Track skill topics that need verification:

```bash
sqlite3 release-history.db "INSERT INTO skill_knowledge (topic, last_verified_version, last_verified_at, needs_update) VALUES ('gateway commands', '2026.4.11', datetime('now'), FALSE);"
```

Key topics to track:
- `gateway commands` — start/stop/status/query
- `security audit` — audit flags, --fix behavior
- `channel config` — channel-specific settings
- `agent config` — agent defaults, sandbox settings
- `cron commands` — cron job management
- `session management` — session commands, history
- `plugin system` — plugin install/update APIs
- `cli flags` — global flags, output options

## Query Examples

```sql
-- Find all breaking changes in a version
SELECT * FROM breaking_changes WHERE version = '2026.4.11';

-- Find topics needing updates
SELECT * FROM skill_knowledge WHERE needs_update = TRUE;

-- Find releases with breaking changes
SELECT version, release_date, breaking_changes 
FROM releases 
WHERE is_breaking = TRUE 
ORDER BY release_date DESC;

-- Check when a topic was last verified
SELECT topic, last_verified_version, last_verified_at 
FROM skill_knowledge 
ORDER BY last_verified_at DESC;
```

## Integration Points

### With openclaw-master-ops Skill

The skill reads `references/release-tracker.json` when:
- User asks about recent OpenClaw changes
- User reports an error that might be version-related
- Running `openclaw update`

### With Heartbeat

Heartbeat checks trigger `skill-update` command when:
- OpenClaw version changed since last check
- Breaking changes detected in last 7 days

### With ClawHub

Auto-suggest skill updates when:
- Breaking changes affect skill content
- More than 30 days since last skill update
