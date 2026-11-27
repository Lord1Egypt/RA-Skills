from __future__ import annotations

import platform
import time
from pathlib import Path
from typing import Optional

from .base import RenderResult, elapsed_since


class PowerPointWindowsRenderer:
    name = "powerpoint_windows"

    def _powerpoint(self) -> object:
        import win32com.client  # type: ignore[import-not-found]

        return win32com.client.Dispatch("PowerPoint.Application")

    def is_available(self) -> bool:
        if platform.system().lower() != "windows":
            return False
        try:
            self._powerpoint()
            return True
        except Exception:
            return False

    def version(self) -> Optional[str]:
        if platform.system().lower() != "windows":
            return None
        try:
            app = self._powerpoint()
            version = str(getattr(app, "Version", "") or "")
            app.Quit()
            return version or None
        except Exception:
            return None

    def render(
        self,
        pptx_path: Path,
        output_dir: Path,
        *,
        timeout_seconds: int,
        dpi: int = 144,
    ) -> RenderResult:
        del timeout_seconds, dpi
        started = time.monotonic()
        output_dir.mkdir(parents=True, exist_ok=True)
        logs_dir = output_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        slides_dir = output_dir / "slides"
        slides_dir.mkdir(parents=True, exist_ok=True)
        if not self.is_available():
            return RenderResult("unavailable", self.name, None, None, errors=["RENDER_ENGINE_UNAVAILABLE"], duration_seconds=elapsed_since(started))

        errors: list[str] = []
        images: list[Path] = []
        app = None
        presentation = None
        try:
            app = self._powerpoint()
            presentation = app.Presentations.Open(str(pptx_path), WithWindow=False)
            for index, slide in enumerate(presentation.Slides, start=1):
                image = slides_dir / f"slide-{index:03d}.png"
                slide.Export(str(image), "PNG")
                if image.exists():
                    images.append(image)
                else:
                    errors.append(f"RENDER_IMAGE_MISSING: slide {index}")
            status = "passed" if images and not errors else "failed"
            return RenderResult(status, self.name, self.version(), None, images, [], errors, elapsed_since(started), len(images))
        except Exception as exc:
            return RenderResult("failed", self.name, self.version(), None, images, [], [f"RENDER_EXPORT_FAILED: {exc}"], elapsed_since(started), len(images))
        finally:
            if presentation is not None:
                presentation.Close()
            if app is not None:
                app.Quit()
