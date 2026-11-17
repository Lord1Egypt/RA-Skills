# BTC Price Monitor

## Description
Fetches current Bitcoin price from CoinGecko and sends it to Telegram. Can also trigger alerts when price drops below a threshold.

## When to use
- When user asks "what's the bitcoin price"
- When user wants to check current BTC rate
- When setting up price alerts

## Setup

### Required environment variables
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID (can get from @userinfobot)

### Optional environment variables
- `PRICE_THRESHOLD_USD`: Set alert threshold (default: 50000). If price drops below this, an alert is added.

## Usage

### Basic usage
```bash
python scripts/main.py

## Support

**USDT (TRC20)**: `TUqLWTyYJMHmp56eEoJdeaFG1PurEvxwkV`  
**USDT (BEP20)**: `0x5a03c0113fddce00fa7953b56541a16cab9a2800`  
**BTC**: `1E3pUfky8iKjQ7Ju5TvkMRPFkw6hzRMPc2`  
**BNB (BSC)**: `0x5a03c0113fddce00fa7953b56541a16cab9a2800`