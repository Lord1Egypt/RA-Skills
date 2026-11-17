from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

try:
    from .common import haversine_nm
    from .demand_sync import build_payload, sync_demand
    from .port_resolver import Port, PortResolver, build_catalog
    from .sol_cargo import get_cargo_detail, get_cargo_list, parse_quantity_tons
except ImportError:
    from common import haversine_nm
    from demand_sync import build_payload, sync_demand
    from port_resolver import Port, PortResolver, build_catalog
    from sol_cargo import get_cargo_detail, get_cargo_list, parse_quantity_tons


TRADE_CONFIG = {
    "domestic": {"trade_code": "A", "radius_nm": 150.0},
    "international": {"trade_code": "B", "radius_nm": 300.0},
}


def build_detail_action(
    solid: str,
    public_base_url: str | None = None,
) -> dict[str, str]:
    """Build a renderer-friendly action that only targets this service."""
    path = f"/cargo/{solid}/view"
    api_path = f"/cargo/{solid}"
    base_url = (
        public_base_url
        if public_base_url is not None
        else os.getenv("CARGO_MATCHER_PUBLIC_URL", "http://127.0.0.1:8765")
    ).rstrip("/")
    return {
        "type": "open_internal_detail",
        "label": "查看详情",
        "method": "GET",
        "path": path,
        "url": f"{base_url}{path}",
        "api_path": api_path,
    }


def infer_trade(current: Port, destination: Port) -> str:
    return (
        "domestic"
        if current.country == "CN" and destination.country == "CN"
        else "international"
    )


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


def search_cargo(
    current_port: str,
    destination_port: str,
    capacity_tons: float,
    user_id: str,
    limit: int = 10,
    force_refresh: bool = False,
    sync_demand_record: bool = True,
) -> dict[str, Any]:
    if capacity_tons <= 0:
        raise ValueError("capacity_tons 必须大于 0")
    if not str(user_id).strip():
        raise ValueError("user_id 不能为空")
    if limit < 1 or limit > 100:
        raise ValueError("limit 必须在 1 到 100 之间")

    resolver = PortResolver()
    current = resolver.resolve(current_port)
    destination = resolver.resolve(destination_port)
    trade_type = infer_trade(current, destination)
    config = TRADE_CONFIG[trade_type]
    cargo_payload = get_cargo_list(
        config["trade_code"],
        force_refresh=force_refresh,
    )

    stats = {
        "source_records": len(cargo_payload["records"]),
        "unresolved_endpoint_records": 0,
        "distance_excluded_records": 0,
        "capacity_excluded_records": 0,
        "matched_records": 0,
    }
    matches: list[dict[str, Any]] = []

    for record in cargo_payload["records"]:
        load_candidates = resolver.resolve_field(record["load_port_raw"])
        discharge_candidates = resolver.resolve_field(record["discharge_port_raw"])
        nearest_load = _nearest_distance(current, load_candidates)
        nearest_discharge = _nearest_distance(destination, discharge_candidates)
        if not nearest_load or not nearest_discharge:
            stats["unresolved_endpoint_records"] += 1
            continue
        load_distance, resolved_load = nearest_load
        discharge_distance, resolved_discharge = nearest_discharge
        if (
            load_distance > config["radius_nm"]
            or discharge_distance > config["radius_nm"]
        ):
            stats["distance_excluded_records"] += 1
            continue

        quantity = parse_quantity_tons(record["quantity_raw"])
        if (
            quantity["status"] == "parsed"
            and quantity["min_tons"] is not None
            and quantity["min_tons"] > capacity_tons
        ):
            stats["capacity_excluded_records"] += 1
            continue

        detail_action = build_detail_action(record["solid"])
        result = {
            **record,
            "detail_path": detail_action["path"],
            "detail_url": detail_action["url"],
            "detail_action": detail_action,
            "quantity_status": quantity["status"],
            "quantity_min_tons": quantity.get("min_tons"),
            "quantity_max_tons": quantity.get("max_tons"),
            "resolved_load_port": resolved_load.to_dict(),
            "resolved_discharge_port": resolved_discharge.to_dict(),
            "current_to_load_nm": round(load_distance, 1),
            "discharge_to_destination_nm": round(discharge_distance, 1),
            "total_deviation_nm": round(load_distance + discharge_distance, 1),
        }
        matches.append(result)

    matches.sort(
        key=lambda item: (
            item["quantity_status"] != "parsed",
            item["total_deviation_nm"],
            item["cargo_id"],
        )
    )
    stats["matched_records"] = len(matches)
    selected = matches[:limit]

    if sync_demand_record:
        demand_payload = build_payload(
            user_id=user_id,
            current_port=current_port,
            destination_port=destination_port,
            capacity_tons=capacity_tons,
            trade_type=trade_type,
        )
        demand_sync = sync_demand(demand_payload)
    else:
        demand_sync = {"status": "disabled_for_validation", "queued": False}

    return {
        "trade_type": trade_type,
        "trade_code": config["trade_code"],
        "radius_nm": config["radius_nm"],
        "current_port": current.to_dict(),
        "destination_port": destination.to_dict(),
        "capacity_tons": capacity_tons,
        "result_count": len(selected),
        "total_matched_count": len(matches),
        "results": selected,
        "source": {
            "fetched_at": cargo_payload.get("fetched_at"),
            "cache_status": cargo_payload.get("cache_status"),
            "record_count": cargo_payload.get("record_count"),
        },
        "coverage": stats,
        "demand_sync": demand_sync,
    }


def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="船东按港口和吨位匹配货盘")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="匹配货盘")
    search.add_argument("--current-port", required=True)
    search.add_argument("--destination-port", required=True)
    search.add_argument("--capacity-tons", type=float, required=True)
    search.add_argument("--user-id", required=True)
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--force-refresh", action="store_true")

    detail = subparsers.add_parser("detail", help="获取货盘详情")
    detail.add_argument("--solid", required=True)

    refresh_ports = subparsers.add_parser(
        "refresh-ports",
        help="刷新 UN/LOCODE 港口目录",
    )
    refresh_ports.add_argument("--force", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "search":
            _print_json(
                search_cargo(
                    current_port=args.current_port,
                    destination_port=args.destination_port,
                    capacity_tons=args.capacity_tons,
                    user_id=args.user_id,
                    limit=args.limit,
                    force_refresh=args.force_refresh,
                )
            )
        elif args.command == "detail":
            _print_json(get_cargo_detail(args.solid))
        elif args.command == "refresh-ports":
            ports = build_catalog(force_refresh=args.force)
            _print_json({"status": "ok", "port_count": len(ports)})
        return 0
    except Exception as exc:
        _print_json({"error": str(exc), "type": type(exc).__name__})
        return 1


if __name__ == "__main__":
    sys.exit(main())
