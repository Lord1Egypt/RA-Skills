#!/usr/bin/env python3
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

MAX_SENTENCE = 240
MAX_POINTS = 6


def load_manifest(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def concept_slug(tag: str) -> str:
    text = tag.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "untagged"


def clean_preview_text(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"^##\s+Abstract\s*", "", text)
    text = re.sub(r"^##\s+Extracted text\s*", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str):
    text = clean_preview_text(text)
    return [s.strip() for s in re.split(r"(?<=[。！？.!?])\s+", text) if s.strip()]


def first_good_sentence(text: str) -> str:
    candidates = split_sentences(text)
    for c in candidates:
        if len(c) < 40:
            continue
        if re.search(r"^<<|/Filter|/Type /XObject|/ColorSpace|/Length ", c):
            continue
        return c[:MAX_SENTENCE]
    text = clean_preview_text(text)
    return text[:MAX_SENTENCE] if text else "No preview extracted yet."


def extract_paper_signals(text: str):
    candidates = split_sentences(text)
    problem = ""
    result = ""
    for c in candidates:
        lower = c.lower()
        if not problem and re.search(r"based on|we propose|we present|we introduce|problem|challenge", lower):
            problem = c[:MAX_SENTENCE]
        if not result and re.search(r"show|achieves|improving|state-of-the-art|superior|faster|better", lower):
            result = c[:MAX_SENTENCE]
    if not problem and candidates:
        problem = candidates[0][:MAX_SENTENCE]
    if not result and len(candidates) > 1:
        result = candidates[1][:MAX_SENTENCE]
    return problem or "No clear problem statement extracted yet.", result or "No clear result statement extracted yet."


def parse_preview_table(text: str):
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    rows = []
    for line in lines:
        if "|" in line:
            rows.append([cell.strip() for cell in line.split("|")])
    if not rows:
        return [], []
    header = rows[0]
    data_rows = rows[1:]
    return header, data_rows


def spreadsheet_snapshot(text: str) -> str:
    header, data_rows = parse_preview_table(text)
    if not header:
        return "No spreadsheet preview extracted yet."
    return f"Columns observed: {', '.join(header)}. Sample preview rows captured: {len(data_rows)}."


def repo_snapshot(text: str) -> str:
    sentence = first_good_sentence(text)
    return sentence if sentence != "No preview extracted yet." else "Repository summary preview is not yet available."


def paper_insights(entries):
    block = []
    if not entries:
        return ["- No paper-specific synthesis available."]
    titles = [e.get("title", e.get("slug", "Untitled")) for e in entries[:MAX_POINTS]]
    block.append(f"- Papers in scope: {', '.join(titles)}.")
    first = entries[0]
    problem, result = extract_paper_signals(first.get("body_preview") or "")
    block.append(f"- Problem framing: {problem} — Source: [[../sources/{first['slug']}|{first.get('title', first['slug'])}]]")
    block.append(f"- Early result signal: {result} — Source: [[../sources/{first['slug']}|{first.get('title', first['slug'])}]]")
    block.append("- Next synthesis pass should separate problem, method, result, and limitation claims per paper.")
    return block[:MAX_POINTS]


def spreadsheet_insights(entries):
    block = []
    if not entries:
        return ["- No spreadsheet-specific synthesis available."]
    first = entries[0]
    header, data_rows = parse_preview_table(first.get("body_preview") or "")
    if header:
        block.append(f"- Columns: {', '.join(header)} — Source: [[../sources/{first['slug']}|{first.get('title', first['slug'])}]]")
    if data_rows:
        sample = "; ".join([", ".join(row[:4]) for row in data_rows[:2]])
        block.append(f"- Sample rows: {sample} — Source: [[../sources/{first['slug']}|{first.get('title', first['slug'])}]]")
    block.append("- Likely next step: convert stable columns into KB facts, metrics tables, or chart candidates.")
    return block[:MAX_POINTS]


def repo_insights(entries):
    block = []
    if not entries:
        return ["- No repository-specific synthesis available."]
    first = entries[0]
    snapshot = repo_snapshot(first.get("body_preview") or "")
    block.append(f"- Repository snapshot: {snapshot} — Source: [[../sources/{first['slug']}|{first.get('title', first['slug'])}]]")
    block.append(f"- Likely local path or summary page is attached via [[../sources/{first['slug']}|{first.get('title', first['slug'])}]] for deeper inspection.")
    block.append("- Next step: identify key files, entry points, and implementation choices worth turning into concept notes.")
    return block[:MAX_POINTS]


def summarize_entries(entries):
    generic_points = []
    open_questions = []
    structured = []
    evidence = []

    paper_entries = [e for e in entries if e.get("source_type") == "paper"]
    spreadsheet_entries = [e for e in entries if e.get("source_type") == "spreadsheet"]
    repo_entries = [e for e in entries if e.get("source_type") == "repo"]

    for entry in entries[:MAX_POINTS]:
        title = entry.get("title", entry.get("slug", "Untitled"))
        sentence = first_good_sentence(entry.get("body_preview") or "")
        generic_points.append(f"- {sentence} — Source: [[../sources/{entry['slug']}|{title}]]")
        evidence.append(f"- [[../sources/{entry['slug']}|{title}]] ({entry.get('source_type', 'unknown')})")
        if entry.get("status") in {"stub", "suspicious"}:
            open_questions.append(f"- Review extraction quality for [[../sources/{entry['slug']}|{title}]].")
        if entry.get("source_type") in {"paper", "spreadsheet", "repo"}:
            structured.append(f"- [[../sources/{entry['slug']}|{title}]] — {entry.get('source_type')}")

    type_sections = []
    if paper_entries:
        type_sections.append(("## Paper synthesis", paper_insights(paper_entries)))
        open_questions.append("- Which claims from the papers are directly supported by extracted evidence versus only hinted at in abstracts/previews?")
    if spreadsheet_entries:
        type_sections.append(("## Spreadsheet synthesis", spreadsheet_insights(spreadsheet_entries)))
        open_questions.append("- Which columns or sheets should become stable KB facts, metrics tables, or charts?")
    if repo_entries:
        type_sections.append(("## Repository synthesis", repo_insights(repo_entries)))
        open_questions.append("- Which implementation details in the repositories deserve standalone concept notes or how-to pages?")
    if not open_questions:
        open_questions.append("- What is the best synthesis across these sources?")
    if not structured:
        structured.append("- No structured artifacts yet.")

    return generic_points[:MAX_POINTS], open_questions[:MAX_POINTS], structured[:MAX_POINTS], evidence[:MAX_POINTS], type_sections


def build_summary(tag: str, entries):
    source_types = sorted({e.get("source_type", "unknown") for e in entries})
    type_text = ", ".join(source_types)
    if any(e.get("source_type") == "paper" for e in entries):
        lead = first_good_sentence(next((e.get("body_preview") for e in entries if e.get("source_type") == "paper"), ""))
    elif any(e.get("source_type") == "spreadsheet" for e in entries):
        lead = spreadsheet_snapshot(next((e.get("body_preview") for e in entries if e.get("source_type") == "spreadsheet"), ""))
    elif any(e.get("source_type") == "repo" for e in entries):
        lead = repo_snapshot(next((e.get("body_preview") for e in entries if e.get("source_type") == "repo"), ""))
    else:
        strong = [first_good_sentence(e.get("body_preview") or "") for e in entries if first_good_sentence(e.get("body_preview") or "") != "No preview extracted yet."]
        lead = strong[0] if strong else "This topic has not accumulated enough clean preview text yet."
    return (
        f"This topic currently groups {len(entries)} source(s) tagged '{tag}' across {type_text}. "
        f"Current evidence suggests: {lead}"
    )


def render_concept(tag, entries):
    slug = concept_slug(tag)
    key_points, open_questions, structured, evidence, type_sections = summarize_entries(entries)
    summary = build_summary(tag, entries)
    lines = [
        "---",
        f"title: {tag}",
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
    for entry in entries:
        lines.append(f"- [[../sources/{entry['slug']}|{entry.get('title', entry['slug'])}]]")
    lines.extend([
        "",
        "## Evidence base",
        "",
        *evidence,
        "",
        "## Key points",
        "",
        *key_points,
        "",
    ])
    for header, bullets in type_sections:
        lines.extend([header, "", *bullets, ""])
    lines.extend([
        "## Open questions",
        "",
        *open_questions,
        "",
        "## Structured artifacts",
        "",
        *structured,
        "",
        "## Backlinks",
        "",
    ])
    for entry in entries:
        lines.append(f"- Referenced by [[../sources/{entry['slug']}|{entry.get('title', entry['slug'])}]]")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate concept memo scaffolds from the KB manifest")
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    manifest = load_manifest(root / "manifest.json")
    entries = manifest.get("entries", [])

    tag_map = defaultdict(list)
    for entry in entries:
        for tag in (entry.get("tags") or ["untagged"]):
            tag_map[tag].append(entry)

    concepts_dir = root / "wiki/concepts"
    indexes_dir = root / "wiki/indexes"
    concepts_dir.mkdir(parents=True, exist_ok=True)
    indexes_dir.mkdir(parents=True, exist_ok=True)

    topic_map = ["# Topic Map", ""]
    for tag in sorted(tag_map):
        slug = concept_slug(tag)
        (concepts_dir / f"{slug}.md").write_text(render_concept(tag, tag_map[tag]), encoding="utf-8")
        topic_map.append(f"- [[../concepts/{slug}|{tag}]] — {len(tag_map[tag])} sources")
    if len(topic_map) == 2:
        topic_map.append("_No topic memos yet._")
    (indexes_dir / "topic-map.md").write_text("\n".join(topic_map) + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "concepts": len(tag_map)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
