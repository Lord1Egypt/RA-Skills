"""Cycle 1: GLM API stub 해결 테스트"""

import ast
import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError

from builder.orchestrator import HybridOrchestrator
from builder.models import ProjectIdea, BuildResult


@pytest.fixture
def orchestrator(monkeypatch):
    monkeypatch.setenv("BUILDER_GLM_API_KEY", "test-key-12345")
    config = MagicMock()
    config.orchestration.claude_timeout_seconds = 300
    return HybridOrchestrator(config)


@pytest.fixture
def simple_project():
    return ProjectIdea(
        title="Test Scanner",
        description="Test description",
        source="cve_database",
        complexity="simple",
        tech_stack=["python"],
    )


def _make_glm_response(code="print('hello')"):
    body = json.dumps({
        "choices": [{"message": {"content": f"```python\n{code}\n```"}}]
    }).encode()
    mock_resp = MagicMock()
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    mock_resp.read.return_value = body
    return mock_resp


def test_glm_returns_success_when_api_responds(orchestrator, simple_project, project_path, monkeypatch):
    monkeypatch.setattr("urllib.request.urlopen", lambda req, timeout=None: _make_glm_response())
    result = orchestrator._develop_via_glm(simple_project, project_path)
    assert result.success is True
    assert result.mode == "glm"


def test_glm_writes_code_to_project_path(orchestrator, simple_project, project_path, monkeypatch):
    code = "def main():\n    return 42"
    monkeypatch.setattr("urllib.request.urlopen", lambda req, timeout=None: _make_glm_response(code))
    orchestrator._develop_via_glm(simple_project, project_path)
    main_py = project_path / "main.py"
    assert main_py.exists()
    assert "def main" in main_py.read_text()


def test_glm_returns_failure_on_http_error(orchestrator, simple_project, project_path, monkeypatch):
    def raise_http_error(req, timeout=None):
        raise HTTPError(url="http://test", code=401, msg="Unauthorized", hdrs=None, fp=None)

    monkeypatch.setattr("urllib.request.urlopen", raise_http_error)
    result = orchestrator._develop_via_glm(simple_project, project_path)
    assert result.success is False


def test_glm_parses_code_block_from_response(orchestrator, simple_project, project_path, monkeypatch):
    code = "x = 1\ny = 2\nprint(x + y)"
    monkeypatch.setattr("urllib.request.urlopen", lambda req, timeout=None: _make_glm_response(code))
    orchestrator._develop_via_glm(simple_project, project_path)
    content = (project_path / "main.py").read_text()
    assert "x = 1" in content
    assert "y = 2" in content


def test_dead_code_removed_from_orchestrator():
    """도달 불가 코드가 없는지 AST로 확인"""
    source_path = Path(__file__).parents[2] / "builder" / "orchestrator.py"
    source = source_path.read_text()
    tree = ast.parse(source)

    # _fix_via_claude 메서드에서 except 블록 이후 if 블록이 없어야 함
    # 단순히 파싱 가능한지 확인 (SyntaxError 없음)
    assert tree is not None

    # 도달 불가 코드 패턴: except 블록 이후의 독립적 if/return 블록
    # orchestrator.py 소스에서 dead code 라인 없음 확인
    lines = source.splitlines()
    # 199-206줄 패턴 (except 블록 이후 if result.returncode == 0) 없어야 함
    dead_code_pattern = False
    in_except = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if "except" in stripped and ("TimeoutExpired" in stripped or "FileNotFoundError" in stripped):
            in_except = True
        elif in_except and stripped.startswith("if result.returncode"):
            dead_code_pattern = True
            break
        elif in_except and (stripped.startswith("def ") or stripped.startswith("return ") or
                             stripped.startswith("#") or not stripped):
            pass
        elif in_except and stripped and not stripped.startswith("#"):
            in_except = False

    assert not dead_code_pattern, "Dead code detected in orchestrator.py"
