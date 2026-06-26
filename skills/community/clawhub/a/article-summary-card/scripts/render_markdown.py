#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def build_markdown(summary: dict) -> str:
    lines = []
    title = str(summary.get("title", "")).strip()
    source = str(summary.get("source", "")).strip()
    one_sentence = str(summary.get("one_sentence", "")).strip()
    closing_takeaway = str(summary.get("closing_takeaway", "")).strip()
    tags = [str(tag).strip() for tag in summary.get("tags", []) if str(tag).strip()]

    if title:
        lines.append(f"# {title}")
        lines.append("")

    if source:
        lines.append(f"来源：{source}")
        lines.append("")

    if one_sentence:
        lines.append("## 一句话总结")
        lines.append("")
        lines.append(one_sentence)
        lines.append("")

    for section in summary.get("sections", [])[:4]:
        heading = str(section.get("heading", "")).strip()
        section_summary = str(section.get("summary", "")).strip()
        points = [str(point).strip() for point in section.get("points", [])[:3] if str(point).strip()]
        if not heading:
            continue
        lines.append(f"## {heading}")
        lines.append("")
        if section_summary:
            lines.append(section_summary)
            lines.append("")
        for point in points:
            lines.append(f"- {point}")
        if points:
            lines.append("")

    if closing_takeaway:
        lines.append("## 最后记住什么")
        lines.append("")
        lines.append(closing_takeaway)
        lines.append("")

    if tags:
        lines.append("## 标签")
        lines.append("")
        lines.append(" ".join(f"`{tag}`" for tag in tags))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Render a summary JSON file into Markdown.")
    parser.add_argument("--summary", required=True, help="Path to summary JSON")
    parser.add_argument("--out", required=True, help="Path to output Markdown")
    args = parser.parse_args()

    summary = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_markdown(summary), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
