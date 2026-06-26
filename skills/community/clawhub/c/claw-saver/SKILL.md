---
name: claw-saver
description: Back up the full OpenClaw environment (~/.openclaw) to a Git repository. Supports scheduled backups, interactive restore, and Git LFS for large model files.
version: 1.6.2
emoji: "💾"
homepage: https://clawhub.ai/skills/claw-saver
metadata:
  openclaw:
    requires:
      env:
        - OPENCLAW_BACKUP_GIT_TOKEN
      bins:
        - git
        - git-lfs
      config:
        - skills/claw-saver/config.json
    primaryEnv: OPENCLAW_BACKUP_GIT_TOKEN
    envVars:
      - name: OPENCLAW_BACKUP_GIT_TOKEN
        required: true
        description: Git personal access token with repo scope. Injected via openclaw config.
      - name: OPENCLAW_DIR
        required: false
        description: Override OpenClaw home directory. Defaults to ~/.openclaw.
---

# claw-saver

Back up the entire OpenClaw environment (~/.openclaw) to a Git repository. Supports scheduled backups, interactive restore, and exponential backoff on network failures.

## Features

- **Full backup**: Everything in ~/.openclaw is backed up, including agents, skills, configurations, knowledge bases, and agent memory
- **Smart exclusions**: Only ignores clearly harmless runtime artifacts (logs, cache, node_modules, canvas)
- **Scheduled backups**: Configurable cron schedule (default: every 5 hours)
- **Atomic commits**: Two-commit strategy ensures backup files and restore guide are always consistent
- **Git LFS support**: Large model files are auto-tracked via Git LFS
- **Exponential backoff**: Failed pushes retry with 60s -> 120s -> 240s delays
- **Stale lock protection**: Orphan backup processes are detected and cleaned up
- **Dynamic .gitignore**: Scans the actual directory structure, no hardcoded assumptions

## Quick Start

```bash
# 1. Configure your Git token
openclaw config set env.OPENCLAW_BACKUP_GIT_TOKEN <your-token>

# 2. Set your repository URL
# Edit ~/.openclaw/skills/claw-saver/config.json and set "repo"
# Example: "repo": "https://cnb.cool/yourname/your-repo"

# 3. Run your first backup
openclaw backup run

# 4. Enable automatic backups (every 5 hours)
openclaw backup enable-cron
```

## CLI Commands

```bash
openclaw backup run            # Run backup immediately
openclaw backup status         # Show last backup time and commit hash
openclaw backup restore        # Restore from a previous commit (interactive)
openclaw backup enable-cron    # Enable scheduled backups
openclaw backup disable-cron   # Disable scheduled backups
openclaw backup set-cron <expr> # Set custom schedule (e.g. "0 */2 * * *")
```

## Configuration

Edit `~/.openclaw/skills/claw-saver/config.json`:

```json
{
  "repo": "https://cnb.cool/yourname/your-repo",
  "cron": "0 */5 * * *",
  "lfs_threshold_mb": 10,
  "lfs_extensions": [".bin", ".gguf", ".safetensors", ".pt", ".pth", ".onnx", ".msgpack", ".model"],
  "push_retries": 3,
  "push_retry_interval_ms": 60000
}
```

| Option | Default | Description |
|--------|---------|-------------|
| `repo` | (required) | Git repository URL |
| `cron` | `0 */5 * * *` | Backup schedule (cron expression, in system timezone) |
| `lfs_threshold_mb` | `10` | Files larger than this are tracked via Git LFS |
| `lfs_extensions` | (see above) | File extensions to LFS-track |
| `push_retries` | `3` | Max push retry attempts on failure |
| `push_retry_interval_ms` | `60000` | Initial retry delay (doubles each attempt) |

## What Is Backed Up

**Everything except harmless runtime artifacts:**

```
# === BACKED UP ===
agents/              # Agent configurations, auth profiles, session data
credentials/         # Channel credentials and keys
identity/           # Device identity keys
kb/                 # Knowledge base (user docs + vector database)
lts/                # Long-term scripts (cleanup, OOM protection)
openclaw.json       # Core configuration (含 tokens)
skills/             # All installed skills and their configs
workspace-* /       # Agent workspaces, memory, learnings
**/.learnings/      # Agent self-improvement logs
**/.openclaw/       # Per-workspace OpenClaw state
And all other directories in ~/.openclaw/
```

## What Is Excluded (Runtime Artifacts Only)

These are transient or rebuildable and intentionally not backed up:

```
.git/               # Git repository itself (local only)
logs/               # Runtime logs
canvas/             # Canvas runtime state
media/             # Uploaded media files
npm/               # NPM packages (rebuild with npm install)
cron/runs/         # Cron execution history
**/node_modules/   # Dependencies (rebuild with npm install / pip install)
**/__pycache__/     # Python bytecode cache
**/.cache/          # Generic cache
**/dreaming/        # Short-term memory state
*.tmp, *.bak        # OS noise
.backup.lock        # Runtime lock file
```

> **User data principle**: If in doubt, it is backed up. Credentials, identity keys, knowledge bases, agent memory, and learned data are all preserved.

## Security

- **Token isolation**: The token is stored only in `~/.openclaw/.git/config` (local, never pushed to the backup repo) and in the cron environment variable (local system only)
- **No token in commits**: RESTORE.md and commit messages contain only the repo URL, never the token
- **stderr suppressed**: `git push` stderr is redirected to prevent token leakage in error messages
- **git directory excluded**: `.git/` is in .gitignore, so `.git/config` (containing the token in the remote URL) is never backed up

## Restore

```bash
openclaw backup restore
```

This clones the repository to a temp directory, checks out the specified commit, and copies files back to ~/.openclaw. A running backup is preserved (skills/claw-saver stays live during restore).

After restore completes:

```bash
openclaw gateway restart
```

## Restore Guide

A `RESTORE.md` file is generated with each backup, embedded in the backup commit. It contains the exact commit hash, clone instructions, and a list of what was excluded so you know what needs manual restoration.

## Architecture

```
skills/claw-saver/
  lib/
    backup.js      # Core orchestration (lock, stage, commit, push)
    git.js         # Git operations (init, add, commit, push, clone)
    lfs.js         # Git LFS setup and tracking
    restore.js     # Interactive restore logic
  scripts/
    cli.js         # CLI entry point (run, status, restore, cron)
  config.json      # User configuration (repo, cron, LFS settings)
```

## Lock Mechanism

Concurrent backup runs are prevented via an atomic mkdir-based lock:

- Lock dir: `~/.openclaw/.backup.lock/` (pid file inside)
- If a stale lock is detected (holder PID is dead), it is forcibly taken over
- Lock is always released via `finally{}` after backup completes or fails
