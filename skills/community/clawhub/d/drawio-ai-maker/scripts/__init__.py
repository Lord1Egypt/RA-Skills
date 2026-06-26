"""
drawio-generator agent-harness
自然语言/文档 → draw.io 图表自动生成

主要模块：
- parser: 输入解析（txt/md/docx/pdf）
- designer: LLM 生成结构化设计描述
- generator: JSON → draw.io XML
- renderer: draw.io CLI → PNG
- schemas: JSON Schema 定义
"""

__version__ = '1.0.0'
__author__ = 'drawio-generator'

from .parser import parse_input, extract_structure_from_text
from .designer import generate_structured_description
from .generator import generate_drawio_xml, validate_xml, get_element_count
from .renderer import render_to_png, render_to_svg, check_drawio_available
from .schemas import (
    NODE_TYPES,
    CHART_TYPES,
    LAYOUT_DIRECTIONS,
    DESIGN_JSON_SCHEMA,
    STYLE_REFERENCE,
    get_style,
    validate_design,
)

__all__ = [
    # parser
    'parse_input',
    'extract_structure_from_text',
    # designer
    'generate_structured_description',
    # generator
    'generate_drawio_xml',
    'validate_xml',
    'get_element_count',
    # renderer
    'render_to_png',
    'render_to_svg',
    'check_drawio_available',
    # schemas
    'NODE_TYPES',
    'CHART_TYPES',
    'LAYOUT_DIRECTIONS',
    'DESIGN_JSON_SCHEMA',
    'STYLE_REFERENCE',
    'get_style',
    'validate_design',
]
