"""Tests for WebPublisher — web viewer manager.

Tests the Python-side lifecycle: start → on_speech → conclude → revoke → stop.
Express subprocess is mocked to keep tests fast (no real PM2).
File I/O uses real tmp_path for integration confidence.
"""

from __future__ import annotations

import errno
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from roundtable.web_publisher import WebPublisher, _generate_token

# ---------------------------------------------------------------------------
# Token generation
# ---------------------------------------------------------------------------


class TestTokenGeneration:
    def test_generate_token_default_length(self):
        token = _generate_token()
        # nanoid returns exact size; secrets.token_urlsafe returns ~ceil(size*4/3)
        assert len(token) >= 21

    def test_generate_token_custom_length(self):
        token = _generate_token(size=10)
        assert len(token) >= 10

    def test_generate_token_unique(self):
        tokens = {_generate_token() for _ in range(100)}
        assert len(tokens) == 100  # all unique

    def test_generate_token_url_safe(self):
        """Token should only contain URL-safe characters."""
        token = _generate_token()
        # nanoid uses A-Za-z0-9_- by default
        import re

        assert re.match(r"^[A-Za-z0-9_-]+$", token)


# ---------------------------------------------------------------------------
# WebPublisher construction
# ---------------------------------------------------------------------------


class TestWebPublisherInit:
    def test_creates_discussion_dir(self, tmp_path):
        d = tmp_path / "new_dir"
        assert not d.exists()
        WebPublisher(str(d))
        assert d.exists()

    def test_defaults(self, tmp_path):
        pub = WebPublisher(str(tmp_path))
        assert pub._port == 8199
        assert pub._host == "0.0.0.0"
        assert pub._token is None
        assert pub.url is None
        assert pub.port is None
        assert pub.token is None


# ---------------------------------------------------------------------------
# Port finding
# ---------------------------------------------------------------------------


class TestPortFinding:
    def test_finds_available_port(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=18199)
        port = pub._find_available_port(18199)
        assert port >= 18199
        assert port < 18209  # within 10 attempts

    def test_skips_busy_port(self, tmp_path):
        """If the preferred port is busy, finds the next one."""
        import socket

        pub = WebPublisher(str(tmp_path), port=18299)

        # Block the first port
        blocker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            blocker.bind(("", 18299))
            port = pub._find_available_port(18299)
            assert port == 18300  # next one
        finally:
            blocker.close()

    def test_raises_if_no_port_available(self, tmp_path):
        """Raises RuntimeError when all 10 ports are busy."""
        import socket

        pub = WebPublisher(str(tmp_path), port=18399)

        blockers = []
        try:
            for i in range(10):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(("", 18399 + i))
                blockers.append(s)

            with pytest.raises(RuntimeError, match="No available port"):
                pub._find_available_port(18399)
        finally:
            for s in blockers:
                s.close()


# ---------------------------------------------------------------------------
# File I/O (atomic write + read)
# ---------------------------------------------------------------------------


class TestFileIO:
    def test_write_and_read_discussion_json(self, tmp_path):
        pub = WebPublisher(str(tmp_path))
        pub._discussion_id = "rt_test01"
        pub._token = "testtoken123"
        pub._topic = "Test Topic"

        pub._write_discussion_json()

        data = pub._read_discussion_json()
        assert data is not None
        assert data["discussion_id"] == "rt_test01"
        assert data["token"] == "testtoken123"
        assert data["topic"] == "Test Topic"
        assert data["status"] == "active"
        assert data["speeches"] == []

    def test_write_creates_json_file(self, tmp_path):
        pub = WebPublisher(str(tmp_path))
        pub._discussion_id = "rt_test02"
        pub._write_discussion_json()

        json_path = tmp_path / "discussion.json"
        assert json_path.exists()

        with open(json_path) as f:
            data = json.load(f)
        assert data["discussion_id"] == "rt_test02"

    def test_read_nonexistent_returns_none(self, tmp_path):
        pub = WebPublisher(str(tmp_path))
        assert pub._read_discussion_json() is None

    def test_atomic_write_no_tmp_file_left(self, tmp_path):
        """After write, .tmp file should be renamed away."""
        pub = WebPublisher(str(tmp_path))
        pub._discussion_id = "rt_test03"
        pub._write_discussion_json()

        tmp_file = tmp_path / "discussion.json.tmp"
        assert not tmp_file.exists()
        assert (tmp_path / "discussion.json").exists()

    def test_write_discussion_json_raw_preserves_extra_fields(self, tmp_path):
        """Raw write allows extra fields like revoked_tokens."""
        pub = WebPublisher(str(tmp_path))
        custom_data = {
            "discussion_id": "rt_custom",
            "extra_field": "hello",
            "revoked_tokens": ["abc"],
        }
        pub._write_discussion_json_raw(custom_data)

        data = pub._read_discussion_json()
        assert data["extra_field"] == "hello"
        assert data["revoked_tokens"] == ["abc"]


# ---------------------------------------------------------------------------
# Lifecycle: start → on_speech → conclude → stop
# ---------------------------------------------------------------------------


class TestWebPublisherLifecycle:
    @patch("roundtable.web_publisher.subprocess.run")
    @patch("roundtable.web_publisher.time.sleep", return_value=None)
    def test_start_returns_url(self, mock_sleep, mock_run, tmp_path):
        mock_run.return_value = MagicMock(returncode=0)

        pub = WebPublisher(str(tmp_path), port=19001)

        # Mock port probe to succeed immediately
        with patch.object(pub, "_start_pm2"):
            url = pub.start("rt_lifecycle01", topic="Test Topic")

        assert url is not None
        assert "/r/" in url
        assert pub.token is not None
        assert pub.port is not None

    def test_start_writes_initial_json(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19002)

        with patch.object(pub, "_start_pm2"):
            pub.start(
                "rt_init",
                topic="AI Ethics",
                participants=[
                    {"profile": "alice", "display_name": "Alice"},
                    {"profile": "bob", "display_name": "Bob"},
                ],
            )

        data = pub._read_discussion_json()
        assert data["discussion_id"] == "rt_init"
        assert data["topic"] == "AI Ethics"
        assert len(data["participants"]) == 2
        assert data["speeches"] == []
        assert data["status"] == "active"

    def test_start_with_custom_token(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19003)
        with patch.object(pub, "_start_pm2"):
            pub.start("rt_tok", token="my-custom-token")

        assert pub.token == "my-custom-token"

    def test_on_speech_appends_and_updates_json(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19004)
        with patch.object(pub, "_start_pm2"):
            pub.start("rt_speech", topic="Test")

        pub.on_speech(
            {
                "participant": "alice",
                "display_name": "Alice",
                "content": "Hello everyone!",
                "round": 1,
            }
        )

        data = pub._read_discussion_json()
        assert len(data["speeches"]) == 1
        assert data["speeches"][0]["participant"] == "alice"
        assert data["speeches"][0]["content"] == "Hello everyone!"
        assert data["speeches"][0]["round"] == 1

    def test_on_speech_multiple(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19005)
        with patch.object(pub, "_start_pm2"):
            pub.start("rt_multi", topic="Test")

        for i in range(5):
            pub.on_speech(
                {
                    "participant": f"speaker_{i}",
                    "content": f"Speech {i}",
                }
            )

        data = pub._read_discussion_json()
        assert len(data["speeches"]) == 5

    def test_on_speech_after_revoke_is_noop(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19006)
        with patch.object(pub, "_start_pm2"):
            pub.start("rt_revoke_speech", topic="Test")

        pub.on_speech({"participant": "alice", "content": "Before revoke"})
        pub.revoke()
        pub.on_speech({"participant": "bob", "content": "After revoke"})

        data = pub._read_discussion_json()
        assert len(data["speeches"]) == 1  # only the first one

    def test_conclude_sets_status_and_conclusion(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19007)
        with patch.object(pub, "_start_pm2"):
            pub.start("rt_conclude", topic="Test")

        pub.on_speech({"participant": "alice", "content": "I think..."})
        pub.conclude("We agreed on X.")

        data = pub._read_discussion_json()
        assert data["status"] == "concluded"
        assert data["conclusion"] == "We agreed on X."

    def test_streaming_speech_events_are_written_to_token_stream(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19021)
        with patch.object(pub, "_start_pm2"):
            pub.start("rt_stream", topic="Streaming")

        pub.on_speech_start("s_1", agent="alice", avatar="🤖", round_num=1)
        pub.on_speech_token("s_1", delta="我", seq=0)
        pub.on_speech_token("s_1", delta="认为", seq=1)
        pub.on_speech_end("s_1", total_tokens=2)

        stream_path = tmp_path / "token_stream.jsonl"
        assert stream_path.exists()
        events = [json.loads(line) for line in stream_path.read_text().splitlines()]
        assert [event["type"] for event in events] == [
            "speech_start",
            "speech_token",
            "speech_token",
            "speech_end",
        ]
        assert events[0] == {
            "type": "speech_start",
            "id": "s_1",
            "agent": "alice",
            "avatar": "🤖",
            "round": 1,
            "timestamp": events[0]["timestamp"],
        }
        assert events[1]["delta"] == "我"
        assert events[1]["seq"] == 0
        assert events[3]["total_tokens"] == 2

    def test_streaming_events_after_revoke_are_noop(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19022)
        with patch.object(pub, "_start_pm2"):
            pub.start("rt_stream_revoke", topic="Streaming")

        pub.revoke()
        pub.on_speech_start("s_1", agent="alice", avatar="🤖", round_num=1)
        pub.on_speech_token("s_1", delta="ignored", seq=0)
        pub.on_speech_end("s_1")

        assert not (tmp_path / "token_stream.jsonl").exists()

    def test_round_summary_updates_json_and_stream(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19023)
        with patch.object(pub, "_start_pm2"):
            pub.start("rt_summary", topic="Summary")

        consensus = [{"content": "Use FastAPI", "supporters": ["Alice", "Bob"]}]
        disagreement = [{"content": "Migration timing", "supporters": ["Alice"], "opponents": ["Bob"]}]
        pub.on_round_summary(round_num=1, consensus=consensus, disagreement=disagreement)

        data = pub._read_discussion_json()
        assert data["round_summaries"] == [
            {
                "type": "round_summary",
                "round": 1,
                "consensus": consensus,
                "disagreement": disagreement,
                "timestamp": data["round_summaries"][0]["timestamp"],
            }
        ]

        events = [json.loads(line) for line in (tmp_path / "token_stream.jsonl").read_text().splitlines()]
        assert events[-1]["type"] == "round_summary"
        assert events[-1]["round"] == 1
        assert events[-1]["consensus"] == consensus

    def test_final_summary_updates_json_and_stream(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19024)
        with patch.object(pub, "_start_pm2"):
            pub.start("rt_final_summary", topic="Summary")

        consensus = [{"content": "Ship Sprint 1", "supporters": ["Alice"]}]
        disagreement = []
        pub.on_final_summary(consensus=consensus, disagreement=disagreement, verdict="Ship it")

        data = pub._read_discussion_json()
        assert data["final_summary"] == {
            "type": "final_summary",
            "consensus": consensus,
            "disagreement": disagreement,
            "verdict": "Ship it",
            "timestamp": data["final_summary"]["timestamp"],
        }

        events = [json.loads(line) for line in (tmp_path / "token_stream.jsonl").read_text().splitlines()]
        assert events[-1]["type"] == "final_summary"
        assert events[-1]["verdict"] == "Ship it"

    def test_revoke_marks_token(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19008)
        with patch.object(pub, "_start_pm2"):
            pub.start("rt_revoke", topic="Test")

        token = pub.token
        pub.revoke()

        data = pub._read_discussion_json()
        assert token in data["revoked_tokens"]

    def test_revoke_sets_internal_flag(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19009)
        with patch.object(pub, "_start_pm2"):
            pub.start("rt_revoke2", topic="Test")

        assert not pub._revoked
        pub.revoke()
        assert pub._revoked


# ---------------------------------------------------------------------------
# stop() — PM2 process cleanup
# ---------------------------------------------------------------------------


class TestStop:
    @patch("roundtable.web_publisher.subprocess.run")
    def test_stop_calls_pm2_delete(self, mock_run, tmp_path):
        mock_run.return_value = MagicMock(returncode=0)

        pub = WebPublisher(str(tmp_path), port=19010)
        with patch.object(pub, "_start_pm2"):
            pub.start("rt_stop")

        # _start_pm2 is mocked, so _pm2_process_name wasn't set — set it manually
        pub._pm2_process_name = "roundtable-web-rt_stop"
        pub.stop()
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert "pm2" in cmd
        assert "delete" in cmd
        assert pub._pm2_process_name is None

    def test_stop_when_not_started(self, tmp_path):
        """stop() on a publisher that never started should be a no-op."""
        pub = WebPublisher(str(tmp_path))
        pub.stop()  # should not raise


# ---------------------------------------------------------------------------
# start() — PM2 integration
# ---------------------------------------------------------------------------


class TestPM2Start:
    @patch("roundtable.web_publisher.subprocess.run")
    @patch("roundtable.web_publisher.time.sleep", return_value=None)
    def test_start_pm2_builds_correct_command(self, mock_sleep, mock_run, tmp_path):
        mock_run.return_value = MagicMock(returncode=0)

        pub = WebPublisher(str(tmp_path), port=19011)

        # Patch socket connect to succeed immediately (port is ready)
        with patch("roundtable.web_publisher.socket.socket") as mock_sock:
            mock_sock.return_value.__enter__ = lambda s: s
            mock_sock.return_value.__exit__ = MagicMock(return_value=False)
            mock_sock.return_value.connect = MagicMock()

            pub.start("rt_pm2_cmd")

        cmd = mock_run.call_args[0][0]
        assert cmd[0] == "pm2"
        assert cmd[1] == "start"
        assert "server.mjs" in cmd[2]
        assert "--name" in cmd
        assert "--interpreter" in cmd
        assert "node" in cmd

    @patch("roundtable.web_publisher.subprocess.run")
    def test_start_pm2_failure_raises(self, mock_run, tmp_path):
        mock_run.return_value = MagicMock(returncode=1, stderr="PM2 error")

        pub = WebPublisher(str(tmp_path), port=19012)
        with pytest.raises(RuntimeError, match="PM2 start failed"):
            pub.start("rt_pm2_fail")

    def test_port_probe_permission_error_is_not_reported_as_exhausted(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19014)
        exc = PermissionError(errno.EPERM, "Operation not permitted")

        with patch("roundtable.web_publisher.socket.socket") as mock_sock:
            mock_sock.return_value.__enter__ = lambda s: s
            mock_sock.return_value.__exit__ = MagicMock(return_value=False)
            mock_sock.return_value.bind.side_effect = exc

            with pytest.raises(PermissionError, match="Cannot bind web viewer"):
                pub._find_available_port(19014)

    def test_port_probe_all_in_use_reports_in_use(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19020)
        exc = OSError(errno.EADDRINUSE, "Address already in use")

        with patch("roundtable.web_publisher.socket.socket") as mock_sock:
            mock_sock.return_value.__enter__ = lambda s: s
            mock_sock.return_value.__exit__ = MagicMock(return_value=False)
            mock_sock.return_value.bind.side_effect = exc

            with pytest.raises(RuntimeError, match="already in use"):
                pub._find_available_port(19020)


# ---------------------------------------------------------------------------
# Properties
# ---------------------------------------------------------------------------


class TestProperties:
    def test_url_before_start(self, tmp_path):
        pub = WebPublisher(str(tmp_path))
        assert pub.url is None

    def test_url_after_start(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19013)
        with patch.object(pub, "_start_pm2"):
            url = pub.start("rt_props")
        assert pub.url == url
        assert url.startswith("http://127.0.0.1:")
        assert pub.port is not None
        assert pub.token is not None

    def test_url_uses_custom_host_when_bind_host_is_specific(self, tmp_path):
        pub = WebPublisher(str(tmp_path), port=19014, host="localhost")
        with patch.object(pub, "_start_pm2"):
            url = pub.start("rt_props_host")
        assert url.startswith("http://localhost:")


# ---------------------------------------------------------------------------
# Integration: full lifecycle with real file I/O
# ---------------------------------------------------------------------------


class TestIntegration:
    def test_full_lifecycle_json_state(self, tmp_path):
        """Simulate a full discussion lifecycle and verify JSON state."""
        pub = WebPublisher(str(tmp_path), port=19020)
        with patch.object(pub, "_start_pm2"):
            pub.start(
                "rt_integration",
                topic="Should we use SSE or WebSocket?",
                participants=[
                    {"profile": "tech_lead", "display_name": "Tech Lead"},
                    {"profile": "pm", "display_name": "PM"},
                ],
            )

        # Initial state
        data = pub._read_discussion_json()
        assert data["status"] == "active"
        assert data["speeches"] == []

        # Speeches
        pub.on_speech(
            {
                "participant": "tech_lead",
                "display_name": "Tech Lead",
                "content": "SSE is simpler for one-way push.",
                "round": 1,
            }
        )
        pub.on_speech(
            {
                "participant": "pm",
                "display_name": "PM",
                "content": "What about WeChat browser compatibility?",
                "round": 1,
            }
        )

        data = pub._read_discussion_json()
        assert len(data["speeches"]) == 2
        assert data["speeches"][0]["participant"] == "tech_lead"
        assert data["speeches"][1]["content"] == "What about WeChat browser compatibility?"

        # Conclude
        pub.conclude("Use SSE with long-polling fallback for WeChat.")

        data = pub._read_discussion_json()
        assert data["status"] == "concluded"
        assert "long-polling" in data["conclusion"]

        # Revoke
        pub.revoke()
        data = pub._read_discussion_json()
        assert pub.token in data["revoked_tokens"]


class TestRunDemoWebIntegration:
    """Test run_demo(web=True) integration with WebPublisher."""

    def test_run_demo_web_starts_publisher(self, tmp_path):
        """run_demo(web=True) should create a WebPublisher and write JSON."""
        from roundtable.adapters.generic import Roundtable

        db_path = str(tmp_path / "test.db")
        rt = Roundtable(db_path=db_path)

        # Mock _start_pm2 to set _actual_port without launching anything
        def fake_start_pm2(self_wp, port):
            self_wp._actual_port = port
            self_wp._pm2_process_name = f"roundtable-web-{self_wp._discussion_id}"

        with patch.object(WebPublisher, "_start_pm2", fake_start_pm2):
            result = rt.run_demo(
                max_rounds=2,
                verbose=False,
                web=True,
                web_port=18199,
            )

        assert result["ok"] is True
        assert result["web_url"] is not None
        assert "/r/" in result["web_url"]

        # Check that the JSON file was written
        disc_dir = Path("/tmp") / "roundtable_web" / result["discussion_id"]
        json_file = disc_dir / "discussion.json"
        assert json_file.exists()

        data = json.loads(json_file.read_text())
        assert data["topic"] == "选择后端框架：FastAPI vs Go Gin vs Node Express"
        assert data["status"] == "concluded"
        assert len(data["speeches"]) == 7  # opening + 2 rounds x 3 participants
        assert data["speeches"][0]["round"] == 0
        assert data["speeches"][1]["round"] == 1
        assert data["speeches"][-1]["round"] == 2
        assert "MVP" in data["conclusion"]
