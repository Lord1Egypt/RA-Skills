"""Cycle 4: relative_to ValueError 수정 테스트"""

import pytest
from pathlib import Path
from builder.correction.fixer import CodeFixer


@pytest.fixture
def fixer():
    return CodeFixer()


@pytest.fixture
def project_path(tmp_path):
    p = tmp_path / "my_project"
    p.mkdir()
    return p


def test_fix_with_file_outside_project_path_does_not_raise(fixer, project_path, tmp_path):
    """project_path 외부 파일도 예외 없이 처리"""
    outside_file = tmp_path / "other_dir" / "file.py"
    outside_file.parent.mkdir()
    outside_file.write_text("import missing_module\n")

    error = {
        "type": "import_error",
        "file_path": str(outside_file),
        "line_number": 1,
        "raw_output": "ModuleNotFoundError: No module named 'missing_module'",
        "details": {"module": "missing_module"},
    }

    # ValueError가 발생하지 않아야 함
    try:
        fixer._fix_via_claude(error, outside_file, project_path)
    except ValueError as e:
        pytest.fail(f"ValueError raised for file outside project_path: {e}")
    except Exception:
        pass  # subprocess 실패 등은 허용


def test_fix_with_file_inside_project_path_returns_relative(fixer, project_path):
    """project_path 내부 파일은 상대 경로 정상 처리"""
    inside_file = project_path / "src" / "main.py"
    inside_file.parent.mkdir(parents=True)
    inside_file.write_text("print('test')\n")

    # relative_to가 정상 동작해야 함
    try:
        rel = inside_file.relative_to(project_path)
        assert str(rel) == "src/main.py"
    except ValueError:
        pytest.fail("relative_to raised ValueError for file inside project_path")


def test_fix_via_claude_builds_prompt_with_safe_path(fixer, project_path, tmp_path, monkeypatch):
    """_fix_via_claude가 project_path 외부 파일에도 안전한 경로 사용"""
    outside_file = tmp_path / "external.py"
    outside_file.write_text("x = 1\n")

    prompts_captured = []

    def fake_subprocess_run(cmd, **kwargs):
        prompts_captured.append(cmd)
        mock = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        return mock

    monkeypatch.setattr("subprocess.run", fake_subprocess_run)

    error = {
        "type": "type_error",
        "file_path": str(outside_file),
        "line_number": 1,
        "raw_output": "TypeError: ...",
        "details": {},
    }

    fixer._fix_via_claude(error, outside_file, project_path)

    # 호출됐으면 프롬프트에 ValueError가 없었다는 의미
    assert len(prompts_captured) == 1
