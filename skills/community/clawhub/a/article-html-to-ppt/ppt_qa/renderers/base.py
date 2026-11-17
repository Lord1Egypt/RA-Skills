from __future__ import annotations

import platform
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Protocol


@dataclass
class RenderResult:
    status: str
    engine: Optional[str]
    engine_version: Optional[str]
    pdf_path: Optional[Path]
    slide_images: list[Path] = field(default_factory=list)
    logs: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    slide_count_rendered: int = 0


class PptxRenderer(Protocol):
    name: str

    def is_available(self) -> bool:
        ...

    def version(self) -> Optional[str]:
        ...

    def render(
        self,
        pptx_path: Path,
        output_dir: Path,
        *,
        timeout_seconds: int,
    ) -> RenderResult:
        ...


class RendererUnavailable(ValueError):
    pass


def elapsed_since(started: float) -> float:
    return round(time.monotonic() - started, 3)


def _platform_auto_order() -> list[str]:
    system = platform.system().lower()
    if system == "darwin":
        # Keynote is a future adapter: it is intentionally skipped here until
        # it can be proven to produce real PPTX exports reliably.
        return ["powerpoint_macos", "libreoffice"]
    if system == "windows":
        return ["powerpoint_windows", "libreoffice"]
    return ["libreoffice"]


def _renderer_by_name(name: str) -> PptxRenderer:
    if name == "libreoffice":
        from .libreoffice import LibreOfficeRenderer

        return LibreOfficeRenderer()
    if name == "powerpoint_macos":
        from .powerpoint_macos import PowerPointMacOSRenderer

        return PowerPointMacOSRenderer()
    if name == "powerpoint_windows":
        from .powerpoint_windows import PowerPointWindowsRenderer

        return PowerPointWindowsRenderer()
    raise RendererUnavailable(f"Unknown renderer engine: {name}")


def select_renderer(engine: str) -> Optional[PptxRenderer]:
    if os.environ.get("PPTSMITH_TEST_RENDERERS") == "none":
        return None
    if engine == "auto":
        for name in _platform_auto_order():
            renderer = _renderer_by_name(name)
            if renderer.is_available():
                return renderer
        return None
    renderer = _renderer_by_name(engine)
    return renderer if renderer.is_available() else None
