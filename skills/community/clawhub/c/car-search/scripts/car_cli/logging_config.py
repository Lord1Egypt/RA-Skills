"""Central logging setup for car-cli (stderr, structured format)."""

from __future__ import annotations

import logging
import os
import sys

LOGGER_NAME = "car_cli"


def _env_truthy(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


def resolve_debug_flags(
    cli_debug: bool,
    cli_trace_http: bool,
) -> tuple[bool, bool]:
    """Merge CLI flags with environment (CAR_CLI_DEBUG, CAR_CLI_TRACE_HTTP)."""
    debug = cli_debug or _env_truthy("CAR_CLI_DEBUG")
    trace_http = cli_trace_http or _env_truthy("CAR_CLI_TRACE_HTTP")
    return debug, trace_http


def setup_logging(*, debug: bool, trace_http: bool = False) -> None:
    """Configure the ``car_cli`` logger.

    - When *debug* is False: only WARNING+ from ``car_cli`` (no extra noise).
    - When *debug* is True: DEBUG to stderr with timestamp and logger name.
    - When *trace_http* is True (implies useful httpx traces): set httpx/httpcore
      loggers to DEBUG (very verbose).
    """
    root = logging.getLogger(LOGGER_NAME)
    root.handlers.clear()
    root.propagate = False

    if not debug:
        root.setLevel(logging.WARNING)
        return

    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s %(levelname)-5s [%(name)s] %(message)s",
            datefmt="%H:%M:%S",
        )
    )
    root.addHandler(handler)

    if trace_http:
        for name in ("httpx", "httpcore"):
            lg = logging.getLogger(name)
            lg.handlers.clear()
            lg.setLevel(logging.DEBUG)
            lg.addHandler(handler)
            lg.propagate = False


def get_logger(suffix: str) -> logging.Logger:
    """Return a child logger, e.g. ``car_cli.http``."""
    return logging.getLogger(f"{LOGGER_NAME}.{suffix}")
