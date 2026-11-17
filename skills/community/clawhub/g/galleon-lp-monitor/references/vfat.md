# Monitoring VFAT/Sickle positions

Reconstruct an existing position independently of the VFAT dashboard. Reviewed 2026-09-05.

## Ownership and accounting

Bind the user's account, chain, Sickle, Sickle owner, approved operator, strategy, gauge, underlying pool and current LP/NFT identity. If a wrapper owns the Sickle, trace its end-user rights and reward router separately. Do not use the user's EOA balance alone to conclude the position is missing.

Include active inventory, staked assets, owed rewards, claimed proceeds, Sickle residue and wallet dust exactly once. Reconcile withdrawals and reward transfers from receipts. A dashboard's APR is not realized P&L; retain the original cash-flow baseline and account for service fees on the correct reward or principal basis.

## Automation evidence

Read both the approved automation account and the per-position harvest, compound, rebalance and exit settings. Compare current settings, fee recipients and registry permissions with the last verified state. A frontend toggle or old transaction receipt does not prove the current permission.

The [documented rebalance policy](https://docs.vfat.io/automation/rebalance/) can preserve settings on a replacement NFT. Follow the old-to-new position transition and reread the settings; otherwise a monitor can miss ongoing automation or double-count both identities. Inspect returned dust in the user's wallet and any residual funds in the Sickle.

The automatic-rebalance stop-loss stops rebalancing; it does not exit. Report the remaining inventory and exposure when that bound is reached. Treat a separately configured automatic exit as a different capability with its own live settings and execution evidence. Do not promise a fill from a displayed trigger.

If a keeper is inactive, fees cannot cover its costs, quote limits fail, or data is stale, distinguish delayed automation from a completed action. A confirmed failure can require a rebuilt plan; an ambiguous broadcast must not be resent. A manual rebalance may race active automation and requires a current conflict check.

## Result and fallback

Return position/ownership evidence, balances, net performance or missing baseline, automation state, cost/risk changes and a recommendation. If the interface or farm listing disappears, use verified deployed contracts and read tools to assess withdrawal or sweep options. A source function's existence does not prove a live usable exit. Do not sign, toggle automation, harvest or rebalance during monitoring.
