# Planning a VFAT/Sickle route

Use this only when the user chooses VFAT as the route for an already assessed pool. Keep direct protocol and other suitable official-tool alternatives available. Reviewed 2026-09-05.

## Route and authority

Bind chain, wallet, Sickle address and owner, any approved operator, factory, registry, strategy, connector, gauge, pool and output recipient. For a new account, show Sickle creation as an explicit plan effect. A wrapper that owns the Sickle and redirects rewards is a separate custody/fee choice; do not insert it to make an SDK example work.

Decompose any one-click route into approvals, input swaps, liquidity addition/removal, staking, reward processing and residue transfers. Show the input token, integer maximum spend, minimum outputs, slippage/price-impact guards, native value, approval scope, deadline and each target. UI convenience does not imply one signature, no approvals or one trust domain. Keep the draft non-executable if exact calls or independent simulation are missing.

## Charge the correct fee basis

Read [current VFAT fees](https://docs.vfat.io/fees/) and reconcile the selected strategy's onchain fee configuration. The reviewed documentation separates swap-based entry/exit charges, reward-based harvest/compound charges, and position-based rebalance charges. Manual and automated actions have different rates. Token/LP-token/NFT withdrawal routes can have different service fees from conversion into a single output token. Do not hardcode the documentation's rates as lasting protocol constants.

An automatic rebalance can incur both a position-based rebalance charge and a separate reward-processing charge. Verify both current rates and bases; do not model the rebalance charge alone as its total service cost.

Record each fee recipient, basis, rate, expected integer amount and whether quoted amounts already include it. Include aggregation, swap, protocol and network costs without double-counting gas that the disclosed automation fee already covers. Model compounding against leaving rewards uninvested; a service's scheduling model is not evidence that every compound is economical for this position.

## Automation is an additional decision

Record the chain-level approved automation account and each position's action settings separately. Verify manual-action conflicts and disable/revoke paths before planning a competing action. The [compound](https://docs.vfat.io/automation/compound/) and [harvest](https://docs.vfat.io/automation/harvest/) guides describe mutually exclusive reward modes; do not enable both as independent yield sources.

For [automatic rebalance](https://docs.vfat.io/automation/rebalance/), distinguish relative buffer/range settings from fixed price bounds. The documented stop-loss suspends rebalancing; it does not liquidate or withdraw. A separate exit configuration must specify trigger, output asset, recipients, limits and authority, and be independently verified. Settings copied to a replacement NFT must be checked after the remint; do not assume a new position is unautomated.

Return an unsigned plan with all costs, ownership effects, permission changes, expected residue and recovery steps. Missing live fee, custody, quote or simulation evidence blocks execution, while public comparison can continue.
