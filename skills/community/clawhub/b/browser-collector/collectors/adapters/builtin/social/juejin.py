#!/usr/bin/env python3
"""
collectors/adapters/builtin/social/juejin.py - 掘金站点适配器（新架构）

支持:
    - 文章页

继承自 DocAdapter，返回 DocumentItem（完整结构化数据）。
"""

import re
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from collectors.adapters.base import DocAdapter
from collectors.adapters.extraction.structure import (
    DocumentItem,
    HeadingItem,
    CodeBlock,
    TableItem,
    ImageItem,
)


class JuejinAdapter(DocAdapter):
    """
    掘金站点适配器（新架构）

    支持掘金社区文章的结构化提取。
    """

    name = 'juejin'
    platform = 'juejin'

    supported_domains = ['juejin.cn', 'juejin.com', 'www.juejin.cn', 'juejin.im']

    SELECTORS = {
        'title': [
            'h1.article-title',
            'h1[class*="title"]',
            '.article-header h1',
        ],
        'content': [
            '.article-content',
            '.markdown-body',
            '[class*="article-content"]',
            'article',
        ],
        'code_block': [
            'pre code',
            '.code-block',
            'pre[class*="language-"]',
            '.highlight pre',
        ],
        'table': [
            'table',
            '.markdown-body table',
        ],
        'heading_h1': ['h1'],
        'heading_h2': ['h2'],
        'heading_h3': ['h3'],
        'heading_h4': ['h4', 'h5', 'h6'],
        'breadcrumb': [
            '.breadcrumb',
            '[class*="tag"]',
        ],
        'author': [
            '[class*="author"]',
            '.user-info',
            '[class*="writer"]',
        ],
        'publish_date': [
            '[class*="date"]',
            'time[datetime]',
            '[class*="time"]',
        ],
        'image': [
            'img',
            '.article-content img',
            '.markdown-body img',
        ],
    }

    def extract(self, page, url: str) -> DocumentItem:
        """从掘金页面提取完整结构化数据"""
        return self._extract_article(page, url)

    def _safe_text(self, page, selector: str, index: int = 0) -> str:
        """安全获取元素文本"""
        try:
            el = page.locator(selector).nth(index)
            if el.count() > 0:
                return el.inner_text().strip()
        except Exception:
            pass
        return ''

    def _safe_texts(self, page, selector: str, limit: int = 10) -> List[str]:
        """安全获取多个元素文本"""
        try:
            els = page.locator(selector).all()
            return [el.inner_text().strip() for el in els[:limit] if el.inner_text().strip()]
        except Exception:
            return []

    def _extract_article(self, page, url: str) -> DocumentItem:
        """提取掘金文章"""
        # 文章标题
        title = ''
        for sel in ['h1.article-title', 'h1[class*="title"]', '.article-header h1']:
            title = self._safe_text(page, sel)
            if title:
                break

        # 文章正文
        content = ''
        for sel in ['.article-content', '.markdown-body', '[class*="article-content"]', 'article']:
            if page.locator(sel).count() > 0:
                content = page.locator(sel).first.inner_text()
                if content and len(content) > 100:
                    break

        # 代码块
        code_blocks: List[CodeBlock] = []
        for sel in ['pre code', 'pre[class*="language-"]', '.highlight pre']:
            if page.locator(sel).count() > 0:
                for el in page.locator(sel).all():
                    code = el.inner_text().strip()
                    if code:
                        # 检测语言
                        language = ''
                        class_attr = el.get_attribute('class') or ''
                        match = re.search(r'language-(\w+)', class_attr)
                        if match:
                            language = match.group(1)
                        code_blocks.append(CodeBlock(
                            language=language,
                            code=code,
                        ))
                break

        # 作者
        author = ''
        for sel in ['[class*="author"] a', '.user-info .name', '[class*="writer"]']:
            author = self._safe_text(page, sel)
            if author:
                break

        # 发布时间
        publish_date = ''
        for sel in ['[class*="date"]', 'time[datetime]']:
            if page.locator(sel).count() > 0:
                dt = page.locator(sel).first.get_attribute('datetime')
                if dt:
                    publish_date = dt
                else:
                    publish_date = self._safe_text(page, sel)
                if publish_date:
                    break

        # 标签
        tags: List[str] = []
        for sel in ['[class*="tag"]']:
            tags = self._safe_texts(page, sel, 10)
            if tags:
                break

        # 点赞数
        like_count = ''
        for sel in ['[class*="like"]']:
            like_count = self._safe_text(page, sel)
            if like_count:
                break

        # 面包屑
        breadcrumbs: List[str] = []
        for sel in ['.breadcrumb a', '[class*="category"]']:
            breadcrumbs = self._safe_texts(page, sel, 5)
            if breadcrumbs:
                break

        # 如果没有获取到正文，使用备用方式
        if not content or len(content) < 100:
            for sel in ['main', '[role="main"]']:
                if page.locator(sel).count() > 0:
                    content = page.locator(sel).first.inner_text()
                    if content:
                        break

        return DocumentItem(
            url=url,
            title=title or page.title(),
            author=author,
            publish_date=publish_date,
            content=content or page.locator('body').inner_text()[:3000],
            code_blocks=code_blocks,
            metadata={
                'tags': tags,
                'like_count': like_count,
            },
            breadcrumbs=breadcrumbs,
            language='zh',
            quality_score=0.85 if content else 0.6,
        )

    def can_handle(self, url: str) -> bool:
        """检查是否支持此URL"""
        return any(host in url for host in self.supported_domains)


# 全局注册
from collectors.adapters.base import register_adapter
_adapter_instance = JuejinAdapter()
register_adapter('juejin', _adapter_instance)
register_adapter('juejin.cn', _adapter_instance)


__all__ = ['JuejinAdapter']