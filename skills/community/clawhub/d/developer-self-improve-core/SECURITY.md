# Security Information

## Safety Features

This skill implements the following safety measures:

1. **No Automatic Memory Modification**
   - All memory changes require human approval
   - AI can only propose rules, never auto-write

2. **Validated Input**
   - All inputs are validated before processing
   - No shell command injection vulnerabilities

3. **Transparent Operations**
   - All operations are logged to `memory/logs/operations.log`
   - Full audit trail with timestamps

4. **Platform Isolation**
   - Rules are isolated by platform (iOS/Android/Flutter/etc.)
   - No cross-platform contamination

5. **Human-in-the-Loop**
   - Every rule requires human confirmation: 【同意/修改/忽略】
   - Users can rollback any changes

## Permissions

This skill requires:
- Read/write access to its own directory
- Read access to configuration files (config/config.yaml)
- Read access to workspace config (workspace/config/current_user.json) for user identity
- Access to openclaw CLI for DingTalk notifications (optional)
- User-configured crontab for scheduled reminders (optional)

**Data Access:**
- Reads: `workspace/config/current_user.json` (user name, platform, project)
- Writes: `memory/` directory (proposals, rules, logs)
- Sends: Rule summaries to DingTalk (if reminders enabled)

## Dependencies

- bash (standard shell)
- find (standard utility)
- grep (standard utility)
- awk (standard utility)
- md5sum (standard utility)
- stat/date (standard utility)
- openclaw CLI (for DingTalk notifications, optional)
- jq (optional, for JSON parsing)

No external or untrusted dependencies.

## Environment Variables

| Variable | Purpose | Required | Default |
|----------|---------|----------|---------|
| `AUTO_MEMORY_WORKSPACE` | Override default workspace path | **No (Optional)** | Current directory (`$(pwd)`) |

**Note:** This skill works without any environment variables. Set `AUTO_MEMORY_WORKSPACE` only if you need to use a custom workspace path.

## External Integrations

### DingTalk Notifications (Optional)

**Default Behavior:** Reminders are **DISABLED** by default (safe mode)

**How It Works:**
- If enabled, the skill sends reminder messages via `openclaw message send` to DingTalk
- Requires user to configure their DingTalk account ID in config/config.yaml
- No API keys are stored by this skill
- Messages contain proposed rule summaries only

**Enable Reminders:**
```yaml
# config/config.yaml
enable_reminder: true  # Default: false (enable after testing)
```

**OpenClaw CLI Credentials:**
- Credentials are managed by OpenClaw CLI, not this skill
- Users should verify their OpenClaw CLI configuration before enabling reminders

**Verify OpenClaw Setup:**
```bash
openclaw whoami  # Check login status
openclaw config list  # View configuration
```

### Workspace Config Access

**File:** `workspace/config/current_user.json`

**Purpose:** Read user identity (name, platform, project) for rule tagging

**Required:** **No (Optional)** - This skill works without this file

**If file exists:**
```json
{
  "user": "lijiujiu",
  "platform": "iOS",
  "project": "WKBasicApp"
}
```

**If file does not exist:**
- User info defaults to "unknown"
- Platform defaults to configured platform
- All core functions work normally

**Privacy:** This file is read-only; the skill does not modify it.

## Automatic Cleanup

### Default Behavior

**Auto cleanup is DISABLED by default** (safe mode for initial testing)

### Proposal Files

**What Gets Cleaned:**
- Proposal files older than `retention_days` (default: 7 days)
- Location: `memory/proposals/YYYY-MM-DD.md`

**When:**
- During `cleanup_expired_proposals()` function call
- Triggered by `cleanup` command or automatic triggers

**Enable Auto Cleanup:**
```yaml
# config/config.yaml
retention_days: 7              # Change retention period
enable_auto_cleanup: true      # Enable after testing (default: false)
```

**Important:** 
- Default is `false` for safety during initial testing
- Enable only after you've tested the skill and are satisfied with its behavior
- If you need to preserve proposals, keep `enable_auto_cleanup: false`

## Integration Points

### How It Works

**Execution Methods:**
1. **Manual**: Call scripts directly
   ```bash
   ./scripts/developer-self-improve-core.sh pre-check "场景"
   ./scripts/developer-self-improve-core.sh post-check "内容" "场景"
   ```

2. **Hooks**: Platform can configure hooks to run scripts automatically
   - Before AI response: `pre-check`
   - After AI response: `post-check`

3. **Cron**: Scheduled reminders via crontab (optional)
   ```bash
   30 9 * * * cd /path/to/skill && ./scripts/daily-check.sh
   ```

**Verify Integration:**
- Check with your platform how hooks are configured
- Test manually first: `./scripts/developer-self-improve-core.sh init`
- Inspect logs: `cat memory/logs/operations.log`

## Testing Recommendations

### Backup Before Enabling

**Important:** Back up the skill directory before enabling automation:

```bash
# Create backup
cp -r ~/.openclaw/workspace/skills/developer-self-improve-core \
        ~/.openclaw/workspace/skills/developer-self-improve-core.backup

# Or use rsync for incremental backups
rsync -av ~/.openclaw/workspace/skills/developer-self-improve-core/ \
        ~/.openclaw/workspace/skills/developer-self-improve-core.backup/
```

**Why backup:**
- Recover if scripts behave unexpectedly
- Restore rule files if accidentally deleted
- Test configuration changes safely

### Sandbox Testing

**Before enabling in production:**

1. **Disable reminders:**
   ```yaml
   # config/config.yaml
   enable_reminder: false
   ```

2. **Disable auto cleanup:**
   ```yaml
   enable_auto_cleanup: false
   ```

3. **Test manually:**
   ```bash
   ./scripts/developer-self-improve-core.sh init
   ./scripts/developer-self-improve-core.sh pre-check "测试"
   ./scripts/developer-self-improve-core.sh post-check "测试内容" "测试"
   ```

4. **Inspect generated files:**
   ```bash
   cat memory/proposals/*.md
   cat memory/logs/operations.log
   ```

5. **Verify no unexpected data leaves your environment**

## Contact

For security concerns, please contact: lijiujiu
