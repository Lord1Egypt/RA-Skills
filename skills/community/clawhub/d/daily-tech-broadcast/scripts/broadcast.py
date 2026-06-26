#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日科技播报 - 从可抓取信息源拉取标题并生成简报。
仅将简报正文输出到 stdout，调试信息输出到 stderr。
无需 API Key，支持 UTF-8。
"""

import sys
import re
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin

# 信息源列表（可配置、可扩展）：名称 -> 首页 URL
# 优先使用已验证可抓取、无需 API Key 的源
NEWS_SOURCES = [
    {"name": "新浪科技", "url": "https://tech.sina.com.cn/"},
    {"name": "IT之家", "url": "https://www.ithome.com/"},
]

# 简报最多条数
MAX_ITEMS = 12
# 请求超时（秒）
TIMEOUT = 15
# User-Agent，避免被拒
UA = "Mozilla/5.0 (compatible; DailyTechBroadcast/1.0)"


def log(msg: str) -> None:
    """调试信息写到 stderr，不污染 stdout。"""
    print(msg, file=sys.stderr)


def fetch_url(url: str) -> str | None:
    """抓取 URL 返回 HTML 文本，失败返回 None。"""
    try:
        req = Request(url, headers={"User-Agent": UA})
        with urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read()
            # 尝试常见编码
            for enc in ("utf-8", "gbk", "gb2312"):
                try:
                    return raw.decode(enc, errors="replace")
                except (LookupError, UnicodeDecodeError):
                    continue
            return raw.decode("utf-8", errors="replace")
    except (URLError, HTTPError, OSError) as e:
        log(f"抓取失败 {url}: {e}")
        return None


def _is_article_link(href: str) -> bool:
    """判断是否为文章链接（排除导航、评论等）。"""
    if not href or "comment" in href or "javascript:" in href:
        return False
    if "/doc-" in href or "/tech/" in href or "finance.sina.com.cn/tech" in href:
        return True
    if "sina.com.cn" in href and ("doc-" in href or "article" in href):
        return True
    return False


def _is_nav_or_short(text: str) -> bool:
    """过滤导航、短标签。"""
    if not text or len(text) < 8:
        return True
    nav = ("首页", "客户端", "微博", "视频", "体育", "财经", "博客", "游戏", "众测", "GIF", "科学大家", "新浪")
    return any(text == x or text.startswith(x) for x in nav)


def extract_headlines_sina(html: str, base_url: str) -> list[dict]:
    """从新浪科技首页提取新闻标题与链接（优先文章链接）。"""
    from html.parser import HTMLParser

    class LinkParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.links = []
            self._in_a = False
            self._current_href = ""
            self._current_text = []

        def handle_starttag(self, tag, attrs):
            if tag == "a":
                self._in_a = True
                self._current_href = ""
                self._current_text = []
                for k, v in attrs:
                    if k == "href" and v:
                        self._current_href = v if v.startswith("http") else urljoin(base_url, v)
                        break

        def handle_endtag(self, tag):
            if tag == "a" and self._in_a:
                self._in_a = False
                text = "".join(self._current_text).strip()
                if not text or not self._current_href:
                    return
                if _is_nav_or_short(text):
                    return
                if len(text) > 120:
                    return
                if not re.search(r"[\u4e00-\u9fff]", text):
                    return
                href = self._current_href
                if "sina.com" not in href or "comment" in href:
                    return
                self.links.append({"title": text, "url": href, "is_article": _is_article_link(href)})

        def handle_data(self, data):
            if self._in_a:
                self._current_text.append(data)

    p = LinkParser()
    try:
        p.feed(html)
    except Exception:
        return []
    # 优先文章链接，再按标题去重
    articles = [{"title": x["title"], "url": x["url"]} for x in p.links if x.get("is_article")]
    others = [{"title": x["title"], "url": x["url"]} for x in p.links if not x.get("is_article")]
    combined = articles + others
    seen = set()
    out = []
    for item in combined:
        t = item["title"]
        if t not in seen:
            seen.add(t)
            out.append(item)
    return out[:MAX_ITEMS]


def extract_headlines_ithome(html: str, base_url: str) -> list[dict]:
    """从 IT之家 首页提取标题与链接。"""
    from html.parser import HTMLParser

    class LinkParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.links = []
            self._in_a = False
            self._current_href = ""
            self._current_text = []

        def handle_starttag(self, tag, attrs):
            if tag == "a":
                self._in_a = True
                self._current_href = ""
                self._current_text = []
                for k, v in attrs:
                    if k == "href" and v:
                        self._current_href = v if v.startswith("http") else urljoin(base_url, v)
                        break

        def handle_endtag(self, tag):
            if tag == "a" and self._in_a:
                self._in_a = False
                text = "".join(self._current_text).strip()
                if text and 4 <= len(text) <= 100 and "ithome.com" in self._current_href:
                    self.links.append({"title": text, "url": self._current_href})

        def handle_data(self, data):
            if self._in_a:
                self._current_text.append(data)

    p = LinkParser()
    try:
        p.feed(html)
    except Exception:
        return []
    seen = set()
    out = []
    for item in p.links:
        t = item["title"]
        if t not in seen and re.search(r"[\u4e00-\u9fff]", t):
            seen.add(t)
            out.append(item)
    return out[:MAX_ITEMS]


def fetch_news() -> list[dict]:
    """从配置的信息源抓取，返回 [{title, url, source}]，失败降级不抛异常。"""
    all_items = []
    for src in NEWS_SOURCES:
        name, url = src["name"], src["url"]
        html = fetch_url(url)
        if not html:
            continue
        if "sina" in url.lower():
            items = extract_headlines_sina(html, url)
        elif "ithome" in url.lower():
            items = extract_headlines_ithome(html, url)
        else:
            items = []
        for it in items:
            it["source"] = name
            all_items.append(it)
        if len(all_items) >= MAX_ITEMS:
            break
    # 去重（按标题）
    seen = set()
    unique = []
    for it in all_items:
        if it["title"] not in seen:
            seen.add(it["title"])
            unique.append(it)
    return unique[:MAX_ITEMS]


def generate_broadcast(items: list[dict]) -> str:
    """生成简报纯文本（UTF-8）。"""
    today = datetime.now().strftime("%Y年%m月%d日")
    lines = [
        f"# 📰 每日科技新闻简报",
        f"**{today}**",
        "",
    ]
    if not items:
        lines.extend(["暂无抓取到的新鲜条目，请稍后再试或检查网络。", ""])
    else:
        for i, it in enumerate(items, 1):
            lines.append(f"{i}. **{it['title']}**")
            lines.append(f"   来源：{it.get('source', '科技媒体')}")
            lines.append("")
    lines.append("---")
    lines.append("*由每日科技播报 Skill 生成，无需 API Key。*")
    return "\n".join(lines)


def main() -> int:
    """仅将简报输出到 stdout；错误信息到 stderr。"""
    try:
        items = fetch_news()
        text = generate_broadcast(items)
        # 仅 stdout 输出简报，供 cron/消息发送使用
        print(text, flush=True)
        return 0
    except Exception as e:
        log(f"broadcast 异常: {e}")
        # 仍输出一段降级文案，避免完全空白
        fallback = f"# 📰 每日科技新闻简报\n\n今日简报生成时遇到问题：{e}\n请稍后重试或检查网络。"
        print(fallback, flush=True)
        return 0  # 返回 0 让上层仍能发送这条降级消息


if __name__ == "__main__":
    sys.exit(main())
