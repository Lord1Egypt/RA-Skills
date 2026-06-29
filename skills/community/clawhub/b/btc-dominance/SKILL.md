---
name: btc-dominance
description: BTC dominance percentage with trend direction signal
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/btc-dominance
    emoji: "👑"
---
# btc-dominance

## What It Does
BTC dominance percentage with trend direction signal. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- When deciding BTC vs altcoin allocation
- To detect altcoin season onset
- As context for capital rotation signals

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/btc-dominance
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/btc-dominance",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "dominance_pct": 54.3,
  "trend": "rising",
  "altcoin_season": false
}
```

## Pricing
**$0.15/call** — standard price

Early adopters automatically receive 30% off ($0.10/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [altcoin-season](https://apexrunner.ai/signals/altcoin-season)
- [capital-rotation-signal](https://apexrunner.ai/signals/capital-rotation-signal)
- [regime](https://apexrunner.ai/signals/regime)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
