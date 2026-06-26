#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Render summary JSON into Markdown, HTML, and PNG in one command."
    )
    parser.add_argument("--summary", required=True, help="Path to summary JSON")
    parser.add_argument(
        "--out-stem",
        required=True,
        help="Output stem path without extension, for example output/article-summary",
    )
    args = parser.parse_args()

    summary_path = Path(args.summary)
    out_stem = Path(args.out_stem)
    out_stem.parent.mkdir(parents=True, exist_ok=True)

    markdown_script = Path(__file__).with_name("render_markdown.py")
    card_script = Path(__file__).with_name("render_card.py")

    markdown_out = out_stem.with_suffix(".md")
    html_out = out_stem.with_suffix(".html")
    png_out = out_stem.with_suffix(".png")

    subprocess.run(
        [sys.executable, str(markdown_script), "--summary", str(summary_path), "--out", str(markdown_out)],
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(card_script),
            "--summary",
            str(summary_path),
            "--out",
            str(png_out),
            "--html-out",
            str(html_out),
        ],
        check=True,
    )

    print(markdown_out)
    print(html_out)
    print(png_out)


if __name__ == "__main__":
    main()
