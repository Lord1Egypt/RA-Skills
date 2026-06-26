# Crypto Portfolio Tracker - Usage Examples

## Configuration File Format

Create a `portfolio-config.json` file with your portfolio settings:

```json
{
  "wallets": {
    "Main Wallet": {
      "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0eB1E",
      "added_date": "2026-03-19"
    }
  },
  "watchlist": ["BTC", "ETH", "SOL", "DOGE", "XRP", "ADA", "AVAX"],
  "cost_basis": {
    "BTC": 45000,
    "ETH": 2800,
    "SOL": 85,
    "DOGE": 0.08
  },
  "target_allocation": {
    "BTC": 40,
    "ETH": 30,
    "SOL": 15,
    "Other": 15
  }
}
```

## Example Commands

### 1. Analyze Portfolio Holdings

```bash
# From JSON string
python3 scripts/portfolio-analyzer.py portfolio --holdings '{"BTC": 1.5, "ETH": 10.2, "SOL": 50}'

# From file
python3 scripts/portfolio-analyzer.py portfolio --holdings ./my-holdings.json
```

### 2. Market Overview

```bash
# Text format
python3 scripts/portfolio-analyzer.py market

# JSON format for automation
python3 scripts/portfolio-analyzer.py market --format json
```

### 3. Add Wallet for Tracking

```bash
python3 scripts/portfolio-analyzer.py wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f0eB1E --name "Main Wallet"
```

## Sample Holdings File Format

Create `holdings.json`:

```json
{
  "BTC": 1.25,
  "ETH": 8.5,
  "SOL": 75,
  "DOGE": 10000,
  "XRP": 2500,
  "ADA": 1000
}
```

## Expected Outputs

### Portfolio Report (Text Format)

```
📊 CRYPTO PORTFOLIO REPORT
==================================================
Generated: 2026-03-19 15:30:45

💰 Total Value: $125,750.50
🟢 Total P&L: $15,750.50 (+14.32%)

📈 POSITION BREAKDOWN:
--------------------------------------------------
BTC:
  💵 Value: $89,237.50 (71.0% of portfolio)
  🟢 P&L: $8,987.50 (+11.20%)
  🔴 24h: -3.92%

ETH:
  💵 Value: $18,642.38 (14.8% of portfolio)
  🟢 P&L: $4,842.38 (+35.10%)
  🔴 24h: -5.84%

SOL:
  💵 Value: $7,177.50 (5.7% of portfolio)
  🔴 P&L: -$1,452.50 (-16.84%)
  🔴 24h: -4.21%
```

### Market Overview

```
🌍 CRYPTO MARKET OVERVIEW
==============================
Sentiment: Bearish
Avg 24h Change: -4.52%

Top Coins:
  🔴 BTC: $71,390.00 (-3.92%)
  🔴 ETH: $2,193.28 (-5.84%)
  🔴 SOL: $95.70 (-4.21%)
  🔴 DOGE: $0.094 (-5.99%)
```

## Integration Examples

### Use in OpenClaw Skills

```javascript
// In another skill or automation
const { exec } = require('child_process');

// Get portfolio value
exec('python3 ~/.openclaw/workspace/skills/crypto-portfolio-tracker/scripts/portfolio-analyzer.py portfolio --holdings ./holdings.json --format json', 
  (error, stdout, stderr) => {
    if (!error) {
      const portfolio = JSON.parse(stdout);
      console.log(`Portfolio worth: $${portfolio.total_value.toLocaleString()}`);
    }
  });
```

### Discord Bot Integration

```javascript
// Post daily portfolio updates to Discord
const portfolioData = await runPortfolioAnalyzer();
const message = `📊 **Daily Portfolio Update**
💰 Total: $${portfolioData.total_value.toLocaleString()}
${portfolioData.total_pnl >= 0 ? '🟢' : '🔴'} P&L: $${portfolioData.total_pnl.toLocaleString()} (${portfolioData.total_pnl_pct.toFixed(2)}%)`;

await sendToDiscord(message);
```

## Cost Basis Setup

Update your cost basis in the config file as you make purchases:

```json
{
  "cost_basis": {
    "BTC": 45000,    // Average buy price
    "ETH": 2800,     // Average buy price
    "SOL": 85,       // Average buy price
    "DOGE": 0.08     // Average buy price
  }
}
```

This enables accurate P&L calculation based on your actual entry prices.

## Automation Ideas

1. **Daily Portfolio Reports**: Set up a cron job to email you daily portfolio summaries
2. **Price Alerts**: Monitor when your portfolio hits certain value thresholds
3. **Rebalancing Alerts**: Get notified when allocations drift from targets
4. **Tax Reporting**: Export P&L data for tax preparation
5. **Performance Tracking**: Log daily portfolio values to track performance over time