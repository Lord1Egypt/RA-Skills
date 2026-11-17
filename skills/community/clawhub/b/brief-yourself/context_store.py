#!/usr/bin/env python3
"""Manage Brief Yourself Personal Context Stores (stdlib only).

Brief Yourself 1.0.1 is the canonical Store format.  V0.2 and V0.3 are deliberately kept on
the read-only side of this module: validate/inspect may inspect them, while
export and mutation commands fail closed.  ``migrate-v02`` is the one
historical exception and only creates a V0.3 Store.  V0.3 to 1.0.1 is a
metadata-only preview until a future, separately approved materialisation
command exists.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Union

try:
    from view_validation import validate_view_core
except ModuleNotFoundError:  # pragma: no cover - supports direct file loading in tests
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from view_validation import validate_view_core

V04_SCHEMA_VERSION = "1.0.1"
V03_SCHEMA_VERSION = "0.3"
V02_SCHEMA_VERSION = "0.2"
SCHEMA_VERSION = V04_SCHEMA_VERSION
LEGACY_SCHEMA_VERSION = V02_SCHEMA_VERSION
SUPPORTED_SCHEMA_VERSIONS = {V02_SCHEMA_VERSION, V03_SCHEMA_VERSION, V04_SCHEMA_VERSION}
READ_ONLY_SCHEMA_VERSIONS = {V02_SCHEMA_VERSION, V03_SCHEMA_VERSION}
DEFAULT_VIEW_TTL_DAYS = 7
MAX_INPUT_BYTES = 4 * 1024 * 1024
MAX_PURGE_DEPTH = 64
AGENT_ENTITY_TYPE = "agent"
KINDS = {"fact", "self_report", "observation", "inference"}
SCOPES = {"cross-context", "domain", "situation"}
DURABILITIES = {"stable", "evolving", "situational"}
CONFIDENCES = {"high", "medium", "low"}
USER_STATUSES = {"confirmed", "corrected", "rejected", "unreviewed", "unresolved"}
CLAIM_STATUSES = {"active", "challenged", "retired"}
SENSITIVITIES = {"public", "private", "restricted"}
PATCH_ACTIONS_V04 = {"add", "update", "challenge", "retire"}
PATCH_ACTIONS_V03 = PATCH_ACTIONS_V04 | {"promote", "demote"}
PATCH_DECISIONS = {"pending", "confirmed", "corrected", "rejected", "unresolved"}
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
DATE_OR_DATETIME = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}(?:T[^\s]+)?$")
V04_TOP_LEVEL = {
    "schema_version", "context_id", "subject", "policy", "coverage", "claims",
    "tensions", "unknowns", "sources", "revision",
}
V04_CLAIM_FIELDS = {
    "id", "statement", "domains", "kind", "scope", "durability", "confidence",
    "user_status", "status", "sensitivity", "disclosure", "evidence_refs",
    "counterevidence_refs", "observed_at", "valid_from", "last_confirmed_at",
    "review_after", "expires_at", "supersedes", "notes",
}
V04_TENSION_FIELDS = {
    "id", "domains", "statement_a", "statement_b", "interpretation", "user_status",
    "status", "sensitivity", "disclosure", "evidence_refs",
}
V04_UNKNOWN_FIELDS = {
    "id", "domains", "question", "reason", "priority", "revisit", "user_status",
    "status", "sensitivity", "disclosure", "evidence_refs",
}
V04_VIEW_FIELDS = {
    "schema_version", "view_id", "subject", "principal", "audience", "purpose",
    "task", "source_revision", "created_at", "expires_at", "claims", "tensions",
    "relevant_unknowns", "exclusions", "permission",
}
V04_PATCH_FIELDS = {
    "schema_version", "patch_id", "subject", "principal", "purpose", "source_task",
    "source_revision", "created_at", "status", "proposals", "task_strategies_not_for_merge",
}
V04_PROPOSAL_FIELDS = {
    "action", "target_claim_id", "candidate_claim", "evidence_refs", "reason", "user_decision",
}
DEFAULT_DISCLOSURE = {
    "audiences": ["self-agent"],
    "purposes": ["user-approved"],
    "allow_downstream_persistence": False,
}
PURGE_KINDS = {"claim", "source", "view", "patch"}


class StoreError(RuntimeError):
    """Expected CLI validation or policy failure."""


class ResourceLimitError(StoreError):
    """A bounded-input or bounded-recursion failure.

    Resource failures use the same exit status as invalid external input so a
    caller cannot mistake a refused oversized/deep document for a successful
    operation.
    """


REPARSE_POINT_ATTRIBUTE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x0400)


_MISSING_FILE = object()
_ACTIVE_WRITE_EXPECTED_STATES: Optional[Dict[Path, Optional[Tuple[str, int, int, int, int]]]] = None
_ACTIVE_STORE_ROOT: Optional[Path] = None


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def format_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso_utc(value: Any, label: str, *, allow_none: bool = False) -> Optional[datetime]:
    if value is None and allow_none:
        return None
    if not isinstance(value, str) or not value.strip():
        raise StoreError(f"{label} must be a non-empty ISO-8601 timestamp")
    normalized = value.strip()
    try:
        parsed = datetime.fromisoformat(normalized[:-1] + "+00:00" if normalized.endswith("Z") else normalized)
    except ValueError as exc:
        raise StoreError(f"{label} must be a valid ISO-8601 timestamp: {value!r}") from exc
    if parsed.tzinfo is None:
        raise StoreError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def validate_date_or_datetime(value: Any, label: str, *, allow_none: bool = True) -> List[str]:
    if value is None and allow_none:
        return []
    if not isinstance(value, str) or not value.strip() or not DATE_OR_DATETIME.fullmatch(value.strip()):
        return [f"{label} must be a date, date-time, or null"]
    if "T" in value:
        try:
            parse_iso_utc(value, label)
        except StoreError as exc:
            return [str(exc)]
    else:
        try:
            datetime.fromisoformat(value)
        except ValueError:
            return [f"{label} must be a valid date"]
    return []


def claim_time_value(value: str, label: str) -> datetime:
    """Parse a Claim temporal bound for View-time comparisons."""

    if "T" in value:
        parsed = parse_iso_utc(value, label)
    else:
        try:
            parsed = datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
        except ValueError as exc:
            raise StoreError(f"{label} must be a valid date") from exc
    if parsed is None:  # defensive for type checkers; allow_none is not used
        raise StoreError(f"{label} must be a temporal value")
    return parsed


def claim_temporal_errors(claim: Dict[str, Any], label: str, *, now: Optional[datetime] = None) -> List[str]:
    """Reject future-valid or expired Claims at View creation/validation time."""

    errors: List[str] = []
    current = now.astimezone(timezone.utc) if now is not None else datetime.now(timezone.utc)
    valid_from = claim.get("valid_from")
    expires_at = claim.get("expires_at")
    try:
        if isinstance(valid_from, str) and claim_time_value(valid_from, f"{label}.valid_from") > current:
            errors.append(f"{label} is not yet valid (valid_from is in the future)")
    except StoreError as exc:
        errors.append(str(exc))
    try:
        if isinstance(expires_at, str) and claim_time_value(expires_at, f"{label}.expires_at") <= current:
            errors.append(f"{label} has expired (expires_at is not in the future)")
    except StoreError as exc:
        errors.append(str(exc))
    return errors


def _read_limited_bytes(path: Path, *, label: Optional[str] = None) -> bytes:
    """Read one input file without allowing an unbounded allocation.

    The size check is performed both before and during the read so a file
    growing between ``stat`` and ``read`` cannot bypass the limit.
    """

    display = label or str(path)
    try:
        if not path.is_file():
            raise StoreError(f"Input is not a regular file: {display}")
        if path.stat().st_size > MAX_INPUT_BYTES:
            raise ResourceLimitError(f"Input exceeds the {MAX_INPUT_BYTES}-byte limit: {display}")
        with path.open("rb") as handle:
            raw = handle.read(MAX_INPUT_BYTES + 1)
    except ResourceLimitError:
        raise
    except FileNotFoundError as exc:
        raise StoreError(f"Missing file: {display}") from exc
    except OSError as exc:
        raise StoreError(f"Cannot read input {display}: {exc}") from exc
    if len(raw) > MAX_INPUT_BYTES:
        raise ResourceLimitError(f"Input exceeds the {MAX_INPUT_BYTES}-byte limit: {display}")
    return raw


def read_json(path: Path) -> Dict[str, Any]:
    try:
        raw = _read_limited_bytes(path, label=f"JSON input {path}")
        data = json.loads(raw.decode("utf-8"))
    except ResourceLimitError:
        raise
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise StoreError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise StoreError(f"Expected a JSON object in {path}")
    return data


def _is_link_or_reparse(path: Path) -> bool:
    """Return whether a path is a symlink or Windows reparse point."""

    try:
        info = os.lstat(path)
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise StoreError(f"Cannot inspect controlled Store path {path}: {exc}") from exc
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE_POINT_ATTRIBUTE)


def _assert_no_link_ancestry(path: Path, *, label: str) -> None:
    """Reject a link/reparse point anywhere in a raw path's ancestry."""

    current = Path(os.path.abspath(str(path)))
    while True:
        if current.exists() or current.is_symlink():
            if _is_link_or_reparse(current):
                raise StoreError(f"{label} contains a symlink or reparse point: {current}")
        parent = current.parent
        if parent == current:
            break
        current = parent


def store_path_from_arg(value: Any) -> Path:
    """Validate a user-supplied Store path before resolving aliases."""

    if not isinstance(value, (str, os.PathLike)):
        raise StoreError("Store path must be a filesystem path")
    lexical = Path(os.path.abspath(str(Path(value).expanduser())))
    _assert_no_link_ancestry(lexical, label="Store root/parent path")
    try:
        return lexical.resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        raise StoreError(f"Cannot resolve Store path: {lexical}") from exc


def _assert_output_path_safe(output: Path) -> None:
    """Reject output aliases that could overwrite a link or hard-linked file."""

    lexical = Path(os.path.abspath(str(output)))
    _assert_no_link_ancestry(lexical.parent, label="output parent path")
    if lexical.exists() or lexical.is_symlink():
        if _is_link_or_reparse(lexical):
            raise StoreError(f"output path must not be a symlink or reparse point: {output}")
        try:
            if int(os.lstat(lexical).st_nlink) > 1:
                raise StoreError(f"output path must not be a hard-link alias: {output}")
        except FileNotFoundError:
            pass
        except OSError as exc:
            raise StoreError(f"Cannot inspect output path: {output}") from exc
def _assert_store_path_safe(store: Path, path: Path, *, label: str = "controlled Store path") -> None:
    """Reject link/reparse ancestry and aliases outside the Store.

    This check intentionally walks the lexical ancestry before resolving the
    candidate.  It is called again immediately before every controlled write
    or delete, so a newly inserted link is not silently followed.
    """

    try:
        # Keep a lexical root for the no-follow ancestry walk.  On Windows a
        # caller may supply an 8.3 short path while ``resolve`` returns the
        # long spelling; mixing those representations causes false escapes.
        store_lexical = Path(os.path.abspath(str(store)))
        store_root = store_lexical.resolve(strict=False)
        candidate = Path(os.path.abspath(str(path)))
        candidate.relative_to(store_lexical)
    except (OSError, RuntimeError, ValueError) as exc:
        raise StoreError(f"{label} is outside the Store: {path}") from exc

    ancestry: List[Path] = []
    current = candidate
    while True:
        ancestry.append(current)
        if current == store_lexical:
            break
        parent = current.parent
        if parent == current:
            raise StoreError(f"{label} has invalid Store ancestry: {path}")
        current = parent
    for entry in reversed(ancestry):
        if entry.exists() or entry.is_symlink():
            if _is_link_or_reparse(entry):
                raise StoreError(f"{label} contains a symlink or reparse point: {entry}")
    try:
        resolved = candidate.resolve(strict=False)
        resolved.relative_to(store_root)
    except (OSError, RuntimeError, ValueError) as exc:
        raise StoreError(f"{label} resolves outside the Store: {path}") from exc


def _assert_store_tree_safe(store: Path) -> None:
    """Fail closed if any controlled Store directory or file is linked."""

    _assert_store_path_safe(store, store, label="Store root")
    if not store.exists():
        return
    try:
        for root, directories, files in os.walk(store, topdown=True, followlinks=False):
            root_path = Path(root)
            _assert_store_path_safe(store, root_path)
            for name in [*directories, *files]:
                _assert_store_path_safe(store, root_path / name)
    except OSError as exc:
        raise StoreError(f"Cannot inspect Store tree: {exc}") from exc


def json_bytes(data: Any) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def jsonl_bytes(records: Iterable[Any]) -> bytes:
    return b"".join(
        (json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
        for record in records
    )


def append_jsonl_bytes(existing: bytes, data: Dict[str, Any]) -> bytes:
    separator = b"" if not existing or existing.endswith(b"\n") else b"\n"
    return existing + separator + (json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def _file_state(path: Path) -> Optional[Tuple[str, int, int, int, int]]:
    """Return content plus filesystem identity for commit-time CAS checks."""

    try:
        stat = path.stat()
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise StoreError(f"Cannot stat transaction target {path}: {exc}") from exc
    if not path.is_file():
        raise StoreError(f"Transaction target is not a regular file: {path}")
    try:
        content = _read_limited_bytes(path, label=f"transaction target {path}")
    except ResourceLimitError:
        raise
    except StoreError as exc:
        raise StoreError(f"Cannot read transaction target {path}: {exc}") from exc
    return (
        hashlib.sha256(content).hexdigest(),
        int(getattr(stat, "st_dev", 0)),
        int(getattr(stat, "st_ino", 0)),
        int(getattr(stat, "st_mtime_ns", int(stat.st_mtime * 1_000_000_000))),
        int(stat.st_size),
    )


def _atomic_write_bytes(path: Path, data: bytes, *, store_root: Optional[Path] = None) -> None:
    if store_root is None:
        store_root = _ACTIVE_STORE_ROOT
    if store_root is not None:
        _assert_store_path_safe(store_root, path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if store_root is not None:
        _assert_store_path_safe(store_root, path)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        expected_states = _ACTIVE_WRITE_EXPECTED_STATES
        if expected_states is not None and path in expected_states and _file_state(path) != expected_states[path]:
            raise StoreError(f"Controlled Store changed before replacing {path}")
        if store_root is not None:
            _assert_store_path_safe(store_root, path)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def atomic_write_bytes(path: Path, data: bytes, *, store_root: Optional[Path] = None) -> None:
    """Write exact bytes atomically; kept separate for transaction fault injection."""

    _atomic_write_bytes(path, data, store_root=store_root)


def atomic_write_json(path: Path, data: Dict[str, Any], *, store_root: Optional[Path] = None) -> None:
    atomic_write_bytes(path, json_bytes(data), store_root=store_root)


def atomic_write_jsonl(path: Path, records: List[Any]) -> None:
    atomic_write_bytes(path, jsonl_bytes(records))


def append_jsonl(path: Path, data: Dict[str, Any]) -> None:
    existing = _read_limited_bytes(path, label=f"JSONL input {path}") if path.exists() else b""
    atomic_write_bytes(path, append_jsonl_bytes(existing, data))


def transactional_commit(
    changes: Sequence[Tuple[Path, Optional[bytes]]],
    *,
    store_root: Optional[Path] = None,
    manifest_root: Optional[Path] = None,
    expected_manifest: Optional[Sequence[Dict[str, str]]] = None,
) -> None:
    """Commit a set of file replacements/deletions with byte-for-byte rollback.

    All target bytes are prepared before this function is called.  If any
    commit step fails, every target is restored to its original bytes (or
    absence).  Rollback uses the private writer so a test/fault injection on
    ``atomic_write_bytes`` cannot mask whether recovery itself succeeded.
    """

    global _ACTIVE_STORE_ROOT, _ACTIVE_WRITE_EXPECTED_STATES
    prepared: Dict[Path, Optional[bytes]] = {}
    for path, data in changes:
        prepared[path] = data

    guarded_states: Optional[Dict[str, Optional[Tuple[str, int, int, int, int]]]] = None
    if (manifest_root is None) != (expected_manifest is None):
        raise StoreError("manifest_root and expected_manifest must be supplied together")
    if manifest_root is not None:
        if store_root is not None and store_root.resolve(strict=False) != manifest_root.resolve(strict=False):
            raise StoreError("store_root and manifest_root must identify the same Store")
        store_root = manifest_root
    if store_root is not None:
        _assert_store_tree_safe(store_root)
        for path in prepared:
            _assert_store_path_safe(store_root, path)
    if manifest_root is not None and expected_manifest is not None:
        verify_controlled_manifest(manifest_root, expected_manifest)
        expected_paths = [manifest_root / entry["path"] for entry in expected_manifest]
        guarded_paths = expected_paths + list(prepared)
        guarded_states = controlled_store_state_map(manifest_root, guarded_paths)
        verify_controlled_state_map(manifest_root, guarded_states)

    originals: Dict[Path, Union[object, bytes]] = {}
    for path in prepared:
        if store_root is not None:
            _assert_store_path_safe(store_root, path)
        try:
            originals[path] = _read_limited_bytes(path, label=f"transaction target {path}") if path.exists() else _MISSING_FILE
        except ResourceLimitError:
            raise
        except (OSError, StoreError) as exc:
            raise StoreError(f"Cannot snapshot transaction target {path}: {exc}") from exc
    if manifest_root is not None and guarded_states is not None:
        verify_controlled_state_map(manifest_root, guarded_states)

    previous_expected_states = _ACTIVE_WRITE_EXPECTED_STATES
    previous_store_root = _ACTIVE_STORE_ROOT
    active_write_states: Optional[Dict[Path, Optional[Tuple[str, int, int, int, int]]]] = None
    if manifest_root is not None and guarded_states is not None:
        active_write_states = {
            manifest_root / relative: state for relative, state in guarded_states.items()
        }
        for path in prepared:
            active_write_states.setdefault(path, _file_state(path))
    _ACTIVE_WRITE_EXPECTED_STATES = active_write_states
    _ACTIVE_STORE_ROOT = store_root
    applied_posts: Dict[Path, Optional[Tuple[str, int, int, int, int]]] = {}
    try:
        for path, data in prepared.items():
            if store_root is not None:
                _assert_store_path_safe(store_root, path)
            if manifest_root is not None and guarded_states is not None:
                verify_controlled_state_map(manifest_root, guarded_states)
            if data is None:
                expected_state = _file_state(path)
                if active_write_states is not None and path in active_write_states and expected_state != active_write_states[path]:
                    raise StoreError(f"Controlled Store changed before deleting {path}")
                if path.exists() or path.is_symlink():
                    path.unlink()
                applied_posts[path] = None
                if active_write_states is not None:
                    active_write_states[path] = None
                if manifest_root is not None and guarded_states is not None:
                    guarded_states[path.relative_to(manifest_root).as_posix()] = None
            else:
                if store_root is not None:
                    _assert_store_path_safe(store_root, path)
                atomic_write_bytes(path, data)
                applied_posts[path] = _file_state(path)
                if active_write_states is not None:
                    active_write_states[path] = applied_posts[path]
                if manifest_root is not None and guarded_states is not None:
                    guarded_states[path.relative_to(manifest_root).as_posix()] = applied_posts[path]
    except BaseException as exc:
        rollback_errors: List[str] = []
        for path, original in reversed(list(originals.items())):
            if path not in applied_posts:
                continue
            try:
                if store_root is not None:
                    _assert_store_path_safe(store_root, path)
                # Never restore over a file that changed after our own write;
                # that is a concurrent mutation, not transaction state.
                if _file_state(path) != applied_posts[path]:
                    continue
                if original is _MISSING_FILE:
                    if path.exists() or path.is_symlink():
                        path.unlink()
                else:
                    _atomic_write_bytes(path, original)  # type: ignore[arg-type]
            except BaseException as rollback_exc:
                rollback_errors.append(f"{path}: {rollback_exc}")
        detail = f"transaction failed and was rolled back: {exc}"
        if rollback_errors:
            detail += "; rollback errors: " + "; ".join(rollback_errors)
        raise StoreError(detail) from exc
    finally:
        _ACTIVE_WRITE_EXPECTED_STATES = previous_expected_states
        _ACTIVE_STORE_ROOT = previous_store_root


def validate_safe_id(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SAFE_ID.fullmatch(value) or ".." in value:
        raise StoreError(f"Invalid {label}: {value!r}")
    return value


def is_safe_id(value: Any) -> bool:
    return isinstance(value, str) and bool(SAFE_ID.fullmatch(value)) and ".." not in value


def context_path(store: Path) -> Path:
    return store / "context.json"


def evidence_path(store: Path) -> Path:
    return store / "evidence" / "index.json"


def load_context(store: Path) -> Dict[str, Any]:
    _assert_store_path_safe(store, context_path(store))
    return read_json(context_path(store))


def ensure_store_dirs(store: Path) -> None:
    _assert_store_path_safe(store, store, label="Store root")
    for relative in ("evidence", "views", "patches/pending", "patches/applied", "patches/rejected", "history"):
        directory = store / relative
        _assert_store_path_safe(store, directory)
        directory.mkdir(parents=True, exist_ok=True)
        _assert_store_path_safe(store, directory)


def empty_v04_context(context_id: str, display_name: str = "") -> Dict[str, Any]:
    timestamp = now_utc()
    return {
        "schema_version": V04_SCHEMA_VERSION,
        "context_id": context_id,
        "subject": {"type": "person", "id": context_id, "display_name": display_name, "preferred_languages": []},
        "policy": {"patch_approval_required": True, "default_view_ttl_days": DEFAULT_VIEW_TTL_DAYS, "auto_import_harness_memory": False},
        "coverage": {"depth": "quick", "included_domains": [], "missing_domains": []},
        "claims": [], "tensions": [], "unknowns": [], "sources": [],
        "revision": {"version": 1, "created_at": timestamp, "updated_at": timestamp, "last_reviewed_at": None},
    }


def schema_version(context: Dict[str, Any]) -> Any:
    return context.get("schema_version")


def require_v04(context: Dict[str, Any], operation: str) -> None:
    version = schema_version(context)
    if version in READ_ONLY_SCHEMA_VERSIONS:
        raise StoreError(f"{operation} is unavailable for schema {version}; {read_only_preview_message(version)}")
    if version != V04_SCHEMA_VERSION:
        raise StoreError(f"{operation} requires schema 1.0.1; unsupported schema_version: {version!r}")


def read_only_preview_message(version: Any) -> str:
    if version == V02_SCHEMA_VERSION:
        return "read-only: only validate/inspect are supported; export is unavailable; use explicit migrate-v02 for a V0.3 copy and never chain to 1.0.1"
    return "read-only preview: only validate/inspect and preview-migrate-v03 are supported; export is unavailable; no legacy View/Patch is migrated or rewritten"


def _enum(errors: List[str], item: Dict[str, Any], key: str, allowed: set[str], label: str) -> None:
    if item.get(key) not in allowed:
        errors.append(f"{label}.{key} must be one of {sorted(allowed)}, got {item.get(key)!r}")


def _string_list(value: Any, label: str, errors: List[str], *, allow_empty: bool = True) -> None:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        errors.append(f"{label} must be an array of non-empty strings")
    elif not allow_empty and not value:
        errors.append(f"{label} must not be empty")
    elif len(value) != len(set(value)):
        errors.append(f"{label} must contain unique values")


def evidence_ref_source_id(ref: str) -> str:
    return ref.split("#", 1)[0]


def validate_source(source: Any, label: str = "source") -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    if not isinstance(source, dict):
        return [f"{label} must be an object"], warnings
    try:
        validate_safe_id(source.get("id"), f"{label}.id")
    except StoreError as exc:
        errors.append(str(exc))
    for key in ("type", "title", "access_scope", "retention"):
        if not isinstance(source.get(key), str) or not source.get(key, "").strip():
            errors.append(f"{label}.{key} must be a non-empty string")
    if "locator" not in source:
        errors.append(f"{label}.locator is required")
    elif source.get("locator") is not None and not isinstance(source.get("locator"), str):
        errors.append(f"{label}.locator must be a string or null")
    if source.get("consent") != "explicit":
        errors.append(f"{label}.consent must be 'explicit'")
    if source.get("sensitivity") not in SENSITIVITIES:
        errors.append(f"{label}.sensitivity must be one of {sorted(SENSITIVITIES)}")
    try:
        parse_iso_utc(source.get("collected_at"), f"{label}.collected_at")
    except StoreError as exc:
        errors.append(str(exc))
    return errors, warnings


def iter_v04_claims(context: Dict[str, Any]) -> Iterable[Tuple[str, Dict[str, Any]]]:
    for index, claim in enumerate(context.get("claims", [])):
        if isinstance(claim, dict):
            yield f"claims[{index}]", claim


def iter_v04_items(context: Dict[str, Any], key: str) -> Iterable[Tuple[str, Dict[str, Any]]]:
    for index, item in enumerate(context.get(key, [])):
        if isinstance(item, dict):
            yield f"{key}[{index}]", item


def validate_v04_disclosure(disclosure: Any, label: str) -> List[str]:
    errors: List[str] = []
    if not isinstance(disclosure, dict) or set(disclosure) != {"audiences", "purposes", "allow_downstream_persistence"}:
        return [f"{label} must contain exactly audiences, purposes, allow_downstream_persistence"]
    _string_list(disclosure.get("audiences"), f"{label}.audiences", errors, allow_empty=False)
    _string_list(disclosure.get("purposes"), f"{label}.purposes", errors, allow_empty=False)
    if not isinstance(disclosure.get("allow_downstream_persistence"), bool):
        errors.append(f"{label}.allow_downstream_persistence must be boolean")
    return errors


def validate_v04_claim(claim: Any, label: str = "claim") -> List[str]:
    errors: List[str] = []
    if not isinstance(claim, dict):
        return [f"{label} must be an object"]
    missing = V04_CLAIM_FIELDS - set(claim)
    extra = set(claim) - V04_CLAIM_FIELDS
    errors.extend(f"{label}.{key} is required" for key in sorted(missing))
    errors.extend(f"{label}.{key} is not allowed" for key in sorted(extra))
    if not is_safe_id(claim.get("id")):
        errors.append(f"{label}.id is invalid")
    if not isinstance(claim.get("statement"), str) or not claim.get("statement", "").strip():
        errors.append(f"{label}.statement must be a non-empty string")
    _string_list(claim.get("domains"), f"{label}.domains", errors)
    for key, allowed in (("kind", KINDS), ("scope", SCOPES), ("durability", DURABILITIES), ("confidence", CONFIDENCES), ("user_status", USER_STATUSES), ("status", CLAIM_STATUSES), ("sensitivity", SENSITIVITIES)):
        _enum(errors, claim, key, allowed, label)
    errors.extend(validate_v04_disclosure(claim.get("disclosure"), f"{label}.disclosure"))
    for key in ("evidence_refs", "counterevidence_refs", "supersedes"):
        _string_list(claim.get(key), f"{label}.{key}", errors)
        if key == "supersedes" and isinstance(claim.get(key), list):
            errors.extend(f"{label}.supersedes contains invalid ID {value!r}" for value in claim[key] if not is_safe_id(value))
    for key in ("observed_at", "valid_from", "last_confirmed_at", "review_after", "expires_at"):
        errors.extend(validate_date_or_datetime(claim.get(key), f"{label}.{key}"))
    if not isinstance(claim.get("notes"), str):
        errors.append(f"{label}.notes must be a string")
    return errors


def validate_v04_context_item(item: Any, item_type: str, label: str) -> List[str]:
    errors: List[str] = []
    if not isinstance(item, dict):
        return [f"{label} must be an object"]
    allowed_fields = V04_TENSION_FIELDS if item_type == "tension" else V04_UNKNOWN_FIELDS
    errors.extend(f"{label}.{key} is not allowed" for key in sorted(set(item) - allowed_fields))
    if not is_safe_id(item.get("id")):
        errors.append(f"{label}.id is invalid")
    _string_list(item.get("domains"), f"{label}.domains", errors)
    required = ("statement_a", "statement_b") if item_type == "tension" else ("question",)
    for key in required:
        if not isinstance(item.get(key), str) or not item.get(key, "").strip():
            errors.append(f"{label}.{key} must be a non-empty string")
    if item_type == "tension" and "interpretation" in item and item.get("interpretation") is not None and not isinstance(item.get("interpretation"), str):
        errors.append(f"{label}.interpretation must be a string or null")
    for key, allowed in (("user_status", USER_STATUSES), ("status", CLAIM_STATUSES), ("sensitivity", SENSITIVITIES)):
        _enum(errors, item, key, allowed, label)
    _string_list(item.get("evidence_refs"), f"{label}.evidence_refs", errors)
    sensitivity = item.get("sensitivity")
    if sensitivity != "public" and "disclosure" not in item:
        errors.append(f"{label}.disclosure is required for non-public content")
    if "disclosure" in item:
        errors.extend(validate_v04_disclosure(item.get("disclosure"), f"{label}.disclosure"))
    return errors


def validate_v04_context(context: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    if set(context) != V04_TOP_LEVEL:
        errors.extend(f"unknown top-level field: {key}" for key in sorted(set(context) - V04_TOP_LEVEL))
        errors.extend(f"missing top-level field: {key}" for key in sorted(V04_TOP_LEVEL - set(context)))
    if context.get("schema_version") != V04_SCHEMA_VERSION:
        errors.append("schema_version must be '1.0.1'")
    context_id = context.get("context_id")
    if not is_safe_id(context_id):
        errors.append("context_id is invalid")
    subject = context.get("subject")
    if not isinstance(subject, dict) or set(subject) != {"type", "id", "display_name", "preferred_languages"}:
        errors.append("subject must contain exactly type, id, display_name, preferred_languages")
    elif subject.get("type") != "person" or subject.get("id") != context_id:
        errors.append("subject.type must be person and subject.id must equal context_id")
    elif not isinstance(subject.get("display_name"), str):
        errors.append("subject.display_name must be a string")
    else:
        _string_list(subject.get("preferred_languages"), "subject.preferred_languages", errors)
    policy = context.get("policy")
    if not isinstance(policy, dict) or set(policy) != {"patch_approval_required", "default_view_ttl_days", "auto_import_harness_memory"}:
        errors.append("policy must contain exactly patch_approval_required, default_view_ttl_days, auto_import_harness_memory")
    elif (type(policy.get("patch_approval_required")) is not bool or type(policy.get("default_view_ttl_days")) is not int or policy.get("default_view_ttl_days", 0) < 1 or policy.get("auto_import_harness_memory") is not False):
        errors.append("policy is invalid")
    coverage = context.get("coverage")
    if not isinstance(coverage, dict) or set(coverage) != {"depth", "included_domains", "missing_domains"}:
        errors.append("coverage must contain exactly depth, included_domains, missing_domains")
    elif coverage.get("depth") not in {"quick", "standard", "deep"}:
        errors.append("coverage.depth is invalid")
    else:
        _string_list(coverage.get("included_domains"), "coverage.included_domains", errors)
        _string_list(coverage.get("missing_domains"), "coverage.missing_domains", errors)
    for key in ("claims", "tensions", "unknowns", "sources"):
        if not isinstance(context.get(key), list):
            errors.append(f"{key} must be an array")
    revision = context.get("revision")
    if not isinstance(revision, dict) or set(revision) != {"version", "created_at", "updated_at", "last_reviewed_at"}:
        errors.append("revision must contain exactly version, created_at, updated_at, last_reviewed_at")
    elif type(revision.get("version")) is not int or revision.get("version", 0) < 1:
        errors.append("revision.version must be a positive integer")
    else:
        for key in ("created_at", "updated_at"):
            try:
                parse_iso_utc(revision.get(key), f"revision.{key}")
            except StoreError as exc:
                errors.append(str(exc))
        try:
            parse_iso_utc(revision.get("last_reviewed_at"), "revision.last_reviewed_at", allow_none=True)
        except StoreError as exc:
            errors.append(str(exc))
    seen_ids: Dict[str, str] = {}
    source_ids: set[str] = set()
    if isinstance(context.get("claims"), list):
        for index, claim in enumerate(context["claims"]):
            label = f"claims[{index}]"
            errors.extend(validate_v04_claim(claim, label))
            if isinstance(claim, dict) and is_safe_id(claim.get("id")):
                if claim["id"] in seen_ids:
                    errors.append(f"duplicate ID {claim['id']!r}: {seen_ids[claim['id']]} and {label}")
                else:
                    seen_ids[claim["id"]] = label
    for key, item_type in (("tensions", "tension"), ("unknowns", "unknown")):
        if isinstance(context.get(key), list):
            for index, item in enumerate(context[key]):
                label = f"{key}[{index}]"
                errors.extend(validate_v04_context_item(item, item_type, label))
                if isinstance(item, dict) and is_safe_id(item.get("id")):
                    if item["id"] in seen_ids:
                        errors.append(f"duplicate ID {item['id']!r}: {seen_ids[item['id']]} and {label}")
                    else:
                        seen_ids[item["id"]] = label
    if isinstance(context.get("sources"), list):
        for index, source in enumerate(context["sources"]):
            label = f"sources[{index}]"
            errors.extend(validate_source(source, label)[0])
            if isinstance(source, dict) and is_safe_id(source.get("id")):
                source_id = source["id"]
                if source_id in source_ids:
                    errors.append(f"duplicate source id {source_id!r}")
                source_ids.add(source_id)
                if source_id in seen_ids:
                    errors.append(f"duplicate global ID {source_id!r}: {seen_ids[source_id]} and {label}")
                else:
                    seen_ids[source_id] = label
    for key in ("claims", "tensions", "unknowns"):
        for index, item in enumerate(context.get(key, []) if isinstance(context.get(key), list) else []):
            if not isinstance(item, dict):
                continue
            refs = list(item.get("evidence_refs", []))
            if key == "claims":
                refs += list(item.get("counterevidence_refs", []))
            for ref in refs:
                if isinstance(ref, str) and evidence_ref_source_id(ref) not in source_ids:
                    errors.append(f"{key}[{index}] references unknown source {evidence_ref_source_id(ref)!r}")
    return errors, warnings


def validate_evidence_index_v04(store: Path, context: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    try:
        evidence = read_json(evidence_path(store))
    except StoreError as exc:
        return [str(exc)]
    if set(evidence) != {"schema_version", "sources"}:
        errors.extend(f"evidence/index.json unknown field: {key}" for key in sorted(set(evidence) - {"schema_version", "sources"}))
    if evidence.get("schema_version") != V04_SCHEMA_VERSION:
        errors.append("evidence/index.json.schema_version must be '1.0.1'")
    sources = evidence.get("sources")
    if not isinstance(sources, list):
        errors.append("evidence/index.json.sources must be an array")
    elif sources != context.get("sources"):
        errors.append("evidence/index.json.sources must exactly match context.sources")
    return errors


def validate_v03_claim(claim: Any, expected_layer: str, expected_domain: Optional[str], label: str) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    if not isinstance(claim, dict):
        return [f"{label} must be an object"], warnings
    try:
        validate_safe_id(claim.get("id"), f"{label}.id")
    except StoreError as exc:
        errors.append(str(exc))
    if not isinstance(claim.get("statement"), str) or not claim.get("statement", "").strip():
        errors.append(f"{label}.statement must be a non-empty string")
    for key, allowed in (("layer", {"core", "domain"}), ("kind", KINDS), ("scope", SCOPES), ("durability", DURABILITIES), ("confidence", CONFIDENCES), ("user_status", USER_STATUSES), ("status", CLAIM_STATUSES), ("sensitivity", SENSITIVITIES)):
        _enum(errors, claim, key, allowed, label)
    if claim.get("layer") != expected_layer:
        errors.append(f"{label}.layer must be {expected_layer!r}")
    if expected_layer == "core":
        if claim.get("domain") not in (None, ""):
            errors.append(f"{label}.domain must be null or empty for core claims")
        if claim.get("status") == "active":
            if claim.get("user_status") != "confirmed":
                errors.append(f"{label}: active core claim must be user-confirmed")
            if claim.get("scope") != "cross-context":
                errors.append(f"{label}: active core claim must have cross-context scope")
            if claim.get("kind") == "inference":
                errors.append(f"{label}: inference cannot be an active core claim")
            if not claim.get("evidence_refs"):
                errors.append(f"{label}: active core claim requires evidence_refs")
            if not claim.get("promotion_evidence"):
                errors.append(f"{label}: active core claim requires promotion_evidence")
    elif claim.get("domain") != expected_domain:
        errors.append(f"{label}.domain must equal {expected_domain!r}")
    for key in ("evidence_refs", "counterevidence_refs", "promotion_evidence", "supersedes"):
        if not isinstance(claim.get(key, []), list) or not all(isinstance(value, str) for value in claim.get(key, [])):
            errors.append(f"{label}.{key} must be an array of strings")
    if claim.get("user_status") == "unreviewed" and claim.get("confidence") == "high":
        warnings.append(f"{label}: unreviewed claim should rarely have high confidence")
    return errors, warnings


def iter_v03_claims(context: Dict[str, Any]) -> Iterable[Tuple[str, Dict[str, Any], str, Optional[str]]]:
    core = context.get("core", {})
    if isinstance(core, dict):
        for index, claim in enumerate(core.get("claims", [])):
            yield f"core.claims[{index}]", claim, "core", None
    domains = context.get("domains", {})
    if isinstance(domains, dict):
        for domain_name, domain_data in domains.items():
            if isinstance(domain_data, dict):
                for index, claim in enumerate(domain_data.get("claims", [])):
                    yield f"domains.{domain_name}.claims[{index}]", claim, "domain", domain_name


def iter_v03_sections(context: Dict[str, Any]) -> Iterable[Tuple[str, Dict[str, Any]]]:
    core = context.get("core", {})
    if isinstance(core, dict):
        yield "core", core
    domains = context.get("domains", {})
    if isinstance(domains, dict):
        for domain_name, section in domains.items():
            if isinstance(section, dict):
                yield f"domains.{domain_name}", section


def validate_v03_item(item: Any, item_type: str, label: str, version: str) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    if not isinstance(item, dict):
        return [f"{label} must be an object"], warnings
    try:
        validate_safe_id(item.get("id"), f"{label}.id")
    except StoreError as exc:
        errors.append(str(exc))
    required = ("statement_a", "statement_b") if item_type == "tension" else ("question",)
    for key in required:
        if not isinstance(item.get(key), str) or not item.get(key, "").strip():
            errors.append(f"{label}.{key} must be a non-empty string")
    for key, allowed, default in (("sensitivity", SENSITIVITIES, "private"), ("user_status", USER_STATUSES, "unreviewed"), ("status", CLAIM_STATUSES, "active")):
        value = item.get(key)
        if value is None and version == V02_SCHEMA_VERSION:
            warnings.append(f"{label}.{key} is absent in legacy v0.2; migration will set {default!r}")
        elif value not in allowed:
            errors.append(f"{label}.{key} must be one of {sorted(allowed)}, got {value!r}")
    if not isinstance(item.get("evidence_refs", []), list) or not all(isinstance(value, str) for value in item.get("evidence_refs", [])):
        errors.append(f"{label}.evidence_refs must be an array of strings")
    return errors, warnings


def iter_v03_evidence_refs(context: Dict[str, Any]) -> Iterable[Tuple[str, str, Optional[str], str]]:
    """Yield label, exact ref, item id and item type for every legacy ref."""

    for label, claim, _layer, _domain in iter_v03_claims(context):
        if not isinstance(claim, dict):
            continue
        item_id = claim.get("id") if isinstance(claim.get("id"), str) else None
        # V0.3 promotion_evidence is legacy metadata and may contain domain
        # labels rather than Source refs; only evidence/counterevidence refs
        # participate in unresolved Source compatibility.
        for field in ("evidence_refs", "counterevidence_refs"):
            for ref in claim.get(field, []) if isinstance(claim.get(field), list) else []:
                if isinstance(ref, str):
                    yield label, ref, item_id, "claim"
    for section_label, section in iter_v03_sections(context):
        for item_type, key in (("tension", "tensions"), ("unknown", "unknowns")):
            values = section.get(key, []) if isinstance(section, dict) else []
            for index, item in enumerate(values if isinstance(values, list) else []):
                if not isinstance(item, dict):
                    continue
                item_id = item.get("id") if isinstance(item.get("id"), str) else None
                for ref in item.get("evidence_refs", []) if isinstance(item.get("evidence_refs"), list) else []:
                    if isinstance(ref, str):
                        yield f"{section_label}.{key}[{index}]", ref, item_id, item_type


def history_proves_legacy_ref(store: Optional[Path], item_type: str, item_id: Optional[str], ref: str) -> bool:
    """Prove a global-only legacy exception from a pre-migration v0.2 snapshot."""

    if store is None or not isinstance(item_id, str):
        return False
    history = store / "history"
    if not history.exists():
        return False
    for snapshot in sorted(history.glob("*.json")):
        try:
            candidate = read_json(snapshot)
        except StoreError:
            continue
        if candidate.get("schema_version") != V02_SCHEMA_VERSION:
            continue
        for _label, candidate_ref, candidate_id, candidate_type in iter_v03_evidence_refs(candidate):
            if candidate_type == item_type and candidate_id == item_id and candidate_ref == ref:
                return True
    return False


def validate_v03_context(context: Dict[str, Any], *, store: Optional[Path] = None) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    version = context.get("schema_version")
    if version not in {V02_SCHEMA_VERSION, V03_SCHEMA_VERSION}:
        return [f"legacy schema_version must be one of ['0.2', '0.3'], got {version!r}"], warnings
    if version == V02_SCHEMA_VERSION:
        warnings.append("legacy schema v0.2 is read-only; run migrate-v02 explicitly to create a v0.3 Store")
    try:
        validate_safe_id(context.get("profile_id"), "profile_id")
    except StoreError as exc:
        errors.append(str(exc))
    for key in ("subject", "policy", "coverage", "core", "domains", "revision"):
        if not isinstance(context.get(key), dict):
            errors.append(f"{key} must be an object")
    if not isinstance(context.get("sources"), list):
        errors.append("sources must be an array")
    revision = context.get("revision", {})
    if isinstance(revision, dict) and (type(revision.get("version")) is not int or revision.get("version", 0) < 1):
        errors.append("revision.version must be a positive integer")
    seen: Dict[str, str] = {}
    refs: List[Tuple[str, str, Optional[str], str]] = []
    active_core: List[Dict[str, Any]] = []
    for label, claim, layer, domain in iter_v03_claims(context):
        claim_errors, claim_warnings = validate_v03_claim(claim, layer, domain, label)
        errors.extend(claim_errors)
        warnings.extend(claim_warnings)
        if isinstance(claim, dict):
            claim_id = claim.get("id")
            if isinstance(claim_id, str):
                if claim_id in seen:
                    errors.append(f"duplicate claim id {claim_id!r}: {seen[claim_id]} and {label}")
                else:
                    seen[claim_id] = label
            if layer == "core" and claim.get("status") == "active":
                active_core.append(claim)
            item_id = claim_id if isinstance(claim_id, str) else None
            for field in ("evidence_refs", "counterevidence_refs"):
                for value in claim.get(field, []) if isinstance(claim.get(field), list) else []:
                    if isinstance(value, str):
                        refs.append((f"{label}.{field}", value, item_id, "claim"))
    for section_label, section in iter_v03_sections(context):
        for item_type, key in (("tension", "tensions"), ("unknown", "unknowns")):
            values = section.get(key, [])
            if not isinstance(values, list):
                errors.append(f"{section_label}.{key} must be an array")
                continue
            for index, item in enumerate(values):
                label = f"{section_label}.{key}[{index}]"
                item_errors, item_warnings = validate_v03_item(item, item_type, label, version)
                errors.extend(item_errors)
                warnings.extend(item_warnings)
                if isinstance(item, dict):
                    item_id = item.get("id")
                    if isinstance(item_id, str):
                        if item_id in seen:
                            errors.append(f"duplicate context item id {item_id!r}: {seen[item_id]} and {label}")
                        else:
                            seen[item_id] = label
                    item_id = item.get("id") if isinstance(item.get("id"), str) else None
                    for value in item.get("evidence_refs", []) if isinstance(item.get("evidence_refs"), list) else []:
                        if isinstance(value, str):
                            refs.append((label, value, item_id, item_type))
    source_ids: set[str] = set()
    for index, source in enumerate(context.get("sources", []) if isinstance(context.get("sources"), list) else []):
        label = f"sources[{index}]"
        source_errors, source_warnings = validate_source(source, label)
        errors.extend(source_errors)
        warnings.extend(source_warnings)
        if isinstance(source, dict) and isinstance(source.get("id"), str):
            if source["id"] in source_ids:
                errors.append(f"duplicate source id {source['id']!r}")
            source_ids.add(source["id"])
    # The explicit V0.2 -> V0.3 migration preserves source references that
    # cannot be resolved inside the legacy Store.  Those references are
    # accepted only when the migration record names them; a normal V0.3 Store
    # remains fail-closed for unknown sources.
    unresolved_legacy_sources: set[str] = set()
    unresolved_bindings: set[Tuple[str, str, str]] = set()
    observed_bindings: set[Tuple[str, str, str]] = set()
    global_only_migration = False
    migration = context.get("migration")
    if version == V03_SCHEMA_VERSION and migration is not None:
        if not isinstance(migration, dict) or migration.get("from_schema") != V02_SCHEMA_VERSION:
            errors.append("migration must describe an explicit v0.2 source")
        else:
            migrated_at = migration.get("migrated_at")
            try:
                parse_iso_utc(migrated_at, "migration.migrated_at")
            except StoreError as exc:
                errors.append(str(exc))
            if not isinstance(migration.get("confirmed_by"), str) or not migration.get("confirmed_by", "").strip():
                errors.append("migration.confirmed_by must be a non-empty string")
            unresolved = migration.get("unresolved_evidence_source_ids", [])
            if not isinstance(unresolved, list) or not all(isinstance(value, str) and is_safe_id(value) for value in unresolved):
                errors.append("migration.unresolved_evidence_source_ids must be an array of safe IDs")
            else:
                unresolved_legacy_sources = set(unresolved)
            bindings = migration.get("unresolved_evidence_bindings")
            if bindings is None:
                global_only_migration = True
            elif not isinstance(bindings, list):
                errors.append("migration.unresolved_evidence_bindings must be an array")
            else:
                for index, binding in enumerate(bindings):
                    if not isinstance(binding, dict) or set(binding) != {"item_type", "item_id", "ref"}:
                        errors.append(f"migration.unresolved_evidence_bindings[{index}] must contain item_type, item_id, ref")
                        continue
                    item_type = binding.get("item_type")
                    item_id = binding.get("item_id")
                    ref = binding.get("ref")
                    if item_type not in {"claim", "tension", "unknown"} or not is_safe_id(item_id) or not isinstance(ref, str) or not ref.strip():
                        errors.append(f"migration.unresolved_evidence_bindings[{index}] has invalid identity or ref")
                        continue
                    unresolved_bindings.add((item_type, item_id, ref))
    for label, ref, item_id, item_type in refs:
        source_id = evidence_ref_source_id(ref)
        if source_id not in source_ids:
            message = f"{label}.evidence_refs references unknown source {source_id!r}"
            if version == V02_SCHEMA_VERSION:
                warnings.append(message + "; accepted read-only for v0.2 compatibility")
            elif (item_type, item_id, ref) in unresolved_bindings:
                observed_bindings.add((item_type, item_id, ref))
                warnings.append(message + "; preserved as an exact unresolved evidence binding from explicit v0.2 migration")
            elif global_only_migration and source_id in unresolved_legacy_sources and history_proves_legacy_ref(store, item_type, item_id, ref):
                warnings.append(message + "; preserved from a history-proven legacy v0.2 reference")
            else:
                errors.append(message)
    if version == V03_SCHEMA_VERSION and migration is not None:
        for binding in sorted(unresolved_bindings - observed_bindings):
            errors.append(f"migration unresolved evidence binding does not match an unknown current reference: {binding!r}")
    policy = context.get("policy", {})
    if isinstance(policy, dict):
        limit = policy.get("core_claim_soft_limit", 30)
        chars = policy.get("core_char_soft_limit", 8000)
        if type(limit) is int and len(active_core) > limit:
            warnings.append(f"active core claims {len(active_core)} exceed soft limit {limit}")
        if type(chars) is int:
            count = sum(len(str(item.get("statement", ""))) for item in active_core)
            if count > chars:
                warnings.append(f"active core statement chars {count} exceed soft limit {chars}")
    return errors, warnings


def validate_context(context: Dict[str, Any], *, store: Optional[Path] = None) -> Tuple[List[str], List[str]]:
    if schema_version(context) == V04_SCHEMA_VERSION:
        return validate_v04_context(context)
    return validate_v03_context(context, store=store)


def validate_store_for_command(store: Path, context: Dict[str, Any], operation: str) -> None:
    _assert_store_tree_safe(store)
    require_v04(context, operation)
    errors, _ = validate_v04_context(context)
    errors.extend(validate_evidence_index_v04(store, context))
    if errors:
        raise StoreError("Store is invalid: " + "; ".join(errors))


def find_v04_claim(context: Dict[str, Any], claim_id: str) -> Tuple[List[Dict[str, Any]], int, Dict[str, Any]]:
    for index, claim in enumerate(context.get("claims", [])):
        if isinstance(claim, dict) and claim.get("id") == claim_id:
            return context["claims"], index, claim
    raise StoreError(f"Claim not found: {claim_id}")


def find_v03_claim(context: Dict[str, Any], claim_id: str) -> Tuple[List[Dict[str, Any]], int, Dict[str, Any], str, Optional[str]]:
    core_claims = context.get("core", {}).get("claims", [])
    for index, claim in enumerate(core_claims):
        if isinstance(claim, dict) and claim.get("id") == claim_id:
            return core_claims, index, claim, "core", None
    for domain_name, section in context.get("domains", {}).items():
        if isinstance(section, dict):
            claims = section.get("claims", [])
            for index, claim in enumerate(claims):
                if isinstance(claim, dict) and claim.get("id") == claim_id:
                    return claims, index, claim, "domain", domain_name
    raise StoreError(f"Claim not found: {claim_id}")


def all_v04_ids(context: Dict[str, Any]) -> set[str]:
    return {item.get("id") for key in ("claims", "tensions", "unknowns", "sources") for item in context.get(key, []) if isinstance(item, dict) and isinstance(item.get("id"), str)}


def validate_entity(entity: Any, label: str) -> List[str]:
    errors: List[str] = []
    if not isinstance(entity, dict) or set(entity) != {"type", "id"}:
        return [f"{label} must contain exactly type and id"]
    if entity.get("type") != AGENT_ENTITY_TYPE:
        errors.append(f"{label}.type must be 'agent' for the 1.0 runtime")
    if not is_safe_id(entity.get("id")):
        errors.append(f"{label}.id is invalid")
    return errors


def principal_from_args(args: argparse.Namespace) -> Dict[str, str]:
    principal_id = getattr(args, "principal_id", None) or "self-agent"
    principal_type = getattr(args, "principal_type", None) or "agent"
    if principal_type != AGENT_ENTITY_TYPE:
        raise StoreError("principal type must be 'agent'; team, organization, shared, and unknown types are rejected")
    return {"type": AGENT_ENTITY_TYPE, "id": validate_safe_id(principal_id, "principal_id")}


def audience_from_args(args: argparse.Namespace, principal: Dict[str, str]) -> List[Dict[str, str]]:
    values: List[str] = []
    for key in ("audience_id", "audience_ids", "audience"):
        value = getattr(args, key, None)
        if isinstance(value, list):
            values.extend(value)
        elif isinstance(value, str) and value:
            values.append(value)
    ids: List[str] = [principal["id"]]
    for value in values:
        validate_safe_id(value, "audience_id")
        if value not in ids:
            ids.append(value)
    audience_type = getattr(args, "audience_type", None) or principal.get("type", "agent")
    if audience_type != AGENT_ENTITY_TYPE:
        raise StoreError("audience type must be 'agent'; team, organization, shared, and unknown types are rejected")
    return [{"type": AGENT_ENTITY_TYPE, "id": item} for item in ids]


def claim_disclosure_allows(claim: Dict[str, Any], principal_id: str, purpose: str, purpose_approved: bool, audience_ids: Optional[Sequence[str]] = None) -> bool:
    disclosure = claim.get("disclosure")
    if not isinstance(disclosure, dict):
        return False
    required_audiences = list(audience_ids) if audience_ids is not None else [principal_id]
    if principal_id not in required_audiences or any(audience_id not in disclosure.get("audiences", []) for audience_id in required_audiences):
        return False
    return purpose in disclosure.get("purposes", []) or ("user-approved" in disclosure.get("purposes", []) and purpose_approved)


def claim_allowed_v04(
    claim: Dict[str, Any],
    sensitivities: set[str],
    principal_id: str,
    purpose: str,
    purpose_approved: bool,
    audience_ids: Optional[Sequence[str]] = None,
    *,
    include_unreviewed: bool = False,
) -> bool:
    return (
        claim.get("status") == "active"
        and (claim.get("user_status") in {"confirmed", "corrected"} or (include_unreviewed and claim.get("user_status") in {"unreviewed", "unresolved"}))
        and not claim_temporal_errors(claim, "claim")
        and claim.get("sensitivity") in sensitivities
        and claim_disclosure_allows(claim, principal_id, purpose, purpose_approved, audience_ids)
    )


def item_disclosure_allows(
    item: Dict[str, Any],
    principal_id: str,
    purpose: str,
    purpose_approved: bool,
    audience_ids: Optional[Sequence[str]] = None,
) -> bool:
    disclosure = item.get("disclosure")
    if item.get("sensitivity") == "public" and disclosure is None:
        return True
    return claim_disclosure_allows(item, principal_id, purpose, purpose_approved, audience_ids)


def item_allowed_v04(
    item: Dict[str, Any],
    sensitivities: set[str],
    principal_id: str,
    purpose: str,
    purpose_approved: bool,
    audience_ids: Optional[Sequence[str]] = None,
    *,
    include_unreviewed: bool = False,
) -> bool:
    reviewed = item.get("user_status") in {"confirmed", "corrected"} or (
        include_unreviewed and item.get("user_status") in {"unreviewed", "unresolved"}
    )
    return (
        item.get("status") == "active"
        and reviewed
        and item.get("sensitivity") in sensitivities
        and item_disclosure_allows(item, principal_id, purpose, purpose_approved, audience_ids)
    )


def select_v04_items(index: Dict[str, Dict[str, Any]], requested: Sequence[str], label: str, predicate) -> List[Dict[str, Any]]:
    selected: List[Dict[str, Any]] = []
    seen: set[str] = set()
    for item_id in requested:
        validate_safe_id(item_id, f"{label}_id")
        if item_id in seen:
            raise StoreError(f"duplicate requested {label} id: {item_id}")
        seen.add(item_id)
        item = index.get(item_id)
        if item is None:
            raise StoreError(f"Requested {label} not found: {item_id}")
        if not predicate(item):
            raise StoreError(f"Requested {label} is not allowed by status, disclosure, purpose, or sensitivity: {item_id}")
        selected.append(copy.deepcopy(item))
    return selected


def validate_v04_view(
    view: Any,
    context: Optional[Dict[str, Any]] = None,
    *,
    purpose_approved: bool = False,
    include_unreviewed: bool = False,
) -> Tuple[List[str], List[str]]:
    errors: List[str] = validate_view_core(
        view,
        include_unreviewed=include_unreviewed,
    )
    warnings: List[str] = []
    if not isinstance(view, dict):
        return ["view must be an object"], warnings
    if set(view) != V04_VIEW_FIELDS:
        errors.extend(f"unknown view field: {key}" for key in sorted(set(view) - V04_VIEW_FIELDS))
        errors.extend(f"missing view field: {key}" for key in sorted(V04_VIEW_FIELDS - set(view)))
    if view.get("schema_version") != V04_SCHEMA_VERSION:
        errors.append("view.schema_version must be '1.0.1'")
    if not is_safe_id(view.get("view_id")):
        errors.append("view.view_id is invalid")
    subject = view.get("subject")
    if not isinstance(subject, dict) or set(subject) != {"type", "id"} or subject.get("type") != "person" or not is_safe_id(subject.get("id")):
        errors.append("view.subject is invalid")
    errors.extend(validate_entity(view.get("principal"), "view.principal"))
    principal = view.get("principal", {})
    audience = view.get("audience")
    audience_ids: List[str] = []
    if not isinstance(audience, list) or not audience:
        errors.append("view.audience must be a non-empty array")
        audience = []
    else:
        for index, entity in enumerate(audience):
            errors.extend(validate_entity(entity, f"view.audience[{index}]"))
        audience_ids = [entity.get("id") for entity in audience if isinstance(entity, dict)]
        if principal.get("id") not in audience_ids:
            errors.append("view.audience must include view.principal.id")
        if len(audience_ids) != len(set(audience_ids)):
            errors.append("view.audience IDs must be unique")
    for key in ("purpose", "task"):
        if not isinstance(view.get(key), str) or not view.get(key, "").strip():
            errors.append(f"view.{key} must be a non-empty string")
    if type(view.get("source_revision")) is not int or view.get("source_revision", 0) < 1:
        errors.append("view.source_revision must be a positive integer")
    for key in ("created_at", "expires_at"):
        try:
            parse_iso_utc(view.get(key), f"view.{key}")
        except StoreError as exc:
            errors.append(str(exc))
    try:
        expiry = parse_iso_utc(view.get("expires_at"), "view.expires_at")
        if expiry is not None and expiry <= datetime.now(timezone.utc):
            errors.append("view has expired")
    except StoreError:
        pass
    view_seen_ids: Dict[str, str] = {}
    for key, item_type in (("claims", "claim"), ("tensions", "tension"), ("relevant_unknowns", "unknown")):
        values = view.get(key)
        if not isinstance(values, list):
            errors.append(f"view.{key} must be an array")
            continue
        for index, item in enumerate(values):
            label = f"view.{key}[{index}]"
            if item_type == "claim":
                errors.extend(validate_v04_claim(item, label))
                if isinstance(item, dict):
                    if item.get("status") != "active":
                        errors.append(f"{label} status must be active for a View")
                    if item.get("user_status") not in {"confirmed", "corrected"}:
                        if not (include_unreviewed and item.get("user_status") in {"unreviewed", "unresolved"}):
                            errors.append(f"{label} user_status must be confirmed/corrected for a View unless include-unreviewed is explicit")
                    if item.get("user_status") == "rejected":
                        errors.append(f"{label} user_status rejected cannot be included in a View")
                    errors.extend(claim_temporal_errors(item, label))
                    if not item_disclosure_allows(item, principal.get("id"), view.get("purpose", ""), purpose_approved, audience_ids):
                        errors.append(f"{label} disclosure does not authorize every view audience and purpose")
            else:
                errors.extend(validate_v04_context_item(item, item_type, label))
                if isinstance(item, dict):
                    if item.get("status") != "active":
                        errors.append(f"{label} status must be active for a View")
                    if item.get("user_status") not in {"confirmed", "corrected"}:
                        if not (include_unreviewed and item.get("user_status") in {"unreviewed", "unresolved"}):
                            errors.append(f"{label} user_status must be confirmed/corrected for a View unless include-unreviewed is explicit")
                    disclosure = item.get("disclosure")
                    if disclosure is not None and isinstance(principal, dict):
                        if not item_disclosure_allows(item, principal.get("id"), view.get("purpose", ""), purpose_approved, audience_ids):
                            errors.append(f"{label} disclosure does not authorize every view audience and purpose")
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                item_id = item["id"]
                if item_id in view_seen_ids:
                    errors.append(f"view object ID {item_id!r} is duplicated in {view_seen_ids[item_id]} and {label}")
                else:
                    view_seen_ids[item_id] = label
    if not isinstance(view.get("exclusions"), list) or not all(isinstance(value, str) for value in view.get("exclusions", [])):
        errors.append("view.exclusions must be an array of strings")
    permission = view.get("permission")
    if not isinstance(permission, dict) or set(permission) != {"allowed_use", "archive_in_personal_store", "allow_downstream_persistence"}:
        errors.append("view.permission must contain exactly allowed_use, archive_in_personal_store, allow_downstream_persistence")
    elif (not isinstance(permission.get("allowed_use"), str) or not permission.get("allowed_use", "").strip() or not isinstance(permission.get("archive_in_personal_store"), bool) or not isinstance(permission.get("allow_downstream_persistence"), bool)):
        errors.append("view.permission is invalid")
    elif permission.get("allow_downstream_persistence"):
        persistence_error = False
        for key in ("claims", "tensions", "relevant_unknowns"):
            for item in view.get(key, []):
                if not isinstance(item, dict):
                    continue
                disclosure = item.get("disclosure")
                if not isinstance(disclosure, dict) or disclosure.get("allow_downstream_persistence") is not True:
                    errors.append(f"view permission cannot allow downstream persistence for {key} item without explicit disclosure")
                    persistence_error = True
                    break
            if persistence_error:
                break
    if context is not None:
        if view.get("subject", {}).get("id") != context.get("context_id"):
            errors.append("view.subject.id does not match the Store")
        current = context.get("revision", {}).get("version")
        if type(current) is int and view.get("source_revision") != current:
            warnings.append("view is frozen against a different Store revision")
        source_ids = {source.get("id") for source in context.get("sources", []) if isinstance(source, dict)}
        for key in ("claims", "tensions", "relevant_unknowns"):
            for index, item in enumerate(view.get(key, []) if isinstance(view.get(key), list) else []):
                if not isinstance(item, dict):
                    continue
                refs = list(item.get("evidence_refs", []))
                if key == "claims":
                    refs.extend(item.get("counterevidence_refs", []))
                for ref in refs:
                    if isinstance(ref, str) and evidence_ref_source_id(ref) not in source_ids:
                        errors.append(f"view.{key}[{index}] references unknown source {evidence_ref_source_id(ref)!r}")
    return errors, warnings


def validate_v03_view(view: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    if view.get("schema_version") not in {V02_SCHEMA_VERSION, V03_SCHEMA_VERSION}:
        errors.append("view schema_version must be one of 0.2 or 0.3")
    try:
        validate_safe_id(view.get("view_id"), "view_id")
    except StoreError as exc:
        errors.append(str(exc))
    for key in ("purpose", "task"):
        if not isinstance(view.get(key), str) or not view.get(key, "").strip():
            errors.append(f"view.{key} must be a non-empty string")
    if type(view.get("parent_revision")) is not int or view.get("parent_revision", 0) < 1:
        errors.append("view.parent_revision must be a positive integer")
    if context is not None and view.get("parent_profile_id") != context.get("profile_id"):
        errors.append("view.parent_profile_id does not match the Store")
    try:
        parse_iso_utc(view.get("created_at"), "view.created_at")
    except StoreError as exc:
        errors.append(str(exc))
    if view.get("expires_at") is not None:
        try:
            if parse_iso_utc(view.get("expires_at"), "view.expires_at") <= datetime.now(timezone.utc):
                errors.append("view has expired")
        except StoreError as exc:
            errors.append(str(exc))
    permission = view.get("permission")
    if not isinstance(permission, dict):
        errors.append("view.permission must be an object")
    elif not isinstance(permission.get("allowed_use"), str) or not permission.get("allowed_use", "").strip():
        errors.append("view.permission.allowed_use must be a non-empty string")
    return errors, warnings


def validate_view_data(
    view: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None,
    *,
    purpose_approved: bool = False,
    include_unreviewed: bool = False,
) -> Tuple[List[str], List[str]]:
    if view.get("schema_version") == V04_SCHEMA_VERSION:
        return validate_v04_view(view, context, purpose_approved=purpose_approved, include_unreviewed=include_unreviewed)
    return validate_v03_view(view, context)


def validate_v04_patch(patch: Any, context: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if not isinstance(patch, dict):
        return ["patch must be an object"]
    if set(patch) != V04_PATCH_FIELDS:
        errors.extend(f"unknown patch field: {key}" for key in sorted(set(patch) - V04_PATCH_FIELDS))
        errors.extend(f"missing patch field: {key}" for key in sorted(V04_PATCH_FIELDS - set(patch)))
    if patch.get("schema_version") != V04_SCHEMA_VERSION:
        errors.append("patch.schema_version must be '1.0.1'")
    if not is_safe_id(patch.get("patch_id")):
        errors.append("patch.patch_id is invalid")
    subject = patch.get("subject")
    if not isinstance(subject, dict) or set(subject) != {"type", "id"} or subject.get("type") != "person":
        errors.append("patch.subject is invalid")
    elif subject.get("id") != context.get("context_id"):
        errors.append("patch.subject.id does not match the Store")
    errors.extend(validate_entity(patch.get("principal"), "patch.principal"))
    for key in ("purpose", "source_task"):
        if not isinstance(patch.get(key), str) or not patch.get(key, "").strip():
            errors.append(f"patch.{key} must be a non-empty string")
    if type(patch.get("source_revision")) is not int or patch.get("source_revision", 0) < 1:
        errors.append("patch.source_revision must be a positive integer")
    try:
        parse_iso_utc(patch.get("created_at"), "patch.created_at")
    except StoreError as exc:
        errors.append(str(exc))
    if patch.get("status") != "pending":
        errors.append("patch.status must be 'pending' when staged")
    if not isinstance(patch.get("task_strategies_not_for_merge"), list) or not all(isinstance(value, str) for value in patch.get("task_strategies_not_for_merge", [])):
        errors.append("patch.task_strategies_not_for_merge must be an array of strings")
    proposals = patch.get("proposals")
    if not isinstance(proposals, list):
        errors.append("patch.proposals must be an array")
        return errors
    source_ids = {source.get("id") for source in context.get("sources", []) if isinstance(source, dict)}
    for index, proposal in enumerate(proposals):
        label = f"proposals[{index}]"
        if not isinstance(proposal, dict):
            errors.append(f"{label} must be an object")
            continue
        if set(proposal) != V04_PROPOSAL_FIELDS:
            errors.extend(f"{label}.{key} is not allowed" for key in sorted(set(proposal) - V04_PROPOSAL_FIELDS))
            errors.extend(f"{label}.{key} is required" for key in sorted(V04_PROPOSAL_FIELDS - set(proposal)))
        if proposal.get("action") not in PATCH_ACTIONS_V04:
            errors.append(f"{label}.action is invalid; schema 1.0.1 does not write promote/demote")
        target = proposal.get("target_claim_id")
        if target is not None and not is_safe_id(target):
            errors.append(f"{label}.target_claim_id is invalid")
        refs = proposal.get("evidence_refs")
        if not isinstance(refs, list) or not all(isinstance(value, str) and value.strip() for value in refs) or len(refs) != len(set(refs)):
            errors.append(f"{label}.evidence_refs must be an array of unique strings")
        if not isinstance(proposal.get("reason"), str) or not proposal.get("reason", "").strip():
            errors.append(f"{label}.reason must be a non-empty string")
        if proposal.get("user_decision") not in PATCH_DECISIONS:
            errors.append(f"{label}.user_decision is invalid")
        action = proposal.get("action")
        candidate = proposal.get("candidate_claim")
        if action == "add":
            if target is not None:
                errors.append(f"{label}.target_claim_id must be null for add")
            errors.extend(validate_v04_claim(candidate, f"{label}.candidate_claim"))
            if isinstance(candidate, dict) and candidate.get("id") in {value for value in all_v04_ids(context)}:
                errors.append(f"{label}.candidate_claim.id already exists; add cannot reuse a Claim or context ID")
        elif action == "update":
            if not is_safe_id(target):
                errors.append(f"{label}.target_claim_id is required for update")
            elif target not in {claim.get("id") for _, claim in iter_v04_claims(context) if isinstance(claim, dict)}:
                errors.append(f"{label}.target_claim_id does not identify an existing Claim")
            errors.extend(validate_v04_claim(candidate, f"{label}.candidate_claim"))
            if isinstance(candidate, dict) and candidate.get("id") != target:
                errors.append(f"{label}.candidate_claim.id must equal target_claim_id")
        elif action in {"challenge", "retire"}:
            if not is_safe_id(target):
                errors.append(f"{label}.target_claim_id is required for {action}")
            elif target not in {claim.get("id") for _, claim in iter_v04_claims(context) if isinstance(claim, dict)}:
                errors.append(f"{label}.target_claim_id does not identify an existing Claim")
            if candidate is not None:
                errors.append(f"{label}.candidate_claim must be null for {action}")
        for ref in refs if isinstance(refs, list) else []:
            if evidence_ref_source_id(ref) not in source_ids:
                errors.append(f"{label}.evidence_refs references unknown source {evidence_ref_source_id(ref)!r}")
    return errors


def command_init(args: argparse.Namespace) -> Dict[str, Any]:
    store = store_path_from_arg(args.store)
    context_id = args.context_id
    profile_id = args.profile_id
    if context_id and profile_id and context_id != profile_id:
        raise StoreError("--context-id and legacy --profile-id conflict; provide only one or the same value")
    context_id = context_id or profile_id
    if not context_id:
        raise StoreError("--context-id is required (legacy --profile-id is accepted as an alias)")
    validate_safe_id(context_id, "context_id")
    if context_path(store).exists():
        raise StoreError(f"Store already exists: {store}")
    ensure_store_dirs(store)
    context = empty_v04_context(context_id, args.preferred_name or "")
    transactional_commit(
        [
            (context_path(store), json_bytes(context)),
            (evidence_path(store), json_bytes({"schema_version": V04_SCHEMA_VERSION, "sources": []})),
        ],
        store_root=store,
    )
    return {"success": True, "store": str(store), "context_id": context_id, "profile_id": context_id, "schema_version": V04_SCHEMA_VERSION, "revision": 1}


def command_validate(args: argparse.Namespace) -> Dict[str, Any]:
    store = store_path_from_arg(args.store)
    context = load_context(store)
    errors, warnings = validate_context(context, store=store)
    if schema_version(context) == V04_SCHEMA_VERSION:
        errors.extend(validate_evidence_index_v04(store, context))
    return {"success": not errors, "store": str(store), "schema_version": schema_version(context), "context_id": context.get("context_id") if schema_version(context) == V04_SCHEMA_VERSION else None, "profile_id": context.get("profile_id") if schema_version(context) != V04_SCHEMA_VERSION else context.get("context_id"), "revision": context.get("revision", {}).get("version"), "errors": errors, "warnings": warnings}


def command_register_source(args: argparse.Namespace) -> Dict[str, Any]:
    store = store_path_from_arg(args.store)
    context = load_context(store)
    require_v04(context, "register-source")
    if not args.approve or not args.confirmed_by:
        raise StoreError("register-source requires --approve and --confirmed-by after explicit user review")
    validate_store_for_command(store, context, "register-source")
    source = read_json(Path(args.source).resolve())
    errors, warnings = validate_source(source)
    if errors:
        raise StoreError("Invalid source: " + "; ".join(errors))
    source_id = validate_safe_id(source.get("id"), "source.id")
    if source_id in {item.get("id") for item in context.get("sources", []) if isinstance(item, dict)}:
        raise StoreError(f"Source already exists in context: {source_id}")
    evidence = read_json(evidence_path(store))
    if source_id in {item.get("id") for item in evidence.get("sources", []) if isinstance(item, dict)}:
        raise StoreError(f"Source already exists in evidence index: {source_id}")
    current = context["revision"]["version"]
    timestamp = now_utc()
    updated = copy.deepcopy(context)
    updated["sources"].append(copy.deepcopy(source))
    updated["revision"] = {**updated["revision"], "version": current + 1, "updated_at": timestamp, "last_reviewed_at": timestamp}
    validation_errors, validation_warnings = validate_v04_context(updated)
    if validation_errors:
        raise StoreError("Resulting context is invalid: " + "; ".join(validation_errors))
    new_evidence = {"schema_version": V04_SCHEMA_VERSION, "sources": copy.deepcopy(updated["sources"])}
    history_path = store / "history" / f"context-v{current}.json"
    if history_path.exists():
        raise StoreError(f"History snapshot already exists: {history_path}")
    audit_path = store / "history" / "changes.jsonl"
    audit_existing = _read_limited_bytes(audit_path, label=f"audit log {audit_path}") if audit_path.exists() else b""
    audit_record = {"timestamp": timestamp, "operation": "register-source", "source_id": source_id, "confirmed_by": args.confirmed_by, "from_revision": current, "to_revision": current + 1}
    transactional_commit(
        [
            (history_path, json_bytes(context)),
            (evidence_path(store), json_bytes(new_evidence)),
            (context_path(store), json_bytes(updated)),
            (audit_path, append_jsonl_bytes(audit_existing, audit_record)),
        ],
        store_root=store,
    )
    return {"success": True, "source_id": source_id, "from_revision": current, "to_revision": current + 1, "warnings": warnings + validation_warnings}


def iter_claims_for_inspect(context: Dict[str, Any]) -> Iterable[Tuple[str, Dict[str, Any], Optional[str]]]:
    if schema_version(context) == V04_SCHEMA_VERSION:
        for label, claim in iter_v04_claims(context):
            yield label, claim, None
    else:
        for label, claim, layer, domain in iter_v03_claims(context):
            yield label, claim, domain if layer == "domain" else None


def derive_core_summary(context: Dict[str, Any]) -> List[Dict[str, Any]]:
    if schema_version(context) != V04_SCHEMA_VERSION:
        raise StoreError("derive-core-summary requires schema 1.0.1; legacy Stores remain limited to validate/inspect and explicit migration preview")
    return [copy.deepcopy(claim) for _, claim in iter_v04_claims(context) if claim.get("user_status") == "confirmed" and claim.get("status") == "active" and claim.get("scope") == "cross-context" and claim.get("durability") in {"stable", "evolving"} and claim.get("kind") != "inference"]


def command_derive_core_summary(args: argparse.Namespace) -> Dict[str, Any]:
    store = store_path_from_arg(args.store)
    context = load_context(store)
    if schema_version(context) != V04_SCHEMA_VERSION:
        raise StoreError("derive-core-summary requires schema 1.0.1; legacy Stores remain limited to validate/inspect and explicit migration preview")
    errors, warnings = validate_context(context, store=store)
    if schema_version(context) == V04_SCHEMA_VERSION:
        errors.extend(validate_evidence_index_v04(store, context))
    if errors:
        raise StoreError("Store is invalid: " + "; ".join(errors))
    summary = derive_core_summary(context)
    return {"success": True, "schema_version": schema_version(context), "revision": context.get("revision", {}).get("version"), "claims": summary, "claim_ids": [item["id"] for item in summary], "warnings": warnings}


def filter_v04_context(context: Dict[str, Any], sensitivities: set[str]) -> Dict[str, Any]:
    exported = copy.deepcopy(context)
    for key in ("claims", "tensions", "unknowns", "sources"):
        exported[key] = [item for item in exported.get(key, []) if isinstance(item, dict) and item.get("sensitivity") in sensitivities]
    source_ids = {item.get("id") for item in exported["sources"] if isinstance(item, dict)}
    for claim in exported["claims"]:
        for key in ("evidence_refs", "counterevidence_refs"):
            claim[key] = [ref for ref in claim.get(key, []) if evidence_ref_source_id(ref) in source_ids]
    for item in exported["tensions"] + exported["unknowns"]:
        item["evidence_refs"] = [ref for ref in item.get("evidence_refs", []) if evidence_ref_source_id(ref) in source_ids]
    return exported


def filter_v03_context(context: Dict[str, Any], sensitivities: set[str]) -> Dict[str, Any]:
    exported = copy.deepcopy(context)
    exported.setdefault("core", {})["claims"] = [claim for claim in exported["core"].get("claims", []) if claim.get("sensitivity") in sensitivities]
    for key in ("tensions", "unknowns"):
        exported["core"][key] = [item for item in exported["core"].get(key, []) if item.get("sensitivity", "private") in sensitivities]
    for section in exported.get("domains", {}).values():
        section["claims"] = [claim for claim in section.get("claims", []) if claim.get("sensitivity") in sensitivities]
        for key in ("tensions", "unknowns"):
            section[key] = [item for item in section.get(key, []) if item.get("sensitivity", "private") in sensitivities]
    exported["sources"] = [source for source in exported.get("sources", []) if source.get("sensitivity") in sensitivities]
    source_ids = {source.get("id") for source in exported["sources"]}
    for _, claim, _, _ in iter_v03_claims(exported):
        for key in ("evidence_refs", "counterevidence_refs"):
            claim[key] = [ref for ref in claim.get(key, []) if evidence_ref_source_id(ref) in source_ids]
    return exported


def render_human_brief(context: Dict[str, Any]) -> str:
    version = schema_version(context)
    identity = context.get("context_id") if version == V04_SCHEMA_VERSION else context.get("profile_id")
    lines = ["# Brief Yourself Export", "", f"- Context ID: `{identity or ''}`", f"- Schema: `{version or ''}`", f"- Revision: `{context.get('revision', {}).get('version', '')}`", f"- Exported at: `{now_utc()}`", "", "## Claims", ""]
    claims = list(iter_v04_claims(context)) if version == V04_SCHEMA_VERSION else [(label, claim) for label, claim, _, _ in iter_v03_claims(context)]
    if claims:
        for _, claim in claims:
            domains = ", ".join(claim.get("domains", [])) if version == V04_SCHEMA_VERSION else (claim.get("domain") or "")
            lines.append(f"- [{claim.get('id')}] [status={claim.get('status', '')}; user_status={claim.get('user_status', '')}; sensitivity={claim.get('sensitivity', '')}] ({domains}) {claim.get('statement', '')}")
    else:
        lines.append("- （无）")
    lines.extend(["", "## Sources", ""])
    sources = context.get("sources", [])
    lines.extend(f"- [{source.get('id')}] {source.get('title', '')}" for source in sources)
    if not sources:
        lines.append("- （无）")
    return "\n".join(lines) + "\n"


def command_export(args: argparse.Namespace) -> Dict[str, Any]:
    store = store_path_from_arg(args.store)
    context = load_context(store)
    require_v04(context, "export")
    errors, warnings = validate_context(context, store=store)
    errors.extend(validate_evidence_index_v04(store, context))
    if errors:
        raise StoreError("Store is invalid: " + "; ".join(errors))
    sensitivities = {"public"}
    if args.include_private:
        sensitivities.add("private")
    if args.include_restricted:
        sensitivities.add("restricted")
    exported = filter_v04_context(context, sensitivities)
    output = Path(args.output).expanduser()
    validate_external_output_path(output, store)
    if args.format == "json":
        _assert_output_path_safe(output)
        atomic_write_json(output, exported)
    else:
        _assert_output_path_safe(output)
        atomic_write_bytes(output, render_human_brief(exported).encode("utf-8"))
    return {"success": True, "output": str(output), "format": args.format, "included_sensitivity": sorted(sensitivities), "warnings": warnings}


def command_inspect(args: argparse.Namespace) -> Dict[str, Any]:
    store = store_path_from_arg(args.store)
    context = load_context(store)
    errors, warnings = validate_context(context, store=store)
    if schema_version(context) == V04_SCHEMA_VERSION:
        errors.extend(validate_evidence_index_v04(store, context))
    claims = list(iter_claims_for_inspect(context))
    version = schema_version(context)
    result: Dict[str, Any] = {"success": not errors, "store": str(store), "schema_version": version, "context_id": context.get("context_id") if version == V04_SCHEMA_VERSION else None, "profile_id": context.get("profile_id") if version != V04_SCHEMA_VERSION else context.get("context_id"), "revision": context.get("revision", {}).get("version"), "counts": {"claims": len(claims), "active_claims": sum(1 for _, claim, _ in claims if claim.get("status") == "active"), "sources": len(context.get("sources", [])), "views": len(list((store / "views").glob("*.json"))) if (store / "views").exists() else 0, "pending_patches": len(list((store / "patches" / "pending").glob("*.json"))) if (store / "patches" / "pending").exists() else 0}, "claim_ids": sorted(claim.get("id") for _, claim, _ in claims if isinstance(claim.get("id"), str)), "source_ids": sorted(source.get("id") for source in context.get("sources", []) if isinstance(source, dict) and isinstance(source.get("id"), str)), "pending_patch_ids": sorted(path.stem for path in (store / "patches" / "pending").glob("*.json")) if (store / "patches" / "pending").exists() else [], "errors": errors, "warnings": warnings}
    if version == V04_SCHEMA_VERSION:
        result["core_summary_ids"] = [item["id"] for item in derive_core_summary(context)]
    if args.claim_id:
        claim_id = validate_safe_id(args.claim_id, "claim_id")
        if version == V04_SCHEMA_VERSION:
            _, _, claim = find_v04_claim(context, claim_id)
            result["claim"] = {"value": claim}
        else:
            _, _, claim, layer, domain = find_v03_claim(context, claim_id)
            result["claim"] = {"layer": layer, "domain": domain, "value": claim}
    return result


def migrate_context_v02(context: Dict[str, Any]) -> Dict[str, Any]:
    migrated = copy.deepcopy(context)
    migrated["schema_version"] = V03_SCHEMA_VERSION
    migrated.setdefault("policy", {})["default_view_ttl_days"] = DEFAULT_VIEW_TTL_DAYS
    for _, section in iter_v03_sections(migrated):
        for key in ("tensions", "unknowns"):
            for item in section.get(key, []):
                if isinstance(item, dict):
                    item.setdefault("sensitivity", "private")
                    item.setdefault("user_status", "unreviewed")
                    item.setdefault("status", "active")
                    item.setdefault("evidence_refs", [])
    known_sources = {source.get("id") for source in migrated.get("sources", []) if isinstance(source, dict) and isinstance(source.get("id"), str)}
    bindings = sorted(
        {
            (item_type, item_id, ref)
            for _label, ref, item_id, item_type in iter_v03_evidence_refs(migrated)
            if isinstance(item_id, str) and evidence_ref_source_id(ref) not in known_sources
        }
    )
    unresolved = sorted({evidence_ref_source_id(ref) for _item_type, _item_id, ref in bindings})
    migrated["migration"] = {
        "from_schema": V02_SCHEMA_VERSION,
        "unresolved_evidence_source_ids": unresolved,
        "unresolved_evidence_bindings": [
            {"item_type": item_type, "item_id": item_id, "ref": ref}
            for item_type, item_id, ref in bindings
        ],
    }
    return migrated


def command_migrate_v02(args: argparse.Namespace) -> Dict[str, Any]:
    if not args.approve or not args.confirmed_by:
        raise StoreError("migrate-v02 requires --approve and --confirmed-by after explicit review")
    store = store_path_from_arg(args.store)
    context = load_context(store)
    if schema_version(context) != V02_SCHEMA_VERSION:
        raise StoreError("migrate-v02 only accepts a v0.2 Store and never chains to v0.4")
    current = context.get("revision", {}).get("version")
    if type(current) is not int:
        raise StoreError("revision.version must be an integer")
    migrated = migrate_context_v02(context)
    timestamp = now_utc()
    migrated["migration"]["migrated_at"] = timestamp
    migrated["migration"]["confirmed_by"] = args.confirmed_by
    migrated["revision"]["version"] = current + 1
    migrated["revision"]["updated_at"] = timestamp
    errors, warnings = validate_v03_context(migrated)
    if errors:
        raise StoreError("Migrated context is invalid: " + "; ".join(errors))
    ensure_store_dirs(store)
    backup_path = store / "history" / f"context-v{current}-schema-v0.2.json"
    if backup_path.exists():
        raise StoreError(f"Migration backup already exists: {backup_path}")
    old_evidence_path = evidence_path(store)
    old_evidence = read_json(old_evidence_path) if old_evidence_path.exists() else {"schema_version": V02_SCHEMA_VERSION, "sources": []}
    if old_evidence.get("schema_version") != V02_SCHEMA_VERSION or old_evidence.get("sources") != context.get("sources"):
        raise StoreError("V0.2 evidence/index.json must have schema 0.2 and exactly match context.sources before migration")
    evidence_backup_path = store / "history" / f"evidence-index-v{current}-schema-v0.2.json"
    if evidence_backup_path.exists():
        raise StoreError(f"Migration evidence backup already exists: {evidence_backup_path}")
    new_evidence = {"schema_version": V03_SCHEMA_VERSION, "sources": copy.deepcopy(migrated.get("sources", []))}
    audit_path = store / "history" / "changes.jsonl"
    audit_existing = _read_limited_bytes(audit_path, label=f"audit log {audit_path}") if audit_path.exists() else b""
    audit_record = {"timestamp": timestamp, "operation": "migrate-v02", "confirmed_by": args.confirmed_by, "from_schema": V02_SCHEMA_VERSION, "to_schema": V03_SCHEMA_VERSION, "from_revision": current, "to_revision": current + 1}
    transactional_commit(
        [
            (backup_path, json_bytes(context)),
            (evidence_backup_path, json_bytes(old_evidence)),
            (context_path(store), json_bytes(migrated)),
            (old_evidence_path, json_bytes(new_evidence)),
            (audit_path, append_jsonl_bytes(audit_existing, audit_record)),
        ],
        store_root=store,
    )
    return {"success": True, "from_revision": current, "to_revision": current + 1, "backup": str(backup_path), "warnings": warnings}


def validate_external_output_path(output: Path, store: Path) -> None:
    """Reject Store-internal paths and aliases to any controlled Store file."""

    store_resolved = store.resolve(strict=False)
    output_lexical = Path(os.path.abspath(str(output)))
    output_resolved = output_lexical.resolve(strict=False)
    if inside_store(output_resolved, store_resolved):
        raise StoreError("View output must be outside the input Store; use --archive-in-personal-store for Store archive")
    _assert_output_path_safe(output)
    if output_lexical.exists() or output_lexical.is_symlink():
        for controlled in controlled_store_files(store):
            try:
                if os.path.samefile(output_lexical, controlled):
                    raise StoreError("View output must not alias a controlled Store file")
            except FileNotFoundError:
                continue
            except OSError:
                continue


def command_create_view(args: argparse.Namespace) -> Dict[str, Any]:
    store = store_path_from_arg(args.store)
    context = load_context(store)
    validate_store_for_command(store, context, "create-view")
    purpose = args.purpose
    principal = principal_from_args(args)
    audience = audience_from_args(args, principal)
    sensitivities = {"public"}
    if args.include_private:
        sensitivities.add("private")
    if args.include_restricted:
        sensitivities.add("restricted")
    claim_index = {claim.get("id"): claim for _, claim in iter_v04_claims(context) if isinstance(claim.get("id"), str)}
    item_index = {key: {item.get("id"): item for _, item in iter_v04_items(context, key) if isinstance(item.get("id"), str)} for key in ("tensions", "unknowns")}
    audience_ids = [entity["id"] for entity in audience]
    include_unreviewed = bool(getattr(args, "include_unreviewed", False))
    claim_predicate = lambda claim: claim_allowed_v04(claim, sensitivities, principal["id"], purpose, args.purpose_approved, audience_ids, include_unreviewed=include_unreviewed)
    selected = select_v04_items(claim_index, args.claim_ids or [], "claim", claim_predicate)
    item_predicate = lambda item: item_allowed_v04(item, sensitivities, principal["id"], purpose, args.purpose_approved, audience_ids, include_unreviewed=include_unreviewed)
    tensions = select_v04_items(item_index["tensions"], args.tension_ids or [], "tension", item_predicate)
    unknowns = select_v04_items(item_index["unknowns"], args.unknown_ids or [], "unknown", item_predicate)
    warnings: List[str] = []
    selected_ids = {item["id"] for item in selected}
    if args.include_core or args.domains:
        warnings.append("broad layer/domain selection is retained for compatibility; prefer explicit item IDs")
        for _, claim in iter_v04_claims(context):
            if (args.include_core or set(claim.get("domains", [])) & set(args.domains or [])) and claim.get("id") not in selected_ids and claim_predicate(claim):
                selected.append(copy.deepcopy(claim))
                selected_ids.add(claim["id"])
        for key, destination in (("tensions", tensions), ("unknowns", unknowns)):
            for _, item in iter_v04_items(context, key):
                if (args.include_core or set(item.get("domains", [])) & set(args.domains or [])) and item.get("id") not in selected_ids and item_predicate(item):
                    destination.append(copy.deepcopy(item))
                    selected_ids.add(item["id"])
    view_id = validate_safe_id(args.view_id or f"view-{uuid.uuid4().hex[:12]}", "view_id")
    created = datetime.now(timezone.utc).replace(microsecond=0)
    if args.expires_at:
        expires = parse_iso_utc(args.expires_at, "expires_at")
        if expires is None or expires <= created:
            raise StoreError("expires_at must be in the future")
    else:
        ttl_days = args.ttl_days if args.ttl_days is not None else context["policy"]["default_view_ttl_days"]
        if type(ttl_days) is not int or ttl_days < 1:
            raise StoreError("TTL days must be a positive integer")
        expires = created + timedelta(days=ttl_days)
    allow_downstream = bool(args.allow_downstream_persistence or args.allow_persistence)
    if allow_downstream and any(
        not isinstance(item.get("disclosure"), dict) or item["disclosure"].get("allow_downstream_persistence") is not True
        for item in [*selected, *tensions, *unknowns]
    ):
        raise StoreError("View cannot allow downstream persistence because a selected item disclosure forbids it")
    view = {"schema_version": V04_SCHEMA_VERSION, "view_id": view_id, "subject": {"type": "person", "id": context["context_id"]}, "principal": principal, "audience": audience, "purpose": purpose, "task": args.task, "source_revision": context["revision"]["version"], "created_at": format_utc(created), "expires_at": format_utc(expires), "claims": selected, "tensions": tensions, "relevant_unknowns": unknowns, "exclusions": [], "permission": {"allowed_use": args.allowed_use or "current task only", "archive_in_personal_store": bool(args.archive_in_personal_store), "allow_downstream_persistence": allow_downstream}}
    errors, view_warnings = validate_v04_view(view, context, purpose_approved=args.purpose_approved, include_unreviewed=include_unreviewed)
    if errors:
        raise StoreError("Generated View is invalid: " + "; ".join(errors))
    output = Path(args.output).expanduser()
    archive_path: Optional[Path] = None
    if args.archive_in_personal_store:
        archive_path = store / "views" / f"{view_id}.json"
        if archive_path.exists():
            raise StoreError(f"Archived View already exists: {view_id}")
    validate_external_output_path(output, store)
    _assert_output_path_safe(output)
    atomic_write_json(output, view)
    if archive_path is not None:
        _assert_store_path_safe(store, archive_path, label="View archive path")
        atomic_write_json(archive_path, view, store_root=store)
    return {"success": True, "view_id": view_id, "output": str(output), "archived_at": str(archive_path) if archive_path else None, "claim_count": len(selected), "warnings": warnings + view_warnings}


def command_validate_view(args: argparse.Namespace) -> Dict[str, Any]:
    view_path = Path(args.view).resolve()
    view = read_json(view_path)
    context = load_context(store_path_from_arg(args.store)) if args.store else None
    errors, warnings = validate_view_data(view, context, purpose_approved=bool(args.purpose_approved), include_unreviewed=bool(getattr(args, "include_unreviewed", False)))
    for key, expected in (("purpose", args.purpose), ("task", args.task)):
        if expected is not None and view.get(key) != expected:
            errors.append(f"view.{key} does not match expected value")
    if args.principal_id is not None and view.get("principal", {}).get("id") != args.principal_id:
        errors.append("view.principal.id does not match expected value")
    if args.allowed_use is not None and view.get("permission", {}).get("allowed_use") != args.allowed_use:
        errors.append("view.permission.allowed_use does not match expected value")
    if args.require_downstream_persistence and not view.get("permission", {}).get("allow_downstream_persistence", False):
        errors.append("view does not allow downstream persistence")
    return {"success": not errors, "view": str(view_path), "view_id": view.get("view_id"), "errors": errors, "warnings": warnings}


def command_stage_patch(args: argparse.Namespace) -> Dict[str, Any]:
    store = store_path_from_arg(args.store)
    context = load_context(store)
    validate_store_for_command(store, context, "stage-patch")
    patch = read_json(Path(args.patch).resolve())
    errors = validate_v04_patch(patch, context)
    if errors:
        raise StoreError("Invalid patch: " + "; ".join(errors))
    if patch["source_revision"] != context["revision"]["version"]:
        raise StoreError("Patch source_revision is stale; rebuild it against the current Store")
    patch_id = validate_safe_id(patch["patch_id"], "patch_id")
    destinations = [store / "patches" / status / f"{patch_id}.json" for status in ("pending", "applied", "rejected")]
    if any(path.exists() for path in destinations):
        raise StoreError(f"Patch ID has already been staged, applied, or rejected: {patch_id}")
    destination = destinations[0]
    _assert_store_path_safe(store, destination, label="Patch destination")
    atomic_write_json(destination, patch, store_root=store)
    return {"success": True, "patch_id": patch_id, "staged_at": str(destination), "context_changed": False}


def apply_v04_proposal(context: Dict[str, Any], proposal: Dict[str, Any]) -> str:
    action = proposal["action"]
    target_id = proposal.get("target_claim_id")
    if action == "add":
        candidate = copy.deepcopy(proposal["candidate_claim"])
        if candidate["id"] in all_v04_ids(context):
            raise StoreError(f"Claim id already exists: {candidate['id']}")
        context["claims"].append(candidate)
        return f"add:{candidate['id']}"
    claims, index, existing = find_v04_claim(context, target_id)
    if action == "update":
        candidate = copy.deepcopy(proposal["candidate_claim"])
        if candidate["id"] != target_id:
            raise StoreError("Updated candidate_claim.id must match target_claim_id")
        claims[index] = candidate
        return f"update:{target_id}"
    if action == "challenge":
        existing["status"] = "challenged"
        return f"challenge:{target_id}"
    if action == "retire":
        existing["status"] = "retired"
        return f"retire:{target_id}"
    raise StoreError(f"Unsupported schema 1.0.1 action: {action}")


def confirmed_actor(args: argparse.Namespace) -> str:
    actor = getattr(args, "confirmed_by", None) or getattr(args, "actor", None) or getattr(args, "confirmed_actor", None)
    if not isinstance(actor, str) or not actor.strip():
        raise StoreError("an explicit confirmed actor is required (--confirmed-by)")
    return actor.strip()


def command_apply_patch(args: argparse.Namespace) -> Dict[str, Any]:
    store = store_path_from_arg(args.store)
    context = load_context(store)
    require_v04(context, "apply-patch")
    if not args.approve:
        raise StoreError("Refusing to apply without --approve after explicit user review")
    actor = confirmed_actor(args)
    validate_store_for_command(store, context, "apply-patch")
    patch_id = validate_safe_id(args.patch_id, "patch_id")
    pending_path = store / "patches" / "pending" / f"{patch_id}.json"
    patch = read_json(pending_path)
    if patch.get("patch_id") != patch_id:
        raise StoreError("Pending Patch filename does not match its internal patch_id")
    errors = validate_v04_patch(patch, context)
    if errors:
        raise StoreError("Invalid patch: " + "; ".join(errors))
    current = context["revision"]["version"]
    if patch["source_revision"] != current:
        raise StoreError("Patch source_revision conflicts with the current context")
    if any(proposal.get("user_decision") == "pending" for proposal in patch["proposals"]):
        raise StoreError("Every proposal must be reviewed before apply")
    updated = copy.deepcopy(context)
    applied_actions: List[str] = []
    for proposal in patch["proposals"]:
        decision = proposal.get("user_decision")
        if decision in {"rejected", "unresolved"}:
            continue
        if decision not in {"confirmed", "corrected"}:
            raise StoreError(f"Unsupported user_decision: {decision}")
        applied_actions.append(apply_v04_proposal(updated, proposal))
    timestamp = now_utc()
    updated["revision"] = {**updated["revision"], "version": current + 1, "updated_at": timestamp, "last_reviewed_at": timestamp}
    validation_errors, validation_warnings = validate_v04_context(updated)
    validation_errors.extend(validate_evidence_index_v04(store, updated))
    if validation_errors:
        raise StoreError("Resulting context is invalid: " + "; ".join(validation_errors))
    history_path = store / "history" / f"context-v{current}.json"
    if history_path.exists():
        raise StoreError(f"History snapshot already exists: {history_path}")
    applied = copy.deepcopy(patch)
    applied["status"] = "applied"
    applied["applied_at"] = timestamp
    applied["confirmed_by"] = actor
    applied_path = store / "patches" / "applied" / f"{patch_id}.json"
    if applied_path.exists():
        raise StoreError(f"Applied Patch already exists: {patch_id}")
    audit_path = store / "history" / "changes.jsonl"
    audit_existing = _read_limited_bytes(audit_path, label=f"audit log {audit_path}") if audit_path.exists() else b""
    audit_record = {"timestamp": timestamp, "patch_id": patch_id, "confirmed_by": actor, "from_revision": current, "to_revision": current + 1, "applied_actions": applied_actions, "warnings": validation_warnings}
    transactional_commit(
        [
            (history_path, json_bytes(context)),
            (context_path(store), json_bytes(updated)),
            (audit_path, append_jsonl_bytes(audit_existing, audit_record)),
            (applied_path, json_bytes(applied)),
        ],
        store_root=store,
    )
    cleanup_warnings: List[str] = []
    try:
        _assert_store_path_safe(store, pending_path, label="pending Patch cleanup path")
        pending_path.unlink()
    except OSError as exc:
        cleanup_warnings.append(f"apply succeeded but failed to remove pending patch file (non-fatal): {exc}")
    return {"success": True, "patch_id": patch_id, "from_revision": current, "to_revision": current + 1, "applied_actions": applied_actions, "warnings": validation_warnings + cleanup_warnings}


def command_reject_patch(args: argparse.Namespace) -> Dict[str, Any]:
    store = store_path_from_arg(args.store)
    context = load_context(store)
    require_v04(context, "reject-patch")
    actor = confirmed_actor(args)
    if not isinstance(args.reason, str) or not args.reason.strip():
        raise StoreError("reject-patch requires a non-empty --reason")
    validate_store_for_command(store, context, "reject-patch")
    patch_id = validate_safe_id(args.patch_id, "patch_id")
    pending_path = store / "patches" / "pending" / f"{patch_id}.json"
    patch = read_json(pending_path)
    if patch.get("patch_id") != patch_id:
        raise StoreError("Pending Patch filename does not match its internal patch_id")
    errors = validate_v04_patch(patch, context)
    if errors:
        raise StoreError("Invalid patch: " + "; ".join(errors))
    timestamp = now_utc()
    rejected = copy.deepcopy(patch)
    rejected["status"] = "rejected"
    rejected["rejected_at"] = timestamp
    rejected["confirmed_by"] = actor
    rejected["rejection_reason"] = args.reason.strip()
    for proposal in rejected.get("proposals", []):
        if isinstance(proposal, dict):
            proposal["user_decision"] = "rejected"
    rejected_path = store / "patches" / "rejected" / f"{patch_id}.json"
    if rejected_path.exists():
        raise StoreError(f"Rejected Patch already exists: {patch_id}")
    audit_path = store / "history" / "changes.jsonl"
    audit_existing = _read_limited_bytes(audit_path, label=f"audit log {audit_path}") if audit_path.exists() else b""
    audit_record = {"timestamp": timestamp, "operation": "reject-patch", "patch_id": patch_id, "confirmed_by": actor, "reason": args.reason.strip(), "context_revision": context["revision"]["version"]}
    transactional_commit(
        [
            (rejected_path, json_bytes(rejected)),
            (audit_path, append_jsonl_bytes(audit_existing, audit_record)),
        ],
        store_root=store,
    )
    cleanup_warnings: List[str] = []
    try:
        _assert_store_path_safe(store, pending_path, label="pending Patch cleanup path")
        pending_path.unlink()
    except OSError as exc:
        cleanup_warnings.append(f"reject succeeded but failed to remove pending patch file (non-fatal): {exc}")
    return {"success": True, "patch_id": patch_id, "rejected_at": str(rejected_path), "context_changed": False, "warnings": cleanup_warnings}


def command_list_patches(args: argparse.Namespace) -> Dict[str, Any]:
    store = store_path_from_arg(args.store)
    context = load_context(store)
    require_v04(context, "list-patches")
    result: Dict[str, List[str]] = {}
    for status in ("pending", "applied", "rejected"):
        folder = store / "patches" / status
        result[status] = sorted(path.stem for path in folder.glob("*.json")) if folder.exists() else []
    return {"success": True, "patches": result}


def purge_target_from_args(args: argparse.Namespace) -> Tuple[str, str]:
    provided = [(kind, getattr(args, f"{kind}_id", None)) for kind in sorted(PURGE_KINDS) if getattr(args, f"{kind}_id", None)]
    if len(provided) != 1:
        raise StoreError("Provide exactly one of --claim-id, --source-id, --view-id, or --patch-id")
    kind, target_id = provided[0]
    return kind, validate_safe_id(target_id, f"{kind}_id")


def purge_string_matches(value: str, kind: str, target_id: str) -> bool:
    if value == target_id:
        return True
    if kind == "source" and value.startswith(target_id + "#"):
        return True
    if kind == "claim" and (value.endswith(":" + target_id) or value.endswith("->" + target_id)):
        return True
    return False


def scrub_node(node: Any, kind: str, target_id: str) -> Tuple[Any, int, bool]:
    return _scrub_node(node, kind, target_id, depth=0)


def _scrub_node(node: Any, kind: str, target_id: str, *, depth: int) -> Tuple[Any, int, bool]:
    if depth > MAX_PURGE_DEPTH:
        raise ResourceLimitError(f"Purge document exceeds the {MAX_PURGE_DEPTH}-level recursion limit")
    if isinstance(node, dict):
        identity_match = ((kind in {"claim", "source"} and node.get("id") == target_id) or (kind == "view" and node.get("view_id") == target_id) or (kind == "patch" and node.get("patch_id") == target_id) or (kind == "claim" and node.get("target_claim_id") == target_id) or (kind == "claim" and isinstance(node.get("candidate_claim"), dict) and node["candidate_claim"].get("id") == target_id))
        if identity_match:
            return None, 1, True
        cleaned: Dict[str, Any] = {}
        removed = 0
        for key, value in node.items():
            new_value, count, remove = _scrub_node(value, kind, target_id, depth=depth + 1)
            removed += count
            if not remove:
                cleaned[key] = new_value
        return cleaned, removed, False
    if isinstance(node, list):
        cleaned_list: List[Any] = []
        removed = 0
        for value in node:
            new_value, count, remove = _scrub_node(value, kind, target_id, depth=depth + 1)
            removed += count
            if not remove:
                cleaned_list.append(new_value)
        return cleaned_list, removed, False
    if isinstance(node, str) and purge_string_matches(node, kind, target_id):
        return None, 1, True
    return node, 0, False


def controlled_store_files(store: Path) -> List[Path]:
    _assert_store_tree_safe(store)
    candidates: set[Path] = set()
    for path in (context_path(store), evidence_path(store), store / "history" / "changes.jsonl", store / "brief.md"):
        if path.exists():
            candidates.add(path)
    for relative in ("views", "patches", "history"):
        root = store / relative
        if root.exists():
            candidates.update(path for path in root.rglob("*") if path.is_file() and path.suffix in {".json", ".jsonl"})
    return sorted(candidates, key=lambda path: str(path).lower())


def verify_controlled_manifest(store: Path, expected_manifest: Sequence[Dict[str, str]]) -> None:
    """Fail closed when any controlled path or byte hash differs from a plan."""

    expected = {entry.get("path"): entry.get("sha256") for entry in expected_manifest}
    actual = {entry["path"]: entry["sha256"] for entry in controlled_store_manifest(store)}
    if actual != expected:
        raise StoreError("Controlled Store manifest changed since purge review; aborting without commit")


def controlled_store_state_map(
    store: Path,
    extra_paths: Sequence[Path] = (),
) -> Dict[str, Optional[Tuple[str, int, int, int, int]]]:
    paths = set(controlled_store_files(store))
    paths.update(extra_paths)
    result: Dict[str, Optional[Tuple[str, int, int, int, int]]] = {}
    for path in paths:
        try:
            relative = path.relative_to(store).as_posix()
        except ValueError as exc:
            raise StoreError(f"Transaction target is outside Store: {path}") from exc
        result[relative] = _file_state(path)
    return result


def verify_controlled_state_map(
    store: Path,
    expected_states: Dict[str, Optional[Tuple[str, int, int, int, int]]],
) -> None:
    actual = controlled_store_state_map(
        store,
        [store / relative for relative in expected_states],
    )
    if actual != expected_states:
        raise StoreError("Controlled Store changed during purge commit; aborting without overwriting concurrent changes")


def controlled_store_manifest(store: Path) -> List[Dict[str, str]]:
    return [
        {"path": path.relative_to(store).as_posix(), "sha256": hashlib.sha256(_read_limited_bytes(path, label=f"controlled Store file {path}")).hexdigest()}
        for path in controlled_store_files(store)
    ]


def build_purge_plan(store: Path, kind: str, target_id: str) -> Dict[str, Any]:
    operations: List[Dict[str, Any]] = []
    canonical_context = read_json(context_path(store))
    _, canonical_matches, _ = scrub_node(canonical_context, kind, target_id)
    canonical_will_change = canonical_matches > 0
    claim_statement: Optional[str] = None
    if kind == "claim":
        for _label, claim in iter_v04_claims(canonical_context):
            if isinstance(claim, dict) and claim.get("id") == target_id and isinstance(claim.get("statement"), str):
                claim_statement = claim["statement"]
                break
    for path in controlled_store_files(store):
        relative = path.relative_to(store).as_posix()
        file_hash = hashlib.sha256(_read_limited_bytes(path, label=f"controlled Store file {path}")).hexdigest()
        if path == store / "brief.md":
            brief_text = _read_limited_bytes(path, label=f"controlled Store file {path}").decode("utf-8")
            brief_mentions_target = target_id in brief_text or (claim_statement is not None and claim_statement in brief_text)
            if canonical_will_change or brief_mentions_target:
                operations.append({"path": relative, "action": "rewrite-derived-brief", "matches": 1, "sha256": file_hash})
        elif path.suffix == ".json":
            data = read_json(path)
            _, removed, remove_document = scrub_node(data, kind, target_id)
            if removed:
                operations.append({"path": relative, "action": "delete" if remove_document else "rewrite", "matches": removed, "sha256": file_hash})
        elif path.suffix == ".jsonl":
            removed_lines = 0
            for raw_line in _read_limited_bytes(path, label=f"controlled Store file {path}").decode("utf-8").splitlines():
                if not raw_line.strip():
                    continue
                record = json.loads(raw_line)
                _, removed, remove_record = scrub_node(record, kind, target_id)
                if removed or remove_record:
                    removed_lines += 1
            if removed_lines:
                operations.append({"path": relative, "action": "rewrite-jsonl", "matches": removed_lines, "sha256": file_hash})
    manifest = controlled_store_manifest(store)
    token_payload = {"kind": kind, "target_id": target_id, "manifest": manifest, "operations": operations}
    token = hashlib.sha256(json.dumps(token_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    return {"success": True, "dry_run": True, "store": str(store), "target": {"kind": kind, "id": target_id}, "controlled_manifest": manifest, "operations": operations, "plan_token": token, "external_uncontrolled_copies": ["原始来源系统中的材料或记录", "Store 之外已导出的 View、JSON、Markdown 或下游副本", "无法仅凭 ID 可靠定位的语义改写或手工复制内容"]}


def command_purge_plan(args: argparse.Namespace) -> Dict[str, Any]:
    store = store_path_from_arg(args.store)
    context = load_context(store)
    validate_store_for_command(store, context, "purge-plan")
    kind, target_id = purge_target_from_args(args)
    return build_purge_plan(store, kind, target_id)


def command_purge(args: argparse.Namespace) -> Dict[str, Any]:
    store = store_path_from_arg(args.store)
    context = load_context(store)
    require_v04(context, "purge")
    if not args.approve:
        raise StoreError("purge requires --approve and --confirmed-by after explicit user review")
    actor = confirmed_actor(args)
    if not args.plan_token:
        raise StoreError("purge requires --plan-token from the immediately preceding purge-plan")
    validate_store_for_command(store, context, "purge")
    kind, target_id = purge_target_from_args(args)
    plan = build_purge_plan(store, kind, target_id)
    if plan["plan_token"] != args.plan_token:
        raise StoreError("Purge plan token does not match current Store state; run purge-plan again")
    if not plan["operations"]:
        raise StoreError("Purge target was not found in the controllable Store")
    operation_paths: List[Tuple[Dict[str, Any], Path]] = []
    for operation in plan["operations"]:
        path = store / Path(operation["path"])
        _assert_store_path_safe(store, path, label="purge target")
        if not path.exists() or not path.is_file():
            raise StoreError(f"Store changed after purge-plan: missing file {operation['path']}")
        if hashlib.sha256(_read_limited_bytes(path, label=f"purge target {path}")).hexdigest() != operation["sha256"]:
            raise StoreError(f"Store changed after purge-plan: {operation['path']}")
        operation_paths.append((operation, path))
    changes: Dict[Path, Optional[bytes]] = {}
    changed: List[str] = []
    prospective_context: Optional[Dict[str, Any]] = None
    prospective_evidence: Optional[Dict[str, Any]] = None
    for operation, path in operation_paths:
        if operation["action"] == "delete":
            changes[path] = None
        elif operation["action"] == "rewrite-derived-brief":
            # The derived copy is rendered only after the prospective
            # canonical context has been fully scrubbed below.
            changed.append(operation["path"])
            continue
        elif operation["action"] == "rewrite":
            data = read_json(path)
            cleaned, _, remove_document = scrub_node(data, kind, target_id)
            if remove_document or not isinstance(cleaned, dict):
                raise StoreError(f"Unexpected purge result for {operation['path']}")
            if path == context_path(store):
                if type(cleaned.get("revision", {}).get("version")) is not int:
                    raise StoreError("Purge would make Store invalid: revision.version must be a strict integer")
                cleaned["revision"]["version"] = cleaned["revision"]["version"] + 1
                purge_timestamp = now_utc()
                cleaned["revision"]["updated_at"] = purge_timestamp
                cleaned["revision"]["last_reviewed_at"] = purge_timestamp
                prospective_context = cleaned
                validation_errors, _ = validate_v04_context(cleaned)
                if validation_errors:
                    raise StoreError("Purge would make Store invalid: " + "; ".join(validation_errors))
            elif path == evidence_path(store):
                prospective_evidence = cleaned
            changes[path] = json_bytes(cleaned)
        elif operation["action"] == "rewrite-jsonl":
            records: List[Any] = []
            for raw_line in _read_limited_bytes(path, label=f"purge target {path}").decode("utf-8").splitlines():
                if not raw_line.strip():
                    continue
                record = json.loads(raw_line)
                cleaned, removed, remove_record = scrub_node(record, kind, target_id)
                if not removed and not remove_record:
                    records.append(cleaned)
            changes[path] = jsonl_bytes(records)
        else:
            raise StoreError(f"Unsupported purge operation: {operation['action']}")
        changed.append(operation["path"])
    if prospective_context is None:
        prospective_context = context
    if prospective_evidence is None:
        prospective_evidence = read_json(evidence_path(store))
    if prospective_evidence.get("schema_version") != V04_SCHEMA_VERSION or prospective_evidence.get("sources") != prospective_context.get("sources"):
        raise StoreError("Purge would make evidence/index.json diverge from context.sources")
    for operation, path in operation_paths:
        if operation["action"] == "rewrite-derived-brief":
            changes[path] = render_human_brief(prospective_context).encode("utf-8")
    fingerprint = hashlib.sha256(f"{kind}:{target_id}".encode("utf-8")).hexdigest()[:16]
    audit_path = store / "history" / "changes.jsonl"
    audit_existing = changes.get(audit_path)
    if audit_existing is None:
        audit_existing = _read_limited_bytes(audit_path, label=f"audit log {audit_path}") if audit_path.exists() else b""
    audit_record = {"timestamp": now_utc(), "operation": "purge", "target_kind": kind, "target_fingerprint": fingerprint, "confirmed_by": actor, "changed_files": changed}
    changes[audit_path] = append_jsonl_bytes(audit_existing, audit_record)
    verify_controlled_manifest(store, plan["controlled_manifest"])
    transactional_commit(
        list(changes.items()),
        manifest_root=store,
        expected_manifest=plan["controlled_manifest"],
    )
    return {"success": True, "dry_run": False, "target": {"kind": kind, "id": target_id}, "changed_files": changed, "external_uncontrolled_copies": plan["external_uncontrolled_copies"]}


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def preview_report() -> Dict[str, Any]:
    return {"status": "previewed", "schema": {"input": V03_SCHEMA_VERSION, "candidate": V04_SCHEMA_VERSION}, "candidate_valid": False, "candidate_sha256": None, "candidate_hash": None, "candidate_validation_errors": [], "counts": {"claims": 0, "tensions": 0, "unknowns": 0, "sources": 0}, "candidate_counts": {"claims": 0, "tensions": 0, "unknowns": 0, "sources": 0}, "ids": {"claims": [], "tensions": [], "unknowns": [], "sources": []}, "candidate_ids": {"claims": [], "tensions": [], "unknowns": [], "sources": []}, "field_mappings": [{"source": "profile_id", "target": "context_id and subject.id"}, {"source": "subject.preferred_name", "target": "subject.display_name"}, {"source": "core.claims[]", "target": "claims[]"}, {"source": "domains.<name>.claims[]", "target": "claims[] with domains[]"}, {"source": "core/domains.tensions[]", "target": "tensions[] with domains[]"}, {"source": "core/domains.unknowns[]", "target": "unknowns[] with domains[]"}, {"source": "sources[]", "target": "sources[] (unchanged)"}, {"source": "revision", "target": "revision"}], "defaulted_fields": [], "retired_legacy_metadata": [], "excluded_artifacts": ["views/**", "patches/**"], "conflicts": [], "warnings": [], "unmapped_fields": [], "loss_risks": [], "errors": [], "input_hashes": {"before": {}, "after": {}}, "input_unchanged": False}


def preview_issue(report: Dict[str, Any], bucket: str, code: str, path: str, message: str) -> None:
    report[bucket].append({"code": code, "path": path, "message": message})


def preview_store(store: Path | str, *, include_candidate: bool = False) -> Dict[str, Any]:
    store_path = Path(store).expanduser().resolve()
    _assert_store_tree_safe(store_path)
    report = preview_report()
    paths = {"context.json": store_path / "context.json", "evidence/index.json": store_path / "evidence" / "index.json"}
    before: Dict[str, str] = {}
    for label, path in paths.items():
        if path.exists() and path.is_file():
            try:
                before[label] = hashlib.sha256(_read_limited_bytes(path, label=f"preview input {path}")).hexdigest()
            except OSError:
                preview_issue(report, "errors", "unreadable_input", label, "required input cannot be hashed")
        else:
            preview_issue(report, "errors", "missing_input", label, "required input file is missing")
    report["input_hashes"]["before"] = before
    context = None
    evidence = None
    if "context.json" in before:
        try:
            context = read_json(paths["context.json"])
        except StoreError:
            preview_issue(report, "errors", "invalid_input", "context.json", "required input is not a readable JSON object")
    if "evidence/index.json" in before:
        try:
            evidence = read_json(paths["evidence/index.json"])
        except StoreError:
            preview_issue(report, "errors", "invalid_input", "evidence/index.json", "required input is not a readable JSON object")
    if context is not None and context.get("schema_version") != V03_SCHEMA_VERSION:
        report["status"] = "rejected"
        version = context.get("schema_version")
        report["schema"]["input"] = version if isinstance(version, str) else "unsupported"
        message = "schema 0.2 is rejected; first use the existing explicit migration flow on a copy to obtain schema 0.3" if version == V02_SCHEMA_VERSION else "only schema 0.3 is accepted by this preview"
        preview_issue(report, "errors", "unsupported_schema", "context.schema_version", message)
    if context is not None and evidence is not None and context.get("schema_version") == V03_SCHEMA_VERSION:
        for key in sorted(set(context) - {"schema_version", "profile_id", "subject", "policy", "coverage", "core", "domains", "sources", "revision"}):
            report["unmapped_fields"].append(key)
            preview_issue(report, "conflicts", "unmapped_field", key, "V0.3 field has no deterministic 1.0.1 target")
            preview_issue(report, "loss_risks", "unmapped_field", key, "field would not be copied to the fixed 1.0.1 Store")
        for key in sorted(set(evidence) - {"schema_version", "sources"}):
            path = f"evidence/index.json.{key}"
            report["unmapped_fields"].append(path)
            preview_issue(report, "conflicts", "unmapped_evidence_index_field", path, "evidence index field is outside the fixed V0.3 envelope")
            preview_issue(report, "loss_risks", "unmapped_evidence_index_field", path, "evidence index field would be dropped")
        context_sources = context.get("sources") if isinstance(context.get("sources"), list) else []
        evidence_sources = evidence.get("sources") if isinstance(evidence.get("sources"), list) else []
        context_table = {item.get("id"): item for item in context_sources if isinstance(item, dict) and isinstance(item.get("id"), str)}
        evidence_table = {item.get("id"): item for item in evidence_sources if isinstance(item, dict) and isinstance(item.get("id"), str)}
        for source_id in sorted(set(context_table) | set(evidence_table)):
            if source_id not in context_table or source_id not in evidence_table or context_table[source_id] != evidence_table[source_id]:
                preview_issue(report, "conflicts", "source_index_mismatch", f"sources[{source_id}]", "same Source ID is not identical in context and evidence index")
                preview_issue(report, "loss_risks", "source_index_mismatch", f"sources[{source_id}]", "source record would not be unambiguously preserved")
        if evidence.get("schema_version") != V03_SCHEMA_VERSION:
            preview_issue(report, "conflicts", "evidence_schema_mismatch", "evidence/index.json.schema_version", "evidence index schema must be V0.3")
            preview_issue(report, "loss_risks", "evidence_schema_mismatch", "evidence/index.json.schema_version", "evidence index schema cannot be mapped safely")
        source_ids = set(context_table)
        flat: Dict[str, List[Dict[str, Any]]] = {"claims": [], "tensions": [], "unknowns": []}
        seen_ids: Dict[str, str] = {}
        containers: List[Tuple[str, Any]] = [("core", context.get("core"))]
        containers.extend((f"domains.{name}", data) for name, data in (context.get("domains") or {}).items())
        for section_name, section in containers:
            if not isinstance(section, dict):
                preview_issue(report, "conflicts", "invalid_container", section_name, "legacy container must be an object")
                continue
            domain = None if section_name == "core" else section_name.split(".", 1)[1]
            if domain and "updated_at" in section:
                report["retired_legacy_metadata"].append({"path": f"{section_name}.updated_at", "reason": "legacy domain-container bookkeeping metadata is retired and is not part of the V0.4 canonical Store"})
                report["warnings"].append(f"{section_name}.updated_at is retired metadata and is not migrated")
            allowed_keys = {"claims", "tensions", "unknowns"} | ({"updated_at"} if domain else set())
            for key in sorted(set(section) - allowed_keys):
                preview_issue(report, "conflicts", "unmapped_section_field", f"{section_name}.{key}", "legacy field has no deterministic 1.0.1 target")
                preview_issue(report, "loss_risks", "unmapped_section_field", f"{section_name}.{key}", "legacy field would be dropped")
            for category in flat:
                values = section.get(category, [])
                if not isinstance(values, list):
                    preview_issue(report, "conflicts", "invalid_collection", f"{section_name}.{category}", "legacy collection must be an array")
                    continue
                for index, item in enumerate(values):
                    label = f"{section_name}.{category}[{index}]"
                    if not isinstance(item, dict) or not is_safe_id(item.get("id")):
                        preview_issue(report, "conflicts", "missing_context_id", label, "Claim/Tension/Unknown has no usable ID")
                        continue
                    if item["id"] in seen_ids:
                        preview_issue(report, "conflicts", "duplicate_context_id", label, "duplicate Claim/Tension/Unknown ID")
                        preview_issue(report, "loss_risks", "duplicate_context_id", label, "duplicate identity prevents deterministic migration")
                    else:
                        seen_ids[item["id"]] = label
                    mapped = copy.deepcopy(item)
                    mapped.pop("layer", None)
                    mapped.pop("domain", None)
                    mapped["domains"] = [domain] if domain else []
                    if isinstance(item.get("domains"), list):
                        if all(isinstance(value, str) for value in item["domains"]) and len(item["domains"]) != len(set(item["domains"])):
                            preview_issue(report, "conflicts", "duplicate_array_value", f"{label}.domains", "legacy domains must contain unique values")
                            preview_issue(report, "loss_risks", "duplicate_array_value", f"{label}.domains", "duplicate domain labels are not silently normalized")
                        mapped["domains"] = list(dict.fromkeys(mapped["domains"] + [value for value in item["domains"] if isinstance(value, str)]))
                    if category == "claims":
                        for ref_field in ("evidence_refs", "counterevidence_refs", "promotion_evidence"):
                            values_for_field = item.get(ref_field)
                            if isinstance(values_for_field, list) and all(isinstance(value, str) for value in values_for_field) and len(values_for_field) != len(set(values_for_field)):
                                preview_issue(report, "conflicts", "duplicate_array_value", f"{label}.{ref_field}", "legacy evidence arrays must contain unique values")
                                preview_issue(report, "loss_risks", "duplicate_array_value", f"{label}.{ref_field}", "duplicate evidence values are not silently normalized")
                        mapped.pop("promotion_evidence", None)
                        promotion = item.get("promotion_evidence", [])
                        for ref in promotion if isinstance(promotion, list) else []:
                            if isinstance(ref, str) and evidence_ref_source_id(ref) in source_ids:
                                mapped.setdefault("evidence_refs", []).append(ref)
                                report["field_mappings"].append({"source": f"{label}.promotion_evidence", "target": f"{label}.evidence_refs"})
                            else:
                                preview_issue(report, "conflicts", "unmapped_promotion_evidence", label, "promotion_evidence is not a resolvable Source reference")
                                preview_issue(report, "loss_risks", "unmapped_promotion_evidence", label, "promotion evidence would be lost or guessed")
                        if "disclosure" not in mapped:
                            mapped["disclosure"] = copy.deepcopy(DEFAULT_DISCLOSURE)
                            report["defaulted_fields"].append({"path": f"{label}.disclosure", "value": copy.deepcopy(DEFAULT_DISCLOSURE), "reason": "V0.3 had no disclosure field; conservative default"})
                        mapped["evidence_refs"] = list(dict.fromkeys(mapped.get("evidence_refs", [])))
                    elif mapped.get("sensitivity") != "public" and "disclosure" not in mapped:
                        mapped["disclosure"] = copy.deepcopy(DEFAULT_DISCLOSURE)
                        report["defaulted_fields"].append(
                            {
                                "path": f"{label}.disclosure",
                                "value": copy.deepcopy(DEFAULT_DISCLOSURE),
                                "reason": "non-public V0.3 items had no disclosure field; conservative default",
                            }
                        )
                    flat[category].append(mapped)
        for category in flat:
            report["counts"][category] = len(flat[category])
            report["ids"][category] = [item.get("id") for item in flat[category] if isinstance(item, dict)]
        report["counts"]["sources"] = len(context_sources)
        report["ids"]["sources"] = [item.get("id") for item in context_sources if isinstance(item, dict)]
        if set(context_table) & set(seen_ids):
            preview_issue(report, "conflicts", "duplicate_global_id", "sources", "Source ID collides with a Claim/Tension/Unknown ID")
            preview_issue(report, "loss_risks", "duplicate_global_id", "sources", "global identity is not unique")
        old_subject = context.get("subject") if isinstance(context.get("subject"), dict) else {}
        old_policy = context.get("policy") if isinstance(context.get("policy"), dict) else {}
        old_coverage = context.get("coverage") if isinstance(context.get("coverage"), dict) else {}
        old_revision = context.get("revision") if isinstance(context.get("revision"), dict) else {}
        profile_id = context.get("profile_id")
        display_name = old_subject.get("preferred_name", "")
        languages = old_subject.get("preferred_languages", [])
        if not is_safe_id(profile_id) or not isinstance(display_name, str) or not isinstance(languages, list) or not all(isinstance(value, str) for value in languages):
            preview_issue(report, "conflicts", "invalid_subject", "subject", "subject/profile ID cannot be mapped deterministically")
        for key in ("patch_approval_required", "default_view_ttl_days"):
            if key not in old_policy:
                preview_issue(report, "conflicts", "missing_policy_field", f"policy.{key}", "required policy field is missing")
                preview_issue(report, "loss_risks", "missing_policy_field", f"policy.{key}", "policy cannot be reconstructed without a default")
        for key in ("core_claim_soft_limit", "core_char_soft_limit"):
            if key in old_policy:
                report["warnings"].append(f"policy.{key} is omitted because Core is a derived summary")
        for key in ("depth", "included_domains", "missing_domains"):
            if key not in old_coverage:
                preview_issue(report, "conflicts", "missing_coverage_field", f"coverage.{key}", "required coverage field is missing")
                preview_issue(report, "loss_risks", "missing_coverage_field", f"coverage.{key}", "coverage cannot be reconstructed deterministically")
        for key in ("version", "created_at", "updated_at", "last_reviewed_at"):
            if key not in old_revision:
                preview_issue(report, "conflicts", "missing_revision_field", f"revision.{key}", "required revision field is missing")
                preview_issue(report, "loss_risks", "missing_revision_field", f"revision.{key}", "revision cannot be preserved completely")
        candidate = {"schema_version": V04_SCHEMA_VERSION, "context_id": profile_id, "subject": {"type": "person", "id": profile_id, "display_name": display_name, "preferred_languages": copy.deepcopy(languages)}, "policy": {"patch_approval_required": old_policy.get("patch_approval_required"), "default_view_ttl_days": old_policy.get("default_view_ttl_days"), "auto_import_harness_memory": False}, "coverage": {"depth": old_coverage.get("depth"), "included_domains": copy.deepcopy(old_coverage.get("included_domains")), "missing_domains": copy.deepcopy(old_coverage.get("missing_domains"))}, "claims": flat["claims"], "tensions": flat["tensions"], "unknowns": flat["unknowns"], "sources": copy.deepcopy(context_sources), "revision": copy.deepcopy(old_revision)}
        candidate_errors, _ = validate_v04_context(candidate)
        report["candidate_validation_errors"] = candidate_errors
        report["candidate_sha256"] = canonical_hash(candidate)
        report["candidate_hash"] = report["candidate_sha256"]
        report["candidate_counts"] = {key: len(candidate[key]) for key in ("claims", "tensions", "unknowns", "sources")}
        report["candidate_ids"] = {key: [item.get("id") for item in candidate[key] if isinstance(item, dict)] for key in ("claims", "tensions", "unknowns", "sources")}
        if include_candidate:
            report["candidate"] = candidate
    after: Dict[str, str] = {}
    for label, path in paths.items():
        if path.exists() and path.is_file():
            after[label] = hashlib.sha256(_read_limited_bytes(path, label=f"preview input {path}")).hexdigest()
    report["input_hashes"]["after"] = after
    report["input_unchanged"] = report["input_hashes"]["before"] == after and len(after) == len(paths)
    if not report["input_unchanged"]:
        preview_issue(report, "conflicts", "input_changed", "input_hashes", "input hashes changed during preview")
        preview_issue(report, "loss_risks", "input_changed", "input_hashes", "candidate cannot be trusted after input mutation")
    report["candidate_valid"] = bool(report["status"] != "rejected" and report["input_unchanged"] and not report["errors"] and not report["conflicts"] and not report["loss_risks"] and not report["unmapped_fields"] and not report["candidate_validation_errors"])
    return report


def inside_store(path: Path, store: Path) -> bool:
    try:
        path.relative_to(store)
        return True
    except ValueError:
        return False


def command_preview_migrate_v03(args: argparse.Namespace) -> Dict[str, Any]:
    store = store_path_from_arg(args.store)
    if args.output:
        output = Path(args.output).expanduser()
        if inside_store(output.resolve(strict=False), store.resolve(strict=False)):
            report = preview_report()
            report["status"] = "rejected"
            preview_issue(report, "errors", "output_inside_store", "output", "--output must be outside the input Store directory")
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return {"success": False, "_exit_code": 2, "_printed": True}
        _assert_output_path_safe(output)
    report = preview_store(store)
    if args.output:
        _assert_output_path_safe(output)
        atomic_write_bytes(output, (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return {"success": report.get("candidate_valid") is True, "report": report, "_exit_code": 0 if report.get("candidate_valid") is True else 2, "_printed": False}


def command_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a Brief Yourself Personal Context Store")
    subs = parser.add_subparsers(dest="command", required=True)
    init = subs.add_parser("init", help="Initialize a new V0.4 Store")
    init.add_argument("--store", required=True)
    init.add_argument("--context-id")
    init.add_argument("--profile-id", help="legacy alias for --context-id")
    init.add_argument("--preferred-name", default="")
    init.set_defaults(func=command_init)
    validate = subs.add_parser("validate", help="Validate a Store")
    validate.add_argument("--store", required=True)
    validate.set_defaults(func=command_validate)
    inspect = subs.add_parser("inspect", help="Inspect Store metadata")
    inspect.add_argument("--store", required=True)
    inspect.add_argument("--claim-id")
    inspect.set_defaults(func=command_inspect)
    derive = subs.add_parser("derive-core-summary", help="Derive a non-canonical Core Summary")
    derive.add_argument("--store", required=True)
    derive.set_defaults(func=command_derive_core_summary)
    export = subs.add_parser("export", help="Export a sensitivity-bounded V0.4 Store")
    export.add_argument("--store", required=True)
    export.add_argument("--format", choices=("json", "markdown"), default="markdown")
    export.add_argument("--output", required=True)
    export.add_argument("--include-private", action="store_true")
    export.add_argument("--include-restricted", action="store_true")
    export.set_defaults(func=command_export)
    source = subs.add_parser("register-source", help="Register one explicitly approved Evidence Source")
    source.add_argument("--store", required=True)
    source.add_argument("--source", required=True)
    source.add_argument("--confirmed-by", required=True)
    source.add_argument("--approve", action="store_true")
    source.set_defaults(func=command_register_source)
    migrate = subs.add_parser("migrate-v02", help="Explicitly migrate V0.2 to V0.3 only")
    migrate.add_argument("--store", required=True)
    migrate.add_argument("--confirmed-by", required=True)
    migrate.add_argument("--approve", action="store_true")
    migrate.set_defaults(func=command_migrate_v02)
    view = subs.add_parser("create-view", help="Create a frozen V0.4 Context View")
    view.add_argument("--store", required=True)
    view.add_argument("--purpose", required=True)
    view.add_argument("--task", required=True)
    view.add_argument("--principal-id", default="self-agent")
    view.add_argument("--principal-type", default="agent")
    view.add_argument("--audience-id", action="append", default=[])
    view.add_argument("--audience-ids", dest="audience_ids", nargs="*", default=[])
    view.add_argument("--audience", dest="audience_ids", action="append", default=[])
    view.add_argument("--audience-type", default="agent")
    view.add_argument("--purpose-approved", action="store_true")
    view.add_argument("--domains", nargs="*", default=[])
    view.add_argument("--claim-ids", nargs="*", default=[])
    view.add_argument("--tension-ids", nargs="*", default=[])
    view.add_argument("--unknown-ids", nargs="*", default=[])
    view.add_argument("--include-core", action="store_true")
    view.add_argument("--include-private", action="store_true")
    view.add_argument("--include-restricted", action="store_true")
    view.add_argument("--include-unreviewed", action="store_true")
    view.add_argument("--archive-in-personal-store", action="store_true")
    view.add_argument("--allow-downstream-persistence", action="store_true")
    view.add_argument("--allow-persistence", action="store_true", help=argparse.SUPPRESS)
    view.add_argument("--allowed-use", default="current task only")
    view.add_argument("--expires-at")
    view.add_argument("--ttl-days", type=int)
    view.add_argument("--view-id")
    view.add_argument("--output", required=True)
    view.set_defaults(func=command_create_view)
    view_validate = subs.add_parser("validate-view", help="Validate a frozen Context View")
    view_validate.add_argument("--view", required=True)
    view_validate.add_argument("--store")
    view_validate.add_argument("--purpose")
    view_validate.add_argument("--task")
    view_validate.add_argument("--principal-id")
    view_validate.add_argument("--purpose-approved", action="store_true")
    view_validate.add_argument("--include-unreviewed", action="store_true", help="Explicitly include unreviewed/unresolved items")
    view_validate.add_argument("--allowed-use")
    view_validate.add_argument("--require-downstream-persistence", action="store_true")
    view_validate.set_defaults(func=command_validate_view)
    stage = subs.add_parser("stage-patch", help="Stage a V0.4 Patch without changing context")
    stage.add_argument("--store", required=True)
    stage.add_argument("--patch", required=True)
    stage.set_defaults(func=command_stage_patch)
    apply = subs.add_parser("apply-patch", help="Apply a reviewed V0.4 Patch")
    apply.add_argument("--store", required=True)
    apply.add_argument("--patch-id", required=True)
    apply.add_argument("--confirmed-by")
    apply.add_argument("--confirmed-actor", dest="confirmed_actor")
    apply.add_argument("--actor")
    apply.add_argument("--approve", action="store_true")
    apply.set_defaults(func=command_apply_patch)
    reject = subs.add_parser("reject-patch", help="Reject a pending V0.4 Patch")
    reject.add_argument("--store", required=True)
    reject.add_argument("--patch-id", required=True)
    reject.add_argument("--confirmed-by")
    reject.add_argument("--confirmed-actor", dest="confirmed_actor")
    reject.add_argument("--actor")
    reject.add_argument("--reason", required=True)
    reject.set_defaults(func=command_reject_patch)
    for name in ("list-patches", "list"):
        listing = subs.add_parser(name, help="List Patch ids")
        listing.add_argument("--store", required=True)
        listing.set_defaults(func=command_list_patches)
    for name, func, help_text in (("purge-plan", command_purge_plan, "Preview an exact purge"), ("purge", command_purge, "Execute an approved purge")):
        purge = subs.add_parser(name, help=help_text)
        purge.add_argument("--store", required=True)
        targets = purge.add_mutually_exclusive_group(required=True)
        targets.add_argument("--claim-id")
        targets.add_argument("--source-id")
        targets.add_argument("--view-id")
        targets.add_argument("--patch-id")
        if name == "purge":
            purge.add_argument("--plan-token", required=True)
            purge.add_argument("--confirmed-by")
            purge.add_argument("--confirmed-actor", dest="confirmed_actor")
            purge.add_argument("--actor")
            purge.add_argument("--approve", action="store_true")
        purge.set_defaults(func=func)
    preview = subs.add_parser("preview-migrate-v03", help="Metadata-only V0.3 to V0.4 migration preview")
    preview.add_argument("--store", "--input-store", "--input", dest="store", required=True)
    preview.add_argument("--output")
    preview.set_defaults(func=command_preview_migrate_v03)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = command_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
        if result.pop("_printed", False):
            return int(result.pop("_exit_code", 0))
        exit_code = int(result.pop("_exit_code", 0))
        if args.command == "preview-migrate-v03":
            report = result.pop("report")
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return exit_code
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("success", False) else 1
    except (MemoryError, RecursionError) as exc:
        print(json.dumps({"success": False, "error": "input exceeds resource limits"}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    except ResourceLimitError as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    except StoreError as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
