---
name: clankerhive
description: "Shared SQLite-backed context store for multi-session agent coordination. Use when: (1) checking if work was already done recently (email checked, briefing sent), (2) preventing duplicate cron/heartbeat runs via task claiming, (3) passing alerts between sessions (cron queues alert → main session pops it), (4) storing short-lived facts with TTL, or (5) any cross-session state sharing. Replaces ad-hoc JSON state files with a proper coordination bus. Triggers on: deduplication, cross-session state, shared facts, alert queue, task coordination, heartbeat state."
homepage: https://github.com/pfrederiksen/clankerhive
metadata:
  {
    "openclaw":
      {
        "emoji": "🐝",
        "requires": { "bins": ["python3"] },
        "install": [],
      },
  }
---

# 🐝 ClankerHive

Shared context store for OpenClaw multi-session coordination. Three primitives:

1. **Facts** — key/value pairs with optional TTL (auto-expire)
2. **Alerts** — cross-session notification queue (producer/consumer)
3. **Tasks** — claim-based deduplication for in-flight work

All backed by a single SQLite database in WAL mode (safe for concurrent access).

## Setup

No dependencies beyond Python 3 stdlib. The DB is created automatically on first use.

```bash
# Default DB location: ~/.openclaw/hive.db
# Override with environment variable:
export CLANKERHIVE_DB=/path/to/custom/hive.db
```

Resolve the script path relative to this skill directory:

```bash
HIVE="python3 $(dirname "$0")/../scripts/clankerhive.py"
# Or use absolute path from skill install location
```

## Facts — Key/Value with TTL

Store short-lived coordination state. Expired facts are auto-pruned on every read.

```bash
# Set a fact (lives forever unless --ttl is given)
python3 scripts/clankerhive.py set email.last_check "$(date +%s)" --ttl 900

# Read it back (empty output if missing/expired)
python3 scripts/clankerhive.py get email.last_check

# List all facts matching a prefix
python3 scripts/clankerhive.py list --prefix email

# Delete a fact
python3 scripts/clankerhive.py delete email.last_check

# Tag who set it (useful for debugging)
python3 scripts/clankerhive.py set weather.checked "1" --ttl 3600 --source heartbeat
```

### Pattern: Skip-if-recent

Before doing expensive work, check if it was done recently:

```bash
LAST=$(python3 scripts/clankerhive.py get email.last_check)
if [ -z "$LAST" ]; then
    # Do the work, then record it
    python3 scripts/clankerhive.py set email.last_check "$(date +%s)" --ttl 900
fi
```

## Alerts — Cross-Session Queue

Cron jobs or sub-agents produce alerts; the main session consumes them.

```bash
# Queue an alert (from cron job)
python3 scripts/clankerhive.py queue-alert email "urgent: server down — production alert from monitoring"

# List unclaimed alerts
python3 scripts/clankerhive.py list-alerts

# Claim and return all pending alerts (marks them claimed)
python3 scripts/clankerhive.py pop-alerts

# Claim only alerts for a specific topic
python3 scripts/clankerhive.py pop-alerts --topic email

# Clean up old claimed alerts (default: older than 24h)
python3 scripts/clankerhive.py purge-alerts --age 86400
```

### Pattern: Cron → Main Session Handoff

Cron job detects something important:
```bash
python3 scripts/clankerhive.py queue-alert calendar "Standup with the platform team in 30 minutes"
```

Main session heartbeat checks for alerts:
```bash
ALERTS=$(python3 scripts/clankerhive.py pop-alerts)
# Process and notify user if non-empty
```

## Tasks — Deduplication

Prevent multiple sessions from doing the same work simultaneously.

```bash
# Try to claim a task (exit 0 = got it, exit 1 = someone else has it)
python3 scripts/clankerhive.py claim-task daily-briefing-2026-04-01
# stdout: "ok" or "already-claimed by <owner>"

# Release when done
python3 scripts/clankerhive.py release-task daily-briefing-2026-04-01 --result "sent to telegram"

# Check status
python3 scripts/clankerhive.py task-status daily-briefing-2026-04-01
```

### Pattern: Idempotent Cron

```bash
if python3 scripts/clankerhive.py claim-task "morning-briefing-$(date +%Y-%m-%d)"; then
    # Do the work...
    python3 scripts/clankerhive.py release-task "morning-briefing-$(date +%Y-%m-%d)" --result "done"
else
    echo "Already running or completed"
fi
```

## Stats

Quick summary of the hive state:

```bash
python3 scripts/clankerhive.py stats
```

Returns JSON with counts for facts, pending/claimed alerts, and claimed/done tasks.

## Replacing heartbeat-state.json

Instead of maintaining a separate `memory/heartbeat-state.json` file, use ClankerHive facts:

```bash
# Old way: read/write JSON file
# New way:
python3 scripts/clankerhive.py set heartbeat.email "$(date +%s)" --ttl 1800
python3 scripts/clankerhive.py set heartbeat.calendar "$(date +%s)" --ttl 3600
python3 scripts/clankerhive.py set heartbeat.weather "$(date +%s)" --ttl 7200

# Check when something was last done:
python3 scripts/clankerhive.py get heartbeat.email
# Empty = time to check again
```

## Notes

- DB path configurable via `CLANKERHIVE_DB` env var (default: `~/.openclaw/hive.db`)
- WAL mode ensures safe concurrent reads/writes from multiple processes
- All list/query commands output JSON; scalar commands output plain text
- Exit code 0 = success, 1 = error (already-claimed, not-found, etc.)
- No external dependencies — pure Python stdlib

## System Access

**Reads:** Nothing — no files, env vars, or network beyond the SQLite DB.

**Writes:** Only to the SQLite database file at `$CLANKERHIVE_DB` (default `~/.openclaw/hive.db`). Creates parent directories if they don't exist. The default path (`~/.openclaw/`) is typically mode `700` on OpenClaw installs, meaning only the owning user can read the DB. If you change `CLANKERHIVE_DB` to a shared or world-readable location, restrict permissions manually: `chmod 600 hive.db`.

**Network:** None. No outbound connections of any kind.

**Imports:** `argparse`, `json`, `os`, `sqlite3`, `sys`, `time`, `typing` — all Python stdlib. No third-party packages, no subprocess calls, no eval/exec.

**Source:** <https://github.com/pfrederiksen/clankerhive>
