---
name: ai-narrative
description: AI-generated market narrative based on current regime and data
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/ai-narrative
    emoji: "🗣️"
---
# ai-narrative

## What It Does
AI-generated market narrative based on current regime and data. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To understand the current macro story
- When crafting agent reasoning summaries
- As context before executing complex strategies

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/ai-narrative
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/ai-narrative",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "narrative": "Market consolidating after rally. Whale accumulation detected. Regime: RANGING.",
  "bias": "cautiously bullish",
  "confidence": 0.71
}
```

## Pricing
**$0.25/call** — standard price

Early adopters automatically receive 30% off ($0.17/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [narrative-intelligence](https://apexrunner.ai/signals/narrative-intelligence)
- [whale-sentiment](https://apexrunner.ai/signals/whale-sentiment)
- [regime](https://apexrunner.ai/signals/regime)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
