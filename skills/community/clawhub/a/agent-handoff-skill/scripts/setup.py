#!/usr/bin/env python3
"""Remove legacy user-level handoff entry blocks for supported CLIs."""

from __future__ import annotations

import argparse
import os
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


BEGIN = b"<!-- handoff:global:begin -->"
END = b"<!-- handoff:global:end -->"
AGENTS = ("codex", "claude", "zcode", "kimi")


class SetupError(Exception):
    pass


@dataclass(frozen=True)
class Target:
    agents: tuple[str, ...]
    configured: Path
    path: Path


@dataclass(frozen=True)
class Snapshot:
    exists: bool
    data: bytes | None
    fingerprint: tuple[int, int, int, int] | None
    mode: int | None


@dataclass(frozen=True)
class Change:
    target: Target
    before: Snapshot
    after: bytes
    remove_file: bool = False


def absolute_path(value: str, label: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise SetupError(f"{label} must be an absolute path: {value}")
    return path


def home_root(value: str | None) -> Path:
    return absolute_path(value, "--home-root") if value else Path.home().resolve()


def configured_dir(env_name: str, default: Path, root_was_explicit: bool) -> Path:
    # --home-root is an explicit, hermetic target for tests and dry administration.
    if root_was_explicit:
        return default
    value = os.environ.get(env_name, "").strip()
    return absolute_path(value, env_name) if value else default


def target_candidates(
    root: Path,
    root_was_explicit: bool,
    names: Iterable[str],
    include_inactive: bool = False,
) -> list[tuple[str, Path]]:
    codex = configured_dir("CODEX_HOME", root / ".codex", root_was_explicit)
    claude = configured_dir("CLAUDE_CONFIG_DIR", root / ".claude", root_was_explicit)
    kimi = configured_dir("KIMI_CODE_HOME", root / ".kimi-code", root_was_explicit)
    candidates: list[tuple[str, Path]] = []
    for name in names:
        if name == "codex":
            override = codex / "AGENTS.override.md"
            if include_inactive:
                candidates.extend([(name, override), (name, codex / "AGENTS.md")])
            else:
                candidates.append(
                    (
                        name,
                        override
                        if override.is_file() and override.stat().st_size
                        else codex / "AGENTS.md",
                    )
                )
        elif name == "claude":
            candidates.append((name, claude / "CLAUDE.md"))
        elif name == "zcode":
            candidates.append((name, root / ".zcode" / "AGENTS.md"))
        elif name == "kimi":
            candidates.append((name, kimi / "AGENTS.md"))
        else:  # argparse prevents this; retain a safe boundary for direct use.
            raise SetupError(f"unsupported agent: {name}")
    return candidates


def within(path: Path, root: Path) -> Path:
    try:
        resolved = path.resolve(strict=False)
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise SetupError(f"refusing path outside --home-root: {path}") from error
    return resolved


def target_list(
    root: Path,
    root_was_explicit: bool,
    names: Iterable[str],
    include_inactive: bool = False,
) -> list[Target]:
    grouped: dict[Path, tuple[list[str], Path]] = {}
    for agent, configured in target_candidates(
        root, root_was_explicit, names, include_inactive
    ):
        configured = absolute_path(str(configured), f"{agent} target")
        resolved = within(configured, root)
        if configured.exists() or configured.is_symlink():
            if not configured.exists() or not resolved.is_file():
                raise SetupError(f"target is not a regular file: {configured}")
        bucket = grouped.get(resolved)
        if bucket is None:
            grouped[resolved] = ([agent], configured)
        else:
            bucket[0].append(agent)
    return [
        Target(tuple(agents), configured, path)
        for path, (agents, configured) in grouped.items()
    ]


def fingerprint(path: Path) -> tuple[int, int, int, int]:
    info = path.stat()
    return (info.st_dev, info.st_ino, info.st_mtime_ns, info.st_size)


def snapshot(target: Target) -> Snapshot:
    if not target.path.exists():
        return Snapshot(False, None, None, None)
    if not target.path.is_file():
        raise SetupError(f"target is not a regular file: {target.configured}")
    info = target.path.stat()
    return Snapshot(
        True,
        target.path.read_bytes(),
        fingerprint(target.path),
        stat.S_IMODE(info.st_mode),
    )


def marker_range(data: bytes) -> tuple[int, int] | None:
    begins = data.count(BEGIN)
    ends = data.count(END)
    if begins == 0 and ends == 0:
        return None
    if begins != 1 or ends != 1:
        raise SetupError("abnormal handoff global markers")
    start = data.index(BEGIN)
    finish = data.index(END)
    if finish < start:
        raise SetupError("abnormal handoff global marker order")
    return start, finish + len(END)


def remove_block(data: bytes) -> bytes:
    found = marker_range(data)
    if found is None:
        return data
    start, finish = found
    # The single separator newline immediately before a block is owned by setup.py.
    if start and data[start - 1 : start] == b"\n":
        start -= 1
    return data[:start] + data[finish:]


def unchanged(target: Target, before: Snapshot) -> bool:
    if (
        target.configured.resolve(strict=False) != target.path
        or target.path.resolve(strict=False) != target.path
    ):
        return False
    if not before.exists:
        return not target.path.exists() and not target.path.is_symlink()
    return (
        target.path.exists()
        and fingerprint(target.path) == before.fingerprint
        and target.path.read_bytes() == before.data
    )


def write_atomic(path: Path, data: bytes, mode: int | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.handoff-", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            os.chmod(temporary, mode)
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def confirm_unchanged(change: Change) -> None:
    if not unchanged(change.target, change.before):
        raise SetupError(
            f"concurrent change detected before writing: {change.target.path}"
        )


def rollback(written: list[Change]) -> list[str]:
    failures: list[str] = []
    for change in reversed(written):
        path = change.target.path
        try:
            # A remove_file change expects the path to be absent, so only a
            # reappeared non-empty file counts as concurrently changed.
            if change.remove_file:
                conflicted = path.exists() and path.read_bytes() != change.after
            else:
                conflicted = not path.exists() or path.read_bytes() != change.after
            if conflicted:
                failures.append(f"not restoring concurrently changed file: {path}")
            elif change.before.exists:
                write_atomic(path, change.before.data or b"", change.before.mode)
            else:
                path.unlink()
        except OSError as error:
            failures.append(f"could not restore {path}: {error}")
    return failures


def apply(changes: list[Change]) -> None:
    for change in changes:
        confirm_unchanged(change)
    written: list[Change] = []
    try:
        for change in changes:
            if change.remove_file:
                confirm_unchanged(change)
                change.target.path.unlink()
                written.append(change)
            elif change.after == (change.before.data or b""):
                continue
            else:
                confirm_unchanged(change)
                write_atomic(change.target.path, change.after, change.before.mode)
                written.append(change)
    except Exception as error:
        restored = rollback(written)
        detail = f"; rollback problems: {'; '.join(restored)}" if restored else ""
        raise SetupError(f"write failed: {error}{detail}") from error


def print_status(targets: list[Target]) -> int:
    all_clean = True
    for target in targets:
        if target.path.exists():
            state = (
                "legacy"
                if marker_range(target.path.read_bytes()) is not None
                else "clean"
            )
        else:
            state = "clean"
        all_clean = all_clean and state == "clean"
        print(f"{','.join(target.agents)}\t{state}\t{target.configured}")
    return 0 if all_clean else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("status", "disable"))
    parser.add_argument(
        "--agents", choices=AGENTS, nargs="+", help="CLI configurations to manage"
    )
    parser.add_argument(
        "--home-root", help="absolute home directory used to resolve target paths"
    )
    args = parser.parse_args()
    if args.command == "disable" and not args.agents:
        parser.error("disable requires --agents")
    if args.command == "status" and not args.agents:
        args.agents = list(AGENTS)
    args.agents = list(dict.fromkeys(args.agents))
    return args


def main() -> int:
    args = parse_args()
    root_was_explicit = args.home_root is not None
    root = home_root(args.home_root)
    if not root.exists() or not root.is_dir():
        raise SetupError(f"home root is not a directory: {root}")
    targets = target_list(
        root, root_was_explicit, args.agents, args.command == "disable"
    )
    if args.command == "status":
        return print_status(targets)
    selected_paths = {target.path for target in targets}
    for agent, configured in target_candidates(root, root_was_explicit, AGENTS, True):
        if agent in args.agents or not (configured.exists() or configured.is_symlink()):
            continue
        try:
            shared = configured.resolve() in selected_paths
        except (OSError, RuntimeError):
            shared = False
        if shared:
            raise SetupError(
                f"selected rule file is shared with {agent}; include that CLI or separate the shared configuration"
            )
    changes = []
    for target in targets:
        before = snapshot(target)
        after = remove_block(before.data or b"")
        remove_file = before.exists and not after.strip()
        changes.append(Change(target, before, after, remove_file))
    apply(changes)
    for change in changes:
        outcome = "removed" if change.remove_file else "disabled"
        print(
            f"{','.join(change.target.agents)}\t{outcome}\t{change.target.configured}"
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SetupError as error:
        print(f"setup.py: {error}", file=sys.stderr)
        raise SystemExit(2)
