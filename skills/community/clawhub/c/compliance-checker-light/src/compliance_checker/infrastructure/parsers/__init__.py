"""
文档解析器模块 - Infrastructure 层

提供各种文档格式的解析功能，实现 Core 层定义的 DocumentParserProtocol 接口。
"""

from .pdf_parser import PDFParser, parse_pdf
from .docx_parser import DocxParser, parse_docx
from .image_parser import ImageParser, parse_image

__all__ = [
    # PDF 解析器
    "PDFParser",
    "parse_pdf",
    # Word 解析器
    "DocxParser",
    "parse_docx",
    # 图片解析器
    "ImageParser",
    "parse_image",
]
