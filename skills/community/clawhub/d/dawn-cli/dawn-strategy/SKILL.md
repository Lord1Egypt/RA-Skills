---
name: dawn-strategy
description: Write and run local trading strategies. Covers the strategy code format, launching background runs, viewing logs, stopping, and revising strategies.
tags: [strategy, run, local]
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

# Strategy — Write, Run, Stop, Revise

## Overview

Strategies are regular Python projects. The runner spawns them as a background process and reads stdout/stderr into a log file. Multiple strategies can run in parallel.

You have full reign over the project shape:

- **Single file**: a `.py` file with whatever structure you want.
- **Project directory**: a folder with a `__main__.py` (or `main.py`) entrypoint, plus any helper modules / tests / configs you want to colocate. The runner sets `cwd` to the project directory so sibling modules import normally.

Dependencies beyond the standard library and the Dawn SDK are declared via `pyproject.toml` (`[project.dependencies]`) or a `requirements.txt` next to the entrypoint. The runner builds a per-deps cached venv on first launch and reuses it on subsequent launches with the same deps.

Common execution shapes:

- **Time loop** — wake every N minutes, do work, sleep. Simplest and works for most strategies. The example below uses this pattern.
- **Event-driven** — connect to a websocket / SSE stream, react to events as they arrive.
- **Scheduled** — APScheduler or similar for cron-like timing.

Pick whichever fits the strategy. The runner doesn't care.

`dawn strategy launch <strategy-path> --name <name> --budget <usd>` launches the script in the background, prints a `run_id`, and returns immediately. `<strategy-path>` can be a `.py` file or a project directory.

**`--name` is required** and should be unique per strategy. Reusing the same name + mode reuses the same strategy record (trade history preserved) — only do this when restarting or revising the same strategy. Never reuse a name for a different strategy.

**`--budget <usd>` is required** and is the **server-enforced** hard cap on cumulative BUY spend for that strategy. Any `polymarket_buy_token` call that would push spend past the cap is rejected with `would_exceed_budget` — strategies do not need to track spend themselves. To gate decisions on remaining headroom, call `read_budget()` from the SDK; it returns `cap`, `spent`, and `remaining` as `Decimal`.

Before doing substantial work, tell the user what you are about to do and roughly how long it should take. Focused research is often 3-5 minutes; research + code + launch is often 8-15 minutes; deep multi-source research or debugging can take 15-30+ minutes. Update the estimate if the task grows.

---

## ALWAYS read SDK docs before writing strategy code

```bash
dawn tool docs directive     # Strategy coding rules — read this first
dawn tool docs overview      # Module overview and when to use each
dawn tool docs prediction_market    # Prediction market tools with code patterns
dawn tool docs portfolio     # Portfolio tools, terminate_strategy
dawn tool docs web           # Browser search, URL extraction
```

---

## Strategy code template

The shape below is a worked example, not a mandate. The only thing the runner needs is a Python entrypoint — a `.py` file or a project dir with `__main__.py`. Constants live in code; per-iteration state can be cached across iterations with `set_state` / `get_state` (a small KV store keyed to the strategy).

```python
import sys
import time
from decimal import Decimal

from dawnai.strategy.tools import (
    get_prediction_market_details,
    get_state,
    prediction_market_buy_token,
    prediction_market_sell_token,
    read_portfolio,
    set_state,
    terminate_strategy,
)

# ── Configuration (constants live in code, not a config file) ────────────────
MARKET_ID = "123456"
BUY_AMOUNT_USD = Decimal("25.0")          # Per-buy size (the budget cap is set at launch)
TAKE_PROFIT_PCT = Decimal("10")
STOP_LOSS_PCT = Decimal("-10")

DURATION_HOURS = 1
INTERVAL_MINUTES = 5
ITERATIONS = int((DURATION_HOURS * 60) / INTERVAL_MINUTES)


# ── Strategy logic ───────────────────────────────────────────────────────────

def run_once() -> None:
    """Execute one iteration of the strategy."""
    print("Checking market conditions...")

    # Cache the token ID across iterations to avoid re-fetching market metadata.
    yes_token_id: str | None = get_state("yes_token_id")
    if yes_token_id is None:
        market = get_prediction_market_details(MARKET_ID)
        if market is None:
            print(f"[Error] Market {MARKET_ID} not found")
            return
        yes_token = next((t for t in (market.tokens or []) if t.outcome.lower() == "yes"), None)
        if yes_token is None:
            print(f"[Error] No Yes token found for market {MARKET_ID}")
            return
        yes_token_id = yes_token.id
        set_state("yes_token_id", yes_token_id)
        print(f"Cached Yes token: {yes_token_id}")

    portfolio = read_portfolio()
    position = next(
        (p for p in portfolio.wallet.positions if p.token_id == yes_token_id),
        None,
    )

    if position is None or position.amount == Decimal("0"):
        # Budget cap is server-enforced — a buy that would exceed it fails with
        # error 'would_exceed_budget'. No client-side spend tracking required.
        print(f"No position found. Buying ${BUY_AMOUNT_USD} of Yes token...")
        result = prediction_market_buy_token(yes_token_id, BUY_AMOUNT_USD)
        if not result.result.success:
            print(f"[Error] Buy failed: {result.error}")
            return
        usd_spent = Decimal(str(result.result.executed_amount)) * Decimal(str(result.result.executed_price))
        print(f"Bought {result.result.executed_amount} tokens at {result.result.executed_price} (${usd_spent:.2f})")
        return

    pnl_pct = position.pnl_percent
    print(f"Position: {position.amount} tokens | PnL: {pnl_pct:.1f}%")
    if pnl_pct >= TAKE_PROFIT_PCT or pnl_pct <= STOP_LOSS_PCT:
        action = "Take profit" if pnl_pct >= TAKE_PROFIT_PCT else "Stop loss"
        print(f"{action} triggered at {pnl_pct:.1f}%. Selling...")
        sell_result = prediction_market_sell_token(yes_token_id, position.amount)
        if not sell_result.result.success:
            print(f"[Error] Sell failed: {sell_result.error}")
            return
        print(f"Sold {sell_result.result.executed_amount} tokens. Terminating.")
        terminate_strategy()
        sys.exit(0)
    else:
        print("Holding position (threshold not hit)")


# ── Main loop ────────────────────────────────────────────────────────────────

def main() -> None:
    print(f"Strategy starting: {ITERATIONS} iterations every {INTERVAL_MINUTES}m over {DURATION_HOURS}h")
    print(f"Market: {MARKET_ID} | Buy size: ${BUY_AMOUNT_USD}")

    for i in range(ITERATIONS):
        print(f"\n=== Iteration {i + 1}/{ITERATIONS} ===")
        try:
            run_once()
        except KeyboardInterrupt:
            print("\nStrategy interrupted by user.")
            sys.exit(0)
        except Exception as e:
            print(f"[Error] Unexpected error in iteration {i + 1}: {e}")

        if i < ITERATIONS - 1:
            print(f"Sleeping {INTERVAL_MINUTES}m until next iteration...")
            time.sleep(INTERVAL_MINUTES * 60)

    print("\nStrategy completed all iterations.")
    terminate_strategy()


if __name__ == "__main__":
    main()
```

---

## Launch

Write the strategy to `~/.dawn-cli/strategies/` using the strategy name (kebab-case) as the filename:
- `~/.dawn-cli/strategies/btc-election-2026.py` *(or a project directory with `__main__.py`)*

```bash
# Paper mode (default) — trades tracked in DB
dawn strategy launch ~/.dawn-cli/strategies/btc-election-2026.py --name "btc-election-2026" --budget 100

# Live mode — real trades using your selected wallet
dawn strategy launch ~/.dawn-cli/strategies/btc-election-2026.py --name "btc-election-2026" --budget 100 --live
```

**Before launching, always tell the user the budget:**
> "This strategy has a budget of **$X**. The server enforces it as a hard cap on cumulative buy spend — any trade that would exceed it is rejected automatically."

Live mode requires a wallet: `dawn wallet use <address-or-name>`

### Budget enforcement (server-side)

`--budget <usd>` at launch sets `strategy.initial_amount` on the server. On every `polymarket_buy_token` call, the API computes `SUM(usd_amount) WHERE type=BUY AND strategy_id=...` and rejects buys where `spent + amount > cap` with `error: 'would_exceed_budget'`.

Strategies do **not** track spend themselves. To gate decisions on remaining headroom, call `read_budget()`:

```python
from dawnai.strategy.tools import read_budget

budget = read_budget()
print(f"Budget: ${budget.spent} spent / ${budget.cap} cap (${budget.remaining} remaining)")
if budget.remaining < Decimal("5"):
    print("Out of room. Holding.")
    return
```

Calling `read_budget()` is a network round-trip — fine to call once per iteration, but don't loop on it. If you don't need the value, just call `polymarket_buy_token` and check `result.error` for `would_exceed_budget`.

---

## Manage runs

```bash
# List all runs (run_id, name, mode, status, pid)
dawn strategy list

# View full logs
dawn strategy logs <run_id>

# View last N lines
dawn strategy logs <run_id> --tail 50

# Stop a running strategy (sends SIGTERM)
dawn strategy stop <run_id>

# Positions for a specific run (from internal DB)
dawn strategy positions <run_id>

# Sell a single position for a run (auto-redeems if market is resolved)
dawn strategy sell <run_id> <token_id>

# Sell all open positions for a run (paper or live)
dawn strategy sell-all <run_id>

# Redeem all resolved/redeemable positions for a run (paper or live)
dawn strategy redeem-all <run_id>

# Real-time live portfolio (from wallet via swaps.xyz — no run_id needed)
dawn wallet current

# Buy a position directly (no strategy attribution)
dawn wallet buy <token_id> <amount>

# Sell a position directly (auto-redeems if market is resolved)
dawn wallet sell <token_id> [--amount <n>]

# Redeem all redeemable positions across the live wallet
dawn wallet redeem-all
```

### Stopping

1. Find the run: `dawn strategy list` — confirm it shows `running`
2. Stop it: `dawn strategy stop <run_id>`
3. Verify: `dawn strategy list` — confirm status is `stopped`

**Notes:**
- Stopping sends `SIGTERM` — the Python script receives `KeyboardInterrupt` if it handles signals
- Stopping does **not** liquidate open positions — to auto-liquidate on exit, include `terminate_strategy(should_liquidate=True)` in the strategy code's exit path
- Log files remain at `~/.dawn-cli/logs/<run_id>.log` after stopping

**Troubleshooting stops:**
- **`Run not found`** — use `dawn strategy list` to find the correct `run_id`
- **Run already stopped** — the strategy may have finished naturally or hit `terminate_strategy()`
- **Still shows `running` after stop** — wait a moment and re-check

---

## Revise a strategy

There are **two kinds of revisions**, and the rule for which `--name` to use is strict:

| What changed | New `--name`? | Why |
|---|---|---|
| Logic tweaks, bug fixes, signal/threshold changes, market_id, timing, added/removed tools | **No** — relaunch under the **same name** with the **same `--budget`** | Trade history and cumulative spend stay attached to the original strategy record. |
| Budget change (`--budget`) | **Yes — always launch under a new name** | Cumulative spend is tracked per strategy. Changing the cap on the same name would either leave old spend counted against the new cap (confusing) or silently reset (dangerous). A fresh name = fresh accounting. |

### Same-name relaunch (minor changes / bug fixes)

```bash
# 1. Find the current run (if needed)
dawn strategy list

# 2. Stop it
dawn strategy stop <run_id>

# 3. Edit ~/.dawn-cli/strategies/btc-election-2026.py — fix bugs, update logic, thresholds, timing, market_id, imports
#    Do NOT change --budget here. If you need a different budget, go to the section below.

# 4. Re-launch with the SAME name and SAME budget — continues trade history under the same strategy record
dawn strategy launch ~/.dawn-cli/strategies/btc-election-2026.py --name "btc-election-2026" --budget 100

# 5. Monitor
dawn strategy logs <new_run_id> --tail 20
```

### Budget change → new strategy, new name

```bash
# 1. Stop the old run
dawn strategy stop <old_run_id>

# 2. Pick a NEW name (e.g. append -v2, or describe the new budget)
#    "btc-election-2026"      → "btc-election-2026-v2"
#    "eth-momentum"           → "eth-momentum-big"

# 3. Copy or reuse the strategy file
cp ~/.dawn-cli/strategies/btc-election-2026.py ~/.dawn-cli/strategies/btc-election-2026-v2.py

# 4. Launch under the new name with the new budget
dawn strategy launch ~/.dawn-cli/strategies/btc-election-2026-v2.py --name "btc-election-2026-v2" --budget 500
```

### Common revisions (all same-name unless noted)

**Change timing or thresholds** — edit the constants in the strategy file and relaunch (the duration/interval are fixed at launch).

**Switch market** — change `MARKET_ID` in the strategy file. Cached `yes_token_id` from the previous market is keyed to the same strategy record; clear it explicitly if needed:
```python
set_state("yes_token_id", None)  # one-shot: drop stale cache after market_id change
```

**Add a signal source:**
```python
from dawnai.strategy.tools import browser_search, classify_text

def check_sentiment() -> str:
    results = browser_search(query="Bitcoin ETF news today", category="news", limit=5)
    headlines = " ".join(r.title for r in results.results[:3])
    result = classify_text(
        text=headlines,
        categories=["bullish", "bearish", "neutral"],
        question="What is the overall sentiment for Bitcoin?"
    )
    return result.category
```

**Research a new market before revising:**
```bash
dawn tool run prediction_market_event_search --input '{"query": "new topic", "limit": 5}'
dawn tool run get_prediction_market_details --input '{"market_id": "654321"}'
```

**Notes:**
- Per-strategy state (e.g. `yes_token_id`, last-check timestamps) is stored server-side and accessed via `get_state` / `set_state` — it survives process restarts as long as the strategy name stays the same
- Each `dawn strategy launch` gets a new `run_id`; old logs remain at `~/.dawn-cli/logs/<old_run_id>.log`
- **Never reuse a name for a different strategy** — this merges unrelated trade histories
- **Never reuse a name with a different `--budget`** — always launch under a new name so spend accounting stays clean

---

## Code guidelines

**Be cost-aware with paid tools** — call them only when they can change the trading decision:
- Put cheap checks first: existing position, cached market metadata, current market price, and last seen signal.
- Use active windows or quiet hours for sources with predictable human/activity patterns.
- Use a delayed-start gate for future catalysts so a strategy can launch now but sleep cheaply until monitoring matters.
- Cache source IDs, extracted text hashes, URLs, token IDs, and last paid-check timestamps via `set_state()` / `get_state()`.
- Slow polling and back off after repeated no-change, empty, timeout, or rate-limit results.
- Add a daily cap on paid-tool calls when polling research tools.

Example pattern for delayed starts and quiet windows:
```python
from datetime import datetime, timezone
from dawnai.strategy.tools import get_state, set_state

START_AT_UTC = "2026-06-01T00:00:00Z"        # None to disable
PAID_TOOL_COOLDOWN_MINUTES = 30

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def should_run_paid_check() -> bool:
    now = utc_now()
    if START_AT_UTC and now < datetime.fromisoformat(START_AT_UTC.replace("Z", "+00:00")):
        print(f"Waiting until {START_AT_UTC} before paid monitoring starts.")
        return False

    last_check = get_state("last_paid_check_at")
    if last_check:
        elapsed = (now - datetime.fromisoformat(last_check.replace("Z", "+00:00"))).total_seconds() / 60
        if elapsed < PAID_TOOL_COOLDOWN_MINUTES:
            print(f"Paid check cooling down ({elapsed:.1f}m/{PAID_TOOL_COOLDOWN_MINUTES}m).")
            return False

    set_state("last_paid_check_at", now.isoformat())
    return True
```

**Log decisions** — the run log is your only visibility into a background process. `print` is fine; stdlib `logging` is better when you want levels and structured output. Whichever you pick, log enough to reconstruct what the strategy decided and why.

**Catch errors at iteration boundaries** — a single bad SDK call shouldn't kill the whole run. Wrap each iteration's body and log what failed; let real setup failures crash in `main` so they're noticed.

```python
import logging
log = logging.getLogger(__name__)

for i in range(ITERATIONS):
    try:
        run_once()
    except Exception:
        log.exception("iteration %d failed; continuing", i)
    time.sleep(INTERVAL_MINUTES * 60)
```

**Cache token IDs** to avoid redundant API calls:
```python
token_id = get_state("yes_token_id")
if token_id is None:
    market = get_prediction_market_details(MARKET_ID)
    token_id = next(t.id for t in market.tokens if t.outcome.lower() == "yes")
    set_state("yes_token_id", token_id)
```

**Use Agent for LLM-driven decisions** — let an AI agent orchestrate your strategy:
```python
from dawnai.strategy.tools import Agent, get_prediction_market_prices, prediction_market_buy_token

agent = Agent(
    model="claude-sonnet-4-6",
    system_prompt="You are a prediction market trader. Buy when you see strong signals.",
    tools=[get_prediction_market_prices, prediction_market_buy_token, read_portfolio],
)

def run_once():
    prices = get_prediction_market_prices(MARKET_ID)
    response = agent.run(f"Current prices: {prices}. Should we trade?")
    print(f"Agent: {response}")
```

The agent maintains conversation history, so it remembers previous iterations and can track trends over time. Requires the user's own LLM API key (e.g. `ANTHROPIC_API_KEY`).

---

## Related skills

- **dawn-sdk-tools** — Full SDK tool reference and research commands
- **dawn-auth** — Authentication setup
