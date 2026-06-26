#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

IGNORED_NAMES = {".DS_Store"}
IGNORED_SUFFIXES = {".uploading.cfg"}
TEXT_EXTS = {".txt", ".md", ".markdown"}
DOC_EXTS = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"}


@dataclass
class ManifestItem:
    id: str
    path: str
    kind: str
    format: str
    title: str
    authority: str
    notes: str
    risk_flags: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a first-pass manifest from source files and directories."
    )
    parser.add_argument("inputs", nargs="+", help="Files or directories to scan")
    parser.add_argument("--out", help="Optional output file path")
    parser.add_argument(
        "--format",
        choices=("json", "md"),
        default="md",
        help="Manifest output format",
    )
    return parser.parse_args()


def should_skip(path: Path) -> bool:
    if path.name in IGNORED_NAMES:
        return True
    return any(path.name.endswith(suffix) for suffix in IGNORED_SUFFIXES)


def walk_inputs(inputs: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in inputs:
        path = Path(raw).expanduser()
        if not path.exists():
            continue
        if path.is_file():
            if not should_skip(path):
                files.append(path)
            continue
        for root, dirnames, filenames in os.walk(path):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
            for name in sorted(filenames):
                candidate = Path(root) / name
                if not should_skip(candidate):
                    files.append(candidate)
    return sorted(files, key=lambda item: str(item).lower())


def detect_kind(path: Path) -> str:
    name = path.name.lower()
    full = str(path).lower()
    if any(token in name for token in ("框架", "模板", "目录", "outline", "template")):
        return "outline"
    if any(token in full for token in ("/draft/", "/chapters/")):
        return "draft"
    if any(token in name for token in ("合并", "final", "output", "输出")):
        return "output"
    return "source"


def detect_authority(kind: str, path: Path) -> str:
    if path.suffix.lower() in TEXT_EXTS and "_pdftext" in str(path).lower():
        return "derived"
    if kind == "source":
        return "authoritative"
    return "working"


def detect_notes(path: Path, kind: str) -> str:
    if kind == "outline":
        return "Target structure or template candidate."
    if path.suffix.lower() == ".pdf":
        return "Likely authoritative narrative or technical source."
    if path.suffix.lower() == ".docx":
        return "Word source or extracted working document."
    if path.suffix.lower() in TEXT_EXTS:
        return "Text source or working draft for quick scanning."
    return "General project material."


def detect_risk_flags(path: Path) -> list[str]:
    flags: list[str] = []
    lowered = path.name.lower()
    if any(token in lowered for token in ("实施", "方案", "建设", "设计", "技术")):
        flags.append("scope")
    if any(token in lowered for token in ("标准", "规范", "接口")):
        flags.append("standards")
    if any(token in lowered for token in ("进度", "计划", "里程碑")):
        flags.append("schedule")
    if path.suffix.lower() in DOC_EXTS:
        flags.append("facts")
    return flags


def slugify(path: Path, index: int) -> str:
    stem = path.stem.strip() or f"file-{index}"
    cleaned = []
    for char in stem:
        if char.isalnum():
            cleaned.append(char.lower())
        elif char in {"-", "_"}:
            cleaned.append("-")
    slug = "".join(cleaned).strip("-")
    if not slug:
        slug = f"file-{index}"
    return f"{index:03d}-{slug[:40]}"


def build_items(paths: list[Path]) -> list[ManifestItem]:
    items: list[ManifestItem] = []
    for index, path in enumerate(paths, start=1):
        kind = detect_kind(path)
        items.append(
            ManifestItem(
                id=slugify(path, index),
                path=str(path),
                kind=kind,
                format=path.suffix.lower().lstrip(".") or "unknown",
                title=path.stem,
                authority=detect_authority(kind, path),
                notes=detect_notes(path, kind),
                risk_flags=detect_risk_flags(path),
            )
        )
    return items


def render_markdown(items: list[ManifestItem]) -> str:
    lines = [
        "| id | kind | authority | format | title | path | risk_flags |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            "| {id} | {kind} | {authority} | {format} | {title} | {path} | {risk_flags} |".format(
                id=item.id,
                kind=item.kind,
                authority=item.authority,
                format=item.format,
                title=item.title.replace("|", "/"),
                path=item.path.replace("|", "/"),
                risk_flags=", ".join(item.risk_flags) or "-",
            )
        )
    return "\n".join(lines) + "\n"


def emit(text: str, out: str | None) -> None:
    if out:
        Path(out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def main() -> int:
    args = parse_args()
    paths = walk_inputs(args.inputs)
    items = build_items(paths)
    if args.format == "json":
        payload = json.dumps([asdict(item) for item in items], ensure_ascii=False, indent=2)
        emit(payload + "\n", args.out)
    else:
        emit(render_markdown(items), args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
