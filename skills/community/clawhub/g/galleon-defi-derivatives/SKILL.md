---
name: galleon-defi-derivatives
description: Assess perpetuals, options and funding-rate derivatives, prepare bounded exposure plans, and reconcile order and margin state. Use when comparing GMX, Drift, Derive, Jupiter Perps or Boros, planning hedges, monitoring positions or recovering orders.
license: MIT
compatibility: Portable Agent Skills instructions. Live work needs official venue data and optional user-authorized wallet tooling. No signer, provider or runtime is installed by this skill.
metadata:
  author: Galleon Labs
  version: "0.1.5"
---

# DeFi derivatives

Translate a market or hedge request into explicit exposure, collateral requirements and venue-specific order evidence. Reuse official tooling; keep research, planning and authorized execution distinct.

## Start with the requested task

Read [task examples and user configuration](references/task-examples.md) for a completed example and recovery path. Apply only the workflow stages needed by the current request. Reuse supplied preferences and compatible tools; ask only for missing terms that affect this task. Public explanation or comparison does not require transaction fields. Keep any existing authorization within its exact scope.

## Select the product and tools

Read [providers](references/providers.md) for GMX, Drift, Derive, Jupiter and Boros, their official integration surfaces and version gaps. Read [workflows](references/workflows.md) for risk planning and order reconciliation. [Evaluation cases](references/evaluation.md) provide bounded fixture scenarios.

For Hyperliquid, use the installed `hyperliquid-analyze`, `hyperliquid-plan`, `hyperliquid-execute` or `hyperliquid-monitor` skill when available. This pack provides the cross-venue comparison and handoff; it does not reproduce Hyperliquid signing or nonce rules. No other pack is required for the general workflow here.

## Define the exposure

Identify network, protocol version, exact instrument/market, expiry, payoff denomination, collateral, margin mode, owner, subaccount and signer role. An ETH perpetual, an ETH option and an ETH funding-rate contract are different exposures. Do not normalize them into a single token price or label annualized funding as guaranteed yield.

Obtain fresh oracle/mark/index prices, order book or available capacity, current positions and orders, balances, margin requirements and accrued funding/borrow costs. State the observation time and source. Missing account data prevents a personalized risk or execution-ready claim; public market analysis can still proceed.

## Build a bounded plan

Use the user's existing risk budget and approved terms. Specify size in both native venue units and economic notional, side, order type, limit/acceptable price, maximum slippage, collateral change, leverage/margin mode, expiry, reduce-only intent, fee recipients and maximum costs. Stress adverse price, funding, volatility and exit liquidity; calculate combined exposure across existing orders and positions, not just the new order. A stop order may trigger without filling.

For options include premium, contract multiplier, settlement asset, exercise/expiry model and uncovered short liability. For funding-rate hedges include settlement period, rate convention, maturity, collateral and basis mismatch against the exposure being hedged. A hedge across venues creates separate liquidation and settlement risks.

## Authorize and reconcile

Use the official builder within the user's established execution boundary. A delegated key with limited withdrawals can still lose trading collateral. Granting or renewing delegation, changing margin mode, depositing and withdrawing are distinct financial actions; none is incidental setup. Never handle a key, create an agent wallet, insert a fee recipient or authorize a trade from this skill's presence.

Before manual changes to a managed account, read [account control](references/account-control.md) to reconcile active bots, open orders and an authorized handoff.

Follow [the venue lifecycle](references/workflows.md): persist operation identity; separate prepared, submitted, created/resting, partially filled, executed, cancelled and unknown states; reconcile authoritative fills and account changes. Resolve unknown outcomes before retries. A keeper-created order, relayer acceptance or successful transport response is not a completed trade. Cancel and replace can race with fills; reread both before calculating remaining size.

## Deliver

Return the market answer, comparison or proposed ticket with exact instrument and account identity, exposure, downside constraints, costs, source times, supported capabilities and material gaps. For monitoring, report position/order/margin changes with trigger conditions and a bounded next action. Creating a schedule, starting continuous trading or changing an existing automation requires the user's actual request; the skill does not start a background service.
