#!/usr/bin/env python3
import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from kb_env import KB_CONFIG_PATH

REQUIRED_DIRS = [
    "raw/articles",
    "raw/papers",
    "raw/repos",
    "raw/files",
    "wiki/sources",
    "wiki/indexes",
    "outputs",
]
REQUIRED_FIELDS = ["id", "slug", "title", "source", "source_type", "raw_path", "ingested_at", "status"]

TERM_PAIRS = [
    ("LLM", "llm"),
    ("RAG", "rag"),
    ("transformer", "Transformer"),
    ("agent", "Agent"),
    ("fine-tuning", "finetuning"),
    ("knowledge base", "knowledge-base"),
    ("prompt injection", "prompt-injection"),
    ("token", "tokens"),
]

CONFIG_PATH = KB_CONFIG_PATH


def load_manifest(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_routing_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {"repos": [], "routing": {"default_repo": "general"}}


def check_terminology(entries):
    issues = []
    for entry in entries:
        preview = (entry.get("body_preview") or "").lower()
        title = (entry.get("title") or "").lower()
        combined = title + " " + preview
        for a, b in TERM_PAIRS:
            if a.lower() in combined and b.lower() in combined and a.lower() != b.lower():
                issues.append({
                    "entry": entry.get("slug"),
                    "title": entry.get("title", ""),
                    "issue": f"Mixed terminology: '{a}' and '{b}'",
                    "severity": "low",
                })
    return issues


def check_extraction_quality(entries):
    issues = []
    for entry in entries:
        slug = entry.get("slug", "?")
        title = entry.get("title", "")
        status = entry.get("status", "")
        extraction = entry.get("extraction", "none")
        prompt_shield = entry.get("prompt_shield", {})
        psl_action = prompt_shield.get("action", "allow")
        psl_severity = prompt_shield.get("severity", "SAFE")
        suspicious_count = entry.get("suspicious_segment_count", 0)

        if status == "suspicious":
            issues.append({
                "entry": slug,
                "title": title,
                "issue": f"Status is 'suspicious'. PSL action={psl_action}, severity={psl_severity}, suspicious_segments={suspicious_count}",
                "severity": "medium",
                "type": "extraction_quality",
            })
        if extraction == "failed":
            issues.append({
                "entry": slug,
                "title": title,
                "issue": "Extraction failed. Content may be a stub or unprocessed.",
                "severity": "medium",
                "type": "extraction_quality",
            })
        if psl_action in ("block", "warn") and psl_severity in ("HIGH", "CRITICAL", "MEDIUM"):
            issues.append({
                "entry": slug,
                "title": title,
                "issue": f"Prompt shield flagged: action={psl_action}, severity={psl_severity}",
                "severity": "high",
                "type": "security",
            })
        if suspicious_count > 5:
            issues.append({
                "entry": slug,
                "title": title,
                "issue": f"High suspicious segment count: {suspicious_count}",
                "severity": "medium",
                "type": "extraction_quality",
            })
    return issues


def check_route_mismatch(entries, config):
    issues = []
    repos = {r.get("name"): r for r in config.get("repos", [])}
    default = config.get("routing", {}).get("default_repo", "general")
    for entry in entries:
        slug = entry.get("slug", "?")
        title = entry.get("title", "")
        tags = [t.lower() for t in entry.get("tags", [])]
        source_type = entry.get("source_type", "")
        source = entry.get("source", "").lower()
        expected_tags = set()
        if source_type == "paper":
            expected_tags = {"arxiv", "paper", "ai"}
        elif source_type == "repo":
            expected_tags = {"repo", "training", "llm"}
        matched = expected_tags & set(tags)
        if not matched and tags:
            issues.append({
                "entry": slug,
                "title": title,
                "issue": f"Source type '{source_type}' but no matching tags found. Tags: {tags}",
                "severity": "low",
                "type": "route_mismatch",
            })
    return issues


def check_concept_coverage(entries):
    tag_map = defaultdict(list)
    for entry in entries:
        for tag in (entry.get("tags") or []):
            tag_map[tag].append(entry)
    orphans = []
    for tag, group in tag_map.items():
        if len(group) == 1:
            orphans.append({
                "tag": tag,
                "entry": group[0].get("slug"),
                "issue": f"Tag '{tag}' used by only 1 source — consider merging or expanding",
                "severity": "low",
            })
    return orphans


def check_missing_metadata(entries):
    issues = []
    for entry in entries:
        slug = entry.get("slug", "?")
        title = entry.get("title", "")
        for field in REQUIRED_FIELDS:
            if field not in entry or entry.get(field) in (None, ""):
                issues.append({
                    "entry": slug,
                    "title": title,
                    "issue": f"Missing required field: {field}",
                    "severity": "low",
                    "type": "metadata",
                })
    return issues


def main():
    parser = argparse.ArgumentParser(description="Knowledge-aware lint for KB health")
    parser.add_argument("--root", required=True)
    parser.add_argument("--config", default=str(CONFIG_PATH))
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    problems = []
    warnings = []

    config = load_routing_config()

    for rel in REQUIRED_DIRS:
        if not (root / rel).exists():
            problems.append(f"Missing directory: {rel}")

    manifest_path = root / "manifest.json"
    if not manifest_path.exists():
        problems.append("Missing manifest.json")
        print(json.dumps({"ok": False, "problems": problems, "warnings": warnings}, ensure_ascii=False, indent=2))
        return

    manifest = load_manifest(manifest_path)
    entries = manifest.get("entries", [])

    counts = Counter(e.get("slug") for e in entries)
    for slug, count in counts.items():
        if slug and count > 1:
            problems.append(f"Duplicate slug: {slug}")

    manifest_slugs = {e.get("slug") for e in entries if e.get("slug")}
    for page in (root / "wiki/sources").glob("*.md"):
        if page.stem not in manifest_slugs:
            warnings.append(f"Orphan source page: wiki/sources/{page.name}")

    extraction_issues = check_extraction_quality(entries)
    warnings.extend([{
        "type": "extraction_quality",
        **item,
    } for item in extraction_issues])

    terminology_issues = check_terminology(entries)
    warnings.extend([{
        "type": "terminology",
        **item,
    } for item in terminology_issues])

    route_issues = check_route_mismatch(entries, config)
    warnings.extend([{
        "type": "route_mismatch",
        **item,
    } for item in route_issues])

    concept_issues = check_concept_coverage(entries)
    warnings.extend([{
        "type": "concept_coverage",
        **item,
    } for item in concept_issues])

    metadata_issues = check_missing_metadata(entries)
    warnings.extend([{
        "type": "metadata",
        **item,
    } for item in metadata_issues])

    ok = not problems
    summary = {
        "ok": ok,
        "problems": problems,
        "warnings": warnings,
        "counts": {
            "total_entries": len(entries),
            "extraction_issues": len(extraction_issues),
            "terminology_issues": len(terminology_issues),
            "route_mismatches": len(route_issues),
            "concept_coverage_issues": len(concept_issues),
            "metadata_issues": len(metadata_issues),
        },
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
