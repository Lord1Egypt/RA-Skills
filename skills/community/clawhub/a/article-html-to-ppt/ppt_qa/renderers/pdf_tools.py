from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def rasterize_pdf_to_pngs(
    pdf_path: Path,
    slides_dir: Path,
    *,
    dpi: int = 144,
    timeout_seconds: int = 300,
) -> tuple[list[Path], list[str]]:
    slides_dir.mkdir(parents=True, exist_ok=True)
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        return [], [
            "PDF rasterization unavailable: pdftoppm is not on PATH and Pillow cannot reliably rasterize PDFs without a PDF backend."
        ]

    output_prefix = slides_dir / "slide"
    try:
        completed = subprocess.run(
            [pdftoppm, "-png", "-r", str(dpi), str(pdf_path), str(output_prefix)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return [], ["RENDER_TIMEOUT: PDF to PNG rasterization timed out."]

    warnings: list[str] = []
    if completed.stdout.strip():
        warnings.append(completed.stdout.strip())
    if completed.stderr.strip():
        warnings.append(completed.stderr.strip())
    if completed.returncode != 0:
        warnings.append(f"RENDER_EXPORT_FAILED: pdftoppm exited with code {completed.returncode}.")
        return [], warnings

    images = sorted(slides_dir.glob("slide-*.png"), key=_pdftoppm_slide_number)
    renamed: list[Path] = []
    for index, image in enumerate(images, start=1):
        target = slides_dir / f"slide-{index:03d}.png"
        if image != target:
            image.replace(target)
        renamed.append(target)
    return renamed, warnings


def _pdftoppm_slide_number(path: Path) -> int:
    try:
        return int(path.stem.rsplit("-", 1)[1])
    except (IndexError, ValueError):
        return 0
