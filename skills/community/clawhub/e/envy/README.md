# Envy Trading System

Non-custodial AI trading agent for crypto perpetual futures. Built on 86M+ data points, 85 orthogonal indicators across 7 dimensions, and a signal engine rooted in nonlinear dynamics and chaos theory.

**Your keys. Your wallet. Your strategies. Open source.**

---

## Install

Requires [OpenClaw](https://docs.openclaw.ai/install) and Node.js 22+.

```bash
npx clawhub@latest install envy
```

Restart OpenClaw. Done.

---

## Quick Start

In OpenClaw chat:

```
"Set me up for trading"
```

The agent handles everything — subscription, portfolio, signals, strategies, and starts paper trading.

### With a referral code (free 14-day trial + 50 credits):

```
"Redeem referral code XXXX and set me up for trading"
```

### Manual setup:

```
1. "Check my subscription status"
2. "Open a common signal pack for BTC"
3. "Assemble a BTC strategy in normal mode"
4. "Start the monitor"
5. "Check my positions"
```

---

## Go Live on Hyperliquid

Paper trading runs by default. When you're ready for real money:

### 1. Install the Hyperliquid skill

```bash
npx clawhub@latest install hyperliquid
```

### 2. Export your wallet

Run in your terminal (not in chat):

```bash
cd ~/.openclaw/workspace/skills/envy && node envy.js wallet
```

This shows your mnemonic and private key. Import the private key into MetaMask.

### 3. Fund your account

Deposit funds to [Hyperliquid](https://app.hyperliquid.xyz) using MetaMask. The wallet address is the same one Envy uses for subscriptions — one wallet for everything.

### 4. Switch to live

In OpenClaw chat:

```
"Switch to live trading on Hyperliquid"
```

The agent updates `controller.yaml` and restarts the controller. It reads your wallet automatically from `wallet.json` — no environment variables to configure.

### Or manually:

Edit `controller.yaml`:

```yaml
executor: hyperliquid
```

Restart the controller.

---

## Why This Is Different

A typical trading signal is an entry detector. It checks a condition and fires.

Envy signals are different. Each signal is a self-contained regime predicate — it encodes not just what to look for, but a complete hypothesis about when its own logic is valid. It fires only when multiple independent dimensions of market state simultaneously satisfy that hypothesis. In all other states, it stays silent.

The system operates across 13+ mathematically derived market regimes — coordinates in Hurst × Lyapunov × DFA phase space. Some of these regimes don't have human names. They are more precise than "bull" or "bear" or "volatile." Signals are built to target specific regimes, not to work across all of them.

This is why Sharpe ratios hold over 365 days. The edge is regime recognition — not entry optimization.

---

## The Perception Layer

Price is a chaotic stochastic process — sometimes predictable, sometimes genuinely random. Envy measures market state continuously across 7 independent dimensions:

**Chaos** — the mathematical foundation. Hurst exponent, DFA, Lyapunov exponents, and strange attractor destabilization measure when price is predictable at all. Linear TA indicators are approximations of a nonlinear system — valid in some regimes, meaningless in others. The chaos layer tells the system which is which.

**Technical & TechnicalRaw** — price structure, momentum, and volatility across multiple timeframes, including unsmoothed microstructure derivatives.

**Social** — analyst, influencer, and crowd sentiment tracked as independent cohorts. The system measures not just sentiment direction but divergence between groups — when analysts and crowd disagree, that disagreement is itself a signal. When PAXG analysts turn bullish before a gold rally, that shows up here before it shows up in price.

**CrossAsset** — rolling BTC correlation across 7-day and 30-day windows with delta tracking. Detects when a coin decouples from the market — driven by coin-specific factors — versus when it's just following crypto broadly.

**Predictor** — Doji resolution dynamics. Rather than treating doji candles as a binary pattern, the system tracks resolution accuracy, accuracy velocity, and distance from baseline — turning a simple candlestick signal into a continuously scored reliability measure.

85 indicators in total. Correlated features were removed. What remains are independent views of market state, updated every 15 minutes across 40+ coins.

Full indicator list: `GET https://arena.nvprotocol.com/api/claw/indicators`

---

## Envy Hunter — How Signals Are Born

Signals are not hand-crafted. They are discovered by **Envy Hunter**, an automated multi-round pipeline:

```
Round N:
  LLM generates hypotheses using real indicator distributions
      ↓
  Expression parser validates syntax against the indicator set
      ↓
  Parallel backtest across all valid candidates (365 days)
      ↓
  SignalTuner generates structural variants of top performers
      ↓
  Monte Carlo filter — only signals with median positive return survive
      ↓
  Winners feed back into Round N+1 as context
      ↓
  [Separate process] Overfit detector audits all saved signals
```

The critical architectural property: **the overfit detector runs after Envy Hunter completes, as a completely separate process**. The hypothesis generator never sees the overfit score and cannot optimize toward it. This is the same separation used in institutional quant research — generation and validation are structurally isolated.

Each round, the LLM receives feedback on which indicator combinations worked and which failed, allowing it to explore adjacent hypothesis space without repeating failures.

Signals are versioned and forkable — a lineage system that tracks how each signal was derived from its ancestors.

5,524 signals have been scored to date across 40+ coins. The ones that survive are in the packs.

---

## What It Looks Like in Practice

```
You: "Set me up for trading"

Agent: Building portfolio... BTC, ETH, SOL
       Opening signal packs... 30 signals scored
       Assembling strategies...
       ✓ BTC: +47.3% return, 1.82 Sharpe (168 trades, 365 days)
       ✓ ETH: +31.5% return, 1.44 Sharpe (203 trades, 365 days)
       ✓ SOL: +52.8% return, 1.67 Sharpe (189 trades, 365 days)
       Starting paper trader... watching 3 coins, 30 signals

You: "How are my positions?"

Agent: 2 open — BTC LONG +1.2%, ETH SHORT -0.3%
       Daily P&L: +$12.40

You: "Switch to live trading on Hyperliquid"

Agent: Confirmed. Updating executor to hyperliquid...
       Restarting controller with live trading.
       ⚠️ Real funds active. Risk rules unchanged.
```

---

## Engagement Levels

**1. Raw Indicators** — access the live 85-dimension feature matrix directly. Snapshot or time series. Build your own signals, models, or visualizations on top of real data.

**2. Signals** — score your own signal expressions against 365 days of history, or open signal packs (Common / Rare / Legendary) to receive pre-scored signals with backtest metrics, Sharpe, drawdown, and rarity tier.

**3. Per-Coin Strategies** — submit a signal set and the strategy assembler runs a backtest tournament to find the optimal combination. Returns a priority-ordered strategy with full metrics.

**4. Portfolio Balancing** — provide your existing holdings and the optimizer finds additions with minimum return correlation. Constructs a portfolio across 40+ coins designed to reduce regime concentration.

Each level can be used independently or as a full pipeline.

---

## Architecture

```
envy.js (API: indicators, signals, strategies, portfolio)
    ↓
monitor.js (WebSocket, evaluates expressions every 15s, emits transitions)
    ↓
controller.js (risk checks → position sizing → executor)
    ↓
Executor: paper | Hyperliquid (separate skill) | your own
```

---

## Configuration

### Risk Rules — `controller.yaml`

```yaml
executor: paper              # paper | hyperliquid | auto
risk:
  reserve_pct: 20            # keep 20% as cash reserve
  max_positions: 3           # max concurrent open positions
  max_daily_loss_pct: 5      # circuit breaker
  max_hold_hours: 48         # force close after N hours
  entry_end_action: hold     # hold | close when signal lost

allocations:
  BTC: 40
  ETH: 35
  SOL: 25
```

### Executors

| Executor | What it does | Required |
|----------|-------------|----------|
| `paper` | Simulated trading, no real funds (default) | Nothing |
| `hyperliquid` | Live perpetual futures trading | `npx clawhub@latest install hyperliquid` + fund wallet |
| `auto` | Try Hyperliquid, fall back to paper | Nothing |

---

## Signal Events

| Event | Meaning | Controller Action |
|-------|---------|-------------------|
| `ENTRY` | Entry condition just became true | Open position (if risk allows) |
| `ENTRY_END` | Entry condition lost (no exit yet) | Hold or close (configurable) |
| `EXIT` | Exit condition just became true | Close position |

---

## API

Full documentation: `GET https://arena.nvprotocol.com/api/claw/discover`
Pricing: `GET https://arena.nvprotocol.com/api/claw/pricing`

- 40+ perpetual futures coins
- 85 indicators across 7 categories
- 5,524 scored signals with rarity tiers (Common / Rare / Legendary)
- 365-day backtesting with Monte Carlo validation and overfit detection
- Strategy assembly via backtest tournament
- Portfolio optimization via return correlation
- Real-time WebSocket stream (15s updates)
- x402 micropayments + subscription system

---

## License

MIT licensed — free to use, modify, and distribute. See LICENSE for details.
