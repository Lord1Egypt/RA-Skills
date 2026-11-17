from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Optional

from .base import RenderResult, elapsed_since
from .pdf_tools import rasterize_pdf_to_pngs


def _powerpoint_export_command(pptx_path: Path, pdf_path: Path) -> list[str]:
    script = '''
    on run argv
      set pptxPath to item 1 of argv
      set pdfPath to item 2 of argv
      tell application "Microsoft PowerPoint"
        activate
        open POSIX file pptxPath
        set activePresentation to active presentation
        save activePresentation in POSIX file pdfPath as save as PDF
        close activePresentation saving no
      end tell
    end run
    '''
    return ["osascript", "-e", script, "--", str(pptx_path), str(pdf_path)]


class PowerPointMacOSRenderer:
    name = "powerpoint_macos"
    app_path = Path("/Applications/Microsoft PowerPoint.app")

    def is_available(self) -> bool:
        return self.app_path.exists()

    def version(self) -> Optional[str]:
        info_plist = self.app_path / "Contents" / "Info"
        completed = subprocess.run(
            ["defaults", "read", str(info_plist), "CFBundleShortVersionString"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        return completed.stdout.strip() or None

    def render(
        self,
        pptx_path: Path,
        output_dir: Path,
        *,
        timeout_seconds: int,
        dpi: int = 144,
    ) -> RenderResult:
        started = time.monotonic()
        output_dir.mkdir(parents=True, exist_ok=True)
        logs_dir = output_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        slides_dir = output_dir / "slides"
        pdf_path = output_dir / "deck.pdf"
        if not self.is_available():
            return RenderResult("unavailable", self.name, None, None, errors=["RENDER_ENGINE_UNAVAILABLE"], duration_seconds=elapsed_since(started))

        try:
            completed = subprocess.run(
                _powerpoint_export_command(pptx_path, pdf_path),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            (logs_dir / "stdout.log").write_text(exc.stdout or "", encoding="utf-8")
            (logs_dir / "stderr.log").write_text(exc.stderr or "", encoding="utf-8")
            return RenderResult("failed", self.name, self.version(), None, errors=["RENDER_TIMEOUT"], duration_seconds=elapsed_since(started))

        (logs_dir / "stdout.log").write_text(completed.stdout or "", encoding="utf-8")
        (logs_dir / "stderr.log").write_text(completed.stderr or "", encoding="utf-8")
        errors: list[str] = []
        if completed.returncode != 0:
            errors.append(f"RENDER_EXPORT_FAILED: osascript exited with code {completed.returncode}.")
        if not pdf_path.exists():
            errors.append("RENDER_PDF_MISSING")
        images: list[Path] = []
        warnings: list[str] = []
        if pdf_path.exists():
            images, warnings = rasterize_pdf_to_pngs(pdf_path, slides_dir, dpi=dpi, timeout_seconds=timeout_seconds)
        status = "passed" if pdf_path.exists() and images and not errors else "failed"
        return RenderResult(status, self.name, self.version(), pdf_path if pdf_path.exists() else None, images, warnings, errors, elapsed_since(started), len(images))
