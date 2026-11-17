#!/usr/bin/env python3
"""Host capability probe for Agent Slim.

This module is intentionally small and side-effect-free.  It reports what the
current host can prove through local files; it never attempts a plugin,
usage, or session operation that is not implemented.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

ADAPTER_VERSION = "0.1"
CAPABILITY_NAMES = (
    "hot_warm_cold_inventory",
    "frontmatter_parse",
    "reference_graph",
    "token_usage_read",
    "skill_usage_index",
    "safe_move",
    "quarantine",
    "plugin_management",
    "plugin_disable",
    "session_archive",
    "regression_runner",
    "rollback",
)


class CapabilityUnavailable(Exception):
    """Raised when a caller asks for a capability the host cannot prove."""

    def __init__(self, capability: str, status: str, reason: str) -> None:
        super().__init__("{} is {}".format(capability, status))
        self.capability = capability
        self.status = status
        self.reason = reason


def _is_readable_file(path: Path) -> bool:
    try:
        return path.is_file() and os.access(path, os.R_OK)
    except OSError:
        return False


def _usage_index_path(home: Path) -> Optional[Path]:
    for path in (
        home / "skill-usage.json",
        home / "skills" / ".usage.json",
        home / "state" / "skill-usage.json",
    ):
        if _is_readable_file(path):
            return path
    return None


def _relative_evidence(home: Path, path: Path) -> str:
    try:
        return path.relative_to(home).as_posix()
    except ValueError:
        return path.name


def probe_codex_home(home: Path, home_source: str = "argument") -> Dict[str, Any]:
    """Return a side-effect-free capability report for a Codex Home.

    Status values follow the adapter contract: ``supported``, ``unsupported``
    or ``unknown``.  ``unknown`` means the relevant directory or evidence is
    absent, not that a destructive action should be attempted.
    """
    home = Path(home).expanduser().resolve()
    home_exists = home.is_dir()
    sessions_exists = (home / "sessions").is_dir()
    archived_exists = (home / "archived_sessions").is_dir()
    plugins_root = home / "plugins"
    plugin_cache_exists = (plugins_root / "cache").is_dir()
    config_exists = _is_readable_file(home / "config.toml")
    usage_index = _usage_index_path(home)
    token_tool = home / "scripts" / "token-usage.sh"
    token_tool_exists = _is_readable_file(token_tool)
    home_writable = home_exists and os.access(home, os.W_OK)

    capabilities: Dict[str, str] = {
        "hot_warm_cold_inventory": "supported" if home_exists else "unknown",
        # Parsers are implemented, but they can only prove something when a
        # readable home exists.  A missing home is reported as unknown rather
        # than as a supported operation.
        "frontmatter_parse": "supported" if home_exists else "unknown",
        "reference_graph": "supported" if home_exists else "unknown",
        "token_usage_read": "supported" if token_tool_exists else "unknown",
        "skill_usage_index": "supported" if usage_index is not None else "unknown",
        "safe_move": "supported" if home_writable else "unknown",
        "quarantine": "supported" if home_writable else "unknown",
        # Agent Slim deliberately does not implement plugin configuration
        # changes, even when plugin files are present.
        "plugin_management": "unsupported",
        "plugin_disable": "unsupported",
        "session_archive": "supported" if sessions_exists else "unknown",
        # The caller supplies a test command; there is no live router probe.
        "regression_runner": "unknown",
        "rollback": "supported",
    }

    evidence: Dict[str, Dict[str, Any]] = {}
    for name in CAPABILITY_NAMES:
        evidence[name] = {
            "status": capabilities[name],
            "method": "local metadata probe",
            "evidence": [],
        }
    if home_exists:
        evidence["hot_warm_cold_inventory"]["evidence"].append("home directory is readable")
    else:
        for name in ("hot_warm_cold_inventory", "frontmatter_parse", "reference_graph"):
            evidence[name]["reason"] = "home directory is missing; no parse or inventory evidence is available"
        evidence["safe_move"]["reason"] = "home directory is missing"
        evidence["quarantine"]["reason"] = "home directory is missing"
    if token_tool_exists:
        evidence["token_usage_read"]["evidence"].append(_relative_evidence(home, token_tool))
    else:
        evidence["token_usage_read"]["reason"] = "token-usage.sh was not found; no live usage facts are claimed"
    if usage_index is not None:
        evidence["skill_usage_index"]["evidence"].append(_relative_evidence(home, usage_index))
    else:
        evidence["skill_usage_index"]["reason"] = "no supported skill usage index was found"
    if sessions_exists:
        evidence["session_archive"]["evidence"].append("sessions/ exists")
    else:
        evidence["session_archive"]["reason"] = "sessions/ is absent; session archiving cannot be confirmed"
    if archived_exists:
        evidence["session_archive"]["evidence"].append("archived_sessions/ exists")
    evidence["plugin_management"]["reason"] = "Agent Slim does not implement plugin configuration changes"
    evidence["plugin_disable"]["reason"] = "plugin disable is outside the Agent Slim allowlist"
    if plugin_cache_exists or config_exists:
        evidence["plugin_management"]["evidence"].append("plugin metadata is present but management is not implemented")
    else:
        evidence["plugin_management"]["evidence"].append("plugin management evidence is absent")
    evidence["regression_runner"]["reason"] = "requires a caller-supplied test-prompts command; no live router was executed"
    if home_writable:
        evidence["safe_move"]["evidence"].append("home is writable")
        evidence["quarantine"]["evidence"].append("home is writable")
    else:
        evidence["safe_move"]["reason"] = "home is missing or not writable"
        evidence["quarantine"]["reason"] = "home is missing or not writable"

    return {
        "schemaVersion": "1.0",
        "kind": "agent-slim-host-capabilities",
        "host": "codex",
        "adapterVersion": ADAPTER_VERSION,
        "homeSource": home_source,
        "scope": {"pathMode": "host-relative", "contentRead": False},
        "detected": {
            "homeExists": home_exists,
            "sessionsRootExists": sessions_exists,
            "archivedSessionsRootExists": archived_exists,
            "pluginCacheExists": plugin_cache_exists,
            "pluginConfigExists": config_exists,
            "usageIndexExists": usage_index is not None,
            "tokenUsageToolExists": token_tool_exists,
        },
        "capabilities": capabilities,
        "evidence": evidence,
        "unsupported": [name for name, status in capabilities.items() if status == "unsupported"],
        "unknown": [name for name, status in capabilities.items() if status == "unknown"],
    }


def detect_home_kind(home: Path) -> str:
    """Classify a home directory by the layout markers it actually has.

    Detection only reads directory metadata; it never opens host content.
    ``unknown`` is returned instead of guessing so callers can report honestly.
    """
    home = Path(home).expanduser()
    if not home.is_dir():
        return "unknown"
    workbuddy_markers = (home / "workspace", home / "projects")
    codex_markers = (home / "config.toml", home / "sessions", home / "archived_sessions")
    has_workbuddy = any(marker.exists() for marker in workbuddy_markers)
    has_codex = any(marker.exists() for marker in codex_markers)
    if has_workbuddy and not has_codex:
        return "workbuddy"
    if has_codex and not has_workbuddy:
        return "codex"
    if has_workbuddy and has_codex:
        return "workbuddy"
    return "unknown"


def probe_workbuddy_home(home: Path, home_source: str = "argument") -> Dict[str, Any]:
    """Return a side-effect-free capability report for a WorkBuddy Home.

    WorkBuddy keeps sessions under ``workspace/sessions`` and has no
    ``scripts/token-usage.sh``; both facts are reported as evidence rather than
    being smoothed over.  Capability tri-state semantics are identical to the
    Codex probe.
    """
    home = Path(home).expanduser().resolve()
    home_exists = home.is_dir()
    sessions_root = home / "workspace" / "sessions"
    sessions_exists = sessions_root.is_dir()
    plugins_root = home / "plugins"
    plugin_cache_exists = (plugins_root / "cache").is_dir()
    config_exists = _is_readable_file(home / "workbuddy.db") or _is_readable_file(home / "config.toml")
    usage_index = _usage_index_path(home)
    token_tool = home / "scripts" / "token-usage.sh"
    token_tool_exists = _is_readable_file(token_tool)
    home_writable = home_exists and os.access(home, os.W_OK)

    capabilities: Dict[str, str] = {
        "hot_warm_cold_inventory": "supported" if home_exists else "unknown",
        "frontmatter_parse": "supported" if home_exists else "unknown",
        "reference_graph": "supported" if home_exists else "unknown",
        "token_usage_read": "supported" if token_tool_exists else "unknown",
        "skill_usage_index": "supported" if usage_index is not None else "unknown",
        "safe_move": "supported" if home_writable else "unknown",
        "quarantine": "supported" if home_writable else "unknown",
        "plugin_management": "unsupported",
        "plugin_disable": "unsupported",
        "session_archive": "supported" if sessions_exists else "unknown",
        "regression_runner": "unknown",
        "rollback": "supported",
    }

    evidence: Dict[str, Dict[str, Any]] = {}
    for name in CAPABILITY_NAMES:
        evidence[name] = {
            "status": capabilities[name],
            "method": "local metadata probe",
            "evidence": [],
        }
    if home_exists:
        evidence["hot_warm_cold_inventory"]["evidence"].append("home directory is readable")
    else:
        for name in ("hot_warm_cold_inventory", "frontmatter_parse", "reference_graph"):
            evidence[name]["reason"] = "home directory is missing; no parse or inventory evidence is available"
    if token_tool_exists:
        evidence["token_usage_read"]["evidence"].append(_relative_evidence(home, token_tool))
    else:
        evidence["token_usage_read"]["reason"] = "WorkBuddy ships no scripts/token-usage.sh; no live usage facts are claimed"
    if usage_index is not None:
        evidence["skill_usage_index"]["evidence"].append(_relative_evidence(home, usage_index))
    else:
        evidence["skill_usage_index"]["reason"] = "no supported skill usage index was found; low-frequency claims stay pending-confirmation"
    if sessions_exists:
        evidence["session_archive"]["evidence"].append("workspace/sessions/ exists")
    else:
        evidence["session_archive"]["reason"] = "workspace/sessions/ is absent; session archiving cannot be confirmed"
    evidence["plugin_management"]["reason"] = "Agent Slim does not implement plugin configuration changes"
    evidence["plugin_disable"]["reason"] = "plugin disable is outside the Agent Slim allowlist"
    if plugin_cache_exists or config_exists:
        evidence["plugin_management"]["evidence"].append("plugin metadata is present but management is not implemented")
    else:
        evidence["plugin_management"]["evidence"].append("plugin management evidence is absent")
    evidence["regression_runner"]["reason"] = "requires a caller-supplied test-prompts command; no live router was executed"
    if home_writable:
        evidence["safe_move"]["evidence"].append("home is writable")
        evidence["quarantine"]["evidence"].append("home is writable")
    else:
        evidence["safe_move"]["reason"] = "home is missing or not writable"
        evidence["quarantine"]["reason"] = "home is missing or not writable"

    return {
        "schemaVersion": "1.0",
        "kind": "agent-slim-host-capabilities",
        "host": "workbuddy",
        "adapterVersion": ADAPTER_VERSION,
        "homeSource": home_source,
        "scope": {"pathMode": "host-relative", "contentRead": False},
        "detected": {
            "homeExists": home_exists,
            "sessionsRootExists": sessions_exists,
            "sessionsRootLabel": "workspace/sessions",
            "archivedSessionsRootExists": False,
            "pluginCacheExists": plugin_cache_exists,
            "pluginConfigExists": config_exists,
            "usageIndexExists": usage_index is not None,
            "tokenUsageToolExists": token_tool_exists,
        },
        "capabilities": capabilities,
        "evidence": evidence,
        "unsupported": [name for name, status in capabilities.items() if status == "unsupported"],
        "unknown": [name for name, status in capabilities.items() if status == "unknown"],
    }


def probe_home(home: Path, home_source: str = "argument") -> Dict[str, Any]:
    """Dispatch to the host-specific probe using layout detection only."""
    kind = detect_home_kind(home)
    if kind == "workbuddy":
        return probe_workbuddy_home(home, home_source)
    return probe_codex_home(home, home_source)


def capability_status(report: Dict[str, Any], capability: str) -> str:
    return str(report.get("capabilities", {}).get(capability, "unknown"))


def require_capability(report: Dict[str, Any], capability: str) -> None:
    """Raise instead of pretending that an unavailable operation is safe."""
    status = capability_status(report, capability)
    if status != "supported":
        detail = report.get("evidence", {}).get(capability, {})
        reason = str(detail.get("reason") or "capability evidence is unavailable")
        raise CapabilityUnavailable(capability, status, reason)
