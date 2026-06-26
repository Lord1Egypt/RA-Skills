#!/usr/bin/env python3
"""
collectors/adapters/builtin/cloud_docs/aliyun.py - 阿里云文档适配器

支持: help.aliyun.com 文档结构化提取

能力:
- 标题和元信息（作者/发布时间/版本）
- 目录导航（侧边栏章节）
- 正文内容（结构化 markdown）
- 代码块（带语言标记）
- 表格（格式保留）
- 图片（含 Alt）
- 面包屑导航
"""

import re
import sys
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path

# 导入 Task 1 建立的基础设施
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from collectors.adapters.base import DocAdapter, register_adapter
from collectors.adapters.extraction.structure import (
    DocumentItem,
    HeadingItem,
    CodeBlock,
    TableItem,
    ImageItem,
)


class AliyunDocAdapter(DocAdapter):
    """
    阿里云文档适配器

    完整支持 help.aliyun.com 文档结构化提取。
    """

    # 适配器标识
    name = 'aliyun_doc'
    platform = 'aliyun'

    # 支持的域名
    supported_domains = [
        'help.aliyun.com',
        'help.aliyun.cn',
        'www.aliyun.com',
    ]

    # 阿里云文档 CSS 选择器（已验证）
    SELECTORS = {
        # 标题
        'title': [
            '.article-title',
            'h1.title',
            '.doc-title',
            'article h1',
            '.article-header h1',
            '.help-title',
        ],

        # 正文内容
        'content': [
            '.article-content',
            '.content-body',
            '.doc-content',
            'article .content',
            '.help-content',
            '#article-content',
            '.markdown-body',
        ],

        # 代码块
        'code_block': [
            '.code-snippet',
            '.example-code',
            'pre code',
            '.code-block',
            'pre.highlight',
            '.highlight pre',
            'pre[class*="language-"]',
            '.mtk',  # 阿里云代码高亮容器
        ],

        # 表格
        'table': [
            '.table',
            'table',
            '.data-table',
            '.article-table',
            '.markdown-body table',
        ],

        # 标题层级
        'heading_h1': ['h1'],
        'heading_h2': ['h2'],
        'heading_h3': ['h3'],
        'heading_h4': ['h4', 'h5', 'h6'],

        # 侧边栏导航
        'sidebar_nav': [
            '.sidebar-nav',
            '.catalog-nav',
            '#catalog',
            '.help-catalog',
            '.article-nav',
            '.doc-nav',
            '[class*="sidebar"]',
        ],

        # 图片
        'image': [
            'img.article-image',
            '.content-body img',
            'article img',
            '.help-content img',
            '.markdown-body img',
        ],

        # 面包屑
        'breadcrumb': [
            '.breadcrumb',
            '.nav-path',
            '.help-breadcrumb',
            '[class*="breadcrumb"]',
        ],

        # 元信息
        'author': [
            '.author',
            '.article-author',
            '[class*="author"]',
            '.writer',
        ],

        'publish_date': [
            '.publish-date',
            '.article-date',
            'time[datetime]',
            '[class*="date"]',
            '.update-time',
        ],

        'version': [
            '.version-tag',
            '.version-badge',
            '[class*="version"]',
            '.doc-version',
        ],

        # API 示例（API文档特有）
        'api_example': [
            '.api-example',
            '.code-example',
            '[class*="example"]',
        ],
    }

    # 已知阿里云文档站点配置
    KNOWN_DOC_SITES = {
        'help.aliyun.com': {
            'content_selector': '.content-body, .article-content, #article-content',
            'heading_selector': 'h1, h2, h3, h4',
            'sidebar_nav': '.sidebar-nav, #catalog, .help-catalog',
            'code_block_selector': 'pre, .code-snippet, .highlight pre',
        },
    }

    def __init__(self):
        super().__init__()
        # 合并已知站点配置
        self.KNOWN_DOC_SITES.update(self._get_custom_sites())

    def _get_custom_sites(self) -> Dict[str, Dict[str, Any]]:
        """获取自定义站点配置"""
        return {}

    @property
    def platform_name(self) -> str:
        return '阿里云文档'

    def can_handle(self, url: str) -> bool:
        """检查是否支持此URL"""
        return any(host in url for host in self.supported_domains)

    def extract(self, page, url: str) -> DocumentItem:
        """
        提取阿里云文档

        Args:
            page: Playwright Page对象
            url: 文档URL

        Returns:
            DocumentItem: 结构化文档数据
        """
        # 提取标题
        title = self.extract_title(page)

        # 提取目录（侧边栏导航）
        toc = self.extract_headings(page)

        # 提取正文内容（markdown格式）
        content = self.extract_content(page)

        # 提取代码块
        code_blocks = self.extract_code_blocks(page)

        # 提取表格
        tables = self.extract_tables(page)

        # 提取图片
        images = self.extract_images(page)

        # 提取面包屑
        breadcrumbs = self.extract_breadcrumbs(page)

        # 提取元信息
        author = self.extract_author(page)
        publish_date, last_updated = self.extract_dates(page)
        version = self.extract_version(page)
        metadata = self.extract_metadata(page)

        return DocumentItem(
            url=url,
            title=title,
            author=author,
            publish_date=publish_date,
            last_updated=last_updated,
            version=version,
            toc=toc,
            content=content,
            code_blocks=code_blocks,
            tables=tables,
            images=images,
            breadcrumbs=breadcrumbs,
            metadata=metadata,
            language=self._detect_language(page, content),
        )

    def extract_title(self, page) -> str:
        """提取文档标题"""
        title_selectors = [
            '.article-title',
            'h1.title',
            '.doc-title',
            'article h1',
            '.article-header h1',
            '.help-title',
            '#article-title',
            '.markdown-body h1',
        ]

        for selector in title_selectors:
            try:
                if page.locator(selector).count() > 0:
                    title = page.locator(selector).first.inner_text().strip()
                    if title and len(title) > 2:
                        # 清理标题
                        title = self._clean_title_suffix(title)
                        return title
            except Exception:
                continue

        return page.title()

    def _clean_title_suffix(self, title: str) -> str:
        """去除标题中的站点后缀"""
        # 常见后缀模式：| 阿里云、 - 帮助文档 等
        patterns = [
            r'\s*[|\-–—:]\s*.+$',
        ]

        for pattern in patterns:
            cleaned = re.sub(pattern, '', title)
            if cleaned != title:
                return cleaned.strip()

        return title

    def extract_content(self, page) -> str:
        """提取正文内容"""
        content_selectors = [
            '.article-content',
            '.content-body',
            '#article-content',
            '.markdown-body',
            'article .content',
            '.help-content',
            '.doc-content',
        ]

        for selector in content_selectors:
            try:
                if page.locator(selector).count() > 0:
                    content = page.locator(selector).first.inner_text()
                    if content and len(content) > 100:
                        return self._clean_content(content)
            except Exception:
                continue

        # 回退到完整正文
        try:
            # 尝试获取 markdown-body
            if page.locator('.markdown-body').count() > 0:
                return self._clean_content(page.locator('.markdown-body').first.inner_text())
        except Exception:
            pass

        return ''

    def _clean_content(self, content: str) -> str:
        """清理内容"""
        if not content:
            return ''

        # 合并连续空白
        content = re.sub(r'\s+', ' ', content)
        # 去除特殊控制字符
        content = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', content)
        # 去除多余空行
        content = re.sub(r'\n{3,}', '\n\n', content)

        return content.strip()

    def extract_headings(self, page) -> List[HeadingItem]:
        """
        提取目录结构（支持侧边栏+正文标题）

        Returns:
            List[HeadingItem]: 嵌套的标题结构
        """
        headings: List[HeadingItem] = []

        # 1. 提取正文标题
        heading_configs = [
            ('h1', 1),
            ('h2', 2),
            ('h3', 3),
            ('h4', 4),
            ('h5', 5),
            ('h6', 6),
        ]

        all_headings: List[Tuple[int, str, str]] = []

        for selector, level in heading_configs:
            try:
                elements = page.locator(selector).all()
                for el in elements:
                    text = el.inner_text().strip()
                    if text and len(text) > 1:
                        anchor = self._extract_anchor(el)
                        all_headings.append((level, text, anchor))
            except Exception:
                continue

        # 2. 提取侧边栏导航（如果存在）
        nav_selectors = [
            '.sidebar-nav a',
            '#catalog a',
            '.help-catalog a',
            '.article-nav a',
        ]

        for nav_selector in nav_selectors:
            try:
                nav_items = page.locator(nav_selector).all()
                for item in nav_items:
                    text = item.inner_text().strip()
                    if text and len(text) > 1:
                        href = item.get_attribute('href') or ''
                        # 跳过外部链接
                        if href.startswith('http') and 'aliyun' not in href:
                            continue
                        anchor = self._text_to_anchor(text)
                        all_headings.append((0, text, anchor))  # level=0 表示导航项
            except Exception:
                continue

        # 构建标题树
        headings = self._build_heading_tree(all_headings)

        return headings

    def _extract_anchor(self, locator) -> str:
        """提取标题锚点"""
        try:
            # 优先从id获取
            if locator.get_attribute('id'):
                return locator.get_attribute('id')
            # 其次从href获取
            href = locator.locator('a').first.get_attribute('href') if locator.locator('a').count() > 0 else None
            if href and href.startswith('#'):
                return href[1:]
        except Exception:
            pass

        # 从文本生成
        text = locator.inner_text().strip()
        return self._text_to_anchor(text)

    def _text_to_anchor(self, text: str) -> str:
        """文本转锚点ID"""
        anchor = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', text)
        anchor = re.sub(r'[\s]+', '-', anchor)
        anchor = re.sub(r'-+', '-', anchor).strip('-')
        return anchor.lower()

    def _build_heading_tree(self, headings: List[Tuple[int, str, str]]) -> List[HeadingItem]:
        """构建标题树形结构"""
        if not headings:
            return []

        root: List[HeadingItem] = []
        stack: List[HeadingItem] = []

        for level, text, anchor in headings:
            # 跳过导航项（level=0）
            if level == 0:
                continue

            item = HeadingItem(level=level, text=text, anchor=anchor)

            # 找到合适的父节点
            while stack and stack[-1].level >= level:
                stack.pop()

            if not stack:
                root.append(item)
            else:
                stack[-1].children.append(item)

            stack.append(item)

        return root

    def extract_code_blocks(self, page) -> List[CodeBlock]:
        """
        提取代码块

        Returns:
            List[CodeBlock]: 代码块列表
        """
        code_blocks: List[CodeBlock] = []

        code_selectors = [
            'pre code',
            'pre.highlight',
            '.code-snippet',
            '.highlight pre',
            'pre[class*="language-"]',
            '.mtk',  # 阿里云代码高亮容器
            '.example-code pre',
        ]

        for selector in code_selectors:
            try:
                elements = page.locator(selector).all()
                for el in elements:
                    code_block = self._parse_code_block(el)
                    if code_block and code_block.code.strip():
                        code_blocks.append(code_block)
            except Exception:
                continue

        # 去重（基于代码内容）
        seen = set()
        unique_blocks = []
        for cb in code_blocks:
            content_hash = hash(cb.code[:100])
            if content_hash not in seen:
                seen.add(content_hash)
                unique_blocks.append(cb)

        return unique_blocks

    def _parse_code_block(self, locator) -> Optional[CodeBlock]:
        """解析单个代码块"""
        try:
            # 获取代码内容
            code = ''

            # 优先获取内部code元素
            if locator.locator('code').count() > 0:
                code = locator.locator('code').first.inner_text()
            else:
                code = locator.inner_text()

            if not code.strip():
                return None

            # 提取语言
            language = self._detect_code_language(locator)

            # 尝试获取文件名
            filename = self._detect_code_filename(locator)

            # 提取行号
            line_start, line_end = self._detect_code_lines(locator)

            return CodeBlock(
                language=language,
                code=code.strip(),
                filename=filename,
                line_start=line_start,
                line_end=line_end,
            )
        except Exception:
            return None

    def _detect_code_language(self, locator) -> str:
        """检测代码语言"""
        # 从class中检测
        try:
            class_attr = locator.get_attribute('class') or ''

            # 常见语言模式
            lang_patterns = [
                r'language-(\w+)',
                r'lang-(\w+)',
                r'highlight-(\w+)',
                r'brush:(\w+)',
            ]

            for pattern in lang_patterns:
                match = re.search(pattern, class_attr, re.IGNORECASE)
                if match:
                    return match.group(1).lower()

            # 从父元素检测
            parent_class = locator.locator('..').first.get_attribute('class') or ''
            for pattern in lang_patterns:
                match = re.search(pattern, parent_class, re.IGNORECASE)
                if match:
                    return match.group(1).lower()
        except Exception:
            pass

        # 回退：检测代码内容特征
        try:
            code = locator.inner_text()[:200]
            return self._infer_code_language(code)
        except Exception:
            return ''

    def _infer_code_language(self, code: str) -> str:
        """根据代码内容推断语言"""
        code_lower = code.lower()

        # Python
        if any(k in code_lower for k in ['def ', 'import ', 'from ', 'class ', 'self.', ' if __name__']):
            return 'python'
        # JavaScript/TypeScript
        if any(k in code_lower for k in ['function ', 'const ', 'let ', 'var ', '=>', 'async ', 'await ']):
            return 'javascript'
        # Java
        if 'public class' in code_lower or 'public static void main' in code_lower:
            return 'java'
        # Go
        if 'func ' in code_lower and 'package ' in code_lower:
            return 'go'
        # Shell
        if code.startswith('#!/') or 'echo ' in code_lower or 'export ' in code_lower:
            return 'bash'
        # SQL
        if any(k in code_lower for k in ['select ', 'from ', 'where ', 'insert into', 'update ']):
            return 'sql'
        # JSON
        if code.strip().startswith('{') and code.strip().endswith('}'):
            return 'json'
        # YAML
        if any(k in code_lower for k in ['apiVersion:', 'kind:', 'metadata:', 'spec:']):
            return 'yaml'

        return ''

    def _detect_code_filename(self, locator) -> Optional[str]:
        """检测代码文件名"""
        try:
            for attr in ['data-filename', 'data-file', 'filename', 'data-src']:
                filename = locator.get_attribute(attr)
                if filename:
                    return filename
        except Exception:
            pass
        return None

    def _detect_code_lines(self, locator) -> Tuple[int, int]:
        """检测代码行号"""
        try:
            line_start = locator.get_attribute('data-line-start')
            line_end = locator.get_attribute('data-line-end')
            if line_start and line_end:
                return int(line_start), int(line_end)
        except Exception:
            pass
        return 0, 0

    def extract_tables(self, page) -> List[TableItem]:
        """
        提取表格

        Returns:
            List[TableItem]: 表格列表
        """
        tables: List[TableItem] = []

        table_selectors = [
            '.table',
            'table',
            '.data-table',
            '.article-table',
            '.markdown-body table',
        ]

        for selector in table_selectors:
            try:
                elements = page.locator(selector).all()
                for el in elements:
                    table = self._parse_table(el)
                    if table:
                        tables.append(table)
            except Exception:
                continue

        return tables

    def _parse_table(self, locator) -> Optional[TableItem]:
        """解析单个表格"""
        try:
            headers: List[str] = []
            rows: List[List[str]] = []
            caption: Optional[str] = None

            # 提取caption
            try:
                if locator.locator('caption').count() > 0:
                    caption = locator.locator('caption').first.inner_text().strip()
            except Exception:
                pass

            # 提取表头
            try:
                header_locator = locator.locator('thead th')
                if header_locator.count() > 0:
                    for el in header_locator.all():
                        headers.append(el.inner_text().strip())
                else:
                    # 尝试从第一行获取
                    first_row = locator.locator('tbody tr').first
                    if first_row.count() > 0:
                        for el in first_row.locator('td, th').all():
                            headers.append(el.inner_text().strip())
            except Exception:
                pass

            # 提取数据行
            try:
                body_locator = locator.locator('tbody tr')
                if body_locator.count() == 0:
                    body_locator = locator.locator('tr')

                for row_el in body_locator.all():
                    cells = []
                    for cell in row_el.locator('td, th').all():
                        cells.append(cell.inner_text().strip())
                    if cells and cells != headers:
                        rows.append(cells)
            except Exception:
                pass

            if not headers and not rows:
                return None

            return TableItem(
                headers=headers,
                rows=rows,
                caption=caption,
            )
        except Exception:
            return None

    def extract_images(self, page) -> List[ImageItem]:
        """
        提取图片

        Returns:
            List[ImageItem]: 图片列表
        """
        images: List[ImageItem] = []

        image_selectors = [
            'img.article-image',
            '.content-body img',
            'article img',
            '.help-content img',
            '.markdown-body img',
            'img[src*="aliyun"]',
        ]

        for selector in image_selectors:
            try:
                elements = page.locator(selector).all()
                for el in elements:
                    img = self._parse_image(el)
                    if img and img.src:
                        images.append(img)
            except Exception:
                continue

        return images

    def _parse_image(self, locator) -> Optional[ImageItem]:
        """解析单个图片"""
        try:
            src = locator.get_attribute('src') or locator.get_attribute('data-src') or ''

            if not src:
                return None

            return ImageItem(
                src=src,
                alt=locator.get_attribute('alt') or '',
                title=locator.get_attribute('title'),
                width=locator.get_attribute('width'),
                height=locator.get_attribute('height'),
                loading=locator.get_attribute('loading') or 'lazy',
            )
        except Exception:
            return None

    def extract_breadcrumbs(self, page) -> List[str]:
        """
        提取面包屑导航

        Returns:
            List[str]: 面包屑文本列表
        """
        breadcrumbs: List[str] = []

        breadcrumb_selectors = [
            '.breadcrumb a, .breadcrumb span',
            '.nav-path a, .nav-path span',
            '.help-breadcrumb a, .help-breadcrumb span',
            '[class*="breadcrumb"] a, [class*="breadcrumb"] span',
        ]

        for selector in breadcrumb_selectors:
            try:
                elements = page.locator(selector).all()
                for el in elements:
                    text = el.inner_text().strip()
                    if text and text not in ['>', '/', '\\', '>']:
                        breadcrumbs.append(text)
                if breadcrumbs:
                    break
            except Exception:
                continue

        return breadcrumbs

    def extract_author(self, page) -> Optional[str]:
        """提取作者"""
        author_selectors = [
            '.author',
            '.article-author',
            '[class*="author"]',
            '.writer',
        ]

        for selector in author_selectors:
            try:
                if page.locator(selector).count() > 0:
                    author = page.locator(selector).first.inner_text().strip()
                    if author and len(author) < 100:
                        return author
            except Exception:
                continue

        return None

    def extract_dates(self, page) -> Tuple[Optional[str], Optional[str]]:
        """
        提取日期信息

        Returns:
            Tuple[publish_date, last_updated]
        """
        publish_date: Optional[str] = None
        last_updated: Optional[str] = None

        date_selectors = [
            '.publish-date',
            '.article-date',
            'time[datetime]',
            '[class*="date"]',
            '.update-time',
        ]

        for selector in date_selectors:
            try:
                if page.locator(selector).count() > 0:
                    el = page.locator(selector).first
                    date_text = el.inner_text().strip()
                    if date_text:
                        parsed = self._parse_date(date_text)
                        if parsed:
                            if not publish_date:
                                publish_date = parsed
                            elif not last_updated:
                                last_updated = parsed
            except Exception:
                continue

        return publish_date, last_updated

    def _parse_date(self, date_str: str) -> Optional[str]:
        """解析日期字符串"""
        patterns = [
            (r'\d{4}-\d{2}-\d{2}', '%Y-%m-%d'),
            (r'\d{4}/\d{2}/\d{2}', '%Y/%m/%d'),
            (r'\d{4}年\d{1,2}月\d{1,2}日', '%Y年%m月%d日'),
        ]

        for pattern, fmt in patterns:
            match = re.search(pattern, date_str)
            if match:
                try:
                    from datetime import datetime
                    dt = datetime.strptime(match.group(), fmt)
                    return dt.strftime('%Y-%m-%d')
                except Exception:
                    pass

        return date_str.strip()[:20] if date_str else None

    def extract_version(self, page) -> str:
        """提取文档版本"""
        version_selectors = [
            '.version-tag',
            '.version-badge',
            '[class*="version"]',
            '.doc-version',
        ]

        for selector in version_selectors:
            try:
                if page.locator(selector).count() > 0:
                    version = page.locator(selector).first.inner_text().strip()
                    if version and len(version) < 50:
                        return version
            except Exception:
                continue

        return ''

    def extract_metadata(self, page) -> Dict[str, Any]:
        """提取额外元数据"""
        metadata = {}

        # 提取标签
        tags = self._extract_tags(page)
        if tags:
            metadata['tags'] = tags

        # 提取阅读时间
        try:
            content_len = len(self.extract_content(page))
            metadata['reading_time_minutes'] = max(1, content_len // 200)
        except Exception:
            pass

        return metadata

    def _extract_tags(self, page) -> List[str]:
        """提取标签列表"""
        tags = []

        tag_selectors = [
            '[class*="tag"]',
            '.topic',
            'a[rel="tag"]',
        ]

        for selector in tag_selectors:
            try:
                if page.locator(selector).count() > 0:
                    for el in page.locator(selector).all():
                        text = el.inner_text().strip()
                        if text and len(text) < 30:
                            tags.append(text)
            except Exception:
                continue

        return tags[:10]

    # ==================== 生命周期方法 ====================

    def before_navigate(self, page, url: str):
        """导航前准备"""
        # 根据域名加载特定配置
        from urllib.parse import urlparse
        domain = urlparse(url).netloc

        for known_domain, config in self.KNOWN_DOC_SITES.items():
            if known_domain in domain:
                self._apply_site_config(config)
                break

    def _apply_site_config(self, config: Dict[str, Any]):
        """应用站点特定配置"""
        for key, value in config.items():
            if key.endswith('_selector') and value:
                selector_key = key.replace('_selector', '')
                self._selectors[selector_key] = [value]


# 注册适配器到全局注册表
_adapter_instance = AliyunDocAdapter()
register_adapter('aliyun_doc', _adapter_instance)
register_adapter('aliyun', _adapter_instance)
register_adapter('help.aliyun.com', _adapter_instance)


__all__ = ['AliyunDocAdapter']
