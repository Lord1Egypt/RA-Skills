"""Background worker for processing download queue."""

import asyncio
import signal
import sys
from pathlib import Path

from app.config import settings
from app.database.postgres_db import postgres_db
from app.services.download_service import download_service
from app.utils.logger import setup_logger, get_logger

# Setup logger
setup_logger()
logger = get_logger(__name__)


class DownloadWorker:
    """Background worker for processing download queue."""
    
    def __init__(self):
        """Initialize download worker."""
        self.running = False
        self.stop_requested = False
        
    async def process_download(self, item: dict) -> bool:
        """Process a single download item.
        
        Args:
            item: Download queue item
            
        Returns:
            True if successful, False otherwise
        """
        item_id = item['id']
        title = item['title']
        
        try:
            # Skip if download is not available
            if not item.get('download_available', True):
                logger.info(
                    f"Skipping download (not available): {title}",
                    extra={"operation": "download_skip", "queue_id": item_id, "title": title}
                )
                # Keep status as pending - book stays in queue for manual download
                return False
            
            logger.info(
                f"Processing download: {title}",
                extra={"operation": "download_process", "queue_id": item_id, "title": title}
            )
            
            # Update status to processing
            postgres_db.update_download_queue_status(item_id, 'processing')
            
            # Perform download
            result = download_service.download_book(
                title=item['title'],
                author=item.get('author'),
                ocaid=item.get('ocaid'),
                download_url=item.get('download_url'),
                preferred_format=item.get('preferred_format', 'PDF')
            )
            
            if result['success']:
                # Update status to completed with file hash
                postgres_db.update_download_queue_status(
                    item_id,
                    'completed',
                    file_path=result.get('file_path'),
                    file_size=result.get('file_size')
                )
                
                # Update file hash separately
                if result.get('file_hash'):
                    postgres_db._update_download_queue_file_hash(item_id, result['file_hash'])
                
                logger.info(
                    f"Download completed: {title}",
                    extra={
                        "operation": "download_complete",
                        "queue_id": item_id,
                        "title": title,
                        "file_path": result.get('file_path'),
                        "file_size": result.get('file_size'),
                        "file_hash": result.get('file_hash')
                    }
                )
                return True
            else:
                # Update status to failed
                error_msg = result.get('error', 'Unknown error')
                postgres_db.update_download_queue_status(
                    item_id,
                    'failed',
                    error_message=error_msg
                )
                logger.error(
                    f"Download failed: {title} - {error_msg}",
                    extra={
                        "operation": "download_failed",
                        "queue_id": item_id,
                        "title": title,
                        "error": error_msg
                    }
                )
                return False
                
        except Exception as e:
            # Update status to failed
            postgres_db.update_download_queue_status(
                item_id,
                'failed',
                error_message=str(e)
            )
            logger.error(
                f"Error processing download {item_id}: {e}",
                extra={"operation": "download_error", "queue_id": item_id, "error": str(e)},
                exc_info=True
            )
            return False
    
    async def run(self):
        """Main worker loop."""
        logger.info("Download worker starting")
        
        # Initialize database connection
        postgres_db.initialize_pool()
        
        self.running = True
        
        while self.running and not self.stop_requested:
            try:
                # Check if download queue is enabled
                if not settings.DOWNLOAD_QUEUE_ENABLED or not settings.DOWNLOAD_AUTO_PROCESS:
                    logger.debug("Download queue or auto-processing disabled, sleeping")
                    await asyncio.sleep(settings.DOWNLOAD_IDLE_SLEEP_SECONDS)
                    continue
                
                # Get next pending download
                item = postgres_db.get_next_pending_download()
                
                if item:
                    logger.info(
                        f"Found pending download: {item['title']}",
                        extra={"operation": "download_found", "queue_id": item['id'], "title": item['title']}
                    )
                    
                    # Process the download
                    await self.process_download(item)
                else:
                    # No pending downloads, sleep
                    logger.debug("No pending downloads, sleeping")
                    await asyncio.sleep(settings.DOWNLOAD_IDLE_SLEEP_SECONDS)
                    
            except asyncio.CancelledError:
                logger.info("Download worker cancelled")
                break
            except Exception as e:
                logger.error(f"Error in download worker loop: {e}", exc_info=True)
                await asyncio.sleep(settings.DOWNLOAD_IDLE_SLEEP_SECONDS)
        
        self.running = False
        logger.info("Download worker stopped")
    
    def stop(self):
        """Request worker to stop."""
        logger.info("Download worker stop requested")
        self.stop_requested = True


async def main():
    """Main entry point."""
    worker = DownloadWorker()
    
    # Setup signal handlers
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}, stopping worker...")
        worker.stop()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run worker
    try:
        await worker.run()
    except Exception as e:
        logger.error(f"Download worker error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
