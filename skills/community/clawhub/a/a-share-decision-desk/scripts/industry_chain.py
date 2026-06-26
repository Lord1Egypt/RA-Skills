#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from mx_api import stock_screen
from runtime_config import require_em_api_key


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WATCHLIST = ROOT / "assets" / "default_watchlists.json"
DEFAULT_CHAIN_CONFIG = ROOT / "assets" / "industry_chains.json"
DEFAULT_EVENT_WATCHLIST = Path.home() / ".uwillberich" / "news-iterator" / "event_watchlists.json"


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def merge_item_details(existing: dict, incoming: dict) -> dict:
    merged = dict(existing)
    for key, value in incoming.items():
        if not merged.get(key) and value:
            merged[key] = value
    return merged


def build_symbol_index(base_watchlists: dict) -> dict[str, dict]:
    symbol_index: dict[str, dict] = {}
    for items in base_watchlists.values():
        for item in items:
            symbol = item["symbol"]
            if symbol in symbol_index:
                symbol_index[symbol] = merge_item_details(symbol_index[symbol], item)
            else:
                symbol_index[symbol] = dict(item)
    return symbol_index


def market_to_symbol(code: str, market: str) -> str:
    market_code = (market or "").strip().lower()
    if market_code.startswith("sh"):
        return f"sh{code}"
    if market_code.startswith("bj"):
        return f"bj{code}"
    return f"sz{code}"


def select_chain_themes(event_payload: dict, selected_groups: list[str], chain_config: dict, max_themes: int = 3) -> list[dict]:
    score_map: dict[str, int] = {}
    reason_map: dict[str, list[str]] = {}
    theme_map = {theme["id"]: theme for theme in chain_config.get("themes", [])}
    group_theme_hints = chain_config.get("group_theme_hints", {})

    def bump(theme_id: str, points: int, reason: str) -> None:
        score_map[theme_id] = score_map.get(theme_id, 0) + points
        reason_map.setdefault(theme_id, [])
        if reason not in reason_map[theme_id]:
            reason_map[theme_id].append(reason)

    for group in selected_groups:
        for theme_id in group_theme_hints.get(group, []):
            bump(theme_id, 3, f"group:{group}")

    summary = event_payload.get("summary", [])
    default_report_groups = event_payload.get("default_report_groups", [])
    for theme in chain_config.get("themes", []):
        theme_id = theme["id"]
        preferred_groups = set(theme.get("preferred_groups", []))
        for group in default_report_groups:
            if group in preferred_groups:
                bump(theme_id, 2, f"event_group:{group}")
        trigger_terms = [term.lower() for term in theme.get("triggers", [])]
        for item in summary:
            if item.get("category") in theme.get("categories", []):
                category_points = max(3, int((int(item.get("total_score", 0)) + 2) / 3))
                bump(theme_id, category_points, f"category:{item.get('category')}")
            for keyword in item.get("top_keywords", []):
                lower_keyword = str(keyword).lower()
                if any(term in lower_keyword or lower_keyword in term for term in trigger_terms):
                    bump(theme_id, max(2, item.get("alert_count", 1)), f"keyword:{keyword}")

    ranked = sorted(
        (
            {
                "id": theme_id,
                "label": theme_map[theme_id]["label"],
                "query": theme_map[theme_id]["query"],
                "score": score,
                "reasons": reason_map.get(theme_id, []),
            }
            for theme_id, score in score_map.items()
            if score > 0 and theme_id in theme_map
        ),
        key=lambda item: (-item["score"], item["id"]),
    )
    return ranked[:max_themes]


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


def build_chain_item(theme: dict, row: dict, symbol_index: dict[str, dict], columns: list[dict], theme_score: int) -> dict:
    code = str(row.get("SECURITY_CODE", "")).strip()
    market = str(row.get("MARKET_SHORT_NAME", "")).strip()
    symbol = market_to_symbol(code, market)
    base = symbol_index.get(symbol, {})
    board_key = first_column_key(columns, ["东财行业总分类"], [])
    concept_key = first_column_key(columns, ["概念"], ["STYLE_CONCEPT"])
    flow_key = first_column_key(columns, ["主力净额"], [])
    role = base.get("role") or base.get("chain_role") or f"{theme['label']}观察"
    board = str(row.get(board_key, "")).strip()
    concept = str(row.get(concept_key, "")).strip()
    driver_parts = ["产业链", theme["label"]]
    if board:
        driver_parts.append(board)
    elif concept:
        driver_parts.append(concept[:32])
    return {
        "symbol": symbol,
        "name": row.get("SECURITY_SHORT_NAME", ""),
        "role": role,
        "event_score": theme_score,
        "trigger_count": 1,
        "event_driver": " | ".join(driver_parts),
        "strong_signal": base.get("strong_signal") or theme.get("strong_signal", ""),
        "weak_signal": base.get("weak_signal") or theme.get("weak_signal", ""),
        "chain_theme": theme["label"],
        "chain_query": theme["query"],
        "flow_hint": row.get(flow_key, ""),
    }


def fetch_chain_group(theme: dict, symbol_index: dict[str, dict], limit: int, theme_score: int) -> list[dict]:
    result = stock_screen(theme["query"], page_no=1, page_size=max(limit, 10))
    items: list[dict] = []
    seen: set[str] = set()
    for row in result["rows"]:
        code = str(row.get("SECURITY_CODE", "")).strip()
        market = str(row.get("MARKET_SHORT_NAME", "")).strip()
        if not code:
            continue
        symbol = market_to_symbol(code, market)
        if symbol in seen:
            continue
        seen.add(symbol)
        items.append(build_chain_item(theme, row, symbol_index, result["columns"], theme_score))
        if len(items) >= limit:
            break
    return items


def enrich_event_payload_with_chain_focus(
    event_payload: dict,
    base_watchlists: dict,
    selected_groups: list[str] | None = None,
    chain_config_path: str | None = None,
    max_themes: int = 3,
    limit: int = 6,
) -> dict:
    if not event_payload:
        return {}

    chain_config = load_json(chain_config_path or str(DEFAULT_CHAIN_CONFIG))
    symbol_index = build_symbol_index(base_watchlists)
    selected_themes = select_chain_themes(event_payload, selected_groups or [], chain_config, max_themes=max_themes)
    if not selected_themes:
        return event_payload

    theme_map = {theme["id"]: theme for theme in chain_config.get("themes", [])}
    enriched = {
        **event_payload,
        "groups": dict(event_payload.get("groups", {})),
        "default_report_groups": list(event_payload.get("default_report_groups", [])),
        "chain_summary": [],
    }
    existing_groups = set(enriched["default_report_groups"])

    for selected in selected_themes:
        theme = theme_map[selected["id"]]
        try:
            items = fetch_chain_group(theme, symbol_index, limit=limit, theme_score=selected["score"])
        except Exception as exc:
            chain_errors = list(enriched.get("chain_errors", []))
            chain_errors.append({"theme": theme["label"], "error": str(exc)})
            enriched["chain_errors"] = chain_errors
            continue
        if not items:
            continue
        group_name = f"chain_focus_{theme['id']}"
        enriched["groups"][group_name] = items
        if group_name not in existing_groups:
            enriched["default_report_groups"].append(group_name)
            existing_groups.add(group_name)
        enriched["chain_summary"].append(
            {
                "group": group_name,
                "theme": theme["label"],
                "score": selected["score"],
                "query": theme["query"],
                "reasons": selected.get("reasons", []),
            }
        )
    return enriched


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build industry-chain focus pools from events and watchlists.")
    parser.add_argument("--watchlist", default=str(DEFAULT_WATCHLIST), help="Base watchlist JSON path.")
    parser.add_argument(
        "--event-watchlist",
        default=str(DEFAULT_EVENT_WATCHLIST),
        help="Path to event_watchlists.json generated by news_iterator.",
    )
    parser.add_argument("--chain-config", default=str(DEFAULT_CHAIN_CONFIG), help="Industry-chain config JSON path.")
    parser.add_argument("--groups", nargs="+", default=["tech_repair", "defensive_gauge"], help="Current desk groups.")
    parser.add_argument("--limit", type=int, default=6, help="Names per chain theme.")
    parser.add_argument("--max-themes", type=int, default=3, help="Maximum number of chain themes.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser


def main() -> int:
    require_em_api_key(script_hint="python3 skill/uwillberich/scripts/runtime_config.py set-em-key --stdin")
    args = build_parser().parse_args()
    base_watchlists = load_json(args.watchlist)
    event_payload = load_json(args.event_watchlist)
    enriched = enrich_event_payload_with_chain_focus(
        event_payload,
        base_watchlists,
        selected_groups=args.groups,
        chain_config_path=args.chain_config,
        max_themes=args.max_themes,
        limit=args.limit,
    )
    if args.format == "json":
        print(json.dumps(enriched, ensure_ascii=False, indent=2))
        return 0
    print("# Industry Chain Focus")
    print()
    print(json.dumps(enriched.get("chain_summary", []), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
