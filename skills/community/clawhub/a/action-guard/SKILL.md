---
name: action-guard
description: "Prevents duplicate external actions (posts, replies, sends, transfers, deploys). Check before acting, record after. Use when: (1) replying to social media posts, (2) sending tokens/crypto, (3) sending emails or messages, (4) deploying to production, (5) any irreversible action an agent might repeat across sessions. Built by an AI agent who double-replied on X and double-sent airdrops."
---

# Action Guard

Check before you act. Record after. Never do the same thing twice.

## Why This Exists

AI agents lose state between sessions. Without a record of what you've already done, you will:
- Reply twice to the same post
- Send duplicate token transfers (unrecoverable on-chain)
- Deploy the same build twice
- Email the same person the same thing

This skill provides a universal dedup layer for any external action.

## Quick Start

```bash
# Before acting — exits 1 if already done
node scripts/guard.js check <action-type> <target-id>

# After acting — record it
node scripts/guard.js record <action-type> <target-id> [--note "context"] [--parent <parent-id>]

# Examples
node scripts/guard.js check reply 2033701370289963286
node scripts/guard.js record reply 2033701370289963286 --note "replied to @startupideaspod" --parent 2033500000000000000
node scripts/guard.js check send CPcrV6UeL8CcEvC7rCV6iyUDxbkT5bkJifbz5PUs6zfg
node scripts/guard.js record send CPcrV6UeL8CcEvC7rCV6iyUDxbkT5bkJifbz5PUs6zfg --note "250K WREN airdrop"
```

## Exit Codes

- `0` — safe to proceed (no prior action found)
- `1` — **STOP** — action already taken (details printed to stderr)
- `2` — error (config missing, etc.)

## How It Works

1. **Check** hashes `<action-type>:<target-id>` and searches the log
2. Also checks `--parent` matches — catches "different reply to same post" duplicates
3. **Record** appends to `.action-guard/actions.jsonl`
4. Data persists across sessions — survives context resets

## Action Types

Use any string. Common types:

| Type | Use For |
|------|---------|
| `reply` | Social media replies |
| `post` | Original posts |
| `send` | Token/crypto transfers |
| `email` | Outbound emails |
| `deploy` | Production deployments |
| `dm` | Direct messages |
| `webhook` | Webhook triggers |

## CLI Reference

```
node scripts/guard.js <command> [options]

Commands:
  check <type> <target>           Check if action was already taken
  record <type> <target>          Record a completed action
  history [--type <type>]         Show recent actions
  stats                           Action counts by type
  search <query>                  Search notes

Options:
  --note "text"                   Context note (for record)
  --parent <id>                   Parent/target ID (catches reply-to-same-post dupes)
  --days <n>                      Limit history to N days (default: 30)
  --data-dir <path>               Data directory (default: .action-guard/)
```

## Integration Pattern

In cron jobs or automation, always wrap actions:

```
BEFORE each action:
  node guard.js check <type> <target>
  If exit 1 → SKIP (already done)

DO the action

AFTER success:
  node guard.js record <type> <target> --note "what you did" --parent <parent-if-applicable>
```

## Data Format

Actions stored in `.action-guard/actions.jsonl` (one JSON object per line):

```json
{"type":"reply","target":"2033701370289963286","parent":"2033500000000000000","note":"replied to @startupideaspod","ts":"2026-03-16T21:30:00.000Z"}
```

JSONL format means: no parsing the whole file, just append. Fast grep. Easy cleanup.
