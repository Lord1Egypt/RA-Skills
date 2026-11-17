from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from typing import Any

try:
    from .demand_sync import build_payload, sync_demand
    from .sol_purchases import get_purchase_detail, get_purchase_list
except ImportError:
    from demand_sync import build_payload, sync_demand
    from sol_purchases import get_purchase_detail, get_purchase_list


BASE_WEIGHTS = {"vessel_type": 35.0, "capacity": 35.0, "age": 25.0, "flag": 5.0}
TYPE_GROUPS = {
    "bulk": {"散货船", "干散货船", "运砂船", "水泥船", "木材船"},
    "tanker": {"油船", "成品油船", "原油船", "化学品船", "沥青船"},
    "gas": {"液化气船", "lng船", "lpg船"},
    "general_cargo": {"杂货船", "多用途船"},
    "barge": {"驳船", "甲板驳船", "自航甲板驳"},
    "ro_ro": {"滚装船", "滚装货船", "滚装客船"},
    "passenger": {"客轮", "交通艇", "游艇", "登陆艇", "救生艇"},
    "engineering": {"工程船", "挖泥船", "浮吊", "浮船坞", "特种船"},
    "fishing": {"渔船", "金枪鱼船"},
    "container": {"集装箱船"},
    "tug": {"拖轮"},
    "reefer": {"冷藏船"},
    "scrap": {"废钢船"},
}
SOURCE_TYPES = {
    "集装箱船", "散货船", "杂货船", "多用途船", "水泥船", "油船",
    "工程船", "木材船", "特种船", "冷藏船", "化学品船", "液化气船",
    "运砂船", "沥青船", "挖泥船", "拖轮", "驳船", "甲板驳船",
    "客轮", "滚装客船", "滚装货船", "交通艇", "游艇", "废钢船",
    "浮吊", "浮船坞", "金枪鱼船", "渔船", "救生艇",
}
UNIT_PATTERNS = (
    ("DWT", r"(?:dwt|dwcc|载重吨|吨\b)"),
    ("TEU", r"(?:teu|标箱|箱量)"),
    ("BHP", r"(?:bhp|马力)"),
    ("GRT", r"(?:grt|gt\b|总吨)"),
    ("CBM", r"(?:cbm|m3|m³|立方米|方\b)"),
    ("PAX", r"(?:pax|乘员|客位|人\b)"),
)


def _normalize_type(value: str) -> str:
    return re.sub(r"[\s（）()\-_/]", "", (value or "").casefold())


def _type_group(value: str) -> str | None:
    normalized = _normalize_type(value)
    for group, labels in TYPE_GROUPS.items():
        if any(_normalize_type(label) == normalized for label in labels):
            return group
    return None


def vessel_type_score(query: str, candidate: str) -> float | None:
    query_name = _normalize_type(query)
    candidate_name = _normalize_type(candidate)
    if not query_name or not candidate_name or candidate_name == _normalize_type("其他船"):
        return None
    if query_name == candidate_name:
        return 35.0
    query_group = _type_group(query)
    if query_group and query_group == _type_group(candidate):
        return 28.0
    return None


def _source_types(query: str) -> list[str]:
    group = _type_group(query)
    if group:
        values = sorted(TYPE_GROUPS[group] & SOURCE_TYPES)
        if values:
            return values
    return [query] if query in SOURCE_TYPES else []


def parse_capacity(raw: str, default_unit: str = "DWT") -> dict[str, Any]:
    value = (raw or "").strip().casefold().replace(",", "").replace("，", "")
    value = value.replace("～", "-").replace("—", "-").replace("–", "-")
    unit = default_unit.upper()
    for code, pattern in UNIT_PATTERNS:
        if re.search(pattern, value, re.I):
            unit = code
            break
    numbers = re.findall(r"\d+(?:\.\d+)?", value)
    if not numbers:
        return {"status": "manual_confirmation", "min": None, "max": None, "unit": unit}
    scale = 10000 if "万" in value else (1000 if re.search(r"\bk\b", value) else 1)
    amounts = [float(number) * scale for number in numbers[:2]]
    return {"status": "parsed", "min": min(amounts), "max": max(amounts), "unit": unit}


def parse_seller_age(raw: str) -> dict[str, Any]:
    value = (raw or "").strip().casefold()
    current_year = date.today().year
    if value in {"新船", "new", "newbuilding"}:
        return {"age": 0, "build_year": current_year, "is_new_ship": True}
    year_match = re.search(r"(?:18|19|20)\d{2}", value)
    if year_match:
        build_year = int(year_match.group(0))
        if build_year > current_year + 1:
            raise ValueError("建造年份不能晚于下一年")
        age = max(0, current_year - build_year)
        return {"age": age, "build_year": build_year, "is_new_ship": age == 0}
    number_match = re.search(r"\d+", value)
    if not number_match:
        raise ValueError("船龄必须是实际年数、建造年份或新船")
    age = int(number_match.group(0))
    return {"age": age, "build_year": current_year - age, "is_new_ship": age == 0}


def parse_buyer_age(raw: str) -> dict[str, Any]:
    value = (raw or "").strip().casefold().replace("～", "-").replace("—", "-").replace("–", "-")
    if not value or re.search(r"(不限|不限制|任意|any)", value):
        return {"status": "unrestricted", "min": None, "max": None}
    if value in {"新船", "new", "newbuilding"}:
        return {"status": "parsed", "min": 0, "max": 0}
    numbers = [int(number) for number in re.findall(r"\d+", value)]
    if not numbers:
        return {"status": "manual_confirmation", "min": None, "max": None}
    if len(numbers) >= 2:
        return {"status": "parsed", "min": min(numbers[:2]), "max": max(numbers[:2])}
    if re.search(r"(以上|不少于|至少)", value):
        return {"status": "parsed", "min": numbers[0], "max": math.inf}
    if re.search(r"(以内|以下|不超过|最大|至多)", value):
        return {"status": "parsed", "min": 0, "max": numbers[0]}
    return {"status": "parsed", "min": numbers[0], "max": numbers[0]}


def _capacity_score(seller: dict[str, Any], demand: dict[str, Any]) -> tuple[float, float] | None:
    if demand["status"] != "parsed" or demand["unit"] != seller["unit"]:
        return None
    seller_value = (seller["min"] + seller["max"]) / 2
    if demand["min"] <= seller_value <= demand["max"]:
        return 35.0, 0.0
    boundary = demand["min"] if seller_value < demand["min"] else demand["max"]
    difference_ratio = abs(seller_value - boundary) / max(boundary, 1.0)
    if difference_ratio > 0.20:
        return None
    return 35.0 * (1 - difference_ratio / 0.20), difference_ratio


def _age_score(seller: dict[str, Any], demand: dict[str, Any]) -> tuple[float, float | None] | None:
    if demand["status"] == "unrestricted":
        return 25.0, 0.0
    if demand["status"] != "parsed":
        return 12.5, None
    seller_age = seller["age"]
    if seller["is_new_ship"] and not demand["min"] <= 0 <= demand["max"]:
        return None
    if demand["min"] <= seller_age <= demand["max"]:
        distance = 0.0
    else:
        distance = min(abs(seller_age - demand["min"]), abs(seller_age - demand["max"]))
    if distance > 3:
        return None
    return 25.0 * (1 - distance / 3), distance


def _normalize_flag(value: str) -> str:
    return re.sub(r"\s+", "", (value or "")).casefold().replace("中华人民共和国", "中国")


def _active_status(value: str) -> bool:
    return not bool(re.search(r"(已售|成交|关闭|下架|过期|失效|无效|撤销)", value or ""))


def _updated_sort_value(value: str) -> int:
    numbers = [int(part) for part in re.findall(r"\d+", value or "")[:3]]
    if len(numbers) != 3:
        return 0
    year, month, day = numbers
    if year < 100:
        year += 2000
    try:
        return date(year, month, day).toordinal()
    except ValueError:
        return 0


def _detail_action(solid: str) -> dict[str, str]:
    path = f"/purchase/{solid}/view"
    base = os.getenv("SELLER_BUYER_PUBLIC_URL", "http://127.0.0.1:8768").rstrip("/")
    return {
        "type": "open_internal_detail",
        "label": "查看详情",
        "method": "GET",
        "path": path,
        "url": base + path,
        "api_path": f"/purchase/{solid}",
    }


def search_buyers(
    vessel_type: str,
    capacity: str,
    age: str,
    flag: str = "",
    trade_scope: str = "",
    user_id: str = "",
    limit: int = 10,
    force_refresh: bool = False,
    sync_demand_record: bool = True,
) -> dict[str, Any]:
    if not vessel_type.strip() or _normalize_type(vessel_type) == _normalize_type("其他船"):
        raise ValueError("必须提供可识别的具体船型")
    seller_capacity = parse_capacity(capacity)
    if seller_capacity["status"] != "parsed" or seller_capacity["min"] <= 0:
        raise ValueError("载重或容量必须包含有效数值")
    seller_age = parse_seller_age(age)
    if trade_scope and trade_scope not in {"内贸", "外贸"}:
        raise ValueError("内贸/外贸只能填写内贸或外贸")
    if not 1 <= limit <= 100:
        raise ValueError("limit必须在1到100之间")

    requested_source_types = _source_types(vessel_type)
    if not requested_source_types:
        raise ValueError(f"数据源不支持船型: {vessel_type}")
    base_filters = {
        "shipflag": "",
        "dwt1": "",
        "dwt2": "",
        "dwt_dw": seller_capacity["unit"],
        "buildyear": "",
    }
    source_payloads: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=min(4, len(requested_source_types))) as executor:
        futures = {
            executor.submit(
                get_purchase_list,
                {"shiptype": source_type, **base_filters},
                force_refresh,
            ): source_type
            for source_type in requested_source_types
        }
        for future in as_completed(futures):
            source_payloads.append(future.result())

    source_records: list[dict[str, Any]] = []
    seen_solids: set[str] = set()
    for payload in source_payloads:
        for record in payload["records"]:
            if record["solid"] not in seen_solids:
                seen_solids.add(record["solid"])
                source_records.append(record)

    stats = {
        "source_records": len(source_records),
        "status_excluded": 0,
        "type_excluded": 0,
        "capacity_excluded": 0,
        "age_excluded": 0,
        "flag_excluded": 0,
        "matched_records": 0,
    }
    candidates: list[dict[str, Any]] = []
    for record in source_records:
        if not _active_status(record["status"]):
            stats["status_excluded"] += 1
            continue
        type_points = vessel_type_score(vessel_type, record["vessel_type"])
        if type_points is None:
            stats["type_excluded"] += 1
            continue
        demand_capacity = parse_capacity(record["capacity_raw"])
        capacity_result = _capacity_score(seller_capacity, demand_capacity)
        if capacity_result is None:
            stats["capacity_excluded"] += 1
            continue
        capacity_points, capacity_error = capacity_result
        demand_age = parse_buyer_age(record["age_range_raw"])
        age_result = _age_score(seller_age, demand_age)
        if age_result is None:
            stats["age_excluded"] += 1
            continue
        age_points, age_error = age_result
        manual_fields: list[str] = []
        if demand_age["status"] == "manual_confirmation":
            manual_fields.append("buyer_age")
        if flag:
            if _normalize_flag(record["flag"]) != _normalize_flag(flag):
                stats["flag_excluded"] += 1
                continue
            flag_points = 5.0
        else:
            flag_points = 0.0

        active_components = ["vessel_type", "capacity", "age"]
        if flag:
            active_components.append("flag")
        active_weight = sum(BASE_WEIGHTS[name] for name in active_components)
        total_score = round((type_points + capacity_points + age_points + flag_points) * 100 / active_weight, 1)
        action = _detail_action(record["solid"])
        clean_record = dict(record)
        if "付费" in clean_record.get("company_name", ""):
            clean_record["company_name"] = ""
        candidates.append(
            {
                **clean_record,
                "match_score": total_score,
                "score_components": {
                    "vessel_type": round(type_points, 2),
                    "capacity": round(capacity_points, 2),
                    "age": round(age_points, 2),
                    "flag": round(flag_points, 2) if flag else None,
                },
                "demand_capacity_min": demand_capacity["min"],
                "demand_capacity_max": demand_capacity["max"],
                "capacity_unit": demand_capacity["unit"],
                "capacity_error_percent": round(capacity_error * 100, 2),
                "demand_age_min": demand_age["min"],
                "demand_age_max": None if demand_age["max"] == math.inf else demand_age["max"],
                "age_requirement_status": demand_age["status"],
                "age_error_years": None if age_error is None else int(age_error),
                "manual_confirmation_fields": manual_fields,
                "detail_url": action["url"],
                "detail_action": action,
            }
        )

    candidates.sort(
        key=lambda item: (
            -item["match_score"],
            item["capacity_error_percent"],
            item["age_error_years"] if item["age_error_years"] is not None else math.inf,
            -_updated_sort_value(item["updated_date"]),
            item["purchase_id"],
        )
    )
    stats["matched_records"] = len(candidates)
    selected = candidates[:limit]
    if selected:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(get_purchase_detail, item["solid"], force_refresh): item
                for item in selected
            }
            for future in as_completed(futures):
                item = futures[future]
                try:
                    detail = future.result()
                except Exception as exc:
                    item["detail_warning"] = str(exc)
                    continue
                detail_company = detail.get("company_name", "")
                if detail_company and "付费" not in detail_company:
                    item["company_name"] = re.sub(r"\s*\[.*$", "", detail_company).strip()

    if not sync_demand_record:
        demand_sync = {"status": "disabled_for_validation", "queued": False}
    elif not user_id.strip():
        demand_sync = {"status": "disabled_without_user_id", "queued": False}
    else:
        demand_sync = sync_demand(
            build_payload(
                user_id=user_id,
                vessel_type=vessel_type,
                capacity=capacity,
                age=age,
                flag=flag,
                trade_scope=trade_scope,
            )
        )
    return {
        "query": {
            "vessel_type": vessel_type,
            "capacity": seller_capacity,
            "age": seller_age,
            "flag": flag or None,
            "trade_scope": trade_scope or None,
            "trade_scope_used_for_matching": False,
        },
        "scoring_weights": BASE_WEIGHTS,
        "result_count": len(selected),
        "total_matched_count": len(candidates),
        "results": selected,
        "source": {
            "fetched_at": max((payload.get("fetched_at", "") for payload in source_payloads), default=""),
            "cache_status": "stale" if any(payload.get("cache_status") == "stale" for payload in source_payloads) else "fresh",
            "record_count": len(source_records),
            "page_count": sum(payload.get("page_count", 0) for payload in source_payloads),
            "truncated": any(payload.get("truncated", False) for payload in source_payloads),
            "shiptypes": requested_source_types,
        },
        "coverage": stats,
        "demand_sync": demand_sync,
    }


def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="卖家按船型、容量、船龄和可选船旗匹配求购买家")
    commands = parser.add_subparsers(dest="command", required=True)
    search = commands.add_parser("search")
    search.add_argument("--vessel-type", required=True)
    search.add_argument("--capacity", required=True)
    search.add_argument("--age", required=True)
    search.add_argument("--flag", default="")
    search.add_argument("--trade-scope", default="")
    search.add_argument("--user-id", default="")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--force-refresh", action="store_true")
    search.add_argument("--skip-demand-sync", action="store_true")
    detail = commands.add_parser("detail")
    detail.add_argument("--solid", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "search":
            _print_json(
                search_buyers(
                    vessel_type=args.vessel_type,
                    capacity=args.capacity,
                    age=args.age,
                    flag=args.flag,
                    trade_scope=args.trade_scope,
                    user_id=args.user_id,
                    limit=args.limit,
                    force_refresh=args.force_refresh,
                    sync_demand_record=not args.skip_demand_sync,
                )
            )
        else:
            _print_json(get_purchase_detail(args.solid))
        return 0
    except Exception as exc:
        _print_json({"error": str(exc), "type": type(exc).__name__})
        return 1


if __name__ == "__main__":
    sys.exit(main())
