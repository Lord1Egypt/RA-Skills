---
name: capital-rotation-signal
description: Detects capital rotation between BTC, ETH, alts, and stables
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/capital-rotation-signal
    emoji: "🔁"
---
# capital-rotation-signal

> **Tier 3 — Strategic Edge**: This signal provides proprietary institutional-grade intelligence computed from APEX's live trading system. Pricing reflects the depth of analysis and the scarcity of the underlying edge.

## What It Does
Detects capital rotation between BTC, ETH, alts, and stables. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To time rotation between BTC, ETH, and alts
- When sector allocation matters
- To front-run capital flow shifts

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/capital-rotation-signal
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/capital-rotation-signal",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "rotation_state": "ALT_SEASON_EARLY",
  "conviction": "MEDIUM",
  "from_asset": "BTC",
  "to_assets": ["ETH", "SOL"],
  "recommended_allocation": {
    "BTC": "REDUCE",
    "ETH": "ACCUMULATE"
  },
  "rotation_phase": "EARLY",
  "timestamp": "2026-06-23T14:00:00Z"
}
```

## Pricing
**$12.00/call** — standard price

Early adopters automatically receive 30% off ($8.40/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [btc-dominance](https://apexrunner.ai/signals/btc-dominance)
- [altcoin-season](https://apexrunner.ai/signals/altcoin-season)
- [regime-transition](https://apexrunner.ai/signals/regime-transition)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
