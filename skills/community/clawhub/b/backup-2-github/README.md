# Backup to GitHub

Backup OpenClaw personalized configuration and user data to a GitHub repository. Ensures you can restore your custom setup to a fresh OpenClaw installation.

## What It Backs Up

This skill backs up **only personalized/modified files**, not default OpenClaw files. Includes:

- **Configuration**: `openclaw.json` (core settings)
- **Memory**: `MEMORY.md` (long-term memories)
- **User Profile**: `USER.md`, `IDENTITY.md`, `SOUL.md`
- **Tools Config**: `TOOLS.md` (camera names, SSH hosts, voice preferences, etc.)
- **Heartbeat**: `HEARTBEAT.md` (periodic checklists)
- **Cron Jobs**: `cron/jobs.json` (scheduled tasks)
- **Monitoring Panel**: Custom monitor scripts (`openclaw-monitor.cjs`, `monitor/*.cjs`)
- **Skill Configurations**: Selected skill config files you've customized (edit `backup.py` to specify paths)
- **Custom Scripts**: Your personal scripts (edit `backup.py` to specify paths)
- **Credentials** (optional): `credentials/*.json` (e.g., Xiaohongshu cookies) - configurable

**Excluded**:
- Default installed skills (standard library)
- Daily memory files (`memory/YYYY-MM-DD.md`) - too large/dynamic
- Cron run logs (`cron/runs/`)
- Temp files, cache, `.git`, `__pycache__`

## Prerequisites

1. **GitHub Account** and a **Personal Access Token** with `repo` scope
2. **GitHub Repository** to store backups (can be private)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create `.env` file in the skill directory:

```env
GITHUB_TOKEN=ghp_your_token_here
GITHUB_REPO=fangbb-coder/OC-backup  # your username/repo
```

Or set them in `openclaw.json` under this skill's config.

### 3. (Optional) Create Backup Repository

On GitHub, create a new repository (e.g., `OC-backup`) to store your backups.

## Usage

### Backup

```bash
python backup.py --action backup
```

Dry-run (see what will be backed up without pushing):
```bash
python backup.py --action backup --dry-run
```

### Restore

To restore your configuration to a fresh OpenClaw installation:

```bash
python backup.py --action restore
```

This will:
1. Download the latest backup from GitHub
2. Restore files to their original locations
3. Print instructions to restart services

**Important**: Restore will overwrite existing files. Confirm with `yes` when prompted.

## How It Works

### Backup
1. Scans the predefined file list (in `backup.py` → `BACKUP_FILES`)
2. Filters out excluded patterns
3. Creates a single commit on the default branch with all files
4. Pushes to GitHub

### Restore
1. Fetches the latest commit from the backup repo
2. Downloads each file
3. Writes to correct locations (workspace or home openclaw dir)
4. Reports success

## Security Notes

- **GitHub Token** should have minimal scope (`repo` only)
- Backup repository can be **private** to keep data secure
- Credentials (like Xiaohongshu cookies) are **optional** and marked in config
- Do not share your token or backup repo publicly

## Limitations

- Does **not** backup large binary files (models, caches)
- Does **not** backup running state (processes, in-memory data)
- Daily memory files are excluded (too big and ephemeral)
- Requires internet access for GitHub push/pull

## Troubleshooting

**Error: GITHUB_TOKEN not set**
→ Set token in `.env` or pass via `--token`

**Error: Repository not found**
→ Check `GITHUB_REPO` format: `owner/repo`

**File not backing up**
→ Ensure file path is in `BACKUP_FILES` list and not excluded

## Advanced

### Custom File List

Edit `BACKUP_FILES` in `backup.py` to add/remove files from backup.

### Different Backup Branch

Modify the script to use a different branch instead of overwriting default.

## License

MIT
