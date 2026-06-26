---
name: ddday
version: 1.0.0
description: |
  Daily work journal + machine migration toolkit.
  Auto-scans all registered projects (git activity, file changes, API status),
  generates a daily dashboard, and provides one-command data export/restore
  for seamless machine migration.
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
  - Glob
  - Grep
---

## What ddday Does

> **Record your daily work. Migrate your data. Resume instantly on a new machine.**

ddday is a personal work journal and migration toolkit. It tracks all your projects, generates daily HTML dashboards and markdown logs, and when you switch machines, packs everything into a portable bundle that any AI agent can read to immediately understand your full work context.

---

## Setup

### Step 1 — Initialize ddday

Create the ddday directory and workspace config:

```bash
DDDAY_HOME="$HOME/Desktop/ddday"
mkdir -p "$DDDAY_HOME"/{logs,context}
```

### Step 2 — Create workspace.json

Register your projects. Edit `$DDDAY_HOME/workspace.json`:

```json
{
  "version": "1.0.0",
  "updated": "YYYY-MM-DD",
  "projects": [
    {
      "name": "my-project",
      "path": "/path/to/my-project",
      "type": "node",
      "emoji": "📦",
      "description": "Brief description of the project"
    }
  ]
}
```

**Supported types**: `node`, `python`, `shopify`, `design`, `workspace`, `skill`

### Step 3 — Register as Claude Code skill

```bash
ln -sfn "$DDDAY_HOME" "$HOME/.claude/skills/ddday"
```

### Step 4 — Set up daily cron (optional)

```bash
chmod +x "$DDDAY_HOME/generate_dashboard.py"
(crontab -l 2>/dev/null; echo "2 18 * * * cd $DDDAY_HOME && python3 generate_dashboard.py") | crontab -
```

---

## Commands

```
/ddday              — Scan all projects, generate daily log + dashboard
/ddday add <path>   — Register a new project
/ddday context      — Generate AI context pack (for new AI conversations)
/ddday snapshot     — Full work snapshot (all data + business reports + AI memory)
/ddday export       — One-command migration bundle to Desktop
/ddday doctor       — Environment health check (run after migration)
/ddday log          — View latest daily log
/ddday status       — Quick project status (no log written)
```

---

## Mode Recognition

Parse user input to select mode:

- Contains `add` + a path → **Mode 2 (Register project)**
- Contains `context` → **Mode 3 (AI context pack)**
- Contains `export` → **Mode 4 (Migration export)**
- Contains `setup` → **Mode 5 (New machine restore)**
- Contains `doctor` → **Mode 6 (Health check)**
- Contains `snapshot` → **Mode 7 (Work snapshot)**
- Contains `log` → Read latest log file
- Contains `status` → Quick scan, no file output
- Default → **Mode 1 (Daily scan + record)**

---

## Mode 1 — Daily Scan + Record (Default)

### Step 1 — Load workspace

```python
import json, os

DDDAY_HOME = os.environ.get("DDDAY_HOME", os.path.expanduser("~/Desktop/ddday"))
ws_file = os.path.join(DDDAY_HOME, "workspace.json")

with open(ws_file, "r") as f:
    workspace = json.load(f)

projects = workspace.get("projects", [])
print(f"Registered {len(projects)} projects")
for p in projects:
    print(f"  - {p['name']}: {p['path']}")
```

### Step 2 — Scan each project

For each registered project folder:

```bash
PROJECT_PATH="/path/to/project"

echo "=== Today's commits ==="
cd "$PROJECT_PATH" && git log --oneline --since="today" 2>/dev/null || echo "Not a git repo"

echo "=== Uncommitted changes ==="
cd "$PROJECT_PATH" && git diff --stat 2>/dev/null

echo "=== Untracked files ==="
cd "$PROJECT_PATH" && git status --short 2>/dev/null | head -20

echo "=== Recently modified files (24h) ==="
find "$PROJECT_PATH" -maxdepth 3 -type f -mtime -1 \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -not -path '*/dist/*' \
  -not -name '.DS_Store' \
  2>/dev/null | head -20
```

Also read the project's `CLAUDE.md` or `README.md` if present.

### Step 3 — Generate daily log

Save scan results to `logs/YYYY-MM-DD.md`:

```markdown
# ddday work log · {date}

## Overview
- Today's commits: {total_commits}
- Active projects: {active}/{total}
- Pending changes: {pending}

## {emoji} {project_name} ({type})
- Status: {status_emoji} {status_text}
- Branch: {branch}
- Today's commits: {count}
  - {commit_messages}
- Uncommitted changes: {diff_stat}

## Summary
- Completed: {from git commits}
- In progress: {from diff}
- Next steps: {AI suggestions}
```

### Step 4 — Generate HTML dashboard

Run the dashboard generator to create `dashboard.html`:
- Project cards with status indicators
- Commit history per project
- Stats bar (total commits, active projects, pending changes)
- Light/dark theme toggle

### Step 5 — Update project overview

Save `context/projects-overview.md` for AI consumption.

---

## Mode 2 — Register Project (/ddday add <path>)

### Step 1 — Validate path and detect type

```python
import os

path = os.path.expanduser("<user-provided-path>")
has_git = os.path.isdir(os.path.join(path, ".git"))
has_package = os.path.isfile(os.path.join(path, "package.json"))
has_shopify = os.path.isdir(os.path.join(path, ".shopify"))
has_python = os.path.isfile(os.path.join(path, "requirements.txt"))

project_type = "unknown"
if has_shopify: project_type = "shopify"
elif has_package: project_type = "node"
elif has_python: project_type = "python"
```

### Step 2 — Add to workspace.json

Append project entry, check for duplicates first.

### Step 3 — Ask for description

Use AskUserQuestion to get a brief description from the user.

---

## Mode 3 — AI Context Pack (/ddday context)

Generates `context/projects-overview.md` containing:
- All project metadata, paths, descriptions
- Recent git log per project
- Key file listings
- Current status

Purpose: feed to any new AI conversation for instant project awareness.

---

## Mode 4 — Migration Export (/ddday export)

### What it does

1. **Generates a work snapshot** first (Mode 7)
2. **Collects all data**:
   - ddday directory (logs, context, config)
   - Report archives (e.g., `~/.shopadmin/` or custom report dirs)
   - Claude Code skills
   - Credential files (user-configured paths)
   - Claude project memory (`~/.claude/projects/*/memory/`)
   - Crontab backup
   - Python requirements
3. **Creates `manifest.json`**: path mappings, credentials index, cron jobs, dependencies
4. **Packs into** `~/Desktop/ddday-migration-{date}.tar.gz`
5. **Includes** `READ-ME-FIRST.md` at pack root (= the work snapshot)

### Migration bundle structure

```
ddday-migration/
├── READ-ME-FIRST.md       # Work snapshot — new AI reads this first
├── manifest.json           # Path mappings, dependencies, cron
├── ddday/                  # Full ddday directory
├── skills/                 # Custom skill definitions
├── credentials/            # Credential files
├── claude-memory/          # Claude project memory files
├── crontab.bak             # Crontab backup
├── requirements.txt        # Python dependencies
├── setup.sh                # One-command restore script
├── doctor.py               # Health check script
└── work_snapshot.py        # Snapshot generator
```

---

## Mode 5 — New Machine Restore (/ddday setup)

Run on new machine after extracting the migration bundle:

```bash
tar xzf ddday-migration-*.tar.gz
cd ddday-migration
bash setup.sh
```

### setup.sh automatically:

1. Detects new `$HOME` and username
2. Installs missing dependencies (Homebrew, Python, Git)
3. Installs Python packages
4. Copies all files to correct locations
5. Replaces all hardcoded paths (old `$HOME` → new `$HOME`)
6. Creates skill symlinks
7. Registers cron jobs

---

## Mode 6 — Health Check (/ddday doctor)

Checks 8 categories:

1. **Project paths** — Do all registered projects exist?
2. **Core files** — SKILL.md, workspace.json, scripts present?
3. **Credentials** — Required credential files in place?
4. **Python deps** — Required packages installed?
5. **Skills** — Symlinks correct, skill directories intact?
6. **Cron jobs** — Registered and scripts exist?
7. **API connectivity** — Can reach configured APIs?
8. **Path consistency** — Any stale paths from old machine?

Output: traffic-light report with pass/warn/fail counts.

---

## Mode 7 — Work Snapshot (/ddday snapshot)

Generates a **self-contained Markdown file** that any AI can read to immediately resume all work:

1. **User profile** — Role, tech stack, work style
2. **Project panorama** — Path, git status, README, .env keys, recent commits
3. **Business data** — Latest reports from all configured report directories
4. **AI memory** — Claude Code project memory files
5. **Recent logs** — Last 7 days of ddday logs
6. **Team handbook** — Available skills and their triggers
7. **Environment** — Cron, credentials, symlinks, system info
8. **Quick start guide** — How to immediately pick up work

Output:
- `context/work-snapshot-YYYY-MM-DD.md` — dated archive
- `context/LATEST-SNAPSHOT.md` — latest copy (AI reads this)

---

## Full Migration Flow

### Old machine
```bash
/ddday export       # Auto-generates snapshot + packs everything
```

### New machine
```bash
tar xzf ddday-migration-*.tar.gz
cd ddday-migration
cat READ-ME-FIRST.md    # AI reads this → instantly knows all your work
bash setup.sh           # Auto-restore environment
python3 doctor.py       # Health check
/ddday                  # Start working
```

---

## Configuration

ddday uses `$DDDAY_HOME` (defaults to `~/Desktop/ddday`) as its root:

```
$DDDAY_HOME/
├── SKILL.md              # This skill definition
├── workspace.json        # Project registry
├── generate_dashboard.py # Dashboard generator
├── work_snapshot.py      # Snapshot generator
├── export.py             # Migration exporter
├── setup.sh              # New machine restore
├── doctor.py             # Health check
├── run_ddday.sh          # Cron entry point
├── dashboard.html        # Latest dashboard (auto-generated)
├── logs/                 # Daily logs (YYYY-MM-DD.md)
└── context/              # AI context files
    ├── projects-overview.md
    ├── LATEST-SNAPSHOT.md
    └── work-snapshot-*.md
```

## Customization

### Adding report directories

If you have report tools (analytics, monitoring, etc.), edit `export.py` to include their output directories in the migration bundle. The work snapshot (`work_snapshot.py`) can also be extended to read from custom report paths.

### Extending project types

Add new type detection logic in Mode 2 by checking for framework-specific files (e.g., `Cargo.toml` for Rust, `go.mod` for Go).
