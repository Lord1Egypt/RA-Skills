# API invariants

Verify exact payloads against the current official docs and maintained SDK before implementation.

## Endpoints and identity

- `/info` requests are unsigned reads.
- `/exchange` actions are signed writes.
- Mainnet and testnet use different endpoints and identities.
- Perp, spot, HIP-3, and other asset classes use different ID spaces.
- UI names can differ from wire names.

For HIP-3 builder perps, the [official asset-ID guide](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/asset-ids), retrieved 2026-09-23, gives `100000 + perp_dex_index * 10000 + index_in_meta`; discover DEX order through [`perpDexs`](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals) and the market index through that DEX's `meta`, then verify the mapping at runtime.
For spot, the [official asset-ID guide](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/asset-ids), retrieved 2026-09-23, gives `10000 + spotInfo["index"]` from `spotMeta`; a spot pair ID differs from a token ID and varies by network.

Resolve all identities from metadata and assert the reverse mapping before sending.

## Signing

Hyperliquid has distinct L1-action and user-signed schemes. Field order, msgpack encoding, address case, decimal formatting, vault address, nonce, network source, and expiry affect the signature. Prefer the official SDK. Manual signing requires parity fixtures for every action and network.

API wallets sign for a user, subaccount, or vault. Account reads use the represented address. Nonces are tracked per signer, so concurrent processes sharing a signer need one atomic nonce allocator and durable ownership.

The [official nonce guide](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets), retrieved 2026-09-23, requires a nonce inside `(T - 2 days, T + 1 day)`, with `T` the block's Unix millisecond timestamp; validate clock skew and expiry before signing.
The [official nonce guide](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets), retrieved 2026-09-23, stores the 100 highest nonces per signer address; each new nonce must exceed the smallest stored nonce and must never have been used before. Serialize allocation across all processes using that signer.

Do not reuse a deregistered API-wallet address. Its stored nonce history may be pruned, enabling replay of old signed actions.

## Numbers

Wire prices and sizes are decimal strings. Apply current price significant-figure and decimal limits. Round size down to current `szDecimals`. Validate minimum notional and the applicable margin tier after rounding.

## Orders

Each leg has a unique 128-bit client order ID. Model action-level rejection, per-leg error, resting, full fill, partial fill, trigger wait, parent wait, cancellation, and unknown transport result.

`expiresAfter` is part of signing for supported L1 actions. A stale expiry can consume extra rate-limit weight. User-signed actions do not all accept it.

## Account modes

Support standard, unified, and portfolio margin as different normalized state variants. Under unified or portfolio mode, individual perp DEX balance state may be incomplete; spot and borrow/lend state become load-bearing.

## Limits

Load current IP, address, open-order, daily action, WebSocket, and in-flight limits from official docs or current API state. Batches count differently for IP and address budgets. Cancellation capacity may differ from placement capacity.
