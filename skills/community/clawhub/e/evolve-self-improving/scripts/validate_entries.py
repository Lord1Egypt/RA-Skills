#!/usr/bin/env python3
"""只读校验 knowledge/experience 条目，并确定性渲染目录 INDEX.md。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = ("id", "title", "scope", "tags", "learned_at", "source")
OPTIONAL_FIELDS = ("supersedes",)
RECURRENCE_SIGNALS = {"correction", "feature-request", "knowledge-gap", "error"}
TARGET_DIRECTORIES = (
    "knowledge/current",
    "knowledge/archive",
    "experience/current",
    "experience/archive",
)
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
FENCE_RE = re.compile(r"(?m)^\s*(```+|~~~+).*$")
LINK_RE = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
LINE_PREFIX_RE = re.compile(r"(?m)^\s{0,3}(?:#{1,6}\s+|>\s*|[-+*]\s+|\d+[.)]\s+)")
CONTROL_RE = re.compile(r"[`*_~]")


def configure_utf8() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


@dataclass(frozen=True)
class Failure:
    code: str
    path: str
    expected: Any
    actual: Any
    remediation: str


@dataclass(frozen=True)
class Entry:
    path: Path
    metadata: dict[str, Any]
    body: str
    effective_text: str


def failure(code: str, path: Path, expected: Any, actual: Any, remediation: str) -> Failure:
    return Failure(code, str(path), expected, actual, remediation)


def strict_text(path: Path) -> tuple[str | None, list[Failure]]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        return None, [failure("E_READ", path, "readable file", str(exc), "修复读取条件后重试，不覆盖原文件。")]
    failures: list[Failure] = []
    if data.startswith(b"\xef\xbb\xbf"):
        failures.append(failure("E_BOM", path, "UTF-8 without BOM", "BOM", "移除 BOM 后重验。"))
    try:
        text = data.decode("utf-8-sig" if data.startswith(b"\xef\xbb\xbf") else "utf-8")
    except UnicodeDecodeError as exc:
        return None, failures + [failure("E_ENCODING", path, "strict UTF-8", str(exc), "转换为严格 UTF-8 后重验。")]
    trailing = [i for i, line in enumerate(text.splitlines(), 1) if line.endswith((" ", "\t"))]
    if trailing:
        failures.append(failure("E_TRAILING", path, [], trailing, "移除行尾空白后重验。"))
    return text, failures


def split_document(path: Path, text: str) -> tuple[dict[str, Any] | None, str, list[Failure]]:
    lines = text.splitlines()
    delimiters = [i for i, line in enumerate(lines) if line == "---"]
    if len(delimiters) < 2 or delimiters[0] != 0:
        return None, "", [failure("E_FRONTMATTER", path, "two --- delimiters", delimiters, "补齐合法 frontmatter。")]
    metadata, failures = parse_frontmatter(path, lines[1 : delimiters[1]])
    body = "\n".join(lines[delimiters[1] + 1 :]).strip("\n") + "\n"
    return metadata, body, failures


def parse_frontmatter(path: Path, lines: list[str]) -> tuple[dict[str, Any], list[Failure]]:
    result: dict[str, Any] = {}
    failures: list[Failure] = []
    active_list: str | None = None
    for line in lines:
        if active_list and re.match(r"^\s+-\s+", line):
            result[active_list].append(unquote(re.sub(r"^\s+-\s+", "", line).strip()))
            continue
        match = re.match(r"^([a-z_]+):(?:\s*(.*))?$", line)
        if not match:
            failures.append(failure("E_FRONTMATTER_LINE", path, "key: value or list item", line, "修正该 frontmatter 行。"))
            active_list = None
            continue
        key, raw = match.group(1), (match.group(2) or "").strip()
        if key in result:
            failures.append(failure("E_FIELD_DUPLICATE", path, "unique field", key, "删除重复字段。"))
        if raw:
            if raw.startswith("[") and raw.endswith("]"):
                result[key] = [unquote(value.strip()) for value in raw[1:-1].split(",") if value.strip()]
            else:
                result[key] = unquote(raw)
            active_list = None
        else:
            result[key] = []
            active_list = key
    return result, failures


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def effective_text(body: str) -> str:
    text = FENCE_RE.sub("", body)
    text = LINK_RE.sub(lambda match: match.group(1), text)
    text = LINE_PREFIX_RE.sub("", text)
    text = CONTROL_RE.sub("", text)
    return "".join(char for char in text if not char.isspace())


def first_summary(body: str) -> str:
    paragraphs: list[str] = []
    current: list[str] = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        if re.match(r"^(?:#{1,6}\s+|```|~~~)", line):
            continue
        current.append(re.sub(r"^(?:>\s*|[-+*]\s+|\d+[.)]\s+)", "", line))
    if current:
        paragraphs.append(" ".join(current))
    summary = effective_text(paragraphs[0] if paragraphs else "")
    return summary[:88]


def load_entry(path: Path, enforce_length: bool = True) -> tuple[Entry | None, list[Failure]]:
    text, failures = strict_text(path)
    if text is None:
        return None, failures
    metadata, body, parse_failures = split_document(path, text)
    failures.extend(parse_failures)
    if metadata is None:
        return None, failures
    allowed = set(REQUIRED_FIELDS + OPTIONAL_FIELDS)
    actual_fields = set(metadata)
    if not set(REQUIRED_FIELDS).issubset(actual_fields) or not actual_fields.issubset(allowed):
        failures.append(failure("E_FIELDS", path, {"required": REQUIRED_FIELDS, "optional": OPTIONAL_FIELDS}, sorted(actual_fields), "只保留六个必填字段及可选 supersedes。"))
        if not set(REQUIRED_FIELDS).issubset(actual_fields):
            return None, failures
    entry_id = metadata.get("id")
    if entry_id != path.stem:
        failures.append(failure("E_ID_FILENAME", path, path.stem, entry_id, "让 id 与文件名一致。"))
    expected_prefix = "k-" if "knowledge" in path.parts else "e-" if "experience" in path.parts else None
    if expected_prefix and (not isinstance(entry_id, str) or not entry_id.startswith(expected_prefix)):
        failures.append(failure("E_ID_PREFIX", path, expected_prefix, entry_id, "按认知类型修正 id 前缀。"))
    if not DATE_RE.fullmatch(str(metadata.get("learned_at", ""))):
        failures.append(failure("E_DATE", path, "YYYY-MM-DD", metadata.get("learned_at"), "修正 learned_at。"))
    if not isinstance(metadata.get("tags"), list) or not metadata.get("tags"):
        failures.append(failure("E_TAGS", path, "non-empty inline list", metadata.get("tags"), "写入非空 tags 列表。"))
    source = metadata.get("source")
    source_values = source if isinstance(source, list) else [source]
    if not source_values or any(not isinstance(value, str) or not value.strip() for value in source_values):
        failures.append(failure("E_SOURCE", path, "non-empty source or source list", source, "保留可回查的非空来源。"))
    else:
        for value in source_values:
            if value.startswith("file:"):
                source_path = Path(value[5:])
                if not source_path.is_absolute() or not source_path.is_file():
                    failures.append(failure("E_SOURCE_PATH", path, "existing absolute file source", value, "回查并修正 file source；不要猜路径。"))
            elif value != "human-confirmation" and not value.startswith(("conversation:", "command:")):
                failures.append(failure("E_SOURCE_KIND", path, "file:/conversation:/command:/human-confirmation", value, "使用受支持且可追溯的 source。"))
    compact = effective_text(body)
    if enforce_length and not 300 <= len(compact) <= 400:
        failures.append(failure("E_BODY_LENGTH", path, "300..400 Unicode code points", len(compact), "依据原证据扩充或压缩正文，不得机械凑字。"))
    summary = first_summary(body)
    if not summary:
        failures.append(failure("E_SUMMARY_EMPTY", path, "content-specific first summary", "", "让正文首个概括表达条目特异内容。"))
    return Entry(path, metadata, body, compact), failures


def display_source(value: Any) -> str:
    values = value if isinstance(value, list) else [value]
    shown: list[str] = []
    for item in values:
        text = str(item)
        if text.startswith("file:"):
            normalized = text[5:].replace("\\", "/")
            parts = [part for part in normalized.split("/") if part]
            suffix = parts[-3:] if len(parts) >= 3 and parts[-2:] == [".git", "config"] else parts[-2:]
            shown.append("file:" + "/".join(suffix))
        elif text.startswith("command:"):
            shown.append(text[:56])
        else:
            shown.append(text[:56])
    return "<br>".join(shown)


def load_recurrences(root: Path, known_ids: set[str]) -> tuple[dict[str, list[dict[str, str]]], list[Failure]]:
    directory = root / "recurrence"
    if not directory.exists():
        return {}, []
    if not directory.is_dir():
        return {}, [failure("E_RECURRENCE_DIRECTORY", directory, "directory", "not a directory", "恢复 recurrence 目录后重验。")]
    records: dict[str, list[dict[str, str]]] = {}
    failures: list[Failure] = []
    expected_header = "| observed_at | source | scope | signal | summary |"
    expected_rule = "|---|---|---|---|---|"
    for path in sorted(directory.glob("*.md")):
        text, item_failures = strict_text(path)
        failures.extend(item_failures)
        if text is None:
            continue
        entry_id = path.stem
        if entry_id not in known_ids:
            failures.append(failure("E_RECURRENCE_ORPHAN", path, "existing knowledge/experience id", entry_id, "删除孤儿记录或恢复对应条目。"))
        lines = text.splitlines()
        if len(lines) < 5 or lines[0] != f"# {entry_id} 复现记录" or lines[2] != expected_header or lines[3] != expected_rule:
            failures.append(failure("E_RECURRENCE_FORMAT", path, "title + fixed five-column table", lines[:4], "按 Skill 的复现表格格式修正。"))
            continue
        seen_sources: set[str] = set()
        rows: list[dict[str, str]] = []
        for number, line in enumerate(lines[4:], 5):
            if not line.strip():
                continue
            cells = [value.strip() for value in line.strip().strip("|").split("|")]
            if len(cells) != 5:
                failures.append(failure("E_RECURRENCE_ROW", path, "five cells", {"line": number, "value": line}, "修正该证据行。"))
                continue
            observed_at, source, scope, signal, summary = cells
            if not DATE_RE.fullmatch(observed_at):
                failures.append(failure("E_RECURRENCE_DATE", path, "YYYY-MM-DD", observed_at, "修正复现日期。"))
            if not source or source in seen_sources:
                failures.append(failure("E_RECURRENCE_SOURCE", path, "unique non-empty source", source, "移除重复来源或补充新的独立来源。"))
            elif source.startswith("file:"):
                source_path = Path(source[5:])
                if not source_path.is_absolute() or not source_path.is_file():
                    failures.append(failure("E_RECURRENCE_SOURCE_PATH", path, "existing absolute file source", source, "回查并修正复现来源；不要猜路径。"))
            elif not source.startswith(("conversation:", "command:")) and source != "human-confirmation":
                failures.append(failure("E_RECURRENCE_SOURCE_KIND", path, "traceable source", source, "使用 file:/conversation:/command:/human-confirmation 来源。"))
            seen_sources.add(source)
            if not scope or not summary:
                failures.append(failure("E_RECURRENCE_CONTENT", path, "non-empty scope and summary", cells, "补齐适用范围和特异概括。"))
            if signal not in RECURRENCE_SIGNALS:
                failures.append(failure("E_RECURRENCE_SIGNAL", path, sorted(RECURRENCE_SIGNALS), signal, "使用四类学习信号之一。"))
            rows.append({"observed_at": observed_at, "source": source, "scope": scope, "signal": signal, "summary": summary})
        if not rows:
            failures.append(failure("E_RECURRENCE_EMPTY", path, "at least one evidence row", 0, "没有复现时删除该文件。"))
        records[entry_id] = rows
    return records, failures


def cell(value: Any) -> str:
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value)
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def recurrence_label(records: list[dict[str, str]]) -> str:
    if not records:
        return "0"
    return f"{len(records)}（最近 {max(item['observed_at'] for item in records)}）"


def render_index(directory: Path, entries: list[Entry], recurrences: dict[str, list[dict[str, str]]] | None = None) -> str:
    kind = "知识" if "knowledge" in directory.parts else "经验"
    state = "当前" if directory.name == "current" else "归档"
    lines = [
        f"# {state}{kind}导航",
        "",
        "本文件只用于缩小只读检索候选；结论仍须打开条目并按来源回查。",
        "",
        "| 条目 | title | scope | tags | learned_at | source | 复现 | 特异概括 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    ordered = sorted(entries, key=lambda entry: entry.metadata["id"])
    ordered.sort(key=lambda entry: entry.metadata["learned_at"], reverse=True)
    for entry in ordered:
        meta = entry.metadata
        link = f"[{cell(meta['id'])}](./{entry.path.name})"
        lines.append(
            "| " + " | ".join(
                (
                    link,
                    cell(meta["title"]),
                    cell(meta["scope"]),
                    cell(meta["tags"]),
                    cell(meta["learned_at"]),
                    cell(display_source(meta["source"])),
                    cell(recurrence_label((recurrences or {}).get(str(meta["id"]), []))),
                    cell(first_summary(entry.body)),
                )
            ) + " |"
        )
    return "\n".join(lines) + "\n"


def read_directory(directory: Path) -> tuple[list[Entry], list[Failure]]:
    entries: list[Entry] = []
    failures: list[Failure] = []
    for path in sorted(directory.glob("*.md")):
        if path.name == "INDEX.md":
            continue
        entry, item_failures = load_entry(path)
        failures.extend(item_failures)
        if entry:
            entries.append(entry)
    return entries, failures


def report(mode: str, entries: list[Entry], failures: list[Failure]) -> dict[str, Any]:
    lengths = [len(entry.effective_text) for entry in entries]
    return {
        "status": "pass" if not failures else "fail",
        "mode": mode,
        "counts": {
            "entries": len(entries),
            "failures": len(failures),
            "min_effective_chars": min(lengths) if lengths else None,
            "max_effective_chars": max(lengths) if lengths else None,
        },
        "failures": [asdict(item) for item in failures],
    }


def command_check_root(root: Path) -> tuple[dict[str, Any], int]:
    entries: list[Entry] = []
    failures: list[Failure] = []
    per_directory: dict[str, int] = {}
    for relative in TARGET_DIRECTORIES:
        directory = root / relative
        if not directory.is_dir():
            failures.append(failure("E_DIRECTORY", directory, "existing directory", "missing", "补齐认知目录。"))
            continue
        found, item_failures = read_directory(directory)
        entries.extend(found)
        failures.extend(item_failures)
        per_directory[relative] = len(found)
    recurrences, recurrence_failures = load_recurrences(root, {str(entry.metadata["id"]) for entry in entries})
    failures.extend(recurrence_failures)
    for relative in TARGET_DIRECTORIES:
        directory = root / relative
        if not directory.is_dir():
            continue
        directory_entries = [entry for entry in entries if entry.path.parent == directory]
        index_path = directory / "INDEX.md"
        actual, index_failures = strict_text(index_path)
        failures.extend(index_failures)
        if actual is not None:
            expected = render_index(directory, directory_entries, recurrences)
            if actual != expected:
                failures.append(failure("E_INDEX_MISMATCH", index_path, expected, actual, "用 render-index 原子重建并读回该目录索引。"))
    result = report("root", entries, failures)
    result["counts"]["directories"] = per_directory
    result["counts"]["recurrence_files"] = len(recurrences)
    result["counts"]["recurrences"] = sum(len(items) for items in recurrences.values())
    return result, 0 if not failures else 1


def command_check_file(path: Path) -> tuple[dict[str, Any], int]:
    entry, failures = load_entry(path)
    entries = [entry] if entry else []
    result = report("file", entries, failures)
    return result, 0 if not failures else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check")
    target = check.add_mutually_exclusive_group(required=True)
    target.add_argument("--root", type=Path)
    target.add_argument("--file", type=Path)
    check.add_argument("--json", action="store_true")
    render = subparsers.add_parser("render-index")
    render.add_argument("--directory", type=Path, required=True)
    return parser


def main() -> int:
    configure_utf8()
    args = build_parser().parse_args()
    if args.command == "render-index":
        entries: list[Entry] = []
        failures: list[Failure] = []
        for path in sorted(args.directory.glob("*.md")):
            if path.name == "INDEX.md":
                continue
            entry, item_failures = load_entry(path)
            failures.extend(item_failures)
            if entry:
                entries.append(entry)
        root = args.directory.parent.parent
        known_ids: set[str] = set()
        for relative in TARGET_DIRECTORIES:
            for path in (root / relative).glob("*.md"):
                if path.name != "INDEX.md":
                    known_ids.add(path.stem)
        recurrences, recurrence_failures = load_recurrences(root, known_ids)
        failures.extend(recurrence_failures)
        if failures:
            print(json.dumps(report("render-index", entries, failures), ensure_ascii=False, indent=2), file=sys.stderr)
            return 1
        sys.stdout.write(render_index(args.directory, entries, recurrences))
        return 0
    result, code = command_check_root(args.root) if args.root else command_check_file(args.file)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status={result['status']} entries={result['counts']['entries']} failures={result['counts']['failures']}")
        for item in result["failures"]:
            print(f"{item['code']} {item['path']}: actual={item['actual']}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
