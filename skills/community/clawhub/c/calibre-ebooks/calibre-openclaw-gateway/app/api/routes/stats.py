from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from datetime import datetime, timedelta
from pathlib import Path
import time

from app.database.postgres_db import postgres_db
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/stats", tags=["statistics"])


def calculate_library_size() -> int:
    """Calculate total size of the Calibre library in bytes."""
    try:
        library_path = Path(settings.CALIBRE_LIBRARY_PATH)
        if not library_path.exists():
            return 0
        
        total_size = 0
        for item in library_path.rglob('*'):
            if item.is_file():
                total_size += item.stat().st_size
        
        logger.info(f"Calculated library size: {total_size} bytes ({total_size / (1024**3):.2f} GB)")
        return total_size
    except Exception as e:
        logger.error(f"Error calculating library size: {e}")
        return 0


def should_recalculate_storage() -> bool:
    """Check if storage should be recalculated."""
    try:
        last_calc = postgres_db.get_last_storage_calc_time()
        current_time = time.time()
        
        # If never calculated, calculate now
        if last_calc is None:
            return True
        
        # Check if more than 24 hours have passed
        hours_since_calc = (current_time - last_calc) / 3600
        if hours_since_calc >= 24:
            # Check if metadata.db has been modified since last calculation
            calibre_db_path = Path(settings.CALIBRE_DB_PATH)
            if calibre_db_path.exists():
                current_mtime = calibre_db_path.stat().st_mtime
                stored_mtime = postgres_db.get_calibre_db_mtime()
                
                # If metadata.db was modified after last storage calc, recalculate
                if stored_mtime and current_mtime > stored_mtime:
                    return True
        
        return False
    except Exception as e:
        logger.error(f"Error checking if storage should be recalculated: {e}")
        return False


def get_cached_library_size() -> int:
    """Get cached library size or calculate if needed."""
    try:
        if should_recalculate_storage():
            library_size = calculate_library_size()
            postgres_db.set_last_storage_calc_time(time.time())
            return library_size
        else:
            # Return cached value - for now, we'll recalculate since we don't have a cache table
            # In a real implementation, you'd store this in the settings table
            return calculate_library_size()
    except Exception as e:
        logger.error(f"Error getting library size: {e}")
        return 0


@router.get("/database")
async def get_database_stats() -> Dict[str, Any]:
    """Get database statistics including books, chunks, embeddings, and queries."""
    try:
        with postgres_db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Combine queries for better performance
            cursor.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM books) as total_books,
                    (SELECT COUNT(*) FROM book_chunks) as total_chunks,
                    (SELECT COUNT(*) FROM book_chunks WHERE embedding IS NOT NULL) as chunks_with_embeddings,
                    (SELECT COUNT(DISTINCT book_id) FROM book_chunks WHERE embedding IS NOT NULL) as books_with_embeddings,
                    (SELECT COUNT(*) FROM processing_queue WHERE status = 'pending') as pending_queue,
                    (SELECT COUNT(*) FROM processing_queue WHERE status = 'processing') as processing_queue,
                    (SELECT COUNT(*) FROM processing_queue WHERE status = 'completed') as completed_queue,
                    (SELECT COUNT(*) FROM processing_queue WHERE status = 'failed') as failed_queue,
                    (SELECT COUNT(*) FROM download_queue WHERE status = 'pending') as download_pending,
                    (SELECT COUNT(*) FROM download_queue WHERE status = 'processing') as download_processing,
                    (SELECT COUNT(*) FROM download_queue WHERE status = 'completed') as download_completed,
                    (SELECT COUNT(*) FROM download_queue WHERE status = 'failed') as download_failed,
                    (SELECT COUNT(*) FROM books WHERE updated_at >= NOW() - INTERVAL '24 hours') as activity_24h
            """)
            
            row = cursor.fetchone()
            
            total_books = row[0]
            total_chunks = row[1]
            chunks_with_embeddings = row[2]
            books_with_embeddings = row[3]
            pending_queue = row[4]
            processing_queue = row[5]
            completed_queue = row[6]
            failed_queue = row[7]
            download_pending = row[8]
            download_processing = row[9]
            download_completed = row[10]
            download_failed = row[11]
            activity_24h = row[12]
            
            total_embeddings = chunks_with_embeddings
            
            # Storage size estimates
            cursor.execute("SELECT pg_total_relation_size('books') + pg_total_relation_size('book_chunks')")
            db_storage_size = cursor.fetchone()[0]
            
            # Library size (calculated periodically)
            library_size = get_cached_library_size()
            
            return {
                "books": {
                    "total": total_books,
                    "with_embeddings": books_with_embeddings,
                    "without_embeddings": total_books - books_with_embeddings
                },
                "chunks": {
                    "total": total_chunks,
                    "with_embeddings": chunks_with_embeddings,
                    "without_embeddings": total_chunks - chunks_with_embeddings
                },
                "embeddings": {
                    "total_stored": total_embeddings,
                    "utilization_rate": round((chunks_with_embeddings / total_chunks * 100) if total_chunks > 0 else 0, 2),
                    # Average over INDEXED books only. Dividing total chunks by
                    # the whole catalog (total_books) is misleading because most
                    # titles are not embedded yet.
                    "indexed_books": books_with_embeddings,
                    "avg_chunks_per_indexed_book": round(
                        (total_chunks / books_with_embeddings) if books_with_embeddings > 0 else 0,
                        2,
                    ),
                    "avg_chunks_per_catalog_book": round(
                        (total_chunks / total_books) if total_books > 0 else 0,
                        2,
                    ),
                },
                "processing_queue": {
                    "pending": pending_queue,
                    "processing": processing_queue,
                    "completed": completed_queue,
                    "failed": failed_queue
                },
                "download_queue": {
                    "pending": download_pending,
                    "processing": download_processing,
                    "completed": download_completed,
                    "failed": download_failed
                },
                "activity": {
                    "last_24_hours": activity_24h
                },
                "storage": {
                    "database_size_bytes": db_storage_size,
                    "database_size_mb": round(db_storage_size / (1024 * 1024), 2),
                    "library_size_bytes": library_size,
                    "library_size_mb": round(library_size / (1024 * 1024), 2),
                    "library_size_gb": round(library_size / (1024**3), 2),
                    "total_size_bytes": db_storage_size + library_size,
                    "total_size_mb": round((db_storage_size + library_size) / (1024 * 1024), 2),
                    "total_size_gb": round((db_storage_size + library_size) / (1024**3), 2)
                },
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        logger.error(f"Error getting database stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/queries")
async def get_query_stats() -> Dict[str, Any]:
    """Get query statistics (placeholder for future query tracking)."""
    try:
        # This is a placeholder - you can add query tracking in the future
        # For now, we'll return basic info
        return {
            "total_queries": 0,
            "semantic_searches": 0,
            "metadata_searches": 0,
            "timestamp": datetime.utcnow().isoformat(),
            "note": "Query tracking not yet implemented"
        }
    except Exception as e:
        logger.error(f"Error getting query stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/library")
async def get_library_summary() -> Dict[str, Any]:
    """Get reader-facing Calibre catalog and RAG summary statistics."""
    try:
        with postgres_db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM books")
            total_books = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(DISTINCT book_id)
                FROM book_chunks
            """)
            books_with_chunks = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(DISTINCT book_id)
                FROM book_chunks
                WHERE embedding IS NOT NULL
            """)
            books_with_embeddings = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(DISTINCT author_name)
                FROM (
                    SELECT NULLIF(BTRIM(author_name), '') AS author_name
                    FROM books,
                         regexp_split_to_table(COALESCE(author, ''), '\\s*,\\s*') AS author_name
                ) authors
                WHERE author_name IS NOT NULL
            """)
            total_authors = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(DISTINCT publisher_name)
                FROM books,
                     LATERAL jsonb_array_elements_text(
                         COALESCE(metadata::jsonb -> 'publishers', '[]'::jsonb)
                     ) AS publisher_name
                WHERE NULLIF(BTRIM(publisher_name), '') IS NOT NULL
            """)
            total_publishers = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(DISTINCT category_name)
                FROM books,
                     LATERAL jsonb_array_elements_text(
                         COALESCE(metadata::jsonb -> 'tags', '[]'::jsonb)
                     ) AS category_name
                WHERE NULLIF(BTRIM(category_name), '') IS NOT NULL
            """)
            total_categories = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM book_chunks")
            total_chunks = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM book_chunks WHERE embedding IS NOT NULL")
            chunks_with_embeddings = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COALESCE(embedding_model, 'unknown') AS model, COUNT(*) AS chunks
                FROM book_chunks
                WHERE embedding IS NOT NULL
                GROUP BY embedding_model
                ORDER BY chunks DESC, model
            """)
            embedding_models = [
                {"model": row[0], "chunks": row[1]}
                for row in cursor.fetchall()
            ]

            configured_model = settings.OLLAMA_MODEL.split(":", 1)[0]
            embedding_coverage = round(
                (chunks_with_embeddings / total_chunks * 100) if total_chunks > 0 else 0,
                2,
            )
            indexed_coverage = round(
                (books_with_chunks / total_books * 100) if total_books > 0 else 0,
                2,
            )

            return {
                "indexed_books": total_books,
                "authors": total_authors,
                "publishers": total_publishers,
                "categories": total_categories,
                "cataloged_topics": total_categories,
                "rag": {
                    "books_with_excerpts": books_with_chunks,
                    "books_with_embeddings": books_with_embeddings,
                    "chunks_excerpts": total_chunks,
                    "chunks_with_embeddings": chunks_with_embeddings,
                    "embedding_model": configured_model,
                    "configured_embedding_model": settings.OLLAMA_MODEL,
                    "models_found_in_chunks": embedding_models,
                    "chunk_size": settings.CHUNK_SIZE,
                    "overlap": settings.CHUNK_OVERLAP,
                },
                "library_status": {
                    "books_in_catalog": total_books,
                    "books_indexed_in_rag": books_with_chunks,
                    "indexing_coverage_percent": indexed_coverage,
                    "chunks_with_embeddings": chunks_with_embeddings,
                    "embedding_coverage_percent": embedding_coverage,
                    "cataloged_topics": total_categories,
                    "cataloged_authors": total_authors,
                    "cataloged_publishers": total_publishers,
                    "embedding_model": configured_model,
                    "chunk_size": settings.CHUNK_SIZE,
                    "overlap": settings.CHUNK_OVERLAP,
                },
                "timestamp": datetime.utcnow().isoformat(),
            }
    except Exception as e:
        logger.error(f"Error getting library summary stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/content-insights")
async def get_content_insights(
    top_words: int = 25,
    top_concepts: int = 15,
    sample_size: int = 6000,
    min_word_length: int = 4,
    language: str = "simple",
) -> Dict[str, Any]:
    """Diagnostic insights over embedded content.

    Combines the per-indexed-book chunk distribution with the most relevant
    words and most frequently cited concepts (detected section/chapter titles).
    Term frequencies are sampled to stay cheap on large libraries.
    """
    try:
        distribution = postgres_db.get_embedding_distribution()
        concepts = postgres_db.get_top_concepts(limit=top_concepts)
        terms = postgres_db.get_top_terms(
            limit=top_words,
            sample_size=sample_size,
            min_word_length=min_word_length,
            regconfig=language,
        )
        logger.info(
            "Content insights computed: indexed_books=%s, avg_chunks=%s, "
            "top_words=%s, top_concepts=%s, sample_size=%s",
            distribution.get("indexed_books"),
            distribution.get("avg_chunks_per_indexed_book"),
            len(terms),
            len(concepts),
            sample_size,
        )
        return {
            "distribution": distribution,
            "top_relevant_words": terms,
            "top_concepts": concepts,
            "params": {
                "top_words": top_words,
                "top_concepts": top_concepts,
                "sample_size": sample_size,
                "min_word_length": min_word_length,
                "language": language,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error computing content insights: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/overview")
async def get_overview_stats() -> Dict[str, Any]:
    """Get overview statistics combining all metrics."""
    try:
        db_stats = await get_database_stats()
        query_stats = await get_query_stats()
        
        return {
            "database": db_stats,
            "queries": query_stats,
            "summary": {
                "total_books": db_stats["books"]["total"],
                "total_embeddings": db_stats["embeddings"]["total_stored"],
                "embedding_coverage": db_stats["embeddings"]["utilization_rate"],
                "queue_status": {
                    "pending": db_stats["processing_queue"]["pending"],
                    "processing": db_stats["processing_queue"]["processing"]
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting overview stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
