#!/usr/bin/env python3
"""Rebuild the `_index/` tree from learned topics."""

from __future__ import annotations

import argparse
import json
import pathlib
from collections import defaultdict

from clawexpert_common import (
    best_label,
    count_formal_nodes,
    count_source_files,
    extract_bullets,
    extract_section,
    first_paragraph,
    first_sentence,
    frontmatter_aliases,
    knowledge_dir,
    list_formal_nodes,
    meta_path,
    parse_frontmatter_and_body,
    read_text,
    relpath,
    write_text,
)


def topic_dirs(kb: pathlib.Path) -> list[pathlib.Path]:
    dirs: list[pathlib.Path] = []
    for child in sorted(kb.iterdir()):
        if not child.is_dir() or child.name.startswith("_"):
            continue
        if (child / "meta.json").exists():
            dirs.append(child)
    return dirs


def topic_record(topic_root: pathlib.Path) -> dict | None:
    meta = json.loads(read_text(topic_root / "meta.json"))
    if meta.get("status") not in {"complete", "partial"}:
        return None

    topic_index = topic_root / "index.md"
    index_text = read_text(topic_index) if topic_index.exists() else ""
    findings = extract_bullets(extract_section(index_text, "Core Findings Summary"))
    questions = extract_bullets(extract_section(index_text, "Further Directions"))

    nodes = []
    for node_path in list_formal_nodes(topic_root):
        frontmatter, body = parse_frontmatter_and_body(read_text(node_path))
        label = best_label(frontmatter, body, node_path.stem)
        summary = first_sentence(extract_section(body, "Summary") or first_paragraph(body))
        nodes.append(
            {
                "path": node_path,
                "label": label,
                "summary": summary,
                "aliases": frontmatter_aliases(frontmatter),
                "canonical_intent": frontmatter.get("canonical_intent", "").strip(),
            }
        )

    sources = []
    for source_path in sorted((topic_root / "raw" / "web").glob("*.md")):
        frontmatter, body = parse_frontmatter_and_body(read_text(source_path))
        title = frontmatter.get("title") or source_path.stem
        abstract = first_sentence(first_paragraph(body))
        sources.append({"path": source_path, "title": title, "abstract": abstract})
    for source_path in sorted((topic_root / "raw" / "pdf").glob("*.md")):
        frontmatter, body = parse_frontmatter_and_body(read_text(source_path))
        title = frontmatter.get("title") or source_path.stem
        abstract = first_sentence(first_paragraph(body))
        sources.append({"path": source_path, "title": title, "abstract": abstract})
    for source_path in sorted((topic_root / "raw" / "pdf").glob("*/_index.md")):
        frontmatter, body = parse_frontmatter_and_body(read_text(source_path))
        title = frontmatter.get("title") or source_path.parent.name
        abstract = first_sentence(first_paragraph(body))
        sources.append({"path": source_path, "title": title, "abstract": abstract})

    core_summary = ""
    if findings:
        core_summary = " ".join(findings[:3])
    elif nodes:
        core_summary = " ".join(filter(None, [node["summary"] for node in nodes[:2]]))

    idx_meta = meta.get("index_categories", {})
    l1 = idx_meta.get("l1") or "uncategorized"
    l1_label = idx_meta.get("l1_label") or "Uncategorized"
    l2_values = []
    for sub_meta in (idx_meta.get("subtopics") or {}).values():
        l2 = sub_meta.get("l2")
        if l2 and l2 not in l2_values:
            l2_values.append(l2)
    if not l2_values:
        l2_values = ["General"]

    return {
        "topic": meta.get("topic", topic_root.name),
        "slug": meta.get("slug", topic_root.name),
        "root": topic_root,
        "source_count": meta.get("source_count", count_source_files(topic_root)),
        "node_count": meta.get("node_count", count_formal_nodes(topic_root)),
        "updated": (meta.get("last_updated") or meta.get("created") or "")[:10],
        "l1": l1,
        "l1_label": l1_label,
        "l2_values": l2_values,
        "core_summary": core_summary.strip(),
        "findings": findings[:8],
        "questions": questions,
        "nodes": nodes,
        "sources": sources[:12],
    }


def build_category_index(l2: str, records: list[dict], out_path: pathlib.Path) -> None:
    lines = [
        f"# {l2}",
        "",
        f"> {len(records)} topics | {sum(int(r['source_count']) for r in records)} total sources | Last updated: {max((r['updated'] for r in records), default='')}",
        "",
        "---",
        "",
    ]
    for record in records:
        lines.append(f"## {record['topic']} (`{record['slug']}`)")
        lines.append("")
        lines.append(f"> Learned: {record['updated']} | Sources: {record['source_count']} | Nodes: {record['node_count']}")
        lines.append("")
        lines.append("### Core Summary")
        lines.append(record["core_summary"] or "Summary pending.")
        lines.append("")
        lines.append("### Key Conclusions")
        findings = record["findings"] or ["Findings pending."]
        for item in findings[:6]:
            lines.append(f"- {item}")
        lines.append("")
        lines.append("### Knowledge Nodes")
        for node in record["nodes"][:12]:
            lines.append(f"- [{node['label']}]({relpath(node['path'], out_path.parent)}) — {node['summary'] or 'Summary pending.'}")
            hints = []
            if node.get("canonical_intent"):
                hints.append(f"canonical: {node['canonical_intent']}")
            if node.get("aliases"):
                hints.append(f"aliases: {', '.join(node['aliases'][:5])}")
            if hints:
                lines.append(f"  - Routing hints: {' | '.join(hints)}")
        if not record["nodes"]:
            lines.append("- No formal nodes yet.")
        lines.append("")
        lines.append("### Source Abstracts")
        for source in record["sources"][:10]:
            lines.append(f"- [{source['title']}]({relpath(source['path'], out_path.parent)}) — {source['abstract'] or 'Abstract pending.'}")
        if not record["sources"]:
            lines.append("- No source abstracts available.")
        lines.append("")
        lines.append("### Open Questions")
        for question in record["questions"][:8]:
            lines.append(f"- {question}")
        if not record["questions"]:
            lines.append("- None recorded.")
        lines.append("")
    write_text(out_path, "\n".join(lines).rstrip() + "\n")


def build_root_index(records: list[dict], out_path: pathlib.Path) -> None:
    grouped: dict[tuple[str, str], dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for record in records:
        key = (record["l1"], record["l1_label"])
        for l2 in record["l2_values"]:
            grouped[key][l2].append(record)

    lines = [
        "# ClawExpert Knowledge Base",
        "",
        f"> Last updated: {max((record['updated'] for record in records), default='')} | Topics: {len(records)} | Total sources: {sum(int(record['source_count']) for record in records)}",
        "",
        "## Category Directory",
        "",
    ]

    for (l1, l1_label), l2_map in sorted(grouped.items(), key=lambda item: item[0][1]):
        lines.append(f"### {l1_label} (`{l1}`)")
        lines.append("")
        for l2, l2_records in sorted(l2_map.items(), key=lambda item: item[0]):
            topic_count = len({record["slug"] for record in l2_records})
            source_count = sum(int(record["source_count"]) for record in l2_records)
            lines.append(f"#### {l2}")
            lines.append(f"→ [`_index.md`]({l1}/{l2}/_index.md) | {topic_count} topics | {source_count} sources")
            lines.append("")
            lines.append("**Topics covered:**")
            for record in sorted(l2_records, key=lambda item: item["updated"], reverse=True):
                lines.append(f"- **{record['topic']}** (`{record['slug']}`): {record['core_summary'] or 'Summary pending.'}")
                for item in (record["findings"] or [])[:3]:
                    lines.append(f"  - {item}")
            lines.append("")

    lines.append("## Recent Learning")
    for record in sorted(records, key=lambda item: item["updated"], reverse=True)[:20]:
        lines.append(
            f"- {record['updated']} **{record['topic']}** (`{record['slug']}`) → "
            f"[{record['l1_label']} / {record['l2_values'][0]}]({record['l1']}/{record['l2_values'][0]}/_index.md)"
        )
    lines.append("")
    write_text(out_path, "\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb")
    args = parser.parse_args()

    kb = knowledge_dir(args.kb)
    records = []
    for root in topic_dirs(kb):
        record = topic_record(root)
        if record:
            records.append(record)

    index_root = kb / "_index"
    index_root.mkdir(parents=True, exist_ok=True)

    grouped: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for record in records:
        for l2 in record["l2_values"]:
            grouped[(record["l1"], record["l1_label"], l2)].append(record)

    for (l1, _l1_label, l2), items in grouped.items():
        out_path = index_root / l1 / l2 / "_index.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        build_category_index(l2, sorted(items, key=lambda item: item["updated"], reverse=True), out_path)

    build_root_index(records, index_root / "_root_index.md")
    print(json.dumps({"topics": len(records), "category_indexes": len(grouped)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
