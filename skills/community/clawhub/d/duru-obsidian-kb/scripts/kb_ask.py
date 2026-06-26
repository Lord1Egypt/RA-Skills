#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent
SEARCH_SCRIPT = SCRIPT_DIR / "kb_search.py"


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:80] or "query"


def load_manifest(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def extract_section(text: str, heading: str):
    pattern = rf"##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s+|\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


def related_concepts(root: Path, question: str):
    concepts_dir = root / "wiki/concepts"
    q = question.lower()
    hits = []
    for path in sorted(concepts_dir.glob("*.md")):
        if path.name == "_template.md":
            continue
        text = read_text(path)
        title = path.stem.lower()
        score = 0
        if title in q:
            score += 5
        if any(token in text.lower() for token in q.split()[:8] if token):
            score += 1
        if score:
            hits.append((score, path))
    hits.sort(key=lambda x: (-x[0], x[1].name))
    return [path for _, path in hits[:5]]


def concept_digest(path: Path):
    text = read_text(path)
    return {
        "path": path,
        "title": path.stem,
        "summary": extract_section(text, "Topic summary"),
        "evidence": extract_section(text, "Evidence base"),
        "key_points": extract_section(text, "Key points"),
        "open_questions": extract_section(text, "Open questions"),
    }


def run_search(root: Path, question: str, top_k: int, include_wiki: bool):
    cmd = [
        "python3",
        str(SEARCH_SCRIPT),
        "--root",
        str(root),
        "--query",
        question,
        "--top-k",
        str(top_k),
    ]
    if include_wiki:
        cmd.append("--include-wiki")
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or proc.stdout or "kb_search failed")
    return json.loads(proc.stdout)


def render_research_md(question: str, search: dict, concept_digests: list[dict]):
    results = search.get("results", [])
    lines = [
        f"# {question}",
        "",
        "## Research brief",
        "",
        "### Question",
        question,
        "",
        "### Retrieval summary",
        "",
        f"- Query: `{search.get('query', question)}`",
        f"- Matched sources: {len(results)}",
        f"- Search root: `{search.get('root', '')}`",
        "",
        "### Top evidence candidates",
        "",
    ]

    if results:
        for i, item in enumerate(results, start=1):
            title = item.get("title") or item.get("slug")
            slug = item.get("slug")
            score = item.get("score", 0)
            source_type = item.get("source_type", "")
            snippet = item.get("snippet", "")
            lines.extend([
                f"#### [{i}] {title}",
                f"- Score: {score}",
                f"- Type: {source_type}",
                f"- Source page: [[../wiki/sources/{slug}|{title}]]",
                f"- Raw path: `{item.get('raw_path')}`",
                f"- Snippet: {snippet if snippet else 'N/A'}",
                "",
            ])
    else:
        lines.extend([
            "- No matching sources found.",
            "- Consider ingesting more material or broadening query terms.",
            "",
        ])

    lines.extend(["### Relevant concepts", ""])
    if concept_digests:
        for concept in concept_digests:
            lines.append(f"- [[../wiki/concepts/{concept['path'].stem}|{concept['title']}]]")
    else:
        lines.append("- No directly matched concept pages yet.")
    lines.append("")

    lines.extend(["### Concept snapshots", ""])
    if concept_digests:
        for concept in concept_digests:
            lines.extend([
                f"#### {concept['title']}",
                concept["summary"] or "No summary yet.",
                "",
            ])
    else:
        lines.append("- No concept snapshots available.")
        lines.append("")

    lines.extend([
        "### Draft answer scaffold",
        "",
        "1) **Direct answer**: write a concise answer using only cited evidence above.",
        "2) **Supporting evidence**: cite source pages in bullet points.",
        "3) **Known gaps**: state uncertainty, missing data, or extraction quality issues.",
        "",
        "### Citation appendix",
        "",
    ])

    if results:
        for i, item in enumerate(results, start=1):
            title = item.get("title") or item.get("slug")
            slug = item.get("slug")
            src = item.get("source") or ""
            lines.append(f"- [{i}] [[../wiki/sources/{slug}|{title}]] — {src}")
    else:
        lines.append("- No citations available.")

    lines.extend([
        "",
        "### Optional filing targets",
        "- If this answer should become long-lived knowledge, file it into a concept memo under `wiki/concepts/`.",
        "",
    ])

    return "\n".join(lines) + "\n"


def render_marp(question: str, search: dict, concept_digests: list[dict]):
    results = search.get("results", [])
    lines = [
        "---",
        "marp: true",
        "theme: default",
        "paginate: true",
        "---",
        "",
        f"# {question}",
        "",
        "---",
        "## Retrieval summary",
        "",
        f"- Matches: {len(results)}",
        f"- Root: {search.get('root', '')}",
        "",
        "---",
        "## Top evidence",
        "",
    ]
    if results:
        for item in results[:6]:
            lines.append(f"- {item.get('title') or item.get('slug')} (score={item.get('score', 0)})")
    else:
        lines.append("- No matching sources")

    lines.extend(["", "---", "## Concepts", ""])
    if concept_digests:
        for c in concept_digests:
            lines.append(f"- {c['title']}")
    else:
        lines.append("- No directly matched concepts")

    lines.extend([
        "",
        "---",
        "## Draft conclusion",
        "",
        "- Fill in key conclusions with citations to source pages.",
        "",
    ])
    return "\n".join(lines) + "\n"


def file_back(root: Path, question: str, content: str, target_slug: Optional[str]):
    slug = target_slug or slugify(question)
    path = root / "wiki/concepts" / f"{slug}-memo.md"
    path.write_text(content, encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(description="Create a KB research brief based on local retrieval")
    parser.add_argument("--root", required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--format", choices=["md", "marp"], default="md")
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--no-wiki-search", action="store_true", help="Disable wiki content bonus in search")
    parser.add_argument("--file-back", action="store_true", help="Also file the output back into wiki/concepts")
    parser.add_argument("--target-concept", default=None, help="Optional concept slug/name for filed-back memo")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    manifest_path = root / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"manifest.json missing under {root}")
    _ = load_manifest(manifest_path)

    date_prefix = datetime.utcnow().strftime("%Y-%m-%d")
    slug = slugify(args.question)
    suffix = ".marp.md" if args.format == "marp" else ".md"
    out_path = root / "outputs" / f"{date_prefix}-{slug}{suffix}"

    search = run_search(root, args.question, args.top_k, include_wiki=not args.no_wiki_search)
    concept_paths = related_concepts(root, args.question)
    concept_digests = [concept_digest(path) for path in concept_paths]

    content = render_marp(args.question, search, concept_digests) if args.format == "marp" else render_research_md(args.question, search, concept_digests)
    out_path.write_text(content, encoding="utf-8")

    filed_back = None
    if args.file_back:
        filed_back = file_back(root, args.question, content, args.target_concept)

    print(json.dumps({
        "ok": True,
        "output": str(out_path),
        "format": args.format,
        "matched_concepts": [p.stem for p in concept_paths],
        "matched_sources": [r.get("slug") for r in search.get("results", [])],
        "total_hits": len(search.get("results", [])),
        "filed_back": str(filed_back) if filed_back else None,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
