#!/usr/bin/env python3
"""Export one book from the daily-reading library, in reading order (from book.json).

  python3 export_book.py xuanzang                 # -> <book>/export/xuanzang.md + xuanzang.html
  python3 export_book.py xuanzang --embed-images  # HTML with images inlined (JPEG, downscaled)
  python3 export_book.py xuanzang --embed-audio   # also inline audio (big file!)
  python3 export_book.py ramayana --from 1 --to 50 --out /tmp/out

Without --embed-* the export references files via relative paths (../vol01/ep001/map.png),
so keep it inside the book folder (or zip the whole book folder) and it stays offline-readable.
"""
import argparse, base64, html, io, json, os, re, sys

LIB = os.environ.get("DAILY_LIBRARY", os.path.dirname(os.path.abspath(__file__)))
BEGIN, END = "<!-- media:begin -->", "<!-- media:end -->"

CSS = """
body{font-family:-apple-system,"PingFang SC","Noto Serif CJK SC","Songti SC",serif;max-width:860px;margin:2em auto;padding:0 1.2em;line-height:1.8;color:#222;background:#fdfbf6}
h1{text-align:center;margin-top:1.5em} h2{border-bottom:2px solid #c9b88a;padding-bottom:.3em;margin-top:2.5em}
blockquote{border-left:4px solid #c9b88a;margin:1em 0;padding:.3em 1em;background:#f6f1e3;color:#444}
img{max-width:100%;border-radius:6px;box-shadow:0 2px 10px rgba(0,0,0,.15)} audio{width:100%;margin:.5em 0}
table{border-collapse:collapse} td,th{border:1px solid #ddd;padding:.3em .6em}
.toc a{text-decoration:none} .episode{page-break-before:always} .chapter-title{text-align:center;color:#8a6d2b;margin-top:3em}
@media print{audio,.audio-link{display:none}}
"""


def load(book):
    p = os.path.join(LIB, book, "book.json")
    if not os.path.exists(p):
        sys.exit(f"no book.json at {p}")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def rewrite_links(md, prefix):
    """Make relative links in an episode's lecture.md relative to the export folder."""
    def fix(url):
        if re.match(r"^(https?:|data:|#|/)", url):
            return url
        return prefix + url
    md = re.sub(r"(!?\[[^\]]*\]\()([^)\s]+)(\))", lambda m: m.group(1) + fix(m.group(2)) + m.group(3), md)
    md = re.sub(r'(src=")([^"]+)(")', lambda m: m.group(1) + fix(m.group(2)) + m.group(3), md)
    return md


def data_uri(path, kind, max_w=1600):
    if kind == "image":
        try:
            from PIL import Image
            im = Image.open(path).convert("RGB")
            if im.width > max_w:
                im = im.resize((max_w, int(im.height * max_w / im.width)))
            buf = io.BytesIO(); im.save(buf, "JPEG", quality=85)
            return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        except Exception:
            ext = os.path.splitext(path)[1].lstrip(".").lower().replace("jpg", "jpeg")
            return f"data:image/{ext};base64," + base64.b64encode(open(path, "rb").read()).decode()
    return "data:audio/mpeg;base64," + base64.b64encode(open(path, "rb").read()).decode()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("book")
    ap.add_argument("--out", help="output folder (default <book>/export)")
    ap.add_argument("--from", dest="ep_from", type=int, default=1)
    ap.add_argument("--to", dest="ep_to", type=int, default=10**9)
    ap.add_argument("--embed-images", action="store_true")
    ap.add_argument("--embed-audio", action="store_true")
    a = ap.parse_args()

    m = load(a.book)
    book_root = os.path.join(LIB, a.book)
    out_dir = os.path.abspath(a.out or os.path.join(book_root, "export"))
    os.makedirs(out_dir, exist_ok=True)
    rel_root = os.path.relpath(book_root, out_dir)
    eps = [e for e in sorted(m["episodes"], key=lambda e: e["episode"]) if a.ep_from <= e["episode"] <= a.ep_to]
    if not eps:
        sys.exit("no episodes in range")

    title = f"{m['title']} · {m['series']}"
    toc, body, last_ch = [], [], object()
    for e in eps:
        anchor = f"ep{e['episode']:03d}"
        ch_label = e.get("chapter_label")
        if ch_label and e.get("chapter") != last_ch:
            last_ch = e.get("chapter")
            body.append(f'\n<h1 class="chapter-title">{html.escape(ch_label)}</h1>\n')
            toc.append(f"\n**{ch_label}**\n")
        toc.append(f"- [第 {e['episode']} 期 · {e.get('title','')}](#{anchor})  <small>{e.get('date','')}</small>")
        ep_dir = os.path.join(book_root, e["dir"])
        lec = os.path.join(ep_dir, e["files"].get("lecture", "lecture.md"))
        md = open(lec, encoding="utf-8").read() if os.path.exists(lec) else f"## 第 {e['episode']} 期\n\n（讲稿缺失）\n"
        prefix = os.path.relpath(ep_dir, out_dir).replace(os.sep, "/") + "/"
        md = rewrite_links(md, prefix)
        body.append(f'<a id="{anchor}"></a>\n<div class="episode" markdown="1">\n\n{md}\n\n</div>\n')

    md_doc = f"# {title}\n\n## 目录\n\n" + "\n".join(toc) + "\n\n" + "\n".join(body)
    md_path = os.path.join(out_dir, f"{a.book}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_doc)

    import markdown
    html_body = markdown.markdown(md_doc, extensions=["extra", "sane_lists", "nl2br"])
    if a.embed_images or a.embed_audio:
        def emb(mt):
            attr, url = mt.group(1), mt.group(2)
            if url.startswith("data:") or re.match(r"^https?:", url):
                return mt.group(0)
            path = os.path.normpath(os.path.join(out_dir, html.unescape(url)))
            is_audio = url.lower().endswith((".mp3", ".m4a", ".wav"))
            if (is_audio and a.embed_audio) or (not is_audio and a.embed_images and attr == "src"):
                if os.path.exists(path):
                    return f'{attr}="{data_uri(path, "audio" if is_audio else "image")}"'
            return mt.group(0)
        html_body = re.sub(r'(src)="([^"]+)"', emb, html_body)
    html_body = html_body.replace('<p>🔊', '<p class="audio-link">🔊')
    doc = (f'<!doctype html><html lang="zh"><head><meta charset="utf-8">'
           f'<meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{html.escape(title)}</title><style>{CSS}</style></head><body>{html_body}</body></html>')
    html_path = os.path.join(out_dir, f"{a.book}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(doc)
    print(json.dumps({"ok": True, "episodes": len(eps), "markdown": md_path, "html": html_path,
                      "html_bytes": os.path.getsize(html_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
