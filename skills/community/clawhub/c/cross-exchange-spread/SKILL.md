---
name: cross-exchange-spread
description: Live spread between Kraken, Coinbase, and Hyperliquid for arb detection
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/cross-exchange-spread
    emoji: "↔️"
---
# cross-exchange-spread

## What It Does
Live spread between Kraken, Coinbase, and Hyperliquid for arb detection. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- Before routing orders between exchanges
- To detect arb windows
- As input to optimal-order-routing

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/cross-exchange-spread
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/cross-exchange-spread",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "kraken_btc": 67480.00,
  "coinbase_btc": 67492.00,
  "spread_usd": 12.00,
  "spread_bps": 1.78
}
```

## Pricing
**$0.10/call** — standard price

Early adopters automatically receive 30% off ($0.07/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [arb-spread](https://apexrunner.ai/signals/arb-spread)
- [cross-exchange-spread](https://apexrunner.ai/signals/cross-exchange-spread)
- [optimal-order-routing](https://apexrunner.ai/signals/optimal-order-routing)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
