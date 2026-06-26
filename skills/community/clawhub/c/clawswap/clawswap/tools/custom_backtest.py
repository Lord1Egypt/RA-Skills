#!/usr/bin/env python3
"""
Custom Strategy Backtest Runner — Track B

Runs arbitrary Python strategy code against historical candle data.
The user implements strategy(df) → list of signals.
This runner executes the signals with proper PnL, fees, and risk management.

Usage:
    python3 custom_backtest.py strategy.py --ticker BTC --days 90

Or from OpenClaw Skill:
    Programmatic: run_custom_backtest(code_str, candles_df, config)
"""

from __future__ import annotations
import sys
import json
import importlib.util
import traceback
import tempfile
from pathlib import Path

# Ensure skill root is on sys.path so `from strategies import ...` works
sys.path.insert(0, str(Path(__file__).parent.parent))
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


# ── Config ──────────────────────────────────────────────────────────────────

@dataclass
class BacktestConfig:
    initial_capital: float = 10000.0
    fee_rate: float = 0.00035          # 3.5 bps
    max_leverage: float = 10.0
    max_position_size: float = 1.0     # Max 100% of equity per trade
    hard_stop_loss: float = 0.20       # -20% forced liquidation (can't be bypassed)
    max_positions: int = 5             # Max concurrent positions


# ── Signal Validation ───────────────────────────────────────────────────────

VALID_ACTIONS = {"long", "short", "close", "close_long", "close_short"}


def validate_signal(sig: dict, bar_count: int) -> Optional[dict]:
    """Validate and normalize a trade signal."""
    if not isinstance(sig, dict):
        return None
    action = sig.get("action", "").lower()
    if action not in VALID_ACTIONS:
        return None
    bar = sig.get("bar", -1)
    if not isinstance(bar, (int, float)) or bar < 0 or bar >= bar_count:
        return None
    size = sig.get("size", 0.2)
    size = max(0.01, min(1.0, float(size)))
    return {
        "bar": int(bar),
        "action": action,
        "size": size,
        "reason": str(sig.get("reason", "")),
    }


# ── Execution Engine ────────────────────────────────────────────────────────

@dataclass
class Position:
    side: str           # "long" or "short"
    entry_price: float
    size: float         # fraction of equity
    entry_bar: int


@dataclass
class Trade:
    bar: int
    side: str
    entry_price: float
    exit_price: float
    pnl: float
    reason: str


def execute_signals(
    df: pd.DataFrame,
    signals: list[dict],
    config: BacktestConfig,
) -> dict:
    """Execute validated signals against candle data, compute PnL."""
    equity = config.initial_capital
    peak_equity = equity
    max_drawdown = 0.0
    positions: list[Position] = []
    trades: list[Trade] = []
    total_fees = 0.0
    pnl_curve = []
    curve_sample = max(1, len(df) // 500)

    # Sort signals by bar index
    signals.sort(key=lambda s: s["bar"])
    signal_idx = 0

    for i in range(len(df)):
        price = df.iloc[i]["close"]

        # ── Process signals at this bar ─────────────────────────────
        while signal_idx < len(signals) and signals[signal_idx]["bar"] == i:
            sig = signals[signal_idx]
            signal_idx += 1

            if sig["action"] in ("close", "close_long", "close_short"):
                # Close matching positions
                to_close = []
                for j, pos in enumerate(positions):
                    if sig["action"] == "close" or \
                       (sig["action"] == "close_long" and pos.side == "long") or \
                       (sig["action"] == "close_short" and pos.side == "short"):
                        to_close.append(j)
                for j in reversed(to_close):
                    pos = positions.pop(j)
                    raw_pnl = (price - pos.entry_price) / pos.entry_price if pos.side == "long" \
                              else (pos.entry_price - price) / pos.entry_price
                    trade_pnl = equity * pos.size * raw_pnl
                    fee = equity * pos.size * config.fee_rate
                    equity += trade_pnl - fee
                    total_fees += fee
                    trades.append(Trade(
                        bar=i, side=pos.side,
                        entry_price=pos.entry_price, exit_price=price,
                        pnl=trade_pnl - fee, reason=sig["reason"],
                    ))

            elif sig["action"] in ("long", "short"):
                if len(positions) >= config.max_positions:
                    continue  # Skip, max positions reached
                size = min(sig["size"], config.max_position_size)
                fee = equity * size * config.fee_rate
                equity -= fee
                total_fees += fee
                positions.append(Position(
                    side=sig["action"],
                    entry_price=price,
                    size=size,
                    entry_bar=i,
                ))

        # ── Hard stop loss check (server-side, can't bypass) ────────
        to_liquidate = []
        for j, pos in enumerate(positions):
            raw_pnl = (price - pos.entry_price) / pos.entry_price if pos.side == "long" \
                      else (pos.entry_price - price) / pos.entry_price
            if raw_pnl <= -config.hard_stop_loss:
                to_liquidate.append(j)
        for j in reversed(to_liquidate):
            pos = positions.pop(j)
            raw_pnl = (price - pos.entry_price) / pos.entry_price if pos.side == "long" \
                      else (pos.entry_price - price) / pos.entry_price
            trade_pnl = equity * pos.size * raw_pnl
            fee = equity * pos.size * config.fee_rate
            equity += trade_pnl - fee
            total_fees += fee
            trades.append(Trade(
                bar=i, side=pos.side,
                entry_price=pos.entry_price, exit_price=price,
                pnl=trade_pnl - fee, reason="HARD_STOP_LOSS",
            ))

        # ── Drawdown tracking ───────────────────────────────────────
        # Include unrealized PnL in equity for DD calculation
        unrealized = 0.0
        for pos in positions:
            raw_pnl = (price - pos.entry_price) / pos.entry_price if pos.side == "long" \
                      else (pos.entry_price - price) / pos.entry_price
            unrealized += equity * pos.size * raw_pnl
        mark_equity = equity + unrealized

        peak_equity = max(peak_equity, mark_equity)
        dd = (peak_equity - mark_equity) / peak_equity if peak_equity > 0 else 0
        max_drawdown = max(max_drawdown, dd)

        if i % curve_sample == 0:
            pnl_curve.append(round((mark_equity - config.initial_capital) / config.initial_capital * 100, 2))

        # Liquidation check
        if equity <= config.initial_capital * 0.05:
            break

    # ── Close remaining positions at last price ─────────────────────
    last_price = df.iloc[-1]["close"]
    for pos in positions:
        raw_pnl = (last_price - pos.entry_price) / pos.entry_price if pos.side == "long" \
                  else (pos.entry_price - last_price) / pos.entry_price
        trade_pnl = equity * pos.size * raw_pnl
        fee = equity * pos.size * config.fee_rate
        equity += trade_pnl - fee
        total_fees += fee
        trades.append(Trade(
            bar=len(df) - 1, side=pos.side,
            entry_price=pos.entry_price, exit_price=last_price,
            pnl=trade_pnl - fee, reason="end_of_backtest",
        ))

    pnl_curve.append(round((equity - config.initial_capital) / config.initial_capital * 100, 2))

    # ── Compute stats ───────────────────────────────────────────────
    total_return = (equity - config.initial_capital) / config.initial_capital * 100
    win_trades = [t for t in trades if t.pnl > 0]
    lose_trades = [t for t in trades if t.pnl <= 0]
    win_rate = len(win_trades) / len(trades) * 100 if trades else 0
    gross_profit = sum(t.pnl for t in win_trades)
    gross_loss = abs(sum(t.pnl for t in lose_trades))
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else (99.9 if gross_profit > 0 else 0)

    # Sharpe from PnL curve
    returns = [pnl_curve[i] - pnl_curve[i - 1] for i in range(1, len(pnl_curve))]
    mean_ret = np.mean(returns) if returns else 0
    std_ret = np.std(returns, ddof=1) if len(returns) > 1 else 1
    sharpe = mean_ret / max(std_ret, 0.0001) * np.sqrt(252)

    return {
        "total_return_pct": round(total_return, 2),
        "max_drawdown_pct": round(max_drawdown * 100, 2),
        "sharpe_ratio": round(sharpe, 2),
        "win_rate": round(win_rate, 2),
        "total_trades": len(trades),
        "avg_trade_pnl": round(np.mean([t.pnl for t in trades]), 2) if trades else 0,
        "max_win": round(max((t.pnl for t in trades), default=0), 2),
        "max_loss": round(min((t.pnl for t in trades), default=0), 2),
        "profit_factor": round(profit_factor, 2),
        "total_fees": round(total_fees, 2),
        "pnl_curve": pnl_curve,
        "trades": [
            {"bar": t.bar, "side": t.side, "entry": t.entry_price,
             "exit": t.exit_price, "pnl": round(t.pnl, 2), "reason": t.reason}
            for t in trades
        ],
    }


# ── Strategy Loading ────────────────────────────────────────────────────────

def load_strategy_from_code(code: str):
    """Load a strategy function from code string. Returns the strategy callable."""
    # Write to temp file and import
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()
        spec = importlib.util.spec_from_file_location("user_strategy", f.name)
        mod = importlib.util.module_from_spec(spec)

        # Inject built-in indicators into module namespace
        from strategies import indicators
        for name in dir(indicators):
            if not name.startswith("_"):
                setattr(mod, name, getattr(indicators, name))

        spec.loader.exec_module(mod)

    if not hasattr(mod, "strategy"):
        raise ValueError("Strategy code must define a `strategy(df)` function")

    return mod.strategy


def load_strategy_from_file(path: str):
    """Load strategy function from a .py file."""
    with open(path) as f:
        return load_strategy_from_code(f.read())


# ── Public API ──────────────────────────────────────────────────────────────

def run_custom_backtest(
    code: str,
    df: pd.DataFrame,
    config: Optional[BacktestConfig] = None,
    max_retries: int = 0,
    fix_callback=None,
) -> dict:
    """
    Run a custom strategy backtest.

    Args:
        code: Python code string with strategy(df) function
        df: DataFrame with columns: timestamp, open, high, low, close, volume
        config: Backtest configuration
        max_retries: Number of auto-fix attempts (0 = no retries)
        fix_callback: async fn(code, error) -> fixed_code (AI-powered fix)

    Returns:
        Standard backtest result dict (same format as Rust engine)
    """
    if config is None:
        config = BacktestConfig()

    attempt = 0
    current_code = code

    # Normalize column names (backtest data uses ts/o/h/l/c/v)
    col_map = {"ts": "timestamp", "o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"}
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

    while True:
        try:
            strategy_fn = load_strategy_from_code(current_code)
            t0 = time.time()
            raw_signals = strategy_fn(df.copy())
            elapsed = (time.time() - t0) * 1000

            if not isinstance(raw_signals, list):
                raise ValueError(f"strategy() must return a list, got {type(raw_signals).__name__}")

            # Validate signals
            signals = []
            warnings = []
            for i, sig in enumerate(raw_signals):
                validated = validate_signal(sig, len(df))
                if validated:
                    signals.append(validated)
                else:
                    warnings.append(f"Signal #{i} invalid: {sig}")

            result = execute_signals(df, signals, config)
            result["elapsed_ms"] = round(elapsed)
            result["signals_total"] = len(raw_signals)
            result["signals_valid"] = len(signals)
            if warnings:
                result["warnings"] = warnings[:10]  # Cap at 10
            return result

        except Exception as e:
            attempt += 1
            error_msg = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"

            if attempt > max_retries or fix_callback is None:
                return {
                    "error": error_msg,
                    "attempt": attempt,
                    "code": current_code,
                }

            # Try AI auto-fix
            try:
                current_code = fix_callback(current_code, error_msg)
            except Exception:
                return {
                    "error": error_msg,
                    "fix_error": "Auto-fix failed",
                    "attempt": attempt,
                }


# ── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Custom strategy backtest")
    parser.add_argument("strategy_file", help="Path to strategy.py")
    parser.add_argument("--ticker", default="BTC", help="Ticker (BTC/ETH/SOL)")
    parser.add_argument("--days", type=int, default=90, help="Backtest period")
    parser.add_argument("--data-dir", default="./data/candles", help="Candle data directory")
    parser.add_argument("--capital", type=float, default=10000, help="Initial capital")
    args = parser.parse_args()

    # Load candle data
    data_file = Path(args.data_dir) / f"{args.ticker}.json"
    if not data_file.exists():
        print(f"Error: {data_file} not found. Run download_data.py first.", file=sys.stderr)
        sys.exit(1)

    with open(data_file) as f:
        raw = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(raw)
    if "ts" in df.columns:
        df = df.rename(columns={"ts": "timestamp", "o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"})

    # Slice to period
    if args.days > 0:
        bars_needed = args.days * 1440  # 1-min bars
        df = df.tail(bars_needed).reset_index(drop=True)

    # Load and run strategy
    with open(args.strategy_file) as f:
        code = f.read()

    config = BacktestConfig(initial_capital=args.capital)
    result = run_custom_backtest(code, df, config)

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2))
