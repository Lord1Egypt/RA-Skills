---
name: funding-rate
description: Funding rate analysis across perps with arb opportunity scoring
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/funding-rate
    emoji: "💸"
---
# funding-rate

## What It Does
Funding rate analysis across perps with arb opportunity scoring. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- Before opening perp positions
- To identify funding arb opportunities
- To monitor ongoing funding costs

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/funding-rate
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/funding-rate",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "avg_rate_8h": 0.00031,
  "arb_score": 0.54,
  "recommended_action": "hold"
}
```

## Pricing
**$1.00/call** — standard price

Early adopters automatically receive 30% off ($0.70/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [funding-rate-hl](https://apexrunner.ai/signals/funding-rate-hl)
- [arb-spread](https://apexrunner.ai/signals/arb-spread)
- [oi-divergence](https://apexrunner.ai/signals/oi-divergence)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
