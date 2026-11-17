# ERC4626 read recipe and worked exit

With verified `VAULT`, `OWNER`, `RPC_URL`, numeric `BLOCK` and raw requested `SHARES`:

```sh
cast call "$VAULT" 'asset()(address)' --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$VAULT" 'maxWithdraw(address)(uint256)' "$OWNER" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$VAULT" 'maxRedeem(address)(uint256)' "$OWNER" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$VAULT" 'previewRedeem(uint256)(uint256)' "$SHARES" --rpc-url "$RPC_URL" --block "$BLOCK"
```

For asynchronous vaults, inspect the implementation and ERC7540 support before choosing request/claim reads. Unsupported synchronous previews are not evidence of zero share value. For an ERC7540 redeem implementation, read `pendingRedeemRequest(requestId, controller)` and `claimableRedeemRequest(requestId, controller)`. Preparation uses `requestRedeem(shares, controller, owner)`; the eventual claim uses `redeem` or `withdraw` with the controller role, not an invented universal `claim()` method. Request ID zero aggregates requests by controller.

## Synthetic worked record

Owner has 1,000 shares. `convertToAssets(1000)` gives 1,100 asset units, `previewRedeem(1000)` gives 1,089, and `maxRedeem(owner)` is 400. A 1,000-share redemption is blocked despite a valid preview. Request a fresh preview for 400 shares; do not multiply the 1,000-share preview by 0.4 because fees can be nonlinear. If the actual 400-share preview returns 435.6, that is the observed partial-exit estimate. The remaining 600 shares retain exposure to the vault and its exit restrictions.

For a request to receive exactly 500 assets with `maxWithdraw=435.6`, report that the requested amount exceeds the current limit by 64.4. Ask only for a decision about a partial exit if no such authorization exists; a read-only report can already return both numbers.

## Primary sources checked 2026-09-27

- [ERC4626 standard](https://eips.ethereum.org/EIPS/eip-4626): limits, previews, rounding and exit methods.
- [OpenZeppelin ERC4626 implementation guidance](https://docs.openzeppelin.com/contracts/5.x/erc4626): conversion and implementation risks.
- [ERC7540 asynchronous vaults](https://eips.ethereum.org/EIPS/eip-7540): request/claim lifecycle.

