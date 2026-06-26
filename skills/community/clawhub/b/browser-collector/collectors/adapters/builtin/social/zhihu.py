#!/usr/bin/env python3
"""
collectors/adapters/builtin/social/zhihu.py - 知乎站点适配器（新架构）

支持:
    - 问题页 (question)
    - 文章页 (article)
    - 用户主页 (people)
    - 回答 (answer)

继承自 DocAdapter，返回 DocumentItem（完整结构化数据）。
"""

import re
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from collectors.adapters.base import DocAdapter
from collectors.adapters.extraction.structure import (
    DocumentItem,
    HeadingItem,
    CodeBlock,
    TableItem,
    ImageItem,
)


class ZhihuAdapter(DocAdapter):
    """
    知乎站点适配器（新架构）

    自动识别页面类型并提取对应数据，返回 DocumentItem。
    """

    name = 'zhihu'
    platform = 'zhihu'

    supported_domains = ['zhihu.com', 'www.zhihu.com']

    QUESTION_PATTERN = re.compile(r'zhihu\.com/question/(\d+)')
    ARTICLE_PATTERN = re.compile(r'zhihu\.com/p/(\d+)')
    ANSWER_PATTERN = re.compile(r'zhihu\.com/question/\d+/answer/(\d+)')
    PEOPLE_PATTERN = re.compile(r'zhihu\.com/people/([^\/\?]+)')

    SELECTORS = {
        'title': [
            'h1.QuestionHeader-title',
            'h1.Post-Title',
            '.ProfileHeader-name',
        ],
        'content': [
            '.QuestionAnswer-content',
            'div.RichText',
            '.Post-RichText',
            '.article-content',
        ],
        'code_block': [
            'pre code',
            'figure.highlight',
            '.code-block',
        ],
        'table': [
            'table',
        ],
        'heading_h1': ['h1'],
        'heading_h2': ['h2'],
        'heading_h3': ['h3'],
        'heading_h4': ['h4', 'h5', 'h6'],
        'breadcrumb': [
            '.Breadcrumb',
            '.QuestionHeader-tags',
        ],
        'author': [
            '.Author-link',
            '.AnswerItem-author',
            '.Post-author',
        ],
        'publish_date': [
            '[class*="Date"]',
            'time[datetime]',
        ],
        'image': [
            'img',
            '.article-content img',
        ],
    }

    def extract(self, page, url: str) -> DocumentItem:
        """从知乎页面提取完整结构化数据"""
        if self.QUESTION_PATTERN.search(url):
            return self._extract_question(page, url)
        elif self.ARTICLE_PATTERN.search(url):
            return self._extract_article(page, url)
        elif self.PEOPLE_PATTERN.search(url):
            return self._extract_profile(page, url)
        else:
            return self._default_extract(page, url)

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

    def _extract_question(self, page, url: str) -> DocumentItem:
        """提取知乎问题"""
        # 问题标题
        question_title = ''
        for sel in ['h1.QuestionHeader-title', 'h1[data-reactid]']:
            question_title = self._safe_text(page, sel)
            if question_title:
                break

        # 问题描述
        question_desc = ''
        for sel in ['span[data-reactid]', '.QuestionHeader-detail']:
            question_desc = self._safe_text(page, sel)
            if question_desc:
                break

        # 回答内容（第一个回答）
        answer_content = ''
        for sel in ['div.RichText', '.QuestionAnswer-content']:
            texts = self._safe_texts(page, sel, 1)
            if texts:
                answer_content = texts[0][:3000]
                break

        # 作者信息
        author = ''
        for sel in ['a.Author-link', '.AnswerItem-author']:
            author = self._safe_text(page, sel)
            if author:
                break

        # 回答数/关注数
        meta = ''
        for sel in ['.QuestionFollowStatus-count']:
            meta = self._safe_text(page, sel)
            if meta:
                break

        # 标签
        tags: List[str] = []
        for sel in ['a.Tag', '.QuestionHeader-tags .Tag']:
            tags = self._safe_texts(page, sel, 10)
            if tags:
                break

        # 组装content
        content_parts = []
        if question_title:
            content_parts.append(f"问题: {question_title}")
        if question_desc:
            content_parts.append(f"描述: {question_desc[:500]}")
        if meta:
            content_parts.append(f"状态: {meta}")
        if answer_content:
            content_parts.append(f"\n最佳回答:\n{answer_content[:2000]}")
        if tags:
            content_parts.append(f"标签: {', '.join(tags)}")

        content = '\n'.join(content_parts) if content_parts else page.locator('body').inner_text()[:2000]

        # 面包屑
        breadcrumbs = self._safe_texts(page, '.QuestionHeader-tags a', 5)

        match = self.QUESTION_PATTERN.search(url)
        qid = match.group(1) if match else ''

        return DocumentItem(
            url=url,
            title=question_title or page.title(),
            author=author,
            content=content,
            metadata={
                'question_id': qid,
                'description': question_desc,
                'labels': tags,
                'meta': meta,
            },
            breadcrumbs=breadcrumbs,
            language='zh',
            quality_score=0.85,
        )

    def _extract_article(self, page, url: str) -> DocumentItem:
        """提取知乎文章"""
        # 文章标题
        article_title = ''
        for sel in ['h1.Post-Title', 'h1[data-reactid]']:
            article_title = self._safe_text(page, sel)
            if article_title:
                break

        # 文章正文
        content = ''
        for sel in ['div.RichText', '.Post-RichText', '.article-content']:
            texts = self._safe_texts(page, sel, 1)
            if texts:
                content = texts[0][:5000]
                break

        # 作者
        author = ''
        for sel in ['a.Author-link', '.Post-author']:
            author = self._safe_text(page, sel)
            if author:
                break

        # 点赞数
        vote_count = ''
        for sel in ['.VoteButton']:
            vote_count = self._safe_text(page, sel)
            if vote_count:
                break

        # 发布时间
        publish_date = ''
        for sel in ['time[datetime]']:
            if page.locator(sel).count() > 0:
                publish_date = page.locator(sel).first.get_attribute('datetime') or ''
                break

        if not content:
            content = page.locator('body').inner_text()[:2000]

        match = self.ARTICLE_PATTERN.search(url)
        aid = match.group(1) if match else ''

        return DocumentItem(
            url=url,
            title=article_title or page.title(),
            author=author,
            publish_date=publish_date,
            content=content,
            metadata={
                'article_id': aid,
                'vote_count': vote_count,
            },
            language='zh',
            quality_score=0.9,
        )

    def _extract_profile(self, page, url: str) -> DocumentItem:
        """提取知乎用户主页"""
        # 用户名
        username = ''
        for sel in ['span.ProfileHeader-name', '.name']:
            username = self._safe_text(page, sel)
            if username:
                break

        # Bio
        bio = ''
        for sel in ['span.ProfileHeader-bio', '.bio']:
            bio = self._safe_text(page, sel)
            if bio:
                break

        # 关注数/粉丝数
        stats: List[str] = []
        for sel in ['.Followship']:
            text = self._safe_text(page, sel)
            if text:
                stats.append(text)
                break

        content_parts = []
        if username:
            content_parts.append(f"用户: {username}")
        if bio:
            content_parts.append(f"简介: {bio}")
        if stats:
            content_parts.append(f"数据: {', '.join(stats)}")

        content = '\n'.join(content_parts) if content_parts else page.locator('body').inner_text()[:1000]

        match = self.PEOPLE_PATTERN.search(url)
        uid = match.group(1) if match else ''

        return DocumentItem(
            url=url,
            title=page.title(),
            author=uid,
            content=content,
            metadata={
                'username': username or uid,
                'bio': bio,
            },
            language='zh',
            quality_score=0.8,
        )

    def _default_extract(self, page, url: str) -> DocumentItem:
        """默认提取"""
        return DocumentItem(
            url=url,
            title=page.title(),
            content=page.locator('body').inner_text()[:3000],
            language='zh',
            quality_score=0.7,
        )

    def can_handle(self, url: str) -> bool:
        """检查是否支持此URL"""
        return any(host in url for host in self.supported_domains)


# 全局注册
from collectors.adapters.base import register_adapter
_adapter_instance = ZhihuAdapter()
register_adapter('zhihu', _adapter_instance)
register_adapter('zhihu.com', _adapter_instance)


__all__ = ['ZhihuAdapter']