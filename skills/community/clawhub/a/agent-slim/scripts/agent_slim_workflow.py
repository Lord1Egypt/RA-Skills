#!/usr/bin/env python3
"""Safe planning, transactional apply, verification, and restore for Agent Slim.

The module is deliberately standard-library only.  It consumes the stable audit
JSON contract, writes plans before changing anything, moves data instead of
deleting it, and stops on any hash, scope, or destination conflict.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

try:
    from agent_slim_adapter import CapabilityUnavailable, probe_codex_home, require_capability
except ImportError as exc:  # pragma: no cover - packaging failure is an IO error
    raise SystemExit("agent_slim_adapter.py is required next to agent_slim_workflow.py") from exc

PLAN_SCHEMA_VERSION = "1.0"
TOOL_VERSION = "0.1.2"
MAX_HASH_BYTES = 256 * 1024 * 1024
MAX_PRESERVED_FILES = 2000
DEFAULT_ACTION_TIMEOUT = 60

ALLOWED_ACTIONS = (
    "quarantine-redundant-backup",
    "archive-verified-old-session",
    "quarantine-low-frequency-file",
)

AUDIT_READ_ONLY_ACTIONS = {
    "review-backup-retention",
    "archive-verified-old-sessions",
    "review-unreferenced-warm-content",
    "route-large-warm-file",
    "route-large-skill-body",
    "review-duplicate-hot-rules",
    "review-wide-skill-description",
    "disable-explicitly-unused-optional-plugin",
}

RISK_ORDER = {"R0": 0, "R1": 1, "R2": 2, "R3": 3}

EXIT_OK = 0
EXIT_VERIFY_FAILED = 1
EXIT_WARNING = 2
EXIT_CONFLICT = 3
EXIT_TRANSACTION = 4
EXIT_USAGE = 64
EXIT_IO = 74


class WorkflowError(Exception):
    """A stable, documentable workflow failure."""

    def __init__(self, code: str, message: str, exit_code: int = EXIT_TRANSACTION):
        super().__init__(message)
        self.code = code
        self.message = message
        self.exit_code = exit_code


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    """Hash a file without decoding or printing its content."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkflowError("FILE_NOT_FOUND", "JSON file was not found: {}".format(path.name), EXIT_IO) from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise WorkflowError("INVALID_JSON", "JSON file could not be parsed: {}".format(path.name), EXIT_IO) from exc
    if not isinstance(value, dict):
        raise WorkflowError("INVALID_JSON_ROOT", "JSON root must be an object: {}".format(path.name), EXIT_IO)
    return value


def write_text_exclusive(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def write_json_exclusive(path: Path, value: Dict[str, Any]) -> None:
    write_text_exclusive(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def write_json_replace(path: Path, value: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def emit_json(value: Dict[str, Any], output: Optional[str]) -> None:
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if not output or output == "-":
        sys.stdout.write(text)
        return
    path = Path(output).expanduser()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    except OSError as exc:
        raise WorkflowError("OUTPUT_WRITE_FAILED", "Could not write output file: {}".format(path.name), EXIT_IO) from exc


def safe_rel(path: Path, root: Path) -> Optional[str]:
    try:
        relative = os.path.relpath(str(path), str(root))
    except (OSError, ValueError):
        return None
    if relative == os.pardir or relative.startswith(os.pardir + os.sep):
        return None
    return Path(relative).as_posix() if relative != "." else "."


def _clean_relative(relative: object, message: str) -> PurePosixPath:
    """Normalize a relative path and reject absolute, drive, UNC and traversal forms."""
    if not isinstance(relative, str) or not relative or relative == ".":
        raise WorkflowError("SCOPE_VIOLATION", message, EXIT_CONFLICT)
    raw = relative.replace("\\", "/")
    if raw.startswith("//") or re.match(r"^[A-Za-z]:", raw):
        raise WorkflowError("SCOPE_VIOLATION", message, EXIT_CONFLICT)
    pure = PurePosixPath(raw)
    if pure.is_absolute() or any(part in ("", ".", "..") or ":" in part for part in pure.parts):
        raise WorkflowError("SCOPE_VIOLATION", message, EXIT_CONFLICT)
    return pure


def safe_relative_target(home: Path, relative: str) -> Path:
    """Resolve a home-relative path and reject absolute, traversal, and symlink escapes."""
    pure = _clean_relative(relative, "Target path must be a clean home-relative path.")
    current = home
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            raise WorkflowError("SCOPE_VIOLATION", "Symlink paths are not eligible for transactional moves.", EXIT_CONFLICT)
    resolved = current.resolve(strict=False)
    if safe_rel(resolved, home.resolve(strict=False)) is None:
        raise WorkflowError("SCOPE_VIOLATION", "Target resolves outside the audited home.", EXIT_CONFLICT)
    return resolved


def resolve_transaction_path(transaction_dir: Path, relative: str) -> Path:
    pure = _clean_relative(relative, "Transaction path must be relative and clean.")
    resolved = (transaction_dir / Path(*pure.parts)).resolve(strict=False)
    if safe_rel(resolved, transaction_dir.resolve()) is None:
        raise WorkflowError("SCOPE_VIOLATION", "Transaction destination escapes the isolation directory.", EXIT_CONFLICT)
    return resolved


def _file_snapshot(path: Path) -> Dict[str, Any]:
    try:
        stat_value = path.stat()
    except OSError as exc:
        raise WorkflowError("TARGET_NOT_FOUND", "Target file is missing or unreadable: {}".format(path.name), EXIT_CONFLICT) from exc
    if not stat.S_ISREG(stat_value.st_mode):
        raise WorkflowError("TARGET_NOT_REGULAR", "Transactional targets must be regular files.", EXIT_CONFLICT)
    if stat_value.st_size > MAX_HASH_BYTES:
        raise WorkflowError("TARGET_TOO_LARGE", "Target exceeds the transactional hash limit.", EXIT_CONFLICT)
    try:
        digest = sha256_file(path)
    except OSError as exc:
        raise WorkflowError("TARGET_HASH_FAILED", "Target could not be hashed: {}".format(path.name), EXIT_IO) from exc
    return {
        "sha256": digest,
        "bytes": stat_value.st_size,
        "mtimeNs": stat_value.st_mtime_ns,
        "mode": stat.S_IMODE(stat_value.st_mode),
    }


def _iter_files(root: Path, max_depth: int = 32) -> Iterable[Path]:
    if not root.is_dir():
        return
    root_depth = len(root.parts)
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        if len(current_path.parts) - root_depth >= max_depth:
            dirs[:] = []
        dirs[:] = sorted(name for name in dirs if not (current_path / name).is_symlink())
        for name in sorted(files):
            path = current_path / name
            if path.is_file() and not path.is_symlink():
                yield path


def _path_in_confirmations(relative: str, confirms: Sequence[str]) -> bool:
    for raw in confirms:
        candidate = raw.strip().replace("\\", "/").rstrip("/")
        if not candidate:
            continue
        relative_normalized = relative.replace("\\", "/")
        if relative_normalized == candidate or relative_normalized.startswith(candidate + "/"):
            return True
    return False


def _action_base(
    action: str,
    target_path: str,
    target: Dict[str, Any],
    reason: str,
    risk: str,
    context_tokens: int,
    context_evidence: str,
    context_basis: str,
    backup_path: Optional[str],
    executable: bool,
    status: str,
    verification: Sequence[str],
    source_ref: Optional[str] = None,
) -> Dict[str, Any]:
    disk = {
        "bytes": 0,
        "evidence": "measured",
        "basis": "Move-only transaction; no deletion and no free-space claim.",
        "recoverableBytes": int(target.get("bytes") or 0),
    }
    value: Dict[str, Any] = {
        "id": "pending",
        "action": action,
        "status": status,
        "executable": executable,
        "sourceRef": source_ref,
        "target": {
            "path": target_path,
            "kind": "file",
            "sha256": target.get("sha256"),
            "bytes": int(target.get("bytes") or 0),
            "mtimeNs": target.get("mtimeNs"),
        },
        "reason": reason,
        "expectedContextSavings": {
            "tokens": int(context_tokens),
            "evidence": context_evidence,
            "basis": context_basis,
        },
        "expectedDiskSavings": disk,
        "risk": risk,
        "reversibility": "Move back from the recorded isolation path after SHA-256 verification.",
        "backupPath": backup_path,
        "verification": list(verification),
    }
    return value


def _candidate_items(audit: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    layers = audit.get("layers", {})
    if isinstance(layers, dict):
        for name in ("hot", "warm", "cold"):
            for item in layers.get(name, []):
                if isinstance(item, dict) and item.get("id"):
                    result[str(item["id"])] = item
    return result


def _duplicate_backup_actions(home: Path, audit: Dict[str, Any], txn_rel: str) -> Tuple[List[Dict[str, Any]], bool]:
    backup_root = home / "backups"
    candidates = [c for c in audit.get("candidates", []) if c.get("action") == "review-backup-retention"]
    files = [path for path in _iter_files(backup_root, int(audit.get("scope", {}).get("maxDepth", 8)))]
    if not files:
        return [], bool(candidates)
    by_size: Dict[int, List[Path]] = {}
    for path in files:
        try:
            by_size.setdefault(path.stat().st_size, []).append(path)
        except OSError:
            continue
    actions: List[Dict[str, Any]] = []
    for size, size_group in sorted(by_size.items()):
        if size > MAX_HASH_BYTES:
            continue
        by_hash: Dict[str, List[Path]] = {}
        for path in size_group:
            try:
                by_hash.setdefault(sha256_file(path), []).append(path)
            except OSError:
                continue
        for digest, group in sorted(by_hash.items()):
            if len(group) < 2:
                continue
            ordered = sorted(group, key=lambda path: (path.stat().st_mtime_ns, safe_rel(path, home) or path.name))
            retained = ordered[0]
            for redundant in ordered[1:]:
                relative = safe_rel(redundant, home)
                if relative is None:
                    continue
                snapshot = _file_snapshot(redundant)
                backup_path = "{}/{}".format(txn_rel, relative)
                actions.append(
                    _action_base(
                        "quarantine-redundant-backup",
                        relative,
                        snapshot,
                        "Byte-identical duplicate of retained backup '{}'; move the redundant copy to isolation.".format(
                            safe_rel(retained, home)
                        ),
                        "R2",
                        0,
                        "unknown",
                        "Cold backup relocation does not establish a per-turn context reduction.",
                        backup_path,
                        True,
                        "ready",
                        ["backup-sha256", "target-state", "restore-roundtrip"],
                        source_ref="duplicate-sha256:{}".format(digest[:16]),
                    )
                )
    return actions, bool(candidates or actions)


def _archive_session_actions(
    home: Path,
    audit: Dict[str, Any],
    confirms: Sequence[str],
    txn_rel: str,
) -> List[Dict[str, Any]]:
    if not any(c.get("action") == "archive-verified-old-sessions" for c in audit.get("candidates", [])):
        return []
    sessions_root = home / "sessions"
    if not sessions_root.is_dir():
        return []
    old_days = 30
    items = _candidate_items(audit)
    for item in items.values():
        if item.get("category") == "sessions" and item.get("evidencePath") == "sessions/":
            old_days = int(item.get("meta", {}).get("ageThresholdDays") or old_days)
            break
    cutoff = datetime.now(timezone.utc).timestamp() - old_days * 86400
    actions: List[Dict[str, Any]] = []
    for path in _iter_files(sessions_root, int(audit.get("scope", {}).get("maxDepth", 8))):
        try:
            if path.stat().st_mtime >= cutoff:
                continue
        except OSError:
            continue
        relative = safe_rel(path, home)
        if relative is None:
            continue
        confirmed = _path_in_confirmations(relative, confirms)
        snapshot = _file_snapshot(path)
        backup_path = "{}/archive/{}".format(txn_rel, relative)
        actions.append(
            _action_base(
                "archive-verified-old-session",
                relative,
                snapshot,
                (
                    "Old session metadata was confirmed by the caller for closure and handoff; move, do not delete."
                    if confirmed
                    else "Session is older than the metadata threshold, but closed/handoff state is not proven; confirmation is required."
                ),
                "R2",
                0,
                "unknown",
                "Archived session storage is cold and cannot be converted into a Token-savings claim.",
                backup_path,
                confirmed,
                "ready" if confirmed else "pending-confirmation",
                ["session-sha256", "closure-confirmation", "restore-roundtrip"],
                source_ref="sessions-age-metadata",
            )
        )
    return actions


def _warm_quarantine_actions(
    home: Path,
    audit: Dict[str, Any],
    confirms: Sequence[str],
    txn_rel: str,
) -> Tuple[List[Dict[str, Any]], set[str]]:
    actions: List[Dict[str, Any]] = []
    consumed: set[str] = set()
    items = _candidate_items(audit)
    for candidate in audit.get("candidates", []):
        if candidate.get("action") != "review-unreferenced-warm-content":
            continue
        item = items.get(str(candidate.get("targetId")))
        if not item or item.get("kind") != "file":
            continue
        relative = str(item.get("evidencePath") or "")
        if not relative.startswith("skills/"):
            continue
        try:
            target = safe_relative_target(home, relative)
            snapshot = _file_snapshot(target)
        except WorkflowError:
            continue
        confirmed = _path_in_confirmations(relative, confirms)
        backup_path = "{}/payload/{}".format(txn_rel, relative)
        actions.append(
            _action_base(
                "quarantine-low-frequency-file",
                relative,
                snapshot,
                (
                    "Unreferenced warm file was explicitly confirmed as low-frequency; move it to reversible isolation."
                    if confirmed
                    else "Warm file is unreferenced by its skill body, but file-level use frequency is not proven; confirmation is required."
                ),
                "R2",
                0,
                "unknown",
                "No load-frequency measurement exists; no Token or disk-free savings are claimed for a move.",
                backup_path,
                confirmed,
                "ready" if confirmed else "pending-confirmation",
                ["reference-integrity", "target-state", "restore-roundtrip"],
                source_ref=str(candidate.get("id") or "warm-reference"),
            )
        )
        consumed.add(str(candidate.get("id")))
    return actions, consumed


def _manual_review_actions(audit: Dict[str, Any], consumed: set[str]) -> List[Dict[str, Any]]:
    items = _candidate_items(audit)
    actions: List[Dict[str, Any]] = []
    for candidate in audit.get("candidates", []):
        candidate_id = str(candidate.get("id") or "")
        requested = str(candidate.get("action") or "")
        if requested not in AUDIT_READ_ONLY_ACTIONS or candidate_id in consumed:
            continue
        if requested in {"review-backup-retention", "archive-verified-old-sessions", "review-unreferenced-warm-content"}:
            continue
        item = items.get(str(candidate.get("targetId")))
        target_path = str((item or {}).get("evidencePath") or candidate.get("targetPath") or "")
        if not target_path:
            continue
        token_value = 0
        token_evidence = "unknown"
        token_basis = "No host load measurement proves a reduction for this manual-review item."
        if requested in {"review-duplicate-hot-rules", "route-large-skill-body"}:
            token_value = int(candidate.get("estimatedTokens") or 0)
            token_evidence = "estimated-upper-bound"
            token_basis = "Audit content-size estimate; not an implemented Token reduction."
        snapshot = {
            "sha256": (item or {}).get("sha256"),
            "bytes": int(candidate.get("bytes") or (item or {}).get("bytes") or 0),
            "mtimeNs": None,
        }
        actions.append(
            _action_base(
                "manual-review",
                target_path,
                snapshot,
                str(candidate.get("reason") or "Audit candidate requires manual review."),
                str(candidate.get("risk") or "R2"),
                token_value,
                token_evidence,
                token_basis,
                None,
                False,
                "pending-confirmation",
                ["manual-review", "evidence-required-before-apply"],
                source_ref=candidate_id,
            )
        )
        actions[-1]["requestedAction"] = requested
    return actions


def _preserved_files(home: Path, audit: Dict[str, Any], target_paths: set[str]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    files: Dict[str, Dict[str, Any]] = {}
    items = _candidate_items(audit)
    for item in items.values():
        if item.get("layer") not in ("hot", "warm") or item.get("kind") != "file":
            continue
        relative = str(item.get("evidencePath") or "")
        if not relative or relative in target_paths:
            continue
        try:
            path = safe_relative_target(home, relative)
            if not path.is_file():
                continue
            snapshot = _file_snapshot(path)
        except WorkflowError:
            continue
        files[relative] = {"path": relative, "sha256": snapshot["sha256"], "bytes": snapshot["bytes"]}
    for extra in ("AGENTS.md", "config.toml"):
        if extra in files or extra in target_paths:
            continue
        try:
            path = safe_relative_target(home, extra)
            if path.is_file():
                snapshot = _file_snapshot(path)
                files[extra] = {"path": extra, "sha256": snapshot["sha256"], "bytes": snapshot["bytes"]}
        except WorkflowError:
            continue
    for edge in audit.get("referenceGraph", []):
        if edge.get("scope") != "inside-home" or not edge.get("evidencePath"):
            continue
        relative = str(edge["evidencePath"])
        if relative in files or relative in target_paths:
            continue
        try:
            path = safe_relative_target(home, relative)
            if path.is_file():
                snapshot = _file_snapshot(path)
                files[relative] = {"path": relative, "sha256": snapshot["sha256"], "bytes": snapshot["bytes"]}
        except WorkflowError:
            continue
    ordered = [files[key] for key in sorted(files)][:MAX_PRESERVED_FILES]
    parse_checks: List[Dict[str, str]] = []
    for record in ordered:
        relative = record["path"]
        suffix = Path(relative).suffix.lower()
        if suffix == ".json":
            parse_checks.append({"path": relative, "kind": "json"})
        elif suffix in (".yaml", ".yml"):
            parse_checks.append({"path": relative, "kind": "yaml-frontmatter-restricted"})
        elif Path(relative).name.lower() == "skill.md":
            parse_checks.append({"path": relative, "kind": "yaml-frontmatter-restricted"})
    return ordered, parse_checks


def _sort_actions(actions: List[Dict[str, Any]]) -> None:
    def key(action: Dict[str, Any]) -> Tuple[int, int, int, int, str]:
        ready = 0 if action.get("status") == "ready" else 1
        risk = RISK_ORDER.get(str(action.get("risk")), 9)
        context = int(action.get("expectedContextSavings", {}).get("tokens") or 0)
        recoverable = int(action.get("expectedDiskSavings", {}).get("recoverableBytes") or 0)
        return (ready, risk, -context, -recoverable, str(action.get("target", {}).get("path") or ""))

    actions.sort(key=key)
    for index, action in enumerate(actions, 1):
        action["id"] = "action-{:03d}".format(index)
        action["priorityScore"] = max(1, 1000 - index)


def _default_transaction_root(home: Path) -> Path:
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "-", home.name).strip("-") or "home"
    return home.parent / ".agent-slim-transactions" / safe_name


def validate_plan(plan: Dict[str, Any]) -> None:
    required = {
        "schemaVersion", "kind", "planId", "createdAt", "mode", "defaultApplyMode",
        "home", "sourceAudit", "transaction", "policy", "actions", "preservedFiles",
        "parseChecks", "referenceGraph", "ranking", "limitations",
    }
    missing = sorted(required - set(plan))
    if missing:
        raise WorkflowError("PLAN_SCHEMA_INVALID", "Plan missing fields: {}".format(", ".join(missing)), EXIT_USAGE)
    if plan.get("schemaVersion") != PLAN_SCHEMA_VERSION or plan.get("kind") != "agent-slim-plan":
        raise WorkflowError("PLAN_SCHEMA_INVALID", "Unsupported plan schema or kind.", EXIT_USAGE)
    if plan.get("mode") != "dry-run":
        raise WorkflowError("PLAN_SCHEMA_INVALID", "Plan mode must be dry-run.", EXIT_USAGE)
    action_ids = set()
    for action in plan.get("actions", []):
        if not isinstance(action, dict):
            raise WorkflowError("PLAN_SCHEMA_INVALID", "Each action must be an object.", EXIT_USAGE)
        for field in (
            "id", "action", "status", "executable", "target", "reason",
            "expectedContextSavings", "expectedDiskSavings", "risk", "backupPath", "verification",
        ):
            if field not in action:
                raise WorkflowError("PLAN_SCHEMA_INVALID", "Action missing field: {}".format(field), EXIT_USAGE)
        if action["id"] in action_ids:
            raise WorkflowError("PLAN_SCHEMA_INVALID", "Duplicate action id: {}".format(action["id"]), EXIT_USAGE)
        action_ids.add(action["id"])
        if action.get("status") not in {"ready", "pending-confirmation"}:
            raise WorkflowError("PLAN_SCHEMA_INVALID", "Unknown action status.", EXIT_USAGE)
        if action.get("executable") and action.get("action") not in ALLOWED_ACTIONS:
            raise WorkflowError("ACTION_NOT_ALLOWED", "Executable action is outside the allowlist: {}".format(action.get("action")), EXIT_USAGE)
        if action.get("executable") and action.get("status") != "ready":
            raise WorkflowError("PLAN_SCHEMA_INVALID", "Executable action must be ready.", EXIT_USAGE)
        if action.get("executable") and not action.get("backupPath"):
            raise WorkflowError("PLAN_SCHEMA_INVALID", "Executable action needs a backup path.", EXIT_USAGE)
        if not isinstance(action.get("target"), dict) or not action["target"].get("path"):
            raise WorkflowError("PLAN_SCHEMA_INVALID", "Action target must contain a relative path.", EXIT_USAGE)


def build_plan(
    audit: Dict[str, Any],
    audit_path: Path,
    confirms: Sequence[str] = (),
    state_root: Optional[Path] = None,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    if audit.get("schemaVersion") != "1.0":
        raise WorkflowError("AUDIT_SCHEMA_INVALID", "Audit schemaVersion must be 1.0.", EXIT_IO)
    if audit.get("summary", {}).get("status") == "FAIL" or audit.get("errors"):
        raise WorkflowError("AUDIT_NOT_ACTIONABLE", "Audit contains blocking errors.", EXIT_IO)
    home_raw = audit.get("host", {}).get("home")
    if not home_raw:
        raise WorkflowError("AUDIT_HOME_MISSING", "Audit does not contain a host home.", EXIT_IO)
    home = Path(home_raw).expanduser().resolve()
    if not home.is_dir():
        raise WorkflowError("HOME_NOT_FOUND", "Audited home is not available.", EXIT_IO)
    try:
        audit_digest = sha256_file(audit_path)
    except OSError as exc:
        raise WorkflowError("AUDIT_READ_FAILED", "Audit file could not be hashed.", EXIT_IO) from exc
    current = now or datetime.now(timezone.utc)
    created = current.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    seed = sha256_bytes((str(audit_digest) + "|" + created + "|" + "|".join(sorted(confirms))).encode("utf-8"))
    plan_id = "plan-{}".format(seed[:20])
    transaction_id = "txn-{}".format(seed[:16])
    txn_root = (state_root.expanduser().resolve() if state_root else _default_transaction_root(home))
    txn_dir = txn_root / transaction_id
    txn_rel = "payload"
    actions: List[Dict[str, Any]] = []
    consumed: set[str] = set()

    duplicate_actions, has_backup_candidate = _duplicate_backup_actions(home, audit, txn_rel)
    actions.extend(duplicate_actions)
    if not duplicate_actions and has_backup_candidate:
        actions.append(
            _action_base(
                "quarantine-redundant-backup",
                "backups/",
                {"sha256": None, "bytes": 0, "mtimeNs": None},
                "Backup retention was flagged, but no byte-identical duplicate hash evidence exists; no move is planned.",
                "R2",
                0,
                "unknown",
                "Cold backup relocation does not establish context savings.",
                None,
                False,
                "pending-confirmation",
                ["duplicate-hash-evidence", "manual-review"],
                source_ref="review-backup-retention",
            )
        )

    session_actions = _archive_session_actions(home, audit, confirms, txn_rel)
    actions.extend(session_actions)
    if not session_actions and any(c.get("action") == "archive-verified-old-sessions" for c in audit.get("candidates", [])):
        actions.append(
            _action_base(
                "archive-verified-old-session",
                "sessions/",
                {"sha256": None, "bytes": 0, "mtimeNs": None},
                "Old-session candidate exists, but no regular session file could be resolved safely.",
                "R2",
                0,
                "unknown",
                "Session relocations are cold and do not claim Token savings.",
                None,
                False,
                "pending-confirmation",
                ["session-file-resolution", "closure-confirmation"],
                source_ref="archive-verified-old-sessions",
            )
        )

    warm_actions, warm_consumed = _warm_quarantine_actions(home, audit, confirms, txn_rel)
    actions.extend(warm_actions)
    consumed.update(warm_consumed)
    actions.extend(_manual_review_actions(audit, consumed))
    _sort_actions(actions)

    target_paths = {
        str(action.get("target", {}).get("path"))
        for action in actions
        if action.get("executable") or action.get("backupPath")
    }
    preserved_files, parse_checks = _preserved_files(home, audit, target_paths)
    existing_edges = []
    for edge in audit.get("referenceGraph", []):
        copied = dict(edge)
        existing_edges.append(copied)
    plan: Dict[str, Any] = {
        "schemaVersion": PLAN_SCHEMA_VERSION,
        "kind": "agent-slim-plan",
        "planId": plan_id,
        "createdAt": created,
        "mode": "dry-run",
        "defaultApplyMode": "dry-run",
        "home": str(home),
        "sourceAudit": {
            "runId": audit.get("runId"),
            "sha256": audit_digest,
            "summaryStatus": audit.get("summary", {}).get("status"),
            "warningCount": audit.get("summary", {}).get("warningCount", 0),
            "unknownCount": audit.get("summary", {}).get("unknownCount", 0),
        },
        "hostCapabilities": probe_codex_home(home, "plan"),
        "transaction": {
            "id": transaction_id,
            "root": str(txn_root),
            "dir": str(txn_dir),
            "manifestPath": str(txn_dir / "manifest.json"),
            "manifestSha256Path": str(txn_dir / "manifest.sha256"),
            "restoreScriptPath": str(txn_dir / "restore.py"),
            "restoreShellPath": str(txn_dir / "restore.sh"),
            "resultPath": str(txn_dir / "result.json"),
        },
        "policy": {
            "allowedActions": list(ALLOWED_ACTIONS),
            "confirmationInput": list(confirms),
            "deleteAllowed": False,
            "vacuumAllowed": False,
            "secretOrProviderChangesAllowed": False,
        },
        "actions": actions,
        "triggerIndex": audit.get("triggerIndex", []),
        "preservedFiles": preserved_files,
        "parseChecks": parse_checks,
        "referenceGraph": existing_edges,
        "ranking": {
            "order": ["ready-before-pending", "lower-risk", "context-estimate", "recoverable-bytes", "target-path"],
            "note": "Benefit estimates sort review order and are not realized-savings claims.",
        },
        "limitations": [
            "Move-only actions do not free disk space and therefore report zero disk savings.",
            "Token values are conservative; no host load-frequency measurement is available in this step.",
            "Old-session closure and low-frequency use require explicit caller confirmation.",
            "The verify command proves the configured test-command contract, not a live host router unless the caller supplies that command.",
        ],
    }
    validate_plan(plan)
    return plan


def _ready_actions(plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        action
        for action in plan.get("actions", [])
        if action.get("executable") is True and action.get("status") == "ready"
    ]


def _manifest_for_plan(plan: Dict[str, Any], plan_path: Path) -> Dict[str, Any]:
    transaction = plan["transaction"]
    transaction_dir = Path(transaction["dir"])
    actions = []
    for action in _ready_actions(plan):
        source_relative = str(action["target"]["path"])
        destination_relative = str(action["backupPath"])
        if not destination_relative:
            raise WorkflowError("PLAN_SCHEMA_INVALID", "Ready action lacks backupPath.", EXIT_USAGE)
        actions.append(
            {
                "id": action["id"],
                "action": action["action"],
                "source": source_relative,
                "destinationRoot": "transaction",
                "destination": destination_relative,
                "sha256": action["target"].get("sha256"),
                "bytes": int(action["target"].get("bytes") or 0),
                "mtimeNs": action["target"].get("mtimeNs"),
                "verification": list(action.get("verification", [])),
            }
        )
    manifest: Dict[str, Any] = {
        "schemaVersion": PLAN_SCHEMA_VERSION,
        "kind": "agent-slim-transaction-manifest",
        "transactionId": transaction["id"],
        "planId": plan["planId"],
        "planSha256": sha256_file(plan_path),
        "createdAt": iso_now(),
        "mode": "apply",
        "status": "prepared",
        "home": plan["home"],
        "transactionDir": transaction_dir.as_posix(),
        "restoreCommand": "python3 restore.py --apply",
        "actions": actions,
    }
    return manifest


def _assert_action_capabilities(plan: Dict[str, Any], action: Dict[str, Any]) -> None:
    """Refuse actions when the adapter cannot prove the needed operation."""
    capabilities = plan.get("hostCapabilities")
    if not isinstance(capabilities, dict):
        capabilities = probe_codex_home(Path(plan["home"]), "plan")
    required = ["safe_move"]
    operation = str(action.get("action") or "")
    if operation == "archive-verified-old-session":
        required.append("session_archive")
    elif operation in {"quarantine-redundant-backup", "quarantine-low-frequency-file"}:
        required.append("quarantine")
    for capability in required:
        try:
            require_capability(capabilities, capability)
        except CapabilityUnavailable as exc:
            raise WorkflowError(
                "CAPABILITY_UNAVAILABLE",
                "{}: {} ({})".format(exc.capability, exc.status, exc.reason),
                EXIT_CONFLICT,
            ) from exc


def _preflight_ready_actions(plan: Dict[str, Any]) -> List[Tuple[Dict[str, Any], Path, Path]]:
    transaction = plan.get("transaction", {})
    transaction_dir = Path(str(transaction.get("dir") or ""))
    if transaction_dir.exists():
        raise WorkflowError("TRANSACTION_EXISTS", "Transaction directory already exists; no overwrite was attempted.", EXIT_CONFLICT)
    home = Path(plan["home"])
    prepared: List[Tuple[Dict[str, Any], Path, Path]] = []
    for action in _ready_actions(plan):
        if action.get("action") not in ALLOWED_ACTIONS:
            raise WorkflowError("ACTION_NOT_ALLOWED", "Action is outside the allowlist.", EXIT_USAGE)
        _assert_action_capabilities(plan, action)
        source_relative = str(action["target"]["path"])
        destination_relative = str(action["backupPath"])
        if action["action"] == "quarantine-redundant-backup" and not source_relative.startswith("backups/"):
            raise WorkflowError("SCOPE_VIOLATION", "Backup quarantine target must be under backups/.", EXIT_CONFLICT)
        if action["action"] == "archive-verified-old-session" and not source_relative.startswith("sessions/"):
            raise WorkflowError("SCOPE_VIOLATION", "Session archive target must be under sessions/.", EXIT_CONFLICT)
        if action["action"] == "quarantine-low-frequency-file" and not source_relative.startswith("skills/"):
            raise WorkflowError("SCOPE_VIOLATION", "Low-frequency quarantine target must be a skill file.", EXIT_CONFLICT)
        source = safe_relative_target(home, source_relative)
        destination = resolve_transaction_path(transaction_dir, destination_relative)
        if not source.is_file():
            raise WorkflowError("TARGET_MISSING", "A planned target no longer exists: {}".format(source_relative), EXIT_CONFLICT)
        if destination.exists():
            raise WorkflowError("DESTINATION_EXISTS", "A transaction destination already exists: {}".format(destination_relative), EXIT_CONFLICT)
        snapshot = _file_snapshot(source)
        if snapshot["sha256"] != action["target"].get("sha256"):
            raise WorkflowError("PLAN_STALE", "Target content changed after planning: {}".format(source_relative), EXIT_CONFLICT)
        prepared.append((action, source, destination))
    return prepared


def _restore_script_source() -> str:
    return '''#!/usr/bin/env python3
"""Offline restore entry generated by Agent Slim. Default mode is dry-run."""

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    manifest_path = HERE / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = (HERE / "manifest.sha256").read_text(encoding="utf-8").split()[0]
    actual = digest(manifest_path)
    if actual != expected:
        print(json.dumps({"status": "FAIL", "code": "MANIFEST_CHECKSUM_MISMATCH"}, ensure_ascii=False))
        return 4
    home = Path(manifest["home"]).resolve()
    operations = []
    for action in manifest["actions"]:
        source = (home / action["source"]).resolve()
        destination = (HERE / action["destination"]).resolve()
        if source.exists():
            if source.is_file() and digest(source) == action["sha256"]:
                operations.append((action, source, destination, "already-restored"))
                continue
            print(json.dumps({"status": "CONFLICT", "source": action["source"], "reason": "SOURCE_HASH_MISMATCH"}, ensure_ascii=False))
            return 3
        if not destination.is_file():
            print(json.dumps({"status": "CONFLICT", "source": action["source"], "reason": "BACKUP_MISSING"}, ensure_ascii=False))
            return 3
        if digest(destination) != action["sha256"]:
            print(json.dumps({"status": "CONFLICT", "source": action["source"], "reason": "BACKUP_HASH_MISMATCH"}, ensure_ascii=False))
            return 3
        operations.append((action, source, destination, "restore"))
    if not args.apply:
        print(json.dumps({"status": "dry-run", "operations": len(operations)}, ensure_ascii=False))
        return 0
    for action, source, destination, operation in operations:
        if operation == "restore":
            source.parent.mkdir(parents=True, exist_ok=True)
            if source.exists():
                print(json.dumps({"status": "CONFLICT", "source": action["source"], "reason": "RACE_DETECTED"}, ensure_ascii=False))
                return 3
            shutil.move(str(destination), str(source))
    print(json.dumps({"status": "restored", "operations": len(operations)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def _write_transaction_artifacts(plan: Dict[str, Any], plan_path: Path) -> Tuple[Dict[str, Any], Path]:
    transaction_dir = Path(plan["transaction"]["dir"])
    try:
        transaction_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise WorkflowError("TRANSACTION_EXISTS", "Transaction directory already exists.", EXIT_CONFLICT) from exc
    manifest = _manifest_for_plan(plan, plan_path)
    manifest_path = transaction_dir / "manifest.json"
    write_json_exclusive(manifest_path, manifest)
    digest = sha256_file(manifest_path)
    write_text_exclusive(transaction_dir / "manifest.sha256", digest + "\n")
    restore_py = transaction_dir / "restore.py"
    write_text_exclusive(restore_py, _restore_script_source())
    try:
        restore_py.chmod(0o755)
    except OSError:
        pass
    write_text_exclusive(
        transaction_dir / "restore.sh",
        '#!/bin/sh\nset -eu\nexec python3 "$(dirname "$0")/restore.py" "$@"\n',
    )
    try:
        (transaction_dir / "restore.sh").chmod(0o755)
    except OSError:
        pass
    write_text_exclusive(
        transaction_dir / "README-restore.txt",
        "Dry-run: python3 restore.py\nApply: python3 restore.py --apply\nShell: sh restore.sh --apply\n",
    )
    return manifest, digest


def append_audit(path: Path, **fields: Any) -> None:
    record = {"time": iso_now(), "project": "agent-slim", "toolVersion": TOOL_VERSION}
    record.update(fields)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    except OSError as exc:
        raise WorkflowError("AUDIT_LOG_WRITE_FAILED", "Dangerous operation audit log could not be written.", EXIT_TRANSACTION) from exc


def _apply_result(plan: Dict[str, Any], mode: str, status: str, applied: Sequence[str], skipped: Sequence[str], failed: Sequence[Dict[str, str]], audit_path: Optional[Path]) -> Dict[str, Any]:
    transaction = plan["transaction"]
    return {
        "schemaVersion": PLAN_SCHEMA_VERSION,
        "kind": "agent-slim-apply-result",
        "createdAt": iso_now(),
        "mode": mode,
        "status": status,
        "planId": plan["planId"],
        "transactionId": transaction["id"],
        "applied": list(applied),
        "skipped": list(skipped),
        "failed": list(failed),
        "quarantine": transaction["dir"],
        "manifest": transaction["manifestPath"],
        "auditPath": str(audit_path) if audit_path else None,
    }


def apply_plan(
    plan_path: Path,
    apply: bool = False,
    audit_log: Optional[Path] = None,
    output: Optional[str] = None,
) -> Dict[str, Any]:
    plan = read_json(plan_path)
    validate_plan(plan)
    ready = _ready_actions(plan)
    if not ready:
        result = _apply_result(plan, "dry-run", "blocked", [], [], [{"code": "NO_READY_ACTIONS", "message": "No confirmed executable action exists."}], audit_log)
        emit_json(result, output)
        return result
    try:
        prepared = _preflight_ready_actions(plan)
    except WorkflowError as exc:
        result = _apply_result(plan, "dry-run" if not apply else "apply", "blocked", [], [], [{"code": exc.code, "message": exc.message}], audit_log)
        emit_json(result, output)
        return result
    if not apply:
        result = _apply_result(plan, "dry-run", "dry-run", [], [action["id"] for action, _, _ in prepared], [], audit_log)
        result["planned"] = [
            {"id": action["id"], "source": action["target"]["path"], "destination": action["backupPath"]}
            for action, _, _ in prepared
        ]
        emit_json(result, output)
        return result
    if audit_log is None:
        audit_log = Path.home() / ".codex" / "audit.log"
    append_audit(
        audit_log,
        event="transaction-begin",
        transactionId=plan["transaction"]["id"],
        planId=plan["planId"],
        mode="apply",
        scope=plan["home"],
        actionCount=len(prepared),
    )
    try:
        manifest, manifest_digest = _write_transaction_artifacts(plan, plan_path)
    except WorkflowError as exc:
        append_audit(audit_log, event="transaction-aborted", transactionId=plan["transaction"]["id"], code=exc.code, result="FAIL")
        result = _apply_result(plan, "apply", "failed", [], [], [{"code": exc.code, "message": exc.message}], audit_log)
        emit_json(result, output)
        return result
    applied: List[str] = []
    try:
        for action, source, destination in prepared:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                raise WorkflowError("DESTINATION_EXISTS", "Destination appeared before move.", EXIT_CONFLICT)
            shutil.move(str(source), str(destination))
            after_hash = sha256_file(destination)
            if after_hash != action["target"]["sha256"]:
                raise WorkflowError("HASH_MISMATCH_AFTER_MOVE", "Moved file hash does not match the plan.", EXIT_TRANSACTION)
            applied.append(action["id"])
            append_audit(
                audit_log,
                event="apply-move",
                transactionId=plan["transaction"]["id"],
                action=action["action"],
                target=action["target"]["path"],
                beforeSha256=action["target"]["sha256"],
                afterSha256=after_hash,
                isolationPath=action["backupPath"],
                result="OK",
            )
    except (OSError, WorkflowError) as exc:
        failed_code = exc.code if isinstance(exc, WorkflowError) else "MOVE_FAILED"
        failed_message = exc.message if isinstance(exc, WorkflowError) else str(exc)
        rollback = _restore_manifest_values(manifest, apply=True, audit_log=audit_log)
        append_audit(
            audit_log,
            event="transaction-failed",
            transactionId=plan["transaction"]["id"],
            code=failed_code,
            rollbackStatus=rollback.get("status"),
            result="FAIL",
        )
        result = _apply_result(plan, "apply", "failed", applied, [], [{"code": failed_code, "message": failed_message}], audit_log)
        result["rollback"] = rollback
        write_json_replace(Path(plan["transaction"]["resultPath"]), result)
        emit_json(result, output)
        return result
    result = _apply_result(plan, "apply", "applied", applied, [], [], audit_log)
    result["manifestSha256"] = manifest_digest
    result["manifest"] = plan["transaction"]["manifestPath"]
    result["restoreCommand"] = "python3 {} --apply".format(Path(plan["transaction"]["restoreScriptPath"]).name)
    write_json_replace(Path(plan["transaction"]["resultPath"]), result)
    append_audit(
        audit_log,
        event="transaction-applied",
        transactionId=plan["transaction"]["id"],
        appliedCount=len(applied),
        manifestSha256=manifest_digest,
        result="OK",
    )
    emit_json(result, output)
    return result


def load_manifest_verified(manifest_path: Path) -> Tuple[Dict[str, Any], str]:
    manifest = read_json(manifest_path)
    checksum_path = manifest_path.with_name("manifest.sha256")
    try:
        expected = checksum_path.read_text(encoding="utf-8").split()[0]
    except (OSError, IndexError) as exc:
        raise WorkflowError("MANIFEST_CHECKSUM_MISSING", "Manifest SHA-256 sidecar is missing.", EXIT_TRANSACTION) from exc
    actual = sha256_file(manifest_path)
    if actual != expected:
        raise WorkflowError("MANIFEST_CHECKSUM_MISMATCH", "Manifest SHA-256 does not match.", EXIT_TRANSACTION)
    return manifest, actual


def _manifest_destination(manifest: Dict[str, Any], action: Dict[str, Any]) -> Path:
    transaction_dir = Path(manifest["transactionDir"]).resolve()
    if action.get("destinationRoot") != "transaction":
        raise WorkflowError("MANIFEST_SCHEMA_INVALID", "Unsupported destination root.", EXIT_TRANSACTION)
    return resolve_transaction_path(transaction_dir, str(action.get("destination") or ""))


def _restore_preflight(manifest: Dict[str, Any]) -> Tuple[List[Tuple[Dict[str, Any], Path, Path, str]], List[Dict[str, str]]]:
    home = Path(manifest["home"]).resolve()
    operations: List[Tuple[Dict[str, Any], Path, Path, str]] = []
    conflicts: List[Dict[str, str]] = []
    for action in manifest.get("actions", []):
        source = safe_relative_target(home, str(action.get("source") or ""))
        destination = _manifest_destination(manifest, action)
        expected_hash = str(action.get("sha256") or "")
        if source.exists():
            if source.is_file() and sha256_file(source) == expected_hash:
                operations.append((action, source, destination, "already-restored"))
            else:
                conflicts.append({"code": "SOURCE_CONFLICT", "target": action.get("source", "")})
            continue
        if not destination.is_file():
            conflicts.append({"code": "BACKUP_MISSING", "target": action.get("source", "")})
            continue
        if sha256_file(destination) != expected_hash:
            conflicts.append({"code": "BACKUP_HASH_MISMATCH", "target": action.get("source", "")})
            continue
        operations.append((action, source, destination, "restore"))
    return operations, conflicts


def _restore_manifest_values(manifest: Dict[str, Any], apply: bool, audit_log: Optional[Path] = None) -> Dict[str, Any]:
    operations, conflicts = _restore_preflight(manifest)
    result: Dict[str, Any] = {
        "schemaVersion": PLAN_SCHEMA_VERSION,
        "kind": "agent-slim-restore-result",
        "createdAt": iso_now(),
        "mode": "apply" if apply else "dry-run",
        "transactionId": manifest.get("transactionId"),
        "operations": [
            {"id": action["id"], "source": action["source"], "operation": operation}
            for action, _, _, operation in operations
        ],
        "conflicts": conflicts,
        "restored": [],
        "alreadyRestored": [action["id"] for action, _, _, operation in operations if operation == "already-restored"],
        "hashMatches": False,
    }
    if conflicts:
        result["status"] = "conflict"
        return result
    if not apply:
        result["status"] = "dry-run"
        return result
    if audit_log is None:
        audit_log = Path.home() / ".codex" / "audit.log"
    append_audit(audit_log, event="restore-begin", transactionId=manifest.get("transactionId"), actionCount=len(operations))
    restored: List[str] = []
    try:
        for action, source, destination, operation in operations:
            if operation != "restore":
                continue
            source.parent.mkdir(parents=True, exist_ok=True)
            if source.exists():
                raise WorkflowError("RESTORE_RACE", "Source appeared during restore; refusing to overwrite.", EXIT_CONFLICT)
            shutil.move(str(destination), str(source))
            if sha256_file(source) != action["sha256"]:
                raise WorkflowError("RESTORE_HASH_MISMATCH", "Restored content hash does not match.", EXIT_TRANSACTION)
            restored.append(action["id"])
            append_audit(
                audit_log,
                event="restore-move",
                transactionId=manifest.get("transactionId"),
                action=action.get("action"),
                target=action.get("source"),
                isolationPath=action.get("destination"),
                afterSha256=action.get("sha256"),
                result="OK",
            )
    except (OSError, WorkflowError) as exc:
        result["status"] = "failed"
        result["failed"] = {"code": getattr(exc, "code", "RESTORE_FAILED"), "message": getattr(exc, "message", str(exc))}
        append_audit(audit_log, event="restore-failed", transactionId=manifest.get("transactionId"), code=result["failed"]["code"], result="FAIL")
        return result
    all_match = True
    for action in manifest.get("actions", []):
        source = safe_relative_target(Path(manifest["home"]).resolve(), str(action["source"]))
        if not source.is_file() or sha256_file(source) != action["sha256"]:
            all_match = False
            break
    result["restored"] = restored
    result["hashMatches"] = all_match
    result["status"] = "restored" if restored else "already-restored"
    if not all_match:
        result["status"] = "failed"
        result["failed"] = {"code": "RESTORE_VERIFY_FAILED", "message": "One or more restored hashes did not match."}
    append_audit(
        audit_log,
        event="restore-complete",
        transactionId=manifest.get("transactionId"),
        restoredCount=len(restored),
        hashMatches=all_match,
        result="OK" if all_match else "FAIL",
    )
    return result


def restore_manifest(manifest_path: Path, apply: bool = False, audit_log: Optional[Path] = None, output: Optional[str] = None) -> Dict[str, Any]:
    manifest, _ = load_manifest_verified(manifest_path)
    result = _restore_manifest_values(manifest, apply=apply, audit_log=audit_log)
    if apply:
        transaction_dir = Path(manifest["transactionDir"])
        result_path = transaction_dir / "result.json"
        try:
            existing = read_json(result_path) if result_path.exists() else {}
        except WorkflowError:
            existing = {}
        existing.update(
            {
                "restoreStatus": result["status"],
                "restoreMode": result["mode"],
                "restoreHashMatches": result.get("hashMatches", False),
                "restoreAt": iso_now(),
                "restoreResult": result,
            }
        )
        write_json_replace(result_path, existing)
    emit_json(result, output)
    return result


def _strict_frontmatter(text: str) -> Dict[str, Any]:
    stripped = text.lstrip("\ufeff")
    lines = stripped.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter fence")
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing frontmatter fence") from exc
    result: Dict[str, Any] = {}
    index = 1
    while index < end:
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if line.startswith((" ", "\t")):
            raise ValueError("unexpected indentation at line {}".format(index + 1))
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if not match:
            raise ValueError("invalid mapping line {}".format(index + 1))
        key, value = match.group(1), (match.group(2) or "").strip()
        if key in result:
            raise ValueError("duplicate key {}".format(key))
        index += 1
        if re.fullmatch(r"[>|][+-]?", value):
            pieces = []
            while index < end and (not lines[index].strip() or lines[index].startswith((" ", "\t"))):
                pieces.append(lines[index].strip())
                index += 1
            result[key] = " ".join(piece for piece in pieces if piece)
        elif value.startswith("[") and value.endswith("]"):
            result[key] = [part.strip().strip("'\"") for part in value[1:-1].split(",") if part.strip()]
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            result[key] = value[1:-1]
        elif value[:1] in ("{", "[", "&", "*", "!", "|", ">"):
            raise ValueError("unsupported YAML construct for key {}".format(key))
        else:
            result[key] = value
    return result


def _parse_check(home: Path, check: Dict[str, str]) -> Dict[str, Any]:
    relative = str(check.get("path") or "")
    kind = str(check.get("kind") or "")
    path = safe_relative_target(home, relative)
    if not path.is_file():
        return {"path": relative, "kind": kind, "status": "FAIL", "reason": "MISSING"}
    try:
        if kind == "json":
            json.loads(path.read_text(encoding="utf-8"))
        elif kind == "yaml-frontmatter-restricted":
            values = _strict_frontmatter(path.read_text(encoding="utf-8"))
            if Path(relative).name.lower() == "skill.md":
                if not values.get("name") or not values.get("description"):
                    raise ValueError("skill frontmatter requires name and description")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return {"path": relative, "kind": kind, "status": "FAIL", "reason": "{}: {}".format(type(exc).__name__, exc)}
    return {"path": relative, "kind": kind, "status": "PASS", "parser": "stdlib/restricted-v1"}


def _run_test_prompts(home: Path, prompts_path: Optional[Path]) -> Dict[str, Any]:
    if prompts_path is None:
        return {
            "status": "SKIPPED",
            "capability": "test-command-only",
            "cases": [],
            "reason": "No --test-prompts file was supplied; trigger and routing behavior was not tested.",
        }
    prompts = read_json(prompts_path)
    cases = prompts.get("test_cases", prompts.get("cases", []))
    if not isinstance(cases, list) or not cases:
        return {"status": "FAIL", "capability": "test-command-only", "cases": [], "reason": "No test cases found."}
    results = []
    any_unknown = False
    any_fail = False
    for index, case in enumerate(cases):
        case_id = str(case.get("id") or "case-{}".format(index + 1))
        prompt = str(case.get("prompt") or "")
        command_value = case.get("command")
        if not prompt or not command_value:
            results.append({"id": case_id, "status": "UNKNOWN", "reason": "Case requires prompt and command."})
            any_unknown = True
            continue
        if isinstance(command_value, list):
            argv = [str(part) for part in command_value]
        elif isinstance(command_value, str):
            argv = shlex.split(command_value, posix=(os.name != "nt"))
        else:
            results.append({"id": case_id, "status": "UNKNOWN", "reason": "Command must be a string or array."})
            any_unknown = True
            continue
        if not argv:
            results.append({"id": case_id, "status": "UNKNOWN", "reason": "Command is empty."})
            any_unknown = True
            continue
        env = dict(os.environ)
        env["AGENT_SLIM_PROMPT"] = prompt
        env["AGENT_SLIM_CASE_ID"] = case_id
        expected = case.get("expect") if isinstance(case.get("expect"), dict) else {}
        expected_exit = int(expected.get("exitCode", case.get("exitCode", 0)))
        expected_text = expected.get("stdoutContains", case.get("stdoutContains"))
        timeout = int(case.get("timeoutSeconds") or DEFAULT_ACTION_TIMEOUT)
        try:
            completed = subprocess.run(
                argv,
                cwd=str(home),
                env=env,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            results.append({"id": case_id, "status": "FAIL", "reason": type(exc).__name__, "promptSha256": sha256_bytes(prompt.encode("utf-8"))})
            any_fail = True
            continue
        passed = completed.returncode == expected_exit
        if expected_text is not None:
            passed = passed and str(expected_text) in completed.stdout
        results.append(
            {
                "id": case_id,
                "status": "PASS" if passed else "FAIL",
                "exitCode": completed.returncode,
                "expectedExitCode": expected_exit,
                "promptSha256": sha256_bytes(prompt.encode("utf-8")),
                "stdoutSha256": sha256_bytes(completed.stdout.encode("utf-8")),
            }
        )
        if not passed:
            any_fail = True
    status = "FAIL" if any_fail else ("UNKNOWN" if any_unknown else "PASS")
    return {"status": status, "capability": "test-command-only", "cases": results}


def _read_existing_result(plan: Dict[str, Any]) -> Dict[str, Any]:
    result_path = Path(plan["transaction"]["resultPath"])
    if result_path.is_file():
        try:
            return read_json(result_path)
        except WorkflowError:
            return {}
    return {}


def verify_plan(plan_path: Path, test_prompts: Optional[Path] = None, phase: str = "auto", output: Optional[str] = None) -> Dict[str, Any]:
    plan = read_json(plan_path)
    validate_plan(plan)
    manifest_path = Path(plan["transaction"]["manifestPath"])
    manifest, manifest_digest = load_manifest_verified(manifest_path)
    existing_result = _read_existing_result(plan)
    if phase == "auto":
        restore_status = existing_result.get("restoreStatus")
        if restore_status in {"restored", "already-restored"}:
            phase = "restored"
        else:
            phase = "applied"
    if phase not in {"applied", "restored"}:
        raise WorkflowError("USAGE", "--phase must be auto, applied, or restored.", EXIT_USAGE)
    home = Path(plan["home"])
    checks: List[Dict[str, Any]] = []
    target_failures: List[str] = []
    backup_failures: List[str] = []
    for action in manifest.get("actions", []):
        source = safe_relative_target(home, str(action.get("source") or ""))
        destination = _manifest_destination(manifest, action)
        if phase == "applied":
            if source.exists():
                target_failures.append(str(action.get("source")))
            if not destination.is_file() or sha256_file(destination) != action.get("sha256"):
                backup_failures.append(str(action.get("source")))
        else:
            if not source.is_file() or sha256_file(source) != action.get("sha256"):
                target_failures.append(str(action.get("source")))
            if destination.exists():
                backup_failures.append(str(action.get("source")))
    checks.append({"id": "target-state", "status": "FAIL" if target_failures else "PASS", "phase": phase, "failed": target_failures})
    checks.append({"id": "backup-sha256", "status": "FAIL" if backup_failures else "PASS", "failed": backup_failures})

    protected_failures = []
    for record in plan.get("preservedFiles", []):
        relative = str(record.get("path") or "")
        path = safe_relative_target(home, relative)
        if not path.is_file() or sha256_file(path) != record.get("sha256"):
            protected_failures.append(relative)
    checks.append({"id": "retained-files", "status": "FAIL" if protected_failures else "PASS", "checked": len(plan.get("preservedFiles", [])), "failed": protected_failures})

    reference_failures = []
    moved_targets = {str(action.get("source")) for action in manifest.get("actions", [])}
    for edge in plan.get("referenceGraph", []):
        if edge.get("scope") != "inside-home" or edge.get("exists") is not True or not edge.get("evidencePath"):
            continue
        relative = str(edge["evidencePath"])
        path = safe_relative_target(home, relative)
        if not path.exists() or relative in moved_targets:
            reference_failures.append(relative)
    checks.append({"id": "reference-integrity", "status": "FAIL" if reference_failures else "PASS", "failed": reference_failures})

    parse_results = [_parse_check(home, check) for check in plan.get("parseChecks", [])]
    parse_failures = [result for result in parse_results if result.get("status") == "FAIL"]
    if not parse_results:
        parse_status = "UNKNOWN"
    else:
        parse_status = "FAIL" if parse_failures else "PASS"
    checks.append(
        {
            "id": "json-yaml-frontmatter",
            "status": parse_status,
            "parser": "JSON stdlib; frontmatter restricted YAML subset",
            "checked": len(parse_results),
            "failures": parse_failures,
        }
    )

    prompt_result = _run_test_prompts(home, test_prompts)
    checks.append({"id": "trigger-routing-regression", **prompt_result})

    blocking = [check["id"] for check in checks if check.get("status") in {"FAIL"}]
    unknown = [check["id"] for check in checks if check.get("status") in {"UNKNOWN", "SKIPPED"}]
    if blocking:
        overall = "FAIL"
    elif unknown:
        overall = "PARTIAL"
    else:
        overall = "PASS"
    report = {
        "schemaVersion": PLAN_SCHEMA_VERSION,
        "kind": "agent-slim-verification",
        "createdAt": iso_now(),
        "planId": plan["planId"],
        "transactionId": plan["transaction"]["id"],
        "phase": phase,
        "checks": checks,
        "summary": {
            "status": overall,
            "blockingFailures": blocking,
            "unknownChecks": unknown,
        },
        "capabilities": {
            "targetAndBackupHashes": "supported",
            "referenceGraph": "supported-from-audit-snapshot",
            "json": "supported-stdlib",
            "yamlFrontmatter": "supported-restricted-subset",
            "triggerRouting": "test-command-only",
            "liveHostTokenMeasurement": "not-performed",
        },
        "artifacts": {"manifestSha256": manifest_digest, "manifest": plan["transaction"]["manifestPath"]},
    }
    emit_json(report, output)
    return report


def result_exit_code(kind: str, result: Dict[str, Any]) -> int:
    status = str(result.get("status") or "")
    if kind == "apply":
        if status in {"applied", "dry-run"}:
            return EXIT_OK
        if status in {"blocked", "failed"}:
            return EXIT_CONFLICT if result.get("failed", [{}])[0].get("code") in {"DESTINATION_EXISTS", "TRANSACTION_EXISTS", "PLAN_STALE", "SCOPE_VIOLATION", "TARGET_MISSING"} else EXIT_TRANSACTION
    if kind == "restore":
        if status in {"restored", "already-restored", "dry-run"}:
            return EXIT_OK
        if status == "conflict":
            return EXIT_CONFLICT
        return EXIT_TRANSACTION
    if kind == "verify":
        verify_status = str(result.get("summary", {}).get("status") or status)
        if verify_status == "PASS":
            return EXIT_OK
        if verify_status == "PARTIAL":
            return EXIT_WARNING
        return EXIT_VERIFY_FAILED
    return EXIT_OK
