"""Additional tests to push core.py coverage from 65% to ≥80%.

Covers: validation errors, not-found paths, demo, structured summary branches.
"""

from __future__ import annotations

import pytest

from roundtable.core import RoundtableCore
from roundtable.db import RoundtableDB
from roundtable.exceptions import (
    DiscussionNotActiveError,
    DiscussionNotFoundError,
)


@pytest.fixture
def core(tmp_path):
    db = RoundtableDB(tmp_path / "roundtable.db")
    return RoundtableCore(db)


def _p():
    return [
        {"profile": "alice", "role": "Engineer", "perspective": "Tech", "display_name": "Alice"},
        {"profile": "bob", "role": "Designer", "perspective": "UX", "display_name": "Bob"},
        {"profile": "carol", "role": "PM", "perspective": "Biz", "display_name": "Carol"},
    ]


def _open(core, discussion_id):
    return core.speak(discussion_id, "coordinator", "Opening")


# ---------------------------------------------------------------------------
# create_discussion validation
# ---------------------------------------------------------------------------


def test_create_discussion_participants_not_list(core):
    with pytest.raises(ValueError, match="non-empty array"):
        core.create_discussion(topic="T", participants="not-a-list")


def test_create_discussion_bad_max_rounds(core):
    with pytest.raises(ValueError, match="max_rounds"):
        core.create_discussion(topic="T", participants=_p(), max_rounds="abc")


# ---------------------------------------------------------------------------
# speak validation & error paths
# ---------------------------------------------------------------------------


def test_speak_empty_discussion_id(core):
    with pytest.raises(ValueError, match="discussion_id"):
        core.speak("", "alice", "hi")


def test_speak_empty_participant(core):
    d = core.create_discussion(topic="T", participants=_p())
    with pytest.raises(ValueError, match="participant"):
        core.speak(d["discussion_id"], "", "hi")


def test_speak_bad_reply_to(core):
    d = core.create_discussion(topic="T", participants=_p())
    _open(core, d["discussion_id"])
    with pytest.raises(ValueError, match="reply_to"):
        core.speak(d["discussion_id"], "alice", "hi", reply_to="notint")


def test_speak_discussion_not_found(core):
    with pytest.raises(DiscussionNotFoundError):
        core.speak("rt_nonexist", "alice", "hi")


def test_speak_discussion_not_active(core):
    d = core.create_discussion(topic="T", participants=_p())
    did = d["discussion_id"]
    core.end_discussion(did)
    with pytest.raises(DiscussionNotActiveError):
        core.speak(did, "alice", "hi")


# ---------------------------------------------------------------------------
# read validation & error paths
# ---------------------------------------------------------------------------


def test_read_empty_discussion_id(core):
    with pytest.raises(ValueError, match="discussion_id"):
        core.read("")


def test_read_bad_since_round(core):
    d = core.create_discussion(topic="T", participants=_p())
    with pytest.raises(ValueError, match="since_round"):
        core.read(d["discussion_id"], since_round="abc")


def test_read_discussion_not_found(core):
    with pytest.raises(DiscussionNotFoundError):
        core.read("rt_nonexist")


# ---------------------------------------------------------------------------
# status validation & error paths
# ---------------------------------------------------------------------------


def test_status_empty_discussion_id(core):
    with pytest.raises(ValueError, match="discussion_id"):
        core.status("")


def test_status_discussion_not_found(core):
    with pytest.raises(DiscussionNotFoundError):
        core.status("rt_nonexist")


# ---------------------------------------------------------------------------
# summarize validation & error paths
# ---------------------------------------------------------------------------


def test_summarize_empty_discussion_id(core):
    with pytest.raises(ValueError, match="discussion_id"):
        core.summarize("")


def test_summarize_discussion_not_found(core):
    with pytest.raises(DiscussionNotFoundError):
        core.summarize("rt_nonexist")


def test_summarize_with_findings_and_convergence(core):
    """Summarize with findings and convergence — covers structured summary branches."""
    d = core.create_discussion(
        topic="T",
        participants=_p(),
        context="ctx",
        max_rounds=2,
    )
    did = d["discussion_id"]

    # Round 0 opening
    _open(core, did)

    # Round 1
    core.speak(did, "alice", "A0")
    core.speak(did, "bob", "B0")
    core.speak(did, "carol", "C0")

    # Add findings for round 1
    conn = core.db.connect()
    core.db.add_finding(conn, did, "consensus", "We agree on X", 1)
    core.db.add_finding(conn, did, "disagreement", "We disagree on Y", 1)
    core.db.add_finding(conn, did, "new_point", "New idea Z", 1)
    core.db.record_convergence(conn, did, 1, 0.67, 2, 1, 1)
    conn.close()

    # Round 2
    core.speak(did, "alice", "A1")
    core.speak(did, "bob", "B1")
    core.speak(did, "carol", "C1")

    # Conclude
    core.end_discussion(did, conclusion="We chose X")

    result = core.summarize(did)
    assert result["ok"] is True
    assert len(result["consensus_points"]) == 1
    assert len(result["disagreement_points"]) == 1
    assert len(result["new_points"]) == 1
    assert result["final_convergence_score"] is not None
    assert "structured_summary" in result
    ss = result["structured_summary"]
    assert "共识点" in ss
    assert "分歧点" in ss
    assert "新议题" in ss
    assert "收敛度" in ss


def test_summarize_convergence_from_history(core):
    """When disc.convergence_score is None, fall back to last history entry."""
    d = core.create_discussion(topic="T", participants=_p())
    did = d["discussion_id"]

    _open(core, did)
    core.speak(did, "alice", "A0")
    core.speak(did, "bob", "B0")
    core.speak(did, "carol", "C0")

    # Record convergence but don't set disc.convergence_score directly
    conn = core.db.connect()
    core.db.record_convergence(conn, did, 1, 0.85, 3, 0, 0)
    conn.close()

    result = core.summarize(did)
    # Should pick up from history
    assert result["final_convergence_score"] == 0.85


# ---------------------------------------------------------------------------
# end_discussion validation & error paths
# ---------------------------------------------------------------------------


def test_end_empty_discussion_id(core):
    with pytest.raises(ValueError, match="discussion_id"):
        core.end_discussion("")


def test_end_discussion_not_found(core):
    with pytest.raises(DiscussionNotFoundError):
        core.end_discussion("rt_nonexist")


def test_end_discussion_already_concluded(core):
    d = core.create_discussion(topic="T", participants=_p())
    did = d["discussion_id"]
    core.end_discussion(did)
    with pytest.raises(DiscussionNotActiveError):
        core.end_discussion(did)


# ---------------------------------------------------------------------------
# list_discussions validation
# ---------------------------------------------------------------------------


def test_list_bad_limit(core):
    with pytest.raises(ValueError, match="limit"):
        core.list_discussions(limit="abc")


# ---------------------------------------------------------------------------
# advance validation
# ---------------------------------------------------------------------------


def test_advance_empty_discussion_id(core):
    with pytest.raises(ValueError, match="discussion_id"):
        core.advance("")


# ---------------------------------------------------------------------------
# notify validation & error paths
# ---------------------------------------------------------------------------


def test_notify_empty_discussion_id(core):
    with pytest.raises(ValueError, match="discussion_id"):
        core.notify("", "speech")


def test_notify_discussion_not_found(core):
    with pytest.raises(DiscussionNotFoundError):
        core.notify("rt_nonexist", "speech")


# ---------------------------------------------------------------------------
# calculate_convergence validation
# ---------------------------------------------------------------------------


def test_calculate_convergence_empty_id(core):
    with pytest.raises(ValueError, match="discussion_id"):
        core.calculate_convergence("", 1)


# ---------------------------------------------------------------------------
# run_demo
# ---------------------------------------------------------------------------


def test_run_demo_default(core, capsys):
    """run_demo with verbose=True exercises the demo formatters."""
    result = core.run_demo(verbose=True)
    assert result["ok"] is True
    assert result["rounds_completed"] == 3
    assert "conclusion" in result
    assert "summary" in result
    assert result["convergence_score"] is not None
    # Verify output was printed
    captured = capsys.readouterr()
    assert "Roundtable Demo" in captured.out or "Round" in captured.out


def test_run_demo_quiet(core):
    """run_demo with verbose=False still works."""
    result = core.run_demo(verbose=False)
    assert result["ok"] is True
    assert result["topic"] == RoundtableCore._DEMO_TOPIC


def test_run_demo_custom_topic(core):
    result = core.run_demo(topic="Custom Topic", max_rounds=1, verbose=False)
    assert result["ok"] is True
    assert result["topic"] == "Custom Topic"
    assert result["rounds_completed"] == 1


def test_run_demo_custom_participants(core):
    custom_p = [
        {"profile": "x", "role": "R1", "display_name": "X", "perspective": "P1"},
        {"profile": "y", "role": "R2", "display_name": "Y", "perspective": "P2"},
        {"profile": "z", "role": "R3", "display_name": "Z", "perspective": "P3"},
    ]
    result = core.run_demo(participants=custom_p, max_rounds=1, verbose=False)
    assert result["ok"] is True


# ---------------------------------------------------------------------------
# set_send_fn
# ---------------------------------------------------------------------------


def test_set_send_fn(core):
    sent = []
    core.set_send_fn(lambda p, c, m: sent.append(m))
    d = core.create_discussion(
        topic="T",
        participants=_p(),
        notifications={"enabled": True, "channels": [{"platform": "feishu", "chat_id": "oc_x"}], "events": ["speech"]},
    )
    _open(core, d["discussion_id"])
    sent.clear()
    core.speak(d["discussion_id"], "alice", "hi")
    assert len(sent) == 1


# ---------------------------------------------------------------------------
# End-to-end: multi-round with notifications covering round_start
# ---------------------------------------------------------------------------


def test_round_start_notification(core):
    """First speech in a new round triggers round_start notification."""
    sent = []
    core.set_send_fn(lambda p, c, m: sent.append(m))

    notif = {
        "enabled": True,
        "channels": [{"platform": "feishu", "chat_id": "oc_x"}],
    }
    d = core.create_discussion(topic="T", participants=_p(), notifications=notif)
    did = d["discussion_id"]

    # Round 0 opening
    _open(core, did)
    sent.clear()

    # Round 1
    core.speak(did, "alice", "A0")
    core.speak(did, "bob", "B0")
    core.speak(did, "carol", "C0")
    sent.clear()

    # Round 2 — first speech should trigger round_start
    core.speak(did, "alice", "A1")
    round_start_msgs = [m for m in sent if "讨论开始" in m]
    assert len(round_start_msgs) >= 1


def test_concluded_notification(core):
    """Concluding a discussion with notifications sends concluded event."""
    sent = []
    core.set_send_fn(lambda p, c, m: sent.append(m))

    notif = {
        "enabled": True,
        "channels": [{"platform": "feishu", "chat_id": "oc_x"}],
    }
    d = core.create_discussion(topic="T", participants=_p(), notifications=notif)
    did = d["discussion_id"]

    _open(core, did)
    core.speak(did, "alice", "A0")
    core.speak(did, "bob", "B0")
    core.speak(did, "carol", "C0")
    sent.clear()

    core.end_discussion(did, conclusion="Done")
    concluded_msgs = [m for m in sent if "结束" in m]
    assert len(concluded_msgs) >= 1


# ---------------------------------------------------------------------------
# read with participant filter
# ---------------------------------------------------------------------------


def test_read_participant_filter(core):
    d = core.create_discussion(topic="T", participants=_p())
    did = d["discussion_id"]
    _open(core, did)
    core.speak(did, "alice", "A0")
    core.speak(did, "bob", "B0")
    core.speak(did, "carol", "C0")

    result = core.read(did, participant="alice")
    assert result["speech_count"] == 1
    assert result["speeches"][0]["participant"] == "alice"


# ---------------------------------------------------------------------------
# status with findings and next_speaker
# ---------------------------------------------------------------------------


def test_status_with_findings_and_next_speaker(core):
    d = core.create_discussion(topic="T", participants=_p())
    did = d["discussion_id"]
    _open(core, did)
    core.speak(did, "alice", "A0")

    conn = core.db.connect()
    core.db.add_finding(conn, did, "consensus", "agree", 0)
    core.db.add_finding(conn, did, "disagreement", "disagree", 0)
    core.db.add_finding(conn, did, "new_point", "new", 0)
    conn.close()

    result = core.status(did)
    assert result["ok"] is True
    assert len(result["consensus_points"]) == 1
    assert len(result["disagreement_points"]) == 1
    assert len(result["new_points"]) == 1
    assert result["next_speaker"] is not None  # bob hasn't spoken yet
