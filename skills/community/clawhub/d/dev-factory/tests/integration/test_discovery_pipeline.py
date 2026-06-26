"""Cycle 7: Discovery 통합 테스트"""

import pytest
from unittest.mock import MagicMock, patch
from builder.pipeline import BuilderPipeline


@pytest.fixture
def mock_config():
    config = MagicMock()
    config.discovery.output_dir = "/tmp/test-builder-discovery"
    config.discovery.cache_ttl_seconds = 3600
    config.discovery.github.enabled = True
    config.discovery.github.method = "browser"
    config.discovery.github.language = "python"
    config.discovery.github.max_results = 3
    config.discovery.cve.enabled = True
    config.discovery.cve.lookback_days = 7
    config.discovery.cve.min_score = 7.0
    config.discovery.cve.severity = "HIGH"
    config.discovery.cve.max_results = 5
    config.discovery.security_news.enabled = True
    config.discovery.security_news.keywords = ["ransomware", "malware"]
    config.orchestration.claude_timeout_seconds = 300
    return config


MOCK_IDEAS = [
    {
        "title": "CVE Scanner A",
        "description": "Scanner for CVE-A",
        "source": "cve_database",
        "complexity": "medium",
        "priority": "high",
        "tech_stack": ["python"],
        "score": 0.9,
        "cve_id": "CVE-2026-0001",
    },
    {
        "title": "CVE Scanner B",
        "description": "Scanner for CVE-B",
        "source": "cve_database",
        "complexity": "simple",
        "priority": "medium",
        "tech_stack": ["python"],
        "score": 0.7,
        "cve_id": "CVE-2026-0002",
    },
    {
        "title": "Ransomware Detector",
        "description": "Detects ransomware",
        "source": "security_news",
        "complexity": "medium",
        "priority": "medium",
        "tech_stack": ["python"],
        "score": 0.6,
    },
]


@pytest.mark.integration
def test_full_discovery_returns_ranked_ideas(mock_config, tmp_path, monkeypatch):
    mock_config.discovery.output_dir = str(tmp_path)

    pipeline = BuilderPipeline(mock_config)

    # 모든 소스를 mock
    for source in pipeline.sources:
        source.discover = MagicMock(return_value=MOCK_IDEAS[:2])

    result = pipeline.run_discovery_pipeline()

    assert result["success"] is True
    assert result["count"] > 0
    ideas = result["ideas"]
    # 점수 내림차순 정렬 확인
    for i in range(len(ideas) - 1):
        assert ideas[i]["score"] >= ideas[i + 1]["score"]


@pytest.mark.integration
def test_discovery_deduplicates_same_cve(mock_config, tmp_path):
    mock_config.discovery.output_dir = str(tmp_path)
    pipeline = BuilderPipeline(mock_config)

    dup_idea = {
        "title": "CVE-2026-SAME Scanner",
        "description": "Same CVE scanner",
        "source": "cve_database",
        "complexity": "medium",
        "priority": "high",
        "tech_stack": ["python"],
        "cve_id": "CVE-2026-SAME",
    }

    for source in pipeline.sources:
        source.discover = MagicMock(return_value=[dup_idea, dup_idea])

    result = pipeline.run_discovery_pipeline()
    cve_same = [i for i in result["ideas"] if i.get("cve_id") == "CVE-2026-SAME"]
    assert len(cve_same) <= 1, "Duplicate CVE ideas should be deduplicated"
