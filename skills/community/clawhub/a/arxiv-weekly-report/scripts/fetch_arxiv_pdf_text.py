#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fetch_arxiv_pdf_text.py

功能：
- 根据 arXiv abs 链接、PDF 链接或 arXiv id 下载 PDF
- 提取 PDF 全文文本
- 支持限制提取页数
- 默认输出 JSON，便于 OpenClaw skill 后续分析

依赖：
- pypdf

安装：
pip install pypdf

示例：
python3 fetch_arxiv_pdf_text.py --id 2503.12345 --max-pages 8 --pretty
python3 fetch_arxiv_pdf_text.py --abs-url https://arxiv.org/abs/2503.12345 --max-pages 10
python3 fetch_arxiv_pdf_text.py --pdf-url https://arxiv.org/pdf/2503.12345.pdf --save-text --pretty
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
from dataclasses import dataclass, asdict
from typing import Optional

try:
    from pypdf import PdfReader
except ImportError:
    print(
        "错误：缺少依赖 pypdf，请先执行 `pip install pypdf`。",
        file=sys.stderr,
    )
    sys.exit(10)


DEFAULT_PDF_DIR = os.path.expanduser(
    "~/.openclaw/skills/arxiv-weekly-report/cache/pdf"
)
DEFAULT_TEXT_DIR = os.path.expanduser(
    "~/.openclaw/skills/arxiv-weekly-report/cache/text"
)


@dataclass
class PdfTextResult:
    source_type: str
    arxiv_id: Optional[str]
    abs_url: Optional[str]
    pdf_url: str
    downloaded_pdf_path: str
    extracted_text_path: Optional[str]
    total_pages: int
    extracted_pages: int
    text_length: int
    text_preview: str
    full_text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="下载并提取 arXiv PDF 全文文本。"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--id", help="arXiv id，例如 2503.12345 或 2503.12345v1")
    group.add_argument("--abs-url", help="arXiv 摘要页链接，例如 https://arxiv.org/abs/2503.12345")
    group.add_argument("--pdf-url", help="arXiv PDF 链接，例如 https://arxiv.org/pdf/2503.12345.pdf")

    parser.add_argument(
        "--max-pages",
        type=int,
        default=12,
        help="最多提取前多少页，默认 12 页。传 0 表示提取全文。",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="下载超时时间（秒），默认 60。",
    )
    parser.add_argument(
        "--save-text",
        action="store_true",
        help="是否将提取文本保存到本地文件。",
    )
    parser.add_argument(
        "--pdf-dir",
        default=DEFAULT_PDF_DIR,
        help=f"PDF 缓存目录，默认 {DEFAULT_PDF_DIR}",
    )
    parser.add_argument(
        "--text-dir",
        default=DEFAULT_TEXT_DIR,
        help=f"文本输出目录，默认 {DEFAULT_TEXT_DIR}",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="是否美化 JSON 输出。",
    )
    parser.add_argument(
        "--preview-chars",
        type=int,
        default=1200,
        help="预览文本长度，默认 1200。",
    )
    return parser.parse_args()


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def normalize_arxiv_id(arxiv_id: str) -> str:
    value = arxiv_id.strip()
    value = value.replace("arXiv:", "")
    value = value.replace(".pdf", "")
    return value


def parse_arxiv_id_from_abs_url(url: str) -> Optional[str]:
    m = re.search(r"/abs/([^/?#]+)", url)
    return normalize_arxiv_id(m.group(1)) if m else None


def parse_arxiv_id_from_pdf_url(url: str) -> Optional[str]:
    m = re.search(r"/pdf/([^/?#]+?)(?:\.pdf)?$", url)
    return normalize_arxiv_id(m.group(1)) if m else None


def build_abs_url(arxiv_id: str) -> str:
    return f"https://arxiv.org/abs/{normalize_arxiv_id(arxiv_id)}"


def build_pdf_url(arxiv_id: str) -> str:
    return f"https://arxiv.org/pdf/{normalize_arxiv_id(arxiv_id)}.pdf"


def resolve_source(
    arxiv_id: Optional[str],
    abs_url: Optional[str],
    pdf_url: Optional[str],
) -> tuple[str, Optional[str], Optional[str], str]:
    """
    返回:
    (source_type, normalized_arxiv_id, normalized_abs_url, normalized_pdf_url)
    """
    if arxiv_id:
        aid = normalize_arxiv_id(arxiv_id)
        return "id", aid, build_abs_url(aid), build_pdf_url(aid)

    if abs_url:
        aid = parse_arxiv_id_from_abs_url(abs_url)
        if not aid:
            raise ValueError("无法从 abs-url 中解析 arXiv id。")
        return "abs_url", aid, build_abs_url(aid), build_pdf_url(aid)

    if pdf_url:
        aid = parse_arxiv_id_from_pdf_url(pdf_url)
        if aid:
            return "pdf_url", aid, build_abs_url(aid), build_pdf_url(aid)
        return "pdf_url", None, None, pdf_url.strip()

    raise ValueError("必须提供 --id 或 --abs-url 或 --pdf-url。")


def download_file(url: str, output_path: str, timeout: int = 60) -> None:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "OpenClaw-arxiv-weekly-report/0.1 (Python urllib)"
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(output_path, "wb") as f:
        f.write(resp.read())


def safe_filename(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name)


def hashed_name(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def extract_text_from_pdf(pdf_path: str, max_pages: int) -> tuple[str, int, int]:
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    if max_pages <= 0:
        pages_to_read = total_pages
    else:
        pages_to_read = min(max_pages, total_pages)

    texts = []
    for idx in range(pages_to_read):
        page = reader.pages[idx]
        page_text = page.extract_text() or ""
        page_text = page_text.strip()
        if page_text:
            texts.append(f"\n\n===== 第 {idx + 1} 页 =====\n{page_text}")

    full_text = "".join(texts).strip()
    return full_text, total_pages, pages_to_read


def write_text_file(text: str, text_dir: str, base_name: str) -> str:
    ensure_dir(text_dir)
    path = os.path.join(text_dir, f"{safe_filename(base_name)}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def main() -> int:
    args = parse_args()

    try:
        source_type, arxiv_id, abs_url, pdf_url = resolve_source(
            args.id, args.abs_url, args.pdf_url
        )
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        return 2

    ensure_dir(args.pdf_dir)

    if arxiv_id:
        base_name = arxiv_id
    else:
        base_name = f"arxiv_pdf_{hashed_name(pdf_url)}"

    pdf_path = os.path.join(args.pdf_dir, f"{safe_filename(base_name)}.pdf")

    try:
        if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) == 0:
            download_file(pdf_url, pdf_path, timeout=args.timeout)
    except Exception as e:
        print(f"错误：下载 PDF 失败：{e}", file=sys.stderr)
        return 3

    try:
        full_text, total_pages, extracted_pages = extract_text_from_pdf(
            pdf_path, args.max_pages
        )
    except Exception as e:
        print(f"错误：解析 PDF 失败：{e}", file=sys.stderr)
        return 4

    extracted_text_path = None
    if args.save_text:
        try:
            extracted_text_path = write_text_file(full_text, args.text_dir, base_name)
        except Exception as e:
            print(f"错误：写入文本文件失败：{e}", file=sys.stderr)
            return 5

    preview = full_text[: args.preview_chars]

    result = PdfTextResult(
        source_type=source_type,
        arxiv_id=arxiv_id,
        abs_url=abs_url,
        pdf_url=pdf_url,
        downloaded_pdf_path=pdf_path,
        extracted_text_path=extracted_text_path,
        total_pages=total_pages,
        extracted_pages=extracted_pages,
        text_length=len(full_text),
        text_preview=preview,
        full_text=full_text,
    )

    if args.pretty:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(asdict(result), ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())