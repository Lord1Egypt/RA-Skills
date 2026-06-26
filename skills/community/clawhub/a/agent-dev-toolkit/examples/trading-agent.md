# Example 2: Building a Trading Agent

This example shows how to build a cryptocurrency trading agent with risk management.

## Goal

Create an agent that can:
1. Monitor market conditions
2. Execute trades based on strategies
3. Manage portfolio
4. Implement risk controls

## Step 1: Create the Agent

```bash
openclaw agent create trading-bot \
  --name "Alpha交易员" \
  --role "加密货币交易员" \
  --tone "analytical, cautious, data-driven" \
  --toolkit agent-dev-toolkit
```

## Step 2: Configure Trading Rules

Edit `AGENTS.md`:

```markdown
## Trading Rules

### Risk Management
- Max position size: 5% of portfolio
- Max daily loss: 2% of portfolio
- Max leverage: 3x
- Required confirmation for trades > $1,000

### Never Do
- Trade without stop-loss
- Average down on losing positions
- Trade during high volatility (>10% in 1h)
- Expose more than 20% in single asset

### Always
- Check market conditions before trading
- Set stop-loss and take-profit
- Log all trades
- Review performance weekly
```

## Step 3: Set Up Wallet

Create a trading wallet with strict limits:

```bash
openclaw wallet create \
  --name "trading-wallet" \
  --chain ethereum \
  --daily-limit 5000 \
  --per-tx-limit 1000 \
  --whitelist "0x...uniswap,0x...sushiswap"
```

## Step 4: Add Market Monitoring

Use **Agent Browser** to monitor markets:

```javascript
// Monitor price
async function monitorPrice(token) {
  await browser.navigate(`https://www.coingecko.com/en/coins/${token}`);
  const price = await browser.extract('.price');
  const change = await browser.extract('.change-24h');
  return { price, change };
}

// Check on-chain data
async function checkOnChain(token) {
  await browser.navigate(`https://etherscan.io/token/${token}`);
  const holders = await browser.extract('.holder-count');
  const volume = await browser.extract('.volume-24h');
  return { holders, volume };
}
```

## Step 5: Implement Trading Strategy

```javascript
// Simple momentum strategy
async function executeStrategy(token) {
  const { price, change } = await monitorPrice(token);
  
  if (change > 5 && volume > averageVolume) {
    // Buy signal
    const amount = calculatePosition(portfolio, risk);
    await wallet.transfer(token, amount, 'buy');
    logTrade('BUY', token, amount, price);
  } else if (change < -5) {
    // Sell signal
    const amount = calculatePosition(portfolio, risk);
    await wallet.transfer(token, amount, 'sell');
    logTrade('SELL', token, amount, price);
  }
}
```

## Step 6: Set Up Alerts

```bash
openclaw alert create \
  --agent trading-bot \
  --condition "price_change > 10%" \
  --action "pause_trading" \
  --notify "telegram"
```

## Risk Controls

### Automatic Safeguards

1. **Circuit Breaker**
   - Stops trading if daily loss > 2%
   - Requires manual reset

2. **Position Limits**
   - Max 5% per position
   - Max 20% per sector

3. **Liquidity Checks**
   - Only trade tokens with > $1M volume
   - Avoid slippage > 1%

### Manual Overrides

```bash
# Emergency stop
openclaw agent pause trading-bot

# Resume trading
openclaw agent resume trading-bot

# Force close all positions
openclaw wallet close-all --wallet trading-wallet
```

## Monitoring Dashboard

```bash
# Start dashboard
openclaw dashboard start trading-bot \
  --metrics "pnl,positions,win-rate,risk-level"
```

## Backtesting

Test strategy before live trading:

```bash
openclaw backtest run \
  --strategy momentum \
  --period "2025-01-01 to 2026-03-01" \
  --capital 10000
```

## Performance Tracking

```bash
# Daily report
openclaw report generate trading-bot \
  --type daily \
  --metrics "trades,pnl,win-rate" \
  --output ./reports/daily.md

# Weekly analysis
openclaw report generate trading-bot \
  --type weekly \
  --metrics "performance,strategy,improvements" \
  --output ./reports/weekly.md
```

## Advanced Features

### Multi-Exchange Support

```bash
# Connect to multiple exchanges
openclaw exchange connect binance --agent trading-bot
openclaw exchange connect coinbase --agent trading-bot
openclaw exchange connect kraken --agent trading-bot
```

### Arbitrage Detection

```javascript
async function findArbitrage() {
  const prices = await Promise.all(
    exchanges.map(ex => ex.getPrice('BTC/USD'))
  );
  
  const spread = Math.max(...prices) - Math.min(...prices);
  if (spread > minSpread) {
    executeArbitrage(prices);
  }
}
```

## Cost Analysis

**Initial costs:**
- Toolkit: $29
- Trading capital: Your choice

**Monthly costs:**
- Exchange fees: 0.1% per trade
- OpenClaw: $20-100 (depending on usage)
- Data feeds: $50-200

**Expected returns:**
- Conservative: 5-15% annually
- Moderate: 15-30% annually
- Aggressive: 30-50% annually (higher risk)

**Risk:**
- Possible total loss
- Requires monitoring
- Market volatility

## Safety Tips

1. **Start Small**: Begin with small amounts
2. **Test First**: Use testnet/paper trading
3. **Monitor**: Check regularly
4. **Diversify**: Don't put all eggs in one basket
5. **Learn**: Study markets continuously
