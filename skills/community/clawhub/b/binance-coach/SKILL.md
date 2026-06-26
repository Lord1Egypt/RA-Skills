---
name: binance-coach
description: 'AI-powered crypto trading behavior coach for Binance users. Analyzes live portfolio health, detects emotional trading patterns (FOMO, panic selling, overtrading), provides smart DCA recommendations based on RSI + Fear & Greed index, and delivers personalized AI coaching via Claude. Use when a user asks to: analyze their crypto portfolio, get DCA advice, check market conditions (RSI, Fear & Greed, SMA200), review trading behavior/FOMO/panic sells, get AI coaching on their holdings, set price/RSI alerts, learn about crypto concepts (RSI, DCA, SMA200), start a Telegram trading coach bot, ask anything about their Binance portfolio, get latest Binance news or announcements, check new coin listings, check launchpools or HODLer airdrops, or start/stop a real-time announcement watcher.'
license: MIT
homepage: https://github.com/UnrealBNB/BinanceCoachAI
metadata:
  openclaw:
    emoji: '📊'
    primaryEnv: BINANCE_API_KEY
    requires:
      env:
        - BINANCE_API_KEY
        - BINANCE_API_SECRET
      bins:
        - python3
        - pip3
    install:
      - id: python3
        kind: brew
        formula: python3
        bins:
          - python3
          - pip3
---

# 📊 BinanceCoach

> Your AI-powered crypto trading behavior coach — connected to your Binance account.

BinanceCoach analyzes your live Binance portfolio, spots emotional trading patterns like FOMO and panic selling, and gives you smart DCA buy signals based on RSI and the Fear & Greed index — all via your OpenClaw assistant.

---

## ✨ What it does

| Feature | Description |
|---|---|
| 💼 Portfolio Health | Score 0–100 with grade, concentration warnings, stablecoin check |
| 📐 Smart DCA | Weekly buy amounts per coin, adjusted by RSI × Fear & Greed (25 combinations) |
| 🧠 Behavior Analysis | FOMO score, overtrading index, panic sell detector, streak tracker |
| 📈 Market Context | Live price, RSI, SMA50/200, trend direction per coin |
| 😱 Fear & Greed | Real-time index with buy/hold advice |
| 🔔 Price Alerts | Set price or RSI alerts, check when triggered |
| 📚 Education | 7 lessons: RSI, DCA, SMA200, Fear & Greed, concentration risk, panic selling |
| 📅 Projections | 12-month DCA accumulation projection per coin |
| 📰 News & Listings | Live Binance announcements, new coin listings, launchpools & HODLer airdrops |
| 👁 Real-time Watcher | Background daemon that polls Binance every 60s and Telegram-notifies instantly |

---

## 🚀 Quick Start

**Only one credential required when using with OpenClaw:**

```
Binance API key + secret (read-only)
```

> OpenClaw already has Claude built in and handles messaging — no Anthropic key or Telegram bot needed.

Just say: **"analyze my portfolio"** or **"set up BinanceCoach"** — your assistant handles the rest.

## 🔗 Optional: Hook into OpenClaw as default crypto handler

During setup, you'll be asked if you want BinanceCoach registered as your default handler for all crypto questions. If you say yes, a preference block is added to your OpenClaw `USER.md`:

- Every session from that point on, your assistant uses BinanceCoach automatically for any crypto question
- Covers: DCA, portfolio, market data, news, launchpools, listings, behavior analysis, alerts, projections, and more
- You can remove it anytime by editing `USER.md`

**This is opt-in — setup will always ask before modifying any config files.**

---

## 🗣️ Example questions

- *"Analyze my portfolio"*
- *"What's the Fear & Greed index?"*
- *"Give me DCA advice for DOGE and ADA"*
- *"Check my trading behavior"*
- *"Set an alert if BTC drops below $60,000"*
- *"Show me the market context for ETH"*
- *"What's a 12-month DCA projection for BTC?"*
- *"Explain dollar cost averaging"*
- *"What are the latest Binance news / announcements?"*
- *"Any new coin listings on Binance?"*
- *"Are there any active launchpools or HODLer airdrops?"*
- *"Watch for new Binance announcements and notify me instantly"*
- *"Start the news watcher"* / *"Stop the watcher"*

---

## 🔐 Security

- **Read-only Binance API** — no trading, no withdrawals possible
- Secrets stored **locally only** in `~/workspace/binance-coach/.env`
- `.env` is gitignored and never committed
- Source code is fully auditable: [github.com/UnrealBNB/BinanceCoachAI](https://github.com/UnrealBNB/BinanceCoachAI)

See [SECURITY.md](SECURITY.md) for full audit guide.

---

## ⚙️ Optional: Standalone Telegram Bot

Want a dedicated Telegram bot (separate from OpenClaw)?

1. Create a bot via [@BotFather](https://t.me/BotFather) — send `/newbot`
2. Get your Telegram user ID from [@userinfobot](https://t.me/userinfobot)
3. Tell your OpenClaw: *"Set up Telegram for BinanceCoach"*

Your assistant will ask for the token and user ID, then start the bot.

The Telegram bot includes **automatic news polling every 2 minutes** — it notifies you instantly when new listings, launchpools, or announcements drop, without you having to ask.

## 👁 Real-time Announcement Watcher

Want instant Telegram notifications even outside the bot? Start the background watcher:

> *"Start watching for Binance announcements"*

This runs a daemon that polls Binance every 60 seconds and pushes a Telegram message the moment something new appears — new listings, launchpools, HODLer airdrops, or news. It also flags announcements that affect coins you actually hold.

---

## 🌍 Languages

Supports **English** and **Dutch (Nederlands)**. Switch anytime:

> *"Switch BinanceCoach to Dutch"*

---

*Built for the Binance OpenClaw AI Assistant Campaign 2026 · [View on GitHub](https://github.com/UnrealBNB/BinanceCoachAI)*

---

<!-- AGENT INSTRUCTIONS — read references/agent-guide.md for full dispatch table -->
