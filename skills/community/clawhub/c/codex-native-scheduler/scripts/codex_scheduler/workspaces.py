"""Direct-directory and Git worktree preparation."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .errors import SchedulerError
from .util import (
    atomic_write_json,
    read_json,
    run_checked,
    secure_directory,
)

BRANCH_SAFE = re.compile(r"[^A-Za-z0-9._/-]+")


def git(
    cwd: Path,
    *arguments: str,
    timeout: float = 30,
    allow_failure: bool = False,
) -> str:
    result = run_checked(["git", "-C", str(cwd), *arguments], timeout=timeout)
    if result.returncode != 0 and not allow_failure:
        detail = result.stderr.strip() or result.stdout.strip()
        raise SchedulerError(f"git {' '.join(arguments)} failed: {detail}")
    return result.stdout.strip()


def inspect_repository(cwd: Path) -> dict[str, Any]:
    root_text = git(cwd, "rev-parse", "--show-toplevel")
    root = Path(root_text).resolve()
    commit = git(root, "rev-parse", "HEAD")
    branch = git(root, "symbolic-ref", "--quiet", "--short", "HEAD", allow_failure=True)
    return {
        "repo_root": str(root),
        "head_commit": commit,
        "head_branch": branch or None,
        "relative_cwd": str(cwd.resolve().relative_to(root)),
    }


def ensure_direct_workspace(cwd: Path, *, allow_dirty: bool) -> bool:
    if not cwd.is_dir():
        raise SchedulerError(f"working directory does not exist: {cwd}")
    repository = run_checked(
        ["git", "-C", str(cwd), "rev-parse", "--is-inside-work-tree"],
        timeout=15,
    )
    if repository.returncode != 0:
        return False
    if not allow_dirty:
        status = git(cwd, "status", "--porcelain")
        if status:
            raise SchedulerError(
                "direct workspace has uncommitted changes; pass --allow-dirty "
                "to acknowledge concurrent writes"
            )
    return True


def worktree_settings(
    cwd: Path,
    *,
    base_policy: str,
    base_ref: str | None,
) -> dict[str, Any]:
    repository = inspect_repository(cwd)
    root = Path(repository["repo_root"])
    requested_ref = base_ref or repository["head_branch"] or repository["head_commit"]
    commit = git(root, "rev-parse", f"{requested_ref}^{{commit}}")
    return {
        "mode": "worktree",
        "repo_root": str(root),
        "relative_cwd": repository["relative_cwd"],
        "base_policy": base_policy,
        "base_ref": requested_ref,
        "base_commit": commit,
        "source_branch": repository["head_branch"],
        "generation": 1,
    }


def _branch_component(value: str) -> str:
    cleaned = BRANCH_SAFE.sub("-", value).strip("-/")
    return cleaned[:80] or "run"


def _base_commit(workspace: dict[str, Any]) -> str:
    root = Path(workspace["repo_root"])
    if workspace["base_policy"] == "latest" and workspace.get("base_ref"):
        return git(root, "rev-parse", f"{workspace['base_ref']}^{{commit}}")
    return workspace["base_commit"]


def prepare_workspace(
    job: dict[str, Any],
    run_id: str,
    *,
    state_root: Path,
) -> tuple[Path, dict[str, Any]]:
    workspace = job["workspace"]
    if workspace["mode"] == "direct":
        cwd = Path(job["cwd"])
        ensure_direct_workspace(
            cwd,
            allow_dirty=bool(workspace.get("allow_dirty")),
        )
        return cwd, {"mode": "direct", "cwd": str(cwd)}

    repo = Path(workspace["repo_root"])
    relative = Path(workspace["relative_cwd"])
    root = state_root / "jobs" / job["id"] / "worktrees"
    secure_directory(root)
    if job["session_mode"] == "resume_fixed":
        generation = int(workspace.get("generation", 1))
        name = f"fixed-{generation}"
        branch = (
            f"codex-schedule/{_branch_component(job.get('name') or job['id'])}"
            f"-fixed-{generation}"
        )
    else:
        name = run_id
        branch = (
            f"codex-schedule/{_branch_component(job.get('name') or job['id'])}"
            f"-{_branch_component(run_id)}"
        )
    path = root / name
    if not path.exists():
        base_commit = _base_commit(workspace)
        git(
            repo,
            "worktree",
            "add",
            "-b",
            branch,
            str(path),
            base_commit,
            timeout=120,
        )
    metadata_path = root / f".{name}.json"
    if not metadata_path.exists():
        atomic_write_json(
            metadata_path,
            {
                "path": str(path),
                "repo_root": str(repo),
                "comparison_ref": (
                    workspace.get("base_ref")
                    or workspace.get("source_branch")
                    or workspace["base_commit"]
                ),
            },
        )
    cwd = path / relative
    if not cwd.is_dir():
        raise SchedulerError(f"worktree subdirectory does not exist: {cwd}")
    actual_branch = git(path, "branch", "--show-current") or branch
    return cwd, {
        "mode": "worktree",
        "repo_root": str(repo),
        "path": str(path),
        "cwd": str(cwd),
        "branch": actual_branch,
        "base_commit": git(path, "rev-parse", "HEAD"),
    }


def managed_worktrees(
    job: dict[str, Any],
    *,
    state_root: Path,
) -> list[Path]:
    root = state_root / "jobs" / job["id"] / "worktrees"
    if not root.is_dir():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir())


def _worktree_metadata(
    job: dict[str, Any],
    path: Path,
    *,
    state_root: Path,
) -> dict[str, Any] | None:
    root = state_root / "jobs" / job["id"] / "worktrees"
    metadata_path = root / f".{path.name}.json"
    if not metadata_path.is_file():
        return None
    return read_json(metadata_path)


def worktree_risks(
    job: dict[str, Any],
    *,
    state_root: Path,
) -> list[dict[str, str]]:
    risks: list[dict[str, str]] = []
    for path in managed_worktrees(job, state_root=state_root):
        metadata = _worktree_metadata(job, path, state_root=state_root)
        if metadata is None:
            risks.append(
                {
                    "path": str(path),
                    "reason": "missing scheduler worktree metadata",
                }
            )
            continue
        repo = Path(metadata["repo_root"])
        comparison = metadata["comparison_ref"]
        status = git(path, "status", "--porcelain", allow_failure=True)
        if status:
            risks.append({"path": str(path), "reason": "uncommitted changes"})
            continue
        head = git(path, "rev-parse", "HEAD", allow_failure=True)
        if not head:
            risks.append({"path": str(path), "reason": "cannot read worktree HEAD"})
            continue
        ahead_result = run_checked(
            [
                "git",
                "-C",
                str(repo),
                "rev-list",
                "--count",
                f"{comparison}..{head}",
            ],
            timeout=30,
        )
        if ahead_result.returncode != 0:
            risks.append(
                {
                    "path": str(path),
                    "reason": "cannot verify whether commits are merged",
                }
            )
            continue
        if int(ahead_result.stdout.strip() or "0") > 0:
            risks.append({"path": str(path), "reason": "unmerged commits"})
    return risks


def remove_safe_worktrees(
    job: dict[str, Any],
    *,
    state_root: Path,
) -> list[str]:
    risks = worktree_risks(job, state_root=state_root)
    if risks:
        detail = "; ".join(
            f"{risk['path']} ({risk['reason']})" for risk in risks
        )
        raise SchedulerError(
            "refusing to delete worktrees with user work; preserve or remove "
            f"them explicitly first: {detail}"
        )
    removed = []
    for path in managed_worktrees(job, state_root=state_root):
        metadata = _worktree_metadata(job, path, state_root=state_root)
        if metadata is None:
            raise SchedulerError(f"missing worktree metadata for {path}")
        repo = Path(metadata["repo_root"])
        git(repo, "worktree", "remove", str(path), timeout=120)
        metadata_path = path.parent / f".{path.name}.json"
        metadata_path.unlink(missing_ok=True)
        removed.append(str(path))
    return removed
