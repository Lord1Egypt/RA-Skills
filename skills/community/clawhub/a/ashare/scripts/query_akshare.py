#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import importlib
import io
import json
import math
import re
import sys
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import pandas as pd

DATE_RE = re.compile(r"^\d{8}$")
DEFAULT_HISTORY_LIMIT = 60
DEFAULT_NEWS_LIMIT = 10
INDEX_GROUPS = ("沪深重要指数", "上证系列指数", "深证系列指数", "指数成份", "中证系列指数")
MAIN_INDEX_CODES = ("000001", "399001", "399006", "000300", "000688", "899050")
FUND_INDICATOR_MAP = {"unit_nav": "单位净值走势", "acc_nav": "累计净值走势", "acc_return": "累计收益率走势"}
FUND_PERIOD_MAP = {"1m": "1月", "3m": "3月", "6m": "6月", "1y": "1年", "3y": "3年", "5y": "5年", "ytd": "今年来", "all": "成立来"}
MACRO_SERIES_MAP = {"china_cpi": "macro_china_cpi", "china_pmi": "macro_china_pmi", "china_rmb": "macro_china_rmb"}
NEWS_SCOPE_MAP = {"all": "全部", "important": "重点"}


@dataclass
class SkillError(Exception):
    error_type: str
    message: str
    details: dict[str, Any] | None = None

    def payload(self) -> dict[str, Any]:
        body = {"ok": False, "error": {"type": self.error_type, "message": self.message}}
        if self.details:
            body["error"]["details"] = self.details
        return body


@dataclass
class ResolvedSymbol:
    input: str
    code: str
    name: str
    category: str
    extra: dict[str, Any] | None = None

    def payload(self) -> dict[str, Any]:
        body = {"input": self.input, "code": self.code, "name": self.name, "category": self.category}
        if self.extra:
            body.update(self.extra)
        return body


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        emit_json(args.handler(args))
        return 0
    except SkillError as exc:
        emit_json(exc.payload())
        return 1
    except Exception as exc:  # pragma: no cover
        emit_json(SkillError("runtime_error", "AKShare query failed unexpectedly.", {"exception": repr(exc)}).payload())
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query a fixed whitelist of AKShare datasets.")
    sub = parser.add_subparsers(dest="command", required=True)

    market = sub.add_parser("market-overview")
    market.set_defaults(handler=handle_market_overview)

    for name, handler in (("stock-quote", handle_stock_quote), ("stock-profile", handle_stock_profile), ("index-quote", handle_index_quote), ("fund-quote", handle_fund_quote)):
        cmd = sub.add_parser(name)
        cmd.add_argument("symbol")
        cmd.set_defaults(handler=handler)

    stock_history = sub.add_parser("stock-history")
    stock_history.add_argument("symbol")
    add_history_args(stock_history, with_adjust=True)
    stock_history.set_defaults(handler=handle_stock_history)

    index_history = sub.add_parser("index-history")
    index_history.add_argument("symbol")
    add_history_args(index_history, with_adjust=False)
    index_history.set_defaults(handler=handle_index_history)

    fund_history = sub.add_parser("fund-history")
    fund_history.add_argument("symbol")
    fund_history.add_argument("--indicator", choices=tuple(FUND_INDICATOR_MAP), default="unit_nav")
    fund_history.add_argument("--period", choices=tuple(FUND_PERIOD_MAP), default="all")
    fund_history.add_argument("--limit", type=int)
    fund_history.set_defaults(handler=handle_fund_history)

    macro_series = sub.add_parser("macro-series")
    macro_series.add_argument("alias")
    macro_series.add_argument("--limit", type=int)
    macro_series.set_defaults(handler=handle_macro_series)

    macro_calendar = sub.add_parser("macro-calendar")
    macro_calendar.add_argument("--date")
    macro_calendar.add_argument("--limit", type=int)
    macro_calendar.set_defaults(handler=handle_macro_calendar)

    news_flash = sub.add_parser("news-flash")
    news_flash.add_argument("--scope", choices=tuple(NEWS_SCOPE_MAP), default="all")
    news_flash.add_argument("--limit", type=int, default=DEFAULT_NEWS_LIMIT)
    news_flash.set_defaults(handler=handle_news_flash)
    return parser


def add_history_args(parser: argparse.ArgumentParser, with_adjust: bool) -> None:
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--period", choices=("daily", "weekly", "monthly"), default="daily")
    if with_adjust:
        parser.add_argument("--adjust", choices=("none", "qfq", "hfq"), default="none")
    parser.add_argument("--limit", type=int)


def handle_market_overview(_: argparse.Namespace) -> dict[str, Any]:
    stocks = get_stock_spot_df()
    indices = get_main_index_df()
    changes = pd.to_numeric(stocks["涨跌幅"], errors="coerce").dropna()
    breadth = {"上涨家数": int((changes > 0).sum()), "下跌家数": int((changes < 0).sum()), "平盘家数": int((changes == 0).sum())}
    cols = ["代码", "名称", "最新价", "涨跌幅", "涨跌额", "成交额", "换手率"]
    row = {
        "breadth": breadth,
        "major_indices": dataframe_to_rows(indices[indices["代码"].isin(MAIN_INDEX_CODES)][["代码", "名称", "最新价", "涨跌幅", "涨跌额", "成交额"]]),
        "top_gainers": dataframe_to_rows(stocks.sort_values("涨跌幅", ascending=False).head(10)[cols]),
        "top_losers": dataframe_to_rows(stocks.sort_values("涨跌幅", ascending=True).head(10)[cols]),
    }
    return success_payload("market_overview", ["stock_zh_a_spot_em", "stock_zh_index_spot_em"], {"market": "A股"}, {}, list(row), [row], False)


def handle_stock_quote(args: argparse.Namespace) -> dict[str, Any]:
    resolved = resolve_stock_symbol(args.symbol)
    df = get_stock_spot_df()
    row = df[df["代码"] == resolved.code].head(1)
    if row.empty:
        raise SkillError("runtime_error", f"Resolved stock {resolved.code} was not found in live quote data.")
    return success_payload("stock_quote", "stock_zh_a_spot_em", resolved.payload(), {"symbol": resolved.code}, list(row.columns), dataframe_to_rows(row), False)


def handle_stock_profile(args: argparse.Namespace) -> dict[str, Any]:
    resolved = resolve_stock_symbol(args.symbol)
    df = call_akshare("stock_individual_info_em", symbol=resolved.code)
    return success_payload("stock_profile", "stock_individual_info_em", resolved.payload(), {"symbol": resolved.code}, list(df.columns), dataframe_to_rows(df), False)


def handle_stock_history(args: argparse.Namespace) -> dict[str, Any]:
    resolved = resolve_stock_symbol(args.symbol)
    start, end, limit = resolve_history_window(args.start_date, args.end_date, args.limit)
    adjust = "" if args.adjust == "none" else args.adjust
    df = call_akshare("stock_zh_a_hist", symbol=resolved.code, period=args.period, start_date=start, end_date=end, adjust=adjust)
    rows, truncated = bounded_rows(df, limit, "tail")
    params = {"symbol": resolved.code, "period": args.period, "start_date": start, "end_date": end, "adjust": adjust, "limit": limit}
    return success_payload("stock_history", "stock_zh_a_hist", resolved.payload(), params, list(df.columns), rows, truncated)


def handle_index_quote(args: argparse.Namespace) -> dict[str, Any]:
    resolved = resolve_index_symbol(args.symbol)
    df = get_index_catalog()
    row = df[df["代码"] == resolved.code].head(1)
    return success_payload("index_quote", "stock_zh_index_spot_em", resolved.payload(), {"symbol": resolved.code}, list(row.columns), dataframe_to_rows(row), False)


def handle_index_history(args: argparse.Namespace) -> dict[str, Any]:
    resolved = resolve_index_symbol(args.symbol)
    start, end, limit = resolve_history_window(args.start_date, args.end_date, args.limit)
    df = call_akshare("index_zh_a_hist", symbol=resolved.code, period=args.period, start_date=start, end_date=end)
    rows, truncated = bounded_rows(df, limit, "tail")
    params = {"symbol": resolved.code, "period": args.period, "start_date": start, "end_date": end, "limit": limit}
    return success_payload("index_history", "index_zh_a_hist", resolved.payload(), params, list(df.columns), rows, truncated)


def handle_fund_quote(args: argparse.Namespace) -> dict[str, Any]:
    resolved = resolve_fund_symbol(args.symbol)
    df = get_fund_daily_df()
    row = df[df["基金代码"] == resolved.code].head(1)
    if row.empty:
        raise SkillError("runtime_error", f"Resolved fund {resolved.code} was not found in daily quote data.")
    return success_payload("fund_quote", "fund_open_fund_daily_em", resolved.payload(), {"symbol": resolved.code}, list(row.columns), dataframe_to_rows(row), False)


def handle_fund_history(args: argparse.Namespace) -> dict[str, Any]:
    resolved = resolve_fund_symbol(args.symbol)
    indicator = FUND_INDICATOR_MAP.get(args.indicator)
    if indicator is None:
        raise SkillError("unsupported_query", f"Unsupported fund indicator alias: {args.indicator}")
    df = call_akshare("fund_open_fund_info_em", symbol=resolved.code, indicator=indicator, period=FUND_PERIOD_MAP[args.period])
    limit = args.limit or DEFAULT_HISTORY_LIMIT
    rows, truncated = bounded_rows(df, limit, "tail")
    params = {"symbol": resolved.code, "indicator": indicator, "period": FUND_PERIOD_MAP[args.period], "limit": limit}
    return success_payload("fund_history", "fund_open_fund_info_em", resolved.payload(), params, list(df.columns), rows, truncated)


def handle_macro_series(args: argparse.Namespace) -> dict[str, Any]:
    fn = MACRO_SERIES_MAP.get(args.alias)
    if fn is None:
        raise SkillError("unsupported_query", f"Unsupported macro series alias: {args.alias}", {"supported_aliases": sorted(MACRO_SERIES_MAP)})
    df = call_akshare(fn)
    limit = args.limit or DEFAULT_HISTORY_LIMIT
    rows, truncated = bounded_rows(df, limit, "head")
    return success_payload("macro_series", fn, {"alias": args.alias}, {"alias": args.alias, "limit": limit}, list(df.columns), rows, truncated)


def handle_macro_calendar(args: argparse.Namespace) -> dict[str, Any]:
    date_value = args.date or today_compact()
    validate_compact_date(date_value, "date")
    df = call_akshare("macro_info_ws", date=date_value)
    limit = args.limit or DEFAULT_HISTORY_LIMIT
    rows, truncated = bounded_rows(df, limit, "head")
    return success_payload("macro_calendar", "macro_info_ws", {"date": date_value}, {"date": date_value, "limit": limit}, list(df.columns), rows, truncated)


def handle_news_flash(args: argparse.Namespace) -> dict[str, Any]:
    scope = NEWS_SCOPE_MAP.get(args.scope)
    if scope is None:
        raise SkillError("unsupported_query", f"Unsupported news scope alias: {args.scope}", {"supported_scopes": sorted(NEWS_SCOPE_MAP)})
    df = call_akshare("stock_info_global_cls", symbol=scope).copy()
    if {"发布日期", "发布时间"}.issubset(df.columns):
        sort_key = pd.to_datetime(df["发布日期"].astype(str) + " " + df["发布时间"].astype(str), errors="coerce")
        df = df.assign(_sort=sort_key).sort_values("_sort", ascending=False).drop(columns="_sort")
    rows, truncated = bounded_rows(df, args.limit or DEFAULT_NEWS_LIMIT, "head")
    return success_payload("news_flash", "stock_info_global_cls", {"scope": scope}, {"scope": scope, "limit": args.limit or DEFAULT_NEWS_LIMIT}, list(df.columns), rows, truncated)


def resolve_history_window(start_date: str | None, end_date: str | None, limit: int | None) -> tuple[str, str, int | None]:
    today = today_compact()
    if start_date:
        validate_compact_date(start_date, "start_date")
    if end_date:
        validate_compact_date(end_date, "end_date")
    if start_date and end_date and start_date > end_date:
        raise SkillError("invalid_argument", "start_date must be less than or equal to end_date.")
    if not start_date and not end_date:
        return "19700101", today, limit or DEFAULT_HISTORY_LIMIT
    return start_date or "19700101", end_date or today, limit


def validate_compact_date(value: str, label: str) -> None:
    if not DATE_RE.match(value):
        raise SkillError("invalid_argument", f"{label} must use YYYYMMDD format.", {"value": value})


def today_compact() -> str:
    return dt.date.today().strftime("%Y%m%d")


def success_payload(dataset: str, akshare_function: str | list[str], resolved: dict[str, Any], params: dict[str, Any], columns: list[str], rows: list[dict[str, Any]], truncated: bool) -> dict[str, Any]:
    return {"ok": True, "dataset": dataset, "akshare_function": akshare_function, "resolved": resolved, "params": params, "columns": columns, "rows": rows, "row_count": len(rows), "truncated": truncated, "as_of": dt.datetime.now().astimezone().isoformat(timespec="seconds")}


def bounded_rows(df: pd.DataFrame, limit: int | None, keep: str) -> tuple[list[dict[str, Any]], bool]:
    if limit is not None and limit <= 0:
        raise SkillError("invalid_argument", "limit must be greater than 0.", {"limit": limit})
    if limit is None:
        sliced = df
    elif keep == "tail":
        sliced = df.tail(limit)
    else:
        sliced = df.head(limit)
    return dataframe_to_rows(sliced), limit is not None and len(df) > len(sliced)


def dataframe_to_rows(df: pd.DataFrame) -> list[dict[str, Any]]:
    if df.empty:
        return []
    frame = df.copy().where(pd.notnull(df), None)
    return [{str(k): normalize_value(v) for k, v in row.items()} for row in frame.to_dict(orient="records")]


def normalize_value(value: Any) -> Any:
    if value is None:
        return None
    if hasattr(value, "item") and callable(value.item):
        try:
            value = value.item()
        except Exception:
            pass
    if isinstance(value, float) and math.isnan(value):
        return None
    if pd.isna(value):
        return None
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        return value.isoformat()
    return value


def emit_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))


def resolve_stock_symbol(query: str) -> ResolvedSymbol:
    return resolve_symbol_from_dataframe(get_stock_catalog(), query, "code", "name", "stock")


def resolve_index_symbol(query: str) -> ResolvedSymbol:
    return resolve_symbol_from_dataframe(get_index_catalog(), query, "代码", "名称", "index", ("市场分组",))


def resolve_fund_symbol(query: str) -> ResolvedSymbol:
    return resolve_symbol_from_dataframe(get_fund_catalog(), query, "基金代码", "基金简称", "fund", ("基金类型",))


def resolve_symbol_from_dataframe(df: pd.DataFrame, query: str, code_col: str, name_col: str, category: str, extra_cols: tuple[str, ...] = ()) -> ResolvedSymbol:
    raw = query.strip()
    if not raw:
        raise SkillError("invalid_argument", f"{category} symbol cannot be empty.")
    exact = df[(df[code_col].astype(str) == raw) | (df[name_col].map(normalize_text) == normalize_text(raw))]
    if len(exact) == 1:
        return build_resolved_symbol(exact.iloc[0], raw, code_col, name_col, category, extra_cols)
    if len(exact) > 1:
        raise ambiguous_symbol_error(exact, raw, code_col, name_col, category)
    fuzzy = df[df[code_col].astype(str).str.contains(re.escape(raw), na=False) | df[name_col].map(normalize_text).str.contains(re.escape(normalize_text(raw)), na=False)]
    if len(fuzzy) == 1:
        return build_resolved_symbol(fuzzy.iloc[0], raw, code_col, name_col, category, extra_cols)
    if len(fuzzy) > 1:
        raise ambiguous_symbol_error(fuzzy, raw, code_col, name_col, category)
    raise SkillError("invalid_argument", f"No {category} symbol matched: {raw}")


def build_resolved_symbol(row: pd.Series, raw: str, code_col: str, name_col: str, category: str, extra_cols: tuple[str, ...]) -> ResolvedSymbol:
    extra = {col: normalize_value(row[col]) for col in extra_cols if col in row.index}
    return ResolvedSymbol(input=raw, code=str(row[code_col]), name=str(row[name_col]), category=category, extra=extra or None)


def ambiguous_symbol_error(df: pd.DataFrame, raw: str, code_col: str, name_col: str, category: str) -> SkillError:
    candidates = df[[code_col, name_col]].drop_duplicates().head(10).rename(columns={code_col: "code", name_col: "name"})
    return SkillError("ambiguous_symbol", f"Multiple {category} symbols matched: {raw}", {"candidates": dataframe_to_rows(candidates)})


def normalize_text(value: Any) -> str:
    return re.sub(r"\s+", "", str(value or "")).lower()


@lru_cache(maxsize=1)
def get_stock_catalog() -> pd.DataFrame:
    return call_akshare("stock_info_a_code_name").copy()


@lru_cache(maxsize=1)
def get_stock_spot_df() -> pd.DataFrame:
    return call_akshare("stock_zh_a_spot_em").copy()


@lru_cache(maxsize=1)
def get_index_catalog() -> pd.DataFrame:
    frames = []
    for group in INDEX_GROUPS:
        frame = call_akshare("stock_zh_index_spot_em", symbol=group).copy()
        frame["市场分组"] = group
        frames.append(frame)
    return pd.concat(frames, ignore_index=True).drop_duplicates(subset=["代码"], keep="first")


@lru_cache(maxsize=1)
def get_main_index_df() -> pd.DataFrame:
    return call_akshare("stock_zh_index_spot_em", symbol="沪深重要指数").copy()


@lru_cache(maxsize=1)
def get_fund_catalog() -> pd.DataFrame:
    return call_akshare("fund_name_em").copy()


@lru_cache(maxsize=1)
def get_fund_daily_df() -> pd.DataFrame:
    return call_akshare("fund_open_fund_daily_em").copy()


def call_akshare(function_name: str, **kwargs: Any) -> pd.DataFrame:
    ak = load_akshare_module()
    if not hasattr(ak, function_name):
        raise SkillError("unsupported_query", f"AKShare function is not available: {function_name}")
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
            result = getattr(ak, function_name)(**kwargs)
    except Exception as exc:
        raise SkillError("runtime_error", f"AKShare call failed: {function_name}", {"params": kwargs, "exception": repr(exc)}) from exc
    if not isinstance(result, pd.DataFrame):
        raise SkillError("runtime_error", f"AKShare call did not return a DataFrame: {function_name}")
    return result


def load_akshare_module() -> Any:
    try:
        return importlib.import_module("akshare")
    except ModuleNotFoundError as exc:
        raise SkillError("missing_dependency", "Python package 'akshare' is not installed.", {"install": "python -m pip install akshare --upgrade"}) from exc


if __name__ == "__main__":
    raise SystemExit(main())
