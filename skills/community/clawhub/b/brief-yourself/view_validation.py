#!/usr/bin/env python3
"""Shared, Store-independent validation for frozen Brief Yourself Views.

This module is intentionally limited to invariants that apply at every View
entry point: envelope shape, lifecycle timestamps, item review state, unique
item IDs, exclusions, and permission shape.  Store-aware source-reference
checks and adapter-specific caller bindings remain in their owning modules.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any


SCHEMA_VERSION = "1.0.1"
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
AGENT_ENTITY_TYPE = "agent"
USER_STATUSES = {"confirmed", "corrected", "rejected", "unreviewed", "unresolved"}
ITEM_STATUSES = {"active", "challenged", "retired"}
SENSITIVITIES = {"public", "private", "restricted"}
VIEW_FIELDS = {
    "schema_version",
    "view_id",
    "subject",
    "principal",
    "audience",
    "purpose",
    "task",
    "source_revision",
    "created_at",
    "expires_at",
    "claims",
    "tensions",
    "relevant_unknowns",
    "exclusions",
    "permission",
}


def _error(errors: list[str], code: str, message: str) -> None:
    errors.append(f"{code}: {message}")


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_safe_id(value: Any) -> bool:
    return isinstance(value, str) and bool(SAFE_ID.fullmatch(value)) and ".." not in value


def _parse_datetime(value: Any, label: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        _error(errors, "invalid_datetime", f"{label} must be a non-empty ISO-8601 timestamp")
        return None
    normalized = value.strip()
    try:
        parsed = datetime.fromisoformat(normalized[:-1] + "+00:00" if normalized.endswith("Z") else normalized)
    except ValueError:
        _error(errors, "invalid_datetime", f"{label} must be a valid ISO-8601 timestamp")
        return None
    if parsed.tzinfo is None:
        _error(errors, "timezone_required", f"{label} must include a timezone")
        return None
    return parsed.astimezone(timezone.utc)


def _validate_entity(value: Any, label: str, errors: list[str]) -> tuple[str, str] | None:
    if not isinstance(value, dict) or set(value) != {"type", "id"}:
        _error(errors, "invalid_entity", f"{label} must contain exactly type and id")
        return None
    if value.get("type") != AGENT_ENTITY_TYPE:
        _error(errors, "invalid_entity_type", f"{label}.type must be 'agent'")
    if not _is_safe_id(value.get("id")):
        _error(errors, "invalid_id", f"{label}.id is not a safe identifier")
    if value.get("type") != AGENT_ENTITY_TYPE or not _is_safe_id(value.get("id")):
        return None
    return value["type"], value["id"]


def _validate_item(
    item: Any,
    label: str,
    *,
    include_unreviewed: bool,
    errors: list[str],
) -> tuple[str | None, str | None]:
    if not isinstance(item, dict):
        _error(errors, "invalid_item", f"{label} must be an object")
        return None, None
    item_id = item.get("id")
    if not _is_safe_id(item_id):
        _error(errors, "invalid_id", f"{label}.id is not a safe identifier")
        item_id = None
    sensitivity = item.get("sensitivity")
    if sensitivity not in SENSITIVITIES:
        _error(errors, "invalid_sensitivity", f"{label}.sensitivity is invalid")
        sensitivity = None
    status = item.get("status")
    if status not in ITEM_STATUSES:
        _error(errors, "invalid_status", f"{label}.status is invalid")
    elif status != "active":
        _error(errors, "inactive_item", f"{label}.status must be active for a View")
    user_status = item.get("user_status")
    if user_status not in USER_STATUSES:
        _error(errors, "invalid_user_status", f"{label}.user_status is invalid")
    elif user_status in {"rejected"}:
        _error(errors, "rejected_item", f"{label}.user_status rejected cannot be included in a View")
    elif user_status not in {"confirmed", "corrected"}:
        if not (include_unreviewed and user_status in {"unreviewed", "unresolved"}):
            _error(errors, "unreviewed_item", f"{label}.user_status requires explicit include-unreviewed")
    return item_id, sensitivity


def validate_view_core(
    view: Any,
    *,
    include_unreviewed: bool = False,
    now: datetime | None = None,
) -> list[str]:
    """Return safe errors for invariants shared by Store and Adapter Views."""

    errors: list[str] = []
    if not isinstance(view, dict):
        return ["invalid_view: input must be a JSON object"]

    unknown = set(view) - VIEW_FIELDS
    missing = VIEW_FIELDS - set(view)
    if unknown:
        _error(errors, "unknown_field", "view contains unsupported fields")
    if missing:
        _error(errors, "missing_field", "view is missing required fields")
    if view.get("schema_version") != SCHEMA_VERSION:
        _error(errors, "invalid_schema", "view.schema_version must be 1.0.1")
    if not _is_safe_id(view.get("view_id")):
        _error(errors, "invalid_id", "view.view_id is not a safe identifier")

    subject = view.get("subject")
    if not isinstance(subject, dict) or set(subject) != {"type", "id"} or subject.get("type") != "person" or not _is_safe_id(subject.get("id")):
        _error(errors, "invalid_subject", "view.subject must be a person entity with a safe id")

    principal = _validate_entity(view.get("principal"), "view.principal", errors)
    audience_value = view.get("audience")
    audience: list[tuple[str, str]] = []
    if not isinstance(audience_value, list) or not audience_value:
        _error(errors, "invalid_audience", "view.audience must be a non-empty list")
    else:
        seen_audience: set[tuple[str, str]] = set()
        for index, entity in enumerate(audience_value):
            parsed = _validate_entity(entity, f"view.audience[{index}]", errors)
            if parsed is None:
                continue
            if parsed in seen_audience:
                _error(errors, "duplicate_audience", "view.audience contains a duplicate entity")
            seen_audience.add(parsed)
            audience.append(parsed)
    if principal is not None and principal not in audience:
        _error(errors, "audience_principal_mismatch", "view.principal must be included in view.audience")

    for field in ("purpose", "task"):
        if not _is_nonempty_string(view.get(field)):
            _error(errors, f"invalid_{field}", f"view.{field} must be non-empty")
    revision = view.get("source_revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        _error(errors, "invalid_revision", "view.source_revision must be a positive integer")

    created_at = _parse_datetime(view.get("created_at"), "view.created_at", errors)
    expires_at = _parse_datetime(view.get("expires_at"), "view.expires_at", errors)
    if created_at is not None and expires_at is not None and expires_at <= created_at:
        _error(errors, "invalid_expiry", "view.expires_at must be after created_at")
    current = now or datetime.now(timezone.utc)
    current = current.replace(tzinfo=timezone.utc) if current.tzinfo is None else current.astimezone(timezone.utc)
    if expires_at is not None and expires_at <= current:
        _error(errors, "expired_view", "view has expired")

    item_records: list[tuple[str, str | None, str | None]] = []
    seen_ids: set[str] = set()
    for field in ("claims", "tensions", "relevant_unknowns"):
        values = view.get(field)
        if not isinstance(values, list):
            _error(errors, f"invalid_{field}", f"view.{field} must be a list")
            continue
        for index, item in enumerate(values):
            item_id, sensitivity = _validate_item(
                item,
                f"view.{field}[{index}]",
                include_unreviewed=include_unreviewed,
                errors=errors,
            )
            if item_id is not None:
                if item_id in seen_ids:
                    _error(errors, "duplicate_item_id", "View item IDs must be unique")
                seen_ids.add(item_id)
            item_records.append((f"{field}[{index}]", item_id, sensitivity))

    exclusions = view.get("exclusions")
    if not isinstance(exclusions, list) or any(not isinstance(item, str) for item in exclusions):
        _error(errors, "invalid_exclusions", "view.exclusions must be a list of strings")
        exclusions = []
    exclusion_tokens = {item.strip() for item in exclusions}
    for label, item_id, sensitivity in item_records:
        if item_id in exclusion_tokens or sensitivity in exclusion_tokens:
            _error(errors, "excluded_item_present", f"{label} is present despite View exclusions")

    permission = view.get("permission")
    if not isinstance(permission, dict) or set(permission) != {
        "allowed_use",
        "archive_in_personal_store",
        "allow_downstream_persistence",
    }:
        _error(errors, "invalid_permission", "view.permission must contain exactly the required fields")
    elif (
        not _is_nonempty_string(permission.get("allowed_use"))
        or not isinstance(permission.get("archive_in_personal_store"), bool)
        or not isinstance(permission.get("allow_downstream_persistence"), bool)
    ):
        _error(errors, "invalid_permission", "view.permission has invalid values")

    return errors
