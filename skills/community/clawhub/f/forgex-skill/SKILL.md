# ForgeX CLI

### Launch tokens. Bundle buy. Manage wallets — Just talk to your agent.

On-chain market making, from a single command line to your OpenClaw agent.<br/>No programming required.

---

⛓️ Supported Platforms

[![Sonic SVM](https://img.shields.io/badge/Sonic_SVM-purple?style=for-the-badge)](https://sonic.game) [![Solana](https://img.shields.io/badge/Solana-9945FF?style=for-the-badge&logo=solana&logoColor=white)](https://solana.com) [![Pump.fun](https://img.shields.io/badge/Pump.fun-green?style=for-the-badge)](https://pump.fun) [![Raydium](https://img.shields.io/badge/Raydium-2B6DEF?style=for-the-badge)](https://raydium.io) [![Jito Bundle](https://img.shields.io/badge/Jito_Bundle-orange?style=for-the-badge)](https://jito.wtf) [![OpenClaw](https://img.shields.io/badge/OpenClaw_Native-blue?style=for-the-badge)](https://openclaw.ai)

---

[![npm version](https://img.shields.io/npm/v/forgex-cli?color=blue)](https://www.npmjs.com/package/forgex-cli) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Open Source](https://img.shields.io/badge/Open%20Source-✓-brightgreen)](https://github.com) [![Jito Bundle](https://img.shields.io/badge/Jito%20Bundle-✓-orange)](https://jito.wtf) [![Multi-wallet](https://img.shields.io/badge/Multi--wallet-✓-blue)](.) [![Sonic SVM](https://img.shields.io/badge/Sonic%20SVM-✓-purple)](https://sonic.game) [![OpenClaw Native](https://img.shields.io/badge/OpenClaw%20Native-✓-blue)](https://openclaw.ai) [![On-chain Market Making](https://img.shields.io/badge/On--chain%20Market%20Making-✓-green)](.)

---

[Overview](#why-forgex) · [Quick Start](#quick-start-5-minutes) · [Configure](#config--configuration) · [Command Reference](#command-reference) · [Examples](#workflow-examples)

---

---

## Why ForgeX?

Most on-chain workflows on Solana are painful:

- **Too many manual steps.** Copy-pasting addresses, switching tabs, signing transaction after transaction — every extra step is a chance to make a costly mistake.
- **Repetitive confirmations waste hours.** Manually confirming the same operations over and over drains time that should go toward strategy, not execution.
- **Complex tools lock out non-developers.** If you're not writing custom scripts, most market making tooling is simply inaccessible.

ForgeX packages the full workflow into a clean CLI. One command at a time.

---

## Install

```bash
npm install -g forgex-cli
```

Requires Node.js >= 22.14.0.

Verify installation:

```bash
forgex --version
```

---

## Quick Start (5 minutes)

### Step 1 — Initialize config

```bash
forgex config init --rpc-url "https://your-rpc-endpoint.com" --network mainnet
```

### Step 2 — Create a wallet group

```bash
forgex wallet create-group --name "my-group"
# Returns groupId — note it for subsequent commands
```

### Step 3 — Generate wallets

```bash
forgex --password "your-password" wallet generate --group 1 --count 10
```

### Step 4 — Fund your wallets

Distribute SOL from a source wallet to the group:

```bash
forgex --password "your-password" transfer out \
  --from "YourSourceWalletAddress" \
  --to-group 1 \
  --value 0.1
```

### Step 5 — Launch a token

```bash
forgex --password "your-password" token create \
  --dex pump \
  --name "MyToken" \
  --symbol "MYT" \
  --image ./logo.png \
  --dev-wallet 1 \
  --dev-buy 0.5 \
  --dry-run   # remove --dry-run when ready to go live
```

### Step 6 — Start the volume bot

```bash
forgex --password "your-password" tools volume \
  --group 1 \
  --token "TOKEN_MINT_ADDRESS" \
  --mode 1b1s \
  --amount 0.01 \
  --count 10 \
  --rounds 20 \
  --interval 10000
```

> **Tip:** Always run with `--dry-run` first to simulate the operation before executing on-chain.

---

## Command Reference

All commands accept `--format json|table|minimal` (default: `json`).

Commands involving private keys require `--password` before the subcommand name:

```bash
forgex --password "your-password" <command> [subcommand] [options]
```

---

### `config` — Configuration

| Command | Description |

|---|---|

| `forgex config init` | Initialize config file |

| `forgex config set <key> <value>` | Set a config value |

| `forgex config get [key]` | View config values |

```bash
# Initialize with RPC endpoint
forgex config init --rpc-url "https://my-rpc.com" --network mainnet

# Set Codex API key for market data
forgex config set codexApiKey "your-api-key"

# Set default slippage (BPS)
forgex config set defaultSlippage 300

# View all config
forgex config get
```

---

### `wallet` — Wallet Group Management

**Create & manage groups**

```bash
# Create a local wallet group
forgex wallet create-group --name "market-making-group"

# Create with optional remark
forgex wallet create-group --name "sniper-group" --remark "launch snipers"

# List all wallet groups
forgex wallet list-groups

# View group details (wallet addresses)
forgex wallet group-info --id 1

# Delete a group
forgex wallet delete-group --id 1 --force
```

**Generate & import wallets**

```bash
# Generate new wallets (max 100 per group)
forgex --password "pwd" wallet generate --group 1 --count 10

# Add an existing wallet by private key
forgex --password "pwd" wallet add --group 1 --private-key "Base58Key..." --note "main wallet"

# Remove a wallet from group
forgex --password "pwd" wallet remove --group 1 --address "WalletAddress..."

# Import from CSV (format: privateKey,note)
forgex --password "pwd" wallet import --group 1 --file ./wallets.csv
```

**Backup & restore**

```bash
# Export group as CSV
forgex --password "pwd" wallet export --group 1 --file ./backup.csv

# Export all groups as encrypted JSON
forgex --password "pwd" wallet export-group \
  --file ./all-groups.json \
  --encrypt \
  --password "file-encryption-password"

# Import all groups from JSON backup
forgex --password "pwd" wallet import-group \
  --file ./all-groups.json \
  --password "file-encryption-password"
```

**Vanity addresses**

```bash
# Generate address ending in "pump"
forgex wallet grind --suffix pump

# Generate 3 addresses with custom suffix, using 8 threads
forgex wallet grind --suffix pump --count 3 --threads 8
```

---

### `trade` — Trading

> All trade commands support `--dry-run` for simulation.

**Buy**

```bash
# Simulate buy (recommended before first run)
forgex --password "pwd" trade buy \
  --group 1 --token "TOKEN_CA" --amount 0.1 --dry-run

# Batch buy — all wallets in group buy the same amount
forgex --password "pwd" trade buy \
  --group 1 --token "TOKEN_CA" --amount 0.1 --slippage 300
```

**Sell**

```bash
# Sell all tokens
forgex --password "pwd" trade sell \
  --group 1 --token "TOKEN_CA" --amount all

# Sell 50%
forgex --password "pwd" trade sell \
  --group 1 --token "TOKEN_CA" --amount 50%

# Sell fixed token quantity
forgex --password "pwd" trade sell \
  --group 1 --token "TOKEN_CA" --amount 1000000
```

**Batch (buy + sell in one bundle)**

```bash
# Execute buy and sell in same Jito Bundle
forgex --password "pwd" trade batch \
  --group 1 --token "TOKEN_CA" \
  --type buyWithSell --mode 1b1s --amount 0.01
```

Modes: `1b1s` (1 buy + 1 sell), `1b2s`, `1b3s`, `2b1s`, `3b1s`

**Sniper**

```bash
# Snipe with different amounts per wallet (amounts count must match wallet count)
forgex --password "pwd" trade sniper \
  --group 1 --token "TOKEN_CA" \
  --amounts "0.5,0.3,0.2" --slippage 500
```

---

### `tools` — Market Making

> All tools support `--dry-run`. Use `--rounds` to limit execution.

**Turnover (wallet cycling)**

Cycles tokens between two wallet groups via Jito Bundle — zero price impact.

```bash
# Simulate
forgex --password "pwd" tools turnover \
  --from-group 1 --to-group 2 --token "TOKEN_CA" --dry-run

# Run 5 turnover cycles
forgex --password "pwd" tools turnover \
  --from-group 1 --to-group 2 --token "TOKEN_CA" \
  --daemon --rounds 5 --interval 2000

# Turnover 50% of holdings
forgex --password "pwd" tools turnover \
  --from-group 1 --to-group 2 --token "TOKEN_CA" \
  --amount 50%
```

**Volume bot**

Generates on-chain trading volume with zero net loss (buy + sell in same transaction).

```bash
# Simulate
forgex --password "pwd" tools volume \
  --group 1 --token "TOKEN_CA" --dry-run

# Run 20 rounds, every 10 seconds, using 10 wallets
forgex --password "pwd" tools volume \
  --group 1 --token "TOKEN_CA" \
  --mode 1b1s --amount 0.01 --count 10 \
  --daemon --rounds 20 --interval 10000
```

Options: `--group <id>`, `--token <ca>`, `--mode 1b1s|1b2s|1b3s|2b1s|3b1s`, `--amount <sol>`, `--count <n>` (limit wallets, default: all), `--interval <ms>` (delay between wallets), `--rounds <n>`, `--daemon`, `--dry-run`

**Price robot**

Automatically moves price toward a target by buying (up) or selling (down).

```bash
# Simulate price push
forgex --password "pwd" tools robot-price \
  --group 1 --token "TOKEN_CA" \
  --direction up --target-price 0.001 --dry-run

# Push price up, max spend 5 SOL
forgex --password "pwd" tools robot-price \
  --group 1 --token "TOKEN_CA" \
  --direction up --target-price 0.001 \
  --amount 0.05 --max-cost 5 --interval 3000
```

Options: `--direction up|down`, `--target-price <sol>`, `--amount <sol>`, `--max-cost <sol>`, `--interval <ms>`

---

### `transfer` — Fund Management

> All transfer commands support `--dry-run`.

**Collect (many → one)**

```bash
# Collect all SOL from group into one wallet
forgex --password "pwd" transfer in \
  --to "MainWalletAddress" --from-group 1 --amount all

# Collect from only the first 5 wallets
forgex --password "pwd" transfer in \
  --to "MainWalletAddress" --from-group 1 --amount all --count 5

# Keep 0.01 SOL in each wallet, collect the rest
forgex --password "pwd" transfer in \
  --to "MainWalletAddress" --from-group 1 \
  --amount reserve --value 0.01

# Collect tokens instead of SOL
forgex --password "pwd" transfer in \
  --to "MainWalletAddress" --from-group 1 \
  --token "TOKEN_CA" --amount all
```

**Distribute (one → many)**

> `--from` address must belong to a wallet group (private key required for signing).

```bash
# Send 0.1 SOL to each wallet in group
forgex --password "pwd" transfer out \
  --from "SourceAddress" --to-group 1 --value 0.1

# Distribute to only the first 10 wallets
forgex --password "pwd" transfer out \
  --from "SourceAddress" --to-group 1 --value 0.1 --count 10

# Random distribution between 0.05 and 0.15 SOL
forgex --password "pwd" transfer out \
  --from "SourceAddress" --to-group 1 \
  --amount random --value 0.05 --max 0.15
```

**Many-to-many (wallet[i] → wallet[i])**

```bash
# Transfer all from group 1 wallets to matching group 2 wallets
forgex --password "pwd" transfer many-to-many \
  --from-group 1 --to-group 2 --amount all

# Fixed amount per pair
forgex --password "pwd" transfer many-to-many \
  --from-group 1 --to-group 2 --amount fixed --value 0.1
```

---

### `token` — Token Operations

> Supports `--dry-run` for simulation.

**Create & launch token**

```bash
# Simulate token creation
forgex --password "pwd" token create \
  --dex pump \
  --name "MyToken" --symbol "MTK" \
  --image ./logo.png \
  --description "My token" \
  --dry-run

# Launch with dev buy + snipers in same block (T0 bundle)
forgex --password "pwd" token create \
  --dex pump \
  --name "MyToken" --symbol "MTK" \
  --image ./logo.png \
  --twitter "https://twitter.com/mytoken" \
  --website "https://mytoken.io" \
  --dev-wallet 1 --dev-buy 2.0 \
  --snipers 2 --sniper-amounts "0.5,0.3,0.2" \
  --bundle-time T0
```

Platforms: `pump` (Pump.fun), `launchlab`

Bundle time: `T0` (dev buy + snipers same block), `T1_T5` (snipers 1-5 blocks after dev)

**Query token**

```bash
# Token info (price, name, dex)
forgex token info --ca "TOKEN_CA"

# Liquidity pool info
forgex token pool --ca "TOKEN_CA"
```

---

### `query` — Data Queries

```bash
# SOL balance
forgex query balance --address "WalletAddress"

# Token balance
forgex query balance --address "WalletAddress" --token "TOKEN_CA"

# Token price
forgex query price --token "TOKEN_CA"

# Candlestick data (intervals: 1m, 5m, 15m, 1h, 4h, 1d)
forgex query kline --token "TOKEN_CA" --interval 5m --count 50

# Transaction history for a group
forgex query transactions --group 1 --token "TOKEN_CA"

# Holdings and PnL across a group
forgex query monitor --group 1 --token "TOKEN_CA"
```

---

## Slippage Reference

| BPS | Percentage | Recommended for |

|---|---|---|

| 100 | 1% | Turnover trades |

| 300 | 3% | Normal buy/sell |

| 500 | 5% | Sniping / fast entries |

| 1000 | 10% | High volatility tokens |

| 2000 | 20% | Extreme conditions |

---

## Demo

<!-- 📹 30-second demo video — coming soon -->

---

## Workflow Examples

### Token Launch in 3 commands

```bash
# 1. Create wallets
forgex --password "pwd" wallet generate --group 1 --count 5

# 2. Fund them
forgex --password "pwd" transfer out --from "MainWallet" --to-group 1 --value 0.5

# 3. Launch token with dev buy + snipers
forgex --password "pwd" token create \
  --dex pump --name "MyToken" --symbol "MTK" \
  --image ./logo.png \
  --dev-wallet 1 --dev-buy 1.0 \
  --snipers 1 --sniper-amounts "0.3,0.2,0.1,0.1,0.1" \
  --bundle-time T0
```

### Run the volume bot

```bash
forgex --password "pwd" tools volume \
  --group 1 --token "TOKEN_CA" \
  --mode 1b1s --amount 0.01 --count 10 \
  --rounds 30 --interval 10000
```

### Collect funds back to main wallet

```bash
forgex --password "pwd" trade sell --group 1 --token "TOKEN_CA" --amount all
forgex --password "pwd" transfer in --to "MainWallet" --from-group 1 --amount all
```

---

## Links

- **Twitter:** [@SonicSVM](https://twitter.com/SonicSVM)
- **npm:** [forgex-cli](https://www.npmjs.com/package/forgex-cli)
- **Sonic SVM:** [sonic.game](https://sonic.game)
