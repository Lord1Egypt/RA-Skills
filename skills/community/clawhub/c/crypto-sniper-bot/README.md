# Crypto Sniper Bot

24/7 automated token sniper bot for pump.fun and four.meme platforms with intelligent take-profit/stop-loss strategies.

## ⚠️ IMPORTANT WARNINGS

- **HIGH RISK**: Cryptocurrency trading involves substantial risk of loss
- **PRIVATE KEYS**: Your wallet private keys are stored locally - keep them secure
- **NO GUARANTEES**: Past performance does not guarantee future results
- **USE AT YOUR OWN RISK**: The developers are not responsible for any financial losses

## Features

- 🤖 24/7 automated monitoring of pump.fun and four.meme
- 🎯 Quality token filtering based on multiple metrics
- 💰 Automated buying and selling with configurable strategies
- 📊 Take-profit and stop-loss management
- 🔔 Multi-channel notifications (Telegram, Discord, WhatsApp, Slack, Email)
- 📈 Real-time position tracking and P&L calculation
- 📜 Complete trading history

## Installation

```bash
npm install
```

## Configuration

1. Copy `.env.example` to `.env`
2. Configure your settings:

```env
# Wallet Configuration
WALLET_PRIVATE_KEY=your_solana_wallet_private_key

# Trading Strategy
BUY_AMOUNT=0.1
TAKE_PROFIT_PERCENT=50
STOP_LOSS_PERCENT=30
MAX_POSITIONS=10

# API Keys
BITQUERY_API_KEY=your_bitquery_api_key

# RPC Endpoints
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
BSC_RPC_URL=https://bsc-dataseed.binance.org

# Notification Channels
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
DISCORD_WEBHOOK_URL=your_discord_webhook
EMAIL_HOST=smtp.gmail.com
EMAIL_USER=your_email
EMAIL_PASS=your_password
EMAIL_TO=recipient_email

# SkillPay
SKILLPAY_API_KEY=sk_e390b52cb259fc4f4aa1489547a48375d72876acdee75de57101d9e0e833fcb7
```

### API Keys Required

1. **Bitquery API Key** (Recommended):
   - Sign up at https://bitquery.io/
   - Get API key for pump.fun and four.meme monitoring
   - Free tier available with rate limits

2. **Solana RPC** (Optional):
   - Default: Public Solana RPC
   - For better performance, use QuickNode, Alchemy, or Helius
   - Get free RPC endpoint at https://www.quicknode.com/

3. **BSC RPC** (Optional):
   - Default: Public Binance RPC
   - For better performance, use dedicated RPC provider

## Usage

### Start the bot
```bash
npm start
```

### API Endpoints

#### Configure Bot
```bash
POST /configure
{
  "walletPrivateKey": "your_private_key",
  "buyAmount": 0.1,
  "takeProfitPercent": 50,
  "stopLossPercent": 30,
  "maxPositions": 10
}
```

#### Start Bot
```bash
POST /start
```

#### Stop Bot
```bash
POST /stop
```

#### Get Status
```bash
GET /status
```

#### Get Trading History
```bash
GET /history
```

#### Configure Notifications
```bash
POST /notifications
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
    "to": "recipient_email"
  }
}
```

## How It Works

1. **Monitoring**: Continuously monitors pump.fun and four.meme for new token launches
   - Uses Bitquery GraphQL API for real-time data
   - Fallback to PumpPortal API for pump.fun
   - Scans every 30 seconds for new tokens

2. **Quality Filter**: Evaluates tokens based on liquidity, holder count, and other metrics

3. **Auto-Buy**: Automatically purchases quality tokens with configured amount
   - Uses Jupiter Aggregator for Solana swaps
   - Optimizes for best price and lowest slippage

4. **Position Management**: Tracks all open positions in real-time

5. **Auto-Sell**: Executes take-profit or stop-loss when thresholds are met
   - Uses Jupiter Aggregator for selling
   - Supports trailing stop-loss

6. **Notifications**: Sends alerts for all buy/sell actions

## Security Best Practices

- Never share your private keys
- Use a dedicated wallet for bot trading
- Start with small amounts to test
- Monitor bot activity regularly
- Keep your API keys secure

## License

MIT
