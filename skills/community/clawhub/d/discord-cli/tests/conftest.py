from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
os.environ.setdefault("OUTPUT", "rich")

from discord_cli.db import MessageDB


@pytest.fixture
def seeded_db(tmp_path, monkeypatch) -> MessageDB:
    db_path = tmp_path / "messages.db"
    monkeypatch.setenv("DB_PATH", str(db_path))

    rows = [
        {
            "msg_id": "100",
            "channel_id": "c-general",
            "channel_name": "general",
            "guild_id": "g-1",
            "guild_name": "Dev",
            "sender_id": "u-1",
            "sender_name": "Alice",
            "content": "first message",
            "timestamp": datetime(2026, 3, 10, 1, 0, tzinfo=timezone.utc),
        },
        {
            "msg_id": "101",
            "channel_id": "c-general",
            "channel_name": "general",
            "guild_id": "g-1",
            "guild_name": "Dev",
            "sender_id": "u-2",
            "sender_name": "Bob",
            "content": "second message",
            "timestamp": datetime(2026, 3, 10, 2, 0, tzinfo=timezone.utc),
        },
        {
            "msg_id": "102",
            "channel_id": "c-random",
            "channel_name": "random",
            "guild_id": "g-1",
            "guild_name": "Dev",
            "sender_id": "u-1",
            "sender_name": "Alice",
            "content": "third message",
            "timestamp": datetime(2026, 3, 10, 3, 0, tzinfo=timezone.utc),
        },
    ]

    with MessageDB() as db:
        db.insert_batch(rows)

    db = MessageDB()
    try:
        yield db
    finally:
        db.close()
