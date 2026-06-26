#!/usr/bin/env python3
"""
portfolio_risk.py — Einstein Research Portfolio Risk Analyzer
=============================================================
Calculates comprehensive portfolio risk metrics using free data from Yahoo Finance.

Usage:
    python3 portfolio_risk.py --positions positions.csv
    python3 portfolio_risk.py --positions "AAPL:100:145,MSFT:50:310,NVDA:30:420"

Options:
    --positions     CSV file path or inline "TICKER:SHARES:COST_BASIS,..." string
    --lookback      Trading days of history (default: 252)
    --benchmark     SPY or QQQ (default: SPY)
    --var-confidence  Comma-separated confidence levels, e.g. "0.95,0.99" (default: both)
    --monte-carlo-sims  Number of MC simulations (default: 10000)
    --output-dir    Directory for report files (default: ./reports)
    --no-stress     Skip historical crisis stress tests
"""

import argparse
import json
import os
import sys
import warnings
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

try:
    import yfinance as yf
except ImportError:
    print("ERROR: yfinance not installed. Run: pip install yfinance numpy pandas scipy")
    sys.exit(1)

try:
    from scipy import stats
except ImportError:
    print("ERROR: scipy not installed. Run: pip install scipy")
    sys.exit(1)

# ─── Sector mapping (simplified GICS sectors via ETF proxies) ─────────────────
SECTOR_ETFS = {
    "XLK": "Technology",
    "XLF": "Financials",
    "XLV": "Health Care",
    "XLC": "Communication Services",
    "XLY": "Consumer Discretionary",
    "XLP": "Consumer Staples",
    "XLE": "Energy",
    "XLI": "Industrials",
    "XLB": "Materials",
    "XLRE": "Real Estate",
    "XLU": "Utilities",
}

# Known sector for common tickers (fallback if yfinance sector is unavailable)
KNOWN_SECTORS = {
    "AAPL": "Technology", "MSFT": "Technology", "NVDA": "Technology",
    "GOOGL": "Communication Services", "GOOG": "Communication Services",
    "META": "Communication Services", "AMZN": "Consumer Discretionary",
    "TSLA": "Consumer Discretionary", "BRK.B": "Financials", "JPM": "Financials",
    "V": "Financials", "MA": "Financials", "JNJ": "Health Care",
    "UNH": "Health Care", "LLY": "Health Care", "XOM": "Energy",
    "CVX": "Energy", "HD": "Consumer Discretionary", "PG": "Consumer Staples",
    "KO": "Consumer Staples", "WMT": "Consumer Staples",
    "SPY": "Broad Market ETF", "QQQ": "Tech ETF", "IWM": "Small Cap ETF",
    "TLT": "Bonds", "BIL": "Cash", "SGOV": "Cash", "GLD": "Gold",
    "SLV": "Commodities", "VNQ": "Real Estate",
}

# Historical crisis periods for stress testing
CRISIS_PERIODS = {
    "2008 GFC": {
        "start": "2008-09-01",
        "end": "2009-03-09",
        "description": "Global Financial Crisis — systematic collapse, credit freeze",
    },
    "2020 COVID": {
        "start": "2020-02-19",
        "end": "2020-03-23",
        "description": "COVID Flash Crash — pandemic panic, liquidity crisis",
    },
    "2022 Rate Hikes": {
        "start": "2022-01-03",
        "end": "2022-10-13",
        "description": "Fed rate hike cycle — duration risk, growth re-rating",
    },
}

# SPY benchmark sector weights (approximate, as of late 2024)
SPY_SECTOR_WEIGHTS = {
    "Technology": 0.31,
    "Financials": 0.13,
    "Health Care": 0.12,
    "Communication Services": 0.09,
    "Consumer Discretionary": 0.10,
    "Consumer Staples": 0.06,
    "Industrials": 0.08,
    "Energy": 0.04,
    "Materials": 0.02,
    "Real Estate": 0.02,
    "Utilities": 0.03,
}


# ─── Data Loading ─────────────────────────────────────────────────────────────

def parse_positions(positions_arg: str) -> pd.DataFrame:
    """Parse positions from CSV file path or inline 'TICKER:SHARES:COST,..." string."""
    if os.path.isfile(positions_arg):
        df = pd.read_csv(positions_arg)
        df.columns = [c.strip().lower() for c in df.columns]
        required = {"ticker", "shares"}
        if not required.issubset(df.columns):
            raise ValueError(f"CSV must have columns: {required}. Got: {list(df.columns)}")
        if "cost_basis" not in df.columns:
            df["cost_basis"] = 0.0
    else:
        # Inline format: "AAPL:100:145.5,MSFT:50:310"
        records = []
        for item in positions_arg.split(","):
            parts = item.strip().split(":")
            if len(parts) < 2:
                raise ValueError(f"Invalid position format: '{item}'. Expected TICKER:SHARES or TICKER:SHARES:COST_BASIS")
            ticker = parts[0].strip().upper()
            shares = float(parts[1].strip())
            cost_basis = float(parts[2].strip()) if len(parts) > 2 else 0.0
            records.append({"ticker": ticker, "shares": shares, "cost_basis": cost_basis})
        df = pd.DataFrame(records)

    df["ticker"] = df["ticker"].str.upper().str.strip()
    df["shares"] = pd.to_numeric(df["shares"], errors="coerce")
    df["cost_basis"] = pd.to_numeric(df["cost_basis"], errors="coerce").fillna(0.0)
    df = df[df["shares"] > 0].reset_index(drop=True)
    return df


def fetch_prices(tickers: list, lookback_days: int = 252, extra_history: int = 0) -> pd.DataFrame:
    """Download adjusted close prices for all tickers via yfinance."""
    total_days = lookback_days + extra_history + 30  # buffer for weekends/holidays
    start = (datetime.today() - timedelta(days=int(total_days * 1.5))).strftime("%Y-%m-%d")
    end = datetime.today().strftime("%Y-%m-%d")

    print(f"  Fetching price data for: {', '.join(tickers)}")
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)

    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw["Close"]
    else:
        prices = raw[["Close"]] if "Close" in raw.columns else raw

    # Ensure all requested tickers are present
    for t in tickers:
        if t not in prices.columns:
            print(f"  WARNING: No data for {t} — it will be excluded from analysis.")

    prices = prices.dropna(axis=1, how="all")
    return prices.tail(lookback_days + extra_history)


def fetch_crisis_data(tickers: list) -> dict:
    """Download price data for each historical crisis period."""
    crisis_data = {}
    # Fetch a wide window covering all crises
    start = "2007-01-01"
    end = datetime.today().strftime("%Y-%m-%d")

    print("  Fetching historical crisis data...")
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)

    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw["Close"]
    else:
        prices = raw[["Close"]] if "Close" in raw.columns else raw

    for name, period in CRISIS_PERIODS.items():
        window = prices.loc[period["start"]:period["end"]]
        # Calculate total return for each ticker over the crisis window
        if len(window) < 5:
            print(f"  WARNING: Insufficient data for crisis '{name}'")
            continue
        returns = (window.iloc[-1] / window.iloc[0]) - 1
        crisis_data[name] = {
            "returns": returns.to_dict(),
            "days": len(window),
            "description": period["description"],
        }
    return crisis_data


def get_sector(ticker: str) -> str:
    """Get sector for a ticker via yfinance, falling back to KNOWN_SECTORS."""
    if ticker in KNOWN_SECTORS:
        return KNOWN_SECTORS[ticker]
    try:
        info = yf.Ticker(ticker).info
        sector = info.get("sector", "Unknown")
        return sector if sector else "Unknown"
    except Exception:
        return "Unknown"


# ─── Risk Calculations ────────────────────────────────────────────────────────

def compute_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Compute daily log returns."""
    return np.log(prices / prices.shift(1)).dropna()


def compute_portfolio_weights(positions: pd.DataFrame, current_prices: pd.Series) -> pd.Series:
    """Compute dollar-weighted portfolio weights."""
    valid = positions[positions["ticker"].isin(current_prices.index)].copy()
    valid["current_price"] = valid["ticker"].map(current_prices)
    valid["market_value"] = valid["shares"] * valid["current_price"]
    total_value = valid["market_value"].sum()
    valid["weight"] = valid["market_value"] / total_value
    return valid.set_index("ticker")["weight"]


def parametric_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """Calculate parametric (normal) VaR for a return series."""
    mu = returns.mean()
    sigma = returns.std()
    z = stats.norm.ppf(1 - confidence)
    return -(mu + z * sigma)


def historical_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """Calculate historical VaR from empirical return distribution."""
    return -np.percentile(returns, (1 - confidence) * 100)


def monte_carlo_var(
    returns: pd.DataFrame,
    weights: pd.Series,
    confidence: float = 0.95,
    n_sims: int = 10000,
) -> float:
    """
    Monte Carlo VaR using Cholesky decomposition for correlated simulations.
    Simulates 1-day portfolio returns and takes the empirical percentile.
    """
    aligned_tickers = [t for t in weights.index if t in returns.columns]
    w = weights[aligned_tickers].values
    r = returns[aligned_tickers].dropna()

    mu = r.mean().values
    cov = r.cov().values

    try:
        chol = np.linalg.cholesky(cov + np.eye(len(cov)) * 1e-8)
    except np.linalg.LinAlgError:
        chol = np.linalg.cholesky(np.diag(np.diag(cov)) + np.eye(len(cov)) * 1e-8)

    rand = np.random.standard_normal((n_sims, len(w)))
    sim_returns = rand @ chol.T + mu
    portfolio_returns = sim_returns @ w

    return -np.percentile(portfolio_returns, (1 - confidence) * 100)


def cvar(returns: pd.Series, confidence: float = 0.95) -> float:
    """Calculate CVaR (Expected Shortfall) — average loss beyond VaR threshold."""
    var = historical_var(returns, confidence)
    tail_returns = returns[returns <= -var]
    if len(tail_returns) == 0:
        return var
    return -tail_returns.mean()


def portfolio_returns_series(returns: pd.DataFrame, weights: pd.Series) -> pd.Series:
    """Compute portfolio daily returns from individual asset returns and weights."""
    aligned = [t for t in weights.index if t in returns.columns]
    w = weights[aligned]
    w = w / w.sum()
    return (returns[aligned] * w).sum(axis=1)


def max_drawdown(cumulative_returns: pd.Series) -> dict:
    """Calculate maximum drawdown and current drawdown from a returns series."""
    wealth = (1 + cumulative_returns).cumprod()
    rolling_max = wealth.cummax()
    drawdown_series = (wealth - rolling_max) / rolling_max

    max_dd = drawdown_series.min()
    max_dd_date = drawdown_series.idxmin()

    # Current drawdown
    current_peak = wealth.cummax().iloc[-1]
    current_value = wealth.iloc[-1]
    current_dd = (current_value - current_peak) / current_peak

    # Find when max drawdown started
    peak_before_max_dd = rolling_max.loc[:max_dd_date].idxmax()

    return {
        "max_drawdown_pct": float(max_dd * 100),
        "max_dd_start": str(peak_before_max_dd.date()),
        "max_dd_end": str(max_dd_date.date()),
        "current_drawdown_pct": float(current_dd * 100),
        "circuit_breaker_yellow": current_dd <= -0.10,
        "circuit_breaker_red": current_dd <= -0.20,
        "circuit_breaker_critical": current_dd <= -0.30,
    }


def correlation_matrix(returns: pd.DataFrame, weights: pd.Series) -> dict:
    """Compute correlation matrix and diversification score."""
    aligned = [t for t in weights.index if t in returns.columns]
    r = returns[aligned].dropna()
    corr = r.corr()

    # Diversification score: 1 - average pairwise absolute correlation (weighted)
    n = len(aligned)
    if n < 2:
        div_score = 100.0
    else:
        pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                pairs.append(abs(corr.iloc[i, j]))
        avg_corr = np.mean(pairs) if pairs else 0.0
        div_score = (1 - avg_corr) * 100

    # Flag highly correlated pairs (>0.85)
    high_corr_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            c = corr.iloc[i, j]
            if abs(c) > 0.85:
                high_corr_pairs.append({
                    "ticker_a": aligned[i],
                    "ticker_b": aligned[j],
                    "correlation": round(float(c), 4),
                })

    return {
        "matrix": {t: {u: round(float(corr.loc[t, u]), 4) for u in aligned} for t in aligned},
        "diversification_score": round(float(div_score), 1),
        "high_correlation_pairs": high_corr_pairs,
    }


def portfolio_beta(portfolio_ret: pd.Series, benchmark_ret: pd.Series) -> float:
    """Compute portfolio beta relative to benchmark."""
    aligned = portfolio_ret.align(benchmark_ret, join="inner")
    p, b = aligned[0].dropna(), aligned[1].dropna()
    common_idx = p.index.intersection(b.index)
    p, b = p[common_idx], b[common_idx]
    if len(p) < 20:
        return float("nan")
    cov = np.cov(p, b)
    return float(cov[0, 1] / cov[1, 1])


def sector_concentration(positions_df: pd.DataFrame, weights: pd.Series) -> dict:
    """Compute sector weights and concentration vs SPY benchmark."""
    sectors = {}
    for _, row in positions_df.iterrows():
        t = row["ticker"]
        if t not in weights.index:
            continue
        sector = get_sector(t)
        sectors[t] = sector

    # Aggregate weights by sector
    sector_weights = {}
    for t, w in weights.items():
        s = sectors.get(t, "Unknown")
        sector_weights[s] = sector_weights.get(s, 0.0) + float(w)

    # Compare to SPY benchmark
    concentration_flags = []
    for sector, weight in sector_weights.items():
        benchmark_weight = SPY_SECTOR_WEIGHTS.get(sector, 0.0)
        if benchmark_weight > 0:
            ratio = weight / benchmark_weight
            if ratio > 2.0:
                concentration_flags.append({
                    "sector": sector,
                    "portfolio_weight_pct": round(weight * 100, 1),
                    "spy_weight_pct": round(benchmark_weight * 100, 1),
                    "ratio": round(ratio, 2),
                })

    return {
        "sector_weights": {s: round(w * 100, 2) for s, w in sorted(sector_weights.items(), key=lambda x: -x[1])},
        "concentration_flags": concentration_flags,
        "ticker_sectors": sectors,
    }


def risk_budget(returns: pd.DataFrame, weights: pd.Series) -> dict:
    """
    Compute each position's marginal contribution to total portfolio VaR.
    Uses the component VaR approach: MCVAR_i = w_i * (Σw)_i / σ_portfolio
    """
    aligned = [t for t in weights.index if t in returns.columns]
    w = weights[aligned].values
    r = returns[aligned].dropna()
    cov = r.cov().values

    portfolio_variance = float(w @ cov @ w)
    portfolio_vol = np.sqrt(portfolio_variance)

    if portfolio_vol == 0:
        return {"contributions": {}, "portfolio_vol_daily_pct": 0.0}

    # Marginal contributions: (Σw)_i * w_i
    marginal = cov @ w
    contributions = w * marginal / portfolio_variance  # fraction of total variance

    budget = {}
    for i, t in enumerate(aligned):
        budget[t] = {
            "risk_contribution_pct": round(float(contributions[i]) * 100, 2),
            "portfolio_weight_pct": round(float(w[i]) * 100, 2),
            "risk_weight_ratio": round(float(contributions[i]) / float(w[i]), 2) if w[i] > 0 else 0.0,
        }

    return {
        "contributions": budget,
        "portfolio_vol_daily_pct": round(float(portfolio_vol * 100), 4),
        "portfolio_vol_annual_pct": round(float(portfolio_vol * np.sqrt(252) * 100), 2),
    }


def stress_test(
    positions_df: pd.DataFrame,
    weights: pd.Series,
    current_prices: pd.Series,
    crisis_data: dict,
) -> dict:
    """Apply historical crisis returns to current portfolio weights."""
    results = {}
    total_value = sum(
        row["shares"] * current_prices.get(row["ticker"], 0)
        for _, row in positions_df.iterrows()
        if row["ticker"] in current_prices.index
    )

    for crisis_name, data in crisis_data.items():
        crisis_returns = data["returns"]
        position_impacts = {}
        portfolio_impact = 0.0

        for t, w in weights.items():
            ret = crisis_returns.get(t)
            if ret is None or np.isnan(ret):
                continue
            impact_pct = float(ret) * 100
            dollar_impact = float(w) * total_value * float(ret)
            position_impacts[t] = {
                "return_pct": round(impact_pct, 2),
                "dollar_impact": round(dollar_impact, 2),
                "weight_pct": round(float(w) * 100, 2),
            }
            portfolio_impact += float(w) * float(ret)

        results[crisis_name] = {
            "portfolio_return_pct": round(portfolio_impact * 100, 2),
            "portfolio_dollar_impact": round(portfolio_impact * total_value, 2),
            "position_impacts": position_impacts,
            "description": data["description"],
            "trading_days": data["days"],
        }

    return results


# ─── Report Generation ────────────────────────────────────────────────────────

def format_markdown_report(report: dict) -> str:
    """Generate a human-readable Markdown report from risk data."""
    ts = report["generated_at"]
    lines = [
        f"# Portfolio Risk Report",
        f"*Generated: {ts}*",
        "",
        "---",
        "",
        "## Portfolio Summary",
        "",
        f"- **Total Market Value**: ${report['portfolio']['total_value']:,.2f}",
        f"- **Positions**: {report['portfolio']['position_count']}",
        f"- **Lookback Period**: {report['portfolio']['lookback_days']} trading days",
        f"- **Benchmark**: {report['portfolio']['benchmark']}",
        "",
    ]

    # VaR
    lines += ["## Value at Risk (1-Day)", ""]
    lines += ["| Method | 95% VaR | 99% VaR |", "|---|---|---|"]
    var = report["var"]
    lines += [
        f"| Parametric | {var['parametric_95_pct']:.2f}% | {var['parametric_99_pct']:.2f}% |",
        f"| Historical | {var['historical_95_pct']:.2f}% | {var['historical_99_pct']:.2f}% |",
        f"| Monte Carlo | {var['monte_carlo_95_pct']:.2f}% | {var['monte_carlo_99_pct']:.2f}% |",
        "",
    ]

    # CVaR
    lines += ["## CVaR / Expected Shortfall (1-Day)", ""]
    lines += ["| Confidence | CVaR |", "|---|---|"]
    lines += [
        f"| 95% | {report['cvar']['cvar_95_pct']:.2f}% |",
        f"| 99% | {report['cvar']['cvar_99_pct']:.2f}% |",
        "",
    ]

    # Drawdown
    dd = report["drawdown"]
    lines += ["## Maximum Drawdown", ""]
    lines += [
        f"- **Historical Max Drawdown**: {dd['max_drawdown_pct']:.2f}%",
        f"  - From: {dd['max_dd_start']} → {dd['max_dd_end']}",
        f"- **Current Drawdown**: {dd['current_drawdown_pct']:.2f}%",
        "",
    ]
    cb_status = []
    if dd["circuit_breaker_critical"]:
        cb_status.append("🚨 **CRITICAL** (>30% drawdown) — Go to 100% cash")
    elif dd["circuit_breaker_red"]:
        cb_status.append("🔴 **RED** (>20% drawdown) — Reduce 50% of positions")
    elif dd["circuit_breaker_yellow"]:
        cb_status.append("⚠️  **YELLOW** (>10% drawdown) — Review and document rationale")
    else:
        cb_status.append("✅ **GREEN** — Within normal range")
    lines += ["**Circuit Breaker Status**: " + cb_status[0], ""]

    # Correlation
    corr = report["correlation"]
    lines += [
        "## Correlation & Diversification",
        "",
        f"- **Diversification Score**: {corr['diversification_score']}/100",
        "",
    ]
    if corr["high_correlation_pairs"]:
        lines += ["**High-Correlation Pairs (>0.85):**", ""]
        for pair in corr["high_correlation_pairs"]:
            lines.append(f"- {pair['ticker_a']} ↔ {pair['ticker_b']}: {pair['correlation']:.3f}")
        lines.append("")

    # Beta
    beta = report["beta"]
    lines += ["## Portfolio Beta", ""]
    lines += ["| Benchmark | Beta |", "|---|---|"]
    for bmark, bval in beta.items():
        lines.append(f"| {bmark} | {bval:.3f} |")
    lines.append("")

    # Sector Concentration
    sec = report["sector_concentration"]
    lines += ["## Sector Concentration", "", "| Sector | Portfolio % | SPY % | Flag |", "|---|---|---|---|"]
    for sector, w_pct in sec["sector_weights"].items():
        spy_w = SPY_SECTOR_WEIGHTS.get(sector, 0.0) * 100
        flag = ""
        if spy_w > 0 and (w_pct / spy_w) > 2.0:
            flag = "⚠️  Overweight 2×+"
        elif sector in ("Unknown", "Bonds", "Cash", "Gold", "Commodities", "Broad Market ETF", "Tech ETF", "Small Cap ETF"):
            flag = "—"
        lines.append(f"| {sector} | {w_pct:.1f}% | {spy_w:.1f}% | {flag} |")
    lines.append("")

    # Risk Budget
    rb = report["risk_budget"]
    lines += [
        "## Risk Budget",
        "",
        f"- **Portfolio Daily Vol**: {rb['portfolio_vol_daily_pct']:.3f}%",
        f"- **Portfolio Annual Vol**: {rb['portfolio_vol_annual_pct']:.1f}%",
        "",
        "| Ticker | Weight % | Risk Contribution % | Risk/Weight Ratio |",
        "|---|---|---|---|",
    ]
    for t, data in sorted(rb["contributions"].items(), key=lambda x: -x[1]["risk_contribution_pct"]):
        flag = " ⚠️" if data["risk_contribution_pct"] > 25 else ""
        lines.append(
            f"| {t} | {data['portfolio_weight_pct']:.1f}% | {data['risk_contribution_pct']:.1f}%{flag} | {data['risk_weight_ratio']:.2f}x |"
        )
    lines.append("")

    # Stress Tests
    stress = report["stress_tests"]
    lines += ["## Historical Crisis Stress Tests", ""]
    for crisis_name, data in stress.items():
        direction = "📉" if data["portfolio_return_pct"] < 0 else "📈"
        lines += [
            f"### {direction} {crisis_name}",
            f"*{data['description']}*",
            "",
            f"- **Portfolio Return**: {data['portfolio_return_pct']:.2f}%",
            f"- **Dollar Impact**: ${data['portfolio_dollar_impact']:,.0f}",
            f"- **Trading Days**: {data['trading_days']}",
            "",
            "| Ticker | Weight % | Return % | Dollar Impact |",
            "|---|---|---|---|",
        ]
        sorted_impacts = sorted(
            data["position_impacts"].items(), key=lambda x: x[1]["return_pct"]
        )
        for t, imp in sorted_impacts:
            lines.append(
                f"| {t} | {imp['weight_pct']:.1f}% | {imp['return_pct']:.2f}% | ${imp['dollar_impact']:,.0f} |"
            )
        lines.append("")

    # Summary Actions
    lines += ["---", "", "## Action Items", ""]
    actions = []
    if report["var"]["historical_95_pct"] > report["var"]["parametric_95_pct"] * 1.5:
        actions.append("⚠️  Historical VaR significantly exceeds parametric — fat tails present. Consider protective puts.")
    if corr["diversification_score"] < 30:
        actions.append("⚠️  Diversification score < 30 — portfolio is concentrated. Add uncorrelated assets (TLT, GLD, or cash).")
    for pair in corr.get("high_correlation_pairs", []):
        actions.append(f"⚠️  {pair['ticker_a']} and {pair['ticker_b']} are highly correlated ({pair['correlation']:.2f}) — consider consolidating.")
    for t, data in rb["contributions"].items():
        if data["risk_contribution_pct"] > 25:
            actions.append(f"⚠️  {t} contributes {data['risk_contribution_pct']:.1f}% of portfolio risk but is {data['portfolio_weight_pct']:.1f}% of value — size down.")
    for flag in sec.get("concentration_flags", []):
        actions.append(f"⚠️  Sector '{flag['sector']}' is {flag['ratio']:.1f}× overweight vs SPY benchmark.")
    spy_beta = beta.get("SPY", float("nan"))
    if not np.isnan(spy_beta) and spy_beta > 1.3:
        actions.append(f"⚠️  Portfolio beta = {spy_beta:.2f} — amplified market exposure. Consider TLT/GLD/short-SPY hedge.")
    if dd["circuit_breaker_yellow"]:
        actions.append("🔴 Circuit breaker triggered — review drawdown protocol.")

    if not actions:
        actions.append("✅ No critical risk flags detected. Continue monitoring.")

    for a in actions:
        lines.append(f"- {a}")

    lines += ["", "*Report generated by einstein-research-portfolio-risk v1.0.0*"]
    return "\n".join(lines)


# ─── Main Entry Point ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Einstein Research Portfolio Risk Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--positions",
        required=True,
        help="CSV file path or inline 'TICKER:SHARES:COST_BASIS,...' string",
    )
    parser.add_argument("--lookback", type=int, default=252, help="Trading days of history (default: 252)")
    parser.add_argument("--benchmark", default="SPY", choices=["SPY", "QQQ"], help="Benchmark (default: SPY)")
    parser.add_argument(
        "--var-confidence",
        default="0.95,0.99",
        help="Comma-separated confidence levels (default: '0.95,0.99')",
    )
    parser.add_argument("--monte-carlo-sims", type=int, default=10000, help="MC simulations (default: 10000)")
    parser.add_argument("--output-dir", default="reports", help="Output directory (default: ./reports)")
    parser.add_argument("--no-stress", action="store_true", help="Skip historical crisis stress tests")
    args = parser.parse_args()

    print("\n═══ Einstein Research: Portfolio Risk Analyzer ═══\n")

    # 1. Parse positions
    print("▶ Loading positions...")
    positions_df = parse_positions(args.positions)
    print(f"  {len(positions_df)} positions loaded: {', '.join(positions_df['ticker'].tolist())}")

    tickers = positions_df["ticker"].tolist()
    benchmarks = [args.benchmark, "QQQ" if args.benchmark == "SPY" else "SPY"]
    all_tickers = list(set(tickers + benchmarks))

    # 2. Fetch price data
    print(f"\n▶ Fetching {args.lookback}-day price history...")
    prices = fetch_prices(all_tickers, lookback_days=args.lookback)

    available_tickers = [t for t in tickers if t in prices.columns]
    if not available_tickers:
        print("ERROR: No price data available for any position.")
        sys.exit(1)

    current_prices = prices[available_tickers].iloc[-1]
    returns = compute_returns(prices)

    # 3. Weights
    weights = compute_portfolio_weights(positions_df, current_prices)
    total_value = sum(
        row["shares"] * current_prices.get(row["ticker"], 0)
        for _, row in positions_df.iterrows()
        if row["ticker"] in current_prices.index
    )

    portfolio_ret = portfolio_returns_series(returns[available_tickers], weights)

    print(f"  Portfolio value: ${total_value:,.2f}")
    print(f"  Available tickers: {', '.join(available_tickers)}")

    # 4. VaR calculations
    print("\n▶ Calculating Value at Risk...")
    np.random.seed(42)
    var_result = {
        "parametric_95_pct": round(parametric_var(portfolio_ret, 0.95) * 100, 4),
        "parametric_99_pct": round(parametric_var(portfolio_ret, 0.99) * 100, 4),
        "historical_95_pct": round(historical_var(portfolio_ret, 0.95) * 100, 4),
        "historical_99_pct": round(historical_var(portfolio_ret, 0.99) * 100, 4),
        "monte_carlo_95_pct": round(
            monte_carlo_var(returns[available_tickers], weights, 0.95, args.monte_carlo_sims) * 100, 4
        ),
        "monte_carlo_99_pct": round(
            monte_carlo_var(returns[available_tickers], weights, 0.99, args.monte_carlo_sims) * 100, 4
        ),
        "dollar_var_95_hist": round(historical_var(portfolio_ret, 0.95) * total_value, 2),
        "dollar_var_99_hist": round(historical_var(portfolio_ret, 0.99) * total_value, 2),
    }

    # 5. CVaR
    print("▶ Calculating CVaR / Expected Shortfall...")
    cvar_result = {
        "cvar_95_pct": round(cvar(portfolio_ret, 0.95) * 100, 4),
        "cvar_99_pct": round(cvar(portfolio_ret, 0.99) * 100, 4),
        "dollar_cvar_95": round(cvar(portfolio_ret, 0.95) * total_value, 2),
        "dollar_cvar_99": round(cvar(portfolio_ret, 0.99) * total_value, 2),
    }

    # 6. Maximum drawdown
    print("▶ Calculating drawdown and circuit breakers...")
    dd_result = max_drawdown(portfolio_ret)

    # 7. Correlation matrix
    print("▶ Computing correlation matrix and diversification score...")
    corr_result = correlation_matrix(returns[available_tickers], weights)

    # 8. Beta
    print(f"▶ Calculating portfolio beta vs {args.benchmark} and QQQ/SPY...")
    beta_result = {}
    for bmark in [args.benchmark, "QQQ" if args.benchmark == "SPY" else "SPY"]:
        if bmark in returns.columns:
            beta_result[bmark] = round(portfolio_beta(portfolio_ret, returns[bmark]), 4)
        else:
            beta_result[bmark] = float("nan")

    # 9. Sector concentration
    print("▶ Analyzing sector concentration...")
    sector_result = sector_concentration(positions_df[positions_df["ticker"].isin(available_tickers)], weights)

    # 10. Risk budget
    print("▶ Computing risk budget...")
    rb_result = risk_budget(returns[available_tickers], weights)

    # 11. Stress tests
    stress_result = {}
    if not args.no_stress:
        print("\n▶ Running historical crisis stress tests...")
        crisis_data = fetch_crisis_data(available_tickers)
        stress_result = stress_test(
            positions_df[positions_df["ticker"].isin(available_tickers)],
            weights,
            current_prices,
            crisis_data,
        )

    # 12. Assemble report
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = {
        "generated_at": ts,
        "portfolio": {
            "total_value": round(total_value, 2),
            "position_count": len(available_tickers),
            "lookback_days": args.lookback,
            "benchmark": args.benchmark,
            "weights": {t: round(float(w), 6) for t, w in weights.items()},
            "current_prices": {t: round(float(p), 4) for t, p in current_prices.items()},
        },
        "var": var_result,
        "cvar": cvar_result,
        "drawdown": dd_result,
        "correlation": corr_result,
        "beta": beta_result,
        "sector_concentration": sector_result,
        "risk_budget": rb_result,
        "stress_tests": stress_result,
    }

    # 13. Write outputs
    os.makedirs(args.output_dir, exist_ok=True)
    file_ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_path = os.path.join(args.output_dir, f"portfolio_risk_{file_ts}.json")
    md_path = os.path.join(args.output_dir, f"portfolio_risk_{file_ts}.md")

    with open(json_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    md_report = format_markdown_report(report)
    with open(md_path, "w") as f:
        f.write(md_report)

    # Print summary to console
    print("\n═══ RISK SUMMARY ═══\n")
    print(f"Portfolio Value:     ${total_value:,.2f}")
    print(f"Annual Volatility:   {rb_result['portfolio_vol_annual_pct']:.1f}%")
    print(f"VaR 95% (1-day):     {var_result['historical_95_pct']:.2f}%  (${var_result['dollar_var_95_hist']:,.0f})")
    print(f"VaR 99% (1-day):     {var_result['historical_99_pct']:.2f}%  (${var_result['dollar_var_99_hist']:,.0f})")
    print(f"CVaR 95% (1-day):    {cvar_result['cvar_95_pct']:.2f}%  (${cvar_result['dollar_cvar_95']:,.0f})")
    print(f"Max Drawdown:        {dd_result['max_drawdown_pct']:.2f}%")
    print(f"Current Drawdown:    {dd_result['current_drawdown_pct']:.2f}%")
    print(f"Diversif. Score:     {corr_result['diversification_score']}/100")
    print(f"Beta vs {args.benchmark}:       {beta_result.get(args.benchmark, float('nan')):.3f}")
    cb_map = {
        "circuit_breaker_critical": "🚨 CRITICAL",
        "circuit_breaker_red": "🔴 RED",
        "circuit_breaker_yellow": "⚠️  YELLOW",
    }
    cb_state = "✅ GREEN"
    for key, label in cb_map.items():
        if dd_result.get(key):
            cb_state = label
            break
    print(f"Circuit Breaker:     {cb_state}")

    if stress_result:
        print("\nCrisis Stress Tests:")
        for crisis, data in stress_result.items():
            print(f"  {crisis}: {data['portfolio_return_pct']:.2f}%  (${data['portfolio_dollar_impact']:,.0f})")

    print(f"\n📊 Full report:  {md_path}")
    print(f"📦 JSON data:    {json_path}\n")


if __name__ == "__main__":
    main()
