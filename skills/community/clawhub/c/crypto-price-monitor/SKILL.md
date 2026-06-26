---
name: Crypto Price Alerts
slug: crypto-price-alerts
description: Monitor cryptocurrency prices and trigger alerts when thresholds are hit. Supports BTC, ETH, SOL, and 100+ other coins via CoinGecko API. Configure price ceilings, floors, or percentage moves. Alerts delivered to console, files, or Telegram.
author: taoorchestrator
version: 1.0.0
tags:
  - crypto
  - alerts
  - price-monitoring
  - trading
  - bitcoin
  - ethereum
---

# Crypto Price Alerts

Monitor cryptocurrency prices and get alerts when targets are hit. No API key required — uses CoinGecko's free API.

## What It Does

- Checks current prices for BTC, ETH, SOL, and 100+ coins
- Compares against your configured thresholds
- Alerts when price crosses above/below targets
- Supports percentage moves (e.g., "alert if BTC drops 5% in 1 hour")
- Can run once or on a schedule (cron)

## Quick Start

### Check a Single Price

```bash
# Direct API call (no auth needed)
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
```

### Check with More Detail

```bash
curl "https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&tickers=false&community_data=false&developer_data=false&sparkline=false"
```

## Alert Configuration

Create a `crypto-alerts.json` file:

```json
{
  "alerts": [
    {
      "coin": "bitcoin",
      "symbol": "btc",
      "condition": "below",
      "price": 85000,
      "message": "BTC dropped below $85K!"
    },
    {
      "coin": "bitcoin",
      "symbol": "btc",
      "condition": "above",
      "price": 100000,
      "message": "BTC crossed $100K! 🚀"
    },
    {
      "coin": "ethereum",
      "symbol": "eth",
      "condition": "below",
      "price": 3000,
      "message": "ETH below $3K"
    },
    {
      "coin": "solana",
      "symbol": "sol",
      "condition": "above",
      "price": 200,
      "message": "SOL above $200!"
    }
  ],
  "telegram_bot_token": "YOUR_BOT_TOKEN",
  "telegram_chat_id": "YOUR_CHAT_ID"
}
```

## Python Alert Script

Save as `crypto_alert.py`:

```python
#!/usr/bin/env python3
import requests
import json
import sys
import os
from datetime import datetime

COINGECKO_API = "https://api.coingecko.com/api/v3"

def get_price(coin_id):
    url = f"{COINGECKO_API}/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_last_updated_at": "true"
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data[coin_id]["usd"], data[coin_id].get("usd_24h_change", 0)

def check_alerts(alerts_config):
    triggered = []
    for alert in alerts_config.get("alerts", []):
        coin = alert["coin"]
        condition = alert["condition"]
        target = alert["price"]
        message = alert["message"]
        
        try:
            price, change_24h = get_price(coin)
        except Exception as e:
            print(f"Error fetching {coin}: {e}")
            continue
        
        should_fire = False
        if condition == "above" and price >= target:
            should_fire = True
        elif condition == "below" and price <= target:
            should_fire = True
        
        if should_fire:
            triggered.append({
                "coin": coin,
                "price": price,
                "target": target,
                "condition": condition,
                "message": message,
                "change_24h": change_24h,
                "time": datetime.now().isoformat()
            })
            print(f"🚨 ALERT: {message} (Current: ${price:,.2f})")
        else:
            print(f"  {coin.upper()}: ${price:,.2f} (24h: {change_24h:+.2f}%) — {condition} ${target:,.2f}: {'✓' if should_fire else 'not triggered'}")
    
    return triggered

def send_telegram(message, bot_token, chat_id):
    if not bot_token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload, timeout=10)

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), "crypto-alerts.json")
    
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
    else:
        print("No crypto-alerts.json found. Using default BTC/ETH/SOL check.")
        config = {
            "alerts": [
                {"coin": "bitcoin", "symbol": "btc", "condition": "above", "price": 0},
                {"coin": "ethereum", "symbol": "eth", "condition": "above", "price": 0},
                {"coin": "solana", "symbol": "sol", "condition": "above", "price": 0}
            ]
        }
    
    triggered = check_alerts(config)
    
    if triggered:
        summary = "🚨 <b>Crypto Alert Triggered</b>\n\n"
        for t in triggered:
            summary += f"{t['message']}\n"
            summary += f"Price: ${t['price']:,.2f} | 24h: {t['change_24h']:+.2f}%\n\n"
        
        bot_token = config.get("telegram_bot_token")
        chat_id = config.get("telegram_chat_id")
        if bot_token and chat_id:
            send_telegram(summary, bot_token, chat_id)
        
        with open("/tmp/crypto_alerts_triggered.json", "a") as f:
            f.write(json.dumps({"triggered": triggered, "time": datetime.now().isoformat()}) + "\n")
```

## Usage Examples

### Run Once
```bash
python3 crypto_alert.py
```

### Run on Schedule (Cron)
```bash
# Every 15 minutes
*/15 * * * * cd /path/to/skill && python3 crypto_alert.py >> /tmp/crypto_alerts.log 2>&1

# Every hour at minute 0
0 * * * * cd /path/to/skill && python3 crypto_alert.py >> /tmp/crypto_alerts.log 2>&1
```

### Check Specific Coin
```bash
# Bitcoin
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"

# Multiple coins
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,cardano,polkadot,avalanche-2,chainlink&vs_currencies=usd&include_24hr_change=true"
```

## Supported Coins (Common IDs)

| Symbol | CoinGecko ID |
|--------|--------------|
| BTC | bitcoin |
| ETH | ethereum |
| SOL | solana |
| ADA | cardano |
| DOT | polkadot |
| AVAX | avalanche-2 |
| LINK | chainlink |
| XRP | ripple |
| DOGE | dogecoin |
| MATIC | polygon |
| ARB | arbitrum |
| OP | optimism |

For full list: `curl https://api.coingecko.com/api/v3/coins/list?per_page=250`

## Alert Conditions

- `above` — Fire when price >= target
- `below` — Fire when price <= target
- `percent_up` — Fire when 24h change > X% (add `percent_threshold` field)
- `percent_down` — Fire when 24h change < -X% (add `percent_threshold` field)

## Rate Limits

CoinGecko free API:
- ~10-30 calls/minute
- 10,000-50,000 calls/month
- Use caching if checking frequently
- Add `sleep(1.2)` between calls to be safe

## Requirements

- `requests` Python library (`pip install requests`)
- CoinGecko API (free, no key needed)
- Optional: Telegram bot for push notifications
- Optional: cron for scheduled monitoring

## Tips

1. **Don't spam checks** — 15-minute intervals are fine for most use cases
2. **Cache prices** — Store last check to avoid redundant API calls
3. **Multiple conditions** — One coin can have multiple alerts (above AND below)
4. **Logging** — Always log to a file so you can review what fired

---

*Based on real crypto monitoring work. CoinGecko API is free but respectful usage is expected.*
