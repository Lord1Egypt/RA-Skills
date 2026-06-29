#!/usr/bin/env python3
"""
extract.py - Fetch a URL and immediately extract something useful, in one
command. The canonical AI-agent workflow: "give me the text / links / title
of this page" without writing a 3-stage shell pipeline.

Internally this is `get.py` followed by a small built-in HTML parser. Pure
Python 3 stdlib.

Modes:
    --mode text     (default) fetch the URL and return plain readable text
                    (scripts / styles stripped, block tags become newlines)
    --mode title    just the <title> of the page (one line on stdout)
    --mode meta     return a JSON object of <meta> tags + title + canonical
    --mode links    list every <a href=...> link the page contains
    --mode images   list every <img src=...> the page contains
    --mode tables   return a JSON array, one entry per <table>, with rows
    --mode raw      just dump the raw HTML (useful with --output)

Usage:
    extract.py URL [--mode MODE] [--output PATH] [options]

Options:
    --output PATH        write extraction to PATH instead of stdout
    --header 'Name: V'   custom HTTP header (may repeat)
    --bearer TOKEN       Authorization: Bearer TOKEN
    --timeout SECONDS    request timeout (default: 30)
    --retries N          retry count for 5xx/429 (default: 3)
    --insecure           skip TLS verification
    --absolute-urls      rewrite link / image paths to absolute URLs
                         (using the response URL as the base)
    --json               JSON-format the output (where applicable)
    --quiet              suppress the request summary on stderr
    -h, --help           show this help

Exit codes:
    0  one or more items extracted (and HTTP 2xx)
    1  zero items extracted
    2  bad arguments / bad URL / unsafe path / network error / non-2xx response
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.parse
from html.parser import HTMLParser
from typing import Dict, List, Optional, Tuple

from _common import (DEFAULT_TIMEOUT, fetch, parse_headers, safe_path,
                     safe_url, write_or_print)


BLOCK_TAGS = {"p", "div", "br", "li", "tr", "td", "th",
              "h1", "h2", "h3", "h4", "h5", "h6",
              "section", "article", "header", "footer",
              "ul", "ol", "table", "blockquote", "pre", "hr"}
DROP_CONTENT = {"script", "style", "noscript"}


class _TextStripper(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: List[str] = []
        self.drop_depth = 0

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        if t in DROP_CONTENT:
            self.drop_depth += 1
            return
        if t in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        t = tag.lower()
        if t in DROP_CONTENT:
            self.drop_depth = max(0, self.drop_depth - 1)
            return
        if t in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.drop_depth > 0:
            return
        self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        raw = re.sub(r"[ \t]+", " ", raw)
        lines = [ln.strip() for ln in raw.splitlines()]
        out: List[str] = []
        blank = 0
        for ln in lines:
            if not ln:
                blank += 1
                if blank <= 1:
                    out.append("")
            else:
                blank = 0
                out.append(ln)
        while out and not out[0]: out.pop(0)
        while out and not out[-1]: out.pop()
        return "\n".join(out) + ("\n" if out else "")


class _MetaExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.canonical = ""
        self.metas: Dict[str, str] = {}
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        adict = dict(attrs)
        if t == "title":
            self._in_title = True
        elif t == "meta":
            name = (adict.get("name") or adict.get("property")
                    or adict.get("itemprop") or "")
            content = adict.get("content", "")
            if name and content:
                self.metas[name] = content
        elif t == "link":
            if (adict.get("rel") or "").lower() == "canonical":
                self.canonical = adict.get("href", "") or ""

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


class _LinksImagesExtractor(HTMLParser):
    def __init__(self, kind: str) -> None:
        super().__init__(convert_charrefs=True)
        self.kind = kind  # 'links' or 'images'
        self.items: List[Dict[str, str]] = []
        self._cur_link_attrs: Optional[Dict[str, str]] = None
        self._cur_link_text: List[str] = []

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        adict = dict(attrs)
        if self.kind == "links" and t == "a" and "href" in adict:
            self._cur_link_attrs = adict
            self._cur_link_text = []
        elif self.kind == "images" and t == "img":
            self.items.append({"src": adict.get("src", "") or "",
                               "alt": adict.get("alt", "") or ""})

    def handle_endtag(self, tag):
        if self.kind == "links" and tag.lower() == "a" and self._cur_link_attrs is not None:
            text = re.sub(r"\s+", " ", "".join(self._cur_link_text)).strip()
            self.items.append({
                "href": self._cur_link_attrs.get("href", "") or "",
                "text": text,
                "title": self._cur_link_attrs.get("title", "") or "",
            })
            self._cur_link_attrs = None
            self._cur_link_text = []

    def handle_data(self, data):
        if self._cur_link_attrs is not None:
            self._cur_link_text.append(data)


class _TableExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: List[List[List[str]]] = []
        self._cur_table: Optional[List[List[str]]] = None
        self._cur_row: Optional[List[str]] = None
        self._cur_cell: Optional[List[str]] = None

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        if t == "table":
            self._cur_table = []
        elif t == "tr" and self._cur_table is not None:
            self._cur_row = []
        elif t in ("td", "th") and self._cur_row is not None:
            self._cur_cell = []

    def handle_endtag(self, tag):
        t = tag.lower()
        if t == "table" and self._cur_table is not None:
            if self._cur_table:
                self.tables.append(self._cur_table)
            self._cur_table = None
        elif t == "tr" and self._cur_row is not None:
            if self._cur_table is not None:
                self._cur_table.append(self._cur_row)
            self._cur_row = None
        elif t in ("td", "th") and self._cur_cell is not None:
            text = re.sub(r"\s+", " ", "".join(self._cur_cell)).strip()
            if self._cur_row is not None:
                self._cur_row.append(text)
            self._cur_cell = None

    def handle_data(self, data):
        if self._cur_cell is not None:
            self._cur_cell.append(data)


def _absolutize(items: List[Dict[str, str]], base_url: str, key: str) -> None:
    for it in items:
        v = it.get(key, "")
        if v:
            it[key] = urllib.parse.urljoin(base_url, v)


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("url", nargs="?")
    p.add_argument("--mode", default="text",
                   choices=("text", "title", "meta", "links", "images",
                            "tables", "raw"))
    p.add_argument("--output")
    p.add_argument("--header", action="append", default=[])
    p.add_argument("--bearer")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    p.add_argument("--retries", type=int, default=3)
    p.add_argument("--insecure", action="store_true")
    p.add_argument("--absolute-urls", dest="absolute_urls", action="store_true")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.url:
        print(__doc__)
        return 0 if args.help else 2

    try:
        url = safe_url(args.url)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    try:
        headers = parse_headers(args.header)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if args.bearer:
        headers["Authorization"] = f"Bearer {args.bearer}"

    out_path = None
    if args.output:
        try:
            out_path = safe_path(args.output)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2

    try:
        status, resp_headers, body, trail = fetch(
            url, method="GET", headers=headers,
            timeout=args.timeout, retries=args.retries,
            follow_redirects=True, allow_insecure=args.insecure,
        )
    except (urllib.error.URLError, OSError) as e:
        print(f"Error: network error: {e}", file=sys.stderr)
        return 2

    if not (200 <= status < 300):
        print(f"Error: HTTP {status}", file=sys.stderr)
        return 2

    final_url = trail[-1][1] if trail else url
    try:
        html_text = body.decode("utf-8", errors="replace")
    except Exception:
        html_text = ""

    n_items = 0

    if args.mode == "raw":
        write_or_print(out_path, body, text=False)
        n_items = 1
    elif args.mode == "text":
        s = _TextStripper()
        s.feed(html_text); s.close()
        result = s.text()
        write_or_print(out_path, result.encode("utf-8"), text=True)
        n_items = 1 if result.strip() else 0
    elif args.mode == "title":
        m = _MetaExtractor()
        m.feed(html_text); m.close()
        title = re.sub(r"\s+", " ", m.title).strip()
        write_or_print(out_path, (title + "\n").encode("utf-8"), text=True)
        n_items = 1 if title else 0
    elif args.mode == "meta":
        m = _MetaExtractor()
        m.feed(html_text); m.close()
        obj = {
            "url": final_url,
            "title": re.sub(r"\s+", " ", m.title).strip(),
            "canonical": (urllib.parse.urljoin(final_url, m.canonical)
                          if args.absolute_urls and m.canonical else m.canonical),
            "meta": m.metas,
        }
        out = json.dumps(obj, indent=2, ensure_ascii=False)
        write_or_print(out_path, (out + "\n").encode("utf-8"), text=True)
        n_items = 1
    elif args.mode == "links":
        e = _LinksImagesExtractor("links")
        e.feed(html_text); e.close()
        if args.absolute_urls:
            _absolutize(e.items, final_url, "href")
        n_items = len(e.items)
        if args.as_json or (out_path and out_path.suffix.lower() == ".json"):
            data = json.dumps(e.items, indent=2, ensure_ascii=False)
            write_or_print(out_path, (data + "\n").encode("utf-8"), text=True)
        else:
            lines = [f"{it.get('href','')}\t{it.get('text','')}" for it in e.items]
            write_or_print(out_path, ("\n".join(lines) + "\n").encode("utf-8"),
                           text=True)
    elif args.mode == "images":
        e = _LinksImagesExtractor("images")
        e.feed(html_text); e.close()
        if args.absolute_urls:
            _absolutize(e.items, final_url, "src")
        n_items = len(e.items)
        if args.as_json or (out_path and out_path.suffix.lower() == ".json"):
            data = json.dumps(e.items, indent=2, ensure_ascii=False)
            write_or_print(out_path, (data + "\n").encode("utf-8"), text=True)
        else:
            lines = [f"{it.get('src','')}\t{it.get('alt','')}" for it in e.items]
            write_or_print(out_path, ("\n".join(lines) + "\n").encode("utf-8"),
                           text=True)
    elif args.mode == "tables":
        e = _TableExtractor()
        e.feed(html_text); e.close()
        n_items = len(e.tables)
        data = json.dumps(e.tables, indent=2, ensure_ascii=False)
        write_or_print(out_path, (data + "\n").encode("utf-8"), text=True)

    if not args.quiet:
        dest = f" -> {out_path}" if out_path else ""
        print(f"extract({args.mode}): {url} -> {status}, "
              f"{n_items} item(s){dest}", file=sys.stderr)

    return 0 if n_items > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
