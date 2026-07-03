---
name: apex-alpha-score
description: APEX proprietary alpha score for current market opportunity quality
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/apex-alpha-score
    emoji: "⚡"
---
# apex-alpha-score

> **Tier 3 — Strategic Edge**: This signal provides proprietary institutional-grade intelligence computed from APEX's live trading system. Pricing reflects the depth of analysis and the scarcity of the underlying edge.

## What It Does
APEX proprietary alpha score for current market opportunity quality. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To rank overall opportunity quality
- Before deploying significant capital
- As the primary entry gate for high-value trades

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/apex-alpha-score
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/apex-alpha-score",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "alpha_score": 0.71,
  "percentile": 82,
  "signal_count": 9,
  "confidence": "high"
}
```

## Pricing
**$5.00/call** — standard price

Early adopters automatically receive 30% off ($3.50/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [combined-alpha](https://apexrunner.ai/signals/combined-alpha)
- [agent-conviction-score](https://apexrunner.ai/signals/agent-conviction-score)
- [apex-alpha-score-institutional](https://apexrunner.ai/signals/apex-alpha-score-institutional)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
