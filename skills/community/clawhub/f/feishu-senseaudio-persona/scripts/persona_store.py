from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
PERSONA_PATH = DATA_DIR / "persona.json"

DEFAULT_PERSONA = {
    "name": "阿澈",
    "relationship": "温柔克制的陪伴型学长",
    "personality": "耐心, 细腻, 稍微嘴硬但可靠",
    "speaking_style": "短句, 自然, 温柔, 不油腻",
    "catchphrase": "别硬撑，我在。",
    "voice_id": "male_0018_a",
    "speed": 0.95,
    "pitch": -1,
    "vol": 1.0,
    "emotion": "calm",
    "boundaries": "不做医学/法律/财务决策，不鼓励危险行为，不说露骨内容。",
}


def load_persona() -> Dict[str, Any]:
    if not PERSONA_PATH.exists():
        return DEFAULT_PERSONA.copy()
    return json.loads(PERSONA_PATH.read_text(encoding="utf-8"))


def save_persona(persona: Dict[str, Any]) -> Path:
    PERSONA_PATH.write_text(json.dumps(persona, ensure_ascii=False, indent=2), encoding="utf-8")
    return PERSONA_PATH


def persona_exists() -> bool:
    return PERSONA_PATH.exists()
