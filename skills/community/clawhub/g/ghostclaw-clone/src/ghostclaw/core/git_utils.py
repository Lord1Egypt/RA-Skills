"""Git utilities for diff extraction and change detection.

Provides functions to obtain unified diffs between git references and
parse them into lists of changed files and line ranges.
"""

import subprocess
import asyncio
import asyncio.subprocess
from dataclasses import dataclass
from typing import List, Optional, Tuple
from pathlib import Path


@dataclass
class DiffResult:
    """Represents a parsed git diff."""

    files_changed: List[str]
    raw_diff: str
    against: str  # the base ref we diffed against


class AsyncGitExecutor:
    """
    Non-blocking git operations using asyncio.create_subprocess_exec.
    """

    def __init__(self, cwd: Optional[Path] = None):
        self.cwd = str(cwd) if cwd else None

    async def run_git(self, args: List[str]) -> Tuple[Optional[int], str, str]:
        """Execute a git command asynchronously."""
        process = await asyncio.create_subprocess_exec(
            "git",
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.cwd,
        )
        stdout, stderr = await process.communicate()
        return process.returncode, stdout.decode("utf-8"), stderr.decode("utf-8")

    async def diff(self, base_ref: str = "HEAD~1") -> DiffResult:
        """Non-blocking git diff."""
        _, stdout, _ = await self.run_git(["diff", base_ref])
        files = _parse_changed_files(stdout)
        return DiffResult(files_changed=files, raw_diff=stdout, against=base_ref)

    async def staged_diff(self) -> DiffResult:
        """Get diff of staged changes."""
        _, stdout, _ = await self.run_git(["diff", "--cached"])
        files = _parse_changed_files(stdout)
        return DiffResult(
            files_changed=files, raw_diff=stdout, against="HEAD (staged)"
        )

    async def unstaged_diff(self) -> DiffResult:
        """Get diff of unstaged changes."""
        _, stdout, _ = await self.run_git(["diff"])
        files = _parse_changed_files(stdout)
        return DiffResult(
            files_changed=files, raw_diff=stdout, against="index (unstaged)"
        )


async def get_git_diff_async(
    base_ref: str = "HEAD~1", cwd: Optional[Path] = None
) -> DiffResult:
    """Async version of get_git_diff."""
    executor = AsyncGitExecutor(cwd)
    return await executor.diff(base_ref)


async def get_current_sha_async(cwd: Optional[Path] = None) -> str:
    """Async version of get_current_sha."""
    executor = AsyncGitExecutor(cwd)
    returncode, stdout, stderr = await executor.run_git(["rev-parse", "HEAD"])
    if returncode != 0:
        raise RuntimeError(f"git rev-parse HEAD failed: {stderr.strip()}")
    return stdout.strip()


def get_git_diff(base_ref: str = "HEAD~1", cwd: Optional[Path] = None) -> DiffResult:
    """
    Run `git diff` against a base reference and return the raw unified diff.
    """
    cmd = ["git", "diff", base_ref]
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    raw = result.stdout
    files = _parse_changed_files(raw)
    return DiffResult(files_changed=files, raw_diff=raw, against=base_ref)


def get_staged_diff(cwd: Optional[Path] = None) -> DiffResult:
    """Get diff of staged changes (index vs HEAD)."""
    cmd = ["git", "diff", "--cached"]
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    raw = result.stdout
    files = _parse_changed_files(raw)
    return DiffResult(files_changed=files, raw_diff=raw, against="HEAD (staged)")


def get_unstaged_diff(cwd: Optional[Path] = None) -> DiffResult:
    """Get diff of unstaged changes (working tree vs index)."""
    cmd = ["git", "diff"]
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    raw = result.stdout
    files = _parse_changed_files(raw)
    return DiffResult(files_changed=files, raw_diff=raw, against="index (unstaged)")


def _parse_changed_files(diff_text: str) -> List[str]:
    """Extract file paths from a unified diff.
    Optimized: Only parse '+++ b/' lines as they represent the destination path.
    """
    files = []
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            path = line[len("+++ b/"):]  # Type-safe slice
            if path != "/dev/null" and path not in files:
                files.append(path)
        elif line.startswith("--- a/"):
            path = line[len("--- a/"):]  # Capture deleted files
            if path != "/dev/null" and path not in files:
                files.append(path)
    return files


def has_uncommitted_changes(cwd: Optional[Path] = None) -> bool:
    """Quick check if there are any staged or unstaged changes."""
    subprocess.run(["git", "update-index", "-q", "--refresh"], cwd=cwd, check=False)
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    return bool(result.stdout.strip())


def get_current_branch(cwd: Optional[Path] = None) -> str:
    """Get the current branch name (or commit SHA if detached)."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    branch = result.stdout.strip()
    if branch != "HEAD":
        return branch
    sha = get_current_sha(cwd)
    return sha[:8]


def get_current_sha(cwd: Optional[Path] = None) -> str:
    """Get full commit SHA of HEAD."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()
