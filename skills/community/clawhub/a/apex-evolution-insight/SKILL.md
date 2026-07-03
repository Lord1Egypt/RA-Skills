---
name: apex-evolution-insight
description: Weekly strategy evolution insights from APEX's self-improvement engine
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/apex-evolution-insight
    emoji: "🧬"
---
# apex-evolution-insight

> **Tier 3 — Strategic Edge**: This signal provides proprietary institutional-grade intelligence computed from APEX's live trading system. Pricing reflects the depth of analysis and the scarcity of the underlying edge.

## What It Does
Weekly strategy evolution insights from APEX's self-improvement engine. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To understand how APEX's strategy is evolving
- For weekly performance review
- When calibrating long-term strategy alignment

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/apex-evolution-insight
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/apex-evolution-insight",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "week": "2026-W25",
  "strategy_score": 0.77,
  "top_insight": "RANGING regime outperforming; momentum edge compressing"
}
```

## Pricing
**$15.00/call** — standard price

Early adopters automatically receive 30% off ($10.50/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [signal-intelligence](https://apexrunner.ai/signals/signal-intelligence)
- [regime-transition](https://apexrunner.ai/signals/regime-transition)
- [apex-evolution-insight-institutional](https://apexrunner.ai/signals/apex-evolution-insight-institutional)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
