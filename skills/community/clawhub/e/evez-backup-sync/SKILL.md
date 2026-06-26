---
name: evez-backup-sync
description: Auto-backup and sync engine for AI agent workspaces. Git commit and push to GitHub on schedule. Supabase cloud backup for critical state. mem0 persistent memory for knowledge retention. Full state snapshot every 15 minutes.
---

# EVEZ Backup and Sync

Never lose your agent's work. Auto-commits, cloud backup, and persistent memory.

## What It Does

- **Git auto-commit and push** — Every 5 minutes, all changes pushed to GitHub
- **Supabase cloud backup** — Critical state backed up to Supabase tables
- **mem0 persistent memory** — Key insights saved to vector memory with search
- **Full state snapshots** — Consciousness, knowledge graph, bridge state, circuit manifest

## Quick Start

```bash
python3 evez_backup_sync.py --port 9114
```

## API

- POST /api/backup — Full backup cycle (git + supabase + mem0)
- POST /api/git/push — Manual git commit and push
- POST /api/mem0/save — Save to persistent memory
- POST /api/mem0/search — Search persistent memory
- GET /api/status — Last backup info

## Requirements

- Python 3.10+
- git (for version control)
- Optional: supabase-py, mem0ai
