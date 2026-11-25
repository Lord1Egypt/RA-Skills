"""Build reviewed, secret-free MCP installation plans without mutation."""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import tomllib
from typing import Any
import approval
from agent_clients import McpServerSpec


class InstallPlanError(ValueError):
    pass


@dataclass(frozen=True)
class InstallTarget:
    client_id: str
    config_path: Path
    action: str
    config_fingerprint: str
    backup_path: Path
    verification: str

    def to_public_dict(self) -> dict[str, str]:
        return {"client_id": self.client_id, "config_path": str(self.config_path), "action": self.action, "config_fingerprint": self.config_fingerprint, "backup_path": str(self.backup_path), "verification": self.verification}


@dataclass(frozen=True)
class InstallPlan:
    server: McpServerSpec
    targets: tuple[InstallTarget, ...]

    def to_public_dict(self) -> dict[str, Any]:
        return {"server": self.server.to_public_dict(), "targets": [target.to_public_dict() for target in self.targets]}

    @property
    def digest(self) -> str:
        canonical = json.dumps(self.to_public_dict(), sort_keys=True, separators=(",", ":"))
        return "sha256:" + sha256(canonical.encode("utf-8")).hexdigest()


def issue_install_receipt(plan: InstallPlan) -> Path:
    """Issue a final-confirmation receipt bound to exactly this public plan."""
    return approval.issue_receipt(plan.digest)


def validate_install_receipt(plan: InstallPlan) -> None:
    """Consume a receipt only when it matches the unchanged installation plan."""
    try:
        approval.validate_and_consume_receipt(plan.digest)
    except approval.ApprovalError as exc:
        raise InstallPlanError("installation confirmation is missing, expired, used, or changed") from exc


def _has_symlink_ancestor(path: Path) -> bool:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        if current.is_symlink():
            return True
    return False


def _contains_without_symlinks(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return False
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            return False
    try:
        return path.resolve().is_relative_to(root)
    except OSError:
        return False


def _fingerprint(path: Path, *, root: Path) -> str:
    if not _contains_without_symlinks(path, root):
        raise InstallPlanError("configuration target must remain under a non-symlink home directory")
    if path.exists() and (path.is_symlink() or not path.is_file()):
        raise InstallPlanError("configuration target must be a regular non-symlink file")
    payload = path.read_bytes() if path.exists() else b""
    return "sha256:" + sha256(payload).hexdigest()


_CLI_TARGETS = {"hermes", "claude-code"}


def _target_path(home: Path, client: str) -> Path:
    mapping = {
        "hermes": home / ".hermes/config.yaml",
        "claude-code": home / ".claude.json",
        "codex": home / ".codex/config.toml",
        "cursor": home / ".cursor/mcp.json",
        "vscode-copilot": home / ".config/Code/User/mcp.json",
        "gemini-cli": home / ".gemini/settings.json",
        "opencode": home / ".config/opencode/opencode.json",
    }
    if client not in mapping:
        raise InstallPlanError(f"unsupported native plan target: {client}")
    return mapping[client]


def _has_duplicate(path: Path, client: str, name: str) -> bool:
    if not path.exists(): return False
    if client == "codex":
        try:
            value = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            raise InstallPlanError("configuration TOML is invalid; refusing a plan") from exc
        servers = value.get("mcp_servers", {})
        return isinstance(servers, dict) and name.replace("-", "_") in servers
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise InstallPlanError("configuration JSON is invalid; refusing a plan") from exc
    if client == "opencode": return name in value.get("mcp", {}).get("servers", {})
    return name in value.get("mcpServers", {})


def _snapshot_spec(spec: McpServerSpec) -> McpServerSpec:
    """Copy the descriptor and reject values that could carry literal secrets."""
    if spec.command != "node" or not spec.args:
        raise InstallPlanError("only node stdio descriptors with an entry argument are exportable")
    suspicious = ("token", "secret", "password", "apikey", "api_key", "authorization")
    if any("=" in value or any(marker in value.lower() for marker in suspicious) for value in (spec.command, *spec.args)):
        raise InstallPlanError("portable export refuses descriptor fields that resemble literal secrets")
    return McpServerSpec(spec.name, spec.command, tuple(spec.args), Path(str(spec.cwd)), tuple(spec.env_names))


def build_plan(spec: McpServerSpec, *, selected: tuple[str, ...], home: Path) -> InstallPlan:
    spec = _snapshot_spec(spec)
    root = home.resolve()
    if _has_symlink_ancestor(home) or home.is_symlink() or not root.is_dir():
        raise InstallPlanError("home must be an existing non-symlink directory")
    if not selected: raise InstallPlanError("at least one client must be selected")
    if len(set(selected)) != len(selected): raise InstallPlanError("duplicate selected client")
    targets: list[InstallTarget] = []
    for client in selected:
        path = _target_path(root, client)
        if client in _CLI_TARGETS:
            targets.append(InstallTarget(
                client,
                path,
                "cli-add",
                "cli-managed",
                path.with_name(path.name + ".api-to-typemcp.bak"),
                "hermes-mcp-test" if client == "hermes" else "claude-mcp-list-connected",
            ))
            continue
        fingerprint = _fingerprint(path, root=root)
        if not path.is_file():
            raise InstallPlanError("native installation requires an existing detected configuration; use portable export instead")
        if _has_duplicate(path, client, spec.name):
            raise InstallPlanError("existing MCP server name requires a separate replace plan")
        targets.append(InstallTarget(client, path, "add", fingerprint, path.with_name(path.name + ".api-to-typemcp.bak"), "config-reread"))
    return InstallPlan(spec, tuple(targets))


def write_portable_export(project: Path, spec: McpServerSpec) -> Path:
    spec = _snapshot_spec(spec)
    root = project.resolve()
    if _has_symlink_ancestor(project) or project.is_symlink() or not root.is_dir(): raise InstallPlanError("portable export project must be a non-symlink directory")
    directory = root / "agent-install"
    if directory.exists() and (directory.is_symlink() or not directory.is_dir()):
        raise InstallPlanError("portable export directory must not be a symlink or file")
    directory.mkdir(exist_ok=True)
    output = directory / "mcpServers.json"
    if output.exists() and (output.is_symlink() or not output.is_file()):
        raise InstallPlanError("portable export target must be a regular file")
    payload = {"mcpServers": {spec.name: {"command": spec.command, "args": list(spec.args), "cwd": str(spec.cwd)}}}
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output
