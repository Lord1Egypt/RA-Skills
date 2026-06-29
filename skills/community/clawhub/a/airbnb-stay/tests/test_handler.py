"""Smoke tests for the airbnb-stay handler. No network — urlopen is mocked."""

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
        self.assertIn("stayingapi.com/app/keys", result["detail"])


class TestInputValidation(unittest.TestCase):
    def test_subresource_without_target_returns_error(self):
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "sk_test"}):
            result = handler.get_stay_photos()
        self.assertEqual(result["error"], "invalid_argument")


class TestEndpoint(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_lookup_by_id_uses_path_param(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"id": "42", "title": "Loft"}')
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "sk_test"}):
            result = handler.lookup_stay_by_id("42")
        called_url = mock_urlopen.call_args[0][0].full_url
        self.assertIn("/v1/stays/42", called_url)
        self.assertNotIn("by-url", called_url)
        self.assertEqual(result["id"], "42")

    @patch("handler.urllib.request.urlopen")
    def test_lookup_by_url_hits_by_url_endpoint(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"id": "42"}')
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "sk_test"}):
            handler.lookup_stay_by_url("https://www.airbnb.com/rooms/42")
        called_url = mock_urlopen.call_args[0][0].full_url
        self.assertIn("/v1/stays/by-url", called_url)
        self.assertIn("url=", called_url)

    @patch("handler.urllib.request.urlopen")
    def test_subresource_with_id_skips_resolution(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"data": []}')
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "sk_test"}):
            handler.get_stay_reviews(stay_id="42")
        self.assertEqual(mock_urlopen.call_count, 1)
        called_url = mock_urlopen.call_args[0][0].full_url
        self.assertIn("/v1/stays/42/reviews", called_url)

    @patch("handler.urllib.request.urlopen")
    def test_subresource_with_url_resolves_first(self, mock_urlopen):
        mock_urlopen.side_effect = [
            _mock_response(b'{"id": "777"}'),
            _mock_response(b'{"data": []}'),
        ]
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "sk_test"}):
            handler.get_stay_photos(url="https://www.airbnb.com/rooms/777")
        self.assertEqual(mock_urlopen.call_count, 2)
        first_url = mock_urlopen.call_args_list[0][0][0].full_url
        second_url = mock_urlopen.call_args_list[1][0][0].full_url
        self.assertIn("/v1/stays/by-url", first_url)
        self.assertIn("/v1/stays/777/photos", second_url)

    @patch("handler.urllib.request.urlopen")
    def test_authorization_header_is_set(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"id": "42"}')
        with patch.dict(os.environ, {"STAYINGAPI_KEY": "sk_secret"}):
            handler.lookup_stay_by_id("42")
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.headers["Authorization"], "Bearer sk_secret")
        self.assertIn("airbnb-skills", req.headers["User-agent"])


if __name__ == "__main__":
    unittest.main()
