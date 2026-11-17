# Atomic position actions

An atomic utility may receive an NFT or tokens, perform swaps and liquidity actions, then return an original or replacement NFT plus leftovers in one transaction.

## Preflight

Verify the utility's deployed code, immutables, position manager, swap router, owner or upgrade controls, supported pool type, and audits. Inspect active vault, gauge, and automation state first. Stop if another actor can move the position or the utility cannot preserve its custody state.

For an NFT action, prefer approval of the exact token ID. Do not create `setApprovalForAll` unless the user explicitly accepts standing authority and no narrower supported path exists.

## Decode the complete action

Verify:

- the NFT transfer receiver and encoded callback instruction
- action selector and old position ID
- full withdrawal and collect limits
- swap input, allowance target, router, path, minimum outputs, and deadline
- new pool identity, range, fee, minimum amounts, and NFT recipient
- token, native-currency, and NFT refund recipients
- operator reward and whether it can consume fees or principal
- approval cleanup and expected loose balances

Reject arbitrary swap targets, a router-controlled recipient, a combined-value floor that leaves one mint leg unprotected, or a utility that can retain funds without an attributable withdrawal path.

## Phase separation

If approval is missing, confirm and submit only the finite approval. After its receipt, reread owner, operator, allowance, pool, quote, nonce, and automation state. Build and simulate a new action transaction. The approval-phase plan is not executable action authority.

## Reconcile

After the action receipt, verify:

- original and replacement NFT IDs
- owner and beneficial owner
- old and new liquidity
- collected fees and swapped amounts
- range and current status
- gauge, vault, and automation configuration
- returned leftovers and residual approvals

Do not report a moved range as complete if the old position changed but the replacement position or refund cannot be proven.
