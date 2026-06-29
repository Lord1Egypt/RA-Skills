"""disk-sweeper: Progress display utilities.

Provides spinner and progress bar for scan/cleanup operations.
"""
import sys
import time
import threading
from typing import Optional, Callable


class Spinner:
    """Simple spinner for indeterminate operations."""
    def __init__(self, message: str = "Processing"):
        self.message = message
        self._running = False
        self._thread = None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def _spin(self):
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        i = 0
        while self._running:
            sys.stdout.write(f"\r{self.message} {chars[i % len(chars)]}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

    def stop(self, done_message: str = "Done"):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
        sys.stdout.write(f"\r{self.message} {done_message}    \n")
        sys.stdout.flush()


class ProgressBar:
    """Simple progress bar for determinate operations."""
    def __init__(self, total: int, prefix: str = ""):
        self.total = total
        self.prefix = prefix
        self.current = 0
        self.start_time = time.time()

    def update(self, n: int = 1):
        self.current += n
        self._draw()

    def set(self, n: int):
        self.current = n
        self._draw()

    def _draw(self):
        if self.total == 0:
            return
        percent = self.current / self.total
        bar_len = 30
        filled = int(bar_len * percent)
        bar = "█" * filled + "░" * (bar_len - filled)
        elapsed = time.time() - self.start_time
        sys.stdout.write(
            f"\r{self.prefix} |{bar}| {self.current}/{self.total} "
            f"({percent * 100:.1f}%) - {elapsed:.1f}s"
        )
        sys.stdout.flush()
        if self.current >= self.total:
            sys.stdout.write("\n")


def format_scan_progress(scanned: int, current_file: str) -> str:
    """Format a scan progress line."""
    return f"  📂 Scanned {scanned:,} files | {current_file[:50]}"


def make_progress_callback() -> Callable:
    """Create a callback that prints scan progress."""
    def callback(scanned: int, filepath: str):
        if scanned % 1000 == 0:
            print(format_scan_progress(scanned, filepath))
    return callback


if __name__ == "__main__":
    print("Progress utilities ready")

    # Test spinner
    sp = Spinner("Testing")
    sp.start()
    time.sleep(0.5)
    sp.stop("Test complete!")

    # Test progress bar
    bar = ProgressBar(100, "Testing")
    for i in range(100):
        time.sleep(0.01)
        bar.update()
    print("Progress modules working")
