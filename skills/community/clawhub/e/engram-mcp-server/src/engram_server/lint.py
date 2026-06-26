from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass(frozen=True, slots=True)
class LintMessage:
    level: Literal["error", "warning"]
    message: str
    file_path: str


def _rel_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _append_message(
    messages: list[LintMessage],
    *,
    level: Literal["error", "warning"],
    message: str,
    file_path: Path,
    root: Path,
) -> None:
    messages.append(
        LintMessage(level=level, message=message, file_path=_rel_path(file_path, root))
    )


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _parse_uses_from_frontmatter(content: str) -> list[str]:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return []

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return []

    uses: list[str] = []
    frontmatter = lines[1:end_idx]
    i = 0
    while i < len(frontmatter):
        stripped = frontmatter[i].strip()
        if stripped.startswith("uses:"):
            inline = stripped[len("uses:"):].strip()
            if inline.startswith("[") and inline.endswith("]"):
                items = [part.strip() for part in inline[1:-1].split(",")]
                uses.extend(item for item in items if item)
                return uses

            i += 1
            while i < len(frontmatter):
                entry = frontmatter[i].strip()
                if not entry:
                    i += 1
                    continue
                if entry.startswith("- "):
                    uses.append(entry[2:].strip())
                    i += 1
                    continue
                break
            return uses
        i += 1
    return uses


def _extract_index_references(content: str, section: str) -> tuple[set[str], set[str]]:
    listed_files: set[str] = set()
    nested_indexes: set[str] = set()

    for token in re.findall(r"`([^`]+)`", content):
        if not token.startswith(f"{section}/") or not token.endswith(".md"):
            continue
        if token.endswith("/_index.md"):
            nested_indexes.add(token)
        else:
            listed_files.add(token)

    ref_pattern = re.compile(rf"→\s*详见\s+({section}/[^\s`]+/_index\.md)")
    nested_indexes.update(match.group(1) for match in ref_pattern.finditer(content))
    return listed_files, nested_indexes


def _lint_index_section(
    *,
    engram_dir: Path,
    section: str,
    messages: list[LintMessage],
) -> tuple[set[str], set[str]]:
    section_dir = engram_dir / section
    listed_files: set[str] = set()
    discovered_files: set[str] = set()

    if not section_dir.is_dir():
        _append_message(
            messages,
            level="error",
            message=f"缺少目录：{section}/",
            file_path=section_dir,
            root=engram_dir,
        )
        return listed_files, discovered_files

    root_index = section_dir / "_index.md"
    if not root_index.is_file():
        _append_message(
            messages,
            level="error",
            message=f"缺少索引文件：{section}/_index.md",
            file_path=root_index,
            root=engram_dir,
        )

    queue: list[Path] = [root_index]
    queue.extend(
        sorted(
            p for p in section_dir.rglob("_index.md")
            if p != root_index
        )
    )
    visited_indexes: set[Path] = set()

    while queue:
        index_path = queue.pop(0)
        if index_path in visited_indexes:
            continue
        visited_indexes.add(index_path)

        if not index_path.is_file():
            continue

        content = _read_text(index_path)
        referenced_files, nested_indexes = _extract_index_references(content, section)

        for rel in sorted(referenced_files):
            listed_files.add(rel)
            target = engram_dir / rel
            if not target.is_file():
                _append_message(
                    messages,
                    level="error",
                    message=f"索引引用文件不存在：`{rel}`",
                    file_path=index_path,
                    root=engram_dir,
                )

        for nested_rel in sorted(nested_indexes):
            nested_path = engram_dir / nested_rel
            if not nested_path.is_file():
                _append_message(
                    messages,
                    level="error",
                    message=f"索引引用子索引不存在：{nested_rel}",
                    file_path=index_path,
                    root=engram_dir,
                )
                continue
            if nested_path not in visited_indexes:
                queue.append(nested_path)

    for path in sorted(section_dir.rglob("*.md")):
        if path.name.startswith("_index"):
            continue
        discovered_files.add(_rel_path(path, engram_dir))

    for orphan in sorted(discovered_files - listed_files):
        _append_message(
            messages,
            level="warning",
            message=f"孤儿文件：未在 {section} 索引中列出",
            file_path=engram_dir / orphan,
            root=engram_dir,
        )

    return listed_files, discovered_files


def _lint_examples_uses(
    *,
    engram_dir: Path,
    example_files: set[str],
    messages: list[LintMessage],
) -> None:
    for rel in sorted(example_files):
        path = engram_dir / rel
        content = _read_text(path)
        uses = _parse_uses_from_frontmatter(content)

        for ref in uses:
            target = (engram_dir / ref).resolve()
            try:
                target.relative_to(engram_dir)
            except ValueError:
                _append_message(
                    messages,
                    level="error",
                    message=f"uses 路径越界：{ref}",
                    file_path=path,
                    root=engram_dir,
                )
                continue

            if not target.is_file():
                _append_message(
                    messages,
                    level="error",
                    message=f"uses 引用文件不存在：{ref}",
                    file_path=path,
                    root=engram_dir,
                )


def _lint_meta(engram_dir: Path, messages: list[LintMessage]) -> dict | None:
    meta_path = engram_dir / "meta.json"
    if not meta_path.is_file():
        _append_message(
            messages,
            level="error",
            message="缺少 meta.json",
            file_path=meta_path,
            root=engram_dir,
        )
        return None

    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        _append_message(
            messages,
            level="error",
            message="meta.json 不是合法 JSON",
            file_path=meta_path,
            root=engram_dir,
        )
        return None

    if not meta.get("name"):
        _append_message(
            messages,
            level="error",
            message="meta.json 缺少 name 字段",
            file_path=meta_path,
            root=engram_dir,
        )
    if not meta.get("description"):
        _append_message(
            messages,
            level="error",
            message="meta.json 缺少 description 字段",
            file_path=meta_path,
            root=engram_dir,
        )

    parent = meta.get("extends")
    if isinstance(parent, str) and parent.strip():
        parent_dir = engram_dir.parent / parent
        if not parent_dir.is_dir():
            _append_message(
                messages,
                level="error",
                message=f"extends 引用的父 Engram 不存在：{parent}",
                file_path=meta_path,
                root=engram_dir,
            )

    return meta


def lint_engram(pack_dir: str | Path) -> list[LintMessage]:
    engram_dir = Path(pack_dir).expanduser().resolve()
    messages: list[LintMessage] = []

    if not engram_dir.is_dir():
        messages.append(
            LintMessage(level="error", message="Engram 目录不存在", file_path=str(pack_dir))
        )
        return messages

    _lint_meta(engram_dir, messages)

    role_path = engram_dir / "role.md"
    if not role_path.is_file():
        _append_message(
            messages,
            level="error",
            message="缺少最小必需文件 role.md",
            file_path=role_path,
            root=engram_dir,
        )

    _, knowledge_files = _lint_index_section(
        engram_dir=engram_dir,
        section="knowledge",
        messages=messages,
    )
    _, example_files = _lint_index_section(
        engram_dir=engram_dir,
        section="examples",
        messages=messages,
    )

    _lint_examples_uses(
        engram_dir=engram_dir,
        example_files=example_files,
        messages=messages,
    )

    for rel in sorted(knowledge_files):
        path = engram_dir / rel
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size == 0:
            _append_message(
                messages,
                level="warning",
                message="知识文件为空（0 字节）",
                file_path=path,
                root=engram_dir,
            )

    return messages
