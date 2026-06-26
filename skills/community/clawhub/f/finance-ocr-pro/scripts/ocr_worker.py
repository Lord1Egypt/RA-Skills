"""Detached worker entrypoint for disk-backed OCR jobs."""

from __future__ import annotations

import argparse
import logging
import os
import sys
import traceback
from pathlib import Path

from ocr_jobs import DiskProgressReporter, JobStore
from ocr_main import ocr_main
from ocr_runtime import CancellationRequested

logger = logging.getLogger(__name__)


def run_worker(job_dir: str | Path) -> int:
    store = JobStore(job_dir)
    manifest = store.load_manifest()
    params = manifest.get("params", {})
    source_file = manifest["input_path"]
    reporter = DiskProgressReporter(store)

    store.mark_started(pid=os.getpid())
    reporter.job_started()

    try:
        ocr_main(
            source_file,
            threads=int(params.get("threads", 1)),
            reporter=reporter,
            project_dir=store.job_dir,
            resume=True,
        )

        reporter.check_cancelled()

        store.mark_completed()
        return 0
    except CancellationRequested:
        store.mark_cancelled()
        return 0
    except SystemExit as exc:
        message = str(exc) or f"OCR worker exited with status {exc.code!r}."
        store.mark_failed(message)
        return exc.code if isinstance(exc.code, int) else 1
    except Exception as exc:
        traceback.print_exc()
        store.mark_failed(str(exc))
        return 1


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    parser = argparse.ArgumentParser(description="Run a detached OCR worker for one job.")
    parser.add_argument("--job-dir", required=True, help="Path to the OCR job directory.")
    args = parser.parse_args()

    sys.exit(run_worker(args.job_dir))


if __name__ == "__main__":
    main()
