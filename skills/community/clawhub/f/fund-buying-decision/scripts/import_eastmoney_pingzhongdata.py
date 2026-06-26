from __future__ import annotations

import argparse
import ast
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FUND_CODE = "011598"
DEFAULT_DB_DIR = Path.home() / ".fund_buying_decision"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "fund_buying_decision.db"
PINGZHONGDATA_URL = "https://fund.eastmoney.com/pingzhongdata/{fund_code}.js"
VAR_PATTERN = re.compile(r"var\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*", re.MULTILINE)
SOURCE_GENERATED_AT_PATTERN = re.compile(r"/\*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\*/")


def fetch_pingzhongdata(fund_code: str, timeout: int = 20) -> str:
    url = PINGZHONGDATA_URL.format(fund_code=fund_code)
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/135.0.0.0 Safari/537.36"
            )
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except HTTPError as exc:
        raise RuntimeError(f"HTTP error while fetching fund {fund_code}: {exc.code}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error while fetching fund {fund_code}: {exc.reason}") from exc


def find_expression_end(source: str, start_index: int) -> int:
    depth = 0
    quote: str | None = None
    escaped = False
    in_line_comment = False
    in_block_comment = False
    index = start_index

    while index < len(source):
        char = source[index]
        next_char = source[index + 1] if index + 1 < len(source) else ""

        if in_line_comment:
            if char == "\n":
                in_line_comment = False
            index += 1
            continue

        if in_block_comment:
            if char == "*" and next_char == "/":
                in_block_comment = False
                index += 2
                continue
            index += 1
            continue

        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            index += 1
            continue

        if char == "/" and next_char == "/":
            in_line_comment = True
            index += 2
            continue

        if char == "/" and next_char == "*":
            in_block_comment = True
            index += 2
            continue

        if char in ("'", '"'):
            quote = char
            index += 1
            continue

        if char in "[{(":
            depth += 1
            index += 1
            continue

        if char in "]})":
            depth -= 1
            index += 1
            continue

        if char == ";" and depth == 0:
            return index

        index += 1

    raise ValueError("Could not find the end of a JS expression.")


def normalize_js_keywords(raw_value: str) -> str:
    output: list[str] = []
    quote: str | None = None
    escaped = False
    index = 0

    while index < len(raw_value):
        char = raw_value[index]

        if quote is not None:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            index += 1
            continue

        if char in ("'", '"'):
            quote = char
            output.append(char)
            index += 1
            continue

        if char.isalpha() or char == "_":
            end_index = index + 1
            while end_index < len(raw_value) and (
                raw_value[end_index].isalnum() or raw_value[end_index] == "_"
            ):
                end_index += 1
            token = raw_value[index:end_index]
            output.append(
                {
                    "true": "True",
                    "false": "False",
                    "null": "None",
                    "undefined": "None",
                    "NaN": "None",
                }.get(token, token)
            )
            index = end_index
            continue

        output.append(char)
        index += 1

    return "".join(output)


def parse_js_literal(raw_value: str) -> Any:
    try:
        return ast.literal_eval(normalize_js_keywords(raw_value))
    except (SyntaxError, ValueError) as exc:
        preview = raw_value[:200].replace("\n", " ")
        raise ValueError(f"Failed to parse JS literal: {preview}") from exc


def parse_var_assignments(js_text: str) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for match in VAR_PATTERN.finditer(js_text):
        name = match.group(1)
        expression_start = match.end()
        expression_end = find_expression_end(js_text, expression_start)
        raw_value = js_text[expression_start:expression_end].strip()
        payload[name] = parse_js_literal(raw_value)
    return payload


def extract_source_generated_at(js_text: str) -> str | None:
    match = SOURCE_GENERATED_AT_PATTERN.search(js_text)
    return match.group(1) if match else None


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def to_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def timestamp_ms_to_date(timestamp_ms: Any) -> str | None:
    if timestamp_ms in (None, ""):
        return None
    return datetime.fromtimestamp(int(timestamp_ms) / 1000, tz=timezone.utc).date().isoformat()


def normalize_code_list(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(value).strip()]


def init_db(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS funds (
            fund_code TEXT PRIMARY KEY,
            fund_name TEXT,
            is_hb INTEGER,
            source_rate REAL,
            current_rate REAL,
            min_subscription REAL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS fund_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fund_code TEXT NOT NULL,
            snapshot_key TEXT NOT NULL,
            source_generated_at TEXT,
            fetched_at TEXT NOT NULL,
            source_url TEXT NOT NULL,
            raw_js TEXT NOT NULL,
            raw_json TEXT NOT NULL,
            UNIQUE (fund_code, snapshot_key),
            FOREIGN KEY (fund_code) REFERENCES funds (fund_code)
        );

        CREATE TABLE IF NOT EXISTS fund_return_metrics (
            snapshot_id INTEGER NOT NULL,
            period_code TEXT NOT NULL,
            return_pct REAL,
            PRIMARY KEY (snapshot_id, period_code),
            FOREIGN KEY (snapshot_id) REFERENCES fund_snapshots (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS fund_asset_codes (
            snapshot_id INTEGER NOT NULL,
            asset_type TEXT NOT NULL,
            position_index INTEGER NOT NULL,
            raw_code TEXT,
            market_code TEXT,
            PRIMARY KEY (snapshot_id, asset_type, position_index),
            FOREIGN KEY (snapshot_id) REFERENCES fund_snapshots (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS fund_timeseries (
            snapshot_id INTEGER NOT NULL,
            series_type TEXT NOT NULL,
            series_name TEXT NOT NULL DEFAULT '',
            point_ts INTEGER NOT NULL,
            point_date TEXT,
            value REAL,
            secondary_value REAL,
            text_value TEXT,
            extra_json TEXT,
            PRIMARY KEY (snapshot_id, series_type, series_name, point_ts),
            FOREIGN KEY (snapshot_id) REFERENCES fund_snapshots (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS fund_report_metrics (
            snapshot_id INTEGER NOT NULL,
            report_type TEXT NOT NULL,
            category TEXT NOT NULL,
            metric_name TEXT NOT NULL,
            value REAL,
            text_value TEXT,
            extra_json TEXT,
            PRIMARY KEY (snapshot_id, report_type, category, metric_name),
            FOREIGN KEY (snapshot_id) REFERENCES fund_snapshots (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS fund_managers (
            snapshot_id INTEGER NOT NULL,
            manager_id TEXT NOT NULL,
            name TEXT NOT NULL,
            pic_url TEXT,
            star INTEGER,
            work_time TEXT,
            fund_size_text TEXT,
            power_avg REAL,
            power_as_of TEXT,
            raw_json TEXT NOT NULL,
            PRIMARY KEY (snapshot_id, manager_id),
            FOREIGN KEY (snapshot_id) REFERENCES fund_snapshots (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS fund_manager_power_metrics (
            snapshot_id INTEGER NOT NULL,
            manager_id TEXT NOT NULL,
            metric_name TEXT NOT NULL,
            metric_value REAL,
            description TEXT,
            PRIMARY KEY (snapshot_id, manager_id, metric_name),
            FOREIGN KEY (snapshot_id) REFERENCES fund_snapshots (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS fund_similar_funds (
            snapshot_id INTEGER NOT NULL,
            bucket_index INTEGER NOT NULL,
            rank_index INTEGER NOT NULL,
            similar_fund_code TEXT,
            similar_fund_name TEXT,
            return_pct REAL,
            raw_value TEXT NOT NULL,
            PRIMARY KEY (snapshot_id, bucket_index, rank_index),
            FOREIGN KEY (snapshot_id) REFERENCES fund_snapshots (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS strategy_accounts (
            account_id TEXT NOT NULL,
            fund_code TEXT NOT NULL,
            fund_type TEXT NOT NULL DEFAULT 'equity_fund',
            cash_pool REAL NOT NULL DEFAULT 0,
            position_units REAL NOT NULL DEFAULT 0,
            avg_cost_price REAL,
            note TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (account_id, fund_code)
        );

        CREATE TABLE IF NOT EXISTS strategy_trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT NOT NULL,
            fund_code TEXT NOT NULL,
            trade_date TEXT NOT NULL,
            trade_time_local TEXT,
            trade_type TEXT NOT NULL,
            direction TEXT NOT NULL,
            gross_amount REAL NOT NULL DEFAULT 0,
            price REAL,
            units REAL NOT NULL DEFAULT 0,
            fee_rate_pct REAL,
            fee_amount REAL NOT NULL DEFAULT 0,
            cash_delta REAL NOT NULL,
            units_delta REAL NOT NULL,
            note TEXT,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS strategy_reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT NOT NULL,
            fund_code TEXT NOT NULL,
            reminder_date TEXT NOT NULL,
            reminder_type TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'generated',
            created_at TEXT NOT NULL,
            UNIQUE (account_id, fund_code, reminder_date, reminder_type)
        );

        CREATE INDEX IF NOT EXISTS idx_fund_snapshots_code ON fund_snapshots (fund_code);
        CREATE INDEX IF NOT EXISTS idx_fund_timeseries_type_date ON fund_timeseries (series_type, point_date);
        CREATE INDEX IF NOT EXISTS idx_fund_reports_type_category ON fund_report_metrics (report_type, category);
        CREATE INDEX IF NOT EXISTS idx_strategy_trades_account_fund_date
            ON strategy_trades (account_id, fund_code, trade_date);
        CREATE INDEX IF NOT EXISTS idx_strategy_reminders_account_fund_date
            ON strategy_reminders (account_id, fund_code, reminder_date);
        """
    )


def upsert_fund(connection: sqlite3.Connection, payload: dict[str, Any], fetched_at: str) -> str:
    fund_code = str(payload.get("fS_code") or "").strip()
    if not fund_code:
        raise ValueError("Missing fS_code in payload.")

    connection.execute(
        """
        INSERT INTO funds (
            fund_code,
            fund_name,
            is_hb,
            source_rate,
            current_rate,
            min_subscription,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(fund_code) DO UPDATE SET
            fund_name = excluded.fund_name,
            is_hb = excluded.is_hb,
            source_rate = excluded.source_rate,
            current_rate = excluded.current_rate,
            min_subscription = excluded.min_subscription,
            updated_at = excluded.updated_at
        """,
        (
            fund_code,
            payload.get("fS_name"),
            1 if payload.get("ishb") else 0,
            to_float(payload.get("fund_sourceRate")),
            to_float(payload.get("fund_Rate")),
            to_float(payload.get("fund_minsg")),
            fetched_at,
        ),
    )
    return fund_code


def upsert_snapshot(
    connection: sqlite3.Connection,
    fund_code: str,
    source_url: str,
    source_generated_at: str | None,
    fetched_at: str,
    raw_js: str,
    payload: dict[str, Any],
) -> int:
    snapshot_key = source_generated_at or fetched_at
    raw_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    connection.execute(
        """
        INSERT INTO fund_snapshots (
            fund_code,
            snapshot_key,
            source_generated_at,
            fetched_at,
            source_url,
            raw_js,
            raw_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(fund_code, snapshot_key) DO UPDATE SET
            source_generated_at = excluded.source_generated_at,
            fetched_at = excluded.fetched_at,
            source_url = excluded.source_url,
            raw_js = excluded.raw_js,
            raw_json = excluded.raw_json
        """,
        (fund_code, snapshot_key, source_generated_at, fetched_at, source_url, raw_js, raw_json),
    )
    snapshot_id = connection.execute(
        "SELECT id FROM fund_snapshots WHERE fund_code = ? AND snapshot_key = ?",
        (fund_code, snapshot_key),
    ).fetchone()[0]
    return int(snapshot_id)


def clear_snapshot_tables(connection: sqlite3.Connection, snapshot_id: int) -> None:
    for table_name in (
        "fund_return_metrics",
        "fund_asset_codes",
        "fund_timeseries",
        "fund_report_metrics",
        "fund_managers",
        "fund_manager_power_metrics",
        "fund_similar_funds",
    ):
        connection.execute(f"DELETE FROM {table_name} WHERE snapshot_id = ?", (snapshot_id,))


def insert_return_metrics(connection: sqlite3.Connection, snapshot_id: int, payload: dict[str, Any]) -> int:
    inserted = 0
    mapping = {
        "1_year": payload.get("syl_1n"),
        "6_months": payload.get("syl_6y"),
        "3_months": payload.get("syl_3y"),
        "1_month": payload.get("syl_1y"),
    }
    for period_code, value in mapping.items():
        connection.execute(
            """
            INSERT INTO fund_return_metrics (snapshot_id, period_code, return_pct)
            VALUES (?, ?, ?)
            """,
            (snapshot_id, period_code, to_float(value)),
        )
        inserted += 1
    return inserted


def insert_asset_codes(connection: sqlite3.Connection, snapshot_id: int, payload: dict[str, Any]) -> int:
    inserted = 0
    stock_codes = normalize_code_list(payload.get("stockCodes"))
    stock_codes_new = normalize_code_list(payload.get("stockCodesNew"))
    bond_codes = normalize_code_list(payload.get("zqCodes"))
    bond_codes_new = normalize_code_list(payload.get("zqCodesNew"))

    for index, raw_code in enumerate(stock_codes, start=1):
        market_code = stock_codes_new[index - 1] if index - 1 < len(stock_codes_new) else None
        connection.execute(
            """
            INSERT INTO fund_asset_codes (snapshot_id, asset_type, position_index, raw_code, market_code)
            VALUES (?, ?, ?, ?, ?)
            """,
            (snapshot_id, "stock", index, raw_code, market_code),
        )
        inserted += 1

    for index, raw_code in enumerate(bond_codes, start=1):
        market_code = bond_codes_new[index - 1] if index - 1 < len(bond_codes_new) else None
        connection.execute(
            """
            INSERT INTO fund_asset_codes (snapshot_id, asset_type, position_index, raw_code, market_code)
            VALUES (?, ?, ?, ?, ?)
            """,
            (snapshot_id, "bond", index, raw_code, market_code),
        )
        inserted += 1

    return inserted


def insert_timeseries_point(
    connection: sqlite3.Connection,
    snapshot_id: int,
    series_type: str,
    point_ts: Any,
    value: Any,
    *,
    series_name: str = "",
    secondary_value: Any = None,
    text_value: Any = None,
    extra: dict[str, Any] | None = None,
) -> None:
    connection.execute(
        """
        INSERT INTO fund_timeseries (
            snapshot_id,
            series_type,
            series_name,
            point_ts,
            point_date,
            value,
            secondary_value,
            text_value,
            extra_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            snapshot_id,
            series_type,
            series_name or "",
            int(point_ts),
            timestamp_ms_to_date(point_ts),
            to_float(value),
            to_float(secondary_value),
            None if text_value in (None, "") else str(text_value),
            json.dumps(extra, ensure_ascii=False, separators=(",", ":")) if extra else None,
        ),
    )


def insert_timeseries(connection: sqlite3.Connection, snapshot_id: int, payload: dict[str, Any]) -> int:
    inserted = 0

    for point_ts, value in payload.get("Data_fundSharesPositions", []):
        insert_timeseries_point(connection, snapshot_id, "fund_shares_position", point_ts, value)
        inserted += 1

    for item in payload.get("Data_netWorthTrend", []):
        insert_timeseries_point(
            connection,
            snapshot_id,
            "net_worth_trend",
            item.get("x"),
            item.get("y"),
            secondary_value=item.get("equityReturn"),
            text_value=item.get("unitMoney"),
        )
        inserted += 1

    for point_ts, value in payload.get("Data_ACWorthTrend", []):
        insert_timeseries_point(connection, snapshot_id, "accumulated_worth_trend", point_ts, value)
        inserted += 1

    for series in payload.get("Data_grandTotal", []):
        for point_ts, value in series.get("data", []):
            insert_timeseries_point(
                connection,
                snapshot_id,
                "grand_total",
                point_ts,
                value,
                series_name=str(series.get("name") or ""),
            )
            inserted += 1

    for item in payload.get("Data_rateInSimilarType", []):
        insert_timeseries_point(
            connection,
            snapshot_id,
            "similar_type_rank",
            item.get("x"),
            item.get("y"),
            secondary_value=item.get("sc"),
        )
        inserted += 1

    for point_ts, value in payload.get("Data_rateInSimilarPersent", []):
        insert_timeseries_point(connection, snapshot_id, "similar_type_percent", point_ts, value)
        inserted += 1

    return inserted


def insert_report_metric(
    connection: sqlite3.Connection,
    snapshot_id: int,
    report_type: str,
    category: str,
    metric_name: str,
    *,
    value: Any = None,
    text_value: Any = None,
    extra: dict[str, Any] | None = None,
) -> None:
    connection.execute(
        """
        INSERT INTO fund_report_metrics (
            snapshot_id,
            report_type,
            category,
            metric_name,
            value,
            text_value,
            extra_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            snapshot_id,
            report_type,
            category,
            metric_name,
            to_float(value),
            None if text_value in (None, "") else str(text_value),
            json.dumps(extra, ensure_ascii=False, separators=(",", ":")) if extra else None,
        ),
    )


def insert_report_metrics(connection: sqlite3.Connection, snapshot_id: int, payload: dict[str, Any]) -> int:
    inserted = 0

    fluctuation = payload.get("Data_fluctuationScale") or {}
    for category, item in zip(fluctuation.get("categories", []), fluctuation.get("series", [])):
        insert_report_metric(connection, snapshot_id, "fluctuation_scale", category, "scale", value=item.get("y"))
        insert_report_metric(
            connection,
            snapshot_id,
            "fluctuation_scale",
            category,
            "mom",
            text_value=item.get("mom"),
        )
        inserted += 2

    holder_structure = payload.get("Data_holderStructure") or {}
    for series in holder_structure.get("series", []):
        for category, value in zip(holder_structure.get("categories", []), series.get("data", [])):
            insert_report_metric(
                connection,
                snapshot_id,
                "holder_structure",
                category,
                str(series.get("name") or ""),
                value=value,
            )
            inserted += 1

    asset_allocation = payload.get("Data_assetAllocation") or {}
    for series in asset_allocation.get("series", []):
        for category, value in zip(asset_allocation.get("categories", []), series.get("data", [])):
            insert_report_metric(
                connection,
                snapshot_id,
                "asset_allocation",
                category,
                str(series.get("name") or ""),
                value=value,
                extra={"yAxis": series.get("yAxis"), "type": series.get("type")},
            )
            inserted += 1

    performance = payload.get("Data_performanceEvaluation") or {}
    average_score = performance.get("avr")
    if average_score not in (None, ""):
        insert_report_metric(
            connection,
            snapshot_id,
            "performance_evaluation",
            "__summary__",
            "average_score",
            value=average_score,
        )
        inserted += 1
    for category, value, description in zip(
        performance.get("categories", []),
        performance.get("data", []),
        performance.get("dsc", []),
    ):
        insert_report_metric(
            connection,
            snapshot_id,
            "performance_evaluation",
            category,
            "score",
            value=value,
            extra={"description": description},
        )
        inserted += 1

    buy_sedemption = payload.get("Data_buySedemption") or {}
    for series in buy_sedemption.get("series", []):
        for category, value in zip(buy_sedemption.get("categories", []), series.get("data", [])):
            insert_report_metric(
                connection,
                snapshot_id,
                "buy_sedemption",
                category,
                str(series.get("name") or ""),
                value=value,
            )
            inserted += 1

    return inserted


def insert_managers(connection: sqlite3.Connection, snapshot_id: int, payload: dict[str, Any]) -> tuple[int, int]:
    manager_count = 0
    metric_count = 0

    for manager in payload.get("Data_currentFundManager", []):
        manager_id = str(manager.get("id") or "")
        if not manager_id:
            continue

        power = manager.get("power") or {}
        connection.execute(
            """
            INSERT INTO fund_managers (
                snapshot_id,
                manager_id,
                name,
                pic_url,
                star,
                work_time,
                fund_size_text,
                power_avg,
                power_as_of,
                raw_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                snapshot_id,
                manager_id,
                str(manager.get("name") or ""),
                manager.get("pic"),
                to_int(manager.get("star")),
                manager.get("workTime"),
                manager.get("fundSize"),
                to_float(power.get("avr")),
                power.get("jzrq"),
                json.dumps(manager, ensure_ascii=False, separators=(",", ":")),
            ),
        )
        manager_count += 1

        for metric_name, metric_value, description in zip(
            power.get("categories", []),
            power.get("data", []),
            power.get("dsc", []),
        ):
            connection.execute(
                """
                INSERT INTO fund_manager_power_metrics (
                    snapshot_id,
                    manager_id,
                    metric_name,
                    metric_value,
                    description
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (snapshot_id, manager_id, str(metric_name), to_float(metric_value), description),
            )
            metric_count += 1

    return manager_count, metric_count


def insert_similar_funds(connection: sqlite3.Connection, snapshot_id: int, payload: dict[str, Any]) -> int:
    inserted = 0
    for bucket_index, bucket in enumerate(payload.get("swithSameType", []), start=1):
        for rank_index, raw_value in enumerate(bucket, start=1):
            parts = str(raw_value).split("_", 2)
            similar_fund_code = parts[0] if len(parts) > 0 else None
            similar_fund_name = parts[1] if len(parts) > 1 else None
            return_pct = to_float(parts[2]) if len(parts) > 2 else None
            connection.execute(
                """
                INSERT INTO fund_similar_funds (
                    snapshot_id,
                    bucket_index,
                    rank_index,
                    similar_fund_code,
                    similar_fund_name,
                    return_pct,
                    raw_value
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    snapshot_id,
                    bucket_index,
                    rank_index,
                    similar_fund_code,
                    similar_fund_name,
                    return_pct,
                    str(raw_value),
                ),
            )
            inserted += 1
    return inserted


def ingest_fund(
    connection: sqlite3.Connection,
    fund_code: str,
    raw_js: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    fetched_at = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()
    source_generated_at = extract_source_generated_at(raw_js)
    source_url = PINGZHONGDATA_URL.format(fund_code=fund_code)

    normalized_fund_code = upsert_fund(connection, payload, fetched_at)
    snapshot_id = upsert_snapshot(
        connection,
        normalized_fund_code,
        source_url,
        source_generated_at,
        fetched_at,
        raw_js,
        payload,
    )
    clear_snapshot_tables(connection, snapshot_id)

    return_metrics = insert_return_metrics(connection, snapshot_id, payload)
    asset_codes = insert_asset_codes(connection, snapshot_id, payload)
    timeseries = insert_timeseries(connection, snapshot_id, payload)
    report_metrics = insert_report_metrics(connection, snapshot_id, payload)
    managers, manager_metrics = insert_managers(connection, snapshot_id, payload)
    similar_funds = insert_similar_funds(connection, snapshot_id, payload)

    return {
        "snapshot_id": snapshot_id,
        "fund_code": normalized_fund_code,
        "fund_name": payload.get("fS_name"),
        "source_generated_at": source_generated_at,
        "return_metrics": return_metrics,
        "asset_codes": asset_codes,
        "timeseries": timeseries,
        "report_metrics": report_metrics,
        "managers": managers,
        "manager_metrics": manager_metrics,
        "similar_funds": similar_funds,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch an Eastmoney pingzhongdata JS payload and store it in SQLite."
    )
    parser.add_argument(
        "fund_code",
        nargs="?",
        default=DEFAULT_FUND_CODE,
        help=f"Fund code to fetch. Default: {DEFAULT_FUND_CODE}",
    )
    parser.add_argument(
        "--db",
        default=str(DEFAULT_DB_PATH),
        help=f"SQLite path. Default: {DEFAULT_DB_PATH}",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    db_path = Path(args.db)
    ensure_parent_dir(db_path)

    raw_js = fetch_pingzhongdata(args.fund_code)
    payload = parse_var_assignments(raw_js)

    with sqlite3.connect(db_path) as connection:
        init_db(connection)
        summary = ingest_fund(connection, args.fund_code, raw_js, payload)
        connection.commit()

    print(f"Imported fund {summary['fund_code']} - {summary['fund_name']}")
    print(f"Database: {db_path.resolve()}")
    print(f"Snapshot ID: {summary['snapshot_id']}")
    print(f"Source generated at: {summary['source_generated_at'] or 'unknown'}")
    print(
        "Inserted rows: "
        f"returns={summary['return_metrics']}, "
        f"assets={summary['asset_codes']}, "
        f"timeseries={summary['timeseries']}, "
        f"reports={summary['report_metrics']}, "
        f"managers={summary['managers']}, "
        f"manager_metrics={summary['manager_metrics']}, "
        f"similar_funds={summary['similar_funds']}"
    )


if __name__ == "__main__":
    main()
