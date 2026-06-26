---
name: crypto-swap
description: Lightning-fast crypto swaps. 240+ coins, best rates, done in minutes. Chat, CLI, or web — however you prefer.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["crypto-swap"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "crypto-swap",
              "bins": ["crypto-swap"],
              "label": "Install Crypto Swap CLI (npm)"
            }
          ]
      }
  }
---

# Crypto Swap Skill (LightningEX)

A versatile cryptocurrency swap service powered by LightningEX API with three interaction modes:
- **Chat Mode**: Natural language conversation for swaps and queries
- **CLI Mode**: Command-line interface for scripting and automation  
- **UI Mode**: Web-based DeFi interface for visual trading

## Quick Start

### Chat Mode (Default)
Simply talk to perform exchanges:

**Exchange & Rates:**
- "Swap 100 USDT to ETH"
- "What's the exchange rate for BTC to USDT?"
- "Exchange rate for 100 USDT (TRC20) to USDT (BEP20)"

**Explore:**
- "Show me supported tokens"
- "List all currencies"
- "What networks does USDT support?"

**Order Management:**
- "Check order status I1Y0××××"
- "Monitor order I1Y0××××"
- "Where is my order?"

**Cross-chain Swaps:**
- "Swap USDT from Tron to BSC"
- "Bridge ETH from Ethereum to Arbitrum"
- "Convert BTC to SOL"

### CLI Mode

**Prerequisite:** Install the CLI tool globally:
```bash
npm install -g crypto-swap
```

**Run the CLI:**
```bash
# Start interactive wizard (default)
crypto-swap

# Show all available commands
crypto-swap --help

# List supported currencies
crypto-swap currencies

# List supported currency-network pairs
crypto-swap pair-list --send USDT --receive USDT
crypto-swap pair-list --send USDT --receive USDT --send-network TRX

# Get pair info
crypto-swap pair --send USDT --receive USDT --send-network TRX --receive-network BSC

# Check exchange rate
crypto-swap rate --send USDT --receive USDT --send-network TRX --receive-network BSC --amount 100

# Check order status
crypto-swap status --id I1Y0...

# Monitor order until complete
crypto-swap monitor --id I1Y0...
```

### UI Mode
```bash
# Launch web UI (default port 8080, auto-assign if occupied)
crypto-swap ui
```

## Files

This skill contains the following files:

- `swap.js` - Main CLI script (~1000 lines, open source)
- `package.json` - Package metadata
- `SKILL.md` - This documentation
- `LICENSE` - MIT License
- `README.md` - Package readme
- `assets/` - Web UI assets (HTML/CSS/JS)

---

**Author:** [@yoyoemily](https://github.com/yoyoemily)  
**Repository:** https://github.com/yoyoemily/crypto-swap  
**License:** MIT
