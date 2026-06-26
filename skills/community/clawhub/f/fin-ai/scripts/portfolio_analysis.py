#!/usr/bin/env python3
"""Phase-1 portfolio analysis workflow.

This script intentionally reuses proven V2 snapshot logic before introducing
new abstractions. Holdings remain the truth source; the output matches the
retained V2 snapshot semantics.
"""

from __future__ import annotations

import argparse
import copy
import glob
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

from market_context import load_market_context
from paths import DEFAULT_PROFILE, bootstrap_portfolio_dir, resolve_portfolio_dir


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_holdings(portfolio_dir: Path, date_str: str) -> dict[str, Any]:
    path = portfolio_dir / "holdings" / f"{date_str}.json"
    if not path.exists():
        raise FileNotFoundError(f"Holdings not found for date {date_str}: {path}")
    return load_json(path)


def load_config(portfolio_dir: Path) -> dict[str, Any]:
    config_path = portfolio_dir / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Portfolio config not found: {config_path}")
    return load_json(config_path)


def load_previous_snapshot(portfolio_dir: Path, date_str: str) -> dict[str, Any] | None:
    snap_dir = portfolio_dir / "snapshots"
    files = sorted(glob.glob(str(snap_dir / "*.json")))
    for file_path in reversed(files):
        fname = Path(file_path).stem
        if fname < date_str:
            return load_json(Path(file_path))
    return None


def load_history_values(portfolio_dir: Path) -> list[tuple[str, float, float]]:
    csv_path = portfolio_dir / "history.csv"
    values: list[tuple[str, float, float]] = []
    if not csv_path.exists():
        return values

    with csv_path.open("r", encoding="utf-8") as f:
        header = f.readline().strip().split(",")
        date_idx = header.index("date") if "date" in header else 0
        val_idx = header.index("total_value") if "total_value" in header else 1
        cost_idx = header.index("total_cost") if "total_cost" in header else 2
        for line in f:
            parts = line.strip().split(",")
            if len(parts) > max(val_idx, cost_idx):
                try:
                    values.append((parts[date_idx], float(parts[val_idx]), float(parts[cost_idx])))
                except ValueError:
                    continue
    return values


def _add_warning(warnings: list[str], message: str) -> None:
    if message not in warnings:
        warnings.append(message)

def calculate_snapshot(
    holdings: dict[str, Any],
    prices: dict[str, float],
    currencies: dict[str, str],
    fx_rates: dict[str, float],
    prev_snapshot: dict[str, Any] | None,
    history_values: list[tuple[str, float, float]] | None = None,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    date_str = holdings["date"]
    currency_map_cfg = {
        "SHA": "CNY",
        "SHE": "CNY",
        "HKG": "HKD",
        "NASDAQ": "USD",
        "NYSE": "USD",
        "OTC": "CNY",
    }

    snapshot: dict[str, Any] = {
        "date": date_str,
        "generated_at": datetime.now().isoformat(),
        "fx_rates": fx_rates,
        "groups": {},
        "summary": {},
    }
    warning_messages = warnings if warnings is not None else []

    grand_total_value = 0.0
    grand_total_cost = 0.0

    for group_name, group_data in holdings.get("groups", {}).items():
        positions_out: list[dict[str, Any]] = []
        group_positions_value = 0.0

        for pos in group_data.get("positions", []):
            ticker = pos["ticker"]
            exchange = ticker.split(":")[0]
            currency = currencies.get(ticker, currency_map_cfg.get(exchange, "CNY"))
            fx = fx_rates.get(currency, 1.0)
            if currency not in fx_rates:
                _add_warning(warning_messages, f"{ticker} 使用未知币种 {currency}，汇率已回退为 1.0")
            current_price = prices.get(ticker, 0.0)
            if current_price == 0 and pos["quantity"] != 0:
                _add_warning(warning_messages, f"{ticker} 当前价格为 0，请确认是否为数据缺失或停牌")

            cost_price = pos.get("cost_price", 0)
            if cost_price == 0 and pos["quantity"] != 0:
                _add_warning(warning_messages, f"{ticker} 的 cost_price 为 0，收益率可能失真")

            market_value_local = current_price * pos["quantity"]
            market_value_cny = market_value_local * fx
            cost_value_cny = cost_price * pos["quantity"] * fx
            profit_cny = market_value_cny - cost_value_cny
            profit_pct = (profit_cny / cost_value_cny * 100) if cost_value_cny != 0 else 0.0

            positions_out.append(
                {
                    "name": pos.get("name", ""),
                    "ticker": ticker,
                    "quantity": pos["quantity"],
                    "cost_price": cost_price,
                    "current_price": current_price,
                    "currency": currency,
                    "fx_rate": fx,
                    "market_value_cny": round(market_value_cny, 2),
                    "cost_value_cny": round(cost_value_cny, 2),
                    "profit_cny": round(profit_cny, 2),
                    "profit_pct": round(profit_pct, 2),
                    "weight_in_group": 0,
                }
            )
            group_positions_value += market_value_cny

        fund = group_data.get("fund", 0)
        cash = group_data.get("cash", 0)
        group_total = group_positions_value + fund + cash
        raw_cost_basis = group_data.get("cost_basis", 0)
        positions_cost_basis_cny = sum(position["cost_value_cny"] for position in positions_out)
        # holdings 里的 cost_basis 在部分账户中是原币口径（例如 USD），
        # 这里统一以已换算后的持仓成本为准，避免组级收益率失真。
        cost_basis = round(positions_cost_basis_cny + fund + cash, 2)
        group_profit = group_total - cost_basis
        group_return_pct = (group_profit / cost_basis * 100) if cost_basis != 0 else 0.0

        for position in positions_out:
            position["weight_in_group"] = round(position["market_value_cny"] / group_total * 100, 1) if group_total else 0

        snapshot["groups"][group_name] = {
            "cost_basis": cost_basis,
            "input_cost_basis": raw_cost_basis,
            "positions": positions_out,
            "fund": fund,
            "cash": cash,
            "positions_value": round(group_positions_value, 2),
            "total_value": round(group_total, 2),
            "profit": round(group_profit, 2),
            "return_pct": round(group_return_pct, 2),
        }

        grand_total_value += group_total
        grand_total_cost += cost_basis

    grand_profit = grand_total_value - grand_total_cost
    grand_return_pct = (grand_profit / grand_total_cost * 100) if grand_total_cost else 0.0

    prev_value = grand_total_value
    prev_cost = grand_total_cost
    prev_date = None
    if history_values:
        prev_entries = [(d, v, c) for d, v, c in history_values if d < date_str]
        if prev_entries:
            prev_date, prev_value, prev_cost = prev_entries[-1]
    if prev_date is None and prev_snapshot:
        prev_value = prev_snapshot["summary"]["total_value"]
        prev_cost = prev_snapshot["summary"].get("total_cost", grand_total_cost)
        prev_date = prev_snapshot.get("date")

    daily_change = grand_total_value - prev_value
    daily_change_pct = (daily_change / prev_value * 100) if prev_value else 0.0

    capital_change = grand_total_cost - prev_cost
    if prev_snapshot and prev_snapshot.get("date") == prev_date:
        prev_cash_total = sum(group.get("cash", 0) for group in prev_snapshot.get("groups", {}).values())
        curr_cash_total = sum(group.get("cash", 0) for group in snapshot["groups"].values())
        capital_change = curr_cash_total - prev_cash_total

    market_daily_change = daily_change - capital_change
    market_daily_change_pct = (market_daily_change / prev_value * 100) if prev_value else 0.0

    history = [(d, v, c) for d, v, c in (history_values or []) if d < date_str]
    history.append((date_str, grand_total_value, grand_total_cost))

    market_daily_returns: list[tuple[str, float, float]] = []
    for i in range(1, len(history)):
        _, prev_v, prev_c = history[i - 1]
        curr_d, curr_v, curr_c = history[i]
        cap_change = curr_c - prev_c
        value_change = curr_v - prev_v
        market_change = value_change - cap_change
        market_return = market_change / prev_v if prev_v else 0.0
        market_daily_returns.append((curr_d, market_return, market_change))

    peak_value_for_dd = history[0][1]
    profit_at_peak = history[0][1] - history[0][2]
    for _, value, cost in history:
        if value > peak_value_for_dd:
            peak_value_for_dd = value
            profit_at_peak = value - cost

    current_profit = grand_total_value - grand_total_cost
    drawdown = ((current_profit - profit_at_peak) / peak_value_for_dd * 100) if peak_value_for_dd else 0.0

    month_first_day = date_str[:8] + "01"
    prev_month_entries = [(d, v) for d, v, _ in history if d < month_first_day]
    month_start_value = prev_month_entries[-1][1] if prev_month_entries else prev_value
    month_market_changes = [mc for d, _, mc in market_daily_returns if d >= month_first_day]
    month_market_change = sum(month_market_changes)
    month_return_pct = (month_market_change / month_start_value * 100) if month_start_value else 0.0
    month_net_change = grand_total_value - month_start_value

    daily_returns = [ret for _, ret, _ in market_daily_returns]
    sharpe_ratio = 0.0
    volatility_annual = 0.0
    win_rate = 0.0
    avg_win = 0.0
    avg_loss = 0.0
    profit_loss_ratio = 0.0
    if len(daily_returns) >= 5:
        mean_r = sum(daily_returns) / len(daily_returns)
        std_r = math.sqrt(sum((r - mean_r) ** 2 for r in daily_returns) / len(daily_returns))
        risk_free_daily = 0.02 / 252
        sharpe_ratio = round(((mean_r - risk_free_daily) / std_r * math.sqrt(252)) if std_r > 0 else 0, 2)
        volatility_annual = round(std_r * math.sqrt(252) * 100, 2)
        wins = [r for r in daily_returns if r > 0]
        losses = [r for r in daily_returns if r < 0]
        win_rate = round(len(wins) / len(daily_returns) * 100, 1)
        avg_win = round(sum(wins) / len(wins) * 100, 3) if wins else 0
        avg_loss = round(sum(losses) / len(losses) * 100, 3) if losses else 0
        profit_loss_ratio = round(abs(avg_win / avg_loss), 2) if avg_loss != 0 else 0

    snapshot["summary"] = {
        "total_value": round(grand_total_value, 2),
        "total_cost": grand_total_cost,
        "total_profit": round(grand_profit, 2),
        "total_return_pct": round(grand_return_pct, 2),
        "prev_date": prev_date,
        "prev_total_value": round(prev_value, 2),
        "daily_change": round(daily_change, 2),
        "daily_change_pct": round(daily_change_pct, 2),
        "capital_change": round(capital_change, 2),
        "market_daily_change": round(market_daily_change, 2),
        "market_daily_change_pct": round(market_daily_change_pct, 2),
        "max_drawdown_pct": round(drawdown, 2),
        "month_start_value": round(month_start_value, 2),
        "month_change": round(month_net_change, 2),
        "month_market_change": round(month_market_change, 2),
        "month_return_pct": round(month_return_pct, 2),
        "sharpe_ratio": sharpe_ratio,
        "volatility_annual": volatility_annual,
        "win_rate": win_rate,
        "avg_win_pct": avg_win,
        "avg_loss_pct": avg_loss,
        "profit_loss_ratio": profit_loss_ratio,
        "trading_days": len(daily_returns),
    }
    if warning_messages:
        snapshot["warnings"] = warning_messages

    return snapshot


def _validate_market_context(market_context: dict[str, Any]) -> dict[str, Any]:
    required_keys = ("prices", "currencies", "fx_rates")
    for key in required_keys:
        if key not in market_context or not isinstance(market_context[key], dict):
            raise ValueError(f"market_context.{key} must be an object")

    normalized = copy.deepcopy(market_context)
    normalized.setdefault("warnings", [])
    normalized.setdefault("meta", {})
    if not isinstance(normalized["warnings"], list):
        raise ValueError("market_context.warnings must be a list when provided")
    if not isinstance(normalized["meta"], dict):
        raise ValueError("market_context.meta must be an object when provided")

    normalized["prices"] = {ticker: float(price) for ticker, price in normalized["prices"].items()}
    normalized["currencies"] = {ticker: str(currency) for ticker, currency in normalized["currencies"].items()}
    normalized["fx_rates"] = {currency: float(rate) for currency, rate in normalized["fx_rates"].items()}
    normalized["fx_rates"].setdefault("CNY", 1.0)
    return normalized


def _load_external_market_context(path: Path) -> dict[str, Any]:
    return _validate_market_context(load_json(path))


def _required_tickers(holdings: dict[str, Any]) -> set[str]:
    return {
        pos["ticker"]
        for group in holdings.get("groups", {}).values()
        for pos in group.get("positions", [])
    }


def _merge_market_context(
    *,
    external_context: dict[str, Any],
    fallback_context: dict[str, Any],
    holdings: dict[str, Any],
) -> dict[str, Any]:
    merged = copy.deepcopy(external_context)
    merged.setdefault("warnings", [])
    merged.setdefault("meta", {})

    missing_tickers = sorted(
        ticker
        for ticker in _required_tickers(holdings)
        if ticker not in merged["prices"] or ticker not in merged["currencies"]
    )

    for ticker in missing_tickers:
        if ticker in fallback_context.get("prices", {}):
            merged["prices"][ticker] = fallback_context["prices"][ticker]
        if ticker in fallback_context.get("currencies", {}):
            merged["currencies"][ticker] = fallback_context["currencies"][ticker]
        if ticker in fallback_context.get("meta", {}):
            merged["meta"][ticker] = fallback_context["meta"][ticker]

    for currency, rate in fallback_context.get("fx_rates", {}).items():
        merged["fx_rates"].setdefault(currency, rate)

    for warning in fallback_context.get("warnings", []):
        if warning not in merged["warnings"]:
            merged["warnings"].append(warning)

    unresolved = sorted(
        ticker
        for ticker in _required_tickers(holdings)
        if ticker not in merged["prices"] or ticker not in merged["currencies"]
    )
    if missing_tickers:
        merged["warnings"].append(
            f"外部 market_context 缺少 {len(missing_tickers)} 个标的，已使用内置 source 补齐"
        )
    if unresolved:
        merged["warnings"].append(
            f"market_context 仍缺少 {len(unresolved)} 个标的：{', '.join(unresolved)}"
        )

    return _validate_market_context(merged)


def analyze_portfolio(
    portfolio_dir: Path,
    date_str: str,
    market_context_path: Path | None = None,
) -> dict[str, Any]:
    bootstrap_portfolio_dir(portfolio_dir)
    config = load_config(portfolio_dir)
    holdings = load_holdings(portfolio_dir, date_str)
    if market_context_path:
        external_context = _load_external_market_context(market_context_path)
        fallback_context = load_market_context(holdings, portfolio_dir, config)
        market_context = _merge_market_context(
            external_context=external_context,
            fallback_context=fallback_context,
            holdings=holdings,
        )
    else:
        market_context = load_market_context(holdings, portfolio_dir, config)
    prev_snapshot = load_previous_snapshot(portfolio_dir, date_str)
    history_values = load_history_values(portfolio_dir)
    return calculate_snapshot(
        holdings,
        market_context["prices"],
        market_context["currencies"],
        market_context["fx_rates"],
        prev_snapshot,
        history_values,
        market_context.get("warnings", []),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze portfolio from holdings and emit snapshot-aligned JSON.")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Target date YYYY-MM-DD")
    parser.add_argument(
        "--portfolio-dir",
        help="持仓数据目录；未提供时优先使用仓库内 engine/portfolio，否则使用用户 profile 目录",
    )
    parser.add_argument("--profile", default=DEFAULT_PROFILE, help="用户数据 profile 名，默认 default")
    parser.add_argument(
        "--market-context",
        help="外部 market_context JSON；提供后将跳过内置行情获取，适合 agent 先调用 CLI 后再注入结果",
    )
    parser.add_argument("--output", help="Optional path to write analysis JSON")
    args = parser.parse_args()

    portfolio_dir = resolve_portfolio_dir(portfolio_dir=args.portfolio_dir, profile=args.profile)
    market_context_path = Path(args.market_context).expanduser() if args.market_context else None
    result = analyze_portfolio(portfolio_dir, args.date, market_context_path)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
