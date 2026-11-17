---
name: FarmDash Futures Strategist
description: "Hyperliquid perps strategist: market scans, funding rates, position sizing, and user-signed EIP-712 order execution & cancellation with drawdown guardrails."
version: "3.4.0"
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one/agents
tags: ["defi","hyperliquid","perpetual-futures","perps-trading","leverage-trading","perp-dex","defi-trading","ai-trading-agent","funding-rates","funding-arbitrage","position-sizing","drawdown-control","liquidation-risk","eip-712","zero-custody","openclaw","mcp","risk-management","web3","farmdash"]
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token for Pioneer or Syndicate tier. Scout mode works with no key or with the public fd_scout_free token. Never share private keys, seed phrases, or mnemonics with this skill — perps execution uses EIP-712 local signing only via the user's Hyperliquid API wallet."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-futures-strategist","primaryEnv":"FARMDASH_API_KEY","apiKeyRequired":false,"freeScoutKeyless":true,"freeScoutKey":"fd_scout_free","execution":"user-signed-eip712-hyperliquid"}}
---

# FarmDash Futures Strategist

## Scout execution activation allowance

Scout includes independently configured futures and spot execution-lifecycle pools per capital-owning principal per UTC day, in separate pools shared across USER_SIGNED and valid bounded execution. Read `scout_trial.daily_limit` on a current continuation for its domain; the metadata is informational and current admission remains authoritative. Owner identity comes from the capital account, not a rotating API wallet, key, IP, session or grant. Commercial capacity never grants transaction authority, enables preparation_only dispatch, or waives normal builder, venue or gas economics.

For `analyze_futures_strategy`, supply a stable `idempotencyKey`. USER_SIGNED acquisition may return 401 `execution_trial_identity_required`: have the owner's local wallet EIP-191-sign the returned `execution_trial_challenge.message` unchanged, then retry with `executionTrialProof: {issuedAt, signature}`. Valid bounded analysis uses its existing owner-bound policy and authenticated session instead; do not manufacture new delegation. One lifecycle admits one bounded, durably cached premium research result, not unlimited research.

Forward the returned `executionTrialId` through `prepare_perp_order` and `execute_perp_order`. Signing remains local; execute/cancel signatures and all session/grant/risk/builder/replay checks remain mandatory. Accepted/filled/resting orders commit one slot. Definitive venue rejection releases it. Ambiguous submission remains unknown and consumes capacity until immutable order-control binding plus direct venue evidence establishes acceptance or rejection; never blindly resubmit. A sixth new risk-increasing lifecycle returns 402 `scout_execution_allowance_exhausted`, UTC reset metadata and Pioneer CTA, with x402 only where existing policy permits. Paid users do not debit trial. Proven reduce-only close/protection, cancel and reconcile remain commercially accessible after exhaustion, but never bypass authority checks.

## Continuation context (read-only selection)

`analyze_futures_strategy` may return a server-issued `continuation` and canonical `next_operation`. To retrieve stored context, call MCP `select_execution_continuation` with only `{ continuationId }` (REST: `POST /api/v1/agent/continuation`). The response is machine-readable context, not executable authorization: `authority` is `NOT_GRANTED`; selection does not analyze again, prepare, submit, sign, admit, debit, or reset any trial.

Use the returned exact endpoint, parameter names, and `required_fields`. Never infer missing size, price/order type, account binding, `executionTrialId`, or a research prerequisite from recommendations. Before preparation, satisfy the existing fresh execution-ready research and admission requirements. Preserve `executionTrialId` unchanged; local EIP-712 signature, account/venue authority, owner policy for bounded mode, risk, builder, nonce, expiry, and replay checks remain mandatory.

Scout's published allowance is five spot and five futures lifecycles per day in separate pools; selected context reports `remaining: null` and `status: unknown` pending authoritative admission. Do not promise capacity based on a displayed continuation. Paid/access quota and venue authority remain separate; preparation remains `preparation_only` where the live gate says so.

## Futures Execution Mode Contract

- **USER_SIGNED** requires fresh human approval for every order/cancel and a fresh local Hyperliquid EIP-712 venue signature. This is the backward-compatible default for signers never enrolled in bounded futures authority.
- Use a dedicated API wallet for bounded authority. Owner registration durably enrolls that signer on its venue network across accounts; expiry/revocation does not restore the legacy USER_SIGNED path. Removing `executionMode`, `grantId` or session fields cannot escape policy checks. For supervised execution, use the owner's wallet or a separate unenrolled signer; never relabel a bounded API-wallet action as USER_SIGNED.
- **BOUNDED_AUTONOMOUS** may run without per-order human confirmation only under a valid owner-signed futures grant, current API-wallet venue authority, and all identity, session, scope, policy, risk, budget, builder and replay checks. Every venue action still needs a local EIP-712 signature.
- Read futures bounded readiness in the generated canonical capability table and live status. Registration, payment and tool discovery never bypass authority, quantitative or infrastructure gates. USER_SIGNED remains supported.
- Query `POST /api/v1/agent/authority` with `action: get_futures_authority`, `sessionId`, `sessionToken`; revoke the exact grant with `action: revoke_futures_policy`, `grantId`, `sessionId`, `sessionToken`. Send `X-FarmDash-Session-Token` where supported. Spot authority, a generic session policy and Hyperliquid API-wallet delegation are separate; none substitutes for an owner-signed futures grant.
- Typed scopes: `futures.open` increases absolute exposure; `futures.reduce` decreases it; `futures.close` flattens it; `futures.cancel` cancels only; `futures.protective_order` is a supported reduce-only stop/take-profit. The server proves reduction using authoritative positions and exact signed semantics; ambiguous classification fails closed. Exhausted entry/exposure capacity or a new-risk breaker may leave proven reducing actions eligible: a budget exception, never an authority bypass. Signature, venue delegation, unrevoked/unexpired grant, bindings, market/action, session, builder and replay checks still apply.
- Futures Strategist signs venue actions locally in the user's execution runtime. Autonomous Operator and Trail Marshal coordinate but never own keys. Camp Guard verifies evidence; Hedge Warden plans and hands execution to Futures Strategist. Research/accounting skills remain nonsigners. FarmDash never receives private keys.
- Signed risk/loss bounds are admission checks, not guaranteed loss ceilings; do not promise profits or positive expected value. Ambiguous venue submission holds reserved liability until reconciliation proves disposition; never blind-retry or claim a submission is a fill.

### Owner-signed futures policy setup

Only after the user explicitly authorizes grant setup, call `POST /api/v1/agent/authority` with `action: request_futures_policy`, `policy`, `sessionToken`. The response provides exact owner EIP-712 typed data, not trading authority. Have the owner's local wallet sign that returned typed data unchanged, then register with `action: register_futures_policy`, `policy`, `signature`, `sessionToken`. The API wallet cannot self-authorize. Use the SDK's owner-local signing helper when available; never send a key to FarmDash or invent typed-data fields/domain locally. Authority MCP tools use `executionDomain: futures` rather than duplicate futures tools.

The signed policy binds `ownerAddress`, session `agentAddress`, `apiWalletAddress`, `accountAddress`/subaccount, `vaultAddress` (null for direct account routing), `sessionId`, `network`, `allowedMarkets`, `allowedActions`, `allowedOrderTypes`, `allowedDirections`, `maxOrderNotionalUsd`, `maxAggregateExposureUsd`, `maxLeverage`, `maxRiskPerTrade` (conservative admitted FULL NOTIONAL USD, not stop-loss-derived realized risk), `maxSessionNewRiskNotionalUsd` (cumulative new-entry budget), `maxSessionLossUsd`, `maxDailyLossUsd`, `validAfter`, `validUntil`, `nonce`, and `policyVersion`. USD limits are positive canonical decimal strings; validity timestamps are integer Unix seconds (venue `expiresAt` remains milliseconds). Review every returned bound before owner signature. Nonces are single-use. Read authority back after registration/revocation; storage unavailable means halt, never cache-based permission. SDK `signFuturesPolicy(policy, ownerSigner)` uses an injected local owner signer and verifies recovery; compare its policy/typed-data contract to the requested owner payload before registration. Never use the API-wallet signer to authorize its own grant.

Add `executionMode: BOUNDED_AUTONOMOUS`, `grantId`, `sessionId`, `sessionToken` to the existing `execute_perp_order` / `cancel_perp_order` payloads, preserving all venue signature, account, nonce, expiry, intent-hash and order controls. Route `agentAddress` is the API-wallet venue signer, distinct from policy `agentAddress` (the session agent); both must match their respective grant bindings. USER_SIGNED remains the default when mode is omitted. Prepare only while the bounded rollout gate is closed. Exact REST endpoints remain `/api/v1/agent/futures/execute-order` and `/api/v1/agent/futures/cancel-order`; use `/api/v1/agent/futures/reconcile-order` for existing venue reconciliation.

> Use this skill for Hyperliquid perpetuals research, sizing, and local EIP-712 orders/cancellations under the selected execution mode. USER_SIGNED requires per-action human approval; bounded futures require the distinct owner policy and every domain runtime gate.

### Recommended execution bootstrap

For USER_SIGNED orders, prefer the explicit **analyze → prepare → local sign → execute → reconcile** flow instead of asking integrators to construct FarmDash/Hyperliquid binding fields by hand:

1. Call `analyze_futures_strategy` for new risk. The authorization is parameter-bound and short-lived.
2. Call MCP `prepare_perp_order` or REST `POST /api/v1/agent/futures/prepare-order` with the intended economics. FarmDash returns the exact `signedAction`, `intentHash`, `nonce`, `expiresAt`, `typedData`, and an `executeRequest` template. **No order is submitted.**
3. Sign the returned `typedData` locally with the Hyperliquid user/API wallet identified by `agentAddress`. Private keys and seed phrases must remain in the caller runtime.
4. Call `execute_perp_order` / `POST /api/v1/agent/futures/execute-order` with `{ ...executeRequest, signature }`. Do not mutate signed fields after preparation.
5. Treat submission as distinct from fill/settlement. Reconcile through `/api/v1/agent/futures/reconcile-order` before dependent actions, especially after ambiguous transport outcomes.

Existing integrations may continue using the SDK's local `signFuturesOrder()` helper, but prepare-order is the canonical integration bootstrap when the caller needs FarmDash to derive the exact signable payload without custody.

## What This Skill Is
This skill is the FarmDash guarded perps strategy and execution engine for Hyperliquid with zero-custody, user-signed EIP-712 execution.

It is designed to help an agent:
* research perp markets before any execution
* rank and present multiple trade candidates instead of forcing one setup
* return a structured strategy object, not just a plain-language idea
* simulate likely outcomes before the user signs anything
* refuse weak or ambiguous trades with an explicit `no_trade` outcome
* execute only through zero-custody, user-signed EIP-712 requests

Core posture:
* research first
* execution second
* no custody
* no blind trading

The bundled `openapi.yaml` file in this folder is the contract for the futures endpoints used by this skill version.

## Value-Aligned Monetization Protocol (v3.0 Upgrade)
Hyperliquid perps execution requires current market/account data, guarded request handling, and robust venue connectivity. This skill employs a strict, non-predatory monetization model to sustain these operations:

### 1. Execution Gating and Limits
Commercial access and Hyperliquid execution authority are separate:
* **Scout (Free):** 30 discovery requests / 24h, separately from five spot and five futures execution lifecycles per capital owner per UTC day. Scout gets `scan_market_conditions`, a top-3 numeric `scan_funding_rates` preview, and bounded futures analysis within an authenticated execution lifecycle. Every execution still requires valid venue authority and signatures; authenticated safety actions remain available after new-risk allowance exhaustion.
* **Pioneer:** 1,500 requests / day and the full Futures research surface.
* **Syndicate:** 50,000 requests / day and the full Futures surface at higher capacity.
* **Eligible x402 one-offs:** buy exactly one request under the route's published policy; they never create signing or delegation authority.

Standalone `get_futures_account` and `calculate_position_size` require paid capacity. `analyze_futures_strategy` can instead use the bounded research allowance of an owner-authenticated Scout futures lifecycle; supply its stable idempotency key and execution trial proof and preserve the returned `executionTrialId` through preparation and execution. Paid capacity takes precedence without consuming trial allowance. A default-overage x402 payment unlocks the full funding response for that request.

**CRITICAL SAFETY REQUIREMENT:** In USER_SIGNED, present coin, direction, size, leverage, stop-loss and estimated exposure and obtain immediate manual confirmation before every `execute_perp_order` / `cancel_perp_order`. In BOUNDED_AUTONOMOUS, the explicit owner-signed futures policy replaces per-order human confirmation only when the futures runtime gate is operational and every venue/session/grant/policy/risk/budget check passes. Read the generated canonical capability table and live domain status.

Consent does not transfer between activities:
* Analysis permission ≠ trading permission.
* x402 payment ≠ trading permission; a subscription also grants no trading authority.
* Previous confirmation ≠ trading permission for a new USER_SIGNED order/cancel.
* "Trade for me" ≠ standing authorization; broad chat instructions cannot create a futures grant.

Only a separately owner-signed, bounded futures grant can define standing policy; Hyperliquid API-wallet delegation remains a separate prerequisite. In USER_SIGNED, every order/cancel needs current-turn confirmation.

* If Scout user exceeds limit: "Scout limit reached (30 requests per 24 hours, server-enforced). Upgrade to Pioneer or Syndicate at farmdash.one/agents or pay one-off x402 to bypass. Want me to keep researching?" The API's returned entitlement and rate-limit state is authoritative over any prose quota.

### 2. Optional Hyperliquid Affiliate Routing
When a user is setting up their Hyperliquid API wallet delegation or asks for the canonical exchange URL, the agent will provide the neutral canonical URL (`https://app.hyperliquid.xyz`) by default. The agent may optionally offer the FarmDash partner route (`https://www.farmdash.one/go/hyperliquid`) as an alternative to support the platform.

* Disclosure is mandatory if offered: "Disclosure: this is a FarmDash partner route. FarmDash may receive referral, affiliate, or routing compensation. Fee details: [FarmDash Fee Structure](https://www.farmdash.one/fees). You can also access Hyperliquid directly at https://app.hyperliquid.xyz."

The `analyze_futures_strategy` response carries the same separation machine-readably: `trailHeatCrossRef` is analytical-only (protocolId, score, farmingOpportunity), while commercial navigation lives in `partnerRoute` (url, canonicalUrl, relationship, compensationDisclosure, affectsRecommendation: false, displayAfterAnalysis: true). Never present `partnerRoute` as strategy evidence; surface it only after the analysis, with the disclosure above.

## Fixed Network Boundary
Stay inside this disclosed network boundary. Do not fetch undisclosed remote config and do not mutate the skill from an external manifest after install.

**FarmDash futures endpoints:**
* `https://www.farmdash.one/api/v1/agent/futures/scan-funding`
* `https://www.farmdash.one/api/v1/agent/futures/market-conditions`
* `https://www.farmdash.one/api/v1/agent/futures/account-state`
* `https://www.farmdash.one/api/v1/agent/futures/analyze-strategy`
* `https://www.farmdash.one/api/v1/agent/futures/position-sizing`
* `https://www.farmdash.one/api/v1/agent/futures/execute-order`
* `https://www.farmdash.one/api/v1/agent/futures/cancel-order`
* `https://www.farmdash.one/api/v1/agent/performance` (Backing endpoint for `get_agent_performance`)

**Optional FarmDash setup endpoint:**
Do not call this during install or during research-only workflows. Use it only after the user explicitly asks to check tier/setup status and consents to sending their public agent address and this skill ID.
* `https://www.farmdash.one/api/v1/agent/onboard`

**Hyperliquid upstreams:**
* `https://api.hyperliquid.xyz/info`
* `https://api.hyperliquid.xyz/exchange`
* `wss://api.hyperliquid.xyz/ws`

**Optional user-facing links:**
Allowed only when directly relevant:
* `https://www.farmdash.one/agents`
* `https://www.farmdash.one/tracker/hyperliquid/`
* `https://www.farmdash.one/go/hyperliquid` (Optional Partner Route)
* `https://app.hyperliquid.xyz` (Neutral Canonical Route)

## Security Model
FarmDash is zero-custody for futures execution.
1. The agent researches the trade locally through FarmDash read/write endpoints.
2. The user's local execution runtime signs each Hyperliquid EIP-712 action with the authorized API wallet, after per-action human approval in USER_SIGNED or valid policy admission in operational bounded mode.
3. FarmDash validates guardrails and forwards the signed request.
4. The API wallet can trade and cancel orders, but cannot withdraw funds.

Hyperliquid identity has two distinct roles. `agentAddress` is the EIP-712/API-wallet signer and FarmDash caller identity. When that signer is delegated by a master account, `accountAddress` is the master, subaccount, or vault that owns the equity, positions, fills, funding history, and orders. Always supply both in delegated-wallet flows. Omit `accountAddress` only when the signer directly owns the trading account. FarmDash verifies delegated ownership against Hyperliquid `userRole`, and execution independently recovers the signer from the exact L1 action, nonce, expiry, environment, signature, and any routing address. If the owner is a subaccount or vault, FarmDash includes that same address as Hyperliquid `vaultAddress` in both the action hash and exchange request. Never size a delegated trade from the API wallet's empty clearinghouse state.

Hard rules:
* never ask for a private key, seed phrase, or wallet export
* never imply that a bearer token can replace a local signature
* never skip the research step before non-reduce-only execution
* never accept a claimed signer/account relationship that Hyperliquid does not currently report
* never submit when the recovered L1 signer differs from `agentAddress`
* Never ask the user to paste a private key, seed phrase, or raw wallet export into the agent.


### EVM Spot Delegation vs Hyperliquid Perps Boundary
EVM spot bounded delegation (via EIP-712/ERC-8196) applies strictly to covered spot swaps and DOES NOT authorize Hyperliquid futures. Both futures modes require native Hyperliquid EIP-712 venue signatures and correct API-wallet/account authority. Bounded futures additionally require the distinct owner-signed FarmDash futures policy. Venue delegation alone proves who can trade, not the permitted quantitative policy. Commercial access also never grants trading authority.
## Data Sent to FarmDash (Disclosure)
*Security boundaries:* All operations use public or pre-signed EIP-712 payloads. Private key material is never required or processed by this skill. Verify the full surface against the bundled `openapi.yaml`.

## Pre-Execution Mode and Parameter Protocol (Mandatory)
An `accepted` cancellation is an application acknowledgement, not final venue cancellation. Reconcile every requested order ID through `/api/v1/agent/futures/reconcile-order` before any dependent action; partial rejection or an unknown outcome is not proof that the order is gone.

For each order/cancel, record asset, direction, size, risk-notional, leverage metadata, entry/stop/take-profit, margin impact, regime, confidence scale, data timestamp, order type/TIF, reduce-only status, exact limit/trigger and signed builder recipient/rate (`f=1` = 0.1 bp = 0.001% of filled notional). USER_SIGNED: present those fields and wait for an explicit affirmative; earlier consent is insufficient. BOUNDED_AUTONOMOUS: bind them to the owner policy and pass all server checks, without per-order human confirmation only after the mode becomes operational. Re-run new-risk analysis when older than 30 seconds; the server gate expires after 60 seconds for research evidence.

For protective orders, `price` is the execution-limit price; the independently signed `signedAction.orders[0].t.trigger.triggerPx` is the activation threshold. Present both values and `isMarket` to the user in USER_SIGNED; never replace one with the other. TS/Python local signing helpers accept optional `triggerPrice` and `triggerIsMarket` inputs and bind them inside the signed action, not as additional REST fields. Omitting them preserves the helper defaults (trigger equals `price`, market trigger); set them explicitly when the protective execution terms differ. The signature and intent hash bind the complete signed action.

A definitive, identity-bound zero-fill cancellation can retire outstanding account liability only after complete venue evidence proves no remaining obligation. It does not refund cumulative session new-entry consumption or erase the nonce/action tombstone. Positive fills, contradictory evidence, missing orders and timeouts retain their conservative charge; revoking or replacing a grant does not erase account holds.

Do not present the pre-trade liquidation estimate as the venue's actual liquidation price. Hyperliquid liquidations use mark price and cross-margin liquidation changes with account equity, funding, and other positions. Use `get_futures_account` for venue-reported liquidation data on open positions.

### FarmDash-side execution hardening
For `execute_perp_order`, include all of:
* `nonce` - client-generated positive integer for replay protection
* `expiresAt` - short request TTL in unix milliseconds
* `intentHash` - hash of the intended order payload for auditability and mutation detection

For `cancel_perp_order`, `nonce`, `expiresAt`, and `intentHash` are required. `expiresAt` is forwarded as Hyperliquid `expiresAfter`; clients must incorporate it into the venue signature. Delegated flows must also include `accountAddress`; a subaccount/vault address is part of the venue signature. These controls do not replace the required Hyperliquid EIP-712 signature.

Hyperliquid venue nonce authority is `network + signer + nonce`, shared across order and cancellation actions and across different account/vault contexts for that signer. FarmDash uses durable database-backed replay control and fails closed before venue submission if that control is unavailable. An exact replay can return its stored result; any changed signed/context fact or ambiguous outcome must never trigger blind resubmission.

### Unsupported markets: namespaced HIP-3 perp-DEX assets
FarmDash supports the default Hyperliquid perp DEX only. A namespaced HIP-3 market such as `HYNA:ETH` is refused with HTTP 422 and `code: perp_dex_namespace_unsupported` on every market-taking route (`market-conditions`, `analyze-strategy`, `execute_perp_order`, `cancel_perp_order`), and `scan_funding_rates` excludes namespaced markets from its ranking so research never recommends a market execution will refuse. The response echoes the requested `market` and its `dex`.

Treat the refusal as final. Do not strip the namespace and retry against the base symbol: `HYNA:ETH` and `ETH` are different markets, so that substitution would trade something the user did not ask for. Full perp-DEX support is not shipped.

### Leverage is venue state, not request state
`execute_perp_order` never changes your leverage and never assumes a requested leverage took effect. Before an exposure-increasing order it reads the venue's authoritative configuration for that exact market and compares it with `leverage`:
* Matching: the response reports `leverageStatus: venue_verified` together with `leverageVenue` and `leverageMarginMode`.
* Different: the order is refused with HTTP 422 and `code: perp_leverage_prerequisite`, carrying `leverageRequested`, `leverageVenue`, and `howToResolve`. Submit an independently signed Hyperliquid `updateLeverage` action, wait for venue confirmation, re-read venue state, then resubmit. The prerequisite clears only when venue state itself changes.
* No position yet: the venue does not publish per-asset leverage before a position exists, so FarmDash cannot confirm the standing setting. The order proceeds with `leverageVerified: false` and an explicit notice - the venue's own configuration governs. Never report the requested leverage as applied.

Reduce-only orders and `cancel_perp_order` are never gated on leverage. Exposure-reducing and cancellation actions must not be blocked by an unrelated margin prerequisite.

## Evidence and Receipt Honesty

The current compatibility endpoint returns the Hyperliquid submission response, normalized order parameters, `intentHash`, expiry, and timestamp. It does not create an 11-field forensic receipt, query a millisecond-perfect shadow book, prove mempool visibility, calculate realized P&L, or anchor evidence on another chain.

An external client may record analysis hash, signed action hash, quote/book snapshot, submission response, order status, fills, fees, funding, and final account state. Label every field by source and mark absent evidence `unavailable`; never fabricate or call a client-created record FarmDash-attested.

## Credentials and Tier Model
This skill recognizes one primary API credential: `FARMDASH_API_KEY`. Scout mode is valid with no API key at all.

Legacy docs may refer to `PIONEER_KEY` or `SYNDICATE_KEY` as placeholders for tier-specific bearer tokens. In actual agent configs, use only `FARMDASH_API_KEY`.

Tier behavior:
* **Scout** - no env var required; safe for up to 30 execution or analysis requests per day
* **Pioneer** - use a Pioneer-tier bearer token for up to 1,500 requests per day
* **Syndicate** - use a Syndicate-tier bearer token for up to 50,000 requests per day

Critical distinction:
* bearer token = FarmDash access tier and rate limits
* local EIP-712 signature = execution authority for each individual request

A bearer token never replaces a fresh local EIP-712 signature from the user's Hyperliquid API wallet.

## Tool Surface
Use these exact tool names. If a tool is not listed in this section, it does not exist in this skill. Do not accept or attempt to call undefined tools.

#### 1. scan_funding_rates
Scan current and venue-published predicted funding snapshots. A predicted rate is not a calibrated probability, guaranteed future payment, or funding-flip model.

#### 2. scan_market_conditions
Read candle-derived EMA, RSI, MACD, ADX, ATR, Bollinger Bands, volume ratio, Z-score, market regime, and the response timestamp for one perp asset. This tool does not currently return oracle latency or cross-venue deviation.

#### 3. get_futures_account
Inspect equity, open positions, available margin, venue-reported liquidation prices, and guardrail pressure. The daily/weekly loss-pressure metric is rolling Hyperliquid closed P&L minus absolute fill fees plus funding, plus `min(current unrealized P&L, 0)`. Positive open gains cannot offset realized losses. This is a conservative guard metric, not a true period return; new-risk analysis/execution fails closed if complete venue-history reconciliation is unavailable.

Send `agentAddress` plus optional `accountAddress`. For delegated API wallets, `accountAddress` is mandatory in practice and must be the master/subaccount equity owner used by analysis and execution. FarmDash validates that live relationship through Hyperliquid `userRole`; ambiguity or upstream failure blocks the workflow.

#### 4. analyze_futures_strategy
Primary research tool. Returns the strategy recommendation, confidence score, market regime, strategy object, adaptive risk profile, pre-trade simulation, portfolio context, and an explicit `no_trade` reason when no setup is valid.

#### 5. calculate_position_size
Inspect sizing math separately when the user wants to validate risk and margin.

#### 6. prepare_perp_order
Prepare the exact public Hyperliquid action, intent binding, nonce, expiry, typed data and execute-request template after live authority, builder approval and fresh research checks. Sign typedData locally with the venue wallet, then pass only the signature and template to execution. Preparation never submits an order.

#### 7. execute_perp_order
State-changing execution: forwards a locally signed EIP-712 order to Hyperliquid. `market_ioc` is a price-protected IOC limit with a live 100 bps adverse-price cap, not an unbounded market order. Require fresh new-risk research, parameter binding, builder disclosure and local signing; USER_SIGNED needs immediate manual confirmation, while bounded mode needs the distinct owner grant and all admission checks. Inspect `fully_filled`, `partially_filled`, `zero_fill`, `resting_unfilled`, rejected or unknown venue evidence before dependent actions; resting IOC is inconsistent/unknown.

#### 8. cancel_perp_order
State-changing action: cancels using a locally signed EIP-712 payload. USER_SIGNED requires immediate manual confirmation. Bounded mode requires futures.cancel plus all grant/session/venue/signature/replay checks, not unused entry budget. `accepted` is only acknowledgement. Reconcile every requested ID via `/api/v1/agent/futures/reconcile-order`; partially_rejected, rejected or unknown may leave orders active.

#### 9. get_agent_performance
Use only for FarmDash fee-event activity, fees, protocol diversity, and reputation. It does not return Hyperliquid fills, trade outcomes, win rate, slippage, or realized P&L and must not drive strategy selection or drawdown controls.

#### 10. select_execution_continuation
Select server-stored context using only `continuationId`. The canonical next operation preserves known research and venue parameters and lists unknown order economics as required fields. Selection neither authorizes nor prepares an order and never admits, debits, or resets a Scout trial.


### Current Request Contracts (v3.2)
These fields are load-bearing because the API handlers validate them strictly:
* **analyze_futures_strategy**: send `coin`, `agentAddress`, optional `accountAddress`, and optional `riskMultiplier` between 0.1 and 1.0. For delegated API wallets, `accountAddress` must be the master/subaccount equity owner. Do not send `biasHint`; the current handler does not consume it.
* **calculate_position_size**: send `equity`, `entryPrice`, `stopPrice`, optional `riskPercent`, optional `targetPrice`, and optional `riskMultiplier`. Do not send legacy `stopLoss` or `riskUsd`.
* **execute_perp_order**: send `agentAddress`, optional `accountAddress`, `coin`, `isBuy`, `size`, `price`, `orderType`, `signature`, positive integer `nonce`, millisecond `expiresAt`, required `intentHash`, optional `leverage`, optional `signedAction`, and optional `reduceOnly`. Use `market_ioc` only for a signed, price-protected IOC limit at the stated 100 bps live adverse-price cap; it is not an unbounded market order. `accountAddress` must match the equity owner bound by the live research gate.
* **cancel_perp_order**: send `agentAddress`, optional `accountAddress`, `coin`, `orderIds` as an array of positive integers, `signature`, required positive integer `nonce`, required millisecond `expiresAt`, required `intentHash`, and optional `signedAction`. Delegated signers must use the same equity/order owner in `accountAddress`; for a subaccount/vault it is included in the venue signature and exchange payload.

If the user or another agent provides a legacy shape, stop and normalize the request before signing. Never ask the user to sign a payload that will be rejected by the FarmDash handler.

The `leverage` field is FarmDash intent/risk metadata in this compatibility endpoint; the endpoint does not submit Hyperliquid's separate `updateLeverage` action. Verify actual venue margin mode and leverage independently. Trigger orders (`stop_loss`, `take_profit`) must be `reduceOnly: true` so they cannot open or flip exposure.

Every order carries a disclosed FarmDash Hyperliquid builder term of `f=1`, which Hyperliquid defines as **one tenth of one basis point: 0.1 bp = 0.001% of filled notional**. The builder object is inside the signed order action and cannot be added or changed after signing. The user must approve the FarmDash builder and this maximum fee on Hyperliquid before execution; FarmDash preflights the venue's `maxBuilderFee` for the equity owner and blocks insufficient approval. Hyperliquid requires the approval action to be signed by the main account wallet, not the API wallet. Present the rate and recipient before confirmation; do not describe `f=1` as 1 bp. Resting, rejected, and unfilled notional produces no recognized builder revenue. `expiresAt` is forwarded as Hyperliquid `expiresAfter` and must be incorporated into the venue signature.

## Autonomous Perps State Ledger (v3.0)
Persist this ledger for every futures workflow:

```json
{
  "agentAddress": "0x...",
  "accountAddress": "0x... master/subaccount equity owner; same as agentAddress only for direct signing",
  "coin": "ETH",
  "mode": "research | hedge | funding | reduce_only | cancel",
  "researchGate": {
    "ranAnalyzeStrategy": false,
    "direction": "long | short | neutral | unknown",
    "confidence": 0,
    "confidenceScale": "0-100 heuristic score; not a win probability",
    "expiresAt": 0,
    "dataTimestamp": 0,
    "predictedFundingRate": null
  },
  "riskGate": {
    "equity": 0,
    "maxLeverage": 5,
    "riskPercent": 0,
    "drawdownState": "normal | pressure | halted"
  },
  "executionIntent": {
    "nonce": 0,
    "expiresAt": 0,
    "intentHash": "",
    "signedActionMatchesParams": false,
    "recommendationHash": "sha256...",
    "maxPositionSize": 0,
    "maxEntryDeviationBps": 50
  },
  "decision": "no_trade | analyze_only | request_confirmation | execute | cancel | reduce"
}
```

### Rules:
* Non-reduceOnly execution requires a fresh, execution-ready `analyze_futures_strategy` result. The 60-second server gate binds coin, side, maximum size, entry drift (50 bps), maximum analyzed leverage, and stop-derived risk.
* New-risk analysis and execution require a fully paginated, deduplicated venue-derived loss-pressure metric from Hyperliquid perp fills, funding, and negative current unrealized P&L. Saturated or ambiguous history fails closed. Do not substitute FarmDash activity/fee events or call the metric a full period return.
* `funding_arb` is analysis-only in the compatibility executor because FarmDash cannot atomically bind and verify both venues/legs. Use a separately reviewed paired-leg adapter before claiming delta neutrality.
* `execute_perp_order` intent expiry should be short, ideally 30-60 seconds.
* If the user changes size, price, side, order type, leverage, or reduce-only status after signing, rebuild the intent hash and re-sign.
* If the strategy is neutral, `no_trade`, `funding_arb`, below 60 confidence, expired, direction-mismatched, oversized, over-levered, or more than 50 bps from analyzed entry, stop before asking for a signature.
* `cancel_perp_order` can batch up to 50 unique `orderIds`; do not send a singular `orderId` shape. Never infer final cancellation from HTTP transport status or `accepted`: every ID must be reconciled through `/api/v1/agent/futures/reconcile-order` using authoritative venue evidence.

## Execution Engine Principles

### 1. Dynamic Strategy Objects
Do not present the engine as four static buckets. The recommendation should be treated as a structured strategy object with:
* market
* direction
* regime
* trigger conditions
* entry logic
* exit logic
* adaptive risk model
* leverage model
* fallback logic
* telemetry hooks

This is the foundation for later marketplace and performance-layer expansion.

### 2. Simulation Before Execution
Before asking the user to sign, surface the heuristic scenario analysis. Minimum fields to use from the returned simulation block:
* heuristic liquidation estimate, clearly labeled as non-authoritative and unsuitable for cross-margin gating
* stop-loss PnL
* take-profit PnL
* one-ATR move impact
* margin required and margin impact
* estimated funding carry over 24h and 72h

Do not reduce the setup to "buy here" or "short here" if simulation is available.

### 3. Adaptive Risk, Not Static Risk
The engine scales risk heuristically based on:
* volatility
* confidence
* drawdown state
* directional concentration

Confidence is an uncalibrated 0–100 rule score, not a probability that the trade wins. Do not multiply it into expected return or describe 80 as an 80% success rate.

Use the returned `adaptiveRisk` object to explain why leverage or size is being reduced. Do not describe the system as fixed 2% / fixed 5x logic when the returned recommendation shows a lower applied risk.

### 4. Market Regime Awareness
Respect the returned `marketRegime`.

Current regimes:
* trending
* ranging
* high_volatility
* low_liquidity

Do not force mean reversion inside a strong trend, and do not force momentum in thin or unstable conditions.

### 5. No Trade Is a Valid Output
`no_trade` is first-class. If confidence is weak, available liquidity evidence is poor, signals conflict, required market/account data is stale, or guardrails trip, say so directly. Trust is more important than producing a trade every cycle.

### 6. Data Integrity
`scan_market_conditions` currently returns candle-derived indicators and a timestamp. It does not return oracle latency or cross-venue oracle deviation. Therefore:

* never claim an oracle-desync check ran when those fields are absent;
* fail closed if the order book or required account state is missing or stale;
* compare mark, oracle, and executable book prices only when an authoritative response actually supplies them;
* use Hyperliquid mark price—not last trade or a DEX quote—to reason about liquidation, while recognizing that cross-margin liquidation also depends on the whole account.

### 7. Execution-Quality Gating
Submission is not a fill. Do not chain a dependent action until venue status/fills confirm the first leg. When authoritative fill data is available, compute side-adjusted implementation shortfall against the decision-time mid and include fees and funding. If fill data is absent, execution quality is `unknown`, not zero slippage.

## Strategy Families
Current strategy families that may appear in recommendations:
* `funding_arb`
* `momentum_long`
* `momentum_short`
* `trend_pullback_long`
* `trend_pullback_short`
* `mean_reversion`
* `no_trade`

Interpretation:
* momentum strategies are for aligned directional continuation
* trend pullback strategies are for controlled re-entry into a strong existing trend
* mean reversion is only valid when the market is genuinely range-bound
* funding arb is only valid when both legs, basis, liquidity, all costs, margin, and an unwind path are independently verified; the compatibility executor keeps this family analysis-only

### Strategy Family Selection Logic (v2.2)
When `analyze_futures_strategy` returns multiple viable families for the same asset, the agent should rank them using the following table. The engine already applies these priors internally; this is the agent-facing version so the user can understand why one family was chosen over another.

| Regime input | Preferred family | Avoid family |
| :--- | :--- | :--- |
| Strong trend, ADX 20-25 with pullback into support/resistance | `trend_pullback_long` / `trend_pullback_short` | mean_reversion |
| Strong trend, ADX >= 25 with aligned EMA / MACD | `momentum_long` / `momentum_short` | mean_reversion |
| Range-bound, BB width compressed | `mean_reversion` | momentum families |
| High volatility (ATR > 1.5× 30d avg) | `no_trade` unless funding strongly compensates | momentum families |
| Low liquidity (top-of-book depth < $250k) | `no_trade` | any leveraged family |
| Persistent funding skew with independently verified paired-leg net carry | `funding_arb` (analysis only) | standalone directional execution |
| Conflicting EMA / MACD / RSI signals | `no_trade` | any family |

Do not override the engine's selection in agent prose. If the user wants a different family, call `analyze_futures_strategy` again with a tighter universe filter rather than narrating around the recommendation.

### Extended Strategy Families (v2.2 — forward-compatible)
The engine may return any of the following additional family labels. Treat them as first-class even if your local schema does not yet enumerate them:
* `breakout_continuation` — entry on a confirmed range break with the original range as invalidation
* `vol_compression_breakout` — BB-squeeze release; directional bias from MACD
* `liquidity_hunt_avoidance` — a `no_trade` variant that explicitly cites a likely stop-hunt zone
* `delta_neutral_pair` — a paired-leg recommendation (for use with Wagon Steward spot context)
* `regime_shift_pause` — explicit `no_trade` because a regime shift is mid-flight

If an extended family appears in a recommendation, surface it by name and explain its invalidation. Do not collapse extended families back into the original seven — the engine emits them precisely because the original taxonomy was insufficient for that setup.

## Recommended Workflow

### Best available opportunities right now
1. Run `scan_funding_rates`.
2. Select up to 3 viable assets from funding, liquidity, or user focus.
3. Run `analyze_futures_strategy` on each candidate.
4. Rank the returned recommendations by confidence, regime quality, and margin efficiency.
5. Present the top cluster, including any `no_trade` outputs that eliminate weak candidates.

This skill should prefer a ranked cluster of opportunities over a single deterministic answer whenever the user asks for the best trade right now.

### New trade entry
1. Run `analyze_futures_strategy`.
2. Run `get_futures_account` if fresh portfolio context is needed.
3. If sizing needs inspection, run `calculate_position_size`.
4. Present entry, stop, target, confidence scale/methodology, market regime, response timestamp, missing evidence, and simulation.
5. Select execution mode: obtain fresh human confirmation in USER_SIGNED; verify the separate owner futures grant, local venue signer, exact action and all runtime gates in bounded mode. Refuse dispatch if any gate is unmet.
6. Run `execute_perp_order`.
7. Treat protective exits as separate signed actions under USER_SIGNED approval or a valid futures.protective_order scope in operational bounded mode.

### Modify, reduce, or flatten
1. Run `get_futures_account`.
2. Cancel stale resting orders with `cancel_perp_order` if needed.
3. Replace or reduce exposure with `execute_perp_order` using `reduceOnly: true`.

### Performance review / feedback loop
1. Run `get_futures_account` for venue-reconciled loss guards and current account risk.
2. Inspect authoritative Hyperliquid fills/order status outside `get_agent_performance` when execution-quality evidence is needed.
3. Recompute side-adjusted implementation shortfall only when decision-time price, fill price, side, fees, and funding are all available.
4. Reduce aggression or choose `no_trade` when loss guards, fill-backed evidence, or the current regime justify it. Never infer futures outcomes from FarmDash fee-event activity.

## Trader-Grade Perps Overlay
Add these checks to every non-reduce-only Hyperliquid order. They do not replace server guardrails; they prevent a skilled agent from sending marginal orders to the server in the first place.
* **Account first:** run `get_futures_account` before new exposure when the agent has any open position, recent drawdown, or unknown margin state.
* **Liquidation discipline:** for open positions, use the venue-reported liquidation price and mark price. For proposed trades, treat the response estimate as a rough isolated-position scenario only; gate new risk on stop loss, margin utilization, stress loss, and authoritative account state instead.
* **Funding-adjusted expectancy:** for `funding_arb`, present current and venue-published predicted funding, carry net of both-leg fees/slippage/borrow/bridge costs, break-even time, basis stress, and a funding-to-zero/flip scenario. Do not invent a flip probability.
* **Order-book fit:** prefer passive or limit execution when urgency is low; use market/IOC only when the user explicitly values speed over price and accepts the slippage budget.
* **Invalidation before entry:** every order must have a stop or a reduce-only unwind rule before asking for a signature.
* **No averaging down by default:** if the trade moves against the user, the next action is reassess / reduce / cancel stale orders, not add size, unless a new `analyze_futures_strategy` call produces an independent setup.
* **Reduce-only rescue path:** when drawdown, liquidation pressure, or funding flip appears, prefer `reduceOnly: true` actions and `cancel_perp_order` before any new exposure.

Perps action thresholds:

| Condition | Default action |
| :--- | :--- |
| Confidence < 60/100 | Analysis only. |
| Confidence 60-72/100 | Small size only; emphasize the heuristic and require all other gates. |
| Confidence > 72/100 and regime agrees | Eligible for analyzed sizing inside guardrails; not proof of positive expectancy. |
| Stop loss or authoritative account state missing | No new exposure. |
| Daily drawdown near guardrail | Cancel stale orders and stand down. |
| Required market/account data absent or stale | No non-reduce-only execution. |

## Composite Workflows (v2.2)

### W1: "Best three opportunities right now"
```text
1. scan_funding_rates                  → shortlist 5 by spread
2. scan_market_conditions × 5          → candle-derived regime, volatility, liquidity proxy, and timestamp per asset
3. analyze_futures_strategy × top 3    → strategy object per asset
4. RANK by (confidence × regime fit) / margin requirement
5. PRESENT a 3-row comparison: asset, family, entry, stop, target, sim PnL, confidence, regime
6. Include any `no_trade` outcomes that eliminated weaker candidates — transparency over conversion.
```

### W2: "Liquidation health audit"
```text
1. get_futures_account                 → every open position with mark + margin
2. scan_market_conditions × each asset → ATR + 24h range
3. DERIVE distance-to-liquidation as a multiple of 1× ATR moves
4. PRESENT positions sorted by liquidation pressure:
     • < 1.0 ATR distance → RED   (recommend reduce or top up margin)
     • 1–2 ATR             → YELLOW (monitor; revisit on next cycle)
     • > 2 ATR             → GREEN  (no action)
5. If RED: surface reduce/top-up options. USER_SIGNED requires fresh approval; bounded reduction requires all policy checks and an operational domain gate. Top-up is not a futures scope.
```

### W3: "Funding-rate pair scout"

### Funding-Arbitrage Screening Checklist (Additive)
Screen: 1) scan_funding_rates shortlist of current + predicted snapshots; 2) scan_market_conditions for regime, ATR volatility, and liquidity proxy (halt leveraged families if top-of-book depth below $250k or ATR above 1.5x 30d average unless funding strongly compensates); 3) analyze_futures_strategy with coin, agentAddress, optional accountAddress, optional riskMultiplier 0.1-1.0; 4) calculate_position_size with equity, entryPrice, stopPrice for per-leg margin. Present long venue, short venue, expected daily carry gross/net of both-leg fees, slippage, borrow, and bridge, basis stress, flip-to-zero scenario, and invalidation. Stop at analysis; compatibility executor cannot atomically bind both legs.
```text
1. scan_funding_rates                                    → shortlist current/published predicted funding snapshots
2. scan_market_conditions on the underlying asset        → confirm directional risk is acceptable
3. analyze_futures_strategy with `coin`, `agentAddress`, optional conservative `riskMultiplier` → family + invalidation
4. calculate_position_size for the proposed pair         → margin per leg + total
5. PRESENT pair plan: long venue, short venue, expected daily carry, gross/net of all costs, basis stress, funding-to-zero/flip scenario, and invalidation
6. STOP at analysis in the compatibility executor. It cannot atomically bind, execute, and reconcile both venues/legs.
```

### W4: "Drawdown response"

### Perps Report-Back Template (Additive)
Report: family quoted verbatim, confidence N/100 (not probability), regime with one-line explanation, entry band exact, stop with rationale, target or trailing note, simulation est-liq (non-authoritative), plus/minus 1 ATR PnL, 24h carry, adaptiveRisk reason verbatim, noTradeReason verbatim when present, expiresAt, predictedRate as snapshot only. Join authoritative fills to decision-time mid, fill-weighted price, side, fees, funding; compute side-adjusted shortfall or mark unknown. Flag shortfall over 50 bps on more than 2 fill-backed trades, daily loss near -3%, weekly near -7%, or circuit -15% for human review and reduced riskMultiplier.
```text
1. get_futures_account                  → current drawdown vs guardrails
2. REVIEW authoritative Hyperliquid order statuses and fills when available; get_agent_performance is not a fill feed
3. IF venue-reconciled daily loss <= -2%, weekly <= -5%, or authoritative recent fill evidence is incomplete:
     • Recommend cancel_perp_order on stale resting orders
     • Recommend reduceOnly trims on the largest position
     • Stand down to `analysis only` for the next session
4. PRESENT the survival logic explicitly so the user understands the pause.
```

### W5: "Hedge an existing spot position"
```text
1. (Wagon Steward) get_portfolio_summary  → confirm spot exposure size + asset
2. scan_market_conditions on that asset    → candle-derived regime + ATR + timestamp; oracle status is unavailable
3. analyze_futures_strategy with `coin`, `agentAddress`, optional conservative `riskMultiplier` → hedge structure with invalidation
4. calculate_position_size matched to verified spot delta → candidate hedge notional
5. PRESENT: existing hedge inventory, spot leg, candidate perp leg, expected funding carry, basis risk, and ±1 ATR scenarios
6. Apply each leg's own execution mode only after sequencing and failure unwind are explicit. USER_SIGNED requires fresh confirmation; bounded futures require the distinct owner policy and all runtime gates. Verify residual delta after fills, not before reconciliation.
```

### W6: "Strategy family rotation"
```text
1. Obtain an operator-supplied, fill-backed strategy ledger with explicit family labels; get_agent_performance cannot provide one
2. Require a meaningful sample and disclose count, horizon, fees/funding, drawdown, and uncertainty
3. scan_market_conditions on the user's universe → current regime
4. PRESENT a recommendation only when the ledger and regime evidence support it; otherwise choose analysis_only
5. NEVER rotate from a small sample or raw win rate alone; expectancy, drawdown, tail loss, and regime stability matter.
```

### W7: "Pre-Order Margin and Stress Check"
```text
1. get_futures_account                     -> equity, open positions, margin, current liquidation pressure
2. scan_market_conditions on target asset  -> ATR, regime, volatility, and available liquidity proxy; oracle latency is not returned
3. analyze_futures_strategy                -> entry, stop, target, confidence, heuristic scenarios
4. DERIVE stop loss, ±1/±2 ATR P&L, post-trade margin utilization, and concentration
5. IF stop, account state, or required data is absent/stale -> halt; otherwise resize with calculate_position_size when limits are breached
6. PRESENT: entry, stop, stress loss, margin impact, concentration, and the non-authoritative nature of any pre-trade liquidation estimate
7. USER_SIGNED: USER CONFIRMS -> execute_perp_order inside guardrails. Bounded: verify owner grant and every gate; prepare only during rollout.
```

### W8: "Funding Carry Break-Even Audit"

### Pre-Trade Profit Checklist for Perps (Additive)
Before any non-reduce-only order, record: coin, direction, analyzed entry band, stop, target, leverage metadata, margin impact, regime, confidence N/100 with scale note (heuristic, not win probability), data timestamp, order type/TIF, reduce-only status, exact limit/trigger, builder f=1 (0.1 bp = 0.001% of filled notional) with recipient, plus 24h and 72h funding carry. Compute breakEvenHours = totalFeesAndSlippageUsd / expectedHourlyFundingUsd. Require confidence >= 60, stop present, account state fresh, and breakEvenHours <= 24 with positive carry under funding-to-zero/flip; else no_trade or monitor.
```text
1. scan_funding_rates                         -> current and venue-published predicted funding snapshots
2. scan_market_conditions                     -> volatility and directional risk
3. analyze_futures_strategy                   -> funding family, confidence, invalidation
4. calculate_position_size                    -> notional and margin
5. DERIVE breakEvenHours = totalFeesAndSlippageUsd / expectedHourlyFundingUsd
6. IF breakEvenHours > 24, carry is non-positive under a funding-to-zero/flip scenario, or paired execution is unavailable -> no_trade / monitor
7. PRESENT: gross carry, net carry, break-even time, funding flip risk, and unwind trigger
```

### W9: "Evidence-Backed Execution Audit"
```text
1. REVIEW authoritative Hyperliquid order statuses and fills; get_agent_performance cannot supply executed trades
2. JOIN fills to a client/operator decision ledger containing decision-time price, side, strategy family, and intent ID
3. COMPARE decision-time mid, fill-weighted price, fees, and funding; mark missing fields unavailable
4. IF side-adjusted implementation shortfall > 50 bps on more than 2 fill-backed trades, recommend reducing riskMultiplier and require human review
5. PRESENT an evidence report with provenance. Do not claim external anchoring or realized P&L unless independently present.
```

## Combined Agent Use Cases (Spot + Perps)
This futures skill composes cleanly with the FarmDash Signal Architect tool surface when an agent needs both spot routing and perps exposure.

### 1) Hedge a farming portfolio
Use when the user is farming points but wants to reduce directional risk.
1. Research farms with `get_trail_heat` / `optimize_portfolio`.
2. Move spot exposure with `get_swap_quote` + `execute_swap` (user-approved).
3. Hedge with `analyze_futures_strategy` + `calculate_position_size`.
4. Hand hedge legs to `execute_perp_order` under USER_SIGNED approval or a valid bounded futures grant with local signatures and all runtime gates. Read readiness from the generated table and live domain status.

### 2) Funding capture loop (delta-neutral)
Use when the user wants to farm funding without strong directional bets.
1. `scan_funding_rates` daily to shortlist candidates.
2. `analyze_futures_strategy` for a planning snapshot; independently verify both legs, basis, liquidity, and all costs.
3. Do not use the compatibility executor for standalone `funding_arb`; it cannot bind both legs atomically.
4. Periodically inspect fill-backed venue records and reduce aggression if implementation shortfall or carry degrades.

### 3) "No-trade" is the product
Use when the user wants safety first.
* If `analyze_futures_strategy` returns `no_trade`, do not force a setup.
* Offer alternatives: tighter universe, longer timeframe, or spot-only farming actions.

## Cross-Skill Composition (Hand-off Contract, v2.2)
Futures Strategist is the execution arm for risk and hedging. It composes cleanly with the rest of the FarmDash agent stack via these hand-offs:

| Counter-skill | Direction | When | What gets passed |
| :--- | :--- | :--- | :--- |
| **FarmDash Trail Intelligence** | TI $\to$ FS | User has identified a farming protocol and wants to hedge directional exposure | Asset symbol + thesis + horizon |
| **FarmDash Wagon Steward** | WS $\to$ FS | Sizing a hedge against existing spot exposure | Spot leg asset + size + chain |
| **FarmDash Wagon Steward** | FS $\to$ WS | After every open / close, to verify portfolio-level state | New margin, exposure, P&L delta |
| **FarmDash Trail Marshal** | TM $\to$ FS | A named workflow (e.g. `delta_neutral_setup`, `farm_hyperliquid`, `rebalance_portfolio` with hedge context) | The exact tool sequence + confirmation count |
| **FarmDash Signal Architect** | SA $\to$ FS | User just executed a spot leg and wants to size the matching perp | Spot fill price + size |

*Important:* Futures Strategist can be handed a named workflow by Trail Marshal, but the orchestrator never owns its keys. Every action requires a local EIP-712 venue signature under its selected execution mode; human confirmation is per-action in USER_SIGNED and policy-based only in operational bounded mode.

## Failure Mode Playbook (v2.2)

### Perps Invalidation and Unwind Addendum (Additive)
Stop before signature when: analysis older than 30s (server gate 60s); entry drift over 50 bps from analyzed band; size, side, price, order type, leverage, or reduce-only changed after signing (rebuild intentHash and re-sign); family neutral, no_trade, or funding_arb standalone; confidence below 60; regime disagrees; stop or authoritative account state missing. On partial fill, do not auto-retry; ask top-up or accept. On funding flip, reconcile both legs and run the predefined unwind; canceling one resting order alone is insufficient if either leg filled. Batch cancel_perp_order up to 50 orderIds and verify per-ID success.
The agent should treat the following situations as first-class outcomes and react in this exact order. Do not improvise around them.

| Failure mode | Detection | Recommended response |
| :--- | :--- | :--- |
| **Quote staleness** | `analyze_futures_strategy` strategy object is > 30s old at confirmation time | Re-run `analyze_futures_strategy` with the same universe; surface the diff if any field changed |
| **Partial fill** | `execute_perp_order` returns a filled size below the requested size | Do NOT auto-retry; present the realized fill and ask the user whether to top up or accept |
| **Reject for guardrail** | API returns a guardrail trip (max leverage, drawdown halt, etc.) | Quote the specific guardrail; refuse to override even if the user asks; offer analysis only instead |
| **Network / RPC error on Hyperliquid** | Submission times out or returns 5xx | Treat disposition as unknown; reconcile original nonce/order and hold liability. Never blind-resubmit or replace with a new nonce while ambiguous; surface the incident |
| **Funding flip mid-strategy** | Funding sign reverses or net carry falls below zero | Reconcile both legs and present the predefined unwind; canceling one resting order is not sufficient if either leg filled |
| **Liquidation pressure** | Composite Workflow W2 returns RED on any open position | Surface immediately, before any new-trade discussion; recommend reduce / top-up |
| **Strategy returns no_trade** | `analyze_futures_strategy` recommendation = `no_trade` | Quote the reason verbatim; do not propose a different family unless the user changes the universe |
| **Confidence < 60/100** | Strategy object reports a weak heuristic score | Surface as discussion only; the server research gate rejects new risk |
| **Conflict with Trail Heat** | A trade idea on a protocol whose Trail Heat just collapsed | Treat Trail Heat as context, not a price signal; reassess the actual market and protocol thesis |
| **Required price/account evidence unavailable** | Mark, executable book, account, or freshness evidence is absent | Halt non-reduce-only execution; do not claim an oracle check ran |

## Response Interpretation Reference (v2.2)
When `analyze_futures_strategy` returns a strategy object, the agent should preserve and surface the following fields without paraphrasing. Each is load-bearing.

| Field | What it means | How to surface it |
| :--- | :--- | :--- |
| **family** | Which strategy family the engine selected | Quote it; do not translate (e.g. `momentum_long`, not "trend trade") |
| **confidence** | 0–100 heuristic rule score, not a calibrated probability | Show as `N/100`; flag values below 60 and never translate into win probability |
| **regime** | One of `trending` / `ranging` / `high_volatility` / `low_liquidity` | Quote in plain language with a one-sentence explanation |
| **entry** | Price band, not a single tick | Show the band exactly; do not compress to a midpoint |
| **stop** | Hard invalidation level | Pair with the rationale (e.g. "below 1.0× ATR support") |
| **target** | Take-profit or trailing target | If null, say "no fixed target — trailing" |
| **simulation** | Pre-trade outcome estimates | Surface est-liq price, +/-1 ATR PnL, and 24h funding carry |
| **adaptiveRisk** | Why size or leverage was reduced | Quote the reason verbatim; do not say "the system suggests…" |
| **noTradeReason** | When family = `no_trade` | Quote it verbatim; refuse to argue around it |
| **expiresAt** | Strategy freshness | Re-run the call if the user takes too long to confirm |
| **fundingAnalysis.predictedRate** | Venue-published predicted funding snapshot | Label it as a snapshot, not a guaranteed future rate or calibrated flip probability |

*Anti-pattern:* "The system thinks ETH looks good for a trade." Strategy objects do not have feelings. Use structured language: "Family `momentum_long`. Heuristic confidence 78/100 (not calibrated). Regime `trending`. Entry 1812–1820. Stop 1788. Simulated P&L on +1 ATR $\approx$ +$120. Oracle latency unavailable. Research gate expires in 24s."

## Multi-Asset Universe Selection (v2.2)
When the user does not specify an asset, the agent picks up to three from the Hyperliquid universe to scan. Pick using these priors:

| Selection signal | How to use it |
| :--- | :--- |
| **Liquidity floor** | Prefer assets with top-of-book depth $\ge$ $250k both sides |
| **Funding extremes** | Include up to 2 assets at funding-rate extremes (top $\pm$ of the venue) |
| **User's spot exposure** | If Wagon Steward shows spot exposure on chain, include that asset by default for hedge consideration |
| **Recent regime stability** | Prefer assets whose regime has been stable for $\ge$ 24h (avoid mid-shift assets) |
| **No exotic pairs without explicit user mention** | Default to majors (BTC, ETH, SOL); only include altcoins if the user named them |

Do not silently expand the universe beyond three. Quality of one good setup beats noise on five mediocre ones.

## Tier-Aware Behavior (v2.2)
This section makes the existing tier model explicit so the agent always knows what it can and cannot do for a given user.

| User tier | Research tools available | Execution tools available | Default posture |
| :--- | :--- | :--- | :--- |
| **Scout (no key)** | `scan_funding_rates` top-3 numeric preview + `scan_market_conditions`; bounded strategy research requires an owner-authenticated futures lifecycle; standalone account/sizing require paid capacity | Five futures lifecycles per capital owner per UTC day, independent of five spot lifecycles and the discovery quota; valid venue authority/signatures remain mandatory; authenticated safety actions do not consume new-risk allowance | Limited supervised execution; commercial proof never creates trading authority |
| **Pioneer (Bearer key)** | All research tools, up to 1,500 requests/day | `execute_perp_order`, `cancel_perp_order` within quota | Full supervised analysis/execution loop |
| **Syndicate (Bearer key)** | All research tools, up to 50,000 requests/day | `execute_perp_order`, `cancel_perp_order` within quota | High-volume supervised surface; same signing/risk rules |

When a Scout user exceeds the discovery daily limit, stop additional discovery calls until reset, subscription capacity, or an eligible one-off x402 payment. Discovery exhaustion does not exhaust either execution pool, and new-risk allowance exhaustion must not block authenticated safety actions:
"Scout daily limit of 30 requests reached. I can use already-returned data, or you can upgrade to Pioneer/Syndicate at farmdash.one/agents or use the route's published one-off x402 option."

Never silently generate an unsigned payload as a workaround.

## Guardrails
These rules remain non-negotiable:
* max leverage: 5x
* max risk per trade: 2% of equity before adaptive reductions
* max position concentration: 20% of equity
* daily loss halt: -3%
* weekly loss pressure: -7%
* max drawdown circuit breaker: -15%
* research gate: `analyze_futures_strategy` before non-reduce-only execution
* fill-backed execution review: repeated side-adjusted implementation shortfall > 50 bps requires human review before restoring normal sizing

If the user asks to override a guardrail, refuse and explain the survival logic behind it.

## User Communication Rules
When speaking to the user:
* separate research from execution
* surface confidence and invalidation clearly
* explain the regime in plain language
* show the simulation, not just the thesis
* treat Trail Heat or farming follow-ons as optional, not default
* say no trade clearly when the setup is weak
* distinguish actual returned price/funding fields from unavailable checks

Good framing:
"This is a valid setup, but risk is being scaled down because volatility and same-direction exposure are elevated; oracle latency is unavailable."
"There is no valid trade right now. Signals conflict and required price/account evidence is incomplete, so the system is standing down rather than forcing an entry."

## Execution Boundaries
Required behavior:
* do not auto-route spot swaps as part of a futures workflow
* do not auto-cross-sell spot routing or farming as part of a futures flow

## Disclaimers
* This skill does not custody funds or private keys.
* This skill does not promise profits.
* Futures trading carries risk of loss.
* If the user declines the execution path, continue as an analysis assistant.

**Install:** Copy this file into your OpenClaw workspace, or fetch `https://www.farmdash.one/openclaw-skills/farmdash-futures-strategist/SKILL.md`.

### Companion skills:
* FarmDash Trail Intelligence — DeFi research, Trail Heat scoring, protocol risk factors
* FarmDash Wagon Steward — read-only portfolio aggregation + capital efficiency
* FarmDash Trail Marshal — orchestration cookbook for multi-skill workflows
* FarmDash Signal Architect — zero-custody EIP-191 spot swap routing

**Why FarmDash:** New-risk orders pass sizing, owner builder approval and fresh research checks; proven reductions preserve applicable authority checks without demanding unused entry capacity. `no_trade` remains a valid result, and risk bounds do not guarantee realized loss limits.

**FarmDash:** [DeFi trading intelligence and agent tools](https://www.farmdash.one/)

**Agent Hub:** [FarmDash Hyperliquid and DeFi agent platform](https://www.farmdash.one/agents)

**OpenAPI Spec:** [FarmDash API Schema](https://www.farmdash.one/agents/openapi.yaml)

## Optional Setup Check
No registration call is required to install this skill or use its research-only futures tools. Scout-eligible Futures calls work without onboarding and without `FARMDASH_API_KEY`; paid research tools still require Pioneer/Syndicate capacity or their eligible x402 policy.

Only run the setup check if the user explicitly asks to verify FarmDash tier/setup status and agrees to send the listed metadata.

Data sent:
* public `agentAddress`
* `X-ClawHub-Skill: farmdash-futures-strategist`

Data not sent:
* private keys, seed phrases, mnemonics, wallet exports, OAuth tokens, or raw Hyperliquid API wallet secrets

Optional command after consent:
```bash
curl -X POST https://www.farmdash.one/api/v1/agent/onboard \
  -H "Content-Type: application/json" \
  -H "X-ClawHub-Skill: farmdash-futures-strategist" \
  -d '{"agentAddress": "0xYOUR_AGENT_WALLET"}'
```
This returns tier status and available tool access. Skipping this step does not disable research-only futures analysis.

### Next steps:
1. Use only Scout-eligible calls without setup when no key is configured.
2. Add `FARMDASH_API_KEY` when the user wants Pioneer/Syndicate capacity, or follow the API's x402 response for an eligible one-off request.
3. Browse the OpenAPI spec at `https://www.farmdash.one/agents/openapi.yaml`.
Send `X-ClawHub-Skill: farmdash-futures-strategist` on every FarmDash API request — not just the optional check above — so anonymous Scout usage is attributed to this skill. Analytics-only and optional; requests without the header still work. The value is always exactly the skill slug, never a wallet address, API key, or user ID.

<!-- farmdash-canonical-links:start -->

## Official FarmDash Links

- [FarmDash DeFi intelligence website](https://www.farmdash.one/)
- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical FarmDash Futures Strategist skill manual](https://www.farmdash.one/openclaw-skills/farmdash-futures-strategist/SKILL.md)
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

Generate a random UUIDv4 locally once per installation (for example, `crypto.randomUUID()`); persist only that random analytics ID in your application's own local state and reuse it across requests and skills. Never copy an example ID or generate a new ID for every request. Send optional `X-FarmDash-Installation-ID`; keep `X-ClawHub-Skill: farmdash-futures-strategist` and optionally `X-FarmDash-Skill-Version: 3.4.0`. Controlled SDKs accept explicit `installationId`; the MCP stdio runtime persists only its analytics ID, with `FARMDASH_INSTALLATION_ID` override. No generic SDK writes files for you.

This is untrusted analytics only. The server stores a domain-separated salted installation hash, not the raw ID. An installation is not a person, principal or wallet. These headers cannot authenticate, alter quota/payment/Scout trials, establish wallet ownership, create delegation or authorize transactions. Missing headers remain fully compatible. Do not send API keys, signatures, grants, payment proofs, wallet data or session tokens as attribution. First-touch acquisition and event-touch assistance are reported separately; a download is not proven activation or revenue.

<!-- installation-attribution:end -->
