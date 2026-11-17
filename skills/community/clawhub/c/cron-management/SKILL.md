---
name: cron-management
description: "Manage OpenClaw cron jobs — list, pause, resume, maintenance mode, and health checks."
---

# cron-management — OpenClaw Cron Job Manager

Structured commands for managing cron jobs without raw JSON patches.

## Commands

| Command | Description |
|---------|-------------|
| `cronctl list` | List all jobs with status (✅/❌) |
| `cronctl show <name>` | Show detailed info for one job |
| `cronctl pause <name>` | Disable a single job |
| `cronctl resume <name>` | Re-enable a single job |
| `cronctl pause-all` | Disable ALL jobs |
| `cronctl resume-all` | Re-enable ALL jobs |
| `cronctl maintenance on` | Enable maintenance mode (stops all jobs at runtime) |
| `cronctl maintenance off` | Disable maintenance mode |
| `cronctl status` | Show health dashboard (recent failures, disabled jobs, overdue) |
| `cronctl health <name>` | Show last run status and diagnostics for a job |

## Maintenance Mode

Emergency stop that works even if OpenClaw is down. Jobs check for `/tmp/cron-paused` at startup:

```bash
if [ -f /tmp/cron-paused ]; then
  echo "Cron paused at $(cat /tmp/cron-paused)" >> /tmp/cron-skipped.log
  exit 0  # or reply NO_REPLY for agentTurn jobs
fi
```

Toggle: `cronctl maintenance on|off`

## Script

- `scripts/cronctl.sh` — Main CLI wrapper around `openclaw cron`

## Integration with Job Payloads

To add maintenance mode checks to existing jobs, add this at the top of each cron payload:

**For shell-based payloads:**
```bash
if [ -f /tmp/cron-paused ]; then
  echo "$(date -Iseconds) — $JOB_NAME skipped (maintenance mode)" >> /tmp/cron-skipped.log
  exit 0
fi
```

**For agentTurn payloads (OpenClaw):**
Add to the beginning of the message text:
```
If /tmp/cron-paused exists, reply NO_REPLY and exit.
```

**For Python scripts:**
```python
import os
import sys
from datetime import datetime

PAUSE_FILE = "/tmp/cron-paused"
SKIP_LOG = "/tmp/cron-skipped.log"

def check_maintenance_mode():
    if os.path.exists(PAUSE_FILE):
        with open(SKIP_LOG, "a") as f:
            f.write(f"{datetime.now().isoformat()} — {sys.argv[0]} skipped (maintenance mode)\n")
        sys.exit(0)

check_maintenance_mode()
```

**For Node.js scripts:**
```javascript
const fs = require('fs');
const path = require('path');

const PAUSE_FILE = '/tmp/cron-paused';
const SKIP_LOG = '/tmp/cron-skipped.log';

function checkMaintenanceMode() {
  if (fs.existsSync(PAUSE_FILE)) {
    const entry = `${new Date().toISOString()} — ${path.basename(process.argv[1])} skipped (maintenance mode)\n`;
    fs.appendFileSync(SKIP_LOG, entry);
    process.exit(0);
  }
}

checkMaintenanceMode();
```

## Rollout Strategy

1. **New jobs**: Include maintenance check from the start
2. **Existing jobs**: Update incrementally, starting with most frequent (every 30 min, hourly)
3. **Verification**: Enable maintenance mode, wait for next trigger, check `/tmp/cron-skipped.log`

## Health Dashboard

`cronctl status` shows:
- Total jobs, enabled/disabled counts
- Jobs that failed in last 24h (consecutiveErrors > 0)
- Jobs disabled but not in maintenance mode (unexpected state)
- Jobs whose last run was >2x their interval (overdue)

## Examples

```bash
# Quick status overview
cronctl status

# Pause just the blog writer for debugging
cronctl pause cloudy-blog-writer

# Emergency stop everything
cronctl maintenance on

# Resume everything after fix
cronctl maintenance off
cronctl resume-all

# Check why a job keeps failing
cronctl health graph-memory-queue-sync
```

## Implementation Details

See `memory-bank/implementation-details/cron-management.md` for:
- Architecture (two-layer design)
- Rollout strategy
- Error handling
- State files and security
- Future enhancements
