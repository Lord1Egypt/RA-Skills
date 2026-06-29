---
name: arb-spread
description: Current arbitrage spread between Kraken and Hyperliquid
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/arb-spread
    emoji: "💱"
---
# arb-spread

## What It Does
Current arbitrage spread between Kraken and Hyperliquid. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To detect Kraken vs Hyperliquid spread opportunities
- Before cross-exchange arb execution
- To size arb legs appropriately

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/arb-spread
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/arb-spread",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "spread_pct": 0.42,
  "threshold_pct": 0.35,
  "arb_viable": true
}
```

## Pricing
**$0.35/call** — standard price

Early adopters automatically receive 30% off ($0.24/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [cross-exchange-spread](https://apexrunner.ai/signals/cross-exchange-spread)
- [funding-rate](https://apexrunner.ai/signals/funding-rate)
- [optimal-order-routing](https://apexrunner.ai/signals/optimal-order-routing)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
