"""Structured logging for OpenClaw."""

import logging
import sys

_configured = False


def get_logger(name: str = "openclaw") -> logging.Logger:
    """Get a configured logger instance."""
    global _configured
    logger = logging.getLogger(name)

    if not _configured:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("[%(asctime)s] %(levelname)-7s %(message)s", datefmt="%H:%M:%S")
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        _configured = True

    return logger


log = get_logger()
