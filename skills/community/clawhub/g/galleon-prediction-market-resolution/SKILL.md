---
name: galleon-prediction-market-resolution
description: Use when explaining a Polymarket outcome, disputed resolution, payout eligibility or whether an existing redemption actually reached a wallet.
license: MIT
compatibility: Official public market data and read-only chain/explorer access. No signer or funded wallet required.
metadata:
  author: Galleon Labs
  version: "0.1.1"
---

# Reconcile prediction resolution

Separate the event outcome, oracle decision, recorded payout, redemption and received collateral. A closed market or displayed winning outcome is insufficient evidence of payment.

## Decision loop

1. Resolve market ID, condition ID, version, outcome identifier and owner address. Confirm CTF `v1` versus PositionManager `v2`, chain, deployed ledger, collateral and proxy/funder ownership. Field presence alone is not a reliable version discriminator. Use [the official ledger references](references/settlement.md).
2. Read the complete rules and resolution source. For UMA, distinguish proposed, challenged, escalated and finalized. Resolve the actual request and bond/challenge parameters from current state. For Chainlink TWAP, compare the specified feed and lookback at the start/end; do not substitute a spot or unrelated oracle price. Recheck additional context and ties.
3. Verify finalized payout on the correct ledger at a recorded block. For CTF, read denominator and outcome numerators; zero denominator means unresolved. For V2, use current PositionManager resolution/payout reads and version-specific events. Do not transplant CTF reads to V2 or infer full payout from a binary label. Split payouts can exist; negative-risk rules differ.
4. Read the holder's canonical balance and any pending redemption state. Calculate entitlement from the verified outcome fraction and actual holdings, identifying fee/rounding/collateral units. A claimable amount is not received collateral; do not double-count a redeemed token and its released backing.
5. If a redemption hash or receipt was supplied, verify chain, success, canonical block/finality, ledger burn and collateral recipient/balance change. Automated redemption may exist: reconcile it before suggesting any new action. Index ERC-1155 transfers once, using lifecycle events as context rather than another balance change.
6. Report resolved/unresolved/disputed, payout fraction, claimable/paid/unknown and evidence identifiers. If submission timed out, track the existing hash and owner state before recommending retry. Do not propose/dispute outcomes, sign messages, call redeem, or perform money movement during this research procedure.

## Worked decision

A market is closed and Yes displays 1.00, but the oracle has a disputed proposal and no finalized denominator. Report unresolved/disputed, with no verified claimable or received payout. In a separate finalized 50/50 market, 20 Yes shares give a gross entitlement of 10 collateral units before contract-specific rounding. A later successful redemption receipt still needs the actual recipient's collateral delta before describing it as paid.

## Completion

Provide the versioned identity, oracle stage, recorded payout, owner balance, existing redemption identifiers, terminal receipt/balance evidence or a precise missing read. Never convert an API flag, proposal or request acceptance into proof of settlement.
