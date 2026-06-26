# Personal Memory System

This is the official skill package for the Personal Memory System.

## What is it?

A self-contained, local-only memory system that automatically syncs your `MEMORY.md` to a searchable SQLite database (`memory.db`) and provides intelligent natural language querying. **It is designed to work as part of a complete, reliable knowledge infrastructure that includes Obsidian and Git synchronization.**

## How to use

1. **Install** this skill into your OpenClaw skills directory.
2. Ensure you have the following files and directories in your workspace root (`/home/awu/.openclaw/workspace-work/`):
   - `MEMORY.md`
   - `obsidian-vault/`
   - `git_sync_on_save.sh`
   - `git_sync.log`
   - `auto_sync_memory.py`
   - `query_memory.py`
3. **Start the Git sync daemon** (if not already running):
   ```bash
   cd /home/awu/.openclaw/workspace-work/
   nohup ./git_sync_on_save.sh > git_sync.log 2>&1 &
   ```
4. **Verify the daemon is running**:
   ```bash
   ps aux | grep git_sync_on_save.sh
   ```
5. The system will automatically sync `MEMORY.md` on every heartbeat.
6. **Query your memories**: Simply ask your OpenClaw assistant a question like "What were my thoughts on AI models?". The assistant will automatically use the `query_memory.py` script to search your database and give you a natural language answer.

## System Health Check

To ensure your memory system is fully operational, run these checks:

| Component | Check Command | Expected Result |
|----------|---------------|-----------------|
| `MEMORY.md` | `ls -l /home/awu/.openclaw/workspace-work/MEMORY.md` | File exists and is writable |
| `memory.db` | `ls -l /home/awu/.openclaw/workspace-work/memory.db` | File exists |
| `git_sync_on_save.sh` | `ls -l /home/awu/.openclaw/workspace-work/git_sync_on_save.sh` | File exists and is executable |
| Git Daemon | `ps aux | grep git_sync_on_save.sh` | Process running (not just the grep command) |
| Git Log | `tail -n 5 /home/awu/.openclaw/workspace-work/git_sync.log` | Shows recent git commits |
| Obsidian Vault | `ls -l /home/awu/.openclaw/workspace-work/obsidian-vault/` | Directory exists and contains .md files |

## Why use it?

- Never forget an important insight again.
- Query your past thoughts with natural language, not SQL.
- Your knowledge is yours, and stays on your machine.
- **Your memory is protected by 3 independent backups: local workspace, Obsidian vault, and remote Git repo.**

> "A mind without memory is like a computer without a hard drive."
> — Your Digital Self