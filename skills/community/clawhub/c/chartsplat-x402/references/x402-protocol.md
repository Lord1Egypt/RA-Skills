# x402 Protocol Reference

This skill uses [x402](https://x402.org), an open standard for HTTP-native micropayments. The buyer signs an off-chain authorization; a facilitator settles the payment on-chain and pays the gas. The buyer never sends an on-chain transaction directly.

## Flow

```
1. Client    POST /chart                                  (no payment)
2. Server -> 402 Payment Required + PAYMENT-REQUIRED header
3. Client    decodes requirements, signs EIP-3009 authorization off-chain
4. Client -> POST /chart with PAYMENT-SIGNATURE header
5. Server    verifies signature via Coinbase facilitator
6. Server    generates the chart
7. Server    settles the payment on-chain (facilitator pays gas)
8. Server -> 200 OK + chart + PAYMENT-RESPONSE header (settlement tx)
```

`@x402/fetch`'s `wrapFetchWithPayment` does the entire dance automatically.

## Headers

| Header | Direction | Content |
|--------|-----------|---------|
| `PAYMENT-REQUIRED` | Server → Client | Base64-encoded payment requirements |
| `PAYMENT-SIGNATURE` | Client → Server | Base64-encoded signed payment payload |
| `PAYMENT-RESPONSE` | Server → Client | Base64-encoded settlement result (tx hash, network, payer) |

## Networks & Tokens

The chart-splat server advertises:

- **Mainnet**: `eip155:8453` (Base) — USDC at `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- **Testnet**: `eip155:84532` (Base Sepolia) — USDC

Use the [Circle faucet](https://faucet.circle.com) for testnet USDC.

## Common Gotchas

### 1. v1 vs v2 package mismatch

Use `@x402/*` (scoped, v2.x) — **not** the legacy unscoped `x402-fetch@1.x`. The header names changed between versions:

- v1: `X-PAYMENT` (request), `X-PAYMENT-RESPONSE` (response)
- v2: `PAYMENT-SIGNATURE` (request), `PAYMENT-RESPONSE` (response), `PAYMENT-REQUIRED` (server hint)

Mixing v1 client with v2 server returns 402 forever — the client never recognizes the v2 hint header.

### 2. Network string format

The server uses CAIP-2 IDs (`eip155:8453`). Some legacy v1 docs use bare names (`base`, `base-sepolia`). The exact-EVM client matches `eip155:*` schemes; don't override the network on the client side.

### 3. Body must be re-readable

`wrapFetchWithPayment` retries the request after attaching the payment header. Pass a string or `Buffer` body — never a consumed `ReadableStream`.

### 4. Header casing

Per spec the headers are uppercase, but proxies often lowercase them. Always read with the case-insensitive `headers.get()` (Web Fetch API) — never index a raw map.

### 5. Validity window

EIP-3009 authorizations carry `validBefore`. The default window is ~1 hour. If the system clock is skewed by more than the window, signatures fail. Re-sign on each retry; never cache a signed authorization.

### 6. Insufficient USDC → settlement failure

The signature step succeeds even if the wallet is empty — only on-chain settlement fails. Symptom: a second 402 with `error: "settlement failed"` in the body. Top up the paying wallet and retry.

## References

- Protocol spec & SDKs: https://github.com/x402-foundation/x402
- Coinbase facilitator: https://x402.org/facilitator
- Chart Splat docs: https://chartsplat.com/docs
- EIP-3009 (Transfer With Authorization): https://eips.ethereum.org/EIPS/eip-3009
