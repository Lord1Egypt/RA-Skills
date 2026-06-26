#!/usr/bin/env python3
"""
htmlstrip.py - Strip HTML tags from a file (or extract structured pieces:
links, images, headings, tables). Built on Python's stdlib html.parser, so
no BeautifulSoup, no lxml, no remote calls.

Agents constantly scrape web pages and end up with raw HTML when what they
actually want is plain text, or a list of links / images / headings. This
script does exactly that.

Three modes:

    --mode text     (default) strip every tag, collapse whitespace, leave
                    plain readable text. `<br>`, `<p>`, `<li>`, `<h1>` etc.
                    become line breaks. `<script>` / `<style>` content is
                    removed entirely.

    --mode html     strip a configurable set of tags but keep the rest of the
                    structure. Useful for sanitizing untrusted HTML before
                    further processing. Defaults to removing
                    `script,style,iframe,object,embed,form,input` and the
                    `on*` event-handler attributes from every remaining tag.

    --mode extract  pull structured pieces out as JSON / JSONL / TSV.
                    Default kinds: links, images, headings, tables.
                    Configure with --extract links,images,headings,tables.

Usage:
    htmlstrip.py INPUT OUTPUT [options]

Options:
    --mode text|html|extract     (default: text)
    --strip-tags TAG[,TAG2...]   for --mode html, override the default
                                 strip-list (default: script,style,iframe,
                                 object,embed,form,input)
    --keep-links                 for --mode text, render <a href=...>text</a>
                                 as 'text (href)' instead of just 'text'
                                 (useful for downstream link extraction)
    --extract LIST               for --mode extract, comma-separated kinds:
                                 links, images, headings, tables (default: all)
    --json                       in extract mode, emit JSON instead of TSV
    --quiet                      suppress the summary on stderr
    -h, --help                   show this help

Exit codes:
    0  success
    1  extract mode produced zero items (or input was empty)
    2  bad arguments / unsafe path / missing file / unsupported mode /
       unknown extract kind
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from _common import read_text, safe_path, write_text


# Tags that introduce a hard line break in --mode text rendering
BLOCK_TAGS = {
    "p", "div", "br", "li", "tr", "td", "th",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "section", "article", "header", "footer", "nav", "main",
    "ul", "ol", "table", "thead", "tbody", "tfoot",
    "blockquote", "pre", "hr",
}
# Tags whose content should be dropped entirely (not just the tag stripped)
DROP_CONTENT = {"script", "style", "noscript"}
# Tags to render as a heading marker in text mode (no markup, just a blank line)
HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}


# ---------------- TEXT MODE ----------------

class TextStripper(HTMLParser):
    """Convert HTML to plain text, preserving readable structure."""

    def __init__(self, keep_links: bool = False):
        super().__init__(convert_charrefs=True)
        self.parts: List[str] = []
        self.drop_depth = 0
        self.in_link = False
        self.link_href = ""
        self.link_text_start = 0
        self.keep_links = keep_links

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        if tag in DROP_CONTENT:
            self.drop_depth += 1
            return
        if tag in BLOCK_TAGS:
            self.parts.append("\n")
        if tag in HEADING_TAGS:
            self.parts.append("\n")  # extra blank line before headings
        if tag == "a" and self.keep_links:
            self.in_link = True
            self.link_href = ""
            for k, v in attrs:
                if k.lower() == "href":
                    self.link_href = v or ""
                    break
            self.link_text_start = len("".join(self.parts))

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in DROP_CONTENT:
            self.drop_depth = max(0, self.drop_depth - 1)
            return
        if tag in BLOCK_TAGS:
            self.parts.append("\n")
        if tag == "a" and self.in_link and self.keep_links:
            self.in_link = False
            if self.link_href:
                self.parts.append(f" ({self.link_href})")

    def handle_startendtag(self, tag: str, attrs) -> None:
        # Self-closing tags like <br/>, <hr/>, <img/>
        if tag.lower() in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.drop_depth > 0:
            return
        self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        # Collapse runs of spaces/tabs (but keep newlines)
        raw = re.sub(r"[ \t]+", " ", raw)
        # Trim each line
        lines = [ln.strip() for ln in raw.splitlines()]
        # Collapse 3+ blank lines into 2
        out: List[str] = []
        blank_run = 0
        for ln in lines:
            if not ln:
                blank_run += 1
                if blank_run <= 2:
                    out.append("")
            else:
                blank_run = 0
                out.append(ln)
        # Strip leading/trailing blank lines
        while out and not out[0]:
            out.pop(0)
        while out and not out[-1]:
            out.pop()
        return "\n".join(out) + "\n"


# ---------------- HTML SANITIZE MODE ----------------

class TagStripper(HTMLParser):
    """Remove a configurable set of tags entirely (content + tag), and strip
    on* event-handler attributes from every other tag. Keeps the rest of the
    HTML intact."""

    def __init__(self, strip_tags: set):
        super().__init__(convert_charrefs=False)
        self.strip_tags = {t.lower() for t in strip_tags}
        self.drop_depth = 0
        self.out: List[str] = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in self.strip_tags:
            self.drop_depth += 1
            return
        clean_attrs = [(k, v) for k, v in attrs
                       if not k.lower().startswith("on")
                       and k.lower() != "style"]
        attr_str = "".join(
            f' {k}="{html.escape(v, quote=True)}"' if v is not None else f" {k}"
            for k, v in clean_attrs
        )
        self.out.append(f"<{tag}{attr_str}>")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.strip_tags:
            self.drop_depth = max(0, self.drop_depth - 1)
            return
        self.out.append(f"</{tag}>")

    def handle_startendtag(self, tag, attrs):
        tag = tag.lower()
        if tag in self.strip_tags:
            return
        clean_attrs = [(k, v) for k, v in attrs
                       if not k.lower().startswith("on")
                       and k.lower() != "style"]
        attr_str = "".join(
            f' {k}="{html.escape(v, quote=True)}"' if v is not None else f" {k}"
            for k, v in clean_attrs
        )
        self.out.append(f"<{tag}{attr_str} />")

    def handle_data(self, data):
        if self.drop_depth > 0:
            return
        self.out.append(data)

    def handle_entityref(self, name):
        if self.drop_depth > 0:
            return
        self.out.append(f"&{name};")

    def handle_charref(self, name):
        if self.drop_depth > 0:
            return
        self.out.append(f"&#{name};")

    def result(self) -> str:
        return "".join(self.out)


# ---------------- EXTRACT MODE ----------------

class StructuredExtractor(HTMLParser):
    """Pull links / images / headings / tables out of HTML."""

    def __init__(self, kinds: set):
        super().__init__(convert_charrefs=True)
        self.kinds = kinds
        self.items: List[Dict[str, str]] = []
        self._stack: List[Tuple[str, dict]] = []
        self._text_buf: List[str] = []
        self._heading_level = 0
        self._in_table = 0
        self._table_rows: List[List[str]] = []
        self._row_cells: List[str] = []
        self._cell_buf: List[str] = []

    def _push_text(self) -> str:
        s = "".join(self._text_buf).strip()
        s = re.sub(r"\s+", " ", s)
        return s

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        adict = dict(attrs)
        if tag == "a" and "links" in self.kinds:
            self._stack.append(("a", adict))
            self._text_buf = []
        elif tag == "img" and "images" in self.kinds:
            self.items.append({
                "kind": "image",
                "src": adict.get("src", "") or "",
                "alt": adict.get("alt", "") or "",
            })
        elif tag in HEADING_TAGS and "headings" in self.kinds:
            self._heading_level = int(tag[1])
            self._text_buf = []
            self._stack.append((tag, adict))
        elif tag == "table" and "tables" in self.kinds:
            self._in_table += 1
            self._table_rows = []
        elif tag == "tr" and self._in_table:
            self._row_cells = []
        elif tag in ("td", "th") and self._in_table:
            self._cell_buf = []

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "a" and self._stack and self._stack[-1][0] == "a":
            _, adict = self._stack.pop()
            self.items.append({
                "kind": "link",
                "href": adict.get("href", "") or "",
                "text": self._push_text(),
            })
            self._text_buf = []
        elif tag in HEADING_TAGS and self._stack and self._stack[-1][0] == tag:
            self._stack.pop()
            self.items.append({
                "kind": "heading",
                "level": str(self._heading_level),
                "text": self._push_text(),
            })
            self._text_buf = []
            self._heading_level = 0
        elif tag == "table" and self._in_table:
            self._in_table -= 1
            if self._table_rows:
                self.items.append({
                    "kind": "table",
                    "rows": json.dumps(self._table_rows, ensure_ascii=False),
                    "n_rows": str(len(self._table_rows)),
                    "n_cols": str(max((len(r) for r in self._table_rows), default=0)),
                })
        elif tag == "tr" and self._in_table and self._row_cells:
            self._table_rows.append(self._row_cells)
            self._row_cells = []
        elif tag in ("td", "th") and self._in_table:
            cell_text = re.sub(r"\s+", " ", "".join(self._cell_buf)).strip()
            self._row_cells.append(cell_text)
            self._cell_buf = []

    def handle_data(self, data):
        if self._stack and self._stack[-1][0] in (("a",) + tuple(HEADING_TAGS)):
            self._text_buf.append(data)
        if self._in_table:
            self._cell_buf.append(data)


# ---------------- MAIN ----------------

def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--mode", choices=("text", "html", "extract"), default="text")
    p.add_argument("--strip-tags", dest="strip_tags",
                   default="script,style,iframe,object,embed,form,input")
    p.add_argument("--keep-links", dest="keep_links", action="store_true")
    p.add_argument("--extract", default="links,images,headings,tables")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input or not args.output:
        print(__doc__)
        return 0 if args.help else 2

    try:
        in_path = safe_path(args.input)
        out_path = safe_path(args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2

    html_text = read_text(in_path)

    if args.mode == "text":
        s = TextStripper(keep_links=args.keep_links)
        s.feed(html_text)
        s.close()
        result = s.text()
        write_text(out_path, result)
        n_items = result.count("\n")
        if not args.quiet:
            print(f"htmlstrip(text): {len(html_text)} chars in -> "
                  f"{len(result)} chars out -> {out_path}", file=sys.stderr)
        return 0 if result.strip() else 1

    if args.mode == "html":
        strip_set = {t.strip() for t in args.strip_tags.split(",") if t.strip()}
        s = TagStripper(strip_set)
        s.feed(html_text)
        s.close()
        result = s.result()
        write_text(out_path, result)
        if not args.quiet:
            print(f"htmlstrip(html): stripped {','.join(sorted(strip_set))} "
                  f"+ on*/style attrs -> {out_path}", file=sys.stderr)
        return 0

    # extract
    kinds = {k.strip() for k in args.extract.split(",") if k.strip()}
    valid = {"links", "images", "headings", "tables"}
    bad = [k for k in kinds if k not in valid]
    if bad:
        print(f"Error: unknown extract kinds: {','.join(bad)}. "
              f"Allowed: links, images, headings, tables", file=sys.stderr)
        return 2
    e = StructuredExtractor(kinds)
    e.feed(html_text)
    e.close()
    items = e.items
    out_path.parent.mkdir(parents=True, exist_ok=True)
    ext = out_path.suffix.lower()

    if args.as_json or ext == ".json":
        out_path.write_text(json.dumps(items, indent=2, ensure_ascii=False),
                            encoding="utf-8")
    elif ext == ".jsonl":
        with out_path.open("w", encoding="utf-8") as f:
            for it in items:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")
    else:
        with out_path.open("w", encoding="utf-8") as f:
            f.write("kind\tprimary\tsecondary\n")
            for it in items:
                kind = it.get("kind", "")
                if kind == "link":
                    f.write(f"link\t{it.get('href','')}\t{it.get('text','')}\n")
                elif kind == "image":
                    f.write(f"image\t{it.get('src','')}\t{it.get('alt','')}\n")
                elif kind == "heading":
                    f.write(f"heading\t{it.get('text','')}\tlevel={it.get('level','')}\n")
                elif kind == "table":
                    f.write(f"table\t{it.get('n_rows','0')}x{it.get('n_cols','0')}\t{it.get('rows','')}\n")

    if not args.quiet:
        print(f"htmlstrip(extract): {len(items)} item(s) -> {out_path}",
              file=sys.stderr)
    return 0 if items else 1


if __name__ == "__main__":
    sys.exit(main())
