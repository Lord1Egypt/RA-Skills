import pytest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1] / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from env import get_dashscope_key


def test_missing_key_raises(monkeypatch, tmp_path: Path):
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    env_path = tmp_path / "bailian.env"
    with pytest.raises(RuntimeError):
        get_dashscope_key(env_path=env_path)


def test_env_overrides_file(monkeypatch, tmp_path: Path):
    env_path = tmp_path / "bailian.env"
    env_path.write_text("DASHSCOPE_API_KEY=from-file", encoding="utf-8")
    monkeypatch.setenv("DASHSCOPE_API_KEY", "from-env")
    assert get_dashscope_key(env_path=env_path) == "from-env"
