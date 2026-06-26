from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from app.config import settings
from app.database.calibre_db import CalibreDB
from app.database.postgres_db import postgres_db
from app.services.book_service import book_service
from app.utils.logger import get_logger

logger = get_logger(__name__)


SUPPORTED_TARGET_FORMATS = {
    "AZW3",
    "DOCX",
    "DJVU",
    "EPUB",
    "FB2",
    "HTML",
    "HTMLZ",
    "LIT",
    "LRF",
    "MOBI",
    "PDB",
    "PDF",
    "RB",
    "RTF",
    "SNB",
    "TCR",
    "TXT",
}


class BookResolutionError(ValueError):
    """Raised when a request does not identify exactly one book."""


class BookNotFoundError(LookupError):
    """Raised when the requested book is not found."""


class FormatConversionError(RuntimeError):
    """Raised when conversion or Calibre registration fails."""


@dataclass(frozen=True)
class ResolvedBook:
    book_id: Optional[int]
    calibre_id: int
    title: str


class FormatConversionService:
    """Convert a Calibre book format and register it back in Calibre."""

    def __init__(self) -> None:
        self.calibre_db = CalibreDB()
        self.library_path = Path(settings.CALIBRE_LIBRARY_PATH)

    def convert_and_register(
        self,
        *,
        target_format: str,
        book_id: Optional[int] = None,
        calibre_id: Optional[int] = None,
        title: Optional[str] = None,
        source_format: Optional[str] = None,
        force: bool = False,
    ) -> Dict[str, Any]:
        target_format = self._normalize_format(target_format)
        source_format = self._normalize_format(source_format) if source_format else None
        book = self._resolve_book(book_id=book_id, calibre_id=calibre_id, title=title)

        existing_target = self.calibre_db.get_book_file_info(
            book.calibre_id,
            preferred_format=target_format,
        )
        if existing_target and target_format in existing_target.get("available_formats", []) and not force:
            output_path = self.library_path / existing_target["path"]
            return {
                "success": True,
                "message": f"{target_format} is already registered for book {book.calibre_id}.",
                "book_id": book.book_id,
                "calibre_id": book.calibre_id,
                "title": book.title,
                "source_format": existing_target.get("format"),
                "target_format": target_format,
                "output_path": str(output_path),
                "already_available": True,
                "registered": True,
                "synced_count": 0,
            }

        source_info = self.calibre_db.get_book_file_info(
            book.calibre_id,
            preferred_format=source_format,
        )
        if not source_info:
            raise BookNotFoundError(f"No source format found for Calibre book {book.calibre_id}.")

        input_path = self.library_path / source_info["path"]
        if not input_path.exists():
            raise BookNotFoundError(f"Source file not found: {input_path}")

        ebook_convert = shutil.which("ebook-convert")
        calibredb = shutil.which("calibredb")
        if not ebook_convert:
            raise FormatConversionError("ebook-convert was not found in PATH.")
        if not calibredb:
            raise FormatConversionError("calibredb was not found in PATH.")

        with tempfile.TemporaryDirectory(prefix="openclaw-calibre-converter-") as tmp_dir:
            output_path = Path(tmp_dir) / f"{input_path.stem}.{target_format.lower()}"
            self._run_command(
                [
                    ebook_convert,
                    str(input_path),
                    str(output_path),
                ],
                operation="ebook-convert",
            )
            if not output_path.exists():
                raise FormatConversionError(f"Conversion finished without creating {output_path}.")

            add_format_command = [
                calibredb,
                "add_format",
                str(book.calibre_id),
                str(output_path),
                "--library-path",
                str(self.library_path),
            ]
            self._run_command(add_format_command, operation="calibredb add_format")

        synced_count = book_service.sync_books_from_calibre()
        registered_info = self.calibre_db.get_book_file_info(
            book.calibre_id,
            preferred_format=target_format,
        )
        registered = (
            registered_info is not None
            and registered_info.get("format") == target_format
            and target_format in registered_info.get("available_formats", [])
        )
        registered_path = (
            str(self.library_path / registered_info["path"])
            if registered
            else None
        )
        postgres_book = postgres_db.get_book_by_calibre_id(book.calibre_id)

        return {
            "success": True,
            "message": f"Converted and registered {target_format} for book {book.calibre_id}.",
            "book_id": postgres_book.get("id") if postgres_book else book.book_id,
            "calibre_id": book.calibre_id,
            "title": book.title,
            "source_format": source_info.get("format"),
            "target_format": target_format,
            "output_path": registered_path,
            "already_available": False,
            "registered": registered,
            "synced_count": synced_count,
        }

    def _resolve_book(
        self,
        *,
        book_id: Optional[int],
        calibre_id: Optional[int],
        title: Optional[str],
    ) -> ResolvedBook:
        identifiers = [book_id is not None, calibre_id is not None, bool(title and title.strip())]
        if sum(identifiers) != 1:
            raise BookResolutionError("Provide exactly one identifier: book_id, calibre_id, or title.")

        if book_id is not None:
            book = postgres_db.get_book_by_id(book_id)
            if not book:
                raise BookNotFoundError(f"Book ID {book_id} was not found.")
            if not book.get("calibre_id"):
                raise BookResolutionError(f"Book ID {book_id} has no Calibre ID.")
            return ResolvedBook(
                book_id=book.get("id"),
                calibre_id=int(book["calibre_id"]),
                title=book["title"],
            )

        if calibre_id is not None:
            calibre_book = self.calibre_db.get_book_by_id(calibre_id)
            if not calibre_book:
                raise BookNotFoundError(f"Calibre book ID {calibre_id} was not found.")
            postgres_book = postgres_db.get_book_by_calibre_id(calibre_id)
            return ResolvedBook(
                book_id=postgres_book.get("id") if postgres_book else None,
                calibre_id=int(calibre_id),
                title=calibre_book["title"],
            )

        exact_title = title.strip()
        matches = [
            book
            for book in self.calibre_db.get_all_books()
            if book.get("title") == exact_title
        ]
        if not matches:
            raise BookNotFoundError(f"No Calibre book found with exact title: {exact_title}")
        if len(matches) > 1:
            ids = [book["calibre_id"] for book in matches]
            raise BookResolutionError(
                f"Title matches multiple Calibre books. Provide one calibre_id: {ids}"
            )

        calibre_book = matches[0]
        postgres_book = postgres_db.get_book_by_calibre_id(calibre_book["calibre_id"])
        return ResolvedBook(
            book_id=postgres_book.get("id") if postgres_book else None,
            calibre_id=int(calibre_book["calibre_id"]),
            title=calibre_book["title"],
        )

    @staticmethod
    def _normalize_format(value: str) -> str:
        normalized = (value or "").strip().lstrip(".").upper()
        if not normalized:
            raise BookResolutionError("target_format is required.")
        if normalized not in SUPPORTED_TARGET_FORMATS:
            raise BookResolutionError(f"Unsupported target format: {normalized}")
        return normalized

    @staticmethod
    def _run_command(command: list[str], *, operation: str) -> None:
        logger.info("%s started", operation, extra={"operation": operation})
        try:
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=900,
            )
        except subprocess.TimeoutExpired as exc:
            raise FormatConversionError(f"{operation} timed out.") from exc

        if completed.returncode != 0:
            stderr = (completed.stderr or "").strip()
            stdout = (completed.stdout or "").strip()
            detail = stderr or stdout or f"exit code {completed.returncode}"
            raise FormatConversionError(f"{operation} failed: {detail}")

        logger.info("%s finished", operation, extra={"operation": operation})


format_conversion_service = FormatConversionService()
