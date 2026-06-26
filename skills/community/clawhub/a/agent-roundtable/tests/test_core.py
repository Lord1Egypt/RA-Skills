"""Tests for RoundtableCore — the business logic layer.

Replaces tests/tools/test_roundtable_tools.py — same 17 test cases,
now testing via RoundtableCore instead of raw handler functions.
"""

from __future__ import annotations

import json

import pytest

from roundtable.core import RoundtableCore
from roundtable.db import RoundtableDB


@pytest.fixture
def core(tmp_path):
    """Isolated RoundtableCore with a fresh database."""
    db = RoundtableDB(tmp_path / "roundtable.db")
    return RoundtableCore(db)


def _make_participants():
    return [
        {"profile": "alice", "role": "Engineer", "perspective": "Technical", "display_name": "Alice"},
        {"profile": "bob", "role": "Designer", "perspective": "UX", "display_name": "Bob"},
    ]


def _open_discussion(core, disc_id):
    return core.speak(disc_id, "coordinator", "Opening")


# ---------------------------------------------------------------------------
# Module import
# ---------------------------------------------------------------------------


def test_core_module_imports():
    """Verify the roundtable core module imports cleanly."""
    from roundtable import core

    assert core is not None


def test_schema_constants_available():
    """Verify all 9 tool schemas are accessible from the Hermes adapter."""
    try:
        from roundtable.adapters.hermes import (
            ROUNDTABLE_ADVANCE_SCHEMA,
            ROUNDTABLE_END_SCHEMA,
            ROUNDTABLE_INIT_SCHEMA,
            ROUNDTABLE_LIST_SCHEMA,
            ROUNDTABLE_NOTIFY_SCHEMA,
            ROUNDTABLE_READ_SCHEMA,
            ROUNDTABLE_SPEAK_SCHEMA,
            ROUNDTABLE_STATUS_SCHEMA,
            ROUNDTABLE_SUMMARIZE_SCHEMA,
        )
    except ImportError:
        pytest.skip("Hermes adapter not available (hermes-agent not installed)")
        return
    schemas = [
        ROUNDTABLE_INIT_SCHEMA,
        ROUNDTABLE_SPEAK_SCHEMA,
        ROUNDTABLE_READ_SCHEMA,
        ROUNDTABLE_STATUS_SCHEMA,
        ROUNDTABLE_SUMMARIZE_SCHEMA,
        ROUNDTABLE_END_SCHEMA,
        ROUNDTABLE_LIST_SCHEMA,
        ROUNDTABLE_ADVANCE_SCHEMA,
        ROUNDTABLE_NOTIFY_SCHEMA,
    ]
    for s in schemas:
        assert "name" in s
        assert "description" in s
        assert "parameters" in s
        assert s["parameters"]["type"] == "object"


# ---------------------------------------------------------------------------
# create_discussion
# ---------------------------------------------------------------------------


def test_create_discussion_success(core):
    result = core.create_discussion(
        topic="Test topic",
        participants=_make_participants(),
        context="Some context",
        max_rounds=3,
    )
    assert result["ok"] is True
    assert result["discussion_id"].startswith("rt_")
    assert result["topic"] == "Test topic"
    assert result["participants"] == ["alice", "bob"]
    assert result["max_rounds"] == 3


def test_create_discussion_missing_topic(core):
    with pytest.raises(ValueError, match="topic"):
        core.create_discussion(topic="", participants=_make_participants())


def test_create_discussion_too_few_participants(core):
    with pytest.raises(ValueError, match="2 participants"):
        core.create_discussion(topic="Test", participants=[{"profile": "alice"}])


# ---------------------------------------------------------------------------
# speak
# ---------------------------------------------------------------------------


def test_speak_success(core):
    disc = core.create_discussion(topic="Test", participants=_make_participants())
    disc_id = disc["discussion_id"]

    _open_discussion(core, disc_id)
    result = core.speak(disc_id, "alice", "Hello!")
    assert result["ok"] is True
    assert result["speech_id"] > 0
    assert result["round"] == 1
    assert result["participant"] == "alice"


def test_speak_unknown_participant(core):
    disc = core.create_discussion(topic="Test", participants=_make_participants())
    disc_id = disc["discussion_id"]

    with pytest.raises(Exception, match="not an active member"):
        core.speak(disc_id, "eve", "Sneaky!")


def test_speak_missing_content(core):
    disc = core.create_discussion(topic="Test", participants=_make_participants())
    disc_id = disc["discussion_id"]

    with pytest.raises(ValueError, match="content"):
        core.speak(disc_id, "alice", "")


# ---------------------------------------------------------------------------
# read
# ---------------------------------------------------------------------------


def test_read_success(core):
    disc = core.create_discussion(topic="Test", participants=_make_participants())
    disc_id = disc["discussion_id"]

    _open_discussion(core, disc_id)
    core.speak(disc_id, "alice", "Hi")
    core.speak(disc_id, "bob", "Hello")

    result = core.read(disc_id)
    assert result["ok"] is True
    assert result["speech_count"] == 3
    assert len(result["speeches"]) == 3
    assert "formatted_history" in result


def test_read_with_since_round(core):
    disc = core.create_discussion(topic="Test", participants=_make_participants())
    disc_id = disc["discussion_id"]

    # Round 1
    _open_discussion(core, disc_id)
    core.speak(disc_id, "alice", "r1s1")
    core.speak(disc_id, "bob", "r1s2")
    # Round 2
    core.speak(disc_id, "alice", "r2s1")

    result = core.read(disc_id, since_round=2)
    assert result["speech_count"] == 1
    assert result["speeches"][0]["content"] == "r2s1"


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------


def test_status(core):
    disc = core.create_discussion(topic="Test", participants=_make_participants())
    disc_id = disc["discussion_id"]

    result = core.status(disc_id)
    assert result["ok"] is True
    assert result["status"] == "active"
    assert result["current_round"] == 0
    assert result["speech_count"] == 0


# ---------------------------------------------------------------------------
# end_discussion
# ---------------------------------------------------------------------------


def test_end_conclude(core):
    disc = core.create_discussion(topic="Test", participants=_make_participants())
    disc_id = disc["discussion_id"]

    result = core.end_discussion(disc_id)
    assert result["ok"] is True
    assert result["action"] == "concluded"


def test_end_force_cancel(core):
    disc = core.create_discussion(topic="Test", participants=_make_participants())
    disc_id = disc["discussion_id"]

    result = core.end_discussion(disc_id, force=True)
    assert result["ok"] is True
    assert result["action"] == "cancelled"


# ---------------------------------------------------------------------------
# list_discussions
# ---------------------------------------------------------------------------


def test_list(core):
    for i in range(3):
        core.create_discussion(topic=f"Topic {i}", participants=_make_participants())

    result = core.list_discussions()
    assert result["ok"] is True
    assert result["count"] == 3


def test_list_filter_status(core):
    disc = core.create_discussion(topic="Test", participants=_make_participants())
    disc_id = disc["discussion_id"]
    core.end_discussion(disc_id)
    core.create_discussion(topic="Test2", participants=_make_participants())

    result = core.list_discussions(status="active")
    assert result["count"] == 1

    result = core.list_discussions(status="concluded")
    assert result["count"] == 1


# ---------------------------------------------------------------------------
# summarize
# ---------------------------------------------------------------------------


def test_summarize(core):
    disc = core.create_discussion(
        topic="DB Selection",
        participants=_make_participants(),
        context="We need a new database",
    )
    disc_id = disc["discussion_id"]

    _open_discussion(core, disc_id)
    core.speak(disc_id, "alice", "PostgreSQL")
    core.speak(disc_id, "bob", "MySQL")

    result = core.summarize(disc_id)
    assert result["ok"] is True
    assert result["topic"] == "DB Selection"
    assert result["speech_count"] == 3
    assert "rounds" in result
    assert "participants" in result
    assert "consensus_points" in result
    assert "formatted_history" in result
    assert "structured_summary" in result
    assert isinstance(result["structured_summary"], str)
    assert len(result["structured_summary"]) > 0


def test_summarize_compact(core):
    """compact=True should omit raw rounds and formatted_history."""
    disc = core.create_discussion(
        topic="Compact Test",
        participants=_make_participants(),
    )
    disc_id = disc["discussion_id"]

    core.speak(disc_id, "coordinator", "Opening")
    core.speak(disc_id, "alice", "Alice says something long " * 100)
    core.speak(disc_id, "bob", "Bob also says something long " * 100)

    # Full (default)
    full = core.summarize(disc_id)
    assert "rounds" in full
    assert "formatted_history" in full

    # Compact
    compact = core.summarize(disc_id, compact=True)
    assert "rounds" not in compact, "compact mode should omit rounds"
    assert "formatted_history" not in compact, "compact mode should omit formatted_history"
    assert "structured_summary" in compact
    assert compact["speech_count"] == 3
    assert compact["ok"] is True

    # Compact should be significantly smaller
    full_size = len(json.dumps(full))
    compact_size = len(json.dumps(compact))
    assert compact_size < full_size, f"compact ({compact_size}B) should be smaller than full ({full_size}B)"


def test_summarize_writes_output_path(core, tmp_path):
    """Configured output_path should receive generated Markdown."""
    output_path = tmp_path / "summary.md"
    disc = core.create_discussion(
        topic="Output Test",
        participants=_make_participants(),
        output_path=str(output_path),
    )
    disc_id = disc["discussion_id"]

    _open_discussion(core, disc_id)
    core.speak(disc_id, "alice", "PostgreSQL")
    result = core.summarize(disc_id)

    assert result["output_written"] is True
    assert output_path.exists()
    assert "Output Test" in output_path.read_text(encoding="utf-8")


def test_end_writes_full_output_markdown_with_conclusion(core, tmp_path):
    output_path = tmp_path / "final.md"
    disc = core.create_discussion(
        topic="Final Output Test",
        participants=_make_participants(),
        output_path=str(output_path),
    )
    disc_id = disc["discussion_id"]
    _open_discussion(core, disc_id)
    core.speak(disc_id, "alice", "Use PostgreSQL")

    result = core.end_discussion(disc_id, conclusion="Final choice: PostgreSQL")

    assert result["output_written"] is True
    text = output_path.read_text(encoding="utf-8")
    assert "Final Output Test" in text
    assert "Use PostgreSQL" in text
    assert "## 最终结论" in text
    assert "Final choice: PostgreSQL" in text


# ---------------------------------------------------------------------------
# advance
# ---------------------------------------------------------------------------


def test_advance_round(core):
    disc = core.create_discussion(topic="Test", participants=_make_participants())
    disc_id = disc["discussion_id"]

    # Round 0 opening advances to round 1
    _open_discussion(core, disc_id)

    # Explicitly advance to round 2 (skip round 1)
    result = core.advance(disc_id)
    assert result["ok"] is True
    assert result["new_round"] == 2
    assert result["discussion_complete"] is False

    # Verify status shows round 2
    status = core.status(disc_id)
    assert status["current_round"] == 2


def test_advance_exceeds_max_rounds(core):
    disc = core.create_discussion(topic="Test", participants=_make_participants(), max_rounds=2)
    disc_id = disc["discussion_id"]

    # Advance past max
    core.advance(disc_id)  # round 1
    core.advance(disc_id)  # round 2
    result = core.advance(disc_id)  # round 3 > max_rounds=2
    assert result["ok"] is True
    assert result["discussion_complete"] is True

    # Discussion should be concluded
    status = core.status(disc_id)
    assert status["status"] == "concluded"


def test_round_tracking_multi_round(core):
    """Verify that speeches are correctly assigned to rounds across multiple rounds."""
    disc = core.create_discussion(topic="Test", participants=_make_participants())
    disc_id = disc["discussion_id"]

    # Round 0 opening
    opening = core.speak(disc_id, "coordinator", "opening")
    assert opening["round"] == 0
    assert opening["round_complete"] is True

    # Round 1
    r1 = core.speak(disc_id, "alice", "r1 alice")
    assert r1["round"] == 1
    r2 = core.speak(disc_id, "bob", "r1 bob")
    assert r2["round"] == 1
    assert r2["round_complete"] is True

    # Round 2 (auto-advanced)
    r3 = core.speak(disc_id, "alice", "r2 alice")
    assert r3["round"] == 2
    r4 = core.speak(disc_id, "bob", "r2 bob")
    assert r4["round"] == 2
    assert r4["round_complete"] is True

    # Verify via read
    result = core.read(disc_id, since_round=1)
    assert result["speech_count"] == 4
    assert all(s["round"] >= 1 for s in result["speeches"])


def test_round_1_starts_after_coordinator_opening(core):
    """Coordinator opening is the only Round 0 speech."""
    disc = core.create_discussion(topic="Round tracking test", participants=_make_participants(), max_rounds=3)
    disc_id = disc["discussion_id"]

    r1 = core.speak(disc_id, "coordinator", "Opening statement")
    assert r1["round"] == 0
    assert r1["round_complete"] is True

    status = core.status(disc_id)
    assert status["current_round"] == 1
    assert status["next_speaker"] == "alice"

    r2 = core.speak(disc_id, "alice", "Alice R1")
    assert r2["round"] == 1


# ---------------------------------------------------------------------------
# convergence
# ---------------------------------------------------------------------------


def test_calculate_convergence(core):
    disc = core.create_discussion(topic="Test", participants=_make_participants())
    disc_id = disc["discussion_id"]

    result = core.calculate_convergence(disc_id, 0)
    assert result["ok"] is True
    assert result["convergence_score"] is None  # no findings yet


# ---------------------------------------------------------------------------
# notifications
# ---------------------------------------------------------------------------


def test_create_discussion_with_notifications(core):
    """Creating a discussion with notifications config stores it."""
    sent = []
    core.set_send_fn(lambda p, c, m: sent.append((p, c, m)))

    notif_config = {
        "enabled": True,
        "channels": [{"platform": "feishu", "chat_id": "oc_test123"}],
        "events": ["speech", "round_end", "concluded"],
    }
    result = core.create_discussion(
        topic="Notif Test",
        participants=_make_participants(),
        notifications=notif_config,
    )
    assert result["ok"] is True
    disc_id = result["discussion_id"]

    # Verify notifications persisted
    status = core.status(disc_id)
    assert status["ok"] is True

    # Speak and verify notification sent
    _open_discussion(core, disc_id)
    sent.clear()
    core.speak(disc_id, "alice", "Hello from Alice")
    assert len(sent) == 1
    assert sent[0][0] == "feishu"
    assert sent[0][1] == "oc_test123"
    assert "Alice" in sent[0][2]


def test_create_discussion_without_notifications(core):
    """Without notifications config, no notifications are sent."""
    sent = []
    core.set_send_fn(lambda p, c, m: sent.append((p, c, m)))

    result = core.create_discussion(
        topic="No Notif",
        participants=_make_participants(),
    )
    disc_id = result["discussion_id"]
    _open_discussion(core, disc_id)
    core.speak(disc_id, "alice", "Hello")
    assert len(sent) == 0


def test_notification_failure_does_not_block(core):
    """Notification send failures must not raise or block the discussion."""

    def bad_send(p, c, m):
        raise RuntimeError("Network error")

    core.set_send_fn(bad_send)
    notif_config = {
        "enabled": True,
        "channels": [{"platform": "feishu", "chat_id": "oc_test"}],
    }
    result = core.create_discussion(
        topic="Fail Test",
        participants=_make_participants(),
        notifications=notif_config,
    )
    disc_id = result["discussion_id"]

    # Should not raise despite bad send_fn
    _open_discussion(core, disc_id)
    r = core.speak(disc_id, "alice", "Still works")
    assert r["ok"] is True


def test_notification_events_filter(core):
    """Only subscribed events should trigger notifications."""
    sent = []
    core.set_send_fn(lambda p, c, m: sent.append(m))

    notif_config = {
        "enabled": True,
        "channels": [{"platform": "feishu", "chat_id": "oc_test"}],
        "events": ["round_end"],  # Only round_end
    }
    result = core.create_discussion(
        topic="Filter Test",
        participants=_make_participants(),
        notifications=notif_config,
    )
    disc_id = result["discussion_id"]

    # Round 0 — opening should NOT trigger (not subscribed)
    core.speak(disc_id, "coordinator", "Opening")
    assert len(sent) == 0

    # Round 1 — speech should NOT trigger
    core.speak(disc_id, "alice", "R1 Alice")
    assert len(sent) == 0

    # Complete round 1 — round_end SHOULD trigger
    core.speak(disc_id, "bob", "R1 Bob")
    assert len(sent) == 1
    assert "第1轮讨论结束" in sent[0]


def test_manual_notify(core):
    """roundtable_notify should send a manual notification."""
    sent = []
    core.set_send_fn(lambda p, c, m: sent.append(m))

    notif_config = {
        "enabled": True,
        "channels": [{"platform": "feishu", "chat_id": "oc_test"}],
    }
    result = core.create_discussion(
        topic="Manual Notif",
        participants=_make_participants(),
        notifications=notif_config,
    )
    disc_id = result["discussion_id"]

    # Manual notify
    r = core.notify(disc_id, "round_start", round_num=1)
    assert r["ok"] is True
    assert len(sent) == 1
    assert "第1轮讨论开始" in sent[0]


# ---------------------------------------------------------------------------
# P0 fix: Round tracking regression tests
# ---------------------------------------------------------------------------


def test_coordinator_speech_uses_current_round(core):
    """Only the coordinator's opening statement uses round 0."""
    result = core.create_discussion(
        topic="Round tracking test",
        participants=_make_participants(),
        max_rounds=3,
    )
    disc_id = result["discussion_id"]

    # Coordinator opening (round 0 — natural, since current_round=0)
    r = core.speak(disc_id, "coordinator", "Opening statement")
    assert r["round"] == 0, "Opening should be round 0"
    assert r["round_complete"] is True

    # Round 1: all participants speak
    r_alice = core.speak(disc_id, "alice", "Alice R1")
    assert r_alice["round"] == 1, "Alice R1 should be round 1"
    r_bob = core.speak(disc_id, "bob", "Bob R1")
    assert r_bob["round"] == 1, "Bob R1 should be round 1"
    assert r_bob["round_complete"] is True, "Round 1 should be complete"

    # Coordinator speaks again in round 2 — should NOT be round 0.
    r_coord2 = core.speak(disc_id, "coordinator", "Round 2 setup")
    assert r_coord2["round"] == 2, f"Coordinator's second speech should be round 2, got {r_coord2['round']}"

    # Round 2: participants speak
    r_alice2 = core.speak(disc_id, "alice", "Alice R2")
    assert r_alice2["round"] == 2
    r_bob2 = core.speak(disc_id, "bob", "Bob R2")
    assert r_bob2["round"] == 2
    assert r_bob2["round_complete"] is True

    # Coordinator in round 3
    r_coord3 = core.speak(disc_id, "coordinator", "Round 3 setup")
    assert r_coord3["round"] == 3, f"Coordinator's third speech should be round 3, got {r_coord3['round']}"


def test_round_advances_after_all_participants_speak(core):
    """Round should auto-advance when all active participants have spoken."""
    result = core.create_discussion(
        topic="Auto-advance test",
        participants=_make_participants(),
        max_rounds=2,
    )
    disc_id = result["discussion_id"]

    # Round 0 (opening)
    r = core.speak(disc_id, "coordinator", "Opening")
    assert r["round"] == 0
    assert r["round_complete"] is True

    # Round 1
    r = core.speak(disc_id, "alice", "A0")
    assert r["round"] == 1
    assert r["round_complete"] is False
    r = core.speak(disc_id, "bob", "B0")
    assert r["round"] == 1
    assert r["round_complete"] is True

    # Round 2
    r = core.speak(disc_id, "alice", "A1")
    assert r["round"] == 2
    r = core.speak(disc_id, "bob", "B1")
    assert r["round"] == 2
    assert r["round_complete"] is True
    # new_round=3 > max_rounds=2 → conclude
    assert r["discussion_complete"] is True


def test_read_shows_correct_rounds(core):
    """roundtable_read should show correct round numbers for all speeches."""
    result = core.create_discussion(
        topic="Read round test",
        participants=_make_participants(),
        max_rounds=2,
    )
    disc_id = result["discussion_id"]

    core.speak(disc_id, "coordinator", "Opening")
    core.speak(disc_id, "alice", "A0")
    core.speak(disc_id, "bob", "B0")
    core.speak(disc_id, "coordinator", "R1 summary")
    core.speak(disc_id, "alice", "A1")

    read = core.read(disc_id)
    speeches = read["speeches"]
    rounds = [s["round"] for s in speeches]
    assert rounds == [0, 1, 1, 2, 2], f"Expected rounds [0, 1, 1, 2, 2], got {rounds}"


# ---------------------------------------------------------------------------
# API method aliases tests
# ---------------------------------------------------------------------------


def test_core_aliases(core):
    """Verify that all wrapper method aliases work in RoundtableCore."""
    disc = core.init(topic="Alias Test", participants=_make_participants())
    assert disc["ok"] is True
    disc_id = disc["discussion_id"]

    # test speak
    _open_discussion(core, disc_id)
    core.speak(disc_id, "alice", "Alice speaks")
    core.speak(disc_id, "bob", "Bob speaks")

    # test get_status alias
    status = core.get_status(disc_id)
    assert status["ok"] is True
    assert status["status"] == "active"

    # test end alias
    end_res = core.end(disc_id, conclusion="Done with aliases")
    assert end_res["ok"] is True

    # test list alias
    discs = core.list()
    assert discs["ok"] is True
    assert any(d["id"] == disc_id for d in discs["discussions"])


def test_generic_adapter_aliases(tmp_path):
    """Verify that Roundtable class in generic adapter supports both aliases."""
    from roundtable.adapters.generic import Roundtable

    rt = Roundtable(db_path=str(tmp_path / "roundtable_generic.db"))

    # test create_discussion (alias for init)
    disc = rt.create_discussion(topic="Generic Alias Test", participants=_make_participants())
    assert disc["ok"] is True
    disc_id = disc["discussion_id"]

    # test speak
    rt.speak(disc_id, "coordinator", "Opening")
    rt.speak(disc_id, "alice", "Alice speaks")
    rt.speak(disc_id, "bob", "Bob speaks")

    # test status (alias for get_status)
    status = rt.status(disc_id)
    assert status["ok"] is True
    assert status["status"] == "active"

    # test end_discussion (alias for end)
    end_res = rt.end_discussion(disc_id, conclusion="Concluded")
    assert end_res["ok"] is True

    # test list_discussions (alias for list)
    discs = rt.list_discussions()
    assert discs["ok"] is True
    assert any(d["id"] == disc_id for d in discs["discussions"])
