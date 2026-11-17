from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional

from .base import RenderResult, elapsed_since
from .pdf_tools import rasterize_pdf_to_pngs


class LibreOfficeRenderer:
    name = "libreoffice"

    def _soffice_path(self) -> Optional[str]:
        candidates = [
            shutil.which("soffice"),
            "/Applications/LibreOffice.app/Contents/MacOS/soffice",
            "/usr/bin/soffice",
            "/usr/local/bin/soffice",
            "/snap/bin/libreoffice",
        ]
        for candidate in candidates:
            if candidate and Path(candidate).exists():
                return str(candidate)
        return None

    def is_available(self) -> bool:
        return self._soffice_path() is not None

    def version(self) -> Optional[str]:
        soffice = self._soffice_path()
        if not soffice:
            return None
        completed = subprocess.run([soffice, "--version"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        return completed.stdout.strip() or completed.stderr.strip() or None

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
        soffice = self._soffice_path()
        if not soffice:
            return RenderResult("unavailable", self.name, None, None, errors=["RENDER_ENGINE_UNAVAILABLE"], duration_seconds=elapsed_since(started))

        try:
            completed = subprocess.run(
                [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(output_dir), str(pptx_path)],
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
        produced_pdf = output_dir / f"{pptx_path.stem}.pdf"
        target_pdf = output_dir / "deck.pdf"
        errors: list[str] = []
        warnings: list[str] = []
        if completed.returncode != 0:
            errors.append(f"RENDER_EXPORT_FAILED: soffice exited with code {completed.returncode}.")
        if produced_pdf.exists():
            if produced_pdf != target_pdf:
                produced_pdf.replace(target_pdf)
        else:
            errors.append("RENDER_PDF_MISSING")
        images: list[Path] = []
        if target_pdf.exists():
            images, warnings = rasterize_pdf_to_pngs(target_pdf, slides_dir, dpi=dpi, timeout_seconds=timeout_seconds)
        status = "passed" if target_pdf.exists() and images and not errors else "failed"
        return RenderResult(status, self.name, self.version(), target_pdf if target_pdf.exists() else None, images, warnings, errors, elapsed_since(started), len(images))
