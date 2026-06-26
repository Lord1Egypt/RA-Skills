# Claw Audit Center

Complete operational oversight, security control, and change management for OpenClaw.

## Quick Start

```bash
# Initialize the audit system
python scripts/init.py

# Start the web UI
python scripts/server.py
# Visit http://localhost:8080

# Start file monitoring
python scripts/monitor.py ~/
```

## Features

### 1. Operation Logging
- Automatically logs all tool calls (exec, read, write, browser, etc.)
- Tracks parameters, results, success/failure, and duration
- Links file changes to operations

### 2. Permission Management
- Define rules for what operations are allowed
- Protect sensitive paths (e.g., `/etc/ssh`, `~/.ssh`)
- Pattern-based matching for tools, actions, and paths
- Priority-based rule evaluation

### 3. Visual Dashboard
- Real-time statistics
- Activity charts
- Operation history
- Alert management

### 4. File Monitoring
- Watch for changes to protected paths
- Track modifications, creations, deletions
- Hash-based change detection

### 5. Snapshots & Rollback
- Create snapshots of system state
- Compare snapshots
- Restore from snapshots (requires backup integration)

## Database Schema

**operations**: All tool calls and actions
- tool_name, action, parameters, result, success, duration_ms

**file_changes**: File modifications linked to operations
- file_path, operation_type, old_hash, new_hash

**snapshots**: System state snapshots
- name, description, snapshot_data

**permission_rules**: Access control rules
- tool_pattern, action_pattern, path_pattern, allowed, priority

**audit_alerts**: Security and compliance alerts
- alert_type, severity, message, resolved

## Usage Examples

### Check if an operation is allowed
```python
from logger import OperationLogger

logger = OperationLogger()
allowed, rule = logger.check_permission(
    tool_name="exec",
    action="run_command",
    path="/etc/ssh/sshd_config"
)

if not allowed:
    print(f"Blocked by rule: {rule}")
```

### Create a snapshot
```bash
python scripts/rollback.py create "before-upgrade" "System state before package upgrade"
```

### List snapshots
```bash
python scripts/rollback.py list
```

### Compare snapshots
```bash
python scripts/rollback.py compare 1 2
```

### Monitor file changes
```bash
python scripts/monitor.py ~/.ssh /etc/ssh
```

## Configuration

Configuration file: `~/.openclaw/audit-config.json`

```json
{
  "database_path": "~/.openclaw/audit.db",
  "retention_days": 90,
  "protected_paths": [
    "/etc/ssh",
    "/etc/sudoers",
    "~/.ssh"
  ],
  "snapshots_enabled": true,
  "auto_snapshot_interval_hours": 24
}
```

## API Endpoints

- `GET /api/stats` - Statistics overview
- `GET /api/operations` - List operations with filters
- `GET /api/operations/<id>` - Operation details
- `GET /api/alerts` - List alerts
- `POST /api/alerts/<id>/resolve` - Resolve alert
- `GET /api/permissions/rules` - List permission rules
- `POST /api/permissions/check` - Check operation permission
- `GET /api/snapshots` - List snapshots
- `POST /api/snapshots` - Create snapshot

## Integration with OpenClaw

To enable operation logging in OpenClaw, wrap tool calls:

```python
from logger import OperationLogger

logger = OperationLogger()

# Before operation
op_id = logger.log_operation(
    tool_name="exec",
    action="run_command",
    parameters={"command": "ls -la"},
    session_id=current_session
)

# Execute operation
result = execute_command("ls -la")

# After operation
logger.log_operation_result(op_id, result, success=True)
```

## Security Notes

- Database should have restricted permissions (chmod 600)
- Protected paths are logged regardless of permission rules
- Consider encrypting snapshots for sensitive data
- Review and resolve alerts regularly

## Limitations

- Rollback requires integration with a backup system (git, restic, rsync)
- File monitoring uses watchdog (may miss rapid changes)
- Large result values are truncated in logs

## Future Enhancements

- Integration with OpenClaw's tool hooks
- Automatic snapshot scheduling
- Export to external logging systems
- Real-time alert notifications (webhook, email)
- Compliance report generation
