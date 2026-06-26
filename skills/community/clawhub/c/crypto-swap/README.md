# crypto-swap

---
name: crypto-swap
description: Lightning-fast crypto swaps. 240+ coins, best rates, done in minutes. Chat, CLI, or web — however you prefer.
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

**Run the CLI:**
```bash
# Navigate to skill directory
cd /path/to/crypto-swap

# Start interactive wizard (default)
node swap.js

# Show all available commands
node swap.js --help
```

### UI Mode
```bash
# Launch web UI (default port 8080, auto-assign if occupied)
node swap.js ui
```
Then open http://localhost:8080 (or the displayed port) in your browser for the DeFi-style trading interface.
