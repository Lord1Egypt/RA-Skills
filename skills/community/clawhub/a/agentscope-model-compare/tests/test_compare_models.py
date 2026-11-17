"""Tests for compare_models.py"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from compare_models import main


def test_main_requires_api_key(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "FAIL" in captured.out
