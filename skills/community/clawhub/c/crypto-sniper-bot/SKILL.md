# Crypto Sniper Bot

## Overview
24/7 automated token sniper bot for pump.fun and four.meme platforms. Automatically detects new token launches, evaluates quality, executes trades, and manages positions with take-profit/stop-loss strategies.

## Key Features
- 🤖 Automated monitoring of pump.fun and four.meme
- 🎯 Intelligent quality filtering
- 💰 Automated buying and selling
- 📊 Take-profit and stop-loss management
- 🔔 Multi-channel notifications
- 📈 Real-time position tracking
- 📜 Complete trading history

## How It Works

### 1. Token Discovery
- Monitors pump.fun and four.meme every 30 seconds
- Detects newly launched tokens
- Filters duplicates

### 2. Quality Evaluation
Tokens are scored based on:
- **Liquidity**: Minimum $1000 recommended
- **Holder Count**: Minimum 10 holders
- **Token Age**: Prefers very new tokens (0-5 minutes)
- **Market Cap**: Higher is better

Tokens must score 60+ to qualify for purchase.

### 3. Automated Trading
- Buys qualified tokens with configured amount
- Tracks all open positions
- Monitors price changes in real-time
- Executes sells based on strategy

### 4. Strategy Management
- **Take Profit**: Sells when profit reaches target %
- **Stop Loss**: Sells when loss reaches limit %
- **Trailing Stop**: Locks in profits on big winners
- **Position Limits**: Maximum concurrent positions

### 5. Notifications
Sends alerts for:
- Successful buys with transaction details
- Successful sells with P&L
- Errors and warnings
- Status updates

## Configuration

### Trading Strategy
```javascript
{
  "buyAmount": 0.1,              // SOL per trade
  "takeProfitPercent": 50,       // Sell at +50%
  "stopLossPercent": 30,         // Sell at -30%
  "maxPositions": 10             // Max concurrent trades
}
```

### Quality Filters
```javascript
{
  "minLiquidity": 1000,          // Minimum $1000 liquidity
  "minHolders": 10,              // Minimum 10 holders
  "maxHolderConcentration": 50   // Max 50% in top holder
}
```

## API Endpoints

### POST /configure
Configure bot settings
```json
{
  "walletPrivateKey": "base58_encoded_key",
  "buyAmount": 0.1,
  "takeProfitPercent": 50,
  "stopLossPercent": 30,
  "maxPositions": 10
}
```

### POST /start
Start the bot (requires configuration)

### POST /stop
Stop the bot

### GET /status
Get current status, positions, and P&L

### GET /history
Get trading history with statistics

### POST /notifications
Configure notification channels
```json
{
  "telegram": {
    "enabled": true,
    "botToken": "your_token",
    "chatId": "your_chat_id"
  },
  "discord": {
    "enabled": true,
    "webhookUrl": "your_webhook"
  },
  "email": {
    "enabled": true,
    "host": "smtp.gmail.com",
    "user": "your_email",
    "pass": "your_password",
    "to": "recipient"
  }
}
```

## Security

### Critical Security Measures
1. **Private Key Storage**: Keys stored locally in encrypted config
2. **Payment Verification**: All API calls require SkillPay signature
3. **No Key Transmission**: Private keys never sent over network
4. **Dedicated Wallet**: Use separate wallet for bot trading
5. **Rate Limiting**: Built-in protection against abuse

### Best Practices
- Start with small amounts (0.01-0.05 SOL)
- Monitor bot activity regularly
- Keep private keys secure
- Use strong passwords for notifications
- Review trading history daily

## Risk Warnings

⚠️ **HIGH RISK ACTIVITY**
- Cryptocurrency trading involves substantial risk of loss
- New tokens are extremely volatile
- Bot cannot guarantee profits
- Past performance doesn't predict future results
- Only invest what you can afford to lose

⚠️ **Technical Risks**
- Smart contract vulnerabilities
- Rug pulls and scams
- Network congestion and failed transactions
- API downtime
- Slippage and MEV

## Performance Optimization

### For Maximum Opportunities
- Lower quality score threshold (50-60)
- Higher max positions (10-15)
- Faster monitoring interval

### For Safety
- Higher quality score threshold (70-80)
- Lower max positions (3-5)
- Stricter liquidity requirements

### For Quick Profits
- Lower take profit (30-50%)
- Tighter stop loss (20-30%)
- Enable trailing stop

### For Big Wins
- Higher take profit (100-200%)
- Wider stop loss (40-60%)
- More patience

## Technical Architecture

### Components
- **Monitors**: Track pump.fun and four.meme APIs
- **Quality Filter**: Evaluate token metrics
- **Trading Engine**: Execute Solana transactions
- **Strategy Manager**: Implement profit/loss logic
- **Position Manager**: Track open/closed positions
- **Notification Manager**: Multi-channel alerts

### Data Storage
- Configuration: `data/config.json`
- Open Positions: `data/positions.json`
- Trading History: `data/history.json`

### Scheduling
- Token monitoring: Every 30 seconds
- Position checking: Every 60 seconds
- Cleanup tasks: Hourly

## Integration Requirements

### APIs Needed
1. **pump.fun API**: Token discovery and details
2. **four.meme API**: Token discovery and details
3. **Jupiter Aggregator**: DEX swap execution
4. **Solana RPC**: Blockchain interaction
5. **Price Feeds**: Real-time token prices

### Current Status
- ✅ Core architecture implemented
- ✅ Strategy management complete
- ✅ Notification system ready
- ⚠️ API integrations are placeholders
- ⚠️ DEX swap needs Jupiter integration
- ⚠️ Price feeds need implementation

## Pricing
- **Model**: Pay-per-use
- **Price**: 0.001 USDT per API call
- **Provider**: SkillPay
- **Payment**: Automatic via SkillPay signature

## Support & Maintenance
- Monitor logs for errors
- Check trading history regularly
- Update API integrations as needed
- Keep dependencies updated
- Backup configuration and history

## Future Enhancements
- [ ] Advanced technical indicators
- [ ] Machine learning quality scoring
- [ ] Multi-chain support
- [ ] Portfolio rebalancing
- [ ] Social sentiment analysis
- [ ] Whale wallet tracking
- [ ] Custom strategy builder
- [ ] Backtesting framework

---

**Disclaimer**: This bot is provided as-is. Use at your own risk. The developers are not responsible for any financial losses.
