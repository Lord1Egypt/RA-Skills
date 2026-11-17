---
name: galleon-defi-payments
description: Use when planning or reconciling stablecoin transfers, paid x402 requests, token streaming, vesting or airdrop distribution. Match the payment obligation to official wallet and protocol tools; distinguish authorization, settlement and service delivery.
license: MIT
compatibility: Portable Agent Skills instructions; provider access and wallet permissions are configured separately.
metadata:
  author: Galleon Labs
  version: "0.2.1"
---

# DeFi payments

Turn a payment request into a bounded obligation and a verifiable outcome. Use maintained wallet, x402 and streaming tools. This skill grants no spending authority and never treats a payment challenge as permission to pay.

## Start with the requested task

Read [task examples and user configuration](references/task-examples.md) for a completed example and recovery path. Apply only the workflow stages needed by the current request. Reuse supplied preferences and compatible tools; ask only for missing terms that affect this task. Public explanation or comparison does not require transaction fields. Keep any existing authorization within its exact scope.

## Choose the payment model

Read [provider access](references/providers.md) for Coinbase/x402, Sablier and Superfluid. Use [payment workflows](references/workflows.md) for reconciliation and failure cases. A one-time token transfer, per-request API purchase, prefunded vesting schedule and open-ended stream have different obligations. Cross-chain funding needs a bridge lifecycle as well as a payment lifecycle.

1. Establish payer account, recipient or resource origin, chain, exact token/mint, base-unit amount, purpose, deadline and maximum total cost. Include gas, service fees, wrapping and recurring obligations. Resolve names before preparing anything; do not substitute a ticker match or follow a redirect with payment credentials.
2. Reuse the user's approved wallet/provider. Inspect current SDK or tool schemas and account permissions. An API key, managed wallet, alias or session may have a different owner and revocation path. Installing an upstream skill is a separate software action, not authorization to create a wallet or fund it.
3. Gather read-only evidence: spendable balance, allowance, nonce, current schedule/stream state and existing receipt for this obligation. A token balance includes neither guaranteed transferability nor issuer redemption access.
4. Prepare with the official tool. Show recipient, asset, amount, chain, fee cap, expiry and every approval or typed message. For streams include rate, time unit, start/end, maximum funded or accrued obligation, cancellation/transfer rights and who can withdraw. Reject an unexpected recipient, unlimited allowance or unstated perpetual stream.
5. Apply existing explicit authorization only within its approved limits. If a required limit or recipient is missing, obtain that input before signing. Any material change to economic terms needs renewed authorization. Keep signatures and wallet secrets outside chat and artifacts.
6. Submit through the approved wallet workflow, then reconcile transaction or payment identifier, final chain status, actual transferred amount and recipient state. For x402 also verify service delivery. An accepted signature or HTTP 200 does not alone prove final settlement; an onchain payment does not prove the purchased work was delivered.

For paid HTTP resources, load [x402 v2 verification and recovery](references/x402-v2.md) before configuring a paying client. Match the advertised protocol version, scheme and network; preserve one payment identity across recovery and report deferred settlement separately from delivery.

## Bounded autonomy

Recurring payments need enforceable wallet/session limits, a finite budget or review interval, allowed origins/contracts and a stop/revoke path. A prose budget is not a wallet control. Schedule monitoring only when requested; do not create permanent jobs as part of setup. On ambiguous submission, inspect the existing payment/nonce and receipts before any retry. Never create a second payment merely because an API response timed out.

Return a plan or receipt with obligation identity, authorized limits, observed state, fees, delivered resource or stream rights, and unresolved next step. Describe queued, accruing, funded, claimed, cancelled and settled states separately.

For Sablier-specific Flow/Lockup lifecycle, prefer `galleon-sablier-streams` when installed; for Superfluid CFA/GDA/operator/scheduler work, prefer `galleon-superfluid-streams`. These are optional handoffs, not required sibling files.
