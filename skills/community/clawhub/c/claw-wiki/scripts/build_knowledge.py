from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone

from common import (
    docs_root,
    dump_json,
    extract_headings,
    extract_summary,
    iter_markdown_files,
    references_root,
    root_docs_json,
    sha256_file,
    skill_root,
    state_root,
    tokenize,
)


def build_manifest() -> dict:
    files = []
    top_level_counts: dict[str, int] = defaultdict(int)
    root = docs_root()
    for path in iter_markdown_files(root):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        headings = extract_headings(text)
        summary = extract_summary(text)
        category = rel.split("/", 1)[0] if "/" in rel else "_root"
        top_level_counts[category] += 1
        files.append(
            {
                "path": rel,
                "category": category,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
                "title": headings[0] if headings else path.stem,
                "summary": summary,
                "headings": headings[:20],
                "keywords": tokenize(rel, " ".join(headings[:8]), summary),
            }
        )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skill_root": str(skill_root()),
        "docs_root": str(root),
        "docs_json_present": root_docs_json().exists(),
        "file_count": len(files),
        "top_level_counts": dict(sorted(top_level_counts.items())),
        "files": files,
    }


def build_topic_index(manifest: dict) -> dict[str, list[str]]:
    index: dict[str, set[str]] = defaultdict(set)
    for item in manifest["files"]:
        rel = item["path"]
        for token in item["keywords"]:
            index[token].add(rel)
    return {key: sorted(value)[:25] for key, value in sorted(index.items()) if len(value) > 0}


def build_routing_cheatsheet(manifest: dict) -> str:
    lines = [
        "# OpenClaw Routing Cheatsheet",
        "",
        "Generated from the current local snapshot. Use this file when the user question is broad and you need a fast first route before full-text search.",
        "",
        "## Snapshot",
        "",
        f"- Generated at: `{manifest['generated_at']}`",
        f"- Markdown files indexed: `{manifest['file_count']}`",
        "",
        "## Top-Level Routes",
        "",
    ]
    for category, count in manifest["top_level_counts"].items():
        lines.append(f"- `{category}/` ({count} files)")
    lines.extend(
        [
            "",
            "## Query Patterns",
            "",
            "Filename-first:",
            "",
            "```bash",
            "rg --files openclaw_docs | rg 'gateway|install|telegram|security|models'",
            "```",
            "",
            "Content search after narrowing paths:",
            "",
            "```bash",
            "rg -n \"auth|pairing|approval|health|provider\" openclaw_docs/gateway openclaw_docs/cli openclaw_docs/channels",
            "```",
            "",
            "## Guardrails",
            "",
            "- Prefer stable docs over experiments unless the user asks for proposals.",
            "- Read the full relevant file before answering defaults, behavior, or constraints.",
            "- If direct documentation is missing, say what you searched and that the gap is in the local snapshot.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    manifest = build_manifest()
    topic_index = build_topic_index(manifest)

    dump_json(state_root() / "docs-manifest.json", manifest)
    dump_json(state_root() / "topic-index.json", topic_index)
    references_root().mkdir(parents=True, exist_ok=True)
    (references_root() / "routing-cheatsheet.md").write_text(
        build_routing_cheatsheet(manifest),
        encoding="utf-8",
    )
    print(f"Indexed {manifest['file_count']} markdown files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
