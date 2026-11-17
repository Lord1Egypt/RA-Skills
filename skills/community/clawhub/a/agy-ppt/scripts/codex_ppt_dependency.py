#!/usr/bin/env python3
"""Resolve the upstream ``codex-ppt-skill`` repository as an external runtime
dependency.

``agy-ppt`` is a standalone repository. It does not vendor, submodule, or copy
the upstream ``codex-ppt-skill`` repository into its own source tree. Anything
that genuinely needs the upstream skill's implementation at runtime resolves
it through this module, which caches a shallow clone **outside** the agy-ppt
repository, outside the Global AGY Skill install location, and outside any
presentation workspace.

Design (single dependency-resolver authority; do not add a second one):

    AGY requires codex-ppt functionality
            |
            v
    resolve_codex_ppt_dependency()
            |
            v
    check external dependency cache
            |
            v
    check upstream latest revision (best-effort; never required for a cache
    hit -- see the network-failure policy below)
            |
            v
    cache current?  YES -> use cache
                    NO  -> update cache (temp checkout -> validate -> atomic
                            rename, so a failed update never corrupts a good
                            cache)
            |
            v
    return resolved codex-ppt root (+ dependency metadata)
            |
            v
    continue normal AGY runtime

"Latest" is defined deterministically as the current HEAD of the upstream
default branch (``main``), i.e. ``origin/main`` -- not a hardcoded, possibly
nonexistent release tag. If upstream later adopts a formal release/tag policy,
that can be layered on top of this resolver without changing its contract.

Network / failure policy:

* Upstream temporarily unreachable + cache exists -> reuse the cache and print
  a clear warning naming the cached commit SHA. This is **not** an API
  fallback: no image-generation backend or paid API is involved anywhere in
  this module.
* Upstream unreachable + no cache -> raise :class:`CodexPptDependencyError`
  with ``error_code="CODEX_PPT_DEPENDENCY_UNAVAILABLE"``. This is a
  dependency/bootstrap failure, never conflated with the Phase 10.3
  ``IMAGE_GENERATION_FAILED`` worker-retry semantics -- those describe a Codex
  image render turn, not fetching this repository.

Authentication: resolving a public GitHub repository over HTTPS never reads or
requires ``OPENAI_API_KEY``, ``CODEX_API_KEY``, ``KIRO_API_KEY``,
``GEMINI_API_KEY``, or any OAuth/session token belonging to AGY, Kiro, or
Codex. Only plain, unauthenticated ``git`` operations against the public
upstream URL are used.

This module intentionally does not touch ``scripts/project_state.py`` (the
frozen Project State control plane), does not add a new Project State error
code, and does not change the generic-image-failure retry policy from
Phase 10.3. A dependency-resolution failure and a Codex image-generation
failure are different failure domains with different owners.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The one trusted upstream URL. Production callers must not accept an
#: arbitrary caller-supplied URL in place of this constant; only the
#: development override below (an explicit local path, never a URL) may
#: replace dependency *resolution*, and even then this constant is unchanged.
UPSTREAM_URL = "https://github.com/ningzimu/codex-ppt-skill.git"

#: Upstream's default branch. "Latest" is defined as this branch's current
#: HEAD -- not a hardcoded, possibly nonexistent release tag.
UPSTREAM_DEFAULT_BRANCH = "main"

#: The subdirectory inside the upstream repository that holds the skill.
UPSTREAM_SKILL_SUBDIR = "skills/codex-ppt"

DEPENDENCY_NAME = "codex-ppt"
METADATA_FILENAME = "dependency.json"
CHECKOUT_DIRNAME = "repo"

#: Environment variable for an explicit, non-secret local development
#: override. Never a production default; never copied into the repository.
LOCAL_OVERRIDE_ENV_VAR = "AGY_PPT_CODEX_PPT_HOME"

#: Environment variable to relocate the external cache root itself (tests use
#: this to guarantee a temp directory; production defaults to the OS cache
#: location computed by :func:`default_cache_root`).
CACHE_ROOT_ENV_VAR = "AGY_PPT_DEPENDENCY_CACHE"

#: Timeout (seconds) for each individual git subprocess call.
DEFAULT_GIT_TIMEOUT = 60.0

# ---------------------------------------------------------------------------
# Error contract
# ---------------------------------------------------------------------------
ERROR_DEPENDENCY_UNAVAILABLE = "CODEX_PPT_DEPENDENCY_UNAVAILABLE"
ERROR_DEPENDENCY_CORRUPT = "CODEX_PPT_DEPENDENCY_CORRUPT"
ERROR_INVALID_OVERRIDE = "CODEX_PPT_DEPENDENCY_OVERRIDE_INVALID"


class CodexPptDependencyError(RuntimeError):
    """A dependency-resolution/bootstrap failure.

    This is a distinct failure domain from Phase 10.3's
    ``IMAGE_GENERATION_FAILED`` worker-retry policy: it means "the codex-ppt
    runtime dependency could not be resolved," never "a Codex image render
    turn failed." Callers must not feed this into the generic image-failure
    retry/blocking policy in ``project_state.py``.
    """

    def __init__(self, message: str, error_code: str = ERROR_DEPENDENCY_UNAVAILABLE) -> None:
        super().__init__(message)
        self.error_code = error_code


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# Cache location
# ---------------------------------------------------------------------------
def default_cache_root() -> Path:
    """OS-appropriate application cache root for the codex-ppt dependency.

    Never inside the agy-ppt repository, never inside the Global AGY Skill
    install location, and never inside a presentation workspace -- all three
    are caller-controlled paths this function has no knowledge of, which is
    exactly the point: this function only ever returns a location under the
    user's OS cache directory.
    """
    override = os.environ.get(CACHE_ROOT_ENV_VAR)
    if override:
        return Path(override).expanduser()
    if sys.platform == "darwin":
        base = Path.home() / "Library" / "Caches"
    elif os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / "agy-ppt" / "dependencies" / DEPENDENCY_NAME


def _dependency_root(cache_root: Path) -> Path:
    return cache_root / CHECKOUT_DIRNAME


def _metadata_path(cache_root: Path) -> Path:
    return cache_root / METADATA_FILENAME


def _tmp_checkout_dir(cache_root: Path) -> Path:
    return cache_root / f".{CHECKOUT_DIRNAME}.tmp"


# ---------------------------------------------------------------------------
# Metadata (kept beside the external cache, never inside the git repository)
# ---------------------------------------------------------------------------
@dataclass
class DependencyMetadata:
    upstream_url: str
    resolved_commit: str
    resolved_at: str
    upstream_branch: str = UPSTREAM_DEFAULT_BRANCH

    def to_dict(self) -> dict[str, str]:
        return {
            "upstream_url": self.upstream_url,
            "upstream_branch": self.upstream_branch,
            "resolved_commit": self.resolved_commit,
            "resolved_at": self.resolved_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DependencyMetadata":
        return cls(
            upstream_url=str(data.get("upstream_url", "")),
            resolved_commit=str(data.get("resolved_commit", "")),
            resolved_at=str(data.get("resolved_at", "")),
            upstream_branch=str(data.get("upstream_branch", UPSTREAM_DEFAULT_BRANCH)),
        )


_CREDENTIAL_LOOKING_KEYS = (
    "token",
    "credential",
    "cookie",
    "password",
    "secret",
    "auth",
)


def _assert_no_credential_shaped_keys(data: dict[str, Any]) -> None:
    for key in data:
        lowered = key.lower()
        if any(marker in lowered for marker in _CREDENTIAL_LOOKING_KEYS):
            raise CodexPptDependencyError(
                f"refusing to write credential-shaped metadata key: {key!r}",
                error_code=ERROR_DEPENDENCY_CORRUPT,
            )


def _write_metadata(cache_root: Path, metadata: DependencyMetadata) -> None:
    payload = metadata.to_dict()
    _assert_no_credential_shaped_keys(payload)
    cache_root.mkdir(parents=True, exist_ok=True)
    body = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=".dependency.", suffix=".json.tmp", dir=cache_root)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(body)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, _metadata_path(cache_root))
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def _read_metadata(cache_root: Path) -> DependencyMetadata | None:
    path = _metadata_path(cache_root)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    return DependencyMetadata.from_dict(data)


# ---------------------------------------------------------------------------
# Git operations (subprocess-based; no network calls from unit tests --
# callers inject a local repository path as ``upstream_url`` instead)
# ---------------------------------------------------------------------------
class GitUnavailableError(CodexPptDependencyError):
    def __init__(self, message: str) -> None:
        super().__init__(message, error_code=ERROR_DEPENDENCY_UNAVAILABLE)


def _run_git(
    args: list[str], *, cwd: str | None = None, timeout: float = DEFAULT_GIT_TIMEOUT
) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(  # noqa: S603 - fixed "git" executable, args are internal
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        raise GitUnavailableError(f"git executable not found: {exc}") from exc
    except subprocess.TimeoutExpired as exc:
        raise GitUnavailableError(f"git command timed out: {' '.join(args)}") from exc
    except OSError as exc:
        raise GitUnavailableError(f"failed to run git: {exc}") from exc


def remote_head_commit(upstream_url: str, branch: str, *, timeout: float = DEFAULT_GIT_TIMEOUT) -> str | None:
    """Return the current commit SHA of ``branch`` on ``upstream_url``.

    Returns ``None`` (never raises) when the remote cannot be reached right
    now -- callers decide whether that is fatal (no cache) or just means "keep
    using the cache" (cache exists). No credential of any kind is used; this
    is a plain, unauthenticated ``git ls-remote``.
    """
    result = _run_git(["ls-remote", upstream_url, f"refs/heads/{branch}"], timeout=timeout)
    if result.returncode != 0:
        return None
    line = result.stdout.strip().splitlines()[0] if result.stdout.strip() else ""
    if not line:
        return None
    sha = line.split("\t", 1)[0].strip()
    return sha or None


def _shallow_clone(upstream_url: str, branch: str, destination: Path, *, timeout: float) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    result = _run_git(
        [
            "clone",
            "--depth",
            "1",
            "--branch",
            branch,
            "--single-branch",
            upstream_url,
            str(destination),
        ],
        timeout=timeout,
    )
    if result.returncode != 0:
        raise CodexPptDependencyError(
            f"failed to clone {upstream_url!r} (branch {branch!r}): {result.stderr.strip()}",
            error_code=ERROR_DEPENDENCY_UNAVAILABLE,
        )


def _checkout_head_commit(repo_dir: Path, *, timeout: float) -> str:
    result = _run_git(["rev-parse", "HEAD"], cwd=str(repo_dir), timeout=timeout)
    if result.returncode != 0:
        raise CodexPptDependencyError(
            f"failed to read HEAD of freshly cloned dependency: {result.stderr.strip()}",
            error_code=ERROR_DEPENDENCY_CORRUPT,
        )
    return result.stdout.strip()


def _validate_checkout(repo_dir: Path) -> None:
    """Minimal sanity check that the checkout is really the expected skill."""
    skill_dir = repo_dir / UPSTREAM_SKILL_SUBDIR
    skill_md = skill_dir / "SKILL.md"
    if not skill_dir.is_dir() or not skill_md.is_file():
        raise CodexPptDependencyError(
            f"cloned dependency does not contain {UPSTREAM_SKILL_SUBDIR}/SKILL.md; "
            "refusing to adopt a corrupt or unexpected checkout",
            error_code=ERROR_DEPENDENCY_CORRUPT,
        )


# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------
@dataclass
class ResolvedDependency:
    """Where the codex-ppt skill can be read from, and how it got there."""

    root: Path
    skill_root: Path
    source: str  # "cache_hit" | "cache_updated" | "cache_stale_offline" | "local_override"
    metadata: DependencyMetadata | None
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": str(self.root),
            "skill_root": str(self.skill_root),
            "source": self.source,
            "metadata": self.metadata.to_dict() if self.metadata else None,
            "warnings": list(self.warnings),
        }


# ---------------------------------------------------------------------------
# Public resolver
# ---------------------------------------------------------------------------
def resolve_codex_ppt_dependency(
    *,
    upstream_url: str | None = None,
    branch: str = UPSTREAM_DEFAULT_BRANCH,
    cache_root: str | Path | None = None,
    local_override: str | Path | None = None,
    timeout: float = DEFAULT_GIT_TIMEOUT,
) -> ResolvedDependency:
    """Resolve the codex-ppt skill root as an external runtime dependency.

    Resolution order:

    1. ``local_override`` (or the ``AGY_PPT_CODEX_PPT_HOME`` environment
       variable) -- an explicit, non-secret local path to an existing
       codex-ppt checkout. Used as-is; never copied or vendored anywhere.
    2. External dependency cache under ``cache_root`` (defaults to
       :func:`default_cache_root`, an OS application-cache location outside
       this repository, outside the Global AGY Skill, and outside any
       presentation workspace):

       * no cache yet -> shallow clone ``upstream_url`` at ``branch`` into a
         temporary checkout, validate it, then atomically rename it into
         place, and record ``dependency.json`` metadata beside the cache
         (never inside the git checkout, never inside this source
         repository).
       * cache exists -> check the remote HEAD of ``branch``:

         * remote reachable and unchanged -> reuse the cache untouched (no
           unnecessary destructive update).
         * remote reachable and changed -> repeat the temp-checkout ->
           validate -> atomic-rename update, so a failed update can never
           leave a half-updated dependency behind.
         * remote unreachable -> reuse the existing cache and return a clear
           warning naming the cached commit. This is a network/availability
           condition, not an API fallback.

    Raises :class:`CodexPptDependencyError` with
    ``error_code="CODEX_PPT_DEPENDENCY_UNAVAILABLE"`` only when there is no
    usable cache *and* the upstream repository cannot be reached (or a
    caller-supplied override path does not exist). This is a
    dependency/bootstrap failure, distinct from the Phase 10.3
    ``IMAGE_GENERATION_FAILED`` worker-retry policy.
    """
    override = local_override if local_override is not None else os.environ.get(LOCAL_OVERRIDE_ENV_VAR)
    if override:
        return _resolve_local_override(override)

    resolved_url = upstream_url or UPSTREAM_URL
    root = Path(cache_root).expanduser() if cache_root is not None else default_cache_root()
    return _resolve_from_cache(resolved_url, branch, root, timeout=timeout)


def _resolve_local_override(override: str | Path) -> ResolvedDependency:
    override_path = Path(override).expanduser()
    if not override_path.is_dir():
        raise CodexPptDependencyError(
            f"{LOCAL_OVERRIDE_ENV_VAR} points to a path that does not exist or is not a "
            f"directory: {override_path}",
            error_code=ERROR_INVALID_OVERRIDE,
        )
    # The override may point directly at the skill directory, or at a full
    # upstream checkout containing skills/codex-ppt/.
    if (override_path / "SKILL.md").is_file():
        skill_root = override_path
    else:
        skill_root = override_path / UPSTREAM_SKILL_SUBDIR
    if not (skill_root / "SKILL.md").is_file():
        raise CodexPptDependencyError(
            f"{LOCAL_OVERRIDE_ENV_VAR}={override_path} does not contain a codex-ppt "
            f"SKILL.md (looked in {override_path} and {skill_root})",
            error_code=ERROR_INVALID_OVERRIDE,
        )
    return ResolvedDependency(
        root=override_path, skill_root=skill_root, source="local_override", metadata=None
    )


def _resolve_from_cache(
    upstream_url: str, branch: str, cache_root: Path, *, timeout: float
) -> ResolvedDependency:
    repo_dir = _dependency_root(cache_root)
    existing_metadata = _read_metadata(cache_root)
    cache_exists = repo_dir.is_dir() and existing_metadata is not None

    remote_head = remote_head_commit(upstream_url, branch, timeout=timeout)

    if remote_head is None:
        # Upstream is unreachable right now.
        if cache_exists:
            warning = (
                "Unable to check/fetch latest upstream revision. "
                f"Using cached codex-ppt revision {existing_metadata.resolved_commit}."
            )
            return ResolvedDependency(
                root=repo_dir,
                skill_root=repo_dir / UPSTREAM_SKILL_SUBDIR,
                source="cache_stale_offline",
                metadata=existing_metadata,
                warnings=[warning],
            )
        raise CodexPptDependencyError(
            "codex-ppt dependency cache is missing and the upstream repository "
            f"({upstream_url}) could not be reached. This is a dependency/bootstrap "
            "failure, not an image-generation failure.",
            error_code=ERROR_DEPENDENCY_UNAVAILABLE,
        )

    if cache_exists and existing_metadata.resolved_commit == remote_head:
        return ResolvedDependency(
            root=repo_dir,
            skill_root=repo_dir / UPSTREAM_SKILL_SUBDIR,
            source="cache_hit",
            metadata=existing_metadata,
        )

    # No cache, or upstream has moved on: (re)build via a temp checkout so a
    # failed update never destroys a working cache.
    metadata = _update_cache(upstream_url, branch, cache_root, timeout=timeout)
    return ResolvedDependency(
        root=repo_dir,
        skill_root=repo_dir / UPSTREAM_SKILL_SUBDIR,
        source="cache_updated",
        metadata=metadata,
    )


def _update_cache(
    upstream_url: str, branch: str, cache_root: Path, *, timeout: float
) -> DependencyMetadata:
    cache_root.mkdir(parents=True, exist_ok=True)
    tmp_dir = _tmp_checkout_dir(cache_root)
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir, ignore_errors=True)

    try:
        _shallow_clone(upstream_url, branch, tmp_dir, timeout=timeout)
        _validate_checkout(tmp_dir)
        commit = _checkout_head_commit(tmp_dir, timeout=timeout)

        final_dir = _dependency_root(cache_root)
        previous_dir = cache_root / f".{CHECKOUT_DIRNAME}.previous"
        if previous_dir.exists():
            shutil.rmtree(previous_dir, ignore_errors=True)
        if final_dir.exists():
            os.replace(final_dir, previous_dir)
        os.replace(tmp_dir, final_dir)
        if previous_dir.exists():
            shutil.rmtree(previous_dir, ignore_errors=True)

        metadata = DependencyMetadata(
            upstream_url=upstream_url,
            resolved_commit=commit,
            resolved_at=now_iso(),
            upstream_branch=branch,
        )
        _write_metadata(cache_root, metadata)
        return metadata
    finally:
        if tmp_dir.exists():
            shutil.rmtree(tmp_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Thin CLI (diagnostics only; AGY runtime calls the function directly)
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Resolve the codex-ppt external runtime dependency (diagnostics)."
    )
    parser.add_argument("--upstream-url", default=None)
    parser.add_argument("--branch", default=UPSTREAM_DEFAULT_BRANCH)
    parser.add_argument("--cache-root", default=None)
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        resolved = resolve_codex_ppt_dependency(
            upstream_url=args.upstream_url, branch=args.branch, cache_root=args.cache_root
        )
    except CodexPptDependencyError as exc:
        print(
            json.dumps({"error_code": exc.error_code, "error_message": str(exc)}, indent=2),
            file=sys.stderr,
        )
        return 1

    for warning in resolved.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    print(json.dumps(resolved.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
