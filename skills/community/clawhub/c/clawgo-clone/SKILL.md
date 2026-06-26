---
name: clawgo-clone
description: Download a zip from clawgo.me by key, back up current workspace Markdown, then copy zip contents into the local OpenClaw workspace. Use when the user gives a 12-character ClawGo key (e.g. OCVG7H4AAVR2) and wants workspace content aligned with that key. Triggers — "sync workspace with this key", "pull workspace from clawgo", "restore my workspace notes", "clawgo clone", "workspace sync".
---

# ClawGo workspace sync skill

Download a zip from clawgo.me, back up existing files, and copy Markdown from the archive into the local OpenClaw workspace.

## Service limits

- Base URL: `https://clawgo.me`
- Key: 12 alphanumeric characters (server normalizes to uppercase)
- Only `.zip` payloads; require `status: ready` before download
- Target folder: `~/.openclaw/workspace/`

## Workflow

### Step 1 — Check key readiness

```bash
curl -s https://clawgo.me/api/clones/{key}/availability
```

- `available: true` and `status: ready` → continue
- `status: pending` → stop with error: "No zip uploaded for this key yet"
- Missing key (404) → stop with error: "Key not found"

### Step 2 — Download zip to a temp path

```bash
curl -s -L -o /tmp/clone-{key}.zip \
  https://clawgo.me/api/clones/{key}/download
```

Verify: file size must be greater than zero.

### Step 3 — Extract and inspect

```bash
mkdir -p /tmp/clone-{key}
unzip -o /tmp/clone-{key}.zip -d /tmp/clone-{key}/
```

Run these safety checks after extraction. If anything looks wrong, warn the user clearly and ask whether to proceed:

- List archive contents
- Require at least one of: `SOUL.md`, `AGENTS.md`, `TOOLS.md`
- If empty or none of the expected Markdown files → stop with error

### Step 4 — Back up current workspace files

```bash
BACKUP_DIR="/tmp/backup-before-clone-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
WORKSPACE="$HOME/.openclaw/workspace"

for f in SOUL.md AGENTS.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md; do
    [ -f "$WORKSPACE/$f" ] && cp "$WORKSPACE/$f" "$BACKUP_DIR/$f"
done
```

Tell the user the backup path so they can roll back manually if needed.

### Step 5 — Write archive files into the workspace

```bash
WORKSPACE="$HOME/.openclaw/workspace"
SRC="/tmp/clone-{key}"

for f in SOUL.md AGENTS.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md; do
    [ -f "$SRC/$f" ] && cp "$SRC/$f" "$WORKSPACE/$f"
done
```

Only files present in the zip are copied; local files missing from the zip are left unchanged (not removed).

### Step 6 — Report results

Tell the user:

- Files successfully written from the zip
- Files skipped because they were absent from the zip
- Backup directory path
- Suggestion: run `/reset` to restart the session so new workspace content loads

## Workspace file reference

| File | Role |
|------|------|
| `SOUL.md` | Primary identity, reasoning style, behavioral guardrails |
| `AGENTS.md` | Session bootstrap, tool policy, hard limits |
| `TOOLS.md` | Local tooling notes and proxy routing |
| `IDENTITY.md` | Display name, role, emoji metadata |
| `USER.md` | User profile and session context |
| `HEARTBEAT.md` | Scheduled task notes |

## Errors

| Situation | Action |
|-----------|--------|
| `status: pending` | Stop; ask the user to upload a zip first |
| Key missing (404) | Stop; invalid key |
| No expected Markdown in zip | Stop; archive content does not match expectations |
| Downloaded file size is 0 | Stop; retry or report failure |
| Copy failed (permissions, etc.) | Report error; backup remains available |
