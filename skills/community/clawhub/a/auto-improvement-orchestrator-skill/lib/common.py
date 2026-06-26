#!/usr/bin/env python3
"""Pure utility functions for the auto-improvement pipeline.

Extracted from the original lane_common.py — contains ONLY stateless helpers
(no state-machine logic).  State-machine helpers live in lib.state_machine.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "1.0"
KEEP_CATEGORIES = {"docs", "reference", "guardrail"}
EXECUTOR_SUPPORTED_CATEGORIES = KEEP_CATEGORIES | {"prompt"}  # superset: includes SKILL.md edits
_DEFAULT_PROTECTED_KEYWORDS = (
    "trading",
    "gateway",
    "openclaw-company-orchestration-proposal",
)

def _load_protected_keywords() -> tuple[str, ...]:
    """Load protected keywords from config file, falling back to defaults."""
    config_path = Path.home() / ".openclaw" / "protected_keywords.json"
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return tuple(str(k).lower() for k in data)
        except (json.JSONDecodeError, OSError):
            pass
    return _DEFAULT_PROTECTED_KEYWORDS

PROTECTED_KEYWORDS = _load_protected_keywords()

# ---------------------------------------------------------------------------
# Timestamp helpers
# ---------------------------------------------------------------------------


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def compact_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def slugify(value: str) -> str:
    cleaned = []
    for ch in value.lower():
        if ch.isalnum():
            cleaned.append(ch)
        elif cleaned and cleaned[-1] != "-":
            cleaned.append("-")
    return "".join(cleaned).strip("-") or "item"


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Source / target helpers
# ---------------------------------------------------------------------------


def infer_source_kind(path: Path) -> str:
    lowered = str(path).lower()
    if ".feedback" in lowered or "feedback" in path.name.lower():
        return "feedback"
    if "learning" in lowered:
        return "learnings"
    if "memory" in lowered:
        return "memory"
    return "source"


def load_source_paths(target: Path, explicit_sources: Iterable[str] | None = None) -> list[Path]:
    sources: list[Path] = []
    for raw in explicit_sources or []:
        if not raw:
            continue
        source = Path(raw).expanduser()
        if source.exists():
            sources.append(source.resolve())
    candidates = [target / "memory", target / "learnings", target / ".feedback"]
    for candidate in candidates:
        if candidate.exists():
            sources.append(candidate.resolve())
    seen: set[str] = set()
    deduped: list[Path] = []
    for source in sources:
        key = str(source)
        if key not in seen:
            deduped.append(source)
            seen.add(key)
    return deduped


def expand_source(source: Path) -> list[dict[str, Any]]:
    if source.is_file():
        return [load_source_entry(source)]
    entries: list[dict[str, Any]] = []
    for child in sorted(source.rglob("*")):
        if not child.is_file():
            continue
        if child.suffix.lower() not in {".md", ".txt", ".json", ".log"}:
            continue
        entries.append(load_source_entry(child))
    return entries


def load_source_entry(path: Path) -> dict[str, Any]:
    raw = read_text(path)
    snippet = " ".join(raw.split())[:400]
    return {
        "path": str(path),
        "kind": infer_source_kind(path),
        "characters": len(raw),
        "snippet": snippet,
    }


def normalize_target(target: str) -> Path:
    return Path(target).expanduser().resolve()


def choose_doc_file(target: Path) -> Path | None:
    if target.is_file():
        return target
    preferred = [target / "README.md", target / "SKILL.md"]
    preferred.extend(sorted((target / "references").glob("*.md")) if (target / "references").exists() else [])
    for candidate in preferred:
        if candidate.exists() and candidate.is_file():
            return candidate.resolve()
    markdown_files = sorted(target.glob("*.md"))
    return markdown_files[0].resolve() if markdown_files else None


def choose_reference_file(target: Path) -> Path | None:
    if target.is_file():
        return target if "reference" in target.name.lower() else None
    references_dir = target / "references"
    if not references_dir.exists():
        return None
    candidates = sorted(references_dir.glob("*.md"))
    return candidates[0].resolve() if candidates else None


def choose_guardrail_file(target: Path) -> Path | None:
    if target.is_file():
        name = target.name.lower()
        return target if "guardrail" in name or "safety" in name else None
    references_dir = target / "references"
    if not references_dir.exists():
        return None
    for candidate in sorted(references_dir.glob("*.md")):
        name = candidate.name.lower()
        if "guardrail" in name or "safety" in name:
            return candidate.resolve()
    return None


def compute_target_profile(target: Path) -> dict[str, Any]:
    markdown_files = []
    if target.is_dir():
        markdown_files = [str(path.resolve()) for path in sorted(target.rglob("*.md"))]
    elif target.is_file() and target.suffix.lower() == ".md":
        markdown_files = [str(target.resolve())]
    return {
        "path": str(target),
        "exists": target.exists(),
        "kind": "directory" if target.is_dir() else "file" if target.is_file() else "missing",
        "name": target.name,
        "has_references": (target / "references").exists() if target.is_dir() else False,
        "markdown_files": markdown_files[:20],
    }


def classify_feedback(entries: list[dict[str, Any]]) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {
        "limitations": [],
        "examples": [],
        "workflow": [],
        "tests": [],
        "guardrails": [],
        "prompt": [],
    }
    for entry in entries:
        snippet = entry.get("snippet", "")
        lowered = snippet.lower()
        if any(word in lowered for word in ("limit", "boundary", "expect", "integrat", "not automate", "manual")):
            buckets["limitations"].append(snippet)
        if any(word in lowered for word in ("example", "sample", "demo", "usage")):
            buckets["examples"].append(snippet)
        if any(word in lowered for word in ("workflow", "step", "orchestrat", "process", "route")):
            buckets["workflow"].append(snippet)
        if any(word in lowered for word in ("test", "validate", "smoke", "check")):
            buckets["tests"].append(snippet)
        if any(word in lowered for word in ("guardrail", "safe", "risk", "do not", "don't", "must not")):
            buckets["guardrails"].append(snippet)
        if any(word in lowered for word in ("prompt", "too long", "navigat", "discoverability", "section")):
            buckets["prompt"].append(snippet)
    return buckets


def protected_target(target_path: str) -> bool:
    lowered = target_path.lower()
    return any(keyword in lowered for keyword in PROTECTED_KEYWORDS)
