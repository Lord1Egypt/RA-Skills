#!/usr/bin/env python3
"""Preprocess Markdown for Bilibili read editor.

- H1 extraction and heading promotion (exactly 1 `# ` line → title, remove it, promote ## → # etc.)
- Local image inlining as base64 data URIs

Usage: preprocess_md.py <input.md> [output-dir]
  output-dir defaults to /tmp/bili_md.XXXXXX

Output (stdout):
  title=<extracted title>
  path=<processed md file path>
  bytes=<md byte size>
"""

import sys, re, os, base64, mimetypes, tempfile

input_path = sys.argv[1] if len(sys.argv) > 1 else None
if not input_path:
    print("Usage: preprocess_md.py <input.md> [output-dir]", file=sys.stderr)
    sys.exit(1)

out_dir = sys.argv[2] if len(sys.argv) > 2 else tempfile.mkdtemp(prefix="bili_md.")

with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

md_dir = os.path.dirname(os.path.abspath(input_path))

# --- H1 extraction and heading promotion ---
# Find lines that are H1 (start with "# " but not "##")
h1_indices = [i for i, line in enumerate(lines) if re.match(r"^# (?!#)", line)]

if len(h1_indices) == 1:
    h1_idx = h1_indices[0]
    title = lines[h1_idx].lstrip("# ").strip()
    # Remove the H1 line
    lines.pop(h1_idx)
    # Remove trailing blank line after H1 if present
    if h1_idx < len(lines) and lines[h1_idx].strip() == "":
        lines.pop(h1_idx)
    # Promote all headings by one level: ## → #, ### → ##, etc.
    for i, line in enumerate(lines):
        m = re.match(r"^(#{2,6}) ", line)
        if m:
            lines[i] = line[1:]  # Remove one leading #
else:
    title = os.path.splitext(os.path.basename(input_path))[0]

content = "".join(lines)

# --- Local image inlining as base64 data URIs ---
def inline_md_img(m):
    prefix = m.group(1)  # ![alt](
    src = m.group(2)     # path
    suffix = m.group(3)  # optional title + )
    if src.startswith(("http://", "https://", "data:")):
        return m.group(0)
    img_path = os.path.join(md_dir, src) if not os.path.isabs(src) else src
    if not os.path.isfile(img_path):
        return m.group(0)
    mime, _ = mimetypes.guess_type(img_path)
    if not mime or not mime.startswith("image/"):
        return m.group(0)
    with open(img_path, "rb") as img_f:
        b64 = base64.b64encode(img_f.read()).decode("ascii")
    return f'{prefix}data:{mime};base64,{b64}{suffix}'

# Match ![alt](path) and ![alt](path "title")
content = re.sub(r'(!\[[^\]]*\]\()([^)\s]+)(\s*(?:"[^"]*")?\s*\))', inline_md_img, content)

# --- Write output ---
os.makedirs(out_dir, exist_ok=True)
safe_title = re.sub(r'[\\/:*?"<>|]', "", title).strip() or "untitled"
out_path = os.path.join(out_dir, safe_title + ".md")

with open(out_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"title={title}")
print(f"path={out_path}")
print(f"bytes={len(content.encode('utf-8'))}")
