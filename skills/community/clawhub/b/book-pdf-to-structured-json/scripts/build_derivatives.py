#!/usr/bin/env python3
"""Build deterministic TXT/TSV derivatives from canonical book-tree JSON.

The canonical JSON is never modified. Existing derivative targets are replaced
only when --replace is supplied.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


REQUIRED_BOOK_FIELDS = ("book_id", "title", "authority", "node_count", "nodes")


def natural_key(path: Path) -> list[Any]:
    return [int(piece) if piece.isdigit() else piece for piece in re.split(r"(\d+)", path.name)]


def collect_tree_paths(inputs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for item in inputs:
        if item.is_dir():
            paths.extend(sorted(item.glob("*_tree.json"), key=natural_key))
        elif item.is_file():
            paths.append(item)
        else:
            raise ValueError(f"input does not exist: {item}")
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    if not unique:
        raise ValueError("no canonical *_tree.json files found")
    return unique


def load_tree(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top level must be an object")
    missing = [field for field in REQUIRED_BOOK_FIELDS if field not in data]
    if missing:
        raise ValueError(f"{path}: missing book fields: {', '.join(missing)}")
    if not isinstance(data["nodes"], list):
        raise ValueError(f"{path}: nodes must be a list")
    return data


def prefix_for(path: Path) -> str:
    suffix = "_tree.json"
    return path.name[: -len(suffix)] if path.name.endswith(suffix) else path.stem


def clean_cell(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\t", " ").replace("\r", " ").replace("\n", " ")


def safe_title(value: Any, limit: int = 80) -> str:
    title = str(value or "untitled").strip()
    title = re.sub(r"[\\/:*?\"<>|\x00-\x1f]", "_", title)
    title = re.sub(r"\s+", " ", title).strip(" .")
    return (title or "untitled")[:limit]


def ordered_nodes(tree: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(tree["nodes"], key=lambda node: (int(node.get("sort", 0)), str(node.get("key", ""))))


def render_derivatives(tree: dict[str, Any], prefix: str) -> dict[Path, str]:
    nodes = ordered_nodes(tree)
    rendered: dict[Path, str] = {}

    tsv_rows = ["序号\t层级\t类型\t父节点\t原书页码\t来源页码\t标题"]
    tree_rows: list[str] = []
    all_rows: list[str] = []
    for index, node in enumerate(nodes, start=1):
        title = str(node.get("title", "")).strip()
        level = int(node.get("level", 0))
        logical_page = node.get("logical_page")
        source_page = node.get("source_page")
        tsv_rows.append(
            "\t".join(
                clean_cell(value)
                for value in (
                    node.get("sort"),
                    level,
                    node.get("kind", ""),
                    node.get("parent_key"),
                    logical_page,
                    source_page,
                    title,
                )
            )
        )
        page_label = f"  [原书P{logical_page}]" if logical_page is not None else ""
        tree_rows.append(f"{'  ' * max(0, level - 1)}- {title}{page_label}")

        metadata = [f"层级：{level}"]
        if logical_page is not None:
            metadata.append(f"原书页码：{logical_page}")
        if source_page is not None:
            metadata.append(f"来源页码：{source_page}")
        content = str(node.get("content", ""))
        all_rows.append(f"## {title}\n{'  '.join(metadata)}\n\n{content}")

        chapter_name = f"{index:03d}_L{level}_{safe_title(title)}.txt"
        rendered[Path(f"{prefix}_chapters") / chapter_name] = content.rstrip("\n") + "\n"

    rendered[Path(f"{prefix}_tree.tsv")] = "\n".join(tsv_rows) + "\n"
    rendered[Path(f"{prefix}_tree.txt")] = "\n".join(tree_rows) + "\n"
    rendered[Path(f"{prefix}_all-content.txt")] = "\n\n".join(all_rows) + "\n"
    return rendered


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def build_one(source: Path, output_dir: Path, replace: bool) -> tuple[str, int, int]:
    tree = load_tree(source)
    prefix = prefix_for(source)
    rendered = render_derivatives(tree, prefix)
    canonical_target = output_dir / f"{prefix}_tree.json"
    targets = [canonical_target, *(output_dir / relative for relative in rendered)]
    existing = [path for path in targets if path.exists()]
    if existing and not replace:
        raise ValueError(
            f"{prefix}: derivative targets already exist; rerun with --replace after confirming the output directory"
        )

    chapter_dir = output_dir / f"{prefix}_chapters"
    if replace and chapter_dir.exists():
        shutil.rmtree(chapter_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    if source.resolve() != canonical_target.resolve():
        atomic_write(canonical_target, source.read_text(encoding="utf-8-sig"))
    for relative, text in rendered.items():
        atomic_write(output_dir / relative, text)
    return str(tree["book_id"]), len(tree["nodes"]), len(rendered)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trees", nargs="+", type=Path, help="canonical *_tree.json files or directories")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--replace", action="store_true", help="replace only the known derivative targets")
    args = parser.parse_args()

    try:
        paths = collect_tree_paths(args.trees)
        total_nodes = 0
        for path in paths:
            book_id, node_count, file_count = build_one(path, args.output_dir, args.replace)
            total_nodes += node_count
            print(f"OK\t{book_id}\t{node_count} nodes\t{file_count} derivatives")
        print(f"PASS\t{len(paths)} books\t{total_nodes} nodes")
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR\t{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
