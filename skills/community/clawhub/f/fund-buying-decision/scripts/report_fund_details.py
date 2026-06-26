from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import import_eastmoney_pingzhongdata as importer
import strategy_engine as engine


DEFAULT_DB_PATH = importer.DEFAULT_DB_PATH
DEFAULT_LOOKBACK_DAYS = 20


def load_default_alert_thresholds_pct() -> list[float]:
    params = engine.load_strategy_parameters()
    raw_values = params["price_state"]["dip_thresholds_pct"]
    return [float(value) for value in raw_values]


def normalize_alert_thresholds_pct(values: list[float] | None = None) -> list[float]:
    raw_values = values if values else load_default_alert_thresholds_pct()
    unique_values = sorted({float(value) for value in raw_values})
    if not unique_values:
        raise ValueError("At least one alert threshold percentage is required")
    return unique_values


def build_drawdown_alert_status(drawdown_pct: float | None, thresholds_pct: list[float] | None = None) -> dict[str, Any]:
    normalized_thresholds = normalize_alert_thresholds_pct(thresholds_pct)
    triggered_thresholds_pct = [
        value for value in normalized_thresholds if drawdown_pct is not None and drawdown_pct >= value
    ]
    untriggered_thresholds_pct = [value for value in normalized_thresholds if value not in triggered_thresholds_pct]
    return {
        "thresholds_pct": normalized_thresholds,
        "triggered_thresholds_pct": triggered_thresholds_pct,
        "untriggered_thresholds_pct": untriggered_thresholds_pct,
        "highest_triggered_threshold_pct": max(triggered_thresholds_pct) if triggered_thresholds_pct else None,
        "triggered": bool(triggered_thresholds_pct),
    }


def format_pct(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:.2f}%"


def format_num(value: float | None, digits: int = 4) -> str:
    if value is None:
        return "N/A"
    return f"{value:.{digits}f}"


def row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def init_connection(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    importer.init_db(connection)
    return connection


def ensure_snapshot(connection: sqlite3.Connection, fund_code: str, refresh: bool) -> int:
    latest_snapshot = connection.execute(
        """
        SELECT id
        FROM fund_snapshots
        WHERE fund_code = ?
        ORDER BY COALESCE(source_generated_at, fetched_at) DESC, id DESC
        LIMIT 1
        """,
        (fund_code,),
    ).fetchone()

    if latest_snapshot is not None and not refresh:
        return int(latest_snapshot["id"])

    raw_js = importer.fetch_pingzhongdata(fund_code)
    payload = importer.parse_var_assignments(raw_js)
    summary = importer.ingest_fund(connection, fund_code, raw_js, payload)
    connection.commit()
    return int(summary["snapshot_id"])


def fetch_latest_series_point(connection: sqlite3.Connection, snapshot_id: int, series_type: str) -> dict[str, Any] | None:
    row = connection.execute(
        """
        SELECT point_date, point_ts, value, secondary_value, text_value
        FROM fund_timeseries
        WHERE snapshot_id = ? AND series_type = ? AND value IS NOT NULL
        ORDER BY point_ts DESC
        LIMIT 1
        """,
        (snapshot_id, series_type),
    ).fetchone()
    return row_to_dict(row)


def fetch_recent_high(connection: sqlite3.Connection, snapshot_id: int, lookback_days: int) -> dict[str, Any] | None:
    rows = connection.execute(
        """
        SELECT point_date, point_ts, value
        FROM fund_timeseries
        WHERE snapshot_id = ? AND series_type = 'net_worth_trend' AND value IS NOT NULL
        ORDER BY point_ts DESC
        LIMIT ?
        """,
        (snapshot_id, lookback_days),
    ).fetchall()
    if not rows:
        return None
    best = max(rows, key=lambda row: row["value"])
    return {"point_date": best["point_date"], "point_ts": best["point_ts"], "value": best["value"]}


def fetch_return_metrics(connection: sqlite3.Connection, snapshot_id: int) -> dict[str, float | None]:
    rows = connection.execute(
        """
        SELECT period_code, return_pct
        FROM fund_return_metrics
        WHERE snapshot_id = ?
        """,
        (snapshot_id,),
    ).fetchall()
    return {str(row["period_code"]): row["return_pct"] for row in rows}


def fetch_latest_report_metrics(
    connection: sqlite3.Connection,
    snapshot_id: int,
    report_type: str,
) -> tuple[str | None, list[dict[str, Any]]]:
    category_row = connection.execute(
        """
        SELECT category
        FROM fund_report_metrics
        WHERE snapshot_id = ? AND report_type = ?
        ORDER BY category DESC
        LIMIT 1
        """,
        (snapshot_id, report_type),
    ).fetchone()
    if category_row is None:
        return None, []
    category = str(category_row["category"])
    rows = connection.execute(
        """
        SELECT metric_name, value, text_value, extra_json
        FROM fund_report_metrics
        WHERE snapshot_id = ? AND report_type = ? AND category = ?
        ORDER BY metric_name
        """,
        (snapshot_id, report_type, category),
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        result.append(
            {
                "metric_name": row["metric_name"],
                "value": row["value"],
                "text_value": row["text_value"],
                "extra": json.loads(row["extra_json"]) if row["extra_json"] else None,
            }
        )
    return category, result


def fetch_performance_metrics(connection: sqlite3.Connection, snapshot_id: int) -> dict[str, Any]:
    rows = connection.execute(
        """
        SELECT category, metric_name, value, text_value, extra_json
        FROM fund_report_metrics
        WHERE snapshot_id = ? AND report_type = 'performance_evaluation'
        ORDER BY category, metric_name
        """,
        (snapshot_id,),
    ).fetchall()
    result = {"average_score": None, "scores": []}
    for row in rows:
        if row["category"] == "__summary__" and row["metric_name"] == "average_score":
            result["average_score"] = row["value"]
            continue
        extra = json.loads(row["extra_json"]) if row["extra_json"] else None
        result["scores"].append(
            {
                "category": row["category"],
                "score": row["value"],
                "description": extra.get("description") if extra else None,
            }
        )
    return result


def fetch_managers(connection: sqlite3.Connection, snapshot_id: int) -> list[dict[str, Any]]:
    manager_rows = connection.execute(
        """
        SELECT manager_id, name, pic_url, star, work_time, fund_size_text, power_avg, power_as_of
        FROM fund_managers
        WHERE snapshot_id = ?
        ORDER BY name
        """,
        (snapshot_id,),
    ).fetchall()

    managers: list[dict[str, Any]] = []
    for manager in manager_rows:
        power_rows = connection.execute(
            """
            SELECT metric_name, metric_value, description
            FROM fund_manager_power_metrics
            WHERE snapshot_id = ? AND manager_id = ?
            ORDER BY metric_name
            """,
            (snapshot_id, manager["manager_id"]),
        ).fetchall()
        managers.append(
            {
                "manager_id": manager["manager_id"],
                "name": manager["name"],
                "star": manager["star"],
                "work_time": manager["work_time"],
                "fund_size_text": manager["fund_size_text"],
                "power_avg": manager["power_avg"],
                "power_as_of": manager["power_as_of"],
                "power_metrics": [dict(row) for row in power_rows],
            }
        )
    return managers


def fetch_asset_codes(connection: sqlite3.Connection, snapshot_id: int, asset_type: str) -> list[str]:
    rows = connection.execute(
        """
        SELECT raw_code
        FROM fund_asset_codes
        WHERE snapshot_id = ? AND asset_type = ?
        ORDER BY position_index
        """,
        (snapshot_id, asset_type),
    ).fetchall()
    return [str(row["raw_code"]) for row in rows if row["raw_code"]]


def fetch_similar_funds(connection: sqlite3.Connection, snapshot_id: int) -> dict[int, list[dict[str, Any]]]:
    rows = connection.execute(
        """
        SELECT bucket_index, rank_index, similar_fund_code, similar_fund_name, return_pct
        FROM fund_similar_funds
        WHERE snapshot_id = ?
        ORDER BY bucket_index, rank_index
        """,
        (snapshot_id,),
    ).fetchall()
    buckets: dict[int, list[dict[str, Any]]] = {}
    for row in rows:
        bucket_index = int(row["bucket_index"])
        buckets.setdefault(bucket_index, []).append(
            {
                "rank_index": row["rank_index"],
                "fund_code": row["similar_fund_code"],
                "fund_name": row["similar_fund_name"],
                "return_pct": row["return_pct"],
            }
        )
    return buckets


def build_report(connection: sqlite3.Connection, fund_code: str, snapshot_id: int, lookback_days: int) -> dict[str, Any]:
    fund = row_to_dict(
        connection.execute(
            """
            SELECT fund_code, fund_name, source_rate, current_rate, min_subscription, updated_at
            FROM funds
            WHERE fund_code = ?
            """,
            (fund_code,),
        ).fetchone()
    )
    snapshot = row_to_dict(
        connection.execute(
            """
            SELECT id, source_generated_at, fetched_at, source_url
            FROM fund_snapshots
            WHERE id = ?
            """,
            (snapshot_id,),
        ).fetchone()
    )
    if fund is None or snapshot is None:
        raise RuntimeError(f"Fund {fund_code} is not available in the local database.")

    latest_net_worth = fetch_latest_series_point(connection, snapshot_id, "net_worth_trend")
    latest_ac_worth = fetch_latest_series_point(connection, snapshot_id, "accumulated_worth_trend")
    latest_position_estimate = fetch_latest_series_point(connection, snapshot_id, "fund_shares_position")
    recent_high = fetch_recent_high(connection, snapshot_id, lookback_days)

    current_price = latest_net_worth["value"] if latest_net_worth else None
    high_value = recent_high["value"] if recent_high else None
    drawdown_pct = None
    if current_price not in (None, 0) and high_value not in (None, 0):
        drawdown_pct = (high_value - current_price) / high_value * 100

    return_metrics = fetch_return_metrics(connection, snapshot_id)
    asset_allocation_category, asset_allocation = fetch_latest_report_metrics(connection, snapshot_id, "asset_allocation")
    holder_category, holder_structure = fetch_latest_report_metrics(connection, snapshot_id, "holder_structure")
    buy_sell_category, buy_sedemption = fetch_latest_report_metrics(connection, snapshot_id, "buy_sedemption")
    performance = fetch_performance_metrics(connection, snapshot_id)
    drawdown_alerts = build_drawdown_alert_status(drawdown_pct)

    return {
        "fund": fund,
        "snapshot": snapshot,
        "latest_net_worth": latest_net_worth,
        "latest_accumulated_worth": latest_ac_worth,
        "recent_high": recent_high,
        "drawdown_pct": drawdown_pct,
        "drawdown_alerts": drawdown_alerts,
        "latest_position_estimate": latest_position_estimate,
        "return_metrics": return_metrics,
        "asset_allocation": {"category": asset_allocation_category, "rows": asset_allocation},
        "holder_structure": {"category": holder_category, "rows": holder_structure},
        "buy_sedemption": {"category": buy_sell_category, "rows": buy_sedemption},
        "performance": performance,
        "managers": fetch_managers(connection, snapshot_id),
        "stock_codes": fetch_asset_codes(connection, snapshot_id, "stock"),
        "bond_codes": fetch_asset_codes(connection, snapshot_id, "bond"),
        "similar_funds": fetch_similar_funds(connection, snapshot_id),
        "lookback_days": lookback_days,
    }


def render_report(report: dict[str, Any]) -> str:
    fund = report["fund"]
    snapshot = report["snapshot"]
    latest_net_worth = report["latest_net_worth"]
    latest_ac_worth = report["latest_accumulated_worth"]
    recent_high = report["recent_high"]
    latest_position_estimate = report["latest_position_estimate"]
    returns = report["return_metrics"]
    drawdown_alerts = report["drawdown_alerts"]
    alert_thresholds = ", ".join(format_pct(value) for value in drawdown_alerts["thresholds_pct"])
    alert_triggered = (
        ", ".join(format_pct(value) for value in drawdown_alerts["triggered_thresholds_pct"])
        if drawdown_alerts["triggered_thresholds_pct"]
        else "无"
    )
    alert_untriggered = (
        ", ".join(format_pct(value) for value in drawdown_alerts["untriggered_thresholds_pct"])
        if drawdown_alerts["untriggered_thresholds_pct"]
        else "无"
    )

    lines = [
        f"基金代码: {fund['fund_code']}",
        f"基金名称: {fund['fund_name']}",
        f"数据快照时间: {snapshot['source_generated_at'] or snapshot['fetched_at']}",
        f"数据来源: {snapshot['source_url']}",
        f"申购费率: 当前 {format_pct(fund['current_rate'])} / 原费率 {format_pct(fund['source_rate'])}",
        f"最小申购金额: {format_num(fund['min_subscription'], 2)}",
        "",
        "净值概览:",
        f"- 最新单位净值: {format_num(latest_net_worth['value']) if latest_net_worth else 'N/A'} ({latest_net_worth['point_date'] if latest_net_worth else 'N/A'})",
        f"- 最新累计净值: {format_num(latest_ac_worth['value']) if latest_ac_worth else 'N/A'} ({latest_ac_worth['point_date'] if latest_ac_worth else 'N/A'})",
        f"- 最近{report['lookback_days']}个交易日高点: {format_num(recent_high['value']) if recent_high else 'N/A'} ({recent_high['point_date'] if recent_high else 'N/A'})",
        f"- 距最近高点回撤: {format_pct(report['drawdown_pct'])}",
        f"- 回撤预警档位: {alert_thresholds}",
        f"- 已触发预警: {alert_triggered}",
        f"- 未触发预警: {alert_untriggered}",
        f"- 最新股票仓位估算: {format_pct(latest_position_estimate['value']) if latest_position_estimate else 'N/A'} ({latest_position_estimate['point_date'] if latest_position_estimate else 'N/A'})",
        "",
        "区间收益:",
        f"- 近1月: {format_pct(returns.get('1_month'))}",
        f"- 近3月: {format_pct(returns.get('3_months'))}",
        f"- 近6月: {format_pct(returns.get('6_months'))}",
        f"- 近1年: {format_pct(returns.get('1_year'))}",
    ]

    performance = report["performance"]
    if performance["average_score"] is not None:
        lines.extend(
            [
                "",
                "绩效评价:",
                f"- 综合评分: {format_num(performance['average_score'], 2)}",
            ]
        )
        for item in performance["scores"]:
            lines.append(f"- {item['category']}: {format_num(item['score'], 2)}")

    asset_allocation = report["asset_allocation"]
    if asset_allocation["rows"]:
        lines.extend(["", f"最新资产配置 ({asset_allocation['category']}):"])
        for row in asset_allocation["rows"]:
            value = format_num(row["value"], 2) if row["value"] is not None else row["text_value"]
            lines.append(f"- {row['metric_name']}: {value}")

    holder_structure = report["holder_structure"]
    if holder_structure["rows"]:
        lines.extend(["", f"最新持有人结构 ({holder_structure['category']}):"])
        for row in holder_structure["rows"]:
            value = format_num(row["value"], 2) if row["value"] is not None else row["text_value"]
            lines.append(f"- {row['metric_name']}: {value}")

    buy_sedemption = report["buy_sedemption"]
    if buy_sedemption["rows"]:
        lines.extend(["", f"最新申赎概览 ({buy_sedemption['category']}):"])
        for row in buy_sedemption["rows"]:
            value = format_num(row["value"], 2) if row["value"] is not None else row["text_value"]
            lines.append(f"- {row['metric_name']}: {value}")

    if report["managers"]:
        lines.extend(["", "基金经理:"])
        for manager in report["managers"]:
            lines.append(
                f"- {manager['name']} | 星级 {manager['star']} | 任职 {manager['work_time']} | 管理规模 {manager['fund_size_text']} | 综合 {format_num(manager['power_avg'], 2)}"
            )

    if report["stock_codes"]:
        lines.extend(["", "持仓股票代码:", f"- {', '.join(report['stock_codes'])}"])
    if report["bond_codes"]:
        lines.extend(["", "持仓债券代码:", f"- {', '.join(report['bond_codes'])}"])

    if report["similar_funds"]:
        lines.extend(["", "同类基金示例:"])
        for bucket_index, items in report["similar_funds"].items():
            preview = ", ".join(
                f"{item['fund_code']} {item['fund_name']} {format_pct(item['return_pct'])}"
                for item in items[:3]
            )
            lines.append(f"- 分组 {bucket_index}: {preview}")

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Show a detailed local report for a fund code.")
    parser.add_argument("fund_code", help="Fund code to report.")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help=f"SQLite path. Default: {DEFAULT_DB_PATH}")
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=DEFAULT_LOOKBACK_DAYS,
        help=f"Recent-high lookback window in trading days. Default: {DEFAULT_LOOKBACK_DAYS}",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Refresh from Eastmoney before showing the report.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the report payload as JSON.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    db_path = Path(args.db)
    with init_connection(db_path) as connection:
        snapshot_id = ensure_snapshot(connection, args.fund_code, args.refresh)
        report = build_report(connection, args.fund_code, snapshot_id, args.lookback_days)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print(render_report(report))


if __name__ == "__main__":
    main()
