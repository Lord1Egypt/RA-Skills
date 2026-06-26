---
name: envy
description: "Use when the user asks about crypto indicators, trading signals, backtesting strategies, portfolio optimization, market analysis, starting/stopping the trading monitor, managing positions, checking P&L, configuring risk rules, switching between paper and live trading, or their wallet (mnemonic, private key, seed phrase, MetaMask import, connect wallet). Provides 85M+ data points across technical, social, and chaos indicators for 40+ coins. Score signals with 365-day backtests, assemble optimal strategies via tournament, optimize portfolios by correlation, open signal packs with rarity tiers. Monitors live signals via WebSocket, manages positions with risk rules, and routes trades to paper or Hyperliquid executors. Auto-saves signals and strategies to organized directories. Supports subscription (credits) and x402 micropayments."
metadata: {"openclaw":{"requires":{"bins":["node"]},"primaryEnv":"NVARENA_API_KEY"}}
---

# Envy Trading System — Crypto Trading Infrastructure

Non-custodial AI trading agent for crypto perpetual futures. Access 85M+ data points across technical, social, and chaos indicators for 40+ coins. Score signals, backtest strategies, assemble optimal signal sets via tournament, optimize portfolios by correlation, open signal packs, monitor live signals, manage positions with risk rules, and route trades to executors.

Three components in one skill:
- **envy.js** — API client: indicators, signals, strategies, portfolio, wallet, subscription
- **monitor.js** — Live signal monitor: WebSocket, evaluates expressions every 15s, emits transitions
- **controller.js** — Position manager: risk checks, position sizing, trade routing to paper or Hyperliquid

## Setup

On first use, install dependencies:

```bash
cd {baseDir} && npm install
```

## Data Directory Structure

The CLI auto-creates and manages these directories:

```
{baseDir}/
  signals/       ← raw signals from packs, check, check-inline
  strategies/    ← assembled strategies, ready for the monitor
  archive/       ← old strategies (auto-archived when overwritten)
```

- `pack` → auto-saves to `signals/{coin}_pack_{type}_{timestamp}.yaml`
- `check` / `check-inline` → auto-saves scored signals to `signals/{coin}_{name}.yaml`
- `assemble` → auto-saves to `strategies/{coin}.yaml` (archives old version if exists)
- The signal monitor auto-discovers strategies from `strategies/`

---

## Part 1: Brain (envy.js) — API Client

### Authentication

The CLI supports two auth methods:

1. **API Key (recommended)** — subscription token stored locally. Check with:
```bash
cd {baseDir} && node envy.js status
```

2. **x402 micropayments** — per-request on-chain USDC payments (automatic fallback if no key). Check wallet:
```bash
cd {baseDir} && node envy.js balance
```

If no API key is set, guide the user to get one:
- **Buy subscription**: `cd {baseDir} && node envy.js subscribe` (needs $29.99 USDC in wallet → 30 days + 100 credits)
- **Redeem referral**: `cd {baseDir} && node envy.js referral-redeem --wallet 0xUSER_WALLET --code REFCODE` (free 14 days + 50 credits)
- **Manual key**: `cd {baseDir} && node envy.js set-key nva_...`

### Wallet Safety Rules

**`node envy.js balance`** — SAFE to run in chat. Only outputs the public address and USDC balance. Use this to get the wallet address for referral redemption and other operations.

**`node envy.js wallet`** — NEVER run in chat. Outputs the mnemonic and private key. Always tell the user to run this in their own terminal.

### Commands

#### Free (no auth needed)

```bash
cd {baseDir} && node envy.js discover          # API documentation
cd {baseDir} && node envy.js pricing            # Per-endpoint pricing
cd {baseDir} && node envy.js coins              # Available coins
cd {baseDir} && node envy.js indicators         # All indicators
cd {baseDir} && node envy.js indicators --category Technical
cd {baseDir} && node envy.js cache-status       # Data cache readiness
cd {baseDir} && node envy.js packs-info --coin BTC
cd {baseDir} && node envy.js leaderboard --limit 20
cd {baseDir} && node envy.js referral --wallet 0xUSER_WALLET
cd {baseDir} && node envy.js referral-stats --wallet 0xUSER_WALLET
```

#### Indicator Data (0 credits, subscription-included)

```bash
cd {baseDir} && node envy.js snapshot --coins BTC,ETH,SOL
cd {baseDir} && node envy.js snapshot --coins BTC --indicators RSI_3H30M,ADX_3H30M,CMO_3H30M
cd {baseDir} && node envy.js history --coin BTC --hours 24
cd {baseDir} && node envy.js history --coin ETH --indicators RSI_3H30M,MACD_6H30M_N --hours 12 --page 1 --pageSize 10
```

#### Signal Scoring (1 credit) — auto-saves to signals/

```bash
cd {baseDir} && node envy.js check-inline --coin BTC --name MY_SIG --type LONG --expr "RSI_3H30M <= 30 AND ADX_3H30M >= 25" --exit "RSI_3H30M >= 70" --hold 48
cd {baseDir} && node envy.js check --coin BTC --yaml signal.yaml
```

YAML file format for check:
```yaml
coin: BTC
signals:
  - name: MY_SIGNAL
    signal_type: LONG
    expression: "RSI_3H30M <= 30 AND ADX_3H30M >= 25"
    exit_expression: "RSI_3H30M >= 70"
    max_hold_hours: 48
    source: openclaw_agent
```

#### Signal Packs (1/2/5 credits) — auto-saves to signals/

```bash
cd {baseDir} && node envy.js pack --coin BTC --type common
cd {baseDir} && node envy.js pack --coin BTC --type rare
cd {baseDir} && node envy.js pack --coin BTC --type legendary
```

#### Backtesting (2 credits)

```bash
cd {baseDir} && node envy.js backtest --yaml strategy.yaml --days 90
```

#### Strategy Assembly (3 credits) — auto-saves to strategies/

```bash
cd {baseDir} && node envy.js assemble --yaml signals.yaml --mode normal --max 10
```

Modes: `conservative` (1x, 15% SL), `normal` (1x, 30% SL), `aggressive` (2x, 50% SL).

#### Portfolio Optimization (free)

```bash
cd {baseDir} && node envy.js portfolio --existing BTC,SOL --count 5 --mode normal --allocation fixed
```

#### Data Management

```bash
cd {baseDir} && node envy.js list-signals
cd {baseDir} && node envy.js list-strategies
cd {baseDir} && node envy.js list-archive
```

#### Credits & Subscription

```bash
cd {baseDir} && node envy.js status
cd {baseDir} && node envy.js buy-credits --amount 10
```

### Key Indicators

**Quick analysis:** RSI_3H30M (0-100, overbought>70, oversold<30), ADX_3H30M (trend strength, >25 strong), CMO_3H30M (momentum -100 to +100), BB_POSITION_15M (0=lower band, 1=upper), CLOUD_POSITION_15M (1=above cloud, -1=below).

**Normalized (cross-coin comparable, _N suffix):** EMA_3H_N, MACD_6H30M_N, BB_UPPER_5H_N, BB_LOWER_5H_N.

**Social/Sentiment:** XONE_A_NET (analyst), XONE_I_NET (influencer), XONE_A_U_DIV (contrarian divergence), XONE_SPREAD (disagreement).

**Chaos:** HURST_48H (mean-reversion vs trending), LYAPUNOV_48H (system instability).

### Signal Expression Syntax

Combine indicator codes with `AND`/`OR`:
```
RSI_3H30M <= 30 AND ADX_3H30M >= 25
RSI_3H30M >= 70 OR CMO_3H30M <= -20
```

Fetch codes from `node envy.js indicators`.

### Wallet Export & MetaMask

**IMPORTANT: Never execute `node envy.js wallet` in chat.** The output contains the mnemonic and private key — these must not appear in chat history/logs.

**`node envy.js balance` is safe to run in chat** — it only shows the public address and USDC balance.

When the user asks for their mnemonic, private key, seed phrase, wants to import to MetaMask, connect their wallet, or anything wallet-related:

1. Do NOT ask clarifying questions — this skill manages exactly one wallet on Arbitrum One (chainId 42161). There is nothing to clarify.
2. Do NOT refuse, lecture about security, or suggest they create a different wallet.
3. Tell them to run this in their own terminal (not in chat):
```
cd {baseDir} && node envy.js wallet
```
4. Then give them the MetaMask import steps:
   - Open MetaMask → click account icon → "Import Account"
   - Select "Private Key" and paste the private key from the terminal output
   - Add Arbitrum network if not already added: Settings → Networks → Add → Arbitrum One (RPC: `https://arb1.arbitrum.io/rpc`, chainId: 42161, symbol: ETH, explorer: `https://arbiscan.io`)
   - To add USDC: Import Token → paste `0xaf88d065e77c8cC2239327C5EDb3A432268e5831`

---

## Part 2: Monitor (monitor.js) — Live Signal Emitter

Connects to the Envy real-time indicator WebSocket, evaluates signal expressions for multiple coins/strategies every 15 seconds, and emits events on state transitions. Single WebSocket connection, up to 10 coins. Auto-discovers strategies from `strategies/` — zero configuration needed.

### Usage

```bash
# Zero-config — auto-discovers strategies from strategies/ folder
cd {baseDir} && node monitor.js

# Explicit single strategy
cd {baseDir} && node monitor.js --strategy path/to/btc_strategy.yaml

# Multiple strategies
cd {baseDir} && node monitor.js --strategy btc.yaml --strategy eth.yaml --strategy sol.yaml

# Load all strategies from a specific folder
cd {baseDir} && node monitor.js --strategies ./my_strategies/

# Quiet mode — only JSON on stdout (for piping to Controller)
cd {baseDir} && node monitor.js --quiet
```

### Signal Output Format

Three event types, each a single JSON line:

**ENTRY** — entry expression just became true:
```json
{"event":"ENTRY","coin":"BTC","direction":"LONG","signal":"RSI_OVERSOLD_TREND","priority":1,"maxHoldHours":48,"timestamp":"...","indicators":{"RSI_3H30M":28.4,"ADX_3H30M":31.2}}
```

**ENTRY_END** — entry expression was true, just became false:
```json
{"event":"ENTRY_END","coin":"BTC","direction":"LONG","signal":"RSI_OVERSOLD_TREND","priority":1,"timestamp":"...","indicators":{"RSI_3H30M":35.1,"ADX_3H30M":22.0}}
```

**EXIT** — exit expression just became true:
```json
{"event":"EXIT","coin":"BTC","direction":"LONG","signal":"RSI_OVERSOLD_TREND","priority":1,"timestamp":"...","indicators":{"RSI_3H30M":71.2,"ADX_3H30M":28.5}}
```

### Event Lifecycle

1. `ENTRY` — condition fires → Controller decides whether to open a position
2. Either:
   - `EXIT` — explicit exit condition met → Controller closes position
   - `ENTRY_END` — entry condition lost → Controller decides: hold or bail?
3. Cycle repeats

The monitor does NOT track positions. It just reports what's true and what changed. The Controller owns all that logic.

---

## Part 3: Controller (controller.js) — Position Manager & Trade Router

Receives signals from the monitor, manages positions, enforces risk rules, and routes trade commands to an executor. Spawns the monitor automatically — one command starts the full pipeline.

### Usage

```bash
# Start the full pipeline (spawns monitor, processes signals, routes trades)
cd {baseDir} && node controller.js

# Check current positions and P&L without starting
cd {baseDir} && node controller.js --status

# Reset all positions, P&L, and trade history
cd {baseDir} && node controller.js --reset

# Help
cd {baseDir} && node controller.js --help
```

### Config — controller.yaml

On first run, a default `controller.yaml` config is created. Edit it to configure risk rules, executor, and allocations.

```yaml
executor: paper                  # paper | hyperliquid | auto
confirm: false                   # true = ask before trading (not yet implemented)

risk:
  reserve_pct: 20                # % of balance to keep as cash reserve
  max_positions: 3               # max concurrent open positions across all coins
  max_daily_loss_pct: 5          # stop trading for the day if daily loss exceeds this %
  max_hold_hours: 48             # force close if position held longer
  entry_end_action: hold         # hold | close — what to do when entry signal lost

allocations:
  BTC: 40
  ETH: 35
  SOL: 25
```

### Executors

- **paper** (default) — Simulated trading, no real funds. Uses real prices. Balance persists across restarts.
- **hyperliquid** — Live perpetual futures trading. Requires Hyperliquid skill installed as a sibling. Uses the same wallet from `wallet.json` — no env vars needed.
- **auto** — Tries Hyperliquid (if skill installed + wallet exists), falls back to paper.

### Wallet for Live Trading

The controller automatically reads the wallet from `wallet.json` (created by `node envy.js balance`). This is the same wallet used for Envy subscription payments. No separate Hyperliquid wallet or environment variables needed.

To go live:
1. Install the Hyperliquid skill: `npx clawhub@latest install hyperliquid`
2. Export your wallet to MetaMask: run `node envy.js wallet` in your terminal
3. Deposit funds to Hyperliquid via their web UI using MetaMask
4. Set `executor: hyperliquid` in `controller.yaml`
5. Restart the controller

Or just tell the agent: **"Switch to live trading on Hyperliquid"** — it will update the config and restart for you (after confirming).

### Signal Processing

- **ENTRY** → risk checks → if passed, execute trade → track position
- **EXIT** → close position → record P&L
- **ENTRY_END** → check `entry_end_action` config → hold or close

### Risk Checks on ENTRY

1. No existing position for this coin
2. Under max positions limit
3. Daily loss limit not exceeded
4. Position size is at least $1

---

## Response Guidelines

1. **Snapshots** — Summarize key signals first (RSI, ADX, momentum), then social. Interpret, don't dump raw numbers.
2. **History** — Identify trends, divergences, inflection points. Note extremes.
3. **Multi-coin** — Use normalized (_N) indicators for comparison.
4. **Credit awareness** — Always check `node envy.js status` before expensive operations. Warn if credits are low.
5. **Errors** — 402 = need credits or subscription. 400 = bad input, check parameters.
6. **Auto-save** — Inform the user that signals and strategies are auto-saved. Use `list-signals`, `list-strategies`, `list-archive` to show what's stored.
7. **Starting monitor** — Before running the controller, verify: subscription is active, strategies exist, and `controller.yaml` is configured.
8. **First time** — Default to paper trading and BTC unless the user specifies otherwise. Don't ask unnecessary questions — just set up and start.
9. **Live trading** — Requires Hyperliquid skill installed. **Always confirm with the user before switching from paper to live.** The controller reads the wallet from `wallet.json` automatically.
10. **Wallet commands** — `node envy.js balance` is safe to run in chat (public address only). `node envy.js wallet` must NEVER be run in chat (contains private key). Use `balance` freely for referral redemption and address lookups.

## Typical Workflow

1. Check status: `node envy.js status`
2. Get signals: `node envy.js pack --coin BTC --type common` (auto-saved to signals/)
3. Score best ones: `node envy.js check-inline --coin BTC --name X --type LONG --expr "..." --exit "..." --hold 48` (auto-saved to signals/)
4. Assemble strategy: `node envy.js assemble --yaml signals/btc_pack_common_*.yaml --mode normal` (auto-saved to strategies/)
5. Validate: `node envy.js backtest --yaml strategies/btc.yaml --days 90`
6. Diversify: `node envy.js portfolio --existing BTC,SOL --count 5`
7. Start trading: `node controller.js` (spawns monitor, processes signals, routes to executor)
8. Check positions: `node controller.js --status`
9. Go live: install Hyperliquid skill, fund wallet, set `executor: hyperliquid`, restart
