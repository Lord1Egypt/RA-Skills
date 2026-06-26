#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
import zipfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a Markdown outline into an XMind file.")
    parser.add_argument("--outline", required=True, help="Markdown outline file")
    parser.add_argument("--output", required=True, help="Target .xmind file path")
    return parser.parse_args()


def clean_line(text: str) -> str:
    return text.rstrip().replace("\t", "    ")


def strip_bullet(text: str) -> str:
    return re.sub(r"^[-*+]\s+", "", text).strip()


def count_indent(text: str) -> int:
    expanded = text.replace("\t", "    ")
    return len(expanded) - len(expanded.lstrip(" "))


def new_topic(title: str) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "title": title.strip() or "(empty)",
        "style": {"id": str(uuid.uuid4()), "properties": {}},
    }


def add_child(parent: dict, child: dict) -> None:
    children = parent.setdefault("children", {})
    attached = children.setdefault("attached", [])
    attached.append(child)


def parse_outline(text: str) -> tuple[str, list[dict]]:
    root_title = "Mind Map"
    lines = [clean_line(line) for line in text.splitlines()]
    bullet_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# ") and root_title == "Mind Map":
            root_title = stripped[2:].strip() or root_title
            continue
        if re.match(r"^\s*[-*+]\s+", line):
            bullet_lines.append(line)

    roots: list[dict] = []
    stack: list[tuple[int, dict]] = []

    for line in bullet_lines:
        indent = count_indent(line)
        topic = new_topic(strip_bullet(line.lstrip()))

        while stack and indent <= stack[-1][0]:
            stack.pop()

        if stack:
            add_child(stack[-1][1], topic)
        else:
            roots.append(topic)

        stack.append((indent, topic))

    return root_title, roots


def build_xmind_json(root_title: str, branches: list[dict]) -> list[dict]:
    root_topic = new_topic(root_title)
    for branch in branches:
        add_child(root_topic, branch)
    return [
        {
            "id": str(uuid.uuid4()),
            "title": "Sheet 1",
            "rootTopic": root_topic,
            "style": {"id": str(uuid.uuid4()), "properties": {}},
            "topicPositioning": "fixed",
        }
    ]


def format_for_console(value: str) -> str:
    encoding = (getattr(sys.stdout, "encoding", None) or "").lower()
    if "utf" in encoding:
        return value
    return value.encode("unicode_escape").decode("ascii")


def write_xmind(output: Path, content: list[dict]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    metadata = {}
    manifest = {"file-entries": {"content.json": {}, "metadata.json": {}}}
    content_xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><xmap-content/>"

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("content.json", json.dumps(content, ensure_ascii=False, separators=(",", ":")))
        archive.writestr("metadata.json", json.dumps(metadata, ensure_ascii=False))
        archive.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, separators=(",", ":")))
        archive.writestr("content.xml", content_xml)


def main() -> int:
    args = parse_args()
    outline = Path(args.outline).resolve()
    output = Path(args.output).resolve()

    if not outline.exists():
        raise SystemExit(f"Outline file not found: {outline}")

    raw = outline.read_text(encoding="utf-8", errors="replace")
    root_title, branches = parse_outline(raw)
    write_xmind(output, build_xmind_json(root_title, branches))
    print(f"XMind file saved: {format_for_console(str(output))}")
    print(f'   Root: "{format_for_console(root_title)}"')
    print(f"   Branches: {len(branches)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
