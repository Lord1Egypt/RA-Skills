from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.models import DownloadQueueRequest, DownloadQueueResponse, DownloadQueueItem
from app.database.postgres_db import postgres_db
from app.services.download_service import download_service
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/downloads", tags=["downloads"])


@router.post("/queue")
async def add_to_download_queue(request: DownloadQueueRequest):
    """Add a book to the download queue.
    
    The book will be downloaded automatically if auto-processing is enabled and
    download is available. If download is not available, the book remains in the
    queue with status 'pending' and download_available=false, waiting for manual
    download or for the user to provide a download URL.
    
    This endpoint checks download availability before adding to the queue.
    """
    try:
        if not download_service.enabled:
            raise HTTPException(
                status_code=503,
                detail="Download queue is not enabled. Set DOWNLOAD_QUEUE_ENABLED=true in .env"
            )
        
        # Check if download is available
        download_available = download_service.check_download_available(
            ocaid=request.ocaid,
            download_url=request.download_url,
            preferred_format=request.preferred_format
        )
        
        # Add to database with download availability status
        queue_id = postgres_db.add_to_download_queue(
            title=request.title,
            author=request.author,
            source=request.source,
            source_id=request.source_id,
            olid=request.olid,
            ocaid=request.ocaid,
            download_url=request.download_url,
            preferred_format=request.preferred_format,
            priority=request.priority,
            download_available=download_available
        )
        
        logger.info(
            f"Added book to download queue: {request.title} (download_available: {download_available})",
            extra={"operation": "download_queue_add", "queue_id": queue_id, "title": request.title, "download_available": download_available}
        )
        
        # Construct LLM-friendly response
        if download_available:
            message = f"Book '{request.title}' added to download queue and will be downloaded automatically"
        else:
            message = f"Book '{request.title}' added to download queue. Automatic download is not available - you can download manually or provide a download URL"
        
        return {
            "success": True,
            "id": queue_id,
            "message": message,
            "download_available": download_available,
            "next_actions": [
                "The book is in the download queue" if download_available else "The book is in the queue but requires manual download",
                "Automatic download will process this book" if download_available else "Download the book manually and provide the file path",
                "You can check the queue status via GET /api/downloads/queue"
            ],
            "summary": f"Book '{request.title}' added to download queue. " + 
                     ("Automatic download is available." if download_available else 
                      "Automatic download is not available - manual download required.")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding to download queue: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/queue")
async def get_download_queue(
    status: Optional[str] = Query(default=None, description="Filter by status: pending, processing, completed, failed"),
    limit: int = Query(default=50, ge=1, le=100)
):
    """Get the download queue with LLM-friendly structured response.
    
    This endpoint is designed for LLM consumption to provide clear, structured
    information about the download queue status. The response includes:
    
    - Queue items with full details
    - Summary statistics (pending, processing, completed, failed, added_to_calibre)
    - Calibre integration status for each item
    - Timeline information
    
    This allows agents to construct natural language responses like:
    "You have 3 books pending download, 2 being processed, and 5 already completed.
    Of the completed downloads, 3 have been added to your Calibre library."
    """
    try:
        queue_items = postgres_db.get_download_queue(status=status, limit=limit)
        
        # Calculate statistics
        stats = {
            "total": len(queue_items),
            "pending": sum(1 for item in queue_items if item['status'] == 'pending'),
            "processing": sum(1 for item in queue_items if item['status'] == 'processing'),
            "completed": sum(1 for item in queue_items if item['status'] == 'completed'),
            "failed": sum(1 for item in queue_items if item['status'] == 'failed'),
            "added_to_calibre": sum(1 for item in queue_items if item.get('calibre_book_id') is not None)
        }
        
        # Enrich items with LLM-friendly structure
        enriched_items = []
        for item in queue_items:
            enriched_item = {
                "id": item['id'],
                "title": item['title'],
                "author": item.get('author'),
                "status": item['status'],
                "priority": item['priority'],
                "source": item['source'],
                "preferred_format": item.get('preferred_format'),
                "created_at": item['created_at'],
                "download_available": item.get('download_available', True),
                "calibre_integration": {
                    "is_added_to_calibre": item.get('calibre_book_id') is not None,
                    "calibre_book_id": item.get('calibre_book_id'),
                    "added_at": item.get('added_to_calibre_at')
                },
                "download_info": {
                    "file_path": item.get('file_path'),
                    "file_size": item.get('file_size'),
                    "file_hash": item.get('file_hash'),
                    "downloaded_at": item.get('completed_at'),
                    "error_message": item.get('error_message')
                } if item['status'] in ('completed', 'failed') else None,
                "source_info": {
                    "olid": item.get('olid'),
                    "ocaid": item.get('ocaid'),
                    "download_url": item.get('download_url')
                }
            }
            enriched_items.append(enriched_item)
        
        # Construct LLM-friendly response
        return {
            "success": True,
            "statistics": stats,
            "items": enriched_items,
            "summary": (
                f"Download queue contains {stats['total']} items: "
                f"{stats['pending']} pending, "
                f"{stats['processing']} processing, "
                f"{stats['completed']} completed, "
                f"{stats['failed']} failed. "
                f"Of the completed downloads, {stats['added_to_calibre']} "
                f"have been added to Calibre."
            ),
            "filter_applied": status or "none",
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error getting download queue: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/queue/{item_id}")
async def get_download_queue_item(item_id: int):
    """Get a specific download queue item."""
    try:
        item = postgres_db.get_download_queue_item(item_id)
        
        if not item:
            raise HTTPException(status_code=404, detail="Download queue item not found")
        
        return DownloadQueueItem(**item)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting download queue item {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/queue/{item_id}/priority")
async def update_download_queue_priority(item_id: int, priority: int = Query(..., ge=0, le=100)):
    """Update the priority of a download queue item.
    
    Higher priority items are downloaded first.
    """
    try:
        updated = postgres_db.update_download_queue_priority(item_id, priority)
        
        if not updated:
            raise HTTPException(status_code=404, detail="Download queue item not found")
        
        logger.info(
            f"Updated download queue item {item_id} priority to {priority}",
            extra={"operation": "download_queue_priority", "queue_id": item_id, "priority": priority}
        )
        
        return {"message": "Priority updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating download queue priority: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/queue/{item_id}/move")
async def move_download_queue_item(item_id: int, direction: str = Query(..., regex="^(up|down)$")):
    """Move a download queue item up or down in the queue.
    
    This swaps the priority with the adjacent item in the current order.
    Only works for pending items.
    """
    try:
        item = postgres_db.get_download_queue_item(item_id)
        
        if not item:
            raise HTTPException(status_code=404, detail="Download queue item not found")
        
        if item['status'] != 'pending':
            raise HTTPException(
                status_code=400,
                detail="Can only move pending items in the queue"
            )
        
        # Get all pending items in current order
        pending_items = postgres_db.get_download_queue(status='pending', limit=100)
        
        # Find current position
        current_index = next((i for i, x in enumerate(pending_items) if x['id'] == item_id), None)
        
        if current_index is None:
            raise HTTPException(status_code=404, detail="Item not found in pending queue")
        
        # Calculate target index
        if direction == 'up':
            if current_index == 0:
                raise HTTPException(status_code=400, detail="Cannot move first item up")
            target_index = current_index - 1
        else:  # down
            if current_index == len(pending_items) - 1:
                raise HTTPException(status_code=400, detail="Cannot move last item down")
            target_index = current_index + 1
        
        # Swap priorities
        current_item = pending_items[current_index]
        target_item = pending_items[target_index]
        
        # Swap priorities
        postgres_db.update_download_queue_priority(item_id, target_item['priority'])
        postgres_db.update_download_queue_priority(target_item['id'], current_item['priority'])
        
        logger.info(
            f"Moved download queue item {item_id} {direction} (swapped with item {target_item['id']})",
            extra={"operation": "download_queue_move", "queue_id": item_id, "direction": direction, "target_id": target_item['id']}
        )
        
        return {"message": f"Item moved {direction} successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error moving download queue item: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/queue/{item_id}")
async def delete_download_queue_item(item_id: int):
    """Delete a download queue item."""
    try:
        deleted = postgres_db.delete_download_queue_item(item_id)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Download queue item not found")
        
        logger.info(
            f"Deleted download queue item {item_id}",
            extra={"operation": "download_queue_delete", "queue_id": item_id}
        )
        
        return {"message": "Download queue item deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting download queue item: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/queue/{item_id}/retry")
async def retry_download(item_id: int):
    """Retry a failed download.
    
    Resets the status to pending so it will be processed again.
    """
    try:
        item = postgres_db.get_download_queue_item(item_id)
        
        if not item:
            raise HTTPException(status_code=404, detail="Download queue item not found")
        
        if item['status'] not in ('failed', 'completed'):
            raise HTTPException(
                status_code=400,
                detail="Can only retry failed or completed downloads"
            )
        
        updated = postgres_db.update_download_queue_status(
            item_id,
            'pending',
            error_message=None
        )
        
        if not updated:
            raise HTTPException(status_code=404, detail="Download queue item not found")
        
        logger.info(
            f"Retried download queue item {item_id}",
            extra={"operation": "download_queue_retry", "queue_id": item_id}
        )
        
        return {"message": "Download queued for retry"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrying download: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/queue/{item_id}/mark-added")
async def mark_added_to_calibre(item_id: int, calibre_book_id: int):
    """Mark a downloaded book as added to Calibre.
    
    This endpoint is designed for LLM consumption to provide clear, structured
    responses about the book's status in the download-to-Calibre workflow.
    
    The response includes:
    - Success/failure status
    - Book details (title, author, file path)
    - Calibre integration status
    - Timeline information (downloaded, added to Calibre)
    - Actionable next steps for the user
    
    This allows agents to construct natural language responses like:
    "The book 'The Hobbit' was successfully downloaded and has been added to
    your Calibre library. You can now access it via Calibre or search for it
    in the catalog."
    """
    try:
        item = postgres_db.get_download_queue_item(item_id)
        
        if not item:
            raise HTTPException(status_code=404, detail="Download queue item not found")
        
        if item['status'] != 'completed':
            raise HTTPException(
                status_code=400,
                detail="Can only mark completed downloads as added to Calibre"
            )
        
        updated = postgres_db.mark_added_to_calibre(item_id, calibre_book_id)
        
        if not updated:
            raise HTTPException(status_code=404, detail="Download queue item not found")
        
        logger.info(
            f"Marked download queue item {item_id} as added to Calibre (book_id: {calibre_book_id})",
            extra={"operation": "download_mark_added", "queue_id": item_id, "calibre_book_id": calibre_book_id}
        )
        
        # Construct LLM-friendly response with rich context
        return {
            "success": True,
            "message": "Book successfully marked as added to Calibre",
            "book": {
                "title": item.get('title'),
                "author": item.get('author'),
                "file_path": item.get('file_path'),
                "file_size": item.get('file_size'),
                "format": item.get('preferred_format'),
                "source": item.get('source'),
                "olid": item.get('olid'),
                "ocaid": item.get('ocaid')
            },
            "calibre_integration": {
                "calibre_book_id": calibre_book_id,
                "added_at": item.get('added_to_calibre_at'),
                "status": "integrated"
            },
            "timeline": {
                "downloaded_at": item.get('completed_at'),
                "added_to_calibre_at": item.get('added_to_calibre_at')
            },
            "next_actions": [
                "The book is now available in your Calibre library",
                f"You can access it via Calibre with ID: {calibre_book_id}",
                "The book file is located at: " + (item.get('file_path') or "unknown"),
                "You can now search for this book in the catalog"
            ],
            "summary": f"The book '{item.get('title')}' by {item.get('author') or 'unknown author'} "
                      f"has been successfully downloaded from {item.get('source')} and "
                      f"added to your Calibre library (ID: {calibre_book_id}). "
                      f"The file is available at {item.get('file_path')}."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking book as added to Calibre: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/queue/{item_id}/mark-manual-download")
async def mark_manual_download(item_id: int, file_path: str, file_size: Optional[int] = None):
    """Mark a book as manually downloaded.
    
    Use this endpoint when a book could not be downloaded automatically
    (download_available=false) but the user downloaded it manually.
    
    This allows the system to track the file and match it with Calibre later.
    """
    try:
        item = postgres_db.get_download_queue_item(item_id)
        
        if not item:
            raise HTTPException(status_code=404, detail="Download queue item not found")
        
        if item['status'] not in ('pending', 'failed'):
            raise HTTPException(
                status_code=400,
                detail="Can only mark pending or failed items as manually downloaded"
            )
        
        # Calculate file hash if possible
        from pathlib import Path
        file_hash = None
        try:
            file_path_obj = Path(file_path)
            if file_path_obj.exists():
                file_hash = download_service.calculate_file_hash(file_path_obj)
                if not file_size:
                    file_size = file_path_obj.stat().st_size
        except Exception as e:
            logger.warning(f"Could not calculate file hash for {file_path}: {e}")
        
        # Update status to completed
        updated = postgres_db.update_download_queue_status(
            item_id,
            'completed',
            file_path=file_path,
            file_size=file_size
        )
        
        if not updated:
            raise HTTPException(status_code=404, detail="Download queue item not found")
        
        # Update file hash separately
        if file_hash:
            postgres_db._update_download_queue_file_hash(item_id, file_hash)
        
        logger.info(
            f"Marked download queue item {item_id} as manually downloaded (file: {file_path})",
            extra={"operation": "download_mark_manual", "queue_id": item_id, "file_path": file_path, "file_hash": file_hash}
        )
        
        # Construct LLM-friendly response
        return {
            "success": True,
            "message": "Book marked as manually downloaded",
            "book": {
                "title": item.get('title'),
                "author": item.get('author'),
                "file_path": file_path,
                "file_size": file_size,
                "file_hash": file_hash,
                "format": item.get('preferred_format'),
                "source": item.get('source')
            },
            "next_actions": [
                "The book is now marked as downloaded",
                f"File location: {file_path}",
                "You can now add this book to Calibre and mark it as integrated",
                "Use POST /api/downloads/queue/{item_id}/mark-added with the Calibre book ID"
            ],
            "summary": f"The book '{item.get('title')}' has been marked as manually downloaded from {file_path}. " +
                     (f"File hash: {file_hash}. " if file_hash else "") +
                     "You can now add it to Calibre and mark it as integrated."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking manual download: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/match")
async def match_downloaded_file(file_hash: Optional[str] = None, file_path: Optional[str] = None):
    """Match a downloaded file with the download queue.
    
    This endpoint helps identify if a file has already been downloaded and
    tracked in the queue, allowing you to determine if it can be removed
    from the queue after being added to Calibre.
    
    Query parameters:
    - file_hash: SHA256 hash of the file (preferred method)
    - file_path: Path to the file (alternative method)
    
    Returns the matching download queue item if found.
    """
    try:
        if not file_hash and not file_path:
            raise HTTPException(
                status_code=400,
                detail="Either file_hash or file_path must be provided"
            )
        
        item = None
        if file_hash:
            item = postgres_db.find_download_queue_by_file_hash(file_hash)
        elif file_path:
            item = postgres_db.find_download_queue_by_file_path(file_path)
        
        if not item:
            return {
                "success": True,
                "found": False,
                "message": "No matching download queue item found",
                "summary": "This file is not tracked in the download queue."
            }
        
        # Construct LLM-friendly response
        return {
            "success": True,
            "found": True,
            "item": {
                "id": item['id'],
                "title": item['title'],
                "author": item.get('author'),
                "status": item['status'],
                "file_path": item.get('file_path'),
                "file_hash": item.get('file_hash'),
                "calibre_book_id": item.get('calibre_book_id'),
                "added_to_calibre_at": item.get('added_to_calibre_at')
            },
            "can_remove_from_queue": item.get('calibre_book_id') is not None,
            "next_actions": [
                f"File matches download queue item {item['id']}",
                f"Status: {item['status']}",
                "File is already in Calibre" if item.get('calibre_book_id') else "File is not yet in Calibre",
                "You can mark it as added to Calibre using POST /api/downloads/queue/{item['id']}/mark-added" if not item.get('calibre_book_id') else "File is already integrated with Calibre"
            ],
            "summary": f"This file matches download queue item {item['id']} ('{item['title']}'). " +
                     f"Status: {item['status']}. " +
                     ("It has been added to Calibre." if item.get('calibre_book_id') else "It has not been added to Calibre yet.")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error matching downloaded file: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
