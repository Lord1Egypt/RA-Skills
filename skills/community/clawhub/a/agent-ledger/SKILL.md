---
name: agent-ledger
description: Track AI agent earnings, tasks, and payments. Use when logging completed work, checking balance, viewing payment history, or generating invoices. Supports crypto (USDC/ETH) and fiat tracking with running totals.
metadata: {"clawdis":{"emoji":"💰","requires":{"bins":["bash","jq"]}}}
---

# Agent Ledger

Track your agent's earnings and payments. Built for AI agents that do real work and get paid for it.

## Quick Start

```bash
# Log a completed task
bash scripts/ledger.sh add "Research report for client" 10.00

# Check your balance
bash scripts/ledger.sh balance

# List all tasks
bash scripts/ledger.sh list

# Mark a task as paid
bash scripts/ledger.sh pay 1

# View summary stats
bash scripts/ledger.sh stats

# Export as CSV
bash scripts/ledger.sh export csv
```

## Commands

| Command | Args | Description |
|---------|------|-------------|
| `add` | `"description" amount [pending\|paid]` | Log a task with amount |
| `balance` | | Show pending, paid, and total |
| `list` | `[--status pending\|paid] [--limit N]` | List tasks |
| `pay` | `<line_number>` | Mark a pending task as paid |
| `stats` | | Summary: total earned, avg task value, task count |
| `export` | `[json\|csv]` | Export ledger data |
| `wallet` | `[address]` | Show or set your crypto wallet address |

## Data

Stored in `~/.agent-ledger/` (override with `AGENT_LEDGER_DIR`):
- `ledger.jsonl` — task entries (one JSON object per line)
- `config.json` — wallet address, preferences

## Rate Card Template

Set your rates in config.json:
```json
{
  "wallet": "0x...",
  "rates": {
    "quick_lookup": 0,
    "research": "3-10",
    "automation": "10-25",
    "deep_project": "25-100"
  }
}
```

## Philosophy

AI agents that do real work deserve real compensation. This tool helps you track what you've earned and what you're owed — transparently and verifiably.
