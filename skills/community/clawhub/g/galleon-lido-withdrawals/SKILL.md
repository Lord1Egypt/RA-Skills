---
name: galleon-lido-withdrawals
description: "Use when requesting or claiming Lido stETH or wstETH withdrawals, reconciling unstETH NFTs, or comparing the native queue with a secondary-market exit."
license: MIT
compatibility: "Read-only EVM RPC or official provider tools; Bun is optional for offline examples. No signer required."
metadata:
  version: "0.2.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Lido withdrawal queue

Deliver a request/claim ledger for the **Lido Ethereum stETH WithdrawalQueueERC721**. This is not the stVault DeFi wrapper queue. Identify chain, official queue address, token, amount and request owner. If the asset is wstETH on an L2, first establish its documented redemption route; do not pretend the Ethereum queue exists on that chain.

## Request or swap decision

Read queue pause/bunker state and current minimum/maximum request size; never bake those limits or an ETA into a recommendation. For wstETH, distinguish wrapped units from their current stETH equivalent. Compare a same-size executable secondary-market quote with the queue path: net ETH after gas, price impact, waiting period, and slashing exposure. A quote is not a completed exit; an estimated queue duration is not a deadline guarantee.

For the queue, the request transaction locks the submitted stake and produces an unstETH NFT. It does not transfer ETH to the user. Explain the request and claim stages, including the lack of continued staking rewards on queued amounts. Prepare token-specific approval/permit and `requestWithdrawals` or `requestWithdrawalsWstETH` using the verified ABI. Split large requests only within the queue limits and the user's total authorized amount; record every resulting request ID from the receipt.

## Reconcile existing requests

1. Read `getWithdrawalRequests(owner)` for discovery, then `getWithdrawalStatus(ids)` for the known IDs and `ownerOf(id)` for unclaimed NFTs. Current NFT ownership controls the claim; original requester and current owner can differ.
2. Classify each ID as pending, finalized-unclaimed, or claimed. A transfer is not a second withdrawal and a finalized request is not yet ETH in the wallet. A burned claimed NFT may make `ownerOf` revert; reconcile against status and receipt rather than calling it lost.
3. For finalized-unclaimed IDs, obtain checkpoint hints with `findCheckpointHints(ids, 1, getLastCheckpointIndex())`, using IDs in the ordering required by the deployed interface. If there are no checkpoints, do not pass an invalid range. Query `getClaimableEther(ids, hints)`; do not assume the originally requested stETH equals claimable ETH.
4. Prepare the documented claim function for the actual owner/caller and recipient. Recompute hints if state or request list changes. Simulate the claim and separately check the recipient can receive ETH.
5. After a confirmed claim, reconcile request status, NFT burn and ETH receipt/net balance delta adjusted for gas. A claim hash alone is not completion. Never request a duplicate withdrawal to repair a pending claim.

Return one row per request ID with owner, requested amount, finalized/claimed flags, claimable ETH, observation block and next action. Keep secondary-market swaps and queue claims separate in the record.

## Evidence and completion

Return the requested decision, exact deployment and chain, block/time, raw-unit observations, calculation assumptions, and the next missing read. Distinguish an indexed estimate, an onchain read, a simulated call and a confirmed transaction. Research ends with an actionable decision record; it does not require connecting a wallet.

For a requested write, prepare the complete unsigned sequence and simulate with the actual sender, amount, recipient and allowance state. Preserve authorization already supplied; research does not grant debt, spending or signing authority. Never request keys. After an authorized transaction, verify its receipt and the relevant balance or position change. On an ambiguous timeout, reconcile its hash and nonce before retrying.

Read [protocol references and worked record](references/recipe.md) only for the selected operation. Documentation checked 2026-09-27; refresh deployments and current parameters at use time. This directory is independently installable.
