"""PIL 字幕渲染 — 底部定位，无背景带"""
import textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def render_text_overlay(text, width=1920, height=1080, font_path=None, font_size=44,
                        y_ratio=0.85, max_chars=20, sub_color=(255, 255, 255)):
    """渲染文字叠加层 → numpy RGBA 数组 (透明背景 + 白字 + 阴影)

    y_ratio: 底部锚点位置（屏幕高度的比例），默认 0.85。
             单行文字居中于该位置；多行文字从该位置向上扩展。
    """
    if not font_path:
        font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)

    lines = textwrap.wrap(text, width=max_chars) if len(text) > max_chars else [text]
    line_height = font_size + 12
    total_text_height = len(lines) * line_height

    # 底部锚定：文字块底部在 y_ratio 位置，多行向上扩展
    text_bottom_y = int(height * y_ratio)
    y_start = text_bottom_y - total_text_height

    # 文字 + 描边（两遍阴影实现描边效果，替代渐变暗带）
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (width - tw) // 2
        y = y_start + i * line_height
        # 描边（4 方向偏移，增强可读性）
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            draw.text((x + dx, y + dy), line, fill=(0, 0, 0, 220), font=font)
        # 正文
        draw.text((x, y), line, fill=sub_color + (255,), font=font)

    return np.array(img)


def prerender_subtitles(subs, width, height, font_path, font_size, y_ratio, max_chars):
    """预渲染所有字幕叠加层 → dict{text: PIL.Image}"""
    from PIL import Image as _PILImage
    text_overlays = {}
    for s in subs:
        if s["text"] not in text_overlays:
            arr = render_text_overlay(
                s["text"], width, height, font_path, font_size, y_ratio, max_chars)
            text_overlays[s["text"]] = _PILImage.fromarray(arr, 'RGBA')
    return text_overlays
