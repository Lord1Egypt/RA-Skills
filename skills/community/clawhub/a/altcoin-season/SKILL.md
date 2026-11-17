---
name: altcoin-season
description: "Paid x402 endpoint: $0.007 USDC per call on Base. Returns altcoin season index — measures capital rotation from BTC to alts."
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/altcoin-season
    emoji: "🌀"
---
# altcoin-season

## What It Does
Altcoin season index — measures capital rotation from BTC to alts. Computed by APEX Runner from live market data, not from backtests.

## When to Use
- When sizing altcoin vs BTC positions
- To time rotation trades
- As context alongside btc-dominance

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/altcoin-season
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
response = session.get("https://apexrunner.ai/signals/altcoin-season")
print(response.json())
```

## Example Response
```json
{
  "index": 38,
  "label": "Bitcoin Season",
  "threshold": 75
}
```

## Pricing
**$0.01/call** — standard price

Every caller is charged $0.007/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [btc-dominance](https://apexrunner.ai/signals/btc-dominance)
- [capital-rotation-signal](https://apexrunner.ai/signals/capital-rotation-signal)
- [regime](https://apexrunner.ai/signals/regime)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
