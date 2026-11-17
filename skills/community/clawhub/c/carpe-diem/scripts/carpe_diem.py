#!/usr/bin/env python3
"""Deterministic local helpers for the Carpe Diem skill."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Sequence


PROFILE_LIST_FIELDS = (
    "strengths",
    "interests",
    "recurring_frictions",
    "constraints",
    "project_preferences",
    "working_style",
    "project_history",
    "consents",
)
PROJECT_PHASES = ("discover", "validate", "plan", "handoff", "track", "paused", "completed")
REQUIRED_PLAN_SECTIONS = (
    "摘要与问题",
    "目标用户与核心场景",
    "价值假设和差异化证据",
    "目标与非目标",
    "用户体验和功能范围",
    "架构、组件、数据流和接口",
    "错误处理、安全和隐私",
    "测试和验收",
    "里程碑、任务和依赖",
    "风险与降级",
    "开源、贡献和发布方式",
    "关键决策记录",
)


class StateCorruptedError(Exception):
    """Raised when an existing local state file cannot be decoded safely."""


def default_profile_path() -> Path:
    return Path.home() / ".carpe-diem" / "profiles" / "me.json"


def new_profile(handle: str = "me") -> Dict[str, Any]:
    profile: Dict[str, Any] = {
        "schema_version": 1,
        "handle": handle,
        "revision": 0,
        "updated_at": None,
    }
    for field in PROFILE_LIST_FIELDS:
        profile[field] = []
    return profile


def load_profile(profile_path: Path) -> tuple[str, Dict[str, Any]]:
    if profile_path.exists():
        try:
            with profile_path.open("r", encoding="utf-8") as stream:
                return "existing", json.load(stream)
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise StateCorruptedError(
                f"profile is corrupted and was left unchanged: {profile_path}"
            ) from error
    return "new", new_profile()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def atomic_write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def command_state_read(args: argparse.Namespace) -> int:
    profile_path = Path(args.profile)
    status, profile = load_profile(profile_path)

    payload = {"status": status, "path": str(profile_path), "profile": profile}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(f"profile={status} revision={profile['revision']} path={profile_path}")
    return 0


def command_state_propose(args: argparse.Namespace) -> int:
    profile_path = Path(args.profile)
    _, profile = load_profile(profile_path)
    previous_fact = None
    fact_id = args.replace_id
    if fact_id:
        previous_fact = next(
            (fact for fact in profile[args.field] if fact.get("id") == fact_id), None
        )
        if previous_fact is None:
            print("replacement fact was not found in the selected field", file=sys.stderr)
            return 2
    else:
        identity_input = "\0".join((args.field, args.value, args.kind, args.basis))
        fact_id = hashlib.sha256(identity_input.encode("utf-8")).hexdigest()[:16]
    proposal = {
        "proposal_version": 1,
        "operation": "replace_profile_fact" if previous_fact else "add_profile_fact",
        "path": str(profile_path),
        "base_revision": profile["revision"],
        "field": args.field,
        "fact": {
            "id": fact_id,
            "value": args.value,
            "kind": args.kind,
            "confidence": "candidate",
            "basis": args.basis,
            "confirmed_at": None,
            "last_used_at": None,
        },
    }
    if previous_fact:
        proposal["previous_fact"] = previous_fact
    if args.json:
        print(json.dumps(proposal, ensure_ascii=False, sort_keys=True))
    else:
        print(f"proposal=add field={args.field} value={args.value!r}")
    return 0


def command_state_apply(args: argparse.Namespace) -> int:
    profile_path = Path(args.profile)
    proposal_path = Path(args.proposal)
    with proposal_path.open("r", encoding="utf-8") as stream:
        proposal = json.load(stream)

    operation = proposal.get("operation")
    if operation not in ("add_profile_fact", "replace_profile_fact"):
        print("unsupported proposal operation", file=sys.stderr)
        return 2
    if Path(proposal.get("path", "")) != profile_path:
        print("proposal target does not match --profile", file=sys.stderr)
        return 2

    _, profile = load_profile(profile_path)
    if proposal.get("base_revision") != profile.get("revision"):
        print("profile revision conflict", file=sys.stderr)
        return 3

    field = proposal.get("field")
    if field not in PROFILE_LIST_FIELDS:
        print("proposal field is not allowed", file=sys.stderr)
        return 2

    fact = dict(proposal["fact"])
    now = utc_now()
    fact["confidence"] = "confirmed"
    fact["confirmed_at"] = now
    fact["last_used_at"] = now
    if operation == "replace_profile_fact":
        previous_id = proposal.get("previous_fact", {}).get("id")
        replacement_index = next(
            (
                index
                for index, existing in enumerate(profile[field])
                if existing.get("id") == previous_id
            ),
            None,
        )
        if replacement_index is None:
            print("replacement fact was not found", file=sys.stderr)
            return 3
        profile[field][replacement_index] = fact
    else:
        profile[field].append(fact)
    profile["revision"] += 1
    profile["updated_at"] = now
    atomic_write_json(profile_path, profile)

    payload = {"status": "applied", "path": str(profile_path), "revision": profile["revision"]}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(f"profile=applied revision={profile['revision']} path={profile_path}")
    return 0


def command_state_forget(args: argparse.Namespace) -> int:
    profile_path = Path(args.profile)
    status, profile = load_profile(profile_path)
    if status == "new":
        print("profile does not exist", file=sys.stderr)
        return 2
    if profile.get("revision") != args.expected_revision:
        print("profile revision conflict", file=sys.stderr)
        return 3

    removed = False
    for field in PROFILE_LIST_FIELDS:
        retained = [fact for fact in profile[field] if fact.get("id") != args.fact_id]
        if len(retained) != len(profile[field]):
            profile[field] = retained
            removed = True
    if not removed:
        print("profile fact was not found", file=sys.stderr)
        return 4

    now = utc_now()
    profile["revision"] += 1
    profile["updated_at"] = now
    atomic_write_json(profile_path, profile)
    payload = {
        "status": "forgotten",
        "fact_id": args.fact_id,
        "revision": profile["revision"],
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(f"profile=forgotten fact={args.fact_id} revision={profile['revision']}")
    return 0


def redact_portable(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: redact_portable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_portable(item) for item in value]
    if isinstance(value, str):
        looks_like_windows_path = len(value) > 2 and value[1:3] in (":\\", ":/")
        if value.startswith("/") or looks_like_windows_path:
            return "<redacted-local-path>"
    return value


def command_state_export(args: argparse.Namespace) -> int:
    profile_path = Path(args.profile)
    status, profile = load_profile(profile_path)
    if status == "new":
        print("profile does not exist", file=sys.stderr)
        return 2

    portable = redact_portable(profile)
    for field in PROFILE_LIST_FIELDS:
        portable[field] = [
            fact for fact in portable[field] if fact.get("confidence") == "confirmed"
        ]
    payload = {
        "export_schema_version": 1,
        "exported_at": utc_now(),
        "profile": portable,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def new_project_state(root: Path) -> Dict[str, Any]:
    now = utc_now()
    project_id = hashlib.sha256(str(root.resolve()).encode("utf-8")).hexdigest()[:16]
    return {
        "schema_version": 1,
        "project_id": project_id,
        "phase": "discover",
        "direction": None,
        "candidates": [],
        "rejected_candidates": [],
        "validation": {},
        "decisions": [],
        "plan": {},
        "milestones": [],
        "deviations": [],
        "evidence": [],
        "next_recommended": "建立第一张机会地图",
        "last_observed_git_head": None,
        "revision": 1,
        "created_at": now,
        "updated_at": now,
    }


def command_project_init(args: argparse.Namespace) -> int:
    root = Path(args.root)
    if not root.is_dir():
        print("project root does not exist or is not a directory", file=sys.stderr)
        return 2

    local_dir = root / ".carpe-diem"
    state_path = local_dir / "project-state.json"
    events_dir = local_dir / "events"
    if state_path.exists():
        with state_path.open("r", encoding="utf-8") as stream:
            state = json.load(stream)
        status = "existing"
    else:
        events_dir.mkdir(parents=True, exist_ok=True)
        state = new_project_state(root)
        atomic_write_json(state_path, state)
        status = "created"

    payload = {
        "status": status,
        "path": str(state_path),
        "project_id": state["project_id"],
        "phase": state["phase"],
        "revision": state["revision"],
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(
            f"project={status} phase={state['phase']} revision={state['revision']} path={state_path}"
        )
    return 0


def command_project_status(args: argparse.Namespace) -> int:
    root = Path(args.root)
    state_path = root / ".carpe-diem" / "project-state.json"
    if not state_path.is_file():
        print("project state does not exist; run project init first", file=sys.stderr)
        return 2
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        print(f"project state is corrupted and was left unchanged: {state_path}", file=sys.stderr)
        return 4
    payload = {
        "status": "existing",
        "path": str(state_path),
        "project_id": state.get("project_id"),
        "phase": state.get("phase"),
        "revision": state.get("revision"),
        "next_recommended": state.get("next_recommended"),
        "state": state,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(
            f"project=existing phase={payload['phase']} revision={payload['revision']} "
            f"next={payload['next_recommended']}"
        )
    return 0


def command_project_event(args: argparse.Namespace) -> int:
    root = Path(args.root)
    state_path = root / ".carpe-diem" / "project-state.json"
    if not state_path.is_file():
        print("project state does not exist; run project init first", file=sys.stderr)
        return 2
    with state_path.open("r", encoding="utf-8") as stream:
        state = json.load(stream)
    if state.get("revision") != args.expected_revision:
        print("project revision conflict", file=sys.stderr)
        return 3

    now = utc_now()
    identity = f"{state['project_id']}\0{args.expected_revision}\0{args.summary}\0{now}"
    event_id = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]
    event = {
        "schema_version": 1,
        "event_id": event_id,
        "project_id": state["project_id"],
        "base_revision": args.expected_revision,
        "result_revision": args.expected_revision + 1,
        "phase_before": state["phase"],
        "phase_after": args.phase,
        "summary": args.summary,
        "next_recommended": args.next,
        "observed_at": now,
    }
    event_name = f"{now.replace(':', '-').replace('Z', '')}-{event_id}.json"
    event_path = root / ".carpe-diem" / "events" / event_name
    atomic_write_json(event_path, event)

    state["phase"] = args.phase
    state["next_recommended"] = args.next
    state["revision"] = args.expected_revision + 1
    state["updated_at"] = now
    state["decisions"].append(
        {"event_id": event_id, "summary": args.summary, "at": now}
    )
    atomic_write_json(state_path, state)

    payload = {
        "status": "recorded",
        "event_id": event_id,
        "event_path": str(event_path),
        "phase": state["phase"],
        "revision": state["revision"],
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(
            f"event=recorded phase={state['phase']} revision={state['revision']} id={event_id}"
        )
    return 0


def command_plan_validate(args: argparse.Namespace) -> int:
    plan_path = Path(args.file)
    if not plan_path.is_file():
        print("plan file does not exist", file=sys.stderr)
        return 2
    text = plan_path.read_text(encoding="utf-8")
    blockers = []
    if not re.search(r"(?m)^# 项目实施计划\s*$", text):
        blockers.append(
            {"code": "missing_title", "message": "use the title: # 项目实施计划"}
        )
    for token in sorted(set(re.findall(r"\b(?:TBD|TODO|FIXME)\b", text, re.IGNORECASE))):
        blockers.append(
            {"code": "placeholder", "message": f"remove unfinished placeholder: {token}"}
        )
    for section in REQUIRED_PLAN_SECTIONS:
        if f"## {section}" not in text:
            blockers.append(
                {"code": "missing_section", "message": f"add required section: {section}"}
            )
            continue
        match = re.search(
            rf"(?ms)^## {re.escape(section)}\s*$\n(.*?)(?=^## |\Z)", text
        )
        if match is None or not match.group(1).strip():
            blockers.append(
                {"code": "empty_section", "message": f"complete required section: {section}"}
            )
    milestone_match = re.search(
        r"(?ms)^## 里程碑、任务和依赖\s*$\n(.*?)(?=^## |\Z)", text
    )
    if milestone_match is not None and "验收标准" not in milestone_match.group(1):
        blockers.append(
            {
                "code": "missing_acceptance_criteria",
                "message": "add explicit 验收标准 to the milestone section",
            }
        )
    payload = {
        "valid": not blockers,
        "file": str(plan_path),
        "blockers": blockers,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        if blockers:
            for blocker in blockers:
                print(f"BLOCK {blocker['code']}: {blocker['message']}")
        else:
            print(f"plan=valid file={plan_path}")
    return 0 if not blockers else 1


def command_plan_diff(args: argparse.Namespace) -> int:
    before = Path(args.before)
    after = Path(args.after)
    allowed_names = {"project-plan.md", "project-handoff.md"}
    if before.name not in allowed_names or after.name != before.name:
        print("plan diff only accepts matching Carpe Diem plan or handoff files", file=sys.stderr)
        return 2
    if not before.is_file() or not after.is_file():
        print("both diff inputs must exist", file=sys.stderr)
        return 2
    before_text = before.read_text(encoding="utf-8")
    after_text = after.read_text(encoding="utf-8")
    diff = "".join(
        difflib.unified_diff(
            before_text.splitlines(keepends=True),
            after_text.splitlines(keepends=True),
            fromfile=str(before),
            tofile=str(after),
        )
    )
    payload = {"changed": before_text != after_text, "diff": diff}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(diff, end="")
    return 0


def run_git(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )


def command_evidence_git(args: argparse.Namespace) -> int:
    root = Path(args.root)
    inside = run_git(root, "rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        print("target is not a Git worktree", file=sys.stderr)
        return 2

    head_result = run_git(root, "rev-parse", "--verify", "HEAD")
    head = head_result.stdout.strip() if head_result.returncode == 0 else None
    head_commit = None
    head_paths = []
    if head is not None:
        head_summary_result = run_git(root, "show", "-s", "--format=%H%x1f%s", "HEAD")
        if "\x1f" in head_summary_result.stdout:
            commit_hash, subject = head_summary_result.stdout.strip().split("\x1f", 1)
            head_commit = {"hash": commit_hash, "subject": subject}
        head_paths_result = run_git(
            root, "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "HEAD"
        )
        if head_paths_result.returncode == 0:
            head_paths = [line for line in head_paths_result.stdout.splitlines() if line]
    branch_result = run_git(root, "symbolic-ref", "--quiet", "--short", "HEAD")
    branch = branch_result.stdout.strip() if branch_result.returncode == 0 else None
    status_result = run_git(root, "status", "--porcelain=v1", "--untracked-files=all")
    if status_result.returncode != 0:
        print(status_result.stderr.strip() or "git status failed", file=sys.stderr)
        return 2
    status_lines = [line for line in status_result.stdout.splitlines() if line]
    changed_paths = []
    for line in status_lines:
        path = line[3:] if len(line) >= 4 else line
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        changed_paths.append(path.strip('"'))
    history_relationship = None
    commits = []
    committed_paths = []
    if args.since:
        exists = run_git(root, "cat-file", "-e", f"{args.since}^{{commit}}")
        if exists.returncode != 0:
            history_relationship = "missing"
        elif head is None:
            history_relationship = "no-head"
        else:
            ancestor = run_git(root, "merge-base", "--is-ancestor", args.since, head)
            history_relationship = "ancestor" if ancestor.returncode == 0 else "diverged"
            if history_relationship == "ancestor":
                log_result = run_git(
                    root,
                    "log",
                    "--reverse",
                    "--format=%H%x1f%s",
                    f"{args.since}..{head}",
                )
                commits = [
                    {"hash": line.split("\x1f", 1)[0], "subject": line.split("\x1f", 1)[1]}
                    for line in log_result.stdout.splitlines()
                    if "\x1f" in line
                ]
                diff_result = run_git(root, "diff", "--name-only", f"{args.since}..{head}")
                committed_paths = [
                    line for line in diff_result.stdout.splitlines() if line
                ]
    payload = {
        "status": "ok",
        "root": str(root),
        "branch": branch,
        "head": head,
        "head_commit": head_commit,
        "head_paths": head_paths,
        "dirty": bool(status_lines),
        "changed_paths": changed_paths,
        "porcelain": status_lines,
        "since": args.since,
        "history_relationship": history_relationship,
        "commits": commits,
        "committed_paths": committed_paths,
        "observed_at": utc_now(),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(
            f"git=ok branch={branch or '-'} head={head or '-'} dirty={str(bool(status_lines)).lower()}"
        )
        for path in changed_paths:
            print(f"change {path}")
    return 0


INSTALL_TARGETS = {
    "codex": Path.home() / ".codex" / "skills" / "carpe-diem",
    "claude-code": Path.home() / ".claude" / "skills" / "carpe-diem",
    "cursor": Path.home() / ".cursor" / "skills" / "carpe-diem",
    "openclaw": Path.home() / ".openclaw" / "skills" / "carpe-diem",
}

INSTALL_ROOTS = {
    "codex": (".codex", "skills"),
    "claude-code": (".claude", "skills"),
    "cursor": (".cursor", "skills"),
    "openclaw": (".openclaw", "skills"),
}

PLATFORM_COMMANDS = {
    "codex": "codex",
    "claude-code": "claude",
    "cursor": "cursor",
    "openclaw": "openclaw",
}


def command_install_detect(args: argparse.Namespace) -> int:
    home = Path(args.home).expanduser().absolute()
    platforms = []
    for platform, parts in INSTALL_ROOTS.items():
        root = home.joinpath(*parts)
        executable = shutil.which(PLATFORM_COMMANDS[platform])
        platforms.append(
            {
                "platform": platform,
                "root": str(root),
                "root_exists": root.is_dir(),
                "target": str(root / "carpe-diem"),
                "target_exists": (root / "carpe-diem").is_dir(),
                "command": PLATFORM_COMMANDS[platform],
                "command_path": executable,
            }
        )
    payload = {"status": "ok", "home": str(home), "platforms": platforms}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        for item in platforms:
            print(
                f"{item['platform']} root={'yes' if item['root_exists'] else 'no'} "
                f"command={item['command_path'] or '-'} target={item['target']}"
            )
    return 0


def validate_snapshot_files(root: Path, files: Sequence[str]) -> list[str]:
    if not isinstance(files, list) or not files:
        raise ValueError("snapshot files must be a non-empty list")

    resolved_root = root.resolve()
    validated = []
    seen = set()
    for relative_path in files:
        if not isinstance(relative_path, str) or not relative_path:
            raise ValueError("unsafe snapshot path: expected a non-empty string")
        path = Path(relative_path)
        if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
            raise ValueError(f"unsafe snapshot path: {relative_path}")
        try:
            (resolved_root / path).resolve().relative_to(resolved_root)
        except ValueError as error:
            raise ValueError(f"unsafe snapshot path: {relative_path}") from error
        if relative_path in seen:
            raise ValueError(f"duplicate snapshot path: {relative_path}")
        seen.add(relative_path)
        validated.append(relative_path)
    return validated


def snapshot_fingerprint(root: Path, files: Sequence[str]) -> str:
    digest = hashlib.sha256()
    for relative_path in sorted(validate_snapshot_files(root, files)):
        path = root / relative_path
        if not path.is_file():
            raise FileNotFoundError(f"snapshot file is missing: {relative_path}")
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def command_install_plan(args: argparse.Namespace) -> int:
    source = Path(args.source).resolve()
    manifest_path = source / "manifest.json"
    if not manifest_path.is_file():
        print("source does not contain manifest.json", file=sys.stderr)
        return 2
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = manifest.get("files", [])
    try:
        fingerprint = snapshot_fingerprint(source, files)
    except (FileNotFoundError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    target = Path(args.target).resolve() if args.target else INSTALL_TARGETS[args.platform]
    plan = {
        "plan_version": 1,
        "operation": "install",
        "platform": args.platform,
        "source": str(source),
        "target": str(target),
        "version": manifest["version"],
        "fingerprint": fingerprint,
        "files": files,
    }
    if args.json:
        print(json.dumps(plan, ensure_ascii=False, sort_keys=True))
    else:
        print(
            f"install-plan platform={args.platform} version={manifest['version']} target={target}"
        )
        print(f"fingerprint={fingerprint}")
    return 0


def command_install_apply(args: argparse.Namespace) -> int:
    if not args.yes:
        print("installation requires explicit --yes after reviewing the plan", file=sys.stderr)
        return 2
    plan_path = Path(args.plan)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("operation") != "install":
        print("invalid install plan", file=sys.stderr)
        return 2
    source = Path(plan["source"])
    target = Path(plan["target"])
    files = plan["files"]
    try:
        current_fingerprint = snapshot_fingerprint(source, files)
    except (FileNotFoundError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    if current_fingerprint != plan["fingerprint"]:
        print("source changed after the install plan was reviewed", file=sys.stderr)
        return 3
    if target.exists():
        print("install target already exists; refusing to overwrite", file=sys.stderr)
        return 3

    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{target.name}.", dir=str(target.parent)))
    try:
        for relative_path in files:
            destination = staging / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / relative_path, destination)
        receipt = {
            "receipt_version": 1,
            "platform": plan["platform"],
            "version": plan["version"],
            "fingerprint": plan["fingerprint"],
            "files": files,
            "installed_at": utc_now(),
        }
        atomic_write_json(staging / ".carpe-diem-install.json", receipt)
        os.replace(staging, target)
    finally:
        if staging.exists():
            shutil.rmtree(staging)

    payload = {
        "status": "installed",
        "platform": plan["platform"],
        "target": str(target),
        "version": plan["version"],
        "fingerprint": plan["fingerprint"],
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(f"skill=installed platform={plan['platform']} target={target}")
    return 0


def command_install_verify(args: argparse.Namespace) -> int:
    target = Path(args.target)
    receipt_path = target / ".carpe-diem-install.json"
    if not receipt_path.is_file():
        print("install receipt is missing", file=sys.stderr)
        return 2
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    try:
        actual = snapshot_fingerprint(target, receipt["files"])
    except (FileNotFoundError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    valid = actual == receipt["fingerprint"]
    payload = {
        "valid": valid,
        "target": str(target),
        "version": receipt["version"],
        "expected_fingerprint": receipt["fingerprint"],
        "actual_fingerprint": actual,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(f"install={'valid' if valid else 'changed'} target={target}")
    return 0 if valid else 1


def command_install_uninstall(args: argparse.Namespace) -> int:
    if not args.yes:
        print("uninstall requires explicit --yes after reviewing the target", file=sys.stderr)
        return 2
    target = Path(args.target)
    receipt_path = target / ".carpe-diem-install.json"
    if not receipt_path.is_file():
        print("install receipt is missing; refusing to delete", file=sys.stderr)
        return 3
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    try:
        actual = snapshot_fingerprint(target, receipt["files"])
    except (FileNotFoundError, ValueError):
        print("installed snapshot changed; refusing to delete", file=sys.stderr)
        return 3
    if actual != receipt["fingerprint"]:
        print("installed snapshot changed; refusing to delete", file=sys.stderr)
        return 3
    shutil.rmtree(target)
    payload = {"status": "uninstalled", "target": str(target)}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(f"skill=uninstalled target={target}")
    return 0


def command_doctor(args: argparse.Namespace) -> int:
    source = Path(args.source).resolve()
    profile_path = Path(args.profile)
    errors = []
    warnings = []
    checks = {
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "source": str(source),
        "profile": str(profile_path),
    }
    if sys.version_info < (3, 10):
        errors.append(
            {"code": "python_too_old", "message": "Carpe Diem requires Python 3.10+"}
        )

    manifest_path = source / "manifest.json"
    if not manifest_path.is_file():
        errors.append({"code": "manifest_missing", "message": "manifest.json is missing"})
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            files = manifest.get("files", [])
            snapshot_fingerprint(source, files)
            checks["version"] = manifest.get("version")
            checks["runtime_files"] = len(files)
        except (json.JSONDecodeError, FileNotFoundError, TypeError) as error:
            errors.append({"code": "manifest_invalid", "message": str(error)})

    skill_path = source / "SKILL.md"
    if not skill_path.is_file():
        errors.append({"code": "skill_missing", "message": "SKILL.md is missing"})
    else:
        skill_text = skill_path.read_text(encoding="utf-8")
        if not skill_text.startswith("---\n") or "\nname: carpe-diem\n" not in skill_text:
            errors.append(
                {"code": "skill_frontmatter_invalid", "message": "SKILL.md frontmatter is invalid"}
            )

    if not profile_path.exists():
        warnings.append(
            {
                "code": "profile_missing",
                "message": "no personal profile yet; the first guided session can create one",
            }
        )
    else:
        try:
            load_profile(profile_path)
        except StateCorruptedError as error:
            errors.append({"code": "profile_corrupted", "message": str(error)})

    payload = {
        "valid": not errors,
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(f"doctor={'ok' if not errors else 'failed'}")
        for warning in warnings:
            print(f"WARN {warning['code']}: {warning['message']}")
        for error in errors:
            print(f"ERROR {error['code']}: {error['message']}")
    return 0 if not errors else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="carpe-diem")
    commands = parser.add_subparsers(dest="command", required=True)

    doctor = commands.add_parser("doctor", help="Check local runtime integrity without writing")
    doctor.add_argument("--source", default=".")
    doctor.add_argument("--profile", default=str(default_profile_path()))
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(handler=command_doctor)

    state = commands.add_parser("state", help="Manage local user profile state")
    state_commands = state.add_subparsers(dest="state_command", required=True)

    read = state_commands.add_parser("read", help="Read a profile without changing it")
    read.add_argument("--profile", default=str(default_profile_path()))
    read.add_argument("--json", action="store_true")
    read.set_defaults(handler=command_state_read)

    propose = state_commands.add_parser(
        "propose", help="Create a reviewable profile change without writing it"
    )
    propose.add_argument("--profile", default=str(default_profile_path()))
    propose.add_argument("--field", choices=PROFILE_LIST_FIELDS, required=True)
    propose.add_argument("--replace-id")
    propose.add_argument("--value", required=True)
    propose.add_argument(
        "--kind", choices=("observed", "inferred", "explicit"), required=True
    )
    propose.add_argument("--basis", required=True)
    propose.add_argument("--json", action="store_true")
    propose.set_defaults(handler=command_state_propose)

    apply_change = state_commands.add_parser(
        "apply", help="Apply a previously reviewed profile proposal"
    )
    apply_change.add_argument("--profile", default=str(default_profile_path()))
    apply_change.add_argument("--proposal", required=True)
    apply_change.add_argument("--json", action="store_true")
    apply_change.set_defaults(handler=command_state_apply)

    forget = state_commands.add_parser(
        "forget", help="Remove one confirmed fact after user approval"
    )
    forget.add_argument("--profile", default=str(default_profile_path()))
    forget.add_argument("--fact-id", required=True)
    forget.add_argument("--expected-revision", type=int, required=True)
    forget.add_argument("--json", action="store_true")
    forget.set_defaults(handler=command_state_forget)

    export = state_commands.add_parser(
        "export", help="Export confirmed profile facts without local paths"
    )
    export.add_argument("--profile", default=str(default_profile_path()))
    export.add_argument("--json", action="store_true")
    export.set_defaults(handler=command_state_export)

    project = commands.add_parser("project", help="Manage local project guidance state")
    project_commands = project.add_subparsers(dest="project_command", required=True)
    initialize = project_commands.add_parser(
        "init", help="Initialize local Carpe Diem project state"
    )
    initialize.add_argument("--root", default=".")
    initialize.add_argument("--json", action="store_true")
    initialize.set_defaults(handler=command_project_init)

    project_status = project_commands.add_parser(
        "status", help="Read current project guidance state without changing it"
    )
    project_status.add_argument("--root", default=".")
    project_status.add_argument("--json", action="store_true")
    project_status.set_defaults(handler=command_project_status)

    event = project_commands.add_parser(
        "event", help="Record a confirmed project guidance event"
    )
    event.add_argument("--root", default=".")
    event.add_argument("--expected-revision", type=int, required=True)
    event.add_argument("--phase", choices=PROJECT_PHASES, required=True)
    event.add_argument("--summary", required=True)
    event.add_argument("--next", required=True)
    event.add_argument("--json", action="store_true")
    event.set_defaults(handler=command_project_event)

    plan = commands.add_parser("plan", help="Validate Carpe Diem planning artifacts")
    plan_commands = plan.add_subparsers(dest="plan_command", required=True)
    validate = plan_commands.add_parser(
        "validate", help="Check that a rendered project plan is handoff-ready"
    )
    validate.add_argument("--file", required=True)
    validate.add_argument("--json", action="store_true")
    validate.set_defaults(handler=command_plan_validate)

    diff = plan_commands.add_parser(
        "diff", help="Show a read-only diff for a managed plan or handoff file"
    )
    diff.add_argument("--before", required=True)
    diff.add_argument("--after", required=True)
    diff.add_argument("--json", action="store_true")
    diff.set_defaults(handler=command_plan_diff)

    evidence = commands.add_parser("evidence", help="Collect read-only project evidence")
    evidence_commands = evidence.add_subparsers(dest="evidence_command", required=True)
    git_evidence = evidence_commands.add_parser(
        "git", help="Read Git metadata without changing the worktree"
    )
    git_evidence.add_argument("--root", default=".")
    git_evidence.add_argument("--since")
    git_evidence.add_argument("--json", action="store_true")
    git_evidence.set_defaults(handler=command_evidence_git)

    install = commands.add_parser("install", help="Plan and verify skill installation")
    install_commands = install.add_subparsers(dest="install_command", required=True)
    install_detect = install_commands.add_parser(
        "detect", help="Inspect supported skill roots without changing them"
    )
    install_detect.add_argument("--home", default=str(Path.home()))
    install_detect.add_argument("--json", action="store_true")
    install_detect.set_defaults(handler=command_install_detect)

    install_plan = install_commands.add_parser(
        "plan", help="Create a reviewable install plan without writing"
    )
    install_plan.add_argument("--platform", choices=tuple(INSTALL_TARGETS), required=True)
    install_plan.add_argument("--source", default=".")
    install_plan.add_argument("--target")
    install_plan.add_argument("--json", action="store_true")
    install_plan.set_defaults(handler=command_install_plan)

    install_apply = install_commands.add_parser(
        "apply", help="Apply an unchanged install plan after confirmation"
    )
    install_apply.add_argument("--plan", required=True)
    install_apply.add_argument("--yes", action="store_true")
    install_apply.add_argument("--json", action="store_true")
    install_apply.set_defaults(handler=command_install_apply)

    install_verify = install_commands.add_parser(
        "verify", help="Verify installed files against their receipt"
    )
    install_verify.add_argument("--target", required=True)
    install_verify.add_argument("--json", action="store_true")
    install_verify.set_defaults(handler=command_install_verify)

    install_uninstall = install_commands.add_parser(
        "uninstall", help="Remove only an unchanged receipt-backed installation"
    )
    install_uninstall.add_argument("--target", required=True)
    install_uninstall.add_argument("--yes", action="store_true")
    install_uninstall.add_argument("--json", action="store_true")
    install_uninstall.set_defaults(handler=command_install_uninstall)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except StateCorruptedError as error:
        print(str(error), file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
