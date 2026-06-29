---
name: funding-rate-hl
description: Current Hyperliquid perpetual funding rates across tracked coins
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/funding-rate-hl
    emoji: "💰"
---
# funding-rate-hl

## What It Does
Current Hyperliquid perpetual funding rates across tracked coins. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- Before opening or holding Hyperliquid perp positions
- To identify funding arb opportunities
- To avoid paying excessive funding

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/funding-rate-hl
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/funding-rate-hl",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "BTC": 0.0003,
  "ETH": 0.00025,
  "SOL": 0.00041,
  "AVAX": 0.00018,
  "timestamp": "2026-06-23T14:00:00Z"
}
```

## Pricing
**$0.02/call** — standard price

Early adopters automatically receive 30% off ($0.01/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [funding-rate](https://apexrunner.ai/signals/funding-rate)
- [arb-spread](https://apexrunner.ai/signals/arb-spread)
- [oi-divergence](https://apexrunner.ai/signals/oi-divergence)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
