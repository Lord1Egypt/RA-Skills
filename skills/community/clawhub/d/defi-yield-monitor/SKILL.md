---
name: defi-yield-monitor
description: Monitor DeFi lending & savings positions across Aave v3, SparkLend, Spark Savings, and Kamino. Track balances, APY, health factors, and compute 7d/30d realized yield. No API keys required. Use when user asks about DeFi positions, lending yields, stablecoin earnings, portfolio health, or wants automated DeFi reporting. Triggers: "check DeFi", "lending yield", "DeFi收益", "持仓", "APY", "health factor", "stablecoin yield", "Aave", "Spark savings", "Kamino", "DeFi report".
---

# DeFi Yield Monitor

Self-contained skill for cross-chain DeFi position & yield monitoring. All data from public endpoints — no API keys needed.

## First-Time Setup

Run the setup script to clone the project, create venv, and init config:

```bash
bash <skill_dir>/scripts/setup.sh
```

Then edit the config with wallet addresses:

```bash
$EDITOR ~/.openclaw/workspace/projects/defi-yield-monitor/config/config.json
```

### Config Template

```json
{
  "wallets": {
    "evm": ["0xYourEthWallet"],
    "solana": ["YourSolanaWallet"]
  },
  "protocols": [
    { "chain": "eth", "name": "aave" },
    { "chain": "bsc", "name": "aave" },
    { "chain": "eth", "name": "spark" },
    { "chain": "eth", "name": "spark_savings" },
    { "chain": "solana", "name": "kamino" }
  ],
  "thresholds": {
    "min_health_factor": 1.25,
    "max_daily_drawdown_pct": 5
  }
}
```

Remove protocols you don't use. Only include chains where you have positions.

## Commands

Use the run script (auto-detects proxy):

```bash
# Daily report — positions + risk alerts
bash <skill_dir>/scripts/run.sh --text

# Yield summary — 7d/30d PnL + per-protocol APY
bash <skill_dir>/scripts/run.sh --yield-summary

# JSON output — for programmatic use
bash <skill_dir>/scripts/run.sh --json
```

Or run directly:

```bash
cd ~/.openclaw/workspace/projects/defi-yield-monitor
.venv/bin/python main.py --config config/config.json --yield-summary
```

## Automated Daily Reports

Create an OpenClaw cron job to collect snapshots and report yields:

- **Schedule**: twice daily (e.g. `13 9,21 * * *`)
- **Command**: `bash <skill_dir>/scripts/run.sh --yield-summary`
- **Delivery**: announce to user's Telegram/Discord

After 7 days of snapshots, `--yield-summary` shows actual realized returns (not just APY estimates).

## Supported Protocols

| Protocol | Chains | What It Tracks |
|----------|--------|---------------|
| Aave v3 | ETH, BSC | Supply/borrow, APY, health factor |
| SparkLend | ETH, Base | Supply/borrow, health factor |
| Spark Savings | ETH | spUSDC/spUSDT/sUSDS vault yields |
| Kamino | Solana | Lending obligations, APY |

## Output Fields

- Per position: chain, protocol, wallet, supplied_usd, borrowed_usd, net_value_usd, apy_supply, apy_borrow, health_factor
- Yield summary: current APY per protocol, 7d/30d PnL (absolute + %), annualized APY from actual returns
- Risk alerts: health factor below threshold, daily drawdown exceeding limit

## Proxy

The run script auto-detects QuickQ/Clash/V2Ray proxies. To set manually:

```bash
export https_proxy=http://127.0.0.1:10020
export http_proxy=http://127.0.0.1:10020
```

## Source

https://github.com/reed1898/defi-yield-monitor
