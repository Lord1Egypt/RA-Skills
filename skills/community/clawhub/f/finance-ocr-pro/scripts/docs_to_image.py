"""
Document → Image Converter

Converts various document formats into high-quality per-page images
suitable for OCR and multi-modal AI processing.

Supported formats:
    PDF, DOC, DOCX, PPT, PPTX, ODP, ODT, RTF, WPS, KEY, PAGES,
    PNG, JPG, JPEG (copied directly to output)

Usage:
    # As a module
    from docs_to_image import document_to_images
    output_dir = document_to_images("report.docx")
    output_dir = document_to_images("slides.pptx", output_format="jpeg")

    # From CLI
    python docs_to_image.py report.docx
    python docs_to_image.py slides.pptx -f jpeg
"""

from __future__ import annotations

import io
import logging
import platform
import re
import shutil
import subprocess
import tempfile
import unicodedata
import zipfile
from contextlib import redirect_stderr
from pathlib import Path
from typing import Literal

from ocr_runtime import NullProgressReporter, ProgressReporter

logger = logging.getLogger(__name__)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Constants
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Maps extension → conversion category
SUPPORTED_EXTENSIONS: dict[str, str] = {
    ".pdf":   "pdf",
    ".doc":   "office",
    ".docx":  "office",
    ".ppt":   "office",
    ".pptx":  "office",
    ".odt":   "office",
    ".odp":   "office",
    ".rtf":   "office",
    ".wps":   "office",
    ".key":   "apple",
    ".pages": "apple",
    ".png":   "image",
    ".jpg":   "image",
    ".jpeg":  "image",
    ".webp":  "image",
    ".bmp":   "image",
    ".tif":   "image",
    ".tiff":  "image",
}

ALLOWED_DPI = {72, 96, 150, 200, 300, 400, 600}
DEFAULT_DPI = 200
MAX_FILENAME_LENGTH = 80
JPEG_QUALITY = 95


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _get_platform() -> str:
    """Detect operating system: 'windows', 'macos', or 'linux'."""
    s = platform.system().lower()
    if "darwin" in s:
        return "macos"
    if "windows" in s:
        return "windows"
    if "linux" in s:
        return "linux"
    return s


def sanitize_filename(name: str, max_length: int = MAX_FILENAME_LENGTH) -> str:
    """
    Produce a filesystem-safe ASCII-friendly name from an arbitrary string.
    Returns ``'document'`` when nothing usable remains.
    """
    name = unicodedata.normalize("NFKD", name)
    name = re.sub(r"[^\w\s\-]", "_", name)
    name = re.sub(r"[\s_]+", "_", name)
    name = name.strip("_. ")[:max_length].rstrip("_. ")
    return name or "document"


def _create_output_dir(doc_name: str, base_dir: Path) -> Path:
    """
    Create ``image_outputs_{doc_name}`` inside *base_dir*.
    Appends ``_1``, ``_2``, … when the directory already exists.
    """
    safe = sanitize_filename(doc_name)
    stem = f"image_outputs_{safe}"
    candidate = base_dir / stem

    if not candidate.exists():
        candidate.mkdir(parents=True)
        return candidate

    n = 1
    while True:
        numbered = base_dir / f"{stem}_{n}"
        if not numbered.exists():
            numbered.mkdir(parents=True)
            return numbered
        n += 1


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PDF Repair
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _try_repair_pdf(pdf_path: Path, tmp_dir: Path) -> Path:
    """
    Return a usable PDF path.  If the file is corrupted, encrypted, or
    otherwise unhealthy, rebuild it page-by-page into *tmp_dir*.
    Returns the original path when no repair is needed.
    """
    import fitz  # PyMuPDF

    try:
        doc = fitz.open(pdf_path)
    except Exception:
        logger.warning("PDF cannot be opened normally; attempting repair.")
        return _force_repair_pdf(pdf_path, tmp_dir)

    try:
        if doc.needs_pass or doc.is_encrypted:
            logger.info("PDF requires password / is encrypted; attempting repair.")
            doc.close()
            return _force_repair_pdf(pdf_path, tmp_dir)
        return pdf_path
    finally:
        if not doc.is_closed:
            doc.close()


def _force_repair_pdf(src: Path, tmp_dir: Path) -> Path:
    """Re-assemble a PDF page-by-page to work around corruption."""
    import fitz

    repaired = tmp_dir / f"repaired_{src.name}"
    try:
        src_doc = fitz.open(src)
    except Exception as exc:
        raise RuntimeError(
            f"PDF is severely corrupted and cannot be repaired: {exc}"
        ) from exc

    new_doc = fitz.open()
    try:
        for i in range(src_doc.page_count):
            try:
                new_doc.insert_pdf(src_doc, from_page=i, to_page=i)
            except Exception:
                new_doc.new_page(width=595, height=842)  # A4 blank placeholder
        new_doc.save(repaired, garbage=4, deflate=True, clean=True)
    finally:
        new_doc.close()
        src_doc.close()

    return repaired


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# OOXML Repair  (docx / pptx are ZIP archives)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _try_repair_ooxml(src: Path, tmp_dir: Path) -> Path | None:
    """
    Re-zip an OOXML file to fix minor archive corruption.
    Returns repaired path on success, ``None`` otherwise.
    """
    if src.suffix.lower() not in (".docx", ".pptx"):
        return None
    try:
        repaired = tmp_dir / f"repaired_{src.name}"
        with zipfile.ZipFile(src, "r") as zin:
            with zipfile.ZipFile(repaired, "w", zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    zout.writestr(item, zin.read(item.filename))
        return repaired
    except Exception:
        return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PDF → Images
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _render_pdf_to_images(
    pdf_path: Path,
    output_dir: Path,
    base_name: str,
    fmt: str,
    dpi: int,
    tmp_dir: Path,
    reporter: ProgressReporter | None = None,
) -> tuple[int, int]:
    """
    Render every page of *pdf_path* as an image.

    Primary renderer: PyMuPDF (fitz).
    Fallback per page: pdf2image / Poppler.

    Returns ``(successes, failures)``.
    """
    import fitz

    reporter = reporter or NullProgressReporter()
    working_pdf = _try_repair_pdf(pdf_path, tmp_dir)

    try:
        doc = fitz.open(working_pdf)
    except Exception as exc:
        logger.error("Cannot open PDF '%s': %s", pdf_path.name, exc)
        return 0, 1

    file_ext = "jpg" if fmt == "jpeg" else "png"
    successes, failures = 0, 0
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)

    try:
        with redirect_stderr(io.StringIO()):
            for idx in range(doc.page_count):
                reporter.check_cancelled()
                out_file = output_dir / f"{base_name}_{idx + 1:05d}.{file_ext}"

                try:
                    pix = doc[idx].get_pixmap(matrix=mat, alpha=False)
                    _save_pixmap(pix, out_file, fmt)
                    successes += 1
                    continue
                except Exception as e:
                    logger.warning("fitz failed on page %d: %s", idx + 1, e)

                if _render_page_with_pdf2image(working_pdf, idx, out_file, fmt, dpi):
                    successes += 1
                else:
                    failures += 1
    finally:
        doc.close()

    return successes, failures


def _save_pixmap(pix, path: Path, fmt: str) -> None:
    """Write a PyMuPDF Pixmap to disk as PNG or JPEG."""
    if fmt == "png":
        pix.save(str(path))
    else:
        from PIL import Image
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        img.save(
            path, format="JPEG",
            quality=JPEG_QUALITY, subsampling=0, optimize=True,
        )


def _render_page_with_pdf2image(
    pdf_path: Path, page_idx: int, out_path: Path, fmt: str, dpi: int,
) -> bool:
    """Render a single PDF page via pdf2image (requires Poppler)."""
    try:
        from pdf2image import convert_from_path

        images = convert_from_path(
            str(pdf_path), dpi=dpi,
            first_page=page_idx + 1, last_page=page_idx + 1,
        )
        if not images:
            return False

        img = images[0]
        if fmt == "png":
            img.save(out_path, format="PNG", optimize=True)
        else:
            img.convert("RGB").save(
                out_path, format="JPEG",
                quality=JPEG_QUALITY, subsampling=0, optimize=True,
            )
        return True
    except Exception as e:
        logger.warning("pdf2image fallback failed for page %d: %s", page_idx + 1, e)
        return False


def _save_input_image(src: Path, dest: Path, fmt: str) -> None:
    """Copy or transcode a direct image input into the requested output format."""
    src_ext = src.suffix.lower()
    dest_ext = dest.suffix.lower()
    if (
        (fmt == "png" and src_ext == ".png" and dest_ext == ".png")
        or (fmt == "jpeg" and src_ext in {".jpg", ".jpeg"} and dest_ext in {".jpg", ".jpeg"})
    ):
        shutil.copy2(src, dest)
        return

    from PIL import Image

    with Image.open(src) as img:
        if fmt == "png":
            img.save(dest, format="PNG", optimize=True)
        else:
            img.convert("RGB").save(
                dest,
                format="JPEG",
                quality=JPEG_QUALITY,
                subsampling=0,
                optimize=True,
            )


def _save_input_image_frames(
    src: Path,
    output_dir: Path,
    base_name: str,
    fmt: str,
) -> int:
    """Write all frames from a direct image input and return the page count."""
    dest_ext = "jpg" if fmt == "jpeg" else "png"

    from PIL import Image, ImageSequence

    with Image.open(src) as img:
        frame_count = getattr(img, "n_frames", 1)
        if frame_count <= 1:
            dest = output_dir / f"{base_name}_00001.{dest_ext}"
            _save_input_image(src, dest, fmt)
            return 1

        written = 0
        for index, frame in enumerate(ImageSequence.Iterator(img), start=1):
            dest = output_dir / f"{base_name}_{index:05d}.{dest_ext}"
            frame_to_save = frame.copy()
            if fmt == "png":
                frame_to_save.save(dest, format="PNG", optimize=True)
            else:
                frame_to_save.convert("RGB").save(
                    dest,
                    format="JPEG",
                    quality=JPEG_QUALITY,
                    subsampling=0,
                    optimize=True,
                )
            written += 1
        return written


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Document → PDF  (high-level dispatcher)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _convert_to_pdf(
    src: Path, tmp_dir: Path, category: str, osname: str,
) -> Path:
    """Route to the correct converter based on document category."""
    if category == "pdf":
        return src
    if category == "office":
        return _office_to_pdf(src, tmp_dir, osname)
    if category == "apple":
        return _apple_to_pdf(src, tmp_dir, osname)
    raise RuntimeError("document type not supported")


# ── Office (DOC, DOCX, PPT, PPTX, ODT, ODP, RTF, WPS) ──────────────

def _office_to_pdf(src: Path, tmp_dir: Path, osname: str) -> Path:
    """
    Convert an Office document to PDF.

    Strategy:
        1. Windows → try MS Office COM automation first.
        2. All platforms → LibreOffice headless.
        3. If step 2 fails and file is OOXML → repair ZIP and retry.
    """
    if osname == "windows":
        try:
            return _office_via_com(src, tmp_dir)
        except Exception as e:
            logger.info("COM conversion unavailable (%s); trying LibreOffice.", e)

    lo_err: Exception | None = None
    try:
        return _office_via_libreoffice(src, tmp_dir, osname)
    except Exception as first_err:
        lo_err = first_err
        logger.warning("LibreOffice conversion failed: %s", first_err)

    # Last resort: repair OOXML archive corruption and retry
    repaired = _try_repair_ooxml(src, tmp_dir)
    if repaired:
        logger.info("Retrying conversion with repaired OOXML archive.")
        try:
            return _office_via_libreoffice(repaired, tmp_dir, osname)
        except Exception as repair_err:
            logger.warning("Repaired OOXML also failed: %s", repair_err)

    raise RuntimeError(
        f"Cannot convert '{src.name}' to PDF: "
        "all conversion strategies exhausted"
    ) from lo_err


def _office_via_com(src: Path, tmp_dir: Path) -> Path:
    """Windows-only: convert via MS Office COM automation."""
    import win32com.client  # will raise ImportError on non-Windows

    ext = src.suffix.lower()
    dst = tmp_dir / f"{src.stem}.pdf"
    src_abs, dst_abs = str(src.resolve()), str(dst.resolve())

    if ext in {".doc", ".docx", ".odt", ".rtf", ".wps"}:
        app = win32com.client.DispatchEx("Word.Application")
        app.Visible = False
        try:
            doc = app.Documents.Open(src_abs)
            doc.ExportAsFixedFormat(dst_abs, ExportFormat=17)  # wdExportFormatPDF
            doc.Close(False)
        finally:
            app.Quit()

    elif ext in {".ppt", ".pptx", ".odp"}:
        app = win32com.client.DispatchEx("PowerPoint.Application")
        app.Visible = 1
        try:
            pres = app.Presentations.Open(src_abs, WithWindow=False)
            pres.SaveAs(dst_abs, 32)  # ppSaveAsPDF
            pres.Close()
        finally:
            app.Quit()

    else:
        raise ValueError(f"COM automation unavailable for {ext}")

    if not dst.exists():
        raise FileNotFoundError("COM conversion produced no PDF.")
    return dst


def _find_libreoffice(osname: str) -> str:
    """Locate the ``soffice`` binary.  Raises if not found."""
    well_known: dict[str, list[str]] = {
        "macos":   ["/Applications/LibreOffice.app/Contents/MacOS/soffice"],
        "linux":   ["/usr/bin/soffice", "/usr/local/bin/soffice", "/snap/bin/soffice"],
        "windows": [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ],
    }
    for p in well_known.get(osname, []):
        if Path(p).exists():
            return p

    found = shutil.which("soffice")
    if found:
        return found

    raise FileNotFoundError(
        "LibreOffice not found.  Install it to convert office documents."
    )


# Filter mapping for LibreOffice --convert-to
_LO_FILTER: dict[str, str] = {
    ".doc":  "writer_pdf_Export",
    ".docx": "writer_pdf_Export",
    ".odt":  "writer_pdf_Export",
    ".rtf":  "writer_pdf_Export",
    ".wps":  "writer_pdf_Export",
    ".ppt":  "impress_pdf_Export",
    ".pptx": "impress_pdf_Export",
    ".odp":  "impress_pdf_Export",
}


def _office_via_libreoffice(src: Path, tmp_dir: Path, osname: str) -> Path:
    """Convert an office document to PDF using LibreOffice headless mode."""
    soffice = _find_libreoffice(osname)
    filt = _LO_FILTER.get(src.suffix.lower())
    convert_arg = f"pdf:{filt}" if filt else "pdf"

    cmd = [
        soffice, "--headless", "--norestore", "--nologo",
        "--convert-to", convert_arg,
        "--outdir", str(tmp_dir),
        str(src.resolve()),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if result.returncode != 0:
        raise RuntimeError(
            f"LibreOffice failed (rc={result.returncode}): "
            f"{(result.stderr or result.stdout).strip()}"
        )

    expected = tmp_dir / f"{src.stem}.pdf"
    if expected.exists():
        return expected

    # LibreOffice sometimes tweaks the output name
    candidates = sorted(
        tmp_dir.glob(f"{src.stem}*.pdf"),
        key=lambda p: p.stat().st_mtime, reverse=True,
    )
    if candidates:
        return candidates[0]

    raise FileNotFoundError(f"LibreOffice produced no PDF for '{src.name}'.")


# ── Apple Formats (KEY, PAGES) ───────────────────────────────────────

def _apple_to_pdf(src: Path, tmp_dir: Path, osname: str) -> Path:
    """
    Export Keynote (.key) or Pages (.pages) to PDF.

    On macOS the native app is preferred (via AppleScript); all platforms
    fall back to LibreOffice, which has limited Apple-format support.
    """
    if osname == "macos":
        try:
            return _apple_via_applescript(src, tmp_dir)
        except Exception as e:
            logger.info("AppleScript export failed (%s); trying LibreOffice.", e)

    try:
        return _office_via_libreoffice(src, tmp_dir, osname)
    except Exception as exc:
        raise RuntimeError(
            f"Cannot convert Apple format '{src.suffix}': "
            "neither AppleScript nor LibreOffice succeeded"
        ) from exc


def _apple_via_applescript(src: Path, tmp_dir: Path) -> Path:
    """macOS: drive Keynote / Pages via ``osascript`` to export PDF."""
    app_map = {".key": "Keynote", ".pages": "Pages"}
    app = app_map.get(src.suffix.lower())
    if not app:
        raise ValueError(f"Not an Apple format: {src.suffix}")

    dst = tmp_dir / f"{src.stem}.pdf"
    script = (
        "on run argv\n"
        "  set srcPath to item 1 of argv\n"
        "  set dstPath to item 2 of argv\n"
        f'  tell application "{app}"\n'
        "    set theDoc to open POSIX file srcPath\n"
        "    delay 2\n"
        "    export theDoc to POSIX file dstPath as PDF\n"
        "    close theDoc saving no\n"
        "  end tell\n"
        "end run"
    )
    result = subprocess.run(
        ["osascript", "-e", script, str(src.resolve()), str(dst)],
        capture_output=True, text=True, timeout=90,
    )
    if result.returncode != 0 or not dst.exists():
        raise RuntimeError(result.stderr.strip() or "AppleScript export failed")
    return dst


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Public API
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def document_to_images(
    file_path: str | Path,
    output_dir: str | Path | None = None,
    output_format: Literal["png", "jpeg"] = "png",
    dpi: int = DEFAULT_DPI,
    reporter: ProgressReporter | None = None,
) -> Path:
    """
    Convert a document into per-page images for OCR / multi-modal AI.

    Args:
        file_path:      Path to the source document.
        output_dir:     Directory to write images into.  Created if absent.
                        When *None*, a new directory is created next to this script.
        output_format:  ``"png"`` (default, lossless) or ``"jpeg"``.
        dpi:            Render resolution.
                        Allowed: 72, 96, 150, 200 (default), 300, 400, 600.

    Returns:
        Path to the output folder containing the generated images.

    Raises:
        FileNotFoundError – source file missing or converter not installed.
        ValueError        – unsupported format, DPI, or document type.
        RuntimeError      – conversion failure on the current platform.
    """
    reporter = reporter or NullProgressReporter()
    src = Path(file_path).resolve()
    if not src.is_file():
        raise FileNotFoundError(f"File not found: {src}")

    fmt = output_format.lower().strip()
    if fmt not in ("png", "jpeg"):
        raise ValueError(
            f"Unsupported format '{output_format}'. Use 'png' or 'jpeg'."
        )
    if dpi not in ALLOWED_DPI:
        raise ValueError(
            f"Unsupported DPI {dpi}. Choose from {sorted(ALLOWED_DPI)}."
        )

    ext = src.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"document type not supported: {ext}")

    category = SUPPORTED_EXTENSIONS[ext]
    osname = _get_platform()
    base_name = sanitize_filename(src.stem)

    if output_dir is not None:
        resolved_output = Path(output_dir)
        resolved_output.mkdir(parents=True, exist_ok=True)
    else:
        try:
            script_dir = Path(__file__).resolve().parent
        except NameError:
            script_dir = Path.cwd()
        resolved_output = _create_output_dir(base_name, script_dir)

    if category == "image":
        page_count = _save_input_image_frames(src, resolved_output, base_name, fmt)
        summary = f"Done: {page_count}/{page_count} page(s) converted, 0 failed.  Output → {resolved_output}"
        logger.info(summary)
        print(summary)
        return resolved_output

    logger.info(
        "Converting '%s' (%s) → %s @ %d DPI → %s",
        src.name, osname, fmt.upper(), dpi, resolved_output,
    )

    with tempfile.TemporaryDirectory(prefix="doc2img_") as tmp:
        tmp_dir = Path(tmp)
        pdf_path = _convert_to_pdf(src, tmp_dir, category, osname)
        ok, fail = _render_pdf_to_images(
            pdf_path, resolved_output, base_name, fmt, dpi, tmp_dir, reporter=reporter,
        )

    total = ok + fail
    summary = (
        f"Done: {ok}/{total} page(s) converted, {fail} failed.  "
        f"Output → {resolved_output}"
    )
    if fail:
        logger.warning(summary)
    else:
        logger.info(summary)
    print(summary)

    return resolved_output


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="Convert documents to per-page images for OCR / AI.",
    )
    parser.add_argument("file", help="Path to the source document.")
    parser.add_argument(
        "-f", "--format",
        choices=["png", "jpeg"], default="png",
        help="Image format (default: png).",
    )
    args = parser.parse_args()

    document_to_images(args.file, output_format=args.format)
