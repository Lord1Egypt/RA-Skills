"""Fail-closed HTTP operation policy primitives."""

from __future__ import annotations

READ_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})
PROTECTED_WRITE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def classify_method(method: object) -> str:
    """Return the only permitted policy mode for an HTTP method."""
    if not isinstance(method, str):
        return "deny"
    normalized = method.upper()
    if normalized in READ_METHODS:
        return "read"
    if normalized in PROTECTED_WRITE_METHODS:
        return "protected-write"
    return "deny"


def is_protected_operation_allowed(
    operation_id: object, allowlist: object, known_operation_ids: set[str] | frozenset[str],
) -> bool:
    """Grant only an exact, unambiguous known protected-operation identifier.

    A comma-separated allowlist may name several known operations, but whitespace,
    wildcards, duplicates, blank entries, and every unknown name invalidate the
    entire value.  This makes malformed environment configuration fail closed.
    """
    if not isinstance(operation_id, str) or operation_id not in known_operation_ids:
        return False
    if not isinstance(allowlist, str) or not allowlist:
        return False
    entries = allowlist.split(",")
    if not entries or any(not entry or entry.strip() != entry or "*" in entry for entry in entries):
        return False
    if len(set(entries)) != len(entries) or any(entry not in known_operation_ids for entry in entries):
        return False
    return operation_id in entries
