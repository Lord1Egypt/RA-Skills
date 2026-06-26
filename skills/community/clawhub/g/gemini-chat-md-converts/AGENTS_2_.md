# AGENTS.md - Solana Funding Arbitrage Bot

This file provides guidelines for AI coding agents working on the Solana Funding Arbitrage Bot.

## Project Overview

**Solana Funding Arbitrage Bot** - Automated funding rate arbitrage across Solana perpetual DEXs (Drift, Flash Trade, Zeta Markets).

- **Language:** TypeScript
- **Runtime:** Node.js 18+
- **Strategy:** Delta-neutral funding rate arbitrage
- **Version:** 2.0

## Build / Test / Lint Commands

### Development
```bash
# Navigate to project
cd ~/Projects/solana-arbitrage/scripts

# Install dependencies
npm install

# Run scanner (development)
npm run scan

# Run dashboard
npm run dashboard

# Run specific DEX scanner
npm run scan:drift
npm run scan:zeta
```

### Testing
```bash
# Run backtest
npm run backtest

# Run Monte Carlo simulation
npm run monte-carlo

# Dry run (no real trades)
npm run trade:dry
```

### Production Trading
```bash
# Check status
npm run trade:status

# Run auto-trader (LIVE TRADING)
npm run trade

# Scan only (no trades)
npm run trade:scan
```

### Build
```bash
# Compile TypeScript
npm run build

# Start compiled version
npm start
```

## Code Style Guidelines

### TypeScript
- Strict mode enabled
- Explicit types on function parameters and returns
- Use interfaces for data structures
- Prefer `const` over `let`

### Naming Conventions
- **Files:** `kebab-case.ts`
- **Classes:** `PascalCase`
- **Interfaces:** `PascalCase`
- **Functions/Variables:** `camelCase`
- **Constants:** `SCREAMING_SNAKE_CASE`

### Project Structure
```
scripts/
├── src/
│   ├── core/           # Arbitrage engine, aggregators
│   ├── protocols/      # DEX protocol clients (Drift, Flash)
│   ├── dex/           # DEX integrations (Jupiter)
│   ├── trading/       # Auto-trader, position manager
│   ├── dashboard/     # Web UI
│   └── utils/         # Logger, helpers
├── references/        # Documentation
├── backtest-1month.ts
├── monte-carlo.ts
└── cron-runner.sh
```

### Error Handling
- Wrap external calls in try-catch
- Log all errors with context
- Graceful degradation (continue on non-critical errors)

```typescript
import { logger } from '../utils/logger';

try {
  const rates = await driftClient.getFundingRates();
  return rates;
} catch (error) {
  logger.error('Failed to fetch Drift rates', { error, market });
  return null; // Continue with other DEXs
}
```

## Configuration

### Environment Variables
Create `.env` in scripts/ directory:
```bash
# Solana RPC - Helius (RECOMMENDED)
# Free tier: 100k requests/day, no rate limiting issues
# Sign up at: https://helius.xyz
SOLANA_RPC_URL=https://mainnet.helius-rpc.com/?api-key=YOUR_API_KEY_HERE

# Alternative: Public RPC (slower, rate limited)
# SOLANA_RPC_URL=https://api.mainnet-beta.solana.com

# Wallet (for live trading)
SOLANA_PRIVATE_KEY=your_base58_private_key
# OR
SOLANA_KEYPAIR_PATH=/path/to/keypair.json
```

### Helius Setup (Step-by-Step)

**Why Helius?**
- ✅ Free tier: 100k requests/day (plenty for development)
- ✅ No rate limiting headaches
- ✅ No front-running or sandwich attacks (unlike public RPCs)
- ✅ Better performance for trading bots

**How to Set Up:**

1. **Go to https://helius.xyz**
2. **Sign up for free account** (no credit card needed)
3. **Click "New Endpoint"**
4. **Select Network:** Mainnet
5. **Copy the URL** - looks like:
   ```
   https://mainnet.helius-rpc.com/?api-key=3a2b1c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p
   ```
6. **Paste into your `.env` file:**
   ```bash
   SOLANA_RPC_URL=https://mainnet.helius-rpc.com/?api-key=YOUR_KEY_HERE
   ```

**Test Your Connection:**
```bash
# This will verify your RPC connection works
curl -X POST "$SOLANA_RPC_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"getHealth"}'
```

**Expected Response:**
```json
{"jsonrpc":"2.0","result":"ok","id":1}
```

### Config Files
- `~/.secrets/funding-arb-config.json` - Trader configuration
- `~/.clawd/funding-arb/trader-state.json` - Runtime state (auto-created)

### Strategy Config
Edit trader config for risk parameters:
```json
{
  "strategy": "conservative",
  "max_position_pct": 10,
  "min_spread": 15,
  "max_dd_pct": 5,
  "leverage": 2
}
```

## Security Notes

⚠️ **CRITICAL:**
- Private keys in `~/.secrets/` - never commit this directory
- Start with `DRY_RUN=true` for testing
- Use small position sizes initially
- Monitor funding rate changes closely

## Supported DEXs

| DEX | Status | Markets |
|-----|--------|---------|
| Drift | ✅ Active | SOL, BTC, ETH perps |
| Flash Trade | ✅ Active | Multiple perps |
| Zeta Markets | ✅ Active | Options + perps |

## Key Concepts

### Funding Rate Arbitrage
1. Find two DEXs with opposite funding rates
2. Long on DEX with negative funding (get paid)
3. Short on DEX with positive funding (get paid)
4. Collect funding differential while delta-neutral

### Risk Management
- Maximum drawdown limits
- Stop-loss on spread reversal
- Position size limits
- Auto-rebalancing

## Cron Scheduling

Run every 4 hours via crontab:
```bash
0 */4 * * * /Users/ryanmolinich/Projects/solana-arbitrage/scripts/cron-runner.sh
```

## Logs

- Console output during development
- File logs: `/tmp/funding-arb-*.log`
- Cron logs: `~/.clawd/funding-arb/logs/`

## Documentation

- `USER_GUIDE.md` - Setup and usage
- `references/setup.md` - Installation guide
- `references/strategies.md` - Strategy details
- `references/api.md` - API documentation

## Related Projects

This project is extracted from OpenClaw skill:
- Original: `~/.openclaw/skills/solana-funding-arb-2.1.0.zip`
- Standalone: `~/Projects/solana-arbitrage/`

Also related to:
- `~/Projects/pocket-options-bot/` - Another trading bot (binary options)

---

**Note:** Trading involves risk. This bot is for educational purposes. Test thoroughly before using real funds.
