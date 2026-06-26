"""Nightly embedding prefetch worker.

Processes queued embedding requests first. Optional prefetch mode can queue
unprocessed books so the library is gradually prepared.
"""

from pathlib import Path
from typing import Optional
import argparse
import signal
import time
from datetime import datetime, time as local_time

from app.config import settings
from app.database.postgres_db import postgres_db
from app.services.book_service import book_service
from app.services.conversion_service import conversion_service
from app.services.embedding_service import EmbeddingRunInterrupted, embedding_service
from app.utils.logger import get_logger, setup_logger

setup_logger(__name__)
logger = get_logger(__name__)
_stop_requested = False


def _request_stop(signum, _frame):
    global _stop_requested
    _stop_requested = True
    logger.warning("Received signal %s; stopping nightly embeddings at the next safe point", signum)


signal.signal(signal.SIGTERM, _request_stop)
signal.signal(signal.SIGINT, _request_stop)


def _pdf_path_for_book(book_id: int) -> tuple[Optional[Path], Optional[str]]:
    pdf_path = book_service.get_book_pdf_path(book_id)
    if not pdf_path:
        return None, "PDF path missing"

    if not pdf_path.exists():
        return None, f"PDF path not found: {pdf_path}"

    if pdf_path.stat().st_size == 0:
        return None, f"PDF file is empty: {pdf_path}"

    return pdf_path, None


def _ensure_random_book_queued() -> bool:
    book = postgres_db.get_random_book_without_embeddings()
    if not book:
        logger.info("No books without embeddings found")
        return False

    book_id = book["id"]
    existing = postgres_db.get_queue_status(book_id)
    if existing and existing["status"] in ("pending", "processing"):
        logger.info("Random book %s is already queued with status %s", book_id, existing["status"])
        return True

    queue_id = postgres_db.add_to_queue(book_id, priority=-1)
    logger.info("Queued random book %s for nightly embeddings as queue item %s", book_id, queue_id)
    return True


def _cleanup_interrupted_item(queue_id: int, book_id: int):
    deleted = postgres_db.delete_chunks_for_book(book_id)
    postgres_db.update_queue_status(
        queue_id,
        "pending",
        f"Interrupted; removed {deleted} partial chunk(s)",
    )
    logger.warning(
        "Interrupted while processing book %s. Removed %s partial chunk(s) and returned queue item %s to pending.",
        book_id,
        deleted,
        queue_id,
    )


def _parse_local_time(value: Optional[str]) -> Optional[local_time]:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("time must be in HH:MM format") from exc


def _deadline_reached(stop_at_local: Optional[local_time]) -> bool:
    if _stop_requested:
        return True
    if not stop_at_local:
        return False
    return datetime.now().time() >= stop_at_local


def process_nightly_embeddings(
    continuous: bool = False,
    idle_sleep_seconds: int = 60,
    stop_at_local: Optional[local_time] = None,
    prefetch_random_books: bool = False,
    reconcile_on_start: bool = False,
) -> int:
    """Process embedding work, optionally looping until interrupted."""
    processed_books = 0
    total_embeddings = 0
    total_pages = 0

    if reconcile_on_start:
        try:
            result = embedding_service.reconcile_embedding_version()
            logger.info("Embedding version reconciliation: %s", result)
        except Exception as exc:
            logger.error("Embedding version reconciliation failed: %s", exc)
    else:
        logger.info("Embedding version reconciliation skipped; enable RAG_RECONCILE_ON_START to run it")

    while True:
        if _deadline_reached(stop_at_local):
            logger.warning("Nightly embedding stop time reached; ending run before starting another item")
            break

        queue_items = postgres_db.get_pending_queue_items(limit=1)
        if not queue_items:
            if not continuous and processed_books > 0:
                break

            if not prefetch_random_books:
                if not continuous:
                    break
                logger.info(
                    "No pending queue items. Random prefetch is disabled; sleeping %s second(s).",
                    idle_sleep_seconds,
                )
                time.sleep(idle_sleep_seconds)
                continue

            if not _ensure_random_book_queued():
                if not continuous:
                    break
                logger.info(
                    "No pending queue items and no books without embeddings. Sleeping %s second(s).",
                    idle_sleep_seconds,
                )
                time.sleep(idle_sleep_seconds)
                continue

            queue_items = postgres_db.get_pending_queue_items(limit=1)
            if not queue_items:
                if continuous:
                    time.sleep(idle_sleep_seconds)
                    continue
                break

        item = queue_items[0]
        queue_id = item["id"]
        book_id = item["book_id"]
        title = item.get("title") or "Untitled"

        if postgres_db.has_embeddings(book_id):
            logger.info("Book %s already has embeddings; marking queue item %s completed", book_id, queue_id)
            postgres_db.update_queue_status(queue_id, "completed")
            continue

        pdf_path, pdf_error = _pdf_path_for_book(book_id)
        if not pdf_path:
            logger.warning("Book %s cannot be processed: %s", book_id, pdf_error)
            postgres_db.update_queue_status(queue_id, "failed", pdf_error)
            continue

        page_count = conversion_service.get_pdf_page_count(pdf_path)
        logger.info(
            "Processing book %s (%s), queue item %s, pages=%s, file=%s",
            book_id,
            title,
            queue_id,
            page_count,
            pdf_path,
        )

        try:
            chunk_count = embedding_service.process_queue_item(
                queue_id,
                book_id,
                pdf_path,
                should_stop=lambda: _deadline_reached(stop_at_local),
            )
            processed_books += 1
            total_embeddings += chunk_count
            total_pages += page_count

            embeddings_per_page = chunk_count / page_count if page_count else 0
            embeddings_per_book = total_embeddings / processed_books if processed_books else 0
            logger.info(
                "Completed book %s (%s): pages=%s, embeddings=%s, embeddings/page=%.2f, run_avg_embeddings/book=%.2f, run_total_embeddings=%s",
                book_id,
                title,
                page_count,
                chunk_count,
                embeddings_per_page,
                embeddings_per_book,
                total_embeddings,
            )
        except (KeyboardInterrupt, EmbeddingRunInterrupted):
            _cleanup_interrupted_item(queue_id, book_id)
            break
        except Exception as exc:
            logger.error(
                "Nightly embedding queue item %s for book %s failed; continuing: %s",
                queue_id,
                book_id,
                exc,
            )
            continue

    avg_embeddings_per_page = total_embeddings / total_pages if total_pages else 0
    avg_embeddings_per_book = total_embeddings / processed_books if processed_books else 0
    logger.info(
        "Embedding worker finished: books=%s, pages=%s, total_embeddings=%s, avg_embeddings/page=%.2f, avg_embeddings/book=%.2f",
        processed_books,
        total_pages,
        total_embeddings,
        avg_embeddings_per_page,
        avg_embeddings_per_book,
    )
    return processed_books


def main() -> int:
    parser = argparse.ArgumentParser(description="Process Calibre OpenClaw embedding queue.")
    parser.add_argument(
        "--continuous",
        action="store_true",
        help="Keep processing forever, adding random unprocessed books when the queue is empty.",
    )
    parser.add_argument(
        "--idle-sleep",
        type=int,
        default=settings.RAG_IDLE_SLEEP_SECONDS,
        help="Seconds to wait before checking again when continuous mode has no work.",
    )
    parser.add_argument(
        "--stop-at-local",
        type=_parse_local_time,
        default=_parse_local_time(settings.RAG_STOP_AT_LOCAL),
        help=(
            "Stop before starting more work after local HH:MM; current item is returned to pending if interrupted. "
            "Defaults to RAG_STOP_AT_LOCAL from the environment when set."
        ),
    )
    parser.add_argument(
        "--no-stop-at-local",
        action="store_true",
        help="Disable the local stop time. Intended for manual daytime runs.",
    )
    parser.add_argument(
        "--prefetch-random",
        action="store_true",
        default=settings.RAG_PREFETCH_RANDOM_BOOKS,
        help="Queue unprocessed books automatically when the explicit queue is empty.",
    )
    parser.add_argument(
        "--reconcile-embedding-version",
        action="store_true",
        default=settings.RAG_RECONCILE_ON_START,
        help="Reconcile embedding signature at startup and invalidate stale embeddings if needed.",
    )
    args = parser.parse_args()
    stop_at_local = None if args.no_stop_at_local else args.stop_at_local

    try:
        processed = process_nightly_embeddings(
            continuous=args.continuous,
            idle_sleep_seconds=args.idle_sleep,
            stop_at_local=stop_at_local,
            prefetch_random_books=args.prefetch_random,
            reconcile_on_start=args.reconcile_embedding_version,
        )
        print(f"Processed {processed} book(s)")
        return 0
    except KeyboardInterrupt:
        logger.info("Embedding worker interrupted by user")
        print("Interrupted")
        return 130
    finally:
        postgres_db.close_pool()


if __name__ == "__main__":
    raise SystemExit(main())
