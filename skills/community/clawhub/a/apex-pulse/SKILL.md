---
name: apex-pulse
description: "Paid x402 endpoint: $0.007 USDC per call on Base. Returns APEX service heartbeat — service status, BTC regime, Fear & Greed and BTC price in one cheap call."
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/apex-pulse
    emoji: "❤️"
---
# apex-pulse

## What It Does
APEX service heartbeat — service status, BTC regime, Fear & Greed and BTC price in one cheap call. Computed by APEX Runner from live market data, not from backtests.

## When to Use
- To verify APEX is live before relying on its signals
- Inside health-check workflows
- To confirm signal freshness before trading

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/apex-pulse
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
response = session.get("https://apexrunner.ai/signals/apex-pulse")
print(response.json())
```

## Example Response
```json
{
  "status": "LIVE",
  "regime": "RANGING",
  "market": "OPEN",
  "fg": 42,
  "fg_label": "Fear",
  "apex_trading": true,
  "active_pairs": 11,
  "timestamp": "2026-06-23T14:00:00Z",
  "valid_for_seconds": 60
}
```

## Pricing
**$0.01/call** — standard price

Every caller is charged $0.007/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [market-tick](https://apexrunner.ai/signals/market-tick)
- [grid-health](https://apexrunner.ai/signals/grid-health)
- [portfolio-heat](https://apexrunner.ai/signals/portfolio-heat)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
