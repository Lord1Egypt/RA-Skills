# Crypto Sniping — Binance CEX Trading Bot

**Version:** 1.0.0  
**Author:** Subhuti  
**Chains:** BTC, ETH, SOL (Binance Spot & Futures)  

---

## Quick Start

1. **Set API keys:**
   ```bash
   export BINANCE_API_KEY="your_key"
   export BINANCE_API_SECRET="your_secret"
   ```

2. **Test mode first:**
   ```bash
   openclaw skills crypto-sniping --test
   ```

3. **Live trading:**
   ```bash
   openclaw skills crypto-sniping --live
   ```

---

## Features

### 📊 Signal Generation
- **Technical Indicators:** RSI, MACD, Bollinger Bands, EMA crossovers
- **Volume Analysis:** Unusual volume spikes, order flow imbalance
- **Support/Resistance:** Auto-detect key levels, breakout alerts

### 🤖 Auto-Trading
- **Entry Conditions:** RSI < 30 (oversold), MACD bullish crossover, volume spike > 200%
- **Exit Conditions:** RSI > 70 (overbought), take-profit hit, stop-loss triggered
- **Position Sizing:** Fixed amount or % of portfolio per trade

### 🛡️ Risk Management
- **Stop-Loss:** Fixed % (e.g., -5%) or trailing stop
- **Take-Profit:** Tiered (sell 50% at 2x, 25% at 5x, 25% at 10x)
- **Daily Limits:** Max trades per day, max loss per day

### 🐋 Whale Tracking
- **Large Orders:** Alert when >$1M order hits order book
- **Liquidation Cascades:** Monitor funding rates, liquidation clusters
- **Smart Money Flow:** Track exchange inflows/outflows

### 📱 Notifications
- **Telegram:** Real-time alerts for signals, fills, liquidations
- **Web Dashboard:** View open positions, P&L, trade history

---

## Configuration

Create `config.yaml`:

```yaml
# Trading Settings
trading:
  mode: paper  # paper or live
  assets: [BTCUSDT, ETHUSDT, SOLUSDT]
  default_position_size: 100  # USDT per trade
  max_daily_trades: 5
  max_daily_loss: 500  # USDT

# Entry Signals
entry:
  rsi_oversold: 30
  rsi_period: 14
  macd_fast: 12
  macd_slow: 26
  volume_spike_threshold: 2.0  # 200% of average
  min_confidence: 2  # Require 2+ signals to trigger

# Risk Management
risk:
  stop_loss_percent: 5
  take_profit_tiers:
    - { percent: 100, sell: 50 }   # At 100% profit, sell 50%
    - { percent: 400, sell: 25 }   # At 400% profit, sell 25%
    - { percent: 900, sell: 25 }   # At 900% profit, sell 25%
  trailing_stop: true
  trailing_stop_percent: 10

# Whale Alerts
whale:
  min_order_size: 1000000  # USDT
  liquidation_threshold: 10000000  # USDT
  funding_rate_alert: 0.01  # 1%

# Notifications
notifications:
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    chat_id: "${TELEGRAM_CHAT_ID}"
  log_level: INFO
```

---

## Commands

```bash
# Start monitoring (paper trading)
openclaw skills crypto-sniping start --config config.yaml

# Check signals without trading
openclaw skills crypto-sniping scan

# View open positions
openclaw skills crypto-sniping positions

# View trade history
openclaw skills crypto-sniping history --days 7

# View whale alerts
openclaw skills crypto-sniping whales --threshold 1000000

# Stop bot
openclaw skills crypto-sniping stop

# Backtest strategy
openclaw skills crypto-sniping backtest --asset BTCUSDT --days 30
```

---

## Architecture

```
crypto-sniping/
├── src/
│   ├── binance_client.py    # API wrapper
│   ├── signals.py           # Technical analysis
│   ├── trader.py            # Order execution
│   ├── risk_manager.py      # Position/risk management
│   ├── whale_tracker.py     # Large order monitoring
│   └── notifier.py          # Telegram alerts
├── config.yaml              # User configuration
├── trades.db                # SQLite trade log
└── SKILL.md                 # This file
```

---

## Safety First

⚠️ **Never share API keys in chat**  
⚠️ **Start with paper trading**  
⚠️ **Set daily loss limits**  
⚠️ **Use restricted API keys** (trading only, no withdrawals)

---

## Troubleshooting

**"Invalid API key"**
- Check key permissions (Enable Spot & Futures Trading)
- Ensure IP whitelist includes your machine

**"Insufficient balance"**
- Check USDT balance in Spot wallet
- Paper mode uses virtual balance

**"No signals generated"**
- Lower confidence threshold in config
- Check if markets are trending (signals work best in ranging markets)

---

## Future Enhancements

- [ ] Machine learning signal prediction
- [ ] Multi-exchange arbitrage
- [ ] Options strategies
- [ ] Copy trading (follow whale wallets)
- [ ] Social sentiment analysis

---

_"The market can stay irrational longer than you can stay solvent."_ — John Maynard Keynes
