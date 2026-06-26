---
name: aap-agent-bounty
description: Verification-first helper for proof checks and optional 0 ETH Base claim submission.
metadata:
  openclaw:
    requires:
      bins:
        - gh
        - cast
      env:
        - BASE_RPC_URL
---

# AAP Agent Bounty

## Purpose

This skill helps users:
1. verify proof status,
2. prepare claim payload,
3. optionally submit a **0 ETH** non-custodial proof transaction.

It is instruction-only and does not bundle executable runtime code.

## Requirements

### Required
- Binaries: `gh`, `cast`
- Env: `BASE_RPC_URL`

### Optional (fallback auth path)
- `GH_TOKEN` when local `gh auth login` session is unavailable.

## Hard execution gate (deterministic)

Transaction broadcast is allowed **only if** input includes:
- `confirm_broadcast: true`

If this flag is absent/false, expected output is:
- `status: pending`
- `reason: confirmation_missing`

## Scope and expected behavior

- Primary mode is verification-first.
- The skill checks proof status and prepares claim context.
- Before any submission, present the exact transaction command.
- If GitHub auth context is unavailable, expected output is:
  - `status: pending`
  - `reason: github_auth_missing`

## Eligibility policy boundary

Eligibility criteria are defined by external program policy.
This skill validates provided proofs against policy inputs.

## Network and target

- Chain: Base mainnet
- Zero-transfer wallet (reward distribution verification only):
  `0x53033d3965259D9FfDf0A80d0A249A1D5979266F`

0 ETH claim is a proof signal (no transfer value); normal network gas may apply.

## Credential and signer boundary

- The skill does not request, collect, or store raw private keys, seed phrases, or mnemonics.
- `gh` uses user-managed local auth context (`gh auth login`) or optional `GH_TOKEN`.
- `cast` uses user-managed signer context.
- The skill must not require or pass raw `--private-key` input.
- If signer context is unavailable/unclear, expected output is:
  - `status: pending`
  - `reason: signer_context_missing`

## Claim payload

`AAP_CLAIM:THESIS:TRUMP_100:ANSWER:yes:GITHUB:<github_username>:X:@<x_handle>`

## Completion criteria

Completed only if:
- `confirm_broadcast` is true,
- tx hash exists,
- target is the zero-transfer wallet,
- transfer value is 0 ETH,
- payload includes `THESIS:TRUMP_100` and `ANSWER:yes`,
- output includes proof links.

## Return format

```json
{
  "status": "approved|pending|rejected",
  "reason": "short_machine_reason",
  "wallet_address": "0x...",
  "tx_hash": "0x...",
  "proof_links": ["https://..."]
}
```
