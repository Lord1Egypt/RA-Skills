#!/usr/bin/env python3
"""
PDF Document Generator
Generates .pdf files from JSON configuration
"""

import json
import sys
import platform
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4, legal
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


# ──────────────────────────────────────────────
#  全局常量：统一内部字体名
# ──────────────────────────────────────────────
CHINESE_FONT_NAME       = 'ChineseFont'
CHINESE_FONT_NAME_BOLD  = 'ChineseFont-Bold'
CHINESE_FONT_NAME_ITALIC = 'ChineseFont-Italic'
CHINESE_FONT_NAME_BI    = 'ChineseFont-BoldItalic'


def hex_to_color(hex_color):
    """Convert hex color to reportlab Color"""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return colors.Color(r / 255, g / 255, b / 255)


# ──────────────────────────────────────────────
#  修复 1 — 跨平台字体搜索 + 字体家族注册
# ──────────────────────────────────────────────
def _collect_candidate_fonts():
    """
    返回 (font_path, bold_path_or_None) 的候选列表，
    按平台收集常见中文字体路径。
    """
    system = platform.system()
    candidates = []

    if system == 'Windows':
        base = 'C:/Windows/Fonts'
        candidates = [
            # (regular, bold_variant)
            (f'{base}/simhei.ttf',   None),                # 黑体
            (f'{base}/msyh.ttc',     f'{base}/msyhbd.ttc'), # 微软雅黑 + 粗体
            (f'{base}/simsun.ttc',   None),                # 宋体
            (f'{base}/simkai.ttf',   None),                # 楷体
            (f'{base}/STKAITI.TTF',  None),                # 华文楷体
            (f'{base}/STSONG.TTF',   None),                # 华文宋体
        ]

    elif system == 'Darwin':  # macOS
        lib = '/Library/Fonts'
        sys_lib = '/System/Library/Fonts'
        sup = f'{sys_lib}/Supplemental'
        candidates = [
            (f'{sys_lib}/PingFang.ttc',        None),
            (f'{sys_lib}/STHeiti Light.ttc',    f'{sys_lib}/STHeiti Medium.ttc'),
            (f'{sup}/Songti.ttc',              None),
            (f'{sup}/Arial Unicode.ttf',       None),
            (f'{lib}/华文黑体.ttf',              None),
        ]

    else:  # Linux / other
        share = '/usr/share/fonts'
        candidates = [
            (f'{share}/truetype/wqy/wqy-zenhei.ttc',         None),
            (f'{share}/truetype/wqy/wqy-microhei.ttc',       None),
            (f'{share}/opentype/noto/NotoSansCJK-Regular.ttc', None),
            (f'{share}/truetype/noto/NotoSansCJK-Regular.ttc', None),
            (f'{share}/truetype/droid/DroidSansFallbackFull.ttf', None),
            (f'{share}/truetype/arphic/uming.ttc',            None),
        ]

    return candidates


def _try_register(internal_name, font_path, sub_index=0):
    """尝试用 TTFont 注册单个字体，返回 True/False"""
    try:
        pdfmetrics.registerFont(
            TTFont(internal_name, font_path, subfontIndex=sub_index)
        )
        return True
    except Exception:
        pass
    # 某些旧版 reportlab 不支持 subfontIndex
    try:
        pdfmetrics.registerFont(TTFont(internal_name, font_path))
        return True
    except Exception:
        return False


def register_chinese_fonts():
    """
    注册中文字体并建立 **字体家族映射**，
    确保 <b> / <i> 标签仍然使用中文字体而不回退到 Helvetica。
    """
    candidates = _collect_candidate_fonts()

    for regular_path, bold_path in candidates:
        if not os.path.exists(regular_path):
            continue

        ok = _try_register(CHINESE_FONT_NAME, regular_path)
        if not ok:
            continue

        # ── 尝试注册粗体变体 ──
        bold_ok = False
        if bold_path and os.path.exists(bold_path):
            bold_ok = _try_register(CHINESE_FONT_NAME_BOLD, bold_path)
        if not bold_ok:
            # 没有专用粗体文件 → 复用 regular
            _try_register(CHINESE_FONT_NAME_BOLD, regular_path)

        # ── 斜体 / 粗斜体一律复用 regular ──
        _try_register(CHINESE_FONT_NAME_ITALIC, regular_path)
        _try_register(CHINESE_FONT_NAME_BI, regular_path)

        # ── 关键：注册字体家族 ──
        from reportlab.pdfbase.pdfmetrics import registerFontFamily
        registerFontFamily(
            CHINESE_FONT_NAME,
            normal=CHINESE_FONT_NAME,
            bold=CHINESE_FONT_NAME_BOLD,
            italic=CHINESE_FONT_NAME_ITALIC,
            boldItalic=CHINESE_FONT_NAME_BI,
        )

        print(f"[OK] 成功注册中文字体: {regular_path}")
        return CHINESE_FONT_NAME

    print("[WARN] 未找到可用中文字体，中文可能无法正常显示。")
    return None


# ──────────────────────────────────────────────
#  页面 / 对齐 工具函数
# ──────────────────────────────────────────────
def get_page_size(size_name):
    sizes = {'letter': letter, 'a4': A4, 'legal': legal}
    return sizes.get(size_name.lower(), A4)


def get_alignment(align_name):
    alignments = {
        'left': TA_LEFT, 'center': TA_CENTER,
        'right': TA_RIGHT, 'justify': TA_JUSTIFY,
    }
    return alignments.get(align_name.lower(), TA_LEFT)


# ──────────────────────────────────────────────
#  修复 2 — 样式创建始终携带中文字体
# ──────────────────────────────────────────────
def create_paragraph_style(font_config, alignment='left', chinese_font=None):
    """Create a ParagraphStyle; always prefer the registered Chinese font."""
    style = ParagraphStyle('custom')

    # ── 字体名 ──
    if chinese_font:
        style.fontName = chinese_font          # 默认用中文字体
    if font_config and 'name' in font_config:
        requested = font_config['name']
        # 仅当明确指定了标准西文字体时才替换
        standard_western = {
            'Helvetica', 'Helvetica-Bold',
            'Times-Roman', 'Times-Bold',
            'Courier', 'Courier-Bold',
        }
        if requested in standard_western:
            style.fontName = requested
        elif chinese_font:
            style.fontName = chinese_font
        else:
            style.fontName = requested

    # ── 字号 & 行高 ──
    if font_config and 'size' in font_config:
        style.fontSize = font_config['size']
        style.leading = font_config['size'] * 1.4   # 中文适当加大行距
    else:
        style.leading = style.fontSize * 1.4

    # ── 颜色 ──
    if font_config and 'color' in font_config:
        style.textColor = hex_to_color(font_config['color'])

    style.alignment = get_alignment(alignment)
    return style


# ──────────────────────────────────────────────
#  修复 3 — 富文本标签显式指定 fontName
#  避免 <b> 让 reportlab 去猜 bold 字体名
# ──────────────────────────────────────────────
def _wrap_rich_text(text, font_config, chinese_font):
    """
    给 text 加上 <b>/<i>/<u> 标签，
    并在最外层包一个 <font face="..."> 确保字体不丢失。
    """
    if font_config.get('bold'):
        text = f'<b>{text}</b>'
    if font_config.get('italic'):
        text = f'<i>{text}</i>'
    if font_config.get('underline'):
        text = f'<u>{text}</u>'

    # 关键：用 <font> 包裹，保证渲染时使用注册过的中文字体
    if chinese_font:
        text = f'<font face="{chinese_font}">{text}</font>'

    return text


# ──────────────────────────────────────────────
#  内容元素构建
# ──────────────────────────────────────────────
def add_text(content_item, styles, chinese_font=None):
    font_config = content_item.get('font', {})
    alignment = content_item.get('alignment', 'left')
    style = create_paragraph_style(font_config, alignment, chinese_font)

    text = content_item['text']
    text = _wrap_rich_text(text, font_config, chinese_font)

    return Paragraph(text, style)


def add_paragraph(content_item, styles, chinese_font=None):
    return add_text(content_item, styles, chinese_font)


def add_heading(content_item, styles, chinese_font=None):
    level = content_item.get('level', 1)
    font_config = content_item.get('font', {})

    default_sizes = {1: 24, 2: 20, 3: 16, 4: 14, 5: 12, 6: 11}
    font_config.setdefault('size', default_sizes.get(level, 14))
    font_config.setdefault('bold', True)

    style = create_paragraph_style(
        font_config,
        content_item.get('alignment', 'left'),
        chinese_font,
    )

    text = content_item['text']
    text = _wrap_rich_text(text, font_config, chinese_font)

    return Paragraph(text, style)


def add_table(content_item, chinese_font=None):
    data = content_item['data']

    # ── 所有单元格包装成 Paragraph 以支持中文 ──
    if chinese_font:
        cell_style = ParagraphStyle('table_cell')
        cell_style.fontName = chinese_font
        cell_style.fontSize = 10
        cell_style.leading = 14
        cell_style.wordWrap = 'CJK'       # 中日韩自动换行

        formatted_data = []
        for row in data:
            formatted_row = []
            for cell in row:
                cell_text = str(cell) if cell else ''
                # 保留 <font> 包裹
                cell_text = f'<font face="{chinese_font}">{cell_text}</font>'
                formatted_row.append(Paragraph(cell_text, cell_style))
            formatted_data.append(formatted_row)
        data = formatted_data

    table = Table(data)

    table_style_commands = [
        ('GRID',   (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]

    if chinese_font:
        table_style_commands.append(
            ('FONTNAME', (0, 0), (-1, -1), chinese_font)
        )

    if 'style' in content_item:
        style_config = content_item['style']
        if 'header_row' in style_config:
            hi = style_config['header_row']
            table_style_commands.extend([
                ('BACKGROUND', (0, hi), (-1, hi), colors.grey),
                ('TEXTCOLOR',  (0, hi), (-1, hi), colors.whitesmoke),
            ])
            if chinese_font:
                table_style_commands.append(
                    ('FONTNAME', (0, hi), (-1, hi), chinese_font)
                )
        if 'cell_backgrounds' in style_config:
            for cell_ref, color in style_config['cell_backgrounds'].items():
                row, col = map(int, cell_ref.split(','))
                table_style_commands.append(
                    ('BACKGROUND', (col, row), (col, row), hex_to_color(color))
                )

    table.setStyle(TableStyle(table_style_commands))
    return table


def add_image(content_item):
    image_path = content_item['path']
    width = content_item.get('width', 3) * inch
    height = content_item.get('height')
    if height:
        return Image(image_path, width=width, height=height * inch)
    return Image(image_path, width=width)


def add_list(content_item, styles, chinese_font=None):
    items = content_item['items']
    list_type = content_item.get('type', 'bullet')
    font_config = content_item.get('font', {})

    style = create_paragraph_style(font_config, 'left', chinese_font)

    elements = []
    for i, item in enumerate(items, start=1):
        prefix = '•' if list_type == 'bullet' else f'{i}.'
        text = f'{prefix} {item}'
        if chinese_font:
            text = f'<font face="{chinese_font}">{text}</font>'
        elements.append(Paragraph(text, style))
        elements.append(Spacer(1, 0.1 * inch))

    return elements


# ──────────────────────────────────────────────
#  主生成流程
# ──────────────────────────────────────────────
def generate_pdf_document(config, output_path):
    chinese_font = register_chinese_fonts()

    page_setup = config.get('page_setup', {})
    page_size = get_page_size(page_setup.get('size', 'A4'))

    margins = page_setup.get('margins', {})
    left_margin   = margins.get('left',   20) * mm
    right_margin  = margins.get('right',  20) * mm
    top_margin    = margins.get('top',    20) * mm
    bottom_margin = margins.get('bottom', 20) * mm

    doc = SimpleDocTemplate(
        output_path,
        pagesize=page_size,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin,
    )

    story = []
    styles = getSampleStyleSheet()

    for item in config.get('content', []):
        t = item['type']
        if t == 'heading':
            story.append(add_heading(item, styles, chinese_font))
            story.append(Spacer(1, 0.2 * inch))
        elif t in ('text', 'paragraph'):
            story.append(add_paragraph(item, styles, chinese_font))
            story.append(Spacer(1, 0.1 * inch))
        elif t == 'table':
            story.append(add_table(item, chinese_font))
            story.append(Spacer(1, 0.2 * inch))
        elif t == 'image':
            story.append(add_image(item))
            story.append(Spacer(1, 0.2 * inch))
        elif t == 'list':
            story.extend(add_list(item, styles, chinese_font))
        elif t == 'page_break':
            story.append(PageBreak())
        elif t == 'spacer':
            story.append(Spacer(1, item.get('height', 0.5) * inch))

    doc.build(story)
    print(f"PDF document generated: {output_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_pdf.py <config.json> <output.pdf>")
        sys.exit(1)

    config_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        generate_pdf_document(config, output_path)
    except Exception as e:
        print(f"Error generating PDF document: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()