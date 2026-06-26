from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from renderers import build_excalidraw_spec, render_excalidraw

_WATERMARK_KEY = "_business_blueprint_skill"


def _get_version() -> str:
    try:
        from importlib.metadata import version
        return version("business-blueprint-skill")
    except Exception:
        return "0.1.0"


def export_excalidraw(blueprint: dict[str, Any], target: Path) -> None:
    spec = build_excalidraw_spec(blueprint)
    content = render_excalidraw(spec)
    data = json.loads(content)
    data[_WATERMARK_KEY] = f"v{_get_version()}"
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
