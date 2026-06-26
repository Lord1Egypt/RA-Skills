#!/usr/bin/env python3
"""cn-image-watermark - 图片水印工具"""
import sys

def add_text_watermark(image_path, text, position='右下', opacity=128):
    """添加文字水印
    
    使用PIL库添加文字水印到图片
    
    Args:
        image_path: 图片路径
        text: 水印文字
        position: 位置（右下/左下/右上/左上/居中）
        opacity: 透明度 0-255
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return {"success": False, "error": "需要安装Pillow: pip install Pillow"}
    
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        w, h = img.size
        
        # 字体大小
        font_size = max(20, min(w, h) // 20)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", font_size)
        except:
            font = ImageFont.load_default()
        
        # 水印位置
        text_w = font_size * len(text) * 0.6
        text_h = font_size * 1.2
        
        positions = {
            '右下': (w - text_w - 10, h - text_h - 10),
            '左下': (10, h - text_h - 10),
            '右上': (w - text_w - 10, 10),
            '左上': (10, 10),
            '居中': ((w - text_w) / 2, (h - text_h) / 2),
        }
        pos = positions.get(position, positions['右下'])
        
        # 绘制水印
        draw.text(pos, text, fill=(255, 255, 255, opacity), font=font)
        
        output = image_path.rsplit('.', 1)[0] + '_watermarked.png'
        img.save(output)
        return {"success": True, "output": output}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python image_watermark.py <图片路径> <水印文字> [位置]")
    else:
        pos = sys.argv[3] if len(sys.argv) > 3 else '右下'
        result = add_text_watermark(sys.argv[1], sys.argv[2], pos)
        print(result)
