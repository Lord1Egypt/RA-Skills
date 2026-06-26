# ADR-003: Stellar Smart Wallet / Smart Account — Fit Assessment

**Status**: Proposed  
**Date**: 2026-03-04  
**Author**: CTO  
**Reviewers**: Founder, Product Owner  
**Decision**: **DEFER** (adopt in M2 — Agentic Spend Controls milestone)

---

## Context

ASG Card currently uses x402 v2 for payment: an agent submits a signed Stellar transaction in the `X-PAYMENT` header, the OZ facilitator verifies and settles it, and the API issues a virtual card. The entire flow assumes the agent controls a standard Stellar keypair (Ed25519) with full signing authority.

Stellar Smart Wallets (Soroban smart accounts) introduce **programmable authorization policies** — contract-level rules that constrain what a signer can do. This ADR evaluates whether ASG Card should adopt Smart Wallet integration now (M1) or defer to a future milestone.

## What Smart Wallets Offer

### Policy Signers

Policy signers are Soroban contracts that compose with Ed25519/secp256r1 signers to enforce constraints:

- **Spending limits**: max USDC per tx, per day, per session
- **Allow lists**: restrict to specific contract addresses (e.g., only ASG Card treasury)
- **Time-based**: session keys expire after N minutes/hours
- **Multi-factor**: require multiple signers above a threshold

### Session Signers

Temporary keypairs granted limited authority. An agent manager can issue a session key that only allows:

- Spending ≤ $500 USDC
- To `payTo: GBQL4G3...` (ASG Card treasury only)
- For 24 hours

### OZ Smart Account Library (Soroban)

OpenZeppelin provides a production-grade composable authorization library for Soroban:

- Context rules (amount, destination, time)
- Pluggable signers (Ed25519, Passkey/WebAuthn, secp256r1)
- Policy enforcement via `__check_auth`

## Current ASG Card Flow vs Smart Wallet

| Aspect | Current (M1) | With Smart Wallet (M2) |
|---|---|---|
| Agent auth | Raw Ed25519 keypair | Session key with policy |
| Spend limit | None — agent can drain wallet | Policy-enforced cap |
| Destination | Any — agent chooses | Allow-listed (treasury only) |
| Session expiry | None | Time-bound (e.g., 24h) |
| Multi-factor | None | Optional co-signer |
| Facilitator compat | OZ Channels (`exact` scheme) | Same — policy is pre-tx |
| API changes | None | Minimal — wallet already abstracted behind X-PAYMENT |
| Soroban dependency | No | Yes — requires contract deployment |

## Analysis

### Benefits of Smart Wallet for ASG Card

1. **Agent Safety**: AI agents operating with session keys can't exceed predefined spend limits. Critical for enterprise deployments where an autonomous agent manages a budget.

2. **Destination Lock**: Policy signers can restrict payments to only the ASG Card treasury address, eliminating the risk of agent misdirection attacks.

3. **Time-Bounded Sessions**: An agent runtime (e.g., IronClaw executor) can receive a 24h session key, limiting blast radius if compromised.

4. **No API-Side Changes**: Smart wallet policies are enforced **on the Stellar side** before the transaction reaches x402. The API continues to receive a valid signed tx in `X-PAYMENT` — it doesn't care how the tx was authorized.

5. **OZ Ecosystem Alignment**: We already use OZ Channels for facilitation. Their Smart Account library is the natural extension for Soroban-native policy enforcement.

### Risks of Adopting Now (M1)

1. **Complexity**: Smart wallet deployment requires Soroban contract ops (deploy, initialize, manage policies). We don't have this infra yet.

2. **No Client-Side SDK**: ASG Card's current clients send raw Stellar transactions. They would need to create transactions through a smart wallet contract invocation instead. This requires client-side changes.

3. **Facilitator Compatibility**: The OZ facilitor's `exact` scheme assumes standard Stellar payments. Smart wallet `invokeHostFunction` calls may need facilitator updates — unconfirmed.

4. **Not Blocking Launch**: No customer has requested spend limits or session keys. The first customers are developer/hacker-house users who control their own wallets.

5. **Soroban Maturity**: Soroban is production-ready, but smart wallet standards are evolving. Protocol 25 (Q1 2026) adds privacy primitives that may affect policy design.

## Decision

**DEFER to M2 (Agentic Spend Controls).**

Rationale:

- M1 is focused on proving the x402 mainnet flow works end-to-end. Smart wallets add no value to this validation.
- Enterprise/institutional users who need spend limits are M2+ customers.
- OZ Smart Account library needs evaluation once our Soroban tooling is in place.
- We should adopt when the first agent platform integration (e.g., NEAR AI, IronClaw) requests bounded spending.

### M2 Adoption Plan (sketch)

1. Deploy OZ Smart Account contract on Stellar mainnet
2. Add "create session key" endpoint to ASG Card API (or SDK)
3. Agent runtime receives session key instead of raw secret
4. Policy: spend limit + treasury allow-list + 24h expiry
5. x402 flow unchanged — facilitator still sees a valid signed tx
6. POC: 1 success ($10 create within limit) + 1 blocked ($600 over limit)

## References

- [Stellar Smart Wallets Docs](https://developers.stellar.org/docs/build/guides/smart-wallets)
- [OZ Smart Account Library (Soroban)](https://github.com/OpenZeppelin/stellar-contracts)
- [Stellar 2025 Roadmap — Freighter Advanced Auth](https://stellar.org/roadmap)
- [ADR-002: x402 Verify/Settle Strategy](./ADR-002-x402-verify-settle-stellar.md)
