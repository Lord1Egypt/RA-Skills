from fastapi import APIRouter, HTTPException, BackgroundTasks
from pathlib import Path
from typing import List
from pydantic import BaseModel

from app.models import (
    EmbeddingStatusResponse,
    EmbeddingQueueResponse,
    QueueItemResponse,
    EmbeddingModelInfoResponse,
    EmbeddingReindexResponse,
)
from app.services.book_service import book_service
from app.services.embedding_service import embedding_service
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/embeddings", tags=["embeddings"])


class PriorityQueueRequest(BaseModel):
    book_ids: List[int]


@router.get("/model", response_model=EmbeddingModelInfoResponse)
async def get_embedding_model_info():
    """Get the active embedding model and version/signature information.

    Use this to verify whether stored embeddings match the current model
    configuration (``up_to_date``).
    """
    try:
        return EmbeddingModelInfoResponse(**embedding_service.get_version_info())
    except Exception as e:
        logger.error(f"Error getting embedding model info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/reindex", response_model=EmbeddingReindexResponse)
async def reindex_embeddings():
    """Force a re-check of the embedding version.

    If the model/configuration signature changed, all stored embeddings are
    invalidated and re-queued so the worker regenerates them with the current
    model. Safe to call repeatedly: it is a no-op when already up to date.
    """
    try:
        return EmbeddingReindexResponse(**embedding_service.reconcile_embedding_version())
    except Exception as e:
        logger.error(f"Error reindexing embeddings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/status/{book_id}", response_model=EmbeddingStatusResponse)
async def get_embedding_status(book_id: int):
    """Check if embeddings are ready for a book."""
    try:
        status = embedding_service.check_embeddings_status(book_id)
        return EmbeddingStatusResponse(**status)
    except Exception as e:
        logger.error(f"Error checking embedding status for book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/generate/{book_id}", response_model=EmbeddingQueueResponse)
async def generate_embeddings(book_id: int, background_tasks: BackgroundTasks):
    """Request generation of embeddings for a book."""
    try:
        # Check if book exists
        book = book_service.get_book(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Server-side embedding generation still uses the PDF conversion path.
        pdf_path = book_service.get_book_pdf_path(book_id)
        if not pdf_path or not pdf_path.exists():
            raise HTTPException(status_code=404, detail="Selected book file is not an available PDF")
        
        # Queue the embedding generation
        queue_response = embedding_service.queue_embedding_generation(book_id, pdf_path)
        
        # If it's a new queue item, start background processing
        if queue_response['status'] == 'queued':
            queue_id = queue_response['queue_id']
            background_tasks.add_task(
                embedding_service.process_queue_item,
                queue_id,
                book_id,
                pdf_path
            )
        
        return EmbeddingQueueResponse(**queue_response)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error queuing embedding generation for book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/queue", response_model=list[QueueItemResponse])
async def get_queue(limit: int = 20):
    """Get the current processing queue."""
    try:
        queue_items = embedding_service.get_all_queue_items(limit)
        return [QueueItemResponse(**item) for item in queue_items]
    except Exception as e:
        logger.error(f"Error getting queue: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/queue/{book_id}", response_model=QueueItemResponse)
async def get_book_queue_status(book_id: int):
    """Get the queue status for a specific book."""
    try:
        queue_status = embedding_service.get_queue_status(book_id)
        if not queue_status:
            raise HTTPException(status_code=404, detail="No queue item found for this book")
        return QueueItemResponse(**queue_status)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting queue status for book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/priority-queue")
async def add_to_priority_queue(request: PriorityQueueRequest, background_tasks: BackgroundTasks):
    """Add books to priority queue for immediate RAG processing."""
    try:
        queued_count = 0
        for book_id in request.book_ids:
            # Check if book exists
            book = book_service.get_book(book_id)
            if not book:
                logger.warning(f"Book {book_id} not found, skipping")
                continue

            # Get PDF path
            pdf_path = book_service.get_book_pdf_path(book_id)
            if not pdf_path or not pdf_path.exists():
                logger.warning(f"PDF not found for book {book_id}, skipping")
                continue

            # Add to queue with high priority (priority=100)
            queue_response = embedding_service.queue_embedding_generation(book_id, pdf_path, priority=100)

            # If it's a new queue item, start background processing
            if queue_response['status'] == 'queued':
                queue_id = queue_response['queue_id']
                background_tasks.add_task(
                    embedding_service.process_queue_item,
                    queue_id,
                    book_id,
                    pdf_path
                )
                queued_count += 1
            elif queue_response['status'] == 'already_queued':
                logger.info(f"Book {book_id} already in queue, updating priority")
                # Update priority to high
                from app.database.postgres_db import postgres_db
                postgres_db.update_queue_priority(book_id, 100)
                queued_count += 1

        logger.info(f"Added {queued_count} books to priority queue")
        return {"queued_count": queued_count, "message": f"Queued {queued_count} books for immediate processing"}
    except Exception as e:
        logger.error(f"Error adding books to priority queue: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/priority-queue")
async def get_priority_queue():
    """Get the current priority queue (high priority items)."""
    try:
        from app.database.postgres_db import postgres_db
        queue_items = postgres_db.get_priority_queue_items(limit=20)

        # Enrich with book information
        enriched_items = []
        for item in queue_items:
            book = book_service.get_book(item['book_id'])
            if book:
                enriched_items.append({
                    **item,
                    'title': book.get('title'),
                    'author': book.get('author')
                })
            else:
                enriched_items.append({
                    **item,
                    'title': f"Book ID {item['book_id']}",
                    'author': None
                })

        return enriched_items
    except Exception as e:
        logger.error(f"Error getting priority queue: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
