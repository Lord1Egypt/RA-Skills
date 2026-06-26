#!/usr/bin/env python3
"""
ClawSwap — Local Backtest Engine (Vectorized)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
High-performance strategy backtests on locally cached candle data.
Numpy-vectorized core — supports 200+ concurrent backtests.

Usage:
    python backtest.py --strategy mean_reversion --ticker BTC --days 180
    python backtest.py --strategy grid --ticker SOL --days 180 --json
    python backtest.py --strategy momentum --ticker ETH --json
"""

import argparse
import json
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

try:
    import numpy as np
    import pandas as pd
except ImportError:
    print("Missing: pip install numpy pandas")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent.parent))
from strategies import STRATEGY_MAP


@dataclass
class BacktestResult:
    strategy: str
    ticker: str
    days: int
    interval: str
    initial_equity: float
    final_equity: float
    total_return_pct: float
    sharpe_ratio: float
    max_drawdown_pct: float
    win_rate: float
    total_trades: int
    profit_factor: float
    avg_trade_pnl: float
    equity_curve: list = field(default_factory=list)
    elapsed_ms: int = 0


def load_candles(ticker, days, interval, data_dir):
    """Find and load candle CSV."""
    coin = ticker.upper()
    exact = data_dir / f"{coin}-{interval}-{days}d.csv"
    if exact.exists():
        return pd.read_csv(exact)
    candidates = sorted(data_dir.glob(f"{coin}-{interval}-*.csv"))
    if candidates:
        df = pd.read_csv(candidates[-1])
        cpd = {"1m": 1440, "5m": 288, "15m": 96, "1h": 24, "4h": 6, "1d": 1}
        return df.tail(days * cpd.get(interval, 1440))
    legacy = sorted(data_dir.glob(f"{coin}USDT-*-merged-*.csv"))
    if legacy:
        return pd.read_csv(legacy[-1])
    raise FileNotFoundError(
        f"No data for {coin}. Run: python scripts/download_data.py --tickers {coin} --days {days} --interval {interval}"
    )


# ── Vectorized strategy engines ────────────────────────────────

def _bt_mean_reversion(close, timestamps, cfg, initial_equity):
    """Vectorized mean reversion: buy on dip from rolling high, TP/SL exit."""
    lookback = getattr(cfg, 'lookback_candles', 96)
    entry_drop = getattr(cfg, 'entry_drop_pct', 2.0) / 100
    tp_pct = getattr(cfg, 'take_profit_pct', 1.5) / 100
    sl_pct = getattr(cfg, 'stop_loss_pct', 3.0) / 100
    leverage = getattr(cfg, 'leverage', 2.0)
    size_pct = getattr(cfg, 'position_size_pct', 0.2)
    fee_rate = 0.0005  # 5 bps

    n = len(close)
    # Rolling max over lookback window
    rolling_high = pd.Series(close).rolling(lookback, min_periods=1).max().values

    # Simulate trades
    equity = initial_equity
    trades = []
    equity_arr = np.empty(n + 1)
    equity_arr[0] = equity
    in_pos = False
    entry_px = 0.0

    for i in range(n):
        px = close[i]
        if not in_pos:
            if i >= lookback:
                drop = (rolling_high[i] - px) / rolling_high[i]
                if drop >= entry_drop:
                    entry_px = px
                    equity -= equity * size_pct * leverage * fee_rate
                    in_pos = True
        else:
            pnl_r = (px - entry_px) / entry_px
            if pnl_r >= tp_pct or pnl_r <= -sl_pct:
                pnl_usd = equity * size_pct * leverage * pnl_r
                fee = equity * size_pct * leverage * fee_rate
                equity += pnl_usd - fee
                trades.append(pnl_usd - fee)
                in_pos = False

        unreal = 0.0
        if in_pos and entry_px > 0:
            unreal = equity * size_pct * leverage * (px - entry_px) / entry_px
        equity_arr[i + 1] = equity + unreal

    # Close open
    if in_pos and entry_px > 0:
        pnl_r = (close[-1] - entry_px) / entry_px
        equity += equity * size_pct * leverage * pnl_r
        equity_arr[-1] = equity

    return equity, trades, equity_arr


def _bt_momentum(close, timestamps, cfg, initial_equity):
    """Vectorized momentum: buy on fast>slow MA crossover."""
    fast = getattr(cfg, 'fast_period', 12)
    slow = getattr(cfg, 'slow_period', 26)
    tp_pct = getattr(cfg, 'take_profit_pct', 3.0) / 100
    sl_pct = getattr(cfg, 'stop_loss_pct', 2.0) / 100
    leverage = getattr(cfg, 'leverage', 3.0)
    size_pct = getattr(cfg, 'position_size_pct', 0.15)
    fee_rate = 0.0005

    n = len(close)
    s = pd.Series(close)
    fast_ma = s.rolling(fast, min_periods=1).mean().values
    slow_ma = s.rolling(slow, min_periods=1).mean().values

    equity = initial_equity
    trades = []
    equity_arr = np.empty(n + 1)
    equity_arr[0] = equity
    in_pos = False
    entry_px = 0.0

    for i in range(slow, n):
        px = close[i]
        if not in_pos:
            if fast_ma[i] > slow_ma[i] and fast_ma[i - 1] <= slow_ma[i - 1]:
                entry_px = px
                equity -= equity * size_pct * leverage * fee_rate
                in_pos = True
        else:
            pnl_r = (px - entry_px) / entry_px
            if pnl_r >= tp_pct or pnl_r <= -sl_pct or (fast_ma[i] < slow_ma[i]):
                pnl_usd = equity * size_pct * leverage * pnl_r
                fee = equity * size_pct * leverage * fee_rate
                equity += pnl_usd - fee
                trades.append(pnl_usd - fee)
                in_pos = False

        unreal = 0.0
        if in_pos and entry_px > 0:
            unreal = equity * size_pct * leverage * (px - entry_px) / entry_px
        equity_arr[i + 1] = equity + unreal

    # Fill early indices
    equity_arr[:slow + 1] = initial_equity

    if in_pos and entry_px > 0:
        pnl_r = (close[-1] - entry_px) / entry_px
        equity += equity * size_pct * leverage * pnl_r
        equity_arr[-1] = equity

    return equity, trades, equity_arr


def _bt_grid(close, timestamps, cfg, initial_equity):
    """Vectorized grid: buy/sell at grid levels around a center price."""
    grid_pct = getattr(cfg, 'grid_spacing_pct', 1.0) / 100
    num_grids = getattr(cfg, 'num_grids', 10)
    leverage = getattr(cfg, 'leverage', 2.0)
    fee_rate = 0.0005

    n = len(close)
    # Center = median of first 1000 candles
    center = float(np.median(close[:min(1000, n)]))
    grid_size = equity_per_grid = initial_equity / num_grids

    # Grid levels
    buy_levels = [center * (1 - grid_pct * (i + 1)) for i in range(num_grids // 2)]
    sell_levels = [center * (1 + grid_pct * (i + 1)) for i in range(num_grids // 2)]

    equity = initial_equity
    trades = []
    equity_arr = np.empty(n + 1)
    equity_arr[0] = equity
    positions = {}  # level_idx -> entry_price

    for i in range(n):
        px = close[i]
        # Check buy levels
        for li, level in enumerate(buy_levels):
            if px <= level and li not in positions:
                positions[li] = px
                equity -= equity_per_grid * leverage * fee_rate
                break
        # Check sell levels / take profit on positions
        closed = []
        for li, ep in positions.items():
            pnl_r = (px - ep) / ep
            # Close if price returned to center or hit grid above
            if pnl_r >= grid_pct or pnl_r <= -grid_pct * 3:
                pnl_usd = equity_per_grid * leverage * pnl_r
                fee = equity_per_grid * leverage * fee_rate
                equity += pnl_usd - fee
                trades.append(pnl_usd - fee)
                closed.append(li)
        for li in closed:
            del positions[li]

        unreal = sum(
            equity_per_grid * leverage * (px - ep) / ep
            for ep in positions.values()
        )
        equity_arr[i + 1] = equity + unreal

    # Close all open
    for ep in positions.values():
        pnl_r = (close[-1] - ep) / ep
        equity += equity_per_grid * leverage * pnl_r
    equity_arr[-1] = equity

    return equity, trades, equity_arr


def _bt_class_fallback(df, StratClass, cfg, initial_equity, close, timestamps):
    """Generic fallback using strategy class interface (slower but universal)."""
    strategy = StratClass(cfg)
    leverage = getattr(cfg, 'leverage', 2.0)
    size_pct = getattr(cfg, 'position_size_pct', 0.15)
    fee_rate = 0.0005
    n = len(close)

    equity = initial_equity
    trades = []
    equity_arr = np.empty(n + 1)
    equity_arr[0] = equity
    in_pos = False
    entry_px = 0.0

    for i in range(n):
        candle = {
            "open": float(df.iloc[i]["open"]) if "open" in df.columns else close[i],
            "high": float(df.iloc[i]["high"]) if "high" in df.columns else close[i],
            "low": float(df.iloc[i]["low"]) if "low" in df.columns else close[i],
            "close": close[i],
            "volume": float(df.iloc[i]["volume"]) if "volume" in df.columns else 0,
        }
        px = close[i]
        if hasattr(strategy, 'on_candle'):
            strategy.on_candle(candle)

        if not in_pos:
            sig = strategy.get_signal() if hasattr(strategy, 'get_signal') else None
            if sig == "buy":
                entry_px = px
                equity -= equity * size_pct * leverage * fee_rate
                in_pos = True
                if hasattr(strategy, 'on_fill'):
                    strategy.on_fill("buy", px, f"t_{len(trades)}")
        else:
            exit_sig = strategy.get_exit_signal(px) if hasattr(strategy, 'get_exit_signal') else None
            if exit_sig:
                pnl_r = (px - entry_px) / entry_px
                pnl_usd = equity * size_pct * leverage * pnl_r
                fee = equity * size_pct * leverage * fee_rate
                equity += pnl_usd - fee
                trades.append(pnl_usd - fee)
                in_pos = False
                if hasattr(strategy, 'on_fill'):
                    strategy.on_fill("sell", px, f"t_{len(trades)}")

        unreal = equity * size_pct * leverage * (px - entry_px) / entry_px if in_pos and entry_px > 0 else 0
        equity_arr[i + 1] = equity + unreal

    if in_pos and entry_px > 0:
        equity += equity * size_pct * leverage * (close[-1] - entry_px) / entry_px
        equity_arr[-1] = equity

    return equity, trades, equity_arr


VECTORIZED = {
    "mean_reversion": _bt_mean_reversion,
    "momentum": _bt_momentum,
    "grid": _bt_grid,
}


def run_backtest(strategy_name, ticker, days, interval="1m",
                 initial_equity=10_000.0, config_overrides=None, data_dir=None):
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / "data" / "candles"

    t0 = time.time()
    df = load_candles(ticker, days, interval, data_dir)

    if len(df) < 50:
        raise ValueError(f"Not enough data: {len(df)} candles (need 50+)")

    # Get config from strategy map
    if strategy_name not in STRATEGY_MAP:
        raise ValueError(f"Unknown strategy: {strategy_name}. Available: {list(STRATEGY_MAP.keys())}")

    StratClass, CfgClass = STRATEGY_MAP[strategy_name]
    cfg_kwargs = {"ticker": ticker}
    if config_overrides:
        cfg_kwargs.update(config_overrides)
    cfg = CfgClass(**cfg_kwargs)

    # Extract numpy arrays
    close = df["close"].values.astype(np.float64)
    timestamps = df["timestamp"].values.astype(np.int64) if "timestamp" in df.columns else np.arange(len(df))

    # Run vectorized backtest (or fallback to class-based)
    bt_fn = VECTORIZED.get(strategy_name)
    if bt_fn is not None:
        equity, trades, equity_arr = bt_fn(close, timestamps, cfg, initial_equity)
    else:
        equity, trades, equity_arr = _bt_class_fallback(
            df, StratClass, cfg, initial_equity, close, timestamps
        )

    # Metrics
    n = len(close)
    ret = (equity - initial_equity) / initial_equity * 100

    # Max drawdown from equity array
    peak = np.maximum.accumulate(equity_arr)
    dd = (peak - equity_arr) / np.where(peak > 0, peak, 1) * 100
    max_dd = float(np.max(dd))

    # Sharpe from returns
    if len(equity_arr) > 2:
        rets = np.diff(equity_arr) / np.where(equity_arr[:-1] != 0, equity_arr[:-1], 1)
        rets = rets[np.isfinite(rets)]
        if len(rets) > 1 and np.std(rets) > 0:
            sharpe = float(np.mean(rets) / np.std(rets) * np.sqrt(252))
        else:
            sharpe = 0.0
    else:
        sharpe = 0.0

    wins = [t for t in trades if t > 0]
    losses = [t for t in trades if t <= 0]
    win_rate = len(wins) / len(trades) * 100 if trades else 0.0
    gp = sum(wins)
    gl = abs(sum(losses))
    pf = gp / gl if gl > 0 else (9.99 if gp > 0 else 0.0)
    avg = sum(trades) / len(trades) if trades else 0.0

    # Downsample equity curve to ~300 points with timestamps
    step = max(1, (n + 1) // 300)
    eq_with_ts = []
    for i in range(0, n + 1, step):
        ts = int(timestamps[min(i, n - 1)]) if i < n else int(timestamps[-1])
        eq_with_ts.append([ts, round(float(equity_arr[i]), 2)])

    return BacktestResult(
        strategy=strategy_name, ticker=ticker, days=days, interval=interval,
        initial_equity=initial_equity, final_equity=round(equity, 2),
        total_return_pct=round(ret, 2), sharpe_ratio=round(sharpe, 3),
        max_drawdown_pct=round(max_dd, 2), win_rate=round(win_rate, 1),
        total_trades=len(trades), profit_factor=round(pf, 2),
        avg_trade_pnl=round(avg, 2), equity_curve=eq_with_ts,
        elapsed_ms=int((time.time() - t0) * 1000),
    )


def print_ascii_chart(curve, width=50, height=12):
    if len(curve) < 2:
        return
    vals = [p[1] if isinstance(p, list) else p for p in curve]
    mn, mx = min(vals), max(vals)
    rng = mx - mn or 1
    step = max(1, len(vals) // width)
    sampled = [vals[i] for i in range(0, len(vals), step)][:width]

    chart = []
    for row in range(height, -1, -1):
        threshold = mn + (rng * row / height)
        line = ""
        for v in sampled:
            line += "█" if v >= threshold else " "
        label = f"${threshold:>10,.0f}" if row in (0, height // 2, height) else " " * 11
        chart.append(f"{label} │{line}")
    chart.append(" " * 11 + " └" + "─" * len(sampled))
    print("\n".join(chart))


def main():
    parser = argparse.ArgumentParser(description="ClawSwap local backtest")
    parser.add_argument("--strategy", default="mean_reversion", choices=list(STRATEGY_MAP.keys()))
    parser.add_argument("--ticker", default="BTC")
    parser.add_argument("--days", type=int, default=180)
    parser.add_argument("--interval", default="1m", choices=["1m", "5m", "15m", "1h"])
    parser.add_argument("--equity", type=float, default=10_000.0)
    parser.add_argument("--config", default="{}", help="JSON config overrides")
    parser.add_argument("--data-dir", default=None)
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--chart", action="store_true", help="Show ASCII equity chart")
    args = parser.parse_args()

    overrides = json.loads(args.config) if args.config else {}
    data_dir = Path(args.data_dir) if args.data_dir else None

    try:
        result = run_backtest(
            strategy_name=args.strategy, ticker=args.ticker, days=args.days,
            interval=args.interval, initial_equity=args.equity,
            config_overrides=overrides, data_dir=data_dir,
        )
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if args.json:
        print(json.dumps(asdict(result)))
        return

    sign = "+" if result.total_return_pct >= 0 else ""
    print(f"""
╔══ BACKTEST RESULTS ═══════════════════════════╗
  Strategy    : {result.strategy}
  Ticker      : {result.ticker}
  Period      : {result.days} days ({result.total_trades} trades)
  Interval    : {result.interval}

  Return      : {sign}{result.total_return_pct}%
  Sharpe      : {result.sharpe_ratio}
  Max DD      : -{result.max_drawdown_pct}%
  Win Rate    : {result.win_rate}%
  Profit Fac. : {result.profit_factor}
  Avg Trade   : ${result.avg_trade_pnl:,.2f}

  Initial Eq  : ${result.initial_equity:,.2f}
  Final Eq    : ${result.final_equity:,.2f}
  Elapsed     : {result.elapsed_ms}ms
╚═══════════════════════════════════════════════╝""")

    if args.chart or not args.json:
        print("\n  Equity Curve:")
        print_ascii_chart(result.equity_curve)
        print()


if __name__ == "__main__":
    main()
