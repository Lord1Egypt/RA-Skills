---
name: capitulation-alert
description: "Paid x402 endpoint: $0.014 USDC per call on Base. Returns contrarian setups when a liquidation cascade meets a crowded trade: fires only when Hyperliquid liquidation pressure is >80/100 and top wallets are crowded >70/100 on the side whose liquidations sit near price, with side, entry zone, target and invalidation (BTC, ETH, SOL)."
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/capitulation-alert
    emoji: "🩸"
---
# capitulation-alert

> **Tier 3 — Strategic Edge**: A composite signal that combines several of APEX Runner's market models into one higher-level reading.

## What It Does
Contrarian setups when a liquidation cascade meets a crowded trade: fires only when Hyperliquid liquidation pressure is >80/100 and top wallets are crowded >70/100 on the side whose liquidations sit near price, with side, entry zone, target and invalidation (BTC, ETH, SOL). Computed by APEX Runner from live market data, not from backtests.

## When to Use
- Polling every few minutes in a stressed market for a contrarian entry (alert=false is the usual answer; no_setup_reason says why)
- To fade a crowded side whose liquidations are stacked within 5% of price
- For a ready entry zone, target and invalidation from the liquidation clusters — probability_estimate is an uncalibrated HIGH/MEDIUM heuristic

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/capitulation-alert
```

The x402 client handles payment automatically. No API key, no account, no subscription — just an EVM wallet with USDC on Base mainnet (no ETH needed).

```python
# pip install "x402[evm,requests]"
import os

import requests
from eth_account import Account
from x402 import max_amount, x402ClientSync
from x402.http.clients import wrapRequestsWithPayment
from x402.mechanisms.evm.exact import register_exact_evm_client
from x402.mechanisms.evm.signers import EthAccountSigner

client = x402ClientSync()
register_exact_evm_client(client, EthAccountSigner(Account.from_key(os.environ["EVM_PRIVATE_KEY"])))
client.register_policy(max_amount(20000))  # never sign more than the list price ($0.02 USDC)

session = wrapRequestsWithPayment(requests.Session(), client)
response = session.get("https://apexrunner.ai/signals/capitulation-alert")
print(response.json())
```

## Example Response
```json
{
  "coin": "BTC",
  "alert": true,
  "status": "CAPITULATION_SETUP",
  "cascade_risk": "HIGH",
  "cascade_risk_score": 96,
  "contrarian_setup": "SHORT",
  "cascade_direction": "DOWN",
  "probability_estimate": {
    "label": "HIGH",
    "basis": "heuristic",
    "calibrated": false
  },
  "suggested_entry_zone": {
    "low": 58090.0,
    "high": 58498.7
  },
  "target": {
    "price": 56455.2,
    "band_low": 56120.0,
    "band_high": 57010.0,
    "distance_pct": 2.814
  },
  "invalidation_price": 60240.0,
  "reward_to_risk": 0.76,
  "summary": "BTC: top wallets crowded LONG (crowding 88/100) with 88% of near liquidations on that side (cascade 96/100). Contrarian SHORT 58,090.0-58,498.7, target 56,455.2, invalidation 60,240.0.",
  "method_version": "cap-1",
  "timestamp": "2026-11-20T19:28:46Z"
}
```

## Pricing
**$0.02/call** — standard price

Every caller is charged $0.014/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [crowded-trade-detector](https://apexrunner.ai/signals/crowded-trade-detector)
- [liquidation-pressure](https://apexrunner.ai/signals/liquidation-pressure)
- [check-trade-safety](https://apexrunner.ai/signals/check-trade-safety)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
