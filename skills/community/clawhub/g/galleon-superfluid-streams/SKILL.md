---
name: galleon-superfluid-streams
description: Use when preparing, adjusting, stopping or reconciling Superfluid CFA streams, GDA distribution pools, Super Token wrapping, or stream and vesting scheduler operations. Inspect real-time funding and flow-operator rights before committing a recurring obligation.
license: MIT
compatibility: Portable instructions for official Superfluid contracts, @sfpro/sdk, metadata and existing read-only EVM tools. No signer or adapter runtime is included.
metadata:
  author: Andrew Wilkinson and Galleon Labs
  version: "0.2.1"
---

# Superfluid flows and distribution

Produce a funded, permission-aware flow plan and verify its resulting state. A created flow is a recurring transfer rate; it is not proof that a whole future subscription has been paid.

## Resolve token and agreement

Read chain, deployment, Host/forwarder, exact Super Token and underlying relationship, decimals, sender, receiver or GDA pool, and actual caller/operator. Use [current SDK and agreement references](references/operations.md); new integrations use `@sfpro/sdk` rather than archived SDKs. Names and symbols cannot identify a wrapper or agreement.

Choose CFA for one-to-one rates and GDA for pool distribution. A pool's units and connected member claims differ from a fixed per-recipient stream. Schedulers, AutoWrap and macros add separately configured authority and automation. Load only the selected track; an old IDA example does not establish current GDA semantics.

Read the current exact flow/aggregate net rate, real-time available balance, locked deposit/buffer, underlying wallet balance and operator permissions at a recorded block/time. Indexed balances can lag time-dependent settlement. An incoming flow may stop; evaluate funding with and without that dependency.

## Bound the recurring commitment

Resolve user rate, unit/time period, proposed end or monitoring obligation, maximum economic budget, acceptable funding horizon, wrapping amount and current approval limits. Convert human rates using exact token decimals and seconds with explicit rounding. Monthly billing needs a defined calendar/fixed-period interpretation; never assume every month is 30 days.

Calculate projected exhaustion from spendable real-time funding and aggregate outgoing obligations. Do not spend the liquidation/deposit buffer twice or subtract it twice from a balance already reported as available. Use actual contract read semantics, current required buffer and conservative incoming assumptions. Show missing buffer/rate reads rather than inferring a deadline from an ERC20 `balanceOf` snapshot.

Inspect old and proposed operator permissions: permitted create/update/delete operations, token/sender scope, rate allowance, caller and expiry if the chosen permission layer supports it. A CFA operator permission is different from ERC20 allowance and smart-wallet session limits. A unlimited flow allowance or automatic replenishment can outlive the user's one-time budget.

## Prepare and verify the complete action

Use imported official ABI/address metadata for the selected chain and current SDK. Inspect wrapping, finite ERC20 approval, operator/session updates and flow calls as separate rights/effects. Clear-signing macros still need every nested action, EIP-712 domain, spender and economic limit reviewed. Readable text alone cannot establish all batch effects.

Simulate using the actual caller/Host context and prerequisite state. A future scheduler needs its current execution policy and permissions; creating the schedule does not prove a keeper executed its boundary. AutoWrap requires its own underlying funding/allowance and automation terms. Never assume an end timestamp guarantees the flow stops without available execution.

For an authorized write, preserve exact user terms and existing authority. Verify receipt/events and fresh flow rate, sender/receiver, real-time balance, deposit, operator permissions or pool units. A stopped stream still leaves prior balance movements. On timeout, reconcile hash/nonce/current flow before creating or updating again.

## Deliver

Return chain/token/agreement/parties, exact rate and scale, current/proposed net rate, spendable funding/buffer, conservative horizon, rights and scheduler dependencies, complete unsigned calls or confirmed receipts, observation time and remaining gap. Separate earned/accrued amounts from withdrawals/claims and future commitments.

Read [worked funding and failure records](references/examples.md). Primary sources reviewed 2026-10-08; no real flow, pool or schedule was changed by this package. This skill is independently installable.
