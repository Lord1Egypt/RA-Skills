---
name: 17track
description: "Track parcels and shipments via the 17TRACK API. Manage a local SQLite database of tracked packages with automatic status polling, webhook ingestion, and daily reports with auto-cleanup. Use this skill whenever the user mentions package tracking, parcel tracking, shipment status, 17TRACK, tracking numbers, delivery status, or wants to check where a package is -- even if they just say 'track this', 'where is my order', or 'any updates on my package' without naming 17TRACK explicitly. Also use for automating delivery notifications and daily shipping reports."
user-invocable: true
metadata: {"requiredEnv": ["TRACK17_TOKEN"], "optionalEnv": ["TRACK17_WEBHOOK_SECRET", "TRACK17_DATA_DIR", "TRACK17_WORKSPACE_DIR"]}
---

# 17TRACK Parcel Tracking

Track parcels using the **17TRACK Tracking API v2.2**. Stores everything in a local SQLite database — no external dependencies beyond Python 3 stdlib.

## Requirements

- `TRACK17_TOKEN` — your 17TRACK API token (sent as the `17token` header). Configure it in `~/.clawdbot/clawdbot.json`:

```json
{
  "skills": {
    "entries": {
      "17track": {
        "enabled": true,
        "apiKey": "YOUR_17TRACK_TOKEN"
      }
    }
  }
}
```

Or export `TRACK17_TOKEN` in your shell.

## Data Storage

Data lives under `<workspace>/packages/track17/` where `<workspace>` is auto-detected from the skill installation path (parent of the `skills/` directory). Override with `TRACK17_DATA_DIR` or `TRACK17_WORKSPACE_DIR`.

## Quick Start

```bash
python3 {baseDir}/scripts/track17.py init                                     # Initialize DB
python3 {baseDir}/scripts/track17.py add "RR123456789CN" --label "Headphones"  # Add a package
python3 {baseDir}/scripts/track17.py sync                                      # Poll for updates
python3 {baseDir}/scripts/track17.py list                                      # List all packages
python3 {baseDir}/scripts/track17.py status 1                                  # Details for package #1
```

If carrier auto-detection fails, specify one: `--carrier 3011`

## Common Commands

| Action | Command |
|--------|---------|
| Add package | `add "TRACKING_NUM" --label "Description" [--carrier CODE]` |
| List all | `list` |
| Sync updates | `sync` |
| Package details | `status <id-or-tracking-number>` |
| Stop tracking | `stop <id>` |
| Resume tracking | `retrack <id>` |
| Remove from DB | `remove <id>` |
| API quota | `quota` |

## Webhooks (optional)

17TRACK can push updates instead of polling. Prefer polling (`sync`) for simplicity — webhooks are only needed if you want real-time updates.

```bash
# Run a webhook HTTP server
python3 {baseDir}/scripts/track17.py webhook-server --bind 127.0.0.1 --port 8789

# Or ingest a payload directly
cat payload.json | python3 {baseDir}/scripts/track17.py ingest-webhook

# Process saved payloads from inbox
python3 {baseDir}/scripts/track17.py process-inbox
```

Set `TRACK17_WEBHOOK_SECRET` to verify webhook signatures.

## Daily Reports with Auto-Cleanup

The `scripts/track17-daily-report.py` script syncs all packages, auto-removes delivered ones, and prints a formatted status report to stdout. It uses the same path resolution and env vars as the main script — no hardcoded paths or external config files.

```bash
TRACK17_TOKEN=your-token python3 {baseDir}/scripts/track17-daily-report.py
```

## Agent Guidance

- Prefer **sync** (polling) over webhooks unless the user explicitly wants push updates — it's simpler and doesn't require a server.
- After adding a package, run `status` to confirm the carrier was detected and tracking data is available.
- When summarizing, prioritize actionable items: delivered/out-for-delivery, exceptions, customs holds, carrier handoffs.
- Delivered packages are automatically cleaned up by the daily report. For ad-hoc checks, use `sync` then `list`.
- Never echo `TRACK17_TOKEN` or `TRACK17_WEBHOOK_SECRET` — these are secrets.
