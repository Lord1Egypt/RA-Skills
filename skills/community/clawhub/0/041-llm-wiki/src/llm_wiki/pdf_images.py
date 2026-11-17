"""Extract embedded raster images and vector figures from PDFs.

Uses PyMuPDF to:

- Extract embedded raster images via ``get_images`` / ``extract_image``.
- Detect vector graphics clusters via ``get_drawings`` / ``cluster_drawings``,
  then render each cluster to an image so LLMs can inspect charts and diagrams.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from pathlib import Path

import fitz

logger = logging.getLogger(__name__)

# Vector graphic clusters smaller than this in either dimension are treated as
# text decorations or stray lines and ignored.
MIN_FIGURE_SIZE_PX = 5


def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def parse_pages(doc: fitz.Document, pages: str | None) -> Iterable[int]:
    """Parse a page range string into zero-based page indices.

    Supported formats:

    - ``None``: all pages.
    - ``"3"``: single 1-based page number.
    - ``"1-10"``: inclusive 1-based range.
    """
    total = len(doc)
    if not pages:
        return range(total)

    def _parse_int(value: str, label: str) -> int:
        try:
            return int(value)
        except ValueError as exc:
            raise ValueError(
                f"Invalid page range {pages!r}: {label} must be an integer"
            ) from exc

    if "-" in pages:
        start_raw, end_raw = pages.split("-", 1)
        start = _parse_int(start_raw, "start")
        end = _parse_int(end_raw, "end")
        start_idx = max(0, start - 1)
        end_idx = min(total, end)
        return range(start_idx, end_idx)

    page = _parse_int(pages, "page")
    page_idx = page - 1
    if page_idx < 0 or page_idx >= total:
        return range(0)
    return range(page_idx, page_idx + 1)


def extract_embedded_images(
    doc: fitz.Document,
    output_dir: Path,
    pages: str | None = None,
) -> list[dict]:
    """Extract embedded raster images from a PDF.

    Args:
        doc: Open PyMuPDF document.
        output_dir: Directory to write extracted images.
        pages: Optional page range, e.g. ``"1-10"`` or ``"3"``.

    Returns:
        Metadata for each extracted image: page, index, path, width, height, ext.
    """
    output_dir = _ensure_dir(output_dir)
    results: list[dict] = []
    seen_xrefs: set[int] = set()

    for page_num in parse_pages(doc, pages):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            # A single image may be reused across pages; extract only once.
            if xref in seen_xrefs:
                continue
            seen_xrefs.add(xref)

            try:
                base_image = doc.extract_image(xref)
            except Exception as exc:  # pragma: no cover - defensive
                logger.warning(
                    "Failed to extract image xref %s: %s", xref, exc, exc_info=True
                )
                continue

            ext = base_image["ext"]
            filename = f"p{page_num + 1:03d}_img{img_index:03d}.{ext}"
            filepath = output_dir / filename
            filepath.write_bytes(base_image["image"])

            results.append(
                {
                    "page": page_num + 1,
                    "index": img_index,
                    "path": str(filepath),
                    "width": base_image.get("width"),
                    "height": base_image.get("height"),
                    "ext": ext,
                    "xref": xref,
                }
            )

    return results


def extract_vector_figures(
    doc: fitz.Document,
    output_dir: Path,
    pages: str | None = None,
    dpi: int = 200,
) -> list[dict]:
    """Detect vector graphic clusters and render each as an image.

    Args:
        doc: Open PyMuPDF document.
        output_dir: Directory to write rendered figures.
        pages: Optional page range, e.g. ``"1-10"`` or ``"3"``.
        dpi: Resolution for rendering clusters.

    Returns:
        Metadata for each rendered figure: page, index, path, bbox.
    """
    output_dir = _ensure_dir(output_dir)
    results: list[dict] = []

    for page_num in parse_pages(doc, pages):
        page = doc.load_page(page_num)
        try:
            drawings = page.get_drawings()
            clusters = page.cluster_drawings(drawings=drawings)
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning(
                "Failed to cluster drawings on page %s: %s",
                page_num + 1,
                exc,
                exc_info=True,
            )
            continue

        for cluster_index, bbox in enumerate(clusters):
            # Skip tiny clusters that are likely text decorations or stray lines.
            if bbox.width < MIN_FIGURE_SIZE_PX or bbox.height < MIN_FIGURE_SIZE_PX:
                continue

            filename = f"p{page_num + 1:03d}_fig{cluster_index:03d}.png"
            filepath = output_dir / filename
            pix = None
            try:
                pix = page.get_pixmap(clip=bbox, dpi=dpi)
                pix.save(str(filepath))
            except Exception as exc:  # pragma: no cover - defensive
                logger.warning(
                    "Failed to render figure on page %s: %s",
                    page_num + 1,
                    exc,
                    exc_info=True,
                )
                continue
            finally:
                pix = None

            results.append(
                {
                    "page": page_num + 1,
                    "index": cluster_index,
                    "path": str(filepath),
                    "bbox": (bbox.x0, bbox.y0, bbox.x1, bbox.y1),
                }
            )

    return results


def extract_pdf_images(
    pdf_path: str | Path,
    output_dir: str | Path,
    pages: str | None = None,
    dpi: int = 200,
) -> dict:
    """Extract both embedded raster images and vector figures from a PDF.

    Args:
        pdf_path: Path to the PDF file.
        output_dir: Directory to write extracted images and figures.
        pages: Optional page range, e.g. ``"1-10"`` or ``"3"``.
        dpi: Resolution for rendering vector figures.

    Returns:
        Dict with ``"images"`` and ``"figures"`` metadata lists.
    """
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    with fitz.open(str(pdf_path)) as doc:
        images = extract_embedded_images(doc, output_dir / "images", pages)
        figures = extract_vector_figures(doc, output_dir / "figures", pages, dpi)

    return {"images": images, "figures": figures}
