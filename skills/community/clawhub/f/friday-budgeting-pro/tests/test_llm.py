"""
tests/test_llm.py — Unit tests for server.llm.

All tests are fully isolated: no real network calls are made.
urllib.request.urlopen and the SDK helpers are patched at the module level.
"""

from __future__ import annotations

import json
import os
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_urlopen_response(body: bytes) -> MagicMock:
    """Return a context-manager mock whose .read() returns *body*."""
    resp = MagicMock()
    resp.read.return_value = body
    # Support "with urlopen(...) as resp:"
    cm = MagicMock()
    cm.__enter__ = MagicMock(return_value=resp)
    cm.__exit__ = MagicMock(return_value=False)
    return cm


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestChatOpenClawPrimary(unittest.TestCase):
    """Happy-path: OpenClaw returns an OpenAI-shaped response."""

    def test_openai_shape_returns_content(self):
        """chat() extracts content from an OpenAI-shape response."""
        body = json.dumps({"choices": [{"message": {"content": "hello world"}}]}).encode()
        cm = _make_urlopen_response(body)

        with patch("urllib.request.urlopen", return_value=cm) as mock_urlopen:
            from server.llm import chat

            result = chat([{"role": "user", "content": "hi"}])

        self.assertEqual(result, "hello world")
        mock_urlopen.assert_called_once()


class TestChatFallbackOnURLError(unittest.TestCase):
    """When urlopen raises URLError, chat() falls back to the SDK path."""

    def test_fallback_used_on_url_error(self):
        with patch(
            "urllib.request.urlopen",
            side_effect=urllib.error.URLError("connection refused"),
        ):
            with patch(
                "server.llm._chat_sdk_fallback", return_value="sdk-response"
            ) as mock_fallback:
                from server.llm import chat

                result = chat([{"role": "user", "content": "hi"}])

        self.assertEqual(result, "sdk-response")
        mock_fallback.assert_called_once()

    def test_fallback_used_on_connection_error(self):
        with patch(
            "urllib.request.urlopen",
            side_effect=ConnectionRefusedError("refused"),
        ):
            with patch(
                "server.llm._chat_sdk_fallback", return_value="fallback-ok"
            ) as mock_fallback:
                from server.llm import chat

                result = chat([{"role": "user", "content": "hi"}])

        self.assertEqual(result, "fallback-ok")
        mock_fallback.assert_called_once()


class TestChatCustomURL(unittest.TestCase):
    """When OPENCLAW_API_URL is set, urlopen receives that URL."""

    def test_custom_url_used(self):
        body = json.dumps({"choices": [{"message": {"content": "custom"}}]}).encode()
        cm = _make_urlopen_response(body)

        custom_url = "http://localhost:9999/v1/completions"
        env_patch = {"OPENCLAW_API_URL": custom_url}

        with patch.dict(os.environ, env_patch):
            with patch("urllib.request.urlopen", return_value=cm) as mock_urlopen:
                from server.llm import chat

                result = chat([{"role": "user", "content": "hi"}])

        self.assertEqual(result, "custom")
        call_args = mock_urlopen.call_args
        # The first positional arg is the Request object
        req = call_args[0][0]
        self.assertEqual(req.full_url, custom_url)


class TestChatFlatResponseShape(unittest.TestCase):
    """Flat {"text": "..."} response shape is parsed correctly."""

    def test_flat_text_shape(self):
        body = json.dumps({"text": "hi"}).encode()
        cm = _make_urlopen_response(body)

        with patch("urllib.request.urlopen", return_value=cm):
            from server.llm import chat

            result = chat([{"role": "user", "content": "hello"}])

        self.assertEqual(result, "hi")

    def test_flat_content_shape(self):
        body = json.dumps({"content": "flat-content"}).encode()
        cm = _make_urlopen_response(body)

        with patch("urllib.request.urlopen", return_value=cm):
            from server.llm import chat

            result = chat([{"role": "user", "content": "hello"}])

        self.assertEqual(result, "flat-content")


class TestChatMalformedJSON(unittest.TestCase):
    """Malformed JSON response falls back to the SDK path."""

    def test_malformed_json_falls_back(self):
        body = b"not valid json {"
        cm = _make_urlopen_response(body)

        with patch("urllib.request.urlopen", return_value=cm):
            with patch("server.llm._chat_sdk_fallback", return_value="sdk-ok") as mock_fallback:
                from server.llm import chat

                result = chat([{"role": "user", "content": "hi"}])

        self.assertEqual(result, "sdk-ok")
        mock_fallback.assert_called_once()


class TestChatUnrecognisedShape(unittest.TestCase):
    """An unrecognised JSON shape falls back to the SDK path."""

    def test_unknown_shape_falls_back(self):
        body = json.dumps({"unknown_key": "value"}).encode()
        cm = _make_urlopen_response(body)

        with patch("urllib.request.urlopen", return_value=cm):
            with patch(
                "server.llm._chat_sdk_fallback", return_value="sdk-shape-fallback"
            ) as mock_fallback:
                from server.llm import chat

                result = chat([{"role": "user", "content": "hi"}])

        self.assertEqual(result, "sdk-shape-fallback")
        mock_fallback.assert_called_once()


class TestChatOpenAIDeltaShape(unittest.TestCase):
    """OpenAI delta (streaming residue) shape is also supported."""

    def test_delta_shape(self):
        body = json.dumps({"choices": [{"delta": {"content": "delta-reply"}}]}).encode()
        cm = _make_urlopen_response(body)

        with patch("urllib.request.urlopen", return_value=cm):
            from server.llm import chat

            result = chat([{"role": "user", "content": "hi"}])

        self.assertEqual(result, "delta-reply")


class TestChatInterface(unittest.TestCase):
    """The chat() function is patchable at 'server.llm.chat'."""

    def test_patchable(self):
        with patch("server.llm.chat", return_value="mocked") as mock_chat:
            from server import llm

            result = llm.chat([{"role": "user", "content": "test"}])

        self.assertEqual(result, "mocked")
        mock_chat.assert_called_once()


if __name__ == "__main__":
    unittest.main()
