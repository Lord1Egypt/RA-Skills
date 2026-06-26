# collectors_v2.py — Phase-1 采集器（新架构 v2）
"""
Phase-1 采集器（v2 架构）。
所有采集器继承 BaseCollector，使用 AnnouncementBuilder。

已在 companies.json 中实际使用的 v2 采集器通过本文件注册到 collectors.COLLECTORS。

架构原则：
  1. Announcement 是唯一数据格式（见 phase1_base.py）
  2. 每个 collector 是独立的 async 生成器
  3. @collector 装饰器注册到 COLLECTORS_V2（由 pipeline.py 使用）

GROUPS:
  G1 — 静态 HTML（无 JS）
  G2 — 翻页列表（通用下一页）
  G3 — JSON API（Vue / AJAX）
  G4 — 详情页 URL 枚举
  G5 — PDF 附件
  G6 — 特殊格式
"""
from __future__ import annotations

import asyncio
import re
from typing import AsyncIterator

from phase1_base import (
    BaseCollector,
    Announcement,
    AnnouncementBuilder,
    collector,
    find_pdf_links,
)
from core import classify


# ═══════════════════════════════════════════════════════════════════════════
# G3 — JSON API（Vue / AJAX / REST）
# ═══════════════════════════════════════════════════════════════════════════

@collector("cfcbnb_v2")
class CfcbnbCollector(BaseCollector):
    """
    宁银消费金融 | cfcbnb.com/xwgg/zygg/
    公告列表通过 Vue data.json API 加载。

    API:
      GET https://www.cfcbnb.com/xwgg/zygg/data.json        (第1页)
      GET https://www.cfcbnb.com/xwgg/zygg/data_{N}.json    (第N+1页)

    字段映射:
      DOCTITLE  → title
      DOCRELTIME → date
      URL       → url (相对路径)
    """
    method = "cfcbnb_v2"
    group = "G3"
    description = "宁银消金 — Vue data.json API"
    base_url = "https://www.cfcbnb.com/xwgg/zygg/"

    async def collect(self) -> AsyncIterator[Announcement]:
        builder = AnnouncementBuilder(self.base_url)
        page_num = 0

        while True:
            api_url = (
                self.base_url + "data.json"
                if page_num == 0
                else f"{self.base_url}data_{page_num}.json"
            )

            try:
                data = await self.get_json(api_url)
                records = data.get("list", [])
                if not records:
                    break

                for rec in records:
                    ann = builder.build(
                        title=rec.get("DOCTITLE", "").strip(),
                        date=rec.get("DOCRELTIME", ""),
                        url=rec.get("URL", ""),
                        content_type="html",
                    )
                    print(
                        f"  宁银(cfcbnb_v2) 第{page_num+1}页: {ann.title[:40]}",
                        flush=True,
                    )
                    yield ann

                page_count = int(data.get("PAGE_COUNT", 0))
                page_num += 1
                if page_num >= page_count:
                    break

            except Exception as e:
                print(f"  宁银(cfcbnb_v2) Error: {e}", flush=True)
                break


# ═══════════════════════════════════════════════════════════════════════════
# G6 — 蒙商消金专用采集器（从 HTML 正文提取合作机构表格）
# ═══════════════════════════════════════════════════════════════════════════

@collector("mengshang_v2")
class MengshangCollector(BaseCollector):
    """
    蒙商消费金融 | mengshangxiaofei.com
    公告列表在 /html/1//208/217/index.html，分页 list-N.html。
    """
    method = "mengshang_v2"
    group = "G6"
    description = "蒙商消金 — HTML 静态列表"
    base_url = "https://www.mengshangxiaofei.com/html/1//208/217/"

    async def collect(self) -> AsyncIterator[Announcement]:
        from phase1_base import AnnouncementBuilder
        from urllib.parse import urljoin
        import re

        builder = AnnouncementBuilder(self.base_url)
        page_url = self.url or self.base_url
        if not page_url.endswith("index.html"):
            page_url = page_url.rstrip("/") + "/index.html"

        skip_text = {"首页", "关于我们", "产品业务", "动态资讯", "消费者保护",
                     "加入我们", "服务公告", "公司新闻", "上一页", "下一页",
                     "公告", "蒙公网安备", "蒙ICP备"}

        while page_url:
            html = await self.get_html(page_url)

            # 提取 href 和链接文本
            hrefs = re.findall('<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html, re.S)
            for href, link_text in hrefs:
                title = re.sub(r"<[^>]+>", "", link_text).strip()
                if len(title) < 5 or title in skip_text:
                    continue
                if "/208/217/" not in href or not href.endswith(".html"):
                    continue
                full_url = urljoin(page_url, href)
                yield builder.build(title=title, url=full_url, content_type="html")

            # 下一页（停在最后一页：next 与当前相同）
            next_m = re.search(r'<a[^>]+href="([^"]*list-\d+\.html)"[^>]*>下一页', html)
            next_url = urljoin(page_url, next_m.group(1)) if next_m else ""
            if next_url and next_url != page_url:
                page_url = next_url
                await asyncio.sleep(0.5)
            else:
                break

# 末端同步：v2 collectors 注册到 phase1_base.COLLECTORS → 同步到 collectors.COLLECTORS
import phase1_base
import collectors as collectors_module
for name, cls in phase1_base.COLLECTORS.items():
    collectors_module.COLLECTORS[name] = cls

# 对外接口（由 pipeline.py 导入使用）
__all__ = ["phase1_base", "collectors"]
