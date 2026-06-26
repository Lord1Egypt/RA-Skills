---
name: claw-insights-snapshot
description: 'Generate visual status cards for your OpenClaw agent as PNG, SVG, or JSON. The rendered cards are designed for social sharing and mobile-friendly channels — cute, compact, and informative at a glance. Use when pushing agent status to Slack, Telegram, Discord, WhatsApp, or any chat channel, generating visual reports of token usage and session activity, extracting metrics programmatically, or scheduling periodic status updates via cron.'
---

# Snapshot Status Cards

**Announce at start:** "I'm generating a visual status card for your OpenClaw agent."

## What is a Snapshot?

A snapshot is a server-rendered visual status card — not a browser screenshot. Powered by Satori, it renders in ~200ms with no browser dependency.

The output is designed to look great in chat: compact, readable on mobile, and visually appealing enough to share. It shows token usage, session activity, error counts, and gateway health in a single glance.

Formats: PNG (default), SVG, or raw JSON for programmatic use.

## REST API

```bash
curl -X POST http://127.0.0.1:41041/api/snapshot \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"detail":"standard","range":"6h","theme":"dark"}' \
  -o snapshot.png
```

No-auth mode: start with `claw-insights start --no-auth`, then omit the Authorization header.

Response includes `Content-Disposition` header with timestamped filename.

## CLI

```bash
claw-insights snapshot                        # Save to ~/.claw-insights/snapshots/
claw-insights snapshot --quick -o status.png  # Compact mobile snapshot
claw-insights snapshot --format json | jq .   # JSON to stdout
claw-insights snapshot --dry-run              # Preview parameters only
```

CLI flags: `--format`, `--detail`, `--range`, `--theme`, `--lang`, `-o <path>`, `-t <token>`, `--port`, `--quick`, `--dry-run`. Run `claw-insights snapshot --help` for full usage.

## Parameters

| Field    | Default (REST / CLI)      | Options                             | Description            |
| -------- | ------------------------- | ----------------------------------- | ---------------------- |
| `detail` | `standard`                | `compact` / `standard` / `full`     | Detail level           |
| `format` | `png`                     | `png` / `svg` / `json`              | Output format          |
| `range`  | `24h` (REST) / `6h` (CLI) | `30m` / `1h` / `6h` / `12h` / `24h` | Time range for metrics |
| `theme`  | `dark`                    | `dark` / `light`                    | Color theme            |
| `lang`   | `en`                      | `en` / `zh`                         | Language               |

> **Note:** REST API and CLI have different default `range` values. REST defaults to `24h` (full day overview), CLI defaults to `6h` (quick status check). Both accept the same set of values.

### Which detail level?

- **compact** — Summary numbers only (session count, total tokens, error count). Best for embedding in chat messages.
- **standard** — Session list + metrics charts. Default for most use cases.
- **full** — Everything: session list, all charts, event log. Best for reports and archival.

## Common Workflows

### Push status card to a channel

Works with any messaging channel — Slack, Telegram, Discord, WhatsApp, etc.

```bash
# 1. Generate a compact status card
curl -X POST http://127.0.0.1:41041/api/snapshot \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"detail":"compact","range":"6h"}' \
  -o /tmp/status.png

# 2. Send via your channel's tool or API
#    The compact detail level is optimized for mobile chat bubbles.
```

**Tips:**

- `compact` — best for chat messages (summary numbers only, small image)
- `standard` — best for daily check-ins (session list + charts)
- `full` — best for reports and archival

### Scheduled status report

```bash
# Full snapshot with 24h range
curl -X POST http://127.0.0.1:41041/api/snapshot \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"detail":"full","range":"24h"}' \
  -o /tmp/daily-report.png
```

### Programmatic metrics extraction

```bash
# Get raw data as JSON
curl -X POST http://127.0.0.1:41041/api/snapshot \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"format":"json","range":"6h"}' \
  -o metrics.json
```

JSON schema: See [references/json-schema.md](references/json-schema.md)

## Error Handling

| Status             | Cause                        | Fix                                         |
| ------------------ | ---------------------------- | ------------------------------------------- |
| `401`              | Missing or invalid token     | Check Bearer token, or use `--no-auth` mode |
| `502`              | OpenClaw gateway not running | `openclaw gateway start`                    |
| `500`              | Internal server error        | Check logs: `~/.claw-insights/logs/`        |
| Connection refused | claw-insights not running    | `claw-insights start`                       |
