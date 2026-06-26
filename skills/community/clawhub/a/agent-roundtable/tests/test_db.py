"""Tests for the Roundtable DB layer (roundtable.db.RoundtableDB).

Replaces tests/hermes_cli/test_roundtable_db.py — same 27 test cases,
now testing the independent library.
"""

from __future__ import annotations

import pytest

from roundtable.db import RoundtableDB


@pytest.fixture
def rt_db(tmp_path):
    """Isolated RoundtableDB with a fresh database."""
    db_path = tmp_path / "roundtable.db"
    return RoundtableDB(db_path)


@pytest.fixture
def db_conn(rt_db):
    """A connected roundtable DB."""
    conn = rt_db.connect()
    yield conn
    conn.close()


PARTICIPANTS = [
    {"profile": "alice", "role": "Engineer", "perspective": "Technical", "display_name": "Alice"},
    {"profile": "bob", "role": "Designer", "perspective": "UX", "display_name": "Bob"},
    {"profile": "carol", "role": "PM", "perspective": "Business", "display_name": "Carol"},
]


# ---------------------------------------------------------------------------
# Schema / init
# ---------------------------------------------------------------------------


def test_connect_creates_tables(db_conn):
    rows = db_conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    names = {r["name"] for r in rows}
    assert {"discussions", "participants", "speeches", "findings", "convergence_history"} <= names


def test_connect_is_idempotent(rt_db, db_conn):
    rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    # Reconnect (new connection, same DB file)
    conn2 = rt_db.connect()
    try:
        discs = rt_db.list_discussions(conn2)
        assert len(discs) == 1
    finally:
        conn2.close()


# ---------------------------------------------------------------------------
# Discussion CRUD
# ---------------------------------------------------------------------------


def test_create_discussion(rt_db, db_conn):
    disc = rt_db.create_discussion(
        db_conn,
        topic="Database selection",
        participants=PARTICIPANTS,
        context="We need a new DB",
        max_rounds=3,
        created_by="coordinator",
    )
    assert disc.id.startswith("rt_")
    assert len(disc.id) == 11  # rt_ + 8 hex
    assert disc.topic == "Database selection"
    assert disc.context == "We need a new DB"
    assert disc.status == "active"
    assert disc.max_rounds == 3
    assert disc.current_round == 0
    assert disc.speech_order == "fixed"


def test_create_discussion_registers_participants(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    parts = rt_db.get_participants(db_conn, disc.id)
    assert len(parts) == 3
    assert parts[0].participant == "alice"
    assert parts[0].role == "Engineer"
    assert parts[0].display_name == "Alice"
    assert parts[0].is_active is True


def test_create_discussion_validates_speech_order(rt_db, db_conn):
    with pytest.raises(ValueError, match="Invalid speech_order"):
        rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS, speech_order="invalid")


def test_create_discussion_requires_participants(rt_db, db_conn):
    with pytest.raises(ValueError, match="At least one participant"):
        rt_db.create_discussion(db_conn, topic="test", participants=[])


def test_create_discussion_rejects_duplicate_participants(rt_db, db_conn):
    participants = [
        {"profile": "alice", "role": "Engineer"},
        {"profile": "alice", "role": "Designer"},
    ]
    with pytest.raises(ValueError, match="Duplicate participant"):
        rt_db.create_discussion(db_conn, topic="test", participants=participants)


def test_create_discussion_validates_max_rounds(rt_db, db_conn):
    with pytest.raises(ValueError, match="max_rounds"):
        rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS, max_rounds=0)


def test_get_discussion(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    fetched = rt_db.get_discussion(db_conn, disc.id)
    assert fetched is not None
    assert fetched.id == disc.id
    assert fetched.topic == "test"


def test_get_discussion_not_found(rt_db, db_conn):
    assert rt_db.get_discussion(db_conn, "rt_nonexistent") is None


def test_list_discussions(rt_db, db_conn):
    for i in range(3):
        rt_db.create_discussion(db_conn, topic=f"topic {i}", participants=PARTICIPANTS)
    discs = rt_db.list_discussions(db_conn)
    assert len(discs) == 3


def test_list_discussions_filter_status(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    rt_db.create_discussion(db_conn, topic="test2", participants=PARTICIPANTS)
    rt_db.conclude_discussion(db_conn, disc.id)

    active = rt_db.list_discussions(db_conn, status="active")
    concluded = rt_db.list_discussions(db_conn, status="concluded")
    assert len(active) == 1
    assert len(concluded) == 1


def test_conclude_discussion(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    ok = rt_db.conclude_discussion(db_conn, disc.id, conclusion="We chose PostgreSQL", convergence_score=0.9)
    assert ok is True
    fetched = rt_db.get_discussion(db_conn, disc.id)
    assert fetched.status == "concluded"
    assert fetched.conclusion == "We chose PostgreSQL"
    assert fetched.convergence_score == 0.9
    assert fetched.concluded_at is not None


def test_conclude_already_concluded(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    rt_db.conclude_discussion(db_conn, disc.id)
    ok = rt_db.conclude_discussion(db_conn, disc.id)
    assert ok is False


def test_cancel_discussion(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    ok = rt_db.cancel_discussion(db_conn, disc.id)
    assert ok is True
    fetched = rt_db.get_discussion(db_conn, disc.id)
    assert fetched.status == "cancelled"


# ---------------------------------------------------------------------------
# Participants
# ---------------------------------------------------------------------------


def test_get_active_participant_names(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    names = rt_db.get_active_participant_names(db_conn, disc.id)
    assert names == ["alice", "bob", "carol"]


# ---------------------------------------------------------------------------
# Speeches
# ---------------------------------------------------------------------------


def test_add_coordinator_speech_in_round_0(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    result = rt_db.add_speech(db_conn, disc.id, "coordinator", "Hello everyone!")
    speech = result["speech"]
    assert speech.id > 0
    assert speech.round == 0
    assert speech.participant == "coordinator"
    assert speech.content == "Hello everyone!"


def test_participant_cannot_speak_in_round_0(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    with pytest.raises(ValueError, match="Round 0"):
        rt_db.add_speech(db_conn, disc.id, "alice", "Hello everyone!")


def test_speech_round_advances_when_all_spoke(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)

    # Round 0: coordinator opening only
    rt_db.add_speech(db_conn, disc.id, "coordinator", "Opening")

    fetched = rt_db.get_discussion(db_conn, disc.id)
    assert fetched.current_round == 1

    # Round 1
    rt_db.add_speech(db_conn, disc.id, "alice", "Round 1 from Alice")
    fetched = rt_db.get_discussion(db_conn, disc.id)
    assert fetched.current_round == 1  # Still round 1

    rt_db.add_speech(db_conn, disc.id, "bob", "Round 1 from Bob")
    rt_db.add_speech(db_conn, disc.id, "carol", "Round 1 from Carol")
    fetched = rt_db.get_discussion(db_conn, disc.id)
    assert fetched.current_round == 2


def test_speech_auto_conclude_on_max_rounds(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS, max_rounds=1)

    # Round 0
    rt_db.add_speech(db_conn, disc.id, "coordinator", "opening")

    fetched = rt_db.get_discussion(db_conn, disc.id)
    assert fetched.current_round == 1

    # Round 1 (max_rounds=1)
    rt_db.add_speech(db_conn, disc.id, "alice", "r1s1")
    rt_db.add_speech(db_conn, disc.id, "bob", "r1s2")
    rt_db.add_speech(db_conn, disc.id, "carol", "r1s3")

    fetched = rt_db.get_discussion(db_conn, disc.id)
    assert fetched.status == "concluded"


def test_speech_with_reply_to(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    rt_db.add_speech(db_conn, disc.id, "coordinator", "opening")
    r1 = rt_db.add_speech(db_conn, disc.id, "alice", "Original point")
    s1 = r1["speech"]
    r2 = rt_db.add_speech(db_conn, disc.id, "bob", "Responding", reply_to=s1.id)
    s2 = r2["speech"]
    assert s2.reply_to == s1.id


def test_speech_reply_to_invalid(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    rt_db.add_speech(db_conn, disc.id, "coordinator", "opening")
    with pytest.raises(ValueError, match="reply_to speech"):
        rt_db.add_speech(db_conn, disc.id, "alice", "test", reply_to=999)


def test_speech_on_concluded_discussion(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    rt_db.conclude_discussion(db_conn, disc.id)
    with pytest.raises(ValueError, match="concluded"):
        rt_db.add_speech(db_conn, disc.id, "alice", "Too late")


def test_get_speeches(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    rt_db.add_speech(db_conn, disc.id, "coordinator", "opening")
    rt_db.add_speech(db_conn, disc.id, "alice", "s1")
    rt_db.add_speech(db_conn, disc.id, "bob", "s2")
    rt_db.add_speech(db_conn, disc.id, "carol", "s3")  # completes round 1
    rt_db.add_speech(db_conn, disc.id, "alice", "r2s1")

    all_speeches = rt_db.get_speeches(db_conn, disc.id)
    assert len(all_speeches) == 5

    round0 = rt_db.get_speeches(db_conn, disc.id, since_round=0)
    assert len(round0) == 5

    round1 = rt_db.get_speeches(db_conn, disc.id, since_round=1)
    assert len(round1) == 4

    alice_only = rt_db.get_speeches(db_conn, disc.id, participant="alice")
    assert len(alice_only) == 2


def test_get_speech_count(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    rt_db.add_speech(db_conn, disc.id, "coordinator", "opening")
    rt_db.add_speech(db_conn, disc.id, "alice", "s1")
    rt_db.add_speech(db_conn, disc.id, "bob", "s2")
    assert rt_db.get_speech_count(db_conn, disc.id) == 3


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------


def test_add_finding(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    fid = rt_db.add_finding(db_conn, disc.id, "consensus", "We all agree on X", 1, [1, 2])
    assert fid > 0

    findings = rt_db.get_findings(db_conn, disc.id)
    assert len(findings) == 1
    assert findings[0].type == "consensus"
    assert findings[0].content == "We all agree on X"
    assert findings[0].related_speeches == [1, 2]


def test_add_finding_invalid_type(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    with pytest.raises(ValueError, match="Invalid finding type"):
        rt_db.add_finding(db_conn, disc.id, "invalid", "test", 1)


def test_get_findings_filter_type(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    rt_db.add_finding(db_conn, disc.id, "consensus", "agree", 1)
    rt_db.add_finding(db_conn, disc.id, "disagreement", "disagree", 1)
    rt_db.add_finding(db_conn, disc.id, "new_point", "new idea", 1)

    consensus = rt_db.get_findings(db_conn, disc.id, finding_type="consensus")
    assert len(consensus) == 1
    all_findings = rt_db.get_findings(db_conn, disc.id)
    assert len(all_findings) == 3


# ---------------------------------------------------------------------------
# Convergence
# ---------------------------------------------------------------------------


def test_record_and_get_convergence(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    rt_db.record_convergence(db_conn, disc.id, 1, 0.67, 2, 1, 1)
    rt_db.record_convergence(db_conn, disc.id, 2, 0.85, 3, 0, 0)

    history = rt_db.get_convergence_history(db_conn, disc.id)
    assert len(history) == 2
    assert history[0].round == 1
    assert history[0].score == 0.67
    assert history[1].round == 2
    assert history[1].score == 0.85


def test_convergence_upsert(rt_db, db_conn):
    disc = rt_db.create_discussion(db_conn, topic="test", participants=PARTICIPANTS)
    rt_db.record_convergence(db_conn, disc.id, 1, 0.5, 1, 1, 0)
    rt_db.record_convergence(db_conn, disc.id, 1, 0.8, 2, 0, 0)  # replace

    history = rt_db.get_convergence_history(db_conn, disc.id)
    assert len(history) == 1
    assert history[0].score == 0.8
