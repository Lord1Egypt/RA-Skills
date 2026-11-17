"""Tests for validate_project.py"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from validate_project import validate, find_project_root


def test_find_project_root(tmp_path: Path):
    root = tmp_path / "my-project"
    root.mkdir()
    (root / "pyproject.toml").write_text("", encoding="utf-8")
    found = find_project_root(root / "src")
    assert found == root


def test_validate_pass(tmp_path: Path):
    root = tmp_path / "project"
    root.mkdir()
    (root / "pyproject.toml").write_text("dependencies = ['agentscope']\n", encoding="utf-8")
    (root / ".env").write_text("OPENAI_API_KEY=\n", encoding="utf-8")
    (root / "main.py").write_text("import agentscope\n", encoding="utf-8")
    assert validate(root) == 0


def test_validate_fail_missing_pyproject(tmp_path: Path):
    root = tmp_path / "project"
    root.mkdir()
    assert validate(root) == 1
