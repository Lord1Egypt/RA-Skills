# phase1_base.py — Phase-1 采集基础架构
"""
设计目标：
  1. Announcement 统一数据 schema，Phase2/P3 直接引用
  2. BaseCollector 封装 HTTP/Playwright 工具
  3. AnnouncementBuilder 简化子类构建逻辑

Schema（统一 Announcement 格式）：
  {
    "title": str,         # 公告标题（≤200字）
    "date": str,           # ISO日期 YYYY-MM-DD
    "url": str,            # 详情页URL
    "category": str,       # classify() 分类
    "text": str,           # 纯文本正文（Phase2用，≤5000字）
    "_content_type": str,  # html|pdf|vue|json|list_page
    "_attachments": list,   # [{filename, path, type}]
  }

采集器分组（按架构模式）：
  G1 静态列表  — 直接解析 HTML，无 JS
  G2 翻页列表  — 有"下一页"按钮
  G3 动态加载  — JS/JSON API / Vue SPA
  G4 详情枚举  — 列表页提取 ID 构造 URL
  G5 PDF附件   — 公告列表→PDF链接→pdftotext
  G6 特殊格式  — 日期分两行/表格/扫描件
"""
from __future__ import annotations

import asyncio
import re
import subprocess
from dataclasses import dataclass, field
from typing import AsyncIterator, Optional
from urllib.parse import urljoin

import httpx


# ─────────────────────────────────────────────────────────────────────────────
# 1. 数据模型
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(slots=True)
class Announcement:
    """统一公告格式，支持 dict 下标访问（兼容 collect.py 的 .get()）。"""
    title: str
    date: str
    url: str
    category: str = "重要公告"
    text: str = ""
    _content_type: str = "html"
    _attachments: list[dict] = field(default_factory=list)

    # ── dict 兼容层 ──────────────────────────────────────────────────────

    def __getitem__(self, key: str):
        if key == "content_type":
            return self._content_type
        if key == "attachments":
            return self._attachments
        if key == "category":
            return self.category
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    def get(self, key: str, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self):
        return ["title", "date", "url", "category", "text", "_content_type", "_attachments"]

    def __iter__(self):
        return iter(self.keys())

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "date": self.date,
            "url": self.url,
            "category": self.category,
            "text": self.text,
            "_content_type": self._content_type,
            "_attachments": list(self._attachments),
        }

    def with_text(self, text: str) -> "Announcement":
        new = Announcement(
            title=self.title,
            date=self.date,
            url=self.url,
            category=self.category,
            text=text[:5000],
            _content_type=self._content_type,
            _attachments=list(self._attachments),
        )
        return new

    def with_type(self, ct: str) -> "Announcement":
        new = Announcement(
            title=self.title,
            date=self.date,
            url=self.url,
            category=self.category,
            text=self.text,
            _content_type=ct,
            _attachments=list(self._attachments),
        )
        return new


# ─────────────────────────────────────────────────────────────────────────────
# 2. 工具函数
# ─────────────────────────────────────────────────────────────────────────────

def pdf_to_text(pdf_path: str, max_kb: int = 10000) -> str:
    """pdftotext 提取文本，超大文件跳过。"""
    try:
        size_kb = int(subprocess.run(
            ["stat", "-c", "%s", pdf_path], capture_output=True, text=True
        ).stdout.strip() or 0) // 1024
        if size_kb > max_kb:
            return f"[PDF oversized: {size_kb}KB]"
        result = subprocess.run(
            ["pdftotext", str(pdf_path), "-"], capture_output=True, text=True, timeout=60
        )
        return result.stdout[:5000]
    except Exception:
        return ""


def extract_links_from_html(
    html: str,
    base_url: str = "",
    link_pat: str = r'href=["\']([^"\']+)["\']',
) -> list[tuple[str, str]]:
    """从 HTML 中提取链接和文本，返回 [(url, link_text), ...]。"""
    raw_links = re.findall(link_pat, html)
    results = []
    for raw in raw_links:
        if not raw or raw.startswith(("javascript:", "#", "mailto:")):
            continue
        url = urljoin(base_url, raw)
        m = re.search(rf'href=["\']({re.escape(raw)})["\'][^>]*>(.*?)</a>', html, re.S)
        text = re.sub(r"<[^>]+>", "", m.group(2)).strip() if m else ""
        results.append((url, text))
    return results


def find_pdf_links(html: str, base_url: str = "") -> list[str]:
    """从 HTML 中提取所有 PDF 链接（绝对路径）。"""
    return [urljoin(base_url, u) for u, _ in extract_links_from_html(
        html, base_url, link_pat=r'href=["\']([^"\']*\.pdf)["\']')]


# ─────────────────────────────────────────────────────────────────────────────
# 3. BaseCollector — 所有 v2 采集器的基类
# ─────────────────────────────────────────────────────────────────────────────

class BaseCollector:
    """
    采集器基类，提供通用 HTTP 工具。

    子类只需：
      1. 设置 class 属性（method, group, description）
      2. 实现 collect() 方法（yield Announcement）
      3. 用 @collector("method_name") 注册

    collect.py 调度方式：
      cls = COLLECTORS[method]   # cls 是 BaseCollector 的子类
      result = await cls(page, url)()   # __call__ → collect() → list[dict]
    """

    method: str = ""
    group: str = "G1"
    description: str = ""
    default_headers: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    default_timeout: int = 120

    def __init__(self, page=None, url: str = ""):
        self.page = page
        self.url = url or getattr(self, 'base_url', '')
        self.headers: dict = dict(self.default_headers)
        self.timeout: int = int(getattr(self, 'default_timeout', 30))
        self._client: Optional[httpx.AsyncClient] = None

    # ── HTTP 工具 ─────────────────────────────────────────────────────────

    async def get_json(self, url: str, **kwargs) -> dict | list:
        hdrs = dict(self.headers)
        hdrs.update(kwargs.pop("headers", {}))
        async with httpx.AsyncClient(follow_redirects=True, timeout=self.timeout) as client:
            r = await client.get(url, headers=hdrs, **kwargs)
            return r.json()

    async def get_text(self, url: str, **kwargs) -> str:
        hdrs = dict(self.headers)
        hdrs.update(kwargs.pop("headers", {}))
        async with httpx.AsyncClient(follow_redirects=True, timeout=self.timeout) as client:
            r = await client.get(url, headers=hdrs, **kwargs)
            return r.text

    async def get_html(self, url: str, **kwargs) -> str:
        hdrs = dict(self.headers)
        hdrs.update(kwargs.pop("headers", {}))
        async with httpx.AsyncClient(follow_redirects=True, timeout=self.timeout) as client:
            r = await client.get(url, headers=hdrs, **kwargs)
            return r.text

    async def download_pdf(self, url: str, dest: str) -> tuple[bool, str]:
        """下载 PDF，返回 (success, extracted_text)。"""
        import os
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=self.timeout) as client:
                r = await client.get(url, headers=self.headers)
                if r.status_code != 200 or r.content[:4] != b"%PDF":
                    return False, ""
                with open(dest, "wb") as f:
                    f.write(r.content)
            text = pdf_to_text(dest)
            return True, text
        except Exception:
            return False, ""

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None

    # ── Playwright 工具 ───────────────────────────────────────────────────

    async def click_and_wait(self, selector: str, timeout: int = 15000):
        if self.page:
            await self.page.click(selector, timeout=timeout)
            await asyncio.sleep(1)

    async def evaluate_js(self, script: str):
        if self.page:
            return await self.page.evaluate(script)
        return None

    # ── 子类必须实现 ──────────────────────────────────────────────────────

    async def collect(self) -> AsyncIterator[Announcement]:
        raise NotImplementedError

    # ── 兼容 collect.py 的 __call__ 接口 ─────────────────────────────────

    async def __call__(self, page=None, url: str = "") -> list[dict]:
        """
        collect.py 的 dispatch 入口：
          cls(page, url)() → list[dict]
        """
        self.page = page or self.page
        self.url = url or self.url
        results = []
        async for ann in self.collect():
            results.append(ann.to_dict())
        await self.close()
        return results


# ─────────────────────────────────────────────────────────────────────────────
# 4. 注册装饰器
# ─────────────────────────────────────────────────────────────────────────────

COLLECTORS: dict[str, type[BaseCollector]] = {}


def collector(name: str):
    """将 BaseCollector 子类注册到 phase1_base.COLLECTORS。"""
    def decor(cls: type[BaseCollector]) -> type[BaseCollector]:
        cls.method = name
        COLLECTORS[name] = cls
        return cls
    return decor


# ─────────────────────────────────────────────────────────────────────────────
# 5. AnnouncementBuilder — 子类构建 Announcement 的简化接口
# ─────────────────────────────────────────────────────────────────────────────

class AnnouncementBuilder:
    """帮助子类构建 Announcement，减少重复代码。"""

    def __init__(self, base_url: str = ""):
        self.base_url = base_url

    def build(
        self,
        title: str,
        url: str,
        date: str = "",
        category: str = "",
        text: str = "",
        content_type: str = "html",
        attachments: list = None,
    ) -> Announcement:
        from core import classify
        full_url = urljoin(self.base_url, url) if url else ""
        cat = category or classify(title)
        dt = date or self._date_from_url(full_url)
        return Announcement(
            title=title[:200],
            date=dt,
            url=full_url,
            category=cat,
            text=text[:5000] if text else "",
            _content_type=content_type,
            _attachments=list(attachments) if attachments else [],
        )

    def _date_from_url(self, url: str) -> str:
        m = re.search(r"/(\d{4})[/-](\d{2})[/-]?(\d{2})?", url)
        if m:
            d = m.group(3) or "01"
            return f"{m.group(1)}-{m.group(2)}-{d}"
        return ""
