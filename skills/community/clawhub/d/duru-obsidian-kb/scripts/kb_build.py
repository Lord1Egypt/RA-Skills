#!/usr/bin/env python3
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


def load_manifest(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fmt_list(items):
    return "\n".join(items) + ("\n" if items else "")


def concept_slug(tag: str) -> str:
    text = tag.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "untagged"


def source_page(entry):
    tags = entry.get("tags") or []
    tags_yaml = "[" + ", ".join(json.dumps(t, ensure_ascii=False) for t in tags) + "]"
    raw_path = entry.get("raw_path", "")
    source = entry.get("source", "")
    concept_links = [f"[[../concepts/{concept_slug(tag)}|{tag}]]" for tag in tags]
    body_preview = entry.get("body_preview") or ""
    repo_local_path = entry.get("repo_local_path") or ""
    pdf_local_path = entry.get("pdf_local_path") or ""
    spreadsheet_local_path = entry.get("spreadsheet_local_path") or ""
    processor = entry.get("processor") or "native"
    body = [
        "---",
        f"title: {json.dumps(entry.get('title', ''), ensure_ascii=False)}",
        f"slug: {entry.get('slug', '')}",
        f"source_type: {entry.get('source_type', '')}",
        f"source_url: {source}",
        f"ingested_at: {entry.get('ingested_at', '')}",
        f"tags: {tags_yaml}",
        f"status: {entry.get('status', '')}",
        f"extraction: {entry.get('extraction', 'none')}",
        "---",
        "",
        f"# {entry.get('title', entry.get('slug', 'Untitled'))}",
        "",
        f"- Source: {source}",
        f"- Type: {entry.get('source_type', '')}",
        f"- Ingested: {entry.get('ingested_at', '')}",
        f"- Status: {entry.get('status', '')}",
        f"- Extraction: {entry.get('extraction', 'none')}",
        f"- Prompt Shield: {entry.get('prompt_shield', {}).get('action', 'allow')} / {entry.get('prompt_shield', {}).get('severity', 'SAFE')}",
        f"- Suspicious segments: {entry.get('suspicious_segment_count', 0)}",
        f"- Processor: {processor}",
        f"- Raw file: [[../../{raw_path}]]" if raw_path else "- Raw file: missing",
        f"- Local repo: [[../../{repo_local_path}]]" if repo_local_path else None,
        f"- Local PDF: [[../../{pdf_local_path}]]" if pdf_local_path else None,
        f"- Local spreadsheet: [[../../{spreadsheet_local_path}]]" if spreadsheet_local_path else None,
        f"- Concepts: {', '.join(concept_links)}" if concept_links else "- Concepts: none",
        "",
        "## Notes",
        "",
        entry.get("notes") or "No notes yet.",
        "",
        "## Preview",
        "",
        body_preview if body_preview else "No extracted preview available.",
        "",
        "## Capabilities",
        "",
        "",
        "",
    ]
    capabilities = entry.get("capabilities") or {}
    if capabilities:
        for key, value in capabilities.items():
            body.append(f"- {key}: {value}")
    else:
        body.append("- No capability snapshot recorded.")
    body.extend([
        "",
        "## Suspicious segments",
        "",
    ])
    suspicious_segments = entry.get("suspicious_segments") or []
    if suspicious_segments:
        for item in suspicious_segments:
            body.append(f"- {item.get('severity', 'n/a')} / {item.get('action', item.get('reason', 'flag'))}: {item.get('text', '')}")
    else:
        body.append("- None recorded.")
    body.extend([
        "",
        "## Backlinks",
        "",
    ])
    if concept_links:
        body.extend([f"- Mentioned in {link}" for link in concept_links])
    else:
        body.append("- No concept backlinks yet.")
    body.extend([
        "",
        "## Extraction status",
        "",
        "Generated from manifest metadata and available extracted preview.",
        "If full text extraction is unavailable, rely on the linked raw file or source URL.",
        "",
    ])
    return "\n".join(line for line in body if line is not None)


def concept_page(tag, entries):
    slug = concept_slug(tag)
    summary = f"This topic currently groups {len(entries)} source(s) tagged '{tag}'. Expand this memo as higher-quality summaries become available."
    lines = [
        "---",
        f"title: {json.dumps(tag, ensure_ascii=False)}",
        f"slug: {slug}",
        "kind: concept",
        f"source_count: {len(entries)}",
        "---",
        "",
        f"# {tag}",
        "",
        "## Topic summary",
        "",
        summary,
        "",
        "## Core sources",
        "",
    ]
    for entry in sorted(entries, key=lambda x: x.get("ingested_at", "")):
        lines.append(f"- [[../sources/{entry['slug']}|{entry.get('title', entry['slug'])}]]")
    lines.extend([
        "",
        "## Key points",
        "",
        "- Consolidate key findings from the linked sources.",
        "",
        "## Open questions",
        "",
        "- What is still missing or weakly supported in this topic?",
        "",
        "## Structured artifacts",
        "",
    ])
    structured = [e for e in entries if e.get("source_type") in {"paper", "spreadsheet", "repo"}]
    if structured:
        for entry in structured:
            lines.append(f"- [[../sources/{entry['slug']}|{entry.get('title', entry['slug'])}]] — {entry.get('source_type')}")
    else:
        lines.append("- No structured artifacts yet.")
    lines.extend([
        "",
        "## Backlinks",
        "",
    ])
    for entry in sorted(entries, key=lambda x: x.get("ingested_at", "")):
        lines.append(f"- Referenced by [[../sources/{entry['slug']}|{entry.get('title', entry['slug'])}]]")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Build source and index pages from manifest")
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    manifest = load_manifest(root / "manifest.json")
    entries = manifest.get("entries", [])

    sources_dir = root / "wiki/sources"
    concepts_dir = root / "wiki/concepts"
    indexes_dir = root / "wiki/indexes"
    sources_dir.mkdir(parents=True, exist_ok=True)
    concepts_dir.mkdir(parents=True, exist_ok=True)
    indexes_dir.mkdir(parents=True, exist_ok=True)

    tag_map = defaultdict(list)
    date_map = defaultdict(list)
    source_lines = ["# Sources", ""]

    for entry in sorted(entries, key=lambda x: x.get("ingested_at", "")):
        slug = entry["slug"]
        (sources_dir / f"{slug}.md").write_text(source_page(entry), encoding="utf-8")
        source_lines.append(f"- [[../sources/{slug}|{entry.get('title', slug)}]] — {entry.get('source_type', '')}")
        tags = entry.get("tags", []) or ["untagged"]
        for tag in tags:
            tag_map[tag].append(entry)
        date_key = entry.get("ingested_at", "")[:10] or "unknown"
        date_map[date_key].append(entry)

    if len(source_lines) == 2:
        source_lines.append("_No sources yet._")
    (indexes_dir / "sources.md").write_text(fmt_list(source_lines), encoding="utf-8")

    tag_lines = ["# Tags", ""]
    concept_index_lines = ["# Concepts", ""]
    if tag_map:
        for tag in sorted(tag_map):
            tag_slug = concept_slug(tag)
            (concepts_dir / f"{tag_slug}.md").write_text(concept_page(tag, tag_map[tag]), encoding="utf-8")
            tag_lines.append(f"## {tag}")
            tag_lines.append("")
            tag_lines.append(f"- [[../concepts/{tag_slug}|{tag}]]")
            for entry in tag_map[tag]:
                slug = entry["slug"]
                tag_lines.append(f"  - [[../sources/{slug}|{entry.get('title', slug)}]]")
            tag_lines.append("")
            concept_index_lines.append(f"- [[../concepts/{tag_slug}|{tag}]] — {len(tag_map[tag])} sources")
    else:
        tag_lines.append("_No tags yet._")
        concept_index_lines.append("_No concepts yet._")
    (indexes_dir / "tags.md").write_text(fmt_list(tag_lines), encoding="utf-8")
    (indexes_dir / "concepts.md").write_text(fmt_list(concept_index_lines), encoding="utf-8")

    timeline_lines = ["# Timeline", ""]
    if date_map:
        for day in sorted(date_map):
            timeline_lines.append(f"## {day}")
            timeline_lines.append("")
            for entry in date_map[day]:
                slug = entry["slug"]
                timeline_lines.append(f"- [[../sources/{slug}|{entry.get('title', slug)}]]")
            timeline_lines.append("")
    else:
        timeline_lines.append("_No entries yet._")
    (indexes_dir / "timeline.md").write_text(fmt_list(timeline_lines), encoding="utf-8")

    topic_map_lines = ["# Topic Map", ""]
    if tag_map:
        for tag in sorted(tag_map):
            tag_slug = concept_slug(tag)
            topic_map_lines.append(f"- [[../concepts/{tag_slug}|{tag}]] — {len(tag_map[tag])} sources")
    else:
        topic_map_lines.append("_No topic memos yet._")
    (indexes_dir / "topic-map.md").write_text(fmt_list(topic_map_lines), encoding="utf-8")

    summary = {
        "ok": True,
        "entry_count": len(entries),
        "generated_sources": len(entries),
        "generated_concepts": len(tag_map),
        "generated_indexes": ["sources.md", "tags.md", "timeline.md", "concepts.md", "topic-map.md"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
