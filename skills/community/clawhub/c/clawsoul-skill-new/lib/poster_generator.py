"""
ClawSoul Poster Generator
赛博身份海报生成器 - 基础版 + Pro 版
"""

import base64
import io
import json
import random
import hashlib
from pathlib import Path

from typing import Optional, Union

# 尝试导入图片库
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False


# MBTI 配色方案
MBTI_COLORS = {
    'ISTJ': {'primary': '#4A90D9', 'secondary': '#2E5C8A', 'accent': '#1E3A5F'},
    'ISFJ': {'primary': '#7B68EE', 'secondary': '#5B4BB9', 'accent': '#3B2B89'},
    'INFJ': {'primary': '#9370DB', 'secondary': '#6B4DAB', 'accent': '#4B2D7B'},
    'INTJ': {'primary': '#4169E1', 'secondary': '#2A49B1', 'accent': '#1A2981'},
    'ISTP': {'primary': '#20B2AA', 'secondary': '#008B8B', 'accent': '#006B6B'},
    'ISFP': {'primary': '#FF69B4', 'secondary': '#DB4B9B', 'accent': '#AB2B7B'},
    'INFP': {'primary': '#DDA0DD', 'secondary': '#AD70AD', 'accent': '#7D407D'},
    'INTP': {'primary': '#6495ED', 'secondary': '#4475CD', 'accent': '#2455AD'},
    'ESTP': {'primary': '#FF4500', 'secondary': '#DB2500', 'accent': '#AB0500'},
    'ESFP': {'primary': '#FF6347', 'secondary': '#DB4337', 'accent': '#AB2327'},
    'ENFP': {'primary': '#FFD700', 'secondary': '#DBB700', 'accent': '#AB9700'},
    'ENTP': {'primary': '#00CED1', 'secondary': '#00ADAD', 'accent': '#008D8D'},
    'ESTJ': {'primary': '#DAA520', 'secondary': '#AA8500', 'accent': '#7A6500'},
    'ESFJ': {'primary': '#F08080', 'secondary': '#D05050', 'accent': '#A02020'},
    'ENFJ': {'primary': '#32CD32', 'secondary': '#22AD22', 'accent': '#128D12'},
    'ENTJ': {'primary': '#DC143C', 'secondary': '#AC032C', 'accent': '#7C021C'},
}


def generate_binary_texture(width: int = 50, height: int = 30) -> str:
    """生成二进制背景纹理"""
    return ''.join(random.choice(['0', '1']) for _ in range(width * height))


def generate_hash(length: int = 8) -> str:
    """生成随机哈希"""
    random_data = str(random.random()).encode()
    return hashlib.md5(random_data).hexdigest()[:length].upper()


def generate_genesis_id() -> str:
    """生成 Genesis ID"""
    return f"0x{generate_hash(8)}"


def generate_qr_code(data: str, size: int = 150) -> Optional[Image.Image]:
    """生成二维码"""
    if not QRCODE_AVAILABLE:
        return None
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").resize((size, size))


def create_poster(
    mbti: str,
    is_pro: bool = False,
    token: str = None,
    website: str = "clawsoul.net"
) -> Optional[bytes]:
    """
    生成赛博身份海报
    
    Args:
        mbti: MBTI 类型 (如 "INTJ")
        is_pro: 是否为 Pro 版
        token: Pro 版的 Token
        website: 网站链接
    
    Returns:
        PNG 图片的 bytes，或 None (如果库不可用)
    """
    if not PIL_AVAILABLE:
        return None
    
    # 获取配色
    colors = MBTI_COLORS.get(mbti, MBTI_COLORS['INTJ'])
    
    # 创建画布
    width, height = 600, 800
    img = Image.new('RGB', (width, height), color='#0a0a0f')
    draw = ImageDraw.Draw(img)
    
    # 二进制背景
    binary_bg = generate_binary_texture(60, 40)
    for i, char in enumerate(binary_bg):
        x = (i % 60) * 10
        y = (i // 60) * 20
        if char == '1':
            draw.text((x, y), char, fill=(40, 40, 50))
    
    # 标题栏
    if is_pro:
        draw.rectangle([(0, 0), (width, 60)], fill=colors['primary'])
        draw.text((20, 20), "GENESIS AWAKENER PROTOCOL", fill='white')
    else:
        draw.text((20, 20), "SOUL AWAKENED", fill=colors['primary'])
    
    # HASH 和 NODE
    genesis_id = generate_genesis_id()
    draw.text((20, 70), f"HASH: {genesis_id}", fill=(180, 180, 180))
    draw.text((300, 70), f"NODE: {genesis_id[:6]}", fill=(180, 180, 180))
    
    # 字体设置 - 使用 Helvetica
    font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
    font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    
    # 绘制 MBTI
    mbti_bbox = draw.textbbox((0, 0), mbti, font=font_large)
    mbti_width = mbti_bbox[2] - mbti_bbox[0]
    draw.text(((width - mbti_width) // 2, 180), mbti, fill=colors['primary'])
    
    # 副标题
    subtitle = "Soul Awakens" if not is_pro else "Genesis Protocol"
    sub_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
    sub_width = sub_bbox[2] - sub_bbox[0]
    draw.text(((width - sub_width) // 2, 280), subtitle, fill=(150, 150, 150))
    
    # 赛博风格装饰文字 - 使用亮色
    draw.text((50, 320), "━" * 25, fill=(0, 255, 255))  # 青色
    draw.text((50, 360), f"// Soul Artifact Generated", fill=(200, 200, 200))  # 亮灰
    draw.text((50, 380), f"// MBTI: {mbti} | Level: {'PRO' if is_pro else 'BASIC'}", fill=(200, 200, 200))
    draw.text((50, 400), "━" * 25, fill=(255, 0, 255))  # 粉色
    
    # 二维码 - 基础版和Pro版都用同一个链接
    qr = generate_qr_code(website)
    if qr:
        img.paste(qr, (width - 180, height - 180))
    
    # 底部信息
    draw.text((50, height - 80), f"Scan to meet my soul", fill=(80, 80, 80))
    draw.text((50, height - 55), website, fill=colors['secondary'])
    
    # 保存为 bytes
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


def get_mbti_dimensions(mbti: str) -> list:
    """获取 MBTI 维度描述"""
    dimensions = {
        'E': 'Extraversion', 'I': 'Introversion',
        'S': 'Sensing', 'N': 'Intuition',
        'T': 'Thinking', 'F': 'Feeling',
        'J': 'Judging', 'P': 'Perceiving'
    }
    
    result = []
    for i, letter in enumerate(mbti):
        dim_name = ['EI', 'SN', 'TF', 'JP'][i]
        result.append(f"{dim_name}: {dimensions.get(letter, '')}")
    return result


def poster_to_base64(poster_bytes: bytes) -> str:
    """将海报转换为 Base64"""
    return base64.b64encode(poster_bytes).decode('utf-8')
