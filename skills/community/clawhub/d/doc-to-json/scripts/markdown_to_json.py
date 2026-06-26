#!/usr/bin/env python3
"""Convert MinerU Markdown -> JSON (simplified, robust parser).

Handles the typical MinerU output:
- Plain text metadata fields (课程名称：xxx)
- Markdown headings (H1-H6)
- HTML <table> blocks (preserved as-is for later parsing)
- Numbered list items (1. xxx)
- Plain text paragraphs

Usage:
    python3 scripts/markdown_to_json.py <input.md> [-o output.json]
"""

import argparse
import json
import re
import sys


def parse_md(content: str) -> dict:
    """Parse MinerU Markdown into structured dict."""
    lines = content.split("\n")
    root = {}
    stack = []  # (level, title, node_ref)
    current = root

    # Phase 1: Extract pre-heading metadata
    i = 0
    meta_pattern = re.compile(r"^(课程名称|课程代码|课程学分|总学时|理论学时|实践学时|适用专业|使用年级|考核方式|课程类型)\s*[：:]\s*(.*)")

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#"):
            break
        m = meta_pattern.match(line)
        if m:
            root[m.group(1)] = m.group(2).strip()
        i += 1

    # Phase 2: Parse structure
    i = i  # continue from where we left off
    while i < len(lines):
        line = lines[i]

        # --- Heading ---
        hm = re.match(r"^(#{1,6})\s+(.+)$", line)
        if hm:
            level = len(hm.group(1))
            title = hm.group(2).strip()
            node = {}

            while stack and stack[-1][0] >= level:
                stack.pop()

            parent = stack[-1][2] if stack else root
            if title not in parent:
                parent[title] = node

            stack.append((level, title, node if title in parent else parent[title]))
            current = node
            i += 1
            continue

        # --- HTML Table ---
        if "<table>" in line:
            table_lines = []
            while i < len(lines) and "<table>" not in lines[i]:
                table_lines.append(lines[i])
                i += 1
            if "<table>" in lines[i]:
                table_lines = [lines[i]]
                i += 1
                while i < len(lines):
                    table_lines.append(lines[i])
                    if "</table>" in lines[i]:
                        i += 1
                        break
                    i += 1

            table_text = "\n".join(table_lines)
            cell_matches = re.findall(r"<td[^>]*>(.*?)</td>", table_text, re.DOTALL)
            cleaned = [re.sub(r"<[^>]+>", "", c).strip() for c in cell_matches]

            if cleaned:
                key = f"表格_{len(current.get('表格', [])) + 1}"
                if "表格" not in current:
                    current["表格"] = []
                current["表格"].append(cleaned)
            continue

        # --- Numbered list ---
        lm = re.match(r"^(\d+[\.\、])\s*(.*)", line.strip())
        if lm:
            items = []
            j = i
            while j < len(lines):
                lm2 = re.match(r"^(\d+[\.\、])\s*(.*)", lines[j].strip())
                if lm2:
                    items.append(lm2.group(2).strip())
                    j += 1
                elif lines[j].strip() == "":
                    j += 1
                    continue
                else:
                    break

            if stack:
                last_title = stack[-1][1]
                current[last_title] = items
            else:
                current["列表"] = items
            i = j
            continue

        # --- Paragraph text ---
        stripped = line.strip()
        if stripped:
            key = "text" if not stack else stack[-1][1]
            current.setdefault(key, "")
            current[key] += " " + stripped if current[key] else stripped
        i += 1

    return root


def main():
    parser = argparse.ArgumentParser(description="MinerU Markdown to JSON")
    parser.add_argument("input", help="Input .md file")
    parser.add_argument("-o", "--output", default=None, help="Output .json file")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()

    result = parse_md(content)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"OK -> {args.output}", file=sys.stderr)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
