"""Shared pytest fixtures and path setup for blog-manager tests."""

from __future__ import annotations

import json
import os
import sys
from unittest.mock import MagicMock

import pytest

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

os.environ.setdefault("BLOG_MANAGER_BASE_URL", "http://test-blog:18080")


def make_mock_response(status_code: int = 200, body: dict | None = None) -> MagicMock:
    """Create a fake requests.Response object."""
    resp = MagicMock()
    resp.status_code = status_code
    payload = body if body is not None else {"code": 200, "data": []}
    resp.json.return_value = payload
    resp.text = json.dumps(payload)
    return resp


def make_mock_session(status_code: int = 200, body: dict | None = None) -> MagicMock:
    """Create a fake requests.Session whose .request() returns a mock response."""
    session = MagicMock()
    session.request.return_value = make_mock_response(status_code, body)
    return session


@pytest.fixture
def mock_client() -> MagicMock:
    """A MagicMock impersonating BlogClient with sensible default returns."""
    client = MagicMock()
    client.get.return_value = {"code": 200, "data": []}
    client.post.return_value = {"code": 200, "data": {"id": 1}}
    client.put.return_value = {"code": 200, "message": "ok"}
    client.delete.return_value = {"code": 200, "message": "deleted"}
    client.base_url = "http://test-blog:18080"
    return client


@pytest.fixture
def mock_session() -> MagicMock:
    return make_mock_session()


@pytest.fixture
def tmp_upload_file(tmp_path):
    """Create a small temporary file for upload tests."""
    f = tmp_path / "test-upload.txt"
    f.write_text("hello blog-manager")
    return str(f)
