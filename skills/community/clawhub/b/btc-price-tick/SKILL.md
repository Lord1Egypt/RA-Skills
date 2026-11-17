---
name: btc-price-tick
description: "Paid x402 endpoint: $0.007 USDC per call on Base. Returns real-time BTC price tick from live exchange feeds."
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/btc-price-tick
    emoji: "💹"
---
# btc-price-tick

## What It Does
Real-time BTC price tick from live exchange feeds. Computed by APEX Runner from live market data, not from backtests.

## When to Use
- When you need a low-latency BTC price reference
- Inside high-frequency polling loops
- As a baseline for spread or momentum calculations

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/btc-price-tick
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
response = session.get("https://apexrunner.ai/signals/btc-price-tick")
print(response.json())
```

## Example Response
```json
{
  "b": 67482.50,
  "e": 3541.20,
  "s": 152.30,
  "a": 24.10,
  "t": 1750000000
}
```

## Pricing
**$0.01/call** — standard price

Every caller is charged $0.007/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [market-tick](https://apexrunner.ai/signals/market-tick)
- [apex-pulse](https://apexrunner.ai/signals/apex-pulse)
- [btc-dominance](https://apexrunner.ai/signals/btc-dominance)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
