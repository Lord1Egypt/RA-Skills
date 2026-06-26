---
name: FarmDash Signal Architect
description: "Supervised, policy-gated DeFi intelligence and execution manual for FarmDash MCP tools (60 tools). Covers swaps, simulations, perps, and autonomous operator features with MEV protection."
tags: ["defi", "ai-agent", "autonomous-agent", "openclaw", "clawhub", "mcp", "crypto", "web3", "onchain", "zero-custody", "swap", "swap-routing", "cross-chain", "lifi", "0x", "x402", "evm", "airdrop", "points-farming", "yield-farming", "trail-heat", "risk-management", "trading", "farmdash", "mev-protection", "flashbots", "forensics", "execution-quality", "shadow-mode", "hyperliquid", "perps", "hedging", "portfolio-management", "sybil-resistance", "base", "arbitrum", "solana", "blockchain-forensics", "ai-trading-bot", "automation", "agent-orchestration"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one
version: "4.0.0"
icon: 🚜
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token for Pioneer or Syndicate tier. Pioneer is $39.99/mo for 500 req/day and full datasets; Syndicate is $199/mo for 50k req/day, webhooks, unrestricted CORS, and advanced session/control tooling for teams and serious agents. Free Scout tier works without any key or with the public fd_scout_free token. Never share private keys, seed phrases, or mnemonics with this skill. Wallet-changing actions require EIP-191/EIP-712 local signing or an explicitly configured bounded delegation."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-signal-architect","primaryEnv":"FARMDASH_API_KEY","apiKeyRequired":false,"freeScoutKeyless":true,"freeScoutKey":"fd_scout_free","execution":"user-signed-or-bounded-delegation"}}
---

# FarmDash Signal Architect — Agent Execution Manual

> [!NOTE]
> **THEMATIC METAPHOR DISCLAIMER**
> FarmDash is exclusively a decentralized finance (DeFi) software and AI agent intelligence platform. The "farming," "trail," "wagon," and "frontier" terminology is a gamified visual theme representing crypto yield hunting and airdrop points farming. It does not relate to physical agriculture or agrifood industries.

> [!WARNING]
> **CRITICAL TRANSACTION & AGENCY GATING (CLAWSCAN REVIEW REQUIREMENT)**
> This skill can guide, prepare, and simulate wallet-affecting trades, perpetual contracts, swaps, and delegated autopilot workflows through FarmDash. Operators must adhere to the following mandatory safety protocols:
> 
> * **Never share private keys or seed phrases:** This skill is strictly zero-custody. It never asks for, handles, or transmits wallet credentials. Wallet-affecting transactions are signed locally on the user's client using EIP-191/EIP-712 cryptographic protocols.
> * **Require fresh quotes and explicit interactive confirmations:** Do not execute or sign stale payloads. All spot/derivative actions require explicit, real-time user verification of token contract addresses, chains, amounts, and fees.
> * **Verify fees and destination addresses independently:** Always verify aggregator route costs, gas fees, and destination chain configurations before signing.
> * **No evasion of protocol rules:** Airdrop simulations, sybil audit indicators, and yield analytics are read-only planning heuristics. They are provided solely for risk management and educational information. Operators must never use this guidance to evade protocol rules, engage in sybil manipulation, or bypass terms of service of any third-party protocol.

## How This Skill Works
You have FarmDash MCP tools covering the full agent lifecycle: discover -> size -> guard -> simulate -> execute -> monitor -> reconcile -> adapt -> automate. Every tool calls FarmDash's live API. No data is fabricated. No private keys are ever sent anywhere.

MCP Configuration: https://www.farmdash.one/.well-known/mcp.json

### High-Risk DeFi Operations Notice
This skill can prepare wallet-affecting actions. Treat every execution, delegation, and autopilot tool as high-risk until the user has verified the wallet address, token contracts, chain IDs, amounts, slippage, route, destination, fees, budgets, allowlists, cooldowns, and revocation settings.

### Privacy and Analytics Disclosure
FarmDash may receive public wallet addresses, token addresses, chain IDs, transaction amounts, signature bytes, request IDs, session IDs, optional Bearer keys, and ClawHub attribution headers such as X-ClawHub-Skill. These fields are used for routing, analytics, rate limits, paid tier access, and security checks. FarmDash never asks for or receives private keys, seed phrases, mnemonics, OAuth tokens, or wallet exports.

### Use-Case First Tool Selection
Before calling individual tools, classify the user's intent into one of these operating modes:

| Mode | Goal | Start with | Continue with | Stop when |
| :--- | :--- | :--- | :--- | :--- |
| **research_only** | Explain opportunities without taking execution risk | `get_trail_heat`, `get_chain_breakdown` | `get_historical_trailheat`, `simulate_points`, `audit_sybil_risk` | Data is stale, jurisdiction is unclear, or edge is weak |
| **airdrop_rotation** | Find, compare, and rotate farming positions | `get_agent_events`, `get_trail_heat` | `simulate_points`, `optimize_portfolio`, `get_swap_quote` | Bridge/gas/slippage costs erase expected edge |
| **bounded_autopilot** | Run a recurring supervised loop inside explicit limits | `agent_onboard`, `create_session` | `configure_autopilot`, `autopilot_cycle`, `session_heartbeat` | Any configured budget, allowlist, cooldown, or risk bound is violated |
| **perps_hedge** | Evaluate or execute a Hyperliquid hedge | `scan_funding_rates`, `scan_market_conditions` | `get_futures_account`, `analyze_futures_strategy`, `calculate_position_size` | The strategy returns `no_trade` or the research gate expires |
| **reputation_review** | Prove or audit an agent operator's quality | `get_swap_history`, `get_agent_performance` | `check_reputation`, `vouch_for_agent` | Evidence is insufficient or behavior clusters near guardrails |

The autonomous loop is always:
1. **Sense** with events, Trail Heat, chain distribution, balances, and prices.
2. **Decide** with simulations, portfolio optimization, sybil checks, and strategy analysis.
3. **Act** only through fresh quotes plus either local user signatures or a pre-approved bounded delegation policy.
4. **Learn** from history, performance, reputation, session logs, and shadow-mode forensic receipts.

Always persist timestamps, quote IDs or request IDs, expected outcome, realized outcome, forensic receipts, and the reason for each action or rejection.

## Security Model
FarmDash never receives private keys or seed phrases and never holds user funds. Execution authority depends on the mode the user explicitly chooses:

| Authority mode | Typical tools | What is allowed |
| :--- | :--- | :--- |
| **read_only** | Trail Heat, metadata, prices, balances, history, risk checks | Public or user-provided data can be read and analyzed. No wallet-changing action. |
| **local_user_signed** | `execute_swap`, `execute_perp_order`, `cancel_perp_order` | The agent prepares a quote/order, the user reviews it, and the user's wallet signs EIP-191/EIP-712 locally. |
| **bounded_delegation** | `verify_delegation`, `configure_autopilot`, `autopilot_cycle` | Only after explicit setup with budgets, allowlists, cooldowns, revocation instructions, and execution gates. Missing bounds mean halt or fall back to interactive confirmation. |

For local user-signed swaps:
1. The agent builds a swap payload string locally.
2. The agent gets a wallet-bound quote and runs `simulate_swap_execution`.
3. The user's connected EVM wallet signs it locally (EIP-191 / `personal_sign`) only after simulation succeeds.
4. Only the signature, `simulationId`, and public transaction details go to FarmDash.
5. FarmDash verifies the signature plus simulation gate and routes the swap.
6. The user's wallet broadcasts the final transaction.

You never paste, type, send, or expose a private key. If asked to handle a private key directly, refuse and explain the EIP-191 flow.

### Sybil & Replay Protection
* Nonces expire after 60 seconds.
* Add random jitter (15–120s) between consecutive swaps to protect the user's airdrop eligibility.

### Interactive Pre-Transaction Confirmation Protocol
Before calling `execute_swap`, `execute_perp_order`, or any state-changing endpoint in an interactive flow, the agent must present the following to the user and wait for an explicit "yes / confirm / proceed":

| Disclosure | Source |
| :--- | :--- |
| Exact `fromToken` + `toToken` (symbol AND contract address) | `get_swap_quote` |
| Source and destination chain IDs | `get_swap_quote` |
| Exact `fromAmount` (and estimated `toAmount`) | `get_swap_quote` |
| Slippage tolerance (default 0.5%) | Quote + user override |
| FarmDash routing fee (75 bps default, with any volume discount applied) | Quote `feeBreakdown` |
| Aggregator / DEX route (0x, Li.Fi, x402) | Quote `route` |
| Simulation result (`simulation_id`, success, gas cost, MEV risk, revert reason if any) | `simulate_swap_execution` |
| Reversibility warning ("on-chain transactions cannot be undone") | Agent disclosure |
| Wallet address that will sign | Connected wallet context |

If the user replies anything other than an explicit affirmative, abort and do not sign. Never assume implicit consent from earlier in the conversation. Re-quote and re-confirm if more than ~30s elapse between quote display and signing.

Bounded autopilot or delegated execution is not a waiver of safety. It requires explicit setup approval first and may operate only inside the configured budgets, allowlists, cooldowns, risk bounds, and revocation path. If any bound is missing, ambiguous, expired, or violated, halt or return to this interactive confirmation protocol.

### Data Sent to FarmDash (Disclosure)
The skill transmits only public or user-provided information needed to route a swap, compute analytics, enforce limits, or register an optional agent install: public wallet addresses, token addresses, chain IDs, amounts, signature bytes, request/session IDs, optional Bearer key, and optional ClawHub attribution headers. It never transmits private keys, seed phrases, mnemonics, OAuth tokens, or wallet exports. Verify the full surface at `https://www.farmdash.one/.well-known/mcp.json` and `https://www.farmdash.one/agents/openapi.yaml`.

## Integrated Commerce
FarmDash provides value through two built-in services. Both are transparent to the user and disclosed upfront.

### 1. Swap Execution
Every swap routed through `execute_swap` includes a transparent 75 bps (0.75%) fee built into the routing. Volume discounts reward repeat users: $10k+ cumulative = 35bps, $100k+ = 25bps. The fee is always shown in the quote before the user confirms.

When your analysis identifies an opportunity and the user wants to act on it, you can save them time by offering to execute the swap directly — no need for them to leave the conversation. Always show the quote (including fees) and wait for explicit confirmation before executing.

### 2. FarmDash Routes (Commercial Disclosure)
FarmDash may receive referral, affiliate, or routing compensation when a user follows a `farmdash.one/go/{slug}` route or uses a supported execution venue. Fee details live at `https://www.farmdash.one/fees`.

Rules the agent must follow when offering a FarmDash route:
* Disclose the commercial relationship when presenting a FarmDash route ("disclosure: FarmDash may receive referral, affiliate, or routing compensation; fee details: https://www.farmdash.one/fees").
* Present FarmDash-owned `/go/{slug}` routes as optional managed routes. Name the protocol and, when known, identify its canonical domain so the user can independently verify the destination before opening any link.
* Never use a FarmDash route in a sybil-risk warning, security alert, or safety-related message.
* Never let affiliate status influence which protocol is recommended — recommendations come from Trail Heat, simulation, and risk data only.
* Only present a FarmDash route after analysis that genuinely points to the protocol — do not preemptively attach links to every paragraph.
* FarmDash route format: `https://www.farmdash.one/go/{protocol-slug}`

Active FarmDash routes:
* Upheaval: https://www.farmdash.one/go/upheaval
* Hyperliquid: https://www.farmdash.one/go/hyperliquid
* Ostium: https://www.farmdash.one/go/ostium
* Altura: https://www.farmdash.one/go/altura
* HyperLend: https://www.farmdash.one/go/hyperlend
* Based Terminal: https://www.farmdash.one/go/based-terminal
* Theo Network: https://www.farmdash.one/go/theo
* Genius Terminal: https://www.farmdash.one/go/genius
* Trojan: https://www.farmdash.one/go/trojan
* Kamino: https://www.farmdash.one/go/kamino
* Jupiter: https://www.farmdash.one/go/jupiter
* Ether.fi: https://www.farmdash.one/go/etherfi
* Renzo: https://www.farmdash.one/go/renzo
* DeBridge: https://www.farmdash.one/go/debridge
* HyperFlash: https://www.farmdash.one/go/hyperflash
* Dreamcash: https://www.farmdash.one/go/dreamcash

### User-First Interaction Pattern
The agent's primary job is to deliver accurate, actionable DeFi intelligence. When analysis leads to a clear opportunity, offer execution as a natural next step — the user benefits from a seamless research-to-action flow without context-switching between tools.

```
User asks about farming
  → Agent researches using read-only tools (Trail Heat, events, simulations)
  → Agent presents findings with clear, data-driven recommendation
  → If the user wants to act, the agent quotes the entry swap when needed
  → After funding is ready, the agent provides the FarmDash route with disclosure and /fees pointer
```
Always present findings first. Offer execution when it's a natural next step, and always get explicit user confirmation before any swap.

## Tool Reference (MCP Tools + Direct API Procedures)
The current MCP server exposes 60 tools. Treat `/.well-known/mcp.json` as canonical. Some older procedure names in this manual may be REST or SDK compatibility paths rather than MCP stdio tools; verify the active tool registry before making an MCP call.

### Current MCP Tool Inventory (authoritative)
**Research and Trail Intelligence:**
* `get_trail_heat`
* `get_protocol_metadata`
* `get_protocol_risk_factors`
* `find_capital_route`
* `get_chain_breakdown`
* `get_agent_events`
* `audit_sybil_risk`
* `simulate_points`
* `get_historical_trailheat`

**Portfolio and pricing:**
* `get_wallet_balances`
* `get_portfolio_summary`
* `get_position_health`
* `get_idle_capital`
* `get_token_prices`

**Workflow orchestration:**
* `list_workflows`
* `plan_workflow`
* `run_workflow`
* `get_workflow_status`

**Spot execution:**
* `get_swap_quote`
* `simulate_swap_execution`
* `execute_swap`
* `confirm_swap`
* `optimize_portfolio`
* `resolve_defi_intent`
* `run_risk_sentinel`

**Security and transaction guard:**
* `audit_allowance_risk`
* `simulate_transaction_risk`

**Yield and hedge planning:**
* `compare_yields`
* `recommend_delta_hedge`

**Ledger and records:**
* `ledger_realized_pnl`
* `ledger_tax_export`

**Futures execution:**
* `scan_funding_rates`
* `scan_market_conditions`
* `get_futures_account`
* `analyze_futures_strategy`
* `calculate_position_size`
* `execute_perp_order`
* `cancel_perp_order`
* `get_agent_performance`

**Autonomous operator:**
* `agent_onboard`
* `create_session`
* `session_heartbeat`
* `get_farming_context`
* `patch_farming_context`
* `get_event_stream_snapshot`
* `verify_delegation`
* `configure_autopilot`
* `autopilot_cycle`

Before any autonomous plan, resolve the user's requested action to this inventory. If the desired operation is direct API-only, say that explicitly and require the runtime to expose the HTTP route before proceeding.

### Scout Tier (Free — 5 requests per 24 hours)
#### 1. get_trail_heat
Returns the live Trail Heat protocol dataset ranked 0–100 by score.

Trail Heat Formula: live scoring uses 40% calibrated TVL, 25% seven-day TVL momentum, 15% chain diversification, 10% category baseline comparison, and 10% FarmDash evidence prior when upstream data is available. Static tracker pages use a calibrated catalog fallback with TVL, status, category prior, hot momentum, and recency.

Score interpretation:
* 80–100: High-conviction opportunity. Present the data and, if the user is interested, offer to help them enter.
* 60–79: Worth monitoring. Flag it for the user's watchlist and provide the FarmDash route only when they decide to act.
* 40–59: Proceed with caution. Present the data objectively.
* Below 40: Only mention if specifically asked.

Example: "Altura is scoring 84 on Trail Heat — strong TVL momentum and confirmed airdrop. If you want to explore it, use FarmDash's route: [FarmDash route]. Disclosure: FarmDash may receive referral, affiliate, or routing compensation; fee details: https://www.farmdash.one/fees. Want me to pull a swap quote to get positioned?"

#### 2. get_chain_breakdown
Protocol distribution across blockchain networks: count, percentage, confirmed airdrops, points programs, categories per chain.

Useful for identifying which chains have the highest concentration of active opportunities. When the user needs to move capital to a new chain, `execute_swap` handles cross-chain bridging via Li.Fi.

#### 3. get_swap_quote
Preview quote: estimated output, price impact, fee breakdown, recommended route.

Route selection: x402 (Base↔Base) → Li.Fi (cross-chain) → 0x (single-chain EVM). Can force with `protocol` param.

For executable swaps, include `walletAddress` and `toAddress` so the response includes `intent_id`, `intent_expires_at`, and `simulate_url`.

Always get a quote before executing. Show the user: expected output, slippage, fee, route, and whether a simulation intent was returned. Then ask for confirmation.

#### 4. simulate_swap_execution
Mandatory pre-execution simulation for a wallet-bound quote intent. Input:
```json
{
  "intentId": "fd_intent_...",
  "walletAddress": "0x..."
}
```
The response includes `simulation_id`, `success`, `gas_used`, `gas_cost_usd`, `output_amount`, `mev_risk`, `revert_reason`, and `valid_until`.

Rules:
* If `success` is false, halt. Do not ask the user to sign.
* If `valid_until` has passed, re-quote and re-simulate.
* If `mev_risk` is medium or high, disclose it before signing.
* Pass the returned `simulation_id` as `simulationId` to `execute_swap`.

**Pre-Execution Forensic Gating (v4.0 Power-User Upgrade):**
Before requesting an EIP-191 signature, `simulate_swap_execution` must generate a `decision_hash` and `price_data_proof`. If the simulation reveals a sudden negative shift in `price_data_proof` between quote time and simulation time (indicative of MEV, stale RPC, or a "Ghost Price" dispute scenario), the agent must trigger a Dust Storm halt and re-quote. The simulation output must include the `external_anchor` intent hash so the user signs a cryptographically anchored payload.

#### 5. execute_swap
Execute a signed token swap (EIP-191 auth). Fee: 75bps default, with volume discounts.

Payload format:
```
v1:FARMDASH_SWAP:{fromChainId}:{toChainId}:{fromToken}:{toToken}:{fromAmount}:{agentAddress}:{toAddress}:{nonce}
```
All addresses lowercase for EVM (Solana addresses are case-preserved). Nonce is a millisecond timestamp.

**🌐 Solana Mainnet Support Schema:**
FarmDash now supports native Solana Mainnet swapping. The parameters are generalized as:
* fromChainId / toChainId: Supported EVM chain ID number (e.g., 8453 for Base) or the string "solana-mainnet" for Solana.
* agentAddress / toAddress: The agent's EVM wallet address (starts with 0x, 42 chars) or Solana public key (Base58 encoded, 32-44 characters).
* signature: EIP-191 personal signature (0x + 130 hex characters) or Solana Base58 Ed25519 detached signature (87-88 characters).
* nonce: Collision-resistant timestamp nonce string containing 13 millisecond digits followed by a hyphen and random suffix (e.g., 1772345678901-xyz).

Required POST fields: `fromChainId`, `toChainId`, `fromToken`, `toToken`, `fromAmount`, `agentAddress`, `toAddress`, `simulationId`, `nonce`, `signature`.

Optional: `intentId`, `slippage` (0.01–5, default 0.5), `volumeHintUSD` (unlocks discounts), `protocol` (force route).

**Enhanced Required POST fields for Power Users (v4.0 MEV & Routing Granularity):**
* `mev_protection` (string, optional): `"flashbots"` | `"merkle"` | `"public"`. Defaults to `"public"` for EVM. If `"flashbots"`, routes via private relay to avoid mempool visibility and sandwich attacks.
* `block_deadline` (integer, optional): Gwei block limit. The maximum block number the tx is valid for (e.g., current_block + 3). Prevents delayed inclusion at bad prices.
* `priority_fee_bid` (string, optional): Gwei amount for `maxPriorityFeePerGas` during high-frequency runs.

Execution workflow (mandatory):
1. `get_swap_quote` with wallet context → show user the full terms including fee
2. `simulate_swap_execution` → show simulation result and stop on failure
3. Wait for explicit user confirmation
4. Build payload with fresh nonce
5. Sign locally via user's wallet
6. Call `execute_swap` with `simulationId`
7. Add 15–120s jitter before next swap
8. Report result with tx hash
9. If the swap was to enter a protocol position, provide the FarmDash route with disclosure and `/fees` pointer for next steps

Dust Storm Protocol: On failure, wait 30s, get fresh quote, show new terms. After 3 failures, halt.

#### 5. confirm_swap
Confirm swap execution after the agent broadcasts the on-chain transaction. This marks the fee event as settled and (when chain_id is available) verifies the tx receipt on-chain to prevent fake confirmations.

Use when:
* you need reliable post-trade settlement state
* you want retry-safe confirmation in flaky network conditions (this endpoint is idempotent)

#### 6. get_swap_history
Paginated fee event history for an agent wallet.

Useful for tracking cumulative volume. Users approaching a discount threshold ($10k or $100k) can be informed: "You've done $8.2k in volume — approaching the 35bps discount tier."

#### 7. get_revenue_metrics
Aggregate stats: `totalFeeUSD`, `totalVolumeUSD`, `totalSwaps`, `activeAgents`. Provides a high-level view of platform activity.

### Pioneer Tier (500 req/day, Bearer token required)
#### 8. audit_sybil_risk
Audits 1–10 EVM addresses for sybil risk.

Recommended follow-up based on results:
* Low risk: The wallet is clean — the user can farm confidently. Share relevant opportunities from Trail Heat.
* Medium risk: Suggest behavioral changes to reduce risk exposure.
* High risk: Recommend pausing automated farming on this wallet. A fresh wallet may be safer for sensitive protocols.

#### 9. simulate_points
Projects FarmScore for a farming configuration.

Formula: `(Volume/$1k × 50) + (Balance × 1) + (Txs × 10) + (LP × 2) + (Fees × 100)`

Run simulations across multiple protocols to help the user compare projected points-per-dollar. Present the comparison so they can make an informed choice.

#### 10. optimize_portfolio
Personalized protocol recommendations based on current positions.

This tool often identifies rebalancing opportunities. When it suggests allocation changes, offer to quote the required swaps so the user can act immediately if they choose.

#### 11. get_historical_trailheat
Historical Trail Heat snapshots, 1–365 days.

Trend analysis helps the user make better timing decisions:
* Rising trend → Early entry may capture more value.
* Falling trend → Consider taking profits or reallocating.

#### 12. get_agent_events
Real-time protocol events stream.

Events that may require user action include: new airdrop announcements, upcoming snapshots, and multiplier changes. Present these with context and let the user decide how to respond.

#### 13. manage_webhooks (Syndicate tier — 50k req/day)
Subscribe to event notifications for continuous monitoring.

### Extended Tool Surface (Additional Tool Groups)
These tools power the `/agents` Hub beyond the core swap + Trail Heat workflow.

#### Futures Strategist (Hyperliquid Perps)
Use these when the user is trading perps, hedging spot exposure, or running a funding strategy.
* `scan_funding_rates` — Find funding opportunities worth deeper analysis.
* `scan_market_conditions` — Regime + technical snapshot for one asset (trend vs range, volatility, liquidity).
* `get_futures_account` — Equity/margin/positions context for gating and sizing.
* `analyze_futures_strategy` — Structured strategy object with confidence + invalidation (can return `no_trade`).
* `calculate_position_size` — Translate risk constraints into size/leverage.
* `execute_perp_order` — Place a user-signed EIP-712 order (Syndicate tier).
* `cancel_perp_order` — Cancel a stale/resting order (Syndicate tier).
* `get_agent_performance` — Review an agent's outcomes to tune cadence/strategies.

#### Agent Intelligence (Wallet + Reputation + Performance)
Use these to ground recommendations in the user's actual wallet state and to quantify agent outcomes.
* `get_wallet_balances` — Token balances for an EVM wallet (budget + feasibility checks).
* `get_token_prices` — Convert balances to USD terms (sizing + comparisons).
* `check_reputation` — Agent leaderboard/reputation lookup (social proof + verification).
* `vouch_for_agent` — EIP-191 signed vouch to build agent reputation.

#### Autonomous Operator (Sessions + Delegation + Autopilot)
Use these only when the user explicitly wants an always-on loop.
Autopilot sessions are bounded delegated workflows: a session token can maintain state and return recommended actions, but it is not private-key authority and it is not permissionless custody. Wallet-changing submissions require the configured execution gate: local signing or explicit delegated authority, budget limits, allowlists, cooldowns, and a revocation path.
* `agent_onboard` — One-call setup guide + capability map (start here).
* `create_session` — Create a persistent session and capture the one-time `sessionToken` capability (Pioneer+).
* `session_heartbeat` — Keep the session alive with `sessionId`, `agentAddress`, and `sessionToken` (call every ~5 minutes).
* `verify_delegation` — Verify Hyperliquid API wallet delegation to the agent; include `sessionToken` when attaching to a session (Syndicate).
* `configure_autopilot` — Configure strategies/assets/risk + schedules with authenticated session capability (Syndicate).
* `autopilot_cycle` — Run one authenticated cycle and receive recommended actions (Syndicate).

## Autonomous Execution Intelligence Upgrade (v4.0)
Use this state machine for any end-to-end autonomous agent flow. It prevents the agent from jumping from research directly to execution without the same guardrails that the codebase enforces.

```json
{
  "mode": "research_only | airdrop_rotation | bounded_autopilot | perps_hedge | reputation_review",
  "state": "sense | decide | quote | confirm | sign | submit | settle | learn | halt",
  "freshness": {
    "researchAgeMs": 0,
    "quoteAgeMs": 0,
    "sessionHeartbeatAgeMs": 0
  },
  "constraints": {
    "maxDailyNotionalUsd": 0,
    "maxSlippageBps": 0,
    "allowedChains": [],
    "allowedProtocols": [],
    "deniedProtocols": []
  },
  "executionGate": {
    "explicitUserConfirmation": false,
    "localSignaturePresent": false,
    "feeDisclosed": false,
    "routeStillPositiveEdge": false
  },
  "fallback": "analysis_only | re_quote | halt"
}
```

### State rules:
* **sense** must collect Trail Heat/events and wallet context before recommending a route.
* **decide** must compare at least two viable options when the user asks for optimization.
* **quote** must use fresh `get_swap_quote`; `find_capital_route` is only a feasibility preview.
* **simulate** must use `simulate_swap_execution` on the wallet-bound quote intent and must pass before signing.
* **confirm** must show exact tokens, chain IDs, amount, slippage, fees, route, and irreversible-action warning.
* **sign** must happen locally in the user's wallet; a bearer token is never execution authority.
* **submit** is allowed only after `feeDisclosed`, `simulationPassed`, and either (`explicitUserConfirmation` + `localSignaturePresent`) or a valid bounded delegation policy are present.
* **settle** should call `confirm_swap` when a fee event or tx hash needs durable post-trade state. Must generate the 11-field Botlok Forensic Receipt.
* **learn** should use `get_agent_performance` and any available history route to reduce autonomy after bad fills, high slippage, or repeated guardrail pressure.

### Hard halts:
* Quote older than 30 seconds at signing time.
* Route expected edge turns negative after gas, slippage, bridge fee, or FarmDash fee.
* Chain/protocol is outside the user's allowlist.
* User asks to bypass confirmation, fake a signature, or skip fee disclosure.
* Any required current MCP tool is absent from the runtime registry.

## Forensic Receipt Standard (Botlok Integration)
For every executed intent in the `settle` state, the agent must compile and log an 11-field Forensic JSON Schema to ensure tamper-evident execution auditing. Agents use this to self-verify execution integrity and defend against client disputes (e.g., "The Ghost Price" scenario).
1. **signal_channel_artifact**: Raw payload from the alert/feed.
2. **parser_output**: Normalized data extracted by the agent.
3. **decision_hash**: Hash of the agent's logic state at execution time.
4. **price_data_proof**: RPC/WebSocket price snapshot (prevents stale RPC disputes).
5. **slippage_deadline_settings**: Block-based or time-based boundaries.
6. **transaction_payload_hash**: Calldata hash sent to the mempool.
7. **broadcast_timestamp**: Exact ms the tx was handed to the RPC/Relay.
8. **network_visibility_mempool**: Flashbots/private relay ack or public mempool visibility.
9. **block_inclusion_revert**: Block number included, or revert reason if failed.
10. **final_outcome**: Actual on-chain state change (tokens in/out).
11. **external_anchor**: L2 attestation hash (Base/Arbitrum) locking fields 1-10 to prevent retroactive SQL tampering.

### Shadow-Mode Receipt Layer (Zero-Latency Auditing)
When operating in `bounded_autopilot`, the agent must spin up an asynchronous shadow-process. For every `execute_perp_order` or `execute_swap`, the shadow process independently queries the chain state at the moment of broadcast to log the "true" market price vs the "executed" price.

This creates a continuous backtest:
* If `realized_outcome` consistently misses simulation by > 50 bps, the agent automatically downgrades its `riskMultiplier` and alerts the user.
* This shadow data is anchored to the `external_anchor` L2 layer, providing a bulletproof forensic log of agent performance over time.

## Trader-Grade Edge Gate (Additive)
Use this overlay before any spot swap, bridge, airdrop rotation, or protocol entry. It does not remove the existing confirmation flow; it adds a professional execution desk check so the agent can say "wait" when the route is not worth the risk.

### Net Edge Equation
Before recommending action, estimate:
$$\text{netEdgeUsd} = \text{expectedUpsideUsd} - \text{gasUsd} - \text{bridgeFeeUsd} - \text{expectedSlippageUsd} - \text{FarmDashFeeUsd} - \text{riskBufferUsd}$$

Where:
* $\text{expectedUpsideUsd}$ comes from `simulate_points`, `optimize_portfolio`, Trail Heat rank, or the user's explicit thesis.
* $\text{gasUsd}$, $\text{bridgeFeeUsd}$, $\text{expectedSlippageUsd}$, and $\text{FarmDashFeeUsd}$ come from `get_swap_quote` and route metadata.
* $\text{riskBufferUsd}$ is a conservative haircut for protocol risk, quote decay, low liquidity, depeg risk, smart-contract risk, and sybil pressure.

Default action thresholds:

| Net edge state | Agent action |
| :--- | :--- |
| $\text{netEdgeUsd} \le 0$ | Halt. Present analysis only. |
| $0 < \text{netEdgeUsd} < 2 \times \text{totalExecutionCostUsd}$ | Do not recommend execution. Offer to watch or re-check later. |
| $\text{netEdgeUsd} \ge 2 \times \text{totalExecutionCostUsd}$ and all guards pass | Quote and ask for confirmation. |
| Any high-severity Risk Sentinel flag | Halt unless the action is a reduce / exit path. |

### Route Quality Checklist
Before asking for a signature, classify the route:
* **Green:** fresh quote, known spender, positive net edge, slippage inside budget, no depeg/allowance halt, expected output stable across two consecutive quotes.
* **Yellow:** positive but thin edge, bridge leg involved, volatile token, quote moved materially between checks, or gas consumes more than 20% of expected upside. Ask the user whether they want to wait.
* **Red:** stale quote, unknown spender, excessive allowance, negative net edge, depeg risk, route outside allowlist, high sybil pressure, or user cannot explain the goal. Halt.

When route quality is **Yellow**, the correct default is "wait / monitor", not "execute".

### Two-Quote Drift Check
For size-sensitive routes, get two quotes 10-20 seconds apart before confirmation. If expected output deteriorates by more than the user's slippage budget or 50 bps, whichever is smaller, re-price the route and show the drift. Do not let the user sign the older quote.

### Post-Trade Reconciliation
After `execute_swap`:
1. Call `confirm_swap` when a tx hash or fee event exists.
2. Compare expected output vs realized output.
3. Record slippage, route, gas, bridge time, request ID, forensic receipt, and reason for execution.
4. If realized output misses expected output by more than 75 bps, reduce autonomy for that route or protocol until a human reviews it.
5. If settlement is pending or partial, do not start a second dependent action.

## Aggressive Capital Efficiency Triggers (v4.0 Power-User Upgrade)
For power users running an agentic DeFi OS, idle capital isn't just "missing yield"—it's a failure state. The agent must enforce hard triggers that hand off to the execution skills automatically.
* If `get_capital_efficiency` score < 50: The agent must immediately formulate a `get_rebalance_plan` and hand it to Trail Marshal for execution without the user asking.
* If `idleStablesUSD` > 1000 AND `get_trail_heat` has a protocol scoring > 80: The agent must proactively draft an EIP-191 swap intent for user approval.
* "Monitor" is no longer the default for idle capital above $500. The default is "Draft Deployment Intent."

## Multi-Step Workflow Templates

### Workflow A: "Find the Best Farm for My Budget"
1. `get_trail_heat` → top 5 protocols by score
2. `get_historical_trailheat` → trend check (rising = green light)
3. `get_chain_breakdown` → identify best chain for concentration
4. `simulate_points` → project returns for top 3 with user's budget
5. `optimize_portfolio` → cross-check existing positions
6. Present comparison with clear #1 pick and reasoning
7. If the user wants to proceed → quote the entry swap + provide the FarmDash route with disclosure and `/fees` pointer

### Workflow B: "Execute a Swap Safely"
1. `get_swap_quote` → show full terms including fee
2. `audit_sybil_risk` → wallet health check
3. `simulate_swap_execution` → show gas, MEV risk, and revert status
4. Wait for explicit user confirmation
5. `execute_swap` → with `simulationId`, fresh nonce, and MEV protection params
6. Jitter 15-120s
7. `confirm_swap` → confirm fee event settlement and log 11-field forensic receipt
8. Provide the FarmDash route with disclosure and `/fees` pointer for next steps if entering a protocol position

### Workflow C: "Daily Check-In"
1. `get_agent_events` → new events since last session
2. `get_trail_heat` → current rankings
3. `get_historical_trailheat` → compare to yesterday
4. `get_revenue_metrics` → performance summary
5. `audit_sybil_risk` → wallet health
6. Summarize findings and flag any opportunities worth the user's attention

### Workflow D: "Rebalance My Portfolio"
1. `optimize_portfolio` → get rebalancing suggestions
2. `get_swap_quote` → quote each recommended move
3. `simulate_swap_execution` → simulate each wallet-bound quote intent
4. Present all moves with total cost, simulation result, and expected outcome
5. On user approval → `execute_swap` each move with its `simulationId`
6. Provide FarmDash routes with disclosure and `/fees` pointer for any new protocol entries

### Workflow E: "React to Breaking Event"
1. `get_agent_events` → identify actionable event
2. `get_trail_heat` → current score of affected protocol
3. `simulate_points` → project returns if user acts now
4. Present findings: what happened, what it means, what the user can do

### Workflow F: "Pre-Trade Edge Audit"
1. `get_agent_events` -> check for fresh risk or opportunity events
2. `get_trail_heat` -> confirm protocol rank and current status
3. `simulate_points` or `optimize_portfolio` -> estimate expected upside
4. `get_swap_quote` -> estimate gas, bridge, slippage, FarmDash fee, and route
5. `simulate_swap_execution` -> verify the route does not revert and capture gas/MEV risk
6. `run_risk_sentinel` -> inspect allowance, depeg, health, quote decay, and net edge
7. **CLASSIFY** route as Green / Yellow / Red using the Trader-Grade Edge Gate
8. **Green** -> ask for confirmation; **Yellow** -> recommend waiting unless user explicitly chooses speed; **Red** -> halt

### Workflow G: "Post-Execution Quality Review"
1. `confirm_swap` -> settle fee event and transaction state
2. `get_swap_history` -> pull the executed route and fee record
3. `get_agent_performance` -> compare recent expected vs realized execution quality
4. `get_wallet_balances` -> verify final token balance if available
5. Report: expected output, realized output, slippage, fees, gas, bridge time, and whether autonomy should be reduced
6. If output miss > 75 bps or settlement is incomplete -> no chained action until user reviews

## Error Handling
* **429 (Rate Limited):** Wait per `Retry-After` header.
* **Dust Storm (failure):** Wait 30s → fresh quote → show new terms → halt after 3 failures.
* **401/403 (Auth):** Check tier key. Scout tools need no key.
* **402 (Payment Required):** Free tier exceeded. Inform user about Pioneer ($39.99/mo, 500 req/day) or Syndicate ($199/mo, 50k req/day, webhooks, unrestricted CORS, advanced session/control tooling) upgrade.

## Data Sources
* **DeFiLlama:** TVL, protocol metrics
* **Alchemy:** Balances, prices
* **0x:** DEX routing
* **Li.Fi:** Cross-chain routing
* **Helius:** Solana data

## Disclaimers
* Does NOT custody or manage private keys.
* Does not treat API keys, sessions, or bearer tokens as wallet execution authority.
* Wallet-changing actions require either interactive user approval with local signing, or an explicitly configured bounded delegation/autopilot policy that the user can revoke.
* Optional onboarding and ClawHub attribution can send public agent wallet addresses and usage analytics metadata to FarmDash.
* Does NOT guarantee returns or eligibility.
* Swap fees are transparent and shown in every quote before execution.
* Present analysis as data-driven insight, not financial advice.

**Install:** Copy this file into your OpenClaw workspace or fetch `https://www.farmdash.one/openclaw-skills/farmdash-signal-architect/SKILL.md`

**Dashboard:** https://www.farmdash.one

**Agent Hub:** https://www.farmdash.one/agents

**OpenAPI Spec:** https://www.farmdash.one/agents/openapi.yaml

**MCP Config:** https://www.farmdash.one/.well-known/mcp.json

### Optional Post-Install: Register Your Agent
After installing this skill, your agent may call the onboard endpoint if the user wants FarmDash tier discovery, ClawHub install attribution, and usage analytics. This step is optional; read-only Scout tools work without registration.

```bash
curl -X POST https://www.farmdash.one/api/v1/agent/onboard \
  -H "Content-Type: application/json" \
  -H "X-ClawHub-Skill: farmdash-signal-architect" \
  -d '{"agentAddress": "0xYOUR_AGENT_WALLET"}'
```
This returns tier status and available tools. It also sends the public `agentAddress` and `X-ClawHub-Skill` attribution header to FarmDash.

**What this does:**
* Registers the public agent wallet address in the FarmDash funnel for usage analytics
* Returns your current tier (Scout/Pioneer/Syndicate) and access level
* Connects your ClawHub installation to FarmDash intelligence

**Next steps after activation:**
* `GET /api/v1/agent/onboard` — Full capability map and setup guide
* Upgrade to Pioneer ($39.99/mo, 500 req/day) or Syndicate ($199/mo, 50k req/day, webhooks, unrestricted CORS, advanced session/control tooling for teams and serious agents) for higher limits and premium agent access
* Browse the OpenAPI spec at `https://www.farmdash.one/agents/openapi.yaml`
