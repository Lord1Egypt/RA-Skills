# ₿ CryptoWatch

**Real-Time Cryptocurrency Price Monitor** - Track BTC, ETH, SOL and 25+ coins instantly!

[![Version](https://img.shields.io/github/v/release/gztanht/cryptowatch)](https://github.com/gztanht/cryptowatch/releases)
[![License](https://img.shields.io/github/license/gztanht/cryptowatch)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-cryptowatch-blue)](https://clawhub.com/skills/cryptowatch)

> **Never Miss a Pump** - Real-time price tracking with instant alerts! ₿

---

## 🌟 Features

- **Live Price Tracking** - 25+ cryptocurrencies via CoinGecko API
- **Price Alerts** - Get notified when price hits your target
- **24h Change** - Track gains/losses with color indicators
- **Market Cap Ranking** - Top 20/50/100 by market cap
- **Multi-Currency** - USD, CNY, EUR support
- **Volume Data** - 24h trading volume
- **Lightning Fast** - < 30 second data delay

---

## 🚀 Quick Start

```bash
# Install
npx @gztanht/cryptowatch

# Check BTC, ETH, SOL prices
node scripts/watch.mjs btc,eth,sol

# View top 20 by market cap
node scripts/watch.mjs --top 20

# Set price alert
node scripts/alert.mjs btc --above 100000
node scripts/alert.mjs eth --below 3000

# List all alerts
node scripts/alert.mjs --list
```

---

## 📊 Example Output

```bash
$ node scripts/watch.mjs btc,eth,sol

₿ CryptoWatch - Live Prices

Coin    Price        24h Change    Market Cap    24h Volume
────────────────────────────────────────────────────────────────
BTC     $71,177.00   🔴 -2.44%     $1.42T        $64.10B
ETH     $2,077.72    🔴 -3.08%     $250.37B      $26.37B
SOL     $88.51       🔴 -3.45%     $50.39B       $5.51B

💡 Tip: node scripts/watch.mjs --top 20 for market ranking
```

---

## 💰 Pricing - Free First!

| Plan | Price | Limit |
|------|-------|-------|
| **Free** | $0 | **5 queries/day** |
| **Sponsor Unlock** | 0.5 USDT or 0.5 USDC | Unlimited |

### Sponsorship Addresses

- **USDT (ERC20)**: `0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`
- **USDC (ERC20)**: `0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44`

---

## 📖 All Commands

| Command | Description |
|---------|-------------|
| `watch.mjs` | Live price monitoring |
| `watch.mjs btc` | Single coin check |
| `watch.mjs --top 20` | Market cap ranking |
| `watch.mjs --vs cny` | CNY pricing |
| `top.mjs` ✨ | 24h gainers leaderboard |
| `top.mjs --losers` | 24h losers leaderboard |
| `alert.mjs btc --above 100000` | Set price alert |
| `alert.mjs --list` | List all alerts |
| `alert.mjs --remove 1` | Remove alert #1 |

---

## 🪙 Supported Coins (25+)

**Major**: BTC, ETH, SOL, BNB, XRP, DOGE, ADA, AVAX

**DeFi**: LINK, DOT, MATIC, LTC, UNI, ATOM

**L2**: ARB, OP

**Emerging**: NEAR, ALGO, FIL, ICP, VET, HBAR, APT, SUI

---

## 📈 API Reference

**Data Source**: CoinGecko API (Free, No Key Required)

- **Endpoint**: `https://api.coingecko.com/api/v3`
- **Rate Limit**: 10-50 calls/min (free tier)
- **Data Delay**: < 30 seconds

---

## 🔧 Configuration

Edit `config/coins.json` to customize your watchlist:

```json
{
  "watchlist": [
    {"id": "bitcoin", "symbol": "BTC", "name": "Bitcoin"},
    {"id": "ethereum", "symbol": "ETH", "name": "Ethereum"}
  ]
}
```

---

## ⚠️ Disclaimer

- Cryptocurrency prices are highly volatile
- This tool provides information only, not financial advice
- Always do your own research before investing
- Past performance does not guarantee future results

---

## 📞 Support

- **ClawHub**: https://clawhub.com/skills/cryptowatch
- **Email**: support@cryptowatch.shark
- **Telegram**: @CryptoWatchBot

---

## 📄 License

MIT © 2026 gztanht

---

**Made with ₿ by [@gztanht](https://github.com/gztanht)**

*Never Miss a Pump!*
