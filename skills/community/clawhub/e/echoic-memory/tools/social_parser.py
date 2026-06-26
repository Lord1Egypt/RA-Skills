#!/usr/bin/env python3
"""
社交媒体内容解析器
从截图中提取文字内容
"""

import argparse
import json
import sys
from pathlib import Path


def parse_text_from_image(image_path):
    """从图片中提取文字（需要 OCR）"""
    # 注意：这里需要 OCR 库，如 pytesseract
    # 为简化，这里提供一个框架，实际使用时需要安装 tesseract
    try:
        # import pytesseract
        # from PIL import Image
        # img = Image.open(image_path)
        # text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        # return text
        return None  # 占位，实际实现需要 OCR
    except ImportError:
        return None


def analyze_screenshot(image_path):
    """分析单张截图"""
    result = {
        'filename': image_path.name,
        'size': None,
        'extracted_text': None
    }
    
    try:
        from PIL import Image
        img = Image.open(image_path)
        result['size'] = img.size
        
        # 尝试 OCR（如果有的话）
        text = parse_text_from_image(image_path)
        if text:
            result['extracted_text'] = text
            
    except Exception as e:
        result['error'] = str(e)
    
    return result


def extract_posting_patterns(texts):
    """从提取的文字中分析发帖模式"""
    patterns = {
        'posting_times': [],
        'common_topics': [],
        'emoji_usage': [],
        'writing_style': []
    }
    
    # 这里可以添加更复杂的文本分析
    # 简单示例：提取时间模式
    import re
    for text in texts:
        if text:
            # 提取时间戳
            times = re.findall(r'(\d{1,2}):(\d{2})', text)
            patterns['posting_times'].extend([f"{h}:{m}" for h, m in times])
    
    return patterns


def main():
    parser = argparse.ArgumentParser(description='解析社交媒体截图')
    parser.add_argument('--dir', required=True, help='截图目录路径')
    parser.add_argument('--output', required=True, help='输出文件路径')
    
    args = parser.parse_args()
    
    screenshot_dir = Path(args.dir)
    if not screenshot_dir.exists():
        print(f"Error: Directory not found: {screenshot_dir}", file=sys.stderr)
        sys.exit(1)
    
    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png'}
    
    # 分析所有截图
    screenshots = []
    all_texts = []
    
    for ext in image_extensions:
        for img_path in screenshot_dir.rglob(f'*{ext}'):
            result = analyze_screenshot(img_path)
            screenshots.append(result)
            if result.get('extracted_text'):
                all_texts.append(result['extracted_text'])
    
    # 分析发帖模式
    patterns = extract_posting_patterns(all_texts)
    
    # 输出
    output = {
        'directory': str(screenshot_dir),
        'screenshot_count': len(screenshots),
        'screenshots_with_ocr': len(all_texts),
        'patterns': patterns,
        'screenshots': screenshots[:30]  # 限制输出数量
    }
    
    # 如果没有 OCR，添加提示
    if not all_texts:
        output['note'] = 'OCR not available. Install pytesseract and tesseract OCR to extract text from images.'
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"分析完成: {len(screenshots)} 张截图")
    print(f"  成功 OCR: {len(all_texts)}")
    print(f"输出文件: {args.output}")
    
    if not all_texts:
        print("\n提示: 如需 OCR 功能，请安装:")
        print("  pip install pytesseract pillow")
        print("  并安装 tesseract OCR 引擎")


if __name__ == '__main__':
    main()
