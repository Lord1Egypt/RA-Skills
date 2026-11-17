"""Shared paths, config helpers, privacy helpers."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATHS = [
    Path.home() / ".config" / "douyin-chat-insight" / "config.yaml",
    SKILL_ROOT / "config.yaml",
]


def skill_root() -> Path:
    return SKILL_ROOT


def default_output_dir() -> Path:
    return Path.cwd() / "output" / "douyin-chat-insight"


def redact_path(path: Optional[str]) -> str:
    """Public surfaces must not leak private absolute paths."""
    if not path:
        return ""
    raw = str(path).strip()
    p = Path(raw)
    # Prefer stable basename for known private roots (even if cwd is inside them)
    s = raw.replace("\\", "/")
    if re.search(r"(?:^|/)(?:Users|home|Volumes|private/var|tmp)/", s) or s.startswith("~"):
        # keep last 1-2 meaningful parts when useful: parent/name for uniqueness
        parts = [x for x in p.parts if x not in ("/", "\\")]
        if len(parts) >= 2 and parts[-1] in {"latest.html", "latest.md", "latest.json"}:
            return f"{parts[-2]}/{parts[-1]}"
        return p.name or "…"
    try:
        rel = p.expanduser().resolve().relative_to(Path.cwd().resolve())
        return str(rel)
    except Exception:
        pass
    if p.is_absolute():
        return p.name
    return raw


def load_config(path: Optional[Path] = None) -> Dict[str, Any]:
    cfg: Dict[str, Any] = {
        "default_locale": "zh",
        "output_dir": str(default_output_dir()),
        "owner_aliases": [],
        "report": {"formats": ["html", "md", "json"]},
        "filters": {
            "drop_system": True,
            "drop_join_leave": True,
            "min_demand_chars": 15,
        },
        "limits": {
            "inventory_top_senders": 12,
            "demand_wall": 24,
            "hard_fact_candidates": 12,
            "contradiction_pairs": 8,
        },
    }
    candidates: List[Path] = []
    if path:
        candidates.append(Path(path))
    candidates.extend(DEFAULT_CONFIG_PATHS)
    raw = None
    used = None
    for p in candidates:
        if p.is_file():
            raw = p.read_text(encoding="utf-8")
            used = p
            break
    if raw is None:
        cfg["_config_path"] = None
        return cfg
    if used.suffix.lower() == ".json":
        data = json.loads(raw)
    else:
        data = _parse_simple_yaml(raw)
    _deep_update(cfg, data)
    # normalize owner_aliases always list[str]
    aliases = cfg.get("owner_aliases") or []
    if isinstance(aliases, dict):
        # broken multi-line parse left {} — treat as empty
        aliases = list(aliases.values()) if aliases else []
    if isinstance(aliases, str):
        aliases = [aliases]
    cfg["owner_aliases"] = [str(a).strip() for a in aliases if str(a).strip()]
    cfg["_config_path"] = str(used)
    return cfg


def save_config(cfg: Dict[str, Any], path: Optional[Path] = None) -> Path:
    path = path or (Path.home() / ".config" / "douyin-chat-insight" / "config.yaml")
    path.parent.mkdir(parents=True, exist_ok=True)
    out = {k: v for k, v in cfg.items() if not str(k).startswith("_")}
    lines = ["# douyin-chat-insight local config (no secrets)", ""]
    lines.append(f"default_locale: {out.get('default_locale', 'zh')}")
    lines.append(f"output_dir: {out.get('output_dir', str(default_output_dir()))}")
    aliases = out.get("owner_aliases") or []
    if aliases:
        # inline list — reliable with simple parser; also accept multi-line on read
        safe = ", ".join(str(a).replace(",", " ") for a in aliases)
        lines.append(f"owner_aliases: [{safe}]")
    else:
        lines.append("owner_aliases: []")
    formats = (out.get("report") or {}).get("formats") or ["html", "md", "json"]
    lines.append("report:")
    lines.append(f"  formats: [{', '.join(formats)}]")
    filt = out.get("filters") or {}
    lines.append("filters:")
    lines.append(f"  drop_system: {str(bool(filt.get('drop_system', True))).lower()}")
    lines.append(f"  drop_join_leave: {str(bool(filt.get('drop_join_leave', True))).lower()}")
    lines.append(f"  min_demand_chars: {int(filt.get('min_demand_chars', 15))}")
    lim = out.get("limits") or {}
    lines.append("limits:")
    defaults = {
        "inventory_top_senders": 12,
        "demand_wall": 24,
        "hard_fact_candidates": 12,
        "contradiction_pairs": 8,
    }
    for k, d in defaults.items():
        lines.append(f"  {k}: {int(lim.get(k, d))}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _deep_update(base: dict, override: dict) -> None:
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_update(base[k], v)
        else:
            base[k] = v


def _parse_simple_yaml(text: str) -> dict:
    """Minimal YAML subset: mappings + inline lists + multi-line list items."""
    root: Dict[str, Any] = {}
    stack: List[tuple] = [(-1, root)]  # (indent, container)

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if line.startswith("- "):
            val = _coerce(line[2:].strip())
            # pop to a list container whose indent is strictly less than item indent
            while len(stack) > 1:
                top_i, top_c = stack[-1]
                if isinstance(top_c, list) and indent > top_i:
                    break
                if indent > top_i and isinstance(top_c, dict):
                    # maybe empty placeholder dict for list key
                    break
                stack.pop()
            parent = stack[-1][1]
            if isinstance(parent, list):
                parent.append(val)
                continue
            if isinstance(parent, dict) and len(parent) == 0 and len(stack) >= 2:
                key_indent = stack[-1][0]
                grand = stack[-2][1]
                if isinstance(grand, dict):
                    for k, v in list(grand.items()):
                        if v is parent:
                            lst: List[Any] = []
                            grand[k] = lst
                            # keep list at KEY indent so sibling items (indent > key) stay attached
                            stack[-1] = (key_indent, lst)
                            lst.append(val)
                            break
                continue
            continue

        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if not isinstance(parent, dict):
            continue
        if ":" not in line:
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest == "" or rest == "[]":
            if rest == "[]":
                parent[key] = []
            else:
                nxt: Any = {}
                parent[key] = nxt
                stack.append((indent, nxt))
        elif rest.startswith("[") and rest.endswith("]"):
            inner = rest[1:-1].strip()
            parent[key] = (
                [_coerce(x.strip()) for x in inner.split(",") if x.strip()] if inner else []
            )
        else:
            parent[key] = _coerce(rest)
    return root


def _coerce(s: str) -> Any:
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    low = s.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if low in ("null", "none", "~"):
        return None
    try:
        if s.isdigit() or (s.startswith("-") and s[1:].isdigit()):
            return int(s)
    except Exception:
        pass
    return s


def detect_sibling_skills() -> Dict[str, bool]:
    roots = [
        Path.home() / ".shared" / "skills",
        Path.home() / ".hermes" / "skills",
        Path.home() / ".codex" / "skills",
        Path.home() / ".Codex" / "skills",
        Path.home() / ".claude" / "skills",
    ]
    names = [
        "douyin-creator-insight",
        "douyin-favorites-to-knowledge",
        "douyin-knowledge-base-pipeline",
        "douyin-video-analyst",
        "douyin-workflow",
    ]
    out: Dict[str, bool] = {}
    for n in names:
        out[n] = any((r / n).exists() for r in roots)
    out["dashscope_key_present"] = bool(
        os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("BAILIAN_API_KEY")
    )
    return out
