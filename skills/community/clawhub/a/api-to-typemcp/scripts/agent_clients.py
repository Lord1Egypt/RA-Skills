"""Read-only discovery contract for local MCP agent clients."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
import re

_SAFE_NAME = re.compile(r"^[a-z][a-z0-9-]{0,62}$")


class AgentClientError(ValueError):
    pass


@dataclass(frozen=True)
class McpServerSpec:
    name: str
    command: str
    args: tuple[str, ...]
    cwd: Path
    env_names: tuple[str, ...] = ()

    def to_public_dict(self) -> dict[str, object]:
        return {"name": self.name, "command": self.command, "args": list(self.args), "cwd": str(self.cwd), "env_names": list(self.env_names)}


@dataclass(frozen=True)
class DetectedClient:
    id: str
    display_name: str
    config_candidates: tuple[Path, ...]
    evidence: tuple[str, ...]
    can_verify_runtime: bool

    def to_public_dict(self) -> dict[str, object]:
        return {"id": self.id, "display_name": self.display_name, "config_candidates": [str(p) for p in self.config_candidates], "evidence": list(self.evidence), "can_verify_runtime": self.can_verify_runtime}


def _contained_without_symlinks(path: Path, boundary: Path) -> bool:
    try:
        relative = path.relative_to(boundary)
    except ValueError:
        return False
    current = boundary
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            return False
    try:
        return path.resolve().is_relative_to(boundary)
    except OSError:
        return False


def _has_symlink_ancestor(path: Path) -> bool:
    """Check original absolute path components before any resolution erases links."""
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        if current.is_symlink():
            return True
    return False


def _project_root(project: Path) -> Path:
    if _has_symlink_ancestor(project) or project.is_symlink() or not project.is_dir():
        raise AgentClientError("generated project must be an existing non-symlink directory")
    return project.resolve()


def _env_names(project: Path) -> tuple[str, ...]:
    example = project / ".env.example"
    if not example.is_file() or example.is_symlink():
        return ()
    result: list[str] = []
    for raw in example.read_text(encoding="utf-8").splitlines():
        value = raw.strip().split("=", 1)[0]
        if re.fullmatch(r"[A-Z][A-Z0-9_]*", value):
            result.append(value)
    return tuple(dict.fromkeys(result))


def server_spec_from_project(project: Path, *, server_name: str) -> McpServerSpec:
    if not _SAFE_NAME.fullmatch(server_name):
        raise AgentClientError("server name must be lowercase kebab-case and start with a letter")
    root = _project_root(project)
    entry = root / "dist" / "index.js"
    if not entry.is_file() or not _contained_without_symlinks(entry, root):
        raise AgentClientError("generated project must contain built non-symlink dist/index.js")
    return McpServerSpec(server_name, "node", (str(entry.resolve()),), root, _env_names(root))


def _existing(paths: tuple[Path, ...], root: Path) -> tuple[Path, ...]:
    return tuple(p for p in paths if p.is_file() and _contained_without_symlinks(p, root))


def detect_clients(*, home: Path, project: Path, which: Callable[[str], str | None]) -> list[DetectedClient]:
    _project_root(project)  # establishes an explicit boundary; does not inspect .env
    if _has_symlink_ancestor(home) or home.is_symlink() or not home.is_dir():
        raise AgentClientError("home must be an existing non-symlink directory")
    root = home.resolve()
    locations = {
        "hermes": (root / ".hermes/config.yaml",), "claude-code": (root / ".claude.json", root / ".claude/settings.json"),
        "codex": (root / ".codex/config.toml",), "cursor": (root / ".cursor/mcp.json",),
        "vscode-copilot": (root / ".config/Code/User/mcp.json",), "gemini-cli": (root / ".gemini/settings.json",),
        "opencode": (root / ".config/opencode/opencode.json",),
    }
    definitions = (("hermes", "Hermes", "hermes", True), ("claude-code", "Claude Code", "claude", True), ("codex", "Codex", "codex", True), ("cursor", "Cursor", None, False), ("vscode-copilot", "VS Code / GitHub Copilot", "code", False), ("gemini-cli", "Gemini CLI", "gemini", False), ("opencode", "OpenCode", "opencode", True))
    found: list[DetectedClient] = []
    for ident, display, executable, runtime in definitions:
        paths = _existing(locations[ident], root)
        executable_path = which(executable) if executable else None
        evidence = tuple(([f"executable:{executable}"] if executable_path else []) + [f"config:{p}" for p in paths])
        if evidence:
            found.append(DetectedClient(ident, display, paths, evidence, bool(executable_path and runtime)))
    return found
