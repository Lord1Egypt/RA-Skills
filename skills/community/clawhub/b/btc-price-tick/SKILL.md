---
name: btc-price-tick
description: Real-time BTC price tick from live exchange feeds
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/btc-price-tick
    emoji: "💹"
---
# btc-price-tick

## What It Does
Real-time BTC price tick from live exchange feeds. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- When you need a low-latency BTC price reference
- Inside high-frequency polling loops
- As a baseline for spread or momentum calculations

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/btc-price-tick
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/btc-price-tick",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "b": 67482.50,
  "e": 3541.20,
  "s": 152.30,
  "a": 24.10,
  "t": 1750000000
}
```

## Pricing
**$0.01/call** — standard price

Early adopters automatically receive 30% off ($0.01/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [market-tick](https://apexrunner.ai/signals/market-tick)
- [apex-pulse](https://apexrunner.ai/signals/apex-pulse)
- [btc-dominance](https://apexrunner.ai/signals/btc-dominance)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
