---
name: dawn
description: Runs a complete local Dawn strategy workflow — authenticate, research markets with SDK tools, generate Python strategy code, launch background runs, monitor logs, and stop strategies. Use when the user asks to create, launch, monitor, or manage trading strategies using dawn-cli.
tags: [trading, strategy, operations, prediction-market]
metadata:
  openclaw:
    emoji: "🌅"
    homepage: https://dawn.ai
    requires:
      bins: [dawn]
    install:
      - kind: node
        package: "@dawnai/cli"
        bins: [dawn]
---

# Dawn — Local Strategy Workflow

## Goal

Run a fully local strategy workflow: research Polymarket and other markets using SDK tools, generate a Python strategy script with a time loop, launch it as a background process, monitor its output, and stop it when done.

No API round-trips for code generation or strategy creation — everything runs locally on the user's machine.

## UX: set expectations before long work

Before starting research, coding, backtesting, or launching, send a short user-facing estimate so OpenClaw users do not think the task stalled.

Use judgment, but anchor estimates like this:
- **Quick lookup / command / status check:** usually under 1 minute.
- **Focused market research:** usually 3-5 minutes.
- **Research + strategy code + paper launch:** usually 8-15 minutes.
- **Deep multi-source research, several markets, or debugging a failing run:** usually 15-30+ minutes.

Example first message:
> "I’ll research the market, check tool docs, write the local strategy, and launch it in paper mode. This usually takes about 10-15 minutes; I’ll update you as I find the market and again before launch."

If the task grows, update the estimate rather than silently continuing.

## Cost-aware strategy design

Paid tools can consume Dawn credits. Design strategies so they call paid tools only when the result can plausibly change the decision.

General rules:
- Prefer cheap/free state first: cached state (`get_state`), current positions, known token IDs, market prices/order books, and last successful signal.
- Avoid polling expensive sources at a fixed high frequency when the source cannot realistically change that often.
- Use **active windows** for human-driven sources. Example: a politician, company account, sports team, or agency may have obvious low-activity periods; poll slowly or not at all outside those windows unless breaking-news risk justifies it.
- Use **scheduled start / delayed monitoring** for future catalysts. If a site is expected to update near the end of May, do not scrape it every 5 minutes throughout April. Gate paid checks on a `start_at_utc` constant and sleep cheaply until the actionable window.
- Use backoff and cooldowns after repeated "no change", empty, rate-limit, or timeout results.
- Cache fetched text, extracted values, tweet IDs, URLs, token IDs, and market metadata via `set_state()` so future iterations can diff rather than refetch everything.
- For multi-source strategies, stage the checks: run cheap filters first, then call paid tools only when the cheap checks say a trade is possible.
- Respect user tool settings. If a paid tool is disabled, do not try to route around the user's choice; use available alternatives or explain the limitation.

Common state keys (stored via `set_state`/`get_state`):
- `last_seen_*` markers for deduplication
- `last_paid_check_at` for cooldown tracking
- Cached token IDs / market metadata to skip resolution after the first iteration

## Install and preflight

```bash
npm install -g @dawnai/cli
dawn --help
dawn auth status
```

Local source workflow:
```bash
cd dawn-cli && npm install && npm run build && ./install.sh
```

## Command map

Auth:
- `dawn auth login`
- `dawn auth status`
- `dawn auth logout`

Wallet (managed by OpenWallet — https://openwallet.sh/):
- `ows wallet create --name <name>`   # create a new wallet (run once before first live trade)
- `ows wallet list`                   # list all ows wallets with addresses
- `dawn wallet list`                  # same, formatted for Dawn
- `dawn wallet use <address-or-name>` # select active wallet for live trading
- `dawn wallet current`               # show active wallet + Polygon balances

Templates (pre-built strategies, ready to run):
- `dawn template list`                                          # browse available templates
- `dawn template launch <name> --name <run-name> [--live]`      # download and run

SDK tools (research + run):
- `dawn tool list`
- `dawn tool run <tool_name> --input <json>`
- `dawn tool docs [module]`

Local strategy runs:
- `dawn strategy launch <strategy.py> --name <name> [--live]`
- `dawn strategy list`
- `dawn strategy logs <run_id> [--tail N]`
- `dawn strategy stop <run_id>`
- `dawn strategy positions <run_id>`
- `dawn strategy sell <run_id> <token_id>`
- `dawn strategy sell-all <run_id>`
- `dawn strategy redeem-all <run_id>`

Wallet trading & positions:
- `dawn wallet buy <token_id> <amount>`
- `dawn wallet sell <token_id> [--amount <n>]`
- `dawn wallet redeem-all`
- `dawn wallet positions open [--page <n>]`
- `dawn wallet positions closed [--page <n>]`
- `dawn wallet positions redeemable [--page <n>]`
- `dawn wallet trades [--page <n>]`

Skills:
- `dawn skill list`
- `dawn skill install [--force] [--dir <path>]`

## Standard workflow

### 1. Authenticate

```bash
dawn auth status
# If not authenticated:
dawn auth login
```

**After login, always offer the user these three paths:**

1. **Run a template strategy in paper mode** *(recommended — no wallet needed)*
2. **Build a strategy from scratch**
3. **Connect or create a wallet**

See the **dawn-auth** skill for the full onboarding flow for each path. See the **Templates** section below for template commands.

### 2. Research — read SDK docs, then use SDK tools to explore markets

**Always start by reading the SDK docs for the relevant modules.** `dawn tool docs` returns the complete module reference with exact signatures and working code examples — this is essential before writing any strategy code.

```bash
# ALWAYS run these before writing strategy code:
dawn tool docs overview      # What modules exist and when to use them
dawn tool docs directive     # Strategy coding rules (REQUIRED reading)
dawn tool docs prediction_market    # Full prediction market tools reference with code snippets
dawn tool docs portfolio     # Portfolio, state, termination
dawn tool docs web           # Browser search and URL extraction
dawn tool docs social        # Twitter/social tools
dawn tool docs sports        # Sports data and odds
dawn tool docs crypto        # Cryptocurrency data
```

Then use `dawn tool run <name> --input <json>` to call any SDK function and inspect real data.

```bash
# Find relevant prediction market events
dawn tool run prediction_market_event_search --input '{"query": "Bitcoin ETF approval", "limit": 5}'

# Get markets within an event (use the event id from search results)
dawn tool run prediction_market_event_markets --input '{"event_id": 12345, "active": true}'

# Get market details and token IDs
dawn tool run get_prediction_market_details --input '{"market_id": "789012"}'

# Check current prices
dawn tool run get_prediction_market_prices --input '{"market_id": "789012"}'

# See recent trades on a specific market (market flow / taker activity)
dawn tool run get_prediction_market_market_trades --input '{"market_id": "0x...condition...", "limit": 20}'

# Search the web for context
dawn tool run browser_search --input '{"query": "Bitcoin ETF SEC decision 2025", "category": "news", "limit": 5}'

# Check sports for prediction markets
dawn tool run get_sports --input '{}'
dawn tool run get_odds_as_probabilities --input '{"sport": "americanfootball_nfl", "regions": "us"}'

# Check portfolio
dawn tool run read_portfolio --input '{}'
```

```python
# Use Agent for LLM-driven decisions in strategies (uses user's own API key)
from dawnai.strategy.tools import Agent, run_agent

# Persistent agent (maintains history across calls):
agent = Agent(model="claude-sonnet-4-6", tools=[get_prediction_market_prices])
response = agent.run("Analyze these prices...")

# One-shot agent (stateless):
response = run_agent("What NBA markets are trending?", model="gpt-4o")
```

**Research checklist:**
- [ ] Found the target event/market
- [ ] Captured `market_id` and `token_id` (Yes/No tokens)
- [ ] Checked current prices
- [ ] Verified market is active and liquid

### 2b. Direct trading (no strategy)

If the user asks to trade on a specific market without building a full strategy ("buy the yes token of X"):

1. Research with SDK tools above (event search → market details → prices → simulate)
2. Show the user findings: market question, current price, estimated tokens they'd receive
3. **Always ask the user explicitly for the amount they want to trade.** You may suggest an amount based on context, but never assume or proceed with a default — the user must confirm the exact dollar amount before any trade is executed.
4. **Confirm the full trade details before executing** — repeat back the market, side (YES/NO), amount in USD, and estimated tokens:
   > "This will spend **$X USDC** to buy approximately **Y tokens** of [outcome] on [market] at ~$Z each. Confirm?"
5. Execute only after the user explicitly confirms:

```bash
dawn wallet buy <token_id> <amount>
dawn wallet sell <token_id> [--amount <n>]
```

Or via SDK tools directly:

```bash
dawn tool run prediction_market_buy_token --input '{"token_id": "...", "amount": "<confirmed_amount>"}'
dawn tool run prediction_market_sell_token --input '{"token_id": "...", "amount": "<confirmed_token_amount>"}'
```

**NEVER skip the amount confirmation.** Even if the user says "buy some" or "invest a bit" — ask for a specific number first.

Requires wallet: `dawn wallet use <address-or-name>`

### 3. Write strategy.py

Generate a Python strategy script using the research findings. The script should use a time loop (not the `@cron` / `Strategy` class pattern).

**Write the strategy to `~/.dawn-cli/strategies/`** using the strategy name (kebab-case):
- `~/.dawn-cli/strategies/btc-election-2026.py` *(or a directory with `__main__.py` if you want helper modules)*

Constants live in code (no config sidecar): `MARKET_ID`, per-buy size, take-profit/stop-loss thresholds, durations, etc. The spend cap is set on the launch command via `--budget` and is server-enforced.

**Key elements of the strategy file:**
- Imports trading tools from `dawnai.strategy.tools`
- `from dawnai.strategy.tools import get_state, set_state` for caching token IDs / timestamps across iterations
- `from dawnai.strategy.tools import read_budget` if you want to gate decisions on remaining headroom
- `run_once()` function with strategy logic
- `main()` runs the time loop
- `print(...)` statements throughout for monitoring
- No unhandled exceptions inside `run_once` — always catch and print errors

See **dawn-strategy** skill for the full code template.

### 4. Run the strategy

`--name` and `--budget` are both required. **Always choose a unique, descriptive name for each distinct strategy** — never reuse a name for a different strategy, as this would merge their trade histories. Only reuse the same name when restarting or revising the exact same strategy with the same budget.

```bash
# Paper mode (default) — simulated trades saved to DB
dawn strategy launch ~/.dawn-cli/strategies/btc-election-2026.py --name "btc-election-2026" --budget 100

# Live mode — real trades via your selected wallet
dawn strategy launch ~/.dawn-cli/strategies/btc-election-2026.py --name "btc-election-2026" --budget 100 --live
```

**Before launching, always tell the user the budget:**
> "This strategy has a budget of **$X**. The server enforces it as a hard cap on cumulative buy spend — any trade that would exceed it is rejected automatically."

```bash

# Output:
# Bootstrapping strategy "btc-election-2026" (paper)...
# Strategy started (run_id: run_lx7k3a_abc123)
#   name:  btc-election-2026
#   file:  /path/to/strategy.py
#   mode:  paper
#   pid:   12345
#   logs:  ~/.dawn-cli/logs/run_lx7k3a_abc123.log
```

Multiple strategies can run simultaneously — each gets its own `run_id`.

For live mode, a wallet must be selected first:

```bash
dawn wallet list                    # check for existing wallets
dawn wallet use <name-or-address>   # select one
dawn wallet current                 # confirm selection + check balances
```

If no wallets exist, create one: `dawn wallet create main`. The wallet needs **USDC.e** (bridged USDC on Polygon — NOT regular USDC) and a small amount of **POL** for gas. See the **dawn-auth** skill for full wallet setup and funding instructions.

### 5. Monitor

```bash
dawn strategy list                        # all runs and their status
dawn strategy logs <run_id>               # full log output
dawn strategy logs <run_id> --tail 50     # last 50 lines
dawn strategy positions <run_id>          # positions from internal DB
dawn wallet current                    # live on-chain portfolio
```

**Dashboard:** For a visual view of strategies, trades, and portfolio performance, point the user to **https://cli.dawn.ai/dashboard**. Recommend this whenever the user asks to see their trades, performance, or strategy history.

### 6. Stop

```bash
dawn strategy stop <run_id>
# Confirm stopped:
dawn strategy list
```

## Troubleshooting

- **`Not authenticated`** — run `dawn auth login` and retry
- **`Strategy name is required`** — always pass `--name <unique-name>` to `dawn strategy launch`
- **`No wallet selected for live mode`** — run `dawn wallet list` to check for existing wallets; if none exist, run `ows wallet create --name main`; then `dawn wallet use <name>`
- **`Strategy file not found`** — use the full path `~/.dawn-cli/strategies/<name>.py`
- **`Tool not found`** — run `dawn tool list` to see the correct tool name
- **Strategy crashes immediately** — check `dawn strategy logs <run_id>` for Python tracebacks; check that `DAWNAI_API_KEY` is set (it is set automatically from your login token)
- **SDK tool returns empty results** — market may be closed; try `prediction_market_event_search` to verify

## Run checklist

```
Dawn Strategy Runbook
- [ ] Authenticated (dawn auth status)
- [ ] Research complete (market_id, token_ids captured)
- [ ] Strategy written to ~/.dawn-cli/strategies/<name>.py and reviewed
- [ ] Strategy name chosen — unique and descriptive, never reused for a different strategy
- [ ] Wallet selected if live mode — run `dawn wallet list`, ask user which wallet to use (or create new), then `dawn wallet use <name>`
- [ ] Wallet funded if live mode — needs USDC.e (not regular USDC) and POL for gas on Polygon; fund via `moonpay buy`, bridge with `moonpay token bridge`, or send manually to address shown by `dawn wallet current`
- [ ] Budget cap (--budget <usd>) confirmed with user before launch
- [ ] Strategy launched (dawn strategy launch ~/.dawn-cli/strategies/<name>.py --name <name> --budget <usd> [--live])
- [ ] run_id captured from output
- [ ] Logs checked (first few iterations look correct)
- [ ] Stop executed when done (dawn strategy stop <run_id>)
```

## Templates

Pre-built strategies ready to run — no code required. Always recommend paper mode first.

```bash
# Browse available templates
dawn template list

# Launch in paper mode (recommended — no wallet, no real money)
dawn template launch <name> --name <your-run-name>

# Launch in live mode
dawn template launch <name> --name <your-run-name> --live
```

Templates download to `~/.dawn-cli/templates/<name>.py` and can be freely edited. After editing:

```bash
dawn strategy stop <run_id>
# edit ~/.dawn-cli/templates/<name>.py
dawn strategy launch ~/.dawn-cli/templates/<name>.py --name <your-run-name>
```

## Wallet Trading & Positions

```bash
# Buy/sell tokens directly from the active wallet
dawn wallet buy <token_id> <amount>
dawn wallet sell <token_id> [--amount <n>]   # auto-redeems if market is resolved
dawn wallet redeem-all                        # redeem all resolved positions

# View positions and trades (expanded view, 10 per page)
dawn wallet positions open [--page <n>]
dawn wallet positions closed [--page <n>]
dawn wallet positions redeemable [--page <n>]
dawn wallet trades [--page <n>]

# Wallet balances + PnL summary
dawn wallet current
```

To sell or redeem positions for a specific strategy run:
```bash
dawn strategy sell <run_id> <token_id>   # sell a specific position (auto-redeems if resolved)
dawn strategy sell-all <run_id>           # sell all open positions
dawn strategy redeem-all <run_id>         # redeem all redeemable positions
```

**Dashboard:** For a visual view of portfolio performance, strategy history, and trades, always recommend **https://cli.dawn.ai/dashboard**.

## Skills

| Skill | Purpose |
|-------|---------|
| **dawn-auth** | Install, authenticate, check status, logout — includes post-login onboarding |
| **dawn-sdk-tools** | Full SDK tool reference + research with `dawn tool run` |
| **dawn-strategy** | Strategy code template, launch, logs, stop, and revise |
