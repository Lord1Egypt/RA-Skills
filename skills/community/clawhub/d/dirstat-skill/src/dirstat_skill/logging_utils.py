from __future__ import annotations

import logging
from pathlib import Path


def configure_run_logger(log_path: Path) -> logging.Logger:
    logger = logging.getLogger("dirstat_skill")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("[%(levelname)s] | %(asctime)s | %(name)s | %(message)s")
    )
    logger.addHandler(handler)
    return logger

