"""Atomic native MCP configuration mutation with descriptor-based safety."""
from __future__ import annotations

import json
import os
import re
import secrets
import stat
import subprocess
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Callable

from agent_clients import McpServerSpec
from config_codecs import UnsupportedConfigFormat, render_codex_toml
from install_plan import InstallPlan, InstallPlanError, InstallTarget, validate_install_receipt


class InstallError(RuntimeError):
    pass


@dataclass(frozen=True)
class ApplyResult:
    client_id: str
    config_path: Path
    backup_path: Path
    status: str


_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)
_DIRECTORY = getattr(os, "O_DIRECTORY", 0)


def _entry(spec: McpServerSpec, client_id: str) -> dict[str, object]:
    if client_id == "opencode":
        return {"command": [spec.command, *spec.args], "cwd": str(spec.cwd)}
    return {"command": spec.command, "args": list(spec.args), "cwd": str(spec.cwd)}


def _open_directory(path: Path) -> int:
    """Open every path component without following symlinks."""
    absolute = path.absolute()
    if not absolute.is_absolute():
        raise InstallError("configuration directory must be absolute")
    fd = os.open(absolute.anchor, os.O_RDONLY | _DIRECTORY)
    try:
        for component in absolute.parts[1:]:
            next_fd = os.open(component, os.O_RDONLY | _DIRECTORY | _NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        return fd
    except Exception:
        os.close(fd)
        raise


def _read_regular(parent_fd: int, name: str) -> tuple[bytes, os.stat_result]:
    fd = os.open(name, os.O_RDONLY | _NOFOLLOW, dir_fd=parent_fd)
    try:
        metadata = os.fstat(fd)
        if not stat.S_ISREG(metadata.st_mode):
            raise InstallError("configuration target must remain a regular non-symlink file")
        payload = bytearray()
        while chunk := os.read(fd, 64 * 1024):
            payload.extend(chunk)
        return bytes(payload), metadata
    finally:
        os.close(fd)


def _assert_current_identity(parent_fd: int, name: str, expected: os.stat_result) -> None:
    current = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    if not stat.S_ISREG(current.st_mode) or (current.st_dev, current.st_ino) != (expected.st_dev, expected.st_ino):
        raise InstallError("configuration target changed during installation")


def _assert_current_state(parent_fd: int, name: str, expected: os.stat_result, expected_digest: str) -> None:
    _assert_current_identity(parent_fd, name, expected)
    current, _ = _read_regular(parent_fd, name)
    if "sha256:" + sha256(current).hexdigest() != expected_digest:
        raise InstallError("configuration content changed during installation")


def _exclusive_backup(parent_fd: int, backup_name: str, content: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | _NOFOLLOW
    try:
        fd = os.open(backup_name, flags, 0o600, dir_fd=parent_fd)
    except FileExistsError as exc:
        raise InstallError("refusing to overwrite an existing backup") from exc
    try:
        view = memoryview(content)
        while view:
            written = os.write(fd, view)
            view = view[written:]
        os.fsync(fd)
        os.fchmod(fd, 0o600)
    finally:
        os.close(fd)


def _atomic_replace(parent_fd: int, name: str, content: bytes, expected: os.stat_result, expected_digest: str | None = None) -> None:
    if expected_digest is None:
        _assert_current_identity(parent_fd, name, expected)
    else:
        _assert_current_state(parent_fd, name, expected, expected_digest)
    temp_name = f".{name}.{secrets.token_hex(16)}.tmp"
    fd = os.open(temp_name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | _NOFOLLOW, 0o600, dir_fd=parent_fd)
    try:
        view = memoryview(content)
        while view:
            written = os.write(fd, view)
            view = view[written:]
        os.fsync(fd)
        os.fchmod(fd, 0o600)
        _assert_current_identity(parent_fd, name, expected)
        os.replace(temp_name, name, src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
        os.fsync(parent_fd)
    except Exception:
        try:
            os.unlink(temp_name, dir_fd=parent_fd)
        except FileNotFoundError:
            pass
        raise
    finally:
        os.close(fd)


def _server_container(config: dict[str, object], client_id: str) -> dict[str, object]:
    if client_id == "opencode":
        mcp = config.setdefault("mcp", {})
        if not isinstance(mcp, dict):
            raise InstallError("OpenCode configuration mcp must be an object")
        servers = mcp.setdefault("servers", {})
    else:
        servers = config.setdefault("mcpServers", {})
    if not isinstance(servers, dict):
        raise InstallError("configuration MCP server collection must be an object")
    return servers


def _restore_target(target: InstallTarget) -> None:
    """Restore a previously successful target from its exclusive same-dir backup."""
    path = target.config_path
    parent_fd = _open_directory(path.parent)
    try:
        backup, _ = _read_regular(parent_fd, target.backup_path.name)
        _current, identity = _read_regular(parent_fd, path.name)
        _atomic_replace(parent_fd, path.name, backup, identity)
    finally:
        os.close(parent_fd)


def _verify_written_target(target: InstallTarget, *, json_target: bool) -> None:
    parent_fd = _open_directory(target.config_path.parent)
    try:
        payload, _ = _read_regular(parent_fd, target.config_path.name)
    finally:
        os.close(parent_fd)
    try:
        if json_target:
            if not isinstance(json.loads(payload.decode("utf-8")), dict):
                raise InstallError("post-write configuration root is not an object")
        else:
            import tomllib
            tomllib.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise InstallError("post-write configuration reread failed") from exc


def _apply_target(target: InstallTarget, spec: McpServerSpec, *, json_target: bool, verifier: Callable[[], bool] | None = None) -> ApplyResult:
    path = target.config_path
    parent_fd = _open_directory(path.parent)
    try:
        original, identity = _read_regular(parent_fd, path.name)
        if "sha256:" + sha256(original).hexdigest() != target.config_fingerprint:
            raise InstallError("configuration changed since the reviewed plan")
        if json_target:
            try:
                config = json.loads(original.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                raise InstallError("configuration JSON is invalid") from exc
            if not isinstance(config, dict):
                raise InstallError("configuration root must be an object")
            servers = _server_container(config, target.client_id)
            if spec.name in servers:
                raise InstallError("server name already exists; replacement needs a fresh plan")
            servers[spec.name] = _entry(spec, target.client_id)
            updated = (json.dumps(config, indent=2, sort_keys=True) + "\n").encode("utf-8")
        else:
            try:
                updated = render_codex_toml(original.decode("utf-8"), spec).encode("utf-8")
            except (UnicodeDecodeError, UnsupportedConfigFormat) as exc:
                raise InstallError("Codex configuration is not safely editable") from exc
        _exclusive_backup(parent_fd, target.backup_path.name, original)
        original_digest = "sha256:" + sha256(original).hexdigest()
        # Verify after backup creation but before beginning any replacement.
        _assert_current_state(parent_fd, path.name, identity, original_digest)
        try:
            _atomic_replace(parent_fd, path.name, updated, identity)
            _verify_written_target(target, json_target=json_target)
            if verifier is not None and not verifier():
                raise InstallError("target verification failed")
        except Exception as exc:
            # The replacement created a new inode; use its current identity for rollback.
            current = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
            if not stat.S_ISREG(current.st_mode):
                raise InstallError("installation failed and rollback target is unsafe") from exc
            try:
                _atomic_replace(parent_fd, path.name, original, current)
            except Exception as rollback_error:
                raise InstallError("installation failed and rollback failed") from rollback_error
            if isinstance(exc, InstallError):
                raise
            raise InstallError("installation failed; target was restored") from exc
    finally:
        os.close(parent_fd)
    return ApplyResult(target.client_id, path, target.backup_path, "verified")


def _apply_json_target(target: InstallTarget, spec: McpServerSpec, *, verifier: Callable[[], bool] | None = None) -> ApplyResult:
    return _apply_target(target, spec, json_target=True, verifier=verifier)


def _apply_codex_target(target: InstallTarget, spec: McpServerSpec) -> ApplyResult:
    return _apply_target(target, spec, json_target=False)


def _default_runner(command: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, text=True, capture_output=True, timeout=20, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        raise InstallError(f"official MCP CLI is unavailable: {command[0]}") from exc


def _cli_commands(client_id: str, spec: McpServerSpec) -> tuple[list[str], list[str], list[str]]:
    if client_id == "hermes":
        return (
            ["hermes", "mcp", "add", spec.name, "--command", spec.command, "--args", *spec.args],
            ["hermes", "mcp", "test", spec.name],
            ["hermes", "mcp", "remove", spec.name],
        )
    if client_id == "claude-code":
        return (
            ["claude", "mcp", "add", "--transport", "stdio", spec.name, "--", spec.command, *spec.args],
            ["claude", "mcp", "list"],
            ["claude", "mcp", "remove", spec.name],
        )
    raise InstallError("unsupported official CLI target")


def _run_checked(runner: Callable[[list[str]], subprocess.CompletedProcess[str]], command: list[str], error: str) -> subprocess.CompletedProcess[str]:
    result = runner(command)
    if result.returncode != 0:
        raise InstallError(error)
    return result


def _apply_cli_target(target: InstallTarget, spec: McpServerSpec, runner: Callable[[list[str]], subprocess.CompletedProcess[str]]) -> ApplyResult:
    add, verify, remove = _cli_commands(target.client_id, spec)
    label = "Hermes" if target.client_id == "hermes" else "Claude Code"
    try:
        _run_checked(runner, add, f"{label} MCP registration failed")
        verified = _run_checked(runner, verify, f"{label} MCP verification failed")
        if target.client_id == "claude-code":
            server_line = re.compile(rf"^\s*{re.escape(spec.name)}\s*:")
            connected = any(server_line.match(line) and "Connected" in line for line in verified.stdout.splitlines())
            if not connected:
                raise InstallError("Claude Code MCP verification failed")
    except Exception as exc:
        try:
            _run_checked(runner, remove, f"{label} MCP rollback failed")
        except InstallError as rollback_error:
            raise InstallError(f"{label} MCP operation failed and rollback failed") from rollback_error
        if isinstance(exc, InstallError):
            raise
        raise InstallError(f"{label} MCP operation failed") from exc
    return ApplyResult(target.client_id, target.config_path, target.backup_path, "verified")


def _remove_cli_target(target: InstallTarget, spec: McpServerSpec, runner: Callable[[list[str]], subprocess.CompletedProcess[str]]) -> None:
    _add, _verify, remove = _cli_commands(target.client_id, spec)
    _run_checked(runner, remove, f"{target.client_id} MCP rollback failed")


def _consume_plan(plan: InstallPlan, spec: McpServerSpec, allowed: set[str]) -> None:
    if plan.server != spec:
        raise InstallError("server specification is not bound to the supplied plan")
    if any(target.client_id not in allowed for target in plan.targets):
        raise InstallError("plan contains an export-only or unsupported target")
    try:
        validate_install_receipt(plan)
    except InstallPlanError as exc:
        raise InstallError(str(exc)) from exc


def _apply_batch(
    plan: InstallPlan,
    spec: McpServerSpec,
    *,
    allowed: set[str],
    verifiers: dict[str, Callable[[], bool]] | None = None,
    runner: Callable[[list[str]], subprocess.CompletedProcess[str]] | None = None,
) -> tuple[ApplyResult, ...]:
    _consume_plan(plan, spec, allowed)
    checks = verifiers or {}
    command_runner = runner or _default_runner
    completed: list[tuple[InstallTarget, ApplyResult]] = []
    try:
        for target in plan.targets:
            if target.action == "cli-add":
                result = _apply_cli_target(target, spec, command_runner)
            elif target.client_id == "codex":
                result = _apply_codex_target(target, spec)
            else:
                result = _apply_json_target(target, spec, verifier=checks.get(target.client_id))
            completed.append((target, result))
    except Exception as exc:
        rollback_failures: list[Exception] = []
        for completed_target, _result in reversed(completed):
            try:
                if completed_target.action == "cli-add":
                    _remove_cli_target(completed_target, spec, command_runner)
                else:
                    _restore_target(completed_target)
            except Exception as rollback_error:
                rollback_failures.append(rollback_error)
        if rollback_failures:
            raise InstallError("batch installation failed and rollback failed") from rollback_failures[0]
        if isinstance(exc, InstallError):
            raise
        raise InstallError("batch installation failed; prior targets were restored") from exc
    return tuple(result for _target, result in completed)


def apply_native_plan(
    plan: InstallPlan,
    spec: McpServerSpec,
    *,
    verifiers: dict[str, Callable[[], bool]] | None = None,
    runner: Callable[[list[str]], subprocess.CompletedProcess[str]] | None = None,
) -> tuple[ApplyResult, ...]:
    """Consume one receipt and atomically apply supported native adapters."""
    return _apply_batch(
        plan,
        spec,
        allowed={"hermes", "claude-code", "codex", "cursor", "vscode-copilot", "gemini-cli", "opencode"},
        verifiers=verifiers,
        runner=runner,
    )


def apply_json_plan(plan: InstallPlan, spec: McpServerSpec, *, verifiers: dict[str, Callable[[], bool]] | None = None) -> tuple[ApplyResult, ...]:
    return _apply_batch(plan, spec, allowed={"cursor", "vscode-copilot", "gemini-cli", "opencode"}, verifiers=verifiers)


def apply_json_target(target: InstallTarget, spec: McpServerSpec, *, plan: InstallPlan, verifier: Callable[[], bool] | None = None) -> ApplyResult:
    if plan.targets != (target,):
        raise InstallError("single-target apply requires a plan containing exactly that target")
    return apply_json_plan(plan, spec, verifiers={target.client_id: verifier} if verifier else None)[0]
