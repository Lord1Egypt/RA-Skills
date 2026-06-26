#!/usr/bin/env python3

import argparse, json, sys, re

def md_to_html(md):
    html = md
    # Headers
    html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
    # Bold/italic
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)
    # Code
    html = re.sub(r"`(.+?)`", r"<code>\1</code>", html)
    # Links
    html = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', html)
    # Paragraphs
    paragraphs = [p.strip() for p in html.split("

") if p.strip()]
    html = "\n".join(f"<p>{p}</p>" if not p.startswith("<") else p for p in paragraphs)
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Converted</title></head>
<body>{html}</body></html>"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    with open(args.file) as f:
        md = f.read()
    print(md_to_html(md))

if __name__ == "__main__":
    main()
