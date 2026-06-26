#!/usr/bin/env python3
"""
Minimal web article extractor for content-alchemy.

Fetches a URL, extracts the main text heuristically, and returns structured JSON
that can be fed into the content transformation workflow.
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0 Safari/537.36"
)

BLOCK_TAGS = {"p", "li", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6"}
SKIP_TAGS = {"script", "style", "noscript", "svg", "iframe", "form", "button"}


@dataclass
class ExtractionResult:
    url: str
    title: str | None
    site_name: str | None
    author: str | None
    published_at: str | None
    text: str
    word_count: int
    block_count: int
    truncated: bool
    extraction_method: str


class TextBlockParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._current_tag: str | None = None
        self._buffer: list[str] = []
        self.blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag in SKIP_TAGS:
            self._skip_depth += 1
            return
        if self._skip_depth > 0:
            return
        if tag in BLOCK_TAGS:
            self._flush_buffer()
            self._current_tag = tag

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1
            return
        if self._skip_depth > 0:
            return
        if tag in BLOCK_TAGS:
            self._flush_buffer()
            self._current_tag = None

    def handle_data(self, data: str) -> None:
        if self._skip_depth > 0:
            return
        normalized = normalize_whitespace(data)
        if normalized:
            self._buffer.append(normalized)

    def _flush_buffer(self) -> None:
        if not self._buffer:
            return
        block = normalize_whitespace(" ".join(self._buffer))
        self._buffer.clear()
        if block and len(block) >= 30:
            self.blocks.append(block)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract readable article text from a web page.")
    parser.add_argument("url", help="Web URL to fetch and extract")
    parser.add_argument("--output", help="Optional JSON output path")
    parser.add_argument(
        "--max-chars",
        type=int,
        default=18000,
        help="Maximum number of characters to keep in extracted text",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="Network timeout in seconds",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate verification for troubleshooting only",
    )
    return parser.parse_args()


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", unescape(text)).strip()


def fetch_html(url: str, timeout: int, insecure: bool) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    context = ssl._create_unverified_context() if insecure else ssl.create_default_context()
    with urlopen(request, timeout=timeout, context=context) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def find_meta(html: str, attr_name: str, attr_value: str) -> str | None:
    pattern = re.compile(
        rf'<meta[^>]+{attr_name}=["\']{re.escape(attr_value)}["\'][^>]+content=["\'](.*?)["\']',
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(html)
    if match:
        return normalize_whitespace(match.group(1))
    return None


def extract_title(html: str) -> str | None:
    for candidate in (
        find_meta(html, "property", "og:title"),
        find_meta(html, "name", "twitter:title"),
    ):
        if candidate:
            return candidate
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if match:
        return normalize_whitespace(match.group(1))
    return None


def extract_site_name(html: str, url: str) -> str | None:
    return find_meta(html, "property", "og:site_name") or urlparse(url).netloc


def extract_author(html: str) -> str | None:
    return (
        find_meta(html, "name", "author")
        or find_meta(html, "property", "article:author")
        or find_meta(html, "name", "dc.creator")
    )


def extract_published_at(html: str) -> str | None:
    return (
        find_meta(html, "property", "article:published_time")
        or find_meta(html, "name", "pubdate")
        or find_meta(html, "name", "date")
    )


def remove_noise_sections(html: str) -> str:
    patterns = [
        r"<script\b.*?</script>",
        r"<style\b.*?</style>",
        r"<noscript\b.*?</noscript>",
        r"<svg\b.*?</svg>",
        r"<iframe\b.*?</iframe>",
        r"<nav\b.*?</nav>",
        r"<footer\b.*?</footer>",
        r"<header\b.*?</header>",
        r"<aside\b.*?</aside>",
        r"<form\b.*?</form>",
        r"<!--.*?-->",
    ]
    cleaned = html
    for pattern in patterns:
        cleaned = re.sub(pattern, " ", cleaned, flags=re.IGNORECASE | re.DOTALL)
    return cleaned


def pick_primary_fragment(html: str) -> tuple[str, str]:
    candidates: list[tuple[str, str]] = []
    for tag in ("article", "main", "body"):
        matches = re.findall(
            rf"<{tag}\b.*?>.*?</{tag}>",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        for match in matches:
            candidates.append((tag, match))
    if not candidates:
        return html, "full_html"
    tag, fragment = max(candidates, key=lambda item: len(item[1]))
    return fragment, tag


def dedupe_blocks(blocks: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for block in blocks:
        normalized = normalize_whitespace(block)
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def fallback_line_extraction(html: str) -> list[str]:
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"</?(p|div|section|article|main|li|blockquote|h1|h2|h3|h4|h5|h6|tr|td)\b[^>]*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text, flags=re.IGNORECASE)
    lines = [normalize_whitespace(line) for line in text.splitlines()]
    return dedupe_blocks(line for line in lines if len(line) >= 30)


def extract_text(html: str, max_chars: int) -> tuple[str, int, int, bool, str]:
    cleaned = remove_noise_sections(html)
    fragment, method = pick_primary_fragment(cleaned)
    parser = TextBlockParser()
    parser.feed(fragment)
    blocks = dedupe_blocks(parser.blocks)
    if len(blocks) < 3:
        fallback_blocks = fallback_line_extraction(fragment)
        if len(fallback_blocks) > len(blocks):
            blocks = fallback_blocks
            method = f"{method}+line_fallback"
    text = "\n\n".join(blocks)
    truncated = False
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(" ", 1)[0].rstrip() + " ..."
        truncated = True
    return text, len(text.split()), len(blocks), truncated, method


def build_result(url: str, html: str, max_chars: int) -> ExtractionResult:
    text, word_count, block_count, truncated, method = extract_text(html, max_chars)
    return ExtractionResult(
        url=url,
        title=extract_title(html),
        site_name=extract_site_name(html, url),
        author=extract_author(html),
        published_at=extract_published_at(html),
        text=text,
        word_count=word_count,
        block_count=block_count,
        truncated=truncated,
        extraction_method=method,
    )


def result_to_dict(result: ExtractionResult) -> dict[str, object]:
    return {
        "status": "ok",
        "url": result.url,
        "title": result.title,
        "site_name": result.site_name,
        "author": result.author,
        "published_at": result.published_at,
        "text": result.text,
        "word_count": result.word_count,
        "block_count": result.block_count,
        "truncated": result.truncated,
        "extraction_method": result.extraction_method,
    }


def main() -> int:
    args = parse_args()
    try:
        html = fetch_html(args.url, args.timeout, args.insecure)
        result = build_result(args.url, html, args.max_chars)
        payload = json.dumps(result_to_dict(result), ensure_ascii=False, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as file:
                file.write(payload + "\n")
        print(payload)
        if result.word_count < 120:
            return 2
        return 0
    except HTTPError as exc:
        print(json.dumps({"status": "error", "error": f"HTTP {exc.code}", "url": args.url}, ensure_ascii=False))
        return 1
    except URLError as exc:
        print(json.dumps({"status": "error", "error": str(exc.reason), "url": args.url}, ensure_ascii=False))
        return 1
    except Exception as exc:  # pragma: no cover - safety net for CLI usage
        print(json.dumps({"status": "error", "error": str(exc), "url": args.url}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
