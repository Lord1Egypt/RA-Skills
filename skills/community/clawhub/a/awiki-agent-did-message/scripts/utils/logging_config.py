"""Application logging utilities with daily file retention.

[INPUT]: SDKConfig (data_dir), logging records, local wall clock time
[OUTPUT]: DailyRetentionFileHandler, configure_logging(), cleanup_log_files(),
          get_log_dir(), get_log_file_path(), find_latest_log_file()
[POS]: Shared runtime logging module for CLI scripts and background listeners;
       stores diagnostic logs under <DATA_DIR>/logs with daily files and
       dual retention limits (15 days / 15 MiB total)

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updates
"""

from __future__ import annotations

import io
import logging
import sys
import threading
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Callable, TextIO

from utils.config import SDKConfig

LOG_FILE_PREFIX = "awiki-agent"
MAX_RETENTION_DAYS = 15
MAX_TOTAL_SIZE_BYTES = 15 * 1024 * 1024

_DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_FILE_HANDLER_NAME = "awiki_daily_file_handler"
_CONSOLE_HANDLER_NAME = "awiki_console_handler"
_STDIO_LOGGER_NAME = "awiki_stdio"

Clock = Callable[[], datetime]


def _default_clock() -> datetime:
    """Return the current local datetime with timezone information."""
    return datetime.now().astimezone()


def get_log_dir(config: SDKConfig | None = None) -> Path:
    """Return the application log directory under <DATA_DIR>/logs."""
    resolved_config = config or SDKConfig()
    log_dir = resolved_config.data_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def get_log_file_path(
    log_dir: Path | None = None,
    *,
    now: datetime | None = None,
    prefix: str = LOG_FILE_PREFIX,
) -> Path:
    """Return the daily log file path for the given date."""
    resolved_log_dir = log_dir or get_log_dir()
    current = now or _default_clock()
    return resolved_log_dir / f"{prefix}-{current.date().isoformat()}.log"


def _extract_log_date(path: Path, prefix: str) -> date | None:
    """Parse the managed log date from a file name."""
    expected_prefix = f"{prefix}-"
    if not path.is_file() or not path.name.startswith(expected_prefix):
        return None
    if path.suffix != ".log":
        return None

    date_part = path.name[len(expected_prefix):-4]
    try:
        return date.fromisoformat(date_part)
    except ValueError:
        return None


def _list_managed_log_files(
    log_dir: Path,
    *,
    prefix: str = LOG_FILE_PREFIX,
) -> list[Path]:
    """List managed daily log files sorted by date ascending."""
    files: list[tuple[date, Path]] = []
    for candidate in log_dir.glob(f"{prefix}-*.log"):
        parsed_date = _extract_log_date(candidate, prefix)
        if parsed_date is None:
            continue
        files.append((parsed_date, candidate))
    files.sort(key=lambda item: (item[0], item[1].name))
    return [path for _, path in files]


def find_latest_log_file(
    log_dir: Path | None = None,
    *,
    prefix: str = LOG_FILE_PREFIX,
) -> Path | None:
    """Return the latest managed daily log file, if any."""
    resolved_log_dir = log_dir or get_log_dir()
    files = _list_managed_log_files(resolved_log_dir, prefix=prefix)
    return files[-1] if files else None


def cleanup_log_files(
    log_dir: Path | None = None,
    *,
    now: datetime | None = None,
    prefix: str = LOG_FILE_PREFIX,
    max_retention_days: int = MAX_RETENTION_DAYS,
    max_total_size_bytes: int = MAX_TOTAL_SIZE_BYTES,
) -> list[Path]:
    """Delete expired or oversized daily logs.

    Cleanup strategy:
    1. Remove files older than the retention window.
    2. If the total managed log size still exceeds the limit, delete the
       oldest remaining files until the total size is within limit or only
       the newest log file remains.

    Returns:
        A list of deleted file paths.
    """
    resolved_log_dir = log_dir or get_log_dir()
    resolved_log_dir.mkdir(parents=True, exist_ok=True)
    current = now or _default_clock()

    deleted_files: list[Path] = []
    keep_after = current.date() - timedelta(days=max_retention_days - 1)

    kept_files: list[Path] = []
    for path in _list_managed_log_files(resolved_log_dir, prefix=prefix):
        file_date = _extract_log_date(path, prefix)
        if file_date is None:
            continue
        if file_date < keep_after:
            try:
                path.unlink()
                deleted_files.append(path)
            except FileNotFoundError:
                continue
        else:
            kept_files.append(path)

    sized_files: list[tuple[Path, int]] = []
    total_size = 0
    for path in kept_files:
        try:
            file_size = path.stat().st_size
        except FileNotFoundError:
            continue
        sized_files.append((path, file_size))
        total_size += file_size

    while total_size > max_total_size_bytes and len(sized_files) > 1:
        oldest_path, oldest_size = sized_files.pop(0)
        try:
            oldest_path.unlink()
            deleted_files.append(oldest_path)
        except FileNotFoundError:
            pass
        total_size -= oldest_size

    return deleted_files


class DailyRetentionFileHandler(logging.Handler):
    """Write logs to a single file per day and apply retention cleanup."""

    terminator = "\n"

    def __init__(
        self,
        *,
        log_dir: Path | None = None,
        prefix: str = LOG_FILE_PREFIX,
        max_retention_days: int = MAX_RETENTION_DAYS,
        max_total_size_bytes: int = MAX_TOTAL_SIZE_BYTES,
        cleanup_interval_seconds: int = 60,
        encoding: str = "utf-8",
        clock: Clock | None = None,
    ) -> None:
        super().__init__()
        self._log_dir = log_dir or get_log_dir()
        self._prefix = prefix
        self._max_retention_days = max_retention_days
        self._max_total_size_bytes = max_total_size_bytes
        self._cleanup_interval = timedelta(seconds=max(1, cleanup_interval_seconds))
        self._encoding = encoding
        self._clock = clock or _default_clock
        self._current_path: Path | None = None
        self._stream = None
        self._next_cleanup_at: datetime | None = None

        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._open_if_needed()
        self._run_cleanup(force=True)

    @property
    def current_path(self) -> Path:
        """Return the active daily log file path."""
        self._open_if_needed()
        assert self._current_path is not None
        return self._current_path

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a record to the active daily log file."""
        try:
            msg = self.format(record)
            self.acquire()
            try:
                self._open_if_needed()
                if self._stream is None:
                    return
                self._stream.write(msg + self.terminator)
                self.flush()
                self._run_cleanup()
            finally:
                self.release()
        except Exception:
            self.handleError(record)

    def flush(self) -> None:
        """Flush the active file stream."""
        if self._stream is not None:
            self._stream.flush()

    def close(self) -> None:
        """Close the active file stream."""
        self.acquire()
        try:
            if self._stream is not None:
                self._stream.close()
                self._stream = None
            self._current_path = None
            super().close()
        finally:
            self.release()

    def _open_if_needed(self) -> None:
        """Open or roll over the active daily file."""
        next_path = get_log_file_path(
            self._log_dir,
            now=self._clock(),
            prefix=self._prefix,
        )
        if next_path == self._current_path and self._stream is not None:
            return

        if self._stream is not None:
            self._stream.close()

        next_path.parent.mkdir(parents=True, exist_ok=True)
        self._stream = next_path.open("a", encoding=self._encoding)
        self._current_path = next_path

    def _run_cleanup(self, *, force: bool = False) -> None:
        """Run periodic retention cleanup."""
        current = self._clock()
        if not force and self._next_cleanup_at is not None and current < self._next_cleanup_at:
            return

        cleanup_log_files(
            self._log_dir,
            now=current,
            prefix=self._prefix,
            max_retention_days=self._max_retention_days,
            max_total_size_bytes=self._max_total_size_bytes,
        )
        self._next_cleanup_at = current + self._cleanup_interval


class _TeeToLogger(io.TextIOBase):
    """Mirror writes to the original stream and to a file-only logger."""

    def __init__(
        self,
        original_stream: TextIO,
        logger: logging.Logger,
        level: int,
    ) -> None:
        self._original_stream = original_stream
        self._logger = logger
        self._level = level
        self._buffer = ""
        self._is_writing_log = False

    @property
    def encoding(self) -> str:
        return getattr(self._original_stream, "encoding", "utf-8")

    @property
    def errors(self) -> str | None:
        return getattr(self._original_stream, "errors", None)

    @property
    def buffer(self):
        return getattr(self._original_stream, "buffer", None)

    def fileno(self) -> int:
        return self._original_stream.fileno()

    def isatty(self) -> bool:
        return self._original_stream.isatty()

    def writable(self) -> bool:
        return True

    def flush(self) -> None:
        self._flush_buffer()
        self._original_stream.flush()

    def write(self, s: str) -> int:
        written = self._original_stream.write(s)
        self._buffer += s
        self._flush_complete_lines()
        return written

    def _flush_complete_lines(self) -> None:
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            self._log_line(line)

    def _flush_buffer(self) -> None:
        if self._buffer:
            pending = self._buffer
            self._buffer = ""
            self._log_line(pending)

    def _log_line(self, line: str) -> None:
        text = line.rstrip()
        if not text or self._is_writing_log:
            return
        try:
            self._is_writing_log = True
            self._logger.log(self._level, "%s", text)
        finally:
            self._is_writing_log = False


def _find_named_handler(logger: logging.Logger, handler_name: str) -> logging.Handler | None:
    """Find a handler by name on the provided logger."""
    for handler in logger.handlers:
        if handler.get_name() == handler_name:
            return handler
    return None


def _remove_named_handler(logger: logging.Logger, handler_name: str) -> None:
    """Remove and close a named handler if present."""
    handler = _find_named_handler(logger, handler_name)
    if handler is None:
        return
    logger.removeHandler(handler)
    handler.close()


def _install_exception_hooks() -> None:
    """Install process-wide exception hooks once."""
    if getattr(_install_exception_hooks, "_installed", False):
        return

    def _log_unhandled_exception(
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback,
    ) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.getLogger(__name__).critical(
            "Unhandled exception",
            exc_info=(exc_type, exc_value, exc_traceback),
        )
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    def _log_unhandled_thread_exception(args: threading.ExceptHookArgs) -> None:
        if issubclass(args.exc_type, KeyboardInterrupt):
            return
        logging.getLogger(__name__).critical(
            "Unhandled thread exception",
            exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
        )

    sys.excepthook = _log_unhandled_exception
    if hasattr(threading, "excepthook"):
        threading.excepthook = _log_unhandled_thread_exception
    setattr(_install_exception_hooks, "_installed", True)


def _restore_stdio() -> None:
    """Restore the original process standard streams."""
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


def _configure_stdio_mirroring(file_handler: logging.Handler | None) -> None:
    """Mirror stdout/stderr writes into the managed log file."""
    if file_handler is None:
        _restore_stdio()
        return

    stdio_logger = logging.getLogger(_STDIO_LOGGER_NAME)
    stdio_logger.handlers.clear()
    stdio_logger.propagate = False
    stdio_logger.setLevel(logging.INFO)
    stdio_logger.addHandler(file_handler)

    if not isinstance(sys.stdout, _TeeToLogger):
        sys.stdout = _TeeToLogger(sys.__stdout__, stdio_logger, logging.INFO)
    if not isinstance(sys.stderr, _TeeToLogger):
        sys.stderr = _TeeToLogger(sys.__stderr__, stdio_logger, logging.ERROR)


def configure_logging(
    *,
    level: int = logging.INFO,
    console_level: int | None = logging.INFO,
    force: bool = False,
    config: SDKConfig | None = None,
    prefix: str = LOG_FILE_PREFIX,
    mirror_stdio: bool = False,
) -> Path:
    """Configure root logging with a daily file handler under <DATA_DIR>/logs.

    When ``mirror_stdio`` is True, stdout/stderr writes (including ``print``)
    are mirrored into the managed daily log file while still being emitted to
    the original terminal streams.
    """
    log_dir = get_log_dir(config)
    root_logger = logging.getLogger()

    if force:
        _remove_named_handler(root_logger, _FILE_HANDLER_NAME)
        _remove_named_handler(root_logger, _CONSOLE_HANDLER_NAME)

    file_handler = _find_named_handler(root_logger, _FILE_HANDLER_NAME)
    if file_handler is None:
        file_handler = DailyRetentionFileHandler(log_dir=log_dir, prefix=prefix)
        file_handler.set_name(_FILE_HANDLER_NAME)
        file_handler.setFormatter(
            logging.Formatter(_DEFAULT_FORMAT, datefmt=_DEFAULT_DATE_FORMAT)
        )
        root_logger.addHandler(file_handler)
    file_handler.setLevel(level)

    if console_level is None:
        _remove_named_handler(root_logger, _CONSOLE_HANDLER_NAME)
    else:
        console_handler = _find_named_handler(root_logger, _CONSOLE_HANDLER_NAME)
        if console_handler is None:
            console_handler = logging.StreamHandler(sys.__stderr__)
            console_handler.set_name(_CONSOLE_HANDLER_NAME)
            console_handler.setFormatter(
                logging.Formatter(_DEFAULT_FORMAT, datefmt=_DEFAULT_DATE_FORMAT)
            )
            root_logger.addHandler(console_handler)
        console_handler.setLevel(console_level)

    root_logger.setLevel(min(level, console_level) if console_level is not None else level)
    _configure_stdio_mirroring(file_handler if mirror_stdio else None)
    _install_exception_hooks()
    return get_log_file_path(log_dir, prefix=prefix)


__all__ = [
    "DailyRetentionFileHandler",
    "LOG_FILE_PREFIX",
    "MAX_RETENTION_DAYS",
    "MAX_TOTAL_SIZE_BYTES",
    "cleanup_log_files",
    "configure_logging",
    "find_latest_log_file",
    "get_log_dir",
    "get_log_file_path",
]
