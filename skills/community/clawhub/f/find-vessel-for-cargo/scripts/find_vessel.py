from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date
from typing import Any

try:
    from .common import haversine_nm
    from .demand_sync import build_payload, sync_demand
    from .port_resolver import Port, PortResolver, infer_trade
    from .sol_tonnage import (
        get_tonnage_list,
        get_vessel_detail,
        parse_capacity_tons,
    )
except ImportError:
    from common import haversine_nm
    from demand_sync import build_payload, sync_demand
    from port_resolver import Port, PortResolver, infer_trade
    from sol_tonnage import (
        get_tonnage_list,
        get_vessel_detail,
        parse_capacity_tons,
    )


TRADE_CONFIG = {
    "domestic": {"trade_code": "A", "radius_nm": 150.0},
    "international": {"trade_code": "B", "radius_nm": 300.0},
}


def parse_loading_date(raw: str) -> date:
    value = (raw or "").strip()
    patterns = (
        r"^(\d{4})-(\d{1,2})-(\d{1,2})$",
        r"^(\d{4})[年/.](\d{1,2})[月/.](\d{1,2})日?$",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, value)
        if match:
            try:
                return date(*(int(part) for part in match.groups()))
            except ValueError as exc:
                raise ValueError(f"预计装货日期无效: {raw}") from exc
    raise ValueError("预计装货日期必须包含完整年月日")


def parse_open_date(raw: str, loading_date: date) -> dict[str, Any]:
    value = (raw or "").strip()
    if not value:
        return {"status": "manual_confirmation", "date": None, "delta_days": None}
    full = re.search(
        r"(?<!\d)(\d{4})\s*[年./-]\s*(\d{1,2})\s*[月./-]\s*"
        r"(\d{1,2})\s*日?",
        value,
    )
    if full:
        try:
            parsed = date(*(int(part) for part in full.groups()))
        except ValueError:
            return {
                "status": "manual_confirmation",
                "date": None,
                "delta_days": None,
            }
    else:
        partial = re.search(
            r"(?<!\d)(\d{1,2})\s*(?:月|[./-])\s*(\d{1,2})\s*日?",
            value,
        )
        month_number: int | None = None
        day_number: int | None = None
        if partial:
            month_number, day_number = (int(part) for part in partial.groups())
        else:
            english_months = {
                "jan": 1, "feb": 2, "mar": 3, "apr": 4,
                "may": 5, "jun": 6, "jul": 7, "aug": 8,
                "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
            }
            english = re.search(
                r"(?<!\d)(\d{1,2})(?:st|nd|rd|th)?\s*[,./ -]\s*"
                r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\b",
                value,
                re.I,
            )
            if english:
                day_number = int(english.group(1))
                month_number = english_months[english.group(2).casefold()]
        if month_number is None or day_number is None:
            return {
                "status": "manual_confirmation",
                "date": None,
                "delta_days": None,
            }
        candidates = []
        for year in (
            loading_date.year - 1,
            loading_date.year,
            loading_date.year + 1,
        ):
            try:
                candidate = date(year, month_number, day_number)
            except ValueError:
                continue
            candidates.append(candidate)
        if not candidates:
            return {
                "status": "manual_confirmation",
                "date": None,
                "delta_days": None,
            }
        parsed = min(
            candidates,
            key=lambda candidate: (
                abs((candidate - loading_date).days),
                candidate < loading_date,
            ),
        )
    delta_days = (parsed - loading_date).days
    return {
        "status": "parsed",
        "date": parsed.isoformat(),
        "delta_days": delta_days,
    }


def build_detail_action(
    solid: str,
    public_base_url: str | None = None,
) -> dict[str, str]:
    path = f"/vessel/{solid}/view"
    api_path = f"/vessel/{solid}"
    base_url = (
        public_base_url
        if public_base_url is not None
        else os.getenv("VESSEL_MATCHER_PUBLIC_URL", "http://127.0.0.1:8766")
    ).rstrip("/")
    return {
        "type": "open_internal_detail",
        "label": "查看详情",
        "method": "GET",
        "path": path,
        "url": f"{base_url}{path}",
        "api_path": api_path,
    }


def _nearest_distance(
    origin: Port,
    candidates: list[Port],
) -> tuple[float, Port] | None:
    if not candidates:
        return None
    ranked = [
        (
            haversine_nm(
                origin.latitude,
                origin.longitude,
                candidate.latitude,
                candidate.longitude,
            ),
            candidate,
        )
        for candidate in candidates
    ]
    return min(ranked, key=lambda item: item[0])


def search_vessels(
    load_port: str,
    discharge_port: str,
    cargo_name: str,
    cargo_tons: float,
    loading_date: str,
    user_id: str = "",
    limit: int = 10,
    force_refresh: bool = False,
    sync_demand_record: bool = True,
) -> dict[str, Any]:
    if cargo_tons <= 0:
        raise ValueError("cargo_tons 必须大于0")
    if not str(cargo_name).strip():
        raise ValueError("cargo_name 不能为空")
    if limit < 1 or limit > 100:
        raise ValueError("limit 必须在1到100之间")
    expected_date = parse_loading_date(loading_date)
    resolver = PortResolver()
    load = resolver.resolve(load_port)
    discharge = resolver.resolve(discharge_port)
    trade_type = infer_trade(load, discharge)
    config = TRADE_CONFIG[trade_type]
    tonnage_payload = get_tonnage_list(
        config["trade_code"],
        force_refresh=force_refresh,
    )
    stats = {
        "source_records": len(tonnage_payload["records"]),
        "distance_excluded_records": 0,
        "capacity_excluded_records": 0,
        "date_excluded_records": 0,
        "manual_confirmation_records": 0,
        "matched_records": 0,
    }
    matches: list[dict[str, Any]] = []
    for record in tonnage_payload["records"]:
        manual_fields: list[str] = []
        capacity = parse_capacity_tons(record["capacity_raw"])
        if capacity["status"] == "parsed":
            if capacity["max_tons"] < cargo_tons:
                stats["capacity_excluded_records"] += 1
                continue
        else:
            manual_fields.append("capacity")

        date_result = parse_open_date(record["open_date_raw"], expected_date)
        if date_result["status"] == "parsed":
            if not -7 <= date_result["delta_days"] <= 15:
                stats["date_excluded_records"] += 1
                continue
        else:
            manual_fields.append("open_date")

        open_ports = resolver.resolve_field(record["open_port_raw"])
        nearest = _nearest_distance(load, open_ports)
        if nearest:
            distance, resolved_open_port = nearest
            if distance > config["radius_nm"]:
                stats["distance_excluded_records"] += 1
                continue
            resolved_port_payload = resolved_open_port.to_dict()
            distance_payload: float | None = round(distance, 1)
        else:
            manual_fields.append("open_port")
            resolved_port_payload = None
            distance_payload = None

        if manual_fields:
            stats["manual_confirmation_records"] += 1
        action = build_detail_action(record["solid"])
        matches.append(
            {
                **record,
                "detail_path": action["path"],
                "detail_url": action["url"],
                "detail_action": action,
                "capacity_status": capacity["status"],
                "capacity_min_tons": capacity.get("min_tons"),
                "capacity_max_tons": capacity.get("max_tons"),
                "resolved_open_port": resolved_port_payload,
                "open_port_to_load_nm": distance_payload,
                "open_date_status": date_result["status"],
                "resolved_open_date": date_result["date"],
                "days_from_loading_date": date_result["delta_days"],
                "capacity_surplus_tons": (
                    round(capacity["max_tons"] - cargo_tons, 2)
                    if capacity["status"] == "parsed"
                    else None
                ),
                "manual_confirmation_fields": manual_fields,
            }
        )

    infinity = float("inf")
    matches.sort(
        key=lambda item: (
            len(item["manual_confirmation_fields"]),
            item["open_port_to_load_nm"]
            if item["open_port_to_load_nm"] is not None
            else infinity,
            abs(item["days_from_loading_date"])
            if item["days_from_loading_date"] is not None
            else infinity,
            item["capacity_surplus_tons"]
            if item["capacity_surplus_tons"] is not None
            else infinity,
            item["vessel_id"],
        )
    )
    stats["matched_records"] = len(matches)
    selected = matches[:limit]

    if not sync_demand_record:
        demand_sync = {"status": "disabled_for_validation", "queued": False}
    elif not str(user_id).strip():
        demand_sync = {"status": "disabled_without_user_id", "queued": False}
    else:
        demand_sync = sync_demand(
            build_payload(
                user_id=user_id,
                load_port=load_port,
                discharge_port=discharge_port,
                cargo_name=cargo_name,
                cargo_tons=cargo_tons,
                loading_date=expected_date.isoformat(),
                trade_type=trade_type,
            )
        )
    return {
        "trade_type": trade_type,
        "trade_code": config["trade_code"],
        "radius_nm": config["radius_nm"],
        "load_port": load.to_dict(),
        "discharge_port": discharge.to_dict(),
        "cargo_name": cargo_name,
        "cargo_tons": cargo_tons,
        "loading_date": expected_date.isoformat(),
        "date_window": {
            "earliest_days": -7,
            "latest_days": 15,
            "inclusive": True,
        },
        "result_count": len(selected),
        "total_matched_count": len(matches),
        "results": selected,
        "source": {
            "fetched_at": tonnage_payload.get("fetched_at"),
            "cache_status": tonnage_payload.get("cache_status"),
            "record_count": tonnage_payload.get("record_count"),
        },
        "coverage": stats,
        "demand_sync": demand_sync,
    }


def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="货主按港口、货量和日期匹配空船")
    subparsers = parser.add_subparsers(dest="command", required=True)
    search = subparsers.add_parser("search", help="匹配空船")
    search.add_argument("--load-port", required=True)
    search.add_argument("--discharge-port", required=True)
    search.add_argument("--cargo-name", required=True)
    search.add_argument("--cargo-tons", type=float, required=True)
    search.add_argument("--loading-date", required=True)
    search.add_argument("--user-id", default="")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--force-refresh", action="store_true")
    search.add_argument("--skip-demand-sync", action="store_true")
    detail = subparsers.add_parser("detail", help="获取空船详情")
    detail.add_argument("--solid", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "search":
            _print_json(
                search_vessels(
                    load_port=args.load_port,
                    discharge_port=args.discharge_port,
                    cargo_name=args.cargo_name,
                    cargo_tons=args.cargo_tons,
                    loading_date=args.loading_date,
                    user_id=args.user_id,
                    limit=args.limit,
                    force_refresh=args.force_refresh,
                    sync_demand_record=not args.skip_demand_sync,
                )
            )
        else:
            _print_json(get_vessel_detail(args.solid))
        return 0
    except Exception as exc:
        _print_json({"error": str(exc), "type": type(exc).__name__})
        return 1


if __name__ == "__main__":
    sys.exit(main())
