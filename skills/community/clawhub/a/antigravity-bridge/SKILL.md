---
name: antigravity-bridge
version: 2.0.1
description: "One-directional knowledge bridge from Google Antigravity IDE to OpenClaw. Syncs only .md documentation files from Antigravity projects into OpenClaw workspace for native vector indexing. No secrets, credentials, or binary state are synced — rsync filters enforce .md-only transfer. Supports multiple projects."
author: heintonny
metadata: {"openclaw":{"emoji":"🌉","tags":["antigravity","gemini","knowledge-sync","multi-agent","bridge","ide","sync"],"requires":{"bins":["rsync","yq"]},"install":[{"id":"yq","kind":"brew","package":"yq","bins":["yq"],"label":"Install yq YAML parser"},{"id":"rsync","kind":"system","package":"rsync","bins":["rsync"],"label":"rsync (usually pre-installed)"}]}}
---

# Antigravity Bridge

One-directional knowledge bridge from Google Antigravity IDE to OpenClaw.

Syncs `.md` files from your Antigravity/Gemini projects into the OpenClaw workspace, where they are natively embedded and indexed for `memory_search`. No MEMORY.md dumping, no custom state tracking — just files on disk, indexed automatically.

## When to Use

- User says "sync antigravity", "bridge sync", "pull antigravity docs"
- You need cross-project awareness of Antigravity-managed context
- After an Antigravity session, to surface new decisions/rules/tasks to OpenClaw
- Scheduled (cron) to keep the knowledge fresh automatically

## When NOT to Use

- Primary coding work (use Antigravity for that — it has IDE, LSP, deep code awareness)
- Writing back to Antigravity projects (this is **one-way only**: Antigravity → OpenClaw)
- Querying the synced knowledge (just use `memory_search` — the files are already indexed)

---

## Architecture

```
Antigravity IDE                  OpenClaw Workspace
─────────────────                ─────────────────────────────
~/repo/acme-corp/acme-platform/
  .agent/memory/       ──rsync──► antigravity/acme-platform/
  .agent/rules/        ──rsync──►   .agent/memory/
  .agent/skills/       ──rsync──►   .agent/rules/
  .agent/sessions/     ──rsync──►   .agent/skills/
  .agent/tasks.md      ──rsync──►   .agent/sessions/
  .gemini/GEMINI.md    ──rsync──►   .agent/tasks.md
  docs/                ──rsync──►   .gemini/GEMINI.md
  *.md (root)          ──rsync──►   docs/
                                    *.md (root)
~/.gemini/antigravity/
  knowledge/           ──rsync──► antigravity/gemini-knowledge/
─────────────────                ─────────────────────────────
                                         │
                                  OpenClaw native embedder
                                  (memorySearch.extraPaths)
                                         │
                                  memory_search queries ✓
```

**Key design decisions:**
- Files land in `antigravity/<project-name>/` under the OpenClaw workspace destination
- OpenClaw's native embedder indexes them automatically via `memorySearch.extraPaths`
- `sync.sh` is idempotent — safe to run repeatedly or on cron
- Source paths that don't exist are skipped gracefully (no failure)

---

## Setup Guide

### Step 1: Prerequisites

```bash
# rsync (usually pre-installed on macOS/Linux)
rsync --version

# yq — YAML parser (required)
brew install yq          # macOS
# or: sudo apt install yq   # Ubuntu/Debian
# or: snap install yq       # Ubuntu snap
yq --version
```

### Step 2: Copy the config template

```bash
cp ~/.openclaw/workspace/skills/antigravity-bridge/config-template.yaml \
   ~/.openclaw/workspace/antigravity-bridge.yaml
```

### Step 3: Edit the config

Open `~/.openclaw/workspace/antigravity-bridge.yaml` and configure your projects:

```yaml
projects:
  - name: acme-platform
    repo: ~/repo/acme-corp/acme-platform
    paths:
      - .agent/memory
      - .agent/rules
      - .agent/skills
      - .agent/tasks.md
      - .gemini/GEMINI.md
      - docs
    include_root_md: true

knowledge:
  - name: gemini-knowledge
    path: ~/.gemini/antigravity/knowledge

destination: antigravity
```

- **`projects`** — list of Antigravity-managed repos
- **`knowledge`** — standalone knowledge directories (e.g. Gemini's global knowledge store)
- **`destination`** — subfolder within the OpenClaw workspace (default: `antigravity`)

### Step 4: Configure OpenClaw extraPaths

Tell OpenClaw to index the synced directory. In your OpenClaw config (`~/.openclaw/config.yaml` or equivalent), add:

```yaml
memorySearch:
  extraPaths:
    - ~/path/to/openclaw/workspace/antigravity
```

Replace with the actual workspace path. After saving, restart OpenClaw or reload memory indexing.

### Step 5: Test with --dry-run

```bash
~/.openclaw/workspace/skills/antigravity-bridge/sync.sh --dry-run --verbose
```

You'll see what *would* be synced without touching anything.

### Step 6: Run for real

```bash
~/.openclaw/workspace/skills/antigravity-bridge/sync.sh --verbose
```

### Step 7: Verify with memory_search

After syncing, query OpenClaw memory to confirm indexing:

```
memory_search: "acme-platform agent rules"
memory_search: "GEMINI.md"
```

If results come back from the synced files, the bridge is working.

---

## Config Reference

```yaml
# ~/.openclaw/workspace/antigravity-bridge.yaml

projects:
  - name: <string>          # Identifier — used as subfolder name
    repo: <path>            # Root of the Antigravity project (~ expanded)
    paths:                  # List of paths relative to repo root
      - .agent/memory       # Directory → recursively sync *.md
      - .agent/tasks.md     # Single file → synced directly
      - docs                # Directory → recursively sync *.md
    include_root_md: true   # Also sync *.md files at repo root (optional, default: false)

knowledge:
  - name: <string>          # Identifier — used as subfolder name
    path: <path>            # Source path to rsync *.md from (~ expanded)

destination: antigravity    # Target subfolder in OpenClaw workspace
                            # Full path: <workspace>/<destination>/
```

**Path types:**
- **Directory** — rsync runs with `--include='*.md' --exclude='*'` recursively
- **Single file** — rsync copies the file directly (must end in `.md`)

**Missing sources:** If a configured path doesn't exist, sync.sh logs a warning and skips it. Other paths continue normally. Exit code remains 0.

---

## CLI Reference

```
sync.sh [options]

Options:
  --config <path>      Config file (default: ~/.openclaw/workspace/antigravity-bridge.yaml)
  --project <name>     Sync only this project (by name)
  --dry-run            Show what would be synced, without making changes
  --verbose            Show rsync output and detailed progress
  --help               Show this help
```

Examples:

```bash
# Sync everything
sync.sh

# Sync one project only
sync.sh --project acme-platform

# Preview without touching files
sync.sh --dry-run --verbose

# Use a custom config
sync.sh --config ~/my-bridge.yaml
```

---

## Cron Integration

Add to crontab (`crontab -e`) for automatic syncing:

```cron
# Antigravity Bridge — hourly during business hours (Mon-Fri, 08:00-18:00)
0 8-18 * * 1-5 ~/.openclaw/workspace/skills/antigravity-bridge/sync.sh >> ~/.openclaw/logs/antigravity-bridge.log 2>&1

# Nightly full sync (all days, 02:00)
0 2 * * * ~/.openclaw/workspace/skills/antigravity-bridge/sync.sh --verbose >> ~/.openclaw/logs/antigravity-bridge.log 2>&1
```

Create the log directory first:

```bash
mkdir -p ~/.openclaw/logs
```

---

## Troubleshooting

**`yq: command not found`**
Install yq: `brew install yq` (macOS) or see https://github.com/mikefarah/yq

**`Config file not found`**
Copy the template: `cp config-template.yaml ~/.openclaw/workspace/antigravity-bridge.yaml`

**`rsync: command not found`**
Install rsync: `brew install rsync` (macOS) or `sudo apt install rsync`

**No results from memory_search**
- Check that `memorySearch.extraPaths` includes the destination folder
- Restart OpenClaw after changing extraPaths
- Verify files landed in the right place: `ls ~/.openclaw/workspace/antigravity/`

**Files not updating**
- Run with `--verbose` to see rsync output
- Check source paths exist: `ls ~/repo/acme-corp/acme-platform/.agent/memory/`

**Wrong files synced**
- Only `.md` files are synced (rsync filter: `--include='*.md' --exclude='*'`)
- To sync other file types, edit sync.sh patterns

---

## Security & Privacy

- **All data stays local.** No external API calls, no cloud sync, no network access.
- **Only `.md` files are synced.** rsync filters (`--filter='+ *.md' --filter='- *'`) enforce markdown-only transfer. No secrets, credentials, API keys, binary state, session tokens, or config files are ever copied.
- `.agent/` and `.gemini/` directories are Antigravity's documentation folders containing markdown notes about rules, tasks, memory, and project context. They do **not** contain credentials or sensitive runtime state — those are stored elsewhere by the IDE.
- sync.sh only reads from user-configured source paths and writes to a designated OpenClaw workspace subfolder.
- No credentials or tokens required to run.
- Safe to run with `--dry-run` to inspect behavior before committing.
- **Dependencies:** `rsync` (system), `yq` (YAML parser) — both declared in manifest metadata.
