#!/usr/bin/env python3
"""
飞书会议室批量忙闲查询工具

用法:
  python3 query_rooms.py --building "丽金" --start "2026-04-20T14:00:00+08:00" --end "2026-04-20T15:00:00+08:00"
  python3 query_rooms.py --building "F4" --start "2026-04-20T09:00:00+08:00" --end "2026-04-20T18:00:00+08:00" --capacity-gte 8
  python3 query_rooms.py --list-buildings
  python3 query_rooms.py --list-rooms --building "丽金"

输出: JSON 格式，包含每个会议室的名称、room_id、容量、忙闲状态
"""

import argparse
import json
import subprocess
import sys
import re
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
from typing import Any, Optional

SCRIPT_DIR = Path(__file__).parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import workspace_manager

MAPPING_FILE = SCRIPT_DIR.parent / "references" / "room-mapping.json"
PREFS_FILE = SCRIPT_DIR.parent / "references" / "user-preferences.json"

# 预加载索引，模块级别缓存
_mapping_cache: Optional[dict] = None
_alias_index: Optional[dict[str, int]] = None
_building_search_cache: Optional[list[dict]] = None
GENERIC_LOCATION_TOKENS = {
    "会议室", "开会", "预订", "订", "找", "查", "room", "rooms", "meeting",
    "meetingroom", "office", "near", "附近", "的", "一个", "一下",
}



def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text).lower().strip()
    normalized = re.sub(r"[（）()\[\]{}]", " ", normalized)
    normalized = normalized.replace("－", "-")
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized



def compact_text(text: str) -> str:
    normalized = normalize_text(text)
    normalized = re.sub(r"\bblock\s*([a-z0-9]+)", r"\1座", normalized)
    normalized = re.sub(r"\bbuilding\s*([a-z0-9]+)", r"\1座", normalized)
    normalized = re.sub(r"\btower\s*([a-z0-9]+)", r"\1座", normalized)
    normalized = re.sub(r"([a-z0-9])\s*座", r"\1座", normalized)
    normalized = re.sub(r"\s*[-_/]\s*", "-", normalized)
    return re.sub(r"[^\w一-鿿-]", "", normalized)



def strip_capacity_suffix(text: str) -> str:
    return re.sub(r"\(\d+\)$", "", text).strip()



def extract_tokens(text: str) -> list[str]:
    normalized = normalize_text(text)
    text_with_spaces = re.sub(r"([a-z0-9])\s*(楼|层|f|floor|座)", r"\1\2", normalized)
    chunks = re.split(r"[^\w一-鿿-]+", text_with_spaces)
    return [chunk for chunk in chunks if chunk and chunk not in GENERIC_LOCATION_TOKENS]



def infer_room_metadata(room_name: str, room_aliases: Optional[list[str]] = None) -> dict:
    aliases = room_aliases or []
    raw_terms = [room_name, strip_capacity_suffix(room_name), *aliases]
    compact_terms = {compact_text(term) for term in raw_terms if term}
    compact_terms = {term for term in compact_terms if term}

    floor_guess = None
    room_code = None
    for term in list(compact_terms):
        match = re.search(r"f?(\d{1,2})-([a-z0-9]{1,4})", term)
        if match:
            floor_guess = match.group(1)
            room_code = match.group(2)
            compact_terms.add(f"f{floor_guess}-{room_code}")
            compact_terms.add(f"{floor_guess}-{room_code}")
            break

    return {
        "floor_guess": floor_guess,
        "room_code": room_code,
        "compact_terms": compact_terms,
    }



def extract_location_hints(keyword: str) -> dict:
    compact_keyword = compact_text(keyword)
    floor_hint = None
    room_hint = None

    room_match = re.search(r"f?(\d{1,2})-([a-z0-9]{1,4})", compact_keyword)
    if room_match:
        floor_hint = room_match.group(1)
        room_code = room_match.group(2)
        room_hint = f"f{floor_hint}-{room_code}"
    else:
        floor_match = re.search(r"(\d{1,2})(?:楼|层|f|floor)", compact_keyword)
        if floor_match:
            floor_hint = floor_match.group(1)

        booth_match = re.search(r"([a-z0-9])(?:discussionbooth|booth)", compact_keyword)
        if booth_match:
            room_hint = f"{booth_match.group(1)}discussionbooth"

    building_query = compact_keyword
    if room_hint:
        building_query = building_query.replace(room_hint, "")
        room_code = room_hint.split("-", 1)[1] if "-" in room_hint else ""
        if room_code:
            building_query = building_query.replace(room_code, "")
    if floor_hint:
        building_query = re.sub(rf"f?{floor_hint}(?:楼|层|f|floor)?", "", building_query)
    building_query = building_query.replace("discussionbooth", "")

    tokens = []
    for token in extract_tokens(keyword):
        compact_token = compact_text(token)
        if not compact_token:
            continue
        if floor_hint and compact_token in {floor_hint, f"f{floor_hint}", f"{floor_hint}楼", f"{floor_hint}层"}:
            continue
        if room_hint and compact_token in {room_hint, room_hint.replace("f", "", 1)}:
            continue
        tokens.append(compact_token)

    if building_query:
        tokens.append(building_query)

    unique_tokens = []
    seen = set()
    for token in tokens:
        if not token or token in seen:
            continue
        seen.add(token)
        unique_tokens.append(token)

    return {
        "normalized": normalize_text(keyword),
        "compact": compact_keyword,
        "tokens": unique_tokens,
        "floor_hint": floor_hint,
        "room_hint": room_hint,
        "building_query": building_query,
    }



def _load_mapping():
    global _mapping_cache, _alias_index, _building_search_cache
    if _mapping_cache is not None:
        return _mapping_cache, _alias_index, _building_search_cache

    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        _mapping_cache = json.load(f)

    _alias_index = {}
    _building_search_cache = []
    for i, building in enumerate(_mapping_cache.get("buildings", [])):
        searchable_aliases = [building["name"], *building.get("alias", [])]
        for alias in searchable_aliases:
            key = alias.lower()
            if key not in _alias_index:
                _alias_index[key] = i

        room_entries = []
        for room in building.get("rooms", []):
            metadata = infer_room_metadata(room["name"], room.get("alias", []))
            room_entries.append({
                "room": room,
                "metadata": metadata,
            })

        _building_search_cache.append({
            "index": i,
            "building": building,
            "aliases": searchable_aliases,
            "alias_compacts": [compact_text(alias) for alias in searchable_aliases if alias],
            "alias_tokens": extract_tokens(" ".join(searchable_aliases)),
            "room_entries": room_entries,
        })

    return _mapping_cache, _alias_index, _building_search_cache



def resolve_location_query(keyword: str) -> dict:
    data, _, search_entries = _load_mapping()
    buildings = data.get("buildings", [])
    hints = extract_location_hints(keyword)
    ranked_matches = []
    minimum_score = 40 if hints["building_query"] else 20

    for entry in search_entries:
        score = 0
        alias_compacts = entry["alias_compacts"]
        building_query = hints["building_query"]
        matched_room_terms = False
        matched_floor = False

        if hints["compact"] in alias_compacts:
            score += 100
        elif building_query and building_query in alias_compacts:
            score += 95
        elif building_query and any(building_query in alias for alias in alias_compacts):
            score += 75
        elif building_query and any(alias and len(alias) >= 4 and alias in building_query for alias in alias_compacts):
            score += 75
        elif any(hints["compact"] and hints["compact"] in alias for alias in alias_compacts):
            score += 60

        token_score = 0
        for token_compact in hints["tokens"]:
            if any(token_compact in alias for alias in alias_compacts):
                token_score += 12
        score += token_score

        for room_entry in entry["room_entries"]:
            metadata = room_entry["metadata"]
            if hints["room_hint"] and hints["room_hint"] in metadata["compact_terms"]:
                matched_room_terms = True
                score += 80
            if hints["floor_hint"] and metadata["floor_guess"] == hints["floor_hint"]:
                matched_floor = True

        if matched_floor:
            score += 20
        if matched_room_terms and matched_floor:
            score += 20

        if score >= minimum_score:
            ranked_matches.append((score, entry["index"]))

    ranked_matches.sort(key=lambda item: (-item[0], item[1]))
    matched_indices = [index for _, index in ranked_matches]
    if not matched_indices:
        return {
            "matched_buildings": [],
            "room_filter": {"floor_hint": hints["floor_hint"], "room_hint": hints["room_hint"]},
        }

    return {
        "matched_buildings": [buildings[index] for index in matched_indices],
        "room_filter": {"floor_hint": hints["floor_hint"], "room_hint": hints["room_hint"]},
    }



def match_building(keyword: str) -> list[dict]:
    """根据关键词匹配楼栋，支持楼层和房间号等自然语言变体。"""
    return resolve_location_query(keyword)["matched_buildings"]



def filter_rooms_by_location_hints(rooms: list[dict], room_filter: Optional[dict]) -> list[dict]:
    if not room_filter:
        return rooms

    floor_hint = room_filter.get("floor_hint")
    room_hint = room_filter.get("room_hint")
    room_matches = []
    floor_matches = []

    for room in rooms:
        metadata = infer_room_metadata(room["name"], room.get("alias", []))
        if room_hint and room_hint in metadata["compact_terms"]:
            room_matches.append(room)
        if floor_hint and metadata["floor_guess"] == floor_hint:
            floor_matches.append(room)

    if room_matches:
        if floor_hint:
            narrowed = [room for room in room_matches if infer_room_metadata(room["name"], room.get("alias", [])).get("floor_guess") == floor_hint]
            if narrowed:
                return narrowed
        return room_matches

    if floor_matches:
        return floor_matches

    return rooms


def query_freebusy(room_id: str, time_min: str, time_max: str) -> dict:
    """查询单个会议室的忙闲状态"""
    cmd = [
        "lark-cli", "calendar", "freebusys", "list", "--as", "bot",
        "--data", json.dumps({
            "room_id": room_id,
            "time_min": time_min,
            "time_max": time_max
        })
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            return {"status": "error", "busy_periods": []}
        data = json.loads(result.stdout)
        fb_list = data.get("data", {}).get("freebusy_list", [])
        return {
            "status": "busy" if fb_list else "free",
            "busy_periods": fb_list
        }
    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        return {"status": "error", "busy_periods": []}


def compute_duration_minutes(time_min: str, time_max: str) -> int:
    start_minutes = parse_minutes(time_min)
    end_minutes = parse_minutes(time_max)
    return max(end_minutes - start_minutes, 0)



def query_freebusy_parallel(rooms: list[dict], time_min: str, time_max: str,
                            max_workers: int = 10) -> list[dict]:
    """并行查询多个会议室的忙闲状态"""
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(query_freebusy, r["room_id"], time_min, time_max): r
            for r in rooms
        }
        done = 0
        total = len(rooms)
        for future in as_completed(future_map):
            room = future_map[future]
            fb = future.result()
            done += 1
            if total > 20 and done % 20 == 0:
                print(f"\r  查询进度: {done}/{total}", file=sys.stderr, end="", flush=True)

            result = {
                "name": room["name"],
                "room_id": room["room_id"],
                "capacity": room["capacity"],
                "building": room["building"],
                "status": fb["status"],
            }
            if fb["status"] == "free":
                result["free_slots"] = [{
                    "start": time_min,
                    "end": time_max,
                    "duration_min": compute_duration_minutes(time_min, time_max),
                }]
            elif fb["status"] == "busy":
                result["free_slots"] = compute_free_slots(fb["busy_periods"], time_min, time_max)
            else:
                result["free_slots"] = []
            results.append(result)

    if total > 20:
        print(file=sys.stderr, flush=True)
    return results


def parse_minutes(value: str) -> int:
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})", value)
    if match:
        return int(match.group(4)) * 60 + int(match.group(5))
    return 0



def compute_free_slots(busy_periods: list[dict], time_min: str, time_max: str) -> list[dict]:
    """从忙碌时段计算空闲时段"""
    if not busy_periods:
        return [{
            "start": time_min,
            "end": time_max,
            "duration_min": compute_duration_minutes(time_min, time_max),
        }]

    gaps = []
    sorted_busy = sorted(busy_periods, key=lambda x: x["start_time"])
    last_end = time_min

    for period in sorted_busy:
        if period["start_time"] > last_end:
            duration = parse_minutes(period["start_time"]) - parse_minutes(last_end)
            gaps.append({
                "start": last_end,
                "end": period["start_time"],
                "duration_min": duration
            })
        last_end = max(last_end, period["end_time"])

    if last_end < time_max:
        duration = parse_minutes(time_max) - parse_minutes(last_end)
        gaps.append({
            "start": last_end,
            "end": time_max,
            "duration_min": duration
        })

    return sorted(gaps, key=lambda x: -x["duration_min"])


def load_preferences(filepath: Optional[Path] = None) -> dict[str, Any]:
    resolved_path = filepath or PREFS_FILE
    if not resolved_path.exists():
        return {"preferences": {}}
    with open(resolved_path, "r", encoding="utf-8") as file:
        return json.load(file)


def parse_target_date(value: Optional[str]) -> str:
    if not value:
        return date.today().isoformat()
    return value[:10]


def get_default_building_for_user(user_id: Optional[str], target_date: Optional[str] = None) -> str:
    if not user_id:
        return ""

    preferences = load_preferences().get("preferences", {})
    user_preferences = preferences.get(user_id, {})
    default_building = user_preferences.get("default_building", "")
    if isinstance(default_building, str) and default_building:
        return default_building

    workspace_data = workspace_manager.load_workspace()
    resolved_workspace = workspace_manager.resolve_workspace_for_date(
        workspace_data,
        target_date or date.today().isoformat(),
    )
    return resolved_workspace or ""


def resolve_requested_building(building: Optional[str], user_id: Optional[str], target_date: Optional[str] = None) -> str:
    if building:
        return building
    return get_default_building_for_user(user_id, target_date)


def main() -> None:
    parser = argparse.ArgumentParser(description="飞书会议室忙闲查询")
    parser.add_argument("--building", "-b", help="楼栋关键词（模糊匹配）")
    parser.add_argument("--user", "-u", help="用户 open_id；未指定楼栋时用于读取偏好或工区")
    parser.add_argument("--start", "-s", help="查询开始时间 (ISO 8601)")
    parser.add_argument("--end", "-e", help="查询结束时间 (ISO 8601)")
    parser.add_argument("--capacity-gte", "-c", type=int, default=0, help="最小容量筛选")
    parser.add_argument("--capacity-lte", type=int, default=999, help="最大容量筛选")
    parser.add_argument("--list-buildings", action="store_true", help="列出所有楼栋")
    parser.add_argument("--list-rooms", action="store_true", help="列出指定楼栋的会议室")
    parser.add_argument("--output", "-o", choices=["json", "table"], default="json", help="输出格式")
    parser.add_argument("--max-workers", "-w", type=int, default=10,
                        help="并行查询线程数 (默认 10)")

    args = parser.parse_args()
    data, _, _ = _load_mapping()

    if args.list_buildings:
        for b in data.get("buildings", []):
            rooms_count = len(b.get("rooms", []))
            aliases = ", ".join(b.get("alias", []))
            print(f"📍 {b['name']}  ({rooms_count}个会议室)  别名: {aliases}")
        return

    resolved_target_date = parse_target_date(args.start)
    resolved_building = resolve_requested_building(args.building, args.user, resolved_target_date)

    if args.list_rooms:
        if not resolved_building:
            print("错误: --list-rooms 需要指定 --building，或通过 --user 提供可用的偏好/工区默认值", file=sys.stderr)
            sys.exit(1)
        location_match = resolve_location_query(resolved_building)
        matched = location_match["matched_buildings"]
        if not matched:
            print(f"未找到匹配的楼栋: {resolved_building}", file=sys.stderr)
            sys.exit(1)
        for b in matched:
            print(f"\n🏢 {b['name']}:")
            rooms = filter_rooms_by_location_hints(b.get("rooms", []), location_match["room_filter"])
            for r in rooms:
                print(f"  {r['name']}  容量:{r['capacity']}  room_id:{r['room_id']}")
        return

    if not resolved_building:
        print("错误: 必须指定 --building，或通过 --user 提供可用的偏好/工区默认值", file=sys.stderr)
        sys.exit(1)
    if not args.start or not args.end:
        print("错误: 必须同时指定 --start 和 --end", file=sys.stderr)
        sys.exit(1)

    location_match = resolve_location_query(resolved_building)
    matched = location_match["matched_buildings"]
    if not matched:
        print(f"未找到匹配的楼栋: {resolved_building}", file=sys.stderr)
        print("\n可用楼栋:", file=sys.stderr)
        for b in data.get("buildings", []):
            print(f"  - {b['name']}", file=sys.stderr)
        sys.exit(1)

    all_rooms = []
    for b in matched:
        rooms = filter_rooms_by_location_hints(b.get("rooms", []), location_match["room_filter"])
        for r in rooms:
            cap = r.get("capacity", 0)
            if args.capacity_gte <= cap <= args.capacity_lte:
                all_rooms.append({
                    "name": r["name"],
                    "room_id": r["room_id"],
                    "capacity": cap,
                    "building": b["name"]
                })

    if not all_rooms:
        print(f"没有符合条件的会议室 (容量 >= {args.capacity_gte}, <= {args.capacity_lte})")
        sys.exit(0)

    room_count = len(all_rooms)
    if room_count > 20:
        print(f"🔍 正在查询 {room_count} 个会议室...", file=sys.stderr)

    results = query_freebusy_parallel(
        all_rooms, args.start, args.end, max_workers=args.max_workers
    )

    free_rooms = [r for r in results if r["status"] == "free"]
    busy_rooms = [r for r in results if r["status"] != "free"]
    free_rooms.sort(key=lambda x: -x["capacity"])
    busy_rooms.sort(key=lambda x: x["name"])
    results = free_rooms + busy_rooms

    if args.output == "table":
        isatty = sys.stdout.isatty()
        print(f"\n{'会议室':<35} {'容量':>4}  {'状态':<6}  空闲时段")
        print("-" * 80)
        for r in results:
            if isatty:
                icon = "🟢" if r["status"] == "free" else ("🔴" if r["status"] == "busy" else "⚠️")
                name_col = f"{icon} {r['name']}"
            else:
                name_col = r["name"]
            slots_str = ", ".join(
                [f"{s['start'][11:16]}-{s['end'][11:16]}" for s in r["free_slots"]]
            ) if r["free_slots"] else "-"
            print(f"{name_col:<35} {r['capacity']:>4}人  {r['status']:<6}  {slots_str}")
        free_count = len(free_rooms)
        total = len(results)
        print(f"\n共 {total} 个会议室，{free_count} 个空闲")
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()