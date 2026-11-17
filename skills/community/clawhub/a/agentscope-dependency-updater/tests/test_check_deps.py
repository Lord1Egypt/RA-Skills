"""Tests for check_deps.py"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from check_deps import validate


def test_validate_pass(tmp_path: Path):
    root = tmp_path / "project"
    root.mkdir()
    (root / "pyproject.toml").write_text('dependencies = ["agentscope>=2.0"]\n', encoding="utf-8")
    assert validate(root) == 0


def test_validate_fail_missing_pyproject(tmp_path: Path):
    root = tmp_path / "project"
    root.mkdir()
    assert validate(root) == 1
