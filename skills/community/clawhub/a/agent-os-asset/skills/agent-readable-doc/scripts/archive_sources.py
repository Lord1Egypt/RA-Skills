#!/usr/bin/env python3
"""Archive original sources after agent-readable conversion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil


ARCHIVE_DIR_NAME = "Archived"
ARCHIVED_TAG = "archived"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    for index in range(2, 1000):
        candidate = path.with_name(f"{path.stem}-{index}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Unable to find a non-overwriting archive path for {path}. / 无法为 {path} 找到不覆盖的归档路径。")


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5 :].lstrip("\n")


def parse_inline_tags(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [tag.strip().strip("'\"") for tag in value.split(",") if tag.strip()]


def frontmatter_tags(lines: list[str]) -> list[str]:
    tags: list[str] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("tags:"):
            continue
        value = stripped.split(":", 1)[1].strip()
        if value:
            tags.extend(parse_inline_tags(value))
            break
        cursor = index + 1
        while cursor < len(lines) and lines[cursor].startswith((" ", "\t")):
            item = lines[cursor].strip()
            if item.startswith("- "):
                tags.append(item[2:].strip().strip("'\""))
            cursor += 1
        break
    return [tag for tag in tags if tag]


def set_frontmatter_tags(frontmatter: str, tags: list[str]) -> str:
    lines = frontmatter.splitlines()
    output: list[str] = []
    index = 0
    replaced = False
    while index < len(lines):
        line = lines[index]
        if line.strip().startswith("tags:"):
            output.append("tags:")
            for tag in tags:
                output.append(f"  - {tag}")
            replaced = True
            index += 1
            while index < len(lines) and lines[index].startswith((" ", "\t")):
                index += 1
            continue
        output.append(line)
        index += 1
    if not replaced:
        output = ["tags:", *[f"  - {tag}" for tag in tags], *output]
    return "\n".join(output).strip() + "\n"


def add_archived_tag(path: Path) -> bool:
    if path.suffix.lower() not in {".md", ".markdown"}:
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    frontmatter, body = split_frontmatter(text)
    if frontmatter is None:
        path.write_text(f"---\ntags:\n  - {ARCHIVED_TAG}\n---\n\n{text.lstrip()}", encoding="utf-8")
        return True
    tags = frontmatter_tags(frontmatter.splitlines())
    if ARCHIVED_TAG in tags:
        return False
    new_frontmatter = set_frontmatter_tags(frontmatter, [*tags, ARCHIVED_TAG])
    path.write_text(f"---\n{new_frontmatter}---\n\n{body}", encoding="utf-8")
    return True


def archive_target(source: Path, vault_root: Path) -> Path:
    relative = source.resolve(strict=False).relative_to(vault_root.resolve(strict=False))
    return unique_path(vault_root / ARCHIVE_DIR_NAME / relative)


def obsidian_heading_link(archived_path: Path, vault_root: Path, heading: str | None = None, label: str | None = None) -> str:
    relative = archived_path.resolve(strict=False).relative_to(vault_root.resolve(strict=False))
    target = relative.as_posix()
    if heading:
        target = f"{target}#{heading}"
    return f"[[{target}|{label or target}]]"


def archive_sources(
    vault_root: Path,
    sources: list[Path],
    dry_run: bool | None = None,
    *,
    execute: bool = False,
) -> list[dict[str, object]]:
    """Plan source archival unless the caller explicitly opts into execution.

    ``dry_run`` remains accepted for older callers and reports, but passing
    ``False`` no longer authorizes file moves. Only ``execute=True`` does.
    """
    if dry_run and execute:
        raise ValueError("dry_run and execute cannot both be enabled. / dry_run 与 execute 不能同时启用。")
    root = vault_root.expanduser().resolve(strict=False)
    rows: list[dict[str, object]] = []
    for source in sources:
        resolved = source.expanduser().resolve(strict=False)
        if not resolved.is_file():
            raise ValueError(f"Source file does not exist: {source}. / 源文件不存在：{source}。")
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"Source is outside the vault root: {source}. / 源文件位于 vault 根目录之外：{source}。") from exc
        target = archive_target(resolved, root)
        tag_added = False
        if execute:
            tag_added = add_archived_tag(resolved)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(resolved), str(target))
        rows.append(
            {
                "source_path": str(resolved),
                "archived_path": str(target),
                "status": "archived" if execute else "planned",
                "archived_tag_added": tag_added,
                "obsidian_link": obsidian_heading_link(target, root),
            }
        )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Archive original sources under vault-root/Archived after conversion. / 转换后将原始来源归档到 vault-root/Archived。"
    )
    parser.add_argument("--vault-root", required=True, help="Obsidian vault root. / Obsidian vault 根目录。")
    parser.add_argument(
        "--map-output",
        default="archive-map.json",
        help="Path for the archive map JSON. / 归档映射 JSON 的写入路径。",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--execute",
        action="store_true",
        help="Execute the planned moves; without this flag the command is a dry-run. / 执行计划移动；不带此参数时仅预演。",
    )
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Deprecated compatibility flag; dry-run is already the default. / 已弃用的兼容参数；dry-run 已是默认行为。",
    )
    parser.add_argument("sources", nargs="+", help="Source files to archive. / 要归档的源文件。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = archive_sources(
        Path(args.vault_root),
        [Path(item) for item in args.sources],
        dry_run=args.dry_run,
        execute=args.execute,
    )
    output = Path(args.map_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"archives": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote archive map: {output} / 已写入归档映射：{output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
