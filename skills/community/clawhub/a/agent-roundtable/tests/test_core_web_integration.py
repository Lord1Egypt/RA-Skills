"""Tests for WebPublisher integration in the normal discussion flow.

Tests that create_discussion, speak, and end_discussion correctly
hook into WebPublisher when web=True is passed.

WebPublisher is mocked to avoid real PM2 subprocess calls.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

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
        {"profile": "alice", "role": "Engineer", "display_name": "Alice"},
        {"profile": "bob", "role": "Designer", "display_name": "Bob"},
    ]


def _mock_publisher():
    """Create a mock WebPublisher with proper return values."""
    mock = MagicMock()
    mock.start.return_value = "http://localhost:8199/rt_test123"
    return mock


# ---------------------------------------------------------------------------
# create_discussion with web=True
# ---------------------------------------------------------------------------


class TestCreateDiscussionWeb:
    def test_web_starts_publisher(self, core):
        """create_discussion with web=True should start a WebPublisher."""
        mock_pub = _mock_publisher()
        with patch("roundtable.web_publisher.WebPublisher", return_value=mock_pub):
            result = core.create_discussion(
                "Test topic",
                _make_participants(),
                web=True,
                web_port=9000,
            )

        assert result["ok"] is True
        assert result["web_url"] == "http://localhost:8199/rt_test123"
        disc_id = result["discussion_id"]
        assert core._publishers[disc_id] is mock_pub
        mock_pub.start.assert_called_once()
        call_kwargs = mock_pub.start.call_args
        assert call_kwargs[0][0] == disc_id  # first positional arg

    def test_web_false_no_publisher(self, core):
        """create_discussion with web=False (default) should not create publisher."""
        result = core.create_discussion(
            "Test topic",
            _make_participants(),
        )
        assert result["ok"] is True
        assert result["web_url"] is None
        assert len(core._publishers) == 0

    def test_web_failure_is_reported(self, core):
        """If web=True is requested, a WebPublisher startup failure is visible."""
        with (
            patch("roundtable.web_publisher.WebPublisher", side_effect=RuntimeError("PM2 not found")),
            pytest.raises(RuntimeError, match="Failed to start web viewer"),
        ):
            core.create_discussion(
                "Test topic",
                _make_participants(),
                web=True,
            )

        assert len(core._publishers) == 0

    def test_publisher_stored_by_discussion_id(self, core):
        """Publisher should be keyed by discussion_id in _publishers dict."""
        mock_pub1 = _mock_publisher()
        mock_pub2 = _mock_publisher()
        with patch("roundtable.web_publisher.WebPublisher", side_effect=[mock_pub1, mock_pub2]):
            r1 = core.create_discussion("Topic A", _make_participants(), web=True)
            r2 = core.create_discussion("Topic B", _make_participants(), web=True)

        assert len(core._publishers) == 2
        assert core._publishers[r1["discussion_id"]] is mock_pub1
        assert core._publishers[r2["discussion_id"]] is mock_pub2


# ---------------------------------------------------------------------------
# speak with publisher
# ---------------------------------------------------------------------------


class TestSpeakWithPublisher:
    def _create_web_discussion(self, core):
        """Helper: create a discussion with web=True and return its id."""
        mock_pub = _mock_publisher()
        with patch("roundtable.web_publisher.WebPublisher", return_value=mock_pub):
            result = core.create_discussion(
                "Test topic",
                _make_participants(),
                web=True,
            )
        core.speak(result["discussion_id"], "coordinator", "Opening")
        mock_pub.reset_mock()
        return result["discussion_id"], mock_pub

    def test_speech_triggers_on_speech(self, core):
        """Each speech should call publisher.on_speech with speech data."""
        disc_id, mock_pub = self._create_web_discussion(core)

        core.speak(disc_id, "alice", "Hello from Alice!")

        mock_pub.on_speech.assert_called_once()
        speech_data = mock_pub.on_speech.call_args[0][0]
        assert speech_data["participant"] == "alice"
        assert speech_data["content"] == "Hello from Alice!"
        assert speech_data["round"] >= 0

    def test_multiple_speeches_all_published(self, core):
        """All speeches should be published, not just the first."""
        disc_id, mock_pub = self._create_web_discussion(core)

        core.speak(disc_id, "alice", "Speech 1")
        core.speak(disc_id, "bob", "Speech 2")

        assert mock_pub.on_speech.call_count == 2

    def test_speak_without_publisher_no_error(self, core):
        """speak() should work fine when there's no publisher (web=False)."""
        result = core.create_discussion("Topic", _make_participants())
        disc_id = result["discussion_id"]
        core.speak(disc_id, "coordinator", "Opening")

        # Should not raise
        speech = core.speak(disc_id, "alice", "Hello!")
        assert speech["ok"] is True

    def test_publisher_on_speech_failure_no_error(self, core):
        """If publisher.on_speech fails, speak() should still succeed."""
        disc_id, mock_pub = self._create_web_discussion(core)
        mock_pub.on_speech.side_effect = RuntimeError("Network error")

        # Should not raise
        speech = core.speak(disc_id, "alice", "Hello!")
        assert speech["ok"] is True


# ---------------------------------------------------------------------------
# end_discussion with publisher
# ---------------------------------------------------------------------------


class TestEndDiscussionWithPublisher:
    def _create_web_discussion(self, core):
        mock_pub = _mock_publisher()
        with patch("roundtable.web_publisher.WebPublisher", return_value=mock_pub):
            result = core.create_discussion(
                "Test topic",
                _make_participants(),
                web=True,
            )
        return result["discussion_id"], mock_pub

    def test_conclude_calls_publisher_conclude_and_retains_viewer(self, core):
        """Normal conclude should keep the web viewer available for review."""
        disc_id, mock_pub = self._create_web_discussion(core)

        result = core.end_discussion(disc_id)

        mock_pub.conclude.assert_called_once()
        mock_pub.stop.assert_not_called()
        assert disc_id in core._publishers
        assert result["web_retained"] is True

    def test_force_cancel_calls_publisher_stop_only(self, core):
        """Force cancel should call publisher.stop() but NOT conclude()."""
        disc_id, mock_pub = self._create_web_discussion(core)

        core.end_discussion(disc_id, force=True)

        mock_pub.conclude.assert_not_called()
        mock_pub.stop.assert_called_once()
        assert disc_id not in core._publishers

    def test_end_without_publisher_no_error(self, core):
        """end_discussion should work fine when there's no publisher."""
        result = core.create_discussion("Topic", _make_participants())
        disc_id = result["discussion_id"]

        end_result = core.end_discussion(disc_id)
        assert end_result["ok"] is True

    def test_publisher_cleanup_failure_no_error(self, core):
        """If publisher cleanup fails, end_discussion should still succeed."""
        disc_id, mock_pub = self._create_web_discussion(core)
        mock_pub.stop.side_effect = RuntimeError("PM2 crash")

        end_result = core.end_discussion(disc_id, force=True)
        assert end_result["ok"] is True
        assert disc_id not in core._publishers


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------


class TestSchemaWebFields:
    def test_init_schema_has_web_field(self):
        """ROUNDTABLE_INIT_SCHEMA should include web and web_port properties."""
        try:
            from roundtable.adapters.hermes import ROUNDTABLE_INIT_SCHEMA
        except ImportError:
            pytest.skip("Hermes adapter not available")

        props = ROUNDTABLE_INIT_SCHEMA["parameters"]["properties"]
        assert "web" in props
        assert props["web"]["type"] == "boolean"
        assert props["web"]["default"] is False
        assert "web_port" in props
        assert props["web_port"]["type"] == "integer"
        assert props["web_port"]["default"] == 8199
