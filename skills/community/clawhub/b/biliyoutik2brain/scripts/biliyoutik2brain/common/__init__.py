"""公共模块层 — 格式转换、工具函数，零外部依赖"""
from .format_converter import md_to_html, md_to_json

__all__ = ["md_to_html", "md_to_json"]
