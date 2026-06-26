# Braingit protocol (Markdown-only snapshots)

Goal: keep a git commit history of Markdown changes (notes, specs, research, plans) without touching code.

## Recommended conventions
- Commit message default: `md: snapshot`.
- Keep `.gitignore` tight (exclude logs, caches, downloaded media).
- Avoid storing secrets in Markdown; if unavoidable, exclude specific paths.

## Suggested automation patterns
- Run on a schedule (cron/launchd) to create periodic snapshots.
- Or run after a pipeline step that updates `.md` files.

## OpenClaw cron example
(If OpenClaw CLI is available on the host)

```bash
openclaw cron add \
  --name braingit-md-midnight \
  --description "Midnight: commit markdown changes snapshot" \
  --cron "0 0 0 * * *" --tz Europe/Madrid \
  --session isolated \
  --timeout-seconds 120 \
  --message "Run <PATH_TO_SKILL>/scripts/commit_md_changes.sh \"md(midnight): snapshot\"" \
  --no-deliver
```

Replace `<PATH_TO_SKILL>` with the installed skill folder.
