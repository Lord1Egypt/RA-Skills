# Market risk

## Price and liquidation

Name the three prices separately:

- Oracle price anchors funding.
- Mark price drives margin, liquidation, TP/SL triggers, and unrealized PnL.
- Executable book prices determine fills and slippage.

Measure divergence among them and explain what would close or widen it. A stop at a trigger price is not a guaranteed fill at that price.

Read the applicable margin table at the proposed notional. Larger positions can move into a lower-leverage tier. Liquidation distance from a current account is more useful than headline maximum leverage.

Map the waterfall: book liquidation, partial-liquidation rules, backstop liquidator, and auto-deleveraging. Verify current mechanics in official docs for the product and account mode.

## Funding and carry

Decompose carry into:

1. Funding received or paid, with its interval and observed window.
2. Spot borrow or supply interest under portfolio margin.
3. Trading fees, spread, impact, and rebalancing costs.
4. Basis drift between the hedge legs.
5. Liquidation, oracle, venue, account-mode, and exit risk.

Annualized spot funding is a comparison aid, not a forecast. Show trailing distributions, sign changes, stress periods, and the cost if funding reverses.

## Liquidity and crowding

Compare intended size with executable book depth, not volume alone. Review open interest versus depth, concentrated positioning, liquidation clusters where observable, and whether exits depend on the same side of the book.

For market making, separate quoted spread and rebates from adverse selection, inventory drift, cancels, queue position, stale quotes, and dead-man-switch behavior.

## Product and DEX class

- Validator-operated perps inherit the protocol's oracle, margin, and liquidation rules.
- HIP-3 markets also inherit the DEX deployer, its collateral choice, oracle operation, margin mode, liquidity, growth settings, and backstop configuration. Assess each DEX separately.
- Spot has balance and execution risk but no perp liquidation. Portfolio margin can make spot collateral part of a liquidation path.
- Index perps and other non-spot references require a clear index methodology, update cadence, market-hours policy, and delisting path.

## Account abstraction

Standard, unified, and portfolio-margin accounts are different balance sheets. Portfolio margin adds borrow and supply rates, collateral LTVs, caps, fallback behavior, and a combined liquidation model. Query the current mode and current parameters. Do not apply a standard cross-margin calculation to another mode.

## Verdict gates

Reject or mark unassessable when market identity is unresolved, the book cannot cover the proposed exit inside the stated impact bound, current margin rules are unavailable, the oracle or index method is unclear, the strategy depends on an unstated funding regime, or the evidence window is too short for the claim.
