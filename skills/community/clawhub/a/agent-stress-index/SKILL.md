---
name: agent-stress-index
description: Composite stress index measuring systemic risk across all APEX modules
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/agent-stress-index
    emoji: "🔥"
---
# agent-stress-index

> **Tier 3 — Strategic Edge**: This signal provides proprietary institutional-grade intelligence computed from APEX's live trading system. Pricing reflects the depth of analysis and the scarcity of the underlying edge.

## What It Does
Composite stress index measuring systemic risk across all APEX modules. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To monitor systemic risk across APEX modules
- As a circuit-breaker signal
- When stress is rising and exposure should reduce

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/agent-stress-index
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/agent-stress-index",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "stress_score": 44,
  "stress_level": "MODERATE",
  "stress_trend": "RISING",
  "anomalies_detected": [
    {
      "pattern": "APEX-STRESS-002",
      "severity": "LOW",
      "signal": "Unusual query pattern detected"
    }
  ],
  "agents_monitored": 3,
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
- [crowded-trade-detector](https://apexrunner.ai/signals/crowded-trade-detector)
- [portfolio-heat](https://apexrunner.ai/signals/portfolio-heat)
- [cross-asset-contagion](https://apexrunner.ai/signals/cross-asset-contagion)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
