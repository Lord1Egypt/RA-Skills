---
name: byreal-perps-cli
description: "Byreal Hyperliquid perpetual futures trading CLI: account setup, market/limit orders with TP/SL, position close-market/close-limit/close-all, leverage control, trade history, market signal scanner & technical analysis. Use when user mentions Hyperliquid, perps, perpetual futures, leverage trading, or market signals/technical analysis."
metadata:
  openclaw:
    homepage: https://github.com/byreal-git/byreal-perps-cli
    requires:
      bins:
        - byreal-perps-cli
    install:
      - kind: node
        package: "@byreal-io/byreal-perps-cli"
        global: true
---

# Hyperliquid Perps Trading

## Installation

```bash
# Check if already installed
which byreal-perps-cli && byreal-perps-cli --version

# Install
npm install -g @byreal-io/byreal-perps-cli
```

## Credentials & Permissions

- **All trading commands** require account initialization via `byreal-perps-cli account init` before any trading operations
- Read-only commands (account info, position list, order list, account history): Require initialized perps account
- Write commands (order market, order limit, order cancel, position close-market/close-limit/close-all, position leverage): Require initialized perps account with valid agent wallet
- Signal commands (signal scan, signal detail): No account required — uses public market data only
- Perps agent keys are stored locally in the byreal data directory with strict file permissions (mode 0600)
- The CLI never transmits private keys over the network — keys are only used locally for transaction signing
- AI agents should **never** ask users to paste private keys in chat; always direct them to run `byreal-perps-cli account init` interactively

## WebSocket / API Fallback

Some commands (`account info`, `position list`, `position close-market`, `position close-limit`, `position close-all`) use WebSocket subscriptions to fetch real-time data. If the WebSocket connection fails or times out, the CLI **automatically falls back to HTTP API** calls. No user action is needed.

If a command returns a connection error:
1. The CLI will retry via HTTP API automatically; if it still fails, the issue is likely network connectivity or Hyperliquid API downtime.
2. Check network connectivity: `curl -s https://api.hyperliquid.xyz/info -X POST -H 'Content-Type: application/json' -d '{"type":"meta"}'`
3. For testnet, check: `curl -s https://api.hyperliquid-testnet.xyz/info -X POST -H 'Content-Type: application/json' -d '{"type":"meta"}'`
4. If HTTP API also fails, the Hyperliquid service may be temporarily unavailable — retry after a short wait.

## Hard Constraints

1. **`-o json` only for parsing** — when showing results to the user, **omit it** and let the CLI's built-in tables render directly. Never fetch JSON then re-draw tables yourself.
2. **Never display private keys** — use keypair paths only
3. **Never call the SDK directly** — do NOT write `node -e` / `tsx -e` scripts that `import` or `require` packages like `@nktkas/hyperliquid` or `viem`. Always use `byreal-perps-cli` commands to interact with Hyperliquid. The SDK is bundled inside the CLI; calling it externally causes CJS/ESM compatibility errors.

## Commands Reference

### Account Management

```bash
# Initialize perps account (interactive wizard)
byreal-perps-cli account init

# Show account info & balance
byreal-perps-cli account info

# Show recent trade history
byreal-perps-cli account history
```

### Orders

```bash
# Market order (side: buy/sell/long/short, size in coin units)
byreal-perps-cli order market <side> <size> <coin>
byreal-perps-cli order market buy 0.01 BTC --tp 110000 --sl 90000

# Limit order
byreal-perps-cli order limit <side> <size> <coin> <price>
byreal-perps-cli order limit sell 1 ETH 4000

# List open orders
byreal-perps-cli order list

# Cancel an order
byreal-perps-cli order cancel <coin> <oid>

# Cancel all orders
byreal-perps-cli order cancel-all -y
```

### Positions

```bash
# List open positions
byreal-perps-cli position list

# Set leverage (1-50x)
byreal-perps-cli position leverage <coin> <leverage>

# Close at market price (full or partial)
byreal-perps-cli position close-market <coin>

# Close with limit order
byreal-perps-cli position close-limit <coin> <price>

# Close all positions
byreal-perps-cli position close-all -y
```

### Market Signals

```bash
# Scan markets for trading signals
byreal-perps-cli signal scan

# Detailed technical analysis
byreal-perps-cli signal detail <coin>
```

### Update

```bash
# Check for available CLI updates
byreal-perps-cli update check

# Install the latest CLI version
byreal-perps-cli update install
```

### Testnet

All commands support `--testnet`:

```bash
byreal-perps-cli --testnet account info
```
