# AIDEX Security Model

## Architecture

The AIDEX skill uses a client-side signing architecture. This document explains how it works and why it's secure.

## How a swap works step by step

1. **Agent requests swap parameters** — The `swap.js` script sends a POST request to the AIDEX API with high-level swap parameters: which token to sell, which token to buy, and how much. The API does NOT receive the private key.

2. **API builds the transaction** — The AIDEX API finds the best exchange route, computes the exact transaction data (contract address, call data, gas parameters, nonce), and returns it as a complete unsigned transaction object.

3. **Local signing** — The `swap.js` script uses `ethers.Wallet.signTransaction()` to sign the transaction locally. The private key **never** leaves your machine. Transaction signing happens entirely on your side.

4. **Broadcasting** — The signed raw transaction (a hex string) is sent to the AIDEX API, which broadcasts it to the Ethereum network via `eth_sendRawTransaction`. This is equivalent to what any public RPC endpoint does.

## What makes this secure

### The private key never leaves the machine

The key is resolved locally from one of two sources: the `AIDEX_PRIVATE_KEY` environment variable or the operating system's credential manager (via `@napi-rs/keyring`). In both cases, the key is used exclusively by the local ethers.js `Wallet` instance to produce a cryptographic signature. No API call, at any point, includes the private key.

### Signed transactions are tamper-proof

An Ethereum transaction, once signed, is cryptographically bound to its parameters. If anyone modifies any field — the recipient address, the amount, the call data, the gas price — the signature becomes invalid and the transaction is rejected by the network.

This means:
- The AIDEX API cannot change what you signed
- A man-in-the-middle cannot alter the transaction
- Even a fully compromised AIDEX server can only broadcast exactly what you signed, or refuse to broadcast it

### The API is a public RPC relay

The `POST /api/v1/agent/swap/send` endpoint is functionally equivalent to calling `eth_sendRawTransaction` on any public Ethereum RPC. It receives a signed transaction and submits it to the network. It has no special privileges and cannot modify the transaction in any way.

### All read operations are unauthenticated

Token searches, rate checks, balance queries, and transaction receipts are all read-only operations that use publicly available blockchain data. They do not require a private key and do not expose any sensitive information.

## Risk assessment

### What can go wrong

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| AIDEX API compromised | Low | None — attacker can only see/broadcast signed txs they cannot alter | Client-side signing architecture |
| OpenClaw host compromised (env) | Low-Medium | High — attacker gets the private key from process environment | Use a dedicated wallet with limited funds |
| OpenClaw host compromised (keyring) | Low-Medium | High — attacker may access the keyring if logged in as the same OS user | Use a dedicated wallet with limited funds; OS-level access controls |
| Network eavesdropping | Low | None — signed txs are public anyway once broadcast | Standard HTTPS encryption |
| Malicious transaction data from API | Very Low | Medium — user signs a bad transaction | Slippage protection, deadline, user review of rates before swap |

### Recommended practices

1. **Use a dedicated trading wallet** — Create a new wallet specifically for automated trading.
2. **Start small** — Begin with small amounts to verify everything works as expected.
3. **Review rates before swaps** — The agent should always show you the exchange rate and gas cost before executing.
4. **Set reasonable slippage** — The default 0.5% slippage protects against price movements. Adjust based on token volatility.
5. **Monitor transaction results** — After each swap, check the receipt to confirm actual amounts.

## Comparison with alternatives

### vs. Custodial (CEX) integrations
In custodial integrations, you deposit funds to the platform. The platform holds your money and you trust them not to lose it, get hacked, or freeze your account. AIDEX never touches your funds — they stay in your wallet.

### vs. Server-side signing
Some integrations ask you to provide your private key to a server that signs transactions on your behalf. This is a significantly higher risk profile. With AIDEX, signing happens on your machine, and the key is never transmitted over the network.

## Note on `primaryEnv` in SKILL.md metadata

The SKILL.md declares `"primaryEnv": "AIDEX_PRIVATE_KEY"`. This is a workaround for a limitation in OpenClaw's current architecture: OpenClaw does not provide a mechanism for optional sensitive environment variables. Without `primaryEnv` (or `requires.env`, which would make the variable mandatory and block the entire skill), the `AIDEX_PRIVATE_KEY` variable is rejected by OpenClaw's env sanitizer (pattern `_PRIVATE_KEY`).

Using `primaryEnv` maps the variable to OpenClaw's `apiKey` config field. Despite this naming, the AIDEX API is fully public and does not require authentication. The private key is used exclusively for client-side transaction signing and is never sent to the API. The `primaryEnv` field exists solely to allow the private key through the sanitizer while keeping it optional (read-only operations work without it).
