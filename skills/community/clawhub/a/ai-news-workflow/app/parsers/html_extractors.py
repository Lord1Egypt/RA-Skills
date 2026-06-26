from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup


SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")


@dataclass
class ExtractedArticle:
    title: str
    publish_time: Optional[datetime]
    content_text: str


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    return text.strip()


def parse_datetime_cn(text: str) -> Optional[datetime]:
    """
    尝试解析中文常见日期格式：
    2026-03-03
    2026/03/03
    2026年03月03日
    可按需继续扩展
    """
    if not text:
        return None
    t = text.strip()

    patterns = [
        r"(\d{4})[-/\.](\d{1,2})[-/\.](\d{1,2})",
        r"(\d{4})年(\d{1,2})月(\d{1,2})日",
    ]
    for p in patterns:
        m = re.search(p, t)
        if m:
            y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            return datetime(y, mo, d, 0, 0, 0, tzinfo=SHANGHAI_TZ)
    return None


def extract_article_by_selectors(
    html: str,
    title_selector: str | None,
    date_selector: str | None,
    content_selector: str | None,
) -> ExtractedArticle:
    soup = BeautifulSoup(html, "lxml")

    # 标题
    title = ""
    if title_selector:
        node = soup.select_one(title_selector)
        title = clean_text(node.get_text(" ", strip=True) if node else "")
    if not title:
        # fallback
        h1 = soup.find("h1")
        title = clean_text(h1.get_text(" ", strip=True) if h1 else "")

    # 时间
    publish_time = None
    date_text = ""
    if date_selector:
        node = soup.select_one(date_selector)
        date_text = clean_text(node.get_text(" ", strip=True) if node else "")
    if date_text:
        publish_time = parse_datetime_cn(date_text)

    # 正文
    content_text = ""
    if content_selector:
        node = soup.select_one(content_selector)
        content_text = clean_text(node.get_text("\n", strip=True) if node else "")
    if not content_text:
        # fallback：取 body 里较大段落（粗略）
        body = soup.find("body")
        content_text = clean_text(body.get_text("\n", strip=True) if body else "")

    return ExtractedArticle(
        title=title or "Untitled",
        publish_time=publish_time,
        content_text=content_text,
    )