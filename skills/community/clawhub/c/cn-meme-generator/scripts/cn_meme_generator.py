#!/usr/bin/env python3
"""
cn-meme-generator - 表情包生成器
支持文字叠加和AI生成两种模式
"""
import argparse
import urllib.parse
import requests
from PIL import Image, ImageDraw, ImageFont
import os
import math

# 表情包配色方案
COLORS = {
    'yellow': (255, 217, 61),
    'blue': (66, 133, 244),
    'red': (234, 67, 53),
    'green': (52, 168, 83),
    'purple': (103, 58, 183),
    'orange': (255, 152, 0),
    'pink': (233, 30, 99),
    'dark': (30, 30, 30),
}

def draw_meme_text(top_text, bottom_text, bg_color='yellow', output='meme_output.png'):
    """绘制文字表情包"""
    # 预设背景颜色或渐变
    colors = COLORS.get(bg_color, COLORS['yellow'])
    
    # 图片尺寸
    width, height = 500, 500
    
    # 创建图片
    img = Image.new('RGB', (width, height), colors)
    draw = ImageDraw.Draw(img)
    
    # 尝试加载中文字体
    font_paths = [
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
        None
    ]
    
    font = None
    for path in font_paths:
        if path and os.path.exists(path):
            try:
                font = ImageFont.truetype(path, 48)
                break
            except:
                continue
    
    if font is None:
        font = ImageFont.load_default()
    
    # 绘制顶部文字
    if top_text:
        text = top_text.strip()
        # 自动换行
        lines = wrap_text(text, font, width - 40)
        y = 30
        for line in lines[:3]:  # 最多3行
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            # 黑色描边
            for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                draw.text((x + offset[0], y + offset[1]), line, fill=(0, 0, 0), font=font)
            draw.text((x, y), line, fill=(255, 255, 255), font=font)
            bbox = draw.textbbox((0, 0), line, font=font)
            y += (bbox[3] - bbox[1]) + 8
    
    # 绘制底部文字
    if bottom_text:
        text = bottom_text.strip()
        lines = wrap_text(text, font, width - 40)
        # 从底部往上排
        total_height = 0
        line_heights = []
        for line in lines[:3]:
            bbox = draw.textbbox((0, 0), line, font=font)
            h = bbox[3] - bbox[1]
            line_heights.append(h)
            total_height += h + 8
        
        y = height - total_height - 30
        for i, line in enumerate(lines[:3]):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            # 黑色描边
            for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                draw.text((x + offset[0], y + offset[1]), line, fill=(0, 0, 0), font=font)
            draw.text((x, y), line, fill=(255, 255, 255), font=font)
            y += line_heights[i] + 8
    
    img.save(output)
    print(f"表情包已保存: {output}")
    return output

def wrap_text(text, font, max_width):
    """文字自动换行"""
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph
        if not words:
            lines.append('')
            continue
        
        current = ''
        for char in words:
            test = current + char
            bbox = __import__('PIL').ImageDraw.ImageDraw.textbbox
            # 简单判断
            try:
                test_bbox = __import__('PIL').ImageDraw.ImageDraw.textbbox((0,0), test, font=font)
                if test_bbox[2] - test_bbox[0] <= max_width:
                    current = test
                else:
                    if current:
                        lines.append(current)
                    current = char
            except:
                if len(current) <= 10:
                    current += char
                else:
                    if current:
                        lines.append(current)
                    current = char
        if current:
            lines.append(current)
    
    return lines if lines else ['']

def generate_ai_meme(prompt, output='meme_output.png'):
    """使用Pollinations AI生成表情包"""
    if not prompt:
        print("请提供提示词 --prompt")
        return None
    
    # 调用Pollinations免费API
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed=42&nologo=true"
    
    print(f"正在生成图片: {prompt[:30]}...")
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            with open(output, 'wb') as f:
                f.write(resp.content)
            print(f"AI表情包已保存: {output}")
            return output
        else:
            print(f"生成失败: HTTP {resp.status_code}")
            return None
    except Exception as e:
        print(f"生成失败: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='表情包生成器')
    parser.add_argument('--mode', choices=['text', 'ai'], default='text', help='模式')
    parser.add_argument('--top', default='', help='顶部文字')
    parser.add_argument('--bottom', default='', help='底部文字')
    parser.add_argument('--prompt', default='', help='AI提示词')
    parser.add_argument('--output', default='meme_output.png', help='输出路径')
    parser.add_argument('--color', default='yellow', choices=list(COLORS.keys()), help='背景颜色')
    
    args = parser.parse_args()
    
    if args.mode == 'text':
        draw_meme_text(args.top, args.bottom, args.color, args.output)
    elif args.mode == 'ai':
        generate_ai_meme(args.prompt, args.output)

if __name__ == '__main__':
    main()