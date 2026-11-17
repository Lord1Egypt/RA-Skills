# Automation and custody

An automation product changes position authority, execution risk, and accounting. Assess the exact route, not its marketing label.

## Classify control

Record:

- NFT or LP-token owner and beneficial owner
- per-token approval, operator approval, gauge deposit, vault custody, or direct ownership
- contracts and accounts allowed to act
- actions each actor can perform
- pause, disable, withdrawal, migration, and emergency paths
- upgrade authority, code verification, and keeper availability

A stateless utility that receives and returns an NFT in one transaction is different from a vault that retains custody. An ownerless contract is not safe merely because it lacks an admin.

## Bind automation policy

For auto-exit, auto-range, or auto-compound rules, record:

- trigger direction and exact tick or price orientation
- range offsets and tick-spacing alignment
- swap direction, maximum input, minimum output, and price guard
- TWAP window, maximum spot-to-TWAP deviation, and behavior when observations are unavailable
- operator reward basis and cap
- whether rewards can consume fees only or principal
- whether configuration follows a replacement position ID

Verify configuration onchain. A dashboard toggle is not authority.

## Conflict gate

Before recommending or planning a manual action, check every contract that can move, transform, stake, or withdraw the position. Active automation can race a manual transaction or invalidate its quote, nonce, owner, range, or position ID.

Return `blocked` when an active configuration must be disabled first, the disable path cannot be verified, or beneficial ownership cannot be proven.

## Economic gate

Count operator fees, automation fees, gas, swap cost, residual balances, approval exposure, and tax effects. Auto-compounding is justified only when expected incremental return clears those costs over the intended holding period.

Prefer per-token NFT approval for a one-off action. Treat `setApprovalForAll` as standing authority over every current and future position in that manager.
