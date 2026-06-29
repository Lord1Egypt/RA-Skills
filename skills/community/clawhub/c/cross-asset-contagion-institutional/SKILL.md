---
name: cross-asset-contagion-institutional
description: Full cross-asset contagion analysis with correlation matrices
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/cross-asset-contagion-institutional
    emoji: "🌐"
---
# cross-asset-contagion-institutional

> **Tier 3 — Strategic Edge**: This signal provides proprietary institutional-grade intelligence computed from APEX's live trading system. Pricing reflects the depth of analysis and the scarcity of the underlying edge.

## What It Does
Full cross-asset contagion analysis with correlation matrices. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- For full cross-asset correlation analysis
- In institutional risk committee reporting
- When systemic risk modelling is required

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/cross-asset-contagion-institutional
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/cross-asset-contagion-institutional",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "contagion_score": 0.28,
  "correlation_matrix": {"BTC_SPX": 0.42, "BTC_DXY": -0.31},
  "tail_risk": "low"
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
- [cross-asset-contagion](https://apexrunner.ai/signals/cross-asset-contagion)
- [regime-confluence-institutional](https://apexrunner.ai/signals/regime-confluence-institutional)
- [apex-alpha-score-institutional](https://apexrunner.ai/signals/apex-alpha-score-institutional)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
