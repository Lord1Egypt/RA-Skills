#!/usr/bin/env python3
"""Initialize a Feishu tenant and import meeting-room resources from event JSON."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
REFERENCES_DIR = ROOT_DIR / "references"
PROFILE_FILE = REFERENCES_DIR / "tenant-profile.json"
BUILTIN_MAPPING_FILE = REFERENCES_DIR / "room-mapping.json"
CUSTOM_MAPPING_FILE = REFERENCES_DIR / "custom-room-mapping.json"

BYTE_COMPANY_TOKENS = {"字节", "字节跳动", "bytedance", "tiktok"}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def normalize_company(company: str) -> str:
    return re.sub(r"\s+", "", company).casefold()


def is_byte_company(company: str) -> bool:
    normalized = normalize_company(company)
    return any(token in normalized for token in BYTE_COMPANY_TOKENS)


def load_profile(profile_file: Path = PROFILE_FILE) -> dict[str, Any]:
    return load_json(profile_file, {"configured": False})


def set_company(company: str, profile_file: Path = PROFILE_FILE) -> dict[str, Any]:
    company = company.strip()
    if not company:
        raise ValueError("公司名称不能为空")
    catalog = "builtin" if is_byte_company(company) else "custom"
    profile = {
        "configured": True,
        "company": company,
        "catalog": catalog,
        "mapping_file": "references/room-mapping.json" if catalog == "builtin" else "references/custom-room-mapping.json",
    }
    save_json(profile_file, profile)
    return profile


def active_mapping_file(
    profile_file: Path | None = None,
    builtin_file: Path | None = None,
    custom_file: Path | None = None,
) -> Path | None:
    profile_file = profile_file or PROFILE_FILE
    builtin_file = builtin_file or BUILTIN_MAPPING_FILE
    custom_file = custom_file or CUSTOM_MAPPING_FILE
    profile = load_profile(profile_file)
    if not profile.get("configured"):
        return None
    return builtin_file if profile.get("catalog") == "builtin" else custom_file


def iter_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for nested in value.values():
            yield from iter_dicts(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from iter_dicts(nested)


def parse_capacity(name: str, fallback: int = 0) -> int:
    matches = re.findall(r"[（(](\d+)\s*(?:人)?[）)]", name)
    return int(matches[-1]) if matches else fallback


def extract_room_resources(payload: Any, default_capacity: int = 0) -> list[dict[str, Any]]:
    rooms: dict[str, dict[str, Any]] = {}
    for item in iter_dicts(payload):
        if item.get("type") != "resource":
            continue
        room_id = item.get("room_id")
        if not isinstance(room_id, str) or not room_id.startswith("omm_"):
            continue
        name = item.get("display_name") or item.get("name") or room_id
        rooms[room_id] = {
            "name": str(name),
            "room_id": room_id,
            "capacity": parse_capacity(str(name), int(item.get("capacity") or default_capacity)),
        }
    return sorted(rooms.values(), key=lambda room: (room["name"], room["room_id"]))


def merge_rooms(
    mapping: dict[str, Any],
    building_name: str,
    aliases: list[str],
    rooms: list[dict[str, Any]],
) -> dict[str, Any]:
    buildings = mapping.setdefault("buildings", [])
    target = next((building for building in buildings if building.get("name") == building_name), None)
    if target is None:
        target = {"name": building_name, "alias": [], "rooms": []}
        buildings.append(target)

    existing_aliases = target.setdefault("alias", [])
    for alias in aliases:
        alias = alias.strip()
        if alias and alias not in existing_aliases:
            existing_aliases.append(alias)

    room_index = {room.get("room_id"): room for room in target.setdefault("rooms", [])}
    for room in rooms:
        room_index[room["room_id"]] = room
    target["rooms"] = sorted(room_index.values(), key=lambda room: room.get("name", ""))
    buildings.sort(key=lambda building: building.get("name", ""))
    return mapping


def fetch_event_resources(calendar_id: str, event_id: str) -> Any:
    process = subprocess.run(
        [
            "lark-cli", "calendar", "event.attendees", "list",
            "--calendar-id", calendar_id,
            "--event-id", event_id,
            "--page-size", "100",
            "--page-all",
            "--as", "user",
            "--format", "json",
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if process.returncode != 0:
        message = process.stderr.strip() or process.stdout.strip() or "读取日程参与人失败"
        raise ValueError(message)
    try:
        return json.loads(process.stdout)
    except json.JSONDecodeError as error:
        raise ValueError("日程参与人接口未返回有效 JSON") from error


def import_event_payload(
    payload: Any,
    building: str,
    aliases: list[str],
    default_capacity: int = 0,
    profile_file: Path = PROFILE_FILE,
    custom_file: Path = CUSTOM_MAPPING_FILE,
) -> dict[str, Any]:
    profile = load_profile(profile_file)
    if not profile.get("configured"):
        raise ValueError("尚未完成公司配置，请先运行 --set-company")
    if profile.get("catalog") != "custom":
        raise ValueError("当前公司使用内置会议室目录，无需导入自定义会议室")
    rooms = extract_room_resources(payload, default_capacity)
    if not rooms:
        raise ValueError("未在日程数据中找到带 room_id 的 resource 参与人")
    mapping = load_json(custom_file, {"company": profile.get("company", ""), "buildings": []})
    mapping["company"] = profile.get("company", "")
    merge_rooms(mapping, building.strip(), aliases, rooms)
    save_json(custom_file, mapping)
    return {"building": building.strip(), "imported": len(rooms), "rooms": rooms}


def import_event_file(
    event_file: Path,
    building: str,
    aliases: list[str],
    default_capacity: int = 0,
    profile_file: Path = PROFILE_FILE,
    custom_file: Path = CUSTOM_MAPPING_FILE,
) -> dict[str, Any]:
    payload = load_json(event_file, None)
    return import_event_payload(
        payload,
        building,
        aliases,
        default_capacity,
        profile_file,
        custom_file,
    )


def status_payload(profile_file: Path = PROFILE_FILE, custom_file: Path = CUSTOM_MAPPING_FILE) -> dict[str, Any]:
    profile = load_profile(profile_file)
    result = {**profile}
    if profile.get("catalog") == "custom":
        mapping = load_json(custom_file, {"buildings": []})
        result["building_count"] = len(mapping.get("buildings", []))
        result["room_count"] = sum(len(building.get("rooms", [])) for building in mapping.get("buildings", []))
        result["ready"] = result["room_count"] > 0
    else:
        result["ready"] = bool(profile.get("configured"))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="飞书会议室技能首次配置")
    parser.add_argument("--status", action="store_true", help="查看配置状态")
    parser.add_argument("--set-company", metavar="COMPANY", help="保存公司名称并选择会议室目录")
    parser.add_argument("--import-event-file", type=Path, help="从飞书日程详情 JSON 导入会议室")
    parser.add_argument("--calendar-id", help="配置日程所在日历 ID")
    parser.add_argument("--event-id", help="配置日程 ID；与 --calendar-id 一起使用")
    parser.add_argument("--building", help="导入会议室所属楼栋")
    parser.add_argument("--aliases", default="", help="楼栋别名，逗号分隔")
    parser.add_argument("--default-capacity", type=int, default=0, help="名称未标容量时的默认容量")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    try:
        if args.set_company:
            result = set_company(args.set_company)
        elif args.import_event_file:
            if not args.building:
                parser.error("--import-event-file 需要 --building")
            aliases = [alias.strip() for alias in args.aliases.split(",") if alias.strip()]
            result = import_event_file(args.import_event_file, args.building, aliases, args.default_capacity)
        elif args.calendar_id or args.event_id:
            if not args.calendar_id or not args.event_id or not args.building:
                parser.error("从日程直接导入需要 --calendar-id、--event-id 和 --building")
            aliases = [alias.strip() for alias in args.aliases.split(",") if alias.strip()]
            payload = fetch_event_resources(args.calendar_id, args.event_id)
            result = import_event_payload(payload, args.building, aliases, args.default_capacity)
        else:
            result = status_payload()
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f"错误: {error}", file=sys.stderr)
        raise SystemExit(1)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if not result.get("configured", True):
        print("⚙️ 尚未配置公司。首次使用时请先询问用户所在公司。")
    elif "imported" in result:
        print(f"✅ 已向 {result['building']} 导入 {result['imported']} 间会议室")
    elif result.get("catalog") == "custom" and not result.get("ready"):
        print(f"⚙️ 已保存公司：{result.get('company')}；请从包含会议室资源的日程导入配置")
    else:
        print(f"✅ 配置已就绪：{result.get('company', '')}")


if __name__ == "__main__":
    main()
