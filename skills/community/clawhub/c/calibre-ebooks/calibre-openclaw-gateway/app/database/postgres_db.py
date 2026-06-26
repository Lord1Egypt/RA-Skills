import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
import json
import re
import unicodedata

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Multilingual stopwords (PT + EN) filtered out of content-insight term
# frequencies so the "most relevant words" reflect domain vocabulary instead of
# grammatical filler. Kept intentionally small and language-agnostic; the SQL
# also drops non-alphabetic tokens and very short words.
CONTENT_INSIGHT_STOPWORDS = set(
    """
    a o e os as um uma uns umas de do da dos das em no na nos nas ao aos pelo pela
    por para com sem sob sobre entre ate apos antes durante que se quando onde como
    porque entao tambem nao sim mais menos muito pouco cada todo toda todos todas
    ser estar ter haver foi era sao seja sendo seu sua seus suas este esta estes estas
    esse essa isso isto aquele aquela aquilo pode podem deve devem qual quais cujo
    the of and to in is it for on with as at by an be this that these those from or
    are was were will would can could should may might must shall not but if then
    than which who whom whose you your they them their our its his her she he we us
    me my mine into out over under up down off again further here there all any some
    such no nor only own same so too very just about after before between because
    while where when what how why both each few more most other have has had does did
    doing done being been using used use also one two three first second new
    """.split()
)

# Text-search configurations allowed for content-insight term frequencies.
CONTENT_INSIGHT_REGCONFIGS = {"simple", "english", "portuguese"}

BOOK_SEARCH_STOPWORDS = CONTENT_INSIGHT_STOPWORDS | set(
    """
    livro livros ebook ebooks pdf epub sobre acerca algum alguma alguns algumas
    tem tenho tinha havia existe existem biblioteca acervo local procurar procure
    buscar busque pesquisar pesquise encontrar encontre catequese tema assunto
    """.split()
)


def build_top_terms_query(
    regconfig: str,
    sample_size: int,
    min_word_length: int,
    limit: int,
) -> tuple[str, int, int]:
    """Validate term-frequency inputs and build the sampled ts_stat inner query.

    Returns ``(inner_query, min_word_length, limit)`` with all values clamped to
    safe ranges. ``regconfig`` is validated against an allow-list and only the
    validated regconfig and integer sample size are interpolated, so caller
    input cannot inject SQL.
    """
    if regconfig not in CONTENT_INSIGHT_REGCONFIGS:
        regconfig = "simple"
    sample_size = max(1, min(int(sample_size), 50000))
    min_word_length = max(1, min(int(min_word_length), 40))
    limit = max(1, min(int(limit), 200))

    inner_query = (
        f"SELECT to_tsvector('{regconfig}', content) "
        f"FROM (SELECT content FROM book_chunks "
        f"WHERE embedding IS NOT NULL ORDER BY random() LIMIT {sample_size}) sampled"
    )
    return inner_query, min_word_length, limit


def extract_book_search_terms(query: str, max_terms: int = 8) -> List[str]:
    """Extract useful catalog terms from a natural-language book query."""
    normalized = unicodedata.normalize("NFKD", query or "")
    ascii_query = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    terms = []
    seen = set()
    for token in re.findall(r"[A-Za-zÀ-ÿ0-9]+", ascii_query.lower()):
        if len(token) < 3 or token in BOOK_SEARCH_STOPWORDS:
            continue
        if token not in seen:
            terms.append(token)
            seen.add(token)
        if len(terms) >= max_terms:
            break
    return terms


class PostgreSQLDB:
    """Interface for PostgreSQL database operations."""
    
    def __init__(self):
        self._pool = None
    
    def initialize_pool(self):
        """Initialize connection pool."""
        if self._pool is None:
            self._pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=settings.postgres_dsn
            )
            logger.info("PostgreSQL connection pool initialized")
            self._ensure_schema()
    
    @contextmanager
    def get_connection(self):
        """Get a connection from the pool."""
        if self._pool is None:
            self.initialize_pool()
        
        conn = self._pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            self._pool.putconn(conn)
    
    def close_pool(self):
        """Close all connections in the pool."""
        if self._pool:
            self._pool.closeall()
            self._pool = None
            logger.info("PostgreSQL connection pool closed")
    
    def _ensure_schema(self):
        """Ensure the application schema exists in the configured database."""
        queries = [
            "CREATE EXTENSION IF NOT EXISTS vector",
            """
            CREATE TABLE IF NOT EXISTS settings (
                key VARCHAR(255) PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                calibre_id INTEGER UNIQUE,
                title TEXT NOT NULL,
                author TEXT,
                file_path TEXT NOT NULL,
                file_size BIGINT,
                file_type TEXT,
                metadata JSONB,
                indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS book_chunks (
                id SERIAL PRIMARY KEY,
                book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
                chunk_index INTEGER NOT NULL,
                content TEXT NOT NULL,
                embedding vector(768),
                embedding_model TEXT,
                page_start INTEGER,
                page_end INTEGER,
                section_title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (book_id, chunk_index)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS processing_queue (
                id SERIAL PRIMARY KEY,
                book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
                status TEXT NOT NULL DEFAULT 'pending',
                priority INTEGER NOT NULL DEFAULT 0,
                error_message TEXT,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS download_queue (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT,
                source TEXT NOT NULL,
                source_id TEXT,
                olid TEXT,
                ocaid TEXT,
                download_url TEXT,
                preferred_format TEXT DEFAULT 'PDF',
                status TEXT NOT NULL DEFAULT 'pending',
                priority INTEGER NOT NULL DEFAULT 0,
                error_message TEXT,
                file_path TEXT,
                file_size BIGINT,
                file_hash TEXT,
                download_available BOOLEAN DEFAULT true,
                calibre_book_id INTEGER,
                added_to_calibre_at TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            "CREATE INDEX IF NOT EXISTS idx_books_calibre_id ON books(calibre_id)",
            "CREATE INDEX IF NOT EXISTS idx_books_title ON books(title)",
            "CREATE INDEX IF NOT EXISTS idx_book_chunks_book_id ON book_chunks(book_id)",
            "CREATE INDEX IF NOT EXISTS idx_book_chunks_embedding ON book_chunks USING ivfflat (embedding vector_cosine_ops) WHERE embedding IS NOT NULL",
            "CREATE INDEX IF NOT EXISTS idx_processing_queue_status_priority ON processing_queue(status, priority DESC, created_at)",
            "CREATE INDEX IF NOT EXISTS idx_processing_queue_book_id ON processing_queue(book_id)",
            "CREATE INDEX IF NOT EXISTS idx_download_queue_status_priority ON download_queue(status, priority DESC, created_at)",
            "CREATE INDEX IF NOT EXISTS idx_download_queue_olid ON download_queue(olid)",
        ]
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for query in queries:
                cursor.execute(query)
            logger.info(
                "Application schema ensured in PostgreSQL database '%s'",
                settings.POSTGRESQL_DB_DATABASE,
            )
    
    def _ensure_embeddings_schema(self):
        """Ensure embedding bookkeeping columns exist (idempotent migration)."""
        query = """
        ALTER TABLE book_chunks
            ADD COLUMN IF NOT EXISTS embedding_model TEXT,
            ADD COLUMN IF NOT EXISTS page_start INTEGER,
            ADD COLUMN IF NOT EXISTS page_end INTEGER,
            ADD COLUMN IF NOT EXISTS section_title TEXT
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                logger.info("book_chunks embedding/citation columns ensured")
        except Exception as e:
            # book_chunks may not exist yet on a fresh database; log and continue.
            logger.warning(f"Could not ensure embeddings schema (will retry later): {e}")
    
    # Generic settings helpers
    def get_setting(self, key: str) -> Optional[str]:
        """Get a raw setting value by key."""
        query = "SELECT value FROM settings WHERE key = %s"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (key,))
            result = cursor.fetchone()
            return result[0] if result else None
    
    def set_setting(self, key: str, value: str):
        """Insert or update a setting value by key."""
        query = """
        INSERT INTO settings (key, value)
        VALUES (%s, %s)
        ON CONFLICT (key)
        DO UPDATE SET value = EXCLUDED.value, updated_at = CURRENT_TIMESTAMP
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (key, str(value)))
            logger.info(f"Setting '{key}' updated")
    
    def get_embedding_column_dimension(self) -> Optional[int]:
        """Return the declared dimension of book_chunks.embedding (pgvector typmod)."""
        query = """
        SELECT a.atttypmod
        FROM pg_attribute a
        JOIN pg_class c ON a.attrelid = c.oid
        WHERE c.relname = 'book_chunks' AND a.attname = 'embedding'
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            if result and result[0] and result[0] > 0:
                # For pgvector, atttypmod stores the dimension directly.
                return int(result[0])
            return None
    
    def invalidate_all_embeddings(self, new_dimension: Optional[int] = None) -> int:
        """Clear all stored embeddings so they can be regenerated.

        If ``new_dimension`` differs from the current column dimension, the
        embedding column type is altered to the new dimension. Completed/failed
        queue items are reset to pending so the worker reprocesses every book.
        Returns the number of chunks that had their embedding cleared.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE book_chunks SET embedding = NULL, embedding_model = NULL "
                "WHERE embedding IS NOT NULL"
            )
            cleared = cursor.rowcount

            current_dim = self.get_embedding_column_dimension()
            if new_dimension and current_dim and new_dimension != current_dim:
                logger.warning(
                    "Altering book_chunks.embedding dimension from %s to %s",
                    current_dim,
                    new_dimension,
                )
                cursor.execute(
                    f"ALTER TABLE book_chunks "
                    f"ALTER COLUMN embedding TYPE vector({int(new_dimension)})"
                )

            cursor.execute(
                "UPDATE processing_queue SET status = 'pending', "
                "completed_at = NULL, error_message = NULL "
                "WHERE status IN ('completed', 'failed')"
            )
            requeued = cursor.rowcount

            logger.warning(
                "Invalidated %s embedding(s) and reset %s queue item(s) to pending",
                cleared,
                requeued,
            )
            return cleared

    def count_embeddings_missing_citation_metadata(self) -> int:
        """Count embedded chunks that cannot cite at least a page number."""
        query = """
        SELECT COUNT(*) AS count
        FROM book_chunks
        WHERE embedding IS NOT NULL
          AND page_start IS NULL
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute(query)
                result = cursor.fetchone()
                return result["count"] if result else 0
        except Exception as e:
            logger.warning(f"Could not count missing citation metadata: {e}")
            return 0
    
    def get_calibre_db_mtime(self) -> Optional[float]:
        """Get the last modification time of Calibre metadata.db stored in PostgreSQL."""
        query = "SELECT value FROM settings WHERE key = 'calibre_db_mtime'"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return float(result[0])
            return None
    
    def set_calibre_db_mtime(self, mtime: float):
        """Store the last modification time of Calibre metadata.db."""
        query = """
        INSERT INTO settings (key, value) 
        VALUES ('calibre_db_mtime', %s)
        ON CONFLICT (key) 
        DO UPDATE SET value = EXCLUDED.value, updated_at = CURRENT_TIMESTAMP
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (str(mtime),))
            logger.info(f"Calibre DB mtime updated to {mtime}")
    
    def get_last_storage_calc_time(self) -> Optional[float]:
        """Get the last storage calculation timestamp."""
        query = "SELECT value FROM settings WHERE key = 'last_storage_calc'"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return float(result[0])
            return None
    
    def set_last_storage_calc_time(self, timestamp: float):
        """Store the last storage calculation timestamp."""
        query = """
        INSERT INTO settings (key, value) 
        VALUES ('last_storage_calc', %s)
        ON CONFLICT (key) 
        DO UPDATE SET value = EXCLUDED.value, updated_at = CURRENT_TIMESTAMP
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (str(timestamp),))
            logger.info(f"Last storage calc time updated to {timestamp}")
    
    # Books operations
    def insert_book(self, calibre_id: int, title: str, file_path: str, 
                    author: Optional[str] = None, metadata: Optional[Dict] = None) -> int:
        """Insert a new book into the database."""
        query = """
        INSERT INTO books (calibre_id, title, file_path, author, metadata)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (calibre_id) 
        DO UPDATE SET 
            title = EXCLUDED.title,
            file_path = EXCLUDED.file_path,
            author = EXCLUDED.author,
            metadata = EXCLUDED.metadata,
            updated_at = CURRENT_TIMESTAMP
        RETURNING id
        """
        
        # Convert metadata dict to JSON for PostgreSQL
        metadata_json = json.dumps(metadata) if metadata else None
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (calibre_id, title, file_path, author, metadata_json))
            result = cursor.fetchone()
            logger.info(f"Book '{title}' inserted/updated with ID {result['id']}")
            return result['id']
    
    def get_book_by_id(self, book_id: int) -> Optional[Dict[str, Any]]:
        """Get a book by internal ID."""
        query = "SELECT * FROM books WHERE id = %s"
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (book_id,))
            book = cursor.fetchone()
            if book:
                return self._enrich_book_with_metadata(book)
            return None
    
    def get_book_by_calibre_id(self, calibre_id: int) -> Optional[Dict[str, Any]]:
        """Get a book by Calibre ID."""
        query = "SELECT * FROM books WHERE calibre_id = %s"
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (calibre_id,))
            book = cursor.fetchone()
            if book:
                return self._enrich_book_with_metadata(book)
            return None
    
    def _enrich_book_with_metadata(self, book: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich a book dict with extracted metadata and RAG status."""
        # Extract metadata from JSONB
        metadata = book.get('metadata', {}) or {}
        if isinstance(metadata, str):
            try:
                metadata = json.loads(metadata)
            except:
                metadata = {}

        book['selected_format'] = metadata.get('selected_format')
        book['available_formats'] = metadata.get('available_formats') or []
        
        # Extract publisher
        publishers = metadata.get('publishers', [])
        if publishers and isinstance(publishers, list) and len(publishers) > 0:
            book['publisher'] = publishers[0] if isinstance(publishers[0], str) else str(publishers[0])
        else:
            book['publisher'] = None
        
        # Extract year from pubdate
        pubdate = metadata.get('pubdate')
        if pubdate:
            try:
                # pubdate might be ISO format or just year
                if isinstance(pubdate, str):
                    if len(pubdate) >= 4:
                        book['year'] = int(pubdate[:4])
                    else:
                        book['year'] = int(pubdate)
                else:
                    book['year'] = pubdate
            except (ValueError, TypeError):
                book['year'] = None
        else:
            book['year'] = None
        
        # Extract ISBN from identifiers if available
        identifiers = metadata.get('identifiers', {})
        if identifiers and isinstance(identifiers, dict):
            isbn = identifiers.get('isbn')
            if isbn:
                book['isbn'] = isbn
            else:
                book['isbn'] = None
        else:
            book['isbn'] = None
        
        # Get page count from book chunks (max page_end)
        book_id = book.get('id')
        if book_id:
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT COALESCE(MAX(page_end), 0) as max_page FROM book_chunks WHERE book_id = %s",
                        (book_id,)
                    )
                    result = cursor.fetchone()
                    book['page_count'] = result[0] if result and result[0] > 0 else None
            except Exception as e:
                logger.warning(f"Error getting page count for book {book_id}: {e}")
                book['page_count'] = None
        else:
            book['page_count'] = None
        
        # Get RAG processing status
        if book_id:
            try:
                # Check if has embeddings
                book['rag_processed'] = self.has_embeddings(book_id)
                
                # Check queue status
                queue_status = self.get_queue_status(book_id)
                if queue_status:
                    book['rag_in_queue'] = queue_status['status'] in ('pending', 'processing')
                    book['rag_status'] = queue_status['status']
                    book['rag_error'] = queue_status.get('error_message')
                else:
                    book['rag_in_queue'] = False
                    book['rag_status'] = None
                    book['rag_error'] = None
            except Exception as e:
                logger.warning(f"Error getting RAG status for book {book_id}: {e}")
                book['rag_processed'] = False
                book['rag_in_queue'] = False
                book['rag_status'] = None
                book['rag_error'] = None
        else:
            book['rag_processed'] = False
            book['rag_in_queue'] = False
            book['rag_status'] = None
            book['rag_error'] = None
        
        # Extract OpenLibrary enrichment data
        openlibrary_data = metadata.get('openlibrary', {})
        if openlibrary_data and isinstance(openlibrary_data, dict):
            book['openlibrary'] = openlibrary_data
            book['openlibrary_olid'] = openlibrary_data.get('olid')
            book['openlibrary_cover_url'] = openlibrary_data.get('thumbnail_url')
            book['openlibrary_preview_url'] = openlibrary_data.get('preview_url')
            # Check if download is available (has ocaid or is public domain)
            book['openlibrary_download_available'] = bool(
                openlibrary_data.get('ocaid') or 
                openlibrary_data.get('public_domain') or
                openlibrary_data.get('preview') == 'full'
            )
        else:
            book['openlibrary'] = None
            book['openlibrary_olid'] = None
            book['openlibrary_cover_url'] = None
            book['openlibrary_preview_url'] = None
            book['openlibrary_download_available'] = False
        
        return book

    def get_all_books(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all books with pagination."""
        query = "SELECT * FROM books ORDER BY title LIMIT %s OFFSET %s"
        
        logger.info(f"PostgreSQLDB.get_all_books: executing query with limit={limit}, offset={offset}")
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (limit, offset))
            books = cursor.fetchall()
            # Enrich with metadata and RAG status
            enriched_books = [self._enrich_book_with_metadata(book) for book in books]
            logger.info(f"PostgreSQLDB.get_all_books: retrieved {len(enriched_books)} books")
            return enriched_books
    
    def search_books(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search books by title, author, or metadata.

        The first rank keeps exact phrase matches first. Natural language
        prompts like "algum livro sobre catecismo" then fall back to useful
        terms such as "catecismo" instead of requiring the full phrase.
        """
        phrase = (query or "").strip()
        terms = extract_book_search_terms(phrase)
        patterns = [f"%{phrase}%"] + [f"%{term}%" for term in terms]
        conditions = []
        params: List[Any] = []

        for rank, pattern in enumerate(patterns):
            conditions.append(
                "(CASE WHEN title ILIKE %s OR author ILIKE %s OR metadata::text ILIKE %s "
                f"THEN {rank} ELSE NULL END)"
            )
            params.extend([pattern, pattern, pattern])

        rank_expression = "LEAST(" + ", ".join(conditions) + ")"
        search_query = f"""
        SELECT *
        FROM (
            SELECT *, {rank_expression} AS search_rank
            FROM books
        ) ranked_books
        WHERE search_rank IS NOT NULL
        ORDER BY search_rank, title
        LIMIT %s
        """
        params.append(limit)

        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(search_query, params)
            books = cursor.fetchall()
            # Enrich with metadata and RAG status
            enriched_books = [self._enrich_book_with_metadata(book) for book in books]
            return enriched_books
    
    def update_book_metadata(self, book_id: int, metadata: Dict[str, Any]) -> bool:
        """Update a book's metadata in the database.
        
        Args:
            book_id: Internal PostgreSQL book ID
            metadata: Updated metadata dictionary
            
        Returns:
            True if update was successful
        """
        query = """
        UPDATE books
        SET metadata = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """
        
        metadata_json = json.dumps(metadata) if metadata else None
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (metadata_json, book_id))
            updated = cursor.rowcount > 0
            if updated:
                logger.info(f"Updated metadata for book {book_id}")
            return updated
    
    # Book chunks operations
    def insert_chunk(self, book_id: int, chunk_index: int, content: str, 
                     embedding: Optional[List[float]] = None,
                     embedding_model: Optional[str] = None,
                     page_start: Optional[int] = None,
                     page_end: Optional[int] = None,
                     section_title: Optional[str] = None) -> int:
        """Insert a book chunk with optional embedding and citation metadata."""
        query = """
        INSERT INTO book_chunks (
            book_id, chunk_index, content, embedding, embedding_model,
            page_start, page_end, section_title
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (book_id, chunk_index)
        DO UPDATE SET 
            content = EXCLUDED.content,
            embedding = EXCLUDED.embedding,
            embedding_model = EXCLUDED.embedding_model,
            page_start = EXCLUDED.page_start,
            page_end = EXCLUDED.page_end,
            section_title = EXCLUDED.section_title
        RETURNING id
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                query,
                (
                    book_id,
                    chunk_index,
                    content,
                    embedding,
                    embedding_model,
                    page_start,
                    page_end,
                    section_title,
                ),
            )
            result = cursor.fetchone()
            return result['id']
    
    def get_chunks_by_book_id(self, book_id: int) -> List[Dict[str, Any]]:
        """Get all chunks for a book."""
        query = """
        SELECT * FROM book_chunks 
        WHERE book_id = %s 
        ORDER BY chunk_index
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (book_id,))
            return cursor.fetchall()
    
    def get_chunk_count(self, book_id: int) -> int:
        """Get the number of chunks for a book."""
        query = "SELECT COUNT(*) as count FROM book_chunks WHERE book_id = %s"
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (book_id,))
            result = cursor.fetchone()
            return result['count']

    def delete_chunks_for_book(self, book_id: int) -> int:
        """Delete all chunks and embeddings for a book."""
        query = "DELETE FROM book_chunks WHERE book_id = %s"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (book_id,))
            deleted = cursor.rowcount
            logger.info(f"Deleted {deleted} chunk(s) for book {book_id}")
            return deleted
    
    def has_embeddings(self, book_id: int) -> bool:
        """Check if a book has embeddings generated."""
        query = """
        SELECT COUNT(*) as count 
        FROM book_chunks 
        WHERE book_id = %s AND embedding IS NOT NULL
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (book_id,))
            result = cursor.fetchone()
            return result['count'] > 0
    
    # Semantic search
    def semantic_search(self, query_embedding: List[float], limit: int = 10, 
                        threshold: float = 0.3, include_totals: bool = False) -> Dict[str, Any]:
        """Search for similar content using vector similarity.
        
        Args:
            query_embedding: Vector embedding for the search query
            limit: Maximum number of results to return
            threshold: Minimum similarity score (0-1)
            include_totals: If True, return total counts of chunks and pages above threshold
        
        Returns:
            Dict with 'results' list and optionally 'total_chunks' and 'total_pages'
        """
        query = """
        SELECT 
            bc.id,
            bc.id as chunk_id,
            bc.book_id,
            bc.chunk_index,
            bc.content,
            bc.page_start,
            bc.page_end,
            bc.section_title,
            b.title,
            b.author,
            b.metadata,
            b.indexed_at,
            b.updated_at,
            1 - (bc.embedding <=> %s::vector) as similarity
        FROM book_chunks bc
        JOIN books b ON bc.book_id = b.id
        WHERE bc.embedding IS NOT NULL
        ORDER BY bc.embedding <=> %s::vector
        LIMIT %s
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (query_embedding, query_embedding, limit))
            results = cursor.fetchall()
            
            # Filter by threshold and enrich with book metadata
            filtered = []
            for r in results:
                if r['similarity'] >= threshold:
                    # Create a minimal book dict for enrichment
                    book_dict = {
                        'id': r['book_id'],
                        'metadata': r.get('metadata')
                    }
                    enriched_book = self._enrich_book_with_metadata(book_dict)
                    # Add enriched fields to the result
                    r['publisher'] = enriched_book.get('publisher')
                    r['year'] = enriched_book.get('year')
                    r['isbn'] = enriched_book.get('isbn')
                    r['page_count'] = enriched_book.get('page_count')
                    r['rag_processed'] = enriched_book.get('rag_processed', False)
                    r['rag_in_queue'] = enriched_book.get('rag_in_queue', False)
                    r['rag_status'] = enriched_book.get('rag_status')
                    r['rag_error'] = enriched_book.get('rag_error')
                    filtered.append(r)
            
            logger.info(f"Semantic search returned {len(filtered)} results above threshold {threshold}")
            
            response = {"results": filtered}
            
            if include_totals:
                # Count total chunks above threshold
                count_query = """
                SELECT COUNT(*) as total_chunks
                FROM book_chunks bc
                WHERE bc.embedding IS NOT NULL
                AND 1 - (bc.embedding <=> %s::vector) >= %s
                """
                cursor.execute(count_query, (query_embedding, threshold))
                total_chunks = cursor.fetchone()['total_chunks']
                response['total_chunks'] = total_chunks
                
                # Count unique pages above threshold
                pages_query = """
                SELECT COUNT(DISTINCT bc.page_start) as total_pages
                FROM book_chunks bc
                WHERE bc.embedding IS NOT NULL
                AND bc.page_start IS NOT NULL
                AND 1 - (bc.embedding <=> %s::vector) >= %s
                """
                cursor.execute(pages_query, (query_embedding, threshold))
                total_pages = cursor.fetchone()['total_pages']
                response['total_pages'] = total_pages
                
                logger.info(f"Semantic search totals: {total_chunks} chunks, {total_pages} pages above threshold {threshold}")
            
            return response
    
    def expand_search_context(self, results: List[Dict[str, Any]], 
                              chunks_before: int = 0, chunks_after: int = 0,
                              pages_before: int = 0, pages_after: int = 0) -> List[Dict[str, Any]]:
        """Expand search results with surrounding chunks and pages.
        
        Args:
            results: Original search results
            chunks_before: Number of chunks before each result to include
            chunks_after: Number of chunks after each result to include
            pages_before: Number of pages before each result to include
            pages_after: Number of pages after each result to include
        
        Returns:
            Expanded list of chunks with context
        """
        if not results or (chunks_before == 0 and chunks_after == 0 and 
                          pages_before == 0 and pages_after == 0):
            return results
        
        expanded_chunks = {}
        seen_chunk_ids = set()
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            for result in results:
                book_id = result.get('book_id')
                chunk_index = result.get('chunk_index')
                page_start = result.get('page_start')
                
                if not book_id:
                    continue
                
                # Add the original result
                chunk_id = result.get('id')
                if chunk_id and chunk_id not in seen_chunk_ids:
                    expanded_chunks[chunk_id] = result
                    seen_chunk_ids.add(chunk_id)
                
                # Expand by chunks (chunk_index)
                if chunks_before > 0 or chunks_after > 0 and chunk_index is not None:
                    min_chunk = max(0, chunk_index - chunks_before)
                    max_chunk = chunk_index + chunks_after
                    
                    chunk_query = """
                    SELECT 
                        bc.id,
                        bc.id as chunk_id,
                        bc.book_id,
                        bc.chunk_index,
                        bc.content,
                        bc.page_start,
                        bc.page_end,
                        bc.section_title,
                        b.title,
                        b.author,
                        b.metadata
                    FROM book_chunks bc
                    JOIN books b ON bc.book_id = b.id
                    WHERE bc.book_id = %s
                    AND bc.chunk_index >= %s
                    AND bc.chunk_index <= %s
                    """
                    cursor.execute(chunk_query, (book_id, min_chunk, max_chunk))
                    context_chunks = cursor.fetchall()
                    
                    for chunk in context_chunks:
                        cid = chunk['id']
                        if cid not in seen_chunk_ids:
                            # Enrich with book metadata
                            book_dict = {
                                'id': chunk['book_id'],
                                'metadata': chunk.get('metadata')
                            }
                            enriched_book = self._enrich_book_with_metadata(book_dict)
                            chunk['publisher'] = enriched_book.get('publisher')
                            chunk['year'] = enriched_book.get('year')
                            chunk['isbn'] = enriched_book.get('isbn')
                            chunk['page_count'] = enriched_book.get('page_count')
                            chunk['rag_processed'] = enriched_book.get('rag_processed', False)
                            chunk['rag_in_queue'] = enriched_book.get('rag_in_queue', False)
                            chunk['rag_status'] = enriched_book.get('rag_status')
                            chunk['rag_error'] = enriched_book.get('rag_error')
                            expanded_chunks[cid] = chunk
                            seen_chunk_ids.add(cid)
                
                # Expand by pages (page_start)
                if pages_before > 0 or pages_after > 0 and page_start is not None:
                    min_page = max(1, page_start - pages_before)
                    max_page = page_start + pages_after
                    
                    page_query = """
                    SELECT 
                        bc.id,
                        bc.id as chunk_id,
                        bc.book_id,
                        bc.chunk_index,
                        bc.content,
                        bc.page_start,
                        bc.page_end,
                        bc.section_title,
                        b.title,
                        b.author,
                        b.metadata
                    FROM book_chunks bc
                    JOIN books b ON bc.book_id = b.id
                    WHERE bc.book_id = %s
                    AND bc.page_start IS NOT NULL
                    AND bc.page_start >= %s
                    AND bc.page_start <= %s
                    """
                    cursor.execute(page_query, (book_id, min_page, max_page))
                    page_chunks = cursor.fetchall()
                    
                    for chunk in page_chunks:
                        cid = chunk['id']
                        if cid not in seen_chunk_ids:
                            # Enrich with book metadata
                            book_dict = {
                                'id': chunk['book_id'],
                                'metadata': chunk.get('metadata')
                            }
                            enriched_book = self._enrich_book_with_metadata(book_dict)
                            chunk['publisher'] = enriched_book.get('publisher')
                            chunk['year'] = enriched_book.get('year')
                            chunk['isbn'] = enriched_book.get('isbn')
                            chunk['page_count'] = enriched_book.get('page_count')
                            chunk['rag_processed'] = enriched_book.get('rag_processed', False)
                            chunk['rag_in_queue'] = enriched_book.get('rag_in_queue', False)
                            chunk['rag_status'] = enriched_book.get('rag_status')
                            chunk['rag_error'] = enriched_book.get('rag_error')
                            expanded_chunks[cid] = chunk
                            seen_chunk_ids.add(cid)
        
        # Convert to list and sort by book_id and chunk_index for consistent ordering
        expanded_list = list(expanded_chunks.values())
        expanded_list.sort(key=lambda x: (x.get('book_id', 0), x.get('chunk_index', 0)))
        
        logger.info(f"Expanded {len(results)} results to {len(expanded_list)} chunks "
                   f"(chunks_before={chunks_before}, chunks_after={chunks_after}, "
                   f"pages_before={pages_before}, pages_after={pages_after})")
        
        return expanded_list
    
    # Processing queue operations
    def add_to_queue(self, book_id: int, priority: int = 0) -> int:
        """Add a book to the processing queue."""
        query = """
        INSERT INTO processing_queue (book_id, status, priority)
        VALUES (%s, 'pending', %s)
        RETURNING id
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (book_id, priority))
            result = cursor.fetchone()
            logger.info(f"Book {book_id} added to processing queue with ID {result['id']}")
            return result['id']
    
    def get_queue_status(self, book_id: int) -> Optional[Dict[str, Any]]:
        """Get the processing status for a book."""
        query = """
        SELECT * FROM processing_queue 
        WHERE book_id = %s 
        ORDER BY created_at DESC 
        LIMIT 1
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (book_id,))
            return cursor.fetchone()
    
    def update_queue_status(self, queue_id: int, status: str, 
                           error_message: Optional[str] = None):
        """Update the status of a queue item."""
        query = """
        UPDATE processing_queue 
        SET status = %s, 
            error_message = %s,
            completed_at = CASE WHEN %s IN ('completed', 'failed') THEN CURRENT_TIMESTAMP ELSE NULL END
        WHERE id = %s
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (status, error_message, status, queue_id))
            logger.info(f"Queue item {queue_id} updated to status: {status}")
    
    def get_pending_queue_items(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get pending items from the processing queue."""
        query = """
        SELECT pq.*, b.title
        FROM processing_queue pq
        JOIN books b ON pq.book_id = b.id
        WHERE pq.status = 'pending'
        ORDER BY pq.priority DESC, pq.created_at ASC
        LIMIT %s
        """

        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (limit,))
            return cursor.fetchall()

    def update_queue_priority(self, book_id: int, priority: int):
        """Update the priority of a queue item for a book."""
        query = """
        UPDATE processing_queue
        SET priority = %s
        WHERE book_id = %s AND status IN ('pending', 'processing')
        """

        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (priority, book_id))
            logger.info(f"Updated priority for book {book_id} to {priority}")

    def get_priority_queue_items(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get high priority items from the processing queue (priority > 0)."""
        query = """
        SELECT pq.*
        FROM processing_queue pq
        WHERE pq.status IN ('pending', 'processing') AND pq.priority > 0
        ORDER BY pq.priority DESC, pq.created_at ASC
        LIMIT %s
        """

        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (limit,))
            return cursor.fetchall()

    def get_random_book_without_embeddings(self) -> Optional[Dict[str, Any]]:
        """Get one random book that has not been embedded yet."""
        query = """
        SELECT b.*
        FROM books b
        WHERE NOT EXISTS (
            SELECT 1
            FROM book_chunks bc
            WHERE bc.book_id = b.id
              AND bc.embedding IS NOT NULL
        )
        AND NOT EXISTS (
            SELECT 1
            FROM processing_queue pq
            WHERE pq.book_id = b.id
              AND pq.status = 'failed'
        )
        ORDER BY RANDOM()
        LIMIT 1
        """

        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query)
            return cursor.fetchone()

    def get_embedding_distribution(self) -> Dict[str, Any]:
        """Return chunk distribution across the books that are actually indexed.

        The catalog (``books``) holds every Calibre title, but only a subset has
        embeddings. Averaging chunks over the whole catalog is misleading; this
        reports the distribution over indexed books only.
        """
        query = """
        SELECT
            COUNT(*) AS indexed_books,
            COALESCE(SUM(c), 0) AS total_chunks,
            COALESCE(ROUND(AVG(c)::numeric, 2), 0) AS avg_chunks_per_indexed_book,
            COALESCE(MIN(c), 0) AS min_chunks,
            COALESCE(MAX(c), 0) AS max_chunks,
            COALESCE(
                ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY c)::numeric, 1),
                0
            ) AS median_chunks
        FROM (
            SELECT book_id, COUNT(*) AS c
            FROM book_chunks
            WHERE embedding IS NOT NULL
            GROUP BY book_id
        ) per_book
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query)
            row = cursor.fetchone() or {}
            return {
                "indexed_books": int(row.get("indexed_books") or 0),
                "total_chunks": int(row.get("total_chunks") or 0),
                "avg_chunks_per_indexed_book": float(row.get("avg_chunks_per_indexed_book") or 0),
                "min_chunks": int(row.get("min_chunks") or 0),
                "max_chunks": int(row.get("max_chunks") or 0),
                "median_chunks": float(row.get("median_chunks") or 0),
            }

    def get_top_concepts(self, limit: int = 15) -> List[Dict[str, Any]]:
        """Return the most frequently cited concepts (detected section/chapter titles)."""
        query = """
        SELECT
            section_title AS concept,
            COUNT(*) AS chunks,
            COUNT(DISTINCT book_id) AS books
        FROM book_chunks
        WHERE embedding IS NOT NULL
          AND NULLIF(BTRIM(section_title), '') IS NOT NULL
        GROUP BY section_title
        ORDER BY chunks DESC, books DESC
        LIMIT %s
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (limit,))
            return [
                {
                    "concept": row["concept"],
                    "chunks": int(row["chunks"]),
                    "books": int(row["books"]),
                }
                for row in cursor.fetchall()
            ]

    def get_top_terms(
        self,
        limit: int = 25,
        sample_size: int = 6000,
        min_word_length: int = 4,
        regconfig: str = "simple",
    ) -> List[Dict[str, Any]]:
        """Return the most relevant content words across embedded chunks.

        Term frequencies are computed with PostgreSQL ``ts_stat`` over a random
        sample of embedded chunks (bounded by ``sample_size`` to keep the query
        cheap on large libraries). Stopwords, short tokens and non-alphabetic
        tokens are removed so the result highlights domain vocabulary.

        ``regconfig`` is validated against an allow-list and the inner query is
        passed to ``ts_stat`` as a bound parameter, so no caller value is
        interpolated into SQL.
        """
        inner_query, min_word_length, limit = build_top_terms_query(
            regconfig, sample_size, min_word_length, limit
        )
        query = """
        SELECT word, nentry AS occurrences, ndoc AS chunks
        FROM ts_stat(%s)
        WHERE char_length(word) >= %s
          AND word ~ '^[[:alpha:]]+$'
          AND word <> ALL(%s)
        ORDER BY nentry DESC, ndoc DESC
        LIMIT %s
        """
        stopwords = list(CONTENT_INSIGHT_STOPWORDS)
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (inner_query, min_word_length, stopwords, limit))
            return [
                {
                    "word": row["word"],
                    "occurrences": int(row["occurrences"]),
                    "chunks": int(row["chunks"]),
                }
                for row in cursor.fetchall()
            ]
    
    # Download queue operations
    def add_to_download_queue(self, title: str, author: Optional[str], source: str,
                              source_id: Optional[str], olid: Optional[str], ocaid: Optional[str],
                              download_url: Optional[str], preferred_format: str = "PDF",
                              priority: int = 0, download_available: bool = True) -> int:
        """Add a book to the download queue.
        
        Args:
            title: Book title
            author: Optional author
            source: Source ('openlibrary' or 'archive')
            source_id: Source-specific ID
            olid: OpenLibrary ID
            ocaid: Archive.org ID
            download_url: Direct download URL
            preferred_format: Preferred format
            priority: Download priority
            download_available: Whether automatic download is available
            
        Returns:
            Queue item ID
        """
        query = """
        INSERT INTO download_queue (
            title, author, source, source_id, olid, ocaid, download_url,
            preferred_format, status, priority, download_available
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s, %s)
        RETURNING id
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                query,
                (title, author, source, source_id, olid, ocaid, download_url, preferred_format, priority, download_available)
            )
            result = cursor.fetchone()
            logger.info(
                f"Added to download queue: {title} (ID: {result['id']}, download_available: {download_available})",
                extra={"operation": "download_queue_add", "queue_id": result['id'], "title": title, "download_available": download_available}
            )
            return result['id']
    
    def get_download_queue(self, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get download queue items.
        
        Args:
            status: Filter by status (pending, processing, completed, failed)
            limit: Maximum items to return
            
        Returns:
            List of queue items
        """
        if status:
            query = """
            SELECT * FROM download_queue
            WHERE status = %s
            ORDER BY priority DESC, created_at
            LIMIT %s
            """
            params = (status, limit)
        else:
            query = """
            SELECT * FROM download_queue
            ORDER BY priority DESC, created_at
            LIMIT %s
            """
            params = (limit,)
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def get_download_queue_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific download queue item.
        
        Args:
            item_id: Queue item ID
            
        Returns:
            Queue item or None
        """
        query = "SELECT * FROM download_queue WHERE id = %s"
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (item_id,))
            return cursor.fetchone()
    
    def update_download_queue_status(self, item_id: int, status: str,
                                     error_message: Optional[str] = None,
                                     file_path: Optional[str] = None,
                                     file_size: Optional[int] = None) -> bool:
        """Update download queue item status.
        
        Args:
            item_id: Queue item ID
            status: New status
            error_message: Optional error message
            file_path: Optional downloaded file path
            file_size: Optional file size
            
        Returns:
            True if updated
        """
        if status == 'processing':
            query = """
            UPDATE download_queue
            SET status = %s, started_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """
            params = (status, item_id)
        elif status == 'completed':
            query = """
            UPDATE download_queue
            SET status = %s, completed_at = CURRENT_TIMESTAMP,
                file_path = %s, file_size = %s
            WHERE id = %s
            """
            params = (status, file_path, file_size, item_id)
        elif status == 'failed':
            query = """
            UPDATE download_queue
            SET status = %s, error_message = %s, completed_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """
            params = (status, error_message, item_id)
        else:
            query = """
            UPDATE download_queue
            SET status = %s
            WHERE id = %s
            """
            params = (status, item_id)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            updated = cursor.rowcount > 0
            if updated:
                logger.info(f"Updated download queue item {item_id} to status: {status}")
            return updated
    
    def update_download_queue_priority(self, item_id: int, priority: int) -> bool:
        """Update download queue item priority.
        
        Args:
            item_id: Queue item ID
            priority: New priority
            
        Returns:
            True if updated
        """
        query = "UPDATE download_queue SET priority = %s WHERE id = %s"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (priority, item_id))
            updated = cursor.rowcount > 0
            if updated:
                logger.info(f"Updated download queue item {item_id} priority to: {priority}")
            return updated
    
    def delete_download_queue_item(self, item_id: int) -> bool:
        """Delete a download queue item.
        
        Args:
            item_id: Queue item ID
            
        Returns:
            True if deleted
        """
        query = "DELETE FROM download_queue WHERE id = %s"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (item_id,))
            deleted = cursor.rowcount > 0
            if deleted:
                logger.info(f"Deleted download queue item {item_id}")
            return deleted
    
    def get_next_pending_download(self) -> Optional[Dict[str, Any]]:
        """Get the next pending download item (highest priority).
        
        Returns:
            Queue item or None
        """
        query = """
        SELECT * FROM download_queue
        WHERE status = 'pending'
        ORDER BY priority DESC, created_at
        LIMIT 1
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query)
            return cursor.fetchone()
    
    def mark_added_to_calibre(self, item_id: int, calibre_book_id: int) -> bool:
        """Mark a downloaded book as added to Calibre.
        
        Args:
            item_id: Queue item ID
            calibre_book_id: Calibre book ID
            
        Returns:
            True if updated
        """
        query = """
        UPDATE download_queue
        SET calibre_book_id = %s, added_to_calibre_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (calibre_book_id, item_id))
            updated = cursor.rowcount > 0
            if updated:
                logger.info(f"Marked download queue item {item_id} as added to Calibre (book_id: {calibre_book_id})")
            return updated
    
    def _update_download_queue_file_hash(self, item_id: int, file_hash: str) -> bool:
        """Update file hash for a download queue item.
        
        Args:
            item_id: Queue item ID
            file_hash: SHA256 hash of the downloaded file
            
        Returns:
            True if updated
        """
        query = "UPDATE download_queue SET file_hash = %s WHERE id = %s"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (file_hash, item_id))
            updated = cursor.rowcount > 0
            if updated:
                logger.info(f"Updated file hash for download queue item {item_id}")
            return updated
    
    def find_download_queue_by_file_hash(self, file_hash: str) -> Optional[Dict[str, Any]]:
        """Find download queue item by file hash.
        
        Args:
            file_hash: SHA256 hash of the file
            
        Returns:
            Queue item or None
        """
        query = "SELECT * FROM download_queue WHERE file_hash = %s"
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (file_hash,))
            return cursor.fetchone()
    
    def find_download_queue_by_file_path(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Find download queue item by file path.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Queue item or None
        """
        query = "SELECT * FROM download_queue WHERE file_path = %s"
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (file_path,))
            return cursor.fetchone()


# Global instance
postgres_db = PostgreSQLDB()
