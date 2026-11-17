"""Bounded parallel runner for early DOI recovery."""

from __future__ import annotations

import queue
import threading
from collections.abc import Callable
from typing import Any


def run_recovery_workers(entries: list[Any], workers: int, recover_one: Callable[[Any], None]) -> None:
    work: queue.Queue[Any] = queue.Queue()
    for entry in entries:
        work.put(entry)

    def worker() -> None:
        while True:
            try:
                entry = work.get_nowait()
            except queue.Empty:
                return
            try:
                recover_one(entry)
            finally:
                work.task_done()

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(min(max(1, workers), len(entries)))]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
