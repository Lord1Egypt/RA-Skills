---
name: Bitget PoolX Monitor
description: Monitor Bitget PoolX for new staking projects using r.jina.ai to bypass Cloudflare. Detect ETH, BTC, SOL and other pool launches.
version: "1.1.0"
author: Liuge
tags:
  - bitget
  - poolx
  - monitor
  - crypto
  - staking
  - jina
---

# Bitget PoolX Monitor

Monitor Bitget PoolX for new staking project launches.

## Features

- Uses r.jina.ai to bypass Cloudflare protection
- Fast and reliable (no Playwright needed)
- Detects new staking pools (ETH, BTC, SOL, etc.)
- Automatic notification support

## Usage

### Command Line
```bash
curl -s "https://r.jina.ai/https://www.bitget.com/events/poolx"
```

### Python
```python
import requests

def check_poolx():
    url = "https://r.jina.ai/https://www.bitget.com/events/poolx"
    content = requests.get(url).text
    
    if "Ongoing" in content:
        # Check for new pools
        return "Has active pools"
    return "No pools"
```

## Output Example

```
Ongoing (2)
- BTC Pool: 2,473 BTC, APR 2.74%
- ETH Pool: 80,664 ETH, APR 7.33%
```

## Monetization

This skill includes SkillPay integration:
- Charge users per API call (0.001 USDT)
- Check balance before execution
- Payment link for deposits

## Files

- bitget-monitor.py - Main script using r.jina.ai
- billing.py - SkillPay billing integration
