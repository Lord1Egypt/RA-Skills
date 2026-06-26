---
name: crypto-safe-portfolio-analyzer-pro
description: "Safe cryptocurrency portfolio tracking and P&L analysis. Monitors portfolio value, calculates profit/loss with custom cost basis, tracks live prices via CoinGecko, and generates detailed reports. Use for portfolio performance tracking, P&L calculation, position monitoring, allocation analysis, and market overviews."
---

# Crypto SAFE Portfolio Analyzer Pro

Track cryptocurrency portfolios, calculate P&L with custom cost basis, and generate comprehensive reports with live market data.

## Overview

This skill provides professional-grade portfolio tracking for cryptocurrency investors. It fetches live prices from CoinGecko, calculates accurate P&L based on your cost basis, and generates detailed reports showing position breakdown, allocations, and performance metrics.

**Key Features:**
- Real-time price tracking for 20+ cryptocurrencies
- Custom cost basis for accurate P&L calculation
- Portfolio allocation analysis with target vs. actual comparisons
- Market sentiment analysis across watchlists
- Multiple output formats (text reports, JSON data)
- Integration-ready for Discord bots, automated alerts, and cron jobs

## Quick Start

### 1. Analyze Portfolio Holdings

For a quick portfolio analysis, provide holdings as a JSON object:

```bash
python3 scripts/portfolio-analyzer.py portfolio --holdings '{"BTC": 1.5, "ETH": 10.2, "SOL": 50, "DOGE": 10000}'
```

**Expected Output:**
```
📊 CRYPTO PORTFOLIO REPORT
==================================================
💰 Total Value: $125,750.50
🟢 Total P&L: $15,750.50 (+14.32%)

📈 POSITION BREAKDOWN:
BTC:
  💵 Value: $89,237.50 (71.0% of portfolio)
  🟢 P&L: $8,987.50 (+11.20%)
  🔴 24h: -3.92%
```

### 2. Market Overview

Get sentiment and price overview for your watchlist:

```bash
python3 scripts/portfolio-analyzer.py market
```

### 3. Set Up Configuration

For advanced features like cost basis tracking, create `portfolio-config.json`:

```json
{
  "cost_basis": {
    "BTC": 45000,
    "ETH": 2800,
    "SOL": 85
  },
  "watchlist": ["BTC", "ETH", "SOL", "DOGE", "XRP"],
  "target_allocation": {
    "BTC": 40,
    "ETH": 30,
    "SOL": 20,
    "Other": 10
  }
}
```

## Core Capabilities

### 1. Portfolio Value Calculation

Calculates total portfolio value with position-level breakdown:

- **Live pricing** from CoinGecko API (no API key required)
- **Cost basis tracking** for accurate P&L calculation
- **24-hour change** for each position
- **Portfolio allocation** percentages
- **Total portfolio P&L** with percentage gains/losses

**Supported Coins:** BTC, ETH, SOL, DOGE, XRP, ADA, AVAX, LINK, DOT, UNI, NEAR, ATOM, and more.

### 2. Market Analysis

Provides market sentiment analysis across your watchlist:

- **Market sentiment** classification (Bullish/Bearish/Neutral)
- **Average 24-hour change** across all tracked coins
- **Individual coin performance** with prices and changes
- **Market cap data** for supported cryptocurrencies

### 3. Report Generation

Multiple output formats for different use cases:

**Text Format:** Human-readable reports with emoji indicators and formatted numbers
```bash
# Generate text report
python3 scripts/portfolio-analyzer.py portfolio --holdings holdings.json
```

**JSON Format:** Structured data for automation and integrations
```bash
# Generate JSON data for automation
python3 scripts/portfolio-analyzer.py portfolio --holdings holdings.json --format json
```

### 4. Integration Ready

Designed for automation and integration:

- **Discord bot integration** - Post daily portfolio updates
- **Cron job automation** - Schedule regular portfolio checks
- **Alert systems** - Monitor portfolio value thresholds
- **API consumption** - JSON output ready for webhooks and APIs

## Common Use Cases

### Daily Portfolio Monitoring

Set up automated daily reports:

```bash
# Add to cron or OpenClaw cron jobs
python3 scripts/portfolio-analyzer.py portfolio --holdings ~/.crypto/holdings.json > daily-report.txt
```

### Rebalancing Analysis

Compare current vs. target allocations:

1. Set target allocations in `portfolio-config.json`
2. Run portfolio analysis to see current allocations
3. Identify positions that need rebalancing

### Performance Tracking

Monitor P&L over time:

```bash
# Log daily values for trend analysis
echo "$(date): $(python3 scripts/portfolio-analyzer.py portfolio --holdings holdings.json --format json | jq '.total_value')" >> portfolio-history.log
```

### Tax Reporting

Generate P&L data for tax calculations:

```bash
# Export detailed P&L breakdown
python3 scripts/portfolio-analyzer.py portfolio --holdings holdings.json --format json | jq '.breakdown'
```

## Configuration Options

### Cost Basis Setup

Define your average purchase prices for accurate P&L:

```json
{
  "cost_basis": {
    "BTC": 45000,    // Your average BTC purchase price
    "ETH": 2800,     // Your average ETH purchase price
    "SOL": 85        // Your average SOL purchase price
  }
}
```

Without cost basis, P&L calculations use current price as basis (showing $0 P&L).

### Watchlist Customization

Customize which coins to track in market overviews:

```json
{
  "watchlist": ["BTC", "ETH", "SOL", "DOGE", "XRP", "ADA", "AVAX", "LINK"]
}
```

### Target Allocation

Set portfolio allocation targets for rebalancing analysis:

```json
{
  "target_allocation": {
    "BTC": 40,    // Target 40% Bitcoin
    "ETH": 30,    // Target 30% Ethereum
    "SOL": 20,    // Target 20% Solana
    "Other": 10   // Target 10% other assets
  }
}
```

## Error Handling

The skill includes robust error handling:

- **API failures**: Graceful fallback when CoinGecko is unavailable
- **Invalid holdings**: Clear error messages for malformed JSON
- **Missing config**: Uses sensible defaults when config files are missing
- **Network timeouts**: 10-second timeout with error reporting

## Integration Examples

### Discord Bot Integration

```javascript
const { exec } = require('child_process');

async function postPortfolioUpdate() {
  const command = 'python3 scripts/portfolio-analyzer.py portfolio --holdings holdings.json --format json';
  exec(command, (error, stdout) => {
    if (!error) {
      const portfolio = JSON.parse(stdout);
      const message = `📊 Portfolio: $${portfolio.total_value.toLocaleString()} | P&L: ${portfolio.total_pnl >= 0 ? '🟢' : '🔴'} ${portfolio.total_pnl_pct.toFixed(2)}%`;
      // Send to Discord channel
    }
  });
}
```

### OpenClaw Automation

```javascript
// In OpenClaw skills or cron jobs
const portfolioData = await exec('python3 ~/.openclaw/workspace/skills/crypto-portfolio-tracker/scripts/portfolio-analyzer.py portfolio --holdings holdings.json --format json');
const portfolio = JSON.parse(portfolioData);

if (portfolio.total_value > 100000) {
  await notify('Portfolio over $100k!');
}
```

## Resources

### scripts/
- **portfolio-analyzer.py**: Main portfolio tracking and analysis script
- **portfolio-tracker.js**: Node.js integration wrapper (adapted from crypto-alerts)

### references/
- **usage-examples.md**: Detailed examples, configurations, and integration patterns
- **config-example.json**: Sample configuration file with all available options

For detailed examples and integration patterns, see `references/usage-examples.md`.