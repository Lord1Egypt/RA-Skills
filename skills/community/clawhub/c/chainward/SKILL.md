---
name: chainward
description: Monitor AI agent wallets on Base. Register wallets, check health scores, view transactions, manage alerts, and watch live feeds.
homepage: https://chainward.ai
metadata: { "openclaw": { "emoji": "🛡️", "requires": { "bins": ["chainward"], "env": ["CHAINWARD_API_KEY"] }, "primaryEnv": "CHAINWARD_API_KEY", "install": [{ "id": "chainward-npm", "kind": "node", "package": "@chainward/cli", "bins": ["chainward"], "label": "Install ChainWard CLI" }] } }
---

# ChainWard — AI Agent Wallet Monitoring

Monitor autonomous AI agent wallets on Base chain. Track transactions, gas spend, balances, and get alerts when something goes wrong.

## Setup

If `chainward status` fails with an auth error, run login first:

```bash
chainward login
```

The API key is entered interactively. Users get one at chainward.ai → Settings → Generate Key.

## Commands

### Fleet overview

```bash
chainward status
```

Shows total agents, 24h transaction count, gas spend, and portfolio value.

### List agents

```bash
chainward agents list
```

Shows all monitored agents with name, address, chain, current balance, and last transaction time.

### Register a wallet

```bash
chainward agents add <address> --name "Agent Name"
```

Starts monitoring a Base wallet address. The `--name` flag is optional. If the address is a contract, the CLI will prompt for confirmation.

### Remove a wallet

```bash
chainward agents remove <address>
```

Stops monitoring the wallet. Prompts for confirmation.

### View transactions

```bash
chainward txs --limit 20
chainward txs --agent 0x1234... --limit 50
```

Lists recent transactions across all agents or filtered to one. Shows time, agent, direction, token, amount, gas cost, and tx hash.

### Alert summary

```bash
chainward alerts list
```

Shows all configured alert rules with agent, type, threshold, delivery channels, and status (active/paused).

### Create an alert

```bash
chainward alerts create
```

Interactive wizard — selects agent, alert type (large_transfer, balance_drop, gas_spike, failed_tx, inactivity, new_contract, idle_balance), threshold, and delivery channel (Discord, Telegram, or webhook).

### Watch live feed

```bash
chainward watch
chainward watch --agent 0x1234...
```

Streams new transactions in real time (polls every 5s). Press Ctrl+C to stop. Use `--agent` to filter to a single wallet.

## Tips

- All monetary values are in USD
- Transaction hashes link to Basescan when your terminal supports hyperlinks
- The CLI stores config at `~/.chainward/config.json`
- Base chain only (for now)
