# -*- coding: utf-8 -*-
"""
ffmpeg Chinese Subtitle Module
Windows 上正确处理中文字幕的解决方案

使用 Pillow 在图片上绘制字幕，避免 ffmpeg 编码问题
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Optional
import os


def add_subtitle_to_image(
    image_path: str,
    subtitle_text: str,
    output_path: str,
    font_size: int = 24,
    y_offset: int = 50,
    font_color: Tuple[int, int, int] = (255, 255, 255),
    shadow_color: Tuple[int, int, int] = (0, 0, 0),
    shadow_radius: int = 2,
    font_path: Optional[str] = None
) -> str:
    """
    在图片上添加中文字幕
    
    Args:
        image_path: 输入图片路径
        subtitle_text: 字幕文本
        output_path: 输出图片路径
        font_size: 字体大小（默认 24）
        y_offset: 距底部的偏移量（默认 50 像素）
        font_color: 字体颜色 RGB（默认白色）
        shadow_color: 阴影颜色 RGB（默认黑色）
        shadow_radius: 阴影半径（默认 2）
        font_path: 自定义字体路径（默认使用系统微软雅黑）
    
    Returns:
        输出图片路径
    """
    # 打开原图
    img = Image.open(image_path)
    width, height = img.size
    
    # 转换为 RGB 模式（如果需要）
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = _load_chinese_font(font_size)
    
    # 计算文本位置（居中）
    bbox = draw.textbbox((0, 0), subtitle_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = height - y_offset - text_height
    
    # 绘制阴影（描边效果）
    for adj_x in range(-shadow_radius, shadow_radius + 1):
        for adj_y in range(-shadow_radius, shadow_radius + 1):
            if adj_x != 0 or adj_y != 0:
                draw.text((x + adj_x, y + adj_y), subtitle_text, font=font, fill=shadow_color)
    
    # 绘制文字
    draw.text((x, y), subtitle_text, font=font, fill=font_color)
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    # 保存
    img.save(output_path, "PNG")
    
    return output_path


def _load_chinese_font(font_size: int) -> ImageFont.FreeTypeFont:
    """
    加载中文字体
    
    优先级：
    1. 微软雅黑 (msyh.ttc)
    2. 黑体 (simhei.ttf)
    3. 宋体 (simsun.ttc)
    4. 默认字体
    """
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",      # 微软雅黑
        "C:/Windows/Fonts/simhei.ttf",    # 黑体
        "C:/Windows/Fonts/simsun.ttc",    # 宋体
        "/System/Library/Fonts/PingFang.ttc",  # macOS
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",  # Linux
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, font_size)
            except:
                continue
    
    # 使用默认字体
    return ImageFont.load_default()


def wrap_text(text: str, max_chars: int = 20) -> str:
    """
    文本自动换行
    
    Args:
        text: 原文本
        max_chars: 每行最大字符数
    
    Returns:
        换行后的文本
    """
    lines = []
    current = ""
    
    for char in text:
        current += char
        if len(current) >= max_chars:
            lines.append(current)
            current = ""
    
    if current:
        lines.append(current)
    
    return "\n".join(lines)


# 示例用法
if __name__ == "__main__":
    # 示例：在图片上添加字幕
    add_subtitle_to_image(
        image_path="input.png",
        subtitle_text="这是中文字幕示例",
        output_path="output.png"
    )
    print("字幕添加完成！")
