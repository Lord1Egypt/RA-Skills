#!/usr/bin/env python3
"""
保存日报采集阶段的原始资讯文本。

用途：
1. 将搜索/抓取工具返回的原始文本落盘到 output/raw/{date}_{phase}.txt
2. 可选地直接抓取 URL，并把响应原文保存下来

设计原则：
- 不强制固定 JSON 结构
- 以纯文本分段记录为主
- 支持多次追加，逐步积累完整候选池
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "output" / "raw"


class HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self._in_title = False
        self._skip_depth = 0
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag in {"script", "style", "svg", "noscript", "nav", "footer", "header", "button"}:
            self._skip_depth += 1
            return
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            meta_name = (attrs_dict.get("name") or attrs_dict.get("property") or "").lower()
            if meta_name in {"description", "og:description", "twitter:description"}:
                content = attrs_dict.get("content") or ""
                if content and not self.meta_description:
                    self.meta_description = content.strip()
        if tag in {"p", "div", "article", "section", "main", "header", "footer", "li", "h1", "h2", "h3", "h4", "h5", "h6", "br"}:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "svg", "noscript", "nav", "footer", "header", "button"} and self._skip_depth > 0:
            self._skip_depth -= 1
            return
        if tag == "title":
            self._in_title = False
        if tag in {"p", "div", "article", "section", "main", "header", "footer", "li", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth > 0:
            return
        text = data.strip()
        if not text:
            return
        if self._in_title and not self.title:
            self.title = text
        self._chunks.append(text)

    def extract(self, raw_html: str) -> str:
        self.feed(raw_html)
        lines = []
        if self.title:
            lines.append(f"title: {self.title}")
        if self.meta_description:
            lines.append(f"description: {self.meta_description}")

        text = html.unescape(" ".join(self._chunks))
        text = re.sub(r"\s*\n\s*", "\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        text = re.sub(r"(?im)^skip to main content(?: skip to footer)?\s*$", "", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        if text:
            lines.append("")
            lines.append(text)
        return "\n".join(lines).strip()


def looks_like_html(content: str) -> bool:
    head = content[:2000].lower()
    return "<html" in head or "<body" in head or "<!doctype html" in head or "<head" in head


def normalize_content(content: str) -> str:
    if not looks_like_html(content):
        return content.strip()
    extractor = HTMLTextExtractor()
    extracted = extractor.extract(content)
    return extracted or content.strip()


def trim_noise(content: str) -> str:
    lines = [line.strip() for line in content.splitlines()]
    cleaned: list[str] = []
    stop_markers = {
        "related content",
        "footnotes",
    }
    skip_exact = {
        "read more",
        "skip to main content",
        "skip to footer",
    }

    for line in lines:
        if not line:
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue

        lowered = line.lower()
        if lowered in stop_markers:
            break
        if lowered in skip_exact:
            continue
        if lowered.startswith("01 / ") or lowered.endswith(" \\ anthropic"):
            continue
        cleaned.append(line)

    text = "\n".join(cleaned)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="保存原始资讯抓取文本")
    parser.add_argument("date", help="日报日期，例如 2026-03-23")
    parser.add_argument(
        "--phase",
        choices=("index", "detail"),
        default="index",
        help="采集阶段：index=候选池，detail=正文深抓，默认 index",
    )
    parser.add_argument("--output", help="输出文件路径，默认 output/raw/{date}_{phase}.txt")
    parser.add_argument("--append", action="store_true", help="追加写入已有文件")
    parser.add_argument("--section", default="capture", help="记录类型，例如 search/fetch/manual")
    parser.add_argument("--query", default="", help="本条记录对应的搜索词或抓取任务")
    parser.add_argument("--source", default="", help="来源名")
    parser.add_argument("--source-type", default="", help="来源类型，例如 official/media/community")
    parser.add_argument("--source-tier", default="", help="来源等级：tier-1(官方一手) / tier-2(主流媒体) / tier-3(社区自媒体)")
    parser.add_argument("--title", default="", help="原始标题")
    parser.add_argument("--url", default="", help="原始链接")
    parser.add_argument("--pub-date", default="", help="来源页面上的原始发布日期，格式 YYYY-MM-DD；无法确认时填 unknown")
    parser.add_argument("--language", default="", help="语言，例如 zh/en")
    parser.add_argument("--content", default="", help="直接传入原始文本内容")
    parser.add_argument("--content-file", help="从文件读取原始文本内容")
    parser.add_argument(
        "--fetch-url",
        action="store_true",
        help="如果提供了 --url 且未提供 content，则尝试直接抓取该 URL 的原始响应文本",
    )
    return parser.parse_args()


def load_content(args: argparse.Namespace) -> str:
    if args.content:
        return args.content

    if args.content_file:
        return Path(args.content_file).read_text(encoding="utf-8")

    if args.fetch_url and args.url:
        request = Request(
            args.url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; daily-raw-capture/1.0)"
            },
        )
        with urlopen(request, timeout=20) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            raw = response.read()
            return raw.decode(charset, errors="replace")

    if not sys.stdin.isatty():
        return sys.stdin.read()

    raise ValueError("未提供原始内容。请使用 --content、--content-file、stdin 或 --fetch-url。")


def render_block(args: argparse.Namespace, content: str) -> str:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    lines = [
        "=" * 80,
        f"captured_at: {now}",
        f"date: {args.date}",
        f"section: {args.section}",
    ]
    if args.query:
        lines.append(f"query: {args.query}")
    if args.source:
        lines.append(f"source: {args.source}")
    if args.source_type:
        lines.append(f"source_type: {args.source_type}")
    if args.source_tier:
        lines.append(f"source_tier: {args.source_tier}")
    if args.title:
        lines.append(f"title: {args.title}")
    if args.url:
        lines.append(f"url: {args.url}")
    if args.pub_date:
        lines.append(f"pub_date: {args.pub_date}")
    if args.language:
        lines.append(f"language: {args.language}")
    lines.extend(
        [
            "-" * 80,
            content.strip(),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    output_path = Path(args.output) if args.output else RAW_DIR / f"{args.date}_{args.phase}.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        content = load_content(args)
    except FileNotFoundError as exc:
        print(f"ERROR: 内容文件不存在: {exc}", file=sys.stderr)
        return 1
    except (HTTPError, URLError) as exc:
        print(f"ERROR: 抓取 URL 失败: {exc}", file=sys.stderr)
        return 1
    except TimeoutError:
        print("ERROR: 抓取 URL 超时", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    content = trim_noise(normalize_content(content))
    mode = "a" if args.append and output_path.exists() else "w"
    block = render_block(args, content)
    with output_path.open(mode, encoding="utf-8") as handle:
        if mode == "a":
            handle.write("\n")
        handle.write(block)

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
