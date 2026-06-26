"""Cycle 2: Security News HTTP stub 테스트"""

import json
import pytest
from unittest.mock import MagicMock, patch
from urllib.error import URLError

from builder.discovery.security_news import SecurityNewsSource
from builder.models import ProjectIdea


def _make_brave_response(results=None):
    if results is None:
        results = [
            {"title": "Ransomware Tool", "url": "https://example.com/tool1", "description": "Detect ransomware"},
            {"title": "Malware Scanner", "url": "https://example.com/tool2", "description": "Scan malware"},
        ]
    body = json.dumps({"web": {"results": results}}).encode()
    mock_resp = MagicMock()
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    mock_resp.read.return_value = body
    return mock_resp


@pytest.fixture
def source(monkeypatch):
    monkeypatch.setenv("BRAVE_API_KEY", "test-brave-key")
    # brave_search_path가 없는 환경으로 강제
    src = SecurityNewsSource()
    src.brave_search_path = None
    src.brave_api_key = "test-brave-key"
    return src


def test_security_news_makes_http_request(source, monkeypatch):
    monkeypatch.setattr("urllib.request.urlopen", lambda req, timeout=None: _make_brave_response())
    results = source._discover_via_http()
    assert len(results) > 0


def test_security_news_returns_project_ideas(source, monkeypatch):
    monkeypatch.setattr("urllib.request.urlopen", lambda req, timeout=None: _make_brave_response())
    results = source._discover_via_http()
    for r in results:
        assert "title" in r
        assert "description" in r
        assert "source" in r


def test_security_news_handles_network_failure(source, monkeypatch):
    def raise_url_error(req, timeout=None):
        raise URLError("Network unreachable")

    monkeypatch.setattr("urllib.request.urlopen", raise_url_error)
    results = source._discover_via_http()
    assert results == []


def test_security_news_filters_duplicates(source, monkeypatch):
    dup_results = [
        {"title": "Tool A", "url": "https://example.com/same", "description": "Same URL tool"},
        {"title": "Tool B", "url": "https://example.com/same", "description": "Duplicate URL"},
    ]
    monkeypatch.setattr("urllib.request.urlopen", lambda req, timeout=None: _make_brave_response(dup_results))
    results = source._discover_via_http()
    urls = [r.get("url") for r in results if r.get("url")]
    assert len(urls) == len(set(urls)), "Duplicate URLs found in results"
