from __future__ import annotations

import fnmatch
import glob
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

TEXT_EXTENSIONS = {
    ".md", ".mdx", ".txt", ".yaml", ".yml", ".json", ".toml",
    ".py", ".ts", ".tsx", ".js", ".jsx", ".sh", ".bash", ".zsh",
    ".ps1", ".psm1", ".psd1", ".env", ".ini", ".cfg", ".conf", ".xml",
    ".html", ".css", ".csv",
}
TEXT_NAMES = {
    "AGENTS.md", "agents.md", "CLAUDE.md", "GEMINI.md", "SKILL.md", "skill.md",
    "skills.md", "SOUL.md", "soul.md", "PLANNER.md", "planner.md", "system.md",
    "developer.md", ".cursorrules", ".clawhubignore", ".gitignore", "README", "README.md",
}
DEFAULT_INCLUDES = [
    "**/*.md", "**/*.mdx", "**/*.txt", "**/*.yaml", "**/*.yml", "**/*.json",
    "**/*.toml", "**/*.py", "**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx",
    "**/*.sh", "**/*.bash", "**/*.zsh", "**/*.ps1", "**/*.ini", "**/*.cfg",
    "**/*.conf", "AGENTS.md", "agents.md", "CLAUDE.md", "GEMINI.md", "SOUL.md",
    "soul.md", "SKILL.md", "skill.md", "skills.md", ".cursorrules", ".clawhubignore",
]
DEFAULT_EXCLUDES = [
    ".git/**", "node_modules/**", ".venv/**", "venv/**", "env/**", "dist/**",
    "build/**", "target/**", "coverage/**", "__pycache__/**", ".pytest_cache/**",
    ".mypy_cache/**", ".ruff_cache/**", "*.lock", "package-lock.json", "pnpm-lock.yaml",
    "yarn.lock", "Cargo.lock", ".agentic-audit/**", ".hermes-audit-backups/**",
]
SENSITIVE_PATH_PATTERNS = [
    ".env", ".env.*", "*.pem", "*.key", "id_rsa", "id_rsa.*",
    "id_ed25519", "id_ed25519.*", "credentials.*", "secrets.*",
    "wallet.*", "*.pfx", "*.p12",
]
SAFE_SENSITIVE_TEMPLATE_MARKERS = (".example", ".sample", ".template")
SHALLOW_PATTERNS = [
    "AGENTS.md", "agents.md", "CLAUDE.md", "GEMINI.md", "SOUL.md", "soul.md",
    "planner.md", "PLANNER.md", "system.md", "developer.md", "README.md", "config.yaml",
    "config.yml", "settings.json", ".cursorrules", ".cursor/rules/**", "skills/*/SKILL.md",
    "prompts/**", "agents/**", "planner/**", "workflows/**", "docs/agent*", "docs/prompt*",
]
OPERATOR_EDITED_PATTERNS = [
    "AGENTS.md", "agents.md", "CLAUDE.md", "GEMINI.md", "SOUL.md", "soul.md",
    "planner.md", "PLANNER.md", "system.md", "developer.md", "prompts/**", "agents/**",
    "planner/**", "workflows/**", "skills/**/SKILL.md", "plugins/**", "config.yaml",
    "config.yml", "settings.json", ".cursorrules", ".cursor/rules/**",
]
PROFILE_PATTERNS = {
    "hermes": ["SOUL.md", "config.yaml", "config.yml", "skills/**/SKILL.md", "plugins/**", "memory/**"],
    "codex": ["AGENTS.md", ".codex/**", "skills/**/SKILL.md", "agents/openai.yaml"],
    "openclaw": ["SKILL.md", ".clawhubignore", "agents/**", "scripts/**", "references/**"],
    "langgraph": ["**/*graph*.py", "**/*node*.py", "**/*state*.py", "prompts/**", "evals/**"],
    "crewai": ["agents/**", "tasks/**", "crew*.yaml", "crew*.yml", "tools/**"],
    "autogen": ["**/*autogen*", "agents/**", "groupchat/**", "tools/**", "prompts/**"],
}
PROFILE_HOME_DEFAULTS = {"hermes": ["~/.hermes"], "codex": ["~/.codex"], "openclaw": ["~/.openclaw"]}
ROLE_ALIASES = {
    "all": [],
    "skill": ["skill"], "skills": ["skill"],
    "prompt": ["prompt_template"], "prompts": ["prompt_template"],
    "config": ["config"], "configs": ["config"],
    "memory": ["memory"],
    "planner": ["planner"], "planning": ["planner"],
    "workflow": ["workflow"], "workflows": ["workflow"],
    "instruction": ["identity_or_system", "project_instructions", "planner", "workflow"],
    "instructions": ["identity_or_system", "project_instructions", "planner", "workflow"],
    "docs": ["documentation"], "documentation": ["documentation"],
    "tooling": ["executable_or_tooling"], "executable": ["executable_or_tooling"],
}


@dataclass
class FileRecord:
    path: str
    root: str
    rel_path: str
    size_bytes: int
    line_count: int
    sha256: str
    extension: str
    role: str
    influence: str
    prompt_bearing: bool
    truncated: bool
    text: str
    warning: str = ""

    def inventory_row(self) -> dict[str, object]:
        return {
            "path": self.path, "root": self.root, "rel_path": self.rel_path,
            "size_bytes": self.size_bytes, "line_count": self.line_count, "sha256": self.sha256,
            "extension": self.extension, "role": self.role, "influence": self.influence,
            "prompt_bearing": self.prompt_bearing, "truncated": self.truncated, "warning": self.warning,
        }


def split_patterns(values: Iterable[str] | str | None) -> list[str]:
    if values is None:
        return []
    if isinstance(values, str):
        values = [values]
    patterns: list[str] = []
    for value in values:
        for part in str(value).split(","):
            cleaned = part.strip().strip('"').strip("'")
            if cleaned:
                patterns.append(cleaned.replace("\\", "/"))
    return patterns


def normalize_roles(values: Iterable[str] | str | None) -> set[str]:
    roles: set[str] = set()
    for value in split_patterns(values):
        key = value.lower().strip()
        expanded = ROLE_ALIASES.get(key, [key])
        if not expanded:
            return set()
        roles.update(expanded)
    return roles


def expand_root(value: str | Path) -> Path:
    return Path(str(value)).expanduser().resolve()


def posix_rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _match(rel_path: str, name: str, pattern: str) -> bool:
    pattern = pattern.strip().replace("\\", "/")
    if not pattern:
        return False
    rel = rel_path.replace("\\", "/")
    parts = set(rel.split("/"))
    if pattern in parts or pattern == name:
        return True
    if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(name, pattern):
        return True
    if pattern.endswith("/**"):
        prefix = pattern[:-3].strip("/")
        return rel == prefix or rel.startswith(prefix + "/") or prefix in parts
    return "/" not in pattern and pattern in parts


def matches_any(rel_path: str, name: str, patterns: Iterable[str]) -> bool:
    return any(_match(rel_path, name, pattern) for pattern in patterns)


def is_sensitive_path(rel_path: str, name: str) -> bool:
    lower_name = name.lower()
    if any(marker in lower_name for marker in SAFE_SENSITIVE_TEMPLATE_MARKERS):
        return False
    return matches_any(rel_path.lower(), lower_name, SENSITIVE_PATH_PATTERNS)


def looks_text_path(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name in TEXT_NAMES


def classify_role(rel_path: str, name: str) -> str:
    rel = rel_path.lower().replace("\\", "/")
    lower_name = name.lower()
    if lower_name in {"soul.md", "system.md", "developer.md", "claude.md", "gemini.md"}:
        return "identity_or_system"
    if lower_name == "agents.md" or rel.endswith("/agents.md"):
        return "project_instructions"
    if lower_name == "planner.md" or rel.startswith("planner/") or "/planner/" in rel:
        return "planner"
    if lower_name in {"skill.md", "skills.md"}:
        return "skill"
    if rel.startswith("prompts/") or "/prompts/" in rel or "prompt" in lower_name:
        return "prompt_template"
    if rel.startswith("workflows/") or "/workflows/" in rel or "workflow" in lower_name:
        return "workflow"
    if "memory" in rel:
        return "memory"
    if lower_name.endswith((".py", ".ts", ".tsx", ".js", ".jsx", ".sh", ".ps1")):
        return "executable_or_tooling"
    if lower_name.startswith("config") or lower_name.endswith((".yaml", ".yml", ".toml", ".json")):
        return "config"
    if rel.startswith("docs/") or "/docs/" in rel or lower_name.startswith("readme"):
        return "documentation"
    return "unknown_text"


def classify_influence(role: str, rel_path: str, name: str) -> str:
    rel = rel_path.lower().replace("\\", "/")
    lower_name = name.lower()
    if role == "identity_or_system":
        return "always_loaded_or_global"
    if role == "project_instructions" or lower_name in {"agents.md", "claude.md", "gemini.md"}:
        return "project_discovered"
    if role == "skill":
        return "conditionally_loaded"
    if role == "config":
        return "runtime_config"
    if role == "memory":
        return "memory_or_persistent_context"
    if role == "executable_or_tooling":
        return "executable_or_generated_context"
    if "/prompts/" in rel or role == "prompt_template":
        return "user_invoked_or_template"
    return "unknown_influence"


def is_prompt_bearing(role: str, rel_path: str, name: str) -> bool:
    rel = rel_path.lower().replace("\\", "/")
    return role in {"identity_or_system", "project_instructions", "planner", "skill", "prompt_template", "workflow", "memory", "config", "documentation"} or "prompt" in rel or name.lower() in {"skill.md", "agents.md"}


def read_text_record(path: Path, root: Path, max_file_bytes: int) -> FileRecord | None:
    try:
        stat = path.stat()
    except OSError:
        return None
    sha = hashlib.sha256()
    chunks: list[bytes] = []
    remaining = max_file_bytes
    line_count = 0
    saw_nul = False
    last_byte = b""
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(65536), b""):
                sha.update(block)
                line_count += block.count(b"\n")
                saw_nul = saw_nul or b"\x00" in block
                last_byte = block[-1:]
                if remaining > 0:
                    chunks.append(block[:remaining])
                    remaining -= min(remaining, len(block))
    except OSError:
        return None
    if saw_nul:
        return None
    raw = b"".join(chunks)
    text = ""
    warning = ""
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            text = raw.decode(encoding)
            if encoding not in {"utf-8-sig", "utf-8"}:
                warning = f"decoded_with_{encoding}"
            break
        except UnicodeDecodeError:
            continue
    if text == "" and raw:
        text = raw.decode("utf-8", errors="replace")
        warning = "decoded_with_replacement"
    line_count += int(bool(stat.st_size) and last_byte != b"\n")
    rel = posix_rel(path, root)
    role = classify_role(rel, path.name)
    influence = classify_influence(role, rel, path.name)
    return FileRecord(str(path.resolve()), str(root.resolve()), rel, stat.st_size, line_count, sha.hexdigest(), path.suffix.lower(), role, influence, is_prompt_bearing(role, rel, path.name), stat.st_size > max_file_bytes, text, warning)


def concrete_paths(patterns: Iterable[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in split_patterns(patterns):
        expanded = str(Path(pattern).expanduser())
        if any(ch in expanded for ch in "*?["):
            paths.extend(Path(item).resolve() for item in glob.glob(expanded, recursive=True))
        else:
            paths.append(Path(expanded).resolve())
    return [path for path in paths if path.exists() and path.is_file()]


def candidate_paths(root: Path, mode: str, profile: str, includes: list[str], operator_edited_only: bool, operator_edited_patterns: list[str]) -> list[Path]:
    if root.is_file():
        return [root]
    if operator_edited_only:
        patterns = operator_edited_patterns or OPERATOR_EDITED_PATTERNS
    elif mode == "shallow":
        patterns = SHALLOW_PATTERNS + PROFILE_PATTERNS.get(profile, [])
    else:
        patterns = []
    if patterns:
        found: dict[str, Path] = {}
        for pattern in patterns:
            if pattern.startswith("~") or Path(pattern).is_absolute():
                for path in concrete_paths([pattern]):
                    found[str(path.resolve())] = path
                continue
            for path in root.glob(pattern):
                if path.is_file():
                    found[str(path.resolve())] = path
        return sorted(found.values(), key=lambda p: p.as_posix().lower())
    try:
        return [path for path in root.rglob("*") if path.is_file()]
    except OSError:
        return []


def collect_files(
    roots: Iterable[str | Path], mode: str = "standard", includes: Iterable[str] | None = None,
    excludes: Iterable[str] | None = None, no_default_excludes: bool = False,
    operator_edited_only: bool = False, operator_edited_patterns: Iterable[str] | None = None,
    only_roles: Iterable[str] | str | None = None, prompt_bearing_only: bool = False,
    profile: str = "generic", max_file_bytes: int = 512_000,
    include_sensitive_files: bool = False,
) -> tuple[list[FileRecord], list[str]]:
    explicit_include_patterns = split_patterns(includes)
    include_patterns = explicit_include_patterns or DEFAULT_INCLUDES
    exclude_patterns = split_patterns(excludes)
    if not no_default_excludes:
        exclude_patterns = DEFAULT_EXCLUDES + exclude_patterns
    operator_patterns = split_patterns(operator_edited_patterns)
    role_filter = normalize_roles(only_roles)
    records: list[FileRecord] = []
    warnings: list[str] = []
    seen: set[str] = set()

    for root_value in roots:
        root = expand_root(root_value)
        if not root.exists():
            warnings.append(f"root_not_found: {root}")
            continue
        for path in candidate_paths(root, mode, profile, include_patterns, operator_edited_only, operator_patterns):
            resolved = str(path.resolve())
            if resolved in seen:
                continue
            rel, name = posix_rel(path, root), path.name
            if matches_any(rel, name, exclude_patterns):
                continue
            if not include_sensitive_files and is_sensitive_path(rel, name):
                warnings.append(f"sensitive_file_skipped: {rel}")
                continue
            if operator_edited_only and not (matches_any(rel, name, operator_patterns or OPERATOR_EDITED_PATTERNS) or path in concrete_paths(operator_patterns)):
                continue
            if mode != "shallow" and not matches_any(rel, name, include_patterns) and not looks_text_path(path):
                continue
            if not looks_text_path(path) and not matches_any(rel, name, include_patterns):
                continue
            record = read_text_record(path, root, max_file_bytes=max_file_bytes)
            if record is None:
                continue
            if mode == "standard" and not operator_edited_only and not record.prompt_bearing and not root.is_file():
                parts = set(record.rel_path.lower().split("/"))
                recognized_tool_path = record.role == "executable_or_tooling" and bool(
                    parts & {"agents", "hooks", "plugins", "scripts", "tools"}
                )
                explicitly_selected = bool(role_filter) or matches_any(
                    rel, name, explicit_include_patterns
                )
                profile_selected = matches_any(rel, name, PROFILE_PATTERNS.get(profile, []))
                if not (recognized_tool_path or explicitly_selected or profile_selected):
                    continue
            if role_filter and record.role not in role_filter:
                continue
            if prompt_bearing_only and not record.prompt_bearing:
                continue
            seen.add(resolved)
            records.append(record)

    if operator_edited_only:
        for path in concrete_paths(operator_patterns):
            resolved = str(path.resolve())
            if resolved in seen:
                continue
            root = path.parent.resolve()
            rel, name = posix_rel(path, root), path.name
            if matches_any(rel, name, exclude_patterns):
                continue
            if not include_sensitive_files and is_sensitive_path(rel, name):
                warnings.append(f"sensitive_file_skipped: {rel}")
                continue
            record = read_text_record(path, root, max_file_bytes=max_file_bytes)
            if record is None:
                continue
            if role_filter and record.role not in role_filter:
                continue
            if prompt_bearing_only and not record.prompt_bearing:
                continue
            seen.add(resolved)
            records.append(record)

    records.sort(key=lambda item: item.path.lower())
    return records, warnings


def detect_profile(roots: Iterable[str | Path]) -> str:
    markers = {
        "hermes": ["SOUL.md", ".hermes", "hermes.yaml", "hermes.yml"],
        "codex": [".codex", "AGENTS.md"],
        "openclaw": [".clawhub", "openclaw.plugin.json", ".clawhubignore"],
        "langgraph": ["langgraph.json"],
        "crewai": ["crew.py", "crew.yaml", "crew.yml"],
        "autogen": ["autogen"],
    }
    root_paths = [expand_root(root) for root in roots]
    for profile, names in markers.items():
        for root in root_paths:
            for name in names:
                if (root / name).exists():
                    return profile
    return "generic"