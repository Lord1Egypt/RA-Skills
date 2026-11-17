---
name: FarmDash Hedge Warden
description: "Use when sizing a hedge for existing DeFi exposure: delta-neutral recommendations with explicit bounds and risk notes. Advisory only; never trades itself."
tags: ["defi","delta-hedging","defi-hedging","crypto-hedging","portfolio-hedge","portfolio-protection","drawdown-protection","perpetual-futures","short-perp","delta-neutral","basis-risk","funding-cost","residual-delta","risk-management","defi-risk-management","openclaw","ai-agent","mcp","web3","farmdash"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one/agents
version: "1.1.2"
icon: hedge
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token for Pioneer or Syndicate tier."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-hedge-warden","primaryEnv":"FARMDASH_API_KEY","execution":"read-only-hedge-plan"}}
---

# FarmDash Hedge Warden

## Futures Execution Mode Contract

- **USER_SIGNED** requires fresh human approval for every order/cancel and a local Hyperliquid EIP-712 venue signature through Futures Strategist.
- **BOUNDED_AUTONOMOUS** may run without per-order human confirmation only under a valid owner-signed futures grant, current API-wallet venue authority, and all session, binding, scope, policy, risk, budget, builder and replay checks. Every venue action still needs a local signature.
- Read futures bounded readiness in the generated canonical table and live status. Bounded hedges may not be automatically executed while a runtime gate is closed. Spot grants, generic session policy, paid access and a hedge recommendation never create futures authority.
- Discover through `POST /api/v1/agent/authority`, `action: get_futures_authority`, `sessionId`, `sessionToken`; revoke the actual grant using `action: revoke_futures_policy`, `grantId`, `sessionId`, `sessionToken`. These are authority REST actions, not new Hedge Warden tools. Hand the selected `executionMode`, `grantId`, `sessionId`, `sessionToken` and reviewed hedge plan to Futures Strategist.
- Scopes are `futures.open`, `futures.reduce`, `futures.close`, `futures.cancel`, `futures.protective_order`. Opening a short hedge increases absolute perp exposure and is new risk, even if portfolio delta falls. Authoritative position state and exact signed semantics must prove reduction. Proven reducing/cancel/protective actions may survive exhausted new-risk capacity: a budget exception, never an authority bypass. Grant, venue delegation, identity/session, allowlists, expiry/revocation, local signature, builder and replay checks still apply.
- Futures Strategist signs venue actions locally; Hedge Warden plans and never signs/submits. Orchestrators never own keys. Research/accounting skills remain nonsigners. Risk/loss limits are admission checks, not guaranteed loss ceilings, profit or positive expected-value promises. Reconcile fills/residual delta and held ambiguous liabilities before dependent legs; never blind-retry.

> Use this skill when protecting spot exposure: sizing a delta hedge before volatility, funding, or basis risk eats the yield.

Hedge Warden helps an agent avoid confusing "earning yield" with "being long beta." It converts spot farming positions into hedge targets, then hands execution research to Futures Strategist.

It never signs or submits perp orders.

## ClawHub Attribution

This skill's canonical ClawHub slug is `farmdash-hedge-warden`. On every FarmDash API request (REST, OpenAPI, or MCP transport where headers are supported), send `X-ClawHub-Skill: farmdash-hedge-warden`. Analytics-only and optional; requests without it still work. The value is always exactly the skill slug, never a wallet address, API key, or user ID.

## Tool

### `recommend_delta_hedge`

Inputs:

- `spotExposure`: array of `{ asset, notionalUsd, beta?, confidence? }`.
- `riskPreference`: `conservative`, `balanced`, or `aggressive`.
- `volatilityRegime`: `low`, `normal`, or `high`.
- `marketConditions`: optional external context from the agent.

Outputs:

- total spot notional.
- recommended hedge notional.
- per-asset short hedge legs.
- handoff instructions for Futures Strategist.
- invalidation rules.
- `dataQuality`, `requiresExposureReview`, `executionEligible`, and residual exposure for each leg.

Sizing formula: `spotNotionalUsd × beta × targetHedgeRatio`. Confidence never reduces the hedge notional. A confidence value below 0.60 blocks the execution handoff until the asset mapping, delta, and notional are independently verified; uncertainty is not permission to under-hedge.

## Agent Rules

### Hedge Pre-Trade Profit Checklist (Additive)
Before handoff, record: total spot notional, per-asset beta, targetHedgeRatio, sizing formula spotNotional x beta x targetHedgeRatio, expected funding plus execution drag over the stated hedge horizon, and portfolio concentration across asset, stablecoin, protocol, chain, venue, and correlated factor. Label negative-carry hedges as insurance cost, not positive edge. Require confidence at or above 0.60 or block execution handoff until mapping, delta, and notional are independently verified; confidence never shrinks hedge notional. Hand only executionEligible legs to Futures Strategist.

- Treat this as a hedge plan, not a trade signal.
- Re-run if spot exposure changes by more than 10%.
- Re-run if volatility regime changes.
- Never execute from Hedge Warden output alone.
- Before execution, Futures Strategist must run `scan_market_conditions`, `get_futures_account`, `analyze_futures_strategy`, and `calculate_position_size`.
- If Futures Strategist says `no_trade`, the hedge is not executable.
- Net existing spot and perp exposure before sizing; this endpoint does not currently subtract existing hedges.
- Verify that the perp is a valid hedge instrument for the spot asset. Symbols alone do not prove correlation, redemption parity, or basis stability.
- Calculate expected funding and execution drag over the hedge horizon. A risk hedge may be justified with negative carry, but it must be labeled as insurance cost rather than positive edge.
- Use portfolio-level limits for asset, stablecoin, protocol, chain, venue, and correlated-factor concentration. Per-leg neutrality can still leave portfolio beta.
- Delta-neutral is a measured state, not a setup label. Verify actual fills and residual delta after both non-atomic legs settle.

## Standard Flow

### Hedge Invalidation and Unwind Rules (Additive)
Re-run recommend_delta_hedge when spot exposure moves over 10% or volatility regime changes. Net existing spot and perp exposure before sizing; the endpoint does not subtract existing hedges. Verify the perp is a valid hedge instrument (symbols alone do not prove correlation, redemption parity, or basis stability). If Futures Strategist returns no_trade, the hedge is not executable. After both non-atomic legs settle, re-read spot/perp state and report residual delta; delta-neutral is measured, not assumed. If one leg fails, stop dependents and present the predefined unwind.

1. Use Wagon Steward to measure spot exposure.
2. Use Trail Intelligence and Supply Master to understand why the spot leg exists.
3. Call `recommend_delta_hedge`.
4. Reconcile existing hedge inventory, correlation/basis, funding, liquidity, and the user's hedge horizon.
5. Hand only `executionEligible` legs to Futures Strategist for research and sizing.
6. Hand off the selected futures mode after fresh research/sizing. USER_SIGNED requires explicit human confirmation through Futures Strategist; bounded execution requires the owner futures grant, local venue signer and all runtime checks.
7. After both non-atomic legs settle, re-read spot/perp state and report residual delta; if one leg fails, stop dependent actions and present the predefined unwind.

## Disclaimers

### Hedge Report-Back Template (Additive)
Report spot legs, notional, beta, hedge targets, handoff, invalidation, dataQuality, requiresExposureReview, executionEligible and residual exposure. Include fresh Futures Strategist research timestamps, selected domain/mode and its authority evidence: USER_SIGNED human confirmation or the distinct bounded owner grant and live readiness. Re-read spot/perp state after settlement. Mark missing evidence unavailable; a hedge plan is never execution authority.

Hedges can lose money, over-hedge, under-hedge, or fail during volatile markets. Funding, liquidation risk, basis, and venue risk can erase yield. This skill is not financial advice.

**Install:** Copy this file into your OpenClaw workspace, or fetch `https://www.farmdash.one/openclaw-skills/farmdash-hedge-warden/SKILL.md`.

**Companion skills:** FarmDash Futures Strategist, FarmDash Wagon Steward, FarmDash Supply Master, FarmDash Camp Guard.

**Why FarmDash:** Unlike generic hedge advice, Hedge Warden sizes by spot-notional × beta × target-hedge-ratio, never lets confidence shrink the hedge, and blocks the execution handoff below 0.60 confidence until independently verified.

**FarmDash:** [DeFi hedging and risk intelligence](https://www.farmdash.one/)
**Agent Hub:** [FarmDash DeFi hedging agent tools](https://www.farmdash.one/agents)
**OpenAPI Spec:** [FarmDash API Schema](https://www.farmdash.one/agents/openapi.yaml)
**MCP Config:** [FarmDash MCP Server](https://www.farmdash.one/.well-known/mcp.json)

<!-- farmdash-canonical-links:start -->

## Official FarmDash Links

- [FarmDash DeFi intelligence website](https://www.farmdash.one/)
- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical FarmDash Hedge Warden skill manual](https://www.farmdash.one/openclaw-skills/farmdash-hedge-warden/SKILL.md)
- [Agent integration documentation](https://www.farmdash.one/docs)
- [Live agent capability status](https://www.farmdash.one/api/v1/agent/status)
- [OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)
- [Fees and commercial terms](https://www.farmdash.one/fees)
- [Security and authority boundaries](https://www.farmdash.one/security)

### Canonical capability readiness

Generated from shared/capability-truth.ts; read live status for deployment and per-request gates. Implementation readiness is not funded-production proof, commercial admission or signer authority.

| Capability | Status | Required runtime/authority prerequisite |
|---|---|---|
| spot.USER_SIGNED | operational | Healthy execution governor, quote provider, RPC and durable receipt store; customer signs and submits. |
| spot.BOUNDED_AUTONOMOUS | operational | Owner-signed EVM grant, exact simulation/calldata binding, durable budget and customer-local signer authority. |
| futures.USER_SIGNED | operational | Venue account ownership, local action signature, builder approval, risk/research gates and durable order control. |
| futures.BOUNDED_AUTONOMOUS | operational | Authenticated owner-bound futures policy, authorized local API-wallet signature, durable nonce/budget/order controls. |
| solana.USER_SIGNED | operational | Native Jupiter/RPC route, durable preparation and finality store; customer signs and broadcasts. |
| solana.BOUNDED_AUTONOMOUS | operational | Native owner-signed Solana policy; local key must be an actual required transaction signer. Policy creates no on-chain authority. |
| ERC4337_SERVER_SUBMISSION | preparation_only | Qualified tenant/account authorization and session-key policy enforcement on public forwarding, configured bundler, durable claims and verified receipt integration. |
| GENERIC_SERVER_INTENT_EXECUTION | preparation_only | Trusted executable adapter, exact signed-transaction binding and canonical receipt verifier. |
| MEE | preparation_only | Production coordinator and authoritative source/destination receipt verifier. |
| ACP | deployment_prerequisite | AcpReadinessService paidWorkflowReady, evaluator/client identities, migrations, funding/finality workers and Base RPC. |

<!-- farmdash-canonical-links:end -->

<!-- installation-attribution:start -->

### Optional installation attribution

Generate a random UUIDv4 locally once per installation (for example, `crypto.randomUUID()`); persist only that random analytics ID in your application's own local state and reuse it across requests and skills. Never copy an example ID or generate a new ID for every request. Send optional `X-FarmDash-Installation-ID`; keep `X-ClawHub-Skill: farmdash-hedge-warden` and optionally `X-FarmDash-Skill-Version: 1.1.2`. Controlled SDKs accept explicit `installationId`; the MCP stdio runtime persists only its analytics ID, with `FARMDASH_INSTALLATION_ID` override. No generic SDK writes files for you.

This is untrusted analytics only. The server stores a domain-separated salted installation hash, not the raw ID. An installation is not a person, principal or wallet. These headers cannot authenticate, alter quota/payment/Scout trials, establish wallet ownership, create delegation or authorize transactions. Missing headers remain fully compatible. Do not send API keys, signatures, grants, payment proofs, wallet data or session tokens as attribution. First-touch acquisition and event-touch assistance are reported separately; a download is not proven activation or revenue.

<!-- installation-attribution:end -->
