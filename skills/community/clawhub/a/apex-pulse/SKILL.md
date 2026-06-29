---
name: apex-pulse
description: APEX system heartbeat — confirms live trading is active and healthy
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/apex-pulse
    emoji: "❤️"
---
# apex-pulse

## What It Does
APEX system heartbeat — confirms live trading is active and healthy. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To verify APEX is live before relying on its signals
- Inside health-check workflows
- To confirm signal freshness before trading

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/apex-pulse
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/apex-pulse",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "status": "LIVE",
  "regime": "RANGING",
  "market": "OPEN",
  "fg": 42,
  "fg_label": "Fear",
  "apex_trading": true,
  "active_pairs": 11,
  "timestamp": "2026-06-23T14:00:00Z",
  "valid_for_seconds": 60
}
```

## Pricing
**$0.05/call** — standard price

Early adopters automatically receive 30% off ($0.03/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [market-tick](https://apexrunner.ai/signals/market-tick)
- [grid-health](https://apexrunner.ai/signals/grid-health)
- [portfolio-heat](https://apexrunner.ai/signals/portfolio-heat)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
