#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import report_fund_details
import strategy_engine as engine


def load_default_lookback_days() -> int:
    params = engine.load_strategy_parameters()
    return int(params["price_state"]["recent_high_lookback_trading_days"])


def load_default_thresholds_pct() -> list[float]:
    params = engine.load_strategy_parameters()
    raw_values = params["price_state"]["dip_thresholds_pct"]
    return [float(value) for value in raw_values]


def normalize_thresholds_pct(values: list[float] | None) -> list[float]:
    raw_values = values if values else load_default_thresholds_pct()
    unique_values = sorted({float(value) for value in raw_values})
    if not unique_values:
        raise ValueError("At least one threshold percentage is required")
    return unique_values


def build_alert_payload(report: dict[str, Any], thresholds_pct: list[float]) -> dict[str, Any]:
    fund = report["fund"]
    latest_net_worth = report["latest_net_worth"] or {}
    recent_high = report["recent_high"] or {}
    current_price = latest_net_worth.get("value")
    recent_high_value = recent_high.get("value")
    drawdown_pct = report.get("drawdown_pct")
    triggered_thresholds_pct = [value for value in thresholds_pct if drawdown_pct is not None and drawdown_pct >= value]
    untriggered_thresholds_pct = [value for value in thresholds_pct if value not in triggered_thresholds_pct]
    triggered = bool(triggered_thresholds_pct)
    as_of_date = latest_net_worth.get("point_date") or report["snapshot"].get("source_generated_at")
    triggered_label = ", ".join(f"{value:.2f}%" for value in triggered_thresholds_pct) if triggered_thresholds_pct else "无"
    untriggered_label = ", ".join(f"{value:.2f}%" for value in untriggered_thresholds_pct) if untriggered_thresholds_pct else "无"
    return {
        "fund_code": fund["fund_code"],
        "fund_name": fund["fund_name"],
        "as_of_date": as_of_date,
        "current_price": current_price,
        "recent_high": recent_high_value,
        "drawdown_pct": drawdown_pct,
        "thresholds_pct": thresholds_pct,
        "triggered_thresholds_pct": triggered_thresholds_pct,
        "untriggered_thresholds_pct": untriggered_thresholds_pct,
        "highest_triggered_threshold_pct": max(triggered_thresholds_pct) if triggered_thresholds_pct else None,
        "triggered": triggered,
        "lookback_days": report["lookback_days"],
        "summary": (
            f"{fund['fund_code']} {fund['fund_name']} 回撤 "
            f"{drawdown_pct:.2f}% | 已触发阈值: {triggered_label} | 未触发阈值: {untriggered_label}"
            if drawdown_pct is not None
            else f"{fund['fund_code']} {fund['fund_name']} 缺少回撤数据"
        ),
    }


def render_text_result(result: dict[str, Any]) -> str:
    drawdown_label = f"{result['drawdown_pct']:.2f}%" if result["drawdown_pct"] is not None else "N/A"
    threshold_list = ", ".join(f"{value:.2f}%" for value in result["thresholds_pct"])
    triggered_list = (
        ", ".join(f"{value:.2f}%" for value in result["triggered_thresholds_pct"])
        if result["triggered_thresholds_pct"]
        else "无"
    )
    lines = [
        f"基金代码: {result['fund_code']}",
        f"基金名称: {result['fund_name']}",
        f"数据日期: {result['as_of_date']}",
        f"当前净值: {result['current_price'] if result['current_price'] is not None else 'N/A'}",
        f"最近高点: {result['recent_high'] if result['recent_high'] is not None else 'N/A'}",
        f"回撤幅度: {drawdown_label}",
        f"检查阈值: {threshold_list}",
        f"是否触发: {'是' if result['triggered'] else '否'}",
        f"已触发阈值: {triggered_list}",
        f"说明: {result['summary']}",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check whether a fund drawdown alert is triggered.")
    parser.add_argument("fund_code", help="Fund code to check.")
    parser.add_argument("--db", default=str(engine.DEFAULT_DB_PATH), help=f"SQLite path. Default: {engine.DEFAULT_DB_PATH}")
    parser.add_argument(
        "--threshold-pct",
        dest="thresholds_pct",
        action="append",
        type=float,
        help="Drawdown threshold percentage. Repeat this option for multiple tiers. Default: use SKILL.md dip_thresholds_pct",
    )
    parser.add_argument(
        "--lookback-days",
        type=int,
        help="Recent-high lookback window in trading days. Default: use SKILL.md price_state.recent_high_lookback_trading_days",
    )
    parser.add_argument("--refresh", action="store_true", help="Refresh fund data from Eastmoney before evaluating.")
    parser.add_argument("--json", action="store_true", help="Print the result as JSON.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    lookback_days = args.lookback_days if args.lookback_days is not None else load_default_lookback_days()
    thresholds_pct = normalize_thresholds_pct(args.thresholds_pct)
    db_path = Path(args.db)

    with report_fund_details.init_connection(db_path) as connection:
        snapshot_id = report_fund_details.ensure_snapshot(connection, args.fund_code, args.refresh)
        report = report_fund_details.build_report(connection, args.fund_code, snapshot_id, lookback_days)

    result = build_alert_payload(report, thresholds_pct)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text_result(result))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
