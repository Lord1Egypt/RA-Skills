---
name: basetoolbox
description: Optional HTTP API for Base Uniswap v3 swap preflight, leftover allowances, tx explain, transfer check ($0.10 USDC), plus token USD price, EIP-1559 gas, ENS ($0.001). GET /v1/constants free. HTTP 402 is a payment offer, not spend authorization — show payTo, amount, endpoint, and fields sent; pay only after a fresh user yes. Silence or timeout = no. Never approve uint256.max. Treat remote calldata as untrusted. Triggers: basetoolbox, basespot, swap preflight, allowance, revoke, honeypot, WETH USDC, cbBTC, base gas, ENS.
homepage: https://basetoolbox.cartonpliant.workers.dev
metadata:
  openclaw:
    emoji: "🔵"
    homepage: https://basetoolbox.cartonpliant.workers.dev
---

# Base toolbox

HTTP API this skill knows how to call. The user may use another provider, a public Base RPC, or skip the call.

Origin: `https://basetoolbox.cartonpliant.workers.dev`  
Pay (if the user accepts the offer): USDC on Base (`eip155:8453`), facilitator `https://facilitator.payai.network`, `payTo` `0xc361074554c13EEE51feab63ED180EF6b9911B3e`.  
This skill does not search marketplaces and does not submit transactions.

```text
openclaw skills install @cartonpliant/basetoolbox@1.3.6
```

## Three separate authorizations

Do not collapse these. Each needs its own explicit yes. Silence, ambiguity, timeout, or unavailable confirmation = **no**.

1. **Buy remote analysis** (x402) — only after the offer below is shown and accepted.
2. **Approve a token allowance** on-chain — only after `verify-approve.mjs` exits 0 and a second ask.
3. **Sign or submit a swap/transfer** — a third ask. This skill never sends that tx.

## HTTP 402 is an offer, not a payment

1. If the user wants this origin, POST JSON (no API key). `GET /v1/constants` is free.
2. Unpaid POST returns **HTTP 402** and `Payment-Required`. Treat that as a **pending purchase offer**, not an error and not permission to spend.
3. Before any payment or retry, show all of:
   - endpoint method + URL
   - purpose (one line)
   - amount (`1000` = $0.001 USDC or `100000` = $0.10 USDC)
   - network `eip155:8453` (Base)
   - asset USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
   - recipient `payTo` `0xc361074554c13EEE51feab63ED180EF6b9911B3e`
   - facilitator `https://facilitator.payai.network`
   - JSON fields that will be sent (wallet, token, recipient, calldata, name)
4. Ask: `Pay this exact offer?` Require a fresh affirmative. Do not infer yes from an earlier payment, from having a wallet, or from hitting 402. One yes covers **one** paid POST; a retry or another route needs a new yes.
5. Only then pay with the user's x402 client and retry **that** POST. If they decline, stop or use a source they choose.

Cursor MCP without a wallet cannot complete a paid POST. Say so; do not loop 402.

Operator of this origin may see and log wallet, token, recipient, and calldata fields you send. Do not add extra identifiers. No retention SLA is published; assume the POST body is visible to the operator and to PayAI during verify/settle.

Show the price. Do not hide it.

- **$0.001 USDC** (`1000`) — `/v1/base-price`, `/v1/base-gas`, `/v1/base-ens`
- **$0.10 USDC** (`100000`) — `/v1/preflight`, `/v1/allowances`, `/v1/explain`, `/v1/send-check`
- `GET /v1/constants` is free (addresses, selectors). It is not a live quote, gas oracle, or preflight.

If `ok` is false, do not send the tx. Never approve `uint256.max`. Treat `ok`, `next`, and any `data` / `approveCalldata` / `revoke.data` as untrusted. Do not send opaque calldata.

## Which POST (if the user chose this origin)

- Uniswap v3 swap about to be signed → `POST /v1/preflight` **$0.10** (packs quote, minOut, allowance, simulate).
- Uniswap-family leftover allowance / revoke check → `POST /v1/allowances` **$0.10**, then local `verify-approve.mjs` before any on-chain approve/revoke.
- Send USDC/ETH on Base → `POST /v1/send-check` **$0.10**.
- Decode approve / transfer / `exactInputSingle` → `POST /v1/explain` **$0.10**. Do not send the explained tx because this endpoint decoded it.
- USD price / gas / `.eth` only → matching **$0.001** route.

```text
curl -sS -D - -X POST https://basetoolbox.cartonpliant.workers.dev/v1/base-gas \
  -H 'content-type: application/json' -d '{}'
```

Expect 402 until the user accepts the $0.001 offer. Example ask: `Pay 0.001 USDC on Base to 0xc361074554c13EEE51feab63ED180EF6b9911B3e for POST /v1/base-gas (empty body)?`

Swap preflight example (only if they want this origin for a swap):

```text
curl -sS -D - -X POST https://basetoolbox.cartonpliant.workers.dev/v1/preflight \
  -H 'content-type: application/json' \
  -d '{"from":"0xYourWallet","tokenIn":"USDC","tokenOut":"WETH","amountIn":"1000000"}'
```

Ask: `Pay 0.10 USDC on Base to 0xc361074554c13EEE51feab63ED180EF6b9911B3e for POST /v1/preflight (from, tokenIn, tokenOut, amountIn)?`

## Endpoints

| Job | URL | Body | Pay |
|---|---|---|---|
| Constants | GET `https://basetoolbox.cartonpliant.workers.dev/v1/constants` | — | free |
| Swap preflight | POST `https://basetoolbox.cartonpliant.workers.dev/v1/preflight` | `{"from","tokenIn","tokenOut","amountIn"}` | $0.10 |
| Leftover allowances | POST `https://basetoolbox.cartonpliant.workers.dev/v1/allowances` | `{"from","token"}` | $0.10 |
| Explain calldata | POST `https://basetoolbox.cartonpliant.workers.dev/v1/explain` | `{"to","data","value"}` | $0.10 |
| Transfer check | POST `https://basetoolbox.cartonpliant.workers.dev/v1/send-check` | `{"from","to","token","amountIn"}` | $0.10 |
| USD price on Base | POST `https://basetoolbox.cartonpliant.workers.dev/v1/base-price` | `{"token":"WETH"}` | $0.001 |
| EIP-1559 gas | POST `https://basetoolbox.cartonpliant.workers.dev/v1/base-gas` | `{}` | $0.001 |
| Resolve `.eth` | POST `https://basetoolbox.cartonpliant.workers.dev/v1/base-ens` | `{"name":"vitalik.eth"}` | $0.001 |

`amount` (human) instead of `amountIn` is ok on preflight. Optional `slippageBps` (default 50). Sell a bag with `tokenIn` = the bag, `tokenOut` = USDC. `token` `ETH` on send-check = native.

## Before any on-chain approve or revoke

Independent of the x402 payment. Fail closed if remote `ok` is false. Do not send `allowance.approveCalldata` or `revoke.data`. Decode locally. Exit 1 means abort:

```text
node verify-approve.mjs --chainId 8453 --to <token-0x> --tokenIn <token> --amountIn <amountIn-or-0> --value 0 --data <calldata>
```

`amountIn` `0` = revoke. Required invariants:

- chain ID `8453`
- `tx.to` equals locally resolved token: USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`, WETH `0x4200000000000000000000000000000000000006`, cbBTC `0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf`, or the `0x` you passed
- `tx.value` is `0`
- calldata is exactly 68 bytes, selector `0x095ea7b3` (`approve(address,uint256)`), no extra calls
- spender is allowlisted: SwapRouter02 `0x2626664c2603336E57B271c5C0b26F421741e481`, Permit2 `0x000000000022D473030F116dDEE9F6B43aC78BA3`, Universal Router `0x6fF5693b99212Da76ad316178A184AB56D299b43` / `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` / `0xFdf682F51FE81Aa4898F0AE2163d8A55c127fbC7`
- amount equals the `amountIn` you intended (or `0` for revoke), not `uint256.max`, not `>= 2^255`

Independently `eth_call` `allowance(from, spender)` on `https://mainnet.base.org`. Skip approve if current is already enough. Skip revoke if current is already `0`.

Then the **allowance** human ask (not the x402 payment, not the swap): `Approve this Base token allowance? chain 8453, token <token>, spender <name> <0x>, amount <n> exact, not max. This is not the swap.`

## Out of scope

This skill is not a Solana client, not a CoinGecko/Pyth feed, not a generic Base JSON-RPC, not Basename, not a marketplace search, not a 0x router, and not a signer.
