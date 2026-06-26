"""공통 fixtures / mock 팩토리"""

import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from io import BytesIO

from builder.models import ProjectIdea, BuildResult


@pytest.fixture
def simple_project():
    return ProjectIdea(
        title="Test Security Scanner",
        description="A simple test scanner",
        source="cve_database",
        complexity="simple",
        priority="medium",
        tech_stack=["python"],
        cve_id="CVE-2026-1234",
    )


@pytest.fixture
def project_path(tmp_path):
    p = tmp_path / "test_project"
    p.mkdir()
    return p


@pytest.fixture
def glm_success_response():
    """GLM API 성공 응답 mock"""
    response_body = json.dumps({
        "choices": [{
            "message": {
                "content": "```python\nprint('hello')\n```"
            }
        }]
    }).encode()

    mock_response = MagicMock()
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = MagicMock(return_value=False)
    mock_response.read.return_value = response_body
    mock_response.status = 200
    return mock_response


@pytest.fixture
def brave_search_response():
    """Brave Search API 성공 응답 mock"""
    response_body = json.dumps({
        "web": {
            "results": [
                {
                    "title": "Ransomware Detection Tool",
                    "url": "https://example.com/ransomware-tool",
                    "description": "A tool to detect ransomware threats"
                },
                {
                    "title": "Vulnerability Scanner 2026",
                    "url": "https://example.com/vuln-scanner",
                    "description": "Modern vulnerability scanning tool"
                }
            ]
        }
    }).encode()

    mock_response = MagicMock()
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = MagicMock(return_value=False)
    mock_response.read.return_value = response_body
    mock_response.status = 200
    return mock_response


@pytest.fixture
def mock_notion_client(monkeypatch):
    """Notion API 호출 mock"""
    captured_calls = []

    def fake_urlopen(req, timeout=None):
        captured_calls.append(req)
        mock_response = MagicMock()
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_response.read.return_value = json.dumps({"id": "page-123"}).encode()
        mock_response.status = 200
        return mock_response

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    return captured_calls
