# Position accounting

## Baseline

The HOLD benchmark is the original token quantities valued at current prices. Reconstruct originals from creation and subsequent increase, decrease, collect, stake, unstake, and transfer receipts.

If a position is imported without history, report a first-seen reference separately. Do not call it the original HOLD baseline and do not overwrite a later reconstructed baseline.

When a range move creates a replacement position ID, preserve one lineage across the old and new IDs. The withdrawal, swap, and remint are cash flows inside the strategy, not fresh deposits or profit.

## Balance sheet

Classify each attributable unit once:

```text
LP net value
  = current position inventory
  + claimable fees
  + claimable incentives
  + realized proceeds no longer inside the position
  + loose wallet residue attributable to the position
  - gas, slippage, MEV, taxes, and other execution costs
```

Do not count claimed fees both as realized proceeds and loose wallet balances. Do not treat principal withdrawn during a reduction as fee income.

Include balances attributable to the beneficial owner but held in a gauge, vault, or automation contract. Deduct operator and protocol rewards separately. Do not classify contract-held residue as lost or earned until its withdrawal right is verified.

```text
inventory divergence = current position inventory / current HOLD value - 1
net result versus HOLD = LP net value / current HOLD value - 1
```

State price sources, observation times, and denomination. A stablecoin symbol does not guarantee a one-dollar mark.

## Return windows

For each fee or reward APR, state the exact earnings window, average capital denominator, time in range, staking state, and whether rewards were valued at spot or realized prices.

Use simple annualization for reporting unless a reinvestment cadence is observed:

```text
simple APR = window income / average capital * 365 / window days
```

Do not compound a trailing window into APY by assumption. Separate organic fees from token incentives and current claims from projections.

## LVR and divergence

Divergence versus HOLD measures inventory outcome. Loss versus rebalancing describes value transferred to better-informed arbitrage through stale AMM prices. State the chosen model before combining them. Do not subtract overlapping loss estimates twice.
