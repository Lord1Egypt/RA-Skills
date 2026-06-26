from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "watch_waitlist.py"
SPEC = spec_from_file_location("watch_waitlist", MODULE_PATH)
watch_waitlist = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(watch_waitlist)


BASE_ITEM = {
    "event_id": "evt_123",
    "summary": "项目例会",
    "start": "2026-04-20T14:00:00+08:00",
    "end": "2026-04-20T15:00:00+08:00",
    "building": "丽金智地中心 B座",
    "capacity_gte": 8,
    "attempted_rooms": [],
    "attempts": 1,
    "status": "ready",
    "suggested_room": "F11-15(8)",
    "suggested_room_id": "omm_room_1",
}


def test_apply_verification_result_removes_confirmed_item():
    updated_item, should_remove = watch_waitlist.apply_verification_result(
        BASE_ITEM,
        "confirmed",
        "会议室预订已确认",
        verified_at="2026-05-20T10:00:00+08:00",
    )

    assert should_remove is True
    assert updated_item is None



def test_apply_verification_result_keeps_pending_item_active():
    updated_item, should_remove = watch_waitlist.apply_verification_result(
        BASE_ITEM,
        "pending",
        "会议室状态待确认",
        verified_at="2026-05-20T10:00:00+08:00",
    )

    assert should_remove is False
    assert updated_item is not None
    assert updated_item["status"] == "verification_pending"
    assert updated_item["last_verification_status"] == "pending"
    assert updated_item["last_verification_reason"] == "会议室状态待确认"
    assert updated_item["last_verified_at"] == "2026-05-20T10:00:00+08:00"
    assert updated_item["suggested_room_id"] == "omm_room_1"



def test_apply_verification_result_returns_failed_item_to_waiting():
    updated_item, should_remove = watch_waitlist.apply_verification_result(
        BASE_ITEM,
        "failed",
        "会议室预订被拒绝",
        verified_at="2026-05-20T10:00:00+08:00",
    )

    assert should_remove is False
    assert updated_item is not None
    assert updated_item["status"] == "waiting"
    assert updated_item["last_verification_status"] == "failed"
    assert updated_item["last_verification_reason"] == "会议室预订被拒绝"
    assert updated_item["last_verified_at"] == "2026-05-20T10:00:00+08:00"
    assert updated_item["attempted_rooms"] == ["omm_room_1"]
    assert "suggested_room" not in updated_item
    assert "suggested_room_id" not in updated_item
