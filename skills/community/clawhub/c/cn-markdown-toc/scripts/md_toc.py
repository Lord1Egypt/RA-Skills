#!/usr/bin/env python3
"""Markdown TOC generator (stdlib only)."""
import re, sys, argparse

def slugify(text):
    s = text.strip().lower()
    s = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', s)
    s = s.strip().replace(' ', '-')
    return s

def build_toc(lines, max_level=6):
    toc = []
    seen = {}
    for line in lines:
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if not m:
            continue
        level = len(m.group(1))
        if level > max_level:
            continue
        title = m.group(2).strip()
        base = slugify(title)
        seen[base] = seen.get(base, 0) + 1
        anchor = base if seen[base] == 1 else f"{base}-{seen[base]-1}"
        toc.append((level, title, anchor))
    return toc

def render(toc):
    out = ["<!-- TOC -->", ""]
    for level, title, anchor in toc:
        indent = "  " * (level - 1)
        out.append(f"{indent}- [{title}](#{anchor})")
    out.append("")
    out.append("<!-- /TOC -->")
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--max", type=int, default=6)
    ap.add_argument("--insert", action="store_true")
    args = ap.parse_args()
    with open(args.file, encoding="utf-8") as f:
        lines = f.readlines()
    toc = build_toc(lines, args.max)
    rendered = render(toc)
    if args.insert:
        # 替换已有 <!-- TOC -->...<!-- /TOC --> 或插入到顶部
        text = "".join(lines)
        if "<!-- TOC -->" in text:
            new_text = re.sub(r'<!-- TOC -->.*?<!-- /TOC -->', rendered, text, flags=re.S)
        else:
            new_text = rendered + "\n" + text
        with open(args.file, "w", encoding="utf-8") as f:
            f.write(new_text)
        print(f"✅ 已插入目录（{len(toc)} 条）到 {args.file}")
    else:
        print(rendered)

if __name__ == "__main__":
    main()
