#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCY 文本转图片工具
使用 Pillow 将文本转换为 PNG/JPEG 图片。

修复要点：
- 保留显式换行，不再把中文整段挤成一行
- 支持无空格中文/长英文的按宽度换行
- 字体加载逻辑集中复用，供 smart_draw 内存渲染文字图层使用
"""

from __future__ import annotations

import os
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


DEFAULT_FONT_CANDIDATES = [
    # Windows 中文字体
    "simhei.ttf",
    "simsun.ttc",
    "msyh.ttf",
    # macOS 中文字体
    "PingFang.ttc",
    "Hiragino Sans GB W3.otf",
    # Linux 中文字体
    "wqy-zenhei.ttc",
    "NotoSansCJK-Regular.ttc",
    "NotoSansCJK-Regular.otf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    # 英文字体后备
    "DejaVuSans.ttf",
    "arial.ttf",
]


def load_font(font_size: int = 16, font_path: Optional[str] = None, verbose: bool = False):
    """加载可用字体；优先使用显式 font_path，其次尝试常见中英文字体。"""
    try:
        if font_path:
            expanded = os.path.expanduser(font_path)
            if os.path.exists(expanded):
                return ImageFont.truetype(expanded, font_size)
            # 允许传 Pillow/fontconfig 可解析的字体名
            return ImageFont.truetype(font_path, font_size)
    except Exception as exc:
        if verbose:
            print(f"字体加载失败: {exc}，尝试系统字体")

    for font_name in DEFAULT_FONT_CANDIDATES:
        try:
            font = ImageFont.truetype(font_name, font_size)
            if verbose:
                print(f"使用字体: {font_name}")
            return font
        except Exception:
            continue

    if verbose:
        print("使用默认字体（可能不支持中文）")
    return ImageFont.load_default()


def detect_format(output_path: str, fmt: Optional[str] = None) -> str:
    if fmt:
        fmt = fmt.upper()
        return "JPEG" if fmt in {"JPG", "JPEG"} else "PNG"
    ext = os.path.splitext(output_path.lower())[1]
    return "JPEG" if ext in [".jpg", ".jpeg"] else "PNG"


def text_to_image(
    text,
    output_path,
    font_size=16,
    text_color="#000000",
    background_color="#ffffff",
    width=800,
    height=600,
    font_path=None,
    padding=20,
    format=None,
    align="center",
    valign="middle",
    verbose=True,
):
    """
    将文本转换为图片。

    Args:
        text (str): 要转换的文本内容
        output_path (str): 输出图片路径
        font_size (int): 字体大小
        text_color (str): 文本颜色，支持 #RGB / #RRGGBB
        background_color (str): 背景颜色，或 transparent
        width (int): 图片宽度
        height (int): 图片高度
        font_path (str): 字体文件路径或字体名
        padding (int): 文本边距
        format (str): PNG / JPEG；不传则按扩展名判断
        align (str): left / center / right
        valign (str): top / middle / bottom
        verbose (bool): 是否打印字体与保存信息
    """
    image = render_text_image(
        text=str(text),
        font_size=font_size,
        text_color=text_color,
        background_color=background_color,
        width=width,
        height=height,
        font_path=font_path,
        padding=padding,
        align=align,
        valign=valign,
        verbose=verbose,
    )

    fmt = detect_format(output_path, format)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)

    if fmt == "JPEG":
        if image.mode == "RGBA":
            rgb_image = Image.new("RGB", image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[-1])
            rgb_image.save(output_path, format="JPEG")
        else:
            image.convert("RGB").save(output_path, format="JPEG")
    else:
        image.save(output_path, format="PNG")

    if verbose:
        print(f"图片已保存至: {output_path} (格式: {fmt})")
    return output_path


def render_text_image(
    text: str,
    font_size=16,
    text_color="#000000",
    background_color="#ffffff",
    width=800,
    height=600,
    font_path=None,
    padding=20,
    align="center",
    valign="middle",
    line_spacing=4,
    verbose=False,
):
    """在内存中渲染文字图片，供 text_to_image 和 smart_draw 复用。"""
    transparent = str(background_color).lower() == "transparent"
    mode = "RGBA" if transparent else "RGB"
    bg_color = (255, 255, 255, 0) if transparent else _hex_to_rgb(background_color)
    image = Image.new(mode, (int(width), int(height)), bg_color)
    draw = ImageDraw.Draw(image)
    font = load_font(int(font_size), font_path=font_path, verbose=verbose)

    max_width = max(1, int(width) - 2 * int(padding))
    lines = _wrap_text(str(text), font, max_width, draw)

    line_heights = []
    line_widths = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line or " ", font=font)
        line_widths.append(bbox[2] - bbox[0])
        line_heights.append(max(1, bbox[3] - bbox[1]))

    total_text_height = sum(line_heights) + max(0, len(lines) - 1) * int(line_spacing)
    if valign == "top":
        y = int(padding)
    elif valign == "bottom":
        y = max(int(padding), int(height) - int(padding) - total_text_height)
    else:
        y = max(int(padding), (int(height) - total_text_height) // 2)

    fill = _hex_to_rgb(text_color)
    for line, line_width, line_height in zip(lines, line_widths, line_heights):
        if align == "left":
            x = int(padding)
        elif align == "right":
            x = max(int(padding), int(width) - int(padding) - line_width)
        else:
            x = max(int(padding), (int(width) - line_width) // 2)
        draw.text((x, y), line, fill=fill, font=font)
        y += line_height + int(line_spacing)
    return image


def _text_width(text: str, font, draw) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def _wrap_long_token(token: str, font, max_width: int, draw):
    """处理无空格中文或超长英文 token。"""
    if _text_width(token, font, draw) <= max_width:
        return [token]
    out = []
    current = ""
    for ch in token:
        test = current + ch
        if current and _text_width(test, font, draw) > max_width:
            out.append(current)
            current = ch
        else:
            current = test
    if current:
        out.append(current)
    return out or [""]


def _wrap_paragraph(paragraph: str, font, max_width: int, draw):
    if paragraph == "":
        return [""]

    # 含空格的英文/混排按词优先；无空格中文按字符切分。
    raw_tokens = paragraph.split(" ") if " " in paragraph else list(paragraph)
    lines = []
    current = ""

    for token in raw_tokens:
        if token == "" and " " in paragraph:
            token = " "
        pieces = _wrap_long_token(token, font, max_width, draw)
        for piece in pieces:
            joiner = " " if current and " " in paragraph and piece != " " else ""
            test = f"{current}{joiner}{piece}" if current else piece
            if current and _text_width(test, font, draw) > max_width:
                lines.append(current)
                current = piece
            else:
                current = test
    if current or not lines:
        lines.append(current)
    return lines


def _wrap_text(text, font, max_width, draw):
    """自动换行；保留用户输入的显式换行。"""
    lines = []
    for paragraph in str(text).splitlines() or [""]:
        lines.extend(_wrap_paragraph(paragraph, font, max_width, draw))
    return lines or [""]


def _hex_to_rgb(hex_color):
    """将十六进制颜色转换为 RGB 元组。"""
    if isinstance(hex_color, tuple):
        return hex_color
    value = str(hex_color).strip().lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    if len(value) != 6:
        raise ValueError(f"无效颜色值: {hex_color}")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def create_code_image(code, output_path, language=None, theme="default", format=None):
    """创建简易代码图片。"""
    themes = {
        "default": {"background": "#f8f8f8", "text": "#333333", "font_size": 14},
        "dark": {"background": "#2d2d2d", "text": "#ffffff", "font_size": 14},
        "github": {"background": "#ffffff", "text": "#24292e", "font_size": 14},
    }
    theme_colors = themes.get(theme, themes["default"])

    lines = str(code).split("\n")
    max_line_length = max((len(line) for line in lines), default=50)
    width = min(max(max_line_length * max(8, theme_colors["font_size"] // 2) + 40, 320), 1600)
    height = max(80, len(lines) * (theme_colors["font_size"] + 8) + 40)

    return text_to_image(
        text=code,
        output_path=output_path,
        font_size=theme_colors["font_size"],
        text_color=theme_colors["text"],
        background_color=theme_colors["background"],
        width=width,
        height=height,
        padding=20,
        format=format,
        align="left",
    )


if __name__ == "__main__":
    sample_text = "这是一个示例文本\n用于演示文本转图片功能\n支持多行文本显示"
    text_to_image(sample_text, "sample.png")
    text_to_image(
        "自定义样式示例",
        "custom.png",
        font_size=24,
        text_color="#ff6b6b",
        background_color="#4ecdc4",
        width=600,
        height=300,
    )
    sample_code = """def hello_world():
    print("Hello, World!")
    return True"""
    create_code_image(sample_code, "code_sample.png", theme="github")
    text_to_image("JPG格式测试", "sample_jpg.jpg", format="JPEG")
