#!/usr/bin/env python3
"""Validate a topic or the whole knowledge base."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

from clawexpert_common import count_formal_nodes, count_source_files, knowledge_dir, read_text


LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def iter_topics(kb: pathlib.Path, slug: str | None) -> list[pathlib.Path]:
    if slug:
        return [kb / slug]
    return [child for child in sorted(kb.iterdir()) if child.is_dir() and not child.name.startswith("_") and (child / "meta.json").exists()]


def validate_links(path: pathlib.Path) -> list[str]:
    issues = []
    for _label, target in LINK_RE.findall(read_text(path)):
        if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            issues.append(f"broken link in {path}: {target}")
    return issues


def validate_topic(topic_root: pathlib.Path) -> list[str]:
    issues = []
    meta_file = topic_root / "meta.json"
    if not meta_file.exists():
        return [f"missing meta.json: {topic_root}"]

    meta = json.loads(read_text(meta_file))
    actual_sources = count_source_files(topic_root)
    actual_nodes = count_formal_nodes(topic_root)

    if meta.get("source_count") != actual_sources:
        issues.append(
            f"{topic_root.name}: source_count mismatch meta={meta.get('source_count')} actual={actual_sources}"
        )
    if meta.get("node_count") != actual_nodes:
        issues.append(
            f"{topic_root.name}: node_count mismatch meta={meta.get('node_count')} actual={actual_nodes}"
        )

    topic_index = topic_root / "index.md"
    if not topic_index.exists():
        issues.append(f"{topic_root.name}: missing index.md")
    else:
        issues.extend(validate_links(topic_index))

    for node in sorted((topic_root / "nodes").glob("node-*.md")):
        issues.extend(validate_links(node))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb")
    parser.add_argument("--slug")
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    issues = []
    for topic_root in iter_topics(kb, args.slug):
        if topic_root.exists():
            issues.extend(validate_topic(topic_root))
        else:
            issues.append(f"missing topic directory: {topic_root}")

    root_index = kb / "_index" / "_root_index.md"
    if not root_index.exists():
        issues.append(f"missing root index: {root_index}")

    payload = {"ok": not issues, "issues": issues}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
