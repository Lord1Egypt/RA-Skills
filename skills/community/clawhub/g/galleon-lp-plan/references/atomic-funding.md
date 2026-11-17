# Atomic funding and transformations

A reviewed utility may combine swaps with minting, increasing, compounding, exiting, or moving a range. Atomicity can remove intermediate price and custody risk, but it concentrates more authority in one call.

## Choose the route

Consider an atomic route when the user has:

- both pool tokens in the wrong ratio
- one pool token
- one unrelated funding token
- an existing position whose range must move
- claimable fees that should be compounded
- an exit that should settle into one chosen token

Do not require a separate pre-swap when a verified utility can perform only the required balancing swap inside the position action. Do not force an atomic route when its target, nested calls, or failure behavior cannot be decoded and simulated.

## Bind every leg

Record:

- utility deployment, runtime code hash, owner or upgrade status, and supported manager
- input token, exact maximum input, pool tokens, token order, and native value
- each swap target, allowance target, path, quoted amount, minimum output, quote time, and expiry
- position recipient, NFT recipient, refund recipient, and leftover-token policy
- range, fee, tick spacing, minimum token amounts, and minimum liquidity
- old position ID, expected new position ID event, custody state, and post-action approvals

For third-token funding, model each output leg independently. A minimum on the combined value does not protect either required pool token.

## Freshness and phases

Short-lived quotes can expire while a wallet prompt is open. Record the signing cutoff. Rebuild the complete transaction after expiry; immutable calldata cannot be refreshed.

Return either the finite approvals needed for the action or one complete action transaction. Do not present both as simultaneously ready. After approval receipts, reread allowances and rebuild the action from current pool state.

## Range moves

Treat a range move as an identity transition. Reconcile the old position, replacement position, ownership, liquidity, fee collection, swap amounts, leftovers, and any automation or gauge configuration that should move. Never assume a new NFT inherited approvals, staking, accounting history, or automation state.
