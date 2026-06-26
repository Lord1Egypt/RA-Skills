---
name: paegents-pay
description: >-
  Use Paegents through the published SDK and API surface to register services,
  create usage agreements, activate bilateral escrow, route metered usage, and
  settle with the recommended execution mode.
license: MIT
compatibility:
  - claude-code
  - openclaw
  - cursor
metadata:
  version: "2.9.1"
  author: paegents
  homepage: https://paegents.com
  repository: https://github.com/MarkMcDaniels/paegents-pay-skill
  payment_rail: stablecoin
  escrow_model: bilateral
  networks: base,base-sepolia
  asset: USDC
  beta: true
  openclaw:
    requires:
      env:
        - PAEGENTS_API_URL
        - PAEGENTS_API_KEY
        - PAEGENTS_AGENT_ID
    primaryEnv: PAEGENTS_API_KEY
allowed-tools: Read Write Edit WebFetch
---

# Paegents Pay

Use this skill when an agent needs to buy or sell a service through Paegents without bypassing the public product surface.

Keep the guidance at the integration layer. Do not expose private keys, seller-side secrets, unpublished endpoints, internal architecture, or internal operations detail. Explain what the system expects and why the workflow is structured that way.

## Why The Product Works This Way

- **Client-side signing** keeps payment authority with the wallet owner instead of the platform.
- **Agreement creation and activation are separate** because commercial acceptance is not the same thing as on-chain funding.
- **The activation package is the source of truth** because fees, spenders, nonces, and chain parameters must come from live state.
- **Settlement mode is chosen at runtime** because direct wallet execution and sponsored execution depend on current signer and agreement state.
- **Usage and settlement stay tied to agreement state** so both sides can monitor whether the agreement is merely accepted, actually funded, or ready for settlement.

## Use This When

- a buyer agent needs to purchase a metered or fixed-quantity service
- a seller agent needs to list a service and accept agreement-backed payments
- an operator needs to understand the next valid public action for an agreement
- bilateral escrow, metered usage, or settlement mode selection is part of the task

## Do Not Use This When

- the task is asking for internal implementation details rather than product usage
- someone wants to bypass policy, approval, verification, or signing requirements
- someone wants to share or log private keys, raw wallet secrets, or seller credentials
- a one-off direct payment is being confused with a bilateral escrow agreement

## Preflight

Before taking any action, confirm:

- the user has the public credentials needed for the chosen flow
  - agent auth for agent payment operations
  - owner auth only for owner-scoped setup or policy operations
- the buyer wallet is self-custody and controlled by the signer
- the wallet has enough USDC for the intended payment or escrow
- the signer has gas if the chosen settlement mode requires direct broadcast
- the SDK is installed when SDK use is expected

Do not ask users to paste secrets into chat. Assume secrets stay in their environment.

## Operating Rules

- Prefer SDK calls over hand-built HTTP when both are available.
- Prefer live responses over hardcoded assumptions.
- Never invent fee amounts, spenders, chain IDs, nonces, or agreement state.
- Treat `get_activation_package()` / `getActivationPackage()` as authoritative for bilateral activation.
- If the activation package shows a pending infra fee, treat the infra fee permit as a required second buyer authorization.
- Call settlement options before choosing direct or sponsored settlement.
- Use the current agreement and escrow status before deciding the next step.

## Workflow Map

### Seller

1. Register the service.
2. Configure acceptance behavior and pricing policy.
3. Accept or reject agreements.
4. Deliver through the metered proxy or record usage through the public API.
5. Monitor escrow and settlement state until funds are claimable.

### Buyer: Bilateral Escrow

1. Search or select the service.
2. Create the usage agreement with the commercial terms.
3. Wait for seller acceptance.
4. Fetch the activation package.
5. Sign the buyer activation intent locally.
6. If the package shows a pending infra fee, sign the separate infra fee permit locally.
7. Submit activation and poll until the agreement is active and confirmed.
8. Use the service through the metered path or agreed delivery path.
9. Check settlement options before any close, claim, or withdraw action.

### Buyer: Direct Stablecoin Purchase

Use the direct stablecoin helper when the task is a one-off purchase without bilateral escrow. That flow exists because it solves a simpler trust problem: immediate payment for a single purchase, not an ongoing metered agreement.

## State Guide

- `proposed` or `pending`: terms exist but the commercial flow is not yet live
- `accepted` with activation still pending: both sides agreed, but funds are not yet locked
- `active` with confirmed activation: escrow is funded and usage can proceed
- activation failed or requires refreshed signatures: inspect the reason, refresh the missing authorization, and retry through the public path

## Which Reference To Read Next

- Read [references/QUICK_START.md](references/QUICK_START.md) for the shortest end-to-end public path.
- Read [references/PAYMENT_FLOWS.md](references/PAYMENT_FLOWS.md) when you need lifecycle guidance and decision rules.
- Read [references/SDK_USAGE.md](references/SDK_USAGE.md) for Python and TypeScript method mapping.
- Read [references/API_REFERENCE.md](references/API_REFERENCE.md) only when the SDK is not enough.
- Read [references/ERROR_CODES.md](references/ERROR_CODES.md) when the task is blocked on an API or state error.
- Read [references/RATE_LIMITS.md](references/RATE_LIMITS.md) when the task involves retries, polling, or bulk operations.

## Public Support Boundary

Stay within what a customer or operator can do through the product:

- published SDK methods
- published API routes
- documented activation, metering, and settlement flows
- documented error handling and retry behavior

Do not answer with internal-only remediation steps when a public next action exists.
