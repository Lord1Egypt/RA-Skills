---
name: execution-window-optimizer
description: Identifies optimal execution windows based on volatility and liquidity
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/execution-window-optimizer
    emoji: "⏱️"
---
# execution-window-optimizer

## What It Does
Identifies optimal execution windows based on volatility and liquidity. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To time order placement for lowest impact
- During high-volatility periods
- When latency-sensitive execution is required

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/execution-window-optimizer
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/execution-window-optimizer",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "current_window_rating": "GOOD",
  "execute_now_recommendation": true,
  "best_windows": [
    {"utc_hours": "02:00-04:00", "avg_quality_score": 92}
  ],
  "timestamp": "2026-06-23T14:00:00Z"
}
```

## Pricing
**$0.20/call** — standard price

Early adopters automatically receive 30% off ($0.14/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [slippage-forecast](https://apexrunner.ai/signals/slippage-forecast)
- [optimal-order-routing](https://apexrunner.ai/signals/optimal-order-routing)
- [live-atr-sizing](https://apexrunner.ai/signals/live-atr-sizing)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
