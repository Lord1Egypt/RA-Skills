---
name: aegisclaw
description: "Use this skill when the user asks to manage Binance assets, check account security, scan for arbitrage opportunities, or perform automated dust sweeps. Commands: init, check, scan, arbitrage, dust, report, status. Requires BINANCE_API_KEY and BINANCE_API_SECRET environment variables."
license: MIT
metadata:
  author: hyy2099
  version: "1.0.0"
  homepage: "https://github.com/hyy2099/aegisclaw"
---

# AegisClaw - 金甲龙虾 (Binance Security & Profit Guardian)

🦞 A defensive AI agent based on the **principle of least privilege** and Binance sub-account ecosystem, focusing on low-risk automated asset management and arbitrage.

## When to Use This Skill

Use this skill when the user asks to:
- Check Binance account security status
- Scan for idle assets and dust
- Monitor funding rate arbitrage opportunities
- Perform dust sweeps (convert small balances to BNB)
- Generate weekly profit reports
- Initialize or configure Binance API connection

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `init <api_key> <api_secret>` | Initialize plugin with Binance API credentials | `/aegisclaw init key secret` |
| `check` | Run security fence check | `/aegisclaw check` |
| `scan` | Scan idle assets and dust | `/aegisclaw scan` |
| `arbitrage` | Scan funding rate arbitrage opportunities | `/aegisclaw arbitrage` |
| `dust [assets]` | Execute dust sweep (convert small balances) | `/aegisclaw dust` |
| `report` | Generate weekly profit report | `/aegisclaw report` |
| `status` | View current status | `/aegisclaw status` |
| `help` | Display help information | `/aegisclaw help` |

## Required Environment Variables

The skill requires the following environment variables (set via `.env` file or system environment):

- `BINANCE_API_KEY` - Binance API Key (required)
- `BINANCE_API_SECRET` - Binance API Secret (required)
- `BINANCE_TESTNET` - Whether to use testnet (optional, default: false)

## Key Features

### 🛡️ Security Fence
- **Sub-account sandbox isolation** - Recommended to use independent sub-accounts
- **API permission self-check** - Automatically detect and warn of dangerous permission configurations
- **Operation firewall** - Slippage limits, trading frequency control

### 💰 Profit Engine
- **Launchpool/Megadrop monitoring** - Intelligent scan for new mining opportunities
- **Automatic dust conversion** - Automatically convert small assets to BNB (Dust Sweeper)
- **Funding rate arbitrage** - Risk-free arbitrage between spot and futures

### 📊 Data Statistics
- **Balance snapshot recording** - Automatically save daily asset snapshots
- **Trade history tracking** - SQLite database persistence
- **Weekly profit reports** - One-click generate and share profit reports

## Security Recommendations

1. **Use Sub-accounts**: Create a sub-account with only 500-1000 USDT for operations. Do not use main accounts.

2. **Limit API Permissions**:
   - ✅ Enable: Spot Trading (SPOT)
   - ❌ Disable: Withdrawals (WITHDRAW)
   - ❌ Disable: Futures Trading (FUTURES)

3. **Bind IP Whitelist**: Restrict API to access from specific IPs only. Regularly check IP whitelist.

4. **Control Fund Scale**: Sub-account funds recommended within 1000 USDT. Use idle funds that won't affect daily life.

## Usage Flow

### Initial Setup
1. Initialize with API credentials: `/aegisclaw init <api_key> <api_secret>`
2. Run security check: `/aegisclaw check`
3. Verify account type and permissions

### Daily Operations
1. Scan assets: `/aegisclaw scan`
2. Check arbitrage opportunities: `/aegisclaw arbitrage`
3. Execute dust sweep if needed: `/aegisclaw dust`

### Weekly Review
1. Generate weekly report: `/aegisclaw report`
2. Review profit/loss and asset distribution

## Error Handling

- **Invalid API credentials**: The skill will report initialization failure and prompt to check API key and secret
- **Permission denied**: If API lacks required permissions, the skill will warn and suggest adjusting settings
- **Rate limit exceeded**: The skill will notify you to retry later
- **Network error**: The skill will attempt one retry before asking user to try again later

## Integration Notes

This skill integrates with OpenClaw through the plugin interface in `openclaw_plugin/plugin.py`. It can be called via:
- Direct commands in chat interfaces
- Scheduled tasks via cron jobs
- Automated workflows with other skills

## Key Safety Points

- Never share or expose API keys or secrets in logs or user-facing messages
- Always validate permissions before executing trading operations
- Use sub-accounts with limited funds for safety
- Monitor account balance regularly and set reasonable limits
- This skill is designed for low-risk operations - avoid high-risk trading strategies

## Repository & Support

- **GitHub**: https://github.com/hyy2099/aegisclaw
- **License**: MIT
- **Author**: hyy2099

🦞 **AegisClaw** - Your Binance risk-free profit guardian and asset protector
