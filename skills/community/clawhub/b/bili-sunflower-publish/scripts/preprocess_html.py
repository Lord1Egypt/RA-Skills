#!/usr/bin/env python3
"""Preprocess HTML for Bilibili read editor.

- H1 extraction and heading promotion (exactly 1 H1 → title, remove H1, promote h2→h1 etc.)
- Local image inlining as base64 data URIs
- Whitespace cleanup between tags

Usage: preprocess_html.py <input.html> [output-dir]
  output-dir defaults to /tmp/bili_html.XXXXXX

Output (stdout):
  title=<extracted title>
  path=<output html path>
  bytes=<html byte size>
"""

import sys, re, os, base64, mimetypes, tempfile

input_path = sys.argv[1] if len(sys.argv) > 1 else None
if not input_path:
    print("Usage: preprocess_html.py <input.html> [output-dir]", file=sys.stderr)
    sys.exit(1)

out_dir = sys.argv[2] if len(sys.argv) > 2 else tempfile.mkdtemp(prefix="bili_html.")

with open(input_path, "r", encoding="utf-8") as f:
    html = f.read()

html_dir = os.path.dirname(os.path.abspath(input_path))

# --- H1 extraction and heading promotion ---
h1_matches = re.findall(r"<h1>(.*?)</h1>", html, re.DOTALL)

if len(h1_matches) == 1:
    title = re.sub(r"<[^>]+>", "", h1_matches[0]).strip()
    html = re.sub(r"<h1>.*?</h1>\n?", "", html, count=1)

    def promote(m):
        n = int(m.group(1))
        new_n = max(n - 1, 1)
        return f"<h{new_n}>{m.group(2)}</h{new_n}>"

    html = re.sub(r"<h([2-6])>(.*?)</h\1>", promote, html)
else:
    title = os.path.splitext(os.path.basename(input_path))[0]

# --- Local image inlining as base64 data URIs ---
def inline_img(m):
    prefix = m.group(1)
    quote = m.group(2)
    src = m.group(3)
    if src.startswith(("http://", "https://", "data:")):
        return m.group(0)
    img_path = os.path.join(html_dir, src) if not os.path.isabs(src) else src
    if not os.path.isfile(img_path):
        return m.group(0)
    mime, _ = mimetypes.guess_type(img_path)
    if not mime or not mime.startswith("image/"):
        return m.group(0)
    with open(img_path, "rb") as img_f:
        b64 = base64.b64encode(img_f.read()).decode("ascii")
    return f'{prefix}{quote}data:{mime};base64,{b64}{quote}'

html = re.sub(r"""(<img\s[^>]*src=)(["'])([^"']+)\2""", inline_img, html)

# --- Whitespace cleanup ---
html = re.sub(r">\s+<", "><", html)

# --- Write output ---
os.makedirs(out_dir, exist_ok=True)
safe_title = re.sub(r'[\\/:*?"<>|]', "", title).strip() or "untitled"
out_path = os.path.join(out_dir, safe_title + ".html")

with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"title={title}")
print(f"path={out_path}")
print(f"bytes={len(html.encode('utf-8'))}")
