# -*- coding: utf-8 -*-
"""从纯文本脚本生成幻灯片图片"""

import argparse
import os
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    """获取可用字体"""
    font_paths = {
        'title': "C:\\Windows\\Fonts\\msyh.ttc",
        'subtitle': "C:\\Windows\\Fonts\\msyh.ttc",
        'body': "C:\\Windows\\Fonts\\msyh.ttc",
        'small': "C:\\Windows\\Fonts\\msyh.ttc",
    }
    
    fonts = {}
    for name, path in font_paths.items():
        try:
            fonts[name] = ImageFont.truetype(path, {
                'title': 72, 'subtitle': 40, 'body': 32, 'small': 24
            }[name])
        except:
            fonts[name] = ImageFont.load_default()
    
    return fonts

def parse_script(script_text):
    """解析脚本文本，提取幻灯片"""
    slides = []
    current_slide = {"title": "", "content": []}
    
    for line in script_text.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            if current_slide["title"] or current_slide["content"]:
                slides.append(current_slide)
            current_slide = {"title": line[2:], "content": []}
        elif line:
            current_slide["content"].append(line)
    
    if current_slide["title"] or current_slide["content"]:
        slides.append(current_slide)
    
    return slides

def create_slide_image(slide, fonts, width=1920, height=1080):
    """创建单张幻灯片图片"""
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 颜色
    DARK_BLUE = (0, 51, 102)
    PRIMARY_BLUE = (0, 102, 255)
    WHITE = (255, 255, 255)
    DARK_TEXT = (51, 51, 51)
    
    # 顶部装饰条
    draw.rectangle([0, 0, width, 120], fill=DARK_BLUE)
    
    # 标题
    draw.text((60, 40), slide["title"], font=fonts['title'], fill=WHITE)
    
    # 内容
    y = 180
    for item in slide["content"]:
        if item:
            draw.text((80, y), item, font=fonts['body'], fill=DARK_TEXT)
        y += 55
    
    return img

def main():
    parser = argparse.ArgumentParser(description='从文本脚本生成幻灯片图片')
    parser.add_argument('input', help='输入脚本文件路径')
    parser.add_argument('output_dir', help='输出目录')
    parser.add_argument('--width', type=int, default=1920, help='图片宽度')
    parser.add_argument('--height', type=int, default=1080, help='图片高度')
    
    args = parser.parse_args()
    
    # 读取脚本
    with open(args.input, 'r', encoding='utf-8') as f:
        script_text = f.read()
    
    # 解析幻灯片
    slides = parse_script(script_text)
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 获取字体
    fonts = get_fonts()
    
    # 生成图片
    for i, slide in enumerate(slides):
        img = create_slide_image(slide, fonts, args.width, args.height)
        filepath = os.path.join(args.output_dir, f"slide_{i+1:02d}.png")
        img.save(filepath, "PNG")
        print(f"已生成: slide_{i+1:02d}.png")
    
    print(f"\n共生成 {len(slides)} 张幻灯片")

if __name__ == "__main__":
    main()