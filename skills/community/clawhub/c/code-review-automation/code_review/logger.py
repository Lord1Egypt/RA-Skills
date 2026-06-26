"""Logging configuration for Code Review Automation."""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "code_review",
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up logger for code review automation.

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        format_string: Optional custom format string

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)

    # Clear existing handlers
    logger.handlers.clear()

    # Set log level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Default format string
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    formatter = logging.Formatter(format_string)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if log_file specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "code_review") -> logging.Logger:
    """
    Get existing logger or create new one.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class LoggerContext:
    """Context manager for temporary logging configuration."""

    def __init__(self, logger: logging.Logger, level: str):
        """
        Initialize logger context.

        Args:
            logger: Logger instance
            level: Temporary logging level
        """
        self.logger = logger
        self.level = level
        self.original_level = None

    def __enter__(self):
        """Enter context and set temporary log level."""
        self.original_level = self.logger.level
        self.logger.setLevel(getattr(logging, self.level.upper()))
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and restore original log level."""
        self.logger.setLevel(self.original_level)
        return False


def log_exception(logger: logging.Logger, exception: Exception, context: str = None):
    """
    Log exception with context.

    Args:
        logger: Logger instance
        exception: Exception to log
        context: Optional context information
    """
    message = f"Exception: {type(exception).__name__}: {str(exception)}"
    if context:
        message = f"{context} - {message}"
    logger.error(message, exc_info=True)


def log_api_call(logger: logging.Logger, method: str, url: str, status_code: int, duration: float):
    """
    Log API call details.

    Args:
        logger: Logger instance
        method: HTTP method (GET, POST, etc.)
        url: API URL
        status_code: HTTP status code
        duration: Request duration in seconds
    """
    logger.debug(f"API Call: {method} {url} - Status: {status_code} - Duration: {duration:.3f}s")


def log_analysis_start(logger: logging.Logger, repo: str, pr_number: int):
    """
    Log start of PR analysis.

    Args:
        logger: Logger instance
        repo: Repository name
        pr_number: Pull request number
    """
    logger.info(f"Starting analysis for {repo} PR #{pr_number}")


def log_analysis_complete(logger: logging.Logger, repo: str, pr_number: int, duration: float, issues_found: int):
    """
    Log completion of PR analysis.

    Args:
        logger: Logger instance
        repo: Repository name
        pr_number: Pull request number
        duration: Analysis duration in seconds
        issues_found: Number of issues found
    """
    logger.info(
        f"Analysis complete for {repo} PR #{pr_number} - "
        f"Duration: {duration:.2f}s - Issues: {issues_found}"
    )


def log_security_issue(logger: logging.Logger, severity: str, category: str, filename: str, line_number: int):
    """
    Log security issue.

    Args:
        logger: Logger instance
        severity: Issue severity (critical, high, medium, low)
        category: Issue category
        filename: File where issue was found
        line_number: Line number where issue was found
    """
    logger.warning(
        f"Security issue [{severity}] {category} in {filename}:{line_number}"
    )


def log_style_issue(logger: logging.Logger, severity: str, category: str, filename: str, line_number: int):
    """
    Log style issue.

    Args:
        logger: Logger instance
        severity: Issue severity (error, warning, info)
        category: Issue category
        filename: File where issue was found
        line_number: Line number where issue was found
    """
    logger.debug(
        f"Style issue [{severity}] {category} in {filename}:{line_number}"
    )
