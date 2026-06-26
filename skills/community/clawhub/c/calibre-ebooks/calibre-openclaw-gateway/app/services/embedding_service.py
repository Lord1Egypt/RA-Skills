import httpx
from typing import Any, Callable, List, Optional
from pathlib import Path

from app.config import settings
from app.database.postgres_db import postgres_db
from app.services.conversion_service import conversion_service
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Setting keys used to track which embedding configuration produced the data.
SIGNATURE_KEY = "embedding_signature"
MODEL_KEY = "embedding_model"
DIMENSION_KEY = "embedding_dimension"
CITATION_SCHEMA_VERSION = 2


class EmptyDocumentError(Exception):
    """Raised when a document yields no usable text to embed."""


class ContextLengthExceededError(Exception):
    """Raised when a chunk is too long for the embedding model's context window.

    Token-dense text (e.g. dense math notation) can produce far more tokens than
    its character count suggests, overflowing the model's context length even
    when CHUNK_SIZE looks safe. Callers can catch this and split the text.
    """


class EmbeddingRunInterrupted(BaseException):
    """Raised when a scheduled embedding run must stop without failing the item."""


class EmbeddingService:
    """Service for generating and managing embeddings using Ollama."""
    
    def __init__(self):
        self.client = httpx.Client(timeout=300.0)  # 5 minute timeout for large documents
        self._dimension: Optional[int] = None
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text using Ollama."""
        try:
            response = self.client.post(
                f"{settings.OLLAMA_HOST}/api/embeddings",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": text
                }
            )
            response.raise_for_status()
            data = response.json()
            embedding = data.get("embedding", [])
            if not embedding:
                raise ValueError(
                    f"Ollama returned an empty embedding for model "
                    f"'{settings.OLLAMA_MODEL}' (is the model pulled and running?)"
                )
            logger.info(f"Generated embedding for text ({len(text)} chars) -> vector size: {len(embedding)}")
            return embedding
        except httpx.HTTPStatusError as e:
            # Surface the real Ollama error body, which raise_for_status hides.
            body = ""
            try:
                body = e.response.text
            except Exception:
                pass
            if "context length" in body.lower() or "exceeds" in body.lower():
                raise ContextLengthExceededError(
                    f"Chunk of {len(text)} chars exceeds the model context window: {body}"
                ) from e
            logger.error(f"Error generating embedding: {e} - response body: {body}")
            raise
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def get_model_dimension(self) -> int:
        """Probe the active Ollama model to discover its embedding dimension."""
        if self._dimension is None:
            probe = self.generate_embedding("dimension probe")
            self._dimension = len(probe)
            logger.info(
                f"Embedding model '{settings.OLLAMA_MODEL}' produces "
                f"{self._dimension}-dimensional vectors"
            )
        return self._dimension
    
    def _build_signature(self, dimension: int) -> str:
        """Build a signature describing the current embedding configuration.

        Any change to this signature (model, vector dimension, chunk settings or
        the manual EMBEDDING_VERSION) means stored embeddings are stale and must
        be regenerated.
        """
        return (
            f"model={settings.OLLAMA_MODEL}"
            f"|dim={dimension}"
            f"|chunk={settings.CHUNK_SIZE}"
            f"|overlap={settings.CHUNK_OVERLAP}"
            f"|citation_schema={CITATION_SCHEMA_VERSION}"
            f"|v={settings.EMBEDDING_VERSION}"
        )
    
    def get_version_info(self) -> dict:
        """Return the current and stored embedding configuration signatures."""
        stored_sig = postgres_db.get_setting(SIGNATURE_KEY)
        info = {
            "model": settings.OLLAMA_MODEL,
            "chunk_size": settings.CHUNK_SIZE,
            "chunk_overlap": settings.CHUNK_OVERLAP,
            "embedding_version": settings.EMBEDDING_VERSION,
            "citation_schema_version": CITATION_SCHEMA_VERSION,
            "stored_signature": stored_sig,
            "stored_model": postgres_db.get_setting(MODEL_KEY),
            "stored_dimension": postgres_db.get_setting(DIMENSION_KEY),
        }
        try:
            dimension = self.get_model_dimension()
            info["dimension"] = dimension
            info["current_signature"] = self._build_signature(dimension)
            info["up_to_date"] = stored_sig == info["current_signature"]
        except Exception as e:
            info["dimension"] = None
            info["current_signature"] = None
            info["up_to_date"] = None
            info["error"] = str(e)
        return info
    
    def _store_signature(self, dimension: int, signature: str):
        postgres_db.set_setting(SIGNATURE_KEY, signature)
        postgres_db.set_setting(MODEL_KEY, settings.OLLAMA_MODEL)
        postgres_db.set_setting(DIMENSION_KEY, str(dimension))
    
    def reconcile_embedding_version(self) -> dict:
        """Ensure stored embeddings match the active embedding configuration.

        If the configuration signature changed (e.g. a new embedding LLM), every
        stored embedding is invalidated and reset so the worker regenerates it
        with the new model. On first run the current signature is recorded as a
        baseline without touching existing data.
        """
        try:
            dimension = self.get_model_dimension()
        except Exception as e:
            logger.error(
                "Could not probe embedding model; skipping version reconciliation: %s",
                e,
            )
            return {"changed": False, "error": str(e)}

        current_sig = self._build_signature(dimension)
        stored_sig = postgres_db.get_setting(SIGNATURE_KEY)
        missing_citations = postgres_db.count_embeddings_missing_citation_metadata()

        if stored_sig is None:
            if missing_citations:
                invalidated = postgres_db.invalidate_all_embeddings(dimension)
                self._store_signature(dimension, current_sig)
                logger.warning(
                    "Invalidated %s embedding(s) missing citation metadata; "
                    "they will be regenerated with page/section citations.",
                    invalidated,
                )
                return {
                    "changed": True,
                    "invalidated": invalidated,
                    "reason": "missing_citation_metadata",
                    "new_signature": current_sig,
                }
            self._store_signature(dimension, current_sig)
            logger.info("Embedding signature baseline recorded: %s", current_sig)
            return {"changed": False, "baseline": True, "signature": current_sig}

        if stored_sig == current_sig and not missing_citations:
            logger.info("Embedding signature unchanged: %s", current_sig)
            return {"changed": False, "signature": current_sig}

        if stored_sig == current_sig and missing_citations:
            logger.warning(
                "%s embedding(s) are missing citation metadata despite current "
                "signature; invalidating for regeneration.",
                missing_citations,
            )

        logger.warning(
            "Embedding configuration changed; invalidating all embeddings.\n"
            "  old: %s\n  new: %s",
            stored_sig,
            current_sig,
        )
        invalidated = postgres_db.invalidate_all_embeddings(dimension)
        self._store_signature(dimension, current_sig)
        logger.warning(
            "Invalidated %s embedding(s); they will be regenerated by the worker.",
            invalidated,
        )
        return {
            "changed": True,
            "invalidated": invalidated,
            "old_signature": stored_sig,
            "new_signature": current_sig,
        }
    
    def generate_embeddings_for_book(
        self,
        book_id: int,
        pdf_path: Path,
        should_stop: Optional[Callable[[], bool]] = None,
    ) -> int:
        """Generate and store embeddings for all chunks of a book."""
        try:
            logger.info(
                f"Starting embedding generation for book {book_id}",
                extra={
                    "operation": "embedding_book_start",
                    "book_id": book_id,
                    "format": pdf_path.suffix.lstrip(".").upper(),
                },
            )
            # Convert PDF to citeable chunks. Each chunk keeps page and a best
            # effort chapter/section heading so RAG answers can cite location.
            chunks = conversion_service.pdf_to_page_chunks(pdf_path)
            if not chunks:
                raise EmptyDocumentError(
                    f"Book {book_id} produced no usable text (scanned PDF needing OCR?)"
                )
            expected_dim = self.get_model_dimension()
            postgres_db.delete_chunks_for_book(book_id)
            total_chunks = len(chunks)
            logger.info(
                f"Book {book_id} text converted into {total_chunks} chunks",
                extra={
                    "operation": "embedding_chunks_ready",
                    "book_id": book_id,
                    "total": total_chunks,
                },
            )
            
            # Generate embeddings for each chunk, validating dimensions.
            # Token-dense chunks (e.g. dense math) may overflow the model's
            # context window even when their character count is within
            # CHUNK_SIZE; those are split and retried instead of failing the
            # whole book.
            stored = 0
            for index, chunk in enumerate(chunks, start=1):
                if should_stop and should_stop():
                    raise EmbeddingRunInterrupted(
                        f"Embedding run interrupted before chunk {index}/{total_chunks}"
                    )
                stored += self._embed_and_store_chunk(
                    book_id, stored, chunk, expected_dim
                )
                if index == total_chunks or index % 25 == 0:
                    logger.info(
                        f"Embedding progress for book {book_id}: {index}/{total_chunks} chunks scanned, {stored} stored",
                        extra={
                            "operation": "embedding_progress",
                            "book_id": book_id,
                            "current": index,
                            "total": total_chunks,
                            "count": stored,
                        },
                    )
            
            logger.info(
                f"Generated {stored} embeddings for book {book_id}",
                extra={
                    "operation": "embedding_book_finished",
                    "book_id": book_id,
                    "count": stored,
                    "total": total_chunks,
                },
            )
            return stored
        except Exception as e:
            logger.error(f"Error generating embeddings for book {book_id}: {e}")
            raise

    def _embed_and_store_chunk(
        self,
        book_id: int,
        next_index: int,
        chunk: Any,
        expected_dim: int,
        min_chars: int = 80,
        depth: int = 0,
    ) -> int:
        """Embed and store a single chunk, splitting it on context overflow.

        Returns the number of embeddings stored (>1 when the chunk had to be
        split). When a fragment is still too dense to embed even at the minimum
        size, it is skipped (logged) rather than aborting the whole book.
        """
        chunk_info = self._normalize_chunk_info(chunk)
        content = chunk_info["content"]

        try:
            embedding = self.generate_embedding(content)
        except ContextLengthExceededError:
            if len(content) <= min_chars or depth >= 12:
                logger.warning(
                    "Skipping un-embeddable fragment for book %s "
                    "(%s chars still exceeds context window after splitting)",
                    book_id,
                    len(content),
                )
                return 0
            left, right = self._split_text(content)
            logger.info(
                "Chunk for book %s exceeded context window; splitting "
                "%s chars -> %s + %s chars (depth=%s)",
                book_id,
                len(content),
                len(left),
                len(right),
                depth + 1,
            )
            left_info = {**chunk_info, "content": left}
            right_info = {**chunk_info, "content": right}
            stored = self._embed_and_store_chunk(
                book_id, next_index, left_info, expected_dim, min_chars, depth + 1
            )
            stored += self._embed_and_store_chunk(
                book_id, next_index + stored, right_info, expected_dim, min_chars, depth + 1
            )
            return stored

        if len(embedding) != expected_dim:
            raise ValueError(
                f"Embedding dimension mismatch for book {book_id} "
                f"(got {len(embedding)}, expected {expected_dim}). "
                f"Model '{settings.OLLAMA_MODEL}' may have changed."
            )
        postgres_db.insert_chunk(
            book_id,
            next_index,
            content,
            embedding,
            settings.OLLAMA_MODEL,
            page_start=chunk_info.get("page_start"),
            page_end=chunk_info.get("page_end"),
            section_title=chunk_info.get("section_title"),
        )
        return 1

    @staticmethod
    def _normalize_chunk_info(chunk: Any) -> dict:
        if isinstance(chunk, dict):
            return {
                "content": chunk.get("content") or chunk.get("text") or "",
                "page_start": chunk.get("page_start") or chunk.get("page"),
                "page_end": chunk.get("page_end") or chunk.get("page_start") or chunk.get("page"),
                "section_title": chunk.get("section_title") or chunk.get("section"),
            }
        return {
            "content": chunk,
            "page_start": None,
            "page_end": None,
            "section_title": None,
        }

    @staticmethod
    def _format_citation(result: dict) -> str:
        """Build a human-readable citation from search metadata."""
        location_parts = []
        page_start = result.get("page_start")
        page_end = result.get("page_end")
        if page_start and page_end and page_start != page_end:
            location_parts.append(f"pp. {page_start}-{page_end}")
        elif page_start:
            location_parts.append(f"p. {page_start}")

        section_title = result.get("section_title")
        if section_title:
            location_parts.append(f"section/chapter: {section_title}")

        location = (
            "; ".join(location_parts)
            if location_parts
            else "location not provided"
        )
        title = result.get("title") or f"book_id {result.get('book_id')}"
        author = result.get("author")
        if author:
            return f"{title}, {author} ({location})"
        return f"{title} ({location})"

    @staticmethod
    def _split_text(text: str) -> tuple[str, str]:
        """Split text near the middle, preferring a whitespace boundary."""
        mid = len(text) // 2
        boundary = text.rfind(" ", 0, mid)
        if boundary <= 0:
            boundary = text.find(" ", mid)
        if boundary <= 0:
            boundary = mid
        return text[:boundary].strip(), text[boundary:].strip()
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a search query."""
        return self.generate_embedding(query)
    
    def search_similar_content(self, query: str, limit: int = 10, 
                               threshold: float = None, include_totals: bool = False,
                               chunks_before: int = 0, chunks_after: int = 0,
                               pages_before: int = 0, pages_after: int = 0) -> Any:
        """Search for similar content using semantic search.
        
        Args:
            query: Search query text
            limit: Maximum number of results to return
            threshold: Minimum similarity score (0-1)
            include_totals: If True, return total counts of chunks and pages above threshold
            chunks_before: Number of chunks before each result to include
            chunks_after: Number of chunks after each result to include
            pages_before: Number of pages before each result to include
            pages_after: Number of pages after each result to include
        
        Returns:
            When include_totals=False: List of result dicts (backward compatible)
            When include_totals=True: Dict with 'results' list and 'total_chunks'/'total_pages'
        """
        threshold = threshold or settings.SIMILARITY_THRESHOLD
        
        try:
            # Generate embedding for query
            query_embedding = self.generate_query_embedding(query)
            
            # Perform semantic search in PostgreSQL
            response = postgres_db.semantic_search(query_embedding, limit, threshold, include_totals)
            results = response.get('results', [])
            
            # Expand context if requested
            if chunks_before > 0 or chunks_after > 0 or pages_before > 0 or pages_after > 0:
                results = postgres_db.expand_search_context(
                    results, chunks_before, chunks_after, pages_before, pages_after
                )
            
            for result in results:
                result["citation"] = self._format_citation(result)
            
            logger.info(f"Semantic search for '{query}' returned {len(results)} results")
            
            if include_totals:
                return {
                    'results': results,
                    'total_chunks': response.get('total_chunks'),
                    'total_pages': response.get('total_pages')
                }
            
            # Backward compatible: return list directly when include_totals=False
            return results
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            raise
    
    def check_embeddings_status(self, book_id: int) -> dict:
        """Check if embeddings are ready for a book."""
        try:
            has_embeddings = postgres_db.has_embeddings(book_id)
            chunk_count = postgres_db.get_chunk_count(book_id)
            
            return {
                "book_id": book_id,
                "has_embeddings": has_embeddings,
                "chunk_count": chunk_count,
                "ready": has_embeddings and chunk_count > 0
            }
        except Exception as e:
            logger.error(f"Error checking embeddings status for book {book_id}: {e}")
            return {
                "book_id": book_id,
                "has_embeddings": False,
                "chunk_count": 0,
                "ready": False,
                "error": str(e)
            }
    
    def queue_embedding_generation(self, book_id: int, pdf_path: Path, priority: int = 0) -> dict:
        """Queue a book for embedding generation."""
        try:
            # Check if already queued
            existing = postgres_db.get_queue_status(book_id)
            if existing and existing['status'] in ['pending', 'processing']:
                logger.info(
                    f"Book {book_id} is already in embedding queue with status {existing['status']}",
                    extra={
                        "operation": "embedding_already_queued",
                        "book_id": book_id,
                        "queue_id": existing["id"],
                    },
                )
                return {
                    "book_id": book_id,
                    "status": "already_queued",
                    "queue_id": existing['id'],
                    "queue_status": existing['status']
                }

            # Add to queue with specified priority
            queue_id = postgres_db.add_to_queue(book_id, priority=priority)

            logger.info(f"Book {book_id} queued for embedding generation with priority {priority} (queue_id: {queue_id})")
            return {
                "book_id": book_id,
                "status": "queued",
                "queue_id": queue_id
            }
        except Exception as e:
            logger.error(f"Error queuing embedding generation for book {book_id}: {e}")
            raise
    
    def process_queue_item(
        self,
        queue_id: int,
        book_id: int,
        pdf_path: Path,
        should_stop: Optional[Callable[[], bool]] = None,
    ) -> int:
        """Process a single queue item (background task)."""
        try:
            logger.info(
                f"Starting queue item {queue_id} for book {book_id}",
                extra={
                    "operation": "queue_item_start",
                    "queue_id": queue_id,
                    "book_id": book_id,
                },
            )
            # Update status to processing
            postgres_db.update_queue_status(queue_id, 'processing')
            
            # Generate embeddings
            chunk_count = self.generate_embeddings_for_book(book_id, pdf_path, should_stop)
            
            # Update status to completed
            postgres_db.update_queue_status(queue_id, 'completed')
            
            logger.info(
                f"Successfully processed queue item {queue_id} for book {book_id} ({chunk_count} chunks)",
                extra={
                    "operation": "queue_item_finished",
                    "queue_id": queue_id,
                    "book_id": book_id,
                    "count": chunk_count,
                },
            )
            return chunk_count
        except Exception as e:
            # Update status to failed
            postgres_db.update_queue_status(queue_id, 'failed', str(e))
            logger.error(
                f"Failed to process queue item {queue_id} for book {book_id}: {e}",
                exc_info=True,
                extra={
                    "operation": "queue_item_failed",
                    "queue_id": queue_id,
                    "book_id": book_id,
                },
            )
            raise
    
    def get_queue_status(self, book_id: int) -> Optional[dict]:
        """Get the current queue status for a book."""
        return postgres_db.get_queue_status(book_id)
    
    def get_all_queue_items(self, limit: int = 20) -> List[dict]:
        """Get all queue items."""
        return postgres_db.get_pending_queue_items(limit)


embedding_service = EmbeddingService()
