"""User-facing scheduler errors."""

from __future__ import annotations


class SchedulerError(RuntimeError):
    """An expected error that should be shown without a traceback."""


class BackendError(SchedulerError):
    """A native scheduler backend operation failed."""

