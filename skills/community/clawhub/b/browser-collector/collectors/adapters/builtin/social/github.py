#!/usr/bin/env python3
"""
collectors/adapters/builtin/social/github.py - GitHub站点适配器（新架构）

支持:
    - 仓库页 (owner/repo)
    - Issue页
    - 用户/组织页
    - README提取

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


class GitHubAdapter(DocAdapter):
    """
    GitHub站点适配器（新架构）

    自动识别页面类型并提取对应数据，返回 DocumentItem。
    """

    name = 'github'
    platform = 'github'

    supported_domains = ['github.com', 'www.github.com']

    # GitHub URL patterns
    REPO_PATTERN = re.compile(r'github\.com[/:]([\w\-\.]+)/([\w\-\.]+)')
    ISSUE_PATTERN = re.compile(r'github\.com[/:]([\w\-\.]+)/([\w\-\.]+)/issues/(\d+)')
    PR_PATTERN = re.compile(r'github\.com[/:]([\w\-\.]+)/([\w\-\.]+)/pull/(\d+)')

    SELECTORS = {
        'title': [
            'h1.ProtectedBranch-name',
            'strong.mr-2',
            '[itemprop="name"]',
            'h1.css-line-height-tight',
        ],
        'content': [
            '#repo-content-turbo-frame',
            '.repository-content',
            '[data-target="repository-content"]',
            'main',
        ],
        'code_block': [
            'pre.code-highlight',
            '.markdown-body pre',
            'pre[class*="language-"]',
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
            '[class*="breadcrumb"]',
            '.UnderlineNav',
        ],
        'author': [
            'a.author',
            '[class*="author"]',
            '.user-mention',
        ],
        'publish_date': [
            'time[datetime]',
            '[class*="date"]',
            '[datetime]',
        ],
        'image': [
            'img',
            'markdown-body img',
        ],
    }

    def extract(self, page, url: str) -> DocumentItem:
        """从GitHub页面提取完整结构化数据"""
        # 判断页面类型
        if self._is_repo_page(page, url):
            return self._extract_repo(page, url)
        elif self._is_issue_page(page, url):
            return self._extract_issue(page, url)
        elif self._is_profile_page(page, url):
            return self._extract_profile(page, url)
        elif self._is_readme_page(page, url):
            return self._extract_readme(page, url)
        else:
            return self._default_extract(page, url)

    def _is_repo_page(self, page, url: str) -> bool:
        """判断是否为仓库主页"""
        selectors = [
            '[itemprop="name"]',
            '.repository-content',
            '#repository-container-header',
        ]
        for sel in selectors:
            if page.locator(sel).count() > 0:
                return True
        path = self._extract_path(url)
        return 'repository' in page.title().lower() or '/' in path

    def _is_issue_page(self, page, url: str) -> bool:
        """判断是否为Issue页"""
        return bool(self.ISSUE_PATTERN.search(url)) or '/issues/' in url

    def _is_pr_page(self, page, url: str) -> bool:
        """判断是否为PR页"""
        return bool(self.PR_PATTERN.search(url)) or '/pull/' in url

    def _is_profile_page(self, page, url: str) -> bool:
        """判断是否为用户/组织页"""
        path = self._extract_path(url)
        parts = path.strip('/').split('/')
        if len(parts) == 1 and parts[0] and '.' not in parts[0]:
            return True
        return False

    def _is_readme_page(self, page, url: str) -> bool:
        """判断是否为README页"""
        return '/blob/' in url or url.endswith('.md') or '/readme' in url.lower()

    def _extract_path(self, url: str) -> str:
        """提取URL路径"""
        from urllib.parse import urlparse
        return urlparse(url).path

    def _extract_repo(self, page, url: str) -> DocumentItem:
        """提取仓库信息"""
        # 标题
        title = page.title()

        # 仓库名
        repo_name = ''
        for sel in ['[itemprop="name"]', '.repository-name']:
            if page.locator(sel).count() > 0:
                repo_name = page.locator(sel).first.inner_text().strip()
                break

        # 描述
        description = ''
        for sel in ['[itemprop="description"]', 'p.js-description', '.f4.my-3']:
            if page.locator(sel).count() > 0:
                description = page.locator(sel).first.inner_text().strip()
                break

        # 星标数
        stars = ''
        for sel in ['[href$="/stargazers"]', '.social-count']:
            if page.locator(sel).count() > 0:
                stars = page.locator(sel).first.inner_text().strip()
                break

        # Topics/Tags
        tags: List[str] = []
        for sel in ['a.topic-tag']:
            if page.locator(sel).count() > 0:
                tags = [t.inner_text().strip() for t in page.locator(sel).all()]
                break

        # README内容
        readme_content = ''
        for sel in ['#readme .markdown-body', '.repository-content .markdown-body']:
            if page.locator(sel).count() > 0:
                readme_content = page.locator(sel).first.inner_text()[:5000]
                break

        # 组装content
        content_parts = []
        if description:
            content_parts.append(f"描述: {description}")
        if stars:
            content_parts.append(f"星标: {stars}")
        if tags:
            content_parts.append(f"Topics: {', '.join(tags)}")
        if readme_content:
            content_parts.append(f"\nREADME:\n{readme_content[:2000]}")

        content = '\n'.join(content_parts) or page.locator('body').inner_text()[:2000]

        # author
        match = self.REPO_PATTERN.search(url)
        owner = match.group(1) if match else ''

        return DocumentItem(
            url=url,
            title=title or repo_name,
            author=owner,
            content=content,
            metadata={
                'repo_name': repo_name,
                'owner': owner,
                'stars': stars,
                'topics': tags,
            },
            language='en',
            quality_score=0.9,
        )

    def _extract_issue(self, page, url: str) -> DocumentItem:
        """提取Issue信息"""
        # Issue标题
        issue_title = ''
        for sel in ['h1.gh-header-title', '.js-issue-title']:
            if page.locator(sel).count() > 0:
                issue_title = page.locator(sel).first.inner_text().strip()
                break

        # Issue正文
        body = ''
        for sel in ['div.comment-body', '.markdown-body']:
            if page.locator(sel).count() > 0:
                body = page.locator(sel).first.inner_text()[:3000]
                break

        # 作者
        author = ''
        for sel in ['a.author', '.opened-by a']:
            if page.locator(sel).count() > 0:
                author = page.locator(sel).first.inner_text().strip()
                break

        # 标签
        tags: List[str] = []
        for sel in ['a[id^="label-"]']:
            if page.locator(sel).count() > 0:
                tags = [t.inner_text().strip() for t in page.locator(sel).all()]
                break

        # 评论数
        comments = ''
        for sel in ['a.js-discussion']:
            if page.locator(sel).count() > 0:
                comments = page.locator(sel).first.inner_text().strip()
                break

        # 发布时间
        publish_date = ''
        for sel in ['time[datetime]']:
            if page.locator(sel).count() > 0:
                publish_date = page.locator(sel).first.get_attribute('datetime') or ''
                break

        content = f"Issue: {issue_title}\n\n{body}"
        if comments:
            content += f"\n\n评论: {comments}"

        match = self.ISSUE_PATTERN.search(url)
        repo = f"{match.group(1)}/{match.group(2)}" if match else ''

        return DocumentItem(
            url=url,
            title=issue_title or page.title(),
            author=author,
            publish_date=publish_date,
            content=content,
            metadata={
                'repo': repo,
                'issue_id': match.group(3) if match else None,
                'labels': tags,
                'comments': comments,
            },
            language='en',
            quality_score=0.85,
        )

    def _extract_profile(self, page, url: str) -> DocumentItem:
        """提取用户/组织信息"""
        # Bio
        bio = ''
        for sel in ['p.user-bio', '[itemprop="description"]']:
            if page.locator(sel).count() > 0:
                bio = page.locator(sel).first.inner_text().strip()
                break

        # 用户名
        username = ''
        for sel in ['span.p-name', '[itemprop="name"]']:
            if page.locator(sel).count() > 0:
                username = page.locator(sel).first.inner_text().strip()
                break

        # 仓库数
        stats = ''
        for sel in ['a[href$="?tab=repositories"]']:
            if page.locator(sel).count() > 0:
                stats = page.locator(sel).first.inner_text().strip()
                break

        content = f"Bio: {bio}\n" if bio else ""
        content += f"Stats: {stats}\n" if stats else ""

        from urllib.parse import urlparse
        path = urlparse(url).path.strip('/')
        author = path.split('/')[0] if path else ''

        return DocumentItem(
            url=url,
            title=page.title(),
            author=author,
            content=content or page.locator('body').inner_text()[:1000],
            metadata={
                'username': username or author,
                'bio': bio,
            },
            language='en',
            quality_score=0.8,
        )

    def _extract_readme(self, page, url: str) -> DocumentItem:
        """提取README内容"""
        content = ''
        for sel in ['.markdown-body', '#readme']:
            if page.locator(sel).count() > 0:
                content = page.locator(sel).first.inner_text()[:5000]
                break

        if not content:
            content = page.locator('body').inner_text()[:2000]

        match = self.REPO_PATTERN.search(url)
        repo = f"{match.group(1)}/{match.group(2)}" if match else ''

        return DocumentItem(
            url=url,
            title=page.title(),
            author=repo,
            content=content,
            metadata={
                'repo': repo,
            },
            language='en',
            quality_score=0.9,
        )

    def _default_extract(self, page, url: str) -> DocumentItem:
        """默认提取"""
        return DocumentItem(
            url=url,
            title=page.title(),
            content=page.locator('body').inner_text()[:3000],
            language='en',
            quality_score=0.7,
        )

    def can_handle(self, url: str) -> bool:
        """检查是否支持此URL"""
        return any(host in url for host in self.supported_domains)


# 全局注册
from collectors.adapters.base import register_adapter
_adapter_instance = GitHubAdapter()
register_adapter('github', _adapter_instance)
register_adapter('github.com', _adapter_instance)


__all__ = ['GitHubAdapter']