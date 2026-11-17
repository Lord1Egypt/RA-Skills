#!/usr/bin/env python3
"""
aeo.py — make any static site answer-engine-citable.

Answer engines (Perplexity, ChatGPT search, Google AI Overviews) cite pages
that are easy to parse: structured data, clean text, and a machine-readable map
of the site. This tool adds those, idempotently, to plain HTML files. No build
system, no framework, Python 3 standard library only.

Subcommands
  audit    Score one or more pages for answer-engine readiness.
  schema   Inject Article/BlogPosting JSON-LD derived from the page's own head.
  faq      Inject FAQPage JSON-LD from question/answer pairs.
  md       Write a clean .md sibling of an HTML page (the text an engine quotes).
  llms     Generate /llms.txt, the map answer engines fetch to decide what to cite.
  sitemap  Generate /sitemap.xml from the HTML files in a directory.

Every write is idempotent: re-running skips work that is already done unless you
pass --force. Run with --dry-run first to see what would change.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

# ----------------------------------------------------------------------------
# HTML extraction
# ----------------------------------------------------------------------------


class _HeadParser(HTMLParser):
    """Pull the metadata an answer engine cares about out of a page's <head>
    and headings, plus a flag for whether each JSON-LD @type is already there."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self._in_title = False
        self.meta: dict[str, str] = {}        # name/property -> content
        self.canonical = ""
        self.h1: list[str] = []
        self.h2: list[str] = []
        self._cur_h = None
        self._h_buf: list[str] = []
        self.ld_types: set[str] = set()
        self._in_ld = False
        self._ld_buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key and "content" in a:
                self.meta[key.lower()] = a["content"]
        elif tag == "link" and a.get("rel", "").lower() == "canonical":
            self.canonical = a.get("href", "")
        elif tag in ("h1", "h2"):
            self._cur_h = tag
            self._h_buf = []
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._in_ld = True
            self._ld_buf = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2") and self._cur_h == tag:
            text = re.sub(r"\s+", " ", "".join(self._h_buf)).strip()
            if text:
                (self.h1 if tag == "h1" else self.h2).append(text)
            self._cur_h = None
        elif tag == "script" and self._in_ld:
            self._in_ld = False
            blob = "".join(self._ld_buf)
            for m in re.findall(r'"@type"\s*:\s*"([^"]+)"', blob):
                self.ld_types.add(m)

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)
        if self._cur_h:
            self._h_buf.append(data)
        if self._in_ld:
            self._ld_buf.append(data)

    @property
    def title(self) -> str:
        return re.sub(r"\s+", " ", "".join(self.title_parts)).strip()


def extract(path: str) -> dict:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    p = _HeadParser()
    p.feed(raw)
    m = p.meta
    title = p.title or (p.h1[0] if p.h1 else "")
    # strip a trailing " — Site" / " | Site" suffix for a cleaner headline
    headline = re.split(r"\s+[—|·]\s+", title)[0].strip() if title else ""
    return {
        "raw": raw,
        "title": title,
        "headline": p.h1[0] if p.h1 else headline,
        "description": m.get("description") or m.get("og:description") or "",
        "canonical": p.canonical or m.get("og:url") or "",
        "image": m.get("og:image") or m.get("twitter:image") or "",
        "author": m.get("author") or "",
        "published": (
            m.get("article:published_time")
            or m.get("datepublished")
            or ""
        ),
        "h2": p.h2,
        "ld_types": p.ld_types,
    }


# ----------------------------------------------------------------------------
# shared helpers
# ----------------------------------------------------------------------------


def _inject_before(raw: str, snippet: str) -> str:
    """Insert snippet just before </head>, falling back to </body> or EOF."""
    for needle in ("</head>", "</body>"):
        idx = raw.lower().rfind(needle)
        if idx != -1:
            return raw[:idx] + snippet + "\n" + raw[idx:]
    return raw + "\n" + snippet + "\n"


def _ld_block(obj: dict) -> str:
    body = json.dumps(obj, indent=2, ensure_ascii=False)
    return '<script type="application/ld+json">\n' + body + "\n</script>"


def _write(path: str, content: str, dry: bool) -> None:
    if dry:
        return
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def _iter_html(paths: list[str]):
    for p in paths:
        if os.path.isdir(p):
            for root, _dirs, files in os.walk(p):
                for f in sorted(files):
                    if f.endswith(".html"):
                        yield os.path.join(root, f)
        elif p.endswith(".html"):
            yield p


# ----------------------------------------------------------------------------
# schema
# ----------------------------------------------------------------------------


def cmd_schema(args) -> int:
    changed = 0
    for path in _iter_html(args.paths):
        data = extract(path)
        if ({"Article", "BlogPosting", "NewsArticle"} & data["ld_types"]) and not args.force:
            print(f"skip   {path}  (Article schema already present)")
            continue
        if not data["headline"]:
            print(f"WARN   {path}  (no <title>/<h1> to build a headline from)")
            continue
        obj = {
            "@context": "https://schema.org",
            "@type": args.type,
            "headline": data["headline"],
        }
        if data["description"]:
            obj["description"] = data["description"]
        url = data["canonical"] or (args.base.rstrip("/") + "/" + os.path.basename(path) if args.base else "")
        if url:
            obj["url"] = url
            obj["mainEntityOfPage"] = {"@type": "WebPage", "@id": url}
        if data["image"]:
            obj["image"] = data["image"]
        published = data["published"] or args.date
        if published:
            obj["datePublished"] = published
            obj["dateModified"] = published
        author = data["author"] or args.author
        if author:
            obj["author"] = {"@type": "Person", "name": author}
        if args.publisher:
            obj["publisher"] = {"@type": "Organization", "name": args.publisher}
        new = _inject_before(data["raw"], _ld_block(obj))
        _write(path, new, args.dry_run)
        changed += 1
        print(f"{'would add' if args.dry_run else 'added'} {args.type} JSON-LD  {path}")
    print(f"\n{changed} page(s) {'would be ' if args.dry_run else ''}updated.")
    return 0


# ----------------------------------------------------------------------------
# faq
# ----------------------------------------------------------------------------


def _parse_qa(items: list[str]) -> list[tuple[str, str]]:
    out = []
    for it in items:
        if "::" not in it:
            raise SystemExit(f"--qa expects 'Question::Answer', got: {it!r}")
        q, a = it.split("::", 1)
        out.append((q.strip(), a.strip()))
    return out


def cmd_faq(args) -> int:
    path = args.file
    data = extract(path)
    if "FAQPage" in data["ld_types"] and not args.force:
        print(f"skip   {path}  (FAQPage already present)")
        return 0
    qa = _parse_qa(args.qa)
    obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in qa
        ],
    }
    new = _inject_before(data["raw"], _ld_block(obj))
    _write(path, new, args.dry_run)
    print(f"{'would add' if args.dry_run else 'added'} FAQPage with {len(qa)} Q&A  {path}")
    return 0


# ----------------------------------------------------------------------------
# md sibling
# ----------------------------------------------------------------------------


class _TextParser(HTMLParser):
    """Render the readable body of a page to plain Markdown."""

    _SKIP = {"script", "style", "nav", "header", "footer", "noscript", "svg", "title", "head"}
    _BLOCK = {"p", "div", "section", "article", "li", "br", "tr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self._skip_depth = 0
        self._heading = None

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip_depth += 1
        elif tag in ("h1", "h2", "h3", "h4"):
            self._heading = "#" * int(tag[1])
            self.out.append("\n\n" + self._heading + " ")
        elif tag == "li":
            self.out.append("\n- ")
        elif tag in self._BLOCK:
            self.out.append("\n\n")

    def handle_endtag(self, tag):
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1
        elif tag in ("h1", "h2", "h3", "h4"):
            self._heading = None

    def handle_data(self, data):
        if self._skip_depth:
            return
        text = re.sub(r"[ \t]+", " ", data)
        if text.strip() or self.out and not self.out[-1].endswith("\n"):
            self.out.append(text)

    def render(self) -> str:
        text = "".join(self.out)
        text = re.sub(r"\n{3,}", "\n\n", text)
        lines = [ln.rstrip() for ln in text.splitlines()]
        return "\n".join(lines).strip() + "\n"


def cmd_md(args) -> int:
    changed = 0
    for path in _iter_html(args.paths):
        out_path = path[:-5] + ".md"
        if os.path.exists(out_path) and not args.force:
            print(f"skip   {out_path}  (already exists)")
            continue
        data = extract(path)
        tp = _TextParser()
        tp.feed(data["raw"])
        front = []
        if data["title"]:
            front.append(f"# {data['headline'] or data['title']}")
        if data["description"]:
            front.append(f"> {data['description']}")
        if data["canonical"]:
            front.append(f"_Source: {data['canonical']}_")
        body = ("\n\n".join(front) + "\n\n" + tp.render()) if front else tp.render()
        _write(out_path, body, args.dry_run)
        changed += 1
        print(f"{'would write' if args.dry_run else 'wrote'} {out_path}")
    print(f"\n{changed} sibling(s) {'would be ' if args.dry_run else ''}written.")
    return 0


# ----------------------------------------------------------------------------
# llms.txt
# ----------------------------------------------------------------------------


def cmd_llms(args) -> int:
    base = args.base.rstrip("/")
    rows = []
    for path in _iter_html([args.dir]):
        if os.path.basename(path) in ("index.html",) and not args.include_index:
            continue
        data = extract(path)
        rel = os.path.relpath(path, args.dir).replace(os.sep, "/")
        url = f"{base}/{rel}"
        title = data["headline"] or data["title"] or rel
        desc = data["description"]
        rows.append((url, title, desc))
    rows.sort(key=lambda r: r[0])
    lines = [f"# {args.site}", ""]
    if args.summary:
        lines += [f"> {args.summary}", ""]
    lines.append("## Pages")
    lines.append("")
    for url, title, desc in rows:
        lines.append(f"- [{title}]({url})" + (f": {desc}" if desc else ""))
    content = "\n".join(lines) + "\n"
    out = args.out or os.path.join(args.dir, "llms.txt")
    _write(out, content, args.dry_run)
    print(f"{'would write' if args.dry_run else 'wrote'} {out}  ({len(rows)} pages)")
    return 0


# ----------------------------------------------------------------------------
# sitemap.xml
# ----------------------------------------------------------------------------


def cmd_sitemap(args) -> int:
    base = args.base.rstrip("/")
    urls = []
    for path in _iter_html([args.dir]):
        rel = os.path.relpath(path, args.dir).replace(os.sep, "/")
        if rel.endswith("index.html"):
            rel = rel[: -len("index.html")]
        urls.append(f"{base}/{rel}")
    urls = sorted(set(urls))
    body = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        body.append(f"  <url><loc>{html.escape(u)}</loc></url>")
    body.append("</urlset>")
    content = "\n".join(body) + "\n"
    out = args.out or os.path.join(args.dir, "sitemap.xml")
    _write(out, content, args.dry_run)
    print(f"{'would write' if args.dry_run else 'wrote'} {out}  ({len(urls)} urls)")
    return 0


# ----------------------------------------------------------------------------
# audit
# ----------------------------------------------------------------------------


CHECKS = [
    ("title", "has a <title>"),
    ("description", "has a meta description"),
    ("canonical", "has a canonical URL"),
    ("image", "has an og:image"),
    ("article", "has Article/BlogPosting JSON-LD"),
    ("faq", "has FAQPage JSON-LD"),
    ("md", "has a clean .md sibling"),
]


def _score(path: str) -> tuple[int, dict]:
    data = extract(path)
    res = {
        "title": bool(data["title"]),
        "description": bool(data["description"]),
        "canonical": bool(data["canonical"]),
        "image": bool(data["image"]),
        "article": bool({"Article", "BlogPosting", "NewsArticle"} & data["ld_types"]),
        "faq": "FAQPage" in data["ld_types"],
        "md": os.path.exists(path[:-5] + ".md"),
    }
    got = sum(1 for k, _ in CHECKS if res[k])
    return round(100 * got / len(CHECKS)), res


def cmd_audit(args) -> int:
    pages = list(_iter_html(args.paths))
    if not pages:
        print("no .html files found")
        return 1
    total = 0
    print(f"{'SCORE':>5}  PAGE")
    print("-" * 60)
    misses: dict[str, int] = {k: 0 for k, _ in CHECKS}
    for path in pages:
        sc, res = _score(path)
        total += sc
        flags = "".join("✓" if res[k] else "·" for k, _ in CHECKS)
        print(f"{sc:>4}%  {flags}  {path}")
        for k, _ in CHECKS:
            if not res[k]:
                misses[k] += 1
    print("-" * 60)
    print("legend: " + "  ".join(f"{i+1}={d}" for i, (_, d) in enumerate(CHECKS)))
    print(f"\naverage score: {round(total / len(pages))}%  across {len(pages)} page(s)")
    todo = [(label, n) for (k, label), n in zip(CHECKS, [misses[k] for k, _ in CHECKS]) if n]
    if todo:
        print("\nbiggest wins:")
        for label, n in sorted(todo, key=lambda x: -x[1]):
            print(f"  {n:>3} page(s) miss: {label}")
    return 0


# ----------------------------------------------------------------------------
# cli
# ----------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="aeo", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("audit", help="score pages for answer-engine readiness")
    a.add_argument("paths", nargs="+")
    a.set_defaults(func=cmd_audit)

    s = sub.add_parser("schema", help="inject Article/BlogPosting JSON-LD")
    s.add_argument("paths", nargs="+")
    s.add_argument("--type", default="BlogPosting", choices=["BlogPosting", "Article", "NewsArticle"])
    s.add_argument("--base", default="", help="base URL, used to build url when no canonical")
    s.add_argument("--author", default="")
    s.add_argument("--publisher", default="")
    s.add_argument("--date", default="", help="fallback datePublished (YYYY-MM-DD)")
    s.add_argument("--force", action="store_true")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(func=cmd_schema)

    f = sub.add_parser("faq", help="inject FAQPage JSON-LD")
    f.add_argument("file")
    f.add_argument("--qa", nargs="+", required=True, metavar="Q::A")
    f.add_argument("--force", action="store_true")
    f.add_argument("--dry-run", action="store_true")
    f.set_defaults(func=cmd_faq)

    m = sub.add_parser("md", help="write clean .md sibling(s)")
    m.add_argument("paths", nargs="+")
    m.add_argument("--force", action="store_true")
    m.add_argument("--dry-run", action="store_true")
    m.set_defaults(func=cmd_md)

    l = sub.add_parser("llms", help="generate llms.txt")
    l.add_argument("dir")
    l.add_argument("--base", required=True, help="site base URL, e.g. https://example.com")
    l.add_argument("--site", default="Site", help="site name for the heading")
    l.add_argument("--summary", default="", help="one-line site summary")
    l.add_argument("--out", default="")
    l.add_argument("--include-index", action="store_true")
    l.add_argument("--dry-run", action="store_true")
    l.set_defaults(func=cmd_llms)

    sm = sub.add_parser("sitemap", help="generate sitemap.xml")
    sm.add_argument("dir")
    sm.add_argument("--base", required=True)
    sm.add_argument("--out", default="")
    sm.add_argument("--dry-run", action="store_true")
    sm.set_defaults(func=cmd_sitemap)

    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
