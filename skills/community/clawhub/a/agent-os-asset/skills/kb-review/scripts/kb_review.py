#!/usr/bin/env python3
"""Operate on kb-review Markdown review files. / 操作 kb-review Markdown 审查文件。

Core behavior / 核心行为:
- Parse review tables with stable decision and source_path fields. / 解析包含稳定 decision 与 source_path 字段的审查表。
- Preview delete and rollback by default; require --execute for mutation. / 默认预演 delete 与 rollback；变更必须使用 --execute。
- Write read-only SecondBrain coverage reports. / 生成只读 SecondBrain coverage 报告。
- Preserve legacy decisions and report conflicts without acting on them. / 兼容旧版 decision，并报告冲突但不执行。
- Constrain destructive operations to an explicit review root. / 将破坏性操作限制在显式 review root 内。
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import fnmatch
import os
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

REVIEW_FILES = ("keep.md", "delete.md", "review.md", "duplicates.md")
TABLE_FIELDS = ["decision", "title", "reason", "source_path"]
REPORT_FIELDS = ["status", "duplicate_group", "decision", "confidence", "title", "source_path"]
DELETE_LOG_FIELDS = [*REPORT_FIELDS, "trash_path", "executed_at", "note", "pruned_dirs"]
ROLLBACK_LOG_FIELDS = ["status", "source_path", "trash_path", "restored_path", "note"]
COVERAGE_LOG_FIELDS = [
    "status",
    "review_file",
    "decision",
    "confidence",
    "title",
    "source_path",
    "agent_record_id",
    "agent_path",
    "note",
]
DECISION_ACTIONS = {"1": "keep", "0": "delete", "keep": "keep", "delete": "delete", "review": "review"}
DEFAULT_FORBIDDEN_TAGS = ("PII",)
DEFAULT_SCAN_EXCLUDED_TAGS = ("archived",)
PRUNE_IGNORED_FILENAMES = {".DS_Store"}
DEFAULT_SCAN_EXCLUDED_PATTERNS = (
    "KB-Review-*",
    "KB-Refactor-*",
    "AI-Era-*",
    ".obsidian",
    ".trash",
    ".Trash",
    ".smart-env",
    "Archived",
    "Attachment",
    "Attachments",
    "Attachment.*",
    "Attachments.*",
    "attachment",
    "attachments",
    "attachment.*",
    "attachments.*",
    # bilingual-compat: exact Chinese attachment path literal retained for legacy matching
    "附件",
    # bilingual-compat: exact Chinese attachment path literal retained for legacy matching
    "附件文件",
    # bilingual-compat: exact Chinese attachment basename pattern retained for legacy matching
    "附件.*",
    # bilingual-compat: exact Chinese attachment basename pattern retained for legacy matching
    "附件文件.*",
)
LINK_TITLE_RE = re.compile(r"^(?P<destination>.+?)(?P<title>\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))$")
MAX_FRONTMATTER_BYTES = 64 * 1024
MAX_FRONTMATTER_LINE_BYTES = 8 * 1024
SKILL_DIR = Path(__file__).resolve().parents[1]
NESTED_SKILLS_DIR = SKILL_DIR.parent


def default_second_brain_index() -> Path:
    """Resolve the sibling second-brain index without assuming a user home layout."""
    explicit = os.environ.get("KB_REVIEW_SECOND_BRAIN_INDEX")
    if explicit:
        return Path(explicit).expanduser().resolve(strict=False)
    package_root = os.environ.get("KB_REVIEW_PACKAGE_ROOT")
    skills_dir = (
        Path(package_root).expanduser().resolve(strict=False) / "skills"
        if package_root
        else NESTED_SKILLS_DIR
    )
    return skills_dir / "second-brain" / "references" / "generated" / "documents.jsonl"


def is_within(path: Path, root: Path) -> bool:
    """Return whether path resolves inside root, including root itself."""
    resolved = path.expanduser().resolve(strict=False)
    resolved_root = root.expanduser().resolve(strict=False)
    try:
        resolved.relative_to(resolved_root)
        return True
    except ValueError:
        return False


def resolve_trash_dir(explicit: Path | None = None, adapter: str = "portable") -> Path:
    """Resolve a recoverable Trash directory with portable and macOS adapters."""
    override = explicit or (Path(os.environ["KB_REVIEW_TRASH_DIR"]) if os.environ.get("KB_REVIEW_TRASH_DIR") else None)
    if override is not None:
        return override.expanduser().resolve(strict=False)
    if adapter == "macos":
        if sys.platform != "darwin":
            raise ValueError("trash adapter 'macos' is only available on macOS / Trash adapter 'macos' 仅可用于 macOS")
        return Path.home() / ".Trash"
    if adapter != "portable":
        raise ValueError(f"unsupported trash adapter: {adapter} / 不支持的 Trash adapter：{adapter}")
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
        return (base / "kb-review" / "Trash").expanduser().resolve(strict=False)
    data_home = Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share")))
    return (data_home / "Trash" / "files").expanduser().resolve(strict=False)


def split_md_row(line: str) -> list[str]:
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in line.strip().strip("|"):
        if char == "\\" and not escaped:
            escaped = True
            current.append(char)
            continue
        if char == "|" and not escaped:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        escaped = False
    cells.append("".join(current).strip())
    return cells


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(set(cell.replace(":", "").strip()) <= {"-"} for cell in cells)


def read_review_table(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if not line.strip().startswith("|"):
            continue
        cells = split_md_row(line)
        normalized = [cell.strip(" `") for cell in cells]
        if header is None and all(field in normalized for field in TABLE_FIELDS):
            header = normalized
            continue
        if header is None or is_separator(normalized):
            continue
        values = {field: cells[index].strip() if index < len(cells) else "" for index, field in enumerate(header)}
        row = {field: values.get(field, "").strip() for field in TABLE_FIELDS}
        row["index"] = values.get("index", "").strip()
        row["confidence"] = values.get("confidence", "").strip()
        row["duplicate_group"] = values.get("duplicate_group", "").strip()
        row["review_file"] = path.name
        row["line_no"] = str(line_no)
        row["decision"] = row["decision"].lower().strip()
        parsed_source = source_path_from_cell(row["source_path"], path.parent)
        row["source_path"] = str(parsed_source) if parsed_source is not None else ""
        rows.append(row)
    return rows


def read_all_review_rows(review_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for file_name in REVIEW_FILES:
        rows.extend(read_review_table(review_dir / file_name))
    return rows


def find_obsidian_vault_root(base_dir: Path) -> Path | None:
    """Return the nearest ancestor that looks like an Obsidian vault."""
    current = base_dir.expanduser().resolve(strict=False)
    for candidate in (current, *current.parents):
        if (candidate / ".obsidian").is_dir():
            return candidate
    return None


def wiki_link_destination(value: str) -> str | None:
    """Extract the file target from an Obsidian wikilink cell."""
    wiki_match = re.match(r"^!?\[\[(?P<body>.*?)\]\]$", value)
    if not wiki_match:
        return None
    body = wiki_match.group("body").replace(r"\|", "|").strip()
    if not body:
        return None
    destination = body.split("|", 1)[0].strip()
    destination = destination.split("#", 1)[0].split("^", 1)[0].strip()
    return destination or None


def resolve_wiki_path(path: Path, base_dir: Path, vault_root: Path | None) -> Path:
    root = vault_root if vault_root is not None else base_dir
    resolved = path if path.is_absolute() else root / path
    if resolved.exists() or str(resolved).endswith(".md"):
        return resolved.resolve(strict=False)
    markdown_candidate = Path(f"{resolved}.md")
    if markdown_candidate.exists():
        return markdown_candidate.resolve(strict=False)
    return resolved.resolve(strict=False)


def source_path_from_cell(cell: str, base_dir: Path) -> Path | None:
    value = (cell or "").strip()
    if not value:
        return None
    wiki_destination = wiki_link_destination(value)
    if wiki_destination is not None:
        destination = unquote(wiki_destination)
        path = Path(destination).expanduser()
        vault_root = find_obsidian_vault_root(base_dir)
        return resolve_wiki_path(path, base_dir, vault_root)
    link_match = re.match(r"^!?\[[^\]\n]*\]\((?P<target>.*)\)$", value)
    if link_match:
        value = link_match.group("target").strip()
    destination, _, _ = parse_link_destination(value)
    destination = unquote(destination.strip())
    if not destination:
        return None
    path = Path(destination).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    return path.resolve(strict=False)


def normalize_source_key(source_path: str) -> str:
    if not source_path.strip():
        return ""
    return str(Path(source_path).expanduser().resolve(strict=False))


def decision_action(decision: str) -> str | None:
    return DECISION_ACTIONS.get(decision.lower().strip())


def split_actionable_rows(rows: list[dict[str, str]], wanted_decision: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Return actionable rows plus skipped invalid/conflict rows for reports."""
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    skipped: list[dict[str, str]] = []

    for row in rows:
        source_key = normalize_source_key(row.get("source_path", ""))
        if not source_key:
            skipped.append({**row, "source_path": row.get("source_path", ""), "status": "invalid-row", "note": "source_path is empty / source_path 为空"})
            continue
        action = decision_action(row.get("decision", ""))
        if action is None:
            skipped.append({**row, "status": "invalid-decision", "note": "decision must be 1/0; legacy keep/delete/review values remain compatible / decision 必须是 1/0；兼容旧值 keep/delete/review"})
            continue
        grouped[source_key].append({**row, "source_path": source_key, "action": action})

    actionable: list[dict[str, str]] = []
    for source_key, same_source_rows in grouped.items():
        actions = {row["action"] for row in same_source_rows}
        if len(actions) > 1:
            files = ", ".join(f"{row['review_file']}:{row['line_no']}={row['decision']}" for row in same_source_rows)
            representative = same_source_rows[0]
            skipped.append({**representative, "status": "conflict", "note": f"Multiple decisions found for one source_path: {files} / 同一 source_path 出现多个 decision：{files}"})
            continue
        action = next(iter(actions))
        if action == wanted_decision:
            actionable.append(same_source_rows[0])
    return actionable, skipped


def escape_cell(value: str) -> str:
    return " ".join((value or "").replace("|", "/").replace("\n", " ").replace("\r", " ").split())


def write_log(path: Path, title: str, rows: list[dict[str, str]], fields: list[str]) -> None:
    lines = [
        f"# {title}",
        "",
        f"- rows / 行数: {len(rows)}",
        "",
        "- Field names and status values are stable machine identifiers. / 字段名和状态值是稳定的机器标识符。",
        "",
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_cell(row.get(field, "")) for field in fields) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_second_brain_records(index_path: Path) -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    if not index_path.exists():
        return records
    for line in index_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("record_type") != "document":
            continue
        path = str(record.get("path", "")).strip()
        if not path:
            continue
        records[path] = {
            "record_id": str(record.get("record_id", "")),
            "path": path,
            "title": str(record.get("title", "")),
        }
    return records


def relative_to_vault(path: Path, vault_root: Path) -> str:
    resolved = path.expanduser().resolve(strict=False)
    root = vault_root.expanduser().resolve(strict=False)
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError:
        return resolved.as_posix()


def agent_readable_candidate_paths(relative_path: str) -> list[str]:
    candidates: list[str] = []
    path = Path(relative_path)
    if path.name.endswith(".agent.md"):
        candidate = path.as_posix()
    elif path.suffix:
        candidate = path.with_suffix(".agent.md").as_posix()
    else:
        candidate = f"{path.as_posix()}.agent.md"
    candidates.append(candidate)
    return candidates


def second_brain_coverage_for_path(
    source_path: Path,
    vault_root: Path,
    records: dict[str, dict[str, str]],
) -> dict[str, str]:
    relative = relative_to_vault(source_path, vault_root)
    if relative.startswith("Archived/") or "Archived" in Path(relative).parts:
        return {
            "status": "skipped-archived",
            "agent_record_id": "",
            "agent_path": "",
            "note": "Archived sources are lifecycle-excluded from kb-review and SecondBrain coverage / Archived 源文件按生命周期规则排除在 kb-review 与 SecondBrain coverage 之外",
        }
    if "archived" in read_frontmatter_tags(source_path):
        return {
            "status": "skipped-archived",
            "agent_record_id": "",
            "agent_path": "",
            "note": "archived-tagged sources are lifecycle-excluded from kb-review and SecondBrain coverage / 带 archived tag 的源文件按生命周期规则排除在 kb-review 与 SecondBrain coverage 之外",
        }
    if relative in records:
        record = records[relative]
        return {
            "status": "indexed-agent-doc" if relative.endswith(".agent.md") else "indexed-document",
            "agent_record_id": record.get("record_id", ""),
            "agent_path": record.get("path", ""),
            "note": "source_path itself is present in the SecondBrain index / source_path 本身已存在于 SecondBrain index",
        }
    for candidate in agent_readable_candidate_paths(relative):
        record = records.get(candidate)
        if record:
            return {
                "status": "covered-by-agent-doc",
                "agent_record_id": record.get("record_id", ""),
                "agent_path": record.get("path", ""),
                "note": "A matching .agent.md is indexed by SecondBrain / 匹配的 .agent.md 已被 SecondBrain 索引",
            }
    return {
        "status": "not-covered",
        "agent_record_id": "",
        "agent_path": "",
        "note": "No matching indexed .agent.md was found / 未找到匹配的已索引 .agent.md",
    }


def second_brain_coverage_rows(
    review_dir: Path,
    index_path: Path,
    vault_root: Path,
) -> list[dict[str, str]]:
    records = load_second_brain_records(index_path)
    rows: list[dict[str, str]] = []
    for row in read_all_review_rows(review_dir):
        source_path = row.get("source_path", "")
        if not source_path:
            coverage = {
                "status": "invalid-row",
                "agent_record_id": "",
                "agent_path": "",
                "note": "source_path is empty / source_path 为空",
            }
        elif not records:
            coverage = {
                "status": "index-missing",
                "agent_record_id": "",
                "agent_path": "",
                "note": f"SecondBrain index is missing or empty: {index_path} / SecondBrain index 缺失或为空：{index_path}",
            }
        else:
            coverage = second_brain_coverage_for_path(Path(source_path), vault_root, records)
        rows.append(
            {
                **row,
                "status": coverage["status"],
                "agent_record_id": coverage["agent_record_id"],
                "agent_path": coverage["agent_path"],
                "note": coverage["note"],
            }
        )
    return rows


def write_second_brain_coverage_report(
    review_dir: Path,
    index_path: Path | None = None,
    vault_root: Path | None = None,
) -> list[dict[str, str]]:
    index_path = index_path if index_path is not None else default_second_brain_index()
    vault = vault_root if vault_root is not None else review_dir.parent
    rows = second_brain_coverage_rows(review_dir, index_path, vault)
    write_log(
        review_dir / "second-brain-coverage.md",
        "Second Brain Coverage / 第二大脑覆盖情况",
        rows,
        COVERAGE_LOG_FIELDS,
    )
    return rows


def read_markdown_table(path: Path, required_fields: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        return []
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = split_md_row(line)
        normalized = [cell.strip(" `") for cell in cells]
        if header is None and all(field in normalized for field in required_fields):
            header = normalized
            continue
        if header is None or is_separator(normalized):
            continue
        rows.append({field: cells[index].strip() if index < len(cells) else "" for index, field in enumerate(header)})
    return rows


def parse_roots(values: list[str]) -> list[Path]:
    return [Path(value).expanduser().resolve() for value in values]


def parse_forbidden_tags(values: list[str]) -> list[str]:
    tags = list(DEFAULT_FORBIDDEN_TAGS)
    for value in values:
        tag = value.strip()
        if tag and tag not in tags:
            tags.append(tag)
    return tags


def scan_excluded_patterns(extra_patterns: list[str] | tuple[str, ...] | None = None) -> tuple[str, ...]:
    return (*DEFAULT_SCAN_EXCLUDED_PATTERNS, *(extra_patterns or ()))


def matches_scan_excluded_pattern(name: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatchcase(name, pattern) for pattern in patterns)


def path_parts_for_scan(path: Path, source_root: Path | None) -> tuple[str, ...]:
    resolved = path.expanduser().resolve(strict=False)
    if source_root is None:
        return resolved.parts
    root = source_root.expanduser().resolve(strict=False)
    try:
        return resolved.relative_to(root).parts
    except ValueError:
        return resolved.parts


def is_scan_excluded(path: Path, source_root: Path | None = None, extra_patterns: list[str] | tuple[str, ...] | None = None) -> bool:
    patterns = scan_excluded_patterns(extra_patterns)
    parts = path_parts_for_scan(path, source_root)
    return any(matches_scan_excluded_pattern(part, patterns) for part in parts)


def iter_scan_candidates(root: Path, extra_excluded_patterns: list[str] | tuple[str, ...] | None = None) -> list[Path]:
    root = root.expanduser().resolve(strict=False)
    patterns = scan_excluded_patterns(extra_excluded_patterns)
    candidates: list[Path] = []

    for current_root, dir_names, file_names in os.walk(root):
        current = Path(current_root)
        dir_names[:] = [
            dir_name
            for dir_name in sorted(dir_names)
            if not matches_scan_excluded_pattern(dir_name, patterns)
            and not is_scan_excluded(current / dir_name, root, extra_excluded_patterns)
        ]
        for file_name in sorted(file_names):
            path = current / file_name
            if is_scan_excluded(path, root, extra_excluded_patterns):
                continue
            if scan_excluded_tag_hits(path):
                continue
            candidates.append(path)
    return candidates


def scan_excluded_tag_hits(path: Path, extra_tags: list[str] | tuple[str, ...] | None = None) -> list[str]:
    excluded = set(DEFAULT_SCAN_EXCLUDED_TAGS)
    excluded.update(extra_tags or ())
    return [tag for tag in read_frontmatter_tags(path) if tag in excluded]


def is_forbidden(path: Path, forbidden_paths: list[Path]) -> bool:
    resolved = path.expanduser().resolve(strict=False)
    for forbidden in forbidden_paths:
        try:
            resolved.relative_to(forbidden)
            return True
        except ValueError:
            if resolved == forbidden:
                return True
    return False


def strip_yaml_comment(value: str) -> str:
    in_single = False
    in_double = False
    escaped = False
    for index, char in enumerate(value):
        if char == "\\" and in_double and not escaped:
            escaped = True
            continue
        if char == "'" and not in_double and not escaped:
            in_single = not in_single
        elif char == '"' and not in_single and not escaped:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
        escaped = False
    return value.strip()


def clean_tag(value: str) -> str:
    value = strip_yaml_comment(value).strip().rstrip(",")
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value.strip()


def split_tag_list(value: str) -> list[str]:
    try:
        return next(csv.reader([value], skipinitialspace=True))
    except csv.Error:
        return value.split(",")


def parse_tag_value(value: str) -> list[str]:
    value = strip_yaml_comment(value).strip()
    if not value or value == "[]":
        return []
    if value.startswith("["):
        value = value[1:-1] if value.endswith("]") else value[1:]
        values = split_tag_list(value)
    elif "," in value:
        values = split_tag_list(value)
    else:
        values = [value]
    return [tag for tag in (clean_tag(item) for item in values) if tag]


def parse_frontmatter_tags(lines: list[str]) -> list[str]:
    tags: list[str] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.match(r"^tags\s*:\s*(.*)$", stripped)
        if not match:
            continue
        value = match.group(1).strip()
        if value:
            tags.extend(parse_tag_value(value))
            break
        for nested in lines[index + 1 :]:
            if not nested.startswith((" ", "\t")):
                break
            item = nested.strip()
            if not item or item.startswith("#"):
                continue
            if item.startswith("- "):
                tags.extend(parse_tag_value(item[2:].strip()))
        break

    seen: set[str] = set()
    unique_tags: list[str] = []
    for tag in tags:
        if tag not in seen:
            unique_tags.append(tag)
            seen.add(tag)
    return unique_tags


def read_frontmatter_tags(path: Path) -> list[str]:
    try:
        with path.open("rb", buffering=0) as handle:
            first = handle.readline(MAX_FRONTMATTER_LINE_BYTES)
            first = first.removeprefix(b"\xef\xbb\xbf")
            if first.strip() != b"---":
                return []
            total = len(first)
            lines: list[str] = []
            while total <= MAX_FRONTMATTER_BYTES:
                raw = handle.readline(MAX_FRONTMATTER_LINE_BYTES)
                if not raw:
                    return []
                total += len(raw)
                if raw.strip() in {b"---", b"..."}:
                    return parse_frontmatter_tags(lines)
                if len(raw) >= MAX_FRONTMATTER_LINE_BYTES and not raw.endswith((b"\n", b"\r")):
                    return []
                lines.append(raw.rstrip(b"\r\n").decode("utf-8", errors="replace"))
    except OSError:
        return []
    return []


def forbidden_tag_hits(path: Path, forbidden_tags: list[str]) -> list[str]:
    if not forbidden_tags:
        return []
    forbidden = set(forbidden_tags)
    return [tag for tag in read_frontmatter_tags(path) if tag in forbidden]


def format_tag_hits(tags: list[str]) -> str:
    return ", ".join(tags)


def parse_link_destination(raw: str) -> tuple[str, str, bool]:
    value = (raw or "").strip()
    if value.startswith("<"):
        end = value.find(">")
        if end != -1:
            return value[1:end].strip(), value[end + 1 :].strip(), True
    match = LINK_TITLE_RE.match(value)
    if match:
        return match.group("destination").strip(), match.group("title").strip(), False
    return value, "", False


def trash_path_for(source: Path, trash_dir: Path) -> Path:
    candidate = trash_dir / source.name
    if not candidate.exists():
        return candidate
    stamp = timestamp_for_path()
    return unique_sibling_path(trash_dir / f"{source.stem}-{stamp}{source.suffix}")


def timestamp_for_path() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def unique_sibling_path(path: Path) -> Path:
    if not path.exists():
        return path
    for index in range(1, 1000):
        candidate = path.with_name(f"{path.stem}-{index}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"unable to find a unique restore path for {path} / 无法为 {path} 找到唯一恢复路径")


def validate_force_delete_patterns(patterns: list[str]) -> list[str]:
    """Accept only literal relative path-component sequences."""
    validated: list[str] = []
    for raw_pattern in patterns:
        pattern = raw_pattern.strip().replace("\\", "/")
        path = Path(pattern)
        if (
            not pattern
            or path.is_absolute()
            or re.match(r"^[A-Za-z]:/", pattern)
            or any(part in {"", ".", ".."} for part in path.parts)
            or any(character in pattern for character in "*?[]")
        ):
            raise ValueError("force-delete patterns must be literal relative path components without wildcards or '..' / force-delete pattern 必须是不含 wildcard 或 '..' 的字面量相对路径组件")
        validated.append("/".join(path.parts))
    return validated


def should_force_delete(source_path: Path, review_root: Path, patterns: list[str]) -> str:
    """Match a literal component sequence inside review_root, never a substring."""
    source = source_path.expanduser().resolve(strict=False)
    root = review_root.expanduser().resolve(strict=False)
    try:
        relative_parts = source.relative_to(root).parts
    except ValueError:
        return ""
    for pattern in validate_force_delete_patterns(patterns):
        pattern_parts = Path(pattern).parts
        width = len(pattern_parts)
        if any(
            tuple(relative_parts[index : index + width]) == pattern_parts
            for index in range(len(relative_parts) - width + 1)
        ):
            return pattern
    return ""


def split_delete_rows(
    rows: list[dict[str, str]],
    force_delete_path_contains: list[str],
    review_root: Path,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Return delete rows, with optional literal component force deletion."""
    force_delete_path_contains = validate_force_delete_patterns(force_delete_path_contains)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    skipped: list[dict[str, str]] = []

    for row in rows:
        source_key = normalize_source_key(row.get("source_path", ""))
        if not source_key:
            skipped.append({**row, "source_path": row.get("source_path", ""), "status": "invalid-row", "note": "source_path is empty / source_path 为空"})
            continue
        action = decision_action(row.get("decision", ""))
        if action is None:
            skipped.append({**row, "status": "invalid-decision", "note": "decision must be 1/0; legacy keep/delete/review values remain compatible / decision 必须是 1/0；兼容旧值 keep/delete/review"})
            continue
        force_pattern = should_force_delete(Path(source_key), review_root, force_delete_path_contains)
        grouped[source_key].append({**row, "source_path": source_key, "action": action, "force_pattern": force_pattern})

    actionable: list[dict[str, str]] = []
    for source_key, same_source_rows in grouped.items():
        forced = [row for row in same_source_rows if row["force_pattern"]]
        if forced:
            actionable.append({**forced[0], "force_pattern": forced[0]["force_pattern"]})
            continue
        actions = {row["action"] for row in same_source_rows}
        if len(actions) > 1:
            files = ", ".join(f"{row['review_file']}:{row['line_no']}={row['decision']}" for row in same_source_rows)
            representative = same_source_rows[0]
            skipped.append({**representative, "status": "conflict", "note": f"Multiple decisions found for one source_path: {files} / 同一 source_path 出现多个 decision：{files}"})
            continue
        if next(iter(actions)) == "delete":
            actionable.append(same_source_rows[0])
    return actionable, skipped


def remove_ignored_prune_files(directory: Path) -> bool:
    try:
        entries = list(directory.iterdir())
    except OSError:
        return False
    if not entries:
        return True
    if any(entry.name not in PRUNE_IGNORED_FILENAMES or not entry.is_file() for entry in entries):
        return False
    for entry in entries:
        try:
            entry.unlink()
        except OSError:
            return False
    return True


def prune_empty_parent_dirs(start_dir: Path, stop_dirs: set[Path]) -> list[str]:
    pruned: list[str] = []
    current = start_dir.resolve(strict=False)
    normalized_stops = {path.resolve(strict=False) for path in stop_dirs}
    while current != current.parent and current not in normalized_stops:
        if not current.exists():
            current = current.parent
            continue
        if not remove_ignored_prune_files(current):
            break
        try:
            current.rmdir()
        except OSError:
            break
        pruned.append(str(current))
        current = current.parent
    return pruned


def execute_delete(
    review_dir: Path,
    review_root: Path,
    forbidden_paths: list[Path],
    forbidden_tags: list[str],
    force_delete_path_contains: list[str],
    trash_dir: Path | None = None,
    trash_adapter: str = "portable",
    execute: bool = False,
) -> list[dict[str, str]]:
    review_dir = review_dir.expanduser().resolve(strict=False)
    review_root = review_root.expanduser().resolve(strict=False)
    if not is_within(review_dir, review_root):
        raise ValueError("review-dir must be inside review-root / review-dir 必须位于 review-root 内")
    resolved_trash_dir = resolve_trash_dir(trash_dir, trash_adapter)
    rows, skipped = split_delete_rows(
        read_all_review_rows(review_dir),
        force_delete_path_contains,
        review_root,
    )
    log_rows = skipped[:]
    for row in rows:
        source = Path(row["source_path"]).expanduser().resolve(strict=False)
        if not is_within(source, review_root):
            log_rows.append({**row, "status": "skipped-outside-review-root", "trash_path": "", "executed_at": "", "note": "source_path is outside the explicit review_root; deletion skipped / source_path 不在显式 review_root 内；跳过删除", "pruned_dirs": ""})
            continue
        if is_within(source, review_dir):
            log_rows.append({**row, "status": "skipped-review-directory", "trash_path": "", "executed_at": "", "note": "The review output directory cannot be deleted / review 输出目录不可删除", "pruned_dirs": ""})
            continue
        if is_forbidden(source, forbidden_paths):
            log_rows.append({**row, "status": "skipped-forbidden", "trash_path": "", "executed_at": "", "note": "The source matches forbidden_paths; deletion skipped / 源文件命中 forbidden_paths；跳过删除", "pruned_dirs": ""})
            continue
        if not source.exists():
            log_rows.append({**row, "status": "missing-source", "trash_path": "", "executed_at": "", "note": "Source file does not exist; parent directories were not pruned / 源文件不存在；未清理父目录", "pruned_dirs": ""})
            continue
        if not source.is_file():
            log_rows.append({**row, "status": "skipped-non-file", "trash_path": "", "executed_at": "", "note": "Only regular files may be moved to Trash / 只允许将普通文件移入 Trash", "pruned_dirs": ""})
            continue
        tag_hits = forbidden_tag_hits(source, forbidden_tags)
        if tag_hits:
            log_rows.append({**row, "status": "skipped-forbidden-tag", "trash_path": "", "executed_at": "", "note": f"The source matches forbidden_tags ({format_tag_hits(tag_hits)}); deletion skipped / 源文件命中 forbidden_tags ({format_tag_hits(tag_hits)})；跳过删除", "pruned_dirs": ""})
            continue
        target = trash_path_for(source, resolved_trash_dir)
        pruned_dirs: list[str] = []
        if execute:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(target))
            pruned_dirs = prune_empty_parent_dirs(source.parent, {review_dir, review_root})
        note = row.get("reason", "")
        if row.get("force_pattern"):
            note = f"force-delete-path-component={row['force_pattern']}; {note}".strip()
        log_rows.append({
            **row,
            "status": "moved-to-trash" if execute else "planned-trash",
            "trash_path": str(target),
            "executed_at": dt.datetime.now().isoformat(timespec="seconds"),
            "note": note,
            "pruned_dirs": "; ".join(pruned_dirs),
        })
    write_log(review_dir / "trash-execution-log.md", "Trash Execution Log / 回收站执行日志", log_rows, DELETE_LOG_FIELDS)
    return log_rows


def restored_conflict_path(source: Path) -> Path:
    return unique_sibling_path(source.with_name(f"{source.stem}.restored-{timestamp_for_path()}{source.suffix}"))


def rollback_delete(
    review_dir: Path,
    review_root: Path,
    trash_dir: Path | None = None,
    trash_adapter: str = "portable",
    execute: bool = False,
) -> list[dict[str, str]]:
    review_dir = review_dir.expanduser().resolve(strict=False)
    review_root = review_root.expanduser().resolve(strict=False)
    if not is_within(review_dir, review_root):
        raise ValueError("review-dir must be inside review-root / review-dir 必须位于 review-root 内")
    resolved_trash_dir = resolve_trash_dir(trash_dir, trash_adapter)
    log_path = review_dir / "trash-execution-log.md"
    rows = read_markdown_table(log_path, ["status", "source_path", "trash_path"])
    rollback_rows: list[dict[str, str]] = []

    for row in rows:
        if row.get("status") not in {"moved-to-trash", "trashed"}:
            continue
        source_cell = row.get("source_path", "")
        trash_cell = row.get("trash_path", "")
        source = source_path_from_cell(source_cell, log_path.parent)
        trash = source_path_from_cell(trash_cell, log_path.parent)
        if source is None or trash is None:
            rollback_rows.append({"status": "invalid-row", "source_path": source_cell, "trash_path": trash_cell, "restored_path": "", "note": "source_path or trash_path is empty / source_path 或 trash_path 为空"})
            continue
        if not is_within(source, review_root):
            rollback_rows.append({"status": "skipped-outside-review-root", "source_path": str(source), "trash_path": str(trash), "restored_path": "", "note": "source_path is outside the explicit review_root; rollback skipped / source_path 不在显式 review_root 内；跳过回退"})
            continue
        if is_within(source, review_dir):
            rollback_rows.append({"status": "skipped-review-directory", "source_path": str(source), "trash_path": str(trash), "restored_path": "", "note": "The review output directory cannot be a rollback target / review 输出目录不可作为回退目标"})
            continue
        if not is_within(trash, resolved_trash_dir):
            rollback_rows.append({"status": "skipped-outside-trash-root", "source_path": str(source), "trash_path": str(trash), "restored_path": "", "note": "trash_path is outside the configured Trash root; rollback skipped / trash_path 不在配置的 Trash 根目录内；跳过回退"})
            continue
        if not trash.exists():
            rollback_rows.append({"status": "missing-trash", "source_path": str(source), "trash_path": str(trash), "restored_path": "", "note": "trash_path does not exist; rollback is unavailable / trash_path 不存在；无法回退"})
            continue
        if source.exists():
            restored = restored_conflict_path(source)
            status = "restored-renamed-conflict" if execute else "planned-restore-renamed-conflict"
            note = f"source_path already exists; restore under a conflict name: {restored} / source_path 已存在；改用冲突名称恢复：{restored}"
        else:
            restored = source
            status = "restored" if execute else "planned-restore"
            note = "Restore to the original source_path / 恢复到原始 source_path"
        if execute:
            restored.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(trash), str(restored))
        rollback_rows.append({"status": status, "source_path": str(source), "trash_path": str(trash), "restored_path": str(restored), "note": note})

    write_log(review_dir / "trash-rollback-log.md", "Trash Rollback Log / 回收站回退日志", rollback_rows, ROLLBACK_LOG_FIELDS)
    return rollback_rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Operate on kb-review Markdown review files. / 操作 kb-review Markdown 审查文件。")
    parser.add_argument("--review-dir", required=True, help="Directory containing keep.md/delete.md/review.md/duplicates.md / 包含四个审查文件的目录")
    parser.add_argument("--review-root", type=Path, default=os.environ.get("KB_REVIEW_ROOT"), help="Explicit root bounding delete and rollback paths; required for destructive workflows / 限制删除与回退路径的显式根目录；破坏性流程必需")
    parser.add_argument("--forbidden-path", action="append", default=[], help="File or directory path that must not be read or processed; repeatable / 禁止读取或处理的文件或目录路径；可重复")
    parser.add_argument("--forbidden-tag", action="append", default=[], help="Frontmatter tag that must not be processed; repeatable; default includes PII / 禁止处理的 frontmatter tag；可重复；默认包含 PII")
    parser.add_argument("--delete", action="store_true", help="Preview decision=0 rows / 预览 decision=0 的行；仅使用 --execute 才移入 Trash")
    parser.add_argument("--rollback", action="store_true", help="Preview restore from trash-execution-log.md / 从 trash-execution-log.md 预演恢复；仅使用 --execute 才恢复")
    parser.add_argument("--second-brain-coverage", action="store_true", help="Write second-brain-coverage.md without moving files / 生成 second-brain-coverage.md，但不移动文件")
    parser.add_argument("--second-brain-index", type=Path, default=None, help="documents.jsonl path; defaults to an override or nested sibling SecondBrain / documents.jsonl 路径；默认使用覆盖值或相邻嵌套 SecondBrain")
    parser.add_argument("--vault-root", type=Path, default=None, help="Vault root for SecondBrain coverage; defaults to the review-dir parent / SecondBrain coverage 的 vault root；默认为 review-dir 父目录")
    parser.add_argument("--force-delete-path-contains", action="append", default=[], help="Force rows matching this exact relative path component; repeatable / 强制处理匹配该完整相对路径组件的行；可重复")
    parser.add_argument("--trash-dir", type=Path, default=None, help="Portable Trash directory override / 可移植 Trash 目录覆盖")
    parser.add_argument("--trash-adapter", choices=("portable", "macos"), default="portable", help="Trash location adapter; macos must be selected explicitly / Trash 位置 adapter；macos 必须显式选择")
    parser.add_argument("--execute", action="store_true", help="Perform delete or rollback mutations / 执行删除或回退变更；缺少该 flag 时仅预演")
    parser.add_argument("--dry-run", action="store_true", help="Explicit preview alias retained for compatibility / 为兼容保留的显式预演别名")
    args = parser.parse_args()

    review_dir = Path(args.review_dir).expanduser().resolve(strict=False)
    forbidden_paths = parse_roots(args.forbidden_path)
    forbidden_tags = parse_forbidden_tags(args.forbidden_tag)

    if args.execute and args.dry_run:
        parser.error("--execute and --dry-run cannot be used together / --execute 与 --dry-run 不能同时使用")
    if (args.delete or args.rollback) and args.review_root is None:
        parser.error("--review-root is required with --delete or --rollback / 使用 --delete 或 --rollback 时必须提供 --review-root")
    review_root = args.review_root.expanduser().resolve(strict=False) if args.review_root else None

    try:
        if args.delete:
            assert review_root is not None
            execute_delete(
                review_dir=review_dir,
                review_root=review_root,
                forbidden_paths=forbidden_paths,
                forbidden_tags=forbidden_tags,
                force_delete_path_contains=args.force_delete_path_contains,
                trash_dir=args.trash_dir,
                trash_adapter=args.trash_adapter,
                execute=args.execute,
            )
        if args.rollback:
            assert review_root is not None
            rollback_delete(
                review_dir=review_dir,
                review_root=review_root,
                trash_dir=args.trash_dir,
                trash_adapter=args.trash_adapter,
                execute=args.execute,
            )
        if args.second_brain_coverage:
            write_second_brain_coverage_report(
                review_dir,
                args.second_brain_index,
                args.vault_root,
            )
    except ValueError as error:
        parser.error(str(error))
    if not args.delete and not args.rollback and not args.second_brain_coverage:
        all_rows = read_all_review_rows(review_dir)
        counts = {"1": 0, "0": 0, "review": 0}
        invalid = 0
        for row in all_rows:
            action = decision_action(row.get("decision", ""))
            if action == "keep":
                counts["1"] += 1
            elif action == "delete":
                counts["0"] += 1
            elif action == "review":
                counts["review"] += 1
            else:
                invalid += 1
        print(" ".join(f"{key}={value}" for key, value in counts.items()) + f" invalid={invalid}")


if __name__ == "__main__":
    main()
