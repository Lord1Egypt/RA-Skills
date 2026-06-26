import sqlite3
import time
from pathlib import Path
from typing import List, Dict, Optional, Any
from contextlib import contextmanager

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

FORMAT_PRIORITY = ["PDF", "EPUB", "AZW3", "MOBI", "DJVU", "FB2", "TXT", "RTF", "DOCX", "HTMLZ"]
REQUIRED_TABLES = {"books", "data", "authors", "books_authors_link"}


class CalibreMetadataDBUnavailable(RuntimeError):
    """Raised when the configured Calibre metadata.db cannot be handled safely."""

    def __init__(self, diagnostic: Dict[str, Any]):
        self.diagnostic = diagnostic
        super().__init__(diagnostic["message"])


def _diagnostic(
    *,
    status: str,
    reason: str,
    message: str,
    path: Optional[Path] = None,
    agent_action: str,
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload = {
        "status": status,
        "reason": reason,
        "message": message,
        "calibre_db_path": str(path) if path else settings.CALIBRE_DB_PATH,
        "agent_action": agent_action,
        "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if details:
        payload["details"] = details
    return payload


def diagnose_calibre_db() -> Dict[str, Any]:
    """Return a structured status for the configured Calibre metadata.db."""
    configured_path = (settings.CALIBRE_DB_PATH or "").strip()
    if not configured_path:
        return _diagnostic(
            status="unavailable",
            reason="not_configured",
            message="CALIBRE_DB_PATH is empty or not configured.",
            path=None,
            agent_action="notify_user",
        )

    db_path = Path(configured_path).expanduser()
    parent = db_path.parent
    if not parent.exists():
        return _diagnostic(
            status="unavailable",
            reason="parent_directory_missing",
            message=f"The parent directory for metadata.db does not exist: {parent}",
            path=db_path,
            agent_action="notify_user",
        )
    if not db_path.exists():
        return _diagnostic(
            status="unavailable",
            reason="file_missing",
            message=f"Calibre metadata.db was not found at {db_path}.",
            path=db_path,
            agent_action="notify_user",
        )
    if not db_path.is_file():
        return _diagnostic(
            status="unavailable",
            reason="not_a_file",
            message=f"CALIBRE_DB_PATH points to a directory or special file, not metadata.db: {db_path}",
            path=db_path,
            agent_action="notify_user",
        )

    try:
        stat = db_path.stat()
    except OSError as exc:
        return _diagnostic(
            status="unavailable",
            reason="stat_failed",
            message=f"Cannot inspect metadata.db: {exc}",
            path=db_path,
            agent_action="notify_user",
            details={"errno": exc.errno},
        )

    if stat.st_size == 0:
        return _diagnostic(
            status="unavailable",
            reason="empty_file",
            message=f"metadata.db exists but is empty: {db_path}",
            path=db_path,
            agent_action="notify_user",
            details={"size_bytes": stat.st_size},
        )

    try:
        conn = sqlite3.connect(
            f"file:{db_path}?mode=ro&nolock=1",
            uri=True,
            timeout=2,
            check_same_thread=False,
        )
        conn.row_factory = sqlite3.Row
        try:
            quick_check = conn.execute("PRAGMA quick_check").fetchone()
            quick_check_result = quick_check[0] if quick_check else None
            if quick_check_result != "ok":
                return _diagnostic(
                    status="unavailable",
                    reason="integrity_check_failed",
                    message=f"SQLite quick_check failed for metadata.db: {quick_check_result}",
                    path=db_path,
                    agent_action="notify_user",
                    details={"quick_check": quick_check_result},
                )

            table_rows = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
            tables = {row["name"] for row in table_rows}
            missing_tables = sorted(REQUIRED_TABLES - tables)
            if missing_tables:
                return _diagnostic(
                    status="unavailable",
                    reason="invalid_calibre_schema",
                    message="metadata.db is readable but does not look like a Calibre database.",
                    path=db_path,
                    agent_action="notify_user",
                    details={"missing_tables": missing_tables},
                )

            book_count = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        finally:
            conn.close()
    except sqlite3.OperationalError as exc:
        raw = str(exc)
        lowered = raw.lower()
        reason = "sqlite_operational_error"
        agent_action = "notify_user"
        if "locked" in lowered or "busy" in lowered:
            reason = "database_locked"
            agent_action = "wait"
        elif "unable to open" in lowered:
            reason = "open_failed"
        elif "file is not a database" in lowered:
            reason = "not_sqlite_database"
        elif "disk i/o" in lowered:
            reason = "disk_io_error"
        return _diagnostic(
            status="unavailable",
            reason=reason,
            message=f"SQLite could not open or validate metadata.db: {raw}",
            path=db_path,
            agent_action=agent_action,
        )
    except sqlite3.DatabaseError as exc:
        return _diagnostic(
            status="unavailable",
            reason="sqlite_database_error",
            message=f"SQLite reported a database error for metadata.db: {exc}",
            path=db_path,
            agent_action="notify_user",
        )
    except OSError as exc:
        return _diagnostic(
            status="unavailable",
            reason="filesystem_error",
            message=f"Filesystem error while reading metadata.db: {exc}",
            path=db_path,
            agent_action="notify_user",
            details={"errno": exc.errno},
        )

    return _diagnostic(
        status="available",
        reason="ok",
        message="metadata.db is readable and has the expected Calibre schema.",
        path=db_path,
        agent_action="proceed",
        details={
            "size_bytes": stat.st_size,
            "mtime": stat.st_mtime,
            "book_count": book_count,
        },
    )


@contextmanager
def get_calibre_db():
    """Context manager for readonly Calibre database connection without file locking."""
    db_path = Path(settings.CALIBRE_DB_PATH)
    diagnostic = diagnose_calibre_db()
    if diagnostic["status"] != "available":
        raise CalibreMetadataDBUnavailable(diagnostic)
    
    # Use read-only mode with no locking to allow external modifications
    # mode=ro: read-only
    # nolock=1: disable file locking (SQLite-specific)
    # immutable=1: treat database as read-only (optimization)
    conn = sqlite3.connect(
        f"file:{db_path}?mode=ro&nolock=1&immutable=1",
        uri=True,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


class CalibreDB:
    """Interface for readonly access to Calibre metadata.db."""
    
    @staticmethod
    def get_all_books() -> List[Dict[str, Any]]:
        """Get all books from Calibre database."""
        query = """
        SELECT 
            b.id as calibre_id,
            b.title,
            b.path,
            b.uuid,
            GROUP_CONCAT(a.name, ', ') as authors,
            b.pubdate,
            b.series_index,
            b.last_modified
        FROM books b
        LEFT JOIN books_authors_link bal ON b.id = bal.book
        LEFT JOIN authors a ON bal.author = a.id
        GROUP BY b.id
        ORDER BY b.title
        """
        
        try:
            with get_calibre_db() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                books = [dict(row) for row in cursor.fetchall()]
                logger.info(f"Retrieved {len(books)} books from Calibre DB")
                return books
        except Exception as e:
            logger.error(f"Error retrieving books from Calibre DB: {e}")
            raise
    
    @staticmethod
    def get_book_by_id(calibre_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific book by Calibre ID."""
        query = """
        SELECT 
            b.id as calibre_id,
            b.title,
            b.path,
            b.uuid,
            GROUP_CONCAT(a.name, ', ') as authors,
            b.pubdate,
            b.series_index,
            b.last_modified
        FROM books b
        LEFT JOIN books_authors_link bal ON b.id = bal.book
        LEFT JOIN authors a ON bal.author = a.id
        WHERE b.id = ?
        GROUP BY b.id
        """
        
        try:
            with get_calibre_db() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (calibre_id,))
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except Exception as e:
            logger.error(f"Error retrieving book {calibre_id} from Calibre DB: {e}")
            raise
    
    @staticmethod
    def get_book_tags(calibre_id: int) -> List[str]:
        """Get tags for a specific book."""
        query = """
        SELECT t.name
        FROM tags t
        JOIN books_tags_link btl ON t.id = btl.tag
        WHERE btl.book = ?
        """
        
        try:
            with get_calibre_db() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (calibre_id,))
                tags = [row['name'] for row in cursor.fetchall()]
                return tags
        except Exception as e:
            logger.error(f"Error retrieving tags for book {calibre_id}: {e}")
            return []
    
    @staticmethod
    def get_book_publishers(calibre_id: int) -> List[str]:
        """Get publishers for a specific book."""
        query = """
        SELECT p.name
        FROM publishers p
        JOIN books_publishers_link bpl ON p.id = bpl.publisher
        WHERE bpl.book = ?
        """
        
        try:
            with get_calibre_db() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (calibre_id,))
                publishers = [row['name'] for row in cursor.fetchall()]
                return publishers
        except Exception as e:
            logger.error(f"Error retrieving publishers for book {calibre_id}: {e}")
            return []
    
    @staticmethod
    def get_book_file_info(calibre_id: int, preferred_format: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get the path and format for the best available book file."""
        query = """
        SELECT b.path, d.name, d.format
        FROM data d
        JOIN books b ON d.book = b.id
        WHERE b.id = ?
        ORDER BY d.format
        """
        
        try:
            with get_calibre_db() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (calibre_id,))
                rows = [dict(row) for row in cursor.fetchall()]
                if rows:
                    available_formats = [row["format"].upper() for row in rows]
                    selected = None
                    if preferred_format:
                        selected = next(
                            (row for row in rows if row["format"].upper() == preferred_format.upper()),
                            None,
                        )
                    if selected is None:
                        selected = min(
                            rows,
                            key=lambda row: (
                                FORMAT_PRIORITY.index(row["format"].upper())
                                if row["format"].upper() in FORMAT_PRIORITY
                                else len(FORMAT_PRIORITY),
                                row["format"].upper(),
                            ),
                        )

                    file_format = selected["format"].lower()
                    file_path = f"{selected['path']}/{selected['name']}.{file_format}"
                    return {
                        "path": file_path,
                        "format": selected["format"].upper(),
                        "available_formats": available_formats,
                    }
                return None
        except Exception as e:
            logger.error(f"Error retrieving file path for book {calibre_id}: {e}")
            return None

    @staticmethod
    def get_book_formats(calibre_id: int) -> List[Dict[str, Any]]:
        """Get every registered file format for a Calibre book."""
        query = """
        SELECT b.path, d.name, d.format
        FROM data d
        JOIN books b ON d.book = b.id
        WHERE b.id = ?
        ORDER BY d.format
        """

        try:
            with get_calibre_db() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (calibre_id,))
                rows = [dict(row) for row in cursor.fetchall()]
                return [
                    {
                        "path": f"{row['path']}/{row['name']}.{row['format'].lower()}",
                        "name": row["name"],
                        "format": row["format"].upper(),
                    }
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"Error retrieving formats for book {calibre_id}: {e}")
            return []

    @staticmethod
    def get_book_file_path(calibre_id: int) -> Optional[str]:
        """Get the file path for the best available book format."""
        info = CalibreDB.get_book_file_info(calibre_id)
        return info["path"] if info else None
    
    @staticmethod
    def search_books(query: str) -> List[Dict[str, Any]]:
        """Search books by title, author, or tags."""
        search_query = """
        SELECT 
            b.id as calibre_id,
            b.title,
            b.path,
            GROUP_CONCAT(a.name, ', ') as authors
        FROM books b
        LEFT JOIN books_authors_link bal ON b.id = bal.book
        LEFT JOIN authors a ON bal.author = a.id
        WHERE b.title LIKE ? OR a.name LIKE ?
        GROUP BY b.id
        ORDER BY b.title
        """
        
        search_pattern = f"%{query}%"
        
        try:
            with get_calibre_db() as conn:
                cursor = conn.cursor()
                cursor.execute(search_query, (search_pattern, search_pattern))
                books = [dict(row) for row in cursor.fetchall()]
                logger.info(
                    "Calibre metadata search returned %s results",
                    len(books),
                    extra={"operation": "calibre_search", "query_length": len(query or "")},
                )
                return books
        except Exception as e:
            logger.error(f"Error searching books in Calibre DB: {e}")
            raise
