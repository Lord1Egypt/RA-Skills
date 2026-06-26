from pathlib import Path
from typing import List, Dict, Any, Optional
import mimetypes
import json

from app.config import settings
from app.database.calibre_db import CalibreDB
from app.database.postgres_db import postgres_db
from app.services.conversion_service import conversion_service
from app.services.openlibrary_service import openlibrary_service
from app.utils.logger import get_logger

logger = get_logger(__name__)


class BookService:
    """Service for managing book operations and synchronization."""
    
    def __init__(self):
        self.calibre_db = CalibreDB()
        self.library_path = Path(settings.CALIBRE_LIBRARY_PATH)
    
    def sync_books_from_calibre(self) -> int:
        """Synchronize books from Calibre to PostgreSQL, including removal of deleted books."""
        try:
            # Get all books from Calibre
            logger.info(
                "Starting Calibre to PostgreSQL synchronization",
                extra={"operation": "sync_start"},
            )
            calibre_books = self.calibre_db.get_all_books()
            calibre_ids = {book['calibre_id'] for book in calibre_books}
            
            synced_count = 0
            removed_count = 0
            skipped_no_file = 0
            skipped_missing_path = 0
            total = len(calibre_books)
            
            logger.info(
                f"Loaded {total} books from Calibre metadata",
                extra={"operation": "sync_loaded", "total": total},
            )

            for index, book in enumerate(calibre_books, start=1):
                calibre_id = book['calibre_id']
                
                # Get the best available file from Calibre, not only PDF.
                file_info = self.calibre_db.get_book_file_info(calibre_id)
                if not file_info:
                    skipped_no_file += 1
                    logger.warning(f"No file path found for book {calibre_id} - Title: {book['title']}")
                    continue
                
                # Build full path
                full_path = self.library_path / file_info["path"]
                
                # Check if file exists
                if not full_path.exists():
                    skipped_missing_path += 1
                    logger.warning(f"File not found for book {calibre_id} - Title: {book['title']}")
                    continue
                
                # Get additional metadata
                tags = self.calibre_db.get_book_tags(calibre_id)
                publishers = self.calibre_db.get_book_publishers(calibre_id)
                
                # Build metadata dict
                metadata = {
                    'uuid': book.get('uuid'),
                    'pubdate': book.get('pubdate'),
                    'series_index': book.get('series_index'),
                    'tags': tags,
                    'publishers': publishers,
                    'last_modified': book.get('last_modified'),
                    'selected_format': file_info["format"],
                    'available_formats': file_info["available_formats"],
                }
                
                # Insert or update in PostgreSQL
                postgres_db.insert_book(
                    calibre_id=calibre_id,
                    title=book['title'],
                    file_path=str(full_path),
                    author=book.get('authors'),
                    metadata=metadata
                )
                synced_count += 1

                if index == total or index % 500 == 0:
                    logger.info(
                        f"Sync progress: {index}/{total} scanned, {synced_count} synced",
                        extra={
                            "operation": "sync_progress",
                            "current": index,
                            "total": total,
                            "count": synced_count,
                        },
                    )
            
            # Remove books that are no longer in Calibre
            postgres_books = postgres_db.get_all_books(limit=1000000, offset=0)
            for postgres_book in postgres_books:
                postgres_calibre_id = postgres_book.get('calibre_id')
                if postgres_calibre_id not in calibre_ids:
                    # Book was removed from Calibre, remove from PostgreSQL
                    book_id = postgres_book.get('id')
                    logger.info(f"Removing book {book_id} (Calibre ID: {postgres_calibre_id}) - {postgres_book.get('title')}")
                    self._remove_book_from_postgres(book_id)
                    removed_count += 1
            
            logger.info(f"Synchronized {synced_count} books from Calibre to PostgreSQL")
            logger.info(f"Removed {removed_count} books that were deleted from Calibre")
            logger.info(
                "Calibre synchronization finished",
                extra={
                    "operation": "sync_finished",
                    "total": total,
                    "count": synced_count,
                },
            )
            if skipped_no_file or skipped_missing_path:
                logger.warning(
                    f"Sync skipped {skipped_no_file} books without formats and "
                    f"{skipped_missing_path} books with missing files",
                    extra={
                        "operation": "sync_skipped",
                        "total": skipped_no_file + skipped_missing_path,
                    },
                )
            
            # Update the mtime after successful sync
            from pathlib import Path
            calibre_db_path = Path(settings.CALIBRE_DB_PATH)
            if calibre_db_path.exists():
                postgres_db.set_calibre_db_mtime(calibre_db_path.stat().st_mtime)
            
            return synced_count
        except Exception as e:
            logger.error(f"Error syncing books from Calibre: {e}")
            raise
    
    def _remove_book_from_postgres(self, book_id: int):
        """Remove a book and its embeddings from PostgreSQL."""
        try:
            # Delete book chunks (including embeddings)
            with postgres_db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM book_chunks WHERE book_id = %s", (book_id,))
                chunks_deleted = cursor.rowcount
                logger.info(f"Deleted {chunks_deleted} chunks for book {book_id}")
            
            # Delete book
            with postgres_db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
                logger.info(f"Deleted book {book_id} from PostgreSQL")
        except Exception as e:
            logger.error(f"Error removing book {book_id} from PostgreSQL: {e}")
            raise
    
    def get_book(self, book_id: int) -> Optional[Dict[str, Any]]:
        """Get a book by internal PostgreSQL ID."""
        return postgres_db.get_book_by_id(book_id)
    
    def get_book_by_calibre_id(self, calibre_id: int) -> Optional[Dict[str, Any]]:
        """Get a book by Calibre ID."""
        return postgres_db.get_book_by_calibre_id(calibre_id)
    
    def get_all_books(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all books with pagination."""
        logger.info(f"BookService.get_all_books called with limit={limit}, offset={offset}")
        books = postgres_db.get_all_books(limit, offset)
        logger.info(f"BookService.get_all_books returned {len(books)} books")
        return books
    
    def search_books(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search books by title, author, or metadata in both PostgreSQL and Calibre DB.
        
        Searches in PostgreSQL first (synchronized books), then in Calibre metadata.db
        to include newly added books that haven't been synced yet. Results are merged
        with PostgreSQL books taking priority.
        """
        logger.info(f"[book_service.py:search_books:182] Starting catalog search - query={query}, limit={limit}")
        
        # Search in PostgreSQL (synchronized books)
        postgres_results = postgres_db.search_books(query, limit)
        postgres_calibre_ids = {book.get('calibre_id') for book in postgres_results if book.get('calibre_id')}
        
        logger.info(f"[book_service.py:search_books:188] PostgreSQL search completed - postgres_count={len(postgres_results)}")
        
        # Search in Calibre metadata.db (all books including new ones)
        try:
            calibre_results = self.calibre_db.search_books(query)
            logger.info(f"[book_service.py:search_books:193] Calibre DB search completed - calibre_count={len(calibre_results)}")
        except Exception as e:
            logger.warning(f"[book_service.py:search_books:195] Calibre DB search failed - error={e}")
            calibre_results = []
        
        # Filter Calibre results to only include books not already in PostgreSQL
        new_books = [
            book for book in calibre_results
            if book.get('calibre_id') not in postgres_calibre_ids
        ]
        
        if new_books:
            logger.info(f"[book_service.py:search_books:205] Found new books in Calibre - new_count={len(new_books)}")
            
            # Optionally sync new books found in Calibre
            for book in new_books[:limit - len(postgres_results)]:
                calibre_id = book.get('calibre_id')
                if calibre_id:
                    try:
                        # Get full book details from Calibre
                        full_book = self.calibre_db.get_book_by_id(calibre_id)
                        if full_book:
                            # Get file info
                            file_info = self.calibre_db.get_book_file_info(calibre_id)
                            if file_info:
                                full_path = self.library_path / file_info["path"]
                                
                                if full_path.exists():
                                    # Get additional metadata
                                    tags = self.calibre_db.get_book_tags(calibre_id)
                                    publishers = self.calibre_db.get_book_publishers(calibre_id)
                                    
                                    metadata = {
                                        'uuid': full_book.get('uuid'),
                                        'pubdate': full_book.get('pubdate'),
                                        'series_index': full_book.get('series_index'),
                                        'tags': tags,
                                        'publishers': publishers,
                                        'last_modified': full_book.get('last_modified'),
                                        'selected_format': file_info["format"],
                                        'available_formats': file_info["available_formats"],
                                    }
                                    
                                    # Insert into PostgreSQL
                                    book_id = postgres_db.insert_book(
                                        calibre_id=calibre_id,
                                        title=full_book['title'],
                                        file_path=str(full_path),
                                        author=full_book.get('authors'),
                                        metadata=metadata
                                    )
                                    
                                    # Add postgres_id to the book dict for consistent response
                                    book['id'] = book_id
                                    book['file_path'] = str(full_path)
                                    book['author'] = full_book.get('authors')
                                    book['metadata'] = metadata
                                    
                                    # Enrich with additional metadata and RAG status
                                    enriched_book = postgres_db._enrich_book_with_metadata(book)
                                    book.update(enriched_book)
                                    
                                    logger.info(f"[book_service.py:search_books:249] Auto-synced book during search - calibre_id={calibre_id}, title={full_book['title']}, postgres_id={book_id}")
                    except Exception as e:
                        logger.warning(f"[book_service.py:search_books:251] Auto-sync failed for book - calibre_id={calibre_id}, error={e}")
        
        # Merge results: PostgreSQL books first, then new Calibre books
        merged_results = postgres_results + new_books[:limit - len(postgres_results)]
        
        logger.info(f"[book_service.py:search_books:256] Search completed - total={len(merged_results)}, postgres={len(postgres_results)}, new_from_calibre={len(new_books)}")
        return merged_results

    def _book_file_path(self, book_id: int, preferred_format: Optional[str] = None) -> Optional[Path]:
        book = postgres_db.get_book_by_id(book_id)
        if preferred_format and book and book.get("calibre_id"):
            file_info = self.calibre_db.get_book_file_info(
                int(book["calibre_id"]),
                preferred_format=preferred_format,
            )
            if file_info and file_info.get("format") == preferred_format.upper():
                return self.library_path / file_info["path"]
            return None
        if book and book.get('file_path'):
            return Path(book['file_path'])
        return None

    @staticmethod
    def _book_file_format(file_path: Path) -> str:
        return file_path.suffix.lstrip('.').upper()

    @staticmethod
    def _book_media_type(file_path: Path) -> str:
        media_type, _ = mimetypes.guess_type(file_path.name)
        return media_type or "application/octet-stream"
    
    def get_book_pdf_path(self, book_id: int) -> Optional[Path]:
        """Get the file path for a book when the selected format is PDF."""
        file_path = self._book_file_path(book_id)
        if file_path and file_path.suffix.lower() == '.pdf':
            return file_path
        return None

    def get_book_formats(self, book_id: int) -> Optional[Dict[str, Any]]:
        """Get every available Calibre format for a book."""
        book = postgres_db.get_book_by_id(book_id)
        if not book:
            return None

        calibre_id = book.get("calibre_id")
        metadata = book.get("metadata", {}) or {}
        if isinstance(metadata, str):
            try:
                metadata = json.loads(metadata)
            except Exception:
                metadata = {}
        selected_format = metadata.get("selected_format")
        formats = []

        if calibre_id:
            for item in self.calibre_db.get_book_formats(int(calibre_id)):
                full_path = self.library_path / item["path"]
                formats.append(
                    {
                        "format": item["format"],
                        "filename": full_path.name,
                        "media_type": self._book_media_type(full_path),
                        "size": full_path.stat().st_size if full_path.exists() else None,
                        "exists": full_path.exists(),
                        "selected": item["format"] == selected_format,
                    }
                )

        available_formats = [item["format"] for item in formats]
        return {
            "book_id": book_id,
            "calibre_id": calibre_id,
            "title": book.get("title"),
            "selected_format": selected_format,
            "available_formats": available_formats,
            "formats": formats,
        }

    def get_book_file_info(self, book_id: int, preferred_format: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get metadata for the selected available book file."""
        file_path = self._book_file_path(book_id, preferred_format=preferred_format)
        if not file_path or not file_path.exists():
            return None
        return {
            "path": file_path,
            "filename": file_path.name,
            "format": self._book_file_format(file_path),
            "media_type": self._book_media_type(file_path),
            "size": file_path.stat().st_size,
        }
    
    def get_book_cover(self, book_id: int) -> Optional[bytes]:
        """Get the cover image for a book."""
        pdf_path = self.get_book_pdf_path(book_id)
        if pdf_path and pdf_path.exists():
            return conversion_service.extract_cover_image(pdf_path)
        return None
    
    def get_book_pdf(self, book_id: int) -> Optional[bytes]:
        """Get the PDF file for a book."""
        pdf_path = self.get_book_pdf_path(book_id)
        if pdf_path and pdf_path.exists():
            return conversion_service.get_pdf_bytes(pdf_path)
        return None

    def get_book_file(self, book_id: int, preferred_format: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get the selected available book file and response metadata."""
        info = self.get_book_file_info(book_id, preferred_format=preferred_format)
        if info:
            info["data"] = conversion_service.get_file_bytes(info["path"])
            return info
        return None
    
    def get_book_page_pdf(self, book_id: int, page_num: int) -> Optional[bytes]:
        """Get a specific page as PDF."""
        pdf_path = self.get_book_pdf_path(book_id)
        if pdf_path and pdf_path.exists():
            # For now, return the full PDF
            # TODO: Implement single page extraction
            return conversion_service.get_pdf_bytes(pdf_path)
        return None
    
    def get_book_markdown(self, book_id: int) -> Optional[str]:
        """Get the book content as Markdown."""
        pdf_path = self.get_book_pdf_path(book_id)
        if pdf_path and pdf_path.exists():
            return conversion_service.pdf_to_markdown(pdf_path)
        return None
    
    def get_book_page_markdown(self, book_id: int, page_num: int) -> Optional[str]:
        """Get a specific page as Markdown."""
        pdf_path = self.get_book_pdf_path(book_id)
        if pdf_path and pdf_path.exists():
            return conversion_service.pdf_page_to_markdown(pdf_path, page_num)
        return None
    
    def get_book_page_count(self, book_id: int) -> int:
        """Get the number of pages in a book."""
        pdf_path = self.get_book_pdf_path(book_id)
        if pdf_path and pdf_path.exists():
            return conversion_service.get_pdf_page_count(pdf_path)
        return 0
    
    def enrich_book_with_openlibrary(self, book_id: int) -> Optional[Dict[str, Any]]:
        """Enrich a book with metadata from OpenLibrary.
        
        Args:
            book_id: Internal PostgreSQL book ID
            
        Returns:
            Updated book metadata or None if enrichment failed
        """
        try:
            book = postgres_db.get_book_by_id(book_id)
            if not book:
                logger.warning(f"Book {book_id} not found for OpenLibrary enrichment")
                return None
            
            # Extract ISBN from metadata
            metadata = book.get('metadata', {}) or {}
            if isinstance(metadata, str):
                try:
                    metadata = json.loads(metadata)
                except:
                    metadata = {}
            
            identifiers = metadata.get('identifiers', {})
            isbn = None
            if identifiers and isinstance(identifiers, dict):
                isbn = identifiers.get('isbn')
            
            # Try to find by ISBN first
            ol_data = None
            if isbn:
                ol_data = openlibrary_service.search_by_isbn(isbn)
            
            # If no ISBN or no result, try by title and author
            if not ol_data:
                title = book.get('title')
                author = book.get('author')
                if title:
                    results = openlibrary_service.search_by_title_author(title, author)
                    if results:
                        ol_data = results[0]
            
            if not ol_data:
                logger.info(f"No OpenLibrary data found for book {book_id}")
                return None
            
            # Update book metadata with OpenLibrary data
            updated_metadata = metadata.copy()
            updated_metadata['openlibrary'] = ol_data
            
            # Update the book in PostgreSQL
            postgres_db.update_book_metadata(book_id, updated_metadata)
            
            logger.info(
                f"Enriched book {book_id} with OpenLibrary data",
                extra={"operation": "ol_enrich", "book_id": book_id, "title": book.get('title')}
            )
            
            # Return updated book
            return postgres_db.get_book_by_id(book_id)
            
        except Exception as e:
            logger.error(f"Error enriching book {book_id} with OpenLibrary: {e}")
            return None
    
    def get_book_download_links(self, book_id: int) -> Dict[str, Any]:
        """Get download links for a book from OpenLibrary.
        
        Args:
            book_id: Internal PostgreSQL book ID
            
        Returns:
            Dictionary with download information
        """
        try:
            book = postgres_db.get_book_by_id(book_id)
            if not book:
                logger.warning(f"Book {book_id} not found for download links")
                return {}
            
            # Extract ISBN and OLID from metadata
            metadata = book.get('metadata', {}) or {}
            if isinstance(metadata, str):
                try:
                    metadata = json.loads(metadata)
                except:
                    metadata = {}
            
            ol_data = metadata.get('openlibrary', {})
            isbn = None
            olid = ol_data.get('olid')
            
            if not olid:
                identifiers = metadata.get('identifiers', {})
                if identifiers and isinstance(identifiers, dict):
                    isbn = identifiers.get('isbn')
            
            # Get download links
            download_info = openlibrary_service.get_download_links(isbn=isbn, olid=olid)
            
            if download_info:
                logger.info(
                    f"Retrieved download links for book {book_id}",
                    extra={"operation": "ol_download", "book_id": book_id}
                )
            
            return download_info
            
        except Exception as e:
            logger.error(f"Error getting download links for book {book_id}: {e}")
            return {}
    
    def enrich_all_books_with_openlibrary(self, limit: Optional[int] = None) -> Dict[str, int]:
        """Enrich all books in the database with OpenLibrary metadata.
        
        Args:
            limit: Optional limit on number of books to process
            
        Returns:
            Dictionary with enrichment statistics
        """
        stats = {
            'total': 0,
            'enriched': 0,
            'failed': 0,
            'skipped': 0
        }
        
        try:
            logger.info("Starting bulk OpenLibrary enrichment", extra={"operation": "ol_bulk_enrich_start"})
            
            # Get all books
            books = postgres_db.get_all_books(limit=limit or 10000, offset=0)
            stats['total'] = len(books)
            
            for book in books:
                book_id = book.get('id')
                
                # Check if already enriched
                metadata = book.get('metadata', {}) or {}
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except:
                        metadata = {}
                
                if metadata.get('openlibrary'):
                    stats['skipped'] += 1
                    continue
                
                # Enrich the book
                result = self.enrich_book_with_openlibrary(book_id)
                if result:
                    stats['enriched'] += 1
                else:
                    stats['failed'] += 1
            
            logger.info(
                "Bulk OpenLibrary enrichment completed",
                extra={
                    "operation": "ol_bulk_enrich_complete",
                    "total": stats['total'],
                    "enriched": stats['enriched'],
                    "failed": stats['failed'],
                    "skipped": stats['skipped']
                }
            )
            
        except Exception as e:
            logger.error(f"Error in bulk OpenLibrary enrichment: {e}")
        
        return stats


book_service = BookService()
