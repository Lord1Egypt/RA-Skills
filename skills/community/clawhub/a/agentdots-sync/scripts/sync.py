#!/usr/bin/env python3
"""Safely copy selected agent assets between a local root and a Git clone."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, NamedTuple, Sequence


MAX_BACKUPS = 10


class PlatformProfile(NamedTuple):
    """Safe defaults for one local agent platform."""

    name: str
    default_root: str | None
    default_assets: tuple[str, ...]
    backup_dir_name: str
    aliases: tuple[str, ...] = ()
    note: str = ""


PLATFORM_PROFILES = (
    PlatformProfile(
        "codex",
        "~/.codex",
        ("AGENTS.md", "rules", "skills"),
        ".codex_backups",
        aliases=("openai-codex",),
        note="Codex user assets",
    ),
    PlatformProfile(
        "claude-code",
        "~/.claude",
        ("CLAUDE.md", "rules", "skills"),
        ".meta-sync-backups",
        aliases=("claude",),
        note="Claude Code user assets",
    ),
    PlatformProfile(
        "opencode",
        "~/.config/opencode",
        ("skills",),
        ".meta-sync-backups",
        note="OpenCode global skills; select config files explicitly",
    ),
    PlatformProfile(
        "grok-build",
        "~/.grok",
        ("skills",),
        ".meta-sync-backups",
        aliases=("grok",),
        note="Grok Build user skills; select config files explicitly",
    ),
    PlatformProfile(
        "codebuddy-code",
        "~/.codebuddy",
        ("rules", "skills"),
        ".meta-sync-backups",
        aliases=("codebuddy",),
        note="CodeBuddy Code user rules and skills",
    ),
    PlatformProfile(
        "workbuddy",
        None,
        ("skills",),
        ".meta-sync-backups",
        note="WorkBuddy package workspace; explicit root required",
    ),
    PlatformProfile(
        "custom",
        None,
        (),
        ".meta-sync-backups",
        note="Any Agent Skills-compatible layout; explicit root and assets required",
    ),
)

PROFILE_LOOKUP = {
    key: profile
    for profile in PLATFORM_PROFILES
    for key in (profile.name, *profile.aliases)
}


class SyncError(RuntimeError):
    """A safe, user-facing failure while synchronising local assets."""


def resolve_profile(name: str) -> PlatformProfile:
    """Resolve a canonical platform profile or one of its documented aliases."""
    try:
        return PROFILE_LOOKUP[name]
    except KeyError as error:
        raise SyncError(f"unknown platform: {name}") from error


def resolve_selection(
    platform_name: str,
    root_value: str | None,
    asset_values: Iterable[str] | None,
    backup_dir_value: str | None = None,
) -> tuple[PlatformProfile, Path, list[str], Path]:
    """Resolve and validate one profile without mutating the filesystem."""
    profile = resolve_profile(platform_name)
    if root_value is None:
        if profile.default_root is None:
            raise SyncError(f"platform '{profile.name}' requires explicit --root")
        root_value = profile.default_root
    if asset_values is None:
        if not profile.default_assets:
            raise SyncError(f"platform '{profile.name}' requires at least one --asset")
        asset_values = profile.default_assets
    root = validate_root(root_value)
    assets = validate_assets(root, asset_values)
    backup_value = backup_dir_value or profile.backup_dir_name
    backup_dir = validate_backup_dir(root, assets, backup_value)
    return profile, root, assets, backup_dir


def print_platforms() -> None:
    """Print canonical profile defaults without touching any platform root."""
    for profile in PLATFORM_PROFILES:
        root = profile.default_root or "<required>"
        assets = ",".join(profile.default_assets) or "<required>"
        aliases = ",".join(profile.aliases) or "-"
        print(
            f"{profile.name}\troot={root}\tassets={assets}\t"
            f"backup={profile.backup_dir_name}\taliases={aliases}\t{profile.note}"
        )


def print_doctor(
    profile: PlatformProfile, root: Path, assets: Sequence[str], backup_dir: Path
) -> None:
    """Report local prerequisites and resolved targets without writing files."""
    git = shutil.which("git")
    print(f"DOCTOR platform={profile.name}")
    print(f"root={root}")
    print(f"root_exists={'yes' if root.exists() else 'no'}")
    print(f"assets={', '.join(assets)}")
    print(f"backup_dir={backup_dir}")
    print(f"git={git or 'missing'}")
    print(f"python={sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")


def _redact_sensitive_text(value: str) -> str:
    """Avoid exposing URL credentials while retaining useful command stderr."""
    value = re.sub(r"([A-Za-z][A-Za-z0-9+.-]*://)[^/@\s]*@", r"\1***@", value)
    value = re.sub(r"\bBearer\s+\S+", "Bearer ***", value, flags=re.IGNORECASE)
    return re.sub(
        r"(?i)\b(?:token|access_token|api_key|password|secret|auth)=([^\s&#]+)",
        "***",
        value,
    )


def run_command(args: list[str], cwd: Path | None = None) -> str:
    """Run one command without a shell and preserve safe stderr on failure."""
    if not isinstance(args, list) or not args or not all(isinstance(arg, str) for arg in args):
        raise SyncError("command must be a non-empty argument list")
    try:
        result = subprocess.run(
            args,
            cwd=str(cwd) if cwd is not None else None,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError as error:
        raise SyncError(_redact_sensitive_text(str(error))) from error
    if result.returncode:
        detail = _redact_sensitive_text(result.stderr.strip())
        raise SyncError(detail or "command failed")
    return result.stdout


@contextmanager
def _mutation_lock(root: Path):
    """Serialize mutating CLI transactions for one root with an atomic lock file."""
    lock = root / ".meta-sync-lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as error:
        raise SyncError(
            f"another mutation may be active for this root; inspect and remove stale lock only after verification: {lock}"
        ) from error
    except OSError as error:
        raise SyncError(f"cannot acquire mutation lock: {error}") from error
    try:
        os.write(descriptor, f"pid={os.getpid()}\n".encode("ascii"))
        yield
    finally:
        os.close(descriptor)
        try:
            lock.unlink()
        except FileNotFoundError:
            pass
        except OSError as error:
            raise SyncError(f"cannot release mutation lock: {error}") from error


def validate_root(root: Path | str) -> Path:
    """Return a normalised root while rejecting dangerous broad targets."""
    resolved = Path(root).expanduser().resolve(strict=False)
    home = Path.home().resolve(strict=False)
    if resolved == Path(resolved.anchor) or resolved == home:
        raise SyncError("refusing to modify filesystem root or the user home directory")
    return resolved


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _asset_path(root: Path, asset: str) -> Path:
    candidate = root / asset
    if not _is_within(candidate.resolve(strict=False), root):
        raise SyncError(f"asset escapes root: {asset}")
    return candidate


def validate_assets(root: Path | str, assets: Iterable[str]) -> list[str]:
    """Validate unique, relative asset paths and reject escaping symlinks."""
    root_path = validate_root(root)
    checked: list[str] = []
    seen: set[str] = set()
    for asset in assets:
        if not isinstance(asset, str) or not asset:
            raise SyncError("asset paths must be non-empty strings")
        path = Path(asset)
        if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
            raise SyncError(f"asset must be a safe relative path: {asset}")
        first_part = path.parts[0]
        if first_part in {".git", ".codex_backups"} or first_part.startswith(".meta-sync-"):
            raise SyncError(f"asset uses a reserved internal path: {asset}")
        normalised = path.as_posix()
        if normalised in seen:
            raise SyncError(f"duplicate asset: {normalised}")
        _asset_path(root_path, normalised)
        seen.add(normalised)
        checked.append(normalised)
    if not checked:
        raise SyncError("at least one asset is required")
    return checked


def validate_backup_dir(root: Path | str, assets: Iterable[str], backup_dir: Path | str) -> Path:
    """Require backups to live in a non-symlinked, separate child of root."""
    root_path = validate_root(root)
    selected = validate_assets(root_path, assets)
    root_lexical = Path(os.path.abspath(str(Path(root).expanduser())))
    raw = Path(backup_dir).expanduser()
    if not raw.is_absolute():
        raw = root_lexical / raw
    lexical = Path(os.path.abspath(str(raw)))
    resolved = lexical.resolve(strict=False)
    if resolved == root_path or not _is_within(resolved, root_path):
        raise SyncError("backup directory must be a strict child of root")
    try:
        relative_parts = lexical.relative_to(root_lexical).parts
    except ValueError:
        relative_parts = resolved.relative_to(root_path).parts
    current = root_lexical
    for component in relative_parts:
        current = current / component
        if current.is_symlink():
            raise SyncError("backup directory cannot traverse a symlink")
    for asset in selected:
        asset_path = _asset_path(root_path, asset)
        asset_resolved = asset_path.resolve(strict=False)
        if _is_within(resolved, asset_resolved) or _is_within(asset_resolved, resolved):
            raise SyncError("backup directory must not overlap a selected asset")
    return resolved


def validate_branch(branch: str) -> str:
    """Accept only a conservative, non-option Git branch ref."""
    forbidden = set("~^:?*[") | {"\\"}
    if (
        not isinstance(branch, str)
        or not branch
        or branch == "@"
        or branch.startswith("-")
        or branch.startswith(("/", "."))
        or branch.endswith(("/", "."))
        or branch.endswith(".lock")
        or ".." in branch
        or "@{" in branch
        or any(
            character.isspace()
            or ord(character) < 32
            or ord(character) == 127
            or character in forbidden
            for character in branch
        )
        or any(
            not component
            or component.startswith(".")
            or component.endswith(".lock")
            for component in branch.split("/")
        )
    ):
        raise SyncError("branch is not a valid Git ref")
    return branch


def validate_remote(remote: str) -> str:
    """Reject option-like and control-character remote values."""
    if (
        not isinstance(remote, str)
        or not remote
        or remote.startswith("-")
        or any(character.isspace() or ord(character) < 32 for character in remote)
    ):
        raise SyncError("remote is invalid")
    return remote


def _ensure_asset_tree_safe(root: Path, asset: str) -> Path:
    """Ensure copied symlinks are relative and remain inside the selected asset."""
    asset_path = _asset_path(root, asset)
    if not asset_path.exists() and not asset_path.is_symlink():
        raise SyncError(f"selected asset does not exist: {asset}")
    if asset_path.is_symlink():
        raise SyncError(f"selected asset cannot itself be a symlink: {asset}")
    asset_root = asset_path.resolve(strict=False)
    paths = [asset_path]
    if asset_path.is_dir():
        for directory, dirnames, filenames in os.walk(asset_path, followlinks=False):
            paths.extend(Path(directory) / name for name in (*dirnames, *filenames))
    for path in paths:
        if not path.is_symlink():
            continue
        try:
            link_target = Path(os.readlink(path))
        except OSError as error:
            raise SyncError(f"cannot inspect asset symlink: {asset}") from error
        if link_target.is_absolute():
            raise SyncError(f"asset contains a nonportable absolute symlink: {asset}")
        resolved_target = path.resolve(strict=False)
        if not _is_within(resolved_target, root):
            raise SyncError(f"asset symlink escapes root: {asset}")
        if not _is_within(resolved_target, asset_root):
            raise SyncError(f"asset symlink crosses the selected asset boundary: {asset}")
    return asset_path


def _copy_to_staging(source: Path, staging: Path) -> None:
    staging.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir() and not source.is_symlink():
        shutil.copytree(source, staging, symlinks=True)
    else:
        shutil.copy2(source, staging, follow_symlinks=False)


def _remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def _atomic_replace(source: Path, target: Path) -> None:
    """Stage beside target, then swap while retaining the old value on failure."""
    parent = target.parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
        stage_parent = Path(tempfile.mkdtemp(prefix=".meta-sync-stage-", dir=parent))
    except OSError as error:
        raise SyncError(f"cannot create replacement staging directory: {error}") from error
    staged = stage_parent / target.name
    old = parent / f".{target.name}.meta-sync-old-{uuid.uuid4().hex}"
    try:
        _copy_to_staging(source, staged)
    except OSError as error:
        shutil.rmtree(stage_parent, ignore_errors=True)
        raise SyncError(f"cannot stage replacement: {error}") from error
    try:
        moved_old = target.exists() or target.is_symlink()
        if moved_old:
            os.replace(target, old)
        try:
            os.replace(staged, target)
        except OSError as swap_error:
            if moved_old and not target.exists() and not target.is_symlink():
                try:
                    os.replace(old, target)
                except OSError as restore_error:
                    raise SyncError(
                        f"replacement failed; old data retained at {old}: {restore_error}"
                    ) from restore_error
            raise SyncError(f"replacement failed; original target restored: {swap_error}") from swap_error
    except OSError as error:
        raise SyncError(f"cannot exchange replacement target: {error}") from error
    finally:
        if stage_parent.exists():
            shutil.rmtree(stage_parent, ignore_errors=True)
    if moved_old and (old.exists() or old.is_symlink()):
        try:
            _remove_path(old)
        except OSError as error:
            raise SyncError(f"replacement succeeded but old data remains at {old}: {error}") from error


def _safe_reason(reason: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", reason).strip(".-")
    return cleaned or "backup"


def _backup_directories(backup_dir: Path) -> list[Path]:
    if not backup_dir.exists():
        return []
    return sorted(
        (item for item in backup_dir.iterdir() if item.is_dir() and not item.name.startswith(".meta-sync-")),
        key=lambda item: item.stat().st_mtime,
    )


def _read_manifest(backup: Path, root: Path) -> list[str]:
    manifest_path = backup / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SyncError("backup manifest is missing or invalid") from error
    assets = manifest.get("assets") if isinstance(manifest, dict) else None
    if not isinstance(assets, list):
        raise SyncError("backup manifest has no valid assets list")
    validated = validate_assets(root, assets)
    if validated != assets:
        raise SyncError("backup manifest asset paths are not canonical")
    for asset in validated:
        _ensure_asset_tree_safe(backup, asset)
    return validated


def create_local_backup(
    root: Path | str, assets: Iterable[str], backup_dir: Path | str, reason: str
) -> Path:
    """Atomically save actual selected assets and retain the newest ten backups."""
    root_path = validate_root(root)
    selected = validate_assets(root_path, assets)
    backup_path = validate_backup_dir(root, selected, backup_dir)
    existing = [
        asset
        for asset in selected
        if _asset_path(root_path, asset).exists() or _asset_path(root_path, asset).is_symlink()
    ]
    if not existing:
        raise SyncError("no selected assets exist to back up")
    try:
        backup_path.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise SyncError(f"cannot create backup directory: {error}") from error
    staging = Path(tempfile.mkdtemp(prefix=".meta-sync-backup-", dir=backup_path))
    copied: list[str] = []
    try:
        for asset in existing:
            source = _asset_path(root_path, asset)
            if not source.exists() and not source.is_symlink():
                continue
            _ensure_asset_tree_safe(root_path, asset)
            _copy_to_staging(source, staging / asset)
            copied.append(asset)
        (staging / "manifest.json").write_text(
            json.dumps(
                {
                    "assets": copied,
                    "reason": _safe_reason(reason),
                    "created_at": datetime.now(timezone.utc).isoformat(),
                },
                ensure_ascii=False,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
        final = backup_path / (
            f"backup_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}_{_safe_reason(reason)}"
        )
        os.replace(staging, final)
        complete: list[Path] = []
        for candidate in _backup_directories(backup_path):
            try:
                _read_manifest(candidate, root_path)
            except SyncError:
                continue
            complete.append(candidate)
        while len(complete) > MAX_BACKUPS:
            _remove_path(complete.pop(0))
        return final
    except Exception:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        raise


def rollback_latest_backup(
    root: Path | str, assets: Iterable[str], backup_dir: Path | str
) -> Path:
    """Validate the newest backup completely before protecting and restoring state."""
    root_path = validate_root(root)
    requested = validate_assets(root_path, assets)
    backup_path = validate_backup_dir(root, requested, backup_dir)
    candidates = _backup_directories(backup_path)
    if not candidates:
        raise SyncError("no backup is available for rollback")
    historical: Path | None = None
    manifest_assets: list[str] | None = None
    for candidate in reversed(candidates):
        try:
            manifest_assets = _read_manifest(candidate, root_path)
            historical = candidate
            break
        except SyncError:
            continue
    if historical is None or manifest_assets is None:
        raise SyncError("no complete backup is available for rollback")
    present = [
        asset
        for asset in requested
        if _asset_path(root_path, asset).exists() or _asset_path(root_path, asset).is_symlink()
    ]
    if present:
        create_local_backup(root, requested, backup_path, reason="before_rollback")
    for asset in (item for item in requested if item in manifest_assets):
        _atomic_replace(_ensure_asset_tree_safe(historical, asset), _asset_path(root_path, asset))
    return historical


def copy_assets(
    source_root: Path | str, destination_root: Path | str, assets: Iterable[str]
) -> list[str]:
    """Atomically replace only selected destination assets from a validated source tree."""
    source = validate_root(source_root)
    destination = validate_root(destination_root)
    selected = validate_assets(source, assets)
    validate_assets(destination, selected)
    for asset in selected:
        _atomic_replace(_ensure_asset_tree_safe(source, asset), _asset_path(destination, asset))
    return selected


def apply_assets_from_tree(
    source_root: Path | str,
    root: Path | str,
    assets: Iterable[str],
    backup_dir: Path | str,
    reason: str,
) -> Path:
    """Create a recovery point before applying selected, validated source assets."""
    source = validate_root(source_root)
    root_path = validate_root(root)
    selected = validate_assets(root_path, assets)
    source_assets = validate_assets(source, selected)
    for asset in source_assets:
        _ensure_asset_tree_safe(source, asset)
    present = [
        asset
        for asset in selected
        if _asset_path(root_path, asset).exists() or _asset_path(root_path, asset).is_symlink()
    ]
    backup = create_local_backup(root, selected, backup_dir, reason) if present else None
    copy_assets(source, root_path, source_assets)
    return backup


def _clone_remote(remote: str, branch: str, temporary: Path) -> Path:
    remote = validate_remote(remote)
    branch = validate_branch(branch)
    clone = temporary / "repository"
    run_command(["git", "clone", "--branch", branch, "--single-branch", "--", remote, str(clone)])
    return clone


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Safely sync selected agent assets")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--apply", action="store_true")
    actions.add_argument("--restore", action="store_true")
    actions.add_argument("--rollback", action="store_true")
    actions.add_argument("--push", action="store_true")
    actions.add_argument("--doctor", action="store_true")
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--list-platforms", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument(
        "--platform",
        default="codex",
        choices=sorted(PROFILE_LOOKUP),
        help="platform profile or alias (default: codex)",
    )
    parser.add_argument("--root", help="override the profile's local root")
    parser.add_argument("--asset", action="append")
    parser.add_argument(
        "--backup-dir",
        help="override the profile's backup directory; must remain inside root",
    )
    parser.add_argument("--remote")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--message", default="chore(sync): update selected assets")
    args = parser.parse_args(argv)

    try:
        if args.list_platforms:
            if any((args.apply, args.restore, args.rollback, args.push, args.doctor)):
                raise SyncError("--list-platforms cannot be combined with another action")
            print_platforms()
            return 0
        profile, root, assets, backup_dir = resolve_selection(
            args.platform,
            args.root,
            args.asset,
            args.backup_dir,
        )
        if args.doctor:
            print_doctor(profile, root, assets, backup_dir)
            return 0
        if args.plan or not any((args.apply, args.restore, args.rollback, args.push)):
            action = next(
                (
                    name
                    for name, selected in (
                        ("apply", args.apply),
                        ("restore", args.restore),
                        ("rollback", args.rollback),
                        ("push", args.push),
                    )
                    if selected
                ),
                "inspect",
            )
            remote_required = action in {"apply", "restore", "push"}
            remote = (
                _redact_sensitive_text(validate_remote(args.remote))
                if args.remote
                else "<required>" if remote_required else "-"
            )
            branch = validate_branch(args.branch) if remote_required else "-"
            print(
                f"PLAN platform={profile.name} action={action} root={root} "
                f"assets={', '.join(assets)} backup_dir={backup_dir} "
                f"remote={remote} branch={branch}"
            )
            return 0
        if not args.yes:
            raise SyncError("mutating actions require --yes")
        with _mutation_lock(root):
            if args.rollback:
                restored = rollback_latest_backup(root, assets, backup_dir)
                print(f"ROLLED BACK from {restored}")
                return 0
            if not args.remote:
                raise SyncError("--remote is required for this action")
            remote = validate_remote(args.remote)
            branch = validate_branch(args.branch)
            with tempfile.TemporaryDirectory(prefix="meta-sync-") as temporary_dir:
                clone = _clone_remote(remote, branch, Path(temporary_dir))
                if args.apply or args.restore:
                    backup = apply_assets_from_tree(
                        clone, root, assets, backup_dir, "apply" if args.apply else "restore"
                    )
                    print(f"APPLIED selected assets; backup={backup}")
                    return 0
                copy_assets(root, clone, assets)
                run_command(["git", "add", "--", *assets], cwd=clone)
                staged_paths = run_command(
                    ["git", "diff", "--cached", "--name-only", "--"], cwd=clone
                ).splitlines()
                if not staged_paths:
                    print("PUSH skipped: selected assets have no changes")
                    return 0
                if any(
                    not any(path == asset or path.startswith(f"{asset}/") for asset in assets)
                    for path in staged_paths
                ):
                    raise SyncError("staged changes include paths outside selected assets")
                run_command(["git", "commit", "-m", args.message], cwd=clone)
                run_command(["git", "push", "origin", "--", branch], cwd=clone)
                print("PUSH completed")
                return 0
    except SyncError as error:
        print(_redact_sensitive_text(str(error)), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
