---
name: polymarket-fast-loop
version: 1.2.0
description: Trade Polymarket BTC 5-minute and 15-minute fast markets using Binance momentum signals, enhanced with TradingAgents pipeline, 50-persona swarm consensus, ACTA receipts, and Cedar governance
category: trading
author: botwave
license: MIT
tags: [polymarket, btc, momentum, fast-markets, simmer, trading-agents, swarm, governance]
dependencies: [simmer-sdk, trading-agents, swarm-consensus, aiohttp, requests]
min_botwave_version: "1.0.0"
capabilities:
  - name: trade_fast_loop
    description: Execute fast-loop trades on Polymarket BTC 5-minute and 15-minute binary markets using CEX momentum signals
    inputs:
      - name: market_id
        description: Polymarket market ID
        type: string
        required: true
      - name: momentum_threshold
        description: Minimum momentum threshold to trigger trade
        type: float
        required: false
        default: 0.001
      - name: volume_filter
        description: Minimum 24h volume in USD
        type: float
        required: false
        default: 10000
      - name: spread_filter
        description: Maximum bid-ask spread percentage
        type: float
        required: false
        default: 0.05
      - name: fee_buffer
        description: Fee multiplier buffer
        type: float
        required: false
        default: 1.5
      - name: position_size_pct
        description: Position size as percentage of bankroll
        type: float
        required: false
        default: 0.05
      - name: max_hold_minutes
        description: Maximum hold time in minutes
        type: integer
        required: false
        default: 5
    outputs: ["trade_result", "pnl", "position_size"]
    permissions: [financial_actions, network_access, read_files]
  - name: get_swarm_decision
    description: Get enhanced decision from 50-persona swarm consensus
    inputs:
      - name: market_data
        description: Market data including momentum, volume, RSI, etc.
        type: object
        required: true
      - name: market_price
        description: Current market implied probability
        type: float
        required: true
    outputs: ["swarm_consensus_prob", "blended_probability", "edge", "kelly_fraction", "recommended_side", "position_size_usd"]
    permissions: [read_files]
---

# Polymarket Fast-Loop Trading Skill

## Purpose
Automated trading on Polymarket BTC 5-minute and 15-minute binary markets using Binance momentum signals, enhanced with:
- **TradingAgents 5-layer pipeline** (Analysts → Research Debate → Trader → Risk → Portfolio Manager)
- **50-Persona Swarm Consensus** (Bayesian aggregation + quarter-Kelly sizing)
- **ACTA Ed25519 Receipts** (IETF draft-farley-acta-signed-receipts-03 compliant)
- **Cedar Policy Governance** (pre/post trade authorization)

## When to Use
- New 5-minute or 15-minute BTC market opens on Polymarket
- Binance BTC/USDT momentum signal exceeds threshold
- Market meets volume, spread, and fee filters

## Workflow
1. **Market Discovery** - Scan Polymarket for active BTC 5m/15m markets
2. **Signal Generation** - Fetch Binance 1m candles, calculate momentum
3. **Filter Application** - Apply volume, spread, fee, momentum thresholds
4. **Enhanced Decision** - Run TradingAgents pipeline + Swarm Consensus
5. **Governance Check** - Cedar policy evaluation + ACTA receipt signing
6. **Trade Execution** - Place trade via Simmer SDK with Kelly sizing
7. **Position Management** - Monitor until expiry, apply stop-loss/take-profit
8. **Outcome Logging** - Record trade with thesis, confidence, outcome

## Configuration
```json
{
  "momentum_threshold_pct": 0.10,
  "volume_filter_usd": 10000,
  "spread_filter_pct": 0.05,
  "fee_buffer": 1.5,
  "position_size_pct": 0.05,
  "max_hold_minutes": 5
}
```

## Integration Points
- Uses `trading_agents.pipeline.TradingAgentsPipeline` for enhanced decisions
- Uses `swarm_consensus.integrate_predictive.PredictiveSwarm` for swarm consensus
- Uses `veritas_receipts.VeritasReceiptSigner` for ACTA receipt signing
- Uses `cedar_policy.CedarPolicyEngine` for policy enforcement
- Emits ACTA receipts for every trade decision
- Logs to prediction-trade-journal for calibration

## Environment Variables
```bash
SIMMER_API_URL=https://api.simmer.markets
SIMMER_API_KEY=<your-api-key>
SIMMER_MOMENTUM_THRESHOLD=0.001
SIMMER_VOLUME_FILTER=10000
SIMMER_SPREAD_FILTER=0.05
SIMMER_FEE_BUFFER=1.5
SIMMER_POSITION_SIZE_PCT=0.05
SIMMER_MAX_HOLD_MINUTES=5
```

## Governance
- All trade decisions emit ACTA Ed25519 receipts (IETF draft-farley-acta-signed-receipts-03)
- Cedar policy engine evaluates pre-trade authorization
- Quarter-Kelly position sizing (max 10% bankroll per trade)
- Hard stop-loss at 5%, take-profit at 10%
- TRADING_VENUE=sim forced for paper trading
- 3-gate safety: TRADING_VENUE=polymarket + --live + SIMMER_MCP_ALLOW_LIVE=true required for live

## Safety
- Only executes when BOTH pipeline and swarm agree on side
- Position size capped at 10% bankroll
- Hard stop-loss at 5% from entry
- Max 3 concurrent trades per tick
- TRADING_VENUE=sim enforced (paper only)