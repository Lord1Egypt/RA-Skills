---
name: base-address-balance
description: Base wallet balance lookup with no API key. Returns the ETH balance and token holdings (USDC, WETH, the top 200 Base tokens, and any token contracts you name) of one Base address at the latest block. Costs $0.01 USDC per lookup, paid from the agent's existing agentcash or awal wallet. Use to check what a Base wallet holds before a payment, transfer or swap. Balances only, with no labels, identities or USD values.
version: 1.0.0
homepage: https://botx402.io
metadata:
  openclaw:
    requires:
      bins:
        - npx
    envVars:
      - name: X402_PRIVATE_KEY
        required: false
        description: agentcash's own key override. agentcash signs with it; the skill only checks that it's set.
---

# Base wallet balance

One paid call to `api.botx402.io` returns what a Base wallet holds now, for $0.01 USDC. No account, no API key.

It needs an existing agentcash or awal wallet holding USDC: x402 on Base, or (agentcash) MPP on Tempo. The wallet CLI holds the signing key, and this skill never reads it.

The skill has no install step. On first use, `npx -y` downloads and runs two npm packages pinned to exact versions: [`agentcash@0.17.1`](https://www.npmjs.com/package/agentcash) and [`awal@2.12.2`](https://www.npmjs.com/package/awal). The call sends the looked-up address to `api.botx402.io`, and nothing else about the user.

## 1. Pick the wallet

- **agentcash** (preferred: pays x402 or MPP), when `test -f ~/.agentcash/wallet.json` or `[ -n "${X402_PRIVATE_KEY:+set}" ]` succeeds. Both test presence only: never print, log or pass the key, or run `env` to find it.
- **awal** (Coinbase Agentic Wallet, x402 on Base), when there's no agentcash wallet and the user says they pay with awal. Only after that yes, run `npx -y awal@2.12.2 status` to confirm a signed-in wallet. This fallback path is untested with awal.

Run agentcash commands only once one of those holds: on its first run agentcash creates a new, empty wallet, and setting up a wallet is the user's decision.

If neither wallet is there, tell the user this skill pays from an existing agentcash or awal wallet holding USDC, and stop.

Done when one wallet is chosen, or you've told the user and stopped.

## 2. Get the user's approval for a budget

Before the first lookup in a conversation, ask once, naming the price, the wallet and a budget:

> Each Base balance lookup costs $0.01 USDC, paid from your agentcash wallet. OK to spend up to $0.10 (10 lookups) in this conversation?

- Make lookups only after a clear yes, and only as many as approved. A budget the user names instead is the budget, if it's a specific amount or number of lookups. If the answer is open-ended ("as many as you need"), ask for a number.
- Count every call the wallet CLI reports as paid, whatever the HTTP status. If you lose count, can't tell whether a call was charged, or the budget is used up, ask again before the next lookup.

The skill asks because neither wallet has a cap it can read that only the user can change: agentcash's `maxAmount` is per call and not locked against the agent, and awal's limits live in its wallet app with no command that reports them. That approval covers each lookup inside the budget, with no prompt per call. Every call also caps its own price with the wallet's max-amount flag, so the wallet refuses a request for more than $0.01. Keep that flag at $0.01, and leave agentcash's `maxAmount` setting as the user set it.

Done when the user has approved a number of lookups and the next lookup is within it.

## 3. Call

The body is JSON. Required: `chain` (`"base"`) and `address` (`0x` + 40 hex). Optional: `token_addresses` (up to 50 ERC-20 contracts beyond the fixed list) and `pagination` (`{"page": 1, "per_page": 100}`, `per_page` up to 250).

With agentcash:

```bash
npx -y agentcash@0.17.1 fetch "https://api.botx402.io/base-address-balance?via=clawhub" \
  -m POST \
  -H "Content-Type: application/json" \
  -H "X-Botx402-Source: clawhub/1.0.0" \
  -b '{"chain":"base","address":"0x28c6c06298d514db089934071355e5743bf21d60"}' \
  --max-amount 0.01
```

With awal (`--max-amount` is in atomic units: 10000 is $0.01):

```bash
npx -y awal@2.12.2 x402 pay "https://api.botx402.io/base-address-balance?via=clawhub" \
  -X POST \
  -h '{"Content-Type":"application/json","X-Botx402-Source":"clawhub/1.0.0"}' \
  -d '{"chain":"base","address":"0x28c6c06298d514db089934071355e5743bf21d60"}' \
  --max-amount 10000
```

`?via=clawhub` and `X-Botx402-Source` are an attribution tag: they tell botx402 the call came through this skill, carry no user data, and don't change the result.

Done when the command returns the answer or an error.

## 4. Read the answer

```json
{"block_number": 52943289,
 "pagination": {"page": 1, "per_page": 10, "is_last_page": true},
 "data": [{"token_address": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913", "token_symbol": "USDC",
   "token_name": "USD Coin", "token_decimals": 6, "token_amount": 604.382274, "token_amount_raw": "604382274"}]}
```

- `data` holds only non-zero balances: ETH first (the zero address), then tokens by market-cap rank, then the contracts you named. A token missing from `data` has a zero balance at `block_number`.
- `token_amount_raw` is exact, in the token's smallest unit: use it for arithmetic, `token_amount` for display.
- `is_last_page` false: the next page is another $0.01 lookup, fetched only if the user needs it.

The seller charges nothing for these errors (still count any call the wallet reports as paid):
- **400:** the input is wrong (only `base` is served; the address is 0x + 40 hex). Fix it and retry.
- **402:** the payment didn't verify or settle.
- **502 / 503:** upstream; for 503, retry after `Retry-After` seconds.

For history, USD values, labels or other chains, tell the user it's outside this lookup.
