"""PDF utilities for splitting and processing PDF files."""

import logging
import unicodedata
from pathlib import Path

import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by normalizing Unicode characters and transliterating to ASCII.

    This handles special characters like é, à, etc. by:
    1. Normalizing Unicode (NFD) to separate base characters from combining marks
    2. Transliterating accented characters to ASCII equivalents
    3. Removing spaces and filesystem-unsafe characters

    Args:
        filename: Original filename (without extension)

    Returns:
        Sanitized filename safe for filesystem and encoding operations
    """
    # Normalize Unicode to NFD (decomposed form)
    normalized = unicodedata.normalize("NFD", filename)

    # Remove combining marks (accents)
    ascii_chars = []
    for char in normalized:
        if unicodedata.category(char) != "Mn":
            ascii_chars.append(char)

    # Join and remove spaces
    sanitized = "".join(ascii_chars).replace(" ", "")

    # Replace filesystem-unsafe characters with underscore
    unsafe_chars = r'/\\:*?"<>|'
    sanitized = "".join("_" if c in unsafe_chars else c for c in sanitized)

    # Keep only alphanumeric, underscore, and hyphen
    final = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in sanitized)

    return final


def split_pdf_to_single_pages(pdf_path: Path, output_folder: Path) -> list[Path]:
    """
    Split a PDF into single-page PDFs (idempotent - skips existing files).

    Args:
        pdf_path: Path to the source PDF file
        output_folder: Directory to save single-page PDFs

    Returns:
        List of paths to single-page PDF files
    """
    output_folder.mkdir(parents=True, exist_ok=True)

    pdf_document = fitz.open(str(pdf_path))
    output_paths = []

    base_filename = sanitize_filename(pdf_path.stem.strip())
    pages_created = 0
    pages_skipped = 0

    for page_num in range(pdf_document.page_count):
        output_path = output_folder / f"{base_filename}_page_{page_num + 1}.pdf"

        # Idempotent check: skip if already exists
        if output_path.exists():
            output_paths.append(output_path)
            pages_skipped += 1
            continue

        # Create new single-page PDF
        new_pdf = fitz.open()
        new_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
        new_pdf.save(str(output_path))
        new_pdf.close()

        output_paths.append(output_path)
        pages_created += 1

    pdf_document.close()

    if pages_skipped > 0:
        logger.debug(
            f"Split PDF: {pages_created} pages created, {pages_skipped} already existed"
        )

    return output_paths
