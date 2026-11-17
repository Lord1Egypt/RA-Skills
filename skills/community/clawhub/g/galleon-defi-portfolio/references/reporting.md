# Reporting and rebalance planning

## Report contract

Lead with what materially changed and what needs attention. Include valuation currency/time, selected accounts/chains, freshness range and known coverage gaps. Then show gross assets, liabilities, priced net equity, unpriced positions, exposure concentration and access constraints. Evidence should make each consequential number traceable to a provider/account/block or a stated calculation.

State the denominator for allocations. Net-equity weights can exceed 100% under leverage; negative equity can make those weights misleading. Show gross asset and gross exposure views when needed. Separate token exposure from shared failure domains such as a bridge, staking operator, vault manager, lending market, stablecoin issuer or collateral oracle. Two differently branded tokens can share the same underlying exposure.

A useful attention list is concrete: collateral/debt changed, stale position data, excessive concentration against the user's chosen limit, withdrawal queue delay, unsupported chain, missing cost basis or mismatched source totals. Do not invent urgency or recommend a trade solely from an arbitrary score.

## Proposed rebalance

Start from the user's target, horizon and constraints: account scope, permitted chains/venues/assets, minimum liquidity, debt limits, cost budget and allowable slippage. If those limits materially determine the plan, ask for the missing information while completing independent reporting.

Present target changes and the dependency order. Repaying debt or releasing collateral can precede a withdrawal; unstaking or vault redemption can involve a queue; a bridge can leave funds temporarily unavailable. Reserve native gas and account for approvals, route fees, price impact, taxes or realization consequences where relevant. Treat these as estimates with missing assumptions, not personalized tax conclusions.

For each proposed operation, state the input ceiling, expected/minimum output, recipient, chain, quote age/deadline, dependencies and unresolved approvals. Compare estimated benefits and costs to leaving the portfolio unchanged. Do not execute from a spreadsheet target or report. A later authorized execution workflow must obtain fresh quotes/state and review exact payloads.

## Candidate sizing

For a new position, size from explicit inputs: reconciled NAV across every included chain, deployable cash after reservations, pending routes and a retained native gas reserve, executable price, reported liquidity, fractional stop distance and total estimated round-trip costs. The candidate notional is the nonnegative minimum of `(NAV * risk fraction - estimated costs) / stop distance`, `NAV * allocation cap`, `cash - estimated costs - gas reserve` and `reported liquidity * participation share`. When costs consume the risk budget the answer is no trade. Holdings on another chain count as deployable only net of a quoted bridge cost and both chains' gas. These are calculator defaults rather than enforced limits, a stop may not execute and quoted liquidity may not be reachable, so obtain a size-specific quote before committing.

## Recurring reports

When explicitly requested, use the host's existing scheduler and a private, access-scoped snapshot store. Save the report scope and methodology with each snapshot so comparisons remain meaningful. Separate a missed refresh from a zero balance, and announce coverage changes before computing period performance. Define the user's delivery destination and cadence; installation alone does not authorize sending reports or creating monitors.

When more than one process can act on the same accounts, such as a chat session and a scheduled run, coordinate through one cooperative lease per execution resource and one shared journal. A lease is coordination, not custody enforcement; reconcile pending operations before continuing after a crash or a lease takeover.
