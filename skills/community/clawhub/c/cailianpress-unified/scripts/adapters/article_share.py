from __future__ import annotations

import re

import requests

CLS_SHARE_URL_TEMPLATE = "https://api3.cls.cn/share/article/{article_id}?os=web&sv=8.4.6&app=CailianpressWeb"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.cls.cn/telegraph",
}


def build_share_url(article_id: int | str) -> str:
    return CLS_SHARE_URL_TEMPLATE.format(article_id=article_id)


def fetch_article_html(article_id: int | str, timeout: int = 20) -> str:
    response = requests.get(build_share_url(article_id), headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def extract_article_title(html: str) -> str:
    match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    return _clean_html_text(match.group(1)).replace("_财联社", "").strip()


def extract_article_content(html: str) -> str:
    patterns = [
        r'<div[^>]*class="[^"]*detail-content[^"]*"[^>]*>(.*?)</div>',
        r'<article[^>]*>(.*?)</article>',
        r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
    ]
    for pattern in patterns:
        match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if match:
            return _clean_html_text(match.group(1)).strip()
    return ""


def _clean_html_text(text: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
