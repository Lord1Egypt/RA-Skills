#!/usr/bin/env python3
"""
markdown.py - Strip / extract / convert Markdown.

Three modes:

    --mode text     strip Markdown markup, leave plain text (default).
                    Removes headings hashes, list bullets, blockquote markers,
                    inline `code`, **bold**, _italic_, links (keeps anchor text
                    or URL via --link-style), images (keeps alt text or drops),
                    HTML tags, horizontal rules.

    --mode html     render a minimal HTML approximation (headings, paragraphs,
                    lists, blockquotes, code blocks, links, images, bold,
                    italic, inline code, horizontal rules). NOT a full
                    CommonMark renderer; intended for previewing snippets.

    --mode extract  pull structured pieces out as JSON / TSV:
                    headings, links, images, code-blocks, list-items.
                    Use --extract heads,links,images,code,lists (default: all).

Usage:
    markdown.py INPUT OUTPUT [--mode MODE] [options]

Options:
    --mode text|html|extract     default: text
    --link-style anchor|url|both for --mode text, how to render [text](url).
                                 anchor (default) keeps the visible text;
                                 url keeps the URL; both becomes 'text (url)'.
    --keep-images                for --mode text, keep '[image: alt]' marker
    --extract LIST               comma-separated kinds for --mode extract
    --json                       --mode extract writes JSON; without this it
                                 writes a simple TSV (kind <TAB> value).
    --quiet                      suppress the summary
    -h, --help                   show this help

Exit codes:
    0  success
    1  extract mode produced no items
    2  bad arguments / unsafe path / missing file / unsupported mode
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

from _common import read_text, safe_path, write_text


# ---- Patterns (kept intentionally pragmatic) -------------------------------

H_RE       = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.MULTILINE)
FENCE_RE   = re.compile(r"^```([^\n`]*)\n([\s\S]*?)^```\s*$", re.MULTILINE)
INDENT_CODE_RE = re.compile(r"(?:^ {4}.*(?:\n|$))+", re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
IMG_RE     = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LINK_RE    = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
BOLD_RE    = re.compile(r"\*\*([^*]+)\*\*|__([^_]+)__")
ITALIC_RE  = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)|(?<!_)_([^_\n]+)_(?!_)")
LIST_RE    = re.compile(r"^[ \t]*(?:[-*+]|\d+\.)[ \t]+(.+)$", re.MULTILINE)
BLOCKQ_RE  = re.compile(r"^>\s?", re.MULTILINE)
HR_RE      = re.compile(r"^[ \t]*(?:-{3,}|\*{3,}|_{3,})[ \t]*$", re.MULTILINE)
HTML_TAG_RE = re.compile(r"<[^>]+>")


def to_plain(md: str, link_style: str = "anchor", keep_images: bool = False) -> str:
    text = md
    # Remove fenced code blocks but keep their body
    def _fence(m):
        return m.group(2)
    text = FENCE_RE.sub(_fence, text)
    # Replace images
    if keep_images:
        text = IMG_RE.sub(lambda m: f"[image: {m.group(1) or ''}]", text)
    else:
        text = IMG_RE.sub("", text)
    # Replace links
    if link_style == "url":
        text = LINK_RE.sub(lambda m: m.group(2), text)
    elif link_style == "both":
        text = LINK_RE.sub(lambda m: f"{m.group(1)} ({m.group(2)})", text)
    else:
        text = LINK_RE.sub(lambda m: m.group(1), text)
    # Bold/italic
    text = BOLD_RE.sub(lambda m: m.group(1) or m.group(2) or "", text)
    text = ITALIC_RE.sub(lambda m: m.group(1) or m.group(2) or "", text)
    # Inline code
    text = INLINE_CODE_RE.sub(lambda m: m.group(1), text)
    # Headings: drop the leading hashes
    text = H_RE.sub(lambda m: m.group(2), text)
    # Lists: drop the bullet
    text = LIST_RE.sub(lambda m: m.group(1), text)
    # Blockquote markers
    text = BLOCKQ_RE.sub("", text)
    # Horizontal rules
    text = HR_RE.sub("", text)
    # Strip raw HTML
    text = HTML_TAG_RE.sub("", text)
    # Collapse 3+ blank lines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def to_html(md: str) -> str:
    """Minimal Markdown -> HTML renderer."""
    lines = md.splitlines()
    out: List[str] = []
    i = 0
    in_list = None  # 'ul' or 'ol'
    in_blockquote = False
    in_code = False
    code_lang = ""

    def close_list():
        nonlocal in_list
        if in_list:
            out.append(f"</{in_list}>")
            in_list = None

    def close_blockquote():
        nonlocal in_blockquote
        if in_blockquote:
            out.append("</blockquote>")
            in_blockquote = False

    def inline(s: str) -> str:
        # Escape raw HTML inside lines (very basic)
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # Restore inline code first to protect it from further markdown
        # (do a simple two-pass: find spans, replace with sentinel, run others, restore)
        placeholders: Dict[str, str] = {}

        def stash_code(m):
            key = f"\x00CODE{len(placeholders)}\x00"
            placeholders[key] = f"<code>{m.group(1)}</code>"
            return key
        s = re.sub(r"`([^`]+)`", stash_code, s)
        s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)",
                   lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}">', s)
        s = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)",
                   lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)
        s = re.sub(r"(?<!_)_([^_\n]+)_(?!_)", r"<em>\1</em>", s)
        for k, v in placeholders.items():
            s = s.replace(k, v)
        return s

    while i < len(lines):
        line = lines[i]

        # Fenced code blocks
        m = re.match(r"^```(.*)$", line)
        if m and not in_code:
            close_list(); close_blockquote()
            in_code = True
            code_lang = m.group(1).strip()
            lang = f' class="language-{code_lang}"' if code_lang else ""
            out.append(f"<pre><code{lang}>")
            i += 1
            continue
        if in_code:
            if line.startswith("```"):
                out.append("</code></pre>")
                in_code = False
            else:
                out.append(line.replace("&", "&amp;").replace("<", "&lt;")
                           .replace(">", "&gt;"))
            i += 1
            continue

        # Headings
        m = H_RE.match(line)
        if m:
            close_list(); close_blockquote()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        # Horizontal rule
        if HR_RE.match(line):
            close_list(); close_blockquote()
            out.append("<hr>")
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            close_list()
            if not in_blockquote:
                out.append("<blockquote>")
                in_blockquote = True
            content = line.lstrip(">").lstrip()
            out.append(f"<p>{inline(content)}</p>")
            i += 1
            continue
        else:
            close_blockquote()

        # Lists
        m_ul = re.match(r"^[ \t]*[-*+][ \t]+(.+)$", line)
        m_ol = re.match(r"^[ \t]*\d+\.[ \t]+(.+)$", line)
        if m_ul or m_ol:
            tag = "ul" if m_ul else "ol"
            if in_list and in_list != tag:
                close_list()
            if not in_list:
                out.append(f"<{tag}>")
                in_list = tag
            item = (m_ul or m_ol).group(1)
            out.append(f"  <li>{inline(item)}</li>")
            i += 1
            continue
        else:
            close_list()

        # Blank line
        if not line.strip():
            i += 1
            continue

        # Paragraph: gather contiguous non-empty lines
        para = [line]
        while i + 1 < len(lines) and lines[i + 1].strip() \
                and not re.match(r"^(#{1,6} |```|>|[-*+] |\d+\. )", lines[i + 1]) \
                and not HR_RE.match(lines[i + 1]):
            i += 1
            para.append(lines[i])
        i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")

    close_list(); close_blockquote()
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out) + "\n"


def extract_items(md: str, kinds: List[str]) -> List[Dict[str, str]]:
    items: List[Dict[str, str]] = []
    if "heads" in kinds or "headings" in kinds:
        for m in H_RE.finditer(md):
            items.append({"kind": "heading", "level": str(len(m.group(1))),
                          "value": m.group(2)})
    if "links" in kinds:
        for m in LINK_RE.finditer(md):
            items.append({"kind": "link", "text": m.group(1), "url": m.group(2)})
    if "images" in kinds:
        for m in IMG_RE.finditer(md):
            items.append({"kind": "image", "alt": m.group(1), "url": m.group(2)})
    if "code" in kinds:
        for m in FENCE_RE.finditer(md):
            items.append({"kind": "code", "language": m.group(1).strip(),
                          "value": m.group(2)})
    if "lists" in kinds:
        for m in LIST_RE.finditer(md):
            items.append({"kind": "list-item", "value": m.group(1)})
    return items


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--mode", choices=("text", "html", "extract"), default="text")
    p.add_argument("--link-style", dest="link_style",
                   choices=("anchor", "url", "both"), default="anchor")
    p.add_argument("--keep-images", dest="keep_images", action="store_true")
    p.add_argument("--extract", default="heads,links,images,code,lists")
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

    md = read_text(in_path)

    n_items = 0
    if args.mode == "text":
        result = to_plain(md, args.link_style, args.keep_images)
        write_text(out_path, result)
        n_items = result.count("\n")
    elif args.mode == "html":
        result = to_html(md)
        write_text(out_path, result)
        n_items = result.count("\n")
    else:  # extract
        kinds = [k.strip() for k in args.extract.split(",") if k.strip()]
        valid = {"heads", "headings", "links", "images", "code", "lists"}
        bad = [k for k in kinds if k not in valid]
        if bad:
            print(f"Error: unknown extract kinds: {','.join(bad)}. "
                  f"Allowed: heads, links, images, code, lists", file=sys.stderr)
            return 2
        items = extract_items(md, kinds)
        n_items = len(items)
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
                # Header
                f.write("kind\tvalue\textra\n")
                for it in items:
                    kind = it.get("kind", "")
                    # Pick the most informative "value" per kind
                    if kind == "link":
                        value = it.get("text", "")
                        extra_keys = ["url"]
                    elif kind == "image":
                        value = it.get("alt", "")
                        extra_keys = ["url"]
                    elif kind == "code":
                        value = (it.get("value", "")
                                 .replace("\t", " ")
                                 .replace("\n", "\\n"))
                        extra_keys = ["language"]
                    else:
                        value = it.get("value", "")
                        extra_keys = [k for k in it
                                      if k not in ("kind", "value")]
                    extra = " ".join(f"{k}={it[k]}" for k in extra_keys
                                     if k in it)
                    f.write(f"{kind}\t{value}\t{extra}\n")

    if not args.quiet:
        if args.mode == "extract":
            print(f"Markdown(extract): {n_items} item(s) -> {out_path}",
                  file=sys.stderr)
        else:
            print(f"Markdown({args.mode}): {len(md)} chars in -> {out_path}",
                  file=sys.stderr)
    return 0 if (args.mode != "extract" or n_items > 0) else 1


if __name__ == "__main__":
    sys.exit(main())
