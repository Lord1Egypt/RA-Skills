---
name: apex-evolution-insight-institutional
description: Full institutional evolution report with strategy scoring and outlook
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/apex-evolution-insight-institutional
    emoji: "💼"
---
# apex-evolution-insight-institutional

> **Tier 3 — Strategic Edge**: This signal provides proprietary institutional-grade intelligence computed from APEX's live trading system. Pricing reflects the depth of analysis and the scarcity of the underlying edge.

## What It Does
Full institutional evolution report with strategy scoring and outlook. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- For deep strategic alignment review
- When advising on long-horizon allocation
- In institutional performance reporting

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/apex-evolution-insight-institutional
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/apex-evolution-insight-institutional",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "report_week": "2026-W25",
  "strategy_scores": {"grid": 0.84, "momentum": 0.71, "dca": 0.62},
  "outlook": "constructive"
}
```

## Pricing
**$30.00/call** — standard price

Early adopters automatically receive 30% off ($21.00/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [apex-evolution-insight](https://apexrunner.ai/signals/apex-evolution-insight)
- [apex-alpha-score-institutional](https://apexrunner.ai/signals/apex-alpha-score-institutional)
- [regime-confluence-institutional](https://apexrunner.ai/signals/regime-confluence-institutional)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
