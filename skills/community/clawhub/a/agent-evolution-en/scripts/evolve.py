#!/usr/bin/env python3
"""Capture and retrieve project memory, and stage verified memory revisions."""

import argparse
import hashlib
import json
import math
import os
import re
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


STATE_NAME = ".agent-evolution"
HEADER = re.compile(r"<!-- agent-evolution version: (initial|[a-f0-9]{12}) -->\n\n")
TRIAL_ID = re.compile(r"[a-f0-9]{12}")
INITIAL_MEMORY = "# Project Memory\n\n## Semantic Memory\n\n## Procedural Memory\n"


def checked_path(path):
    if path.is_symlink():
        raise ValueError(f"Refusing to use a symlink: {path}")
    return path


def read_text(path):
    return checked_path(path).read_bytes().decode("utf-8")


def read_json(path):
    return json.loads(read_text(path))


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def atomic_write(path, text):
    checked_path(path)
    descriptor, filename = tempfile.mkstemp(dir=path.parent, prefix=".memory-")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as output:
            output.write(text)
        os.replace(filename, path)
    finally:
        Path(filename).unlink(missing_ok=True)


def write_json(path, value):
    atomic_write(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def now():
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def locked(state):
    lock = state / ".write-lock"
    try:
        lock.mkdir()
    except FileExistsError as error:
        raise ValueError("Another write is in progress or the write lock is stale.") from error
    try:
        yield
    finally:
        lock.rmdir()


def revision_path(state, version):
    if version != "initial" and not TRIAL_ID.fullmatch(version):
        raise ValueError("Invalid version ID.")
    return checked_path(state / "versions") / f"{version}.json"


def revision(state, version):
    return read_json(revision_path(state, version))


def active(state):
    text = read_text(state / "MEMORY.md")
    marker = HEADER.match(text)
    if not marker:
        raise ValueError("MEMORY.md has no valid version marker.")
    version = marker.group(1)
    memory = text[marker.end():]
    if digest(memory) != revision(state, version)["sha256"]:
        raise ValueError("MEMORY.md changed outside the revision tool. Reconcile the edit before continuing.")
    return version, memory


def activate(state, version, memory):
    atomic_write(state / "MEMORY.md", f"<!-- agent-evolution version: {version} -->\n\n" + memory)


def initialize(state, initial_file):
    for folder in ("trials", "versions"):
        checked_path(state / folder).mkdir(exist_ok=True)
    if (state / "MEMORY.md").exists():
        version, _ = active(state)
        if initial_file is not None:
            raise ValueError("Project memory is already initialized.")
        return {"version": version, "file": str(state / "MEMORY.md")}

    first = revision_path(state, "initial")
    if first.exists():
        record = revision(state, "initial")
        memory = record["memory"]
        if initial_file is not None and read_text(initial_file) != memory:
            raise ValueError("The recorded initial version differs from the supplied file.")
    else:
        memory = INITIAL_MEMORY if initial_file is None else read_text(initial_file)
        if not memory.strip():
            raise ValueError("The supplied initial memory is empty.")
        write_json(first, {"parent": None, "sha256": digest(memory), "memory": memory, "created_at": now()})
    activate(state, "initial", memory)
    return {"version": "initial", "file": str(state / "MEMORY.md")}


ENTRY_STATUS = {
    "artifact": "available",
    "fact": "verified",
    "decision": "confirmed",
    "hypothesis": "candidate",
    "practice": "candidate",
    "observation": "observed",
}
REUSABLE_KINDS = {"artifact", "fact", "decision"}
ENTRY_REQUIRED_TEXT = ("title", "summary", "scope", "source")
ENTRY_OPTIONAL_TEXT = ("trigger", "review_when")


def capture(state, entry_file):
    raw = read_json(entry_file)
    if not isinstance(raw, dict):
        raise ValueError("A memory entry must be a JSON object.")
    allowed = {"kind", "supersedes", *ENTRY_REQUIRED_TEXT, *ENTRY_OPTIONAL_TEXT}
    unknown = raw.keys() - allowed
    if unknown:
        raise ValueError(f"Unrecognized memory entry fields: {', '.join(sorted(unknown))}.")

    kind = raw.get("kind")
    if not isinstance(kind, str) or kind not in ENTRY_STATUS:
        raise ValueError("Invalid memory entry kind.")
    entry = {"kind": kind}
    for field in ENTRY_REQUIRED_TEXT + ENTRY_OPTIONAL_TEXT:
        if field in ENTRY_OPTIONAL_TEXT and field not in raw:
            continue
        value = raw.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"A memory entry needs a nonempty {field}.")
        entry[field] = value.strip()

    entries = checked_path(state / "entries")
    replaces = raw.get("supersedes")
    if replaces is not None:
        if not isinstance(replaces, str) or not TRIAL_ID.fullmatch(replaces):
            raise ValueError("supersedes must be an existing memory entry ID.")
        previous = read_json(entries / f"{replaces}.json")
        if previous["scope"] != entry["scope"]:
            raise ValueError("A replacement must have the same project scope.")
        if previous["kind"] in REUSABLE_KINDS and kind not in REUSABLE_KINDS:
            raise ValueError("A provisional entry cannot replace a reusable one.")
        entry["supersedes"] = replaces

    canonical = json.dumps(entry, ensure_ascii=False, sort_keys=True)
    identifier = digest(canonical)[:12]
    path = checked_path(entries / f"{identifier}.json")
    if path.exists():
        existing = read_json(path)
        if any(existing.get(key) != value for key, value in entry.items()):
            raise ValueError("A different entry has the same ID.")
        return {"id": identifier, "status": existing["status"], "file": str(path), "created": False}

    entries.mkdir(exist_ok=True)
    status = ENTRY_STATUS[kind]
    write_json(path, {"id": identifier, "status": status, "created_at": now(), **entry})
    return {"id": identifier, "status": status, "file": str(path), "created": True}


def recall(state, query, limit, include_unverified, scope):
    terms = set(query.casefold().split())
    if not terms:
        raise ValueError("Provide at least one search keyword.")
    if not 1 <= limit <= 30:
        raise ValueError("The result limit must be from 1 to 30.")

    entries = checked_path(state / "entries")
    records = []
    for path in entries.glob("*.json"):
        if TRIAL_ID.fullmatch(path.stem):
            records.append((path, read_json(path)))
    superseded = {record["supersedes"] for _, record in records if "supersedes" in record}
    matches = []
    search_fields = ("title", "summary", "scope", "source", "trigger")
    for path, entry in records:
        if entry["id"] in superseded or (not include_unverified and entry["kind"] not in REUSABLE_KINDS):
            continue
        if scope is not None and entry["scope"] != scope:
            continue
        content = " ".join(entry.get(field, "") for field in search_fields).casefold()
        score = sum(term in content for term in terms)
        if score:
            matches.append((score, entry["created_at"], entry["id"], {**entry, "file": str(path)}))
    matches.sort(reverse=True, key=lambda match: match[:3])
    return {"matches": [match[3] for match in matches[:limit]]}


def stage(state, proposal):
    version, baseline = active(state)
    candidate = read_text(proposal)
    if not candidate.strip() or candidate == baseline:
        raise ValueError("The candidate must be nonempty and different from the baseline.")

    trial_id = uuid4().hex[:12]
    trials = checked_path(state / "trials")
    manifest = {
        "trial": trial_id,
        "baseline_version": version,
        "baseline_sha256": digest(baseline),
        "candidate_sha256": digest(candidate),
        "created_at": now(),
    }
    with tempfile.TemporaryDirectory(dir=trials, prefix=".stage-") as staging:
        pending = Path(staging) / "trial"
        pending.mkdir()
        atomic_write(pending / "baseline.md", baseline)
        atomic_write(pending / "candidate.md", candidate)
        write_json(pending / "manifest.json", manifest)
        pending.rename(trials / trial_id)
    return manifest


def validate_evaluation(evaluation, manifest):
    for key in ("trial", "baseline_sha256", "candidate_sha256"):
        if evaluation.get(key) != manifest[key]:
            raise ValueError(f"Evaluation does not match the staged {key}.")

    cases = evaluation.get("cases")
    if not isinstance(cases, list):
        raise ValueError("The evaluation must contain a list of paired cases.")
    seen = set()
    has_regression_case = False
    holdout_gain = False
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("Each case must be an object.")
        for key in ("id", "criterion", "baseline_evidence", "candidate_evidence"):
            if not isinstance(case.get(key), str) or not case[key].strip():
                raise ValueError(f"Each case needs a nonempty {key}.")
        if case["id"] in seen:
            raise ValueError(f"Duplicate case ID: {case['id']}")
        seen.add(case["id"])
        kind = case.get("kind")
        if kind not in {"holdout", "regression"}:
            raise ValueError("Use held-out or regression cases for the adoption decision.")
        for key in ("before", "after"):
            score = case.get(key)
            if type(score) not in (int, float) or not 0 <= score <= 1 or not math.isfinite(score):
                raise ValueError(f"{case['id']} has an invalid {key} score.")
        if case["after"] < case["before"]:
            raise ValueError(f"The candidate regressed on {case['id']}.")
        has_regression_case |= kind == "regression"
        holdout_gain |= kind == "holdout" and case["after"] > case["before"]

    if not has_regression_case or not holdout_gain:
        raise ValueError("Adoption needs a regression case and improvement on a held-out case.")


def promote(state, trial_id, result_path):
    if not TRIAL_ID.fullmatch(trial_id):
        raise ValueError("Invalid trial ID.")
    trial = checked_path(checked_path(state / "trials") / trial_id)
    manifest = read_json(trial / "manifest.json")
    if manifest.get("trial") != trial_id:
        raise ValueError("The trial directory and manifest do not match.")
    version, baseline = active(state)
    if version != manifest["baseline_version"] or digest(baseline) != manifest["baseline_sha256"]:
        raise ValueError("Active memory changed since staging. Compare against the current baseline.")
    if digest(read_text(trial / "baseline.md")) != manifest["baseline_sha256"]:
        raise ValueError("The baseline file changed after staging.")
    candidate = read_text(trial / "candidate.md")
    if digest(candidate) != manifest["candidate_sha256"]:
        raise ValueError("The candidate file changed after staging.")

    evaluation = read_json(result_path)
    if not isinstance(evaluation, dict):
        raise ValueError("The evaluation must be a JSON object.")
    validate_evaluation(evaluation, manifest)
    record = {
        "parent": version,
        "sha256": manifest["candidate_sha256"],
        "memory": candidate,
        "evaluation": evaluation,
        "created_at": now(),
    }
    path = revision_path(state, trial_id)
    if path.exists():
        saved = read_json(path)
        if any(saved.get(key) != record[key] for key in ("parent", "sha256", "memory", "evaluation")):
            raise ValueError("This trial already has a different saved evaluation or revision.")
    else:
        write_json(path, record)
    activate(state, trial_id, candidate)
    return {"version": trial_id, "parent": version, "file": str(state / "MEMORY.md")}


def rollback(state, target):
    version, _ = active(state)
    destination = target if target is not None else revision(state, version)["parent"]
    if destination is None or destination == version:
        raise ValueError("There is no different version to restore.")
    record = revision(state, destination)
    if digest(record["memory"]) != record["sha256"]:
        raise ValueError("The stored revision does not match its recorded digest.")
    activate(state, destination, record["memory"])
    return {"version": destination, "restored_from": version, "file": str(state / "MEMORY.md")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("initial_memory", type=Path, nargs="?")
    subparsers.add_parser("status")
    capture_parser = subparsers.add_parser("capture")
    capture_parser.add_argument("entry", type=Path)
    recall_parser = subparsers.add_parser("recall")
    recall_parser.add_argument("query")
    recall_parser.add_argument("--limit", type=int, default=5)
    recall_parser.add_argument("--scope", help="Return entries with this exact recorded scope.")
    recall_parser.add_argument("--include-unverified", action="store_true")
    stage_parser = subparsers.add_parser("stage")
    stage_parser.add_argument("candidate", type=Path)
    promote_parser = subparsers.add_parser("promote")
    promote_parser.add_argument("trial")
    promote_parser.add_argument("results", type=Path)
    rollback_parser = subparsers.add_parser("rollback")
    rollback_parser.add_argument("--to")
    args = parser.parse_args()

    try:
        project = args.project.resolve(strict=True)
        if not project.is_dir():
            raise ValueError("The project must be an existing directory.")
        state = checked_path(project / STATE_NAME)
        if args.command == "init":
            state.mkdir(exist_ok=True)
        elif not state.is_dir():
            raise ValueError("Initialize project memory first.")

        if args.command == "status":
            version, memory = active(state)
            result = {"version": version, "sha256": digest(memory), "file": str(state / "MEMORY.md")}
        elif args.command == "recall":
            result = recall(state, args.query, args.limit, args.include_unverified, args.scope)
        else:
            with locked(state):
                if args.command == "init":
                    result = initialize(state, args.initial_memory)
                elif args.command == "capture":
                    result = capture(state, args.entry)
                elif args.command == "stage":
                    result = stage(state, args.candidate)
                elif args.command == "promote":
                    result = promote(state, args.trial, args.results)
                else:
                    result = rollback(state, args.to)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
