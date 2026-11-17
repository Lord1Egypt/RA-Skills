---
name: galleon-sablier-streams
description: Use when creating, funding, withdrawing, pausing or cancelling Sablier Flow streams or Lockup vesting, or diagnosing covered versus uncovered stream debt. Resolve product, deployment and current NFT rights before preparing a bounded payment action.
license: MIT
compatibility: Portable instructions for official Sablier contracts, SDK/CLI examples and read-only EVM tools. No signer or provider runtime is included.
metadata:
  author: Andrew Wilkinson and Galleon Labs
  version: "0.2.1"
---

# Sablier stream lifecycle

Turn a stream request into product-specific obligations and an evidence-backed state. Flow debt, Lockup vesting, airdrop allocation and actual recipient cash are different quantities.

## Select model and rights

Resolve chain, deployed product/version, stream or campaign identity, exact token/decimals, sender and current recipient/NFT owner. Read onchain state to corroborate indexed discovery. Use [module procedures and sources](references/modules.md) for official interfaces; names and app aliases cannot establish version or ownership.

Choose Flow for an open-ended rate/debt model; choose Lockup for prefunded linear, dynamic or tranched vesting. A campaign's claim and clawback policy is a separate module; a claimed stream may have its own Lockup rights. Do not convert a pause request into permanent termination.

For creation, resolve deposit, exact rate/schedule, start/end/cliff, cancelability, transferability, withdrawal rights, total approved budget and any fee. Reuse already supplied terms. A past Flow start can create retroactive debt; a future start and `startTime: 0` are different intents. Read-only explanation needs no wallet connection.

## Compute the actual obligation

Flow `ratePerSecond` is UD21x18 whole tokens per second. It does not use the token's decimals as its rate scale. Current Flow only supports tokens with at most 18 decimals. Convert the user's rate with exact arithmetic and explicit rounding; use token decimals for deposit/withdrawal amounts separately. A fixed per-second rate does not exactly implement unequal calendar months. If a rate does not represent exactly, show the represented rate and horizon difference before changing the amount.

Read total, covered and uncovered debt, funded balance, withdrawn amount and withdrawable amount at a recorded time. Debt can accrue beyond the deposit; available cash is not total earned. Show exhaustion time under the current rate/funding and whether debt continues. An open-ended stream needs a bounded mandate or an explicit recurring obligation, rather than an unstated permanent budget.

Lockup schedules are prefunded. Reconcile deposit, vested/streamed, withdrawable, withdrawn and refundable values with current cancelability and NFT rights. Cancellation preserves vested recipient rights while returning eligible unvested funds; renouncing cancellation removes an irreversible right. Do not apply a campaign clawback window to the stream without reading its module.

## Prepare and reconcile

Use the official current builder/ABI. Inspect finite token approval, exact target/value/calldata, stream parameters, sender/current recipient and nested batches. An EOA and contract caller can have different rights. Simulate the exact sender and complete ordered sequence; synthetic funding or permission bypasses leave real prerequisites unresolved. Skills and upstream wallet examples supply no spending authority.

For an authorized write, preserve existing amount/recipient/product limits. Persist hash and exact deployment. After creation, verify successful receipt and emitted stream identity, then read its onchain token, parties, funding, rate/schedule and rights. After withdrawal, verify actual token receipt and new withdrawable/withdrawn amounts. A pause, refund or void needs its own event/state checks.

On timeout, reconcile hash/nonce/current state before retrying. A refund followed by void should be atomic when the approved official operation supports it; otherwise each committed effect must be reconciled. Multi-stream work stays within the requested set, without defaulting to every discovered eligible stream. Current owner changes require refreshed rights and recipient review.

## Deliver

Return exact product/version/chain/stream, parties and current rights, amounts and scales, obligation horizon, covered/uncovered or vested/refundable state, unsigned calls or actual receipts, observation time and next missing fact. A stream created onchain is not all future payments received.

Read [worked calculations and recovery](references/examples.md). Sources reviewed 2026-10-08; no live stream was created or modified by this package. This directory is independently installable.
