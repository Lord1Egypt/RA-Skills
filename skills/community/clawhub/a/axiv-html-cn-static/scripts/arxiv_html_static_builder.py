#!/usr/bin/env python3
"""Prepare local arXiv HTML assets and build a Chinese static HTML page.

This script intentionally does not translate text. Use CodeBuddy / LLM workflow to
produce a Chinese Markdown document first, then use this script to wrap it into a
local static HTML page with figures/assets copied from arXiv HTML.
"""

import argparse
import hashlib
import html
import json
import mimetypes
import os
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 arxiv-html-cn-static/1.0"
SKIP_SECTION_KEYWORDS = [
    "references", "acknowledgments", "acknowledgements", "appendix",
    "supplementary", "instructions for reporting",
]


def fetch(url, binary=False, timeout=40):
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    resp.raise_for_status()
    return resp.content if binary else resp.text


def extract_arxiv_id(raw):
    raw = raw.strip()
    patterns = [
        r"arxiv\.org/(?:abs|html|pdf|src)/([A-Za-z\-]+/\d{7}|\d{4}\.\d{4,5})(?:v\d+)?",
        r"^([A-Za-z\-]+/\d{7}|\d{4}\.\d{4,5})(?:v\d+)?$",
    ]
    for pattern in patterns:
        match = re.search(pattern, raw)
        if match:
            return match.group(1)
    return None


def sanitize_title(title):
    name = title.lower()
    name = re.sub(r"[^a-z0-9\s-]", "", name)
    name = re.sub(r"\s+", "-", name.strip())
    name = re.sub(r"-+", "-", name)
    return name[:90].rstrip("-") or "arxiv-paper"


def get_abs_info(arxiv_id):
    abs_url = f"https://arxiv.org/abs/{arxiv_id}"
    soup = BeautifulSoup(fetch(abs_url), "html.parser")

    title = ""
    title_el = soup.find("h1", class_="title")
    if title_el:
        title = re.sub(r"^Title:\s*", "", title_el.get_text(" ", strip=True), flags=re.I)

    authors = ""
    authors_el = soup.find("div", class_="authors")
    if authors_el:
        authors = re.sub(r"^Authors?:\s*", "", authors_el.get_text(" ", strip=True), flags=re.I)

    links = {
        "abs": abs_url,
        "pdf": f"https://arxiv.org/pdf/{arxiv_id}",
        "html": f"https://arxiv.org/html/{arxiv_id}",
        "tex": f"https://arxiv.org/src/{arxiv_id}",
    }
    pdf_link = soup.find("a", class_="download-pdf")
    if pdf_link and pdf_link.get("href"):
        links["pdf"] = urljoin(abs_url, pdf_link["href"])
    html_link = soup.find("a", id="latexml-download-link")
    if html_link and html_link.get("href"):
        links["html"] = urljoin(abs_url, html_link["href"])
    tex_link = soup.find("a", class_="download-eprint")
    if tex_link and tex_link.get("href"):
        links["tex"] = urljoin(abs_url, tex_link["href"])

    return {"arxiv_id": arxiv_id, "title": title, "authors": authors, "links": links}


def fetch_arxiv_html(arxiv_id, preferred_url=None):
    candidates = []
    if preferred_url:
        candidates.append(preferred_url)
    candidates.extend([
        f"https://arxiv.org/html/{arxiv_id}v1",
        f"https://arxiv.org/html/{arxiv_id}",
    ])
    seen = set()
    for url in candidates:
        if url in seen:
            continue
        seen.add(url)
        try:
            return fetch(url), url
        except Exception as exc:
            print(f"HTML fetch failed: {url}: {exc}", file=sys.stderr)
    raise RuntimeError(f"Cannot fetch arXiv HTML for {arxiv_id}")


def extension_from_type(content_type):
    if not content_type:
        return ""
    ctype = content_type.split(";", 1)[0].strip().lower()
    return mimetypes.guess_extension(ctype) or ""


def safe_asset_name(url, content_type=""):
    parsed = urlparse(url)
    base = unquote(Path(parsed.path).name) or "asset"
    base = re.sub(r"[^A-Za-z0-9._-]", "_", base)
    if "." not in base:
        base += extension_from_type(content_type) or ".bin"
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
    stem, suffix = os.path.splitext(base)
    return f"{stem[:70]}-{digest}{suffix}"


def download_asset(url, assets_dir, manifest):
    if not url or url.startswith(("data:", "javascript:", "mailto:", "#")):
        return url
    if url in manifest:
        return manifest[url]["local"]
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=40)
        resp.raise_for_status()
    except Exception as exc:
        print(f"Asset fetch failed: {url}: {exc}", file=sys.stderr)
        return url
    filename = safe_asset_name(url, resp.headers.get("content-type", ""))
    local_path = assets_dir / filename
    local_path.write_bytes(resp.content)
    manifest[url] = {
        "url": url,
        "local": f"assets/{filename}",
        "bytes": len(resp.content),
        "content_type": resp.headers.get("content-type", ""),
    }
    return manifest[url]["local"]


def rewrite_css_urls(css_text, css_url, assets_dir, manifest):
    def repl(match):
        raw = match.group(1).strip().strip("'\"")
        if raw.startswith(("data:", "#")):
            return match.group(0)
        abs_url = urljoin(css_url, raw)
        local = download_asset(abs_url, assets_dir, manifest)
        return f"url('{local}')"
    return re.sub(r"url\(([^)]+)\)", repl, css_text)


def rewrite_srcset(value, base_url, assets_dir, manifest):
    items = []
    for part in value.split(","):
        tokens = part.strip().split()
        if not tokens:
            continue
        abs_url = urljoin(base_url, tokens[0])
        tokens[0] = download_asset(abs_url, assets_dir, manifest)
        items.append(" ".join(tokens))
    return ", ".join(items)


def rewrite_html_assets(soup, base_url, assets_dir):
    manifest = {}

    for tag in soup.find_all(src=True):
        tag["src"] = download_asset(urljoin(base_url, tag["src"]), assets_dir, manifest)

    for tag in soup.find_all(srcset=True):
        tag["srcset"] = rewrite_srcset(tag["srcset"], base_url, assets_dir, manifest)

    for tag in soup.find_all(href=True):
        rel = {r.lower() for r in tag.get("rel", [])} if tag.get("rel") else set()
        should_fetch = tag.name == "link" and ("stylesheet" in rel or "icon" in rel or "preload" in rel)
        if tag.name in {"image", "use"}:
            should_fetch = True
        if should_fetch:
            abs_url = urljoin(base_url, tag["href"])
            if "stylesheet" in rel:
                try:
                    css_text = fetch(abs_url)
                    css_text = rewrite_css_urls(css_text, abs_url, assets_dir, manifest)
                    filename = safe_asset_name(abs_url, "text/css")
                    css_path = assets_dir / filename
                    css_path.write_text(css_text, encoding="utf-8")
                    manifest[abs_url] = {
                        "url": abs_url,
                        "local": f"assets/{filename}",
                        "bytes": len(css_text.encode("utf-8")),
                        "content_type": "text/css",
                    }
                    tag["href"] = manifest[abs_url]["local"]
                except Exception as exc:
                    print(f"CSS fetch failed: {abs_url}: {exc}", file=sys.stderr)
            else:
                tag["href"] = download_asset(abs_url, assets_dir, manifest)

    for tag in soup.find_all(attrs={"xlink:href": True}):
        tag["xlink:href"] = download_asset(urljoin(base_url, tag["xlink:href"]), assets_dir, manifest)

    return manifest


def section_index_map(soup):
    mapping = {}
    idx = 0
    for h2 in soup.find_all("h2"):
        text = h2.get_text(" ", strip=True)
        if any(k in text.lower() for k in SKIP_SECTION_KEYWORDS):
            break
        idx += 1
        mapping[h2] = idx
    return mapping


def nearest_section_index(node, h2_to_index):
    h2 = node.find_previous("h2")
    return h2_to_index.get(h2) if h2 else None


def extract_label(caption, node_id):
    match = re.search(r"\b(Figure|Table)\s*\d+\b", caption or "", flags=re.I)
    if match:
        return re.sub(r"\s+", " ", match.group(0)).title()
    id_match = re.search(r"\.([FT])(\d+)$", node_id or "")
    if id_match:
        return ("Figure" if id_match.group(1) == "F" else "Table") + " " + id_match.group(2)
    return ""


def clean_embedded_html(node, kind):
    frag = BeautifulSoup(str(node), "html.parser")
    for tag in frag.find_all(True):
        if tag.has_attr("style"):
            del tag["style"]
        if kind == "table":
            tag.attrs.pop("width", None)
            tag.attrs.pop("height", None)

    if kind == "table":
        unwrap_classes = {
            "ltx_transformed_outer", "ltx_transformed_inner", "ltx_inline-block",
            "ltx_flex_figure", "ltx_flex_cell", "ltx_figure_panel",
            "ltx_align_center", "ltx_centering",
        }
        for tag in list(frag.find_all(True)):
            classes = set(tag.get("class") or [])
            if classes & unwrap_classes and tag.name not in {"figure", "table", "thead", "tbody", "tr", "th", "td", "figcaption"}:
                tag.unwrap()
        for table in list(frag.find_all("table")):
            if table.find_parent(class_="table-scroll") is None:
                wrapper = frag.new_tag("div")
                wrapper["class"] = "table-scroll"
                table.wrap(wrapper)

    root = frag.find("figure") or frag.find("table") or frag
    return str(root)


def extract_figures(soup):
    h2_to_index = section_index_map(soup)
    candidates = []
    candidates.extend(soup.find_all("figure"))
    candidates.extend(soup.find_all(lambda tag: tag.name in {"div", "table"} and tag.get("class") and any("ltx_figure" in c or "ltx_table" in c for c in tag.get("class", []))))

    seen = set()
    figures = []
    section_counts = {}
    for node in candidates:
        if node.name != "figure" and node.find_parent("figure") is not None:
            continue
        key = node.get("id") or str(id(node))
        if key in seen:
            continue
        seen.add(key)
        caption_el = node.find("figcaption") or node.find(class_=re.compile(r"ltx_caption"))
        caption = caption_el.get_text(" ", strip=True) if caption_el else ""
        image_paths = []
        for img in node.find_all("img"):
            src = img.get("src")
            if src and not src.startswith(("data:", "http://", "https://")):
                image_paths.append(src)
        for image in node.find_all("image"):
            href = image.get("href") or image.get("xlink:href")
            if href and not href.startswith(("data:", "http://", "https://")):
                image_paths.append(href)
        if not image_paths and not caption and not node.find("table"):
            continue
        section_index = nearest_section_index(node, h2_to_index)
        section_counts[section_index] = section_counts.get(section_index, 0) + 1
        node_id = node.get("id", f"figure-{len(figures)+1}")
        classes = node.get("class") or []
        kind = "table" if node.name == "table" or "ltx_table" in classes or node.find("table") else "figure"
        figures.append({
            "id": node_id,
            "section_index": section_index,
            "ordinal_in_section": section_counts[section_index],
            "kind": kind,
            "label": extract_label(caption, node_id),
            "caption": caption,
            "images": list(dict.fromkeys(image_paths)),
            "html": clean_embedded_html(node, kind),
        })

    totals = {}
    for fig in figures:
        idx = fig.get("section_index")
        totals[idx] = totals.get(idx, 0) + 1
    seen_ord = {}
    for fig in figures:
        idx = fig.get("section_index")
        seen_ord[idx] = seen_ord.get(idx, 0) + 1
        fig["ordinal_in_section"] = seen_ord[idx]
        fig["total_in_section"] = totals[idx]
    return figures


def prepare(args):
    arxiv_id = extract_arxiv_id(args.paper)
    if not arxiv_id:
        raise SystemExit("Cannot extract arXiv ID. Provide an abs/html/pdf URL or bare ID.")

    info = get_abs_info(arxiv_id)
    html_text, html_url = fetch_arxiv_html(arxiv_id, info["links"].get("html"))
    info["links"]["html"] = html_url
    title_slug = sanitize_title(info.get("title") or arxiv_id)
    paper_dir = Path(args.output).expanduser().resolve() / title_slug
    assets_dir = paper_dir / "assets"
    paper_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    soup = BeautifulSoup(html_text, "html.parser")
    manifest = rewrite_html_assets(soup, html_url, assets_dir)
    figures = extract_figures(soup)

    original_html = paper_dir / f"{arxiv_id}_original_local.html"
    original_html.write_text(str(soup), encoding="utf-8")

    try:
        pdf_data = fetch(info["links"]["pdf"], binary=True)
        (paper_dir / f"{arxiv_id}.pdf").write_bytes(pdf_data)
    except Exception as exc:
        print(f"PDF fetch failed: {exc}", file=sys.stderr)

    metadata = {
        **info,
        "title_slug": title_slug,
        "paper_dir": str(paper_dir),
        "original_local_html": str(original_html),
        "asset_count": len(manifest),
        "figure_count": len(figures),
    }
    (paper_dir / f"{arxiv_id}_static_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    (paper_dir / f"{arxiv_id}_asset_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (paper_dir / f"{arxiv_id}_figures.json").write_text(json.dumps(figures, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(metadata, ensure_ascii=False, indent=2))


def inline_md(text):
    placeholders = []

    def hold(match):
        placeholders.append(match.group(0))
        return f"@@PLACEHOLDER_{len(placeholders)-1}@@"

    text = re.sub(r"\$[^$]+\$", hold, text)
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    for i, value in enumerate(placeholders):
        text = text.replace(f"@@PLACEHOLDER_{i}@@", html.escape(value))
    return text


def figure_html(figures):
    if not figures:
        return ""
    parts = ["<div class=\"paper-figures\">"]
    for fig in figures:
        label = fig.get("label") or fig.get("id", "figure")
        parts.append(f'<div class="paper-figure" data-label="{html.escape(label)}">')
        embedded = fig.get("html")
        if embedded:
            parts.append(embedded)
        else:
            parts.append("<figure>")
            for src in fig.get("images", []):
                parts.append(f'<img src="{html.escape(src)}" loading="lazy" alt="{html.escape(fig.get("caption") or label)}">')
            if fig.get("caption"):
                parts.append(f'<figcaption>{html.escape(fig["caption"])}</figcaption>')
            parts.append("</figure>")
        parts.append("</div>")
    parts.append("</div>")
    return "\n".join(parts)


def render_markdown_block(kind, payload):
    if kind == "heading":
        level, text = payload
        return f"<h{level}>{inline_md(text)}</h{level}>"
    if kind == "paragraph":
        return f"<p>{inline_md(payload)}</p>"
    if kind == "list":
        items = "".join(f"<li>{inline_md(item)}</li>" for item in payload)
        return f"<ul>{items}</ul>"
    if kind == "hr":
        return "<hr>"
    return ""


def label_variants(label):
    if not label:
        return []
    variants = {label, label.replace(" ", "")}
    m = re.match(r"(Figure|Table)\s*(\d+)", label, flags=re.I)
    if m:
        zh = "图" if m.group(1).lower() == "figure" else "表"
        variants.update({f"{zh}{m.group(2)}", f"{zh} {m.group(2)}"})
    return list(variants)


def block_mentions_figure(block, fig):
    if block[0] not in {"paragraph", "list"}:
        return False
    text = " ".join(block[1]) if block[0] == "list" else block[1]
    compact = re.sub(r"\s+", "", text).lower()
    for variant in label_variants(fig.get("label", "")):
        if variant.lower() in text.lower() or re.sub(r"\s+", "", variant).lower() in compact:
            return True
    return False


def render_section_blocks(blocks, figures):
    out = []
    body_indices = [i for i, b in enumerate(blocks) if b[0] in {"paragraph", "list"}]
    insert_after = {i: [] for i in range(len(blocks))}
    used = set()

    for fig_i, fig in enumerate(figures):
        for block_i, block in enumerate(blocks):
            if block_mentions_figure(block, fig):
                insert_after.setdefault(block_i, []).append(fig)
                used.add(fig_i)
                break

    leftovers = [fig for i, fig in enumerate(figures) if i not in used]
    for fig in leftovers:
        if body_indices:
            ordinal = int(fig.get("ordinal_in_section") or 1)
            total = int(fig.get("total_in_section") or len(leftovers) or 1)
            pos = min(len(body_indices) - 1, max(0, round((ordinal / (total + 1)) * (len(body_indices) - 1))))
            block_i = body_indices[pos]
        else:
            block_i = len(blocks) - 1
        insert_after.setdefault(block_i, []).append(fig)

    for i, block in enumerate(blocks):
        out.append(render_markdown_block(block[0], block[1]))
        if insert_after.get(i):
            out.append(figure_html(insert_after[i]))
    return out


def markdown_to_html(md_text, figures_by_section):
    out = []
    current_section_num = None
    current_blocks = []
    paragraph = []
    list_items = []

    def close_paragraph():
        nonlocal paragraph
        if paragraph:
            current_blocks.append(("paragraph", " ".join(paragraph)))
            paragraph = []

    def close_list():
        nonlocal list_items
        if list_items:
            current_blocks.append(("list", list_items))
            list_items = []

    def flush_section():
        nonlocal current_blocks
        figures = figures_by_section.get(current_section_num, []) if current_section_num else []
        out.extend(render_section_blocks(current_blocks, figures))
        current_blocks = []

    for raw in md_text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            close_paragraph(); close_list(); continue
        if re.match(r"^---+$", line.strip()):
            close_paragraph(); close_list(); current_blocks.append(("hr", None)); continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            close_paragraph(); close_list()
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if level == 2:
                flush_section()
                m = re.match(r"(\d+)\.", text)
                current_section_num = int(m.group(1)) if m else None
            current_blocks.append(("heading", (level, text)))
            continue
        item = re.match(r"^-\s+(.+)$", line)
        if item:
            close_paragraph()
            list_items.append(item.group(1).strip())
            continue
        close_list()
        paragraph.append(line.strip())

    close_paragraph(); close_list(); flush_section()
    return "\n".join(out)


def load_first_json(paper_dir, suffix):
    files = sorted(Path(paper_dir).glob(f"*{suffix}"))
    if not files:
        return None
    return json.loads(files[0].read_text(encoding="utf-8"))


def build(args):
    paper_dir = Path(args.paper_dir).expanduser().resolve()
    md_path = Path(args.markdown).expanduser().resolve()
    if not paper_dir.exists():
        raise SystemExit(f"paper_dir not found: {paper_dir}")
    if not md_path.exists():
        raise SystemExit(f"markdown not found: {md_path}")

    metadata = load_first_json(paper_dir, "_static_metadata.json") or {}
    figures = load_first_json(paper_dir, "_figures.json") or []
    by_section = {}
    unassigned = []
    for fig in figures:
        idx = fig.get("section_index")
        if idx:
            by_section.setdefault(int(idx), []).append(fig)
        else:
            unassigned.append(fig)

    body = markdown_to_html(md_path.read_text(encoding="utf-8"), by_section)
    if unassigned:
        body += "\n<h2>未归属图表</h2>\n" + figure_html(unassigned)

    title = args.title or metadata.get("title") or md_path.stem
    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} - 中文静态版</title>
<style>
:root {{ --bg:#f7f8fb; --paper:#ffffff; --text:#172033; --muted:#5d6678; --line:#e6e9f0; --accent:#2454d6; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font:16px/1.72 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Noto Sans SC","PingFang SC",Arial,sans-serif; }}
.page {{ max-width: min(96vw, 1400px); margin: 0 auto; padding: 32px 18px 64px; }}
.paper {{ background:var(--paper); border:1px solid var(--line); border-radius:18px; box-shadow:0 10px 30px rgba(20,32,64,.08); padding:42px 52px; overflow:visible; }}
h1 {{ font-size:2.1rem; line-height:1.25; margin:0 0 1rem; }}
h2 {{ margin-top:2.4rem; padding-top:1.2rem; border-top:1px solid var(--line); font-size:1.55rem; }}
h3 {{ margin-top:1.5rem; font-size:1.18rem; }}
p {{ margin: .8rem 0; }}
ul {{ padding-left:1.4rem; }}
hr {{ border:0; border-top:1px solid var(--line); margin:2rem 0; }}
code {{ background:#f0f3fa; padding:.12rem .32rem; border-radius:5px; }}
a {{ color:var(--accent); }}
.meta {{ color:var(--muted); margin-bottom:1.5rem; }}
.paper-figures {{ margin: 1.25rem 0 1.75rem; padding: 1rem; border:1px dashed var(--line); border-radius:14px; background:#fafbff; overflow:visible; }}
.paper-figure {{ margin:1rem 0; text-align:center; overflow:visible; }}
.paper-figure figure {{ margin:0 auto; max-width:100%; overflow:visible; }}
.paper-figure img {{ max-width:100%; height:auto; border-radius:10px; border:1px solid var(--line); background:#fff; }}
.paper-figure figcaption, .ltx_caption {{ margin:.55rem 0 .75rem; color:var(--muted); font-size:.92rem; text-align:left; }}
.table-scroll {{ width:100%; max-width:100%; overflow-x:auto; overflow-y:visible; -webkit-overflow-scrolling:touch; margin:.8rem 0; padding-bottom:.35rem; }}
.paper-figure table, .ltx_tabular {{ border-collapse:collapse; margin:0 auto; width:max-content; min-width:100%; max-width:none; table-layout:auto; font-size:.88rem; line-height:1.35; white-space:normal; }}
.paper-figure th, .paper-figure td, .ltx_td {{ border:1px solid var(--line); padding:.38rem .55rem; vertical-align:middle; word-break:normal; overflow-wrap:normal; }}
.paper-figure th, .ltx_th {{ background:#eef2ff; font-weight:700; }}
.ltx_transformed_outer {{ max-width:100% !important; width:auto !important; height:auto !important; overflow:visible !important; }}
.ltx_transformed_inner {{ display:inline !important; transform:none !important; }}
@media (max-width:720px) {{ .paper {{ padding:24px 18px; border-radius:12px; }} h1 {{ font-size:1.65rem; }} }}
</style>
<script>
window.MathJax = {{ tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$','$$'], ['\\\\[','\\\\]']], processEscapes: true }}, svg: {{ fontCache: 'global' }} }};
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
<main class="page">
<article class="paper">
<div class="meta">本地中文静态 HTML · arXiv ID: {html.escape(str(metadata.get('arxiv_id', '')))}</div>
{body}
</article>
</main>
</body>
</html>
"""

    output = Path(args.output).expanduser().resolve() if args.output else paper_dir / "index.html"
    output.write_text(html_doc, encoding="utf-8")
    print(str(output))


def main():
    parser = argparse.ArgumentParser(description="Prepare arXiv assets and build Chinese static HTML.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_prepare = sub.add_parser("prepare", help="Fetch arXiv HTML/PDF and localize assets.")
    p_prepare.add_argument("paper", help="arXiv abs/html/pdf URL or bare ID.")
    p_prepare.add_argument("-o", "--output", default="~/papers", help="Output parent directory.")
    p_prepare.set_defaults(func=prepare)

    p_build = sub.add_parser("build", help="Build local Chinese static HTML from Chinese Markdown.")
    p_build.add_argument("paper_dir", help="Directory created by prepare.")
    p_build.add_argument("--markdown", "--md", required=True, help="Chinese Markdown document path.")
    p_build.add_argument("--output", help="Output HTML path. Defaults to paper_dir/index.html.")
    p_build.add_argument("--title", help="Override HTML title.")
    p_build.set_defaults(func=build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
