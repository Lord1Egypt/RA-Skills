"""类型定义 - PDF Reader"""
from typing import TypedDict, List, Optional, Dict, Any
from dataclasses import dataclass, field


class FontInfo(TypedDict, total=False):
    """字体信息"""
    name: str
    size: float
    bold: bool
    italic: bool


class BBox(TypedDict, total=False):
    """边界框 [x0, y0, x1, y1]"""
    x0: float
    y0: float
    x1: float
    y1: float


class ImageRef(TypedDict):
    """图片引用"""
    ref: str
    bbox: BBox
    width: int
    height: int


class Line(TypedDict):
    """行数据"""
    line_num: int
    text: str


class Block(TypedDict):
    """块数据"""
    block_id: int
    page_idx: int
    type: str  # heading|paragraph|caption|image|table|formula|mixed
    level: int  # 标题层级 1-6
    y_range: List[float]  # [y0, y1]
    x_range: List[float]  # [x0, x1]
    font: Optional[FontInfo]
    global_line_start: int
    lines: List[Line]
    images: List[ImageRef]


class TOCEntry(TypedDict):
    """目录条目"""
    title: str
    page: int
    block_id: int


class PDFMeta(TypedDict):
    """PDF元数据"""
    pdf_path: str
    total_pages: int
    total_blocks: int
    has_toc: bool
    is_scanned: bool
    layout: str  # single|multi
    index_generated: bool


class PageData(TypedDict):
    """页面数据"""
    blocks: List[Block]


class Bookmark(TypedDict):
    """书签"""
    id: int
    page: int
    block_id: int
    note: str
    created_at: str


class SearchResult(TypedDict):
    """搜索结果"""
    keyword: str
    page: int
    block_id: int
    snippet: str


# 阅读模式
class ReadingMode:
    BLOCK = "block"
    LINE = "line"
    PARAGRAPH = "paragraph"
    PAGE = "page"


# 块类型
class BlockType:
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CAPTION = "caption"
    IMAGE = "image"
    TABLE = "table"
    FORMULA = "formula"
    MIXED = "mixed"
