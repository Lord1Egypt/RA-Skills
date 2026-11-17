---
name: apex-evolution-insight
description: "Paid x402 endpoint: $0.007 USDC per call on Base. Returns weekly strategy evolution insights from APEX's self-improvement engine."
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

> **Tier 3 — Strategic Edge**: A composite signal that combines several of APEX Runner's market models into one higher-level reading.

## What It Does
Weekly strategy evolution insights from APEX's self-improvement engine. Computed by APEX Runner from live market data, not from backtests.

## When to Use
- To understand how APEX's strategy is evolving
- For weekly performance review
- When calibrating long-term strategy alignment

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/apex-evolution-insight
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
response = session.get("https://apexrunner.ai/signals/apex-evolution-insight")
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
**$0.01/call** — standard price

Every caller is charged $0.007/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [signal-intelligence](https://apexrunner.ai/signals/signal-intelligence)
- [regime-transition](https://apexrunner.ai/signals/regime-transition)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
