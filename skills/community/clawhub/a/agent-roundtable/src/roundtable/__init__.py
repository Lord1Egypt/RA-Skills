"""Roundtable — independent multi-agent discussion library.

A framework-agnostic Python package for structured roundtable discussions
between AI agents. Works standalone or integrates with any agent framework
via adapters.

Usage::

    from roundtable import RoundtableDB, RoundtableCore

    db = RoundtableDB()
    core = RoundtableCore(db)
    disc = core.create_discussion(topic="...", participants=[...])

Adapter registration::

    from roundtable import register_adapter
    from roundtable.adapters.simple import SimpleAdapter

    register_adapter("simple", SimpleAdapter)
"""

from __future__ import annotations

from roundtable.adapters.base import RoundtableAdapter
from roundtable.adapters.generic import Roundtable
from roundtable.adapters.simple import SimpleAdapter
from roundtable.core import RoundtableCore
from roundtable.db import RoundtableDB
from roundtable.exceptions import (
    DiscussionNotActiveError,
    DiscussionNotFoundError,
    InvalidFindingTypeError,
    InvalidParticipantError,
    InvalidReplyToError,
    InvalidSpeechOrderError,
    RoundtableError,
)
from roundtable.models import (
    ConvergenceRecord,
    Discussion,
    Finding,
    Participant,
    Speech,
)
from roundtable.notify import Notifier
from roundtable.web_publisher import WebPublisher

__version__ = "0.2.0"

# ---------------------------------------------------------------------------
# Adapter registry
# ---------------------------------------------------------------------------

_ADAPTER_REGISTRY: dict[str, type[RoundtableAdapter]] = {}


def register_adapter(name: str, adapter_class: type[RoundtableAdapter]) -> None:
    """Register a custom adapter for use with ``--adapter name``.

    Args:
        name: Unique adapter name (lowercase, no spaces).
        adapter_class: A subclass of ``RoundtableAdapter``.

    Raises:
        TypeError: If adapter_class is not a RoundtableAdapter subclass.
        ValueError: If name is already registered.
    """
    if not (isinstance(adapter_class, type) and issubclass(adapter_class, RoundtableAdapter)):
        raise TypeError(f"{adapter_class!r} is not a RoundtableAdapter subclass")
    if name in _ADAPTER_REGISTRY:
        raise ValueError(f"Adapter '{name}' is already registered")
    _ADAPTER_REGISTRY[name] = adapter_class


def get_adapter(name: str) -> type[RoundtableAdapter] | None:
    """Look up a registered adapter by name. Returns None if not found."""
    return _ADAPTER_REGISTRY.get(name)


def list_adapters() -> dict[str, type[RoundtableAdapter]]:
    """Return a copy of the adapter registry."""
    return dict(_ADAPTER_REGISTRY)


__all__ = [
    "ConvergenceRecord",
    "Discussion",
    "DiscussionNotActiveError",
    "DiscussionNotFoundError",
    "Finding",
    "InvalidFindingTypeError",
    "InvalidParticipantError",
    "InvalidReplyToError",
    "InvalidSpeechOrderError",
    "Notifier",
    "Participant",
    "Roundtable",
    "RoundtableAdapter",
    "RoundtableCore",
    "RoundtableDB",
    "RoundtableError",
    "SimpleAdapter",
    "Speech",
    "WebPublisher",
    "get_adapter",
    "list_adapters",
    "register_adapter",
]
