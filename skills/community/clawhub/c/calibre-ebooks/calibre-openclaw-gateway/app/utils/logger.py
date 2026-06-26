import logging
import gzip
import shutil
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
import json

from app.config import settings


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add extra fields if present
        for name in (
            "request_id",
            "endpoint",
            "method",
            "query",
            "params",
            "ip",
            "duration",
            "duration_ms",
            "status_code",
            "bytes",
            "operation",
            "book_id",
            "queue_id",
            "format",
            "count",
            "current",
            "total",
        ):
            if hasattr(record, name):
                log_data[name] = getattr(record, name)
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


class ConsoleFormatter(logging.Formatter):
    """Readable terminal formatter with common structured fields appended."""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        base = (
            f"{timestamp} | {record.levelname:<7} | "
            f"{record.name}:{record.funcName}:{record.lineno} | {record.getMessage()}"
        )

        fields = []
        for name in (
            "request_id",
            "method",
            "endpoint",
            "query",
            "ip",
            "status_code",
            "duration_ms",
            "bytes",
            "operation",
            "book_id",
            "queue_id",
            "format",
            "count",
            "current",
            "total",
        ):
            if hasattr(record, name):
                value = getattr(record, name)
                if value is not None:
                    fields.append(f"{name}={value}")

        if fields:
            base = f"{base} | {' '.join(fields)}"

        if record.exc_info:
            base = f"{base}\n{self.formatException(record.exc_info)}"

        return base


def setup_logger(name: str = "calibre_openclaw") -> logging.Logger:
    """Setup application logging for file, terminal, and app.* loggers."""
    level_name = getattr(settings, "LOG_LEVEL", "INFO")
    level = getattr(logging, str(level_name).upper(), logging.INFO)
    
    # Create log directory if it doesn't exist
    log_dir = settings.log_dir_path
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Remove old log files and compress
    cleanup_old_logs(log_dir)
    
    # Create daily log file
    log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    
    # File handler with JSON formatter
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(JSONFormatter())
    
    # Console handler for terminal visibility
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(ConsoleFormatter())

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = True

    for logger_name in ("app", "uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        child = logging.getLogger(logger_name)
        child.handlers.clear()
        child.setLevel(level)
        child.propagate = True
    
    return logger


def cleanup_old_logs(log_dir: Path):
    """Compress and remove old log files based on retention policy."""
    cutoff_date = datetime.now() - timedelta(days=settings.LOG_RETENTION_DAYS)
    
    for log_file in log_dir.glob("*.log"):
        file_date = datetime.strptime(log_file.stem, "%Y-%m-%d")
        
        if file_date < cutoff_date:
            if settings.LOG_COMPRESS:
                # Compress the file
                compressed_file = log_dir / f"{log_file.stem}.log.gz"
                with open(log_file, 'rb') as f_in:
                    with gzip.open(compressed_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                log_file.unlink()
            else:
                # Just remove the file
                log_file.unlink()
    
    # Remove compressed files older than retention period
    for compressed_file in log_dir.glob("*.log.gz"):
        file_date = datetime.strptime(compressed_file.stem.split('.')[0], "%Y-%m-%d")
        if file_date < cutoff_date:
            compressed_file.unlink()


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get or create a logger instance."""
    if name is None:
        name = "calibre_openclaw"
    return logging.getLogger(name)
