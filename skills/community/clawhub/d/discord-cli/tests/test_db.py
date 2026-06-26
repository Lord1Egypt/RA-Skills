from __future__ import annotations

from datetime import datetime, timedelta, timezone

from discord_cli.db import MessageDB


def test_get_latest_returns_latest_messages_in_chronological_order(seeded_db: MessageDB):
    messages = seeded_db.get_latest(limit=2)

    assert [m["msg_id"] for m in messages] == ["101", "102"]
    assert [m["content"] for m in messages] == ["second message", "third message"]


def test_get_today_uses_provided_timezone(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "messages.db"))

    with MessageDB() as db:
        db.insert_batch(
            [
                {
                    "msg_id": "1",
                    "channel_id": "c-1",
                    "channel_name": "general",
                    "sender_name": "Alice",
                    "content": "before local midnight",
                    "timestamp": datetime(2026, 3, 9, 15, 59, tzinfo=timezone.utc),
                },
                {
                    "msg_id": "2",
                    "channel_id": "c-1",
                    "channel_name": "general",
                    "sender_name": "Bob",
                    "content": "after local midnight",
                    "timestamp": datetime(2026, 3, 9, 16, 1, tzinfo=timezone.utc),
                },
            ]
        )

        messages = db.get_today(
            tz=timezone(timedelta(hours=8)),
            now=datetime(2026, 3, 10, 4, 0, tzinfo=timezone.utc),
        )

    assert [m["msg_id"] for m in messages] == ["2"]


def test_get_recent_returns_latest_messages_in_chronological_order(seeded_db: MessageDB):
    messages = seeded_db.get_recent(hours=None, limit=2)

    assert [m["msg_id"] for m in messages] == ["101", "102"]


def test_top_senders_groups_by_sender_id_not_name(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "messages.db"))

    with MessageDB() as db:
        db.insert_batch(
            [
                {
                    "msg_id": "1",
                    "channel_id": "c-1",
                    "channel_name": "general",
                    "sender_id": "u-1",
                    "sender_name": "Alex",
                    "content": "hello",
                    "timestamp": datetime(2026, 3, 10, 1, 0, tzinfo=timezone.utc),
                },
                {
                    "msg_id": "2",
                    "channel_id": "c-1",
                    "channel_name": "general",
                    "sender_id": "u-2",
                    "sender_name": "Alex",
                    "content": "world",
                    "timestamp": datetime(2026, 3, 10, 2, 0, tzinfo=timezone.utc),
                },
            ]
        )

        top = db.top_senders(limit=10)

    assert len(top) == 2
    assert {row["sender_id"] for row in top} == {"u-1", "u-2"}
