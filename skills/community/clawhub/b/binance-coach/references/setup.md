# BinanceCoach — Setup Guide

## Requirements

- Python 3.10+
- pip (or pip3)
- Git
- A Binance account (read-only API keys)
- An Anthropic account (for AI coaching features)

## Quick Install

```bash
# 1. Clone the project
git clone https://github.com/UnrealBNB/BinanceCoachAI.git ~/workspace/binance-coach
cd ~/workspace/binance-coach

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Configure
cp config.example.env .env
# Edit .env with your API keys (see below)

# 4. Test
python3 main.py --demo
```

Or use the skill setup script:
```bash
scripts/setup.sh
```

## API Keys

### Binance (Required for portfolio features)
1. Go to Binance → Account → API Management
2. Create a new API key
3. Enable **Read Only** permissions (no trading, no withdrawals)
4. Add to `.env`:
   ```
   BINANCE_API_KEY=your_key
   BINANCE_API_SECRET=your_secret
   ```

### Anthropic Claude (Required for AI coaching)
1. Go to https://console.anthropic.com/
2. Create an API key
3. Add to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

### Telegram Bot (Optional)
1. Message @BotFather on Telegram → `/newbot`
2. Copy the token to `.env`:
   ```
   TELEGRAM_BOT_TOKEN=your_token
   TELEGRAM_USER_ID=your_telegram_user_id
   ```
   Find your user ID at https://t.me/userinfobot

## Verify Setup

```bash
# Market data (no API key needed)
python3 main.py --demo

# Portfolio (requires Binance key)
cd ~/workspace/binance-coach && python3 main.py
coach> portfolio

# AI coaching (requires Anthropic key)
coach> coach

# Telegram bot
python3 main.py --telegram
```

## Project Structure

```
binance-coach/
├── main.py                    # Entry point (CLI + Telegram + demo)
├── .env                       # Your secrets (gitignored)
├── config.example.env         # Template
├── requirements.txt
├── modules/
│   ├── market.py              # Binance market data + RSI + MAs
│   ├── portfolio.py           # Portfolio health scoring
│   ├── dca.py                 # Smart DCA advisor
│   ├── behavior.py            # Behavioral bias detection
│   ├── alerts.py              # Price/RSI alert system
│   ├── education.py           # Educational lessons
│   ├── news.py                # News, listings, launchpool fetcher + watcher daemon
│   ├── ai_coach.py            # Claude AI coaching engine
│   ├── i18n.py                # Translation loader
│   ├── tg_utils.py            # Telegram HTML helpers
│   └── locales/
│       ├── en.py              # English strings + lessons
│       └── nl.py              # Dutch strings + lessons
├── bot/
│   └── telegram_bot.py        # Telegram bot (21 commands + auto news/alert polling)
├── data/                      # SQLite databases (gitignored)
│   ├── alerts.db              # Price/RSI alert state
│   ├── seen_news.db           # Dedup tracker for news watcher
│   └── watcher.log            # Background watcher log (watch-bg)
└── openclaw-skill/            # This OpenClaw skill
    └── binance-coach/
```
