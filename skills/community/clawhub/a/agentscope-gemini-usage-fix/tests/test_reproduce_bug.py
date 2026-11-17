"""Tests for agentscope-gemini-usage-fix."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from reproduce_bug import main


def test_reproduce_bug_fails_without_fix():
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 1
