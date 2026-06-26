import pytest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1] / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from oss_upload import upload_image


def test_missing_oss_config_raises(monkeypatch, tmp_path: Path):
    monkeypatch.delenv("OSS_ACCESS_KEY", raising=False)
    with pytest.raises(RuntimeError):
        upload_image(tmp_path / "a.png")
