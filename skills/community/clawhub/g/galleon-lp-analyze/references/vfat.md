# VFAT yield screening

Use [VFAT Yield](https://vfat.io/yield) to discover candidates and compare displayed measures; it is not the authority for pool identity, executable returns, or permission to deposit. Reviewed 2026-09-05.

## Make the comparison reproducible

Capture the view, filters, sort order, chain, protocol, pool and gauge identities, observation time and units. Inspect the row details and official pool links. Never match by ticker alone. VFAT's live page exposes multiple protocols; the yield guide's original two-protocol launch description is historical, not current coverage.

Distinguish total pool TVL, farm/staked TVL, rewarded TVL and active TVL. They describe different capital populations. A concentrated position's range and reward eligibility may differ from the displayed averages. Do not use Avg APR and Avg Range as an executable estimate for the user's proposed range. Missing tooltip definitions, windows or denominators remain explicit data gaps.

## Decompose the yield

The [APR guide](https://docs.vfat.io/aprs/) describes fee APR using the previous seven days of fees against current pool capital, while reward APR derives from emissions. Treat the former as a trailing estimate and the latter as a changing incentive projection. Verify the current epoch, remaining budget, token valuation, reward eligibility and the user's denominator; neither includes a guarantee of net return.

For Aerodrome/Slipstream, establish whether the exact staked position receives fees, emissions or both. Subtract route-specific VFAT fees, swaps, gas and maintenance costs once, and compare against HOLD. Higher displayed reward APR cannot repair weak token, custody, dilution or exit evidence.

## Assess the selected route separately

A public screen does not require Sickle adoption. If the user considers a VFAT deposit, inspect its account, strategy, registry permissions, automation and withdrawal path as a separate layer over pool risk. Disclose current [fees](https://docs.vfat.io/fees/) and compare the direct protocol route on the same basis. Do not label a source-code fee cap as the actual charge.

Do not recommend rebalancing solely because a position is out of range. Establish its objective, inventory, expected fee opportunity and cost. The documented automatic-rebalance stop-loss suspends rebalancing; it does not sell the assets. A distinct exit feature requires separate verification.

## Deliver

Return a sourced shortlist with raw fields, definition/window gaps, chain verification, net-return assumptions, hard-gate failures and the next read needed. A failed UI fetch or hidden row is unavailable evidence, not zero TVL or zero rewards.
