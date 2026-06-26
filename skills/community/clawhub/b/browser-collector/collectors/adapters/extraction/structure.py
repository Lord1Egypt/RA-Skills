#!/usr/bin/env python3
"""
collectors/adapters/extraction/structure.py - 结构化数据模型

定义文档结构化提取的完整数据模型:
- DocumentItem: 完整文档结构
- HeadingItem: 章节/标题
- CodeBlock: 代码块
- TableItem: 表格
- ImageItem: 图片
- ApiEndpoint: API端点

Usage:
    from collectors.adapters.extraction.structure import (
        DocumentItem, HeadingItem, CodeBlock, TableItem, ImageItem
    )
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime
import hashlib


@dataclass
class HeadingItem:
    """文档章节/标题"""
    level: int          # H1-H6 (1-6)
    text: str           # 标题文本
    anchor: str = ''    # 锚点ID
    children: List['HeadingItem'] = field(default_factory=list)  # 子标题

    def to_dict(self) -> Dict[str, Any]:
        return {
            'level': self.level,
            'text': self.text,
            'anchor': self.anchor,
            'children': [c.to_dict() if isinstance(c, HeadingItem) else c for c in self.children]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HeadingItem':
        children = [cls.from_dict(c) if isinstance(c, dict) else c 
                   for c in data.get('children', [])]
        return cls(
            level=data['level'],
            text=data['text'],
            anchor=data.get('anchor', ''),
            children=children
        )


@dataclass
class CodeBlock:
    """代码块"""
    language: str = ''           # 代码语言 (python/js/go等)
    code: str = ''               # 代码内容
    filename: Optional[str] = None  # 可选文件名
    line_start: int = 0          # 开始行号
    line_end: int = 0            # 结束行号
    highlight_lines: List[int] = field(default_factory=list)  # 高亮行

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CodeBlock':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def __str__(self):
        preview = self.code[:80].replace('\n', ' ')
        return f"<CodeBlock [{self.language}] '{preview}...'>"


@dataclass
class TableItem:
    """表格"""
    headers: List[str] = field(default_factory=list)      # 表头
    rows: List[List[str]] = field(default_factory=list)    # 数据行
    caption: Optional[str] = None     # 表格标题/说明
    alignment: List[str] = field(default_factory=list)     # 列对齐方式

    @property
    def col_count(self) -> int:
        return len(self.headers) if self.headers else (len(self.rows[0]) if self.rows else 0)

    @property
    def row_count(self) -> int:
        return len(self.rows)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'headers': self.headers,
            'rows': self.rows,
            'caption': self.caption,
            'alignment': self.alignment,
            'col_count': self.col_count,
            'row_count': self.row_count,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TableItem':
        allowed = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in allowed})

    def to_markdown(self) -> str:
        """转为Markdown表格"""
        lines = []
        if self.caption:
            lines.append(f"**{self.caption}**")
        
        if not self.headers and not self.rows:
            return ''
        
        # 表头
        header_line = '| ' + ' | '.join(self.headers) + ' |' if self.headers else ''
        lines.append(header_line)
        
        # 分隔行
        if self.headers:
            sep = '| ' + ' | '.join(['---'] * len(self.headers)) + ' |'
            lines.append(sep)
        
        # 数据行
        for row in self.rows:
            lines.append('| ' + ' | '.join(str(c) for c in row) + ' |')
        
        return '\n'.join(lines)

    def __str__(self):
        return f"<TableItem {self.col_count}x{self.row_count}>"


@dataclass
class ImageItem:
    """图片"""
    src: str = ''                 # 图片URL
    alt: str = ''                 # Alt文本
    title: Optional[str] = None   # 标题
    width: Optional[int] = None   # 宽度
    height: Optional[int] = None  # 高度
    loading: str = 'lazy'         # 加载策略 (lazy/eager)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'src': self.src,
            'alt': self.alt,
            'title': self.title,
            'width': self.width,
            'height': self.height,
            'loading': self.loading,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ImageItem':
        allowed = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in allowed})

    def __str__(self):
        alt_preview = self.alt[:30] if self.alt else 'no-alt'
        return f"<ImageItem {alt_preview}>"


@dataclass
class ApiEndpoint:
    """API端点"""
    path: str = ''                  # 端点路径 (e.g., /v1/chat/completions)
    method: str = 'GET'             # HTTP方法
    description: str = ''           # 端点描述
    summary: str = ''               # 简短摘要
    parameters: List[Dict[str, Any]] = field(default_factory=list)  # 参数列表
    request_body: Optional[Dict[str, Any]] = None  # 请求体Schema
    request_example: Optional[str] = None  # 请求示例
    response_example: Optional[str] = None  # 响应示例
    tags: List[str] = field(default_factory=list)  # 所属分类标签
    deprecated: bool = False        # 是否废弃
    security: List[str] = field(default_factory=list)  # 安全要求

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ApiEndpoint':
        allowed = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in allowed})

    def __str__(self):
        return f"<ApiEndpoint {self.method} {self.path}>"


@dataclass
class ModelInfo:
    """AI模型信息"""
    name: str = ''                  # 模型名称
    display_name: str = ''         # 显示名称
    description: str = ''          # 模型描述
    context_window: int = 0        # 上下文窗口大小
    capabilities: List[str] = field(default_factory=list)  # 能力列表
    input_modalities: List[str] = field(default_factory=list)  # 输入模式
    output_modalities: List[str] = field(default_factory=list)  # 输出模式
    pricing: Optional[Dict[str, float]] = None  # 价格信息
    version: str = ''               # 版本
    deprecated: bool = False        # 是否废弃

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelInfo':
        allowed = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in allowed})


@dataclass
class DocumentItem:
    """
    完整文档结构化数据

    包含文档的所有结构化组成部分，支持JSON和Markdown双格式输出。

    Usage:
        item = DocumentItem(
            url="https://help.aliyun.com/doc",
            title="使用指南",
            author="阿里云",
            publish_date="2024-01-15",
        )
        item.extract_from_page(page)
        
        # JSON输出
        print(item.to_json())
        
        # Markdown输出
        print(item.to_markdown())
    """
    # 基础信息
    url: str = ''
    title: str = ''
    author: Optional[str] = None
    publish_date: Optional[str] = None
    last_updated: Optional[str] = None
    
    # 结构化内容
    toc: List[HeadingItem] = field(default_factory=list)      # 目录章节
    content: str = ''                                         # 正文（markdown）
    code_blocks: List[CodeBlock] = field(default_factory=list) # 代码块列表
    tables: List[TableItem] = field(default_factory=list)      # 表格列表
    images: List[ImageItem] = field(default_factory=list)      # 图片列表
    
    # 扩展信息
    metadata: Dict[str, Any] = field(default_factory=dict)    # 额外元数据
    breadcrumbs: List[str] = field(default_factory=list)       # 面包屑导航
    version: str = ''                                         # 文档版本
    language: str = 'zh'                                      # 文档语言
    
    # 质量评估
    quality_score: float = 0.0
    checksum: str = ''                                        # 内容MD5校验和

    def __post_init__(self):
        """计算校验和"""
        if not self.checksum and self.content:
            self.checksum = hashlib.md5(self.content[:5000].encode()).hexdigest()[:12]

    # ==================== 提取方法 ====================

    def extract_from_page(self, page, url: str) -> 'DocumentItem':
        """
        从Playwright Page提取完整文档结构

        Args:
            page: playwright.sync_api.Page
            url: str - 原始URL

        Returns:
            self - 便于链式调用
        """
        from .base import DocAdapter
        
        # 创建临时适配器进行提取
        adapter = DocAdapter()
        adapter.extract_into(self, page, url)
        return self

    # ==================== 序列化方法 ====================

    def to_dict(self) -> Dict[str, Any]:
        """转为dict"""
        return {
            'url': self.url,
            'title': self.title,
            'author': self.author,
            'publish_date': self.publish_date,
            'last_updated': self.last_updated,
            'toc': [h.to_dict() if isinstance(h, HeadingItem) else h for h in self.toc],
            'content': self.content,
            'code_blocks': [cb.to_dict() if isinstance(cb, CodeBlock) else cb for cb in self.code_blocks],
            'tables': [t.to_dict() if isinstance(t, TableItem) else t for t in self.tables],
            'images': [img.to_dict() if isinstance(img, ImageItem) else img for img in self.images],
            'metadata': self.metadata,
            'breadcrumbs': self.breadcrumbs,
            'version': self.version,
            'language': self.language,
            'quality_score': self.quality_score,
            'checksum': self.checksum,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocumentItem':
        """从dict恢复"""
        # 处理嵌套类型
        if 'toc' in data:
            data['toc'] = [HeadingItem.from_dict(h) if isinstance(h, dict) else h for h in data['toc']]
        if 'code_blocks' in data:
            data['code_blocks'] = [CodeBlock.from_dict(cb) if isinstance(cb, dict) else cb for cb in data['code_blocks']]
        if 'tables' in data:
            data['tables'] = [TableItem.from_dict(t) if isinstance(t, dict) else t for t in data['tables']]
        if 'images' in data:
            data['images'] = [ImageItem.from_dict(img) if isinstance(img, dict) else img for img in data['images']]
        
        allowed = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in allowed})

    def to_json(self, indent: int = 2) -> str:
        """转为JSON字符串"""
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> 'DocumentItem':
        """从JSON恢复"""
        import json
        return cls.from_dict(json.loads(json_str))

    def to_markdown(self) -> str:
        """
        转为Markdown格式

        包含:
        - 标题层级结构
        - 正文内容
        - 代码块（带语言标记）
        - 表格（Markdown格式）
        - 图片
        """
        lines = []

        # 元信息
        if self.title:
            lines.append(f"# {self.title}\n")
        
        # 面包屑/导航
        if self.breadcrumbs:
            lines.append(' > '.join(self.breadcrumbs))
            lines.append('')

        # 元数据
        meta_parts = []
        if self.author:
            meta_parts.append(f"**作者**: {self.author}")
        if self.publish_date:
            meta_parts.append(f"**发布日期**: {self.publish_date}")
        if self.last_updated:
            meta_parts.append(f"**更新日期**: {self.last_updated}")
        if self.version:
            meta_parts.append(f"**版本**: {self.version}")
        if meta_parts:
            lines.append(' | '.join(meta_parts))
            lines.append('')

        # 目录
        if self.toc:
            lines.append("## 目录\n")
            for heading in self.toc:
                lines.append(self._format_toc_item(heading))
            lines.append('')

        # 正文内容（如果有不同于code_blocks/tables的内容）
        if self.content and self.content.strip():
            lines.append(self.content)
            lines.append('')

        # 代码块
        if self.code_blocks:
            lines.append("## 代码示例\n")
            for i, cb in enumerate(self.code_blocks, 1):
                lines.append(f"### 示例 {i}: {cb.language or 'code'}\n")
                if cb.filename:
                    lines.append(f"**文件**: `{cb.filename}`\n")
                lines.append(f"```{cb.language}\n{cb.code}\n```\n")

        # 表格
        if self.tables:
            lines.append("## 数据表格\n")
            for i, table in enumerate(self.tables, 1):
                if table.caption:
                    lines.append(f"### 表格 {i}: {table.caption}\n")
                lines.append(table.to_markdown())
                lines.append('')

        # 图片
        if self.images:
            lines.append("## 图片\n")
            for img in self.images:
                alt = img.alt or 'image'
                lines.append(f"![{alt}]({img.src})\n")

        return '\n'.join(lines)

    def _format_toc_item(self, heading: HeadingItem, level: int = 0) -> str:
        """格式化目录项"""
        indent = '  ' * (heading.level - 1)
        anchor = f"#{heading.anchor}" if heading.anchor else ''
        line = f"{indent}- [{heading.text}](#{heading.anchor})\n"
        
        for child in heading.children:
            line += self._format_toc_item(child, level + 1)
        
        return line

    # ==================== 统计方法 ====================

    @property
    def heading_count(self) -> int:
        """标题总数"""
        def count_recursive(headings):
            count = len(headings)
            for h in headings:
                if h.children:
                    count += count_recursive(h.children)
            return count
        return count_recursive(self.toc)

    @property
    def code_block_count(self) -> int:
        """代码块数量"""
        return len(self.code_blocks)

    @property
    def table_count(self) -> int:
        """表格数量"""
        return len(self.tables)

    @property
    def image_count(self) -> int:
        """图片数量"""
        return len(self.images)

    @property
    def word_count(self) -> int:
        """字数统计"""
        return len(self.content.split())

    @property
    def reading_time_minutes(self) -> int:
        """预估阅读时间（分钟）"""
        return max(1, self.word_count // 200)

    def summary(self) -> str:
        """返回摘要信息"""
        return (
            f"DocumentItem("
            f"title='{self.title[:30]}...', "
            f"headings={self.heading_count}, "
            f"code_blocks={self.code_block_count}, "
            f"tables={self.table_count}, "
            f"images={self.image_count}, "
            f"words={self.word_count}, "
            f"reading_time={self.reading_time_minutes}min)"
        )

    def __str__(self):
        return self.summary()

    def __repr__(self):
        return f"<DocumentItem '{self.title[:50]}' score={self.quality_score:.2f}>"


# ==================== 导出 ====================

__all__ = [
    'HeadingItem',
    'CodeBlock',
    'TableItem',
    'ImageItem',
    'ApiEndpoint',
    'ModelInfo',
    'DocumentItem',
]
