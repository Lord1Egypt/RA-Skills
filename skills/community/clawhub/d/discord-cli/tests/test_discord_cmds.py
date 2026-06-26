from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from click.testing import CliRunner

from discord_cli.cli import discord_cmds
from discord_cli.cli.main import cli
from discord_cli.db import MessageDB


def test_tail_fetch_once_enriches_and_stores_messages(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "messages.db"))

    async def fake_fetch_messages(client, channel_id, *, limit, after=None, before=None):
        assert channel_id == "c-1"
        assert after == "100"
        assert limit == 10
        return [
            {
                "msg_id": "101",
                "channel_id": "c-1",
                "sender_id": "u-1",
                "sender_name": "Alice",
                "content": "hello live",
                "timestamp": datetime(2026, 3, 10, 4, 0, tzinfo=timezone.utc),
            }
        ]

    monkeypatch.setattr(discord_cmds, "fetch_messages", fake_fetch_messages)

    with MessageDB() as db:
        messages, last_id, inserted = asyncio.run(
            discord_cmds._tail_fetch_once(
                object(),
                db,
                "c-1",
                after="100",
                fetch_limit=10,
                context={"channel_name": "general", "guild_name": "Dev", "guild_id": "g-1"},
                store=True,
            )
        )
        stored = db.get_latest(channel_id="c-1", limit=10)

    assert [m["msg_id"] for m in messages] == ["101"]
    assert last_id == "101"
    assert inserted == 1
    assert stored[0]["channel_name"] == "general"
    assert stored[0]["guild_name"] == "Dev"


def test_dc_tail_once_prints_snapshot(seeded_db: MessageDB, monkeypatch):
    class FakeResponse:
        status_code = 200

        @staticmethod
        def json():
            return {"id": "c-general", "name": "general", "guild_id": "g-1"}

    class FakeClient:
        async def get(self, path):
            if path == "/channels/c-general":
                return FakeResponse()
            raise AssertionError(path)

    @asynccontextmanager
    async def fake_get_client():
        yield FakeClient()

    async def fake_get_guild_info(client, guild_id):
        assert guild_id == "g-1"
        return {"id": "g-1", "name": "Dev"}

    async def fake_fetch_messages(client, channel_id, *, limit, after=None, before=None):
        assert channel_id == "c-general"
        assert limit == 2
        return [
            {
                "msg_id": "201",
                "channel_id": "c-general",
                "sender_id": "u-1",
                "sender_name": "Alice",
                "content": "live one",
                "timestamp": datetime(2026, 3, 10, 5, 0, tzinfo=timezone.utc),
            },
            {
                "msg_id": "202",
                "channel_id": "c-general",
                "sender_id": "u-2",
                "sender_name": "Bob",
                "content": "live two",
                "timestamp": datetime(2026, 3, 10, 5, 1, tzinfo=timezone.utc),
            },
        ]

    monkeypatch.setattr(discord_cmds, "get_client", fake_get_client)
    monkeypatch.setattr(discord_cmds, "get_guild_info", fake_get_guild_info)
    monkeypatch.setattr(discord_cmds, "fetch_messages", fake_fetch_messages)

    runner = CliRunner()
    result = runner.invoke(cli, ["dc", "tail", "c-general", "--once", "-n", "2", "--no-store"])

    assert result.exit_code == 0
    assert "live one" in result.output
    assert "live two" in result.output
    assert "Watching" not in result.output


def test_dc_sync_all_discovers_channels_from_api(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "messages.db"))

    class FakeClient:
        pass

    @asynccontextmanager
    async def fake_get_client():
        yield FakeClient()

    async def fake_list_guilds(client):
        assert isinstance(client, FakeClient)
        return [{"id": "g-1", "name": "Dev", "owner": False}]

    async def fake_list_channels(client, guild_id):
        assert guild_id == "g-1"
        return [{"id": "c-1", "name": "general", "type": 0, "position": 1}]

    async def fake_fetch_messages(client, channel_id, *, limit, after=None, before=None):
        assert channel_id == "c-1"
        assert after is None
        return [
            {
                "msg_id": "101",
                "channel_id": "c-1",
                "sender_id": "u-1",
                "sender_name": "Alice",
                "content": "bootstrapped",
                "timestamp": datetime(2026, 3, 10, 5, 0, tzinfo=timezone.utc),
            }
        ]

    monkeypatch.setattr(discord_cmds, "get_client", fake_get_client)
    monkeypatch.setattr(discord_cmds, "list_guilds", fake_list_guilds)
    monkeypatch.setattr(discord_cmds, "list_channels", fake_list_channels)
    monkeypatch.setattr(discord_cmds, "fetch_messages", fake_fetch_messages)

    runner = CliRunner()
    result = runner.invoke(cli, ["dc", "sync-all", "-n", "50"])

    assert result.exit_code == 0
    assert "Discovered 1 channels across 1 guilds" in result.output
    assert "+1" in result.output

    with MessageDB() as db:
        stored = db.get_latest(channel_id="c-1", limit=10)

    assert [msg["msg_id"] for msg in stored] == ["101"]
    assert stored[0]["guild_name"] == "Dev"
    assert stored[0]["channel_name"] == "general"
