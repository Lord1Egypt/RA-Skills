---
name: disk-cleanup
description: >
  Automated disk space cleanup and maintenance for OpenClaw deployments.
  Cleans 12 categories: memory SQLite orphan tmp files, SQLite VACUUM,
  Docker dangling images/volumes/build cache, OpenClaw gateway logs,
  /tmp temp files, workspace backup artifacts, delivery queue stale entries,
  systemd journal vacuum, package manager caches (npm/yarn/pnpm/bun/prisma),
  rotated syslogs and btmp, git workspace gc, and stale migration artifacts
  (e.g. QMD models after backend switch). Use when: disk is filling up,
  after long-running deployments, as weekly cron maintenance, when
  disk usage exceeds 80%, when memory reindex leaves orphan .sqlite.tmp files,
  or when Docker images accumulate from sandbox rebuilds. Triggers on:
  disk cleanup, disk full, free space, storage maintenance, prune,
  vacuum, cleanup script, disk usage high.
---

# Disk Cleanup

Automated disk space recovery for OpenClaw deployments. Covers 12 cleanup categories that OpenClaw does not handle natively (as of 2026.3.13).

## What OpenClaw Already Handles (skip these)

- **Session store**: `session.maintenance` config (pruneAfter, maxEntries, rotateBytes)
- **Sandbox containers**: `sandbox.prune` config (idleHours, maxAgeDays)
- **Context pruning**: `contextPruning` config (cache-ttl mode)

## What This Skill Handles (the gaps)

| # | Category | Typical Growth | Trigger |
|---|----------|---------------|---------|
| 1 | Memory SQLite `.tmp-*` orphans | Hundreds of MB from failed reindex | Always |
| 2 | Memory SQLite VACUUM | Fragmentation after heavy use | `--aggressive` |
| 3 | Docker images/volumes/build cache | GB from sandbox rebuilds | Always |
| 4 | Gateway logs (`/tmp/openclaw/*.log`) | Grows daily | >3 days old |
| 5 | `/tmp` OpenClaw temp files | Patrol/board/cron artifacts | >24h old |
| 6 | Workspace `.prebind.*` backups | Hundreds of MB per backup | >7 days old |
| 7 | Delivery queue old entries | Grows with message volume | >7 days old |
| 8 | systemd journal | GB on default VPS configs | >500MB |
| 9 | npm/yarn/pnpm/bun/prisma/node-gyp cache | GB from skill/plugin installs | >100MB |
| 10 | Rotated syslogs + btmp | SSH brute-force logs on public VPS | Always |
| 11 | Git workspace `.git` | Auto-commit growth (board-move etc.) | >200MB |
| 12 | QMD/migration artifacts | Stale after backend switch | Auto-detected |

## Quick Start

Run directly:

```bash
# Preview what would be cleaned (safe, no deletions)
bash scripts/disk-cleanup.sh --dry-run

# Normal cleanup
bash scripts/disk-cleanup.sh

# Deep cleanup: includes SQLite VACUUM + aggressive git gc
bash scripts/disk-cleanup.sh --aggressive

# Cron mode: only outputs summary line
bash scripts/disk-cleanup.sh --quiet
```

## Schedule as Cron Job

Weekly Sunday 04:00 CET (recommended):

```
Use the cron tool:
  schedule: { kind: "cron", expr: "0 3 * * 0", tz: "Europe/Luxembourg" }
  payload: { kind: "agentTurn", message: "Run disk cleanup: bash scripts/disk-cleanup.sh --aggressive --quiet. Report results." }
  sessionTarget: "isolated"
```

Or integrate into an existing infra-health-check script by adding a disk usage threshold trigger:

```bash
DISK_PCT=$(df / --output=pcent | tail -1 | tr -d ' %')
if [ "$DISK_PCT" -ge 85 ]; then
  bash /path/to/disk-cleanup.sh --quiet
fi
if [ "$DISK_PCT" -ge 90 ]; then
  bash /path/to/disk-cleanup.sh --aggressive --quiet
fi
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENCLAW_HOME` | `~/.openclaw` | OpenClaw state directory |
| `OPENCLAW_WORKSPACE` | `$(pwd)` | Agent workspace root |

## Exit Codes

- `0` — Success (cleaned or nothing to clean)
- `1` — Error during cleanup

## Output Format

Last line is machine-parseable:

```
CLEAN|0|0B|44%          # Nothing cleaned
CLEANED|5|1.2GB|67%     # 5 actions, freed 1.2GB, now at 67%
```

## Safety

- `--dry-run` previews all actions without deleting
- SQLite VACUUM only on `--aggressive` and only when fragmentation ≥5%
- Docker prune only removes dangling (untagged) images; named images are safe
- btmp is truncated (not deleted) — system expects the file to exist
- Journal vacuum installs a persistent 500MB limit to prevent regrowth
- Git gc uses `--auto` by default; `--aggressive` only with flag
