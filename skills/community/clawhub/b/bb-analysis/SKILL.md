---
name: bb-analysis
description: Bollinger Band analysis with squeeze detection and breakout probability
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/bb-analysis
    emoji: "📉"
---
# bb-analysis

## What It Does
Bollinger Band analysis with squeeze detection and breakout probability. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To detect Bollinger Band squeezes
- Before breakout or mean-reversion trades
- To gauge price extremity

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/bb-analysis
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/bb-analysis",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "squeeze": false,
  "position": "mid-band",
  "breakout_probability": 0.38
}
```

## Pricing
**$1.00/call** — standard price

Early adopters automatically receive 30% off ($0.70/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [mean-reversion-scan](https://apexrunner.ai/signals/mean-reversion-scan)
- [volume-analysis](https://apexrunner.ai/signals/volume-analysis)
- [momentum-status](https://apexrunner.ai/signals/momentum-status)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
