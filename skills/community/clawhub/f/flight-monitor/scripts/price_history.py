#!/usr/bin/env python3
"""
price_history.py — Read and write flight price history records.

Storage layout:
  ~/.workbuddy/flight-monitor/{DEP}-{ARR}-{DATE}.json

Usage:
    # Append a price record
    python price_history.py append --from BJS --to SYX --date 2026-03-25 --price 1280 --flight CA1234

    # Show history for a route
    python price_history.py show --from BJS --to SYX --date 2026-03-25

    # List all monitored routes
    python price_history.py list
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

HISTORY_DIR = Path.home() / ".workbuddy" / "flight-monitor"

# ── Input validators (whitelist approach) ───────────────────────────────────
_CITY_CODE_RE = re.compile(r'^[A-Za-z]{2,4}$')
_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def _validate_city_code(code: str) -> bool:
    """Only allow 2-4 letter IATA city/airport codes."""
    return bool(_CITY_CODE_RE.match(code))


def _validate_date(date: str) -> bool:
    """Only allow dates in YYYY-MM-DD format with plausible values."""
    if not _DATE_RE.match(date):
        return False
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def _validate_inputs(dep: str, arr: str, date: str) -> str | None:
    """
    Validate all three route parameters. Returns an error message string if
    validation fails, or None if all inputs are safe.
    """
    if not _validate_city_code(dep):
        return f"❌ 无效的出发城市代码 `{dep}`（只允许 2-4 位字母 IATA 代码，如 BJS、SHA）"
    if not _validate_city_code(arr):
        return f"❌ 无效的到达城市代码 `{arr}`（只允许 2-4 位字母 IATA 代码，如 SYX、CTU）"
    if not _validate_date(date):
        return f"❌ 无效的日期 `{date}`（格式应为 YYYY-MM-DD，如 2026-04-10）"
    return None


def _safe_resolve_under(path: Path, base: Path) -> bool:
    """Return True only if the resolved path is strictly under base directory."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def _route_key(dep: str, arr: str, date: str) -> str:
    return f"{dep.upper()}-{arr.upper()}-{date}"


def _history_file(dep: str, arr: str, date: str) -> Path:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    target = HISTORY_DIR / f"{_route_key(dep, arr, date)}.json"
    if not _safe_resolve_under(target, HISTORY_DIR):
        raise ValueError(f"安全错误：路径 `{target}` 超出允许的存储目录范围")
    return target


def load_history(dep: str, arr: str, date: str) -> dict:
    err = _validate_inputs(dep, arr, date)
    if err:
        raise ValueError(err)
    f = _history_file(dep, arr, date)
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return {
        "route": f"{dep.upper()} → {arr.upper()}",
        "date": date,
        "records": [],
        "threshold": None,
    }


def save_history(dep: str, arr: str, date: str, data: dict):
    err = _validate_inputs(dep, arr, date)
    if err:
        raise ValueError(err)
    f = _history_file(dep, arr, date)
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def append_record(dep: str, arr: str, date: str, price: float,
                  flight: str = "", threshold: float = None) -> dict:
    err = _validate_inputs(dep, arr, date)
    if err:
        raise ValueError(err)
    data = load_history(dep, arr, date)
    if threshold is not None:
        data["threshold"] = threshold

    prev_price = data["records"][-1]["price"] if data["records"] else None
    change = None
    if prev_price is not None:
        change = price - prev_price

    record = {
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "price": price,
        "flight": flight,
        "change": change,
    }
    data["records"].append(record)
    save_history(dep, arr, date, data)
    return data


def format_history(data: dict) -> str:
    records = data.get("records", [])
    route = data.get("route", "")
    date = data.get("date", "")
    threshold = data.get("threshold")

    lines = [
        f"# {route} 机票价格历史",
        "",
        f"- 航线：{route}",
        f"- 出行日期：{date}",
    ]
    if threshold:
        lines.append(f"- 低价阈值：¥{threshold}")
    lines.append("")

    if not records:
        lines.append("暂无记录。")
        return "\n".join(lines)

    lines += [
        "## 价格记录",
        "",
        "| 查询时间 | 价格 | 航班 | 变化 |",
        "|----------|------|------|------|",
    ]
    for r in records:
        change_str = ""
        if r.get("change") is not None:
            diff = r["change"]
            change_str = f"↑¥{diff}" if diff > 0 else (f"↓¥{abs(diff)}" if diff < 0 else "−")
        lines.append(f"| {r['ts']} | ¥{r['price']} | {r.get('flight','')} | {change_str} |")

    prices = [r["price"] for r in records]
    lines += [
        "",
        f"**最低价：** ¥{min(prices)}  |  **最高价：** ¥{max(prices)}  |  **最新价：** ¥{prices[-1]}",
    ]

    # Trigger alert
    if threshold and prices[-1] <= threshold:
        lines += [
            "",
            f"> 🔔 **低价提醒！** 当前价格 ¥{prices[-1]} 已低于阈值 ¥{threshold}",
        ]

    return "\n".join(lines)


def list_routes() -> str:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    files = list(HISTORY_DIR.glob("*.json"))
    if not files:
        return "暂无监控记录。"

    lines = ["## 当前监控路线", "", "| 航线 | 日期 | 最新价 | 阈值 | 记录次数 |",
             "|------|------|--------|------|----------|"]
    for f in sorted(files):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            records = data.get("records", [])
            latest = f"¥{records[-1]['price']}" if records else "−"
            threshold = f"¥{data['threshold']}" if data.get("threshold") else "−"
            lines.append(
                f"| {data.get('route','')} | {data.get('date','')} | {latest} | {threshold} | {len(records)} |"
            )
        except Exception:
            pass
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Flight price history manager")
    sub = parser.add_subparsers(dest="cmd")

    p_append = sub.add_parser("append")
    p_append.add_argument("--from", dest="dep", required=True)
    p_append.add_argument("--to", dest="arr", required=True)
    p_append.add_argument("--date", required=True)
    p_append.add_argument("--price", type=float, required=True)
    p_append.add_argument("--flight", default="")
    p_append.add_argument("--threshold", type=float)

    p_show = sub.add_parser("show")
    p_show.add_argument("--from", dest="dep", required=True)
    p_show.add_argument("--to", dest="arr", required=True)
    p_show.add_argument("--date", required=True)

    sub.add_parser("list")

    args = parser.parse_args()

    if args.cmd == "append":
        try:
            data = append_record(args.dep, args.arr, args.date, args.price,
                                 args.flight, args.threshold)
            print(format_history(data))
        except ValueError as e:
            print(str(e))
            sys.exit(1)
    elif args.cmd == "show":
        try:
            data = load_history(args.dep, args.arr, args.date)
            print(format_history(data))
        except ValueError as e:
            print(str(e))
            sys.exit(1)
    elif args.cmd == "list":
        print(list_routes())
    else:
        parser.print_help()


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    main()
