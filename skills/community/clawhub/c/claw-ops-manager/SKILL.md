---
name: claw-ops-manager
description: OpenClaw operations management center v3 with multilingual support, intelligent descriptions, automatic git-based snapshots, and one-click rollback. Every operation automatically translated into 6 languages (English, Chinese, Japanese, Spanish, French, German), snapshotted for recovery, and logged for audit. Features include visual web dashboard with language switcher, permission management, real-time alerts, and seamless integration. Perfect for global teams requiring operational oversight, mistake prevention, and instant recovery.
---

# Claw Operations Manager

Complete operational oversight and security control for OpenClaw.

## Quick Start

```bash
# 1. Initialize the audit system
python3 scripts/init.py

# 2. Start the web dashboard v3 (multilingual)
python3 scripts/server_v3.py
# Visit http://localhost:8080
# Switch language with 🌐 button (EN/ZH/JA/ES/FR/DE)

# 3. Use automatic auditing with snapshots
python3 << 'EOF'
import sys
sys.path.insert(0, ".")
from scripts.audited_ops import audited_exec

# All commands automatically described + snapshotted
audited_exec("rm important.txt")  # EN: "Deleted ~/Desktop/important.txt"
                                 # ZH: "删除了 ~/Desktop/important.txt"
                                 # JA: "~/Desktop/important.txt を削除しました"

# Rollback anytime from the web UI!
EOF
```

**New in v3.0:**
- 🌐 **Multilingual Support** - 6 languages: EN, ZH, JA, ES, FR, DE
- 📝 **Intelligent Descriptions** - Commands → Human language (auto-translated)
- 📸 **Auto-Snapshots** - Git-based snapshots before every operation
- 🔄 **1-Click Rollback** - Instant recovery from web UI
- 🎨 **Modern Dashboard** - Language switcher, real-time stats

## Core Capabilities

### 1. Operation Audit Logging

**Automatic logging of all OpenClaw operations:**

- Tool calls (exec, read, write, browser, etc.)
- Parameters and results
- Success/failure status
- Execution duration
- File changes linked to operations

**Usage:**
```python
from logger import OperationLogger

logger = OperationLogger()
op_id = logger.log_operation(
    tool_name="exec",
    action="run_command",
    parameters={"command": "ls -la"},
    success=True,
    duration_ms=150
)
```

### 2. Permission Management

**Define access control rules:**

```python
# Check if operation is allowed
allowed, rule = logger.check_permission(
    tool_name="exec",
    action="run_command",
    path="/etc/ssh/sshd_config"
)

if not allowed:
    raise PermissionError(f"Blocked by rule: {rule}")
```

**Default protected paths:**
- `/etc/ssh`
- `/etc/sudoers`
- `~/.ssh`
- `/usr/bin`
- `/usr/sbin`

**Add custom rules:**
```sql
INSERT INTO permission_rules (rule_name, tool_pattern, action_pattern, path_pattern, allowed, priority)
VALUES ('protect-my-data', 'write|edit', '*', '/data/*', False, 100);
```

### 3. Visual Dashboard

**Complete web-based management interface - no command line required!**

Features:
- **Operation Browser**: View, search, and filter all operations by type, time, status
- **Permission Manager**: Add, edit, and delete access control rules
- **Snapshot Manager**: Create, compare, and restore system snapshots
- **Alert Center**: View and resolve security alerts
- **Real-time Statistics**: Live dashboard with auto-refresh

**Access:** http://localhost:8080

All operations can be performed through the graphical interface - no need for command-line tools!

### 4. File System Monitoring

**Monitor protected paths for changes:**

```bash
python scripts/monitor.py ~/.ssh /etc/ssh /var/log
```

**Tracks:**
- File modifications
- Creations and deletions
- Move operations
- Hash-based change detection

### 5. Snapshots & Rollback

**Create system state snapshots:**

```bash
# Create snapshot
python scripts/rollback.py create "before-change" "Snapshot before making changes"

# List snapshots
python scripts/rollback.py list

# Compare snapshots
python scripts/rollback.py compare 1 2

# Restore (dry-run first)
python scripts/rollback.py restore 1 --dry-run
```

**Limitations:**
- Rollback requires integration with backup system (git, restic, rsync)
- Current implementation captures metadata and hashes only
- For full restore, integrate with version control or backup tools

## Database Schema

**Located at:** `~/.openclaw/audit.db`

**Tables:**
- `operations` - All tool calls and actions
- `file_changes` - File modifications linked to operations
- `snapshots` - System state snapshots
- `permission_rules` - Access control rules
- `audit_alerts` - Security and compliance alerts

## Configuration

**Config file:** `~/.openclaw/audit-config.json`

**Key settings:**
```json
{
  "retention_days": 90,
  "protected_paths": ["/etc/ssh", "~/.ssh"],
  "snapshots_enabled": true,
  "auto_snapshot_interval_hours": 24,
  "web_ui": {
    "enabled": true,
    "port": 8080
  }
}
```

## API Endpoints

**Statistics:**
- `GET /api/stats` - Overview statistics

**Operations:**
- `GET /api/operations?limit=50&tool=exec` - List operations
- `GET /api/operations/<id>` - Operation details

**Alerts:**
- `GET /api/alerts?resolved=false` - List alerts
- `POST /api/alerts/<id>/resolve` - Mark as resolved

**Snapshots:**
- `GET /api/snapshots` - List all snapshots
- `POST /api/snapshots` - Create new snapshot

**Permissions:**
- `GET /api/permissions/rules` - List all rules
- `POST /api/permissions/check` - Check operation permission

## Security Best Practices

1. **Protect the database:**
   ```bash
   chmod 600 ~/.openclaw/audit.db
   ```

2. **Review alerts regularly:**
   - Check dashboard daily
   - Investigate high-severity alerts
   - Document resolutions

3. **Schedule automatic snapshots:**
   - Before system updates
   - Before major configuration changes
   - On a regular schedule (daily/weekly)

4. **Set up retention policy:**
   - Archive old logs
   - Purge records older than retention_days
   - Export for compliance reporting

## Troubleshooting

**Dashboard not loading:**
- Check if port 8080 is available
- Verify Flask is installed: `pip install flask watchdog plotly`
- Check server logs for errors

**File monitor not working:**
- Ensure paths exist and are accessible
- Check watchdog installation: `pip install watchdog`
- Verify path permissions

**Permission check failing:**
- Review rules in database: `SELECT * FROM permission_rules;`
- Check rule priorities (higher = more important)
- Verify pattern syntax (use fnmatch wildcards)

## Integration Examples

**Wrap OpenClaw tool calls:**

```python
from logger import OperationLogger

logger = OperationLogger()

def safe_exec(command):
    # Check permission
    allowed, rule = logger.check_permission("exec", "run_command", path=None)
    if not allowed:
        raise PermissionError(f"Blocked: {rule}")

    # Log operation
    op_id = logger.log_operation(
        tool_name="exec",
        action="run_command",
        parameters={"command": command}
    )

    # Execute
    try:
        result = subprocess.run(command, shell=True, capture_output=True)
        logger.log_operation_result(op_id, result, success=True)
        return result
    except Exception as e:
        logger.log_operation_result(op_id, None, success=False)
        raise
```

## Advanced Features

**Create audit alerts:**

```python
logger.create_alert(
    operation_id=op_id,
    alert_type="security",
    severity="high",
    message="Attempted modification of protected file"
)
```

**Get operation statistics:**

```python
stats = logger.get_statistics()
print(f"Total: {stats['total_operations']}")
print(f"Success rate: {stats['success_rate']:.2%}")
print(f"Unresolved alerts: {stats['unresolved_alerts']}")
```

**Export data for analysis:**

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("~/.openclaw/audit.db")
df = pd.read_sql_query("SELECT * FROM operations", conn)
df.to_csv("audit_export.csv", index=False)
```

## Dependencies

```bash
pip install flask watchdog plotly
```

For full functionality:
- Flask (web UI)
- watchdog (file monitoring)
- plotly (charts)
- sqlite3 (included in Python stdlib)

## Notes

- Database is created automatically on first run
- Web UI runs on port 8080 by default
- File monitoring requires write permissions to watched directories
- Snapshots store metadata only (not full file contents)
- For production use, consider external backup integration
