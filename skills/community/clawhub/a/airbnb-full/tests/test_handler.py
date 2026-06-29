"""Smoke tests for the airbnb-full handler. No network — urlopen is mocked."""

import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import handler  # noqa: E402


def _mock_response(body):
    cm = MagicMock()
    cm.__enter__.return_value.read.return_value = body
    return cm


class TestAuth(unittest.TestCase):
    def test_missing_key_returns_auth_error(self):
        with patch.dict(os.environ, {}, clear=True):
            result = handler.lookup_stay_by_id("42")
        self.assertEqual(result["error"], "auth")
        self.assertIn("STAYINGAPI_KEY", result["detail"])

    def test_empty_key_returns_auth_error(self):
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "   "}, clear=True):
            result = handler.get_account()
        self.assertEqual(result["error"], "auth")


class TestInputValidation(unittest.TestCase):
    def test_batch_requires_targets(self):
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "sk_test"}):
            result = handler.batch_stays([])
        self.assertEqual(result["error"], "invalid_argument")

    def test_create_webhook_requires_url_and_events(self):
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "sk_test"}):
            result = handler.create_webhook(url=None, events=None)
        self.assertEqual(result["error"], "invalid_argument")


class TestRequests(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_lookup_by_id(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"id": "42"}')
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "sk_test"}):
            handler.lookup_stay_by_id("42")
        self.assertIn("/v1/stays/42", mock_urlopen.call_args[0][0].full_url)

    @patch("handler.urllib.request.urlopen")
    def test_search_posts_camelcase_body(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"data": []}')
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "sk_test"}):
            handler.search_stays(location="Austin, TX", max_items=10)
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.method, "POST")
        self.assertIn("/v1/search", req.full_url)
        body = json.loads(req.data)
        self.assertEqual(body["locationQueries"], ["Austin, TX"])
        self.assertEqual(body["maxItems"], 10)

    @patch("handler.urllib.request.urlopen")
    def test_batch_classifies_entries(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"job_id": "j1", "status": "queued"}')
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "sk_test"}):
            handler.batch_stays(["42", "https://www.airbnb.com/rooms/99", "1 Main St, Austin TX"])
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.method, "POST")
        self.assertIn("/v1/stays/batch", req.full_url)
        entries = json.loads(req.data)["entries"]
        self.assertEqual(entries[0], {"id": "42"})
        self.assertEqual(entries[1], {"url": "https://www.airbnb.com/rooms/99"})
        self.assertEqual(entries[2], {"address": "1 Main St, Austin TX"})

    @patch("handler.urllib.request.urlopen")
    def test_create_webhook_posts_events(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"id": "wh_1"}')
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "sk_test"}):
            handler.create_webhook("https://ex.com/h", ["job.succeeded", "job.failed"])
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.method, "POST")
        self.assertIn("/v1/webhooks", req.full_url)
        body = json.loads(req.data)
        self.assertEqual(body["url"], "https://ex.com/h")
        self.assertEqual(body["events"], ["job.succeeded", "job.failed"])

    @patch("handler.urllib.request.urlopen")
    def test_delete_webhook_uses_delete_method(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b"")
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "sk_test"}):
            result = handler.delete_webhook("wh_1")
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.method, "DELETE")
        self.assertIn("/v1/webhooks/wh_1", req.full_url)
        self.assertEqual(result, {})

    @patch("handler.urllib.request.urlopen")
    def test_authorization_header_is_set(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"account_id": "a1"}')
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "sk_secret"}):
            handler.get_account()
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.headers["Authorization"], "Bearer sk_secret")
        self.assertIn("airbnb-skills", req.headers["User-agent"])


if __name__ == "__main__":
    unittest.main()
