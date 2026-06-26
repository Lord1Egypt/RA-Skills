#!/usr/bin/env python3
"""
collectors/adapters/base.py - 统一适配器基类

提供统一的文档适配器接口和结构化提取能力。

核心类:
- BaseAdapter: 基础适配器抽象类
- DocAdapter: 文档适配器基类（完整结构化提取）
- AdapterRegistry: 适配器注册表

Usage:
    from collectors.adapters.base import DocAdapter, AdapterRegistry

    class MyDocAdapter(DocAdapter):
        name = 'mydoc'
        supported_domains = ['docs.example.com']
        
        # 自定义选择器
        SELECTORS = {
            'title': '.doc-title',
            'content': '.article-content',
            ...
        }
"""

import re
import time
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Page, Locator

from .extraction.structure import (
    DocumentItem, HeadingItem, CodeBlock, TableItem, ImageItem
)


# ==================== DocAdapter选择器定义 ====================

DEFAULT_SELECTORS = {
    # 基础元素
    'title': [
        'h1', '[class*="title"]', '.doc-title', '.article-title',
        '.post-title', '.entry-title', '#title', 'title'
    ],
    'content': [
        'article', '[role="main"]', '.markdown-body', '.article-content',
        '.docs-content', '.documentation', '.post-content', '.entry-content',
        'main', '.content', '#content', '.content-body'
    ],
    
    # 代码块
    'code_block': [
        'pre code', 'pre', '.highlight', '.code-block',
        '[class*="highlight"]', '[class*="code-block"]', '.code-snippet',
        '[data-type="code"]', '.sourceCode'
    ],
    'code_language': [
        '[class*="language-"]', '[class*="highlight-"]', 
        'code[class*="language-"]', '.highlight .name'
    ],
    
    # 表格
    'table': [
        'table', '.table', '.data-table', '[class*="table"]',
        '.table-responsive table'
    ],
    'table_caption': [
        'caption', '[class*="caption"]', '.table-caption'
    ],
    
    # 标题层级
    'heading_h1': ['h1'],
    'heading_h2': ['h2'],
    'heading_h3': ['h3'],
    'heading_h4': ['h4', 'h5', 'h6'],
    
    # 导航
    'sidebar_nav': [
        '.sidebar-nav', '.catalog-nav', '#catalog', '.toc',
        '[class*="sidebar"]', '[class*="nav"]', '.menu'
    ],
    'breadcrumb': [
        '.breadcrumb', '.nav-path', '[class*="breadcrumb"]',
        '[class*="path"]', '.crumbs'
    ],
    
    # 图片
    'image': [
        'img', '[class*="image"]', '[class*="img"]', 'picture img'
    ],
    
    # 元信息
    'author': [
        '[class*="author"]', '.writer', '[rel="author"]', 
        '[itemprop="author"]', '.byline'
    ],
    'publish_date': [
        '[class*="date"]', '[class*="time"]', '[datetime]',
        '[itemprop="datePublished"]', '.timestamp'
    ],
    'version': [
        '[class*="version"]', '[class*="ver"]', '.doc-version'
    ],
    
    # 特殊元素
    'api_endpoint': [
        '[class*="endpoint"]', '[class*="api-"]', '.operation-tag',
        '[data-method]', '.api-endpoint'
    ],
    'callout': [
        '[class*="callout"]', '[class*="note"]', '[class*="warning"]',
        '[class*="tip"]', '[class*="info"]', '.alert'
    ],
}


class BaseAdapter(ABC):
    """
    站点适配器基类

    所有站点适配器继承此基类，提供统一的extract接口。

    子类需实现:
        name: str - 适配器名称
        supported_domains: List[str] - 支持的域名列表
        extract(page, url) -> DocumentItem - 数据提取
    """

    name: str = 'base'
    supported_domains: List[str] = []

    @abstractmethod
    def extract(self, page, url: str) -> DocumentItem:
        """
        从Playwright Page提取结构化数据

        Args:
            page: playwright.sync_api.Page
            url: str - 原始URL

        Returns:
            DocumentItem - 提取的文档结构化数据
        """
        ...

    def before_navigate(self, page, url: str):
        """导航前准备（可重写）"""
        pass

    def after_load(self, page, url: str):
        """页面加载后处理（可重写）"""
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name}>"


class DocAdapter(BaseAdapter):
    """
    文档适配器基类 - 完整结构化提取

    提供文档类站点的通用提取逻辑，包括:
    - 标题提取（支持多级标题）
    - 正文提取（支持Markdown转换）
    - 代码块识别（带语言标记）
    - 表格提取（支持复杂表格）
    - 图片提取（含Alt文本）
    - 目录结构识别
    - 面包屑导航
    - 元数据提取

    子类可通过重写以下方法自定义:
        SELECTORS: 自定义CSS选择器
        extract_content(): 自定义内容提取
        extract_metadata(): 自定义元数据提取
        pre_process(): 导航前预处理
        post_process(): 加载后后处理

    Usage:
        class AliyunDocAdapter(DocAdapter):
            name = 'aliyun_doc'
            supported_domains = ['help.aliyun.com']
            
            SELECTORS = {
                'content': ['.article-content', '.content-body'],
                ...
            }
    """

    name = 'doc_adapter'
    supported_domains: List[str] = []

    # 统一选择器配置（子类可覆盖）
    SELECTORS: Dict[str, List[str]] = DEFAULT_SELECTORS.copy()

    # 已知文档站点配置
    KNOWN_DOC_SITES: Dict[str, Dict[str, Any]] = {
        'readthedocs.io': {
            'content_selector': '.markdown-body',
            'heading_selector': 'h1, h2, h3',
            'code_block_selector': '.highlight pre',
        },
        'docs.python.org': {
            'content_selector': '.body',
            'heading_selector': 'h1, h2, h3',
        },
        'help.aliyun.com': {
            'content_selector': '.content-body',
            'heading_selector': 'h1, h2, h3',
            'sidebar_nav': '.sidebar-nav, #catalog',
        },
        'help.cloud.tencent.com': {
            'content_selector': '.doc-content',
            'heading_selector': 'h1, h2, h3',
        },
        'platform.kimi.com': {
            'content_selector': '.api-doc-content',
            'heading_selector': 'h1, h2, h3, h4',
        },
    }

    def __init__(self):
        self._reset_state()

    def _reset_state(self):
        """重置状态"""
        self._page = None
        self._url = ''
        self._selectors = self.SELECTORS.copy()

    # ==================== 核心提取方法 ====================

    def extract(self, page, url: str) -> DocumentItem:
        """
        从文档页面提取完整结构化数据

        Args:
            page: playwright.sync_api.Page
            url: str - 原始URL

        Returns:
            DocumentItem - 包含所有结构化数据
        """
        self._page = page
        self._url = url

        # 提取各项数据
        title = self.extract_title(page)
        author = self.extract_author(page)
        publish_date, last_updated = self.extract_dates(page)
        breadcrumbs = self.extract_breadcrumbs(page)
        toc = self.extract_headings(page)
        content = self.extract_content(page)
        code_blocks = self.extract_code_blocks(page)
        tables = self.extract_tables(page)
        images = self.extract_images(page)
        metadata = self.extract_metadata(page)
        version = self.extract_version(page)

        # 构建DocumentItem
        item = DocumentItem(
            url=url,
            title=title,
            author=author,
            publish_date=publish_date,
            last_updated=last_updated,
            toc=toc,
            content=content,
            code_blocks=code_blocks,
            tables=tables,
            images=images,
            metadata=metadata,
            breadcrumbs=breadcrumbs,
            version=version,
            language=self._detect_language(page, content),
        )

        # 计算质量评分
        item.quality_score = self._calculate_quality(item)

        return item

    def extract_into(self, item: DocumentItem, page, url: str) -> DocumentItem:
        """
        将提取结果写入已存在的DocumentItem

        用于批量提取场景，避免重复创建对象。
        """
        self._page = page
        self._url = url

        item.url = url
        item.title = self.extract_title(page)
        item.author = self.extract_author(page)
        item.publish_date, item.last_updated = self.extract_dates(page)
        item.breadcrumbs = self.extract_breadcrumbs(page)
        item.toc = self.extract_headings(page)
        item.content = self.extract_content(page)
        item.code_blocks = self.extract_code_blocks(page)
        item.tables = self.extract_tables(page)
        item.images = self.extract_images(page)
        item.metadata = self.extract_metadata(page)
        item.version = self.extract_version(page)
        item.language = self._detect_language(page, item.content)
        item.quality_score = self._calculate_quality(item)

        return item

    # ==================== 标题提取 ====================

    def extract_title(self, page) -> str:
        """提取文档标题"""
        selectors = self._selectors.get('title', [])
        
        for sel in selectors:
            try:
                if page.locator(sel).count() > 0:
                    title = page.locator(sel).first.inner_text().strip()
                    if title and len(title) > 2:
                        # 清理标题
                        title = self._clean_text(title)
                        # 去除站点特定后缀
                        title = self._clean_title_suffix(title, page)
                        return title
            except Exception:
                continue
        
        return page.title()

    def _clean_title_suffix(self, title: str, page) -> str:
        """去除标题中的站点后缀"""
        # 常见后缀模式
        patterns = [
            r'\s*[|\-–—]\s*.+$',  # | 或 - 或 — 后面的内容
            r'\s*:\s*.+$',         # : 后面的内容
        ]
        
        for pattern in patterns:
            cleaned = re.sub(pattern, '', title)
            if cleaned != title:
                return cleaned
        
        return title

    # ==================== 内容提取 ====================

    def extract_content(self, page) -> str:
        """提取文档正文"""
        selectors = self._selectors.get('content', [])
        
        for sel in selectors:
            try:
                if page.locator(sel).count() > 0:
                    content = page.locator(sel).first.inner_text()
                    if content and len(content) > 100:
                        return self._clean_content(content)
            except Exception:
                continue
        
        # 回退到body
        try:
            content = page.locator('body').inner_text()
            return self._clean_content(content)
        except Exception:
            return ''

    def _clean_content(self, content: str) -> str:
        """清理内容"""
        if not content:
            return ''

        # 合并连续空白
        content = re.sub(r'\s+', ' ', content)
        # 去除特殊控制字符
        content = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', content)
        # 去除多余空行（超过2个连续空行）
        content = re.sub(r'\n{3,}', '\n\n', content)

        return content.strip()

    # ==================== 标题结构提取 ====================

    def extract_headings(self, page) -> List[HeadingItem]:
        """
        提取目录结构（带层级）

        Returns:
            List[HeadingItem] - 嵌套的标题结构
        """
        headings: List[HeadingItem] = []
        
        # 收集所有标题
        all_headings: List[Tuple[int, str, str]] = []  # (level, text, anchor)
        
        for level in [1, 2, 3, 4, 5, 6]:
            selector_key = f'heading_h{min(level, 4)}'
            selectors = self._selectors.get(selector_key, [f'h{level}'])
            
            for sel in selectors:
                try:
                    locator = page.locator(sel)
                    count = locator.count()
                    for i in range(count):
                        el = locator.nth(i)
                        text = el.inner_text().strip()
                        if text and len(text) > 1:
                            anchor = self._extract_anchor(el)
                            all_headings.append((level, text, anchor))
                except Exception:
                    continue
        
        # 按文档顺序排序
        all_headings.sort(key=lambda x: (
            page.locator(f'h{x[0]}').all().index(page.locator(f'h{x[0]}', has_text=x[1])) 
            if page.locator(f'h{x[0]}', has_text=x[1]).count() > 0 else 999
        ))

        # 构建树形结构
        headings = self._build_heading_tree(all_headings)

        return headings

    def _extract_anchor(self, locator: 'Locator') -> str:
        """提取标题锚点"""
        try:
            # 优先从id获取
            if locator.get_attribute('id'):
                return locator.get_attribute('id')
            # 其次从href获取（常见的锚点格式）
            href = locator.locator('a').first.get_attribute('href') if locator.locator('a').count() > 0 else None
            if href and href.startswith('#'):
                return href[1:]
        except Exception:
            pass
        
        # 从文本生成
        text = locator.inner_text().strip()
        anchor = re.sub(r'[^\w\u4e00-\u9fff\-_]', '-', text.lower())
        anchor = re.sub(r'-+', '-', anchor).strip('-')
        return anchor

    def _build_heading_tree(self, headings: List[Tuple[int, str, str]]) -> List[HeadingItem]:
        """构建标题树形结构"""
        if not headings:
            return []

        root: List[HeadingItem] = []
        stack: List[HeadingItem] = []

        for level, text, anchor in headings:
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

    def extract_headings_flat(self, page) -> List[str]:
        """
        提取扁平标题列表（兼容旧接口）

        Returns:
            List[str] - 标题文本列表
        """
        headings = self.extract_headings(page)
        result = []
        
        def flatten(items):
            for item in items:
                result.append(item.text)
                if item.children:
                    flatten(item.children)
        
        flatten(headings)
        return result

    # ==================== 代码块提取 ====================

    def extract_code_blocks(self, page) -> List[CodeBlock]:
        """
        提取代码块列表

        Returns:
            List[CodeBlock] - 代码块列表
        """
        code_blocks: List[CodeBlock] = []
        selectors = self._selectors.get('code_block', [])

        for sel in selectors:
            try:
                locator = page.locator(sel)
                count = locator.count()
                
                for i in range(count):
                    el = locator.nth(i)
                    code_block = self._parse_code_block(el)
                    if code_block and code_block.code.strip():
                        code_blocks.append(code_block)
            except Exception:
                continue

        return code_blocks

    def _parse_code_block(self, locator: 'Locator') -> Optional[CodeBlock]:
        """解析单个代码块"""
        try:
            # 尝试获取代码内容
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

    def _detect_code_language(self, locator: 'Locator') -> str:
        """检测代码语言"""
        # 从class中检测
        try:
            class_attr = locator.get_attribute('class') or ''
            
            # 常见语言模式
            lang_patterns = [
                r'language-(\w+)', r'lang-(\w+)', r'highlight-(\w+)',
                r'brush:(\w+)', r'coder-(\w+)'
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
        # Rust
        if 'fn ' in code_lower and 'let mut' in code_lower:
            return 'rust'
        # SQL
        if any(k in code_lower for k in ['select ', 'from ', 'where ', 'insert into', 'update ']):
            return 'sql'
        # Shell
        if code.startswith('#!/') or 'echo ' in code_lower or 'export ' in code_lower:
            return 'bash'
        # HTML
        if '<html' in code_lower or '<div' in code_lower or '<!doctype' in code_lower:
            return 'html'
        # CSS
        if '{' in code and any(k in code_lower for k in ['color:', 'margin:', 'padding:', 'background:']):
            return 'css'
        
        return ''

    def _detect_code_filename(self, locator: 'Locator') -> Optional[str]:
        """检测代码文件名"""
        try:
            # 从data属性
            for attr in ['data-filename', 'data-file', 'filename', 'data-src']:
                filename = locator.get_attribute(attr)
                if filename:
                    return filename
            
            # 从class或title
            for attr in ['class', 'title']:
                value = locator.get_attribute(attr) or ''
                match = re.search(r'filename[:\s]*([^\s]+)', value, re.IGNORECASE)
                if match:
                    return match.group(1)
        except Exception:
            pass
        
        return None

    def _detect_code_lines(self, locator: 'Locator') -> Tuple[int, int]:
        """检测代码行号"""
        try:
            # 尝试从data属性获取
            line_start = locator.get_attribute('data-line-start')
            line_end = locator.get_attribute('data-line-end')
            
            if line_start and line_end:
                return int(line_start), int(line_end)
            
            # 尝试从class检测
            class_attr = locator.get_attribute('class') or ''
            match = re.search(r'lines-(\d+)(?:-(\d+))?', class_attr)
            if match:
                start = int(match.group(1))
                end = int(match.group(2)) if match.group(2) else start
                return start, end
        except Exception:
            pass
        
        return 0, 0

    # ==================== 表格提取 ====================

    def extract_tables(self, page) -> List[TableItem]:
        """
        提取表格列表

        Returns:
            List[TableItem] - 表格列表
        """
        tables: List[TableItem] = []
        selectors = self._selectors.get('table', ['table'])

        for sel in selectors:
            try:
                locator = page.locator(sel)
                count = locator.count()
                
                for i in range(count):
                    el = locator.nth(i)
                    table = self._parse_table(el)
                    if table:
                        tables.append(table)
            except Exception:
                continue

        return tables

    def _parse_table(self, locator: 'Locator') -> Optional[TableItem]:
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
                header_locator = locator.locator('thead th, thead th[scope="col"]')
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
                    if cells and cells != headers:  # 跳过表头行
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

    # ==================== 图片提取 ====================

    def extract_images(self, page) -> List[ImageItem]:
        """
        提取图片列表

        Returns:
            List[ImageItem] - 图片列表
        """
        images: List[ImageItem] = []
        selectors = self._selectors.get('image', ['img'])

        for sel in selectors:
            try:
                locator = page.locator(sel)
                count = locator.count()
                
                for i in range(count):
                    el = locator.nth(i)
                    img = self._parse_image(el)
                    if img and img.src:
                        images.append(img)
            except Exception:
                continue

        return images

    def _parse_image(self, locator: 'Locator') -> Optional[ImageItem]:
        """解析单个图片"""
        try:
            src = locator.get_attribute('src') or locator.get_attribute('data-src') or ''
            
            if not src:
                return None
            
            # 过滤图标等小图
            width = locator.get_attribute('width')
            height = locator.get_attribute('height')
            
            return ImageItem(
                src=src,
                alt=locator.get_attribute('alt') or '',
                title=locator.get_attribute('title'),
                width=int(width) if width and width.isdigit() else None,
                height=int(height) if height and height.isdigit() else None,
                loading=locator.get_attribute('loading') or 'lazy',
            )
        except Exception:
            return None

    # ==================== 元数据提取 ====================

    def extract_author(self, page) -> Optional[str]:
        """提取作者"""
        selectors = self._selectors.get('author', [])
        
        for sel in selectors:
            try:
                if page.locator(sel).count() > 0:
                    author = page.locator(sel).first.inner_text().strip()
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
        
        selectors = self._selectors.get('publish_date', [])
        
        for sel in selectors:
            try:
                if page.locator(sel).count() > 0:
                    date_text = page.locator(sel).first.inner_text().strip()
                    if date_text:
                        # 尝试解析日期
                        parsed = self._parse_date(date_text)
                        if parsed:
                            if not publish_date:
                                publish_date = parsed
                            elif not last_updated:
                                last_updated = parsed
                        
                        if publish_date and last_updated:
                            break
            except Exception:
                continue
        
        return publish_date, last_updated

    def _parse_date(self, date_str: str) -> Optional[str]:
        """解析日期字符串"""
        # 常见日期格式
        patterns = [
            (r'\d{4}-\d{2}-\d{2}', '%Y-%m-%d'),
            (r'\d{4}/\d{2}/\d{2}', '%Y/%m/%d'),
            (r'\d{4}年\d{1,2}月\d{1,2}日', '%Y年%m月%d日'),
        ]
        
        for pattern, _ in patterns:
            match = re.search(pattern, date_str)
            if match:
                try:
                    from datetime import datetime
                    dt = datetime.strptime(match.group(), patterns[[p for p, _ in patterns].index(pattern)][1])
                    return dt.strftime('%Y-%m-%d')
                except Exception:
                    pass
        
        # 回退：返回原始文本
        return date_str.strip()[:20] if date_str else None

    def extract_version(self, page) -> str:
        """提取文档版本"""
        selectors = self._selectors.get('version', [])
        
        for sel in selectors:
            try:
                if page.locator(sel).count() > 0:
                    version = page.locator(sel).first.inner_text().strip()
                    if version and len(version) < 50:
                        return version
            except Exception:
                continue
        
        return ''

    def extract_breadcrumbs(self, page) -> List[str]:
        """提取面包屑导航"""
        breadcrumbs: List[str] = []
        selectors = self._selectors.get('breadcrumb', [])
        
        for sel in selectors:
            try:
                if page.locator(sel).count() > 0:
                    items = page.locator(sel).first.locator('a, span, li').all()
                    for el in items:
                        text = el.inner_text().strip()
                        if text and text not in ['>', '/', '\\']:
                            breadcrumbs.append(text)
                    
                    if breadcrumbs:
                        break
            except Exception:
                continue
        
        return breadcrumbs

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
        
        for sel in ['[class*="tag"]', '.topic', 'a[rel="tag"]', '[itemprop="keywords"]']:
            try:
                if page.locator(sel).count() > 0:
                    for el in page.locator(sel).all():
                        text = el.inner_text().strip()
                        if text and len(text) < 30:
                            tags.append(text)
            except Exception:
                continue
        
        return tags[:10]  # 最多10个

    def _detect_language(self, page, content: str) -> str:
        """检测文档语言"""
        # 从html lang属性
        try:
            lang = page.evaluate('document.documentElement.lang')
            if lang:
                return lang[:2].lower()
        except Exception:
            pass
        
        # 从内容推断
        sample = content[:500].lower() if content else ''
        
        zh_chars = len(re.findall(r'[\u4e00-\u9fff]', sample))
        en_words = len(re.findall(r'[a-zA-Z]+', sample))
        
        if zh_chars > en_words * 0.3:
            return 'zh'
        
        return 'en'

    # ==================== 质量评估 ====================

    def _calculate_quality(self, item: DocumentItem) -> float:
        """
        计算内容质量分数

        评估因素:
        - 内容长度（太短质量低）
        - 代码块数量（有代码质量高）
        - 标题层级（层级丰富质量高）
        - 表格数量（信息密度高）
        """
        score = 0.3  # 基础分

        # 内容长度
        content_len = len(item.content)
        if content_len > 500:
            score += 0.1
        if content_len > 2000:
            score += 0.1
        if content_len > 5000:
            score += 0.1
        if content_len > 10000:
            score += 0.1

        # 代码块
        code_count = item.code_block_count
        if code_count > 0:
            score += 0.1
        if code_count >= 3:
            score += 0.1

        # 标题层级
        heading_count = item.heading_count
        if heading_count >= 3:
            score += 0.1
        if heading_count >= 10:
            score += 0.1

        # 表格
        if item.table_count > 0:
            score += 0.05

        # 图片
        if item.image_count > 0:
            score += 0.05

        return min(1.0, score)

    # ==================== 文本处理工具 ====================

    def _clean_text(self, text: str) -> str:
        """通用文本清理"""
        if not text:
            return ''
        
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 去除特殊字符
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', text)
        
        return text.strip()

    # ==================== 生命周期方法 ====================

    def before_navigate(self, page, url: str):
        """导航前准备"""
        self._reset_state()
        
        # 根据域名加载特定配置
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        
        for known_domain, config in self.KNOWN_DOC_SITES.items():
            if known_domain in domain:
                self._apply_site_config(config)
                break

    def _apply_site_config(self, config: Dict[str, Any]):
        """应用站点特定配置"""
        # 可以用站点特定选择器覆盖默认选择器
        for key, value in config.items():
            if key.endswith('_selector') and value:
                selector_key = key.replace('_selector', '')
                self._selectors[selector_key] = [value]

    def after_load(self, page, url: str):
        """页面加载后处理"""
        # 等待主要内容加载
        try:
            for sel in self._selectors.get('content', ['article', 'main']):
                if page.locator(sel).count() > 0:
                    page.wait_for_selector(sel, timeout=5000)
                    break
        except Exception:
            pass

    # ==================== 兼容性方法 ====================

    def extract_content_simple(self, page) -> str:
        """
        简单内容提取（兼容旧接口）
        仅提取正文文本，不包含代码块和表格
        """
        return self.extract_content(page)

    def _count_elements(self, page, selectors: List[str]) -> int:
        """统计元素数量（兼容旧接口）"""
        count = 0
        for sel in selectors:
            try:
                count += page.locator(sel).count()
            except Exception:
                pass
        return count


# ==================== 适配器注册表 ====================

class AdapterRegistry:
    """
    适配器注册表

    提供全局适配器注册和查询功能。

    Usage:
        registry = AdapterRegistry()
        registry.register('aliyun', AliyunDocAdapter())
        
        adapter = registry.get_for_url('https://help.aliyun.com/doc')
    """

    def __init__(self):
        self._adapters: Dict[str, BaseAdapter] = {}
        self._domains: Dict[str, str] = {}  # domain -> adapter_name

    def register(self, name: str, adapter: BaseAdapter):
        """注册适配器"""
        self._adapters[name] = adapter
        for domain in adapter.supported_domains:
            self._domains[domain] = name

    def get(self, name: str) -> Optional[BaseAdapter]:
        """按名称获取适配器"""
        return self._adapters.get(name)

    def get_for_url(self, url: str) -> Optional[BaseAdapter]:
        """根据URL获取适配器"""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc

        # 精确匹配
        if domain in self._domains:
            return self._adapters[self._domains[domain]]

        # 部分匹配
        for known_domain, adapter_name in self._domains.items():
            if known_domain in domain or domain in known_domain:
                return self._adapters[adapter_name]

        return None

    def detect(self, url: str) -> Optional[str]:
        """根据URL检测适配器名称"""
        adapter = self.get_for_url(url)
        return adapter.name if adapter else None

    def list_all(self) -> List[str]:
        """列出所有适配器"""
        return list(self._adapters.keys())

    def unregister(self, name: str):
        """取消注册"""
        if name in self._adapters:
            adapter = self._adapters.pop(name)
            # 清理域名映射
            domains_to_remove = [d for d, n in self._domains.items() if n == name]
            for d in domains_to_remove:
                del self._domains[d]


# 全局注册表
_global_registry = AdapterRegistry()


def get_registry() -> AdapterRegistry:
    """获取全局适配器注册表"""
    return _global_registry


def register_adapter(name: str, adapter: BaseAdapter):
    """注册到全局注册表"""
    _global_registry.register(name, adapter)


def detect_adapter(url: str) -> Optional[str]:
    """检测URL对应的适配器名称"""
    return _global_registry.detect(url)


# ==================== 导出 ====================

__all__ = [
    # 基类
    'BaseAdapter',
    'DocAdapter',
    
    # 注册表
    'AdapterRegistry',
    'get_registry',
    'register_adapter',
    'detect_adapter',
    
    # 选择器
    'DEFAULT_SELECTORS',
    
    # 数据模型（重新导出）
    'DocumentItem',
    'HeadingItem',
    'CodeBlock',
    'TableItem',
    'ImageItem',
]
