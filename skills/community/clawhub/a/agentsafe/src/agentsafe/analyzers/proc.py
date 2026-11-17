"""Shared subprocess safety layer for external analyzers.

Security rules enforced here (E_VERSION_PLAN section 1, rules 5-6):
- FIXED executables + argument arrays via create_subprocess_exec; NEVER shell=True.
- Hard per-process timeout; process is killed on timeout.
- Output size cap: only the first max_output_bytes are retained/processed.
- Missing tools (FileNotFoundError) are reported as "not executed", never as
  "zero findings". Zero findings is NOT proof of safety.
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
import shutil
import stat
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

logger = logging.getLogger("agentSAFE.analyzers")

DEFAULT_TIMEOUT_SECONDS = 300.0
DEFAULT_MAX_OUTPUT_BYTES = 2_000_000  # 2 MiB retained per stream


class AnalyzerError(RuntimeError):
    """Analyzer-level failure. Partial results may still exist."""


@dataclass
class ProcResult:
    exit_code: int | None
    stdout: bytes
    stderr: bytes
    timed_out: bool = False
    missing: bool = False
    error: str | None = None


@dataclass
class ProcSpec:
    executable: str
    args: list[str]
    cwd: Path
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    max_output_bytes: int = DEFAULT_MAX_OUTPUT_BYTES
    # Extra env vars merged ON TOP of the sanitized env for this process only
    # (e.g. SOLC_VERSION to pin the compiler for one slither run). Keys are
    # validated: simple NAMEs, no embedded NULs - never arbitrary strings.
    extra_env: dict[str, str] | None = None


class SubprocessRunner(Protocol):
    """Injectable runner so unit tests never spawn real processes."""

    async def run(self, spec: ProcSpec) -> ProcResult: ...


@dataclass
class DefaultSubprocessRunner:
    """create_subprocess_exec-based runner. No shell, ever."""

    async def run(self, spec: ProcSpec) -> ProcResult:
        argv = [spec.executable, *spec.args]
        env = _sanitized_env()
        for key, value in (spec.extra_env or {}).items():
            if not re.fullmatch(r"[A-Z_][A-Z0-9_]*", key) or "\x00" in value:
                return ProcResult(
                    None,
                    b"",
                    b"",
                    error=f"refusing invalid extra_env entry: {key!r}",
                )
            env[key] = value
        try:
            proc = await asyncio.create_subprocess_exec(
                *argv,
                cwd=str(spec.cwd),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,  # the sanitized env WITH any validated extra_env merged in
            )
        except FileNotFoundError:
            return ProcResult(
                None, b"", b"", missing=True, error=f"executable not found: {spec.executable}"
            )
        except OSError as exc:
            return ProcResult(None, b"", b"", missing=False, error=f"spawn failed: {exc}")

        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=spec.timeout_seconds
            )
        except TimeoutError:
            try:
                proc.kill()
            except ProcessLookupError:
                pass
            await proc.wait()
            return ProcResult(
                None, b"", b"", timed_out=True, error=f"timeout after {spec.timeout_seconds:.0f}s"
            )

        cap = spec.max_output_bytes
        return ProcResult(
            exit_code=proc.returncode,
            stdout=stdout[:cap],
            stderr=stderr[:cap],
        )


def _sanitized_env() -> dict[str, str]:
    """Minimal env: no secrets inherited by analyzers. PATH is required to find
    solc when the tool shells out internally; that is the worker's controlled
    environment, not the MCP service's."""
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": os.environ.get("HOME", os.environ.get("USERPROFILE", "")),
        "USERPROFILE": os.environ.get("USERPROFILE", ""),
        "APPDATA": os.environ.get("APPDATA", ""),
        "LOCALAPPDATA": os.environ.get("LOCALAPPDATA", ""),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "SOLC_VERSION": "",
    }
    # Explicitly drop anything that looks like a credential.
    return {k: v for k, v in env.items() if v or k == "PATH"}


@dataclass
class TempWorkspace:
    """Temp dir that always cleans up in finally (rule: no residue)."""

    root: Path
    _finalized: bool = field(default=False, repr=False)

    @classmethod
    def create(cls, prefix: str = "agentSAFE-audit-") -> TempWorkspace:
        import tempfile

        root = Path(tempfile.mkdtemp(prefix=prefix))
        return cls(root=root)

    def safe_relpath(self, rel: str) -> Path:
        """Resolve a repo-internal relative path, rejecting traversal/absolute.

        Source file paths come from Etherscan (untrusted-ish): reject anything
        that could escape the workspace.
        """
        norm = (rel or "").replace("\\", "/")
        if not norm:
            raise AnalyzerError("empty file path")
        if norm.startswith("/") or (len(norm) > 1 and norm[1] == ":"):
            raise AnalyzerError(f"absolute path rejected: {rel!r}")
        parts = [seg for seg in norm.split("/") if seg not in ("", ".")]
        if any(seg == ".." for seg in parts):
            raise AnalyzerError(f"path traversal rejected: {rel!r}")
        if not parts:
            raise AnalyzerError(f"empty file path: {rel!r}")
        target = self.root.joinpath(*parts)
        resolved = target.resolve()
        root_resolved = self.root.resolve()
        if root_resolved != resolved and root_resolved not in resolved.parents:
            raise AnalyzerError(f"path escapes workspace: {rel!r}")
        return resolved

    def cleanup(self) -> None:
        if self._finalized:
            return
        self._finalized = True
        shutil.rmtree(self.root, ignore_errors=True)


def safe_relpath_str(rel: str) -> str:
    """Validate + normalize an explorer-provided relative path (no workspace)."""
    norm = (rel or "").replace("\\", "/")
    if not norm or norm.startswith("/") or (len(norm) > 1 and norm[1] == ":"):
        raise AnalyzerError(f"invalid path: {rel!r}")
    parts = [seg for seg in norm.split("/") if seg not in ("", ".")]
    if not parts or any(seg == ".." for seg in parts):
        raise AnalyzerError(f"invalid path: {rel!r}")
    return "/".join(parts)


def is_executable_available(name: str) -> bool:
    """Best-effort PATH check (worker diagnostics only)."""
    found = shutil.which(name)
    if not found:
        return False
    try:
        return bool(found and os.stat(found).st_mode & stat.S_IXUSR)
    except OSError:
        return True  # exists but stat failed; let the runner report the real error
