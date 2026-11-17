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
            # Registration probe only: availability must not start an application.
            import pythoncom  # type: ignore[import-not-found]

            pythoncom.CLSIDFromProgID("PowerPoint.Application")
            return True
        except Exception:
            return False

    def version(self) -> Optional[str]:
        if platform.system().lower() != "windows":
            return None
        try:
            import win32com.client  # type: ignore[import-not-found]

            # Do not start an idle instance just to read its version, nor Quit
            # an application that may belong to the user or an active render.
            app = win32com.client.GetActiveObject("PowerPoint.Application")
            return str(getattr(app, "Version", "") or "") or None
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
        version = None
        status = "failed"
        try:
            app = self._powerpoint()
            try:
                version = str(getattr(app, "Version", "") or "") or None
            except Exception:
                pass  # Optional metadata must not prevent a document export.
            # Untitled creates a new copy, even if the source is already open.
            # Only that returned document belongs to us; the application does
            # not. Dispatch (and even DispatchEx with singleton COM servers)
            # is not proof of process ownership, so never Quit it.
            presentation = app.Presentations.Open(
                str(pptx_path), ReadOnly=True, Untitled=True, WithWindow=False)
            for index, slide in enumerate(presentation.Slides, start=1):
                image = slides_dir / f"slide-{index:03d}.png"
                slide.Export(str(image), "PNG")
                if image.exists():
                    images.append(image)
                else:
                    errors.append(f"RENDER_IMAGE_MISSING: slide {index}")
            status = "passed" if images and not errors else "failed"
        except Exception as exc:
            errors.append(f"RENDER_EXPORT_FAILED: {exc}")
        finally:
            if presentation is not None:
                try:
                    presentation.Close()
                except Exception as exc:
                    errors.append(f"RENDER_CLOSE_FAILED: {exc}")
                    status = "failed"
        return RenderResult(status, self.name, version, None, images, [], errors,
                            elapsed_since(started), len(images))
