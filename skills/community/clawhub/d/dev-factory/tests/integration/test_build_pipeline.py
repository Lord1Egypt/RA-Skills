"""Cycle 7: Build 통합 테스트"""

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from builder.pipeline import BuilderPipeline
from builder.models import BuildResult


@pytest.fixture
def mock_config():
    config = MagicMock()
    config.discovery.output_dir = "/tmp/test-builder-discovery"
    config.discovery.cache_ttl_seconds = 3600
    config.discovery.github.enabled = False
    config.discovery.cve.enabled = False
    config.discovery.security_news.enabled = False
    config.orchestration.claude_timeout_seconds = 300
    return config


SAMPLE_IDEA = {
    "title": "Test CVE Scanner",
    "description": "A test scanner",
    "source": "cve_database",
    "complexity": "medium",
    "priority": "high",
    "tech_stack": ["python"],
    "score": 0.8,
    "cve_id": "CVE-2026-0001",
}


@pytest.mark.integration
def test_build_retries_up_to_3_times_on_failure(mock_config, tmp_path):
    mock_config.discovery.output_dir = str(tmp_path)
    pipeline = BuilderPipeline(mock_config)

    call_count = {"n": 0}

    def always_fail(project, path):
        call_count["n"] += 1
        return BuildResult(
            success=False,
            project_path=str(path),
            retry_count=call_count["n"],
            mode="claude",
            test_output="Build failed",
        )

    pipeline.orchestrator.develop = always_fail

    project_path = tmp_path / "test_project"
    project_path.mkdir()

    result = pipeline.run_build_pipeline(SAMPLE_IDEA, project_path)
    assert result["success"] is False


@pytest.mark.integration
def test_build_succeeds_after_self_correction(mock_config, tmp_path):
    mock_config.discovery.output_dir = str(tmp_path)
    pipeline = BuilderPipeline(mock_config)

    project_path = tmp_path / "test_project"
    project_path.mkdir()

    # 1차: 빌드 성공 (테스트는 실패)
    pipeline.orchestrator.develop = MagicMock(return_value=BuildResult(
        success=True,
        project_path=str(project_path),
        retry_count=1,
        mode="claude",
    ))

    # 첫 번째 테스트: 실패, 두 번째 테스트: 성공
    call_counts = {"n": 0}

    def mock_run_tests(path):
        call_counts["n"] += 1
        if call_counts["n"] == 1:
            return {"success": False, "output": 'File "src/main.py", line 5\nAssertionError'}
        return {"success": True, "output": "All tests passed"}

    pipeline._run_tests = mock_run_tests
    pipeline.analyzer.analyze = MagicMock(return_value={
        "type": "test_failure",
        "file_path": str(project_path / "src" / "main.py"),
        "line_number": 5,
        "raw_output": "AssertionError",
        "details": {},
        "fix_suggestion": "Fix assertion",
    })
    pipeline.fixer.fix = MagicMock(return_value=True)

    result = pipeline.run_build_pipeline(SAMPLE_IDEA, project_path)
    assert result["success"] is True
    assert call_counts["n"] == 2  # 2번 테스트 실행됨
