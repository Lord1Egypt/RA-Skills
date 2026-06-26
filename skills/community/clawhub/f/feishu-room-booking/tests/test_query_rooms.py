import json
import subprocess
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "query_rooms.py"
SPEC = spec_from_file_location("query_rooms", MODULE_PATH)
query_rooms = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(query_rooms)


WORKSPACE_MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "workspace_manager.py"
WORKSPACE_SPEC = spec_from_file_location("workspace_manager_for_query_tests", WORKSPACE_MODULE_PATH)
workspace_manager = module_from_spec(WORKSPACE_SPEC)
assert WORKSPACE_SPEC.loader is not None
WORKSPACE_SPEC.loader.exec_module(workspace_manager)


def building_names(buildings):
    return [building["name"] for building in buildings]


def room_names(rooms):
    return [room["name"] for room in rooms]


def test_match_building_keeps_current_alias_behavior():
    matched = query_rooms.match_building("丽金")

    assert any("丽金智地中心 B座" in name for name in building_names(matched))


def test_match_building_supports_building_with_floor_phrase():
    matched = query_rooms.match_building("丽金B座11楼")

    assert building_names(matched) == ["Beijing-Lijin Zhidi Center Building B(丽金智地中心 B座)"]


def test_match_building_supports_room_code_phrase():
    matched = query_rooms.match_building("F11-15")

    assert building_names(matched)[0] == "Beijing-Lijin Zhidi Center Building B(丽金智地中心 B座)"


def test_match_building_supports_city_and_building_phrase():
    matched = query_rooms.match_building("北京 国家会议中心二期F座 3楼")

    assert building_names(matched) == ["Beijing-China National Convention Center Block F(国家会议中心二期 F座)"]


def test_match_building_supports_room_alias_phrase():
    matched = query_rooms.match_building("A DiscussionBooth")

    assert any("国家会议中心二期 F座" in name for name in building_names(matched))


def test_filter_rooms_by_location_hints_keeps_only_target_floor_and_room():
    matched = query_rooms.match_building("丽金B座11楼 F11-15")
    building = matched[0]
    location_match = query_rooms.resolve_location_query("丽金B座11楼 F11-15")
    filtered = query_rooms.filter_rooms_by_location_hints(building.get("rooms", []), location_match["room_filter"])

    assert room_names(filtered) == ["F11-15(8)"]


def test_filter_rooms_by_location_hints_keeps_only_target_floor():
    matched = query_rooms.match_building("国家会议中心二期F座 3楼")
    building = matched[0]
    location_match = query_rooms.resolve_location_query("国家会议中心二期F座 3楼")
    filtered = query_rooms.filter_rooms_by_location_hints(building.get("rooms", []), location_match["room_filter"])

    assert filtered
    assert all(room["name"].startswith("F3-") for room in filtered)



def test_compute_free_slots_uses_actual_query_duration_when_room_is_fully_free():
    slots = query_rooms.compute_free_slots([], "2026-04-20T14:00:00+08:00", "2026-04-20T15:30:00+08:00")

    assert slots == [{"start": "2026-04-20T14:00:00+08:00", "end": "2026-04-20T15:30:00+08:00", "duration_min": 90}]



def test_resolve_requested_building_prefers_explicit_input(tmp_path):
    prefs_file = tmp_path / "user-preferences.json"
    prefs_file.write_text(json.dumps({
        "preferences": {
            "ou_self": {"default_building": "丽金智地中心 B座"}
        }
    }, ensure_ascii=False), encoding="utf-8")

    workspace_file = tmp_path / "weekly-workspace.json"
    workspace_file.write_text(json.dumps({
        "segments": [{"from": "2026-05-20", "to": "2026-05-25", "workspace": "紫金数码园4号楼"}],
        "next_week": None,
    }, ensure_ascii=False), encoding="utf-8")

    query_rooms.PREFS_FILE = prefs_file
    query_rooms.workspace_manager.WORKSPACE_FILE = workspace_file

    resolved = query_rooms.resolve_requested_building("国家会议中心二期 F座", "ou_self", "2026-05-20")

    assert resolved == "国家会议中心二期 F座"


def test_get_default_building_for_user_falls_back_to_workspace(tmp_path):
    prefs_file = tmp_path / "user-preferences.json"
    prefs_file.write_text(json.dumps({"preferences": {"ou_self": {}}}, ensure_ascii=False), encoding="utf-8")

    workspace_file = tmp_path / "weekly-workspace.json"
    workspace_file.write_text(json.dumps({
        "segments": [{"from": "2026-05-20", "to": "2026-05-25", "workspace": "丽金智地中心 B座"}],
        "next_week": None,
    }, ensure_ascii=False), encoding="utf-8")

    query_rooms.PREFS_FILE = prefs_file
    query_rooms.workspace_manager.WORKSPACE_FILE = workspace_file

    resolved = query_rooms.get_default_building_for_user("ou_self", "2026-05-20")

    assert resolved == "丽金智地中心 B座"


def test_get_default_building_for_user_uses_next_week_when_date_matches(tmp_path):
    prefs_file = tmp_path / "user-preferences.json"
    prefs_file.write_text(json.dumps({"preferences": {"ou_self": {}}}, ensure_ascii=False), encoding="utf-8")

    workspace_file = tmp_path / "weekly-workspace.json"
    workspace_file.write_text(json.dumps({
        "segments": [],
        "next_week": {"week_start": "2026-05-26", "workspace": "紫金数码园4号楼"},
    }, ensure_ascii=False), encoding="utf-8")

    query_rooms.PREFS_FILE = prefs_file
    query_rooms.workspace_manager.WORKSPACE_FILE = workspace_file

    resolved = query_rooms.get_default_building_for_user("ou_self", "2026-05-27")

    assert resolved == "紫金数码园4号楼"


def test_cli_requires_start_and_end_for_availability_query():
    result = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--building",
            "丽金B座",
            "--output",
            "json",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "必须同时指定 --start 和 --end" in result.stderr
