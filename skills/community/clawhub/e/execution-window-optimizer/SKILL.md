---
name: execution-window-optimizer
description: "Paid x402 endpoint: $0.007 USDC per call on Base. Returns an execute-now-or-wait verdict before a large order: scores the current execution window 0-100 from session, regime, Fear & Greed and volatility."
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/execution-window-optimizer
    emoji: "⏱️"
---
# execution-window-optimizer

## What It Does
An execute-now-or-wait verdict before a large order: scores the current execution window 0-100 from session, regime, Fear & Greed and volatility. Computed by APEX Runner from live market data, not from backtests.

## When to Use
- Before sending a large order: a check costing at most $0.01 says execute now or wait
- To pick market vs limit for the current session and volatility
- Together with slippage-forecast, which prices your exact order size

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/execution-window-optimizer
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
client.register_policy(max_amount(10000))  # never sign more than the list price ($0.01 USDC)

session = wrapRequestsWithPayment(requests.Session(), client)
response = session.get("https://apexrunner.ai/signals/execution-window-optimizer")
print(response.json())
```

## Example Response
```json
{
  "coin": "BTC",
  "window_score": 83,
  "verdict": "EXECUTE_NOW",
  "recommended_order_type": "market",
  "rationale": "Historically favorable execution conditions",
  "components": {
    "time_of_day": {
      "score": 95,
      "utc_hour": 14,
      "session": "US"
    },
    "regime": {
      "score": 80,
      "regime": "RANGING"
    },
    "fear_greed": {
      "score": 70,
      "value": 24
    },
    "volatility": {
      "score": 75,
      "atr_pct": 1.812
    }
  },
  "next_optimal_window": "15:00 UTC (+1h)",
  "timestamp": "2026-11-20T14:05:00Z",
  "valid_for_seconds": 300
}
```

## Pricing
**$0.01/call** — standard price

Every caller is charged $0.007/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [slippage-forecast](https://apexrunner.ai/signals/slippage-forecast)
- [optimal-order-routing](https://apexrunner.ai/signals/optimal-order-routing)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
