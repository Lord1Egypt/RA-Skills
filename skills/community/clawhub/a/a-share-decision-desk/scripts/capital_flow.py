#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from mx_api import data_query, stock_screen
from runtime_config import require_em_api_key


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WATCHLIST = ROOT / "assets" / "default_watchlists.json"

MARKET_FLOW_QUERY = "全部A股 主力净流入资金 今日 大单净流入 中单净流入 小单净流入"
TOP_FLOW_QUERIES = {
    "inflow": "A股 主力资金净流入前{limit}股票",
    "outflow": "A股 主力资金净流出前{limit}股票",
}


def parse_amount_to_yi(value: object) -> float | None:
    text = str(value or "").strip().replace(",", "")
    if not text:
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return None
    number = float(match.group(0))
    if "万亿" in text:
        return round(number * 10000, 2)
    if "亿" in text:
        return round(number, 2)
    if "万" in text:
        return round(number / 10000, 4)
    if "元" in text or text.endswith("00"):
        return round(number / 100000000, 2)
    return round(number, 2)


def subtract_amounts(left: object, right: object) -> float | None:
    left_value = parse_amount_to_yi(left)
    right_value = parse_amount_to_yi(right)
    if left_value is None or right_value is None:
        return None
    return round(left_value - right_value, 2)


def market_to_symbol(code: str, market: str) -> str:
    market_code = (market or "").strip().lower()
    if market_code.startswith("sh"):
        return f"sh{code}"
    if market_code.startswith("bj"):
        return f"bj{code}"
    return f"sz{code}"


def load_watchlist(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def first_column_key(columns: list[dict], title_terms: list[str], fallback_keys: list[str]) -> str:
    for column in columns:
        title = str(column.get("title", "")).strip()
        if any(term in title for term in title_terms):
            return column.get("key", "")
    for fallback in fallback_keys:
        for column in columns:
            if column.get("key") == fallback:
                return fallback
    return ""


def build_metric_map(table: dict) -> dict[str, object]:
    metric_map: dict[str, object] = {}
    name_map = table.get("nameMap") or {}
    data_table = table.get("table") or {}
    for key, label in name_map.items():
        if key == "headNameSub":
            continue
        values = data_table.get(key) or []
        if values:
            metric_map[str(label)] = values[0]
    return metric_map


def find_metric_value(metric_map: dict[str, object], token_groups: list[list[str]]) -> object | None:
    for tokens in token_groups:
        for label, value in metric_map.items():
            if all(token in label for token in tokens):
                return value
    return None


def fetch_market_flow_snapshot() -> dict:
    result = data_query(MARKET_FLOW_QUERY)
    target_table = next((table for table in result["tables"] if table.get("entityName") == "全部A股"), None)
    if not target_table and result["tables"]:
        target_table = result["tables"][0]
    if not target_table:
        return {
            "label": "未知",
            "main_net_yi": None,
            "big_order_net_yi": None,
            "medium_order_net_yi": None,
            "small_order_net_yi": None,
            "as_of": "",
        }

    metrics = build_metric_map(target_table)
    main_net_yi = parse_amount_to_yi(
        find_metric_value(
            metrics,
            [
                ["主力净流入资金"],
                ["主力净额"],
            ],
        )
    )
    big_order_inflow_yi = parse_amount_to_yi(find_metric_value(metrics, [["大单流入资金"], ["大单流入"]]))
    medium_order_inflow_yi = parse_amount_to_yi(find_metric_value(metrics, [["中单流入资金"], ["中单流入"]]))
    small_order_inflow_yi = parse_amount_to_yi(find_metric_value(metrics, [["小单流入资金"], ["小单流入"]]))
    if main_net_yi is None:
        label = "未知"
    elif main_net_yi >= 50:
        label = "强流入"
    elif main_net_yi > 0:
        label = "偏流入"
    elif main_net_yi <= -50:
        label = "强流出"
    else:
        label = "偏流出"
    return {
        "label": label,
        "main_net_yi": main_net_yi,
        "big_order_inflow_yi": big_order_inflow_yi,
        "medium_order_inflow_yi": medium_order_inflow_yi,
        "small_order_inflow_yi": small_order_inflow_yi,
        "as_of": ((target_table.get("table") or {}).get("headName") or [""])[0],
    }


def fetch_top_main_flows(direction: str, limit: int = 10) -> list[dict]:
    query = TOP_FLOW_QUERIES[direction].format(limit=limit)
    result = stock_screen(query, page_no=1, page_size=limit)
    columns = result["columns"]
    rows = result["rows"]

    flow_key = first_column_key(columns, ["主力净额"], ["010000_FLOWZLAMOUNT<70>{2026-03-20}"])
    amount_key = first_column_key(columns, ["成交额"], ["010000_TRADING_VOLUMES<70>{2026-03-20}"])
    board_key = first_column_key(columns, ["东财行业总分类"], [])
    concept_key = first_column_key(columns, ["概念"], ["STYLE_CONCEPT"])

    items: list[dict] = []
    for row in rows[:limit]:
        code = str(row.get("SECURITY_CODE", "")).strip()
        market = str(row.get("MARKET_SHORT_NAME", "")).strip()
        if not code:
            continue
        main_flow_yi = parse_amount_to_yi(row.get(flow_key))
        trading_amount_yi = parse_amount_to_yi(row.get(amount_key))
        item = {
            "symbol": market_to_symbol(code, market),
            "code": code,
            "name": row.get("SECURITY_SHORT_NAME", ""),
            "market": market,
            "price": row.get("NEWEST_PRICE"),
            "change_pct": row.get("CHG"),
            "main_flow_yi": main_flow_yi,
            "trading_amount_yi": trading_amount_yi,
            "board": row.get(board_key, ""),
            "concept": row.get(concept_key, ""),
            "direction": direction,
            "flow_tag": "主力流入榜" if direction == "inflow" else "主力流出榜",
        }
        items.append(item)
    return items


def build_flow_lookup(inflow_items: list[dict], outflow_items: list[dict]) -> dict[str, dict]:
    lookup: dict[str, dict] = {}
    for item in inflow_items + outflow_items:
        current = lookup.get(item["symbol"])
        if current is None or abs(item.get("main_flow_yi") or 0) > abs(current.get("main_flow_yi") or 0):
            lookup[item["symbol"]] = dict(item)
    return lookup


def build_group_flow_scoreboard(watchlists: dict, groups: list[str], flow_lookup: dict[str, dict]) -> list[dict]:
    scoreboard: list[dict] = []
    for group in groups:
        items = watchlists.get(group, [])
        if not items:
            continue
        inflow_hits: list[dict] = []
        outflow_hits: list[dict] = []
        net_flow_yi = 0.0
        for item in items:
            flow = flow_lookup.get(item["symbol"])
            if not flow:
                continue
            if flow["direction"] == "inflow":
                inflow_hits.append(flow)
            else:
                outflow_hits.append(flow)
            net_flow_yi += flow.get("main_flow_yi") or 0.0
        if inflow_hits and len(inflow_hits) >= len(outflow_hits):
            bias = "资金共振"
        elif outflow_hits and len(outflow_hits) > len(inflow_hits):
            bias = "资金承压"
        else:
            bias = "中性"
        leaders = inflow_hits if inflow_hits else outflow_hits
        top_names = "、".join(flow["name"] for flow in leaders[:3]) or "n/a"
        scoreboard.append(
            {
                "group": group,
                "inflow_hits": len(inflow_hits),
                "outflow_hits": len(outflow_hits),
                "net_flow_yi": round(net_flow_yi, 2),
                "bias": bias,
                "leaders": top_names,
            }
        )
    return scoreboard


def attach_flow_tags(rows: list[dict], flow_lookup: dict[str, dict]) -> list[dict]:
    tagged: list[dict] = []
    for row in rows:
        symbol = ""
        code = str(row.get("code", "")).strip()
        if code:
            if code.startswith(("sh", "sz", "bj")):
                symbol = code
            elif code[0] in {"6", "9"}:
                symbol = f"sh{code}"
            elif code[0] in {"4", "8"}:
                symbol = f"bj{code}"
            else:
                symbol = f"sz{code}"
        flow = flow_lookup.get(symbol)
        enriched = dict(row)
        enriched["flow_tag"] = flow.get("flow_tag", "") if flow else ""
        enriched["flow_yi"] = flow.get("main_flow_yi") if flow else None
        tagged.append(enriched)
    return tagged


def render_flow_snapshot(snapshot: dict) -> list[dict]:
    return [
        {
            "label": snapshot.get("label", ""),
            "main_net_yi": snapshot.get("main_net_yi"),
            "big_order_inflow_yi": snapshot.get("big_order_inflow_yi"),
            "medium_order_inflow_yi": snapshot.get("medium_order_inflow_yi"),
            "small_order_inflow_yi": snapshot.get("small_order_inflow_yi"),
            "as_of": snapshot.get("as_of", ""),
        }
    ]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Capital-flow monitor for uwillberich.")
    parser.add_argument(
        "--watchlist",
        default=str(DEFAULT_WATCHLIST),
        help="Watchlist JSON path.",
    )
    parser.add_argument(
        "--groups",
        nargs="+",
        default=["tech_repair", "defensive_gauge"],
        help="Watchlist groups to intersect with top-flow leaderboards.",
    )
    parser.add_argument("--limit", type=int, default=10, help="Top inflow/outflow rows to fetch.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser


def main() -> int:
    require_em_api_key(script_hint="python3 skill/uwillberich/scripts/runtime_config.py set-em-key --stdin")
    args = build_parser().parse_args()
    watchlists = load_watchlist(args.watchlist)
    snapshot = fetch_market_flow_snapshot()
    inflow_items = fetch_top_main_flows("inflow", limit=args.limit)
    outflow_items = fetch_top_main_flows("outflow", limit=args.limit)
    flow_lookup = build_flow_lookup(inflow_items, outflow_items)
    group_flow = build_group_flow_scoreboard(watchlists, args.groups, flow_lookup)
    payload = {
        "market_flow": snapshot,
        "top_inflow": inflow_items,
        "top_outflow": outflow_items,
        "group_flow": group_flow,
    }
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print("# Capital Flow")
    print()
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
