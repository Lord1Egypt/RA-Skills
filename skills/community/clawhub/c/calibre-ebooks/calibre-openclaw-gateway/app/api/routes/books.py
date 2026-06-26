from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from fastapi.responses import Response, StreamingResponse, JSONResponse
from typing import Optional
from pathlib import Path

from app.models import (
    BookFormatConversionRequest,
    BookFormatConversionResponse,
    BookFormatsResponse,
    BookResponse,
    BookListResponse,
    SyncResponse,
)
from app.services.book_service import book_service
from app.services.format_conversion_service import (
    BookNotFoundError,
    BookResolutionError,
    FormatConversionError,
    format_conversion_service,
)
from app.services.virus_service import virus_service
from app.utils.logger import get_logger
from app.config import settings
from app.database.calibre_db import CalibreMetadataDBUnavailable, diagnose_calibre_db
from app.utils.ebook_validator import is_ebook_bytes, validate_bytes_size, get_supported_formats

logger = get_logger(__name__)
router = APIRouter(prefix="/api/books", tags=["books"])


def require_content_downloads_enabled() -> None:
    if not settings.ALLOW_BOOK_CONTENT_DOWNLOADS:
        raise HTTPException(
            status_code=403,
            detail="Book content downloads are disabled. Set ALLOW_BOOK_CONTENT_DOWNLOADS=true to enable them.",
        )


def calibre_db_unavailable_response(exc: CalibreMetadataDBUnavailable) -> HTTPException:
    return HTTPException(
        status_code=503,
        detail={
            "error": "calibre_metadata_db_unavailable",
            **exc.diagnostic,
        },
    )


@router.get("", response_model=BookListResponse)
async def list_books(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    auto_sync: bool = Query(default=False, description="Auto-sync from Calibre if PostgreSQL is empty")
):
    """List all books with pagination."""
    try:
        logger.info(f"Listing books with limit={limit}, offset={offset}, auto_sync={auto_sync}")
        books = book_service.get_all_books(limit, offset)
        total = len(books)
        
        # Auto-sync if PostgreSQL is empty and auto_sync is enabled
        if total == 0 and auto_sync:
            if not settings.ALLOW_GET_AUTO_SYNC:
                raise HTTPException(
                    status_code=403,
                    detail="GET auto-sync is disabled. Use /api/books/sync or set ALLOW_GET_AUTO_SYNC=true.",
                )
            logger.info("PostgreSQL is empty, auto-syncing from Calibre...")
            synced_count = book_service.sync_books_from_calibre()
            logger.info(f"Auto-synced {synced_count} books from Calibre")
            books = book_service.get_all_books(limit, offset)
            total = len(books)
        
        logger.info(f"Retrieved {total} books from PostgreSQL")
        if total == 0:
            logger.warning("No books found in PostgreSQL. Call /api/books/sync to sync from Calibre, or use ?auto_sync=true")
        return BookListResponse(
            books=books,
            total=total,
            limit=limit,
            offset=offset
        )
    except HTTPException:
        raise
    except CalibreMetadataDBUnavailable as e:
        logger.warning("Calibre metadata.db unavailable during book listing: %s", e.diagnostic)
        raise calibre_db_unavailable_response(e)
    except Exception as e:
        logger.error(f"Error listing books: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/calibre-db/status")
async def calibre_db_status():
    """Diagnose whether CALIBRE_DB_PATH points to a usable Calibre metadata.db."""
    diagnostic = diagnose_calibre_db()
    status_code = 200 if diagnostic["status"] == "available" else 503
    return JSONResponse(status_code=status_code, content=diagnostic)


@router.get("/sync", response_model=SyncResponse)
async def sync_books():
    """Synchronize books from Calibre to PostgreSQL."""
    try:
        synced_count = book_service.sync_books_from_calibre()
        return SyncResponse(
            synced_count=synced_count,
            message=f"Successfully synchronized {synced_count} books"
        )
    except CalibreMetadataDBUnavailable as e:
        logger.warning("Calibre metadata.db unavailable during sync: %s", e.diagnostic)
        raise calibre_db_unavailable_response(e)
    except Exception as e:
        logger.error(f"Error syncing books: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/sync/status")
async def sync_status():
    """Check synchronization status between Calibre and PostgreSQL."""
    try:
        from app.database.calibre_db import CalibreDB
        from app.database.postgres_db import postgres_db
        
        # Get counts from both databases
        calibre_db = CalibreDB()
        calibre_books = calibre_db.get_all_books()
        calibre_count = len(calibre_books)
        
        postgres_books = postgres_db.get_all_books(limit=1000000, offset=0)
        postgres_count = len(postgres_books)
        
        # Get last sync info (from most recent book update in PostgreSQL)
        with postgres_db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(updated_at) FROM books")
            result = cursor.fetchone()
            last_sync = result[0] if result and result[0] else None
        
        is_synced = calibre_count == postgres_count
        
        return {
            "calibre_count": calibre_count,
            "postgres_count": postgres_count,
            "is_synced": is_synced,
            "last_sync": last_sync,
            "needs_sync": not is_synced,
            "message": f"Calibre: {calibre_count} books, PostgreSQL: {postgres_count} books"
        }
    except CalibreMetadataDBUnavailable as e:
        logger.warning("Calibre metadata.db unavailable during sync status: %s", e.diagnostic)
        raise calibre_db_unavailable_response(e)
    except Exception as e:
        logger.error(f"Error checking sync status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/convert-format", response_model=BookFormatConversionResponse)
async def convert_book_format(request: BookFormatConversionRequest):
    """Convert a Calibre book to another format and register it in Calibre."""
    try:
        result = format_conversion_service.convert_and_register(
            book_id=request.book_id,
            calibre_id=request.calibre_id,
            title=request.title,
            target_format=request.target_format,
            source_format=request.source_format,
            force=request.force,
        )
        return BookFormatConversionResponse(**result)
    except BookNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BookResolutionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FormatConversionError as e:
        logger.error(f"Book format conversion failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected book format conversion error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/problems")
async def list_problem_books():
    """List books with problems (missing files, RAG processing errors, etc.)."""
    try:
        from app.database.calibre_db import CalibreDB
        from app.database.postgres_db import postgres_db
        from pathlib import Path
        
        calibre_db = CalibreDB()
        postgres_books = postgres_db.get_all_books(limit=1000000, offset=0)
        
        problem_books = []
        
        for book in postgres_books:
            problems = []
            
            # Check if file exists
            if book.get('file_path'):
                full_path = Path(book['file_path'])
                if not full_path.is_absolute():
                    full_path = Path(settings.CALIBRE_LIBRARY_PATH) / full_path
                if not full_path.exists():
                    problems.append("File not found")
            else:
                problems.append("No file path")
            
            # Check if has no embeddings
            book_id = book.get('id')
            if book_id and not postgres_db.has_embeddings(book_id):
                problems.append("No embeddings")
            
            # Check for RAG processing errors
            if book_id:
                queue_status = postgres_db.get_queue_status(book_id)
                if queue_status and queue_status.get('status') == 'failed':
                    error_msg = queue_status.get('error_message', 'RAG processing failed')
                    problems.append(f"RAG error: {error_msg}")
            
            if problems:
                problem_books.append({
                    "id": book.get('id'),
                    "calibre_id": book.get('calibre_id'),
                    "title": book.get('title'),
                    "author": book.get('author'),
                    "file_path": book.get('file_path'),
                    "problems": problems
                })
        
        return {
            "total": len(problem_books),
            "books": problem_books
        }
    except Exception as e:
        logger.error(f"Error listing problem books: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/recent")
async def list_recent_books(limit: int = Query(default=10, ge=1, le=50)):
    """List recently added or RAG-processed books."""
    try:
        from app.database.postgres_db import postgres_db
        from psycopg2.extras import RealDictCursor
        
        # Get recently added books (by indexed_at)
        with postgres_db.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT b.*, 
                       pq.status as queue_status,
                       pq.error_message as queue_error,
                       pq.completed_at as rag_completed_at
                FROM books b
                LEFT JOIN processing_queue pq ON b.id = pq.book_id 
                    AND pq.id = (
                        SELECT MAX(id) FROM processing_queue 
                        WHERE book_id = b.id
                    )
                ORDER BY b.indexed_at DESC, pq.completed_at DESC NULLS LAST
                LIMIT %s
            """, (limit,))
            books = cursor.fetchall()
        
        # Enrich with metadata and RAG status
        enriched_books = [postgres_db._enrich_book_with_metadata(book) for book in books]
        
        return {
            "total": len(enriched_books),
            "books": enriched_books
        }
    except Exception as e:
        logger.error(f"Error listing recent books: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{book_id}/formats", response_model=BookFormatsResponse)
async def get_book_formats(book_id: int):
    """Get the formats currently registered for a Calibre book."""
    try:
        format_info = book_service.get_book_formats(book_id)
        if not format_info:
            raise HTTPException(status_code=404, detail="Book not found")
        return BookFormatsResponse(**format_info)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting formats for book {book_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int):
    """Get a specific book by ID."""
    try:
        book = book_service.get_book(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return BookResponse(**book)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{book_id}/cover")
async def get_book_cover(book_id: int):
    """Get the cover image for a book (JPG format)."""
    try:
        cover_data = book_service.get_book_cover(book_id)
        if not cover_data:
            raise HTTPException(status_code=404, detail="Cover not found")
        
        return Response(
            content=cover_data,
            media_type="image/jpeg",
            headers={"Content-Disposition": f"inline; filename=book_{book_id}_cover.jpg"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting cover for book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{book_id}/pdf")
async def get_book_pdf(
    book_id: int,
    check_virus: bool = Query(default=False, description="Enable virus scanning using VirusTotal API")
):
    """Get the complete PDF file for a book when PDF is the selected format."""
    try:
        require_content_downloads_enabled()
        pdf_data = book_service.get_book_pdf(book_id)
        if not pdf_data:
            raise HTTPException(status_code=404, detail="PDF not found")
        
        # Virus scan if requested and enabled
        if check_virus and virus_service.is_enabled():
            logger.info(f"Starting virus scan for PDF of book {book_id}")
            virus_result = await virus_service.scan_bytes(pdf_data, f"book_{book_id}.pdf")
            
            if virus_result.get("malicious"):
                logger.warning(f"PDF for book {book_id} detected as malicious: {virus_result}")
                raise HTTPException(
                    status_code=403,
                    detail={
                        "error": "malicious_file_detected",
                        "message": "File contains malware and was blocked",
                        "virus_scan": virus_result
                    }
                )
            
            logger.info(f"Virus scan completed for PDF of book {book_id}: {virus_result.get('summary', 'No threats detected')}")
        elif check_virus and not virus_service.is_enabled():
            logger.warning(f"Virus scan requested for book {book_id} PDF but VT_API_KEY not configured")
        
        return Response(
            content=pdf_data,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename=book_{book_id}.pdf"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting PDF for book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{book_id}/file")
async def get_book_file(
    book_id: int,
    format: Optional[str] = Query(default=None, description="Preferred registered format to download, e.g. EPUB, PDF, AZW3"),
    check_virus: bool = Query(default=False, description="Enable virus scanning using VirusTotal API")
):
    """Get the book file in the selected or requested available Calibre format."""
    try:
        require_content_downloads_enabled()
        file_info = book_service.get_book_file(book_id, preferred_format=format)
        if not file_info:
            raise HTTPException(status_code=404, detail="Book file not found")

        # Virus scan if requested and enabled
        if check_virus and virus_service.is_enabled():
            logger.info(f"Starting virus scan for file of book {book_id}")
            virus_result = await virus_service.scan_bytes(file_info["data"], file_info["filename"])
            
            if virus_result.get("malicious"):
                logger.warning(f"File for book {book_id} detected as malicious: {virus_result}")
                raise HTTPException(
                    status_code=403,
                    detail={
                        "error": "malicious_file_detected",
                        "message": "File contains malware and was blocked",
                        "virus_scan": virus_result
                    }
                )
            
            logger.info(f"Virus scan completed for file of book {book_id}: {virus_result.get('summary', 'No threats detected')}")
        elif check_virus and not virus_service.is_enabled():
            logger.warning(f"Virus scan requested for book {book_id} file but VT_API_KEY not configured")

        return Response(
            content=file_info["data"],
            media_type=file_info["media_type"],
            headers={
                "Content-Disposition": f"inline; filename={file_info['filename']}",
                "X-Book-Format": file_info["format"],
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting file for book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{book_id}/page/{page_num}/pdf")
async def get_book_page_pdf(book_id: int, page_num: int):
    """Get a specific page as PDF."""
    try:
        require_content_downloads_enabled()
        if page_num < 1:
            raise HTTPException(status_code=400, detail="Page number must be >= 1")
        
        pdf_data = book_service.get_book_page_pdf(book_id, page_num)
        if not pdf_data:
            raise HTTPException(status_code=404, detail="Page not found")
        
        return Response(
            content=pdf_data,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename=book_{book_id}_page_{page_num}.pdf"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting page {page_num} for book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{book_id}/markdown")
async def get_book_markdown(book_id: int):
    """Get the complete book content as Markdown."""
    try:
        require_content_downloads_enabled()
        markdown = book_service.get_book_markdown(book_id)
        if not markdown:
            raise HTTPException(status_code=404, detail="Book not found or conversion failed")
        
        return Response(
            content=markdown,
            media_type="text/markdown",
            headers={"Content-Disposition": f"inline; filename=book_{book_id}.md"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting markdown for book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{book_id}/page/{page_num}/markdown")
async def get_book_page_markdown(book_id: int, page_num: int):
    """Get a specific page as Markdown."""
    try:
        require_content_downloads_enabled()
        if page_num < 1:
            raise HTTPException(status_code=400, detail="Page number must be >= 1")
        
        markdown = book_service.get_book_page_markdown(book_id, page_num)
        if not markdown:
            raise HTTPException(status_code=404, detail="Page not found or conversion failed")
        
        return Response(
            content=markdown,
            media_type="text/markdown",
            headers={"Content-Disposition": f"inline; filename=book_{book_id}_page_{page_num}.md"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting markdown for page {page_num} of book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/upload")
async def upload_ebook(
    file: UploadFile = File(..., description="Ebook file to upload"),
    check_virus: bool = Query(default=False, description="Enable virus scanning using VirusTotal API")
):
    """
    Upload an ebook file with format validation and optional virus scanning.
    
    The file is validated to ensure it's a valid ebook format. If VT_API_KEY is configured
    and check_virus=true, the file will be scanned for malware before being accepted.
    
    Supported formats: PDF, EPUB, MOBI, AZW3, KFX, DJVU, LIT, PDB, TXT, RTF, DOCX, ODT, FB2, HTML, CBZ, CBR
    """
    try:
        logger.info(f"Received file upload request: {file.filename}, check_virus={check_virus}")
        
        # Read file content
        file_data = await file.read()
        
        # Validate file size (max 100MB)
        size_valid, size_error = validate_bytes_size(file_data, file.filename)
        if not size_valid:
            raise HTTPException(status_code=413, detail=size_error)
        
        # Validate ebook format
        is_valid, format_name = is_ebook_bytes(file_data, file.filename)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid ebook format. Supported formats: {', '.join(get_supported_formats())}"
            )
        
        logger.info(f"File {file.filename} validated as {format_name}")
        
        # Virus scan if enabled and requested
        virus_result = None
        if check_virus and virus_service.is_enabled():
            logger.info(f"Starting virus scan for {file.filename}")
            virus_result = await virus_service.scan_bytes(file_data, file.filename)
            
            if virus_result.get("malicious"):
                logger.warning(f"File {file.filename} detected as malicious: {virus_result}")
                raise HTTPException(
                    status_code=403,
                    detail={
                        "error": "malicious_file_detected",
                        "message": "File contains malware and was rejected",
                        "virus_scan": virus_result
                    }
                )
            
            logger.info(f"Virus scan completed for {file.filename}: {virus_result.get('summary', 'No threats detected')}")
        elif check_virus and not virus_service.is_enabled():
            logger.warning(f"Virus scan requested but VT_API_KEY not configured")
            virus_result = {
                "scanned": False,
                "reason": "VirusTotal API not configured (VT_API_KEY not set)"
            }
        
        # Save file to library
        library_path = Path(settings.CALIBRE_LIBRARY_PATH)
        upload_dir = library_path / "uploads"
        upload_dir.mkdir(exist_ok=True)
        
        # Generate safe filename
        safe_filename = Path(file.filename).name
        file_path = upload_dir / safe_filename
        
        # Avoid overwriting existing files
        counter = 1
        while file_path.exists():
            stem = Path(file.filename).stem
            suffix = Path(file.filename).suffix
            safe_filename = f"{stem}_{counter}{suffix}"
            file_path = upload_dir / safe_filename
            counter += 1
        
        # Write file
        with open(file_path, "wb") as f:
            f.write(file_data)
        
        logger.info(f"File saved to: {file_path}")
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "File uploaded successfully",
                "filename": safe_filename,
                "format": format_name,
                "size_bytes": len(file_data),
                "path": str(file_path),
                "virus_scan": virus_result
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file {file.filename}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{book_id}/openlibrary/enrich")
async def enrich_book_with_openlibrary(book_id: int):
    """Enrich a book with metadata from OpenLibrary."""
    try:
        logger.info(f"Enriching book {book_id} with OpenLibrary data")
        enriched_book = book_service.enrich_book_with_openlibrary(book_id)
        
        if not enriched_book:
            raise HTTPException(
                status_code=404,
                detail="Book not found or no OpenLibrary data available"
            )
        
        return BookResponse(**enriched_book)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enriching book {book_id} with OpenLibrary: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{book_id}/openlibrary/download-links")
async def get_book_download_links(book_id: int):
    """Get download links for a book from OpenLibrary (if available as public domain)."""
    try:
        logger.info(f"Getting download links for book {book_id}")
        download_info = book_service.get_book_download_links(book_id)
        
        if not download_info:
            return {
                "message": "No download links available",
                "reason": "Book not found in OpenLibrary or not available as public domain"
            }
        
        return download_info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting download links for book {book_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/openlibrary/bulk-enrich")
async def bulk_enrich_books_with_openlibrary(
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of books to enrich")
):
    """Enrich all books in the database with OpenLibrary metadata."""
    try:
        logger.info(f"Starting bulk OpenLibrary enrichment with limit={limit}")
        stats = book_service.enrich_all_books_with_openlibrary(limit=limit)
        
        return {
            "message": "Bulk enrichment completed",
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Error in bulk OpenLibrary enrichment: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
