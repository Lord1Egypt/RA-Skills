---
name: apex-alpha-score-institutional
description: Institutional alpha score with full factor decomposition
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/apex-alpha-score-institutional
    emoji: "🏆"
---
# apex-alpha-score-institutional

> **Tier 3 — Strategic Edge**: This signal provides proprietary institutional-grade intelligence computed from APEX's live trading system. Pricing reflects the depth of analysis and the scarcity of the underlying edge.

## What It Does
Institutional alpha score with full factor decomposition. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- For institutional alpha factor attribution
- When building factor models
- Before deploying large allocations

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/apex-alpha-score-institutional
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/apex-alpha-score-institutional",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "alpha_score": 0.71,
  "institutional": {
    "cex_grid_win_rate": 1.0,
    "cex_completed_cycles": 97,
    "hl_win_rate": 1.0,
    "hl_completed_fills": 2380,
    "evolution_runs": 10,
    "confidence_interval": {
      "low": 0.65,
      "high": 0.77,
      "confidence": 0.85
    }
  },
  "timestamp": "2026-06-23T14:00:00Z"
}
```

## Pricing
**$50.00/call** — standard price

Early adopters automatically receive 30% off ($35.00/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [apex-alpha-score](https://apexrunner.ai/signals/apex-alpha-score)
- [regime-confluence-institutional](https://apexrunner.ai/signals/regime-confluence-institutional)
- [apex-evolution-insight-institutional](https://apexrunner.ai/signals/apex-evolution-insight-institutional)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
