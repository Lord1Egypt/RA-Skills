from __future__ import annotations

from pathlib import Path
from typing import Optional

from loguru import logger

from app.core.settings import Settings


def setup_logger(settings: Settings, log_name: Optional[str] = None) -> None:
    """
    初始化日志系统。
    """
    logger.remove()

    log_dir = Path(settings.get("paths", "log_dir"))
    log_dir.mkdir(parents=True, exist_ok=True)

    log_level = settings.get("logging", "level", default="INFO")
    rotation = settings.get("logging", "rotation", default="10 MB")
    retention = settings.get("logging", "retention", default="30 days")
    encoding = settings.get("logging", "encoding", default="utf-8")

    if not log_name:
        log_name = "workflow.log"

    log_file = log_dir / log_name

    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=log_level,
        colorize=True,
        enqueue=False,
    )

    logger.add(
        str(log_file),
        level=log_level,
        rotation=rotation,
        retention=retention,
        encoding=encoding,
        enqueue=False,
    )


def get_logger():
    return logger