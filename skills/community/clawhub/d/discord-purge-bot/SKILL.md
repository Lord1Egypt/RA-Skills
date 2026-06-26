---
name: discord-purge-bot
description: "Operate a Discord message cleanup workflow with an official bot token and Discord HTTP API. Use when asked to purge guild channel history, delete messages by user/keyword/time window, run dry-run previews, execute guarded bulk deletion jobs, or recreate a channel for fast wipe. Do not use for self-bot cleanup or personal DM history wipe."
---

# Discord Purge Bot

Run controlled cleanup in Discord guild channels with safety gates and audit-friendly outputs.

## Safety Contract

- Use only a bot token (`DISCORD_BOT_TOKEN` or `--token`).
- Refuse user-account token flows and self-bot behavior.
- Run `purge-preview.mjs` first for every destructive request.
- Require explicit confirmation code before running deletion.
- Abort if channel is not a guild channel.
- Keep logs and JSON summaries for each run.

## Workflow

1. Collect scope: `channel-id`, optional `author-id`, `contains`, `regex`, `after`, `before`.
2. Read `references/discord-limits.md` before deletion runs.
3. Run preview to estimate impact and get confirm code.
4. Run deletion with confirm code.
5. Share summary: scanned, matched, deleted, failed, old-vs-recent split.

## Commands

### Preview

```bash
node scripts/purge-preview.mjs \
  --channel-id 123456789012345678 \
  --author-id 987654321098765432 \
  --contains "error" \
  --after "2026-03-01T00:00:00Z" \
  --max-scan 5000 \
  --out ./tmp/purge-preview.json
```

### Run Purge

```bash
node scripts/purge-runner.mjs \
  --channel-id 123456789012345678 \
  --author-id 987654321098765432 \
  --contains "error" \
  --after "2026-03-01T00:00:00Z" \
  --confirm "PURGE-XXXXXXXX" \
  --state-file ./tmp/purge-state.json \
  --out ./tmp/purge-result.json
```

### Dry Run

```bash
node scripts/purge-runner.mjs --channel-id 123456789012345678 --confirm "PURGE-XXXXXXXX" --dry-run
```

### Clone or Nuke Channel

```bash
node scripts/purge-nuke.mjs --channel-id 123456789012345678 --confirm "NUKE-XXXXXXXX" --out ./tmp/nuke.json
node scripts/purge-nuke.mjs --channel-id 123456789012345678 --confirm "NUKE-XXXXXXXX" --delete-old --out ./tmp/nuke.json
```

## Script Roles

- `scripts/purge-preview.mjs`: scan channel messages, apply filters, return counts and confirm code.
- `scripts/purge-runner.mjs`: execute deletion with 2-week split (`bulk-delete` + single delete fallback).
- `scripts/purge-nuke.mjs`: create replacement channel; optionally delete original channel.
- `scripts/scan-filter.mjs`: reusable scan and filtering logic.
- `scripts/discord-api.mjs`: Discord API wrapper with rate-limit retries.
- `scripts/job-code.mjs`: deterministic confirm code helpers.

## Operator Rules

- Keep `max-scan` bounded for broad channels.
- Use `--state-file` on long jobs.
- Prefer content/user/time filters over whole-channel wipes.
- Use nuke mode only when preserving channel history is unnecessary.
- Treat pinned messages as protected unless `--include-pinned` is set.

## Troubleshooting

- 401/403: verify bot token and channel permissions.
- Empty preview with expected history: check `READ_MESSAGE_HISTORY`.
- Heavy 429: reduce parallelism and keep retry handling enabled.
- `bulk-delete` failures: expect messages older than 14 days, runner falls back to single deletes.
- Cannot reach Discord behind a proxy: export `HTTP_PROXY`/`HTTPS_PROXY` (uppercase recommended) and run with `NODE_USE_ENV_PROXY=1`, or use a recent Node that supports `setGlobalProxyFromEnv()`.
- If your proxy tool exposes both HTTP and SOCKS ports, point `HTTP_PROXY`/`HTTPS_PROXY` at the HTTP port; `ALL_PROXY=socks5://...` alone is not enough for this skill.

### Proxy Example

```bash
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
export NODE_USE_ENV_PROXY=1

node scripts/purge-preview.mjs --channel-id 123456789012345678 --max-scan 200
```
