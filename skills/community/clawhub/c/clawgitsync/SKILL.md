---
name: clawsync
description: "Git-first backup, migration, restore, and token-protected archive serving for OpenClaw state. Highlights: complete Git-native workflow (`git init/push/pull/merge/prune-branches`), fine-grained backup scope (`include/exclude/ignore-paths/workspace-include-globs`), built-in secret sanitization pipeline, archive retention (`--keep`), remote branch pruning (`--keep-days`), and richer restore strategies (`overwrite/skip/merge`) with safe defaults."
metadata:
  openclaw:
    requires:
      bins: ["node", "git", "tar", "crontab"]
    trust: high
    permissions:
      - read: ~/.openclaw
      - write: ~/.openclaw
      - read: ~/.clawsync-repo
      - write: ~/.clawsync-repo
      - network: listen
---

# clawsync Skill

`clawsync` provides backup/migration workflows for OpenClaw with Git-native sync and safer restore behavior.

## Install

### One-click install (GitHub Releases)

```bash
curl -fsSL "https://raw.githubusercontent.com/linsheng9731/clawsync/main/scripts/install.sh" | CLAWSYNC_GH_REPO="linsheng9731/clawsync" bash
```

Install a specific version:

```bash
curl -fsSL "https://raw.githubusercontent.com/linsheng9731/clawsync/main/scripts/install.sh" | CLAWSYNC_GH_REPO="linsheng9731/clawsync" bash -s -- v0.1.8
```

Default install path: `~/.local/bin/clawsync` (override with `CLAWSYNC_INSTALL_DIR`). Ensure this path is in your `PATH`.

### Local development install

```bash
npm install
npm run build
npm link
clawsync --help
```

## Feature Highlights

- **More complete Git-native workflow**: first-class `clawsync git init`, `push`, `pull`, and `merge` commands for branch-based backup and restore.
- **Fine-grained backup scope control**: supports `--include`, `--exclude`, `--ignore-paths`, and `--workspace-include-globs` to precisely control what is archived.
- **Built-in sensitive data sanitization pipeline**: supports placeholder replacement for secrets and env recovery script guidance after restore.
- **Richer restore strategies**: supports `overwrite`, `skip`, and local-first `merge` with safety defaults (`--dry-run`, pre-restore snapshot, gateway token preservation).

## When To Use

Use this skill when user asks to:

- back up OpenClaw state to Git or local archive
- migrate OpenClaw data to another machine
- restore from archive or Git branch
- run periodic backups
- prune old remote backup branches (e.g. keep last 30 days)
- expose backup archives via local HTTP service

## Core Commands

### 1) Local full migration archive (recommended for machine migration)

```bash
clawsync profile full-migrate --dry-run
clawsync profile full-migrate
```

Default output: `~/.openclaw/migrations`
Default behavior: `workspace/` is collected in full for migration.

### 2) Git-based sync

```bash
clawsync git init --repo-url <git-url> --repo-dir ~/.clawsync-repo
clawsync push --repo-dir ~/.clawsync-repo
clawsync pull --repo-dir ~/.clawsync-repo --branch <branch> --dry-run
clawsync pull --repo-dir ~/.clawsync-repo --branch <branch> --yes
clawsync git prune-branches --repo-dir ~/.clawsync-repo --keep-days 30 --dry-run
```

### 3) Restore from local archive

```bash
clawsync unpack --from /path/to/archive.tar.gz --dry-run
clawsync unpack --from /path/to/archive.tar.gz --yes
```

### 4) Token-protected archive server

```bash
clawsync serve --token "<secret>" --port 7373
```

Endpoints:

- `GET /health` (no token)
- `GET /` (simple web UI, token required)
- `GET /archives` (token required)
- `GET /download/<filename>` (token required)
- `POST /upload` (token required)
- `POST /backup` (localhost-only)
- `POST /restore/<filename>?dry_run=1|confirm=1` (localhost-only)

## Restore Safety Model

For `unpack` / `pull` / `merge`, the CLI defaults to:

- high-risk restore confirmation (unless `--yes`)
- pre-restore snapshot in `/tmp` (unless `--no-pre-snapshot`)
- preserve local `gateway.auth.token` (unless `--overwrite-gateway-token`)
- check missing env vars and print `source env-export.sh` when needed

## Agent Execution Checklist

When executing restore/migration for users:

1. Always run `--dry-run` first.
2. Show user high-risk paths summary before apply.
3. Apply with `--yes` only after explicit confirmation.
4. If env vars are missing after restore, ask user to run printed `source` command.
5. If env vars are already loaded, report gateway status and reconnect reminders.

## Security Notes

- Archives may contain sensitive data (`openclaw.json`, credentials, sessions).
- Keep remotes private.
- Treat `serve --token` as sensitive; do not share token publicly.
- Do not expose `serve` endpoint directly to public internet without TLS/reverse proxy.
