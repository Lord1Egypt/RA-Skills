#!/usr/bin/env python3
"""
render_mermaid.py — Extract and render Mermaid diagrams from Markdown.

Finds all ```mermaid fenced blocks in a Markdown file, writes each to
a .mmd file, and renders each to PNG via mmdc (Mermaid CLI).

Usage:
    python render_mermaid.py <markdown_file> <output_image_dir>

Requirements:
    - Node.js with npx available on PATH
    - puppeteer-config.json in the same directory as this script
      (enables --no-sandbox for Linux/container environments)

Output:
    diagram_1.png, diagram_2.png, ... in the output directory.
    This naming convention matches inject_docx.py's expectations.
"""
import os
import re
import subprocess
import sys


def extract_and_render(md_file, output_dir):
    """Extract all mermaid blocks from a Markdown file and render to PNG."""
    os.makedirs(output_dir, exist_ok=True)

    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.findall(r"```mermaid\n(.*?)```", content, re.DOTALL)
    print(f"Found {len(blocks)} mermaid blocks.")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    puppeteer_cfg = os.path.join(script_dir, "puppeteer-config.json")
    puppeteer_args = ["-p", puppeteer_cfg] if os.path.exists(puppeteer_cfg) else []

    for i, block in enumerate(blocks, 1):
        mmd_path = os.path.join(output_dir, f"diagram_{i}.mmd")
        png_path = os.path.join(output_dir, f"diagram_{i}.png")

        with open(mmd_path, "w", encoding="utf-8") as f:
            f.write(block.strip())

        print(f"Rendering diagram {i}...")
        cmd = [
            "npx", "-y", "@mermaid-js/mermaid-cli",
            "-i", mmd_path,
            "-o", png_path,
            "-b", "white",
            "-s", "2",
        ] + puppeteer_args

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully rendered {png_path}")
        else:
            print(f"ERROR rendering diagram {i}: {result.stderr}")


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        md = sys.argv[1]
        out = sys.argv[2]
    else:
        print("Usage: python render_mermaid.py <markdown_file> <output_image_dir>")
        sys.exit(1)
    extract_and_render(md, out)
