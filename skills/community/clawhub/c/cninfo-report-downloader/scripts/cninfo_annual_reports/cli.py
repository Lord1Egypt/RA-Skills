from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .config import AppConfig
from .http_client import HttpClient
from .repository import StateRepository
from .service import AnnualReportService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download formal 2025 A-share annual and semiannual reports from CNInfo."
    )
    parser.add_argument("--year", type=int, default=2025, help="Target report year.")
    parser.add_argument(
        "--stock-csv",
        type=Path,
        default=Path("上市公司基础信息.csv"),
        help="CSV file whose first column contains stock codes.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("downloads") / "2025",
        help="Directory used to store downloaded PDFs.",
    )
    parser.add_argument(
        "--runtime-dir",
        type=Path,
        default=Path("runtime"),
        help="Directory used for SQLite state, manifest, and logs.",
    )
    parser.add_argument("--page-size", type=int, default=20, help="Search page size.")
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=1.2,
        help="Minimum delay between requests.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds.",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=5,
        help="Maximum HTTP retries per request.",
    )
    parser.add_argument(
        "--retry-backoff-seconds",
        type=float,
        default=1.5,
        help="Base backoff seconds used for retries.",
    )
    parser.add_argument(
        "--max-pages-per-keyword",
        type=int,
        default=None,
        help="Optional page cap per stock code for debugging.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Search and build the manifest without downloading files.",
    )
    parser.add_argument(
        "--force-redownload",
        action="store_true",
        help="Download again even if the target file already exists and was recorded.",
    )
    return parser


def configure_logging(log_path: Path) -> logging.Logger:
    logger = logging.getLogger("cninfo_annual_reports")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger


def configure_console_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except ValueError:
                pass


def build_config(args: argparse.Namespace) -> AppConfig:
    runtime_dir = args.runtime_dir
    year = args.year
    return AppConfig(
        year=year,
        stock_csv_path=args.stock_csv,
        page_size=args.page_size,
        sleep_seconds=args.sleep_seconds,
        timeout_seconds=args.timeout_seconds,
        max_retries=args.max_retries,
        retry_backoff_seconds=args.retry_backoff_seconds,
        output_dir=args.output_dir,
        runtime_dir=runtime_dir,
        database_path=runtime_dir / "state.db",
        manifest_path=runtime_dir / f"manifest_{year}.csv",
        log_path=runtime_dir / "logs" / f"cninfo_{year}.log",
        dry_run=args.dry_run,
        force_redownload=args.force_redownload,
        max_pages_per_keyword=args.max_pages_per_keyword,
    )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    configure_console_encoding()
    config = build_config(args)
    config.ensure_directories()

    logger = configure_logging(config.log_path)
    logger.info("Starting CNInfo annual report downloader")
    logger.info("Output directory: %s", config.output_dir)
    logger.info("Runtime database: %s", config.database_path)

    repository = StateRepository(config.database_path)
    client = HttpClient(config, logger)
    service = AnnualReportService(config, repository, client, logger)

    try:
        summary = service.run()
        logger.info("Finished successfully")
        logger.info("Pages fetched: %s", summary.pages_fetched)
        logger.info("Announcements seen: %s", summary.announcements_seen)
        logger.info("Eligible announcements: %s", summary.announcements_eligible)
        logger.info("Download candidates: %s", summary.download_candidates)
        logger.info("Downloaded this run: %s", summary.downloaded)
        logger.info("Skipped existing: %s", summary.skipped_existing)
        logger.info("Failed downloads: %s", summary.failed_downloads)
        return 0
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        return 130
    except Exception:  # noqa: BLE001
        logger.exception("Run failed")
        return 1
    finally:
        repository.close()
