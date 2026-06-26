# FILE_META
# INPUT:  adapter name (str) + pipeline options
# OUTPUT: registered adapter module or AdapterSpec
# POS:    skill lib — multi-agent dispatch layer, used by pipeline + CLI
# MISSION: Registry for agent-specific trajectory adapters (openclaw / hermes / claude-code / codex).

"""Adapter registry + shared IR types.

Each adapter is a package under ``lib/adapters/<name>/`` that exposes
at least ``discover`` and ``parse``. Optional: ``harness``, ``filters``.

See ``docs/adapter-design.md`` §4 for the contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterable


# ─── Shared IR types (docs/adapter-design.md §4.1 / §4.2) ──────────────

@dataclass
class SessionHandle:
    """Lightweight reference to a candidate session produced by discover()."""

    adapter: str
    session_id: str
    path: Path | None = None
    cwd: str | None = None
    model: str | None = None
    started_at: datetime | None = None
    size_bytes: int = 0
    extras: dict = field(default_factory=dict)


@dataclass
class Attachment:
    """One file to ship inside session_bundle.zip."""

    zip_path: str   # relative path inside the zip (e.g. "raw_session.jsonl")
    content: bytes
    is_core: bool = False  # True = core zone (server parses), False = extras/


@dataclass
class ParseResult:
    """Output of adapter.parse(): trajectory IR + companion data."""

    trajectory: dict
    prompt_hint: dict = field(default_factory=dict)
    attachments: list[Attachment] = field(default_factory=list)
    stats: dict = field(default_factory=dict)
    reject_reason: str | None = None


@dataclass
class ScopeInfo:
    """Describes one available harness scope (docs/adapter-design.md §6.2).

    ``display_name`` is shown in CLI pickers; keep it short and human-readable.
    """

    scope_type: str  # "user" | "project" | "agent"
    scope_id: str
    display_name: str = ""


# ─── Registry ──────────────────────────────────────────────────────────

@dataclass(frozen=True)
class AdapterSpec:
    """What a registered adapter provides.

    ``discover`` and ``parse`` are required. ``build_harness`` /
    ``list_scopes`` / ``default_filters`` are optional — absence means the
    adapter does not support that capability.
    """

    name: str
    discover: Callable[..., Iterable[Any]]
    parse: Callable[..., Any]
    build_harness: Callable[..., Any] | None = None
    list_scopes: Callable[..., list] | None = None
    default_filters: dict[str, Any] = field(default_factory=dict)


_REGISTRY: dict[str, AdapterSpec] = {}


def register(spec: AdapterSpec) -> None:
    if spec.name in _REGISTRY:
        raise ValueError(f"adapter already registered: {spec.name}")
    _REGISTRY[spec.name] = spec


def get(name: str) -> AdapterSpec:
    if name not in _REGISTRY:
        raise KeyError(
            f"unknown adapter: {name!r}. registered: {sorted(_REGISTRY)}"
        )
    return _REGISTRY[name]


def names() -> list[str]:
    return sorted(_REGISTRY)


def is_registered(name: str) -> bool:
    return name in _REGISTRY
