"""Service layer for OCR Cloud module - Gemini cloud OCR processing."""

import asyncio
import logging
from pathlib import Path

from gemini_client import get_gemini_client, GeminiClient
from utils import split_pdf_to_single_pages
from file_service import get_file_service, FileService
from config import settings

logger = logging.getLogger(__name__)

from schemas import OcrPageSchema, OcrResultSchema


class OcrCloudService:
    """Service for processing PDFs with Gemini cloud OCR."""

    def __init__(
        self,
        gemini_client: GeminiClient | None = None,
        file_service: FileService | None = None,
        max_concurrent: int | None = None,
    ):
        self._gemini_client = gemini_client
        self._file_service = file_service
        self._max_concurrent = max_concurrent or settings.ocr_max_concurrent

    @property
    def gemini_client(self) -> GeminiClient:
        """Lazy initialization of Gemini client."""
        if self._gemini_client is None:
            self._gemini_client = get_gemini_client()
        return self._gemini_client

    @property
    def file_service(self) -> FileService:
        """Lazy initialization of file service."""
        if self._file_service is None:
            self._file_service = get_file_service()
        return self._file_service

    async def process_page(
        self,
        page_path: Path,
        page_num: int,
        semaphore: asyncio.Semaphore,
    ) -> OcrPageSchema:
        """
        Process a single page with Gemini OCR.

        Args:
            page_path: Path to single-page PDF
            page_num: Page number (1-indexed)
            semaphore: Semaphore for concurrency control

        Returns:
            OcrPageSchema with extracted text
        """
        async with semaphore:
            try:
                logger.debug(f"Processing page {page_num}: {page_path}")

                # Run OCR (async wrapper around sync Gemini API)
                text = await self.gemini_client.ocr_pdf_page_async(page_path)

                return OcrPageSchema(
                    page_number=page_num,
                    text=text,
                    status="success",
                    char_count=len(text),
                )

            except Exception as e:
                logger.error(f"Error processing page {page_num}: {e}")
                return OcrPageSchema(
                    page_number=page_num,
                    text="",
                    status="error",
                    char_count=0,
                    error=str(e),
                )

    async def process_pdf(
        self,
        pdf_path: Path,
        max_pages: int | None = None,
    ) -> OcrResultSchema:
        """
        Process a PDF document with Gemini OCR.

        Args:
            pdf_path: Path to the PDF file
            max_pages: Maximum pages to process (for testing)

        Returns:
            OcrResultSchema with all page results
        """
        logger.info(f"Processing PDF: {pdf_path}")

        # Create temp folder for split pages
        temp_folder = self.file_service.create_temp_folder(prefix="ocr")

        try:
            # Split PDF into single pages (already in page order)
            page_paths = split_pdf_to_single_pages(pdf_path, temp_folder)
            logger.debug(f"Split PDF into {len(page_paths)} pages")

            # Apply max_pages limit if specified
            if max_pages and len(page_paths) > max_pages:
                logger.info(f"Limiting to {max_pages} pages (total: {len(page_paths)})")
                page_paths = page_paths[:max_pages]

            # Create semaphore for concurrency control
            semaphore = asyncio.Semaphore(self._max_concurrent)

            # Process all pages concurrently (page_num from list position, 1-indexed)
            tasks = []
            for page_num, page_path in enumerate(page_paths, start=1):
                task = self.process_page(page_path, page_num, semaphore)
                tasks.append(task)

            # Wait for all pages to complete
            logger.info(
                f"Processing {len(tasks)} pages concurrently (max {self._max_concurrent} concurrent)"
            )
            page_results = await asyncio.gather(*tasks)

            # Calculate totals
            total_chars = sum(p.char_count for p in page_results)
            failed_pages = sum(1 for p in page_results if p.status == "error")
            overall_status = "success" if failed_pages == 0 else "partial"
            logger.info(
                f"OCR processing complete: {len(page_results)} pages, {total_chars} chars extracted, {failed_pages} failed"
            )

            return OcrResultSchema(
                pdf_name=pdf_path.name,
                total_pages=len(page_results),
                pages=list(page_results),
                total_chars=total_chars,
                status=overall_status,
            )

        finally:
            # Cleanup temp folder
            self.file_service.cleanup_temp_folder(temp_folder)

    async def process_multiple_pdfs(
        self,
        pdf_paths: list[Path],
        max_pages: int | None = None,
    ) -> list[OcrResultSchema]:
        """
        Process multiple PDF documents.

        Args:
            pdf_paths: List of PDF file paths
            max_pages: Maximum pages per document (for testing)

        Returns:
            List of OcrResultSchema for each document
        """
        results = []
        for pdf_path in pdf_paths:
            try:
                result = await self.process_pdf(pdf_path, max_pages)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing {pdf_path}: {e}")
                results.append(
                    OcrResultSchema(
                        pdf_name=pdf_path.name,
                        total_pages=0,
                        pages=[],
                        total_chars=0,
                        status="error",
                    )
                )

        return results


# Singleton instance
_ocr_cloud_service: OcrCloudService | None = None


def get_ocr_cloud_service() -> OcrCloudService:
    """Get or create singleton OcrCloudService instance."""
    global _ocr_cloud_service
    if _ocr_cloud_service is None:
        _ocr_cloud_service = OcrCloudService()
    return _ocr_cloud_service
