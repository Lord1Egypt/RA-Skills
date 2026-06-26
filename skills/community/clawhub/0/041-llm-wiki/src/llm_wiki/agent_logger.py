"""
Agent-visible logging infrastructure.

Provides structured, file:line-precise logging so Agents can trace
execution flow through CLI and library code. All log output goes to
stderr so stdout remains clean for structured markdown output.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

_AGENT_LOG_LEVEL = logging.DEBUG
_AGENT_LOG_FORMAT = (
    "[%(levelname)s] %(pathname)s:%(lineno)d %(funcName)s() | %(message)s"
)


class _AgentLogFilter(logging.Filter):
    """Filter that stamps log records with project-relative pathname for clarity."""

    def __init__(self, project_root: Optional[Path] = None):
        super().__init__()
        self.project_root = project_root

    def filter(self, record: logging.LogRecord) -> bool:
        if self.project_root and hasattr(record, "pathname"):
            try:
                rel = Path(record.pathname).relative_to(self.project_root)
                record.pathname = str(rel).replace("\\", "/")
            except ValueError:
                pass
        return True


def setup_agent_logging(project_root: Optional[Path] = None) -> None:
    """
    Configure root logger for agent-visible output.
    Safe to call multiple times; idempotent.
    """
    root = logging.getLogger("llm_wiki")
    if root.handlers:
        # Already configured
        return

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(_AGENT_LOG_LEVEL)
    handler.setFormatter(logging.Formatter(_AGENT_LOG_FORMAT))
    handler.addFilter(_AgentLogFilter(project_root))

    root.addHandler(handler)
    root.setLevel(_AGENT_LOG_LEVEL)


def get_logger(name: str) -> logging.Logger:
    """Get a logger under the 'llm_wiki' namespace."""
    return logging.getLogger(f"llm_wiki.{name}")
