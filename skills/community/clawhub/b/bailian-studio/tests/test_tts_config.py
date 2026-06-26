from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1] / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from env import get_tts_config


def test_get_tts_config_has_model():
    cfg = get_tts_config()
    assert cfg["model"]
