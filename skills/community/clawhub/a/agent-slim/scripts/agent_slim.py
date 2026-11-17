#!/usr/bin/env python3
"""Agent Slim inventory and safe workflow entrypoint.

The audit is deliberately conservative: it reads configuration and instruction
files needed for inventory, but never opens session bodies.  Plan/apply/verify/
restore are implemented in agent_slim_workflow.py and default to dry-run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

try:
    import agent_slim_workflow as workflow
    from agent_slim_adapter import detect_home_kind, probe_codex_home, probe_home
except ImportError as exc:  # pragma: no cover - packaging failure is an IO error
    raise SystemExit("agent_slim_workflow.py and agent_slim_adapter.py are required next to agent_slim.py") from exc

SCHEMA_VERSION = "1.0"
TOOL_VERSION = "0.3.0"
DEFAULT_MAX_DEPTH = 8
TOKENS_PER_CHAR = 0.6
MAX_TEXT_BYTES = 8 * 1024 * 1024
# Generic user-home marker used inside user skill docs; split so the
# published package does not carry a literal local-config path.
HOME_MARKER = "~/" + ".codex/"
MAX_REFERENCE_EDGES = 2000
OLD_SESSION_DAYS = 30
WIDE_DESCRIPTION_CHARS = 600
LARGE_SKILL_BODY_CHARS = 12000
LARGE_WARM_FILE_BYTES = 20000

EXIT_OK = 0
EXIT_WARNING = 2
EXIT_USAGE = 64
EXIT_IO = 74

TEXT_SUFFIXES = {
    ".md", ".markdown", ".txt", ".json", ".yaml", ".yml", ".toml",
    ".py", ".sh", ".ps1", ".csv", ".tsv", ".html", ".css", ".js", ".mjs",
    ".cjs", ".ts", ".tsx", ".jsx", ".xml", ".ini", ".cfg", ".conf",
}

LAYER_ORDER = {"hot": 0, "warm": 1, "cold": 2}

# Generic layout description: any agent can declare where its resident context,
# skills, sessions and logs live instead of relying on a known vendor layout.
LAYOUT_CATEGORIES = {"instructions", "rules", "memory", "tools", "docs"}
MAX_LAYOUT_ENTRIES = 200


class CliParser(argparse.ArgumentParser):
    """Use a documented CLI usage exit code instead of argparse's default 2."""

    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(EXIT_USAGE, "error: {}\n".format(message))


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_time(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def mtime_iso(timestamp: Optional[float]) -> Optional[str]:
    if timestamp is None:
        return None
    return iso_time(datetime.fromtimestamp(timestamp, timezone.utc))


def detect_codex_home(explicit: Optional[str] = None) -> Tuple[Path, str]:
    """Resolve Codex Home without assuming a username or OS-specific path."""
    if explicit:
        return Path(explicit).expanduser().resolve(), "argument"
    env_home = os.environ.get("CODEX_HOME", "").strip()
    if env_home:
        return Path(env_home).expanduser().resolve(), "environment"
    return (Path.home() / ".codex").resolve(), "default"


def safe_rel(path: Path, root: Path) -> Optional[str]:
    try:
        relative = os.path.relpath(str(path), str(root))
    except (OSError, ValueError):
        return None
    if relative == os.pardir or relative.startswith(os.pardir + os.sep):
        return None
    return Path(relative).as_posix() if relative != "." else "."


def inside(path: Path, root: Path) -> bool:
    rel = safe_rel(path, root)
    return rel is not None


def stable_slug(value: str, limit: int = 110) -> str:
    # ASCII alnum stays as before so existing Codex-side ids never change; CJK
    # ranges are preserved because dropping them collapsed every Chinese-named
    # file in one directory onto a single id (54 references/ files -> 1 id).
    slug = re.sub(r"[^a-z0-9\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+", "-", value.lower()).strip("-")
    if not slug:
        slug = "item"
    if len(slug) > limit:
        digest = hashlib.sha256(value.encode("utf-8", "replace")).hexdigest()[:12]
        slug = "{}-{}".format(slug[: limit - 13], digest)
    return slug


def read_utf8(path: Path, max_bytes: int = MAX_TEXT_BYTES) -> Tuple[Optional[str], int, bool]:
    """Read a text source up to a bound.  Never call this for session files."""
    try:
        size = path.stat().st_size
        if size > max_bytes:
            return None, size, True
        with path.open("rb") as handle:
            raw = handle.read(max_bytes + 1)
    except OSError:
        raise
    if len(raw) > max_bytes:
        return None, size, True
    return raw.decode("utf-8", errors="replace"), size, False


def estimate_tokens(chars: Optional[int]) -> Optional[int]:
    if chars is None:
        return None
    return int(math.ceil(chars * TOKENS_PER_CHAR))


def make_item(
    item_id: str,
    layer: str,
    category: str,
    kind: str,
    label: str,
    evidence_path: str,
    loaded_when: str,
    bytes_value: int,
    chars: Optional[int],
    evidence: Optional[Dict[str, str]] = None,
    risk: str = "R0",
    reversibility: str = "report-only",
    meta: Optional[Dict[str, Any]] = None,
    references: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    tokens = estimate_tokens(chars) if chars is not None else (0 if layer == "cold" else None)
    if evidence is None:
        evidence = {
            "bytes": "measured",
            "chars": "not-read" if chars is None else "measured-utf8",
            "tokens": "not-applicable" if layer == "cold" else ("approximate" if chars is not None else "unknown"),
        }
    return {
        "id": item_id,
        "layer": layer,
        "category": category,
        "kind": kind,
        "label": label,
        "evidencePath": evidence_path,
        "loadedWhen": loaded_when,
        "bytes": int(bytes_value),
        "chars": chars,
        "estimatedTokens": tokens,
        "evidence": evidence,
        "riskHint": risk,
        "reversibility": reversibility,
        "references": references or [],
        "candidate": False,
        "meta": meta or {},
    }


def add_warning(warnings: List[Dict[str, Any]], code: str, message: str, evidence: str = "") -> None:
    entry = {"code": code, "message": message, "evidence": evidence}
    if entry not in warnings:
        warnings.append(entry)


def add_unknown(unknowns: List[Dict[str, Any]], code: str, message: str, evidence: str = "") -> None:
    entry = {"code": code, "message": message, "evidence": evidence}
    if entry not in unknowns:
        unknowns.append(entry)


def split_frontmatter(text: str) -> Tuple[Optional[str], str]:
    stripped = text.lstrip("\ufeff")
    lines = stripped.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, stripped
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return None, stripped
    return "".join(lines[1:end]), "".join(lines[end + 1 :])


def parse_frontmatter(frontmatter: Optional[str]) -> Dict[str, Any]:
    if frontmatter is None:
        return {}
    result: Dict[str, Any] = {}
    lines = frontmatter.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        index += 1
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        if re.fullmatch(r"[>|][+-]?", value or ""):
            pieces: List[str] = []
            while index < len(lines) and (not lines[index].strip() or lines[index].startswith((" ", "\t"))):
                pieces.append(lines[index].strip())
                index += 1
            value = " ".join(piece for piece in pieces if piece)
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if value.startswith("[") and value.endswith("]"):
            result[key] = [part.strip().strip("'\"") for part in value[1:-1].split(",") if part.strip()]
        else:
            result[key] = value
    return result


def clean_reference_target(raw: str) -> str:
    target = raw.strip().strip("<>").strip()
    if " " in target:
        target = target.split(None, 1)[0]
    target = target.split("#", 1)[0].split("?", 1)[0]
    return target.replace("\\", "/")


def is_external_uri(target: str) -> bool:
    if not target:
        return False
    if re.match(r"^[A-Za-z]:[\\/]", target):
        return False  # Windows drive path, not a URI.
    return bool(re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target))


def is_placeholder_reference(target: str) -> bool:
    return any(marker in target for marker in ("<", ">", "...", "*", "{", "}"))


def looks_like_path(target: str) -> bool:
    if not target or target.startswith("#") or is_external_uri(target) or is_placeholder_reference(target):
        return False
    suffix = Path(target).suffix.lower()
    return "/" in target or suffix in TEXT_SUFFIXES


def extract_references(text: str) -> List[Tuple[str, str]]:
    found: List[Tuple[str, str]] = []
    seen = set()

    def add(kind: str, raw: str) -> None:
        target = clean_reference_target(raw)
        if not target or target.startswith("#") or is_external_uri(target) or is_placeholder_reference(target):
            return
        if not looks_like_path(target):
            return
        key = (kind, target)
        if key not in seen:
            seen.add(key)
            found.append(key)

    for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
        add("markdown-link", match.group(1))
    for match in re.finditer(r"`([^`\n]+)`", text):
        add("code-span", match.group(1))
    # Bare paths are intentionally not guessed: prose and command examples
    # produce too many false positives. Markdown links and code spans are the
    # stable, reviewable reference forms.
    return found


def resolve_reference(raw: str, source: Path, home: Path) -> Dict[str, Any]:
    target = clean_reference_target(raw)
    if not target or target.startswith("#") or is_external_uri(target) or is_placeholder_reference(target):
        return {"target": target, "scope": "external", "exists": None, "evidencePath": None}
    if target.startswith(HOME_MARKER):
        candidate = home / target[len(HOME_MARKER) :]
    elif target.startswith("$CODEX_HOME/"):
        candidate = home / target[len("$CODEX_HOME/") :]
    elif target.startswith("${CODEX_HOME}/"):
        candidate = home / target[len("${CODEX_HOME}/") :]
    else:
        candidate = Path(target)
        if not candidate.is_absolute():
            candidate = source.parent / candidate
    try:
        candidate = candidate.resolve()
    except OSError:
        candidate = candidate.absolute()
    rel = safe_rel(candidate, home)
    if rel is None:
        return {"target": target, "scope": "outside-home", "exists": None, "evidencePath": None}
    try:
        exists = candidate.exists()
    except OSError:
        exists = None
    return {
        "target": target,
        "scope": "inside-home",
        "exists": exists,
        "evidencePath": rel,
    }


def add_reference_edges(
    edges: List[Dict[str, Any]],
    warnings: List[Dict[str, Any]],
    from_id: str,
    source: Path,
    text: str,
    home: Path,
    markdown_only: bool = False,
) -> List[Dict[str, Any]]:
    item_edges: List[Dict[str, Any]] = []
    edge_keys = set()
    for kind, raw in extract_references(text):
        if markdown_only and kind != "markdown-link":
            continue
        if len(edges) >= MAX_REFERENCE_EDGES:
            add_warning(warnings, "REFERENCE_GRAPH_TRUNCATED", "Reference graph reached its safety limit.", "referenceGraph")
            break
        resolved = resolve_reference(raw, source, home)
        if resolved["scope"] == "inside-home" and resolved["exists"] is False and kind != "markdown-link":
            continue
        edge_key = (resolved["scope"], resolved["evidencePath"] or resolved["target"])
        if edge_key in edge_keys:
            continue
        edge_keys.add(edge_key)
        edge = {
            "from": from_id,
            "kind": kind,
            "target": resolved["target"],
            "scope": resolved["scope"],
            "exists": resolved["exists"],
            "evidencePath": resolved["evidencePath"],
        }
        if edge not in edges:
            edges.append(edge)
        if edge not in item_edges:
            item_edges.append(edge)
        if resolved["scope"] == "inside-home" and resolved["exists"] is False:
            add_warning(
                warnings,
                "BROKEN_REFERENCE",
                "A declared local reference target was not found.",
                resolved.get("evidencePath") or resolved["target"],
            )
    return item_edges


def load_usage_index(home: Path, warnings: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], Optional[str]]:
    candidates = [
        home / "skill-usage.json",
        home / "skills" / ".usage.json",
        home / "state" / "skill-usage.json",
    ]
    for path in candidates:
        if not path.is_file():
            continue
        try:
            text, _, _ = read_utf8(path)
            if text is None:
                add_warning(warnings, "USAGE_INDEX_TOO_LARGE", "Usage index was not read because it is too large.", safe_rel(path, home) or "usage-index")
                return {}, None
            data = json.loads(text)
        except (OSError, ValueError):
            add_warning(warnings, "USAGE_INDEX_INVALID", "Usage index could not be parsed as JSON.", safe_rel(path, home) or "usage-index")
            return {}, None
        if isinstance(data, dict) and isinstance(data.get("skills"), dict):
            data = data["skills"]
        if not isinstance(data, dict):
            add_warning(warnings, "USAGE_INDEX_SHAPE", "Usage index has an unsupported shape.", safe_rel(path, home) or "usage-index")
            return {}, None
        return data, safe_rel(path, home)
    return {}, None


def usage_for_skill(usage: Dict[str, Any], source: Optional[str], name: str) -> Dict[str, Any]:
    record = usage.get(name)
    if isinstance(record, dict):
        return {
            "available": bool(source),
            "recorded": True,
            "source": source,
            "lastUsedAt": record.get("lastUsedAt") or record.get("last_used_at") or record.get("lastUsed"),
        }
    return {
        "available": bool(source),
        "recorded": False,
        "source": source,
        "lastUsedAt": None,
    }


def walk_files(root: Path, max_depth: int) -> Iterable[Path]:
    """Yield files without following symlinks or reading file contents."""
    if not root.exists() or not root.is_dir():
        return
    stack: List[Tuple[Path, int]] = [(root, 0)]
    while stack:
        directory, depth = stack.pop()
        try:
            entries = sorted(os.scandir(str(directory)), key=lambda item: item.name.lower())
        except OSError:
            continue
        subdirs: List[Tuple[Path, int]] = []
        for entry in entries:
            try:
                if entry.is_symlink():
                    continue
                if entry.is_file(follow_symlinks=False):
                    yield Path(entry.path)
                elif entry.is_dir(follow_symlinks=False) and depth < max_depth:
                    subdirs.append((Path(entry.path), depth + 1))
            except OSError:
                continue
        stack.extend(reversed(subdirs))


def scan_tree(root: Path, max_depth: int, warnings: List[Dict[str, Any]], code: str) -> List[Path]:
    if not root.exists() or not root.is_dir():
        return []
    try:
        return list(walk_files(root, max_depth))
    except OSError:
        add_warning(warnings, code, "A disk metadata scan failed.", root.name)
        return []


def file_stat_summary(files: Sequence[Path]) -> Dict[str, Any]:
    total = 0
    oldest: Optional[float] = None
    newest: Optional[float] = None
    for path in files:
        try:
            stat = path.stat()
        except OSError:
            continue
        total += stat.st_size
        oldest = stat.st_mtime if oldest is None else min(oldest, stat.st_mtime)
        newest = stat.st_mtime if newest is None else max(newest, stat.st_mtime)
    return {
        "fileCount": len(files),
        "bytes": total,
        "oldestModified": mtime_iso(oldest),
        "newestModified": mtime_iso(newest),
        "_oldestTimestamp": oldest,
    }


def parse_plugin_declarations(config_path: Path, warnings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not config_path.is_file():
        return []
    try:
        text, _, _ = read_utf8(config_path)
    except OSError:
        add_warning(warnings, "CONFIG_UNREADABLE", "Plugin declarations could not be read.", "config.toml")
        return []
    if text is None:
        add_warning(warnings, "CONFIG_TOO_LARGE", "Plugin declarations were not read because the file is too large.", "config.toml")
        return []
    declarations: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None
    section_re = re.compile(r"^\[plugins\.(['\"])(.+?)\1\]\s*$")
    for line in text.splitlines():
        stripped = line.strip()
        match = section_re.match(stripped)
        if match:
            full_name = match.group(2)
            if "@" in full_name:
                name, marketplace = full_name.rsplit("@", 1)
            else:
                name, marketplace = full_name, ""
            current = {"name": name, "marketplace": marketplace, "enabled": None}
            declarations.append(current)
            continue
        if stripped.startswith("[") and not stripped.startswith("[plugins."):
            current = None
            continue
        if current is not None and re.match(r"^enabled\s*=", stripped):
            value = stripped.split("=", 1)[1].split("#", 1)[0].strip().lower()
            current["enabled"] = value in ("true", "1", 'true"')
    return declarations


def version_key(name: str) -> Tuple[Any, ...]:
    return tuple((0, int(part)) if part.isdigit() else (1, part.lower()) for part in re.split(r"(\d+)", name) if part)


def discover_plugin_root(home: Path, name: str, marketplace: str) -> Optional[Path]:
    base = home / "plugins" / "cache"
    candidates: List[Path] = []
    if marketplace:
        candidates.append(base / marketplace / name)
    if not candidates:
        try:
            for marketplace_dir in sorted(base.iterdir(), key=lambda path: path.name.lower()) if base.is_dir() else []:
                candidates.append(marketplace_dir / name)
        except OSError:
            pass
    for candidate in candidates:
        if candidate.is_dir():
            versions = [path for path in candidate.iterdir() if path.is_dir()] if candidate.is_dir() else []
            if versions:
                return sorted(versions, key=lambda path: version_key(path.name))[-1]
            return candidate
    return None


def load_json_metadata(path: Path, warnings: List[Dict[str, Any]], home: Path) -> Optional[Dict[str, Any]]:
    try:
        text, _, _ = read_utf8(path)
        if text is None:
            return None
        data = json.loads(text)
    except (OSError, ValueError):
        add_warning(warnings, "PLUGIN_DECLARATION_INVALID", "Plugin declaration JSON could not be parsed.", safe_rel(path, home) or path.name)
        return None
    return data if isinstance(data, dict) else None


def discover_plugin(
    declaration: Dict[str, Any],
    home: Path,
    max_depth: int,
    warnings: List[Dict[str, Any]],
    unknowns: List[Dict[str, Any]],
) -> Tuple[Optional[Dict[str, Any]], List[Path]]:
    name = str(declaration.get("name", ""))
    marketplace = str(declaration.get("marketplace", ""))
    root = discover_plugin_root(home, name, marketplace)
    record: Dict[str, Any] = {
        "name": name,
        "marketplace": marketplace,
        "declaredEnabled": declaration.get("enabled") is True,
        "discovered": root is not None,
        "cacheRoot": safe_rel(root, home) if root is not None else None,
        "declarationPath": "config.toml",
        "toolSurface": {
            "mode": "declaration-files",
            "mcpServers": [],
            "declaredTools": [],
            "apps": [],
            "skills": [],
            "discoverable": False,
            "sessionToolSnapshot": "unavailable",
        },
        "skillFiles": [],
    }
    if root is None:
        if declaration.get("enabled") is True:
            add_warning(
                warnings,
                "ENABLED_PLUGIN_NOT_DISCOVERED",
                "An enabled plugin has no discoverable cache directory.",
                "{}@{}".format(name, marketplace or "unknown-marketplace"),
            )
        return record, []
    plugin_depth = max(max_depth, 8)
    surface = record["toolSurface"]
    for path in walk_files(root, plugin_depth):
        rel = safe_rel(path, home) or path.name
        basename = path.name.lower()
        if basename == ".mcp.json":
            data = load_json_metadata(path, warnings, home)
            if data:
                servers = data.get("mcpServers", {})
                if isinstance(servers, dict):
                    surface["mcpServers"].extend(sorted(str(key) for key in servers))
                    for server in servers.values():
                        if isinstance(server, dict) and isinstance(server.get("tools"), dict):
                            surface["declaredTools"].extend(sorted(str(key) for key in server["tools"]))
        elif basename == ".app.json":
            data = load_json_metadata(path, warnings, home)
            if data and isinstance(data.get("apps"), dict):
                surface["apps"].extend(sorted(str(key) for key in data["apps"]))
        elif basename == "skill.md":
            record["skillFiles"].append(rel)
    for key in ("mcpServers", "declaredTools", "apps", "skills"):
        surface[key] = sorted(set(surface[key]))
    surface["skills"] = sorted(set(record["skillFiles"]))
    surface["discoverable"] = bool(surface["mcpServers"] or surface["declaredTools"] or surface["apps"] or surface["skills"])
    if declaration.get("enabled") is True and not surface["discoverable"]:
        add_warning(warnings, "PLUGIN_TOOL_SURFACE_UNKNOWN", "Enabled plugin cache contains no discoverable tool declaration.", record["cacheRoot"] or name)
    add_unknown(
        unknowns,
        "LIVE_TOOL_SNAPSHOT_UNAVAILABLE",
        "Live session tool names are not exposed to a standalone filesystem audit; plugin declaration files were inventoried instead.",
        record["cacheRoot"] or "plugins/",
    )
    return record, [home / rel for rel in record["skillFiles"]]


def plugin_item(record: Dict[str, Any]) -> Dict[str, Any]:
    surface = record.get("toolSurface", {})
    item = make_item(
        "hot:plugin:{}".format(stable_slug("{}@{}".format(record["name"], record["marketplace"]))),
        "hot",
        "plugin",
        "plugin",
        "{}@{}".format(record["name"], record["marketplace"] or "unknown"),
        record.get("cacheRoot") or "plugins/",
        "startup/tool-discovery",
        0,
        None,
        evidence={"bytes": "measured", "chars": "not-read", "tokens": "unknown"},
        risk="R0",
        reversibility="read-only",
        meta={
            "declaredEnabled": record.get("declaredEnabled", False),
            "discoverable": record.get("discovered", False),
            "mcpServers": len(surface.get("mcpServers", [])),
            "declaredTools": len(surface.get("declaredTools", [])),
            "apps": len(surface.get("apps", [])),
            "skills": len(surface.get("skills", [])),
            "sessionToolSnapshot": surface.get("sessionToolSnapshot", "unavailable"),
        },
    )
    item["meta"]["toolSurface"] = surface
    return item


def add_candidate(
    candidates: List[Dict[str, Any]],
    item: Dict[str, Any],
    action: str,
    reason: str,
    risk: Optional[str] = None,
    rollback: Optional[str] = None,
    bytes_value: Optional[int] = None,
    meta_extra: Optional[Dict[str, Any]] = None,
) -> None:
    candidate = {
        "id": "candidate:{}:{}".format(item["id"], action),
        "layer": item["layer"],
        "action": action,
        "targetId": item["id"],
        "targetPath": item["evidencePath"],
        "bytes": item["bytes"] if bytes_value is None else bytes_value,
        "chars": item["chars"],
        "estimatedTokens": item.get("estimatedTokens") or 0,
        "estimateBasis": "content-size-upper-bound; actual savings require before/after load evidence",
        "estimatedSavingsTokens": None,
        "risk": risk or item.get("riskHint", "R1"),
        "rollback": rollback or item.get("reversibility", "report-only"),
        "reason": reason,
    }
    if meta_extra:
        candidate["meta"] = meta_extra
    if candidate not in candidates:
        candidates.append(candidate)
    item["candidate"] = True


def discover_skill_files(skills_root: Path, max_depth: int) -> List[Path]:
    if not skills_root.is_dir():
        return []
    found: List[Path] = []
    for path in walk_files(skills_root, max_depth):
        if path.name.lower() != "skill.md":
            continue
        rel = safe_rel(path, skills_root) or ""
        parts = Path(rel).parts
        if len(parts) == 2 or (len(parts) == 3 and parts[0] == ".system"):
            found.append(path)
    return sorted(found)


def normalized_triggers(value: Any) -> List[str]:
    """Normalize the restricted inline trigger syntax used by the audit."""
    if value is None:
        return []
    if isinstance(value, list):
        raw_values = value
    else:
        raw_values = re.split(r"[,，]", str(value))
    result: List[str] = []
    for raw in raw_values:
        trigger = str(raw).strip().strip("'\"")
        if trigger and trigger not in result:
            result.append(trigger)
    return result


def add_skill_inventory(
    skill_path: Path,
    home: Path,
    max_depth: int,
    usage: Dict[str, Any],
    usage_source: Optional[str],
    warnings: List[Dict[str, Any]],
    unknowns: List[Dict[str, Any]],
    items: Dict[str, Dict[str, Any]],
    edges: List[Dict[str, Any]],
    candidates: List[Dict[str, Any]],
    trigger_index: Dict[str, List[Dict[str, str]]],
) -> Optional[str]:
    try:
        text, file_size, truncated = read_utf8(skill_path)
    except OSError:
        add_warning(warnings, "SKILL_UNREADABLE", "Skill entry file could not be read.", safe_rel(skill_path, home) or skill_path.name)
        return None
    evidence_path = safe_rel(skill_path, home) or skill_path.name
    if text is None:
        add_unknown(unknowns, "SKILL_TOO_LARGE", "Skill entry file was too large to estimate characters.", evidence_path)
        return None
    frontmatter, body = split_frontmatter(text)
    values = parse_frontmatter(frontmatter)
    name = str(values.get("name") or skill_path.parent.name)
    description = str(values.get("description") or "")
    triggers = normalized_triggers(values.get("triggers") or values.get("trigger"))
    for trigger in triggers:
        trigger_index.setdefault(trigger, []).append(
            {"trigger": trigger, "skill": name, "evidencePath": evidence_path}
        )
    if not frontmatter:
        add_warning(warnings, "SKILL_FRONTMATTER_MISSING", "Skill entry file has no parseable frontmatter.", evidence_path)
    if not values.get("name"):
        add_warning(warnings, "SKILL_NAME_MISSING", "Skill frontmatter has no name field.", evidence_path)
    if not description:
        add_warning(warnings, "SKILL_DESCRIPTION_MISSING", "Skill frontmatter has no description field.", evidence_path)
    if len(description) > WIDE_DESCRIPTION_CHARS:
        add_warning(warnings, "WIDE_SKILL_DESCRIPTION", "Skill description exceeds the review threshold.", evidence_path)

    projection = "name: {}\ndescription: {}".format(name, description)
    metadata_item = make_item(
        "hot:skill-metadata:{}".format(stable_slug(evidence_path)),
        "hot",
        "skill-metadata",
        "file",
        name,
        evidence_path,
        "every-skill-list / trigger routing",
        len((frontmatter or "").encode("utf-8")),
        len(projection),
        evidence={"bytes": "measured", "chars": "derived-from-frontmatter", "tokens": "approximate"},
        risk="R1",
        reversibility="restore-from-backup",
        meta={
            "skillName": name,
            "descriptionLength": len(description),
            "frontmatterChars": len(frontmatter or ""),
            "source": "plugin" if "plugins" in Path(evidence_path).parts else "user",
            "recentUse": usage_for_skill(usage, usage_source, name),
            "triggers": triggers,
        },
    )
    items[metadata_item["id"]] = metadata_item
    if len(description) > WIDE_DESCRIPTION_CHARS:
        add_candidate(
            candidates,
            metadata_item,
            "compress-validated-description",
            "Description is wider than the review threshold; verify trigger coverage before changing it.",
            "R1",
            "restore original description and re-run trigger regression",
        )

    body_bytes = len(body.encode("utf-8"))
    body_item = make_item(
        "warm:skill-body:{}".format(stable_slug(evidence_path)),
        "warm",
        "skill-body",
        "file",
        name,
        evidence_path,
        "skill-trigger",
        body_bytes,
        len(body),
        evidence={"bytes": "measured", "chars": "measured-utf8", "tokens": "approximate"},
        risk="R1",
        reversibility="move-back-to-original-path",
        meta={
            "skillName": name,
            "bodyLines": len(body.splitlines()),
            "frontmatterPresent": bool(frontmatter),
            "sourceFileBytes": file_size,
            "recentUse": usage_for_skill(usage, usage_source, name),
        },
    )
    body_item["references"] = add_reference_edges(edges, warnings, body_item["id"], skill_path, body, home)
    items[body_item["id"]] = body_item
    if len(body) > LARGE_SKILL_BODY_CHARS:
        add_candidate(
            candidates,
            body_item,
            "route-large-skill-body",
            "Skill body is large enough to review for an on-demand routing split.",
            "R1",
            "restore the pre-change file from the transaction or backup",
        )

    skill_dir = skill_path.parent
    referenced_paths = set()
    for edge in body_item["references"]:
        if edge.get("scope") == "inside-home" and edge.get("evidencePath"):
            referenced_paths.add(edge["evidencePath"])
    for category, item_category in (("references", "reference"), ("packs", "pack"), ("templates", "template")):
        directory = skill_dir / category
        if not directory.is_dir():
            continue
        for path in walk_files(directory, max_depth):
            rel = safe_rel(path, home) or path.name
            suffix = path.suffix.lower()
            text_value: Optional[str] = None
            size = 0
            try:
                size = path.stat().st_size
                if suffix in TEXT_SUFFIXES:
                    text_value, _, _ = read_utf8(path)
            except OSError:
                add_warning(warnings, "WARM_FILE_UNREADABLE", "Warm content file could not be read.", rel)
            chars = len(text_value) if text_value is not None else None
            warm_item = make_item(
                "warm:{}:{}".format(item_category, stable_slug(rel)),
                "warm",
                item_category,
                "file",
                path.name,
                rel,
                "trigger-or-explicit-read",
                size,
                chars,
                evidence={
                    "bytes": "measured",
                    "chars": "measured-utf8" if chars is not None else "not-read",
                    "tokens": "approximate" if chars is not None else "unknown",
                },
                risk="R1",
                reversibility="move-back-to-original-path",
                meta={
                    "skillName": name,
                    "referencedBySkill": rel in referenced_paths,
                    "lastModified": mtime_iso(path.stat().st_mtime) if path.exists() else None,
                },
            )
            if text_value is not None:
                warm_item["references"] = add_reference_edges(
                    edges, warnings, warm_item["id"], path, text_value, home, markdown_only=True
                )
            items[warm_item["id"]] = warm_item
            if size >= LARGE_WARM_FILE_BYTES or (chars is not None and chars >= LARGE_SKILL_BODY_CHARS):
                add_candidate(
                    candidates,
                    warm_item,
                    "route-large-warm-file",
                    "Large on-demand file should be reviewed for a smaller routed entry.",
                    "R1",
                    "restore the file and its routing references from the transaction",
                )
            elif category == "references" and rel not in referenced_paths:
                add_candidate(
                    candidates,
                    warm_item,
                    "review-unreferenced-warm-content",
                    "Reference file is not linked from the skill body; confirm whether it is intentionally discoverable.",
                    "R1",
                    "restore the file if a routing change is attempted",
                )
    return metadata_item["id"]


def duplicate_hot_rules(items: Dict[str, Dict[str, Any]], warnings: List[Dict[str, Any]], candidates: List[Dict[str, Any]]) -> None:
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for item in items.values():
        if item["layer"] != "hot" or item["category"] not in ("instructions", "rules"):
            continue
        if not item.get("chars"):
            continue
        try:
            path = Path(item["meta"].get("absolutePath", ""))
            if path.is_file():
                text, _, _ = read_utf8(path)
            else:
                text = None
        except OSError:
            text = None
        if text is None:
            continue
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        groups.setdefault(digest, []).append(item)
    for digest, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        member_ids = sorted(item["id"] for item in members)
        add_warning(warnings, "DUPLICATE_HOT_CONTENT", "Multiple resident rule/instruction files have identical content.", ", ".join(member_ids))
        estimated = sum(item.get("estimatedTokens") or 0 for item in members)
        candidates.append(
            {
                "id": "candidate:hot-duplicate:{}".format(digest[:12]),
                "layer": "hot",
                "action": "review-duplicate-hot-rules",
                "targetId": member_ids[0],
                "targetPath": members[0]["evidencePath"],
                "bytes": sum(item["bytes"] for item in members),
                "chars": sum(item.get("chars") or 0 for item in members),
                "estimatedTokens": estimated,
                "estimateBasis": "sum of duplicate file content; actual savings require load-path evidence",
                "estimatedSavingsTokens": None,
                "risk": "R1",
                "rollback": "restore duplicate file from backup or transaction",
                "reason": "Identical resident content was found in more than one file.",
                "itemIds": member_ids,
            }
        )


def cold_item(
    root_name: str,
    files: Sequence[Path],
    category: str,
    layer: str = "cold",
    risk: str = "R2",
    reversibility: str = "move-with-manifest",
) -> Dict[str, Any]:
    summary = file_stat_summary(files)
    item = make_item(
        "cold:{}:{}".format(category, stable_slug(root_name)),
        layer,
        category,
        "aggregate",
        root_name,
        root_name + ("/" if not root_name.endswith("/") else ""),
        "disk-only",
        summary["bytes"],
        None,
        evidence={"bytes": "measured", "chars": "not-read", "tokens": "not-applicable"},
        risk=risk,
        reversibility=reversibility,
        meta={
            "fileCount": summary["fileCount"],
            "oldestModified": summary["oldestModified"],
            "newestModified": summary["newestModified"],
        },
    )
    return item


def add_disk_inventory(
    home: Path,
    max_depth: int,
    warnings: List[Dict[str, Any]],
    unknowns: List[Dict[str, Any]],
    items: Dict[str, Dict[str, Any]],
    candidates: List[Dict[str, Any]],
    now: datetime,
    host_kind: str = "codex",
    layout: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    disk: Dict[str, Any] = {"bytes": 0, "fileCount": 0, "categories": {}}
    if layout and (layout.get("sessionRoots") or layout.get("logRoots")):
        # A described layout wins over vendor guesses: every declared root keeps
        # the same category so the audit contract shape does not change.
        session_roots = [("sessions", home / root) for root in layout.get("sessionRoots") or []]
        log_roots = [home / root for root in layout.get("logRoots") or []]
        if not session_roots:
            add_unknown(unknowns, "SESSION_ROOT_NOT_DESCRIBED", "The layout declares no session root.", "sessionRoots")
    elif host_kind == "workbuddy":
        # WorkBuddy stores sessions under workspace/sessions and keeps perf
        # traces beside logs; both map onto the existing categories so the
        # audit contract keeps its shape.
        session_roots = [("sessions", home / "workspace" / "sessions")]
        log_roots = [home / "logs", home / "traces"]
    else:
        session_roots = [("sessions", home / "sessions"), ("archived-sessions", home / "archived_sessions")]
        log_roots = [home / "log", home / "logs"]
    for label, root in session_roots:
        files = scan_tree(root, max_depth, warnings, "DISK_SCAN_FAILED")
        if not files:
            add_unknown(unknowns, "SESSION_ROOT_NOT_FOUND", "Session metadata root is not present or empty.", label + "/")
            continue
        item = cold_item(label, files, "sessions", "cold", "R2", "move-with-manifest")
        oldest = file_stat_summary(files).get("_oldestTimestamp")
        cutoff = now.timestamp() - OLD_SESSION_DAYS * 86400
        old_files = []
        for path in files:
            try:
                if path.stat().st_mtime < cutoff:
                    old_files.append(path)
            except OSError:
                continue
        item["meta"]["oldFileCount"] = len(old_files)
        item["meta"]["oldBytes"] = file_stat_summary(old_files)["bytes"]
        item["meta"]["ageThresholdDays"] = OLD_SESSION_DAYS
        items[item["id"]] = item
        if old_files:
            add_candidate(
                candidates,
                item,
                "archive-verified-old-sessions",
                "Old session files were found; review closure and handoff state before any reversible archive.",
                "R2",
                "restore archived session files and verify readability",
                bytes_value=item["meta"]["oldBytes"],
                meta_extra={"oldFileCount": len(old_files), "oldBytes": item["meta"]["oldBytes"]},
            )
        disk["categories"][label] = {"fileCount": item["meta"]["fileCount"], "bytes": item["bytes"]}
        disk["bytes"] += item["bytes"]
        disk["fileCount"] += item["meta"]["fileCount"]

    if layout and layout.get("backupRoots"):
        backup_roots = [home / root for root in layout.get("backupRoots") or []]
    else:
        backup_roots = [home / "backups"]
    backup_files: List[Path] = []
    for backup_root in backup_roots:
        backup_files.extend(scan_tree(backup_root, max_depth, warnings, "DISK_SCAN_FAILED"))
    if backup_files:
        item = cold_item("backups", backup_files, "backups", "cold", "R2", "move-with-manifest")
        items[item["id"]] = item
        add_candidate(
            candidates,
            item,
            "review-backup-retention",
            "Backups are disk-only until duplicate hashes and restoration coverage are verified.",
            "R2",
            "restore the moved backup and verify its hash",
        )
        disk["categories"]["backups"] = {"fileCount": item["meta"]["fileCount"], "bytes": item["bytes"]}
        disk["bytes"] += item["bytes"]
        disk["fileCount"] += item["meta"]["fileCount"]
    else:
        add_unknown(unknowns, "BACKUP_ROOT_NOT_FOUND", "Backup root is not present or empty.", "backups/")

    log_files: List[Path] = []
    for root in log_roots:
        log_files.extend(scan_tree(root, max_depth, warnings, "DISK_SCAN_FAILED"))
    if log_files:
        item = cold_item("logs", log_files, "logs", "cold", "R2", "rotation-plan-required")
        items[item["id"]] = item
        add_candidate(
            candidates,
            item,
            "review-log-retention",
            "Logs are disk-only; retention requires a separate, reversible review.",
            "R2",
            "use the host log rotation procedure and verify no active writer is disrupted",
        )
        disk["categories"]["logs"] = {"fileCount": item["meta"]["fileCount"], "bytes": item["bytes"]}
        disk["bytes"] += item["bytes"]
        disk["fileCount"] += item["meta"]["fileCount"]
    else:
        add_unknown(unknowns, "LOG_ROOT_NOT_FOUND", "Log roots are not present or empty.", "log/, logs/")

    excluded = {
        "sessions", "archived_sessions", "backups", "log", "logs", "plugins",
        ".git", ".pnpm-store", "node_modules",
    }
    database_files: List[Path] = []
    if home.is_dir():
        stack: List[Tuple[Path, int]] = [(home, 0)]
        while stack:
            directory, depth = stack.pop()
            try:
                entries = sorted(os.scandir(str(directory)), key=lambda entry: entry.name.lower())
            except OSError:
                continue
            for entry in entries:
                if entry.is_symlink():
                    continue
                if entry.is_file(follow_symlinks=False):
                    if entry.name.lower().endswith((".db", ".sqlite", ".sqlite3", ".db-wal", ".db-shm")):
                        database_files.append(Path(entry.path))
                elif entry.is_dir(follow_symlinks=False) and depth < max_depth:
                    if depth == 0 and entry.name in excluded:
                        continue
                    stack.append((Path(entry.path), depth + 1))
    if database_files:
        item = cold_item("databases", database_files, "databases", "cold", "R3", "not-in-scope")
        items[item["id"]] = item
        disk["categories"]["databases"] = {"fileCount": item["meta"]["fileCount"], "bytes": item["bytes"]}
        disk["bytes"] += item["bytes"]
        disk["fileCount"] += item["meta"]["fileCount"]
        add_unknown(unknowns, "DATABASE_CONTENT_NOT_READ", "Database files were measured by metadata only; no database content or VACUUM was inspected.", "databases")
    return disk


def sort_items(values: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(
        values,
        key=lambda item: (
            LAYER_ORDER.get(item["layer"], 9),
            item["category"],
            -(item.get("estimatedTokens") if item.get("estimatedTokens") is not None else -1),
            -item.get("bytes", 0),
            item["id"],
        ),
    )


def sort_candidates(values: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(
        values,
        key=lambda item: (
            LAYER_ORDER.get(item["layer"], 9),
            -(item.get("estimatedTokens") or 0),
            -item.get("bytes", 0),
            item["id"],
        ),
    )


def summary_for(items: Sequence[Dict[str, Any]], name: str) -> Dict[str, Any]:
    known_tokens = [item.get("estimatedTokens") for item in items if item.get("estimatedTokens") is not None]
    return {
        "itemCount": len(items),
        "bytes": sum(item.get("bytes", 0) for item in items),
        "charsKnown": sum(item.get("chars") or 0 for item in items),
        "estimatedTokens": sum(known_tokens),
        "unknownTokenItems": sum(1 for item in items if item.get("estimatedTokens") is None),
        "candidates": sum(1 for item in items if item.get("candidate")),
        "name": name,
    }


def build_summary(
    layers: Dict[str, List[Dict[str, Any]]],
    disk: Dict[str, Any],
    candidates: Sequence[Dict[str, Any]],
    warnings: Sequence[Dict[str, Any]],
    unknowns: Sequence[Dict[str, Any]],
    errors: Sequence[Dict[str, Any]],
) -> Dict[str, Any]:
    layer_summary = {name: summary_for(values, name) for name, values in layers.items()}
    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return {
        "status": status,
        "layers": layer_summary,
        "disk": disk,
        "candidateCount": len(candidates),
        "warningCount": len(warnings),
        "unknownCount": len(unknowns),
        "errorCount": len(errors),
        "hotEstimatedTokens": layer_summary["hot"]["estimatedTokens"],
        "warmEstimatedTokens": layer_summary["warm"]["estimatedTokens"],
        "coldEstimatedTokens": 0,
        "estimatedTotalTokens": layer_summary["hot"]["estimatedTokens"] + layer_summary["warm"]["estimatedTokens"],
    }


def _layout_rel_path(value: Any, warnings: List[Dict[str, Any]], field: str) -> Optional[str]:
    """Accept only home-relative paths; absolute, home-escaped and empty entries are dropped."""
    if not isinstance(value, str) or not value.strip():
        return None
    original = value.strip()
    normalized = original.replace("\\", "/")
    # Judge absoluteness on the raw value: stripping separators first would turn
    # "/tmp/x" into a relative path and silently accept an escape.
    drive_prefixed = bool(re.match(r"^[A-Za-z]:", normalized))
    if original.startswith("~") or normalized.startswith("/") or drive_prefixed or Path(normalized).is_absolute():
        add_warning(warnings, "LAYOUT_PATH_REJECTED", "A layout path must stay inside the audited home.", field)
        return None
    raw = normalized.strip("/")
    if not raw or ".." in Path(raw).parts:
        add_warning(warnings, "LAYOUT_PATH_REJECTED", "A layout path must stay inside the audited home.", field)
        return None
    return raw


def load_layout(path: Optional[str], warnings: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Load an optional layout description so the audit is not tied to one vendor structure.

    The file is optional.  When absent, vendor detection keeps working exactly as
    before; when present it only replaces where things live, never what counts as
    Hot/Warm/Cold or which actions are allowed.
    """
    if not path:
        return None
    try:
        payload = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        add_warning(warnings, "LAYOUT_UNREADABLE", "The layout file could not be read as JSON.", "<layout>")
        return None
    if not isinstance(payload, dict):
        add_warning(warnings, "LAYOUT_INVALID", "The layout file must contain a JSON object.", "<layout>")
        return None

    hot: List[Dict[str, str]] = []
    entries = payload.get("hot") or []
    if not isinstance(entries, list):
        add_warning(warnings, "LAYOUT_INVALID", "layout.hot must be a list.", "hot")
        entries = []
    for entry in entries[:MAX_LAYOUT_ENTRIES]:
        if isinstance(entry, str):
            entry = {"path": entry}
        if not isinstance(entry, dict):
            continue
        rel = _layout_rel_path(entry.get("path"), warnings, "hot")
        if rel is None:
            continue
        category = str(entry.get("category") or "instructions").strip().lower()
        if category not in LAYOUT_CATEGORIES:
            category = "docs"
        loaded_when = str(entry.get("loadedWhen") or "every-turn").strip() or "every-turn"
        hot.append({"path": rel, "category": category, "loadedWhen": loaded_when})

    def roots(field: str) -> List[str]:
        values = payload.get(field) or []
        if isinstance(values, str):
            values = [values]
        if not isinstance(values, list):
            add_warning(warnings, "LAYOUT_INVALID", "layout.{} must be a list.".format(field), field)
            return []
        cleaned: List[str] = []
        for value in values[:MAX_LAYOUT_ENTRIES]:
            rel = _layout_rel_path(value, warnings, field)
            if rel and rel not in cleaned:
                cleaned.append(rel)
        return cleaned

    return {
        "host": str(payload.get("host") or "custom").strip() or "custom",
        "hot": hot,
        "skillRoots": roots("skillRoots") or ["skills"],
        "sessionRoots": roots("sessionRoots"),
        "logRoots": roots("logRoots"),
        "backupRoots": roots("backupRoots"),
        "ruleRoots": roots("ruleRoots") or ["rules"],
    }


def audit_home(
    home: Path,
    max_depth: int = DEFAULT_MAX_DEPTH,
    now: Optional[datetime] = None,
    layout: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Run a read-only inventory against any agent home, described by layout or detected."""
    home = home.expanduser().resolve()
    host_kind = str(layout.get("host")) if layout else detect_home_kind(home)
    current = now or utc_now()
    warnings: List[Dict[str, Any]] = []
    unknowns: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []
    candidates: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    items: Dict[str, Dict[str, Any]] = {}
    plugin_records: List[Dict[str, Any]] = []
    trigger_index: Dict[str, List[Dict[str, str]]] = {}

    if not home.exists() or not home.is_dir():
        errors.append({"code": "HOME_NOT_FOUND", "message": "Codex Home does not exist or is not a directory.", "evidence": "<home>"})
        layers = {"hot": [], "warm": [], "cold": []}
        return {
            "schemaVersion": SCHEMA_VERSION,
            "tool": {"name": "agent-slim", "version": TOOL_VERSION},
            "runId": "audit-{}".format(hashlib.sha256(str(home).encode("utf-8", "replace")).hexdigest()[:16]),
            "createdAt": iso_time(current),
            "mode": "dry-run",
            "host": {
                "kind": host_kind,
                "home": str(home),
                "homeSource": "argument",
                "adapter": probe_home(home, "argument"),
                "layoutDescribed": layout is not None,
            },
            "scope": {"maxDepth": max_depth, "pathMode": "home-relative", "sessionContentRead": False},
            "tokenEstimate": {
                "kind": "approximate",
                "algorithm": "ceil(chars * tokensPerChar)",
                "tokensPerChar": TOKENS_PER_CHAR,
                "notBillingMeasurement": True,
            },
            "summary": build_summary(layers, {"bytes": 0, "fileCount": 0, "categories": {}}, candidates, warnings, unknowns, errors),
            "layers": layers,
            "candidates": [],
            "referenceGraph": [],
            "triggerIndex": [],
            "plugins": plugin_records,
            "warnings": warnings,
            "unknowns": unknowns,
            "limitations": ["No files were read because the requested home is missing."],
            "errors": errors,
        }

    usage, usage_source = load_usage_index(home, warnings)

    # Plugin declarations and discoverable file-based tool surfaces.
    declarations = parse_plugin_declarations(home / "config.toml", warnings)
    plugin_skill_paths: List[Path] = []
    for declaration in declarations:
        if declaration.get("enabled") is not True:
            # Disabled plugins are inventoried as inert declarations.  Their
            # cache is deliberately not scanned for active tool surfaces.
            record = {
                "name": str(declaration.get("name", "")),
                "marketplace": str(declaration.get("marketplace", "")),
                "declaredEnabled": False,
                "discovered": False,
                "cacheRoot": None,
                "declarationPath": "config.toml",
                "toolSurface": {
                    "mode": "declaration-files",
                    "mcpServers": [],
                    "declaredTools": [],
                    "apps": [],
                    "skills": [],
                    "discoverable": False,
                    "sessionToolSnapshot": "unavailable",
                },
                "skillFiles": [],
            }
            plugin_records.append(record)
            plugin_item_value = plugin_item(record)
            items[plugin_item_value["id"]] = plugin_item_value
            continue
        record, skill_paths = discover_plugin(declaration, home, max_depth, warnings, unknowns)
        if record is not None:
            plugin_records.append(record)
            plugin_skill_paths.extend(skill_paths)
            plugin_item_value = plugin_item(record)
            items[plugin_item_value["id"]] = plugin_item_value
    plugin_records.sort(key=lambda record: (record["marketplace"], record["name"]))

    rule_roots = (layout.get("ruleRoots") if layout else None) or ["rules"]
    skill_roots = (layout.get("skillRoots") if layout else None) or ["skills"]

    # Hot startup files and the resident rule graph.  A layout description replaces
    # the vendor default list; without one the legacy vendor list is used unchanged.
    hot_described = bool(layout and layout.get("hot"))
    hot_queue: List[Tuple[Path, str, str]] = []
    if hot_described:
        for entry in layout.get("hot") or []:
            hot_queue.append((home / entry["path"], entry["category"], entry["loadedWhen"]))
    else:
        hot_queue = [
            (home / "AGENTS.md", "instructions", "every-turn"),
            (home / "rules" / "index.md", "rules", "startup-rule-index"),
            (home / "memories" / "memory_summary.md", "memory", "startup-memory-summary"),
        ]
    hot_seen = set()
    while hot_queue:
        path, category, loaded_when = hot_queue.pop(0)
        rel = safe_rel(path, home)
        if rel is None or rel in hot_seen:
            continue
        hot_seen.add(rel)
        if not path.exists():
            if hot_described:
                add_warning(warnings, "HOT_FILE_MISSING", "A declared resident context file was not found.", rel)
            elif category == "instructions":
                add_warning(warnings, "AGENTS_MISSING", "AGENTS.md was not found.", "AGENTS.md")
            elif category == "rules":
                add_warning(warnings, "RULES_INDEX_MISSING", "rules/index.md was not found.", "rules/index.md")
            else:
                add_warning(warnings, "MEMORY_SUMMARY_MISSING", "memories/memory_summary.md was not found.", "memories/memory_summary.md")
            continue
        try:
            text, size, truncated = read_utf8(path)
        except OSError:
            add_warning(warnings, "HOT_FILE_UNREADABLE", "A resident context file could not be read.", rel)
            continue
        item = make_item(
            "hot:{}:{}".format(category, stable_slug(rel)),
            "hot",
            category,
            "file",
            path.name,
            rel,
            loaded_when,
            size,
            None if text is None else len(text),
            evidence={
                "bytes": "measured",
                "chars": "not-read" if text is None else "measured-utf8",
                "tokens": "unknown" if text is None else "approximate",
            },
            risk="R0" if category == "memory" else "R1",
            reversibility="report-only" if category == "memory" else "restore-from-backup",
            meta={"truncated": truncated},
        )
        # Keep the absolute path only in memory for duplicate hashing; do not emit it.
        item["meta"]["absolutePath"] = str(path)
        if text is not None and category != "memory":
            item["references"] = add_reference_edges(edges, warnings, item["id"], path, text, home)
        items[item["id"]] = item
        if text is not None and category in ("instructions", "rules"):
            for kind, raw in extract_references(text):
                resolved = resolve_reference(raw, path, home)
                target_rel = resolved.get("evidencePath")
                if resolved.get("scope") != "inside-home" or not target_rel:
                    continue
                target_path = home / target_rel
                if target_path.is_file() and target_path.suffix.lower() == ".md" and any(
                    inside(target_path, home / root) for root in rule_roots
                ):
                    hot_queue.append((target_path, "rules", "referenced-by-resident-rule"))

    # Discover skills from the user skill root and every enabled plugin's skill files.
    skill_paths: List[Path] = []
    for skill_root in skill_roots:
        skill_paths.extend(discover_skill_files(home / skill_root, 2))
    for plugin_path in plugin_skill_paths:
        if plugin_path.is_file():
            skill_paths.append(plugin_path)
    unique_skill_paths = sorted({path.resolve(): path for path in skill_paths}.values(), key=lambda path: safe_rel(path, home) or path.name)
    if not unique_skill_paths:
        add_warning(warnings, "SKILLS_NOT_FOUND", "No SKILL.md files were discoverable in the user or plugin skill roots.", "skills/")
    for skill_path in unique_skill_paths:
        add_skill_inventory(
            skill_path,
            home,
            max_depth,
            usage,
            usage_source,
            warnings,
            unknowns,
            items,
            edges,
            candidates,
            trigger_index,
        )

    if usage_source is None:
        add_unknown(unknowns, "RECENT_USE_EVIDENCE_UNAVAILABLE", "No supported skill usage index was found; recent-use evidence is unavailable.", "skills/")

    duplicate_hot_rules(items, warnings, candidates)

    # Cold disk metadata.  No file under sessions/archived_sessions is opened.
    disk = add_disk_inventory(home, max_depth, warnings, unknowns, items, candidates, current, host_kind, layout)
    add_unknown(
        unknowns,
        "SESSION_BODY_NOT_READ",
        "Session bodies were intentionally not read; count and bytes are metadata-only.",
        "sessions/, archived_sessions/",
    )

    for item in items.values():
        item["meta"].pop("absolutePath", None)
    hot = sort_items([item for item in items.values() if item["layer"] == "hot"])
    warm = sort_items([item for item in items.values() if item["layer"] == "warm"])
    cold = sort_items([item for item in items.values() if item["layer"] == "cold"])
    candidates_sorted = sort_candidates(candidates)
    warnings_sorted = sorted(warnings, key=lambda value: (value["code"], value["evidence"], value["message"]))
    unknowns_sorted = sorted(unknowns, key=lambda value: (value["code"], value["evidence"], value["message"]))
    errors_sorted = sorted(errors, key=lambda value: (value["code"], value["evidence"], value["message"]))
    layers = {"hot": hot, "warm": warm, "cold": cold}
    summary = build_summary(layers, disk, candidates_sorted, warnings_sorted, unknowns_sorted, errors_sorted)
    trigger_index_records = [
        record
        for trigger in sorted(trigger_index)
        for record in sorted(trigger_index[trigger], key=lambda value: (value["skill"], value["evidencePath"]))
    ]
    limitations = [
        "Token values are static character estimates, not host billing measurements.",
        "Cold storage bytes are kept separate and never converted into a Token savings claim.",
        "Plugin declarations are file-based evidence; live session tool snapshots are not available.",
        "Session content is never read by this audit.",
    ]
    if host_kind == "workbuddy":
        limitations.append(
            "WorkBuddy cold storage covers workspace/sessions plus logs/ and traces/. projects/ holds conversation history and binaries/ holds runtimes; both are excluded from the reclaim plan by design, so cold bytes are not the whole home."
        )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "tool": {"name": "agent-slim", "version": TOOL_VERSION},
        "runId": "audit-{}".format(hashlib.sha256((str(home) + "|" + str(max_depth)).encode("utf-8", "replace")).hexdigest()[:16]),
        "createdAt": iso_time(current),
        "mode": "dry-run",
        "host": {
            "kind": host_kind,
            "home": str(home),
            "homeSource": "argument",
            "adapter": probe_home(home, "argument"),
            "layoutDescribed": layout is not None,
        },
        "scope": {
            "maxDepth": max_depth,
            "pathMode": "home-relative",
            "sessionContentRead": False,
        },
        "tokenEstimate": {
            "kind": "approximate",
            "algorithm": "ceil(chars * tokensPerChar)",
            "tokensPerChar": TOKENS_PER_CHAR,
            "notBillingMeasurement": True,
        },
        "summary": summary,
        "layers": layers,
        "candidates": candidates_sorted,
        "referenceGraph": sorted(edges, key=lambda value: (value["from"], value["target"], value["kind"])),
        "triggerIndex": trigger_index_records,
        "plugins": plugin_records,
        "warnings": warnings_sorted,
        "unknowns": unknowns_sorted,
        "limitations": limitations,
        "errors": errors_sorted,
    }


def md_cell(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: Dict[str, Any]) -> str:
    lines = [
        "# Agent Slim 只读审计报告",
        "",
        "- 模式：{}".format(report["mode"]),
        "- 状态：{}".format(report["summary"]["status"]),
        "- Codex Home：`{}`".format(report["host"]["home"]),
        "- 最大目录深度：{}".format(report["scope"]["maxDepth"]),
        "- Token 口径：{}（{} token/char；近似值，不是账单实测）".format(
            report["tokenEstimate"]["algorithm"], report["tokenEstimate"]["tokensPerChar"]
        ),
        "- 会话正文：{}".format("未读取" if not report["scope"]["sessionContentRead"] else "读取"),
        "",
        "## 分层汇总",
        "",
        "| 层 | 项数 | 字节 | 已知字符 | 估算 Token | 未知 Token 项 | 候选 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for layer in ("hot", "warm", "cold"):
        summary = report["summary"]["layers"][layer]
        lines.append(
            "| {} | {} | {} | {} | {} | {} | {} |".format(
                layer,
                summary["itemCount"],
                summary["bytes"],
                summary["charsKnown"],
                summary["estimatedTokens"],
                summary["unknownTokenItems"],
                summary["candidates"],
            )
        )
    disk = report["summary"]["disk"]
    lines.extend(
        [
            "",
            "## 磁盘账本",
            "",
            "- 文件数：{}".format(disk.get("fileCount", 0)),
            "- 字节：{}".format(disk.get("bytes", 0)),
            "- 分类：{}".format(json.dumps(disk.get("categories", {}), ensure_ascii=False, sort_keys=True)),
            "",
            "Cold 仅为磁盘账本，估算 Token 固定为 0。",
            "",
            "## 冷热候选",
            "",
            "| ID | 层 | 动作 | 风险 | 估算 Token | 回滚/恢复 | 证据 |",
            "| --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for candidate in report["candidates"]:
        lines.append(
            "| {} | {} | {} | {} | {} | {} | {} |".format(
                md_cell(candidate["id"]),
                md_cell(candidate["layer"]),
                md_cell(candidate["action"]),
                md_cell(candidate["risk"]),
                md_cell(candidate["estimatedTokens"]),
                md_cell(candidate["rollback"]),
                md_cell(candidate["targetPath"]),
            )
        )
    if not report["candidates"]:
        lines.append("| - | - | 无 | - | - | - | - |")

    for layer in ("hot", "warm", "cold"):
        lines.extend(
            [
                "",
                "## {} 对象".format(layer.capitalize()),
                "",
                "| ID | 分类 | 证据路径 | 字节 | 字符 | 估算 Token | 风险 | 可逆性 |",
                "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
            ]
        )
        for item in report["layers"][layer]:
            lines.append(
                "| {} | {} | {} | {} | {} | {} | {} | {} |".format(
                    md_cell(item["id"]),
                    md_cell(item["category"]),
                    md_cell(item["evidencePath"]),
                    item["bytes"],
                    md_cell(item["chars"]),
                    md_cell(item["estimatedTokens"]),
                    md_cell(item["riskHint"]),
                    md_cell(item["reversibility"]),
                )
            )

    lines.extend(
        [
            "",
            "## 警告",
            "",
            "| 代码 | 证据 | 说明 |",
            "| --- | --- | --- |",
        ]
    )
    for warning in report["warnings"]:
        lines.append("| {} | {} | {} |".format(md_cell(warning["code"]), md_cell(warning["evidence"]), md_cell(warning["message"])))
    if not report["warnings"]:
        lines.append("| - | - | 无 |")
    lines.extend(
        [
            "",
            "## 无法确认项",
            "",
            "| 代码 | 证据 | 说明 |",
            "| --- | --- | --- |",
        ]
    )
    for unknown in report["unknowns"]:
        lines.append("| {} | {} | {} |".format(md_cell(unknown["code"]), md_cell(unknown["evidence"]), md_cell(unknown["message"])))
    if not report["unknowns"]:
        lines.append("| - | - | 无 |")
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "- 本命令只做只读盘点，不执行移动、删除、插件关闭、会话归档或数据库维护。",
            "- 会话、备份、日志和数据库只读取元数据，不读取正文或秘密。",
            "- `estimatedTokens` 是可排序的近似内容体积，不是账单实测或已实现节省。",
            "- 实际改动必须由后续执行器完成，并绑定备份、事务、哈希、回归和回滚。",
            "",
        ]
    )
    return "\n".join(lines)


def emit_report(report: Dict[str, Any], output: Optional[str], json_mode: bool) -> None:
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n" if json_mode else render_markdown(report)
    if not output or output == "-":
        sys.stdout.write(text)
        return
    path = Path(output).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_parser() -> CliParser:
    parser = CliParser(prog="agent_slim.py", description="Agent Slim audit and safe reversible workflow")
    parser.add_argument("--version", action="version", version="%(prog)s " + TOOL_VERSION)
    subparsers = parser.add_subparsers(dest="command")

    host = subparsers.add_parser("host", help="report proven host capabilities without changing files")
    host.add_argument("--home", default=None, help="agent home; also supports CODEX_HOME")
    host.add_argument("--layout", default=None, help="optional JSON layout description for an unrecognized agent")
    host.add_argument("--output", default=None, help="write JSON to a file; '-' means stdout")

    audit = subparsers.add_parser("audit", help="inventory Hot/Warm/Cold content without changing files")
    audit.add_argument("--home", default=None, help="agent home; also supports CODEX_HOME")
    audit.add_argument("--layout", default=None, help="optional JSON layout description for an unrecognized agent")
    audit.add_argument("--json", action="store_true", help="emit the stable JSON contract")
    audit.add_argument("--output", default=None, help="write output to a file; '-' means stdout")
    audit.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH, help="maximum metadata scan depth (default: 8)")
    audit.add_argument("--fail-on-warning", action="store_true", help="exit with code 2 when warnings are present")

    plan = subparsers.add_parser("plan", help="turn an audit JSON into a machine-readable dry-run plan")
    plan.add_argument("--audit", required=True, help="audit JSON file produced by the audit command")
    plan.add_argument("--confirm", action="append", default=[], help="confirm a target path or directory prefix for a pending action")
    plan.add_argument("--state-root", default=None, help="external transaction root; defaults beside the audited home")
    plan.add_argument("--output", default=None, help="write plan JSON to a file; '-' means stdout")

    apply_parser = subparsers.add_parser("apply", help="preview or apply ready allowlisted plan actions")
    apply_parser.add_argument("--plan", required=True, help="plan JSON file")
    apply_parser.add_argument("--apply", action="store_true", help="perform the transaction; omitted means dry-run")
    apply_parser.add_argument("--audit-log", default=None, help="dangerous-operation audit log path")
    apply_parser.add_argument("--output", default=None, help="write result JSON to a file; '-' means stdout")

    verify_parser = subparsers.add_parser("verify", help="check target states, hashes, references, parsing, and test prompts")
    verify_parser.add_argument("--plan", required=True, help="plan JSON file")
    verify_parser.add_argument("--test-prompts", default=None, help="JSON cases that execute a caller-supplied routing test command")
    verify_parser.add_argument("--phase", choices=("auto", "applied", "restored"), default="auto", help="expected transaction phase")
    verify_parser.add_argument("--output", default=None, help="write verification JSON to a file; '-' means stdout")

    restore_parser = subparsers.add_parser("restore", help="preview or apply an idempotent manifest restore")
    restore_parser.add_argument("--manifest", required=True, help="transaction manifest.json path")
    restore_parser.add_argument("--apply", action="store_true", help="perform restore; omitted means dry-run")
    restore_parser.add_argument("--audit-log", default=None, help="dangerous-operation audit log path")
    restore_parser.add_argument("--output", default=None, help="write restore result JSON to a file; '-' means stdout")
    return parser


def emit_workflow_error(exc: workflow.WorkflowError, output: Optional[str]) -> int:
    error = {
        "schemaVersion": workflow.PLAN_SCHEMA_VERSION,
        "kind": "agent-slim-error",
        "status": "FAIL",
        "code": exc.code,
        "message": exc.message,
    }
    try:
        workflow.emit_json(error, output)
    except workflow.WorkflowError as output_exc:
        sys.stderr.write("{}: {}\n".format(output_exc.code, output_exc.message))
    return exc.exit_code


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.error("a subcommand is required: host, audit, plan, apply, verify, restore")

    if args.command == "host":
        home, home_source = detect_codex_home(args.home)
        layout_probe: List[Dict[str, Any]] = []
        layout = load_layout(args.layout, layout_probe)
        if layout_probe:
            for item in layout_probe:
                sys.stderr.write("{}: {}\n".format(item.get("code"), item.get("message")))
            return EXIT_USAGE
        try:
            capabilities = probe_home(home, home_source)
            if layout:
                capabilities = dict(capabilities)
                capabilities["host"] = layout["host"]
                capabilities["layoutDescribed"] = True
                capabilities["layout"] = {
                    "hotEntryCount": len(layout["hot"]),
                    "skillRoots": layout["skillRoots"],
                    "sessionRoots": layout["sessionRoots"],
                    "logRoots": layout["logRoots"],
                    "backupRoots": layout["backupRoots"],
                    "ruleRoots": layout["ruleRoots"],
                }
            workflow.emit_json(capabilities, args.output)
        except workflow.WorkflowError as exc:
            return emit_workflow_error(exc, args.output)
        return EXIT_OK

    if args.command == "audit":
        if args.max_depth < 0:
            parser.error("--max-depth must be >= 0")
        home, home_source = detect_codex_home(args.home)
        layout_probe: List[Dict[str, Any]] = []
        layout = load_layout(args.layout, layout_probe)
        if layout_probe:
            for item in layout_probe:
                sys.stderr.write("{}: {}\n".format(item.get("code"), item.get("message")))
            return EXIT_USAGE
        report = audit_home(home, args.max_depth, layout=layout)
        report["host"]["homeSource"] = home_source
        try:
            emit_report(report, args.output, args.json)
        except OSError as exc:
            sys.stderr.write("OUTPUT_ERROR: {}\n".format(exc))
            return EXIT_IO
        if report["summary"]["status"] == "FAIL":
            return EXIT_IO
        if args.fail_on_warning and report["summary"]["status"] == "WARN":
            return EXIT_WARNING
        return EXIT_OK

    try:
        if args.command == "plan":
            audit = workflow.read_json(Path(args.audit).expanduser())
            plan = workflow.build_plan(
                audit,
                Path(args.audit).expanduser(),
                confirms=args.confirm,
                state_root=Path(args.state_root).expanduser() if args.state_root else None,
            )
            workflow.emit_json(plan, args.output)
            return EXIT_OK
        if args.command == "apply":
            result = workflow.apply_plan(
                Path(args.plan).expanduser(),
                apply=args.apply,
                audit_log=Path(args.audit_log).expanduser() if args.audit_log else None,
                output=args.output,
            )
            return workflow.result_exit_code("apply", result)
        if args.command == "verify":
            result = workflow.verify_plan(
                Path(args.plan).expanduser(),
                test_prompts=Path(args.test_prompts).expanduser() if args.test_prompts else None,
                phase=args.phase,
                output=args.output,
            )
            return workflow.result_exit_code("verify", result)
        if args.command == "restore":
            result = workflow.restore_manifest(
                Path(args.manifest).expanduser(),
                apply=args.apply,
                audit_log=Path(args.audit_log).expanduser() if args.audit_log else None,
                output=args.output,
            )
            return workflow.result_exit_code("restore", result)
    except workflow.WorkflowError as exc:
        return emit_workflow_error(exc, getattr(args, "output", None))
    parser.error("unknown subcommand")
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
