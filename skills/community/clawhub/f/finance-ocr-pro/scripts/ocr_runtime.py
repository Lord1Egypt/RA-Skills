"""Shared runtime helpers for the OCR pipeline and background jobs."""

from __future__ import annotations

from pathlib import Path


class CancellationRequested(RuntimeError):
    """Raised when a background OCR job has been asked to stop."""


class ProgressReporter:
    """Interface for reporting progress from the OCR pipeline."""

    def job_started(self) -> None:
        pass

    def step_started(self, step_id: str, label: str) -> None:
        pass

    def step_completed(self, step_id: str) -> None:
        pass

    def pages_discovered(self, total_pages: int) -> None:
        pass

    def page_done(self, page_num: int, total_pages: int, *, skipped: bool = False) -> None:
        pass

    def page_failed(self, page_num: int, total_pages: int, error: str) -> None:
        pass

    def artifact_ready(self, name: str, path: str | Path) -> None:
        pass

    def warning(self, message: str) -> None:
        pass

    def log(self, message: str) -> None:
        pass

    def is_cancelled(self) -> bool:
        return False

    def check_cancelled(self) -> None:
        if self.is_cancelled():
            raise CancellationRequested("Cancellation requested.")


class NullProgressReporter(ProgressReporter):
    """Default reporter that keeps the current synchronous scripts simple."""

