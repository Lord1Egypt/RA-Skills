from __future__ import annotations

import ast
import re
import sqlite3
import sys
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import import_eastmoney_pingzhongdata as importer


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = importer.DEFAULT_DB_PATH
SKILL_MD_PATH = REPO_ROOT / "SKILL.md"
SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")
BUY_TRADE_TYPES = {"buy_dca", "buy_dip", "manual_buy"}
SELL_TRADE_TYPES = {"sell_take_profit", "manual_sell"}
EPSILON = 1e-9
WEEKDAY_LABELS = {
    "monday": "Monday",
    "tuesday": "Tuesday",
    "wednesday": "Wednesday",
    "thursday": "Thursday",
    "friday": "Friday",
    "saturday": "Saturday",
    "sunday": "Sunday",
}


def utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()


def shanghai_now() -> datetime:
    return datetime.now(tz=SHANGHAI_TZ).replace(microsecond=0)


def normalize_weekday(value: Any) -> str | None:
    if value in (None, ""):
        return None
    return str(value).strip().lower()


def parse_scalar(value: str) -> Any:
    text = value.strip()
    if not text:
        return ""
    if text in {"true", "false"}:
        return text == "true"
    if text in {"null", "None"}:
        return None
    if text.startswith(("[", "{", "'", '"')):
        return ast.literal_eval(text)
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+\.\d+", text):
        return float(text)
    return text


def parse_strategy_parameter_block(block: str) -> dict[str, Any]:
    parsed_lines: list[tuple[int, str]] = []
    for raw_line in block.splitlines():
        if not raw_line.strip():
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        parsed_lines.append((indent, raw_line.strip()))

    def parse_block(index: int, indent_level: int) -> tuple[Any, int]:
        if index >= len(parsed_lines):
            return {}, index

        current_indent, current_text = parsed_lines[index]
        if current_indent != indent_level:
            return {}, index

        if current_text.startswith("- "):
            items: list[Any] = []
            while index < len(parsed_lines):
                line_indent, line_text = parsed_lines[index]
                if line_indent != indent_level or not line_text.startswith("- "):
                    break
                item_text = line_text[2:].strip()
                index += 1
                if item_text:
                    items.append(parse_scalar(item_text))
                else:
                    child, index = parse_nested_block(index, indent_level)
                    items.append(child)
            return items, index

        mapping: dict[str, Any] = {}
        while index < len(parsed_lines):
            line_indent, line_text = parsed_lines[index]
            if line_indent != indent_level or line_text.startswith("- "):
                break
            key, value = line_text.split(":", 1)
            key = key.strip()
            value = value.strip()
            index += 1
            if value:
                mapping[key] = parse_scalar(value)
            else:
                child, index = parse_nested_block(index, indent_level)
                mapping[key] = child
        return mapping, index

    def parse_nested_block(index: int, parent_indent: int) -> tuple[Any, int]:
        if index >= len(parsed_lines):
            return {}, index
        next_indent = parsed_lines[index][0]
        if next_indent <= parent_indent:
            return {}, index
        return parse_block(index, next_indent)

    root, _ = parse_block(0, parsed_lines[0][0] if parsed_lines else 0)
    return root.get("strategy_parameters", root) if isinstance(root, dict) else {}


def deep_merge_mapping(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge_mapping(merged[key], value)
        else:
            merged[key] = value
    return merged


def normalize_strategy_parameters(params: dict[str, Any]) -> dict[str, Any]:
    fixed = params.get("fixed")
    editable = params.get("editable")
    if not isinstance(fixed, dict) and not isinstance(editable, dict):
        return params

    normalized: dict[str, Any] = {}
    if isinstance(fixed, dict):
        normalized = deep_merge_mapping(normalized, fixed)

    direct_sections = {key: value for key, value in params.items() if key not in {"fixed", "editable"}}
    if direct_sections:
        normalized = deep_merge_mapping(normalized, direct_sections)

    if isinstance(editable, dict):
        normalized = deep_merge_mapping(normalized, editable)

    return normalized


def load_strategy_parameters(skill_md_path: Path = SKILL_MD_PATH) -> dict[str, Any]:
    skill_md = skill_md_path.read_text(encoding="utf-8")
    marker = "## Strategy Parameters"
    start_index = skill_md.find(marker)
    if start_index < 0:
        raise ValueError(f"Could not find the strategy parameter section in {skill_md_path}")

    code_start = skill_md.find("```yaml", start_index)
    if code_start < 0:
        raise ValueError(f"Could not find the strategy parameter code block in {skill_md_path}")
    code_start = skill_md.find("\n", code_start)
    if code_start < 0:
        raise ValueError(f"Could not parse the strategy parameter code block in {skill_md_path}")
    code_start += 1

    code_end = skill_md.find("```", code_start)
    if code_end < 0:
        raise ValueError(f"Could not find the end of the strategy parameter code block in {skill_md_path}")
    return normalize_strategy_parameters(parse_strategy_parameter_block(skill_md[code_start:code_end]))


def connect_db(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    importer.init_db(connection)
    return connection


def row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def ensure_market_snapshot(connection: sqlite3.Connection, fund_code: str, refresh: bool = False) -> int:
    latest = connection.execute(
        """
        SELECT id
        FROM fund_snapshots
        WHERE fund_code = ?
        ORDER BY COALESCE(source_generated_at, fetched_at) DESC, id DESC
        LIMIT 1
        """,
        (fund_code,),
    ).fetchone()
    if latest is not None and not refresh:
        return int(latest["id"])

    raw_js = importer.fetch_pingzhongdata(fund_code)
    payload = importer.parse_var_assignments(raw_js)
    summary = importer.ingest_fund(connection, fund_code, raw_js, payload)
    connection.commit()
    return int(summary["snapshot_id"])


def get_fund_row(connection: sqlite3.Connection, fund_code: str) -> dict[str, Any] | None:
    row = connection.execute(
        """
        SELECT fund_code, fund_name, source_rate, current_rate, min_subscription, updated_at
        FROM funds
        WHERE fund_code = ?
        """,
        (fund_code,),
    ).fetchone()
    return row_to_dict(row)


def get_latest_series_point(
    connection: sqlite3.Connection,
    snapshot_id: int,
    series_type: str,
) -> dict[str, Any] | None:
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


def get_recent_high(
    connection: sqlite3.Connection,
    snapshot_id: int,
    lookback_days: int,
) -> dict[str, Any] | None:
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


def get_market_state(
    connection: sqlite3.Connection,
    fund_code: str,
    lookback_days: int,
    refresh: bool = False,
) -> dict[str, Any]:
    snapshot_id = ensure_market_snapshot(connection, fund_code, refresh=refresh)
    fund = get_fund_row(connection, fund_code)
    if fund is None:
        raise RuntimeError(f"Missing fund row for {fund_code}")
    latest_net_worth = get_latest_series_point(connection, snapshot_id, "net_worth_trend")
    recent_high = get_recent_high(connection, snapshot_id, lookback_days)
    latest_position_estimate = get_latest_series_point(connection, snapshot_id, "fund_shares_position")
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
    return {
        "snapshot_id": snapshot_id,
        "snapshot": snapshot,
        "fund": fund,
        "current_price": latest_net_worth["value"] if latest_net_worth else None,
        "current_price_date": latest_net_worth["point_date"] if latest_net_worth else None,
        "recent_high": recent_high["value"] if recent_high else None,
        "recent_high_date": recent_high["point_date"] if recent_high else None,
        "stock_position_estimate_pct": latest_position_estimate["value"] if latest_position_estimate else None,
        "stock_position_estimate_date": latest_position_estimate["point_date"] if latest_position_estimate else None,
        "fee_rate_pct": fund["current_rate"],
        "min_subscription": fund["min_subscription"],
        "fund_name": fund["fund_name"],
    }


def get_account(
    connection: sqlite3.Connection,
    account_id: str,
    fund_code: str,
) -> dict[str, Any] | None:
    row = connection.execute(
        """
        SELECT account_id, fund_code, fund_type, cash_pool, position_units, avg_cost_price, note, created_at, updated_at
        FROM strategy_accounts
        WHERE account_id = ? AND fund_code = ?
        """,
        (account_id, fund_code),
    ).fetchone()
    return row_to_dict(row)


def upsert_account(
    connection: sqlite3.Connection,
    account_id: str,
    fund_code: str,
    *,
    fund_type: str,
    cash_pool: float,
    position_units: float,
    avg_cost_price: float | None,
    note: str | None = None,
) -> dict[str, Any]:
    now = utc_now_iso()
    if position_units < -EPSILON:
        raise ValueError("position_units cannot be negative")
    if cash_pool < -EPSILON:
        raise ValueError("cash_pool cannot be negative")
    if position_units <= EPSILON:
        position_units = 0.0
        avg_cost_price = None
    elif avg_cost_price is None or avg_cost_price <= EPSILON:
        raise ValueError("avg_cost_price is required when position_units is positive")

    existing = get_account(connection, account_id, fund_code)
    created_at = existing["created_at"] if existing else now

    connection.execute(
        """
        INSERT INTO strategy_accounts (
            account_id,
            fund_code,
            fund_type,
            cash_pool,
            position_units,
            avg_cost_price,
            note,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(account_id, fund_code) DO UPDATE SET
            fund_type = excluded.fund_type,
            cash_pool = excluded.cash_pool,
            position_units = excluded.position_units,
            avg_cost_price = excluded.avg_cost_price,
            note = excluded.note,
            updated_at = excluded.updated_at
        """,
        (
            account_id,
            fund_code,
            fund_type,
            float(cash_pool),
            float(position_units),
            float(avg_cost_price) if avg_cost_price is not None else None,
            note,
            created_at,
            now,
        ),
    )
    return get_account(connection, account_id, fund_code) or {}


def get_last_add_trade_date(
    connection: sqlite3.Connection,
    account_id: str,
    fund_code: str,
) -> str | None:
    row = connection.execute(
        """
        SELECT trade_date
        FROM strategy_trades
        WHERE account_id = ? AND fund_code = ? AND trade_type IN ('buy_dca', 'buy_dip', 'manual_buy')
        ORDER BY trade_date DESC, id DESC
        LIMIT 1
        """,
        (account_id, fund_code),
    ).fetchone()
    return str(row["trade_date"]) if row else None


def get_trade_count_for_day(
    connection: sqlite3.Connection,
    account_id: str,
    fund_code: str,
    trade_date: str,
) -> int:
    row = connection.execute(
        """
        SELECT COUNT(*)
        FROM strategy_trades
        WHERE account_id = ? AND fund_code = ? AND trade_date = ?
          AND trade_type IN ('buy_dca', 'buy_dip', 'sell_take_profit', 'manual_buy', 'manual_sell')
        """,
        (account_id, fund_code, trade_date),
    ).fetchone()
    return int(row[0]) if row else 0


def is_business_day(target_date: date) -> bool:
    return target_date.weekday() < 5


def previous_business_days_in_month(target_date: date) -> list[date]:
    cursor = date(target_date.year, target_date.month, 1)
    days: list[date] = []
    while cursor.month == target_date.month:
        if is_business_day(cursor):
            days.append(cursor)
        cursor += timedelta(days=1)
    return days


def second_to_last_business_day(target_date: date) -> date:
    business_days = previous_business_days_in_month(target_date)
    if len(business_days) < 2:
        return business_days[-1]
    return business_days[-2]


def last_business_day(target_date: date) -> date:
    business_days = previous_business_days_in_month(target_date)
    return business_days[-1]


def last_calendar_day(target_date: date) -> date:
    if target_date.month == 12:
        next_month = date(target_date.year + 1, 1, 1)
    else:
        next_month = date(target_date.year, target_date.month + 1, 1)
    return next_month - timedelta(days=1)


def resolve_monthly_schedule_date(
    target_date: date,
    *,
    schedule_type: str | None,
    day_of_month: int | None = None,
) -> date:
    normalized_type = str(schedule_type or "second_to_last_business_day").strip().lower()
    if normalized_type == "second_to_last_business_day":
        return second_to_last_business_day(target_date)
    if normalized_type == "last_business_day":
        return last_business_day(target_date)
    if normalized_type == "day_of_month":
        if day_of_month is None:
            raise ValueError("day_of_month is required when schedule_type=day_of_month")
        month_end = last_calendar_day(target_date)
        resolved_day = min(max(int(day_of_month), 1), month_end.day)
        return date(target_date.year, target_date.month, resolved_day)
    raise ValueError(f"Unsupported monthly schedule_type: {schedule_type}")


def next_business_day(target_date: date) -> date:
    cursor = target_date + timedelta(days=1)
    while not is_business_day(cursor):
        cursor += timedelta(days=1)
    return cursor


def count_business_days_between(start_date: date, end_date: date) -> int:
    if end_date <= start_date:
        return 0
    count = 0
    cursor = start_date + timedelta(days=1)
    while cursor <= end_date:
        if is_business_day(cursor):
            count += 1
        cursor += timedelta(days=1)
    return count


def get_weekly_schedule_config(
    scheduling: dict[str, Any],
    key: str,
    *,
    legacy_weekday_key: str,
    legacy_time_key: str | None = None,
) -> dict[str, Any]:
    nested = scheduling.get(key)
    weekday = None
    time_local = None
    if isinstance(nested, dict):
        weekday = nested.get("weekday")
        time_local = nested.get("time_local")
    if weekday is None:
        weekday = scheduling.get(legacy_weekday_key)
    if time_local is None and legacy_time_key:
        time_local = scheduling.get(legacy_time_key)
    return {
        "weekday": normalize_weekday(weekday),
        "time_local": str(time_local) if time_local not in (None, "") else None,
    }


def get_monthly_schedule_config(
    scheduling: dict[str, Any],
    key: str,
    *,
    legacy_rule_key: str,
    legacy_day_of_month_key: str | None = None,
    legacy_time_key: str | None = None,
) -> dict[str, Any]:
    nested = scheduling.get(key)
    schedule_type = None
    day_of_month = None
    time_local = None
    if isinstance(nested, dict):
        schedule_type = nested.get("schedule_type")
        day_of_month = nested.get("day_of_month")
        time_local = nested.get("time_local")
    if schedule_type is None:
        schedule_type = scheduling.get(legacy_rule_key)
    if day_of_month is None and legacy_day_of_month_key:
        day_of_month = scheduling.get(legacy_day_of_month_key)
    if time_local is None and legacy_time_key:
        time_local = scheduling.get(legacy_time_key)
    return {
        "schedule_type": str(schedule_type or "second_to_last_business_day").strip().lower(),
        "day_of_month": int(day_of_month) if day_of_month is not None else None,
        "time_local": str(time_local) if time_local not in (None, "") else None,
    }


def compute_max_buy_gross_amount(
    *,
    cash_pool: float,
    position_value: float,
    total_asset: float,
    max_position_ratio_pct: float,
    fee_rate_pct: float,
) -> float:
    fee_fraction = max(fee_rate_pct, 0.0) / 100
    max_ratio = max_position_ratio_pct / 100
    if total_asset <= EPSILON:
        return max(cash_pool / (1 + fee_fraction), 0.0)

    room = max_ratio * total_asset - position_value
    if room <= EPSILON:
        return 0.0

    limit_by_ratio = room / (1 + max_ratio * fee_fraction)
    limit_by_cash = cash_pool / (1 + fee_fraction)
    return max(min(limit_by_ratio, limit_by_cash), 0.0)


def compute_max_sell_units(
    *,
    cash_pool: float,
    position_units: float,
    current_price: float,
    min_position_ratio_pct: float,
    fee_rate_pct: float,
) -> float:
    if position_units <= EPSILON or current_price <= EPSILON:
        return 0.0

    fee_fraction = max(fee_rate_pct, 0.0) / 100
    min_ratio = min_position_ratio_pct / 100
    position_value = position_units * current_price
    numerator = position_value * (1 - min_ratio) - min_ratio * cash_pool
    denominator = current_price * (1 - min_ratio * fee_fraction)
    if numerator <= EPSILON or denominator <= EPSILON:
        return 0.0
    return max(min(numerator / denominator, position_units), 0.0)


def apply_trade_to_account(
    account: dict[str, Any],
    *,
    trade_type: str,
    gross_amount: float,
    price: float | None,
    units: float,
    fee_rate_pct: float,
) -> tuple[dict[str, Any], dict[str, Any]]:
    fee_amount = gross_amount * max(fee_rate_pct, 0.0) / 100
    cash_pool = float(account["cash_pool"])
    position_units = float(account["position_units"])
    avg_cost_price = account["avg_cost_price"]

    if trade_type in BUY_TRADE_TYPES:
        cash_delta = -(gross_amount + fee_amount)
        units_delta = units
        new_cash = cash_pool + cash_delta
        new_units = position_units + units_delta
        if new_cash < -EPSILON:
            raise ValueError("Insufficient cash_pool for the requested buy")
        prior_cost_basis = position_units * float(avg_cost_price or 0.0)
        new_cost_basis = prior_cost_basis + gross_amount + fee_amount
        new_avg_cost_price = new_cost_basis / new_units if new_units > EPSILON else None
    elif trade_type in SELL_TRADE_TYPES:
        cash_delta = gross_amount - fee_amount
        units_delta = -units
        new_cash = cash_pool + cash_delta
        new_units = position_units + units_delta
        if new_units < -EPSILON:
            raise ValueError("Insufficient position_units for the requested sell")
        new_avg_cost_price = float(avg_cost_price) if new_units > EPSILON and avg_cost_price is not None else None
    elif trade_type == "cash_inflow":
        cash_delta = gross_amount
        units_delta = 0.0
        new_cash = cash_pool + cash_delta
        new_units = position_units
        new_avg_cost_price = float(avg_cost_price) if avg_cost_price is not None else None
    elif trade_type == "cash_outflow":
        cash_delta = -gross_amount
        units_delta = 0.0
        new_cash = cash_pool + cash_delta
        new_units = position_units
        if new_cash < -EPSILON:
            raise ValueError("Insufficient cash_pool for the requested cash outflow")
        new_avg_cost_price = float(avg_cost_price) if avg_cost_price is not None else None
    else:
        raise ValueError(f"Unsupported trade_type: {trade_type}")

    new_account = {
        **account,
        "cash_pool": max(new_cash, 0.0),
        "position_units": max(new_units, 0.0),
        "avg_cost_price": new_avg_cost_price if new_units > EPSILON else None,
    }
    trade_effect = {
        "fee_amount": fee_amount,
        "cash_delta": cash_delta,
        "units_delta": units_delta,
    }
    return new_account, trade_effect


def record_trade(
    connection: sqlite3.Connection,
    *,
    account_id: str,
    fund_code: str,
    trade_date: str,
    trade_time_local: str | None,
    trade_type: str,
    gross_amount: float,
    price: float | None,
    units: float,
    fee_rate_pct: float,
    note: str | None = None,
) -> dict[str, Any]:
    account = get_account(connection, account_id, fund_code)
    if account is None:
        raise ValueError(f"Account {account_id}/{fund_code} does not exist")

    updated_account, trade_effect = apply_trade_to_account(
        account,
        trade_type=trade_type,
        gross_amount=float(gross_amount),
        price=price,
        units=float(units),
        fee_rate_pct=float(fee_rate_pct or 0.0),
    )
    direction = (
        "buy"
        if trade_type in BUY_TRADE_TYPES
        else "sell"
        if trade_type in SELL_TRADE_TYPES
        else "cash_in"
        if trade_type == "cash_inflow"
        else "cash_out"
    )

    connection.execute(
        """
        INSERT INTO strategy_trades (
            account_id,
            fund_code,
            trade_date,
            trade_time_local,
            trade_type,
            direction,
            gross_amount,
            price,
            units,
            fee_rate_pct,
            fee_amount,
            cash_delta,
            units_delta,
            note,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            account_id,
            fund_code,
            trade_date,
            trade_time_local,
            trade_type,
            direction,
            float(gross_amount),
            float(price) if price is not None else None,
            float(units),
            float(fee_rate_pct or 0.0),
            float(trade_effect["fee_amount"]),
            float(trade_effect["cash_delta"]),
            float(trade_effect["units_delta"]),
            note,
            utc_now_iso(),
        ),
    )
    upsert_account(
        connection,
        account_id,
        fund_code,
        fund_type=str(updated_account["fund_type"]),
        cash_pool=float(updated_account["cash_pool"]),
        position_units=float(updated_account["position_units"]),
        avg_cost_price=(
            float(updated_account["avg_cost_price"])
            if updated_account["avg_cost_price"] is not None
            else None
        ),
        note=updated_account.get("note"),
    )
    return {
        "account": get_account(connection, account_id, fund_code),
        "trade_effect": trade_effect,
    }


def _legacy_build_reminder_messages_unused(
    params: dict[str, Any],
    fund_code: str,
    fund_name: str | None,
) -> dict[str, str]:
    capital = params["capital"]
    target_name = fund_name or fund_code
    monthly_amount = capital["monthly_cash_pool_inflow"]
    return {
        "weekly_pretrade_reminder": (
            f"明天是周二策略检查日，请提前检查 {target_name}({fund_code}) 的现金池、持仓、回撤和可交易资金。"
        ),
        "weekly_trade_reminder": (
            f"今天是周二策略交易日，请检查 {target_name}({fund_code}) 是否应执行 buy_dca / buy_dip / sell_take_profit / hold。"
        ),
        "monthly_cash_inflow_reminder": (
            f"今天是本月倒数第二个工作日，请为 {target_name}({fund_code}) 向 cash_pool 补充 {monthly_amount}。"
        ),
    }


def _legacy_generate_reminders_unused(
    connection: sqlite3.Connection,
    *,
    account_id: str,
    fund_code: str,
    fund_name: str | None,
    as_of_date: date,
    params: dict[str, Any],
) -> list[dict[str, Any]]:
    scheduling = params["scheduling"]
    weekday_name = as_of_date.strftime("%A").lower()
    reminder_types: list[str] = []

    if weekday_name == scheduling["weekly_pretrade_reminder_weekday"]:
        reminder_types.append("weekly_pretrade_reminder")
    if weekday_name == scheduling["weekly_trade_reminder_weekday"]:
        reminder_types.append("weekly_trade_reminder")
    if as_of_date == second_to_last_business_day(as_of_date):
        reminder_types.append("monthly_cash_inflow_reminder")

    messages = build_reminder_messages(params, fund_code, fund_name)
    now = utc_now_iso()
    for reminder_type in reminder_types:
        connection.execute(
            """
            INSERT OR IGNORE INTO strategy_reminders (
                account_id,
                fund_code,
                reminder_date,
                reminder_type,
                message,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, 'generated', ?)
            """,
            (account_id, fund_code, as_of_date.isoformat(), reminder_type, messages[reminder_type], now),
        )

    rows = connection.execute(
        """
        SELECT reminder_date, reminder_type, message, status
        FROM strategy_reminders
        WHERE account_id = ? AND fund_code = ? AND reminder_date = ?
        ORDER BY reminder_type
        """,
        (account_id, fund_code, as_of_date.isoformat()),
    ).fetchall()
    return [dict(row) for row in rows]


def parse_local_time(value: str) -> time:
    hour_text, minute_text = value.split(":", 1)
    return time(hour=int(hour_text), minute=int(minute_text))


def is_schedule_time_reached(
    current_time_local: str | None,
    scheduled_time_local: str | None,
) -> bool:
    if not scheduled_time_local or not current_time_local:
        return True
    return parse_local_time(current_time_local) >= parse_local_time(scheduled_time_local)


def build_reminder_messages(
    params: dict[str, Any],
    fund_code: str,
    fund_name: str | None,
) -> dict[str, str]:
    capital = params["capital"]
    scheduling = params["scheduling"]
    target_name = fund_name or fund_code
    monthly_amount = capital["monthly_cash_pool_inflow"]
    weekly_pretrade = get_weekly_schedule_config(
        scheduling,
        "weekly_pretrade_reminder",
        legacy_weekday_key="weekly_pretrade_reminder_weekday",
        legacy_time_key="weekly_pretrade_reminder_time_local",
    )
    weekly_trade = get_weekly_schedule_config(
        scheduling,
        "weekly_trade_reminder",
        legacy_weekday_key="weekly_trade_reminder_weekday",
        legacy_time_key="weekly_trade_reminder_time_local",
    )
    weekly_dca = get_weekly_schedule_config(
        scheduling,
        "weekly_dca",
        legacy_weekday_key="weekly_dca_weekday",
    )
    monthly_reminder = get_monthly_schedule_config(
        scheduling,
        "monthly_cash_inflow_reminder",
        legacy_rule_key="monthly_cash_inflow_reminder_rule",
        legacy_day_of_month_key="monthly_cash_inflow_reminder_day_of_month",
        legacy_time_key="monthly_cash_inflow_reminder_time_local",
    )
    pretrade_time = f" at {weekly_pretrade['time_local']}" if weekly_pretrade["time_local"] else ""
    trade_time = f" at {weekly_trade['time_local']}" if weekly_trade["time_local"] else ""
    monthly_time = f" at {monthly_reminder['time_local']}" if monthly_reminder["time_local"] else ""
    trade_day = WEEKDAY_LABELS.get(
        str(weekly_trade["weekday"] or weekly_dca["weekday"] or "").lower(),
        str(weekly_trade["weekday"] or weekly_dca["weekday"] or "configured_trade_day"),
    )
    monthly_rule = (
        f"day_of_month={monthly_reminder['day_of_month']}"
        if monthly_reminder["schedule_type"] == "day_of_month"
        else monthly_reminder["schedule_type"]
    )
    return {
        "weekly_pretrade_reminder": (
            f"Pretrade reminder{pretrade_time}: review {target_name}({fund_code}) before the configured "
            f"{trade_day} trade day."
        ),
        "weekly_trade_reminder": (
            f"Trade reminder{trade_time}: review {target_name}({fund_code}) and decide "
            f"buy_dca / buy_dip / sell_take_profit / hold."
        ),
        "monthly_cash_inflow_reminder": (
            f"Monthly cash reminder{monthly_time}: add {monthly_amount} to cash_pool for "
            f"{target_name}({fund_code}) on schedule {monthly_rule}."
        ),
    }


def generate_reminders(
    connection: sqlite3.Connection,
    *,
    account_id: str,
    fund_code: str,
    fund_name: str | None,
    as_of_date: date,
    as_of_time_local: str | None = None,
    params: dict[str, Any],
) -> list[dict[str, Any]]:
    scheduling = params["scheduling"]
    weekday_name = as_of_date.strftime("%A").lower()
    reminder_types: list[str] = []

    weekly_pretrade = get_weekly_schedule_config(
        scheduling,
        "weekly_pretrade_reminder",
        legacy_weekday_key="weekly_pretrade_reminder_weekday",
        legacy_time_key="weekly_pretrade_reminder_time_local",
    )
    weekly_trade = get_weekly_schedule_config(
        scheduling,
        "weekly_trade_reminder",
        legacy_weekday_key="weekly_trade_reminder_weekday",
        legacy_time_key="weekly_trade_reminder_time_local",
    )
    monthly_reminder = get_monthly_schedule_config(
        scheduling,
        "monthly_cash_inflow_reminder",
        legacy_rule_key="monthly_cash_inflow_reminder_rule",
        legacy_day_of_month_key="monthly_cash_inflow_reminder_day_of_month",
        legacy_time_key="monthly_cash_inflow_reminder_time_local",
    )
    monthly_reminder_date = resolve_monthly_schedule_date(
        as_of_date,
        schedule_type=monthly_reminder["schedule_type"],
        day_of_month=monthly_reminder["day_of_month"],
    )

    if (
        weekly_pretrade["weekday"]
        and weekday_name == weekly_pretrade["weekday"]
        and is_schedule_time_reached(as_of_time_local, weekly_pretrade["time_local"])
    ):
        reminder_types.append("weekly_pretrade_reminder")
    if (
        weekly_trade["weekday"]
        and weekday_name == weekly_trade["weekday"]
        and is_schedule_time_reached(as_of_time_local, weekly_trade["time_local"])
    ):
        reminder_types.append("weekly_trade_reminder")
    if (
        as_of_date == monthly_reminder_date
        and is_schedule_time_reached(as_of_time_local, monthly_reminder["time_local"])
    ):
        reminder_types.append("monthly_cash_inflow_reminder")

    messages = build_reminder_messages(params, fund_code, fund_name)
    now = utc_now_iso()
    for reminder_type in reminder_types:
        connection.execute(
            """
            INSERT OR IGNORE INTO strategy_reminders (
                account_id,
                fund_code,
                reminder_date,
                reminder_type,
                message,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, 'generated', ?)
            """,
            (account_id, fund_code, as_of_date.isoformat(), reminder_type, messages[reminder_type], now),
        )

    rows = connection.execute(
        """
        SELECT reminder_date, reminder_type, message, status
        FROM strategy_reminders
        WHERE account_id = ? AND fund_code = ? AND reminder_date = ?
        ORDER BY reminder_type
        """,
        (account_id, fund_code, as_of_date.isoformat()),
    ).fetchall()
    return [dict(row) for row in rows]


def build_account_market_snapshot(
    account: dict[str, Any],
    market_state: dict[str, Any],
) -> dict[str, Any]:
    current_price = market_state.get("current_price")
    position_units = float(account["position_units"])
    cash_pool = float(account["cash_pool"])
    position_value = position_units * float(current_price or 0.0)
    total_asset = cash_pool + position_value
    position_ratio_pct = (position_value / total_asset * 100) if total_asset > EPSILON else 0.0
    recent_high = market_state.get("recent_high")
    drawdown_pct = None
    if current_price not in (None, 0) and recent_high not in (None, 0):
        drawdown_pct = (float(recent_high) - float(current_price)) / float(recent_high) * 100
    avg_cost_price = account.get("avg_cost_price")
    profit_pct = None
    if position_units > EPSILON and avg_cost_price not in (None, 0):
        profit_pct = (float(current_price) - float(avg_cost_price)) / float(avg_cost_price) * 100
    return {
        "cash_pool": cash_pool,
        "position_units": position_units,
        "avg_cost_price": avg_cost_price,
        "current_price": current_price,
        "position_value": position_value,
        "total_asset": total_asset,
        "position_ratio_pct": position_ratio_pct,
        "recent_high": recent_high,
        "drawdown_pct": drawdown_pct,
        "profit_pct": profit_pct,
        "effective_fee_rate_pct": float(market_state.get("fee_rate_pct") or 0.0),
    }


def evaluate_strategy_state(
    *,
    params: dict[str, Any],
    account: dict[str, Any],
    market_state: dict[str, Any],
    as_of_date: date,
    trade_time_local: str,
    last_add_trade_date: str | None,
    trades_today: int,
    reminders: list[dict[str, Any]],
) -> dict[str, Any]:
    account_state = build_account_market_snapshot(account, market_state)
    cash_pool = account_state["cash_pool"]
    position_units = account_state["position_units"]
    current_price = account_state["current_price"]
    recent_high = account_state["recent_high"]
    avg_cost_price = account_state["avg_cost_price"]
    effective_fee_rate_pct = account_state["effective_fee_rate_pct"]
    blockers: list[str] = []

    required_values = {
        "current_price": current_price,
        "recent_high": recent_high,
        "cash_pool": cash_pool,
        "position_units": position_units,
    }
    missing_fields = [name for name, value in required_values.items() if value is None]
    if position_units > EPSILON and avg_cost_price in (None, 0):
        missing_fields.append("avg_cost_price")
    if missing_fields:
        return {
            **account_state,
            "action": "skip_data_missing",
            "reason": f"missing_fields={','.join(sorted(set(missing_fields)))}",
            "candidate_trade": None,
            "reminders": reminders,
            "last_add_trade_date": last_add_trade_date,
            "business_days_since_last_add": None,
            "execution_date": as_of_date.isoformat(),
            "trades_today": trades_today,
            "blockers": blockers,
        }

    fund_type = str(account.get("fund_type") or "")
    universe = params["universe"]
    allowed_types = set(universe["allowed_fund_types"])
    disallowed_types = set(universe["disallowed_fund_types"])
    if not fund_type:
        return {
            **account_state,
            "action": "skip_data_missing",
            "reason": "missing_fund_type",
            "candidate_trade": None,
            "reminders": reminders,
            "last_add_trade_date": last_add_trade_date,
            "business_days_since_last_add": None,
            "execution_date": as_of_date.isoformat(),
            "trades_today": trades_today,
            "blockers": blockers,
        }
    if fund_type in disallowed_types or (allowed_types and fund_type not in allowed_types):
        return {
            **account_state,
            "action": "hold",
            "reason": f"fund_type_not_supported={fund_type}",
            "candidate_trade": None,
            "reminders": reminders,
            "last_add_trade_date": last_add_trade_date,
            "business_days_since_last_add": None,
            "execution_date": as_of_date.isoformat(),
            "trades_today": trades_today,
            "blockers": blockers,
        }

    scheduling = params["scheduling"]
    price_state = params["price_state"]
    take_profit = params["take_profit"]
    risk = params["risk"]
    weekday_name = as_of_date.strftime("%A").lower()
    weekly_dca = get_weekly_schedule_config(
        scheduling,
        "weekly_dca",
        legacy_weekday_key="weekly_dca_weekday",
    )
    monthly_cash_inflow = get_monthly_schedule_config(
        scheduling,
        "monthly_cash_inflow",
        legacy_rule_key="monthly_cash_inflow_rule",
        legacy_day_of_month_key="monthly_cash_inflow_day_of_month",
    )
    is_weekly_dca_day = weekday_name == str(weekly_dca["weekday"] or "").lower()
    is_monthly_cash_inflow_day = as_of_date == resolve_monthly_schedule_date(
        as_of_date,
        schedule_type=monthly_cash_inflow["schedule_type"],
        day_of_month=monthly_cash_inflow["day_of_month"],
    )

    spacing_days = None
    if last_add_trade_date:
        spacing_days = count_business_days_between(date.fromisoformat(last_add_trade_date), as_of_date)

    trade_cutoff = parse_local_time(scheduling["trade_cutoff_local_time"])
    local_trade_time = parse_local_time(trade_time_local)
    execution_date = (
        as_of_date.isoformat()
        if is_business_day(as_of_date) and local_trade_time <= trade_cutoff
        else next_business_day(as_of_date).isoformat()
    )

    if trades_today >= int(scheduling["max_trades_per_day"]):
        blockers.append("max_trades_per_day_reached")

    decision = {
        **account_state,
        "action": "hold",
        "reason": "no_rule_triggered",
        "candidate_trade": None,
        "reminders": reminders,
        "last_add_trade_date": last_add_trade_date,
        "business_days_since_last_add": spacing_days,
        "execution_date": execution_date,
        "trades_today": trades_today,
        "blockers": blockers,
        "is_weekly_dca_day": is_weekly_dca_day,
        "is_monthly_cash_inflow_day": is_monthly_cash_inflow_day,
    }

    if blockers:
        decision["reason"] = blockers[0]
        return decision

    total_asset = account_state["total_asset"]
    position_value = account_state["position_value"]

    profit_pct = account_state["profit_pct"]
    if profit_pct is not None and position_units > EPSILON:
        matched_sell_index = None
        for index, threshold in enumerate(take_profit["profit_thresholds_pct"]):
            if profit_pct >= threshold:
                matched_sell_index = index
        if matched_sell_index is not None:
            sell_ratio_pct = float(take_profit["profit_sell_ratios_pct"][matched_sell_index])
            desired_units = position_units * sell_ratio_pct / 100
            max_sell_units = compute_max_sell_units(
                cash_pool=cash_pool,
                position_units=position_units,
                current_price=float(current_price),
                min_position_ratio_pct=float(risk["min_position_ratio_pct"]),
                fee_rate_pct=effective_fee_rate_pct,
            )
            sell_units = min(desired_units, max_sell_units)
            if sell_units > EPSILON:
                gross_amount = sell_units * float(current_price)
                fee_amount = gross_amount * effective_fee_rate_pct / 100
                decision.update(
                    {
                        "action": "sell_take_profit",
                        "reason": f"profit_pct>={take_profit['profit_thresholds_pct'][matched_sell_index]}",
                        "candidate_trade": {
                            "gross_amount": gross_amount,
                            "units": sell_units,
                            "price": float(current_price),
                            "fee_rate_pct": effective_fee_rate_pct,
                            "fee_amount": fee_amount,
                            "cash_delta": gross_amount - fee_amount,
                            "units_delta": -sell_units,
                            "matched_threshold_pct": float(take_profit["profit_thresholds_pct"][matched_sell_index]),
                            "target_sell_ratio_pct": sell_ratio_pct,
                        },
                    }
                )
                return decision
            blockers.append("sell_blocked_by_min_position_ratio")

    drawdown_pct = account_state["drawdown_pct"] or 0.0
    matched_dip_index = None
    for index, threshold in enumerate(price_state["dip_thresholds_pct"]):
        if drawdown_pct >= threshold:
            matched_dip_index = index
    if matched_dip_index is not None:
        min_spacing = int(price_state["min_trading_days_between_adds"])
        spacing_ok = spacing_days is None or spacing_days >= min_spacing
        if not spacing_ok:
            blockers.append("dip_buy_blocked_by_min_spacing")
        else:
            target_gross_amount = float(price_state["dip_base_buy_amounts"][matched_dip_index])
            max_buy_gross = compute_max_buy_gross_amount(
                cash_pool=cash_pool,
                position_value=position_value,
                total_asset=total_asset,
                max_position_ratio_pct=float(risk["max_position_ratio_pct"]),
                fee_rate_pct=effective_fee_rate_pct,
            )
            actual_gross_amount = min(target_gross_amount, max_buy_gross)
            if actual_gross_amount > EPSILON:
                units = actual_gross_amount / float(current_price)
                fee_amount = actual_gross_amount * effective_fee_rate_pct / 100
                decision.update(
                    {
                        "action": "buy_dip",
                        "reason": f"drawdown_pct>={price_state['dip_thresholds_pct'][matched_dip_index]}",
                        "candidate_trade": {
                            "gross_amount": actual_gross_amount,
                            "units": units,
                            "price": float(current_price),
                            "fee_rate_pct": effective_fee_rate_pct,
                            "fee_amount": fee_amount,
                            "cash_delta": -(actual_gross_amount + fee_amount),
                            "units_delta": units,
                            "matched_threshold_pct": float(price_state["dip_thresholds_pct"][matched_dip_index]),
                        },
                    }
                )
                return decision
            blockers.append("dip_buy_blocked_by_cash_or_max_position")

    if is_weekly_dca_day:
        target_gross_amount = float(params["capital"]["weekly_dca_amount"])
        max_buy_gross = compute_max_buy_gross_amount(
            cash_pool=cash_pool,
            position_value=position_value,
            total_asset=total_asset,
            max_position_ratio_pct=float(risk["max_position_ratio_pct"]),
            fee_rate_pct=effective_fee_rate_pct,
        )
        actual_gross_amount = min(target_gross_amount, max_buy_gross)
        if actual_gross_amount > EPSILON:
            units = actual_gross_amount / float(current_price)
            fee_amount = actual_gross_amount * effective_fee_rate_pct / 100
            decision.update(
                {
                    "action": "buy_dca",
                    "reason": "weekly_dca_day",
                    "candidate_trade": {
                        "gross_amount": actual_gross_amount,
                        "units": units,
                        "price": float(current_price),
                        "fee_rate_pct": effective_fee_rate_pct,
                        "fee_amount": fee_amount,
                        "cash_delta": -(actual_gross_amount + fee_amount),
                        "units_delta": units,
                    },
                }
            )
            return decision
        blockers.append("dca_blocked_by_cash_or_max_position")

    decision["blockers"] = blockers
    decision["reason"] = blockers[0] if blockers else "no_rule_triggered"
    return decision


def evaluate_strategy(
    connection: sqlite3.Connection,
    *,
    account_id: str,
    fund_code: str,
    as_of_date: date,
    trade_time_local: str,
    refresh: bool = False,
) -> dict[str, Any]:
    params = load_strategy_parameters()
    lookback_days = int(params["price_state"]["recent_high_lookback_trading_days"])
    market_state = get_market_state(connection, fund_code, lookback_days, refresh=refresh)
    account = get_account(connection, account_id, fund_code)
    reminders = generate_reminders(
        connection,
        account_id=account_id,
        fund_code=fund_code,
        fund_name=market_state.get("fund_name"),
        as_of_date=as_of_date,
        as_of_time_local=trade_time_local,
        params=params,
    )

    if account is None:
        return {
            "action": "skip_data_missing",
            "reason": "missing_strategy_account",
            "candidate_trade": None,
            "reminders": reminders,
            "market_state": market_state,
            "account": None,
        }

    last_add_trade_date = get_last_add_trade_date(connection, account_id, fund_code)
    trades_today = get_trade_count_for_day(connection, account_id, fund_code, as_of_date.isoformat())
    decision = evaluate_strategy_state(
        params=params,
        account=account,
        market_state=market_state,
        as_of_date=as_of_date,
        trade_time_local=trade_time_local,
        last_add_trade_date=last_add_trade_date,
        trades_today=trades_today,
        reminders=reminders,
    )
    decision["market_state"] = market_state
    decision["account"] = account
    decision["params"] = params
    return decision


def apply_strategy_decision(
    connection: sqlite3.Connection,
    *,
    account_id: str,
    fund_code: str,
    decision: dict[str, Any],
    note: str | None = None,
) -> dict[str, Any] | None:
    if decision.get("action") not in {"buy_dca", "buy_dip", "sell_take_profit"}:
        return None
    candidate = decision.get("candidate_trade")
    if not candidate:
        return None
    return record_trade(
        connection,
        account_id=account_id,
        fund_code=fund_code,
        trade_date=decision["execution_date"],
        trade_time_local=None,
        trade_type=decision["action"],
        gross_amount=float(candidate["gross_amount"]),
        price=float(candidate["price"]),
        units=float(candidate["units"]),
        fee_rate_pct=float(candidate["fee_rate_pct"]),
        note=note or f"confirmed:{decision['reason']}",
    )


def format_account_summary(account: dict[str, Any] | None, decision: dict[str, Any]) -> str:
    if account is None:
        return "策略账户不存在。请先初始化账户状态。"
    market_state = decision.get("market_state") or {}
    reminders = decision.get("reminders") or []
    lines = [
        f"账户: {account['account_id']} / {account['fund_code']}",
        f"基金名称: {market_state.get('fund_name') or account['fund_code']}",
        f"基金类型: {account['fund_type']}",
        f"现金池: {decision.get('cash_pool', 0.0):.2f}",
        f"持仓份额: {decision.get('position_units', 0.0):.6f}",
        f"持仓成本: {decision.get('avg_cost_price') if decision.get('avg_cost_price') is not None else 'N/A'}",
        f"当前净值: {decision.get('current_price') if decision.get('current_price') is not None else 'N/A'}",
        f"持仓市值: {decision.get('position_value', 0.0):.2f}",
        f"总资产: {decision.get('total_asset', 0.0):.2f}",
        f"仓位: {decision.get('position_ratio_pct', 0.0):.2f}%",
        f"最近高点: {decision.get('recent_high') if decision.get('recent_high') is not None else 'N/A'}",
        f"回撤: {decision.get('drawdown_pct') if decision.get('drawdown_pct') is not None else 'N/A'}",
        f"浮动收益: {decision.get('profit_pct') if decision.get('profit_pct') is not None else 'N/A'}",
        f"当前动作: {decision.get('action')}",
        f"动作原因: {decision.get('reason')}",
        f"执行日期: {decision.get('execution_date')}",
    ]
    if reminders:
        lines.append("提醒:")
        for reminder in reminders:
            lines.append(f"- {reminder['reminder_type']}: {reminder['message']}")
    candidate = decision.get("candidate_trade")
    if candidate:
        lines.append("建议交易:")
        lines.append(f"- 金额: {candidate['gross_amount']:.2f}")
        lines.append(f"- 份额: {candidate['units']:.6f}")
        lines.append(f"- 价格: {candidate['price']:.4f}")
        lines.append(f"- 费率: {candidate['fee_rate_pct']:.4f}%")
    return "\n".join(lines)
