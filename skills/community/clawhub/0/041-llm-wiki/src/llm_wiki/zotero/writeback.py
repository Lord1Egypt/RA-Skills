"""Authorized collection-level Zotero write-back planning and verification.

The executable manifest is deliberately narrower than Zotero's data model: it
can add llm-wiki managed tags and ensure explicitly reviewed reciprocal Related
pairs. Tag removal is possible only through a scoped opt-in: a plan must set
``policy.allow_managed_removals: true`` and list each tag under an item's
``reviewed_removals``, and even then only managed ``llm-wiki:`` tags other than
the protected status/preserved tags may be removed. It cannot change metadata
or collection membership, write notes, or touch Trash. Every apply run ends
with a fresh verification pass.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .local import LocalWriteError, LocalZoteroWriter
from .plan import MANAGED_TAG_PREFIX, PRESERVED_MANAGED_TAGS

_ITEM_KEY_RE = re.compile(r"^[A-Z0-9]{8}$")
_CREDENTIAL_FIELDS = {
    "api_key",
    "apikey",
    "authorization",
    "credential",
    "credentials",
    "password",
    "secret",
    "token",
}

# Managed tags that must never be removed through the scoped write-back path:
# the ingest status marker plus any explicitly preserved managed tags.
_NON_REMOVABLE_TAGS = (
    frozenset({f"{MANAGED_TAG_PREFIX}ingested"}) | PRESERVED_MANAGED_TAGS
)


class WritePlanError(ValueError):
    """Raised when an authorized write plan widens the safe mutation boundary."""


@dataclass(frozen=True)
class WritePolicy:
    preserve_existing_tags: bool = True
    replace_tags: bool = False
    write_notes: bool = False
    change_collections: bool = False
    change_metadata: bool = False
    relation_policy: str = "reviewed-only"
    # Opt-in escape hatch: when True, items may carry `reviewed_removals` to
    # delete specific managed tags. Deliberately excluded from the strict
    # default-equality policy check; guarded separately at plan load.
    allow_managed_removals: bool = False


@dataclass(frozen=True)
class WritePlanItem:
    item_key: str
    expected_collections: tuple[str, ...]
    desired_managed_tags: tuple[str, ...]
    reviewed_relations: tuple[str, ...]
    reviewed_removals: tuple[str, ...] = ()


@dataclass(frozen=True)
class WritePlan:
    library_id: str
    collection_key: str
    collection_name: str
    policy: WritePolicy
    items: tuple[WritePlanItem, ...]


@dataclass(frozen=True)
class WritebackItemReport:
    item_key: str
    status: str
    missing_tags: tuple[str, ...] = ()
    relation_gaps: tuple[str, ...] = ()
    present_removals: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class WritebackReport:
    phase: str
    library_id: str
    collection_key: str
    collection_name: str
    items: tuple[WritebackItemReport, ...]

    @property
    def updated_count(self) -> int:
        return sum(item.status == "updated_verified" for item in self.items)

    @property
    def skipped_count(self) -> int:
        return sum(item.status == "skipped_current" for item in self.items)

    @property
    def failed_count(self) -> int:
        return sum(item.status == "failed" for item in self.items)


def _load_data(path: Path) -> Mapping[str, Any]:
    source = Path(path)
    try:
        if source.suffix.lower() == ".json":
            data = json.loads(source.read_text(encoding="utf-8"))
        else:
            data = yaml.safe_load(source.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        raise WritePlanError("write plan is unreadable or invalid YAML/JSON") from exc
    if not isinstance(data, Mapping):
        raise WritePlanError("write plan root must be a mapping")
    return data


def _reject_credentials(value: Any, path: str = "root") -> None:
    if isinstance(value, Mapping):
        for raw_key, nested in value.items():
            key = str(raw_key).strip().casefold().replace("-", "_")
            if key in _CREDENTIAL_FIELDS:
                raise WritePlanError(
                    f"credential field is forbidden in write plans: {path}.{raw_key}"
                )
            _reject_credentials(nested, f"{path}.{raw_key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _reject_credentials(nested, f"{path}[{index}]")


def _reject_unknown_fields(
    value: Mapping[str, Any], allowed: set[str], path: str
) -> None:
    unknown = sorted(str(key) for key in value if str(key) not in allowed)
    if unknown:
        raise WritePlanError(f"{path} contains unknown fields: {unknown}")


def _string_list(raw: Any, *, field: str) -> tuple[str, ...]:
    if raw is None:
        return ()
    if isinstance(raw, str):
        values = [raw]
    elif isinstance(raw, list):
        values = raw
    else:
        raise WritePlanError(f"{field} must be a string or list")
    normalized = tuple(str(value).strip() for value in values if str(value).strip())
    if len(normalized) != len(set(normalized)):
        raise WritePlanError(f"{field} contains duplicates")
    return normalized


def _item_key(value: Any, *, field: str) -> str:
    key = str(value or "").strip().upper()
    if not _ITEM_KEY_RE.fullmatch(key):
        raise WritePlanError(f"{field} must be exactly 8 ASCII letters/digits")
    return key


def _validate_managed_tag(tag: str, *, field: str) -> None:
    if (
        not tag.startswith(MANAGED_TAG_PREFIX)
        or len(tag) <= len(MANAGED_TAG_PREFIX)
        or len(tag) > 255
        or any(ord(char) < 32 or ord(char) == 127 for char in tag)
    ):
        raise WritePlanError(f"{field} contains an invalid managed tag: {tag!r}")


def _validate_reviewed_removals(
    removals: tuple[str, ...],
    desired: tuple[str, ...],
    *,
    policy: WritePolicy,
    field: str,
) -> None:
    if not removals:
        return
    if not policy.allow_managed_removals:
        raise WritePlanError(
            f"{field} requires policy.allow_managed_removals: true (scoped removal opt-in)"
        )
    desired_set = set(desired)
    for tag in removals:
        _validate_managed_tag(tag, field=field)
        if tag in _NON_REMOVABLE_TAGS:
            raise WritePlanError(
                f"{field} cannot remove protected managed tag: {tag!r}"
            )
        if tag in desired_set:
            raise WritePlanError(
                f"{field} cannot both add and remove the same tag (conflict): {tag!r}"
            )


def load_write_plan(path: Path) -> WritePlan:
    """Load a reviewed, executable, secret-free write plan."""
    data = _load_data(path)
    _reject_credentials(data)
    _reject_unknown_fields(
        data,
        {"version", "mode", "library_id", "collection", "policy", "items"},
        "root",
    )
    if data.get("version") != 1:
        raise WritePlanError("write plan must declare version: 1")
    if data.get("mode") != "authorized-write":
        raise WritePlanError("write plan mode must be authorized-write")

    policy_raw = data.get("policy") or {}
    if not isinstance(policy_raw, Mapping):
        raise WritePlanError("policy must be a mapping")
    _reject_unknown_fields(
        policy_raw,
        {
            "preserve_existing_tags",
            "replace_tags",
            "write_notes",
            "change_collections",
            "change_metadata",
            "relation_policy",
            "allow_managed_removals",
        },
        "policy",
    )
    policy = WritePolicy(
        preserve_existing_tags=policy_raw.get("preserve_existing_tags") is True,
        replace_tags=policy_raw.get("replace_tags") is True,
        write_notes=policy_raw.get("write_notes") is True,
        change_collections=policy_raw.get("change_collections") is True,
        change_metadata=policy_raw.get("change_metadata") is True,
        relation_policy=str(policy_raw.get("relation_policy") or ""),
        allow_managed_removals=policy_raw.get("allow_managed_removals") is True,
    )
    expected_policy = WritePolicy()
    for field in (
        "preserve_existing_tags",
        "replace_tags",
        "write_notes",
        "change_collections",
        "change_metadata",
        "relation_policy",
    ):
        if getattr(policy, field) != getattr(expected_policy, field):
            raise WritePlanError(
                f"policy.{field} widens or changes the safe write boundary"
            )

    collection = data.get("collection") or {}
    if not isinstance(collection, Mapping):
        raise WritePlanError("collection must be a mapping")
    _reject_unknown_fields(collection, {"key", "name"}, "collection")
    collection_key = _item_key(collection.get("key"), field="collection.key")
    collection_name = str(collection.get("name") or "").strip()

    raw_items = data.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        raise WritePlanError("items must be a non-empty list")
    items: list[WritePlanItem] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_items):
        if not isinstance(raw, Mapping):
            raise WritePlanError(f"items[{index}] must be a mapping")
        _reject_unknown_fields(
            raw,
            {
                "item_key",
                "expected_collections",
                "desired_managed_tags",
                "reviewed_relations",
                "reviewed_removals",
            },
            f"items[{index}]",
        )
        key = _item_key(raw.get("item_key"), field=f"items[{index}].item_key")
        if key in seen:
            raise WritePlanError(f"duplicate item_key: {key}")
        seen.add(key)
        expected_collections = tuple(
            _item_key(value, field=f"items[{index}].expected_collections")
            for value in _string_list(
                raw.get("expected_collections"),
                field=f"items[{index}].expected_collections",
            )
        )
        if not expected_collections:
            raise WritePlanError(f"items[{index}] must declare expected_collections")
        tags = _string_list(
            raw.get("desired_managed_tags"),
            field=f"items[{index}].desired_managed_tags",
        )
        for tag in tags:
            _validate_managed_tag(tag, field=f"items[{index}].desired_managed_tags")
        removals = _string_list(
            raw.get("reviewed_removals"),
            field=f"items[{index}].reviewed_removals",
        )
        _validate_reviewed_removals(
            removals,
            tags,
            policy=policy,
            field=f"items[{index}].reviewed_removals",
        )
        relations = tuple(
            _item_key(value, field=f"items[{index}].reviewed_relations")
            for value in _string_list(
                raw.get("reviewed_relations"),
                field=f"items[{index}].reviewed_relations",
            )
        )
        if key in relations:
            raise WritePlanError(f"items[{index}] cannot relate an item to itself")
        items.append(
            WritePlanItem(key, expected_collections, tags, relations, removals)
        )

    known = {item.item_key for item in items}
    for item in items:
        unknown = set(item.reviewed_relations) - known
        if unknown:
            raise WritePlanError(
                f"reviewed relation targets must be present in the plan: {sorted(unknown)}"
            )

    library_id = str(data.get("library_id") or "").strip()
    if library_id and not library_id.isdigit():
        raise WritePlanError("library_id must be numeric when provided")
    if len(collection_name) > 255 or any(ord(char) < 32 for char in collection_name):
        raise WritePlanError("collection.name contains invalid characters")

    return WritePlan(
        library_id=library_id,
        collection_key=collection_key,
        collection_name=collection_name,
        policy=policy,
        items=tuple(items),
    )


def _relation_pairs(plan: WritePlan) -> tuple[tuple[str, str], ...]:
    pairs = {
        tuple(sorted((item.item_key, target)))
        for item in plan.items
        for target in item.reviewed_relations
    }
    return tuple(sorted(pairs))


def _tag_names(raw_tags: Any) -> set[str]:
    names: set[str] = set()
    for raw in raw_tags or []:
        value = raw.get("tag") if isinstance(raw, Mapping) else raw
        name = str(value or "").strip()
        if name:
            names.add(name)
    return names


def _identity_error(plan: WritePlan, item_plan: WritePlanItem, observed) -> str:
    collections = observed.data.get("collections")
    if not isinstance(collections, list):
        return "current collection membership was not observed"
    missing = sorted(
        set(item_plan.expected_collections) - {str(value) for value in collections}
    )
    if missing:
        return f"item is outside an expected collection: {missing}"
    if (
        plan.library_id
        and plan.library_id != "0"
        and observed.library_id != plan.library_id
    ):
        return "item belongs to a different Zotero library than the write plan"
    return ""


async def _observe(
    plan: WritePlan,
    writer: LocalZoteroWriter,
) -> tuple[dict[str, WritebackItemReport], dict[tuple[str, str], str]]:
    reports: dict[str, WritebackItemReport] = {}
    for item_plan in plan.items:
        try:
            observed = await writer.get_item(item_plan.item_key)
            identity_error = _identity_error(plan, item_plan, observed)
            if identity_error:
                reports[item_plan.item_key] = WritebackItemReport(
                    item_plan.item_key,
                    "failed",
                    errors=(identity_error,),
                )
                continue
            missing_tags = tuple(
                sorted(
                    set(item_plan.desired_managed_tags)
                    - _tag_names(observed.data.get("tags"))
                )
            )
            present_removals = tuple(
                sorted(
                    set(item_plan.reviewed_removals)
                    & _tag_names(observed.data.get("tags"))
                )
            )
            reports[item_plan.item_key] = WritebackItemReport(
                item_plan.item_key,
                "ready" if (missing_tags or present_removals) else "skipped_current",
                missing_tags=missing_tags,
                present_removals=present_removals,
            )
        except (LocalWriteError, KeyError, TypeError, ValueError) as exc:
            reports[item_plan.item_key] = WritebackItemReport(
                item_plan.item_key,
                "failed",
                errors=(str(exc),),
            )

    relation_errors: dict[tuple[str, str], str] = {}
    relation_gaps: dict[str, list[str]] = {item.item_key: [] for item in plan.items}
    for pair in _relation_pairs(plan):
        if any(reports[key].status == "failed" for key in pair):
            continue
        try:
            audit = await writer.audit_relation_pair(*pair)
            if not audit.source_has_target:
                relation_gaps[pair[0]].append(pair[1])
                relation_gaps[pair[1]].append(pair[0])
            if not audit.target_has_source and pair[1] not in relation_gaps[pair[0]]:
                relation_gaps[pair[0]].append(pair[1])
                relation_gaps[pair[1]].append(pair[0])
        except (LocalWriteError, KeyError, TypeError, ValueError) as exc:
            relation_errors[pair] = str(exc)
            for key in pair:
                current = reports[key]
                reports[key] = WritebackItemReport(
                    key,
                    "failed",
                    missing_tags=current.missing_tags,
                    present_removals=current.present_removals,
                    errors=current.errors + (str(exc),),
                )

    for key, gaps in relation_gaps.items():
        if not gaps or reports[key].status == "failed":
            continue
        current = reports[key]
        reports[key] = WritebackItemReport(
            key,
            "ready",
            missing_tags=current.missing_tags,
            relation_gaps=tuple(sorted(set(gaps))),
            present_removals=current.present_removals,
            errors=current.errors,
        )
    return reports, relation_errors


async def audit_write_plan(
    plan: WritePlan,
    writer: LocalZoteroWriter,
) -> WritebackReport:
    """Audit the live local-visible state without writing."""
    reports, _ = await _observe(plan, writer)
    return WritebackReport(
        phase="audit",
        library_id=plan.library_id,
        collection_key=plan.collection_key,
        collection_name=plan.collection_name,
        items=tuple(reports[item.item_key] for item in plan.items),
    )


async def verify_write_plan(
    plan: WritePlan,
    writer: LocalZoteroWriter,
) -> WritebackReport:
    """Re-read every item and require the complete authorized plan state."""
    reports, _ = await _observe(plan, writer)
    verified: list[WritebackItemReport] = []
    for item in plan.items:
        current = reports[item.item_key]
        if current.status == "failed":
            verified.append(current)
        elif current.missing_tags or current.relation_gaps or current.present_removals:
            errors: list[str] = []
            if current.missing_tags:
                errors.append(
                    f"managed tags missing after verification: {list(current.missing_tags)}"
                )
            if current.present_removals:
                errors.append(
                    f"reviewed removals still present after verification: {list(current.present_removals)}"
                )
            if current.relation_gaps:
                errors.append(
                    f"reviewed Related pairs incomplete: {list(current.relation_gaps)}"
                )
            verified.append(
                WritebackItemReport(
                    item.item_key,
                    "failed",
                    missing_tags=current.missing_tags,
                    relation_gaps=current.relation_gaps,
                    present_removals=current.present_removals,
                    errors=tuple(errors),
                )
            )
        else:
            verified.append(WritebackItemReport(item.item_key, "updated_verified"))
    return WritebackReport(
        phase="verify",
        library_id=plan.library_id,
        collection_key=plan.collection_key,
        collection_name=plan.collection_name,
        items=tuple(verified),
    )


async def apply_write_plan(
    plan: WritePlan,
    writer: LocalZoteroWriter,
) -> WritebackReport:
    """Apply missing managed tags/relations and cross the final verification barrier."""
    preflight, _ = await _observe(plan, writer)
    changed: set[str] = set()
    errors: dict[str, list[str]] = {
        item.item_key: list(preflight[item.item_key].errors)
        for item in plan.items
        if preflight[item.item_key].status == "failed"
    }

    for item_plan in plan.items:
        state = preflight[item_plan.item_key]
        if state.status == "failed" or not (
            state.missing_tags or state.present_removals
        ):
            continue
        try:
            result = await writer.write_safe_mutation(
                item_plan.item_key,
                add_tags=state.missing_tags,
                remove_tags=state.present_removals,
            )
            if result.status == "updated_verified":
                changed.add(item_plan.item_key)
        except (LocalWriteError, KeyError, TypeError, ValueError) as exc:
            errors.setdefault(item_plan.item_key, []).append(str(exc))

    for pair in _relation_pairs(plan):
        if any(key in errors for key in pair):
            continue
        if not any(
            target in preflight[key].relation_gaps for key, target in (pair, pair[::-1])
        ):
            continue
        try:
            result = await writer.ensure_relation_pair(*pair)
            changed.update(result.changed_items)
        except (LocalWriteError, KeyError, TypeError, ValueError) as exc:
            for key in pair:
                errors.setdefault(key, []).append(str(exc))

    verified = await verify_write_plan(plan, writer)
    final_items: list[WritebackItemReport] = []
    for item in verified.items:
        item_errors = tuple(errors.get(item.item_key, ())) + item.errors
        if item_errors:
            final_items.append(
                WritebackItemReport(
                    item.item_key,
                    "failed",
                    missing_tags=item.missing_tags,
                    relation_gaps=item.relation_gaps,
                    present_removals=item.present_removals,
                    errors=item_errors,
                )
            )
        elif item.status == "failed":
            final_items.append(item)
        else:
            final_items.append(
                WritebackItemReport(
                    item.item_key,
                    "updated_verified"
                    if item.item_key in changed
                    else "skipped_current",
                )
            )

    return WritebackReport(
        phase="apply",
        library_id=plan.library_id,
        collection_key=plan.collection_key,
        collection_name=plan.collection_name,
        items=tuple(final_items),
    )


def report_to_manifest(report: WritebackReport) -> dict[str, Any]:
    """Serialize a secret-free, machine-readable audit/apply/verify report."""
    items: list[dict[str, Any]] = []
    for item in report.items:
        row: dict[str, Any] = {
            "item_key": item.item_key,
            "status": item.status,
        }
        if item.missing_tags:
            row["missing_tags"] = list(item.missing_tags)
        if item.present_removals:
            row["present_removals"] = list(item.present_removals)
        if item.relation_gaps:
            row["relation_gaps"] = list(item.relation_gaps)
        if item.errors:
            row["errors"] = list(item.errors)
        items.append(row)
    return {
        "version": 1,
        "mode": "writeback-report",
        "phase": report.phase,
        "library_id": report.library_id,
        "collection": {
            "key": report.collection_key,
            "name": report.collection_name,
        },
        "summary": {
            "items": len(report.items),
            "updated_verified": report.updated_count,
            "skipped_current": report.skipped_count,
            "failed": report.failed_count,
        },
        "items": items,
    }
