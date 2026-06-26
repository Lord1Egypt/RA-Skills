---
name: cryptowatch
description: ₿ CryptoWatch - 实时监控加密货币价格，价格突破自动预警
version: 0.1.0
author: gztanht
license: MIT
tags: [crypto, price, bitcoin, ethereum, monitoring, alert]
pricing:
  free_tier: 5 queries/day
  sponsorship: 0.5 USDT or 0.5 USDC for unlimited
  note: "Feel free to sponsor more if you find it useful!"
wallet:
  usdt_erc20: "0x33f943e71c7b7c4e88802a68e62cca91dab65ad9"
  usdc_erc20: "0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44"
metadata:
  clawdbot:
    emoji: ₿
    requires:
      bins: [npm, node]
---

# ₿ CryptoWatch - 加密货币监控

**Never Miss a Pump** - 实时追踪币价，猎杀每个波动！

## Overview

CryptoWatch 实时监控主流加密货币价格（BTC、ETH、SOL 等），支持价格预警、涨跌幅追踪、市值排行等功能。数据来自 CoinGecko API（免费、无需 API Key）。

## Features

- 📊 **实时价格** - 秒级更新，支持 100+ 加密货币
- 🚨 **价格预警** - 突破设定价位自动提醒
- 📈 **涨跌幅** - 24h/7d/30d 涨跌追踪
- 💰 **市值排行** - 按市值/音量排序
- 🔔 **多币种** - BTC、ETH、SOL、BNB、XRP 等主流币
- 🌐 **多法币** - USD、CNY、EUR、JPY 支持

## Installation

```bash
npx @gztanht/cryptowatch
```

## Usage

### 查看实时价格

```bash
# 查询单个币种
node scripts/watch.mjs btc

# 查询多个币种
node scripts/watch.mjs btc,eth,sol

# 查看所有主流币
node scripts/watch.mjs --top 20
```

### 设置价格预警

```bash
# BTC 突破 $100,000 提醒
node scripts/alert.mjs btc --above 100000

# ETH 跌破 $3,000 提醒
node scripts/alert.mjs eth --below 3000

# 查看已设置的预警
node scripts/alert.mjs --list
```

### 查看涨跌幅排行

```bash
# 24 小时涨幅榜
node scripts/rank.mjs --period 24h

# 7 日跌幅榜
node scripts/rank.mjs --period 7d --order asc
```

## Configuration

编辑 `config/coins.json` 添加自定义币种：

```json
{
  "watchlist": [
    {"id": "bitcoin", "symbol": "BTC", "name": "Bitcoin"},
    {"id": "ethereum", "symbol": "ETH", "name": "Ethereum"},
    {"id": "solana", "symbol": "SOL", "name": "Solana"}
  ]
}
```

## API Reference

- **CoinGecko API** - https://www.coingecko.com/en/api
- 免费 tier：10-50 calls/min，无需 API Key
- 数据延迟：< 30 秒

## Support

- 📧 Email: support@cryptowatch.shark
- 💬 Telegram: @CryptoWatchBot
- 🦈 赞助：USDT (ERC20): `0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`

## License

MIT © 2026 gztanht
