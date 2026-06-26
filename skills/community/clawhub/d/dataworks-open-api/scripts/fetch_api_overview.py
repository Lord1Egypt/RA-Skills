#!/usr/bin/env python3
"""Fetch DataWorks API overview from the official Alibaba Cloud help docs.

Dynamically curls the help page, extracts the API list from
window.__ICE_PAGE_PROPS__.docDetailData.storeData.data.content,
parses the HTML tables, and outputs a structured markdown file.

Usage:
    python scripts/fetch_api_overview.py
    python scripts/fetch_api_overview.py --url <custom_help_url>
    python scripts/fetch_api_overview.py --output-dir output/alicloud-dataworks

Env:
- FETCH_TIMEOUT (seconds, default: 30)
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import urllib.request
from html.parser import HTMLParser

DEFAULT_PRODUCT_CODE = "dataworks-public"
DEFAULT_VERSION = "2024-05-18"
DEFAULT_URL = (
    f"https://help.aliyun.com/zh/dataworks/developer-reference"
    f"/api-{DEFAULT_PRODUCT_CODE}-{DEFAULT_VERSION}-overview"
)
OUTPUT_DIR = pathlib.Path("output/dataworks-open-api")


def fetch_page(url: str, timeout: int) -> str:
    """Fetch page HTML. Tries urllib first, falls back to curl on SSL errors."""
    import ssl
    import subprocess

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    }

    # Try with default SSL context first
    for ctx in [None, ssl.create_default_context(), ssl._create_unverified_context()]:
        try:
            req = urllib.request.Request(url, headers=headers)
            kwargs: dict = {"timeout": timeout}
            if ctx is not None:
                kwargs["context"] = ctx
            with urllib.request.urlopen(req, **kwargs) as resp:
                return resp.read().decode("utf-8")
        except (urllib.error.URLError, ssl.SSLError):
            continue

    # Fallback: use curl
    print("urllib SSL failed, falling back to curl...")
    result = subprocess.run(
        ["curl", "-fsSL", "-H", f"User-Agent: {headers['User-Agent']}", url],
        capture_output=True, text=True, timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl failed ({result.returncode}): {result.stderr}")
    return result.stdout


def extract_doc_content(html: str) -> str:
    """Extract content from window.__ICE_PAGE_PROPS__."""
    match = re.search(
        r"window\.__ICE_PAGE_PROPS__\s*=\s*(\{.*?\});?\s*</script>",
        html,
        re.DOTALL,
    )
    if not match:
        raise ValueError("Could not find window.__ICE_PAGE_PROPS__ in page")

    data = json.loads(match.group(1))

    # Navigate: docDetailData.storeData.data.content (primary)
    #       or: docDetailData.data.content (fallback)
    detail = data.get("docDetailData", {})
    content = (
        detail.get("storeData", {}).get("data", {}).get("content", "")
        or detail.get("data", {}).get("content", "")
    )
    if not content:
        raise ValueError(
            "content field is empty. "
            f"Available top-level keys: {list(detail.keys())}"
        )
    return content


class _APITableParser(HTMLParser):
    """Parse API tables from the help doc HTML content."""

    def __init__(self) -> None:
        super().__init__()
        self._in_h2 = False
        self._in_h3 = False
        self._in_td = False
        self._text = ""
        self._row: list[str] = []
        self._in_tr = False
        self._current_section: str | None = None
        self._rows: list[tuple[list[str], str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "h2":
            self._in_h2 = True
            self._text = ""
        elif tag == "h3":
            self._in_h3 = True
            self._text = ""
        elif tag == "tr":
            self._in_tr = True
            self._row = []
        elif tag == "td":
            self._in_td = True
            self._text = ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2" and self._in_h2:
            self._in_h2 = False
            t = self._text.strip()
            if t and "SDK" not in t:
                self._current_section = t
        elif tag == "h3" and self._in_h3:
            self._in_h3 = False
            t = self._text.strip()
            if t:
                self._current_section = t
        elif tag == "td":
            self._in_td = False
            self._row.append(self._text.strip())
        elif tag == "tr" and self._in_tr:
            self._in_tr = False
            if self._row and len(self._row) >= 2:
                self._rows.append((list(self._row), self._current_section))

    def handle_data(self, data: str) -> None:
        if self._in_h2 or self._in_h3 or self._in_td:
            self._text += data

    def get_grouped(self) -> dict[str, list[list[str]]]:
        from collections import OrderedDict
        grouped: dict[str, list[list[str]]] = OrderedDict()
        for row, section in self._rows:
            if not section:
                continue
            if section not in grouped:
                grouped[section] = []
            grouped[section].append(row)
        return grouped


def parse_api_tables(html_content: str) -> dict[str, list[list[str]]]:
    parser = _APITableParser()
    parser.feed(html_content)
    return parser.get_grouped()


def build_markdown(grouped: dict[str, list[list[str]]], version: str = DEFAULT_VERSION) -> str:
    lines = [f"# DataWorks API Overview ({version})", ""]

    total_apis = 0
    for section, rows in grouped.items():
        api_rows = [r for r in rows if len(r) >= 2 and r[0] != "API"]
        if not api_rows:
            continue
        total_apis += len(api_rows)
        lines.append(f"## {section} ({len(api_rows)} APIs)")
        lines.append("")
        lines.append("| API | 描述 |")
        lines.append("|-----|------|")
        for row in api_rows:
            lines.append(f"| {row[0]} | {row[1]} |")
        lines.append("")

    lines.insert(2, f"Total: {total_apis} APIs across {len(grouped)} categories")
    lines.insert(3, "")
    return "\n".join(lines) + "\n"


def build_json(grouped: dict[str, list[list[str]]]) -> list[dict]:
    result = []
    for section, rows in grouped.items():
        apis = []
        for row in rows:
            if len(row) >= 2 and row[0] != "API":
                apis.append({"name": row[0], "description": row[1]})
        if apis:
            result.append({"category": section, "count": len(apis), "apis": apis})
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch DataWorks API overview from official help docs"
    )
    parser.add_argument("--url", default=DEFAULT_URL, help="Help doc URL")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    args = parser.parse_args()

    timeout = int(os.getenv("FETCH_TIMEOUT", "30"))
    output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching: {args.url}")
    page_html = fetch_page(args.url, timeout)
    print(f"Page size: {len(page_html):,} bytes")

    doc_content = extract_doc_content(page_html)
    print(f"Doc content: {len(doc_content):,} chars")

    grouped = parse_api_tables(doc_content)

    total = sum(
        len([r for r in rows if len(r) >= 2 and r[0] != "API"])
        for rows in grouped.values()
    )
    print(f"Found: {total} APIs across {len(grouped)} categories")
    for section, rows in grouped.items():
        count = len([r for r in rows if len(r) >= 2 and r[0] != "API"])
        print(f"  {section}: {count} APIs")

    md_file = output_dir / "api_overview.md"
    md_file.write_text(build_markdown(grouped), encoding="utf-8")
    print(f"\nSaved: {md_file}")

    json_file = output_dir / "api_overview.json"
    json_data = build_json(grouped)
    json_file.write_text(
        json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Saved: {json_file}")


if __name__ == "__main__":
    main()
