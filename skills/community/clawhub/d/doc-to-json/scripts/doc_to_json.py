#!/usr/bin/env python3
"""Full pipeline: Doc/PDF/XLSX -> MinerU Markdown -> JSON.

Usage:
    python3 scripts/doc_to_json.py <input_file> [-o output.json]

Supported formats: .doc .docx .pdf .xlsx .xls

Steps:
  1. Convert doc/docx/pdf/xlsx/xls to Markdown via mineru-open-api
  2. Parse Markdown into structured JSON via markdown_to_json.py

The mineru-open-api CLI must be installed and MINERU_TOKEN set.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile


def run_mineru(input_file: str, temp_dir: str) -> str:
    """Run mineru-open-api to convert document to Markdown."""
    output_dir = os.path.join(temp_dir, "mineru_out")
    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        "mineru-open-api",
        "extract",
        "--token", os.environ.get("MINERU_TOKEN", ""),
        input_file,
        "-o", output_dir
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"MinerU failed: {result.stderr}")

    # Find the output .md file
    for fname in os.listdir(output_dir):
        if fname.endswith(".md"):
            md_path = os.path.join(output_dir, fname)
            return md_path

    raise FileNotFoundError("No .md output from MinerU")


def parse_md(content: str) -> dict:
    """Parse MinerU Markdown into structured JSON dict."""
    lines = content.split("\n")
    root = {}
    stack = []
    current = root

    # Phase 1: Extract pre-heading metadata
    i = 0
    meta_pattern = re.compile(
        r"^(课程名称|课程代码|课程学分|总学时|理论学时|实践学时|"
        r"适用专业|使用年级|考核方式|课程类型|所属专业\（部\）|编制负责人|"
        r"审定人|编制团队成员)\s*[：:]\s*(.*)"
    )

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#"):
            break
        m = meta_pattern.match(line)
        if m:
            root[m.group(1)] = m.group(2).strip()
        i += 1

    # Phase 2: Parse headings, tables, lists, paragraphs
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
            if "<table>" not in lines[i]:
                while i < len(lines):
                    table_lines.append(lines[i])
                    i += 1
            else:
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
            cleaned = [re.sub(r"<[^>]+>", "", c).strip().replace("\n", " ") for c in cell_matches]

            if cleaned:
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
    parser = argparse.ArgumentParser(description="Document -> MinerU Markdown -> JSON")
    parser.add_argument("input", help="Input file (.doc/.docx/.pdf/.xlsx/.xls)")
    parser.add_argument("-o", "--output", default=None, help="Output .json file")
    parser.add_argument("--keep-temp", action="store_true", help="Keep temp files for debugging")
    args = parser.parse_args()

    input_file = os.path.abspath(args.input)
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    tmpdir = tempfile.mkdtemp(prefix="doc2json_")
    try:
        # Step 1: MinerU -> Markdown
        print(f"Step 1: Converting to Markdown via MinerU...", file=sys.stderr)
        md_path = run_mineru(input_file, tmpdir)
        print(f"  Markdown: {md_path}", file=sys.stderr)

        # Step 2: Markdown -> JSON
        print("Step 2: Parsing Markdown to JSON...", file=sys.stderr)
        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()

        result = parse_md(md_content)

        # Step 3: Write output
        output_path = args.output or os.path.splitext(input_file)[0] + ".json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"OK -> {output_path}", file=sys.stderr)

    finally:
        if not args.keep_temp:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
