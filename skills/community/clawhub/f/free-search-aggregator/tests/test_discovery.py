from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from free_search.discovery import (
    CANDIDATE_SOURCES,
    SourceDiscovery,
    _probe_candidate_source,
)


class TestCandidateSources(unittest.TestCase):
    def test_registry_not_empty(self) -> None:
        self.assertGreater(len(CANDIDATE_SOURCES), 0)

    def test_all_sources_have_required_fields(self) -> None:
        for src in CANDIDATE_SOURCES:
            self.assertIn("name", src, f"Missing 'name' in {src}")
            self.assertIn("search_url", src, f"Missing 'search_url' in {src}")
            self.assertIn("type", src, f"Missing 'type' in {src}")


class TestProbeCandidate(unittest.TestCase):
    @patch("free_search.discovery.requests.get")
    def test_successful_json_api(self, mock_get: MagicMock) -> None:
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"results": [{"title": "Test"}]}
        mock_get.return_value = response

        source = {
            "name": "test_source",
            "search_url": "https://example.com/search?q={query}&count={count}",
            "type": "json_api",
            "result_path": "results",
        }

        result = _probe_candidate_source(source)
        self.assertEqual(result["status"], "available")
        self.assertEqual(result["result_count"], 1)
        self.assertGreater(result["quality_score"], 0)

    @patch("free_search.discovery.requests.get")
    def test_successful_searxng(self, mock_get: MagicMock) -> None:
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "results": [
                {"title": "Test 1", "url": "https://a.com"},
                {"title": "Test 2", "url": "https://b.com"},
            ]
        }
        mock_get.return_value = response

        source = {
            "name": "test_searxng",
            "search_url": "https://searx.example.com/search?q={query}&format=json",
            "type": "searxng",
        }

        result = _probe_candidate_source(source)
        self.assertEqual(result["status"], "available")
        self.assertEqual(result["result_count"], 2)

    @patch("free_search.discovery.requests.get")
    def test_http_error(self, mock_get: MagicMock) -> None:
        response = MagicMock()
        response.status_code = 403
        mock_get.return_value = response

        source = {
            "name": "blocked",
            "search_url": "https://blocked.com/search?q={query}",
            "type": "json_api",
        }

        result = _probe_candidate_source(source)
        self.assertEqual(result["status"], "http_error")
        self.assertEqual(result["quality_score"], 0.0)

    @patch("free_search.discovery.requests.get")
    def test_timeout(self, mock_get: MagicMock) -> None:
        import requests
        mock_get.side_effect = requests.exceptions.Timeout("timed out")

        source = {
            "name": "slow",
            "search_url": "https://slow.com/search?q={query}",
            "type": "json_api",
        }

        result = _probe_candidate_source(source)
        self.assertEqual(result["status"], "timeout")

    def test_no_url(self) -> None:
        result = _probe_candidate_source({"name": "empty", "type": "json_api"})
        self.assertEqual(result["status"], "no_url")


class TestSourceDiscovery(unittest.TestCase):
    def test_init(self) -> None:
        discovery = SourceDiscovery()
        self.assertIsNotNone(discovery.storage_path)


if __name__ == "__main__":
    unittest.main()
