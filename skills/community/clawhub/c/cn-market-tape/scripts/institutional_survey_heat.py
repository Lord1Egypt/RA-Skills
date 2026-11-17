#!/usr/bin/env python3
"""Aggregate A-share institutional survey heat from public market data."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError


SURVEY_URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"
QUOTE_URL = "https://push2delay.eastmoney.com/api/qt/ulist.np/get"
QUOTE_UT = "fa5fd1943c7b386f172d6893dbfba10b"

SURVEY_COLUMNS = ",".join(
    [
        "SECUCODE",
        "SECURITY_CODE",
        "SECURITY_NAME_ABBR",
        "NOTICE_DATE",
        "RECEIVE_START_DATE",
        "RECEIVE_OBJECT_TYPE",
        "RECEIVE_OBJECT",
        "RECEIVE_WAY_EXPLAIN",
    ]
)


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def add_months(year: int, month: int, delta: int) -> tuple[int, int]:
    month_index = year * 12 + (month - 1) + delta
    return month_index // 12, month_index % 12 + 1


def calendar_month_start(end_date: date, months: int) -> date:
    year, month = add_months(end_date.year, end_date.month, -(months - 1))
    return date(year, month, 1)


def cache_key(prefix: str, payload: Any) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return f"{prefix}_{hashlib.sha256(raw).hexdigest()[:16]}.json"


def cache_fresh(path: Path, ttl_hours: float) -> bool:
    if not path.exists():
        return False
    age_hours = (time.time() - path.stat().st_mtime) / 3600
    return age_hours <= ttl_hours


def read_cache(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_cache(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def endpoint_family(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    return f"{parsed.netloc}{parsed.path}"


def throttle_same_host(url: str, request_state: dict[str, Any]) -> None:
    host = urllib.parse.urlsplit(url).netloc
    last_host = request_state.get("last_host")
    consecutive = int(request_state.get("consecutive", 0)) if last_host == host else 0
    if consecutive and consecutive % 3 == 0:
        time.sleep(random.uniform(8.0, 20.0))
    request_state["last_host"] = host
    request_state["consecutive"] = consecutive + 1


def fetch_json(url: str, timeout: int, request_state: dict[str, Any]) -> dict[str, Any]:
    throttle_same_host(url, request_state)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def fetch_with_retry(
    url: str,
    timeout: int,
    retries: int,
    retry_sleep: float,
    request_state: dict[str, Any],
) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return fetch_json(url, timeout, request_state)
        except (HTTPError, URLError, TimeoutError) as exc:
            message = f"request failed: host={urllib.parse.urlsplit(url).netloc} endpoint={endpoint_family(url)} error={exc}"
            raise RuntimeError(message) from exc
        except Exception as exc:  # noqa: BLE001 - CLI should surface concise network failures.
            last_error = exc
            if attempt < retries:
                time.sleep(retry_sleep)
    raise RuntimeError(
        f"request failed after {retries + 1} attempts: "
        f"host={urllib.parse.urlsplit(url).netloc} endpoint={endpoint_family(url)} error={last_error}"
    )


def fetch_survey_rows(args: argparse.Namespace, start: date, end: date) -> tuple[list[dict[str, Any]], int, int]:
    payload = {
        "start": str(start),
        "end": str(end),
        "columns": SURVEY_COLUMNS,
        "source": "RPT_ORG_SURVEYNEW",
    }
    cache_path = args.cache_dir / cache_key("survey", payload)
    if not args.no_cache and cache_fresh(cache_path, args.cache_ttl_hours):
        cached = read_cache(cache_path)
        return cached["rows"], cached["pages"], cached["count"]

    base_params = {
        "sortColumns": "RECEIVE_START_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "reportName": "RPT_ORG_SURVEYNEW",
        "columns": SURVEY_COLUMNS,
        "source": "WEB",
        "client": "WEB",
        "filter": f"(RECEIVE_START_DATE>='{start}')(RECEIVE_START_DATE<='{end}')",
    }

    def fetch_page(page: int) -> dict[str, Any]:
        params = dict(base_params)
        params["pageNumber"] = str(page)
        url = SURVEY_URL + "?" + urllib.parse.urlencode(params)
        return fetch_with_retry(url, args.timeout, args.retries, args.retry_sleep, args.request_state)

    first = fetch_page(1)
    result = first.get("result") or {}
    pages = int(result.get("pages") or 0)
    count = int(result.get("count") or 0)
    rows: list[dict[str, Any]] = []
    for page in range(1, pages + 1):
        data = first if page == 1 else fetch_page(page)
        rows.extend((data.get("result") or {}).get("data") or [])
        if page < pages:
            time.sleep(args.page_sleep)

    if not args.no_cache:
        write_cache(cache_path, {"rows": rows, "pages": pages, "count": count})
    return rows, pages, count


def secid(secucode: str) -> str:
    code, market = secucode.split(".")
    prefix = "1" if market == "SH" else "0"
    return f"{prefix}.{code}"


def fetch_industry_map(args: argparse.Namespace, codes: list[str]) -> tuple[dict[str, dict[str, str]], int]:
    payload = {"codes": sorted(codes), "fields": "f12,f14,f100,f103"}
    cache_path = args.cache_dir / cache_key("industry", payload)
    if not args.no_cache and cache_fresh(cache_path, args.cache_ttl_hours):
        cached = read_cache(cache_path)
        return cached["industry_map"], cached["batches"]

    industry_map: dict[str, dict[str, str]] = {}
    batches = 0
    for idx in range(0, len(codes), args.quote_batch_size):
        batch = codes[idx : idx + args.quote_batch_size]
        params = {
            "fltt": "2",
            "invt": "2",
            "fields": "f12,f14,f100,f103",
            "secids": ",".join(secid(code) for code in batch),
            "ut": QUOTE_UT,
        }
        url = QUOTE_URL + "?" + urllib.parse.urlencode(params)
        data = fetch_with_retry(url, args.timeout, args.retries, args.retry_sleep, args.request_state)
        batches += 1
        by_plain_code = {code.split(".")[0]: code for code in batch}
        for item in (data.get("data") or {}).get("diff") or []:
            secucode = by_plain_code.get(item.get("f12"))
            if secucode:
                industry_map[secucode] = {
                    "industry": item.get("f100") or "未分类",
                    "concepts": item.get("f103") or "",
                }
        if idx + args.quote_batch_size < len(codes):
            time.sleep(args.quote_sleep)

    if not args.no_cache:
        write_cache(cache_path, {"industry_map": industry_map, "batches": batches})
    return industry_map, batches


def row_date(row: dict[str, Any]) -> date | None:
    value = (row.get("RECEIVE_START_DATE") or "")[:10]
    if not value:
        return None
    try:
        return parse_date(value)
    except ValueError:
        return None


def iso_week_key(day: date) -> str:
    year, week, _ = day.isocalendar()
    return f"{year}-W{week:02d}"


def collect_names_and_orgs(rows: list[dict[str, Any]]) -> tuple[dict[str, str], list[tuple[date, str, str, str]]]:
    stock_names: dict[str, str] = {}
    records: list[tuple[date, str, str, str]] = []
    for row in rows:
        if row.get("RECEIVE_OBJECT_TYPE") != "001":
            continue
        day = row_date(row)
        code = row.get("SECUCODE")
        name = row.get("SECURITY_NAME_ABBR")
        org = (row.get("RECEIVE_OBJECT") or "").strip()
        if not day or not code or not name or not org:
            continue
        stock_names[code] = name
        records.append((day, code, name, org))
    return stock_names, records


def aggregate_stock_and_sector(
    records: list[tuple[date, str, str, str]],
    industry_map: dict[str, dict[str, str]],
    start: date,
    end: date,
    top: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    stock_orgs: dict[str, set[str]] = defaultdict(set)
    stock_names: dict[str, str] = {}
    stock_dates: dict[str, set[str]] = defaultdict(set)
    for day, code, name, org in records:
        if start <= day <= end:
            stock_orgs[code].add(org)
            stock_names[code] = name
            stock_dates[code].add(str(day))

    stock_rank = sorted(stock_orgs, key=lambda code: len(stock_orgs[code]), reverse=True)
    top_stocks = [
        {
            "rank": idx + 1,
            "code": code,
            "name": stock_names.get(code, ""),
            "institutionCount": len(stock_orgs[code]),
            "industry": industry_map.get(code, {}).get("industry", "未分类"),
            "concepts": industry_map.get(code, {}).get("concepts", ""),
            "surveyDates": sorted(stock_dates[code]),
        }
        for idx, code in enumerate(stock_rank[:top])
    ]

    sector_total: dict[str, int] = defaultdict(int)
    sector_stocks: dict[str, list[tuple[str, str, int]]] = defaultdict(list)
    for code in stock_rank:
        industry = industry_map.get(code, {}).get("industry", "未分类")
        count = len(stock_orgs[code])
        sector_total[industry] += count
        sector_stocks[industry].append((code, stock_names.get(code, ""), count))

    sector_rank = sorted(sector_total, key=lambda industry: sector_total[industry], reverse=True)
    top_sectors = [
        {
            "rank": idx + 1,
            "industry": industry,
            "institutionCountSum": sector_total[industry],
            "topStocks": [
                {"code": code, "name": name, "institutionCount": count}
                for code, name, count in sorted(sector_stocks[industry], key=lambda row: row[2], reverse=True)[:top]
            ],
        }
        for idx, industry in enumerate(sector_rank[:top])
    ]
    return top_stocks, top_sectors


def aggregate_weekly_sectors(
    records: list[tuple[date, str, str, str]],
    industry_map: dict[str, dict[str, str]],
    start: date,
    end: date,
    top: int,
) -> tuple[list[str], list[dict[str, Any]], dict[tuple[str, str], list[tuple[str, str, int]]]]:
    stock_week_orgs: dict[tuple[str, str], set[str]] = defaultdict(set)
    stock_names: dict[str, str] = {}
    for day, code, name, org in records:
        if start <= day <= end:
            week = iso_week_key(day)
            stock_week_orgs[(code, week)].add(org)
            stock_names[code] = name

    weeks = sorted({week for _, week in stock_week_orgs})
    sector_week: dict[tuple[str, str], int] = defaultdict(int)
    sector_stock_week: dict[tuple[str, str], list[tuple[str, str, int]]] = defaultdict(list)
    for (code, week), orgs in stock_week_orgs.items():
        industry = industry_map.get(code, {}).get("industry", "未分类")
        count = len(orgs)
        sector_week[(industry, week)] += count
        sector_stock_week[(industry, week)].append((code, stock_names.get(code, ""), count))

    sectors = sorted({industry for industry, _ in sector_week})
    sector_total = {industry: sum(sector_week[(industry, week)] for week in weeks) for industry in sectors}
    ranked = sorted(sectors, key=lambda industry: sector_total[industry], reverse=True)
    weekly = [
        {
            "rank": idx + 1,
            "industry": industry,
            "total": sector_total[industry],
            "weekly": {week: sector_week[(industry, week)] for week in weeks},
        }
        for idx, industry in enumerate(ranked[:top])
    ]
    return weeks, weekly, sector_stock_week


def save_csv(
    output_dir: Path,
    top_stocks: list[dict[str, Any]],
    top_sectors: list[dict[str, Any]],
    weeks: list[str],
    weekly_sectors: list[dict[str, Any]],
) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "topStocksCsv": str(output_dir / "survey_top_stocks.csv"),
        "topSectorsCsv": str(output_dir / "survey_top_sectors.csv"),
        "weeklySectorsCsv": str(output_dir / "survey_weekly_sector_heat.csv"),
    }
    with Path(paths["topStocksCsv"]).open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "code", "name", "institution_count", "industry", "survey_dates", "concepts"])
        for row in top_stocks:
            writer.writerow(
                [
                    row["rank"],
                    row["code"],
                    row["name"],
                    row["institutionCount"],
                    row["industry"],
                    ",".join(row["surveyDates"]),
                    row["concepts"],
                ]
            )
    with Path(paths["topSectorsCsv"]).open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "industry", "institution_count_sum", "top_stocks"])
        for row in top_sectors:
            top_stock_text = "; ".join(
                f"{item['name']}({item['code']}) {item['institutionCount']}" for item in row["topStocks"]
            )
            writer.writerow([row["rank"], row["industry"], row["institutionCountSum"], top_stock_text])
    with Path(paths["weeklySectorsCsv"]).open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "industry", "total"] + weeks)
        for row in weekly_sectors:
            writer.writerow([row["rank"], row["industry"], row["total"]] + [row["weekly"].get(week, 0) for week in weeks])
    return paths


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# A股机构调研热度",
        "",
        f"- {summary['stockWindow']['days']}天窗口: {summary['stockWindow']['start']} 至 {summary['stockWindow']['end']}",
        f"- 周度窗口: {summary['weeklyWindow']['start']} 至 {summary['weeklyWindow']['end']}",
        f"- 请求: 调研明细 {summary['requestCountApprox']['surveyPages']} 页 + 行业补齐 {summary['requestCountApprox']['quoteBatches']} 批，合计约 {summary['requestCountApprox']['total']} 次",
        f"- 原始明细: {summary['rawRowsFetched']} 行；机构调研股票: {summary['stocksWithInstitutionSurvey']} 只",
        f"- 口径: {summary['method']}",
        "",
        f"## 调研最多股票 Top {summary['top']}",
        "| 排名 | 股票 | 机构数 | 行业 | 调研日期 |",
        "|---:|---|---:|---|---|",
    ]
    for row in summary["topStocks"]:
        lines.append(
            f"| {row['rank']} | {row['name']} `{row['code']}` | {row['institutionCount']} | {row['industry']} | {', '.join(row['surveyDates'])} |"
        )
    lines.extend(
        [
            "",
            f"## 板块/行业调研热度 Top {summary['top']}",
            "| 排名 | 行业 | 机构数合计 | 主要贡献股票 |",
            "|---:|---|---:|---|",
        ]
    )
    for row in summary["topSectors"]:
        top_stocks = "；".join(
            f"{item['name']} {item['institutionCount']}" for item in row["topStocks"][:5]
        )
        lines.append(f"| {row['rank']} | {row['industry']} | {row['institutionCountSum']} | {top_stocks} |")
    lines.extend(
        [
            "",
            "## Top 板块周度调研热度",
            "| 行业 | 合计 | " + " | ".join(summary["weeks"]) + " |",
            "|---|---:|" + "|".join(["---:"] * len(summary["weeks"])) + "|",
        ]
    )
    for row in summary["weeklySectors"]:
        values = " | ".join(str(row["weekly"].get(week, 0)) for week in summary["weeks"])
        lines.append(f"| {row['industry']} | {row['total']} | {values} |")
    if summary.get("csvFiles"):
        lines.extend(["", "## CSV", *[f"- {key}: {value}" for key, value in summary["csvFiles"].items()]])
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--end-date", default=str(date.today()), help="YYYY-MM-DD, default today")
    parser.add_argument("--days", type=int, default=7, help="Window for stock and sector Top lists")
    parser.add_argument("--months", type=int, default=2, help="Calendar months for weekly sector trend")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--save-csv", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=Path(tempfile.gettempdir()) / "a_share_survey_heat")
    parser.add_argument("--cache-dir", type=Path, default=Path(tempfile.gettempdir()) / "a_share_survey_heat_cache")
    parser.add_argument("--cache-ttl-hours", type=float, default=12.0)
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--retry-sleep", type=float, default=1.5)
    parser.add_argument("--page-sleep", type=float, default=0.45)
    parser.add_argument("--quote-sleep", type=float, default=0.25)
    parser.add_argument("--quote-batch-size", type=int, default=80)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    args.request_state = {}
    end = parse_date(args.end_date)
    stock_start = end - timedelta(days=args.days - 1)
    weekly_start = calendar_month_start(end, args.months)
    fetch_start = min(stock_start, weekly_start)

    try:
        rows, pages, raw_count = fetch_survey_rows(args, fetch_start, end)
        stock_names, records = collect_names_and_orgs(rows)
        industry_map, quote_batches = fetch_industry_map(args, list(stock_names))
    except RuntimeError as exc:
        print(f"机构调研数据源失败：{exc}", file=sys.stderr)
        return 2

    top_stocks, top_sectors = aggregate_stock_and_sector(records, industry_map, stock_start, end, args.top)
    weeks, weekly_sectors, _sector_stock_week = aggregate_weekly_sectors(records, industry_map, weekly_start, end, args.top)

    summary: dict[str, Any] = {
        "stockWindow": {"start": str(stock_start), "end": str(end), "days": args.days},
        "weeklyWindow": {"start": str(weekly_start), "end": str(end), "months": args.months},
        "requestCountApprox": {"surveyPages": pages, "quoteBatches": quote_batches, "total": pages + quote_batches},
        "rawRowsExpected": raw_count,
        "rawRowsFetched": len(rows),
        "stocksWithInstitutionSurvey": len(stock_names),
        "weeks": weeks,
        "top": args.top,
        "method": "Count unique RECEIVE_OBJECT where RECEIVE_OBJECT_TYPE == 001; stock/sector Top lists use the recent-day window; weekly sector heat counts unique institution per stock-week and aggregates to Eastmoney industry.",
        "topStocks": top_stocks,
        "topSectors": top_sectors,
        "weeklySectors": weekly_sectors,
    }
    if args.save_csv:
        summary["csvFiles"] = save_csv(args.output_dir, top_stocks, top_sectors, weeks, weekly_sectors)

    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
