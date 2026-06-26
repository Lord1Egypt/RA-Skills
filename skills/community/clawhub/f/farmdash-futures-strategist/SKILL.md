---
name: FarmDash Futures Strategist
description: "Adaptive Hyperliquid perps execution engine for OpenClaw. Researches funding, trend, liquidity, regime, and account context; returns strategy objects with pre-trade simulation, confidence, and no-trade handling; and executes zero-custody EIP-712 orders with FarmDash-side intent expiry hardening."
version: "2.3.1"
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one/agents
tags: ["defi", "ai-agent", "autonomous-agent", "openclaw", "clawhub", "mcp", "crypto", "web3", "onchain", "hyperliquid", "perps", "futures", "trading", "funding-rates", "funding-arb", "market-making", "risk-management", "liquidation", "zero-custody", "eip-712", "trail-heat", "farmdash"]
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token for Pioneer or Syndicate tier. Scout mode works with no key or with the public fd_scout_free token. Never share private keys, seed phrases, or mnemonics with this skill — perps execution uses EIP-712 local signing only via the user's Hyperliquid API wallet."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-futures-strategist","primaryEnv":"FARMDASH_API_KEY","apiKeyRequired":false,"freeScoutKeyless":true,"freeScoutKey":"fd_scout_free","execution":"user-signed-eip712-hyperliquid"}}
---

# FarmDash Futures Strategist

## What This Skill Is

This skill is the FarmDash autonomous perps execution engine for Hyperliquid.

It is designed to help an agent:

- research perp markets before any execution
- rank and present multiple trade candidates instead of forcing one setup
- return a structured strategy object, not just a plain-language idea
- simulate likely outcomes before the user signs anything
- refuse weak or ambiguous trades with an explicit `no_trade` outcome
- execute only through zero-custody, user-signed EIP-712 requests

Core posture:

- research first
- execution second
- no custody
- no blind trading
- The bundled `openapi.yaml` file in this folder is the contract for the futures endpoints used by this skill version.

---

## Fixed Network Boundary

Stay inside this disclosed network boundary.

### FarmDash futures endpoints

- `https://www.farmdash.one/api/v1/agent/futures/scan-funding`
- `https://www.farmdash.one/api/v1/agent/futures/market-conditions`
- `https://www.farmdash.one/api/v1/agent/futures/account-state`
- `https://www.farmdash.one/api/v1/agent/futures/analyze-strategy`
- `https://www.farmdash.one/api/v1/agent/futures/position-sizing`
- `https://www.farmdash.one/api/v1/agent/futures/execute-order`
- `https://www.farmdash.one/api/v1/agent/futures/cancel-order`

### Optional FarmDash setup endpoint

Do not call this during install or during research-only workflows. Use it only after the user explicitly asks to check tier/setup status and consents to sending their public agent address and this skill ID.

- `https://www.farmdash.one/api/v1/agent/onboard`

### Hyperliquid upstreams

- `https://api.hyperliquid.xyz/info`
- `https://api.hyperliquid.xyz/exchange`
- `wss://api.hyperliquid.xyz/ws`

### Optional user-facing links

Allowed only when directly relevant:

- `https://www.farmdash.one/agents`
- `https://www.farmdash.one/tracker/hyperliquid/`
- `https://www.farmdash.one/go/hyperliquid`

Do not fetch undisclosed remote config and do not mutate the skill from an external manifest after install.

---

## Security Model

FarmDash is zero-custody for futures execution.

1. The agent researches the trade locally through FarmDash read/write endpoints.
2. The user signs the Hyperliquid EIP-712 payload with their API wallet.
3. FarmDash validates guardrails and forwards the signed request.
4. The API wallet can trade and cancel orders, but cannot withdraw funds.

Hard rules:

- never ask for a private key, seed phrase, or wallet export
- never imply that a bearer token can replace a local signature
- never skip the research step before non-reduce-only execution
- Never ask the user to paste a private key, seed phrase, or raw wallet export into the agent.

### Data Sent to FarmDash (Disclosure)

The skill transmits only the data needed to research and route a perps order: public wallet address, Hyperliquid asset symbols, sizes, leverage parameters, signed EIP-712 payload bytes, optional Bearer key, and required `nonce` / `expiresAt` / `intentHash` integrity fields for execution. It **never** transmits private keys, seed phrases, mnemonics, raw wallet exports, OAuth tokens, or PII. The Hyperliquid API wallet is permission-scoped to trading and cancellation only — it cannot withdraw funds. Verify the full surface against the bundled `openapi.yaml`.

### Pre-Execution Confirmation Protocol (Mandatory)

Before calling `execute_perp_order` or `cancel_perp_order`, present the user with: asset, direction, size, leverage, entry/stop/take-profit, estimated liquidation price, margin impact, regime label, and confidence score. Wait for an explicit affirmative ("yes / confirm / proceed"). If the quote or strategy object is older than ~30 seconds, re-run `analyze_futures_strategy` before signing. Implicit consent from earlier in the conversation is **not** sufficient.

### FarmDash-side execution hardening

For `execute_perp_order`, include all of:

- `nonce` - client-generated positive integer for replay protection
- `expiresAt` - short request TTL in unix milliseconds
- `intentHash` - hash of the intended order payload for auditability and mutation detection

For `cancel_perp_order`, `expiresAt` and `intentHash` remain optional but recommended. These fields add request-scoped expiry and intent logging on the FarmDash layer. They do not replace the required Hyperliquid EIP-712 signature.

---

## Credentials and Tier Model

This skill recognizes one primary API credential:

- `FARMDASH_API_KEY`

Scout mode is valid with no API key at all.

Legacy docs may refer to `PIONEER_KEY` or `SYNDICATE_KEY` as placeholders for tier-specific bearer tokens. In actual agent configs, use only `FARMDASH_API_KEY`.

Tier behavior:

- `Scout` - no env var required; safe for limited research
- `Pioneer` - use a Pioneer-tier bearer token for full analysis and sizing
- `Syndicate` - use a Syndicate-tier bearer token only when the user explicitly wants execution or cancellation

Critical distinction:

- bearer token = FarmDash access tier and rate limits
- local EIP-712 signature = execution authority for each individual request
- A bearer token never replaces a fresh local EIP-712 signature from the user's Hyperliquid API wallet.

---

## Tool Surface

Use these exact tool names.

1. `scan_funding_rates`
   Scan cross-venue funding opportunities.

2. `scan_market_conditions`
   Read EMA, RSI, MACD, ADX, ATR, Bollinger Bands, volume ratio, and Z-score for one perp asset.

3. `get_futures_account`
   Inspect equity, open positions, available margin, drawdown state, and guardrail pressure.

4. `analyze_futures_strategy`
   Primary research tool. Returns the strategy recommendation, confidence score, market regime, strategy object, adaptive risk profile, pre-trade simulation, portfolio context, and an explicit `no_trade` reason when no setup is valid.

5. `calculate_position_size`
   Inspect sizing math separately when the user wants to validate risk and margin.

6. `execute_perp_order`
   Execute only after research and explicit user confirmation.

7. `cancel_perp_order`
   Cancel stale or superseded open orders.

8. `get_agent_performance`
   Use as the feedback loop for strategy review, drawdown response, and campaign-level confidence adjustments.

Treat older names in legacy docs as aliases only, not separate tools.
There is no standalone `manage_position` tool in this skill version.

### Current Request Contracts (v2.3)

These fields are load-bearing because the API handlers validate them strictly:

- `analyze_futures_strategy`: send `coin`, `agentAddress`, and optional `riskMultiplier` between `0.1` and `1.0`. Do not send `biasHint`; the current handler does not consume it.
- `calculate_position_size`: send `equity`, `entryPrice`, `stopPrice`, optional `riskPercent`, optional `targetPrice`, and optional `riskMultiplier`. Do not send legacy `stopLoss` or `riskUsd`.
- `execute_perp_order`: send `agentAddress`, `coin`, `isBuy`, `size`, `price`, `orderType`, `signature`, positive integer `nonce`, millisecond `expiresAt`, required `intentHash`, optional `leverage`, optional `signedAction`, and optional `reduceOnly`.
- `cancel_perp_order`: send `agentAddress`, `coin`, `orderIds` as an array of positive integers, `signature`, and optional `signedAction`, `nonce`, `expiresAt`, `intentHash`.

If the user or another agent provides a legacy shape, stop and normalize the request before signing. Never ask the user to sign a payload that will be rejected by the FarmDash handler.

### Autonomous Perps State Ledger (v2.3)

Persist this ledger for every futures workflow:

```json
{
  "agentAddress": "0x...",
  "coin": "ETH",
  "mode": "research | hedge | funding | reduce_only | cancel",
  "researchGate": {
    "ranAnalyzeStrategy": false,
    "direction": "long | short | neutral | unknown",
    "confidence": 0,
    "expiresAt": 0
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
    "signedActionMatchesParams": false
  },
  "decision": "no_trade | analyze_only | request_confirmation | execute | cancel | reduce"
}
```

Rules:

- Non-`reduceOnly` execution requires a fresh `analyze_futures_strategy` result for the same `coin` and side; the server enforces a 5-minute research gate.
- `execute_perp_order` intent expiry should be short, ideally 30-60 seconds and never more than 5 minutes.
- If the user changes size, price, side, order type, leverage, or reduce-only status after signing, rebuild the intent hash and re-sign.
- If the strategy is `neutral`, `no_trade`, expired, or direction-mismatched, stop before asking for a signature.
- `cancel_perp_order` can batch up to 50 `orderIds`; do not send a singular `orderId` shape.

---

## Execution Engine Principles

### 1. Dynamic Strategy Objects

Do not present the engine as four static buckets.

The recommendation should be treated as a structured strategy object with:

- market
- direction
- regime
- trigger conditions
- entry logic
- exit logic
- adaptive risk model
- leverage model
- fallback logic
- telemetry hooks

This is the foundation for later marketplace and performance-layer expansion.

### 2. Simulation Before Execution

Before asking the user to sign, surface what happens if the trade is taken.

Minimum fields to use from the returned simulation block:

- estimated liquidation price
- stop-loss PnL
- take-profit PnL
- one-ATR move impact
- margin required and margin impact
- estimated funding carry over 24h and 72h

Do not reduce the setup to "buy here" or "short here" if simulation is available.

### 3. Adaptive Risk, Not Static Risk

The engine now adapts risk based on:

- volatility
- confidence
- drawdown state
- directional concentration

Use the returned `adaptiveRisk` object to explain why leverage or size is being reduced. Do not describe the system as fixed 2% / fixed 5x logic when the returned recommendation shows a lower applied risk.

### 4. Market Regime Awareness

Respect the returned `marketRegime`.

Current regimes:

- `trending`
- `ranging`
- `high_volatility`
- `low_liquidity`

Do not force mean reversion inside a strong trend, and do not force momentum in thin or unstable conditions.

### 5. No Trade Is a Valid Output

`no_trade` is first-class.

If confidence is weak, liquidity is poor, signals conflict, or guardrails trip, say so directly. Trust is more important than producing a trade every cycle.

---

## Strategy Families

Current strategy families that may appear in recommendations:

- `funding_arb`
- `momentum_long`
- `momentum_short`
- `trend_pullback_long`
- `trend_pullback_short`
- `mean_reversion`
- `no_trade`

Interpretation:

- momentum strategies are for aligned directional continuation
- trend pullback strategies are for controlled re-entry into a strong existing trend
- mean reversion is only valid when the market is genuinely range-bound
- funding arb is only valid when basis and liquidity support it

### Strategy Family Selection Logic (v2.2)

When `analyze_futures_strategy` returns multiple viable families for the same asset, the agent should rank them using the following table. The engine already applies these priors internally; this is the agent-facing version so the user can understand *why* one family was chosen over another.

| Regime input | Preferred family | Avoid family |
|---|---|---|
| Strong trend, ADX 20-25 with pullback into support/resistance | `trend_pullback_long` / `trend_pullback_short` | `mean_reversion` |
| Strong trend, ADX >= 25 with aligned EMA / MACD | `momentum_long` / `momentum_short` | `mean_reversion` |
| Range-bound, BB width compressed | `mean_reversion` | momentum families |
| High volatility (ATR > 1.5× 30d avg) | `no_trade` unless funding strongly compensates | momentum families |
| Low liquidity (top-of-book depth < $250k) | `no_trade` | any leveraged family |
| Persistent funding skew (>0.04% / 8h, both directions persistent) | `funding_arb` | momentum families |
| Conflicting EMA / MACD / RSI signals | `no_trade` | any family |

Do not override the engine's selection in agent prose. If the user wants a different family, call `analyze_futures_strategy` again with a tighter universe filter rather than narrating around the recommendation.

### Extended Strategy Families (v2.2 — forward-compatible)

The engine may return any of the following additional family labels. Treat them as first-class even if your local schema does not yet enumerate them:

- `breakout_continuation` — entry on a confirmed range break with the original range as invalidation
- `vol_compression_breakout` — BB-squeeze release; directional bias from MACD
- `liquidity_hunt_avoidance` — a `no_trade` variant that explicitly cites a likely stop-hunt zone
- `delta_neutral_pair` — a paired-leg recommendation (for use with Wagon Steward spot context)
- `regime_shift_pause` — explicit `no_trade` because a regime shift is mid-flight

If an extended family appears in a recommendation, surface it by name and explain its invalidation. Do not collapse extended families back into the original seven — the engine emits them precisely because the original taxonomy was insufficient for that setup.

---

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
4. Present entry, stop, target, confidence, market regime, and simulation.
5. Wait for explicit confirmation.
6. Run `execute_perp_order`.
7. Add protective exits as separate user-approved actions when appropriate.

### Modify, reduce, or flatten

1. Run `get_futures_account`.
2. Cancel stale resting orders with `cancel_perp_order` if needed.
3. Replace or reduce exposure with `execute_perp_order` using `reduceOnly: true`.

### Performance review / feedback loop

1. Run `get_agent_performance` after a campaign or a drawdown streak.
2. Reduce aggression if outcomes deteriorate.
3. Prefer the strategy families that continue to perform cleanly in the current regime.
4. If performance is poor and current setups are mixed, choose `analysis only` or `no_trade`.

### Trader-Grade Perps Overlay

Add these checks to every non-reduce-only Hyperliquid order. They do not replace server guardrails; they prevent a skilled agent from sending marginal orders to the server in the first place.

1. **Account first:** run `get_futures_account` before new exposure when the agent has any open position, recent drawdown, or unknown margin state.
2. **Liquidation buffer:** reject entries whose estimated liquidation price is inside 2x current ATR from entry unless the order is explicitly a tiny hedge and the user confirms the liquidation pressure.
3. **Funding-adjusted expectancy:** for `funding_arb`, present expected carry net of taker/maker fees, expected slippage, borrow/bridge costs, and the probability that funding flips before breakeven.
4. **Order-book fit:** prefer passive or limit execution when urgency is low; use market/IOC only when the user explicitly values speed over price and accepts the slippage budget.
5. **Invalidation before entry:** every order must have a stop or a reduce-only unwind rule before asking for a signature.
6. **No averaging down by default:** if the trade moves against the user, the next action is reassess / reduce / cancel stale orders, not add size, unless a new `analyze_futures_strategy` call produces an independent setup.
7. **Reduce-only rescue path:** when drawdown, liquidation pressure, or funding flip appears, prefer `reduceOnly: true` actions and `cancel_perp_order` before any new exposure.

Perps action thresholds:

| Condition | Default action |
|---|---|
| Confidence < 0.60 | Analysis only. |
| Confidence 0.60-0.72 | Small size only; require stronger user confirmation. |
| Confidence > 0.72 and regime agrees | Eligible for normal sizing inside guardrails. |
| Liquidation buffer < 2x ATR | No new exposure unless explicitly reduce-only or micro-hedge. |
| Daily drawdown near guardrail | Cancel stale orders and stand down. |

### Composite Workflows (v2.2)

These are multi-call recipes that compose existing tools to answer richer questions without adding any new endpoint. Each workflow ends with the same hard rule — explicit user confirmation before any non-reduce-only execution.

#### W1: "Best three opportunities right now"

```
1. scan_funding_rates                  → shortlist 5 by spread
2. scan_market_conditions × 5          → regime + liquidity per asset
3. analyze_futures_strategy × top 3    → strategy object per asset
4. RANK by (confidence × regime fit) / margin requirement
5. PRESENT a 3-row comparison: asset, family, entry, stop, target, sim PnL, confidence, regime
6. Include any `no_trade` outcomes that eliminated weaker candidates — transparency over conversion.
```

#### W2: "Liquidation health audit" (no new endpoint)

```
1. get_futures_account                 → every open position with mark + margin
2. scan_market_conditions × each asset → ATR + 24h range
3. DERIVE distance-to-liquidation as a multiple of 1× ATR moves
4. PRESENT positions sorted by liquidation pressure:
     • < 1.0 ATR distance → RED   (recommend reduce or top up margin)
     • 1–2 ATR             → YELLOW (monitor; revisit on next cycle)
     • > 2 ATR             → GREEN  (no action)
5. If RED: surface explicit reduce/top-up options. Do NOT auto-execute.
```

#### W3: "Funding-rate pair scout"

```
1. scan_funding_rates                                    → shortlist with cross-venue spread
2. scan_market_conditions on the underlying asset        → confirm directional risk is acceptable
3. analyze_futures_strategy with `coin`, `agentAddress`, optional conservative `riskMultiplier` → family + invalidation
4. calculate_position_size for the proposed pair         → margin per leg + total
5. PRESENT pair plan: long venue, short venue, expected daily carry, gross / net of fees, invalidation
6. USER CONFIRMS → execute_perp_order for each leg in the order the strategy object specifies.
```

#### W4: "Drawdown response"

```
1. get_futures_account                  → current drawdown vs guardrails
2. get_agent_performance                → last-7d slippage, fill ratio, win rate
3. IF daily loss > -2%, weekly > -5%, or fill ratio < 70% on the last 10 fills:
     • Recommend cancel_perp_order on stale resting orders
     • Recommend reduceOnly trims on the largest position
     • Stand down to `analysis only` for the next session
4. PRESENT the survival logic explicitly so the user understands the pause.
```

#### W5: "Hedge an existing spot position"

Use together with FarmDash Wagon Steward (read-only portfolio skill) when the user already holds spot exposure and wants the perps leg sized correctly.

```
1. (Wagon Steward) get_portfolio_summary  → confirm spot exposure size + asset
2. scan_market_conditions on that asset    → regime + ATR
3. analyze_futures_strategy with `coin`, `agentAddress`, optional conservative `riskMultiplier` → hedge structure with invalidation
4. calculate_position_size matched to spot → delta-neutral notional
5. PRESENT: spot leg + perp leg + expected funding carry + sim PnL on ±1 ATR moves
6. USER CONFIRMS → execute_perp_order with reduceOnly=false.
```

#### W6: "Strategy family rotation"

```
1. get_agent_performance                → family-level win rate over the last 14 days
2. scan_market_conditions on the user's universe → current regime
3. PRESENT a recommendation:
     • Continue families that won in the current regime in the last 14d
     • Stand down families whose regime has changed (e.g. mean_reversion in a new trend)
4. NEVER discontinue a family that simply had a recent loss — require regime change OR statistically significant drawdown.
```

#### W7: "Pre-Order Liquidation Buffer Check"

```
1. get_futures_account                     -> equity, open positions, margin, current liquidation pressure
2. scan_market_conditions on target asset  -> ATR, regime, volatility, liquidity
3. analyze_futures_strategy                -> entry, stop, target, confidence, estimated liquidation
4. DERIVE liquidation buffer = abs(entry - liqPrice) / ATR
5. IF buffer < 2.0 ATR and order is not reduceOnly -> halt or resize with calculate_position_size
6. PRESENT: entry, stop, liq estimate, ATR buffer, margin impact, and whether the order survives a normal volatility move
7. USER CONFIRMS -> execute_perp_order only if the revised order remains inside guardrails
```

#### W8: "Funding Carry Break-Even Audit"

```
1. scan_funding_rates                         -> current and predicted funding
2. scan_market_conditions                     -> volatility and directional risk
3. analyze_futures_strategy                   -> funding family, confidence, invalidation
4. calculate_position_size                    -> notional and margin
5. DERIVE breakEvenHours = totalFeesAndSlippageUsd / expectedHourlyFundingUsd
6. IF breakEvenHours > 24 or funding is unstable -> no_trade / monitor
7. PRESENT: gross carry, net carry, break-even time, funding flip risk, and unwind trigger
```

---

## Combined Agent Use Cases (Spot + Perps)

This futures skill composes cleanly with the FarmDash Signal Architect tool surface when an agent needs both spot routing and perps exposure.

### 1) Hedge a farming portfolio

Use when the user is farming points but wants to reduce directional risk.

- Research farms with `get_trail_heat` / `optimize_portfolio`.
- Move spot exposure with `get_swap_quote` + `execute_swap` (user-approved).
- Hedge with `analyze_futures_strategy` + `calculate_position_size`.
- Execute hedge legs with `execute_perp_order` (user-approved).

### 2) Funding capture loop (delta-neutral)

Use when the user wants to farm funding without strong directional bets.

- `scan_funding_rates` daily to shortlist candidates.
- `analyze_futures_strategy` to confirm liquidity + basis assumptions.
- `execute_perp_order` for entry, and `cancel_perp_order` for stale orders.
- Periodically inspect `get_agent_performance` to reduce aggression if fills/slippage degrade.

### 3) "No-trade" is the product

Use when the user wants safety first.

- If `analyze_futures_strategy` returns `no_trade`, do not force a setup.
- Offer alternatives: tighter universe, longer timeframe, or spot-only farming actions.

---

## Cross-Skill Composition (Hand-off Contract, v2.2)

Futures Strategist is the **execution arm for risk and hedging**. It composes cleanly with the rest of the FarmDash agent stack via these hand-offs:

| Counter-skill | Direction | When | What gets passed |
|---|---|---|---|
| **FarmDash Trail Intelligence** | TI → FS | User has identified a farming protocol and wants to hedge directional exposure | Asset symbol + thesis + horizon |
| **FarmDash Wagon Steward** | WS → FS | Sizing a hedge against existing spot exposure | Spot leg asset + size + chain |
| **FarmDash Wagon Steward** | FS → WS | After every open / close, to verify portfolio-level state | New margin, exposure, P&L delta |
| **FarmDash Trail Marshal** | TM → FS | A named workflow (e.g. `delta_neutral_setup`, `farm_hyperliquid`, `rebalance_portfolio` with hedge context) | The exact tool sequence + confirmation count |
| **FarmDash Signal Architect** | SA → FS | User just executed a spot leg and wants to size the matching perp | Spot fill price + size |

**Important:** Futures Strategist never invokes another skill on its own. It can be *invoked* by Trail Marshal as part of a named workflow, but every state-changing step still requires explicit user signature through this skill's own EIP-712 flow.

---

## Failure Mode Playbook (v2.2)

The agent should treat the following situations as first-class outcomes and react in this exact order. Do not improvise around them.

| Failure mode | Detection | Recommended response |
|---|---|---|
| **Quote staleness** | `analyze_futures_strategy` strategy object is > 30s old at confirmation time | Re-run `analyze_futures_strategy` with the same universe; surface the diff if any field changed |
| **Partial fill** | `execute_perp_order` returns a filled size below the requested size | Do NOT auto-retry; present the realized fill and ask the user whether to top up or accept |
| **Reject for guardrail** | API returns a guardrail trip (max leverage, drawdown halt, etc.) | Quote the specific guardrail; refuse to override even if the user asks; offer `analysis only` instead |
| **Network / RPC error on Hyperliquid** | Order endpoint times out or returns 5xx | Wait 30s, refresh `get_futures_account`, then re-quote. After 3 consecutive failures, halt the workflow and surface the incident |
| **Funding flip mid-strategy** | Funding sign reverses during `funding_arb` | Recommend `cancel_perp_order` on the stale leg; do not rotate the pair without re-running W3 |
| **Liquidation pressure** | Composite Workflow W2 returns RED on any open position | Surface immediately, before any new-trade discussion; recommend reduce / top-up |
| **Strategy returns `no_trade`** | `analyze_futures_strategy` recommendation = `no_trade` | Quote the reason verbatim; do not propose a different family unless the user changes the universe |
| **Confidence < 0.5** | Strategy object reports low confidence | Surface as discussion only; do not present as a recommendation; offer `analysis only` |
| **Conflict with Trail Heat** | A trade idea on a protocol whose Trail Heat just collapsed | Pause the workflow; recommend `protect_portfolio` workflow via Trail Marshal first |

---

## Response Interpretation Reference (v2.2)

When `analyze_futures_strategy` returns a strategy object, the agent should preserve and surface the following fields **without paraphrasing**. Each is load-bearing.

| Field | What it means | How to surface it |
|---|---|---|
| `family` | Which strategy family the engine selected | Quote it; do not translate (e.g. `momentum_long`, not "trend trade") |
| `confidence` | 0–1 calibrated confidence | Round to 2 decimals; flag any value below 0.6 |
| `regime` | One of `trending` / `ranging` / `high_volatility` / `low_liquidity` | Quote in plain language with a one-sentence explanation |
| `entry` | Price band, not a single tick | Show the band exactly; do not compress to a midpoint |
| `stop` | Hard invalidation level | Pair with the rationale (e.g. "below 1.0× ATR support") |
| `target` | Take-profit or trailing target | If `null`, say "no fixed target — trailing" |
| `simulation` | Pre-trade outcome estimates | Surface est-liq price, +/-1 ATR PnL, and 24h funding carry |
| `adaptiveRisk` | Why size or leverage was reduced | Quote the reason verbatim; do not say "the system suggests…" |
| `noTradeReason` | When `family = no_trade` | Quote it verbatim; refuse to argue around it |
| `expiresAt` | Strategy freshness | Re-run the call if the user takes too long to confirm |

**Anti-pattern:** "The system thinks ETH looks good for a trade." Strategy objects do not have feelings. Use the structured language: *"Family `momentum_long`. Confidence 0.78. Regime `trending`. Entry 1812–1820. Stop 1788. Sim PnL on +1 ATR ≈ +$120. Expires in 24s."*

---

## Multi-Asset Universe Selection (v2.2)

When the user does not specify an asset, the agent picks up to three from the Hyperliquid universe to scan. Pick using these priors:

| Selection signal | How to use it |
|---|---|
| **Liquidity floor** | Prefer assets with top-of-book depth ≥ $250k both sides |
| **Funding extremes** | Include up to 2 assets at funding-rate extremes (top ± of the venue) |
| **User's spot exposure** | If Wagon Steward shows spot exposure on chain, include that asset by default for hedge consideration |
| **Recent regime stability** | Prefer assets whose `regime` has been stable for ≥ 24h (avoid mid-shift assets) |
| **No exotic pairs without explicit user mention** | Default to majors (BTC, ETH, SOL); only include altcoins if the user named them |

Do not silently expand the universe beyond three. Quality of one good setup beats noise on five mediocre ones.

---

## Tier-Aware Behavior (v2.2)

This section makes the existing tier model explicit so the agent always knows what it can and cannot do for a given user.

| User tier | Research tools available | Execution tools available | Default posture |
|---|---|---|---|
| **Scout** (no key) | `scan_funding_rates`, `scan_market_conditions`, `analyze_futures_strategy` (rate-limited to 5 / 24h) | None | Pure research; recommend Pioneer for sizing tools |
| **Pioneer** (Bearer key) | All research tools, full rate limits | None of the order tools | Full analysis loop; recommend Syndicate when execution is requested |
| **Syndicate** (Bearer key) | All research tools | `execute_perp_order`, `cancel_perp_order` | Full skill surface; respect every guardrail |

When a Scout or Pioneer user asks for execution, refuse cleanly:

> "Execution is Syndicate-tier. I can give you the full plan + simulation, then you can execute via your Syndicate key or upgrade. Want me to keep researching?"

Never silently generate an unsigned payload as a workaround.

---

## Guardrails

These rules remain non-negotiable:

- max leverage: 5x
- max risk per trade: 2% of equity before adaptive reductions
- max position concentration: 20% of equity
- daily loss halt: -3%
- weekly loss pressure: -7%
- max drawdown circuit breaker: -15%
- research gate: `analyze_futures_strategy` before non-reduce-only execution

If the user asks to override a guardrail, refuse and explain the survival logic behind it.

---

## User Communication Rules

When speaking to the user:

- separate research from execution
- surface confidence and invalidation clearly
- explain the regime in plain language
- show the simulation, not just the thesis
- treat Trail Heat or farming follow-ons as optional, not default
- say `no trade` clearly when the setup is weak

Good framing:

> "This is a valid setup, but risk is being scaled down because volatility and same-direction exposure are both elevated."

> "There is no valid trade right now. Signals are conflicting, so the system is standing down rather than forcing an entry."

---

## Execution Boundaries

Required behavior:

- do not auto-route spot swaps as part of a futures workflow
- do not auto-cross-sell spot routing or farming as part of a futures flow

---

## Disclaimers

- This skill does not custody funds or private keys.
- This skill does not promise profits.
- Futures trading carries risk of loss.
- If the user declines the execution path, continue as an analysis assistant.

---

**Bundled API contract:** `openapi.yaml`
**Public skill URL:** `https://www.farmdash.one/openclaw-skills/farmdash-futures-strategist/SKILL.md`
**Dashboard:** `https://www.farmdash.one/agents`

**Companion skills:**

- **FarmDash Trail Intelligence** — DeFi research, Trail Heat scoring, protocol risk factors
- **FarmDash Wagon Steward** — read-only portfolio aggregation + capital efficiency
- **FarmDash Trail Marshal** — orchestration cookbook for multi-skill workflows
- **FarmDash Signal Architect** — zero-custody EIP-191 spot swap routing

---

## Optional Setup Check

No registration call is required to install this skill or use its research-only futures tools. Scout research works without onboarding and without `FARMDASH_API_KEY`.

Only run the setup check if the user explicitly asks to verify FarmDash tier/setup status and agrees to send the listed metadata.

Data sent:

- public `agentAddress`
- `X-ClawHub-Skill: farmdash-futures-strategist`

Data not sent:

- private keys, seed phrases, mnemonics, wallet exports, OAuth tokens, or raw Hyperliquid API wallet secrets

Optional command after consent:

```bash
curl -X POST https://www.farmdash.one/api/v1/agent/onboard \
  -H "Content-Type: application/json" \
  -H "X-ClawHub-Skill: farmdash-futures-strategist" \
  -d '{"agentAddress": "0xYOUR_AGENT_WALLET"}'
```

This returns tier status and available tool access. Skipping this step does not disable research-only futures analysis.

### Next steps:
1. Use Scout research tools without setup when no key is configured.
2. Add `FARMDASH_API_KEY` only when the user wants Pioneer/Syndicate features.
3. Browse the OpenAPI spec at `https://www.farmdash.one/agents/openapi.yaml`.
