#!/usr/bin/env python3
"""
Einstein Research — Backtest Engine
=====================================
Programmatic backtesting framework supporting:
  - Multiple strategy types (momentum, mean reversion, factor, signal-based)
  - Walk-forward optimization (rolling and expanding windows)
  - Transaction cost modeling (commission, slippage, market impact)
  - Regime-aware performance splits (bull/bear/sideways)
  - Benchmark comparison (default: buy-and-hold SPY)
  - Full metrics: Sharpe, Sortino, Calmar, max drawdown, CAGR, win rate, profit factor

Usage:
    python3 backtest_engine.py --tickers SPY QQQ --start 2015-01-01 --end 2024-12-31 \
        --strategy momentum --commission 0.001 --slippage 0.0005 --output-dir reports/

    python3 backtest_engine.py --csv prices.csv --strategy mean_reversion --output-dir reports/

    python3 backtest_engine.py --tickers SPY AGG GLD --strategy dual_momentum \
        --walk-forward --train-months 24 --test-months 6 --output-dir reports/
"""

import argparse
import importlib.util
import json
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────────────────────────────────────
# Data Loading
# ──────────────────────────────────────────────────────────────────────────────

def fetch_prices(tickers: List[str], start: str, end: str) -> pd.DataFrame:
    """Download adjusted close prices via yfinance."""
    try:
        import yfinance as yf
    except ImportError:
        sys.exit("ERROR: yfinance not installed. Run: pip install yfinance")

    print(f"Fetching price data for {tickers} from {start} to {end} ...")
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)
    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw["Close"]
    else:
        prices = raw[["Close"]] if "Close" in raw.columns else raw
    prices.dropna(how="all", inplace=True)
    return prices


def load_csv_prices(path: str) -> pd.DataFrame:
    """Load prices from a CSV file. Expects Date index + ticker columns."""
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    df.sort_index(inplace=True)
    return df


# ──────────────────────────────────────────────────────────────────────────────
# Strategy Loader
# ──────────────────────────────────────────────────────────────────────────────

def load_builtin_strategy(name: str) -> Callable:
    """Load a strategy from strategy_templates.py."""
    templates_path = Path(__file__).parent / "strategy_templates.py"
    spec = importlib.util.spec_from_file_location("strategy_templates", templates_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn_map = {
        "momentum": "momentum_strategy",
        "mean_reversion": "mean_reversion_strategy",
        "dual_momentum": "dual_momentum_strategy",
    }
    fn_name = fn_map.get(name.lower(), name)
    if not hasattr(mod, fn_name):
        sys.exit(f"ERROR: Strategy '{fn_name}' not found in strategy_templates.py")
    return getattr(mod, fn_name)


def load_custom_strategy(strategy_file: str, strategy_fn: str) -> Callable:
    """Load a user-defined strategy function from an external file."""
    spec = importlib.util.spec_from_file_location("user_strategy", strategy_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, strategy_fn):
        sys.exit(f"ERROR: Function '{strategy_fn}' not found in {strategy_file}")
    return getattr(mod, strategy_fn)


# ──────────────────────────────────────────────────────────────────────────────
# Regime Detection
# ──────────────────────────────────────────────────────────────────────────────

def compute_regime(prices: pd.DataFrame, regime_ticker: str = "SPY", sma_window: int = 200,
                   sideways_band: float = 0.02) -> pd.Series:
    """
    Label each date as 'bull', 'bear', or 'sideways' based on regime_ticker vs its 200-day SMA.
    """
    if regime_ticker in prices.columns:
        ref = prices[regime_ticker]
    else:
        # Try fetching SPY separately
        try:
            import yfinance as yf
            spy = yf.download(regime_ticker, start=str(prices.index[0].date()),
                              end=str(prices.index[-1].date()), auto_adjust=True, progress=False)
            ref = spy["Close"].reindex(prices.index).ffill()
        except Exception:
            # Fallback: use first column
            ref = prices.iloc[:, 0]

    sma = ref.rolling(sma_window, min_periods=sma_window // 2).mean()
    ratio = (ref - sma) / sma
    regime = pd.Series("bull", index=prices.index)
    regime[ratio < -sideways_band] = "bear"
    regime[(ratio >= -sideways_band) & (ratio <= sideways_band)] = "sideways"
    return regime


# ──────────────────────────────────────────────────────────────────────────────
# Transaction Cost Modeling
# ──────────────────────────────────────────────────────────────────────────────

def apply_transaction_costs(returns: pd.Series, signals: pd.DataFrame,
                             commission: float = 0.001, slippage: float = 0.0005,
                             impact_model: str = "linear",
                             pessimistic: bool = False) -> pd.Series:
    """
    Subtract transaction costs from the strategy's gross returns.

    cost per trade = commission + slippage
    If pessimistic: slippage *= 2, commission *= 1.5
    If impact_model == 'sqrt': slippage component scaled by sqrt(turnover)
    """
    if pessimistic:
        slippage *= 2.0
        commission *= 1.5

    # Compute daily turnover as sum of absolute position changes across tickers
    if isinstance(signals, pd.DataFrame):
        turnover = signals.diff().abs().sum(axis=1)
    else:
        turnover = signals.diff().abs()

    if impact_model == "sqrt":
        cost_per_day = turnover * (commission + slippage * np.sqrt(turnover.clip(lower=0)))
    else:
        cost_per_day = turnover * (commission + slippage)

    net_returns = returns - cost_per_day.reindex(returns.index).fillna(0)
    return net_returns


# ──────────────────────────────────────────────────────────────────────────────
# Core Backtest Runner
# ──────────────────────────────────────────────────────────────────────────────

def run_backtest(prices: pd.DataFrame, strategy_fn: Callable,
                 initial_capital: float = 100_000,
                 commission: float = 0.001, slippage: float = 0.0005,
                 impact_model: str = "linear", pessimistic_costs: bool = False,
                 **strategy_params) -> Dict:
    """
    Run a single backtest.

    Returns a dict with:
      - equity_curve (pd.Series)
      - returns (pd.Series)
      - signals (pd.DataFrame or pd.Series)
      - metrics (dict)
    """
    # 1. Generate signals
    signals = strategy_fn(prices, **strategy_params)

    # Normalise signals: ensure DataFrame aligned to prices
    if isinstance(signals, pd.Series):
        signals = signals.to_frame(name=prices.columns[0] if len(prices.columns) == 1 else "signal")
    signals = signals.reindex(prices.index).fillna(0).clip(-1, 1)

    # 2. Compute daily asset returns
    asset_returns = prices.pct_change()

    # 3. Strategy gross returns: position(t-1) * return(t)  — lag to avoid look-ahead
    position = signals.shift(1).fillna(0)
    if isinstance(position, pd.DataFrame) and isinstance(asset_returns, pd.DataFrame):
        # Multi-asset: align columns, compute weighted sum
        common = position.columns.intersection(asset_returns.columns)
        gross_returns = (position[common] * asset_returns[common]).sum(axis=1)
    else:
        gross_returns = (position.squeeze() * asset_returns.squeeze())

    gross_returns = gross_returns.dropna()

    # 4. Apply transaction costs
    net_returns = apply_transaction_costs(
        gross_returns, signals,
        commission=commission, slippage=slippage,
        impact_model=impact_model, pessimistic=pessimistic_costs
    )

    # 5. Build equity curve
    equity_curve = (1 + net_returns).cumprod() * initial_capital

    # 6. Compute metrics
    metrics = compute_metrics(net_returns, equity_curve, initial_capital)

    return {
        "equity_curve": equity_curve,
        "returns": net_returns,
        "gross_returns": gross_returns,
        "signals": signals,
        "metrics": metrics,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Performance Metrics
# ──────────────────────────────────────────────────────────────────────────────

def compute_metrics(returns: pd.Series, equity_curve: pd.Series,
                    initial_capital: float = 100_000, rf: float = 0.0) -> Dict:
    """
    Compute comprehensive performance metrics.
    """
    returns = returns.dropna()
    if len(returns) == 0:
        return {}

    ann_factor = 252  # trading days per year
    total_days = len(returns)
    years = total_days / ann_factor

    # CAGR
    final_value = equity_curve.iloc[-1]
    cagr = (final_value / initial_capital) ** (1 / years) - 1 if years > 0 else 0.0

    # Volatility
    ann_vol = returns.std() * np.sqrt(ann_factor)

    # Sharpe
    excess = returns - rf / ann_factor
    sharpe = (excess.mean() / returns.std() * np.sqrt(ann_factor)) if returns.std() > 0 else 0.0

    # Sortino (downside deviation)
    downside = returns[returns < 0]
    downside_std = downside.std() * np.sqrt(ann_factor) if len(downside) > 1 else np.nan
    sortino = ((returns.mean() - rf / ann_factor) * ann_factor / downside_std
               if downside_std and downside_std > 0 else 0.0)

    # Max drawdown
    roll_max = equity_curve.cummax()
    drawdowns = (equity_curve - roll_max) / roll_max
    max_dd = drawdowns.min()
    # Drawdown duration
    in_dd = drawdowns < 0
    dd_groups = (in_dd != in_dd.shift()).cumsum()[in_dd]
    max_dd_duration = dd_groups.value_counts().max() if len(dd_groups) > 0 else 0

    # Calmar
    calmar = cagr / abs(max_dd) if max_dd != 0 else 0.0

    # Trade-level stats
    # A "trade" is a non-zero return day (simplification for daily signal strategies)
    winning = returns[returns > 0]
    losing = returns[returns < 0]
    win_rate = len(winning) / len(returns) if len(returns) > 0 else 0.0
    avg_win = winning.mean() if len(winning) > 0 else 0.0
    avg_loss = losing.mean() if len(losing) > 0 else 0.0
    gross_profit = winning.sum()
    gross_loss = abs(losing.sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf

    # Total return
    total_return = (final_value - initial_capital) / initial_capital

    return {
        "total_return_pct": round(total_return * 100, 2),
        "cagr_pct": round(cagr * 100, 2),
        "ann_volatility_pct": round(ann_vol * 100, 2),
        "sharpe_ratio": round(sharpe, 3),
        "sortino_ratio": round(sortino, 3),
        "calmar_ratio": round(calmar, 3),
        "max_drawdown_pct": round(max_dd * 100, 2),
        "max_drawdown_duration_days": int(max_dd_duration),
        "win_rate_pct": round(win_rate * 100, 2),
        "avg_win_pct": round(avg_win * 100, 4),
        "avg_loss_pct": round(avg_loss * 100, 4),
        "profit_factor": round(profit_factor, 3) if profit_factor != np.inf else "inf",
        "total_trading_days": total_days,
        "years_tested": round(years, 2),
        "initial_capital": initial_capital,
        "final_value": round(final_value, 2),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Benchmark
# ──────────────────────────────────────────────────────────────────────────────

def compute_benchmark(prices: pd.DataFrame, benchmark_ticker: str = "SPY",
                       initial_capital: float = 100_000) -> Dict:
    """Buy-and-hold benchmark."""
    if benchmark_ticker in prices.columns:
        bm_prices = prices[benchmark_ticker]
    else:
        try:
            import yfinance as yf
            raw = yf.download(benchmark_ticker,
                              start=str(prices.index[0].date()),
                              end=str(prices.index[-1].date()),
                              auto_adjust=True, progress=False)
            bm_prices = raw["Close"].reindex(prices.index).ffill()
        except Exception:
            bm_prices = prices.iloc[:, 0]

    bm_returns = bm_prices.pct_change().dropna()
    bm_equity = (1 + bm_returns).cumprod() * initial_capital
    bm_metrics = compute_metrics(bm_returns, bm_equity, initial_capital)
    bm_metrics["ticker"] = benchmark_ticker
    return {"equity_curve": bm_equity, "returns": bm_returns, "metrics": bm_metrics}


# ──────────────────────────────────────────────────────────────────────────────
# Walk-Forward Optimization
# ──────────────────────────────────────────────────────────────────────────────

def run_walk_forward(prices: pd.DataFrame, strategy_fn: Callable,
                     train_months: int = 24, test_months: int = 6,
                     wf_mode: str = "rolling",
                     initial_capital: float = 100_000,
                     commission: float = 0.001, slippage: float = 0.0005,
                     impact_model: str = "linear", pessimistic_costs: bool = False,
                     **strategy_params) -> Dict:
    """
    Walk-forward backtesting with rolling or expanding training windows.

    Returns aggregate OOS metrics + per-window breakdown.
    """
    dates = prices.index
    train_td = pd.DateOffset(months=train_months)
    test_td = pd.DateOffset(months=test_months)

    windows = []
    cursor = dates[0] + train_td
    while cursor + test_td <= dates[-1]:
        test_end = cursor + test_td
        if wf_mode == "expanding":
            train_start = dates[0]
        else:
            train_start = cursor - train_td
        train_end = cursor
        windows.append((train_start, train_end, cursor, test_end))
        cursor = test_end

    if not windows:
        sys.exit("ERROR: Not enough data for walk-forward with given window sizes.")

    print(f"Walk-forward: {len(windows)} windows ({wf_mode} mode)")

    all_oos_returns = []
    window_results = []

    for i, (tr_start, tr_end, te_start, te_end) in enumerate(windows):
        train_data = prices.loc[tr_start:tr_end]
        test_data = prices.loc[te_start:te_end]

        # In-sample backtest (for reference)
        is_result = run_backtest(train_data, strategy_fn, initial_capital, commission,
                                 slippage, impact_model, pessimistic_costs, **strategy_params)

        # Out-of-sample backtest
        oos_result = run_backtest(test_data, strategy_fn, initial_capital, commission,
                                  slippage, impact_model, pessimistic_costs, **strategy_params)

        all_oos_returns.append(oos_result["returns"])

        window_results.append({
            "window": i + 1,
            "train_start": str(tr_start.date()),
            "train_end": str(tr_end.date()),
            "test_start": str(te_start.date()),
            "test_end": str(te_end.date()),
            "is_sharpe": is_result["metrics"].get("sharpe_ratio"),
            "oos_sharpe": oos_result["metrics"].get("sharpe_ratio"),
            "is_cagr_pct": is_result["metrics"].get("cagr_pct"),
            "oos_cagr_pct": oos_result["metrics"].get("cagr_pct"),
            "oos_max_dd_pct": oos_result["metrics"].get("max_drawdown_pct"),
        })

        print(f"  Window {i+1}: IS Sharpe={is_result['metrics'].get('sharpe_ratio'):.2f} | "
              f"OOS Sharpe={oos_result['metrics'].get('sharpe_ratio'):.2f}")

    # Aggregate OOS returns
    combined_oos = pd.concat(all_oos_returns).sort_index()
    # Rebuild equity curve
    oos_equity = (1 + combined_oos).cumprod() * initial_capital
    agg_metrics = compute_metrics(combined_oos, oos_equity, initial_capital)

    # Degradation ratio: avg OOS Sharpe / avg IS Sharpe
    avg_is = np.mean([w["is_sharpe"] for w in window_results if w["is_sharpe"] is not None])
    avg_oos = np.mean([w["oos_sharpe"] for w in window_results if w["oos_sharpe"] is not None])
    degradation_ratio = avg_oos / avg_is if avg_is and avg_is != 0 else None

    return {
        "mode": wf_mode,
        "n_windows": len(windows),
        "train_months": train_months,
        "test_months": test_months,
        "aggregate_oos_metrics": agg_metrics,
        "avg_is_sharpe": round(avg_is, 3),
        "avg_oos_sharpe": round(avg_oos, 3),
        "degradation_ratio": round(degradation_ratio, 3) if degradation_ratio else None,
        "window_results": window_results,
        "oos_equity_curve": oos_equity,
        "oos_returns": combined_oos,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Regime-Aware Analysis
# ──────────────────────────────────────────────────────────────────────────────

def compute_regime_metrics(returns: pd.Series, regime: pd.Series,
                            initial_capital: float = 100_000) -> Dict:
    """Split returns by regime and compute metrics for each."""
    results = {}
    for r in ["bull", "bear", "sideways"]:
        mask = regime.reindex(returns.index) == r
        r_returns = returns[mask]
        if len(r_returns) < 5:
            results[r] = {"n_days": len(r_returns), "note": "insufficient data"}
            continue
        r_equity = (1 + r_returns).cumprod() * initial_capital
        m = compute_metrics(r_returns, r_equity, initial_capital)
        m["n_days"] = len(r_returns)
        results[r] = m
    return results


# ──────────────────────────────────────────────────────────────────────────────
# Report Generation
# ──────────────────────────────────────────────────────────────────────────────

def generate_report(strategy_name: str, backtest_result: Dict, benchmark_result: Dict,
                    regime_metrics: Dict, wf_result: Optional[Dict],
                    tickers: List[str], start: str, end: str,
                    commission: float, slippage: float,
                    pessimistic_costs: bool, output_dir: str) -> Tuple[str, str]:
    """Generate JSON + Markdown reports."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(output_dir, exist_ok=True)

    m = backtest_result["metrics"]
    bm = benchmark_result["metrics"]

    # ── JSON Report ─────────────────────────────────────────────────────────
    report_data = {
        "meta": {
            "strategy": strategy_name,
            "tickers": tickers,
            "start": start,
            "end": end,
            "commission": commission,
            "slippage": slippage,
            "pessimistic_costs": pessimistic_costs,
            "generated_at": datetime.now().isoformat(),
        },
        "strategy_metrics": m,
        "benchmark_metrics": bm,
        "regime_metrics": regime_metrics,
        "walk_forward": (
            {k: v for k, v in wf_result.items() if k not in ("oos_equity_curve", "oos_returns")}
            if wf_result else None
        ),
    }

    json_path = os.path.join(output_dir, f"backtest_{strategy_name}_{ts}.json")
    with open(json_path, "w") as f:
        json.dump(report_data, f, indent=2, default=str)

    # ── Markdown Report ──────────────────────────────────────────────────────
    bm_ticker = bm.get("ticker", "SPY")
    alpha_cagr = round(m.get("cagr_pct", 0) - bm.get("cagr_pct", 0), 2)
    alpha_sharpe = round(m.get("sharpe_ratio", 0) - bm.get("sharpe_ratio", 0), 3)

    md = f"""# Backtest Report: {strategy_name}
_Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}_

## Configuration
- **Tickers**: {", ".join(tickers)}
- **Period**: {start} → {end} ({m.get('years_tested', '?')} years)
- **Commission**: {commission*100:.2f} bps | **Slippage**: {slippage*100:.2f} bps
- **Pessimistic costs**: {"Yes" if pessimistic_costs else "No"}
- **Initial capital**: ${m.get('initial_capital', 100_000):,.0f}

---

## Performance Summary

| Metric | Strategy | {bm_ticker} (B&H) | Alpha |
|---|---|---|---|
| Total Return | {m.get('total_return_pct', '?')}% | {bm.get('total_return_pct', '?')}% | {round(m.get('total_return_pct', 0) - bm.get('total_return_pct', 0), 2)}% |
| CAGR | {m.get('cagr_pct', '?')}% | {bm.get('cagr_pct', '?')}% | {alpha_cagr}% |
| Sharpe Ratio | {m.get('sharpe_ratio', '?')} | {bm.get('sharpe_ratio', '?')} | {alpha_sharpe} |
| Sortino Ratio | {m.get('sortino_ratio', '?')} | {bm.get('sortino_ratio', '?')} | — |
| Calmar Ratio | {m.get('calmar_ratio', '?')} | {bm.get('calmar_ratio', '?')} | — |
| Max Drawdown | {m.get('max_drawdown_pct', '?')}% | {bm.get('max_drawdown_pct', '?')}% | — |
| Ann. Volatility | {m.get('ann_volatility_pct', '?')}% | {bm.get('ann_volatility_pct', '?')}% | — |
| Win Rate | {m.get('win_rate_pct', '?')}% | — | — |
| Profit Factor | {m.get('profit_factor', '?')} | — | — |
| Final Value | ${m.get('final_value', '?'):,.2f} | — | — |

---

## Regime Analysis

| Regime | Days | CAGR % | Sharpe | Max DD % |
|---|---|---|---|---|
"""
    for regime_name in ["bull", "bear", "sideways"]:
        rm = regime_metrics.get(regime_name, {})
        if "note" in rm:
            md += f"| {regime_name.capitalize()} | {rm.get('n_days', 0)} | insufficient data | — | — |\n"
        else:
            md += (f"| {regime_name.capitalize()} | {rm.get('n_days', '?')} | "
                   f"{rm.get('cagr_pct', '?')}% | {rm.get('sharpe_ratio', '?')} | "
                   f"{rm.get('max_drawdown_pct', '?')}% |\n")

    if wf_result:
        wm = wf_result["aggregate_oos_metrics"]
        md += f"""
---

## Walk-Forward Analysis ({wf_result['mode'].capitalize()} Windows)

- **Windows**: {wf_result['n_windows']} × ({wf_result['train_months']}m train / {wf_result['test_months']}m test)
- **Avg IS Sharpe**: {wf_result.get('avg_is_sharpe')} | **Avg OOS Sharpe**: {wf_result.get('avg_oos_sharpe')}
- **Degradation Ratio** (OOS/IS): {wf_result.get('degradation_ratio')} _(>0.5 is acceptable)_

### Aggregate OOS Performance
| Metric | Value |
|---|---|
| CAGR | {wm.get('cagr_pct', '?')}% |
| Sharpe | {wm.get('sharpe_ratio', '?')} |
| Max Drawdown | {wm.get('max_drawdown_pct', '?')}% |
| Win Rate | {wm.get('win_rate_pct', '?')}% |

### Per-Window Results
| Window | Train | Test | IS Sharpe | OOS Sharpe | OOS CAGR | OOS Max DD |
|---|---|---|---|---|---|---|
"""
        for w in wf_result["window_results"]:
            md += (f"| {w['window']} | {w['train_start']}→{w['train_end']} | "
                   f"{w['test_start']}→{w['test_end']} | "
                   f"{w['is_sharpe']} | {w['oos_sharpe']} | "
                   f"{w['oos_cagr_pct']}% | {w['oos_max_dd_pct']}% |\n")

    md += f"""
---

## Verdict

"""
    # Simple heuristic verdict
    sharpe = m.get("sharpe_ratio", 0) or 0
    dd = abs(m.get("max_drawdown_pct", 100) or 100)
    cagr = m.get("cagr_pct", 0) or 0
    degrade = wf_result.get("degradation_ratio") if wf_result else None

    if sharpe >= 1.0 and dd <= 20 and cagr > 0:
        if degrade is None or degrade >= 0.5:
            verdict = "✅ **DEPLOY CANDIDATE** — Strategy clears key thresholds. Proceed to paper trading."
        else:
            verdict = "🔄 **REFINE** — Good in-sample performance but significant walk-forward degradation. Revisit parameters."
    elif sharpe >= 0.5 and cagr > 0:
        verdict = "🔄 **REFINE** — Marginal metrics. Stress test further before considering live deployment."
    else:
        verdict = "❌ **ABANDON** — Metrics below acceptable thresholds. Reformulate hypothesis."

    md += verdict + "\n\n"
    md += f"_See `{os.path.basename(json_path)}` for full structured data._\n"

    md_path = os.path.join(output_dir, f"backtest_{strategy_name}_{ts}.md")
    with open(md_path, "w") as f:
        f.write(md)

    return json_path, md_path


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="Einstein Research Backtest Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    # Data source
    data_grp = p.add_mutually_exclusive_group(required=True)
    data_grp.add_argument("--tickers", nargs="+", help="Ticker symbols (e.g. SPY QQQ IWM)")
    data_grp.add_argument("--csv", help="Path to CSV price file (Date index, ticker columns)")

    p.add_argument("--start", default="2015-01-01", help="Start date YYYY-MM-DD (ignored with --csv)")
    p.add_argument("--end", default=datetime.now().strftime("%Y-%m-%d"), help="End date YYYY-MM-DD")

    # Strategy
    strat_grp = p.add_mutually_exclusive_group(required=True)
    strat_grp.add_argument("--strategy", choices=["momentum", "mean_reversion", "dual_momentum"],
                           help="Built-in strategy name")
    strat_grp.add_argument("--strategy-file", help="Path to Python file with custom strategy function")

    p.add_argument("--strategy-fn", default="strategy",
                   help="Function name in --strategy-file (default: 'strategy')")

    # Costs
    p.add_argument("--commission", type=float, default=0.001, help="Commission as fraction (default: 0.001 = 10bps)")
    p.add_argument("--slippage", type=float, default=0.0005, help="Slippage as fraction (default: 0.0005 = 5bps)")
    p.add_argument("--impact-model", choices=["linear", "sqrt"], default="linear")
    p.add_argument("--pessimistic-costs", action="store_true", help="Double slippage, +50%% commission")

    # Capital
    p.add_argument("--initial-capital", type=float, default=100_000)

    # Walk-forward
    p.add_argument("--walk-forward", action="store_true", help="Enable walk-forward analysis")
    p.add_argument("--train-months", type=int, default=24)
    p.add_argument("--test-months", type=int, default=6)
    p.add_argument("--wf-mode", choices=["rolling", "expanding"], default="rolling")

    # Regime
    p.add_argument("--regime-ticker", default="SPY", help="Ticker for regime detection (default: SPY)")

    # Benchmark
    p.add_argument("--benchmark-ticker", default="SPY", help="Benchmark ticker (default: SPY)")

    # Output
    p.add_argument("--output-dir", default="reports/", help="Output directory for reports")

    return p.parse_args()


def main():
    args = parse_args()

    # 1. Load prices
    if args.csv:
        prices = load_csv_prices(args.csv)
        tickers = list(prices.columns)
        start, end = str(prices.index[0].date()), str(prices.index[-1].date())
    else:
        prices = fetch_prices(args.tickers, args.start, args.end)
        tickers = args.tickers
        start, end = args.start, args.end

    print(f"Loaded {len(prices)} trading days × {len(prices.columns)} tickers")

    # 2. Load strategy
    if args.strategy_file:
        strategy_fn = load_custom_strategy(args.strategy_file, args.strategy_fn)
        strategy_name = args.strategy_fn
    else:
        strategy_fn = load_builtin_strategy(args.strategy)
        strategy_name = args.strategy

    print(f"Strategy: {strategy_name}")

    # 3. Full backtest
    print("\nRunning backtest...")
    result = run_backtest(
        prices, strategy_fn,
        initial_capital=args.initial_capital,
        commission=args.commission,
        slippage=args.slippage,
        impact_model=args.impact_model,
        pessimistic_costs=args.pessimistic_costs,
    )

    # 4. Benchmark
    benchmark_result = compute_benchmark(prices, args.benchmark_ticker, args.initial_capital)

    # 5. Regime analysis
    regime = compute_regime(prices, regime_ticker=args.regime_ticker)
    regime_metrics = compute_regime_metrics(result["returns"], regime, args.initial_capital)

    # 6. Walk-forward (optional)
    wf_result = None
    if args.walk_forward:
        print("\nRunning walk-forward analysis...")
        wf_result = run_walk_forward(
            prices, strategy_fn,
            train_months=args.train_months,
            test_months=args.test_months,
            wf_mode=args.wf_mode,
            initial_capital=args.initial_capital,
            commission=args.commission,
            slippage=args.slippage,
            impact_model=args.impact_model,
            pessimistic_costs=args.pessimistic_costs,
        )

    # 7. Generate reports
    print("\nGenerating reports...")
    json_path, md_path = generate_report(
        strategy_name=strategy_name,
        backtest_result=result,
        benchmark_result=benchmark_result,
        regime_metrics=regime_metrics,
        wf_result=wf_result,
        tickers=tickers,
        start=start,
        end=end,
        commission=args.commission,
        slippage=args.slippage,
        pessimistic_costs=args.pessimistic_costs,
        output_dir=args.output_dir,
    )

    # 8. Print summary to stdout
    m = result["metrics"]
    bm = benchmark_result["metrics"]
    print(f"""
╔══════════════════════════════════════════════════════╗
║  BACKTEST RESULTS: {strategy_name:<34}║
╠══════════════════════════════════════════════════════╣
║  Period : {start} → {end:<26}║
║  Capital: ${args.initial_capital:>10,.0f} → ${m.get('final_value', 0):>12,.2f}          ║
╠══════════════════════════════════════════════════════╣
║  Metric          Strategy    {bm.get('ticker','BM'):<6}       Alpha    ║
║  ─────────────────────────────────────────────────  ║
║  CAGR            {m.get('cagr_pct','?'):>7}%    {bm.get('cagr_pct','?'):>7}%   {round((m.get('cagr_pct',0) or 0)-(bm.get('cagr_pct',0) or 0),2):>+7}%  ║
║  Sharpe          {m.get('sharpe_ratio','?'):>8}   {bm.get('sharpe_ratio','?'):>8}          ║
║  Sortino         {m.get('sortino_ratio','?'):>8}                         ║
║  Calmar          {m.get('calmar_ratio','?'):>8}                         ║
║  Max Drawdown    {m.get('max_drawdown_pct','?'):>7}%                         ║
║  Win Rate        {m.get('win_rate_pct','?'):>7}%                         ║
║  Profit Factor   {str(m.get('profit_factor','?')):>8}                         ║
╠══════════════════════════════════════════════════════╣""")
    if wf_result:
        print(f"║  Walk-Forward OOS Sharpe: {wf_result.get('avg_oos_sharpe','?'):<4}  "
              f"Degradation: {wf_result.get('degradation_ratio','?'):<6}          ║")
    print(f"""╠══════════════════════════════════════════════════════╣
║  Reports saved to: {args.output_dir:<34}║
╚══════════════════════════════════════════════════════╝
""")
    print(f"  JSON: {json_path}")
    print(f"  MD:   {md_path}")


if __name__ == "__main__":
    main()
