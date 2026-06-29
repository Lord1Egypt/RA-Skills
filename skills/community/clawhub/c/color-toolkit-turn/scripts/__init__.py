#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Color Toolkit - 通用颜色工具包

使用方法:
    from color_toolkit import convert_color, get_contrast, recommend_color

    # 颜色转换
    result = convert_color("#3498db")

    # 对比度计算
    result = get_contrast("#000000", "#ffffff")

    # 智能推荐
    from color_recommender import recommend_color
    result = recommend_color("科技感 蓝色")
"""

from color_toolkit import (
    ColorCore,
    RGB, HSL, HSV, CMYK, ColorInfo,
    ContrastEvaluation, ContrastResult,
    convert_color,
    get_contrast,
    get_complementary,
    get_palette,
)

from color_recommender import recommend_color
from preview_generator import generate_full_preview_html, generate_palette_page_html

__all__ = [
    # 核心类
    "ColorCore",
    "RGB", "HSL", "HSV", "CMYK", "ColorInfo",
    "ContrastEvaluation", "ContrastResult",
    # 函数
    "convert_color",
    "get_contrast",
    "get_complementary",
    "get_palette",
    "recommend_color",
    "generate_full_preview_html",
    "generate_palette_page_html",
]

__version__ = "1.0.0"
