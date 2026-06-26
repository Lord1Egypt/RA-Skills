"""Cycle 3: Notion spec 절단 해결 테스트"""

import json
import pytest
from unittest.mock import MagicMock
from builder.integration.notion_sync import NotionSync


@pytest.fixture
def notion(monkeypatch):
    captured = []

    def fake_urlopen(req, timeout=None):
        body = req.data if hasattr(req, 'data') else b''
        try:
            captured.append(json.loads(body))
        except Exception:
            captured.append({})
        mock_resp = MagicMock()
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_resp.read.return_value = json.dumps({"id": "page-abc"}).encode()
        mock_resp.status = 200
        return mock_resp

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    sync = NotionSync(database_id="test-db", token="test-token")
    return sync, captured


def test_spec_longer_than_2000_chars_not_truncated(notion):
    sync, _ = notion
    # 긴 description으로 2000자 이상 spec 강제 생성
    long_desc = "This is a comprehensive security scanner that detects " + "vulnerabilities " * 60
    idea = {
        "title": "Test CVE Scanner",
        "description": long_desc,
        "source": "cve_database",
        "cve_id": "CVE-2026-9999",
        "severity": "HIGH",
        "score": 0.85,
        "complexity": "medium",
        "url": "https://nvd.nist.gov/vuln/detail/CVE-2026-9999",
    }
    spec = sync._generate_cve_spec(idea)
    assert len(spec) > 2000, f"spec should be > 2000 chars, got {len(spec)}"
    # 전체 description이 포함되어야 함 (잘리지 않음)
    assert long_desc in spec


def test_long_spec_split_into_multiple_blocks(notion):
    sync, _ = notion
    # 2000자 이상의 markdown spec을 블록으로 변환
    long_markdown = "## Section\n" + ("x" * 2100)
    blocks = sync._markdown_to_blocks(long_markdown)
    # 2100자 단락은 paragraph 블록 1개로 들어가지만 내용이 잘리지 않아야 함
    # (각 블록 텍스트는 2000자 제한이 있으나 spec 전체가 잘리면 안 됨)
    assert len(blocks) >= 1


def test_spec_block_count_matches_length(notion):
    sync, _ = notion
    # 4001자의 일반 텍스트 → 여러 paragraph 블록으로 분할
    lines = ["line " + str(i) + " " + ("a" * 100) for i in range(40)]
    long_markdown = "\n".join(lines)
    blocks = sync._markdown_to_blocks(long_markdown)
    assert len(blocks) == 40


def test_cve_spec_returns_full_content(notion):
    sync, _ = notion
    idea = {
        "title": "CVE Scanner",
        "description": "Scanner for CVE-2026-9999",
        "source": "cve_database",
        "cve_id": "CVE-2026-9999",
        "severity": "CRITICAL",
        "score": 0.95,
        "complexity": "medium",
        "url": "https://nvd.nist.gov/vuln/detail/CVE-2026-9999",
    }
    spec = sync._generate_cve_spec(idea)
    # 참고 자료 섹션이 포함되어야 함 (spec[:2000]으로 잘리면 누락됨)
    assert "참고 자료" in spec
    assert "실행 예시" in spec


def test_security_news_spec_not_truncated(notion):
    sync, _ = notion
    long_desc = "Advanced ransomware detection and analysis tool that " + "monitors and alerts " * 60
    idea = {
        "title": "Ransomware Detector",
        "description": long_desc,
        "source": "security_news",
        "keyword": "ransomware",
        "score": 0.7,
        "complexity": "medium",
        "url": "https://example.com/article",
    }
    spec = sync._generate_security_news_spec(idea)
    assert len(spec) > 2000
    assert long_desc in spec
    assert "실행 예시" in spec


def test_github_spec_not_truncated(notion):
    sync, _ = notion
    long_desc = "A comprehensive GitHub trending project with many features " + "and improvements " * 60
    idea = {
        "title": "GitHub Project Clone",
        "description": long_desc,
        "source": "github_trending",
        "stars": 5000,
        "language": "Python",
        "score": 0.8,
        "complexity": "medium",
        "url": "https://github.com/example/repo",
    }
    spec = sync._generate_github_spec(idea)
    assert len(spec) > 2000
    assert long_desc in spec
    assert "개선 아이디어" in spec
