#!/usr/bin/env python3
"""Locked, atomic records and replayable history for management extensions.

History hashes detect inconsistency, not authenticated identity or malicious
rewriting of an entire repository. Git review remains the external trust anchor.
"""

from contextlib import contextmanager
import copy
from datetime import date, datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess

from pm_common import requirement_definitions, requirement_files, write_json_atomic, write_text_atomic


# Mutable registries and their generated views are not independent proof. Stage a
# reviewed report/snapshot elsewhere in the project before sealing it as evidence.
MANAGEMENT_STATE = {
    "00-project/management/management.json",
    "00-project/management/milestones.json", "00-project/management/milestones.md",
    "09-risks/risks.json", "09-risks/risks.md",
    "07-quality/problems.json", "07-quality/problems.md",
    "01-requirements/intake/sources.json", "01-requirements/intake/sources.md",
    "01-requirements/intake/compliance.json", "01-requirements/intake/compliance.md",
}


class RecordError(ValueError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True, allow_nan=False).encode()).hexdigest()


def require_text(value, label):
    if not isinstance(value, str) or not value.strip() or any(ord(c) < 32 for c in value):
        raise RecordError(f"{label} must be nonempty single-line text")
    return value.strip()


def require_strings(value, label):
    if not isinstance(value, list):
        raise RecordError(f"{label} must be a list of strings")
    result = [require_text(item, label) for item in value]
    if len(set(result)) != len(result):
        raise RecordError(f"{label} contains duplicate values")
    return result


def require_date(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise RecordError(f"{label} must use YYYY-MM-DD")
    try:
        date.fromisoformat(value)
    except ValueError:
        raise RecordError(f"{label} is not a valid calendar date") from None
    return value


def project_file(project, relative, must_exist=True):
    root = Path(project).resolve()
    if not root.is_dir():
        raise RecordError("Project directory does not exist")
    value = str(relative)
    logical = PurePosixPath(value)
    if (not logical.parts or logical.is_absolute() or "\\" in value or ":" in value
            or any(ord(char) < 32 for char in value)
            or any(p == ".." or p.casefold() == ".git" for p in logical.parts)):
        raise RecordError("Path must be relative to the project without traversal or Git metadata")
    path = root.joinpath(*logical.parts)
    resolved = path.resolve()
    if (resolved == root or not resolved.is_relative_to(root) or
            any(part.casefold() == ".git" for part in resolved.relative_to(root).parts)):
        raise RecordError("Path resolves outside the allowed project files")
    if must_exist and not path.is_file():
        raise RecordError(f"Project file is missing: {logical.as_posix()}")
    return path


def seal_artifact(project, relative):
    path = project_file(project, relative)
    root = Path(project).resolve()
    logical = path.relative_to(root).as_posix()
    resolved = path.resolve().relative_to(root).as_posix()
    if any(value.casefold() in MANAGEMENT_STATE or value.casefold().endswith(".lock")
           for value in (logical, resolved)):
        raise RecordError("Management state, generated views and locks cannot be sealed as independent evidence")
    hashed = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hashed.update(chunk)
    return {"path": logical, "sha256": hashed.hexdigest()}


def artifact_errors(project, artifact):
    try:
        if not isinstance(artifact, dict) or set(artifact) != {"path", "sha256"}:
            raise RecordError("Artifact must contain path and sha256")
        if not isinstance(artifact["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", artifact["sha256"]):
            raise RecordError("Artifact SHA-256 is invalid")
        if seal_artifact(project, artifact["path"]) != artifact:
            raise RecordError("Artifact content or path differs from its sealed record")
        return []
    except (RecordError, OSError, TypeError) as exc:
        return [str(exc)]


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise RecordError("Duplicate JSON object key")
        result[key] = value
    return result


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=_pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(RecordError("Nonfinite JSON value")))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RecordError(f"Cannot read registry JSON: {Path(path).name}") from exc


def previously_managed(project, relative):
    try:
        result = subprocess.run(["git", "-C", str(project), "log", "--all", "-1", "--format=%H", "--", str(relative)],
                                capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RecordError("Cannot inspect Git history for previously managed data") from exc
    if result.returncode:
        root = Path(project).resolve()
        if (any((parent / ".git").exists() for parent in [root, *root.parents]) or
                os.environ.get("GIT_DIR") or os.environ.get("GIT_WORK_TREE")):
            raise RecordError("Git history is unavailable; previously managed data cannot be ruled out")
        return False  # A genuine standalone legacy project has no Git history.
    return bool(result.stdout.strip())


def task_records(project):
    data = read_json(project_file(project, "00-project/management/TASKS.json"))
    if not isinstance(data, dict) or not isinstance(data.get("tasks"), list):
        raise RecordError("Invalid task registry")
    result = {}
    for task in data["tasks"]:
        if not isinstance(task, dict):
            raise RecordError("Invalid task record")
        tid = require_text(task.get("id"), "Task id")
        if (tid in result or not isinstance(task.get("status"), str) or
                task["status"] not in {"BACKLOG", "READY", "IN_PROGRESS", "BLOCKED", "REVIEW", "REWORK", "DONE", "CANCELLED"}):
            raise RecordError("Duplicate task ID or invalid task state")
        result[tid] = task
    return result


def link_errors(project, record):
    errors = []
    for key in ("tasks", "requirements", "changes"):
        try:
            links = require_strings(record.get(key, []), key)
            if not links:
                continue
            if key == "tasks":
                known = set(task_records(project))
            elif key == "requirements":
                project_file(project, "01-requirements", must_exist=False)
                for path in requirement_files(Path(project).resolve()):
                    project_file(project, path.relative_to(Path(project).resolve()).as_posix())
                definitions = requirement_definitions(project)
                known = {r["id"] for r in definitions if r.get("scheme") == "V1.1"}
            else:
                data = read_json(project_file(project, "08-configuration/CHANGE-REQUESTS.json"))
                if not isinstance(data, dict) or not isinstance(data.get("changes"), list):
                    raise RecordError("Invalid change registry")
                known = set()
                for change in data["changes"]:
                    if not isinstance(change, dict) or not isinstance(change.get("Change_ID"), str):
                        raise RecordError("Invalid change record")
                    known.add(change["Change_ID"])
            for value in links:
                if value not in known:
                    errors.append(f"Unknown {key} reference: {value}")
        except (RecordError, OSError, KeyError, TypeError) as exc:
            errors.append(str(exc))
    return errors


def get_record(data, record_id):
    for record in data["records"]:
        if record["id"] == record_id:
            return record
    raise RecordError(f"Record does not exist: {record_id}")


def add_record(data, prefix, title, owner, status, **fields):
    if any(key in fields for key in ("id", "created_at", "updated_at")):
        raise RecordError("Cannot override record identity or timestamps")
    stamp = now()
    record = {"id": f"{prefix}-{data['next_id']:04d}", "title": require_text(title, "title"),
              "owner": require_text(owner, "owner"), "status": require_text(status, "status"),
              "created_at": stamp, "updated_at": stamp, **copy.deepcopy(fields)}
    data["next_id"] += 1
    data["records"].append(record)
    return record


def cell(value):
    if isinstance(value, (dict, list)):
        value = json.dumps(value, sort_keys=True, ensure_ascii=False)
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def write_view(project, relative, content):
    write_text_atomic(project_file(project, relative, must_exist=False), content)


def control_path(project, relative):
    """Registry and lock identity cannot be redirected through filesystem links."""
    path = project_file(project, relative, must_exist=False)
    current = Path(project).resolve()
    for component in path.relative_to(current).parts:
        current = current / component
        if current.is_symlink() or (hasattr(current, "is_junction") and current.is_junction()):
            raise RecordError("Management registry and lock paths must not contain symlinks or junctions")
    return path


@contextmanager
def _lock(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as stream:
        if os.name == "nt":
            import msvcrt
            if path.stat().st_size == 0:
                stream.write(b"\0")
                stream.flush()
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if os.name == "nt":
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


class Store:
    def __init__(self, project, relative, kind, prefix):
        self.project = Path(project).resolve()
        self.relative, self.kind, self.prefix = str(relative), kind, prefix
        self.path = control_path(self.project, self.relative)
        lock_relative = str(PurePosixPath(self.relative).with_name("." + self.path.stem.lower() + ".lock"))
        self.lock_relative = lock_relative
        self.lock_path = control_path(self.project, lock_relative)

    @contextmanager
    def locked(self):
        control_path(self.project, self.relative)
        control_path(self.project, self.lock_relative)
        with _lock(self.lock_path):
            yield

    def exists(self):
        return self.path.exists()

    def errors(self, data):
        errors = []
        try:
            if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1 or data.get("kind") != self.kind:
                return [f"Invalid {self.kind} registry schema or kind"]
            if not isinstance(data.get("records"), list) or not isinstance(data.get("history"), list):
                return ["Registry records and history must be lists"]
            if type(data.get("next_id")) is not int or data["next_id"] < 1:
                return ["Registry next_id must be a positive integer"]
            records = {}
            sequence = []
            for record in data["records"]:
                if not isinstance(record, dict):
                    errors.append("Record must be an object")
                    continue
                rid = record.get("id")
                if not isinstance(rid, str) or not re.fullmatch(re.escape(self.prefix) + r"-\d{4,}", rid):
                    errors.append("Invalid record identifier")
                    continue
                if rid in records:
                    errors.append(f"Duplicate record identifier: {rid}")
                records[rid] = record
                sequence.append(int(rid.rsplit("-", 1)[1]))
                for key in ("title", "owner", "status"):
                    require_text(record.get(key), key)
                for key in ("created_at", "updated_at"):
                    stamp = datetime.fromisoformat(record.get(key, ""))
                    if stamp.tzinfo is None:
                        errors.append(f"{rid}: {key} needs timezone")
                if record["updated_at"] < record["created_at"]:
                    errors.append(f"{rid}: updated_at precedes creation")
            if data["next_id"] != len(records) + 1 or sorted(sequence) != list(range(1, len(records) + 1)):
                errors.append("Record identity sequence or next_id is inconsistent")
            replay, previous_hash = {}, None
            for index, event in enumerate(data["history"], 1):
                if not isinstance(event, dict):
                    errors.append("History event must be an object")
                    continue
                if set(event) != {"sequence", "at", "actor", "action", "record_id", "before_sha256", "after", "previous_hash", "hash"}:
                    errors.append("History event fields are invalid")
                    continue
                if type(event["sequence"]) is not int or event["sequence"] != index:
                    errors.append("History sequence is discontinuous")
                require_text(event["actor"], "History actor")
                require_text(event["action"], "History action")
                if datetime.fromisoformat(event["at"]).tzinfo is None:
                    errors.append("History timestamp needs timezone")
                if event["previous_hash"] != previous_hash:
                    errors.append("History hash chain is discontinuous")
                expected_hash = digest({k: v for k, v in event.items() if k != "hash"})
                if event["hash"] != expected_hash:
                    errors.append("History event hash mismatch")
                previous_hash = event["hash"]
                rid, after = event["record_id"], event["after"]
                if not isinstance(rid, str) or not isinstance(after, dict) or after.get("id") != rid:
                    errors.append("History record identity is invalid")
                    continue
                before = replay.get(rid)
                if event["before_sha256"] != (digest(before) if before else None):
                    errors.append(f"{rid}: history before-state mismatch")
                if before and after.get("created_at") != before.get("created_at"):
                    errors.append(f"{rid}: creation timestamp changed")
                if after.get("updated_at") != event["at"]:
                    errors.append(f"{rid}: history timestamp differs from updated record")
                replay[rid] = after
            if replay != records:
                errors.append("Authoritative records differ from replayed history")
        except (RecordError, ValueError, TypeError, KeyError, OverflowError) as exc:
            errors.append("Malformed registry: " + str(exc))
        return errors

    def read(self):
        data = read_json(control_path(self.project, self.relative))
        errors = self.errors(data)
        if errors:
            raise RecordError("; ".join(errors))
        return data

    def initialize(self, actor):
        require_text(actor, "actor")
        with self.locked():
            if self.exists():
                return self.read()
            if self.path.is_symlink() or previously_managed(self.project, self.relative):
                raise RecordError("Missing previously managed registry; restore it from Git instead of reinitializing")
            data = {"schema_version": 1, "kind": self.kind, "next_id": 1, "records": [], "history": []}
            write_json_atomic(self.path, data)
            return data

    def update(self, actor, action, operation, validator=None):
        actor, action = require_text(actor, "actor"), require_text(action, "action")
        with self.locked():
            before = self.read()
            working = copy.deepcopy(before)
            record_id = operation(working)
            require_text(record_id, "Changed record ID")
            if working["history"] != before["history"] or any(working.get(k) != before.get(k) for k in before if k not in ("records", "next_id", "history")) or set(working) != set(before):
                raise RecordError("Mutation attempted to change registry metadata or history")
            before_map = {r["id"]: r for r in before["records"]}
            after_map = {r["id"]: r for r in working["records"]}
            if len(after_map) != len(working["records"]) or set(before_map) - set(after_map):
                raise RecordError("Deleting or duplicating records is not allowed")
            changed = {rid for rid in after_map if after_map[rid] != before_map.get(rid)}
            if changed != {record_id}:
                raise RecordError("A mutation must change exactly one record")
            stamp = now()
            after_map[record_id]["updated_at"] = stamp
            previous = before_map.get(record_id)
            event = {"sequence": len(before["history"]) + 1, "at": stamp, "actor": actor,
                     "action": action, "record_id": record_id,
                     "before_sha256": digest(previous) if previous else None,
                     "after": copy.deepcopy(after_map[record_id]),
                     "previous_hash": before["history"][-1]["hash"] if before["history"] else None}
            event["hash"] = digest(event)
            working["history"].append(event)
            errors = self.errors(working)
            if validator:
                errors.extend(validator(self.project, working))
            if errors:
                raise RecordError("; ".join(sorted(set(errors))))
            # Recheck containment immediately before replacing the canonical file.
            control_path(self.project, self.relative)
            write_json_atomic(self.path, working)
            return working
