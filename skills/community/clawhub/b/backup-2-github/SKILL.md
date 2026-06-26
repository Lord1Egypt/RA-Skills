# Backup to GitHub

OpenClaw skill to backup personalized configuration and user data to a GitHub repository. Ensures easy migration and disaster recovery.

## Features

- ✅ Backup only **personalized files** (not default OpenClaw)
- ✅ Restore to fresh installation with identical state
- ✅ Supports GitHub via Personal Access Token
- ✅ Single-commit backup (clean history)
- ✅ Dry-run mode to preview changes

## What Gets Backed Up

This skill backs up files that are **specific to your setup**, excluding default OpenClaw installation files:

- **Core Configuration**: `openclaw.json` (TTS, skills, plugins settings)
- **Long-term Memory**: `MEMORY.md` (curated memories, learned context)
- **User Identity**: `USER.md`, `IDENTITY.md`, `SOUL.md` (your profile & persona)
- **Custom Tools**: `TOOLS.md` (camera names, SSH hosts, voice preferences, etc.)
- **Heartbeat Tasks**: `HEARTBEAT.md` (periodic checklists)
- **Scheduled Jobs**: `cron/jobs.json` (your cron task configuration)
- **Monitoring Panel**: Custom monitor scripts (`openclaw-monitor.cjs`, `monitor/*.cjs`)
- **Skill Configurations**: Selected skill config files (YAML, README, SKILL.md) for skills you've customized (edit `backup.py` to add paths)
- **Custom Scripts**: Any user-created scripts (edit `backup.py` to add paths)
- **Credentials** (optional): `credentials/*.json` (Xiaohongshu cookies, etc.) - configurable

**Automatically Excluded**:
- Default/standard skills from the library
- Daily memory files (`memory/YYYY-MM-DD.md`) - too large/ephemeral
- Cron run logs (`cron/runs/`)
- Temporary files, caches, `.git`, `__pycache__`, `venv`, `node_modules`
- Large model files and binaries

## Prerequisites

- GitHub account with **Personal Access Token** (`repo` scope)
- Backup repository (private recommended)

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure (create .env file)
GITHUB_TOKEN=ghp_your_token_here
GITHUB_REPO=your-username/your-backup-repo
```

## Usage

```bash
# Backup current configuration
python backup.py --action backup

# Preview what will be backed up (no push)
python backup.py --action backup --dry-run

# Restore from backup (overwrites existing files)
python backup.py --action restore
```

## How It Works

### Backup
1. Scans predefined file list (in `backup.py` → `BACKUP_FILES`)
2. Filters out excluded patterns
3. Creates a single commit on the default branch with all file changes
4. Pushes to your GitHub repository

### Restore
1. Fetches the latest backup commit
2. Downloads each file to its original location
3. Reports success and suggests service restarts

## Customization

Edit `BACKUP_FILES` in `backup.py` to add or remove files from backup.

## Security Notes

- **GitHub Token** should have minimal scope (`repo` only)
- Store token in `.env` (never commit)
- Use a **private repository** for backups
- Credentials (e.g., Xiaohongshu cookies) are optional and clearly marked

## Limitations

- Does **not** backup large binary files (ML models, caches, datasets)
- Does **not** backup running state (processes, logs)
- Daily memory files excluded by design (too large, ephemeral)
- Requires internet access for GitHub operations

## Troubleshooting

**Error: GITHUB_TOKEN not set**
→ Set token in `.env` or use `--token` flag.

**Error: Repository not found**
→ Check `GITHUB_REPO` format: `owner/repo`.

**File not backing up**
→ Ensure path is in `BACKUP_FILES` and not excluded by patterns.

## License

MIT
