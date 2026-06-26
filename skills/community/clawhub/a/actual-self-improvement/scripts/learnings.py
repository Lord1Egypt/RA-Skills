#!/usr/bin/env python3
"""Manage workspace .learnings files for the self-improvement skill.

This script is designed for agentic use:
- non-interactive only
- structured JSON output by default
- clear errors on stderr
- no external dependencies
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Dict, Any, Optional

AREAS = ["frontend", "backend", "infra", "tests", "docs", "config"]
PRIORITIES = ["low", "medium", "high", "critical"]
STATUSES = ["pending", "in_progress", "resolved", "wont_fix", "promoted", "promoted_to_skill"]
LEARNING_CATEGORIES = ["correction", "knowledge_gap", "best_practice", "insight"]
COMPLEXITY = ["simple", "medium", "complex"]
FREQUENCY = ["first_time", "recurring"]
REPRODUCIBLE = ["yes", "no", "unknown"]
OUTPUT_FORMATS = ["json", "text", "markdown"]

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
ASSETS_DIR = SKILL_ROOT / "assets"

TEMPLATE_FILES = {
    "LEARNINGS.md": ASSETS_DIR / "LEARNINGS.md",
    "ERRORS.md": ASSETS_DIR / "ERRORS.md",
    "FEATURE_REQUESTS.md": ASSETS_DIR / "FEATURE_REQUESTS.md",
}

TYPE_CONFIG = {
    "learning": {"prefix": "LRN", "file": "LEARNINGS.md"},
    "error": {"prefix": "ERR", "file": "ERRORS.md"},
    "feature": {"prefix": "FEAT", "file": "FEATURE_REQUESTS.md"},
}

ENTRY_HEADER_RE = re.compile(r"^## \[(?P<id>[A-Z]+-\d{8}-\d{3})\] (?P<title>.+)$", re.M)
FIELD_RE = re.compile(r"^\*\*(?P<key>[^*]+)\*\*: (?P<value>.+)$", re.M)
SUMMARY_RE = re.compile(r"^### Summary\n(?P<summary>.+?)(?:\n\n|\n### |\Z)", re.M | re.S)
PATTERN_KEY_RE = re.compile(r"^- Pattern-Key: (?P<value>.+)$", re.M)
RECURRENCE_RE = re.compile(r"^- Recurrence-Count: (?P<value>\d+)\b", re.M)


class CliError(Exception):
    def __init__(self, message: str, exit_code: int = 1):
        super().__init__(message)
        self.exit_code = exit_code


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def print_output(payload: Any, fmt: str) -> None:
    if fmt == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    if isinstance(payload, dict):
        if fmt == "markdown":
            for key, value in payload.items():
                print(f"- **{key}**: {value}")
        else:
            for key, value in payload.items():
                print(f"{key}: {value}")
        return
    if isinstance(payload, list):
        if fmt == "markdown":
            for item in payload:
                print(f"- {item}")
        else:
            for item in payload:
                print(item)
        return
    print(payload)


def resolve_root(path_str: str) -> Path:
    root = Path(path_str).expanduser().resolve()
    if not root.exists():
        raise CliError(f"Workspace root does not exist: {root}", 2)
    if not root.is_dir():
        raise CliError(f"Workspace root is not a directory: {root}", 2)
    return root


def learnings_dir(root: Path) -> Path:
    return root / ".learnings"


def require_learnings_dir(root: Path) -> Path:
    directory = learnings_dir(root)
    if not directory.exists():
        raise CliError(
            f"Missing {directory}. Run 'python3 scripts/learnings.py init --root {root}' first.",
            2,
        )
    return directory


def read_text_or_file(text: Optional[str], file_path: Optional[str], field_name: str) -> str:
    if text and file_path:
        raise CliError(f"Provide either --{field_name} or --{field_name}-file, not both.")
    if file_path:
        path = Path(file_path).expanduser().resolve()
        if not path.exists():
            raise CliError(f"File not found for --{field_name}-file: {path}", 2)
        return path.read_text(encoding="utf-8").rstrip()
    return (text or "").rstrip()


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def next_id(target_file: Path, prefix: str) -> str:
    date_part = today_str()
    pattern = re.compile(rf"\[{prefix}-{date_part}-(\d{{3}})\]")
    max_seq = 0
    if target_file.exists():
        text = target_file.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            max_seq = max(max_seq, int(match.group(1)))
    return f"{prefix}-{date_part}-{max_seq + 1:03d}"


def ensure_choice(value: str, allowed: Iterable[str], label: str) -> str:
    if value not in allowed:
        raise CliError(f"Invalid {label}: {value}. Allowed values: {', '.join(allowed)}")
    return value


def split_csvish(values: Optional[List[str]]) -> List[str]:
    if not values:
        return []
    result: List[str] = []
    for value in values:
        for part in value.split(","):
            clean = part.strip()
            if clean:
                result.append(clean)
    return result


def normalise_metadata_lines(lines: List[str]) -> List[str]:
    return [line for line in lines if line and not line.endswith(": ")]


def append_entry(target_file: Path, entry: str) -> None:
    target_file.parent.mkdir(parents=True, exist_ok=True)
    prefix = "\n" if target_file.exists() and target_file.read_text(encoding="utf-8").rstrip() else ""
    with target_file.open("a", encoding="utf-8") as f:
        f.write(prefix)
        f.write(entry.rstrip())
        f.write("\n")


def parse_entries(file_path: Path) -> List[Dict[str, Any]]:
    if not file_path.exists():
        return []
    text = file_path.read_text(encoding="utf-8")
    matches = list(ENTRY_HEADER_RE.finditer(text))
    entries: List[Dict[str, Any]] = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end].strip()
        fields = {m.group("key").strip(): m.group("value").strip() for m in FIELD_RE.finditer(block)}
        summary_match = SUMMARY_RE.search(block)
        pattern_key_match = PATTERN_KEY_RE.search(block)
        recurrence_match = RECURRENCE_RE.search(block)
        entries.append(
            {
                "id": match.group("id"),
                "title": match.group("title").strip(),
                "summary": summary_match.group("summary").strip() if summary_match else "",
                "fields": fields,
                "pattern_key": pattern_key_match.group("value").strip() if pattern_key_match else None,
                "recurrence_count": int(recurrence_match.group("value")) if recurrence_match else None,
                "text": block,
                "file": str(file_path),
            }
        )
    return entries


def kind_to_file(root: Path, kind: str) -> Path:
    return require_learnings_dir(root) / TYPE_CONFIG[kind]["file"]


def cmd_init(args: argparse.Namespace) -> Dict[str, Any]:
    root = resolve_root(args.root)
    directory = learnings_dir(root)
    directory.mkdir(parents=True, exist_ok=True)
    created: List[str] = []
    skipped: List[str] = []

    for name, template in TEMPLATE_FILES.items():
        target = directory / name
        if target.exists() and not args.force:
            skipped.append(str(target))
            continue
        shutil.copyfile(template, target)
        created.append(str(target))

    return {
        "ok": True,
        "workspace_root": str(root),
        "learnings_dir": str(directory),
        "created": created,
        "skipped": skipped,
    }


def cmd_status(args: argparse.Namespace) -> Dict[str, Any]:
    root = resolve_root(args.root)
    directory = require_learnings_dir(root)
    all_entries: List[Dict[str, Any]] = []
    by_file: Dict[str, int] = {}

    for name in TEMPLATE_FILES:
        file_path = directory / name
        entries = parse_entries(file_path)
        by_file[name] = len(entries)
        all_entries.extend(entries)

    status_counts = Counter(entry["fields"].get("Status", "unknown") for entry in all_entries)
    priority_counts = Counter(entry["fields"].get("Priority", "unknown") for entry in all_entries)

    pending_high = [
        {
            "id": entry["id"],
            "title": entry["title"],
            "summary": entry["summary"],
            "file": entry["file"],
        }
        for entry in all_entries
        if entry["fields"].get("Status") == "pending"
        and entry["fields"].get("Priority") in {"high", "critical"}
    ]

    promotion_candidates = [
        {
            "id": entry["id"],
            "title": entry["title"],
            "summary": entry["summary"],
            "recurrence_count": entry["recurrence_count"],
        }
        for entry in all_entries
        if (entry["recurrence_count"] or 0) >= 3
        and entry["fields"].get("Status") in {"pending", "resolved"}
    ]

    return {
        "ok": True,
        "workspace_root": str(root),
        "counts": {
            "total_entries": len(all_entries),
            "by_file": by_file,
            "by_status": dict(status_counts),
            "by_priority": dict(priority_counts),
        },
        "pending_high_priority": pending_high[: args.limit],
        "promotion_candidates": promotion_candidates[: args.limit],
    }


def cmd_search(args: argparse.Namespace) -> Dict[str, Any]:
    root = resolve_root(args.root)
    directory = require_learnings_dir(root)
    query = args.query.strip().lower()
    if not query:
        raise CliError("--query must be non-empty")

    files = {
        None: list(TEMPLATE_FILES.keys()),
        "learning": [TYPE_CONFIG["learning"]["file"]],
        "error": [TYPE_CONFIG["error"]["file"]],
        "feature": [TYPE_CONFIG["feature"]["file"]],
    }[args.kind]

    matches: List[Dict[str, Any]] = []
    for file_name in files:
        for entry in parse_entries(directory / file_name):
            haystack = "\n".join(
                [entry["id"], entry["title"], entry["summary"], entry["text"], entry.get("pattern_key") or ""]
            ).lower()
            if query in haystack:
                matches.append(
                    {
                        "id": entry["id"],
                        "title": entry["title"],
                        "summary": entry["summary"],
                        "file": entry["file"],
                        "status": entry["fields"].get("Status"),
                        "priority": entry["fields"].get("Priority"),
                        "pattern_key": entry.get("pattern_key"),
                    }
                )
    return {
        "ok": True,
        "workspace_root": str(root),
        "query": args.query,
        "count": len(matches),
        "matches": matches[: args.limit],
    }


def render_metadata(lines: List[str]) -> str:
    valid = normalise_metadata_lines(lines)
    return "\n".join(valid) if valid else "- Source: unknown"


def cmd_log_learning(args: argparse.Namespace) -> Dict[str, Any]:
    root = resolve_root(args.root)
    directory = require_learnings_dir(root)
    ensure_choice(args.category, LEARNING_CATEGORIES, "category")
    ensure_choice(args.priority, PRIORITIES, "priority")
    ensure_choice(args.status, STATUSES, "status")
    ensure_choice(args.area, AREAS, "area")

    details = read_text_or_file(args.details, args.details_file, "details")
    suggested_action = read_text_or_file(args.suggested_action, args.suggested_action_file, "suggested-action")
    tags = ", ".join(split_csvish(args.tags))
    related_files = ", ".join(split_csvish(args.related_files))
    see_also = ", ".join(split_csvish(args.see_also))

    target_file = directory / TYPE_CONFIG["learning"]["file"]
    entry_id = next_id(target_file, TYPE_CONFIG["learning"]["prefix"])
    metadata_lines = [
        f"- Source: {args.source}",
        f"- Related Files: {related_files}" if related_files else "",
        f"- Tags: {tags}" if tags else "",
        f"- See Also: {see_also}" if see_also else "",
        f"- Pattern-Key: {args.pattern_key}" if args.pattern_key else "",
        f"- Recurrence-Count: {args.recurrence_count}" if args.recurrence_count is not None else "",
        f"- First-Seen: {args.first_seen}" if args.first_seen else "",
        f"- Last-Seen: {args.last_seen}" if args.last_seen else "",
    ]

    entry = f"""## [{entry_id}] {args.category}

**Logged**: {now_iso()}
**Priority**: {args.priority}
**Status**: {args.status}
**Area**: {args.area}

### Summary
{args.summary}

### Details
{details or '[TODO: add details]'}

### Suggested Action
{suggested_action or '[TODO: add suggested action]'}

### Metadata
{render_metadata(metadata_lines)}

---
"""

    if not args.dry_run:
        append_entry(target_file, entry)

    return {
        "ok": True,
        "action": "dry_run" if args.dry_run else "logged",
        "kind": "learning",
        "id": entry_id,
        "target_file": str(target_file),
        "summary": args.summary,
        "entry_markdown": entry.strip(),
    }


def cmd_log_error(args: argparse.Namespace) -> Dict[str, Any]:
    root = resolve_root(args.root)
    directory = require_learnings_dir(root)
    ensure_choice(args.priority, PRIORITIES, "priority")
    ensure_choice(args.status, STATUSES, "status")
    ensure_choice(args.area, AREAS, "area")
    ensure_choice(args.reproducible, REPRODUCIBLE, "reproducible")

    error_text = read_text_or_file(args.error_text, args.error_text_file, "error-text")
    context = read_text_or_file(args.context, args.context_file, "context")
    suggested_fix = read_text_or_file(args.suggested_fix, args.suggested_fix_file, "suggested-fix")
    related_files = ", ".join(split_csvish(args.related_files))
    see_also = ", ".join(split_csvish(args.see_also))

    target_file = directory / TYPE_CONFIG["error"]["file"]
    entry_id = next_id(target_file, TYPE_CONFIG["error"]["prefix"])
    metadata_lines = [
        f"- Reproducible: {args.reproducible}",
        f"- Related Files: {related_files}" if related_files else "",
        f"- See Also: {see_also}" if see_also else "",
    ]

    entry = f"""## [{entry_id}] {args.name}

**Logged**: {now_iso()}
**Priority**: {args.priority}
**Status**: {args.status}
**Area**: {args.area}

### Summary
{args.summary}

### Error
```
{error_text or '[TODO: add representative error output]'}
```

### Context
{context or '[TODO: add context]'}

### Suggested Fix
{suggested_fix or '[TODO: add suggested fix]'}

### Metadata
{render_metadata(metadata_lines)}

---
"""

    if not args.dry_run:
        append_entry(target_file, entry)

    return {
        "ok": True,
        "action": "dry_run" if args.dry_run else "logged",
        "kind": "error",
        "id": entry_id,
        "target_file": str(target_file),
        "summary": args.summary,
        "entry_markdown": entry.strip(),
    }


def cmd_log_feature(args: argparse.Namespace) -> Dict[str, Any]:
    root = resolve_root(args.root)
    directory = require_learnings_dir(root)
    ensure_choice(args.priority, PRIORITIES, "priority")
    ensure_choice(args.status, STATUSES, "status")
    ensure_choice(args.area, AREAS, "area")
    ensure_choice(args.complexity_estimate, COMPLEXITY, "complexity-estimate")
    ensure_choice(args.frequency, FREQUENCY, "frequency")

    user_context = read_text_or_file(args.user_context, args.user_context_file, "user-context")
    suggested_impl = read_text_or_file(
        args.suggested_implementation,
        args.suggested_implementation_file,
        "suggested-implementation",
    )
    related_features = ", ".join(split_csvish(args.related_features))

    target_file = directory / TYPE_CONFIG["feature"]["file"]
    entry_id = next_id(target_file, TYPE_CONFIG["feature"]["prefix"])
    metadata_lines = [
        f"- Frequency: {args.frequency}",
        f"- Related Features: {related_features}" if related_features else "",
    ]

    entry = f"""## [{entry_id}] {args.capability}

**Logged**: {now_iso()}
**Priority**: {args.priority}
**Status**: {args.status}
**Area**: {args.area}

### Requested Capability
{args.capability.replace('-', ' ')}

### Summary
{args.summary}

### User Context
{user_context or '[TODO: add user context]'}

### Complexity Estimate
{args.complexity_estimate}

### Suggested Implementation
{suggested_impl or '[TODO: add suggested implementation]'}

### Metadata
{render_metadata(metadata_lines)}

---
"""

    if not args.dry_run:
        append_entry(target_file, entry)

    return {
        "ok": True,
        "action": "dry_run" if args.dry_run else "logged",
        "kind": "feature",
        "id": entry_id,
        "target_file": str(target_file),
        "summary": args.summary,
        "entry_markdown": entry.strip(),
    }


def add_common_output_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--format", choices=OUTPUT_FORMATS, default="json", help="Output format (default: json)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage workspace .learnings files for the self-improvement skill.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create .learnings files in a workspace")
    init_parser.add_argument("--root", required=True, help="Workspace root where .learnings should live")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing template files")
    add_common_output_arg(init_parser)
    init_parser.set_defaults(func=cmd_init)

    status_parser = subparsers.add_parser("status", help="Summarise current learnings status")
    status_parser.add_argument("--root", required=True, help="Workspace root containing .learnings")
    status_parser.add_argument("--limit", type=int, default=10, help="Max items for list sections")
    add_common_output_arg(status_parser)
    status_parser.set_defaults(func=cmd_status)

    search_parser = subparsers.add_parser("search", help="Search learnings entries")
    search_parser.add_argument("--root", required=True, help="Workspace root containing .learnings")
    search_parser.add_argument("--query", required=True, help="Case-insensitive search query")
    search_parser.add_argument("--kind", choices=["learning", "error", "feature"], default=None, help="Restrict to one entry kind")
    search_parser.add_argument("--limit", type=int, default=10, help="Max matches to return")
    add_common_output_arg(search_parser)
    search_parser.set_defaults(func=cmd_search)

    ll_parser = subparsers.add_parser("log-learning", help="Append a learning entry")
    ll_parser.add_argument("--root", required=True, help="Workspace root containing .learnings")
    ll_parser.add_argument("--category", required=True, choices=LEARNING_CATEGORIES)
    ll_parser.add_argument("--summary", required=True)
    ll_parser.add_argument("--priority", default="medium", choices=PRIORITIES)
    ll_parser.add_argument("--status", default="pending", choices=STATUSES)
    ll_parser.add_argument("--area", default="backend", choices=AREAS)
    ll_parser.add_argument("--details")
    ll_parser.add_argument("--details-file")
    ll_parser.add_argument("--suggested-action")
    ll_parser.add_argument("--suggested-action-file")
    ll_parser.add_argument("--source", default="conversation")
    ll_parser.add_argument("--related-files", nargs="*")
    ll_parser.add_argument("--tags", nargs="*")
    ll_parser.add_argument("--see-also", nargs="*")
    ll_parser.add_argument("--pattern-key")
    ll_parser.add_argument("--recurrence-count", type=int)
    ll_parser.add_argument("--first-seen")
    ll_parser.add_argument("--last-seen")
    ll_parser.add_argument("--dry-run", action="store_true")
    add_common_output_arg(ll_parser)
    ll_parser.set_defaults(func=cmd_log_learning)

    le_parser = subparsers.add_parser("log-error", help="Append an error entry")
    le_parser.add_argument("--root", required=True, help="Workspace root containing .learnings")
    le_parser.add_argument("--name", required=True, help="Short error identifier, e.g. docker-build")
    le_parser.add_argument("--summary", required=True)
    le_parser.add_argument("--priority", default="high", choices=PRIORITIES)
    le_parser.add_argument("--status", default="pending", choices=STATUSES)
    le_parser.add_argument("--area", default="backend", choices=AREAS)
    le_parser.add_argument("--error-text")
    le_parser.add_argument("--error-text-file")
    le_parser.add_argument("--context")
    le_parser.add_argument("--context-file")
    le_parser.add_argument("--suggested-fix")
    le_parser.add_argument("--suggested-fix-file")
    le_parser.add_argument("--reproducible", default="unknown", choices=REPRODUCIBLE)
    le_parser.add_argument("--related-files", nargs="*")
    le_parser.add_argument("--see-also", nargs="*")
    le_parser.add_argument("--dry-run", action="store_true")
    add_common_output_arg(le_parser)
    le_parser.set_defaults(func=cmd_log_error)

    lf_parser = subparsers.add_parser("log-feature", help="Append a feature request entry")
    lf_parser.add_argument("--root", required=True, help="Workspace root containing .learnings")
    lf_parser.add_argument("--capability", required=True, help="Capability slug, e.g. export-to-csv")
    lf_parser.add_argument("--summary", required=True)
    lf_parser.add_argument("--priority", default="medium", choices=PRIORITIES)
    lf_parser.add_argument("--status", default="pending", choices=STATUSES)
    lf_parser.add_argument("--area", default="backend", choices=AREAS)
    lf_parser.add_argument("--user-context")
    lf_parser.add_argument("--user-context-file")
    lf_parser.add_argument("--complexity-estimate", default="medium", choices=COMPLEXITY)
    lf_parser.add_argument("--suggested-implementation")
    lf_parser.add_argument("--suggested-implementation-file")
    lf_parser.add_argument("--frequency", default="first_time", choices=FREQUENCY)
    lf_parser.add_argument("--related-features", nargs="*")
    lf_parser.add_argument("--dry-run", action="store_true")
    add_common_output_arg(lf_parser)
    lf_parser.set_defaults(func=cmd_log_feature)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        payload = args.func(args)
        print_output(payload, args.format)
        return 0
    except CliError as exc:
        eprint(f"Error: {exc}")
        return exc.exit_code


if __name__ == "__main__":
    sys.exit(main())
