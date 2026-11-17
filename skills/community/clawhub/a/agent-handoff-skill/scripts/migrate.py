#!/usr/bin/env python3
"""Remove a verified repository-local handoff deployment, preserving task data."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

BEGIN = b"<!-- handoff:begin -->"
END = b"<!-- handoff:end -->"
LOCK = ".agents/handoff.lock"
OLD_TRANSACTION = ".agents/handoff.transaction"
JOURNAL = ".agents/handoff-migration.json"
FILES = {".agents/handoff/PROTOCOL.md", ".agents/handoff/ledger.sh", ".agents/tasks/TEMPLATE.md",
         ".agents/skills/handoff/SKILL.md", ".agents/skills/handoff/ledger.sh", "tools/ledger.sh"}
FRAGMENTS = {"AGENTS.md#handoff", "CLAUDE.md#handoff", ".claude/skills/handoff#target"}


class MigrationError(RuntimeError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def decode(text: str) -> bytes:
    return base64.b64decode(text, validate=True)


def repo_root(path: Path) -> Path:
    result = subprocess.run(["git", "-C", str(path), "rev-parse", "--show-toplevel"],
                            capture_output=True, text=True, check=False)
    if result.returncode:
        raise MigrationError(f"Not a Git worktree: {path}")
    return Path(result.stdout.removesuffix("\n")).resolve()


def safe_path(root: Path, relative: str, *, link: bool = False) -> Path:
    path = root / relative
    for parent in path.parents:
        if parent == root:
            break
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            raise MigrationError(f"Unsafe managed directory: {parent}")
    if path.is_symlink():
        if not link:
            raise MigrationError(f"Managed file became a symlink: {relative}")
    elif path.exists() and (link or not path.is_file()):
        raise MigrationError(f"Unexpected managed object type: {relative}")
    elif path.exists() and path.stat().st_nlink != 1:
        raise MigrationError(f"Managed file is hard-linked: {relative}")
    return path


def read_optional(path: Path) -> bytes | None:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        return None


def block(data: bytes) -> tuple[bytes, bytes]:
    starts, ends, offset = [], [], 0
    for line in data.splitlines(keepends=True):
        if line.rstrip(b"\n") == BEGIN:
            starts.append(offset)
        if line.rstrip(b"\n") == END:
            ends.append(offset + len(line))
        offset += len(line)
    if len(starts) != 1 or len(ends) != 1 or ends[0] <= starts[0]:
        raise MigrationError("AGENTS.md must contain exactly one complete handoff block")
    selected = data[starts[0]:ends[0]]
    normalized = selected if selected.endswith(b"\n") else selected + b"\n"
    return normalized, data[:starts[0]] + data[ends[0]:]


def parse_lock(data: bytes) -> tuple[dict[str, str], dict[str, str]]:
    version = None
    sections = {"managed_files:": {}, "managed_fragments:": {}}
    current = None
    seen_sections = set()
    for line in data.decode("utf-8").splitlines():
        if line.startswith("version: ") and version is None:
            version = line[9:]
        elif line in sections and line not in seen_sections:
            current = sections[line]
            seen_sections.add(line)
        elif line.startswith("  ") and current is not None:
            try:
                key, value = line[2:].rsplit(": ", 1)
            except ValueError as exc:
                raise MigrationError("Invalid installation lock entry") from exc
            if key in current or not (re.fullmatch("[0-9a-f]{64}", value) or value == "missing"):
                raise MigrationError(f"Invalid or duplicate lock entry: {key}")
            current[key] = value
        elif line:
            raise MigrationError("Unrecognized installation lock format")
    if version != "unknown":
        if not version or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise MigrationError("Invalid installed version")
        supported = Path(__file__).resolve().parents[1] / "VERSION"
        if tuple(map(int, version.split("."))) > tuple(map(int, supported.read_text().strip().split("."))):
            raise MigrationError("Installed deployment is newer than this migration tool")
    files, fragments = sections.values()
    if not set(files) <= FILES or not set(fragments) <= FRAGMENTS:
        raise MigrationError("Installation lock contains unknown managed paths")
    base = {".agents/tasks/TEMPLATE.md"}
    fragment_keys = {"AGENTS.md#handoff", "CLAUDE.md#handoff"}
    if ".agents/handoff/PROTOCOL.md" in files:
        expected = base | {".agents/handoff/PROTOCOL.md", ".agents/handoff/ledger.sh"}
    else:
        ledgers = set(files) & {".agents/skills/handoff/ledger.sh", "tools/ledger.sh"}
        if not ledgers or not any(files[p] != "missing" for p in ledgers):
            raise MigrationError("Incomplete legacy ledger registration")
        expected = base | {".agents/skills/handoff/SKILL.md"} | ledgers
        fragment_keys.add(".claude/skills/handoff#target")
    if set(files) != expected or set(fragments) != fragment_keys:
        raise MigrationError("Incomplete installation lock; ownership cannot be established")
    for key, value in {**files, **fragments}.items():
        if value == "missing" and key != ".agents/skills/handoff/ledger.sh":
            raise MigrationError(f"Missing ownership hash: {key}")
    return files, fragments


def file_hash(root: Path, relative: str) -> str:
    value = read_optional(safe_path(root, relative))
    return digest(value) if value is not None else "missing"


def link_hash(root: Path) -> str:
    path = safe_path(root, ".claude/skills/handoff", link=True)
    return digest(os.readlink(path).encode()) if path.is_symlink() else "missing"


def expected_actions(lock_data: bytes, agents_before: bytes) -> list[dict]:
    files, fragments = parse_lock(lock_data)
    old_block, remaining = block(agents_before)
    if digest(old_block) != fragments["AGENTS.md#handoff"]:
        raise MigrationError("AGENTS.md handoff block has local modifications")
    actions = [{"kind": "delete", "path": name, "old": value, "new": "missing"}
               for name, value in sorted(files.items()) if value != "missing"]
    if ".claude/skills/handoff#target" in fragments:
        expected_link = digest(b"../../.agents/skills/handoff")
        if fragments[".claude/skills/handoff#target"] != expected_link:
            raise MigrationError("Unrecognized legacy Claude link")
        actions.append({"kind": "unlink", "path": ".claude/skills/handoff", "old": expected_link, "new": "missing"})
    actions.append({"kind": "strip-block", "path": "AGENTS.md", "old": digest(agents_before),
                    "new": digest(remaining), "content": encode(remaining)})
    # Keep CLAUDE.md and its @AGENTS.md import; it may carry unrelated project rules.
    actions.append({"kind": "delete", "path": LOCK, "old": digest(lock_data), "new": "missing"})
    return actions


def make_plan(root: Path) -> dict | None:
    lock_data = read_optional(safe_path(root, LOCK))
    if lock_data is None:
        signals = [safe_path(root, ".agents/handoff/PROTOCOL.md"), safe_path(root, ".agents/handoff/ledger.sh")]
        old_skill = safe_path(root, ".agents/skills/handoff/SKILL.md")
        if old_skill.is_file() and b"# \xe4\xbb\xbb\xe5\x8a\xa1\xe6\x8e\xa5\xe5\x8a\x9b\xe8\xa7\x84\xe7\xa8\x8b" in old_skill.read_bytes():
            signals.append(old_skill)
        agents = read_optional(safe_path(root, "AGENTS.md")) or b""
        if any(p.exists() or p.is_symlink() for p in signals) or BEGIN in agents or END in agents:
            raise MigrationError("Legacy files without an ownership lock; migrate explicitly after resolving ownership")
        return None
    files, fragments = parse_lock(lock_data)
    for name, stored in files.items():
        if file_hash(root, name) != stored:
            raise MigrationError(f"Managed file has local modifications: {name}")
    if ".agents/skills/handoff/SKILL.md" in files and (root / ".agents/skills/handoff/scripts/install.sh").exists():
        raise MigrationError("Refusing to remove a same-name installer skill")
    claude = read_optional(safe_path(root, "CLAUDE.md"))
    first_line = claude.splitlines(keepends=True)[0] if claude else b""
    if first_line not in (b"@AGENTS.md\n", b"@AGENTS.md") or digest(first_line) != fragments["CLAUDE.md#handoff"]:
        raise MigrationError("CLAUDE.md import has local modifications")
    if ".claude/skills/handoff#target" in fragments and link_hash(root) != fragments[".claude/skills/handoff#target"]:
        raise MigrationError("Claude skill link has local modifications")
    before = safe_path(root, "AGENTS.md").read_bytes()
    return {"format": 1, "root": str(root), "lock": encode(lock_data), "agents_before": encode(before),
            "actions": expected_actions(lock_data, before)}


def validate_plan(root: Path, plan: dict) -> None:
    if set(plan) != {"format", "root", "lock", "agents_before", "actions"} or plan["format"] != 1 or plan["root"] != str(root):
        raise MigrationError("Invalid cleanup transaction")
    expected = expected_actions(decode(plan["lock"]), decode(plan["agents_before"]))
    if plan["actions"] != expected:
        raise MigrationError("Cleanup transaction has missing, changed or unknown actions")
    for action in expected:
        actual = link_hash(root) if action["kind"] == "unlink" else file_hash(root, action["path"])
        if actual not in (action["old"], action["new"]):
            raise MigrationError(f"Cleanup transaction conflict: {action['path']}")


def atomic_write(path: Path, value: bytes, *, exclusive: bool = False) -> None:
    fd, name = tempfile.mkstemp(prefix=".handoff-cleanup-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(value)
        if exclusive:
            os.link(name, path)
        else:
            os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def inspect(root: Path) -> tuple[str, dict | None]:
    old = safe_path(root, OLD_TRANSACTION)
    if old.exists():
        raise MigrationError("Unfinished old installation transaction; recover it with its original installer first")
    journal = safe_path(root, JOURNAL)
    if journal.exists():
        plan = json.loads(journal.read_text())
        validate_plan(root, plan)
        return "interrupted", plan
    plan = make_plan(root)
    return ("legacy", plan) if plan else ("clean", None)


def migrate(root: Path) -> dict:
    state, plan = inspect(root)
    if state == "clean":
        return {"state": "clean", "changed": False}
    journal = safe_path(root, JOURNAL)
    if state == "legacy":
        # Exclusive creation prevents two first-use migrations from replacing each other's journal.
        atomic_write(journal, (json.dumps(plan, indent=2) + "\n").encode(), exclusive=True)
    validate_plan(root, plan)
    for action in plan["actions"]:
        path = safe_path(root, action["path"], link=action["kind"] == "unlink")
        actual = link_hash(root) if action["kind"] == "unlink" else file_hash(root, action["path"])
        if actual == action["new"]:
            continue
        if actual != action["old"]:
            raise MigrationError(f"Managed file changed during cleanup: {action['path']}")
        if action["kind"] == "strip-block":
            atomic_write(path, decode(action["content"]))
        else:
            path.unlink()
    for relative in (".agents/handoff", ".agents/skills/handoff", "tools"):
        path = root / relative
        if path.is_dir() and not path.is_symlink():
            try:
                path.rmdir()
            except OSError:
                pass
    journal.unlink()
    return {"state": "clean", "changed": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("status", "migrate"))
    parser.add_argument("repo", type=Path, nargs="?", default=Path.cwd())
    args = parser.parse_args()
    try:
        root = repo_root(args.repo)
        if args.mode == "status":
            state, plan = inspect(root)
            result = {"state": state, "repo": str(root), "paths": [a["path"] for a in plan["actions"]] if plan else []}
        else:
            result = {**migrate(root), "repo": str(root)}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (MigrationError, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"state": "blocked", "reason": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
