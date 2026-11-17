# Pool assessment

Run gates before ranking. An unknown hard gate is a failed gate for deployment purposes.

## Identity gate

- Chain ID and finality model
- Protocol version and official factory
- Pool address, or v4 PoolId plus full PoolKey
- Token addresses, order, symbols, names, and decimals
- Fee, tick spacing, invariant, hook, NFT manager, gauge, and reward contracts
- Verified bytecode or verified source, proxy implementation, owners, admins, pausers, and upgrade delays

## Token gate

Test both assets for transfer restrictions, taxes, rebases, blacklists, pausing, mint authority, upgradeability, wrapper or bridge dependence, redemption terms, holder concentration, and counterfeit identity. Simulate buy, transfer, approve, add, remove, and sell paths where lawful and possible. A successful buy does not prove a successful sell or liquidity removal.

## Pool gate

- Position model: concentrated NFT, fungible reserve share, gauge receipt, vault claim, or hook-issued share
- Pool age and observation history
- Total liquidity and active liquidity near the current price
- Depth at the user's entry and exit size, not headline TVL
- Executable depth at the current tick rather than a scanner's share of total LP; concentrated positions supply depth only inside their ranges
- Volume by consistent windows, unique flow where available, and wash or self-trade signs
- Fee switches, dynamic fee control, hook permissions, gauge state, reward budget, and epoch end
- Oracle or TWAP availability and manipulation cost
- Liquidity and ownership concentration
- Pauses, incidents, migrations, and prior range or reward discontinuities

If a utility, vault, or keeper is part of the intended route, apply a separate custody and automation gate. Verify beneficial ownership, standing approvals, executable triggers, operator compensation, disable and withdrawal paths, and whether a replacement position preserves configuration.

## Return decomposition

Report each component separately:

1. Swap fees actually earned over a stated window.
2. Incentives at current token price, remaining budget, end time, eligibility, and dilution assumptions.
3. Inventory value relative to the original HOLD quantities at current prices.
4. Entry, rebalancing, claim, exit, conversion, bridge, gas, slippage, MEV, and tax costs.
5. Opportunity cost of the user's chosen benchmark.

A concentrated LP is short path volatility. Narrower ranges increase capital efficiency and gamma exposure. Fee APR is compensation from realized flow; it is not evidence that fees exceed divergence or loss versus rebalancing.

Choose one accounting convention for divergence, LVR, and execution loss. Explain it. Do not subtract overlapping estimates twice.

For Aerodrome and Slipstream, prove whether a position receives fees, emissions, or both. Do not sum mutually exclusive routes.

## Exit gate

Quote the full unwind at the user's size. Verify unstake delays, reward claims, liquidity removal, collect semantics, token taxes, price impact, native wrapping, bridges, approval cleanup, and whether the position remains manageable if a pool leaves the curated list.

## Fee tiers and quote assets

ETH or WETH quote pairs are valid venues; wrapping or a native-input router path is an execution step, not a blocker, and a thin stablecoin pool does not veto a deeper WETH route. Treat a fee tier as a measured cost: two 1% legs lose about 1.99% to pool fees before impact, gas or taxes. Compare size-specific quotes over the viable routes, including multihop through any supported quote asset, and remember those quotes already embed pool fees and impact. An unavailable route is a concrete blocker; a quote symbol, fee tier or protocol version by itself is not.

## Ranking

Remove gate failures first. Rank the remainder on dated evidence:

- executable depth and exit quality
- organic fee pace and persistence
- reward quality and remaining runway
- active-liquidity fit for the intended range
- contract, token, hook, admin, and bridge risk
- operational load and expected action cost

Show raw measures beside any score. Avoid universal weights or fixed thresholds. Use the user's capital, horizon, and loss constraints.
