import json
import subprocess
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "scan_events.py"
SPEC = spec_from_file_location("scan_events", MODULE_PATH)
scan_events = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(scan_events)


def build_event(*, attendees=None, location=None, summary="项目例会", start_time="2026-04-20T14:00:00+08:00", end_time="2026-04-20T15:00:00+08:00"):
    return {
        "event_id": "evt_123",
        "summary": summary,
        "start_time": start_time,
        "end_time": end_time,
        "location": location or {"name": "丽金智地中心 B座"},
        "attendees": attendees or [],
    }


def test_needs_room_for_accepted_self_attendee():
    event = build_event(
        attendees=[
            {"is_self": True, "status": "accepted"},
            {"type": "user", "display_name": "Teammate"},
        ]
    )

    need, reason = scan_events.needs_room(event, "ou_self")

    assert need is True
    assert reason == "需要补订会议室"


def test_skips_event_when_self_attendee_not_accepted():
    event = build_event(attendees=[{"is_self": True, "status": "needs_action"}])

    need, reason = scan_events.needs_room(event, "ou_self")

    assert need is False
    assert reason == "当前用户尚未接受会议"


def test_reads_event_level_self_rsvp_status_first():
    event = build_event(
        attendees=[{"is_self": True, "rsvp_status": "needs_action"}],
        start_time={"datetime": "2026-04-20T14:00:00+08:00", "timezone": "Asia/Shanghai"},
        end_time={"datetime": "2026-04-20T15:00:00+08:00", "timezone": "Asia/Shanghai"},
    )
    event["self_rsvp_status"] = "accept"

    need, reason = scan_events.needs_room(event, "ou_self")

    assert need is True
    assert reason == "需要补订会议室"


def test_reads_response_status_for_self_attendee():
    event = build_event(attendees=[{"is_self": True, "response_status": "accept"}])

    need, reason = scan_events.needs_room(event, "ou_self")

    assert need is True
    assert reason == "需要补订会议室"


def test_reads_nested_response_status_for_self_attendee():
    event = build_event(attendees=[{"is_self": True, "response_status": {"status": "accepted"}}])

    need, reason = scan_events.needs_room(event, "ou_self")

    assert need is True
    assert reason == "需要补订会议室"


def test_matches_user_id_when_is_self_missing():
    event = build_event(attendees=[{"open_id": "ou_self", "status": "accepted"}])

    need, reason = scan_events.needs_room(event, "ou_self")

    assert need is True
    assert reason == "需要补订会议室"



def test_does_not_treat_other_organizer_status_as_self_status():
    event = build_event(
        attendees=[{"open_id": "ou_organizer", "status": "accepted"}],
    )
    event["event_organizer"] = {"open_id": "ou_organizer", "display_name": "Owner"}

    need, reason = scan_events.needs_room(event, "ou_self")

    assert need is False
    assert reason == "当前用户尚未接受会议"



def test_treats_current_user_as_accepted_when_user_is_organizer():
    event = build_event(attendees=[])
    event["event_organizer"] = {"open_id": "ou_self", "display_name": "Owner"}

    need, reason = scan_events.needs_room(event, "ou_self")

    assert need is True
    assert reason == "需要补订会议室"


def test_skips_when_room_resource_already_exists():
    event = build_event(
        attendees=[
            {"is_self": True, "status": "accepted"},
            {"type": "resource", "room_id": "omm_room_1", "status": "accepted"},
        ]
    )

    need, reason = scan_events.needs_room(event, "ou_self")

    assert need is False
    assert reason == "已有会议室"


def test_does_not_treat_pending_resource_as_existing_room():
    event = build_event(
        attendees=[
            {"is_self": True, "status": "accepted"},
            {"type": "resource", "room_id": "omm_room_1", "status": "needs_action"},
        ]
    )

    need, reason = scan_events.needs_room(event, "ou_self")

    assert need is False
    assert reason == "会议室状态待确认"


def test_treats_declined_resource_as_needing_rebooking():
    event = build_event(
        attendees=[
            {"is_self": True, "status": "accepted"},
            {"type": "resource", "room_id": "omm_room_1", "status": "declined"},
        ]
    )

    need, reason = scan_events.needs_room(event, "ou_self")

    assert need is True
    assert reason == "会议室预订失败，需要补订"


def test_books_accepted_event_even_with_online_location():
    event = build_event(
        attendees=[{"is_self": True, "status": "accepted"}],
        location={"name": "飞书视频会议"},
    )

    need, reason = scan_events.needs_room(event, "ou_self")

    assert need is True
    assert reason == "需要补订会议室"


def test_does_not_treat_multi_day_timed_event_as_all_day():
    event = build_event(
        attendees=[{"is_self": True, "status": "accepted"}],
        start_time={"datetime": "2026-06-19T00:00:00+08:00", "timezone": "Asia/Shanghai"},
        end_time={"datetime": "2026-06-21T23:59:59+08:00", "timezone": "Asia/Shanghai"},
        location={},
    )

    need, reason = scan_events.needs_room(event, "ou_self")

    assert need is True
    assert reason == "需要补订会议室"


def test_skips_all_day_event_with_date_only_fields():
    event = build_event(
        attendees=[{"is_self": True, "status": "accepted"}],
        start_time={"date": "2026-06-19"},
        end_time={"date": "2026-06-21"},
        location={},
    )

    need, reason = scan_events.needs_room(event, "ou_self")

    assert need is False
    assert reason == ""


def test_get_default_building_for_user_falls_back_to_workspace(tmp_path):
    prefs_file = tmp_path / "user-preferences.json"
    prefs_file.write_text(json.dumps({"preferences": {"ou_self": {}}}, ensure_ascii=False), encoding="utf-8")

    workspace_file = tmp_path / "weekly-workspace.json"
    workspace_file.write_text(json.dumps({
        "segments": [{"from": "2026-04-20", "to": "2026-04-25", "workspace": "丽金智地中心 B座"}],
        "next_week": None,
    }, ensure_ascii=False), encoding="utf-8")

    scan_events.PREFS_FILE = prefs_file
    scan_events.workspace_manager.WORKSPACE_FILE = workspace_file

    default_building = scan_events.get_default_building_for_user("ou_self", "2026-04-20")

    assert default_building == "丽金智地中心 B座"


def test_get_default_building_for_user_uses_next_week_when_date_matches(tmp_path):
    prefs_file = tmp_path / "user-preferences.json"
    prefs_file.write_text(json.dumps({"preferences": {"ou_self": {}}}, ensure_ascii=False), encoding="utf-8")

    workspace_file = tmp_path / "weekly-workspace.json"
    workspace_file.write_text(json.dumps({
        "segments": [],
        "next_week": {"week_start": "2026-04-21", "workspace": "紫金数码园4号楼"},
    }, ensure_ascii=False), encoding="utf-8")

    scan_events.PREFS_FILE = prefs_file
    scan_events.workspace_manager.WORKSPACE_FILE = workspace_file

    default_building = scan_events.get_default_building_for_user("ou_self", "2026-04-22")

    assert default_building == "紫金数码园4号楼"


def test_outputs_json_only_when_events_file_is_used(tmp_path):
    events_file = tmp_path / "events.json"
    events_file.write_text(json.dumps([
        build_event(attendees=[{"is_self": True, "status": "accepted"}])
    ], ensure_ascii=False), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--user",
            "ou_self",
            "--events-file",
            str(events_file),
            "--output",
            "json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(result.stdout)

    assert payload["needs"] == [
        {
            "event_id": "evt_123",
            "summary": "项目例会",
            "start_time": "2026-04-20T14:00:00+08:00",
            "end_time": "2026-04-20T15:00:00+08:00",
            "organizer": "",
            "reason": "需要补订会议室",
            "verification_status": "confirmed",
        }
    ]
    assert payload["pending_verification"] == []
    assert payload["scan_config"]["user_id"] == "ou_self"



def test_outputs_single_json_document_when_no_events_need_room(tmp_path):
    events_file = tmp_path / "events.json"
    events_file.write_text(json.dumps([
        build_event(attendees=[{"is_self": True, "status": "accepted"}, {"type": "resource", "room_id": "omm_room_1", "status": "accepted"}])
    ], ensure_ascii=False), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--user",
            "ou_self",
            "--events-file",
            str(events_file),
            "--output",
            "json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(result.stdout)

    assert payload["needs"] == []
    assert payload["pending_verification"] == []
    assert payload["scan_config"]["user_id"] == "ou_self"



def test_outputs_pending_verification_events_in_json(tmp_path):
    events_file = tmp_path / "events.json"
    events_file.write_text(json.dumps([
        build_event(attendees=[{"is_self": True, "status": "accepted"}, {"type": "resource", "room_id": "omm_room_1", "status": "needs_action"}])
    ], ensure_ascii=False), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--user",
            "ou_self",
            "--events-file",
            str(events_file),
            "--output",
            "json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(result.stdout)

    assert payload["needs"] == []
    assert payload["pending_verification"] == [
        {
            "event_id": "evt_123",
            "summary": "项目例会",
            "start_time": "2026-04-20T14:00:00+08:00",
            "end_time": "2026-04-20T15:00:00+08:00",
            "organizer": "",
            "reason": "会议室状态待确认",
            "verification_status": "pending",
        }
    ]
