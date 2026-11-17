"""Tests for the shared HTTP client layer (BlogClient)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from blog_manager.client import (
    BASE_URL_ENV,
    BlogAPIError,
    BlogClient,
    BlogConfigError,
)

from conftest import make_mock_response, make_mock_session


class TestConfigResolution:
    def test_reads_from_env(self, monkeypatch):
        monkeypatch.setenv(BASE_URL_ENV, "http://env-host:9999")
        c = BlogClient()
        assert c.base_url == "http://env-host:9999"

    def test_strips_trailing_slash(self, monkeypatch):
        monkeypatch.setenv(BASE_URL_ENV, "http://h:1////")
        c = BlogClient()
        assert c.base_url == "http://h:1"

    def test_explicit_arg_overrides_env(self, monkeypatch):
        monkeypatch.setenv(BASE_URL_ENV, "http://env:1")
        c = BlogClient(base_url="http://arg:2")
        assert c.base_url == "http://arg:2"

    def test_raises_when_not_set(self, monkeypatch):
        monkeypatch.delenv(BASE_URL_ENV, raising=False)
        with pytest.raises(BlogConfigError, match=BASE_URL_ENV):
            BlogClient()

    def test_raises_for_non_http_url(self, monkeypatch):
        monkeypatch.setenv(BASE_URL_ENV, "ftp://bad")
        with pytest.raises(BlogConfigError, match="http://"):
            BlogClient()

    def test_address_not_hardcoded(self, monkeypatch):
        """The API host must never be baked into source code."""
        monkeypatch.setenv(BASE_URL_ENV, "http://dynamic:1234")
        c = BlogClient()
        assert "123.249.19.227" not in c.base_url
        assert "dynamic" in c.base_url


class TestRequestHelper:
    def test_get_calls_session_correctly(self):
        session = make_mock_session(200, {"code": 200, "data": {"id": 1}})
        c = BlogClient(base_url="http://h:1", session=session)
        result = c.get("/api/articles", params={"page": 1})
        session.request.assert_called_once_with(
            "GET", "http://h:1/api/articles",
            params={"page": 1}, json=None, files=None, timeout=30,
        )
        assert result == {"code": 200, "data": {"id": 1}}

    def test_post_with_json(self):
        session = make_mock_session(200, {"code": 200, "data": {"id": 5}})
        c = BlogClient(base_url="http://h:1", session=session)
        result = c.post("/api/articles", json={"title": "t"})
        session.request.assert_called_once_with(
            "POST", "http://h:1/api/articles",
            params=None, json={"title": "t"}, files=None, timeout=30,
        )
        assert result["data"]["id"] == 5

    def test_put(self):
        session = make_mock_session(200, {"code": 200, "message": "ok"})
        c = BlogClient(base_url="http://h:1", session=session)
        c.put("/api/articles/1", json={"heat": 10})
        session.request.assert_called_once_with(
            "PUT", "http://h:1/api/articles/1",
            params=None, json={"heat": 10}, files=None, timeout=30,
        )

    def test_delete_with_params(self):
        session = make_mock_session(200, {"code": 200, "message": "deleted"})
        c = BlogClient(base_url="http://h:1", session=session)
        c.delete("/api/articles/1", params={"soft": True})
        session.request.assert_called_once_with(
            "DELETE", "http://h:1/api/articles/1",
            params={"soft": True}, json=None, files=None, timeout=30,
        )

    def test_health_path_not_under_api(self):
        session = make_mock_session(200, {"status": "ok"})
        c = BlogClient(base_url="http://h:1", session=session)
        c.get("/health")
        session.request.assert_called_once_with(
            "GET", "http://h:1/health",
            params=None, json=None, files=None, timeout=30,
        )


class TestErrorHandling:
    def test_raises_api_error_on_404(self):
        session = make_mock_session(404, {"detail": "文章不存在"})
        c = BlogClient(base_url="http://h:1", session=session)
        with pytest.raises(BlogAPIError) as exc_info:
            c.get("/api/articles/99999")
        assert exc_info.value.status_code == 404
        assert "文章不存在" in exc_info.value.detail

    def test_raises_api_error_on_500(self):
        session = make_mock_session(500, {"detail": "internal error"})
        c = BlogClient(base_url="http://h:1", session=session)
        with pytest.raises(BlogAPIError, match="HTTP 500"):
            c.get("/api/articles")

    def test_handles_non_json_response(self):
        resp = MagicMock()
        resp.status_code = 200
        resp.json.side_effect = ValueError("not json")
        resp.text = "plain text"
        session = MagicMock()
        session.request.return_value = resp
        c = BlogClient(base_url="http://h:1", session=session)
        result = c.get("/health")
        assert result == {"raw": "plain text"}
