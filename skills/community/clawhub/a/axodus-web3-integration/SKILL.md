---
name: web3-integration
description: Integrate apps with blockchain providers, wallets, and contract calls safely.
metadata:
  author: RedHat Dev
  version: 1.0.0
  owner: RedHat Dev Agent
  category: blockchain
---

# SKILL: web3-integration

## Purpose
Integrate a frontend/backend with blockchain interaction (wallet connect, provider configuration, contract calls) using safe, testable patterns.

## When to Use
- A dApp needs to read/write contract state.
- A backend service must index or react to on-chain events.
- Wallet connection UX and chain gating is required.

## Inputs
- `stack` (required, enum: `ethers|viem|web3js`): preferred client library.
- `chain` (required, string): chain name + chainId.
- `rpc` (optional, string): RPC URL reference (env/config), not hardcoded.
- `contract_address` (required, string).
- `abi_source` (required, string): ABI path/artifact reference.
- `wallet_flow` (optional, enum: `injected|walletconnect|server_signer`).

## Steps
1. Validate chain/contract coordinates (chainId, address format, ABI match).
2. Set provider/signer flow:
   - frontend: user wallet signer
   - backend: server signer only when explicitly required and keys are secured externally
3. Implement contract client wrapper:
   - typed interfaces when possible
   - explicit timeouts/retries for RPC
4. Add chain gating:
   - refuse wrong chain
   - prompt network switch (frontend)
5. Add logging/audit hooks for write operations.
6. Add tests:
   - unit tests for wrapper
   - local chain simulation when available

## Validation
- No secrets stored in repo (keys only via secrets manager/env).
- Wrong-chain behavior is safe (no accidental writes).
- Errors are handled deterministically (retry policy is explicit).

## Output
- Wrapper module path(s)
- Environment variable contract (what must be configured)
- Validation commands (tests/build)

## Safety Rules
- Never request or paste private keys into chat/output.
- Never default to mainnet.
- Avoid â€œauto-signâ€ server flows unless explicitly required and approved.

## Example
Input:
- `stack`: `viem`
- `chain`: `base:8453`
- `contract_address`: `0x...`
- `abi_source`: `artifacts/MyContract.json`

Output:
- `src/web3/client.ts` with chainId checks and a typed contract instance.
