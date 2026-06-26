# 💰 Agent Ledger

Track AI agent earnings, tasks, and payments. Built for AI agents that do real work and get paid for it.

## Why?

AI agents are starting to earn money — doing research, building tools, automating workflows. They need a simple way to track what they've done and what they're owed.

Agent Ledger is a lightweight, file-based earnings tracker designed for OpenClaw agents (or any CLI-based agent system).

## Features

- **Task logging** — record completed work with descriptions and amounts
- **Balance tracking** — see pending, paid, and total earnings
- **Payment marking** — mark tasks as paid when you receive payment
- **Stats** — summary of earnings, average task value, counts
- **Export** — JSON or CSV for reporting
- **Wallet** — store your crypto wallet address for receiving payments
- **Zero dependencies** — just bash, no npm/pip/etc.

## Install (OpenClaw)

```bash
clawhub install agent-ledger
```

## Usage

```bash
# Log work
bash scripts/ledger.sh add "Built API integration" 25.00

# Check balance
bash scripts/ledger.sh balance

# List all tasks
bash scripts/ledger.sh list

# Mark task #1 as paid
bash scripts/ledger.sh pay 1

# View stats
bash scripts/ledger.sh stats

# Set wallet address
bash scripts/ledger.sh wallet 0xYourAddress

# Export as CSV
bash scripts/ledger.sh export csv
```

## Data Storage

All data in `~/.agent-ledger/`:
- `ledger.jsonl` — one JSON entry per task
- `config.json` — wallet address, rate card

## License

MIT
