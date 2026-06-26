#!/usr/bin/env python3
"""Structured logging utilities for dreaming-optimizer."""
import logging
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

# Module-level log format
_LOG_FORMAT = "[%(asctime)s] [%(name)s] %(levelname)s: %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(
    name: str = "dreaming-optimizer",
    level: int = logging.INFO,
    log_file: Path = None,
) -> logging.Logger:
    """Get a configured logger instance.
    
    Args:
        name: Logger name (typically module name)
        level: Logging level (default: INFO)
        log_file: Optional file path to also write logs to
        
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(
        logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)
    )
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(
            logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)
        )
        logger.addHandler(file_handler)
    
    return logger


def log_pipeline_event(
    logger: logging.Logger,
    phase: str,
    action: str,
    count: int = None,
    details: dict = None,
) -> None:
    """Log a structured pipeline event.
    
    Args:
        logger: Logger instance
        phase: Pipeline phase (e.g., "score", "dedup", "commit")
        action: Action taken (e.g., "scored", "merged", "committed")
        count: Optional count for structured logging
        details: Optional additional details dict
    """
    msg = f"[{phase.upper()}] {action}"
    if count is not None:
        msg += f" (count={count})"
    if details:
        for k, v in details.items():
            msg += f" {k}={v}"
    logger.info(msg)


def log_error_with_context(
    logger: logging.Logger,
    error: Exception,
    context: dict,
) -> None:
    """Log an error with structured context.
    
    Args:
        logger: Logger instance
        error: Exception that was raised
        context: Dict of context variables
    """
    logger.error(
        f"Error: {error.__class__.__name__}: {error}",
        extra={"context": context}
    )


# Global default logger (lazy initialization)
_default_logger: Optional[logging.Logger] = None


def get_default_logger() -> logging.Logger:
    """Get the default logger for the module.
    
    Returns:
        logging.Logger: Default logger
    """
    global _default_logger
    if _default_logger is None:
        _default_logger = get_logger("dreaming-optimizer")
    return _default_logger


if __name__ == "__main__":
    log = get_logger("test")
    log.info("Test info message")
    log.warning("Test warning message")
    log_pipeline_event(log, "score", "scored", count=42, details={"threshold": 70})
