---
name: bd-stock-live
description: Bangladesh stock market data and analytics for DSE (Dhaka Stock Exchange) - prices, signals, EMA channels, Fibonacci levels
homepage: https://stock-ai.live
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: ["python3"]
      env: ["STOCKAI_API_KEY"]
    primaryEnv: STOCKAI_API_KEY
---

# BD Stock Live — Bangladesh Stock Market Data & Analytics

**Real-time Dhaka Stock Exchange (DSE) market data and trading analytics.**

---

## Setup

### Get API Key

1. Visit **https://stock-ai.live/register** to create a free account
2. Go to **https://stock-ai.live/api-keys**
3. Click "Create New API Key"
4. Copy your API key (starts with `sk_live_`)

### Configure Environment

**Option 1: Environment variable (recommended)**
```bash
export STOCKAI_API_KEY=sk_live_your_api_key_here
```

**Option 2: OpenClaw config**
Set `skills."bd-stock-live".env.STOCKAI_API_KEY` in `~/.openclaw/openclaw.json`

**Option 3: Local .env (for development)**
Create `skill/bd-stock-live/.env`:
```
STOCKAI_API_KEY=sk_live_your_api_key_here
```

**Optional:** Override API base URL (must be stock-ai.live domain):
```bash
export STOCKAI_API_BASE=https://stock-ai.live
```

---

## Quick Start

```bash
# Get stock price
python scripts/stock.py price ACI

# Search stocks
python scripts/stock.py search "BRAC Bank"

# Market overview
python scripts/stock.py market

# Recent news
python scripts/stock.py news
```

---

## Pricing Tiers

| Feature | Free | Pro (৳899/mo) | Enterprise (৳4,499/mo) |
|---------|------|---------------|------------------------|
| Stock prices | ✅ 100/day | ✅ 10,000/day | ✅ Unlimited |
| Stock search | ✅ | ✅ | ✅ |
| Market overview | ✅ | ✅ | ✅ |
| Recent news | ✅ | ✅ | ✅ |
| **Gainers/Losers** | ❌ | ✅ | ✅ |
| **Price history** | ❌ | ✅ | ✅ |
| **Trading signals** | ❌ | ❌ | ✅ |
| **EMA/Fibonacci** | ❌ | ❌ | ✅ |

---

## Free Tier Commands

### `price <symbol>`

Get current stock price and details.

```bash
python scripts/stock.py price ACI
```

### `search <query>`

Search stocks by name or symbol.

```bash
python scripts/stock.py search "BRAC Bank"
```

### `market`

Get market overview with indices (DSEX, DSES, DS30).

```bash
python scripts/stock.py market
```

### `news`

Get recent market news.

```bash
python scripts/stock.py news
```

---

## Pro Commands ($9/month)

### `gainers [--limit N]`

Get top gaining stocks.

```bash
python scripts/stock.py gainers --limit 5
```

### `losers [--limit N]`

Get top losing stocks.

```bash
python scripts/stock.py losers --limit 10
```

### `history <symbol> [--days N]`

Get historical price data.

```bash
python scripts/stock.py history ACI --days 30
```

---

## Enterprise Commands (৳4,499/month)

### `signal <symbol>`

Get AI-powered trading signal (BUY/SELL/HOLD).

```bash
python scripts/stock.py signal ACI
```

### `vegas <symbol>`

Vegas Tunnel multi-dimensional trend analysis.

```bash
python scripts/stock.py vegas ACI
```

### `ema <symbol>`

Get EMA channel status (Fibonacci-based pairs).

```bash
python scripts/stock.py ema ACI
```

### `fib <symbol>`

Get Fibonacci retracement levels.

```bash
python scripts/stock.py fib ACI
```

### `sectors`

Get sector performance analysis.

```bash
python scripts/stock.py sectors
```

---

## Command-Line Options

| Option | Description |
|--------|-------------|
| `--api-key KEY` | API key (or set `STOCKAI_API_KEY` env) |
| `--limit N` | Limit number of results |
| `--days N` | Days of history (default: 30) |

---

## Free Tier Limits

- **100 requests/day**
- **10 requests/minute**
- Basic endpoints only: price, search, market, news

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `STOCKAI_API_KEY` | Yes | API key from stock-ai.live |
| `STOCKAI_API_BASE` | No | Override API base URL (must be stock-ai.live domain) |

---

## Support

- Documentation: https://stock-ai.live/docs
- API Keys: https://stock-ai.live/api-keys
- Pricing: https://stock-ai.live/pricing
- Contact: support@stock-ai.live

---

## License

MIT License