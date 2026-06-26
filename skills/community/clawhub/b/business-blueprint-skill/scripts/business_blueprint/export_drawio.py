from __future__ import annotations

from pathlib import Path
from typing import Any

from renderers import build_drawio_spec, render_drawio

_WATERMARK = "<!-- business-blueprint-skill v{version} -->"


def _get_version() -> str:
    try:
        from importlib.metadata import version
        return version("business-blueprint-skill")
    except Exception:
        return "0.1.0"


def export_drawio(blueprint: dict[str, Any], target: Path) -> None:
    spec = build_drawio_spec(blueprint)
    xml = render_drawio(spec)
    watermark = _WATERMARK.format(version=_get_version())
    target.write_text(watermark + "\n" + xml, encoding="utf-8")
